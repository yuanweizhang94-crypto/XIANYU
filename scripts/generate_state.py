from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from scripts.repo_utils import (
    discover_active_change,
    extract_change_status,
    extract_suspension_metadata,
    find_suspended_changes,
    is_executable_change_status,
    load_capabilities,
    next_uncompleted_task,
    parse_tasks,
)


def _active_change_state(root: Path) -> tuple[dict[str, str] | None, list[Any], str | None]:
    active_change = discover_active_change(root)
    if active_change is None:
        return None, [], None

    status = extract_change_status(active_change)
    tasks_path = active_change / "tasks.md"
    tasks = parse_tasks(tasks_path) if tasks_path.exists() else []
    next_task = next_uncompleted_task(tasks) if is_executable_change_status(status) else None
    active_state = {
        "id": active_change.name,
        "status": status,
        "path": active_change.relative_to(root).as_posix(),
    }
    return active_state, tasks, next_task


def _tasks_state(change_dir: Path, *, executable: bool) -> dict[str, Any]:
    tasks_path = change_dir / "tasks.md"
    tasks = parse_tasks(tasks_path) if tasks_path.exists() else []
    return {
        "total": len(tasks),
        "completed": sum(1 for task in tasks if task.completed),
        "next_task": next_uncompleted_task(tasks) if executable else None,
        "items": [{"text": task.text, "completed": task.completed} for task in tasks],
    }


def _runtime_authority_state(root: Path, active_state: dict[str, str] | None) -> dict[str, Any] | None:
    if active_state is None:
        return None
    source = root / active_state["path"] / "runtime_authority.json"
    if not source.exists():
        return None
    value = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("runtime_authority.json must contain an object")
    return value


def _suspended_change_states(root: Path) -> list[dict[str, Any]]:
    states: list[dict[str, Any]] = []
    for change_dir in find_suspended_changes(root):
        status = extract_change_status(change_dir)
        metadata = extract_suspension_metadata(change_dir)
        states.append(
            {
                "id": change_dir.name,
                "status": status,
                "path": change_dir.relative_to(root).as_posix(),
                "suspended_from": metadata["suspended_from"],
                "suspended_at": metadata["suspended_at"],
                "suspended_reason": metadata["suspended_reason"],
                "resume_condition": metadata["resume_condition"],
                "tasks": _tasks_state(change_dir, executable=False),
            }
        )
    return states


def build_project_state(root: Path) -> dict[str, Any]:
    active_change, tasks, next_task = _active_change_state(root)
    capabilities = load_capabilities(root)
    status_counts = Counter(str(item.get("status", "unknown")) for item in capabilities)

    return {
        "project": "XIANYU",
        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "active_change": active_change,
        "tasks": {
            "total": len(tasks),
            "completed": sum(1 for task in tasks if task.completed),
            "next_task": next_task,
            "items": [{"text": task.text, "completed": task.completed} for task in tasks],
        },
        "suspended_changes": _suspended_change_states(root),
        "capabilities": {
            "total": len(capabilities),
            "by_status": dict(sorted(status_counts.items())),
            "items": capabilities,
        },
        "runtime_authority": _runtime_authority_state(root, active_change),
    }


def project_state_json(root: Path) -> str:
    return json.dumps(build_project_state(root), ensure_ascii=False, indent=2) + "\n"


def write_project_state(root: Path) -> Path:
    output = root / "generated" / "PROJECT_STATE.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(project_state_json(root), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = write_project_state(args.root)
    print(f"generated {output.relative_to(args.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
