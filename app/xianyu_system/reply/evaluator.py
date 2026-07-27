"""Pure deterministic evaluator for the local Reply boundary."""

from __future__ import annotations

from xianyu_system.reply.domain import (
    ConditionOperator,
    ReplyAuthorizationState,
    ReplyCondition,
    ReplyDecisionType,
    ReplyEvaluationContext,
    ReplyEvaluationResult,
    ReplyLifecycleState,
    ReplyReasonCode,
    ReplyRiskState,
    ReplyRuleSnapshot,
    condition_field_supported,
    normalize_text_for_condition,
)

_SUPPORTED_LANGUAGE_HINTS = frozenset({"zh", "zh-cn", "zh-hans"})


class DeterministicReplyEvaluator:
    """Evaluate approved local rule snapshots without side effects."""

    def evaluate(
        self,
        context: ReplyEvaluationContext,
        snapshots: tuple[ReplyRuleSnapshot, ...],
    ) -> ReplyEvaluationResult:
        boundary_result = self._validate_context(context)
        if boundary_result is not None:
            return boundary_result
        matches: list[ReplyRuleSnapshot] = []
        for snapshot in snapshots:
            validation_result = self._validate_snapshot(snapshot)
            if validation_result is not None:
                return validation_result
            if snapshot.lifecycle_state != ReplyLifecycleState.ENABLED:
                continue
            if self._matches_all(context, snapshot.conditions):
                matches.append(snapshot)
        if not matches:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.NO_MATCH,
                reason_code=ReplyReasonCode.NO_RULE_MATCHED,
            )
        best_priority = min(snapshot.priority for snapshot in matches)
        best_matches = [snapshot for snapshot in matches if snapshot.priority == best_priority]
        if len(best_matches) > 1:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.CONFLICT,
                reason_code=ReplyReasonCode.DUPLICATE_HIGHEST_PRIORITY_MATCH,
            )
        selected = best_matches[0]
        return ReplyEvaluationResult(
            decision_type=ReplyDecisionType.REPLY,
            reason_code=ReplyReasonCode.READY_TO_REPLY,
            rule_id=selected.rule_id,
            rule_version=selected.rule_version,
            template_id=selected.template_id,
            template_version=selected.template_version,
        )

    def _validate_context(self, context: ReplyEvaluationContext) -> ReplyEvaluationResult | None:
        if not context.is_synthetic:
            return _invalid(ReplyReasonCode.MISSING_REQUIRED_INPUT)
        if context.authorization_state != ReplyAuthorizationState.EXPLICITLY_AUTHORIZED:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.ESCALATE,
                reason_code=ReplyReasonCode.AUTHORIZATION_UNKNOWN,
            )
        if context.risk_state == ReplyRiskState.BLOCKED:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.SUPPRESSED,
                reason_code=ReplyReasonCode.SAFETY_SUPPRESSED,
            )
        if context.risk_state not in {ReplyRiskState.ALLOWED, ReplyRiskState.LOW}:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.ESCALATE,
                reason_code=ReplyReasonCode.RISK_UNKNOWN,
            )
        language = "" if context.language_hint is None else context.language_hint.strip().casefold()
        if language not in _SUPPORTED_LANGUAGE_HINTS:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.ESCALATE,
                reason_code=ReplyReasonCode.UNSUPPORTED_LANGUAGE,
            )
        if context.suppression_asserted or context.sensitive_topic_asserted:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.SUPPRESSED,
                reason_code=ReplyReasonCode.SENSITIVE_TOPIC,
            )
        if context.human_transfer_requested:
            return ReplyEvaluationResult(
                decision_type=ReplyDecisionType.ESCALATE,
                reason_code=ReplyReasonCode.HUMAN_TRANSFER_REQUIRED,
            )
        return None

    def _validate_snapshot(self, snapshot: ReplyRuleSnapshot) -> ReplyEvaluationResult | None:
        if snapshot.lifecycle_state != ReplyLifecycleState.ENABLED:
            return None
        if snapshot.priority < 0:
            return _invalid(ReplyReasonCode.INVALID_PRIORITY)
        if not snapshot.conditions:
            return _invalid(ReplyReasonCode.EMPTY_CONDITION_SET)
        for condition in snapshot.conditions:
            if not condition_field_supported(condition.field_name):
                return _invalid(ReplyReasonCode.UNSUPPORTED_FIELD)
            try:
                ConditionOperator(condition.operator)
            except ValueError:
                return _invalid(ReplyReasonCode.UNSUPPORTED_OPERATOR)
        return None

    def _matches_all(
        self,
        context: ReplyEvaluationContext,
        conditions: tuple[ReplyCondition, ...],
    ) -> bool:
        return all(self._matches_condition(context, condition) for condition in conditions)

    def _matches_condition(
        self, context: ReplyEvaluationContext, condition: ReplyCondition
    ) -> bool:
        source_value = {
            "content_text": context.content_text,
            "language_hint": context.language_hint or "",
        }[condition.field_name]
        source = normalize_text_for_condition(
            source_value,
            flags=condition.normalization_flags,
            case_sensitive=condition.case_sensitive,
        )
        expected = normalize_text_for_condition(
            condition.expected_value,
            flags=condition.normalization_flags,
            case_sensitive=condition.case_sensitive,
        )
        operator = ConditionOperator(condition.operator)
        if operator == ConditionOperator.EQUALS:
            return source == expected
        if operator == ConditionOperator.CONTAINS:
            return expected in source
        if operator == ConditionOperator.STARTS_WITH:
            return source.startswith(expected)
        return source.endswith(expected)


def _invalid(reason_code: ReplyReasonCode) -> ReplyEvaluationResult:
    return ReplyEvaluationResult(
        decision_type=ReplyDecisionType.INVALID_INPUT,
        reason_code=reason_code,
    )
