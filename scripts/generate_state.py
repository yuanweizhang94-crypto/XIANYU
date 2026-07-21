from __future__ import annotations



import argparse

import json

from collections import Counter

from datetime import UTC, datetime

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from typing import Any



from scripts.repo_utils import (

    ACTIVE_CHANGE_ID,

    extract_change_status,

    find_active_changes,

    load_capabilities,

    next_uncompleted_task,

    parse_tasks,

    run_git,

)





def _git_status(root: Path) -> list[str]:

    status = run_git(["status", "--short"], root)

    if not status:

        return []

    return status.splitlines()





def _recent_tests(root: Path) -> dict[str, str]:

    summary_path = root / "generated" / "LAST_TEST_SUMMARY.json"

    if summary_path.exists():

        data = json.loads(summary_path.read_text(encoding="utf-8"))

        summary = str(data.get("summary", "external summary"))

        return {"summary": summary, "source": str(summary_path.relative_to(root))}

    return {"summary": "No test summary file recorded; run verification commands for current results.", "source": "none"}





def build_project_state(root: Path) -> dict[str, Any]:

    active_changes = find_active_changes(root)

    active_change = active_changes[0] if active_changes else root / "changes" / "active" / ACTIVE_CHANGE_ID

    tasks_path = active_change / "tasks.md"

    tasks = parse_tasks(tasks_path) if tasks_path.exists() else []

    capabilities = load_capabilities(root)

    status_counts = Counter(str(item.get("status", "unknown")) for item in capabilities)

    status_short = _git_status(root)



    return {

        "project": "XIANYU",

        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),

        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),

        "git": {

            "branch": run_git(["branch", "--show-current"], root),

            "head": run_git(["rev-parse", "HEAD"], root),

            "status_short": status_short,

            "worktree_clean": not status_short,

        },

        "active_change": {

            "id": active_change.name,

            "status": extract_change_status(active_change),

            "path": str(active_change.relative_to(root)).replace("\\", "/"),

        },

        "tasks": {

            "total": len(tasks),

            "completed": sum(1 for task in tasks if task.completed),

            "next_uncompleted": next_uncompleted_task(tasks),

            "items": [{"text": task.text, "completed": task.completed} for task in tasks],

        },

        "capabilities": {

            "total": len(capabilities),

            "by_status": dict(sorted(status_counts.items())),

            "items": capabilities,

        },

        "recent_tests": _recent_tests(root),

    }





def write_project_state(root: Path) -> Path:

    output = root / "generated" / "PROJECT_STATE.json"

    output.parent.mkdir(parents=True, exist_ok=True)

    state = build_project_state(root)

    output.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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

