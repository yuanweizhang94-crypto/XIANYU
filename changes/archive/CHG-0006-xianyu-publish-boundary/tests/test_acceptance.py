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
PUBLISH_EVIDENCE_CANDIDATE_SHA = "66ac5134e0f62b9b30b7423e7bebab297c5ced7a"
T9_READY_CANDIDATE_SHA = "52e389e804ca24f144c6c1bd73cc21b1ba21d4cb"
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
    "app/xianyu_system/worker/publish/adapter.py",
    "app/xianyu_system/worker/publish/browser.py",
    "app/xianyu_system/worker/publish/playwright.py",
    "app/xianyu_system/worker/publish/client.py",
    "app/xianyu_system/worker/publish/xianyu.py",
    "app/xianyu_system/worker/publish/worker.py",
    "app/xianyu_system/worker/publish/scheduler.py",
    "app/xianyu_system/worker/publish/uploader.py",
    "app/xianyu_system/worker/publish/credential.py",
    "app/xianyu_system/worker/publish/api.py",
    "app/xianyu_system/publish",
    "worker/publish",
    "adapters/xianyu",
)


EXPECTED_TASKS = [
    "T1 Obtain explicit project-owner approval for CHG-0006",
    "T2 Finalize listing, publish request, attempt, and outcome terminology",
    "T3 Approve permission, credential, risk-control, and platform boundaries",
    "T4 Approve validation, idempotency, duplicate, and uncertainty boundaries",
    "T5 Approve ownership, persistence, lifecycle, audit, and failure boundaries",
    "T6 Implement only the separately approved local publishing boundary",
    "T7 Add unit, contract, security, and active-change acceptance tests",
    "T8 Update capability evidence and run complete verification",
    "T9 Complete final PR administration",
]
NEXT_BY_COMPLETED = {
    1: EXPECTED_TASKS[1],
    2: EXPECTED_TASKS[2],
    3: EXPECTED_TASKS[3],
    4: EXPECTED_TASKS[4],
    5: EXPECTED_TASKS[5],
    6: EXPECTED_TASKS[6],
    7: EXPECTED_TASKS[7],
    8: EXPECTED_TASKS[8],
    9: None,
}


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



def completed_count() -> int:
    lines = task_lines()
    assert len(lines) == 9
    marks = [line.startswith("- [x]") for line in lines]
    completed = sum(marks)
    assert 1 <= completed <= 9
    assert marks == [index < completed for index in range(9)]
    assert [line[6:] for line in lines] == EXPECTED_TASKS
    return completed

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


def test_chg_0006_is_the_only_active_change_with_expected_status() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())
    assert active_dirs == ["CHG-0006-xianyu-publish-boundary"]
    state_status = str(project_state()["active_change"]["status"])
    assert state_status in {"APPROVED", "VERIFYING"}
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = CHG_0006 / name
        assert path.is_file()
        assert status_of(path) == state_status
        assert "Change ID: CHG-0006-xianyu-publish-boundary" in path.read_text(
            encoding="utf-8"
        )
    assert (CHG_0006 / "tests" / "test_acceptance.py").is_file()


def test_chg_0006_tasks_are_a_contiguous_prefix_with_expected_next_task() -> None:
    completed = completed_count()
    state = project_state()
    assert state["active_change"] == {
        "id": "CHG-0006-xianyu-publish-boundary",
        "status": status_of(CHG_0006 / "tasks.md"),
        "path": "changes/active/CHG-0006-xianyu-publish-boundary",
    }
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == completed
    assert state["tasks"]["next_task"] == NEXT_BY_COMPLETED[completed]
    assert [item["text"] for item in state["tasks"]["items"]] == EXPECTED_TASKS
    assert [item["completed"] for item in state["tasks"]["items"]] == [
        index < completed for index in range(9)
    ]

