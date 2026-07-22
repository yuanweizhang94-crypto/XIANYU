from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"
CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ACTIVE / "CHG-0003-xianyu-account-boundary"
CORE_IDS = {"CAP-CORE-CONFIG", "CAP-CORE-DATABASE", "CAP-HEALTH-MONITOR"}


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load((ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8"))
    return {item["id"]: item for item in registry["capabilities"]}


def test_chg_0002_is_archived_with_historical_tests_preserved() -> None:
    assert not (ACTIVE / "CHG-0002-core-application").exists()
    assert CHG_0002.is_dir()
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0002 / name) == "ARCHIVED"
    assert (CHG_0002 / "tests" / "test_acceptance.py").is_file()


def test_chg_0003_is_the_only_draft_active_change() -> None:
    active_dirs = [path.name for path in ACTIVE.iterdir() if path.is_dir()]
    assert active_dirs == ["CHG-0003-xianyu-account-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0003 / name) == "DRAFT"


def test_chg_0003_tasks_and_generated_state_are_draft_only() -> None:
    task_lines = [
        line
        for line in (CHG_0003 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]
    assert len(task_lines) == 9
    assert all(line.startswith("- [ ]") for line in task_lines)

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"]["id"] == "CHG-0003-xianyu-account-boundary"
    assert state["active_change"]["status"] == "DRAFT"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["items"][0]["text"] == "T1 Obtain explicit project-owner approval for CHG-0003"
    assert state["tasks"]["items"][0]["completed"] is False
    assert state["tasks"]["next_task"] is None


def test_account_capability_and_security_boundary_remain_unimplemented() -> None:
    registry = registry_by_id()
    account = registry["CAP-XY-ACCOUNT"]
    assert account["status"] == "planned"
    assert account["active_change"] is None
    assert account["implementation_paths"] == []
    assert account["test_paths"] == []
    assert account["last_verified_commit"] is None

    for capability_id in CORE_IDS:
        capability = registry[capability_id]
        assert capability["status"] == "verified"
        assert "changes/archive/CHG-0002-core-application/tests/test_acceptance.py" in capability["test_paths"]
        assert "changes/active/CHG-0002-core-application/tests/test_acceptance.py" not in capability["test_paths"]

    forbidden_paths = [
        ROOT / "app" / "xianyu_system" / "account.py",
        ROOT / "app" / "xianyu_system" / "account",
        ROOT / "app" / "xianyu_system" / "workers" / "account.py",
        ROOT / "app" / "xianyu_system" / "worker" / "account.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "Cookie=" not in env_example
    assert "Token=" not in env_example
    assert "Secret=" not in env_example
    assert "Password=" not in env_example
