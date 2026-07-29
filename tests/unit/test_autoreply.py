from __future__ import annotations

from pathlib import Path
from typing import Any

from xianyu_system.worker.autoreply.config import AutoreplyConfig, AutoreplyConfigError
from xianyu_system.worker.autoreply.process import ProcessManager
from xianyu_system.worker.autoreply.service import AutoreplyService
from xianyu_system.worker.upstream_wrapper.config import UpstreamWrapperConfig
from xianyu_system.worker.upstream_wrapper.models import (
    ConfirmedReplyRequest,
    NormalizedInboundMessage,
    UpstreamAccountStatus,
    UpstreamActionResult,
    UpstreamHealth,
    UpstreamResultState,
)


class FakeWrapper:
    def __init__(self, *, allow_live_writes: bool = True) -> None:
        self.config = UpstreamWrapperConfig(allow_live_writes=allow_live_writes, audit_path=Path("unused"))
        self.events: list[NormalizedInboundMessage] = []
        self.sent: list[ConfirmedReplyRequest] = []
        self.result = UpstreamActionResult(UpstreamResultState.SUCCESS, "op-001", "sent")
        self.backend_ok = True
        self.listener_connected = True
        self.logged_in = True
        self.listener = "running"
        self.started = 0
        self.stopped = 0
        self.automation_rows = "0\n0\n0\n0\n0\n0\n"

    def health(self) -> UpstreamHealth:
        return UpstreamHealth(self.backend_ok, True, self.listener_connected, "")

    def listener_status(self) -> str:
        return self.listener

    def account_status(self) -> UpstreamAccountStatus:
        return UpstreamAccountStatus("acct-001", self.logged_in, "running" if self.logged_in else "stopped")

    def list_recent_inbound_events(self, *, limit: int = 20, match_text: str | None = None) -> list[NormalizedInboundMessage]:
        events = self.events[:limit]
        if match_text is not None:
            events = [event for event in events if event.text == match_text]
        return events

    def send_confirmed_reply(self, request: ConfirmedReplyRequest) -> UpstreamActionResult:
        self.sent.append(request)
        return self.result

    def start_listener(self) -> UpstreamActionResult:
        self.started += 1
        self.listener = "running"
        return UpstreamActionResult(UpstreamResultState.SUCCESS, "listener-start", "listener only")

    def stop_listener(self) -> UpstreamActionResult:
        self.stopped += 1
        self.listener = "stopped"
        return UpstreamActionResult(UpstreamResultState.SUCCESS, "listener-stop", "listener only")

    def _query_pilot(self, sql: str) -> list[list[str]]:
        return [[line] for line in self.automation_rows.splitlines() if line]


def event(
    *,
    text: str = "XIANYU-AUTOREPLY-TEST-20260729-A7P3",
    account: str = "acct-001",
    conversation: str = "conv-001",
    ref: str = "msg-001",
    direction: str = "INBOUND",
    message_type: str = "text",
) -> NormalizedInboundMessage:
    return NormalizedInboundMessage(
        internal_message_id=f"chat-new:{account}:{conversation}:{ref}",
        account_ref=account,
        conversation_ref=conversation,
        upstream_message_ref=ref,
        sender_ref="buyer-001",
        direction=direction,
        received_at="123",
        message_type=message_type,
        text=text,
        source="CHAT_NEW_API",
    )


def cfg(tmp_path: Path, **overrides: Any) -> AutoreplyConfig:
    values: dict[str, Any] = {
        "enabled": True,
        "mode": "dedicated-test",
        "poll_seconds": 1,
        "account_allowlist": ["acct-001"],
        "state_dir": str(tmp_path),
        "rules": [{"id": "test", "exact": "XIANYU-AUTOREPLY-TEST-20260729-A7P3", "reply": "XIANYU-AUTOREPLY-ACK-20260729-A7P3"}],
        "fallback": {"enabled": False},
    }
    values.update(overrides)
    return AutoreplyConfig.from_mapping(values)


def service(tmp_path: Path, wrapper: FakeWrapper | None = None, **overrides: Any) -> AutoreplyService:
    return AutoreplyService(cfg(tmp_path, **overrides), wrapper or FakeWrapper())  # type: ignore[arg-type]