EXPECTED_PUBLISH_IMPLEMENTATION_PATHS = [
    "app/xianyu_system/worker/publish/__init__.py",
    "app/xianyu_system/worker/publish/domain.py",
    "app/xianyu_system/worker/publish/fingerprint.py",
    "app/xianyu_system/worker/publish/validation.py",
    "app/xianyu_system/worker/publish/persistence.py",
    "app/xianyu_system/worker/publish/service.py",
    "migrations/versions/0005_xianyu_publish_boundary.py",
]
EXPECTED_PUBLISH_TEST_PATHS = [
    "tests/unit/test_publish_domain.py",
    "tests/unit/test_publish_fingerprint.py",
    "tests/unit/test_publish_validation.py",
    "tests/unit/test_publish_service.py",
    "tests/unit/test_import_safety.py",
    "tests/contract/test_publish_persistence.py",
    "tests/contract/test_publish_security.py",
    "tests/contract/test_migrations.py",
    "tests/contract/test_capability_registry.py",
    "changes/active/CHG-0006-xianyu-publish-boundary/tests/test_acceptance.py",
]


def test_cap_xy_publish_state_matches_current_t8_phase() -> None:
    publish = registry_by_id()[PUBLISH_CAPABILITY]
    completed = completed_count()
    state = project_state()
    publish_state = {
        str(item["id"]): item for item in state["capabilities"]["items"]
    }[PUBLISH_CAPABILITY]

    if completed < 7:
        assert publish["status"] == "planned"
        assert publish["implementation_paths"] == []
        assert publish["test_paths"] == []
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] is None
        assert state["capabilities"]["by_status"] == {"planned": 4, "verified": 6}
    elif completed == 7:
        assert publish["status"] == "implementing"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] == "CHG-0006-xianyu-publish-boundary"
        assert publish["last_verified_commit"] is None
        assert state["capabilities"]["by_status"] == {
            "planned": 3,
            "implementing": 1,
            "verified": 6,
        }
    else:
        assert completed >= 8
        assert publish["status"] == "verified"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] == PUBLISH_EVIDENCE_CANDIDATE_SHA
        assert state["capabilities"]["by_status"] == {"planned": 3, "verified": 7}

    assert publish_state == publish


def test_approved_documents_keep_publish_runtime_unapproved() -> None:
    completed = completed_count()
    combined = "\n".join(
        (CHG_0006 / name).read_text(encoding="utf-8")
        for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
    )
    required_governance = ["T1 is complete"]
    if NEXT_BY_COMPLETED[completed] is not None:
        required_governance.append(str(NEXT_BY_COMPLETED[completed]))
    else:
        required_governance.append("All nine tasks")
    for required in required_governance:
        assert required in combined
    if completed >= 2:
        for required in ["ListingDraft", "PublishRequest", "PublishDecisionType"]:
            assert required in combined
    if completed >= 3:
        for required in ["PublishAuthorizationState", "PublishRiskState", "fail closed"]:
            assert required in combined
    if completed >= 4:
        for required in ["IDEMPOTENCY_REPLAY", "IDEMPOTENCY_CONFLICT", "UNKNOWN_PREVIOUS_OUTCOME"]:
            assert required in combined
    if completed >= 5:
        for required in ["worker.publish", "ListingDraftLifecycle", "Failure classification"]:
            assert required in combined
    if completed < 6:
        for required in ["T6 implementation is not authorized", "Current implementation: none"]:
            assert required in combined
    if completed >= 6:
        for required in ["T6 is complete", "PublishService", "0005_xianyu_publish_boundary"]:
            assert required in combined
    if completed >= 7:
        for required in [
            "T7 is complete",
            "test_publish_domain.py",
            "test_publish_persistence.py",
            "CAP-XY-PUBLISH remains planned and unbound until T8",
        ]:
            assert required in combined
    for forbidden_path in FORBIDDEN_PUBLISH_PATH_PREFIXES:
        assert not (ROOT / forbidden_path).exists()

