from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

from xianyu_system.application import create_application

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "openapi.yaml"
FORBIDDEN_PATHS = {
    "/",
    "/ready",
    "/live",
    "/metrics",
    "/status",
    "/api/health",
    "/login",
    "/messages",
    "/replies",
    "/products",
    "/publish",
    "/schedule",
    "/wecom",
    "/ai",
    "/accounts",
}


def contract_schema() -> dict[str, object]:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_health_openapi_contract_contains_only_health_path() -> None:
    contract = contract_schema()

    assert contract["openapi"] == "3.1.0"
    assert set(contract["paths"]) == {"/health"}
    assert set(contract["paths"]).isdisjoint(FORBIDDEN_PATHS)
    assert "security" not in contract
    assert "securitySchemes" not in contract.get("components", {})


def test_health_contract_operation_and_responses_match_runtime_openapi() -> None:
    contract = contract_schema()
    runtime = create_application().openapi()
    contract_operation = contract["paths"]["/health"]["get"]
    runtime_operation = runtime["paths"]["/health"]["get"]

    assert set(runtime["paths"]) == {"/health"}
    assert contract_operation["operationId"] == runtime_operation["operationId"] == "get_health"
    assert contract_operation["summary"] == runtime_operation["summary"] == "Get Core health"
    assert contract_operation["description"] == runtime_operation["description"]
    assert set(contract_operation["responses"]) == {"200", "503"}
    assert {"200", "503"} <= set(runtime_operation["responses"])
    for status in ["200", "503"]:
        assert (
            contract_operation["responses"][status]["content"]["application/json"]["schema"]["$ref"]
            == "#/components/schemas/HealthResponse"
        )
        assert (
            runtime_operation["responses"][status]["content"]["application/json"]["schema"]["$ref"]
            == "#/components/schemas/HealthResponse"
        )


def test_health_contract_schemas_preserve_safe_required_fields_and_enums() -> None:
    schemas = contract_schema()["components"]["schemas"]

    assert schemas["HealthResponse"]["additionalProperties"] is False
    assert schemas["HealthResponse"]["required"] == [
        "status",
        "service",
        "version",
        "environment",
        "database",
        "scheduler",
    ]
    assert schemas["HealthResponse"]["properties"]["status"]["enum"] == ["ok", "degraded"]
    assert schemas["HealthResponse"]["properties"]["environment"]["enum"] == ["local", "test"]

    assert schemas["DatabaseHealth"]["additionalProperties"] is False
    assert schemas["DatabaseHealth"]["required"] == ["status", "connected", "journal_mode"]
    assert schemas["DatabaseHealth"]["properties"]["status"]["enum"] == ["ok", "unavailable"]

    assert schemas["SchedulerHealth"]["additionalProperties"] is False
    assert schemas["SchedulerHealth"]["required"] == ["status", "running", "job_count", "timezone"]
    assert schemas["SchedulerHealth"]["properties"]["status"]["enum"] == ["ok", "unavailable"]
    assert schemas["SchedulerHealth"]["properties"]["timezone"]["enum"] == ["UTC"]
    assert schemas["SchedulerHealth"]["properties"]["job_count"]["minimum"] == 0


def test_health_contract_contains_no_sensitive_or_external_details() -> None:
    text = CONTRACT.read_text(encoding="utf-8").lower()
    for forbidden in [
        "cookie",
        "token",
        "secret",
        "password",
        "authorization",
        "account",
        "customer",
        "database_path",
        "traceback",
        "exception",
        "http://",
        "https://",
        "wecom",
        "openai",
        "login",
    ]:
        assert forbidden not in text


def test_runtime_openapi_generation_has_no_file_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app"), str(ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    script = "from xianyu_system.application import create_application; schema=create_application().openapi(); assert set(schema['paths']) == {'/health'}"

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == ""
    assert result.stderr == ""
    assert not (tmp_path / "data").exists()
    assert not (tmp_path / "logs").exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3", "*.log"]:
        assert list(tmp_path.glob(pattern)) == []
