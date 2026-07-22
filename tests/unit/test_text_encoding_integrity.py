from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".css", ".html", ".ini", ".js", ".json", ".mako", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
IGNORED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist"}
REPLACEMENT_CHARACTER = "\ufffd"
REPEATED_QUESTION_MARKS = "?" * 3


def tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = Path(line)
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if IGNORED_PARTS.intersection(path.parts):
            continue
        paths.append(path)
    return paths


def test_tracked_text_files_are_utf8_and_not_mojibake() -> None:
    failures: list[str] = []
    for relative in tracked_text_files():
        path = ROOT / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{relative.as_posix()}: not valid UTF-8: {exc}")
            continue
        if REPLACEMENT_CHARACTER in text:
            failures.append(f"{relative.as_posix()}: contains Unicode replacement character")
        if REPEATED_QUESTION_MARKS in text:
            failures.append(f"{relative.as_posix()}: contains repeated literal question marks")
    assert failures == []
