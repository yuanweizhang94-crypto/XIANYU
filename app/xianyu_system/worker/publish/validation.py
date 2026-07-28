"""Fail-closed local validation for deterministic publish decisions."""

from __future__ import annotations

from xianyu_system.worker.publish.domain import (
    ListingDraft,
    PublishAuthorizationState,
    PublishDecision,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishFailureCategory,
    PublishReasonCode,
    PublishRequest,
    PublishRiskState,
    PublishValidationResult,
    ValidationIssue,
)
from xianyu_system.worker.publish.fingerprint import compute_publish_fingerprint


class PublishValidator:
    """Validate one local synthetic publish request in the approved fixed order."""

    def validate(
        self,
        draft: ListingDraft,
        request: PublishRequest,
        context: PublishEvaluationContext,
    ) -> PublishValidationResult:
        if not request.synthetic_fixture or not context.synthetic_fixture:
            return self._invalid(
                field="synthetic_fixture",
                reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
                failure_category=PublishFailureCategory.VALIDATION_ERROR,
                safe_detail="synthetic fixture must be true",
            )
        if draft.draft_id != request.draft_id or draft.revision != request.draft_revision:
            return self._invalid(
                field="draft_revision",
                reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
                failure_category=PublishFailureCategory.VALIDATION_ERROR,
                safe_detail="draft identity mismatch",
            )
        if request.authorization_state != context.authorization_state:
            return self._invalid(
                field="authorization_state",
                reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
                failure_category=PublishFailureCategory.VALIDATION_ERROR,
                safe_detail="authorization context mismatch",
            )
        if request.risk_state != context.risk_state:
            return self._invalid(
                field="risk_state",
                reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
                failure_category=PublishFailureCategory.VALIDATION_ERROR,
                safe_detail="risk context mismatch",
            )
        if request.authorization_state == PublishAuthorizationState.DENIED:
            return self._invalid(
                field="authorization_state",
                reason_code=PublishReasonCode.AUTHORIZATION_DENIED,
                failure_category=PublishFailureCategory.AUTHORIZATION_ERROR,
                safe_detail="authorization denied",
            )
        if request.authorization_state == PublishAuthorizationState.UNKNOWN:
            return self._invalid(
                field="authorization_state",
                reason_code=PublishReasonCode.AUTHORIZATION_UNKNOWN,
                failure_category=PublishFailureCategory.AUTHORIZATION_ERROR,
                safe_detail="authorization unknown",
            )
        if request.risk_state == PublishRiskState.BLOCKED:
            return self._invalid(
                field="risk_state",
                reason_code=PublishReasonCode.RISK_BLOCKED,
                failure_category=PublishFailureCategory.RISK_BLOCKED,
                safe_detail="risk blocked",
            )
        if request.risk_state == PublishRiskState.UNKNOWN:
            return self._invalid(
                field="risk_state",
                reason_code=PublishReasonCode.RISK_UNKNOWN,
                failure_category=PublishFailureCategory.RISK_BLOCKED,
                safe_detail="risk unknown",
            )
        fingerprint = compute_publish_fingerprint(draft, request, context)
        return PublishValidationResult(
            is_valid=True,
            issues=(),
            normalized_fingerprint=fingerprint,
            reason_codes=(),
        )

    def decision_for_invalid_result(
        self,
        request: PublishRequest,
        result: PublishValidationResult,
    ) -> PublishDecision:
        issue = result.issues[0]
        if issue.reason_code in {
            PublishReasonCode.AUTHORIZATION_DENIED,
            PublishReasonCode.AUTHORIZATION_UNKNOWN,
        }:
            decision_type = PublishDecisionType.UNAUTHORIZED
        elif issue.reason_code in {PublishReasonCode.RISK_BLOCKED, PublishReasonCode.RISK_UNKNOWN}:
            decision_type = PublishDecisionType.RISK_BLOCKED
        else:
            decision_type = PublishDecisionType.INVALID_INPUT
        return PublishDecision(
            decision_type=decision_type,
            reason_code=issue.reason_code,
            draft_id=request.draft_id,
            draft_revision=request.draft_revision,
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            normalized_fingerprint=None,
            manual_review_reason=None,
            audit_identifiers=(request.request_id,),
        )

    def _invalid(
        self,
        *,
        field: str,
        reason_code: PublishReasonCode,
        failure_category: PublishFailureCategory,
        safe_detail: str,
    ) -> PublishValidationResult:
        issue = ValidationIssue(
            field=field,
            reason_code=reason_code,
            failure_category=failure_category,
            safe_detail=safe_detail,
        )
        return PublishValidationResult(
            is_valid=False,
            issues=(issue,),
            normalized_fingerprint=None,
            reason_codes=(reason_code,),
        )
