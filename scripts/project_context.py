from __future__ import annotations



from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))



from scripts.generate_state import build_project_state



REQUIRED_READING = [

    "changes/active/CHG-0001-project-baseline/proposal.md",

    "changes/active/CHG-0001-project-baseline/design.md",

    "changes/active/CHG-0001-project-baseline/tasks.md",

    "changes/active/CHG-0001-project-baseline/acceptance.md",

    "specs/PROJECT_SCOPE.md",

    "specs/SYSTEM_ARCHITECTURE.md",

    "specs/CAPABILITY_REGISTRY.yaml",

    "docs/adr/ADR-0001.md",

    "docs/adr/ADR-0002.md",

    "docs/adr/ADR-0003.md",

    "docs/adr/ADR-0004.md",

    "docs/adr/ADR-0005.md",

    "docs/adr/ADR-0006.md",

    "docs/adr/ADR-0007.md",

    "docs/adr/ADR-0008.md",

]



VERIFY_COMMANDS = [

    "python scripts/verify_repository.py",

    "pytest",

    "ruff check .",

    "mypy scripts",

]





def render_context(root: Path) -> str:

    state = build_project_state(root)

    lines = [

        "XIANYU Project Context",

        "======================",

        "Project goal path: Product template -> Xianyu listing -> Inquiry receiving -> Fixed reply -> WeCom customer service -> AI fallback -> Human transfer",

        f"Current branch: {state['git']['branch']}",

        f"Current commit: {state['git']['head']}",

        f"Worktree clean: {state['git']['worktree_clean']}",

        f"Active change: {state['active_change']['id']}",

        f"Active change status: {state['active_change']['status']}",

        f"Next unfinished task: {state['tasks']['next_uncompleted']}",

        f"Capability total: {state['capabilities']['total']}",

        f"Capability status counts: {state['capabilities']['by_status']}",

        "Required reading order:",

    ]

    lines.extend(f"- {item}" for item in REQUIRED_READING)

    lines.append("Verification commands:")

    lines.extend(f"- {item}" for item in VERIFY_COMMANDS)

    return "\n".join(lines)





def main() -> int:

    root = Path(__file__).resolve().parents[1]

    print(render_context(root))

    return 0





if __name__ == "__main__":

    raise SystemExit(main())

