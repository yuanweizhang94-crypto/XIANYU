from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_contributing_documents_change_transition_rules() -> None:
    text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "Starting the next change" in text
    assert "changes/archive/" in text
    assert "changes/active/<change-id>/tests/" in text
    assert "default pytest" in text
    assert "audit only" in text
    assert "ARCHIVED" in text
    assert "generated/PROJECT_STATE.json" in text


def test_change_transition_runbook_exists_and_documents_invariants() -> None:
    text = (ROOT / "docs" / "runbooks" / "change-transition.md").read_text(encoding="utf-8")
    assert "Atomic transition steps" in text
    assert "changes/active/" in text
    assert "changes/archive/" in text
    assert "changes/active/<change-id>/tests/" in text
    assert "default pytest" in text
    assert "historical audit evidence only" in text
    assert "ARCHIVED" in text
    assert "DRAFT" in text
