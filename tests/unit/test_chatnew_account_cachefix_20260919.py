from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "patch_chatnew_account_cachefix_20260919.py"


def _module():
    spec = importlib.util.spec_from_file_location("chatnew_cachefix", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_locked_runtime_hashes_are_present() -> None:
    module = _module()
    assert module.BASE_SHA256 == "7d58515be1e86a9370b8fcce91a08943e4c9df253838477f0eba4e92e0294843"
    assert module.FIXED_SHA256 == "5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b"


def test_fresh_server_truth_replaces_account_cache_even_when_empty() -> None:
    module = _module()
    source = f"before::{module.OLD_SNIPPET}::after"
    fixed = module.transform_text(source)
    assert module.OLD_SNIPPET not in fixed
    assert module.NEW_SNIPPET in fixed
    assert "Pe.current[e]={convs:y,hasMore:g.hasMore,cursor:g.nextCursor}" in fixed


def test_append_path_updates_same_account_cache() -> None:
    module = _module()
    fixed = module.transform_text(module.OLD_SNIPPET)
    assert "const F=[...b,...y]" in fixed
    assert "Pe.current[e]={convs:F,hasMore:g.hasMore,cursor:g.nextCursor}" in fixed


def test_transform_fails_closed_on_missing_or_duplicate_preimage() -> None:
    module = _module()
    with pytest.raises(ValueError):
        module.transform_text("no production preimage here")
    with pytest.raises(ValueError):
        module.transform_text(module.OLD_SNIPPET + module.OLD_SNIPPET)


def test_hotfix_scope_does_not_add_send_publish_or_auth_logic() -> None:
    module = _module()
    added = module.NEW_SNIPPET
    for forbidden in (
        "send-message",
        "send-image",
        "product-publish",
        "cookie",
        "token",
        "authorization",
        "password",
        "qr",
    ):
        assert forbidden not in added.lower()
