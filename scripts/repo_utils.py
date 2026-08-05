from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID_CHANGE_STATUSES = {
    "DRAFT",
    "APPROVED",
    "IMPLEMENTING",
    "VERIFYING",
    "MERGED",
    "ARCHIVED",
    "SUSPENDED",
}
ACTIVE_CHANGE_STATUSES = {"DRAFT", "APPROVED", "IMPLEMENTING", "VERIFYING"}
EXECUTABLE_CHANGE_STATUSES = {"APPROVED", "IMPLEMENTING", "VERIFYING"}
SUSPENDED_CHANGE_STATUSES = {"SUSPENDED"}
REQUIRED_CHANGE_FILES = ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
TASK_RE = re.compile(r"^- \[(?P<mark>[ xX])] (?P<text>T\d+ .+)$")
BRANCH_CHANGE_RE = re.compile(r"(?P<change_id>CHG-\d{4}-[A-Za-z0-9_.-]+)")


@dataclass(frozen=True)
class TaskItem:
    text: str
    completed: bool


def run_git(args: list[str], root: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def try_git(args: list[str], root: Path = ROOT) -> str | None:
    try:
        return run_git(args, root)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return data


def read_json_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_active_changes(root: Path = ROOT) -> list[Path]:
    active = root / "changes" / "active"
    if not active.exists():
        return []
    return sorted(p for p in active.iterdir() if p.is_dir())


def find_suspended_changes(root: Path = ROOT) -> list[Path]:
    suspended = root / "changes" / "suspended"
    if not suspended.exists():
        return []
    return sorted(p for p in suspended.iterdir() if p.is_dir())


def discover_active_change(root: Path = ROOT) -> Path | None:
    active_changes = find_active_changes(root)
    if not active_changes:
        return None
    if len(active_changes) > 1:
        raise ValueError(f"expected at most one active change, found {len(active_changes)}")
    return active_changes[0]


def extract_status_from_file(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


def extract_change_statuses(change_dir: Path) -> dict[str, str]:
    return {name: extract_status_from_file(change_dir / name) for name in REQUIRED_CHANGE_FILES}


def extract_change_status(change_dir: Path) -> str:
    statuses = extract_change_statuses(change_dir)
    non_empty = [status for status in statuses.values() if status]
    if not non_empty:
        return ""
    first = non_empty[0]
    if all(status == first for status in non_empty):
        return first
    return first


def is_executable_change_status(status: str | None) -> bool:
    return status in EXECUTABLE_CHANGE_STATUSES


def current_branch_change_id(root: Path = ROOT) -> str | None:
    branch = try_git(["branch", "--show-current"], root)
    if not branch:
        return None
    match = BRANCH_CHANGE_RE.search(branch)
    return match.group("change_id") if match else None


def parse_tasks(tasks_path: Path) -> list[TaskItem]:
    tasks: list[TaskItem] = []
    for line in tasks_path.read_text(encoding="utf-8").splitlines():
        match = TASK_RE.match(line.strip())
        if match:
            tasks.append(TaskItem(text=match.group("text"), completed=match.group("mark").lower() == "x"))
    return tasks


def next_uncompleted_task(tasks: list[TaskItem]) -> str | None:
    for task in tasks:
        if not task.completed:
            return task.text
    return None


def extract_suspension_metadata(change_dir: Path) -> dict[str, str | None]:
    metadata: dict[str, str | None] = {
        "suspended_from": None,
        "suspended_at": None,
        "suspended_reason": None,
        "resume_condition": None,
    }
    for name in REQUIRED_CHANGE_FILES:
        path = change_dir / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            if key in metadata and metadata[key] is None:
                metadata[key] = value.strip() or None
    return metadata


def load_capabilities(root: Path = ROOT) -> list[dict[str, Any]]:
    registry = read_yaml(root / "specs" / "CAPABILITY_REGISTRY.yaml")
    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list):
        raise ValueError("capabilities must be a list")
    typed: list[dict[str, Any]] = []
    for item in capabilities:
        if not isinstance(item, dict):
            raise ValueError("each capability must be an object")
        typed.append(item)
    return typed


def required_repo_paths() -> list[str]:
    return [
        "README.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md",
        "VERSION",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "specs",
        "changes",
        "docs",
        "contracts",
        "app",
        "worker",
        "tests",
        "scripts",
        "generated",
        "adapters",
        ".github",
    ]
