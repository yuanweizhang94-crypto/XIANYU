from __future__ import annotations

from dataclasses import replace

import pytest

from xianyu_system.reply.domain import (
    NormalizationFlag,
    ReplyAuditIdentifiers,
    ReplyAuthorizationState,
    ReplyCondition,
    ReplyDecisionType,
    ReplyEvaluationContext,
    ReplyLifecycleState,
    ReplyReasonCode,
    ReplyRiskState,
    ReplyRuleSnapshot,
)
from xianyu_system.reply.evaluator import DeterministicReplyEvaluator

PROFILE_ID = "00000000-0000-4000-8000-000000000101"
CONVERSATION_ID = "00000000-0000-4000-8000-000000000102"
MESSAGE_ID = "00000000-0000-4000-8000-000000000103"
RULE_ID = "00000000-0000-4000-8000-000000000104"
RULE_ID_2 = "00000000-0000-4000-8000-000000000105"
TEMPLATE_ID = "00000000-0000-4000-8000-000000000106"


def context(**overrides: object) -> ReplyEvaluationContext:
    values = {
        "identifiers": ReplyAuditIdentifiers(
            profile_id=PROFILE_ID,
            account_reference="acct",
            conversation_id=CONVERSATION_ID,
            message_id=MESSAGE_ID,
        ),
        "content_text": "  你好，想要购买Ａ款  ",
        "language_hint": "ZH-CN",
        "is_synthetic": True,
        "authorization_state": ReplyAuthorizationState.EXPLICITLY_AUTHORIZED,
        "risk_state": ReplyRiskState.LOW,
    }
    values.update(overrides)
    return ReplyEvaluationContext(**values)


def condition(
    *,
    field_name: str = "content_text",
    operator: str = "contains",
    expected_value: str = "购买A款",
    flags: tuple[NormalizationFlag, ...] = (NormalizationFlag.TRIM, NormalizationFlag.NFKC),
    case_sensitive: bool = False,
) -> ReplyCondition:
    return ReplyCondition(
        rule_id=RULE_ID,
        rule_version=1,
        field_name=field_name,
        operator=operator,
        expected_value=expected_value,
        normalization_flags=flags,
        case_sensitive=case_sensitive,
    )


def snapshot(
    *,
    rule_id: str = RULE_ID,
    priority: int = 1,
    conditions: tuple[ReplyCondition, ...] | None = None,
    lifecycle_state: ReplyLifecycleState = ReplyLifecycleState.ENABLED,
) -> ReplyRuleSnapshot:
    return ReplyRuleSnapshot(
        rule_id=rule_id,
        rule_version=1,
        template_id=TEMPLATE_ID,
        template_version=1,
        lifecycle_state=lifecycle_state,
        priority=priority,
        conditions=((condition(),) if conditions is None else conditions),
    )


def evaluate(ctx: ReplyEvaluationContext, *snapshots_: ReplyRuleSnapshot):
    return DeterministicReplyEvaluator().evaluate(ctx, tuple(snapshots_))


@pytest.mark.parametrize(
    ("overrides", "decision_type", "reason"),
    [
        (
            {"is_synthetic": False},
            ReplyDecisionType.INVALID_INPUT,
            ReplyReasonCode.MISSING_REQUIRED_INPUT,
        ),
        (
            {"authorization_state": ReplyAuthorizationState.UNKNOWN},
            ReplyDecisionType.ESCALATE,
            ReplyReasonCode.AUTHORIZATION_UNKNOWN,
        ),
        (
            {"risk_state": ReplyRiskState.UNKNOWN},
            ReplyDecisionType.ESCALATE,
            ReplyReasonCode.RISK_UNKNOWN,
        ),
        (
            {"risk_state": ReplyRiskState.BLOCKED},
            ReplyDecisionType.SUPPRESSED,
            ReplyReasonCode.SAFETY_SUPPRESSED,
        ),
        ({"language_hint": "en"}, ReplyDecisionType.ESCALATE, ReplyReasonCode.UNSUPPORTED_LANGUAGE),
        (
            {"suppression_asserted": True},
            ReplyDecisionType.SUPPRESSED,
            ReplyReasonCode.SENSITIVE_TOPIC,
        ),
        (
            {"human_transfer_requested": True},
            ReplyDecisionType.ESCALATE,
            ReplyReasonCode.HUMAN_TRANSFER_REQUIRED,
        ),
    ],
)
def test_context_gate_order_is_fail_closed(
    overrides: dict[str, object],
    decision_type: ReplyDecisionType,
    reason: ReplyReasonCode,
) -> None:
    result = evaluate(context(**overrides), snapshot())
    assert result.decision_type == decision_type
    assert result.reason_code == reason


