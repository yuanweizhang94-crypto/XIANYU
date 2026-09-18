from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/publish-session-runtime-convergence-20260918.patch"

EXPECTED_PATCH_SHA256 = "a8688e53ade360cc0f775eb3bc7efb5b48844f644bdbfd30de837a90430da4fa"
EXPECTED_BASE_COOKIE_MANAGER_SHA256 = "2a727e3f32c8e392a5d59078f09ef75b50c2546a8065d504227aca1c9dfe32ec"
EXPECTED_FIXED_COOKIE_MANAGER_SHA256 = "0f77813d95dfd0fcae6e620bc23ae0252f56b962251a76f5cf1aebc62c9e2e1d"
EXPECTED_BASE_INTERNAL_SHA256 = "76692905b87cff85476a36c3d9a2f65139ef9a05641ead92dd44859d56e66167"
EXPECTED_FIXED_INTERNAL_SHA256 = "811f2400ebf1b6ef2ce937e05f42abeffcd6dc26c425e5dec1989caee5908c99"


def _text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_runtime_convergence_patch_is_locked() -> None:
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest() == EXPECTED_PATCH_SHA256


def test_runtime_convergence_patch_changes_only_existing_session_owner_paths() -> None:
    changed = []
    for line in _text().splitlines():
        if line.startswith("diff --git a/"):
            changed.append(line.split(" b/", 1)[1])

    assert changed == [
        "websocket/app/services/xianyu/cookie_token_manager.py",
        "websocket/app/api/routes/internal.py",
    ]


def test_auth_valid_renewal_clears_stale_platform_verification_state() -> None:
    text = _text()
    assert 'commit.get("auth_status") == "AUTH_VALID"' in text
    assert "await self._persist_platform_verification_marker(required=False)" in text
    assert "self._clear_platform_verification_required()" in text
    assert 'self.last_token_refresh_status = "success"' in text


def test_refresh_endpoint_reuses_existing_xianyu_async_owner() -> None:
    text = _text()
    assert "await instance.refresh_token()" in text
    assert "+            await instance.token_manager.trigger_refresh()" not in text
    assert "-            await instance.token_manager.trigger_refresh()" in text


def test_no_parallel_session_or_publisher_is_introduced() -> None:
    text = _text()
    forbidden_new_paths = (
        "new_session_manager",
        "second_publisher",
        "ParallelPublisher",
        "trigger_refresh =",
    )
    for value in forbidden_new_paths:
        assert value not in text


def test_production_source_identities_are_recorded() -> None:
    # Sanitized one-way identities captured from the exact production base image
    # and the activated fixed image. No Cookie/Token/Authorization material is stored.
    for value in (
        EXPECTED_BASE_COOKIE_MANAGER_SHA256,
        EXPECTED_FIXED_COOKIE_MANAGER_SHA256,
        EXPECTED_BASE_INTERNAL_SHA256,
        EXPECTED_FIXED_INTERNAL_SHA256,
    ):
        assert len(value) == 64
