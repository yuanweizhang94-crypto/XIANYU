"""Fixed-script renderer for the local Reply boundary."""

from __future__ import annotations

import string

from xianyu_system.reply.domain import (
    ReplyReasonCode,
    ReplyRenderedText,
    ReplyRenderError,
    ReplyTemplateRenderInput,
    TemplateVariableName,
)


class FixedScriptTemplateRenderer:
    """Render allowlisted ``{variable_name}`` placeholders only."""

    def render(self, render_input: ReplyTemplateRenderInput) -> ReplyRenderedText:
        template = render_input.template
        if not template.is_enabled:
            raise ReplyRenderError(reason_code=ReplyReasonCode.MISSING_TEMPLATE)
        allowlist = {item.value for item in template.variable_allowlist}
        variables = dict(render_input.variables)
        values: dict[str, str] = {}
        for _literal, field_name, format_spec, conversion in string.Formatter().parse(
            template.script_text
        ):
            if field_name is None:
                continue
            if field_name == "" or conversion is not None or format_spec:
                raise ReplyRenderError(reason_code=ReplyReasonCode.FORBIDDEN_PLACEHOLDER)
            try:
                normalized_name = TemplateVariableName(field_name).value
            except Exception:
                raise ReplyRenderError(reason_code=ReplyReasonCode.FORBIDDEN_PLACEHOLDER) from None
            if normalized_name != field_name or normalized_name not in allowlist:
                raise ReplyRenderError(reason_code=ReplyReasonCode.FORBIDDEN_PLACEHOLDER)
            if normalized_name not in variables or not isinstance(variables[normalized_name], str):
                raise ReplyRenderError(reason_code=ReplyReasonCode.MISSING_TEMPLATE_VARIABLE)
            values[normalized_name] = variables[normalized_name]
        try:
            return ReplyRenderedText(template.script_text.format(**values))
        except (KeyError, IndexError):
            raise ReplyRenderError(reason_code=ReplyReasonCode.MISSING_TEMPLATE_VARIABLE) from None
        except (AttributeError, ValueError):
            raise ReplyRenderError(reason_code=ReplyReasonCode.FORBIDDEN_PLACEHOLDER) from None