def test_transition_readme_documents_final_state() -> None:
    completed = completed_count()
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in [
        "PR #5 was merged into `main`.",
        PR_5_MERGE_COMMIT,
        CHG_0005_FEATURE_HEAD,
        "CHG-0005-xianyu-reply-boundary is archived.",
        "CAP-XY-REPLY remains verified.",
        REPLY_EVIDENCE_CANDIDATE,
        "CHG-0006-xianyu-publish-boundary is the only Active Change.",
        f"CHG-0006 status is `{status_of(CHG_0006 / 'tasks.md')}`.",
        f"CHG-0006 completed tasks: {completed} / 9.",
        (f"Next task: `{NEXT_BY_COMPLETED[completed]}`." if NEXT_BY_COMPLETED[completed] is not None else "Next task: none."),
        (
            "T6 is not authorized and has not started."
            if completed < 6
            else (
                "T7 is not authorized and has not started."
                if completed < 7
                else (
                    "T7 permanent local Publish boundary testing is complete."
                    if completed < 8
                    else "T8 capability evidence verification is complete."
                )
            )
        ),
        (
            "CAP-XY-PUBLISH remains planned and unbound."
            if completed < 7
            else (
                "CAP-XY-PUBLISH is registered as implementing for the T8 Evidence Candidate."
                if completed == 7
                else "CAP-XY-PUBLISH evidence paths are registered and verified."
            )
        ),
        "The T6 implementation performs only local deterministic publish-boundary decisions and introduces no Playwright, browser automation, real Xianyu access, listing publication, media upload, credential access, real data access, or external network access.",
    ]:
        assert required in text
    if completed >= 8:
        assert PUBLISH_EVIDENCE_CANDIDATE_SHA in text
    if completed == 8:
        assert "T9 remains incomplete" in text or "T9 is not authorized and has not started." in text
        assert "PR #6 remains Draft" in text
    if completed == 9:
        assert "CHG-0006 final PR administration is complete." in text
        assert "PR #6 is Ready for review, open and unmerged." in text

def test_no_forbidden_transition_file_scope_or_publish_implementation() -> None:
    completed = completed_count()
    for path in FORBIDDEN_PUBLISH_PATH_PREFIXES:
        assert not (ROOT / path).exists()
    if completed < 6:
        assert not any((ROOT / "migrations" / "versions").glob("*publish*"))
    else:
        for relative_path in [
            "app/xianyu_system/worker/publish/__init__.py",
            "app/xianyu_system/worker/publish/domain.py",
            "app/xianyu_system/worker/publish/fingerprint.py",
            "app/xianyu_system/worker/publish/validation.py",
            "app/xianyu_system/worker/publish/persistence.py",
            "app/xianyu_system/worker/publish/service.py",
            "migrations/versions/0005_xianyu_publish_boundary.py",
        ]:
            assert (ROOT / relative_path).is_file()
    assert not any((ROOT / ".github" / "workflows").glob("*publish*"))

    tracked_publish_mentions = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".toml"}
        and any(prefix in path.relative_to(ROOT).as_posix() for prefix in ["publish_boundary"])
    ]
    if completed >= 6:
        tracked_publish_mentions = [
            path
            for path in tracked_publish_mentions
            if path != "migrations/versions/0005_xianyu_publish_boundary.py"
        ]
    assert tracked_publish_mentions == []


def test_t6_runtime_exists_without_registry_evidence_or_platform_modules() -> None:
    completed = completed_count()
    if completed < 6:
        return
    for relative_path in [
        "app/xianyu_system/worker/publish/__init__.py",
        "app/xianyu_system/worker/publish/domain.py",
        "app/xianyu_system/worker/publish/fingerprint.py",
        "app/xianyu_system/worker/publish/validation.py",
        "app/xianyu_system/worker/publish/persistence.py",
        "app/xianyu_system/worker/publish/service.py",
        "migrations/versions/0005_xianyu_publish_boundary.py",
    ]:
        assert (ROOT / relative_path).is_file()

    combined = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in [
            "app/xianyu_system/worker/publish/domain.py",
            "app/xianyu_system/worker/publish/validation.py",
            "app/xianyu_system/worker/publish/service.py",
        ]
    )
    for required in [
        "PublishDecisionType",
        "PublishReasonCode",
        "PublishAuthorizationState",
        "PublishRiskState",
        "ListingDraftLifecycle",
        "PublishRequestLifecycle",
        "PublishFailureCategory",
        "IDEMPOTENCY_REPLAY",
        "IDEMPOTENCY_CONFLICT",
        "DUPLICATE_DRAFT",
        "UNKNOWN_PREVIOUS_OUTCOME",
        "READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY",
    ]:
        assert required in combined
    for forbidden in ["PUBLISHED =", "PUBLISHING", "LIVE", "ONLINE"]:
        assert forbidden not in combined

    publish = registry_by_id()[PUBLISH_CAPABILITY]
    if completed == 6:
        assert publish["status"] == "planned"
        assert publish["implementation_paths"] == []
        assert publish["test_paths"] == []
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] is None
    elif completed == 7:
        assert publish["status"] == "implementing"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] == "CHG-0006-xianyu-publish-boundary"
        assert publish["last_verified_commit"] is None
    else:
        assert completed >= 8
        assert publish["status"] == "verified"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] == PUBLISH_EVIDENCE_CANDIDATE_SHA


