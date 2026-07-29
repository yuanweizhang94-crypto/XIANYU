from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def test_chg_0011_upstream_first_documents_exist() -> None:
    for relative in [
        "docs/UPSTREAM_CAPABILITY_MATRIX.md",
        "docs/LOCAL_COMPONENT_DISPOSITION.md",
        "docs/UPSTREAM_FIRST_POLICY.md",
    ]:
        assert (ROOT / relative).exists()


def test_chg_0011_locks_upstream_first_direction() -> None:
    matrix = (ROOT / "docs" / "UPSTREAM_CAPABILITY_MATRIX.md").read_text(encoding="utf-8")
    policy = (ROOT / "docs" / "UPSTREAM_FIRST_POLICY.md").read_text(encoding="utf-8")
    architecture = (ROOT / "specs" / "SYSTEM_ARCHITECTURE.md").read_text(encoding="utf-8")

    assert "bda1a859df63fa5f24e51398fa80a23490bb6dfc" in matrix
    assert "ADOPT_UPSTREAM" in matrix
    assert "WRAP_FOR_OPERATIONS" in policy
    assert "BUILD_LOCAL_EXCEPTION" in policy
    assert "Two automatic-reply send executors must never run" in policy
    assert "business app and execution engine" in architecture
    assert "safety policy" in architecture
    assert "operational wrappers" in architecture


def test_chg_0011_does_not_create_next_change_or_send_fixture() -> None:
    assert not (ROOT / "changes" / "active" / "CHG-0012-validate-upstream-native-multi-account-fixed-template-reply").exists()
    acceptance = (ROOT / "changes" / "active" / "CHG-0011-upstream-first-product-direction-freeze" / "acceptance.md").read_text(encoding="utf-8")
    assert "No platform messages" in acceptance
