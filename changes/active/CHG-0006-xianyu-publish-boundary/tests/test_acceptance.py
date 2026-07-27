from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"

CHG_0005 = ARCHIVE / "CHG-0005-xianyu-reply-boundary"
CHG_0006 = ACTIVE / "CHG-0006-xianyu-publish-boundary"

REPLY_CAPABILITY = "CAP-XY-REPLY"
PUBLISH_CAPABILITY = "CAP-XY-PUBLISH"
PR_5_MERGE_COMMIT = "f00156045d75e632d71ade640a85a4c522568158"
CHG_0005_FEATURE_HEAD = "c4f7a3a3d14e34e5ebdaf6abd79587d45137f587"
REPLY_EVIDENCE_CANDIDATE = "5724d164619c64e93295595b3acdd1429d24e3e0"
REPLY_ARCHIVE_ACCEPTANCE = (
    "changes/archive/CHG-0005-xianyu-reply-boundary/tests/test_acceptance.py"
)
REPLY_ACTIVE_ACCEPTANCE = (
    "changes/active/CHG-0005-xianyu-reply-boundary/tests/test_acceptance.py"
)
EXPECTED_REPLY_IMPLEMENTATION_PATHS = [
    "app/xianyu_system/reply/__init__.py",
    "app/xianyu_system/reply/domain.py",
    "app/xianyu_system/reply/evaluator.py",
    "app/xianyu_system/reply/renderer.py",
    "app/xianyu_system/reply/mapper.py",
    "app/xianyu_system/reply/persistence.py",
    "app/xianyu_system/reply/service.py",
    "migrations/versions/0004_xianyu_reply_boundary.py",
]
EXPECTED_REPLY_TEST_PATHS = [
    "tests/unit/test_reply_domain.py",
    "tests/unit/test_reply_evaluator.py",
    "tests/unit/test_reply_renderer.py",
    "tests/unit/test_reply_mapper.py",
    "tests/unit/test_reply_service.py",
    "tests/unit/test_import_safety.py",
    "tests/contract/test_reply_persistence.py",
    "tests/contract/test_reply_security.py",
    "tests/contract/test_migrations.py",
    "tests/contract/test_core_runtime.py",
    "tests/contract/test_capability_registry.py",
    REPLY_ARCHIVE_ACCEPTANCE,
]
ALLOWED_TRANSITION_PATH_PREFIXES = (
    "README.md",
    "changes/archive/CHG-0005-xianyu-reply-boundary/",
    "changes/active/CHG-0006-xianyu-publish-boundary/",
    "specs/CAPABILITY_REGISTRY.yaml",
    "specs/capabilities/CAP-XY-REPLY.md",
    "generated/PROJECT_STATE.json",
    "tests/contract/test_capability_registry.py",
)
FORBIDDEN_PUBLISH_PATH_PREFIXES = (
    "app/xianyu_system/worker/publish",
    "app/xianyu_system/publish",
    "worker/publish",
    "adapters/xianyu",
)


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, Any]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8")
    )
    return {str(item["id"]): cast(dict[str, Any], item) for item in registry["capabilities"]}


def project_state() -> dict[str, Any]:
    return json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))


