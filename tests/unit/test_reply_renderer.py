from __future__ import annotations

from datetime import UTC, datetime

import pytest

from xianyu_system.reply.domain import (
    ReplyLifecycleState,
    ReplyReasonCode,
    ReplyRenderError,
    ReplyTemplate,
    ReplyTemplateRenderInput,
    TemplateVariableName,
)
from xianyu_system.reply.renderer import FixedScriptTemplateRenderer

NOW = datetime(2026, 1, 1, tzinfo=UTC)
PROFILE_ID = "00000000-0000-4000-8000-000000000201"
TEMPLATE_ID = "00000000-0000-4000-8000-000000000202"


def template(script: str, allowlist: tuple[str, ...] = ("name", "code")) -> ReplyTemplate:
    return ReplyTemplate(
        template_id=TEMPLATE_ID,
        version=1,
        profile_id=PROFILE_ID,
        account_reference="acct",
        lifecycle_state=ReplyLifecycleState.ENABLED,
        script_text=script,
        variable_allowlist=tuple(TemplateVariableName(item) for item in allowlist),
        row_version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def render(
    script: str, variables: dict[str, str], allowlist: tuple[str, ...] = ("name", "code")
) -> str:
    return (
        FixedScriptTemplateRenderer()
        .render(ReplyTemplateRenderInput(template=template(script, allowlist), variables=variables))
        .text
    )


def test_allowlisted_substitution_multiple_variables_and_escaped_braces() -> None:
    assert (
        render("你好 {name}，编号 {code}，{{固定}}", {"name": "买家", "code": "A1"})
        == "你好 买家，编号 A1，{固定}"
    )


@pytest.mark.parametrize(
    ("script", "variables", "reason"),
    [
        ("你好 {name}", {}, ReplyReasonCode.MISSING_TEMPLATE_VARIABLE),
        ("你好 {other}", {"other": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {name.value}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {name[0]}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {name!r}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {name:>5}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {name()}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
        ("你好 {0}", {"name": "x"}, ReplyReasonCode.FORBIDDEN_PLACEHOLDER),
    ],
)
def test_forbidden_or_missing_placeholders_are_sanitized(
    script: str,
    variables: dict[str, str],
    reason: ReplyReasonCode,
) -> None:
    with pytest.raises(ReplyRenderError) as exc_info:
        render(script, variables)
    assert exc_info.value.reason_code == reason


def test_renderer_has_no_file_environment_or_network_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("pathlib.Path.read_text", lambda *args, **kwargs: pytest.fail("file read"))
    assert render("固定 {name}", {"name": "文本"}) == "固定 文本"