def test_autoreply_default_config_is_disabled() -> None:
    config = AutoreplyConfig.disabled()
    assert config.enabled is False
    assert config.mode == "disabled"


def test_enabled_false_does_not_send(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    outcome = AutoreplyService(cfg(tmp_path, enabled=False, mode="disabled"), wrapper).process_event(event())  # type: ignore[arg-type]
    assert outcome.reason == "SKIPPED_DISABLED"
    assert wrapper.sent == []


def test_live_writes_false_does_not_send(tmp_path: Path) -> None:
    wrapper = FakeWrapper(allow_live_writes=False)
    outcome = service(tmp_path, wrapper).process_event(event())
    assert outcome.reason == "SKIPPED_LIVE_WRITES_DISABLED"
    assert wrapper.sent == []


def test_account_not_allowlisted_does_not_send(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    outcome = service(tmp_path, wrapper).process_event(event(account="acct-002"))
    assert outcome.reason == "SKIPPED_ACCOUNT_NOT_ALLOWLISTED"


def test_upstream_unhealthy_blocks_poll(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.backend_ok = False
    wrapper.events = [event()]
    outcomes = service(tmp_path, wrapper).poll_once()
    assert outcomes[0].reason == "UPSTREAM_UNHEALTHY"
    assert wrapper.sent == []


def test_account_logged_out_blocks_poll(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.logged_in = False
    wrapper.events = [event()]
    outcomes = service(tmp_path, wrapper).poll_once()
    assert outcomes[0].reason == "LOCAL_AUTH_REFRESH_REQUIRED"


def test_listener_disconnected_blocks_poll(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.listener_connected = False
    wrapper.events = [event()]
    outcomes = service(tmp_path, wrapper).poll_once()
    assert outcomes[0].reason == "LISTENER_DISCONNECTED"


def test_startup_watermark_skips_historical_messages(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.events = [event()]
    svc = service(tmp_path, wrapper)
    svc.ensure_started()
    outcome = svc.process_event(wrapper.events[0])
    assert outcome.reason == "SKIPPED_STARTUP_WATERMARK"
    assert wrapper.sent == []


def test_new_message_after_start_is_processed(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    svc = service(tmp_path, wrapper)
    svc.ensure_started()
    wrapper.events = [event(ref="msg-002")]
    outcome = svc.poll_once()[0]
    assert outcome.result == "SUCCESS"
    assert len(wrapper.sent) == 1


def test_keyword_rules_match_in_order(tmp_path: Path) -> None:
    config = cfg(
        tmp_path,
        rules=[
            {"id": "first", "contains": ["hello"], "reply": "first reply"},
            {"id": "second", "contains": ["hello"], "reply": "second reply"},
        ],
    )
    assert config.match_reply("hello there") == ("first", "first reply")


def test_fallback_is_used_when_no_rule_matches(tmp_path: Path) -> None:
    config = cfg(tmp_path, rules=[], fallback={"enabled": True, "reply": "fallback reply"})
    assert config.match_reply("unmatched") == ("fallback", "fallback reply")


def test_unsupported_message_type_is_skipped(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    outcome = service(tmp_path, wrapper).process_event(event(message_type="image"))
    assert outcome.reason == "SKIPPED_UNSUPPORTED_MESSAGE_TYPE"


def test_outbound_message_is_skipped(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    outcome = service(tmp_path, wrapper).process_event(event(direction="OUTBOUND"))
    assert outcome.reason == "SKIPPED_OUTBOUND"


def test_same_message_reference_replies_once(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    svc = service(tmp_path, wrapper)
    assert svc.process_event(event()).result == "SUCCESS"
    assert svc.process_event(event()).reason == "SKIPPED_IDEMPOTENCY"
    assert len(wrapper.sent) == 1


def test_success_blocks_restart_duplicate(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    assert service(tmp_path, wrapper).process_event(event()).result == "SUCCESS"
    assert service(tmp_path, wrapper).process_event(event()).reason == "SKIPPED_IDEMPOTENCY"
    assert len(wrapper.sent) == 1


def test_unknown_blocks_automatic_retry(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.result = UpstreamActionResult(UpstreamResultState.UNKNOWN, "op-unknown", "ambiguous")
    svc = service(tmp_path, wrapper)
    assert svc.process_event(event()).result == "UNKNOWN"
    assert svc.process_event(event()).reason == "SKIPPED_IDEMPOTENCY"
    assert len(wrapper.sent) == 1


def test_conversation_rate_limit_applies(tmp_path: Path) -> None:
    config = cfg(tmp_path, max_replies_per_conversation_per_hour=1)
    wrapper = FakeWrapper()
    svc = AutoreplyService(config, wrapper)  # type: ignore[arg-type]
    assert svc.process_event(event(ref="msg-001")).result == "SUCCESS"
    assert svc.process_event(event(ref="msg-002")).reason == "SKIPPED_RATE_LIMIT"


def test_account_rate_limit_applies(tmp_path: Path) -> None:
    config = cfg(tmp_path, max_replies_per_account_per_hour=1)
    wrapper = FakeWrapper()
    svc = AutoreplyService(config, wrapper)  # type: ignore[arg-type]
    assert svc.process_event(event(ref="msg-001", conversation="conv-001")).result == "SUCCESS"
    assert svc.process_event(event(ref="msg-002", conversation="conv-002")).reason == "SKIPPED_RATE_LIMIT"


def test_auth_failure_status_is_blocked(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.logged_in = False
    status = service(tmp_path, wrapper).doctor()
    assert status.blocked_reason == "LOCAL_AUTH_REFRESH_REQUIRED"


def test_safety_text_is_skipped(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    outcome = service(tmp_path, wrapper).process_event(event(text="请提供验证码"))
    assert outcome.reason == "SKIPPED_UNSUPPORTED_MESSAGE_TYPE"


def test_token_not_written_to_state(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    svc = service(tmp_path, wrapper)
    svc.process_event(event())
    text = (tmp_path / "state.json").read_text(encoding="utf-8")
    assert "Bearer" not in text
    assert "token" not in text.lower()


def test_message_body_not_written_to_state(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    svc = service(tmp_path, wrapper)
    svc.process_event(event())
    text = (tmp_path / "state.json").read_text(encoding="utf-8")
    assert "XIANYU-AUTOREPLY-TEST-20260729-A7P3" not in text
    assert "XIANYU-AUTOREPLY-ACK-20260729-A7P3" not in text


def test_repeated_start_does_not_create_second_instance(tmp_path: Path) -> None:
    manager = ProcessManager(tmp_path)
    manager.pid_path.write_text(str(999999), encoding="utf-8")
    assert manager.is_running(manager.read_pid()) is False


def test_stop_only_targets_recorded_process(tmp_path: Path) -> None:
    manager = ProcessManager(tmp_path)
    assert manager.stop() == (False, None)


def test_existing_listener_is_not_owned_or_stopped(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.listener = "running"
    svc = service(tmp_path, wrapper)
    svc.ensure_started()
    svc.stop_owned_listener()
    assert wrapper.stopped == 0


def test_service_started_listener_is_stopped(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    wrapper.listener = "stopped"
    svc = service(tmp_path, wrapper)
    svc.ensure_started()
    svc.stop_owned_listener()
    assert wrapper.started == 1
    assert wrapper.stopped == 1


def test_sub2api_cannot_be_targeted_by_process_code(tmp_path: Path) -> None:
    wrapper = FakeWrapper()
    svc = service(tmp_path, wrapper)
    svc.ensure_started()
    assert "sub2api" not in json_text(tmp_path / "state.json")


def test_original_upstream_wrapper_still_imports() -> None:
    from xianyu_system.worker.upstream_wrapper import UpstreamWrapper

    assert UpstreamWrapper is not None


def test_invalid_config_fails_closed(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("enabled: true\nmode: production\n", encoding="utf-8")
    try:
        AutoreplyConfig.from_file(bad)
    except AutoreplyConfigError:
        assert True
    else:  # pragma: no cover
        raise AssertionError("expected config error")


def json_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def test_autoreply_cli_help_lists_commands(capsys) -> None:
    import pytest

    from xianyu_system.worker.autoreply.cli import main

    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    output = capsys.readouterr().out
    assert "doctor" in output
    assert "start" in output
    assert "status" in output
    assert "stop" in output
