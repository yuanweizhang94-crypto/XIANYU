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

def test_chg_0008_upstream_pilot_governance_facts_are_recorded() -> None:
    roadmap = (ROOT / "specs" / "PRODUCT_ROADMAP.yaml").read_text(encoding="utf-8")
    upstream = (ROOT / "specs" / "UPSTREAM_REGISTRY.yaml").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    archived_acceptance = (
        ROOT / "changes" / "archive" / "CHG-0008-xianyu-upstream-integration-foundation" / "acceptance.md"
    ).read_text(encoding="utf-8")

    assert "current_priority: upstream_wrapper_mvp" in roadmap
    assert "pilot_status: P2_P6_PASSED_WITH_OPERATOR_DELISTED_CLEANUP" in roadmap
    assert "P0_system_startup: PASSED" in roadmap
    assert "P1_manual_scan_login: PASSED" in roadmap
    assert "P6_manual_cleanup: PASSED_OPERATOR_DELISTED_NOT_DELETED" in roadmap
    assert "recommendation: WRAP" in roadmap
    assert "allowed_next_change: CHG-0009-xianyu-upstream-wrapper-mvp" in roadmap
    assert "Status: ARCHIVED" in archived_acceptance
    assert "P2 online state: PASSED" in archived_acceptance
    assert "P6 test listing cleanup: PASSED as operator-delisted cleanup, not deletion" in archived_acceptance
    assert "Final recommendation: `WRAP`" in archived_acceptance
    assert "bda1a859df63fa5f24e51398fa80a23490bb6dfc" in upstream
    assert "AGPL-3.0" in upstream
    assert "5ce38ab2c4236f7eaa65983ce5c2da1f2fbd09af" in upstream
    assert "license: UNRESOLVED" in upstream
    assert "Do not create large adapter abstractions" in agents


def test_chg_0008_does_not_create_local_xianyu_adapter_runtime() -> None:
    assert not (ROOT / "app" / "xianyu_system" / "adapters" / "xianyu").exists()
    for relative in [
        "app/xianyu_system/adapters/xianyu/models.py",
        "app/xianyu_system/adapters/xianyu/ports.py",
        "app/xianyu_system/adapters/xianyu/fake.py",
    ]:
        assert not (ROOT / relative).exists()
