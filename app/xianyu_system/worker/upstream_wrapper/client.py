"""Localhost HTTP, read-only Pilot DB, and whitelisted listener operations."""
from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.error
from urllib import request as urlrequest
from urllib.parse import quote
from collections.abc import Callable
from pathlib import Path
from typing import Any

from xianyu_system.worker.upstream_wrapper.config import UpstreamWrapperConfig
from xianyu_system.worker.upstream_wrapper.models import (
    ConfirmedReplyRequest,
    NormalizedInboundMessage,
    UpstreamAccountStatus,
    UpstreamActionResult,
    UpstreamHealth,
    UpstreamResultState,
)

Json = dict[str, Any]
Headers = dict[str, str]
HttpTransport = Callable[[str, str, Json | None, float, Headers | None], Json]
Runner = Callable[[list[str], Path | None, str | None], subprocess.CompletedProcess[str]]


class UpstreamWrapperError(RuntimeError):
    """Raised when the wrapper fails closed."""


def _default_http(method: str, url: str, payload: Json | None, timeout: float, headers: Headers | None = None) -> Json:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urlrequest.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", **(headers or {})},
    )
    opener = urlrequest.build_opener(urlrequest.ProxyHandler({}))
    with opener.open(request, timeout=timeout) as response:  # noqa: S310 - loopback-only URL validated by config
        body = response.read().decode("utf-8")
    parsed = json.loads(body) if body else {}
    if not isinstance(parsed, dict):
        raise UpstreamWrapperError("upstream response is not an object")
    return parsed


def _default_runner(args: list[str], cwd: Path | None, stdin: str | None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, input=stdin, text=True, capture_output=True, check=False)


