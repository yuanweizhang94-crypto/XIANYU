from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from scripts.repo_utils import load_capabilities

ACCOUNT_SPECIFIC_FILE_RE = re.compile(
    r"(publisher|reply|message|schedule|worker).*account[_-]?[a-z0-9]+\.py$|"
    r".*account[_-]?(1|2|3|a|b|c)\.py$",
    re.IGNORECASE,
)
SOURCE_DIRS = ["app", "worker", "adapters"]
APPROVED_SHARED_IMPLEMENTATION_PATHS = {"app/xianyu_system/application.py"}


class DuplicateCapabilityError(ValueError):
    """Raised when deterministic duplicate capability checks fail."""


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise DuplicateCapabilityError("path fields must be lists")
    return [str(item) for item in value]


def detect_duplicate_capabilities(root: Path) -> list[str]:
    errors: list[str] = []
    capabilities = load_capabilities(root)

    ids = [str(capability.get("id", "")) for capability in capabilities]
    for cap_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate capability id: {cap_id}")

    specs = [str(capability.get("specification", "")) for capability in capabilities]
    for spec, count in Counter(specs).items():
        if spec and count > 1:
            errors.append(f"duplicate specification path: {spec}")

    implementation_owner: dict[str, str] = {}
    conflicts: defaultdict[str, list[str]] = defaultdict(list)
    for capability in capabilities:
        cap_id = str(capability.get("id", ""))
        owner = str(capability.get("owner_module", "")).strip()
        if not owner:
            errors.append(f"owner_module is empty for {cap_id}")
        for impl_path in _as_str_list(capability.get("implementation_paths")):
            if not impl_path:
                continue
            previous = implementation_owner.get(impl_path)
            if previous and previous != cap_id:
                conflicts[impl_path].extend([previous, cap_id])
            implementation_owner[impl_path] = cap_id

    for impl_path, owners in conflicts.items():
        if impl_path in APPROVED_SHARED_IMPLEMENTATION_PATHS:
            continue
        unique_owners = sorted(set(owners))
        errors.append(f"implementation path conflict: {impl_path} -> {', '.join(unique_owners)}")

    for dirname in SOURCE_DIRS:
        source_root = root / dirname
        if not source_root.exists():
            continue
        for path in source_root.rglob("*.py"):
            if ACCOUNT_SPECIFIC_FILE_RE.match(path.name):
                errors.append(f"account-specific source filename is forbidden: {path.relative_to(root)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = detect_duplicate_capabilities(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("duplicate capability validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
