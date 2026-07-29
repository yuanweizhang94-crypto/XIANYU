"""Automatic reply service built on the CHG-0009 upstream Wrapper."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Protocol

from xianyu_system.worker.autoreply.config import AutoreplyConfig
from xianyu_system.worker.autoreply.state import AutoreplyState, now_epoch
from xianyu_system.worker.upstream_wrapper.client import UpstreamWrapper, UpstreamWrapperError
from xianyu_system.worker.upstream_wrapper.models import ConfirmedReplyRequest, NormalizedInboundMessage, UpstreamResultState


class Clock(Protocol):
    def __call__(self) -> float: ...


@dataclass(frozen=True)
class AutoreplyStatus:
    running: bool
    config_enabled: bool
    blocked_reason: str | None
    listener_status: str
    backend_healthy: bool
    listener_connected: bool
    account_logged_in: bool
    success_count: int
    skipped_count: int
    failed_count: int
    unknown_count: int


@dataclass(frozen=True)
class ProcessOutcome:
    result: str
    rule_id: str | None
    operation_id: str | None
    reason: str | None = None


SAFETY_TEXT_MARKERS = (
    "验证码",
    "账号安全",
    "风控",
    "退款",
    "投诉",
    "支付",
    "订单",
    "人脸",
    "captcha",
    "verification",
)


def message_key(message: NormalizedInboundMessage) -> str:
    material = "|".join([message.account_ref, message.conversation_ref, message.upstream_message_ref])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _masked(value: str) -> str:
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}...{value[-3:]}"


class AutoreplyService:
    def __init__(
        self,
        config: AutoreplyConfig,
        wrapper: UpstreamWrapper | None = None,
        *,
        clock: Clock = now_epoch,
    ) -> None:
        self.config = config
        self.wrapper = wrapper or UpstreamWrapper()
        self.clock = clock
        self.state = AutoreplyState.load(config.state_dir / "state.json")

    def _automation_enabled_count(self) -> int:
        sql = """
