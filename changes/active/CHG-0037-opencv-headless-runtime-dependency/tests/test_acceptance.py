from __future__ import annotations

import subprocess
from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0037-opencv-headless-runtime-dependency.patch"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chg0037_dependency_patch_is_exact_and_business_logic_untouched() -> None:
    text = _text(PATCH)
    assert '+    "opencv-python-headless==5.0.0.93",' in text
    changed = [line.split(" b/", 1)[1] for line in text.splitlines() if line.startswith("diff --git a/")]
    assert changed == ["backend-web/pyproject.toml"]
    for forbidden in (
        "publish_execution_service.py",
        "xianyu_personal_publisher.py",
        "xianyu_direct_publisher.py",
        "xianyu_publish_service.py",
        "cookies.py",
    ):
        assert forbidden not in text


def test_chg0037_dependency_patch_clean_apply_check(tmp_path: Path) -> None:
    target = tmp_path / "backend-web" / "pyproject.toml"
    target.parent.mkdir(parents=True)
    target.write_text("\n" * 39 + '    "opencv-python-headless>=4.10.0",\n', encoding="utf-8")

    result = subprocess.run(
        ["git", "apply", "--check", "--unidiff-zero", str(PATCH)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_chg0037_source_acceptance_and_tasks_match_implemented_delta() -> None:
    acceptance = _text(CHANGE / "acceptance.md")
    tasks = _text(CHANGE / "tasks.md")

    for marker in (
        "Vendor patch changes only `backend-web/pyproject.toml`.",
        "Exact dependency after patch: `opencv-python-headless==5.0.0.93`.",
        "`BUSINESS_SOURCE_LOGIC_CHANGED=false`.",
        "Targeted tests, change validation, secret scan and `git diff --check` pass.",
    ):
        assert marker in acceptance

    for task in ("T5", "T6", "T7"):
        assert f"- [x] {task} " in tasks
    assert "- [ ] T8 " in tasks
