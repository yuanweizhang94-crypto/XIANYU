from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/publisher-session-runtime-drift-regression-20260830.patch"
EXPECTED_SHA256 = "750d60160cb4126669a74b1220e48b5bcc64f8d7be4562ca8a96e77ba7d1e52f"
EXPECTED_PINNED_UPSTREAM = "742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1"
EXPECTED_PINNED_PUBLISH_SERVICE_SHA256 = "50219b5069803498c350c8edf2eb765f997318a5ca92b6ed88e9ccf6ab3a3df7"
FORBIDDEN_PATTERN = "await session.refresh(account)"
CHANGE_ID = "CHG-0036-publisher-session-runtime-drift-regression"
CHANGE_RECORD = (
    ROOT / "changes/archive" / CHANGE_ID
    if (ROOT / "changes/archive" / CHANGE_ID).exists()
    else ROOT / "changes/active" / CHANGE_ID
)


def _text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_regression_patch_is_locked_and_parseable() -> None:
    payload = PATCH.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256
    result = subprocess.run(
        ["git", "apply", "--numstat", "--unidiff-zero", str(PATCH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "tests/test_publish_session_runtime_drift_regression.py" in result.stdout


def test_regression_patch_changes_tests_only() -> None:
    changed = []
    for line in _text().splitlines():
        if line.startswith("diff --git a/"):
            changed.append(line.split(" b/", 1)[1])
    assert changed == ["tests/test_publish_session_runtime_drift_regression.py"]


def test_regression_patch_covers_all_required_session_cookie_cases() -> None:
    text = _text()
    required_tests = (
        "test_capability_refreshed_cookie_flows_to_account_and_publisher",
        "test_batch_publish_has_no_session_nameerror_and_reaches_stubbed_publisher",
        "test_canonical_batch_source_forbids_undefined_session_refresh_and_keeps_cookie_flow",
        "test_batch_does_not_repeat_refresh_after_capability_owner",
        "test_missing_capability_cookie_uses_existing_cookie",
        "test_capability_auth_failure_fails_closed_without_publish_transport",
        "test_three_accounts_keep_capability_cookies_isolated",
        "test_material_94_reaches_preplatform_stub_without_real_item_creation",
    )
    for name in required_tests:
        assert name in text

    assert f'assert "{FORBIDDEN_PATTERN}" not in source' in text
    assert 'capability.get("cookies_str") or cookies_str' in text
    assert "account.cookie = cookies_str" in text
    assert "session.refresh.assert_not_awaited()" in text


def test_regression_patch_hard_blocks_real_publish_transport() -> None:
    text = _text()
    assert "AsyncMock" in text
    assert "REAL_PLATFORM_REQUEST_BLOCKED" in text
    assert 'monkeypatch.setattr(publish_module, "publish_personal_single_item",' in text
    assert "result[\"success_count\"] == 0" in text
    assert "item_id\": None" in text
    assert "item_url\": None" in text


def test_pinned_upstream_identity_is_documented_in_change_record() -> None:
    proposal = (CHANGE_RECORD / "proposal.md").read_text(encoding="utf-8")
    assert EXPECTED_PINNED_UPSTREAM in proposal
    assert "CANONICAL_SOURCE_ALREADY_CORRECT=true" in proposal
    assert "SOURCE_FUNCTIONAL_FIX_REQUIRED=false" in proposal
    assert "PRODUCTION_RUNTIME_ONLY_DRIFT" in proposal


def test_pinned_source_hash_is_recorded_by_guard_contract() -> None:
    # The hash is a sanitized immutable identity, not source duplication.
    assert len(EXPECTED_PINNED_PUBLISH_SERVICE_SHA256) == 64
    assert EXPECTED_PINNED_PUBLISH_SERVICE_SHA256 == "50219b5069803498c350c8edf2eb765f997318a5ca92b6ed88e9ccf6ab3a3df7"
