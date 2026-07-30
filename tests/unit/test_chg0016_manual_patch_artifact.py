from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH_PATH = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "bda1a85-manual-only-verification.patch"
EXPECTED_PATCH_FILES = {
    "common/services/captcha/manual_verification.py",
    "common/services/captcha/orchestrator.py",
    "tests/test_manual_verification.py",
    "websocket/app/core/config.py",
    "websocket/app/services/xianyu/cookie_token_manager.py",
}
FULL_INDEX_RE = re.compile(
    r"^index [0-9a-f]{40}\.\.[0-9a-f]{40}(?: [0-7]{6})?$"
)


def _patch_text() -> str:
    return PATCH_PATH.read_text(encoding="utf-8")


def _patch_lines() -> list[str]:
    return _patch_text().splitlines()


def _git_apply_numstat() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "apply", "--numstat", "--unidiff-zero", str(PATCH_PATH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _sanitized_process_output(result: subprocess.CompletedProcess[str]) -> str:
    stdout = result.stdout.replace(str(ROOT), "<repo>")
    stderr = result.stderr.replace(str(ROOT), "<repo>")
    return f"stdout={stdout}\nstderr={stderr}"


def _numstat_paths(stdout: str) -> set[str]:
    paths = set()
    for line in stdout.splitlines():
        fields = line.split("\t")
        if len(fields) == 3:
            paths.add(fields[2])
    return paths


def _added_patch_text() -> str:
    added_lines = []
    for line in _patch_lines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def _added_patch_text_for(path_fragment: str) -> str:
    in_file = False
    added_lines = []
    for line in _patch_lines():
        if line.startswith("diff --git "):
            in_file = path_fragment in line
            continue
        if in_file and line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def test_chg0016_patch_is_git_parseable() -> None:
    result = _git_apply_numstat()

    assert result.returncode == 0, _sanitized_process_output(result)
    assert _numstat_paths(result.stdout) == EXPECTED_PATCH_FILES


def test_chg0016_patch_has_exact_expected_file_set() -> None:
    result = _git_apply_numstat()

    assert result.returncode == 0, _sanitized_process_output(result)
    assert _numstat_paths(result.stdout) == EXPECTED_PATCH_FILES


def test_chg0016_patch_uses_full_index() -> None:
    index_lines = [
        line
        for line in _patch_lines()
        if line.startswith("index ")
    ]

    assert len(index_lines) == len(EXPECTED_PATCH_FILES)
    assert all(FULL_INDEX_RE.fullmatch(line) for line in index_lines)


def test_chg0016_patch_is_zero_context() -> None:
    in_hunk = False
    hunk_count = 0
    context_lines = []
    invalid_hunk_lines = []

    for number, line in enumerate(_patch_lines(), start=1):
        if line.startswith("diff --git "):
            in_hunk = False
            continue
        if line.startswith("@@"):
            in_hunk = True
            hunk_count += 1
            continue
        if not in_hunk:
            continue
        if line.startswith(" "):
            context_lines.append(number)
        if line and not line.startswith(("+", "-", "\\ No newline")):
            invalid_hunk_lines.append(number)

    assert hunk_count > 0
    assert context_lines == []
    assert invalid_hunk_lines == []


def test_chg0016_patch_added_lines_have_no_trailing_whitespace() -> None:
    bad = [
        number
        for number, line in enumerate(_patch_lines(), start=1)
        if line.startswith("+")
        and not line.startswith("+++")
        and line != "+"
        and line[1:].endswith((" ", "\t"))
    ]

    assert bad == []


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
    assert "if parsed.port not in (None, 443):" in manual_added
    assert "test_invalid_initial_url_does_not_consume_one_shot" in added
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
