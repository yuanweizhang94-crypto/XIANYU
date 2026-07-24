from __future__ import annotations

import ast
import json
from pathlib import Path

import yaml
from alembic.script import ScriptDirectory

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
    "changes/archive/CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)
ACCOUNT_ACTIVE_ACCEPTANCE = (
    "changes/active/CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)
MESSAGE_PACKAGE = ROOT / "app" / "xianyu_system" / "worker" / "message"
MESSAGE_MIGRATION = ROOT / "migrations" / "versions" / "0003_xianyu_message_boundary.py"


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


def top_level_test_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]


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


def test_chg_0004_t7_adds_permanent_message_boundary_coverage() -> None:
    task_lines = [
        line
        for line in (CHG_0004 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]
    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:7])
    assert all(line.startswith("- [ ]") for line in task_lines[7:])

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["completed"] == 7
    assert state["tasks"]["next_task"] == (
        "T8 Update capability evidence and run complete verification"
    )

    expected_counts = {
        ROOT / "tests" / "unit" / "test_message_domain.py": 12,
        ROOT / "tests" / "unit" / "test_message_service.py": 9,
        ROOT / "tests" / "unit" / "test_message_worker.py": 8,
        ROOT / "tests" / "contract" / "test_message_persistence.py": 8,
        ROOT / "tests" / "contract" / "test_message_security.py": 5,
    }
    assert sum(expected_counts.values()) == 42
    for path, expected_count in expected_counts.items():
        assert path.is_file()
        assert not path.read_bytes().startswith(b"\xef\xbb\xbf")
        assert len(top_level_test_names(path)) == expected_count
        source = path.read_text(encoding="utf-8")
        for forbidden in [
            "pytest.mark.parametrize",
            "pytest.param",
            "pytest_generate_tests",
            "pytest.skip",
            "pytest.xfail",
            "time.sleep",
            "asyncio.sleep",
        ]:
            assert forbidden not in source

    assert len(top_level_test_names(ROOT / "tests" / "unit" / "test_import_safety.py")) == 3
    import_safety_source = (ROOT / "tests" / "unit" / "test_import_safety.py").read_text(
        encoding="utf-8"
    )
    assert '"xianyu_system.worker.message"' in import_safety_source
    assert '"xianyu_system.worker.message.domain"' in import_safety_source
    assert '"xianyu_system.worker.message.transport"' in import_safety_source

    proposal = (CHG_0004 / "proposal.md").read_text(encoding="utf-8")
    design = (CHG_0004 / "design.md").read_text(encoding="utf-8")
    acceptance = (CHG_0004 / "acceptance.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "T1 through T7 are complete." in proposal
    assert "T7 permanent Message test coverage is complete." in design
    assert "## T7 acceptance criteria" in acceptance
    assert "T7 dedicated unit, contract, security, and active-change acceptance tests are complete." in readme
    assert MESSAGE_PACKAGE.is_dir()
    assert MESSAGE_MIGRATION.is_file()


def test_message_capability_remains_planned_and_unbound_after_t7() -> None:
    registry = registry_by_id()
    account = registry[ACCOUNT_CAPABILITY]
    assert account["status"] == "verified"
    assert account["active_change"] is None
    assert account["last_verified_commit"] == ACCOUNT_VERIFIED_CANDIDATE_SHA
    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account["test_paths"]
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account["test_paths"]

    account_spec = (ROOT / "specs" / "capabilities" / "CAP-XY-ACCOUNT.md").read_text(
        encoding="utf-8"
    )
    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account_spec
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account_spec

    message = registry[MESSAGE_CAPABILITY]
    assert message["status"] == "planned"
    assert message["owner_module"] == "worker.message"
    assert message["implementation_paths"] == []
    assert message["test_paths"] == []
    assert message["active_change"] is None
    assert message["last_verified_commit"] is None

    message_spec = (ROOT / "specs" / "capabilities" / "CAP-XY-MESSAGE.md").read_text(
        encoding="utf-8"
    )
    assert "without opening a real WebSocket" in message_spec
    assert "Status remains planned." in message_spec

    script = ScriptDirectory.from_config(
        __import__(
            "xianyu_system.core.database",
            fromlist=["build_alembic_config"],
        ).build_alembic_config()
    )
    assert script.get_current_head() == "0003_xianyu_message_boundary"