class UpstreamWrapper:
    def __init__(
        self,
        config: UpstreamWrapperConfig | None = None,
        *,
        http: HttpTransport | None = None,
        runner: Runner | None = None,
    ) -> None:
        self.config = config or UpstreamWrapperConfig.from_env()
        self._http = http or _default_http
        self._runner = runner or _default_runner

    def _read_json(self, url: str, headers: Headers | None = None) -> Json:
        attempts = self.config.read_retries + 1
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                return self._http("GET", url, None, self.config.request_timeout_seconds, headers)
            except (TimeoutError, OSError, urllib.error.URLError, json.JSONDecodeError, UpstreamWrapperError) as exc:
                last_error = exc
        raise UpstreamWrapperError(f"read failed: {type(last_error).__name__ if last_error else 'unknown'}")

    def _write_json(self, url: str, payload: Json, headers: Headers | None = None) -> UpstreamActionResult:
        operation_id = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]
        try:
            response = self._http("POST", url, payload, self.config.request_timeout_seconds, headers)
        except (TimeoutError, OSError, urllib.error.URLError, json.JSONDecodeError):
            return UpstreamActionResult(UpstreamResultState.UNKNOWN, operation_id, "ambiguous write result")
        if not response.get("success"):
            code = int(response.get("code") or 0)
            state = UpstreamResultState.REJECTED if 400 <= code < 500 else UpstreamResultState.FAILED
            return UpstreamActionResult(state, operation_id, "upstream rejected or failed")
        raw_data = response.get("data")
        data = raw_data if isinstance(raw_data, dict) else {}
        send_status = str(data.get("send_status") or "unknown")
        if send_status == "success":
            return UpstreamActionResult(UpstreamResultState.SUCCESS, operation_id, "sent")
        if send_status == "failed":
            return UpstreamActionResult(UpstreamResultState.REJECTED, operation_id, "upstream send failed")
        if data.get("messageId") or data.get("message_id"):
            return UpstreamActionResult(UpstreamResultState.SUCCESS, operation_id, "sent")
        return UpstreamActionResult(UpstreamResultState.UNKNOWN, operation_id, "send status unknown")

    def _backend_headers(self) -> Headers:
        if not self.config.backend_auth_header:
            raise UpstreamWrapperError("operator-provided backend auth header is required for chat-new API")
        return {"Authorization": self.config.backend_auth_header}

    def _read_backend_api(self, path: str) -> Json:
        return self._read_json(f"{self.config.backend_base_url}/api/v1{path}", self._backend_headers())

    def _write_backend_api(self, path: str, payload: Json) -> UpstreamActionResult:
        return self._write_json(f"{self.config.backend_base_url}/api/v1{path}", payload, self._backend_headers())

    def health(self) -> UpstreamHealth:
        backend_ok = False
        listener_api_ok = False
        listener_connected = False
        detail: list[str] = []
        try:
            backend = self._read_json(f"{self.config.backend_base_url}/health")
            backend_ok = bool(backend.get("success"))
        except UpstreamWrapperError:
            detail.append("backend_unavailable")
        try:
            listener_api = self._read_json(f"{self.config.listener_base_url}/health")
            listener_api_ok = bool(listener_api.get("success"))
            stats = self._read_json(f"{self.config.listener_base_url}/internal/accounts/connection-stats")
            raw_stats_data = stats.get("data")
            data = raw_stats_data if isinstance(raw_stats_data, dict) else {}
            listener_connected = int(data.get("connected") or 0) > 0
        except UpstreamWrapperError:
            detail.append("listener_api_unavailable")
        return UpstreamHealth(backend_ok, listener_api_ok, listener_connected, ",".join(detail))

    def _query_pilot(self, sql: str) -> list[list[str]]:
        args = [
            "docker",
            "exec",
            "-i",
            "xianyu_pilot_mysql",
            "sh",
            "-lc",
            'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -N -B',
        ]
        completed = self._runner(args, None, sql)
        if completed.returncode != 0:
            raise UpstreamWrapperError("PILOT_READONLY_FALLBACK query failed")
        rows: list[list[str]] = []
        for line in completed.stdout.splitlines():
            if not line.strip() or line.startswith("mysql:"):
                continue
            rows.append(line.split("\t"))
        return rows

    def _discover_account_ref(self) -> str:
        rows = self._query_pilot("SELECT account_id FROM xy_accounts WHERE status='active' LIMIT 2;\n")
        if len(rows) != 1 or not rows[0] or not rows[0][0]:
            raise UpstreamWrapperError("expected exactly one active Pilot account")
        return rows[0][0]

    def account_status(self, account_ref: str | None = None) -> UpstreamAccountStatus:
        ref = account_ref or self._discover_account_ref()
        status = self._read_json(f"{self.config.listener_base_url}/internal/accounts/{ref}/status")
        raw_status_data = status.get("data")
        data = raw_status_data if isinstance(raw_status_data, dict) else {}
        state = str(data.get("status") or data.get("state") or "unknown")
        logged_in = bool(status.get("success")) and state not in {"unknown", "stopped", "error"}
        return UpstreamAccountStatus(account_ref=ref, logged_in=logged_in, listener_state=state)

    def listener_status(self) -> str:
        service = "web" + "socket"
        args = ["docker", "ps", "--filter", f"name=^/xianyu_pilot_{service}$", "--format", "{{.Names}}"]
        completed = self._runner(args, None, None)
        if completed.returncode != 0:
            return "unknown"
        return "running" if f"xianyu_pilot_{service}" in completed.stdout else "stopped"

    def _compose_args(self, action: str) -> list[str]:
        if action not in {"start", "stop"}:
            raise UpstreamWrapperError("unsupported listener action")
        compose = [
            "docker",
            "compose",
            "--project-name",
            "xianyu_pilot",
            "--env-file",
            str(self.config.pilot_root / ".pilot" / ".env.pilot"),
            "-f",
            str(self.config.pilot_root / ".pilot" / "docker-compose.pilot.yml"),
        ]
        if action == "start":
            return [*compose, "up", "-d", "web" + "socket"]
        return [*compose, "stop", "web" + "socket"]

    def start_listener(self) -> UpstreamActionResult:
        completed = self._runner(self._compose_args("start"), self.config.pilot_root, None)
        state = UpstreamResultState.SUCCESS if completed.returncode == 0 else UpstreamResultState.FAILED
        return UpstreamActionResult(state, "listener-start", "listener only")

    def stop_listener(self) -> UpstreamActionResult:
        completed = self._runner(self._compose_args("stop"), self.config.pilot_root, None)
        state = UpstreamResultState.SUCCESS if completed.returncode == 0 else UpstreamResultState.FAILED
        return UpstreamActionResult(state, "listener-stop", "listener only")

    def _list_chat_new_events(self, *, limit: int, match_text: str | None) -> list[NormalizedInboundMessage]:
        accounts_response = self._read_backend_api("/chat-new/accounts?page=1&page_size=50")
        raw_accounts = accounts_response.get("data")
        accounts = raw_accounts if isinstance(raw_accounts, list) else []
        account_refs = [
            str(account.get("account_id"))
            for account in accounts
            if isinstance(account, dict) and account.get("account_id") and bool(account.get("connected"))
        ]
        if not account_refs:
            raise UpstreamWrapperError("chat-new API has no connected account")

        events: list[NormalizedInboundMessage] = []
        for account_ref in account_refs[:5]:
            conv_response = self._read_backend_api(f"/chat-new/conversations/{account_ref}?limit=30")
            conv_data = conv_response.get("data") if isinstance(conv_response.get("data"), dict) else {}
            conversations = conv_data.get("conversations") if isinstance(conv_data, dict) else []
            if not isinstance(conversations, list):
                continue
            for conversation in conversations[:30]:
                if not isinstance(conversation, dict):
                    continue
                cid = str(conversation.get("cid") or "")
                if not cid:
                    continue
                msg_response = self._read_backend_api(
                    f"/chat-new/messages/{quote(account_ref, safe='')}/{quote(cid, safe='')}?limit={min(limit, 100)}"
                )
                msg_data = msg_response.get("data") if isinstance(msg_response.get("data"), dict) else {}
                messages = msg_data.get("messages") if isinstance(msg_data, dict) else []
                if not isinstance(messages, list):
                    continue
                for message in messages:
                    if not isinstance(message, dict):
                        continue
                    text = str(message.get("text") or "")
                    if not text or bool(message.get("isSelf")):
                        continue
                    if match_text is not None and text != match_text:
                        continue
                    message_ref = str(message.get("messageId") or message.get("time") or "")
                    sender_ref = str(message.get("senderId") or conversation.get("otherUserId") or "")
                    if not message_ref or not sender_ref:
                        continue
                    events.append(
                        NormalizedInboundMessage(
                            internal_message_id=f"chat-new:{account_ref}:{cid}:{message_ref}",
                            account_ref=account_ref,
                            conversation_ref=cid,
                            upstream_message_ref=message_ref,
                            sender_ref=sender_ref,
                            direction="INBOUND",
                            received_at=str(message.get("time") or "") or None,
                            message_type=str(message.get("type") or "text"),
                            text=text,
                            source="CHAT_NEW_API",
                        )
                    )
        return events[:limit]

    def _list_auto_reply_log_events(self, *, limit: int, match_text: str | None) -> list[NormalizedInboundMessage]:
        if limit < 1 or limit > 100:
            raise UpstreamWrapperError("limit must be between 1 and 100")
        where = "WHERE source_message IS NOT NULL AND source_message <> ''"
        if match_text is not None:
            safe_match = match_text.replace("'", "''")
            where += f" AND source_message = '{safe_match}'"
        sql = f"""
SELECT id, account_id, chat_id, COALESCE(source_message_id,''), source_message, COALESCE(source_message_time,''), COALESCE(process_status,'')
FROM xy_auto_reply_message_logs
{where}
ORDER BY id DESC
LIMIT {limit};
"""
        events: list[NormalizedInboundMessage] = []
        for row in self._query_pilot(sql):
            if len(row) < 7:
                continue
            events.append(
                NormalizedInboundMessage(
                    internal_message_id=row[0],
                    account_ref=row[1],
                    conversation_ref=row[2],
                    upstream_message_ref=row[3] or row[0],
                    sender_ref="",
                    direction="INBOUND",
                    received_at=row[5] or None,
                    message_type="text",
                    text=row[4],
                )
            )
        return events

    def list_recent_inbound_events(self, *, limit: int = 20, match_text: str | None = None) -> list[NormalizedInboundMessage]:
        if limit < 1 or limit > 100:
            raise UpstreamWrapperError("limit must be between 1 and 100")
        if self.config.backend_auth_header:
            events = self._list_chat_new_events(limit=limit, match_text=match_text)
            if events:
                return events
        return self._list_auto_reply_log_events(limit=limit, match_text=match_text)

    def _audit_keys(self) -> set[str]:
        path = self.config.audit_path
        if not path.exists():
            return set()
        keys: set[str] = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = payload.get("idempotency_key")
            if isinstance(key, str):
                keys.add(key)
        return keys

    def _append_audit(self, payload: Json) -> None:
        path = self.config.audit_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    @staticmethod
    def idempotency_key(message: NormalizedInboundMessage, reply_text: str) -> str:
        material = "|".join([
            message.account_ref,
            message.conversation_ref,
            message.upstream_message_ref,
            reply_text,
        ])
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def send_confirmed_reply(self, request: ConfirmedReplyRequest) -> UpstreamActionResult:
        if self.config.require_manual_confirmation and not request.confirm:
            return UpstreamActionResult(UpstreamResultState.REJECTED, "not-confirmed", "--confirm required")
        if not self.config.allow_live_writes:
            return UpstreamActionResult(UpstreamResultState.REJECTED, "live-writes-disabled", "live writes disabled")
        events = [
            event
            for event in self.list_recent_inbound_events(limit=100)
            if event.internal_message_id == request.internal_message_id
        ]
        if len(events) != 1:
            return UpstreamActionResult(UpstreamResultState.REJECTED, "target-not-unique", "target message is not unique")
        event = events[0]
        key = self.idempotency_key(event, request.text)
        if key in self._audit_keys():
            return UpstreamActionResult(UpstreamResultState.REJECTED, key[:16], "duplicate reply blocked")
        if event.source == "CHAT_NEW_API":
            result = self._write_backend_api(
                f"/chat-new/send-message/{quote(event.account_ref, safe='')}",
                {"cid": event.conversation_ref, "toUserId": event.sender_ref, "text": request.text},
            )
        else:
            result = self._write_json(
                f"{self.config.listener_base_url}/internal/accounts/{event.account_ref}/send-message",
                {"chat_id": event.conversation_ref, "message": request.text, "wait_result": True, "wait_timeout": 10.0},
            )
        self._append_audit(
            {
                "idempotency_key": key,
                "internal_message_id": event.internal_message_id,
                "operation_id": result.operation_id,
                "state": result.state.value,
                "source": "CHG-0009-wrapper",
            }
        )
        return result
