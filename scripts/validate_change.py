from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from scripts.repo_utils import (
    ACTIVE_CHANGE_STATUSES,
    REQUIRED_CHANGE_FILES,
    VALID_CHANGE_STATUSES,
    current_branch_change_id,
    extract_change_status,
    extract_change_statuses,
    find_active_changes,
    parse_tasks,
)


class ChangeValidationError(ValueError):
    """Raised when the active change is invalid."""


REQUIRED_UPSTREAM_FIRST_FIELDS = [
    "Upstream capability audit",
    "Pinned upstream evidence",
    "Existing local implementation search",
    "Reuse decision",
    "Duplicate implementation risk",
    "Why upstream cannot satisfy the requirement",
    "Approved exception ADR",
    "Component owner",
    "Retirement plan for overlapping local code",
]

VALID_REUSE_DECISIONS = {
    "ADOPT_UPSTREAM",
    "CONFIGURE_UPSTREAM",
    "PATCH_UPSTREAM",
    "WRAP_FOR_OPERATIONS",
    "BUILD_LOCAL_EXCEPTION",
}

LOCAL_REWRITE_PATTERNS = [
    re.compile(r"local rewrite plan\s*:\s*(yes|true|planned|required)", re.IGNORECASE),
    re.compile(r"plans?\s+(?:a\s+)?local rewrite", re.IGNORECASE),
    re.compile(r"rewrite\s+.+\s+in\s+D:/xianyu", re.IGNORECASE),
    re.compile(r"rewrite\s+.+\s+in\s+D:\\xianyu", re.IGNORECASE),
]


def _change_id_mentions_are_consistent(change_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_CHANGE_FILES:
        path = change_dir / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        expected = f"Change ID: {change_dir.name}"
        if expected not in content:
            errors.append(f"{name} does not declare {expected}")
    return errors


def _field_present(text: str, field: str) -> bool:
    pattern = re.compile(
        rf"(?im)^\s*(?:#+\s+{re.escape(field)}|{re.escape(field)}\s*:)\s*$"
        rf"|^\s*{re.escape(field)}\s*:",
    )
    return bool(pattern.search(text))


def _extract_reuse_decision(text: str) -> str | None:
    match = re.search(r"(?im)^\s*Decision\s*:\s*([A-Z_]+)\b", text)
    if not match:
        return None
    return match.group(1)


def _section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*#+\s+{re.escape(heading)}\s*$"
        rf"(?P<body>.*?)(?=^\s*#+\s+\S|\Z)",
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def _has_local_rewrite_plan(text: str) -> bool:
    return any(pattern.search(text) for pattern in LOCAL_REWRITE_PATTERNS)


def _validate_upstream_first_fields(change_dir: Path) -> list[str]:
    errors: list[str] = []
    chunks = []
    for name in REQUIRED_CHANGE_FILES:
        path = change_dir / name
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8"))
    text = "\n\n".join(chunks)

    missing = [field for field in REQUIRED_UPSTREAM_FIRST_FIELDS if not _field_present(text, field)]
    if missing:
        errors.append(f"missing upstream-first change fields: {', '.join(missing)}")

    decision = _extract_reuse_decision(text)
    if decision is None:
        errors.append("missing reuse decision")
    elif decision not in VALID_REUSE_DECISIONS:
        errors.append(f"invalid reuse decision: {decision}")

    if decision == "BUILD_LOCAL_EXCEPTION":
        exception_body = _section_text(text, "Approved exception ADR")
        if "docs/adr/ADR-" not in exception_body:
            errors.append("BUILD_LOCAL_EXCEPTION requires approved exception ADR evidence")

    if decision == "ADOPT_UPSTREAM" and _has_local_rewrite_plan(text):
        errors.append("ADOPT_UPSTREAM change must not plan local rewrite in D:/xianyu")

    return errors


def _validate_archived_changes(root: Path) -> list[str]:
    errors: list[str] = []
    archive_root = root / "changes" / "archive"
    if not archive_root.exists():
        return errors
    for change_dir in sorted(path for path in archive_root.iterdir() if path.is_dir()):
        missing = [name for name in REQUIRED_CHANGE_FILES if not (change_dir / name).exists()]
        if missing:
            errors.append(f"missing archived change files for {change_dir.name}: {', '.join(missing)}")
            continue
        statuses = extract_change_statuses(change_dir)
        unique_statuses = {status for status in statuses.values() if status}
        if unique_statuses != {"ARCHIVED"}:
            errors.append(f"archived change must have ARCHIVED status: {change_dir.name}")
        errors.extend(_change_id_mentions_are_consistent(change_dir))
    return errors


def validate_change(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_archived_changes(root))
    active_changes = find_active_changes(root)

    if len(active_changes) > 1:
        errors.append(f"expected at most one active change, found {len(active_changes)}")
        return errors

    if not active_changes:
        return errors

    change_dir = active_changes[0]
    missing = [name for name in REQUIRED_CHANGE_FILES if not (change_dir / name).exists()]
    if missing:
        errors.append(f"missing change files: {', '.join(missing)}")

    statuses = extract_change_statuses(change_dir)
    unique_statuses = {status for status in statuses.values() if status}
    missing_status_files = [name for name, status in statuses.items() if not status and name not in missing]
    if missing_status_files:
        errors.append(f"missing change status in: {', '.join(missing_status_files)}")
    invalid_statuses = sorted(status for status in unique_statuses if status not in VALID_CHANGE_STATUSES)
    if invalid_statuses:
        errors.append(f"invalid change status: {', '.join(invalid_statuses)}")
    if len(unique_statuses) > 1:
        errors.append(f"change status mismatch: {statuses}")

    status = extract_change_status(change_dir)
    if status in {"MERGED", "ARCHIVED"}:
        errors.append(f"{status} change must not remain in changes/active")
    elif status and status not in ACTIVE_CHANGE_STATUSES:
        errors.append(f"invalid active change status: {status}")

    errors.extend(_change_id_mentions_are_consistent(change_dir))
    errors.extend(_validate_upstream_first_fields(change_dir))

    branch_change_id = current_branch_change_id(root)
    if branch_change_id is not None and branch_change_id != change_dir.name:
        errors.append(f"branch change id mismatch: {branch_change_id} != {change_dir.name}")

    tasks_path = change_dir / "tasks.md"
    if tasks_path.exists():
        tasks = parse_tasks(tasks_path)
        if not tasks:
            errors.append("tasks.md contains no valid task checkboxes")
        for task in tasks:
            if not task.text.startswith("T"):
                errors.append(f"invalid task text: {task.text}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_change(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("change validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
