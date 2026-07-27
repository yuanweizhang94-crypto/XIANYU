from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"

CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ARCHIVE / "CHG-0003-xianyu-account-boundary"
CHG_0004 = ARCHIVE / "CHG-0004-xianyu-message-boundary"
CHG_0005 = ACTIVE / "CHG-0005-xianyu-reply-boundary"

MESSAGE_CAPABILITY = "CAP-XY-MESSAGE"
REPLY_CAPABILITY = "CAP-XY-REPLY"

MESSAGE_VERIFIED_CANDIDATE_SHA = (
    "49498e6f30944883c1a0a5a504932bbd02fc86de"
)

MESSAGE_ARCHIVED_ACCEPTANCE = (
    "changes/archive/"
    "CHG-0004-xianyu-message-boundary/"
    "tests/test_acceptance.py"
)

MESSAGE_ACTIVE_ACCEPTANCE = (
    "changes/active/"
    "CHG-0004-xianyu-message-boundary/"
    "tests/test_acceptance.py"
)


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8")
    )
    return {str(item["id"]): item for item in registry["capabilities"]}


def test_completed_changes_are_archived_with_history_preserved() -> None:
    for change in [CHG_0002, CHG_0003, CHG_0004]:
        assert change.is_dir()
        assert not (ACTIVE / change.name).exists()
        for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
            assert status_of(change / name) == "ARCHIVED"
        assert (change / "tests" / "test_acceptance.py").is_file()

    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        text = (CHG_0004 / name).read_text(encoding="utf-8")
        assert "Merge and archive record" in text
        assert "bab7a1a86239cb4dba9b2f7dc8db0ff33bc80dc6" in text
        assert "0cfd719dff5d472e9e5ac26bf720afc7efb74e9f" in text
        assert "CHG-0005 is a DRAFT preparation only" in text


def test_chg_0005_is_the_only_draft_active_change() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())
    assert active_dirs == ["CHG-0005-xianyu-reply-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0005 / name) == "APPROVED"


def test_chg_0005_tasks_and_generated_state_are_draft_only() -> None:
    task_lines = [
        line
        for line in (CHG_0005 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]
    assert len(task_lines) == 9
    assert task_lines[0] == "- [x] T1 Obtain explicit project-owner approval for CHG-0005"
    assert all(line.startswith("- [ ]") for line in task_lines[1:])

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] == {
        "id": "CHG-0005-xianyu-reply-boundary",
        "status": "APPROVED",
        "path": "changes/active/CHG-0005-xianyu-reply-boundary",
    }
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 1
    assert state["tasks"]["next_task"] == "T2 Finalize reply rule, template, and decision terminology"
    assert state["tasks"]["items"][0]["completed"] is True
    assert all(item["completed"] is False for item in state["tasks"]["items"][1:])
    assert state["capabilities"]["by_status"] == {"planned": 5, "verified": 5}


def test_reply_capability_remains_planned_and_unimplemented() -> None:
    registry = registry_by_id()
    message = registry[MESSAGE_CAPABILITY]
    reply = registry[REPLY_CAPABILITY]

    assert message["status"] == "verified"
    assert message["active_change"] is None
    assert message["last_verified_commit"] == MESSAGE_VERIFIED_CANDIDATE_SHA
    assert len(message["implementation_paths"]) == 7
    assert len(message["test_paths"]) == 10
    assert MESSAGE_ARCHIVED_ACCEPTANCE in message["test_paths"]
    assert MESSAGE_ACTIVE_ACCEPTANCE not in message["test_paths"]

    assert reply["status"] == "planned"
    assert reply["owner_module"] == "app.reply"
    assert reply["specification"] == "specs/capabilities/CAP-XY-REPLY.md"
    assert reply["implementation_paths"] == []
    assert reply["test_paths"] == []
    assert reply["active_change"] is None
    assert reply["last_verified_commit"] is None

    forbidden_reply_paths = [
        ROOT / "app" / "xianyu_system" / "reply.py",
        ROOT / "app" / "xianyu_system" / "reply",
        ROOT / "app" / "xianyu_system" / "worker" / "reply.py",
        ROOT / "app" / "xianyu_system" / "worker" / "reply",
    ]
    assert not any(path.exists() for path in forbidden_reply_paths)
    assert not list((ROOT / "migrations" / "versions").glob("*reply*"))
    assert not list((ROOT / "tests" / "unit").glob("*reply*"))
    assert not list((ROOT / "tests" / "contract").glob("*reply*"))

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for forbidden in [
        "Cookie=",
        "Token=",
        "Secret=",
        "Password=",
        "Session=",
        "Customer=",
        "Reply_API=",
        "AI_API=",
        "WECOM=",
    ]:
        assert forbidden not in env_example

    documents = [
        (CHG_0005 / "proposal.md").read_text(encoding="utf-8"),
        (CHG_0005 / "design.md").read_text(encoding="utf-8"),
        (CHG_0005 / "acceptance.md").read_text(encoding="utf-8"),
    ]
    joined = "\n".join(documents)
    for required in [
        "APPROVED",
        "No real Xianyu message sending",
        "No WeCom integration",
        "No AI Provider",
        "Synthetic Fixtures",
        "Fail closed",
    ]:
        assert required in joined
