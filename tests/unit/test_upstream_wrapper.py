from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from xianyu_system.worker.upstream_wrapper import UpstreamWrapper, UpstreamWrapperConfig
from xianyu_system.worker.upstream_wrapper.client import UpstreamWrapperError
from xianyu_system.worker.upstream_wrapper.config import UpstreamWrapperConfigError
from xianyu_system.worker.upstream_wrapper.models import ConfirmedReplyRequest, UpstreamResultState


class FakeRuntime:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []
        self.runner_calls: list[list[str]] = []
        self.send_response: dict[str, Any] = {
            "success": True,
            "code": 200,
            "data": {"send_status": "success", "message": "redacted"},
        }
        self.account_rows = "acct-001\n"
        self.message_rows = "1\tacct-001\tchat-001\tmsg-001\tXIANYU-WRAPPER-TEST-001\t2026-07-29 12:00:00\tskipped\n"

    def http(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        self.calls.append((method, url, payload))
        if url.endswith("/health"):
            return {"success": True, "code": 200, "data": {"status": "running", "database": "connected"}}
        if url.endswith("/connection-stats"):
            return {"success": True, "code": 200, "data": {"total_instances": 1, "connected": 1}}
        if url.endswith("/status"):
            return {"success": True, "code": 200, "data": {"status": "running"}}
        if url.endswith("/send-message"):
            return self.send_response
        raise AssertionError(f"unexpected URL {url}")

    def runner(self, args: list[str], cwd: Path | None, stdin: str | None) -> subprocess.CompletedProcess[str]:
        self.runner_calls.append(args)
        if args[:2] == ["docker", "ps"]:
            return subprocess.CompletedProcess(args, 0, "xianyu_pilot_" + "websocket\n", "")
        if args[:3] == ["docker", "compose", "--project-name"]:
            return subprocess.CompletedProcess(args, 0, "ok\n", "")
        if args[:3] == ["docker", "exec", "-i"]:
            assert stdin is not None
            stdout = self.account_rows if "FROM xy_accounts" in stdin else self.message_rows
            return subprocess.CompletedProcess(args, 0, stdout, "")
        if args[:3] == ["powershell", "-NoProfile", "-Command"]:
            return subprocess.CompletedProcess(args, 0, "running\n", "")
        raise AssertionError(f"unexpected args {args}")


class FakeProcess:
    def __init__(self, pid: int = 4321, *, returncodes: list[int | None] | None = None) -> None:
        self.pid = pid
        self.returncodes = returncodes or [None]
        self.polls = 0
        self.terminated = False
        self.killed = False

    def poll(self) -> int | None:
        index = min(self.polls, len(self.returncodes) - 1)
        self.polls += 1
        return self.returncodes[index]

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True

    def wait(self, timeout: float | None = None) -> int:
        return 0


class StoppedRuntime(FakeRuntime):
    def runner(self, args: list[str], cwd: Path | None, stdin: str | None) -> subprocess.CompletedProcess[str]:
        self.runner_calls.append(args)
        if args[:2] == ["docker", "ps"]:
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:3] == ["powershell", "-NoProfile", "-Command"]:
            return subprocess.CompletedProcess(args, 0, "", "")
        return super().runner(args, cwd, stdin)


