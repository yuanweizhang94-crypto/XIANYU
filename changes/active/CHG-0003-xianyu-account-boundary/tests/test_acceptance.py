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


def test_chg_0003_t3_completion_advances_only_to_t4() -> None:
    task_lines = [
        line
        for line in (CHG_0003 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]

    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:3])
    assert all(line.startswith("- [ ]") for line in task_lines[3:])

    state = json.loads(
        (ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8")
    )

    assert state["active_change"]["id"] == "CHG-0003-xianyu-account-boundary"
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 3

    assert state["tasks"]["items"][0]["completed"] is True
    assert state["tasks"]["items"][1]["completed"] is True
    assert state["tasks"]["items"][2]["completed"] is True
    assert state["tasks"]["items"][3]["completed"] is False

    assert state["tasks"]["next_task"] == (
        "T4 Approve persistence and migration boundaries"
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

    required_terms = [
        "Platform Account",
        "Account Reference",
        "Profile",
        "Profile Identifier",
        "Account Alias",
        "External Account Identifier",
        "Credential Reference",
        "Session Material",
        "Profile-scoped State",
        "Isolation Boundary",
        "Synthetic Fixture",
    ]
    for term in required_terms:
        assert term in design

    assert "A Profile is not a browser profile" in design
    assert "Each Profile owns exactly one Account Reference." in design
    assert "Each Account Reference belongs to exactly one Profile." in design
    assert "A Credential Reference must never contain a secret value." in design
    assert "Profile-scoped State must not be shared as mutable state across Profiles." in design
    assert "Missing, ambiguous, conflicting, or cross-Profile ownership information must fail closed." in design

    required_sections = [
        "## Security data classification",
        "## Secure Storage Boundary",
        "## Credential Reference security rules",
        "## Future credential resolution boundary",
        "## Credential resolution and authorization states",
        "## Permission and risk boundary",
        "## Logging, errors, and redaction",
        "## Prohibited Secret Material ingress",
        "## Credential lifecycle boundary",
        "## Security testing boundary",
        "## Decisions deferred after T3",
    ]
    for section in required_sections:
        assert section in design

    required_security_rules = [
        "Secret Material must never be committed to the repository.",
        "Each Credential Reference belongs to exactly one Profile.",
        "A Credential Reference must not be shared across Profiles.",
        "There must be no implicit default Credential Reference.",
        "There must be no global current-account credential state.",
        "Do not cache resolved Secret Material across operations.",
        "Do not silently fall back to another Credential Reference.",
        "Credential Resolution Status is RESOLVED",
        "Operation Authorization Status is AUTHORIZED",
        "UNKNOWN must never be treated as AUTHORIZED.",
        "VERIFICATION_REQUIRED must never be bypassed",
        "Secret Material must never appear in logs",
        "Full Credential References must not be logged.",
        "Rotation must not create cross-Profile credential reuse.",
        "Only Synthetic Fixtures may be used.",
    ]
    for rule in required_security_rules:
        assert rule in design

    assert "### Deferred to T4" in design
    assert "### Deferred to T5" in design
    assert "### Deferred to T6" in design

    assert "T1, T2, and T3 are complete." in proposal
    assert "T4 is the next executable task" in proposal
    assert "This execution completes T3 only." in proposal
    assert "T4 must not begin in the same execution." in proposal

    assert "T1, T2, and T3 are complete." in acceptance
    assert "T4 is the next executable task" in acceptance
    assert "PR #3 remains Draft" in acceptance
