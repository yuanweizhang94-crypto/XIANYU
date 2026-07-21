from __future__ import annotations

import argparse
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r'(?i)cookie\s*[:=]\s*[^\s<>{}\[\]\'"]{20,}'),
    re.compile(r'(?i)(token|secret|corpsecret)\s*[:=]\s*(?!replace|placeholder|disabled)[^\s<>{}\[\]\'"]{16,}'),
    re.compile(r"(?i)password\s*=\s*(?!replace|placeholder|example)[^\s]{8,}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]
IGNORED_DIRS = {".git", ".venv", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build"}
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".example"}


def _is_ignored(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(part in IGNORED_DIRS or part.endswith(".egg-info") for part in parts)


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    env_file = root / ".env"
    if env_file.exists():
        findings.append(".env must not be committed or present for security scan")
    profiles = root / "profiles"
    if profiles.exists() and any(profiles.iterdir()):
        findings.append("profiles directory must not contain committed content")

    for path in root.rglob("*"):
        if not path.is_file() or _is_ignored(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        if rel == ".env.example":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"CODEOWNERS"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"sensitive pattern in {rel}: {pattern.pattern}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    findings = scan(args.root)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        return 1
    print("security scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
