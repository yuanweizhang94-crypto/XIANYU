from __future__ import annotations



import argparse

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))



from scripts.repo_utils import (

    ACTIVE_CHANGE_ID,

    VALID_CHANGE_STATUSES,

    extract_change_status,

    find_active_changes,

    parse_tasks,

)



REQUIRED_CHANGE_FILES = ["proposal.md", "design.md", "tasks.md", "acceptance.md"]





class ChangeValidationError(ValueError):

    """Raised when the active change is invalid."""





def validate_change(root: Path) -> list[str]:

    errors: list[str] = []

    active_changes = find_active_changes(root)

    if len(active_changes) != 1:

        errors.append(f"expected exactly one active change, found {len(active_changes)}")

        return errors



    change_dir = active_changes[0]

    if change_dir.name != ACTIVE_CHANGE_ID:

        errors.append(f"active change id mismatch: {change_dir.name} != {ACTIVE_CHANGE_ID}")



    missing = [name for name in REQUIRED_CHANGE_FILES if not (change_dir / name).exists()]

    if missing:

        errors.append(f"missing change files: {', '.join(missing)}")



    status = extract_change_status(change_dir)

    if status not in VALID_CHANGE_STATUSES:

        errors.append(f"invalid change status: {status or '<missing>'}")



    tasks_path = change_dir / "tasks.md"

    if tasks_path.exists():

        tasks = parse_tasks(tasks_path)

        if not tasks:

            errors.append("tasks.md contains no valid task checkboxes")

        for task in tasks:

            if not task.text.startswith("T"):

                errors.append(f"invalid task text: {task.text}")

        content = tasks_path.read_text(encoding="utf-8")

        if ACTIVE_CHANGE_ID not in content:

            errors.append("tasks.md does not mention active change id")



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

