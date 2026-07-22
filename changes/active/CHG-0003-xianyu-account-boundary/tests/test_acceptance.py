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


def test_chg_0003_is_the_only_approved_active_change() -> None:
    active_dirs = [path.name for path in ACTIVE.iterdir() if path.is_dir()]
    assert active_dirs == ["CHG-0003-xianyu-account-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_of(CHG_0003 / name) == "APPROVED"


def test_chg_0003_approval_completes_only_t1() -> None:
    task_lines = [
        line
        for line in (CHG_0003 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]

    assert len(task_lines) == 9
    assert task_lines[0].startswith("- [x]")
    assert all(line.startswith("- [ ]") for line in task_lines[1:])

    state = json.loads(
        (ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8")
    )

    assert state["active_change"]["id"] == "CHG-0003-xianyu-account-boundary"
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 1

    assert state["tasks"]["items"][0]["text"] == (
        "T1 Obtain explicit project-owner approval for CHG-0003"
    )
    assert state["tasks"]["items"][0]["completed"] is True

    assert state["tasks"]["items"][1]["text"] == (
        "T2 Finalize account and Profile isolation terminology"
    )
    assert state["tasks"]["items"][1]["completed"] is False

    assert state["tasks"]["next_task"] == (
        "T2 Finalize account and Profile isolation terminology"
    )


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

    proposal = (CHG_0003 / "proposal.md").read_text(encoding="utf-8")
    design = (CHG_0003 / "design.md").read_text(encoding="utf-8")
    acceptance = (CHG_0003 / "acceptance.md").read_text(encoding="utf-8")

    assert "This approval transition completes T1 only." in proposal
    assert "T2 must not begin in the same execution." in proposal

    assert "No runtime account design or implementation has been approved yet." in design
    assert "T2 is the next executable task." in design
    assert "T2 must be performed in a separate execution." in design

    assert "This approval transition completes T1 only." in acceptance
    assert "No runtime implementation" in acceptance
    assert "PR #3 remains Draft" in acceptance
