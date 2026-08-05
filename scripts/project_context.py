from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from scripts.generate_state import build_project_state
from scripts.repo_utils import is_executable_change_status, run_git, try_git

VERIFY_COMMANDS = [
    "python scripts/verify_repository.py",
    "pytest",
    "ruff check .",
    "mypy scripts",
]


def _git_status(root: Path) -> list[str]:
    status = run_git(["status", "--short"], root)
    return status.splitlines() if status else []


def _accepted_adr_paths(root: Path) -> list[str]:
    adr_root = root / "docs" / "adr"
    if not adr_root.exists():
        return []
    accepted: list[str] = []
    for path in sorted(adr_root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "## Status" in text and "Accepted" in text:
            accepted.append(path.relative_to(root).as_posix())
    return accepted


def required_reading(root: Path, state: dict[str, object]) -> list[str]:
    items = [
        "AGENTS.md",
        "specs/PROJECT_SCOPE.md",
        "specs/SYSTEM_ARCHITECTURE.md",
        "specs/CAPABILITY_REGISTRY.yaml",
    ]
    items.extend(
        entry
        for entry in [
            "docs/UPSTREAM_CAPABILITY_MATRIX.md",
            "docs/LOCAL_COMPONENT_DISPOSITION.md",
            "docs/UPSTREAM_FIRST_POLICY.md",
        ]
        if (root / entry).exists()
    )
    active_change = state.get("active_change")
    if isinstance(active_change, dict):
        active_path = str(active_change["path"])
        items.extend(
            f"{active_path}/{name}" for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
        )
    items.extend(_accepted_adr_paths(root))
    contract_entries = ["contracts/openapi.yaml"]
    contract_entries.extend(
        path.relative_to(root).as_posix() for path in sorted((root / "contracts" / "schemas").glob("*.json"))
    )
    items.extend(entry for entry in contract_entries if (root / entry).exists())
    items.extend(
        path.relative_to(root).as_posix()
        for path in sorted((root / "tests").rglob("test_*.py"))
    )
    return items


def render_context(root: Path) -> str:
    state = build_project_state(root)
    status_short = _git_status(root)
    active_change = state["active_change"]
    active_id = None
    active_status = None
    if isinstance(active_change, dict):
        active_id = active_change["id"]
        active_status = active_change["status"]

    next_task = state["tasks"]["next_task"]
    suspended_changes = state.get("suspended_changes", [])
    executable = is_executable_change_status(str(active_status)) if active_status else False

    lines = [
        "XIANYU Project Context",
        "======================",
        "Project goal path: Product template -> Xianyu listing -> Inquiry receiving -> Fixed reply -> WeCom customer service -> AI fallback -> Human transfer",
        f"Current branch: {run_git(['branch', '--show-current'], root)}",
        f"Current HEAD: {try_git(['rev-parse', 'HEAD'], root) or 'unavailable'}",
        "Current git status:",
    ]
    if status_short:
        lines.extend(f"- {line}" for line in status_short)
    else:
        lines.append("- clean")
    lines.extend(
        [
            f"Worktree clean: {not status_short}",
            f"active_change: {active_id if active_id is not None else 'null'}",
            f"Active change status: {active_status if active_status is not None else 'null'}",
            f"next_task: {next_task if next_task is not None else 'null'}",
            f"suspended_changes: {len(suspended_changes) if isinstance(suspended_changes, list) else 0}",
        ]
    )
    if isinstance(suspended_changes, list):
        for item in suspended_changes:
            if isinstance(item, dict):
                lines.append(
                    "Suspended change: "
                    f"{item.get('id')} "
                    f"status={item.get('status')} "
                    f"progress={item.get('tasks', {}).get('completed')}/"
                    f"{item.get('tasks', {}).get('total')}"
                )
    if not executable:
        lines.append("no approved executable change")
    lines.extend(
        [
            f"Capability total: {state['capabilities']['total']}",
            f"Capability status counts: {state['capabilities']['by_status']}",
            "Required reading order:",
        ]
    )
    lines.extend(f"- {item}" for item in required_reading(root, state))
    lines.append("Verification commands:")
    lines.extend(f"- {item}" for item in VERIFY_COMMANDS)
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print(render_context(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
