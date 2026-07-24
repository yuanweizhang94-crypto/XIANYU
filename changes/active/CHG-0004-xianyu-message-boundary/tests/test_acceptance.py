from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"

CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ARCHIVE / "CHG-0003-xianyu-account-boundary"
CHG_0004 = ACTIVE / "CHG-0004-xianyu-message-boundary"

ACCOUNT_CAPABILITY = "CAP-XY-ACCOUNT"
MESSAGE_CAPABILITY = "CAP-XY-MESSAGE"

ACCOUNT_VERIFIED_CANDIDATE_SHA = "2aab941cb7f713d7e46675789c47971a2c79c564"

ACCOUNT_ARCHIVED_ACCEPTANCE = (
    "changes/archive/"
    "CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)

ACCOUNT_ACTIVE_ACCEPTANCE = (
    "changes/active/"
    "CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(
            encoding="utf-8"
        )
    )
    return {str(item["id"]): item for item in registry["capabilities"]}


def test_completed_changes_are_archived_with_history_preserved() -> None:
    assert not (ACTIVE / "CHG-0002-core-application").exists()
    assert not (ACTIVE / "CHG-0003-xianyu-account-boundary").exists()

    for change_dir in [CHG_0002, CHG_0003]:
        assert change_dir.is_dir()

        for name in [
            "proposal.md",
            "design.md",
            "tasks.md",
            "acceptance.md",
        ]:
            assert status_of(change_dir / name) == "ARCHIVED"

        assert (change_dir / "tests" / "test_acceptance.py").is_file()


def test_chg_0004_is_the_only_approved_active_change() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())

    assert active_dirs == ["CHG-0004-xianyu-message-boundary"]

    for name in [
        "proposal.md",
        "design.md",
        "tasks.md",
        "acceptance.md",
    ]:
        assert status_of(CHG_0004 / name) == "APPROVED"


def test_chg_0004_t3_approves_transport_authentication_and_risk_boundaries() -> None:
    task_lines = [
        line
        for line in (CHG_0004 / "tasks.md").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.startswith("- [")
    ]

    assert len(task_lines) == 9
    assert task_lines[0].startswith("- [x]")
    assert task_lines[1].startswith("- [x]")
    assert task_lines[2].startswith("- [x]")
    assert all(line.startswith("- [ ]") for line in task_lines[3:])

    state = json.loads(
        (ROOT / "generated" / "PROJECT_STATE.json").read_text(
            encoding="utf-8"
        )
    )

    assert state["active_change"]["id"] == (
        "CHG-0004-xianyu-message-boundary"
    )
    assert state["active_change"]["status"] == "APPROVED"

    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 3

    assert all(
        item["completed"] is True
        for item in state["tasks"]["items"][:3]
    )

    assert all(
        item["completed"] is False
        for item in state["tasks"]["items"][3:]
    )

    assert state["tasks"]["next_task"] == (
        "T4 Approve ordering, deduplication, and persistence boundaries"
    )

    assert state["capabilities"]["by_status"] == {
        "planned": 6,
        "verified": 4,
    }


def test_message_capability_remains_planned_and_unimplemented() -> None:
    registry = registry_by_id()

    account = registry[ACCOUNT_CAPABILITY]
    assert account["status"] == "verified"
    assert account["active_change"] is None
    assert account["last_verified_commit"] == ACCOUNT_VERIFIED_CANDIDATE_SHA
    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account["test_paths"]
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account["test_paths"]

    account_spec = (
        ROOT / "specs" / "capabilities" / "CAP-XY-ACCOUNT.md"
    ).read_text(encoding="utf-8")

    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account_spec
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account_spec

    message = registry[MESSAGE_CAPABILITY]
    assert message["status"] == "planned"
    assert message["owner_module"] == "worker.message"
    assert message["specification"] == "specs/capabilities/CAP-XY-MESSAGE.md"
    assert message["implementation_paths"] == []
    assert message["test_paths"] == []
    assert message["active_change"] is None
    assert message["last_verified_commit"] is None

    message_spec = (
        ROOT / "specs" / "capabilities" / "CAP-XY-MESSAGE.md"
    ).read_text(encoding="utf-8")

    assert "without opening a real WebSocket" in message_spec
    assert "Status remains planned." in message_spec

    forbidden_message_paths = [
        ROOT / "app" / "xianyu_system" / "worker" / "message.py",
        ROOT / "app" / "xianyu_system" / "worker" / "message",
        ROOT / "worker" / "message.py",
        ROOT / "worker" / "message",
    ]

    assert not any(path.exists() for path in forbidden_message_paths)
    assert not list((ROOT / "migrations" / "versions").glob("*message*"))

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for forbidden in [
        "Cookie=",
        "Token=",
        "Secret=",
        "Password=",
        "Session=",
    ]:
        assert forbidden not in env_example

    proposal = (CHG_0004 / "proposal.md").read_text(encoding="utf-8")
    design = (CHG_0004 / "design.md").read_text(encoding="utf-8")
    acceptance = (CHG_0004 / "acceptance.md").read_text(encoding="utf-8")

    assert "T1 through T3 are complete." in proposal
    assert (
        "The canonical terminology and the transport, "
        "authentication, Credential-resolution"
        in proposal
    )
    assert "T4 is the next executable task" in proposal

    required_sections = [
        "## Approved transport boundary",
        "## Authentication and Credential boundary",
        "## Credential Resolution Status",
        "## Operation Authorization Status",
        "## Risk Decision",
        "## Connection authorization invariant",
        "## Platform verification and risk-control boundary",
        "## Reconnect and retry safety",
        "## Acknowledgement safety boundary",
        "## Logging, errors, and redaction",
        "## Approved non-secret reason-code classes",
        "## Security testing boundary",
        "## Decisions deferred after T3",
    ]

    for marker in required_sections:
        assert marker in design

    assert "The connection uses `wss://`." in design
    assert "Plaintext `ws://` is prohibited." in design
    assert "TLS certificate verification remains enabled." in design
    assert "TLS hostname verification remains enabled." in design

    assert (
        "Credential Resolution Status = RESOLVED"
        in design
    )
    assert (
        "Operation Authorization Status = AUTHORIZED"
        in design
    )
    assert "Risk Decision = ALLOWED" in design

    assert (
        "`VERIFICATION_REQUIRED` must stop the operation."
        in design
    )
    assert (
        "Reconnect must not be treated as permission to change "
        "Profile, Account Reference, Credential Reference"
        in design
    )
    assert (
        "Acknowledgement remains a transport-level receipt concept."
        in design
    )
    assert (
        "Message Content must never appear in logs or diagnostics."
        in design
    )
    assert (
        "Tests must not perform HTTP or WebSocket requests."
        in design
    )

    assert "T1 through T3 are complete." in acceptance
    assert "T4 is the next executable task" in acceptance
    assert "PR #4 remains Draft" in acceptance
