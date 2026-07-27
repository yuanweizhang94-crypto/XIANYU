from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REPLY_PACKAGE = ROOT / "app" / "xianyu_system" / "reply"
MIGRATION = ROOT / "migrations" / "versions" / "0004_xianyu_reply_boundary.py"


def read_sources() -> dict[str, str]:
    paths = list(REPLY_PACKAGE.glob("*.py")) + [MIGRATION]
    return {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8") for path in paths}


def test_reply_sources_have_no_external_platform_sender_ai_wecom_api_or_worker_behavior() -> None:
    combined = "\n".join(read_sources().values()).lower()
    forbidden = [
        "requests",
        "httpx",
        "aiohttp",
        "websocket",
        "playwright",
        "selenium",
        "browser profile",
        "wecom",
        "openai",
        "anthropic",
        "send_message",
        "scheduler",
        "apscheduler",
        "fastapi",
        "apirouter",
        "click.command",
        "typer.",
    ]
    for term in forbidden:
        assert term not in combined


def test_reply_sources_do_not_store_full_content_rendered_reply_or_arbitrary_metadata_in_audit() -> (
    None
):
    from xianyu_system.reply.persistence import reply_audit_event_table

    audit_columns = set(reply_audit_event_table.c.keys())
    for forbidden in [
        "message_content",
        "rendered_text",
        "raw_payload",
        "metadata",
        "extras",
        "properties",
    ]:
        assert forbidden not in audit_columns


def test_importing_reply_package_and_domain_has_no_persistence_or_engine_side_effects() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "app")
    script = """
import importlib
import sys
package = importlib.import_module("xianyu_system.reply")
assert package.__name__ == "xianyu_system.reply"
assert "xianyu_system.reply.persistence" not in sys.modules
domain = importlib.import_module("xianyu_system.reply.domain")
assert domain.ReplyDecisionType.REPLY.value == "REPLY"
assert "xianyu_system.reply.persistence" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stderr == ""


def test_runtime_components_do_not_call_network_subprocess_home_or_file_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from datetime import UTC, datetime

    from xianyu_system.reply.domain import (
        ReplyLifecycleState,
        ReplyTemplate,
        ReplyTemplateRenderInput,
        TemplateVariableName,
    )
    from xianyu_system.reply.renderer import FixedScriptTemplateRenderer

    def blocked(*args: object, **kwargs: object) -> object:
        raise AssertionError("external behavior is blocked")

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(subprocess, "run", blocked)
    monkeypatch.setattr(Path, "home", blocked)
    monkeypatch.setattr(Path, "read_text", blocked)
    template = ReplyTemplate(
        template_id="00000000-0000-4000-8000-000000000601",
        version=1,
        profile_id="00000000-0000-4000-8000-000000000602",
        account_reference="acct",
        lifecycle_state=ReplyLifecycleState.ENABLED,
        script_text="固定 {name}",
        variable_allowlist=(TemplateVariableName("name"),),
        row_version=1,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        updated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    result = FixedScriptTemplateRenderer().render(
        ReplyTemplateRenderInput(template=template, variables={"name": "文本"})
    )
    assert result.text == "固定 文本"


def test_reply_migration_has_no_seed_data_or_startup_auto_migration() -> None:
    migration_source = MIGRATION.read_text(encoding="utf-8")
    env_source = (ROOT / "migrations" / "env.py").read_text(encoding="utf-8")
    app_source = (ROOT / "app" / "xianyu_system" / "application.py").read_text(encoding="utf-8")
    assert "bulk_insert" not in migration_source
    assert "op.execute" not in migration_source
    assert "command.upgrade" not in app_source
    assert "upgrade_database(" not in app_source
    assert "reply_template_table" in env_source
