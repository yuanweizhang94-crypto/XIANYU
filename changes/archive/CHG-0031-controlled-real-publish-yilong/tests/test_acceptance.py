from __future__ import annotations

import re
from pathlib import Path


CHANGE_ID = "CHG-0031-controlled-real-publish-yilong"
MASKED_ACCOUNT = "280***247"
BLOCKER = "HUMAN_BLOCKED_MATERIAL_DATA"
BLOCKED_ACCEPTANCE = "REAL_PUBLISH_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA"


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / "changes").exists():
            return parent
    raise AssertionError("repository root not found")


def _change_dir() -> Path:
    root = _repo_root()
    for base in (root / "changes" / "active", root / "changes" / "archive"):
        candidate = base / CHANGE_ID
        if candidate.exists():
            return candidate
    raise AssertionError(f"{CHANGE_ID} not found")


def _text(name: str) -> str:
    return (_change_dir() / name).read_text(encoding="utf-8")


def test_chg0031_archived_material_data_blocker_is_recorded() -> None:
    combined = "\n".join(
        _text(name)
        for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md")
    )

    assert "Status: ARCHIVED" in _text("proposal.md")
    assert "Status: ARCHIVED" in _text("design.md")
    assert "Status: ARCHIVED" in _text("tasks.md")
    assert "Status: ARCHIVED" in _text("acceptance.md")
    assert "USER_PROVIDED_IDENTITY_BINDING=PASS" in combined
    assert BLOCKER in combined
    assert BLOCKED_ACCEPTANCE in combined
    assert "NO_QUALIFYING_MATERIAL_EXISTS=true" in (_change_dir() / "evidence" / "20260825-active-record-correction.md").read_text(
        encoding="utf-8"
    )
    assert "qualified_candidate_count_with_owner_address=0" in (
        _change_dir() / "evidence" / "20260825-active-record-correction.md"
    ).read_text(encoding="utf-8")
    assert "IDENTITY_UNIQUE=PASS_BY_PROJECT_OWNER_EXTERNAL_SCREENSHOT_ASSERTION_FOR_THIS_RUN" in combined
    assert "GO_RECOMMENDED=false" in combined
    assert "PRODUCTION_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA" in combined
    assert "IDENTITY_BLOCKER_SUPERSEDED=true" in combined


def test_chg0031_zero_action_counters_and_masking_are_preserved() -> None:
    evidence = (_change_dir() / "evidence" / "20260825-active-record-correction.md").read_text(
        encoding="utf-8"
    )
    acceptance = _text("acceptance.md")
    combined = acceptance + "\n" + evidence

    for counter in (
        "PUBLISH_INVOCATIONS=0",
        "FRESH_ITEM_SYNC_INVOCATIONS=0",
        "MESSAGE_SEND_INVOCATIONS=0",
        "AI_INVOCATIONS=0",
        "BROWSER_INVOCATIONS=0",
        "ACCOUNT_MUTATION_COUNT=0",
        "DEPLOY_INVOCATIONS=0",
        "PRODUCTION_MUTATION_COUNT=0",
    ):
        assert counter in combined

    assert MASKED_ACCOUNT in combined
    assert not re.search(r"\b280\d+247\b", combined)
    assert "full_account_id_recorded=false" in evidence
    assert "external_sensitive_evidence_committed=false" in evidence
    assert "Publish and terminal durable readback remain not executed and are not passed" in acceptance


def test_chg0031_publish_tasks_are_not_falsely_marked_as_executed() -> None:
    tasks = _text("tasks.md")

    assert "Do not perform publish" in tasks
    assert "Do not claim terminal platform ACTIVE/readback/item-count +1 acceptance" in tasks
    assert "perform exactly one publish" not in tasks
    assert "prove one platform item ACTIVE" not in tasks