def test_project_state_and_registry_capability_totals_are_consistent() -> None:
    state = project_state()
    registry = registry_by_id()
    assert len(registry) == 10
    assert state["capabilities"]["total"] == 10
    completed = completed_count()
    if completed < 7:
        assert state["capabilities"]["by_status"] == {"planned": 4, "verified": 6}
    elif completed == 7:
        assert state["capabilities"]["by_status"] == {
            "planned": 3,
            "implementing": 1,
            "verified": 6,
        }
    else:
        assert completed >= 8
        assert state["capabilities"]["by_status"] == {"planned": 3, "verified": 7}
    assert sorted(registry) == sorted(item["id"] for item in state["capabilities"]["items"])


def test_t7_permanent_publish_tests_exist_and_registry_remains_unbound() -> None:
    completed = completed_count()
    if completed < 7:
        return
    expected_test_files = [
        "tests/unit/test_publish_domain.py",
        "tests/unit/test_publish_fingerprint.py",
        "tests/unit/test_publish_validation.py",
        "tests/unit/test_publish_service.py",
        "tests/contract/test_publish_persistence.py",
        "tests/contract/test_publish_security.py",
        "tests/unit/test_import_safety.py",
        "tests/contract/test_migrations.py",
        "changes/active/CHG-0006-xianyu-publish-boundary/tests/test_acceptance.py",
    ]
    for relative_path in expected_test_files:
        path = ROOT / relative_path
        assert path.is_file()
        text = path.read_text(encoding="utf-8")
        assert "publish" in text.lower()

    publish = registry_by_id()[PUBLISH_CAPABILITY]
    if completed == 6:
        assert publish["status"] == "planned"
        assert publish["implementation_paths"] == []
        assert publish["test_paths"] == []
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] is None
    elif completed == 7:
        assert publish["status"] == "implementing"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] == "CHG-0006-xianyu-publish-boundary"
        assert publish["last_verified_commit"] is None
    else:
        assert completed >= 8
        assert publish["status"] == "verified"
        assert publish["implementation_paths"] == EXPECTED_PUBLISH_IMPLEMENTATION_PATHS
        assert publish["test_paths"] == EXPECTED_PUBLISH_TEST_PATHS
        assert publish["active_change"] is None
        assert publish["last_verified_commit"] == PUBLISH_EVIDENCE_CANDIDATE_SHA



def test_t9_governance_state_matches_review_phase() -> None:
    completed = completed_count()
    status = status_of(CHG_0006 / "tasks.md")
    if completed < 8:
        return
    assert status in {"APPROVED", "VERIFYING"}
    publish = registry_by_id()[PUBLISH_CAPABILITY]
    assert publish["status"] == "verified"
    assert publish["active_change"] is None
    assert publish["last_verified_commit"] == PUBLISH_EVIDENCE_CANDIDATE_SHA
    combined = "\n".join(
        (CHG_0006 / name).read_text(encoding="utf-8")
        for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
    )
    if status == "VERIFYING" and completed == 8:
        assert "T9 Ready Candidate" in combined
        assert "T9 remains incomplete" in combined
        assert project_state()["tasks"]["next_task"] == EXPECTED_TASKS[8]
    if completed == 9:
        assert status == "VERIFYING"
        assert project_state()["tasks"]["next_task"] is None
        assert T9_READY_CANDIDATE_SHA in combined
        assert "Ready for review" in combined
        assert "open, and unmerged" in combined
        assert "Merge requires separate" in combined
