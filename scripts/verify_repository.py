from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

import jsonschema
import yaml

from scripts.detect_duplicate_capabilities import detect_duplicate_capabilities
from scripts.generate_state import build_project_state, project_state_json
from scripts.repo_utils import load_capabilities, read_yaml, required_repo_paths
from scripts.security_scan import scan as security_scan
from scripts.validate_change import validate_change

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CAPABILITY_STATUSES = {"planned", "implementing", "verified", "deprecated"}


class VerificationError(RuntimeError):
    """Raised when repository verification fails."""


def check_repository_structure(root: Path) -> None:
    missing = [path for path in required_repo_paths() if not (root / path).exists()]
    if missing:
        raise VerificationError(f"missing required paths: {', '.join(missing)}")

    for path in [
        "contracts/openapi.yaml",
        "contracts/schemas/project-state.schema.json",
        "contracts/schemas/capability-registry.schema.json",
        ".github/CODEOWNERS",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/feature.yml",
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/workflows/quality.yml",
        ".github/workflows/tests.yml",
        ".github/workflows/security.yml",
    ]:
        if not (root / path).exists():
            raise VerificationError(f"missing required file: {path}")


def check_change(root: Path) -> None:
    errors = validate_change(root)
    if errors:
        raise VerificationError("; ".join(errors))


def check_capability_registry(root: Path) -> None:
    registry = read_yaml(root / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((root / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)
    capabilities = load_capabilities(root)
    if len(capabilities) != 10:
        raise VerificationError(f"expected 10 capabilities, found {len(capabilities)}")

    for capability in capabilities:
        cap_id = str(capability.get("id"))
        status = capability.get("status")
        active_change = capability.get("active_change")
        last_verified_commit = capability.get("last_verified_commit")
        if status not in ALLOWED_CAPABILITY_STATUSES:
            raise VerificationError(f"invalid capability status for {cap_id}: {status}")
        if status == "planned" and active_change is not None:
            raise VerificationError(f"planned capability must not bind active_change: {cap_id}")
        if status == "implementing" and not isinstance(active_change, str):
            raise VerificationError(f"implementing capability must bind active_change: {cap_id}")
        if status == "verified" and not isinstance(last_verified_commit, str):
            raise VerificationError(f"verified capability must record last_verified_commit: {cap_id}")
        if status == "verified" and active_change is not None:
            raise VerificationError(f"verified capability must clear active_change: {cap_id}")

        spec_path = root / str(capability["specification"])
        if not spec_path.exists():
            raise VerificationError(f"missing capability spec: {spec_path}")


def check_json_schemas(root: Path) -> None:
    for path in (root / "contracts" / "schemas").glob("*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)


def check_openapi(root: Path) -> None:
    openapi = yaml.safe_load((root / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    if not isinstance(openapi, dict):
        raise VerificationError("openapi root must be an object")
    if openapi.get("openapi") != "3.1.0":
        raise VerificationError("openapi version must be 3.1.0")
    if openapi.get("paths") != {}:
        raise VerificationError("paths must be empty in CHG-0001")


def check_duplicates(root: Path) -> None:
    errors = detect_duplicate_capabilities(root)
    if errors:
        raise VerificationError("; ".join(errors))


def run_pytest(root: Path) -> None:
    result = subprocess.run(["python", "-m", "pytest"], cwd=root, text=True)
    if result.returncode != 0:
        raise VerificationError("pytest failed")


def validate_project_state(root: Path) -> None:
    output = root / "generated" / "PROJECT_STATE.json"
    if not output.exists():
        raise VerificationError("missing generated/PROJECT_STATE.json; run python scripts/generate_state.py")

    actual_text = output.read_text(encoding="utf-8")
    expected_text = project_state_json(root)
    if actual_text != expected_text:
        raise VerificationError("generated/PROJECT_STATE.json is stale; run python scripts/generate_state.py")

    state = json.loads(actual_text)
    schema = json.loads((root / "contracts" / "schemas" / "project-state.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(state, schema)

    expected_state = build_project_state(root)
    if state != expected_state:
        raise VerificationError("generated/PROJECT_STATE.json content differs from in-memory project state")


def check_security(root: Path) -> None:
    findings = security_scan(root)
    if findings:
        raise VerificationError("; ".join(findings))


def run_step(name: str, func: Callable[[Path], None], root: Path) -> None:
    print(f"[verify] {name}")
    func(root)


def main() -> int:
    steps: list[tuple[str, Callable[[Path], None]]] = [
        ("repository structure", check_repository_structure),
        ("change validation", check_change),
        ("capability registry", check_capability_registry),
        ("json schemas", check_json_schemas),
        ("openapi baseline", check_openapi),
        ("duplicate capabilities", check_duplicates),
        ("security scan", check_security),
        ("unit and acceptance tests", run_pytest),
        ("validate tracked project state", validate_project_state),
    ]
    try:
        for name, func in steps:
            run_step(name, func, ROOT)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
    print("repository verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
