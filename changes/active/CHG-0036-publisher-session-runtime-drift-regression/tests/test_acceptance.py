from __future__ import annotations

import hashlib
from pathlib import Path

CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/publisher-session-runtime-drift-regression-20260830.patch"


def test_chg0036_execution_contract_and_zero_publish_gate() -> None:
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "ROOT_CAUSE=PRODUCTION_RUNTIME_ONLY_DRIFT" in proposal
    assert "CANONICAL_SOURCE_ALREADY_CORRECT=true" in proposal
    assert "SOURCE_FUNCTIONAL_FIX_REQUIRED=false" in proposal
    assert "real Material 94-103 publish" in acceptance


def test_chg0036_regression_artifact_identity() -> None:
    assert PATCH.exists()
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest() == "750d60160cb4126669a74b1220e48b5bcc64f8d7be4562ca8a96e77ba7d1e52f"


def test_chg0036_business_source_logic_is_not_patched() -> None:
    text = PATCH.read_text(encoding="utf-8")
    changed = [line.split(" b/", 1)[1] for line in text.splitlines() if line.startswith("diff --git a/")]
    assert changed == ["tests/test_publish_session_runtime_drift_regression.py"]