def task_lines() -> list[str]:
    return [
        line
        for line in (CHG_0006 / "tasks.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]


def test_chg_0005_is_archived_with_history_and_merge_record() -> None:
    assert not (ACTIVE / "CHG-0005-xianyu-reply-boundary").exists()
    assert CHG_0005.is_dir()
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = CHG_0005 / name
        assert path.is_file()
        assert status_of(path) == "ARCHIVED"
        text = path.read_text(encoding="utf-8")
        assert "PR #5" in text
        assert "merged" in text
        assert CHG_0005_FEATURE_HEAD in text
        assert PR_5_MERGE_COMMIT in text
        assert "normal two-parent merge commit" in text
    assert (CHG_0005 / "tests" / "test_acceptance.py").is_file()


def test_cap_xy_reply_evidence_is_frozen_and_points_to_archive() -> None:
    reply = registry_by_id()[REPLY_CAPABILITY]
    assert reply["status"] == "verified"
    assert reply["owner_module"] == "app.reply"
    assert reply["active_change"] is None
    assert reply["last_verified_commit"] == REPLY_EVIDENCE_CANDIDATE
    assert reply["implementation_paths"] == EXPECTED_REPLY_IMPLEMENTATION_PATHS
    assert reply["test_paths"] == EXPECTED_REPLY_TEST_PATHS
    assert REPLY_ACTIVE_ACCEPTANCE not in reply["test_paths"]
    assert REPLY_ARCHIVE_ACCEPTANCE in reply["test_paths"]

    spec_text = (ROOT / "specs" / "capabilities" / "CAP-XY-REPLY.md").read_text(
        encoding="utf-8"
    )
    assert "Registry status: verified" in spec_text
    assert REPLY_EVIDENCE_CANDIDATE in spec_text
    assert f"`{REPLY_ARCHIVE_ACCEPTANCE}`" in spec_text
    assert REPLY_ACTIVE_ACCEPTANCE not in spec_text


def test_chg_0006_is_the_only_draft_active_change() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())
    assert active_dirs == ["CHG-0006-xianyu-publish-boundary"]
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = CHG_0006 / name
        assert path.is_file()
        assert status_of(path) == "DRAFT"
        assert "Change ID: CHG-0006-xianyu-publish-boundary" in path.read_text(
            encoding="utf-8"
        )
    assert (CHG_0006 / "tests" / "test_acceptance.py").is_file()


def test_chg_0006_has_zero_of_nine_tasks_and_no_next_task() -> None:
    tasks = task_lines()
    assert len(tasks) == 9
    assert all(line.startswith("- [ ]") for line in tasks)
    assert tasks[0] == "- [ ] T1 Obtain explicit project-owner approval for CHG-0006"
    assert tasks[5] == "- [ ] T6 Implement only the separately approved local publishing boundary"
    assert tasks[7] == "- [ ] T8 Update capability evidence and run complete verification"
    assert tasks[8] == "- [ ] T9 Complete final PR administration"

    state = project_state()
    assert state["active_change"] == {
        "id": "CHG-0006-xianyu-publish-boundary",
        "status": "DRAFT",
        "path": "changes/active/CHG-0006-xianyu-publish-boundary",
    }
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None
    assert all(item["completed"] is False for item in state["tasks"]["items"])


def test_cap_xy_publish_remains_planned_unbound_and_empty() -> None:
    publish = registry_by_id()[PUBLISH_CAPABILITY]
    assert publish["status"] == "planned"
    assert publish["implementation_paths"] == []
    assert publish["test_paths"] == []
    assert publish["active_change"] is None
    assert publish["last_verified_commit"] is None

    state = project_state()
    publish_state = {
        str(item["id"]): item for item in state["capabilities"]["items"]
    }[PUBLISH_CAPABILITY]
    assert publish_state["status"] == "planned"
    assert publish_state["implementation_paths"] == []
    assert publish_state["test_paths"] == []
    assert publish_state["active_change"] is None
    assert publish_state["last_verified_commit"] is None
    assert state["capabilities"]["by_status"] == {"planned": 4, "verified": 6}


def test_draft_documents_keep_publish_runtime_unapproved() -> None:
    combined = "\n".join(
        (CHG_0006 / name).read_text(encoding="utf-8")
        for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
    )
    for required in [
        "No CHG-0006 task is approved",
        "T1 has not started",
        "DRAFT state has no executable next task",
        "Moving beyond DRAFT requires separate explicit project-owner approval",
        "No Runtime design is approved",
        "No Playwright or external platform behavior is approved",
        "Current implementation: none",
    ]:
        assert required in combined
    for forbidden_path in FORBIDDEN_PUBLISH_PATH_PREFIXES:
        assert not (ROOT / forbidden_path).exists()


def test_transition_readme_documents_final_state() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in [
        "PR #5 was merged into `main`.",
        PR_5_MERGE_COMMIT,
        CHG_0005_FEATURE_HEAD,
        "CHG-0005-xianyu-reply-boundary is archived.",
        "CAP-XY-REPLY remains verified.",
        REPLY_EVIDENCE_CANDIDATE,
        "CHG-0006-xianyu-publish-boundary is the only Active Change.",
        "CHG-0006 status is `DRAFT`.",
        "No CHG-0006 task is complete.",
        "DRAFT has no executable next task.",
        "CAP-XY-PUBLISH remains planned and unbound.",
        "No Playwright, browser automation, real Xianyu access, publishing behavior, credential access, real data access, or external network access is introduced.",
    ]:
        assert required in text


def test_no_forbidden_transition_file_scope_or_publish_implementation() -> None:
    for path in FORBIDDEN_PUBLISH_PATH_PREFIXES:
        assert not (ROOT / path).exists()
    assert not any((ROOT / "migrations" / "versions").glob("*publish*"))
    assert not any((ROOT / ".github" / "workflows").glob("*publish*"))

    tracked_publish_mentions = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".toml"}
        and any(prefix in path.relative_to(ROOT).as_posix() for prefix in ["publish_boundary"])
    ]
    assert tracked_publish_mentions == []


def test_project_state_and_registry_capability_totals_are_consistent() -> None:
    state = project_state()
    registry = registry_by_id()
    assert len(registry) == 10
    assert state["capabilities"]["total"] == 10
    assert state["capabilities"]["by_status"] == {"planned": 4, "verified": 6}
    assert sorted(registry) == sorted(item["id"] for item in state["capabilities"]["items"])