@pytest.mark.parametrize("language", ["zh", "ZH-CN", " zh-hans "])
def test_supported_chinese_language_hints_can_match(language: str) -> None:
    result = evaluate(context(language_hint=language), snapshot())
    assert result.decision_type == ReplyDecisionType.REPLY
    assert result.reason_code == ReplyReasonCode.READY_TO_REPLY
    assert result.rule_id == RULE_ID
    assert result.rule_version == 1
    assert not hasattr(result, "rendered_text")


@pytest.mark.parametrize(
    ("operator", "expected"),
    [
        ("equals", "你好，想要购买A款"),
        ("contains", "购买A款"),
        ("starts_with", "你好"),
        ("ends_with", "款"),
    ],
)
def test_supported_operators_trim_nfkc_and_casefold(operator: str, expected: str) -> None:
    result = evaluate(
        context(), snapshot(conditions=(condition(operator=operator, expected_value=expected),))
    )
    assert result.decision_type == ReplyDecisionType.REPLY


def test_case_sensitive_and_and_composition_are_deterministic() -> None:
    case_sensitive = condition(expected_value="购买a款", case_sensitive=True)
    language = condition(field_name="language_hint", operator="equals", expected_value="zh-cn")
    assert (
        evaluate(context(), snapshot(conditions=(case_sensitive,))).decision_type
        == ReplyDecisionType.NO_MATCH
    )
    assert (
        evaluate(
            context(language_hint="zh-cn"), snapshot(conditions=(condition(), language))
        ).decision_type
        == ReplyDecisionType.REPLY
    )


def test_no_match_lower_priority_ignored_and_same_priority_conflict() -> None:
    no_match = condition(expected_value="不存在")
    assert (
        evaluate(context(), snapshot(conditions=(no_match,))).reason_code
        == ReplyReasonCode.NO_RULE_MATCHED
    )
    high = snapshot(priority=0)
    low = snapshot(rule_id=RULE_ID_2, priority=5)
    assert evaluate(context(), low, high).rule_id == RULE_ID
    conflict = evaluate(context(), high, snapshot(rule_id=RULE_ID_2, priority=0))
    assert conflict.decision_type == ReplyDecisionType.CONFLICT
    assert conflict.reason_code == ReplyReasonCode.DUPLICATE_HIGHEST_PRIORITY_MATCH


def test_invalid_rule_configuration_returns_invalid_input() -> None:
    invalid_priority = replace(snapshot(), priority=-1)
    assert evaluate(context(), invalid_priority).reason_code == ReplyReasonCode.INVALID_PRIORITY
    empty = snapshot(conditions=())
    assert evaluate(context(), empty).reason_code == ReplyReasonCode.EMPTY_CONDITION_SET
    bad_field = snapshot(conditions=(condition(field_name="profile_id"),))
    assert evaluate(context(), bad_field).reason_code == ReplyReasonCode.UNSUPPORTED_FIELD
    bad_operator = snapshot(conditions=(condition(operator="regex"),))
    assert evaluate(context(), bad_operator).reason_code == ReplyReasonCode.UNSUPPORTED_OPERATOR


def test_disabled_rules_do_not_participate_and_repeated_execution_is_stable() -> None:
    disabled = snapshot(lifecycle_state=ReplyLifecycleState.DISABLED)
    first = evaluate(context(), disabled, snapshot())
    second = evaluate(context(), disabled, snapshot())
    assert first == second
    assert first.decision_type == ReplyDecisionType.REPLY