SELECT COUNT(*) FROM xy_scheduled_tasks WHERE enabled=1
UNION ALL SELECT COUNT(*) FROM xy_default_replies WHERE enabled=1
UNION ALL SELECT COUNT(*) FROM xy_confirm_receipt_messages WHERE enabled=1
UNION ALL SELECT COUNT(*) FROM xy_goofish_crawl_jobs WHERE enabled=1
UNION ALL SELECT COUNT(*) FROM xy_notification_channels WHERE enabled=1
UNION ALL SELECT COUNT(*) FROM xy_auto_rate_configs WHERE enabled=1;
"""
        try:
            rows = self.wrapper._query_pilot(sql)  # noqa: SLF001 - CHG-0010 intentionally reuses Wrapper Pilot fallback.
        except UpstreamWrapperError:
            return 1
        total = 0
        for row in rows:
            if row and row[0].isdigit():
                total += int(row[0])
        return total

    def doctor(self) -> AutoreplyStatus:
        blocked: str | None = None
        health = self.wrapper.health()
        listener_status = self.wrapper.listener_status()
        account_logged_in = False
        if not self.config.enabled:
            return AutoreplyStatus(
                running=False,
                config_enabled=False,
                blocked_reason="DISABLED",
                listener_status=listener_status,
                backend_healthy=health.backend_ok,
                listener_connected=health.listener_connected,
                account_logged_in=False,
                success_count=self.state.counters.get("success", 0),
                skipped_count=self.state.counters.get("skipped", 0),
                failed_count=self.state.counters.get("failed", 0),
                unknown_count=self.state.counters.get("unknown", 0),
            )
        try:
            account_logged_in = self.wrapper.account_status().logged_in
        except UpstreamWrapperError:
            blocked = "LOCAL_AUTH_REFRESH_REQUIRED"
        if self.config.enabled and not self.wrapper.config.allow_live_writes:
            blocked = blocked or "LIVE_WRITES_DISABLED"
        if self.config.enabled and self.config.mode != "dedicated-test":
            blocked = blocked or "MODE_NOT_DEDICATED_TEST"
        if self.config.enabled and self._automation_enabled_count() > 0:
            blocked = blocked or "OTHER_AUTOMATION_ENABLED"
        if self.config.enabled and not health.backend_ok:
            blocked = blocked or "UPSTREAM_UNHEALTHY"
        if self.config.enabled and not health.listener_connected:
            blocked = blocked or "LISTENER_DISCONNECTED"
        if self.config.enabled and not account_logged_in:
            blocked = blocked or "LOCAL_AUTH_REFRESH_REQUIRED"
        return AutoreplyStatus(
            running=False,
            config_enabled=self.config.enabled,
            blocked_reason=blocked,
            listener_status=listener_status,
            backend_healthy=health.backend_ok,
            listener_connected=health.listener_connected,
            account_logged_in=account_logged_in,
            success_count=self.state.counters.get("success", 0),
            skipped_count=self.state.counters.get("skipped", 0),
            failed_count=self.state.counters.get("failed", 0),
            unknown_count=self.state.counters.get("unknown", 0),
        )

    def ensure_started(self) -> None:
        if self.state.started_at is None:
            self.state.started_at = self.clock()
        if self.wrapper.listener_status() != "running":
            result = self.wrapper.start_listener()
            if result.state is UpstreamResultState.SUCCESS:
                self.state.listener_owned = True
        existing = self.wrapper.list_recent_inbound_events(limit=100)
        self.state.mark_historical({message_key(event) for event in existing})

    def stop_owned_listener(self) -> None:
        if self.state.listener_owned:
            self.wrapper.stop_listener()
            self.state.listener_owned = False
            self.state.save()

    def _within_hour(self, key_prefix: str) -> int:
        cutoff = self.clock() - 3600
        count = 0
        for key, record in self.state.processed.items():
            if key.startswith(key_prefix) and float(record.get("timestamp") or 0) >= cutoff and record.get("result") == "SUCCESS":
                count += 1
        return count

    def _conversation_cooling_down(self, event: NormalizedInboundMessage) -> bool:
        if self.config.conversation_cooldown_seconds <= 0:
            return False
        conv_prefix = "conv:" + hashlib.sha256(f"{event.account_ref}|{event.conversation_ref}".encode()).hexdigest()
        cutoff = self.clock() - self.config.conversation_cooldown_seconds
        return any(
            key.startswith(conv_prefix)
            and record.get("result") == "SUCCESS"
            and float(record.get("timestamp") or 0) >= cutoff
            for key, record in self.state.processed.items()
        )

    def _rate_limited(self, event: NormalizedInboundMessage) -> bool:
        conv_prefix = "conv:" + hashlib.sha256(f"{event.account_ref}|{event.conversation_ref}".encode()).hexdigest()
        acct_prefix = "acct:" + hashlib.sha256(event.account_ref.encode("utf-8")).hexdigest()
        return (
            self._within_hour(conv_prefix) >= self.config.max_replies_per_conversation_per_hour
            or self._within_hour(acct_prefix) >= self.config.max_replies_per_account_per_hour
        )

    def _record_success_limits(self, event: NormalizedInboundMessage) -> None:
        timestamp = self.clock()
        conv_key = "conv:" + hashlib.sha256(f"{event.account_ref}|{event.conversation_ref}".encode()).hexdigest() + f":{timestamp}"
        acct_key = "acct:" + hashlib.sha256(event.account_ref.encode("utf-8")).hexdigest() + f":{timestamp}"
        self.state.processed[conv_key] = {"result": "SUCCESS", "timestamp": timestamp}
        self.state.processed[acct_key] = {"result": "SUCCESS", "timestamp": timestamp}

    def _skip(self, key: str, reason: str) -> ProcessOutcome:
        self.state.record(key, result="SKIPPED", rule_id=None, operation_id=None)
        return ProcessOutcome("SKIPPED", None, None, reason)

    def process_event(self, event: NormalizedInboundMessage) -> ProcessOutcome:
        key = message_key(event)
        if key in self.state.historical:
            return self._skip(key, "SKIPPED_STARTUP_WATERMARK")
        if self.state.has_blocking_record(key):
            return ProcessOutcome("SKIPPED", None, None, "SKIPPED_IDEMPOTENCY")
        if not self.config.enabled:
            return self._skip(key, "SKIPPED_DISABLED")
        if not self.wrapper.config.allow_live_writes:
            return self._skip(key, "SKIPPED_LIVE_WRITES_DISABLED")
        if event.account_ref not in self.config.account_allowlist:
            return self._skip(key, "SKIPPED_ACCOUNT_NOT_ALLOWLISTED")
        if event.direction.upper() != "INBOUND":
            return self._skip(key, "SKIPPED_OUTBOUND")
        if event.message_type.lower() not in self.config.allowed_message_types:
            return self._skip(key, "SKIPPED_UNSUPPORTED_MESSAGE_TYPE")
        if any(marker.lower() in event.text.lower() for marker in SAFETY_TEXT_MARKERS):
            return self._skip(key, "SKIPPED_UNSUPPORTED_MESSAGE_TYPE")
        if self._conversation_cooling_down(event):
            return self._skip(key, "SKIPPED_RATE_LIMIT")
        if self._rate_limited(event):
            return self._skip(key, "SKIPPED_RATE_LIMIT")
        match = self.config.match_reply(event.text)
        if match is None:
            return self._skip(key, "SKIPPED_NO_RULE")
        rule_id, reply = match
        result = self.wrapper.send_confirmed_reply(ConfirmedReplyRequest(event.internal_message_id, reply, confirm=True))
        mapped = result.state.value
        self.state.record(key, result=mapped, rule_id=rule_id, operation_id=result.operation_id)
        if mapped == "SUCCESS":
            self._record_success_limits(event)
            self.state.save()
        return ProcessOutcome(mapped, rule_id, result.operation_id)

    def poll_once(self, *, limit: int = 100) -> list[ProcessOutcome]:
        self.state.last_poll_at = self.clock()
        self.state.save()
        status = self.doctor()
        if status.blocked_reason:
            return [ProcessOutcome("SKIPPED", None, None, status.blocked_reason)]
        events = self.wrapper.list_recent_inbound_events(limit=limit)
        outcomes: list[ProcessOutcome] = []
        for event in events:
            outcomes.append(self.process_event(event))
        return outcomes

    def write_status(self, *, running: bool, pid: int | None = None) -> None:
        self.config.state_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "running": running,
            "pid": pid,
            "started_at": self.state.started_at,
            "last_poll_at": self.state.last_poll_at,
            "last_success_at": self.state.last_success_at,
            "success_count": self.state.counters.get("success", 0),
            "skipped_count": self.state.counters.get("skipped", 0),
            "failed_count": self.state.counters.get("failed", 0),
            "unknown_count": self.state.counters.get("unknown", 0),
            "listener_owned": self.state.listener_owned,
            "masked_accounts": [_masked(value) for value in self.config.account_allowlist],
        }
        (self.config.state_dir / "status.json").write_text(json.dumps(payload, sort_keys=True), encoding="utf-8", newline="\n")