class ManualListenerWrapperForTest(UpstreamWrapper):
    def __init__(
        self,
        *args: Any,
        manual_paths: tuple[Path, Path, Path],
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._test_manual_paths = manual_paths

    def _manual_listener_paths(self) -> tuple[Path, Path, Path]:
        return self._test_manual_paths


class ManualListenerStartupRuntime(StoppedRuntime):
    def __init__(self, health_failures: int = 0) -> None:
        super().__init__()
        self.health_failures = health_failures
        self.health_calls = 0

    def http(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if url.endswith("/health"):
            self.health_calls += 1
            if self.health_calls <= self.health_failures:
                raise TimeoutError
            return {"success": True, "code": 200, "data": {"status": "running"}}
        return super().http(method, url, payload, timeout, headers)


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


def config(tmp_path: Path, *, allow_live_writes: bool = False) -> UpstreamWrapperConfig:
    return UpstreamWrapperConfig(
        allow_live_writes=allow_live_writes,
        audit_path=tmp_path / "audit.jsonl",
        pilot_root=Path("D:/xianyu-upstream-pilot"),
    )


def chat_new_config(tmp_path: Path, *, allow_live_writes: bool = False) -> UpstreamWrapperConfig:
    return UpstreamWrapperConfig(
        allow_live_writes=allow_live_writes,
        backend_auth_header="Bearer operator-provided-placeholder",
        audit_path=tmp_path / "audit.jsonl",
        pilot_root=Path("D:/xianyu-upstream-pilot"),
    )


def wrapper(runtime: FakeRuntime, tmp_path: Path, *, allow_live_writes: bool = False) -> UpstreamWrapper:
    return UpstreamWrapper(config(tmp_path, allow_live_writes=allow_live_writes), http=runtime.http, runner=runtime.runner)


def test_chat_new_event_source_matches_online_chat_api(tmp_path: Path) -> None:
    calls: list[tuple[str, str, dict[str, str] | None]] = []

    def http(
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        calls.append((method, url, headers))
        if url.endswith("/api/v1/chat-new/accounts?page=1&page_size=50"):
            return {"success": True, "data": [{"account_id": "acct-001", "connected": True}]}
        if "/api/v1/chat-new/conversations/acct-001" in url:
            return {
                "success": True,
                "data": {"conversations": [{"cid": "chat-001", "otherUserId": "buyer-001"}]},
            }
        if "/api/v1/chat-new/messages/acct-001/chat-001" in url:
            return {
                "success": True,
                "data": {
                    "messages": [
                        {
                            "messageId": "msg-001",
                            "senderId": "buyer-001",
                            "isSelf": False,
                            "type": "text",
                            "text": "XIANYU-WRAPPER-TEST-001",
                            "time": 123,
                        }
                    ]
                },
            }
        raise AssertionError(f"unexpected URL {url}")

    client = UpstreamWrapper(chat_new_config(tmp_path), http=http, runner=FakeRuntime().runner)
    event = client.list_recent_inbound_events(match_text="XIANYU-WRAPPER-TEST-001")[0]
    assert event.source == "CHAT_NEW_API"
    assert event.sender_ref == "buyer-001"
    assert event.internal_message_id.startswith("chat-new:")
    assert all(call[2] == {"Authorization": "Bearer operator-provided-placeholder"} for call in calls)


def test_health_success_and_account_status_mapping(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    client = wrapper(runtime, tmp_path)
    health = client.health()
    account = client.account_status()
    assert health.backend_ok is True
    assert health.listener_api_ok is True
    assert health.listener_connected is True
    assert account.logged_in is True
    assert account.listener_state == "running"


def test_non_loopback_url_is_rejected() -> None:
    with pytest.raises(UpstreamWrapperConfigError):
        UpstreamWrapperConfig(backend_base_url="http://192.168.1.2:18089")


def test_config_from_env_file_rejects_non_loopback(tmp_path: Path) -> None:
    env = tmp_path / "wrapper.env"
    env.write_text("XIANYU_UPSTREAM_BACKEND_URL=http://example.com\n", encoding="utf-8")
    with pytest.raises(UpstreamWrapperConfigError):
        UpstreamWrapperConfig.from_env(env)


def test_message_event_normalization_and_body_not_logged(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    runtime = FakeRuntime()
    event = wrapper(runtime, tmp_path).list_recent_inbound_events(match_text="XIANYU-WRAPPER-TEST-001")[0]
    assert event.internal_message_id == "1"
    assert event.direction == "INBOUND"
    assert event.source == "PILOT_READONLY_FALLBACK"
    assert event.text == "XIANYU-WRAPPER-TEST-001"
    captured = capsys.readouterr()
    assert "XIANYU-WRAPPER-TEST-001" not in captured.out


def test_model_and_audit_do_not_contain_credential_fields(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    event = wrapper(runtime, tmp_path).list_recent_inbound_events()[0]
    assert "cookie" not in event.__dict__
    assert "token" not in event.__dict__
    assert "session" not in event.__dict__


def test_listener_commands_only_target_service(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    client = wrapper(runtime, tmp_path)
    assert client.listener_status() == "running"
    assert client.start_listener().state is UpstreamResultState.SUCCESS
    assert client.stop_listener().state is UpstreamResultState.SUCCESS
    flattened = " ".join(" ".join(call) for call in runtime.runner_calls)
    assert "web" + "socket" in flattened
    assert "sub2api" not in flattened
    assert " down " not in f" {flattened} "
    assert " prune " not in f" {flattened} "


def test_manual_listener_start_rejects_when_docker_listener_running(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    result = wrapper(runtime, tmp_path).start_manual_listener()
    assert result.state is UpstreamResultState.REJECTED
    assert "docker listener is already running" in result.detail


def test_manual_listener_status_uses_owned_pid_file(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    cfg = UpstreamWrapperConfig(
        audit_path=tmp_path / "audit.jsonl",
        manual_listener_pid_path=tmp_path / "manual-listener.pid.json",
    )
    cfg.manual_listener_pid_path.write_text(
        '{"pid": 1234, "root": "D:/xianyu-upstream-manual-chg0016"}',
        encoding="utf-8",
    )
    client = UpstreamWrapper(cfg, http=runtime.http, runner=runtime.runner)
    assert client.manual_listener_status() == "running"
    assert any(call[:3] == ["powershell", "-NoProfile", "-Command"] for call in runtime.runner_calls)


def test_manual_listener_start_forces_manual_only_safe_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    runtime = ManualListenerStartupRuntime()
    upstream_root = tmp_path / "upstream"
    python_exe = upstream_root / ".venv" / "Scripts" / "python.exe"
    entry = upstream_root / "websocket" / "main.py"
    python_exe.parent.mkdir(parents=True)
    entry.parent.mkdir(parents=True)
    python_exe.write_text("", encoding="utf-8")
    entry.write_text("", encoding="utf-8")
    popen_calls: list[dict[str, Any]] = []

    monkeypatch.setenv("CAPTCHA_REMOTE_SERVICE_URL", "https://solver.invalid")
    monkeypatch.setenv("CAPTCHA_REMOTE_SECRET_KEY", "redacted")
    monkeypatch.setenv("REMOTE_TOKEN_URL", "https://token.invalid")
    monkeypatch.setenv("AUTO_START_WEBSOCKET", "true")

    def fake_popen(*args: Any, **kwargs: Any) -> FakeProcess:
        popen_calls.append({"args": args, "kwargs": kwargs})
        assert kwargs["stdout"] is not subprocess.DEVNULL
        assert kwargs["stderr"] is not subprocess.DEVNULL
        return FakeProcess()

    cfg = UpstreamWrapperConfig(
        audit_path=tmp_path / "audit.jsonl",
        manual_listener_pid_path=tmp_path / "manual-listener.pid.json",
    )
    client = ManualListenerWrapperForTest(
        cfg,
        http=runtime.http,
        runner=runtime.runner,
        popen=fake_popen,
        sleep=lambda _: None,
        manual_paths=(upstream_root, python_exe, entry),
    )

    result = client.start_manual_listener()

    assert result.state is UpstreamResultState.SUCCESS
    assert len(popen_calls) == 1
    env = popen_calls[0]["kwargs"]["env"]
    assert env["AUTO_START_WEBSOCKET"] == "false"
    assert env["CAPTCHA_MANUAL_ONLY"] == "true"
    assert env["CAPTCHA_MANUAL_ONE_SHOT"] == "true"
    assert env["CAPTCHA_MANUAL_TIMEOUT_SECONDS"] == "300"
    assert env["CAPTCHA_DRISSIONPAGE_FALLBACK_ENABLED"] == "false"
    assert env["CAPTCHA_DRISSIONPAGE_HEADLESS"] == "true"
    assert env["BROWSER_HEADLESS"] == "false"
    assert "CAPTCHA_REMOTE_SERVICE_URL" not in env
    assert "CAPTCHA_REMOTE_SECRET_KEY" not in env
    assert "REMOTE_TOKEN_URL" not in env
    assert env["MYSQL_HOST"] == "127.0.0.1"
    assert env["MYSQL_PORT"] == "13306"
    assert env["REDIS_HOST"] == "127.0.0.1"
    assert env["REDIS_PORT"] == "16379"
    assert env["WEBSOCKET_PORT"] == "18090"
    pid_data = (tmp_path / "manual-listener.pid.json").read_text(encoding="utf-8")
    assert "CHG-0016-manual-listener.log" in pid_data


def test_manual_listener_start_fails_when_process_exits_and_cleans_pid(tmp_path: Path) -> None:
    runtime = ManualListenerStartupRuntime()
    upstream_root = tmp_path / "upstream"
    python_exe = upstream_root / ".venv" / "Scripts" / "python.exe"
    entry = upstream_root / "websocket" / "main.py"
    python_exe.parent.mkdir(parents=True)
    entry.parent.mkdir(parents=True)
    python_exe.write_text("", encoding="utf-8")
    entry.write_text("", encoding="utf-8")
    log_path = Path("D:/xianyu/.local/logs/CHG-0016-manual-listener.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("password=placeholder\nTraceback\nasyncmy OperationalError\n", encoding="utf-8")
    pid_path = tmp_path / "manual-listener.pid.json"
    process = FakeProcess(returncodes=[1])

    client = ManualListenerWrapperForTest(
        UpstreamWrapperConfig(audit_path=tmp_path / "audit.jsonl", manual_listener_pid_path=pid_path),
        http=runtime.http,
        runner=runtime.runner,
        popen=lambda *args, **kwargs: process,
        sleep=lambda _: None,
        manual_paths=(upstream_root, python_exe, entry),
    )

    result = client.start_manual_listener()

    assert result.state is UpstreamResultState.FAILED
    assert result.detail == "DATABASE_CONNECTION_ERROR"
    assert "placeholder" not in result.detail.lower()
    assert not pid_path.exists()


def test_manual_listener_start_timeout_stops_own_process_and_cleans_pid(tmp_path: Path) -> None:
    runtime = ManualListenerStartupRuntime(health_failures=100)
    upstream_root = tmp_path / "upstream"
    python_exe = upstream_root / ".venv" / "Scripts" / "python.exe"
    entry = upstream_root / "websocket" / "main.py"
    python_exe.parent.mkdir(parents=True)
    entry.parent.mkdir(parents=True)
    python_exe.write_text("", encoding="utf-8")
    entry.write_text("", encoding="utf-8")
    pid_path = tmp_path / "manual-listener.pid.json"
    process = FakeProcess(returncodes=[None] * 100)
    clock = FakeClock()

    client = ManualListenerWrapperForTest(
        UpstreamWrapperConfig(audit_path=tmp_path / "audit.jsonl", manual_listener_pid_path=pid_path),
        http=runtime.http,
        runner=runtime.runner,
        popen=lambda *args, **kwargs: process,
        sleep=clock.sleep,
        clock=clock,
        manual_paths=(upstream_root, python_exe, entry),
    )

    result = client.start_manual_listener()

    assert result.state is UpstreamResultState.FAILED
    assert result.detail == "STARTUP_HEALTH_TIMEOUT"
    assert process.terminated is True
    assert process.killed is False
    assert not pid_path.exists()
    assert runtime.health_calls >= 1


def test_manual_listener_start_waits_for_health_before_success(tmp_path: Path) -> None:
    runtime = ManualListenerStartupRuntime(health_failures=2)
    upstream_root = tmp_path / "upstream"
    python_exe = upstream_root / ".venv" / "Scripts" / "python.exe"
    entry = upstream_root / "websocket" / "main.py"
    python_exe.parent.mkdir(parents=True)
    entry.parent.mkdir(parents=True)
    python_exe.write_text("", encoding="utf-8")
    entry.write_text("", encoding="utf-8")

    client = ManualListenerWrapperForTest(
        UpstreamWrapperConfig(audit_path=tmp_path / "audit.jsonl", manual_listener_pid_path=tmp_path / "pid.json"),
        http=runtime.http,
        runner=runtime.runner,
        popen=lambda *args, **kwargs: FakeProcess(returncodes=[None] * 10),
        sleep=lambda _: None,
        manual_paths=(upstream_root, python_exe, entry),
    )

    result = client.start_manual_listener()

    assert result.state is UpstreamResultState.SUCCESS
    assert runtime.health_calls == 3


def test_local_runtime_log_directory_is_gitignored() -> None:
    assert ".local/" in Path(".gitignore").read_text(encoding="utf-8").splitlines()


def test_reply_without_confirm_is_rejected(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    result = wrapper(runtime, tmp_path, allow_live_writes=True).send_confirmed_reply(
        ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=False)
    )
    assert result.state is UpstreamResultState.REJECTED


def test_reply_with_live_writes_disabled_is_rejected(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    result = wrapper(runtime, tmp_path).send_confirmed_reply(
        ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True)
    )
    assert result.state is UpstreamResultState.REJECTED


def test_non_unique_target_message_is_rejected(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    runtime.message_rows = runtime.message_rows + runtime.message_rows
    result = wrapper(runtime, tmp_path, allow_live_writes=True).send_confirmed_reply(
        ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True)
    )
    assert result.state is UpstreamResultState.REJECTED


def test_successful_reply_is_audited_and_duplicate_blocked(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    client = wrapper(runtime, tmp_path, allow_live_writes=True)
    first = client.send_confirmed_reply(ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True))
    second = client.send_confirmed_reply(ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True))
    assert first.state is UpstreamResultState.SUCCESS
    assert second.state is UpstreamResultState.REJECTED
    audit = (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
    assert "XIANYU-WRAPPER-ACK-001" not in audit
    assert "XIANYU-WRAPPER-TEST-001" not in audit


def test_chat_new_reply_uses_online_chat_send_api(tmp_path: Path) -> None:
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def http(
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        calls.append((method, url, payload))
        if url.endswith("/api/v1/chat-new/accounts?page=1&page_size=50"):
            return {"success": True, "data": [{"account_id": "acct-001", "connected": True}]}
        if "/api/v1/chat-new/conversations/acct-001" in url:
            return {"success": True, "data": {"conversations": [{"cid": "chat-001", "otherUserId": "buyer-001"}]}}
        if "/api/v1/chat-new/messages/acct-001/chat-001" in url:
            return {
                "success": True,
                "data": {
                    "messages": [
                        {
                            "messageId": "msg-001",
                            "senderId": "buyer-001",
                            "isSelf": False,
                            "type": "text",
                            "text": "XIANYU-WRAPPER-TEST-001",
                            "time": 123,
                        }
                    ]
                },
            }
        if url.endswith("/api/v1/chat-new/send-message/acct-001"):
            assert payload == {"cid": "chat-001", "toUserId": "buyer-001", "text": "XIANYU-WRAPPER-ACK-001"}
            return {"success": True, "data": {"messageId": "sent-001"}}
        raise AssertionError(f"unexpected URL {url}")

    client = UpstreamWrapper(chat_new_config(tmp_path, allow_live_writes=True), http=http, runner=FakeRuntime().runner)
    event = client.list_recent_inbound_events(match_text="XIANYU-WRAPPER-TEST-001")[0]
    result = client.send_confirmed_reply(ConfirmedReplyRequest(event.internal_message_id, "XIANYU-WRAPPER-ACK-001", True))
    assert result.state is UpstreamResultState.SUCCESS
    assert any(call[1].endswith("/api/v1/chat-new/send-message/acct-001") for call in calls)


def test_write_timeout_returns_unknown_and_does_not_retry(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    post_count = 0

    def timeout_http(
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        nonlocal post_count
        if method == "POST":
            post_count += 1
            raise TimeoutError
        return runtime.http(method, url, payload, timeout)

    client = UpstreamWrapper(config(tmp_path, allow_live_writes=True), http=timeout_http, runner=runtime.runner)
    result = client.send_confirmed_reply(ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True))
    assert result.state is UpstreamResultState.UNKNOWN
    assert post_count == 1


def test_upstream_rejection_maps_to_rejected(tmp_path: Path) -> None:
    runtime = FakeRuntime()
    runtime.send_response = {"success": False, "code": 400, "data": None}
    result = wrapper(runtime, tmp_path, allow_live_writes=True).send_confirmed_reply(
        ConfirmedReplyRequest("1", "XIANYU-WRAPPER-ACK-001", confirm=True)
    )
    assert result.state is UpstreamResultState.REJECTED


def test_query_failure_fails_closed(tmp_path: Path) -> None:
    runtime = FakeRuntime()

    def failing_runner(args: list[str], cwd: Path | None, stdin: str | None) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args, 1, "", "failed")

    client = UpstreamWrapper(config(tmp_path), http=runtime.http, runner=failing_runner)
    with pytest.raises(UpstreamWrapperError):
        client.list_recent_inbound_events()
