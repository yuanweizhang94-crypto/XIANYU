from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CHANGE_ID = "CHG-0001-project-baseline"
VALID_CHANGE_STATUSES = {"APPROVED", "IN_PROGRESS", "COMPLETE"}
TASK_RE = re.compile(r"^- \[(?P<mark>[ xX])] (?P<text>T\d+ .+)$")


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


def extract_change_status(change_dir: Path) -> str:
    proposal = change_dir / "proposal.md"
    if not proposal.exists():
        return ""
    for line in proposal.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


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
