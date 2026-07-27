from __future__ import annotations

from datetime import UTC, datetime

import pytest

from xianyu_system.reply.domain import (
    ConditionOperator,
    InvalidReplyInput,
    NormalizationFlag,
    ReplyAuditEvent,
    ReplyAuditIdentifiers,
    ReplyCondition,
    ReplyDecision,
    ReplyDecisionType,
    ReplyLifecycleState,
    ReplyPriority,
    ReplyReasonCode,
    ReplyRule,
    ReplyTemplate,
    TemplateVariableName,
    validate_lifecycle_transition,
)

NOW = datetime(2026, 1, 1, tzinfo=UTC)
PROFILE_ID = "00000000-0000-4000-8000-000000000001"
CONVERSATION_ID = "00000000-0000-4000-8000-000000000002"
MESSAGE_ID = "00000000-0000-4000-8000-000000000003"
RULE_ID = "00000000-0000-4000-8000-000000000004"
TEMPLATE_ID = "00000000-0000-4000-8000-000000000005"
AUDIT_ID = "00000000-0000-4000-8000-000000000006"


def template() -> ReplyTemplate:
    return ReplyTemplate(
        template_id=TEMPLATE_ID,
        version=1,
        profile_id=PROFILE_ID,
        account_reference="acct",
        lifecycle_state=ReplyLifecycleState.ENABLED,
        script_text="固定回复 {account_reference}",
        variable_allowlist=(TemplateVariableName("account_reference"),),
        row_version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def rule(version: int = 1) -> ReplyRule:
    return ReplyRule(
        rule_id=RULE_ID,
        version=version,
        profile_id=PROFILE_ID,
        account_reference="acct",
        lifecycle_state=ReplyLifecycleState.ENABLED,
        template_id=TEMPLATE_ID,
        template_version=1,
        priority=ReplyPriority(0),
        row_version=1,
        created_at=NOW,
        updated_at=NOW,
        name="synthetic rule",
    )


def test_rule_identity_is_composite_and_versions_are_positive() -> None:
    first = rule(1)
    second = rule(2)
    assert (first.rule_id, first.version) != (second.rule_id, second.version)
    assert first.rule_id == second.rule_id
    with pytest.raises(InvalidReplyInput):
        rule(0)
    with pytest.raises(InvalidReplyInput):
        ReplyPriority(-1)


def test_lifecycle_transitions_and_archived_immutability_are_enforced() -> None:
    assert validate_lifecycle_transition("DRAFT", "ENABLED") == ReplyLifecycleState.ENABLED
    assert validate_lifecycle_transition("ENABLED", "DISABLED") == ReplyLifecycleState.DISABLED
    assert validate_lifecycle_transition("DISABLED", "ENABLED") == ReplyLifecycleState.ENABLED
    assert validate_lifecycle_transition("DRAFT", "ARCHIVED") == ReplyLifecycleState.ARCHIVED
    assert validate_lifecycle_transition("DISABLED", "ARCHIVED") == ReplyLifecycleState.ARCHIVED
    for current, target in [("ENABLED", "ARCHIVED"), ("ARCHIVED", "DISABLED")]:
        with pytest.raises(InvalidReplyInput):
            validate_lifecycle_transition(current, target)


def test_template_variable_names_and_rendered_text_inputs_are_validated() -> None:
    assert TemplateVariableName("reply_text").value == "reply_text"
    for value in ["", "1bad", "bad.name", "bad[index]", "bad call"]:
        with pytest.raises(InvalidReplyInput):
            TemplateVariableName(value)
    assert template().is_enabled is True


def test_audit_identifiers_and_rule_version_pairing_are_required() -> None:
    identifiers = ReplyAuditIdentifiers(
        profile_id=PROFILE_ID,
        account_reference="acct",
        conversation_id=CONVERSATION_ID,
        message_id=MESSAGE_ID,
    )
    event = ReplyAuditEvent(
        audit_event_id=AUDIT_ID,
        identifiers=identifiers,
        decision_type=ReplyDecisionType.NO_MATCH,
        reason_code=ReplyReasonCode.NO_RULE_MATCHED,
        occurred_at=NOW,
    )
    assert event.rule_id is None
    with pytest.raises(InvalidReplyInput):
        ReplyDecision(
            decision_type=ReplyDecisionType.REPLY,
            reason_code=ReplyReasonCode.READY_TO_REPLY,
            identifiers=identifiers,
            rule_id=RULE_ID,
            rule_version=None,
        )


def test_condition_canonical_normalization_and_operator_values_are_stable() -> None:
    condition = ReplyCondition(
        rule_id=RULE_ID,
        rule_version=1,
        field_name="content_text",
        operator=ConditionOperator.CONTAINS.value,
        expected_value="  Ａ  ",
        normalization_flags=(NormalizationFlag.TRIM, NormalizationFlag.NFKC),
    )
    assert condition.canonical_normalization == "NFKC,TRIM"
