"""Lazy public surface for the local deterministic Reply boundary."""

from __future__ import annotations

from typing import Any

_DOMAIN_EXPORTS = {
    "ConditionOperator",
    "InvalidReplyInput",
    "ReplyAuditEvent",
    "ReplyAuditIdentifiers",
    "ReplyAuthorizationState",
    "ReplyBoundaryError",
    "ReplyCondition",
    "ReplyDecision",
    "ReplyDecisionType",
    "ReplyErrorCode",
    "ReplyEvaluationContext",
    "ReplyEvaluationResult",
    "ReplyLifecycleState",
    "ReplyPriority",
    "ReplyReasonCode",
    "ReplyRenderedText",
    "ReplyRiskState",
    "ReplyRule",
    "ReplyRuleSnapshot",
    "ReplyTemplate",
    "ReplyTemplateRenderInput",
    "TemplateVariableName",
    "NormalizationFlag",
    "ReplyMappingError",
    "ReplyPersistenceError",
    "ReplyRenderError",
}
__all__ = sorted(
    [
        *_DOMAIN_EXPORTS,
        "DeterministicReplyEvaluator",
        "FixedScriptTemplateRenderer",
        "ReplyMessageMapper",
        "ReplyService",
    ]
)


def __getattr__(name: str) -> Any:
    if name in _DOMAIN_EXPORTS:
        from xianyu_system.reply import domain

        return getattr(domain, name)
    if name == "DeterministicReplyEvaluator":
        from xianyu_system.reply.evaluator import DeterministicReplyEvaluator

        return DeterministicReplyEvaluator
    if name == "FixedScriptTemplateRenderer":
        from xianyu_system.reply.renderer import FixedScriptTemplateRenderer

        return FixedScriptTemplateRenderer
    if name == "ReplyMessageMapper":
        from xianyu_system.reply.mapper import ReplyMessageMapper

        return ReplyMessageMapper
    if name == "ReplyService":
        from xianyu_system.reply.service import ReplyService

        return ReplyService
    raise AttributeError(name)
