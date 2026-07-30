from __future__ import annotations

from pathlib import Path


PATCH_PATH = Path("vendor/patches/xianyu-auto-reply/bda1a85-manual-only-verification.patch")


def _added_patch_text() -> str:
    added_lines = []
    for line in PATCH_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def _added_patch_text_for(path_fragment: str) -> str:
    in_file = False
    added_lines = []
    for line in PATCH_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("diff --git "):
            in_file = path_fragment in line
            continue
        if in_file and line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def test_chg0016_patch_adds_single_shot_manual_verification_boundary() -> None:
    added = _added_patch_text()

    assert "_STATE = \"IDLE\"" in added
    assert "\"CONSUMED\"" in added
    assert "manual_already_consumed" in added
    assert "manual_verification_busy_or_consumed" in added
    assert "manual_verification_not_accepted" in added
    assert "launch_persistent_context" in added


def test_chg0016_patch_keeps_cookie_and_url_boundary_strict() -> None:
    added = _added_patch_text()
    manual_added = _added_patch_text_for("common/services/captcha/manual_verification.py")

    assert "_ALLOWED_INITIAL_HOST = \"h5api.m.goofish.com\"" in added
    assert "VERIFICATION_REDIRECT_BLOCKED" in added
    assert "_ALLOWED_COOKIE_NAMES = {\"x5sec\"}" in added
    assert "startswith(\"x5\")" not in manual_added
    assert "startswith('x5')" not in manual_added
    assert "if captcha_engine == \"manual\":" in added
    assert "if cookie_name_lower == 'x5sec':" in added
    assert "return True, {\"x5sec\": x5sec}" in added


def test_chg0016_patch_does_not_add_automated_or_remote_verification() -> None:
    added = _added_patch_text()
    forbidden = [
        "page.mouse",
        "page.keyboard",
        ".click(",
        ".drag",
        "solve_slider",
        "run_drissionpage",
        "run_real_mouse",
        "_call_remote_solve(",
        "send-message",
    ]

    assert [term for term in forbidden if term in added] == []
