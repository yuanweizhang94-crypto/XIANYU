"""Application service for local deterministic Publish decisions."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from sqlalchemy.orm import Session

from xianyu_system.worker.publish.domain import (
    ListingDraft,
    PublishAuthorizationState,
    PublishDecision,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishFailureCategory,
    PublishPersistenceError,
    PublishReasonCode,
    PublishRequest,
    PublishRequestLifecycle,
    PublishRiskState,
)
from xianyu_system.worker.publish.persistence import PublishRepository
from xianyu_system.worker.publish.validation import PublishValidator

ZERO_UUID = "00000000-0000-0000-0000-000000000000"


def utc_clock() -> datetime:
    """Return an aware UTC timestamp."""
    return datetime.now(UTC)


class PublishService:
    """Local-only service for deterministic synthetic publish decisions."""

    def __init__(
        self,
        session_factory: Callable[[], Session],
        *,
        identifier_factory: Callable[[], UUID] = uuid.uuid4,
        clock: Callable[[], datetime] = utc_clock,
        validator: PublishValidator | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._identifier_factory = identifier_factory
        self._clock = clock
        self._validator = validator or PublishValidator()

    def evaluate(
        self,
        draft: object,
        request: object,
        context: object,
    ) -> PublishDecision:
        """Evaluate local input without platform access or publish execution."""
        if not isinstance(draft, ListingDraft) or not isinstance(request, PublishRequest):
            return self._shape_invalid()
        if not isinstance(context, PublishEvaluationContext):
            return self._shape_invalid(request=request)

        validation_result = self._validator.validate(draft, request, context)
        if not validation_result.is_valid:
            decision = self._validator.decision_for_invalid_result(request, validation_result)
            failure_category = validation_result.issues[0].failure_category
            return self._record_or_return(
                decision=decision,
                request=request,
                context=context,
                request_lifecycle=self._lifecycle_for(decision.decision_type),
                failure_category=failure_category,
            )

        fingerprint = validation_result.normalized_fingerprint
        assert fingerprint is not None

        session: Session | None = None
        try:
            session = self._session_factory()
            repository = PublishRepository(session)
            by_key = repository.get_by_idempotency_key(request.idempotency_key)
            if by_key is not None:
                session.rollback()
                if by_key.normalized_fingerprint == fingerprint:
                    return self._decision(
                        request=request,
                        decision_type=by_key.decision_type,
                        reason_code=PublishReasonCode.IDEMPOTENCY_REPLAY,
                        normalized_fingerprint=fingerprint,
                    )
                return self._decision(
                    request=request,
                    decision_type=PublishDecisionType.CONFLICT,
                    reason_code=PublishReasonCode.IDEMPOTENCY_CONFLICT,
                    normalized_fingerprint=fingerprint,
                )

            duplicate = repository.get_by_draft_fingerprint(
                draft_id=request.draft_id,
                draft_revision=request.draft_revision,
                normalized_fingerprint=fingerprint,
            )
            if duplicate is not None:
                session.rollback()
                return self._decision(
                    request=request,
                    decision_type=PublishDecisionType.DUPLICATE,
                    reason_code=PublishReasonCode.DUPLICATE_DRAFT,
                    normalized_fingerprint=fingerprint,
                )

            if repository.has_unknown_outcome(
                draft_id=request.draft_id,
                draft_revision=request.draft_revision,
                normalized_fingerprint=fingerprint,
            ):
                decision = self._manual_review(
                    request=request,
                    reason_code=PublishReasonCode.UNKNOWN_PREVIOUS_OUTCOME,
                    normalized_fingerprint=fingerprint,
                    manual_review_reason="unknown historical outcome",
                )
                repository.record_decision(
                    event_id=str(self._identifier_factory()),
                    decision=decision,
                    request_lifecycle=PublishRequestLifecycle.MANUAL_REVIEW,
                    authorization_state=self._authorization_value(request),
                    risk_state=self._risk_value(request),
                    synthetic_fixture=request.synthetic_fixture,
                    correlation_id=request.correlation_id,
                    occurred_at=self._clock(),
                    failure_category=PublishFailureCategory.UNKNOWN_OUTCOME,
                )
                session.commit()
                return decision

            decision = self._decision(
                request=request,
                decision_type=PublishDecisionType.READY,
                reason_code=PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY,
                normalized_fingerprint=fingerprint,
            )
            repository.record_decision(
                event_id=str(self._identifier_factory()),
                decision=decision,
                request_lifecycle=PublishRequestLifecycle.READY,
                authorization_state=self._authorization_value(request),
                risk_state=self._risk_value(request),
                synthetic_fixture=request.synthetic_fixture,
                correlation_id=request.correlation_id,
                occurred_at=self._clock(),
                failure_category=None,
            )
            session.commit()
            return decision
        except PublishPersistenceError:
            if session is not None:
                session.rollback()
            return self._persistence_failure(request=request)
        finally:
            if session is not None:
                session.close()

    def _record_or_return(
        self,
        *,
        decision: PublishDecision,
        request: PublishRequest,
        context: PublishEvaluationContext,
        request_lifecycle: PublishRequestLifecycle,
        failure_category: PublishFailureCategory | None,
    ) -> PublishDecision:
        session: Session | None = None
        try:
            session = self._session_factory()
            PublishRepository(session).record_decision(
                event_id=str(self._identifier_factory()),
                decision=decision,
                request_lifecycle=request_lifecycle,
                authorization_state=cast(PublishAuthorizationState, context.authorization_state).value,
                risk_state=cast(PublishRiskState, context.risk_state).value,
                synthetic_fixture=request.synthetic_fixture and context.synthetic_fixture,
                correlation_id=request.correlation_id,
                occurred_at=self._clock(),
                failure_category=failure_category,
            )
            session.commit()
            return decision
        except PublishPersistenceError:
            if session is not None:
                session.rollback()
            return self._persistence_failure(request=request)
        finally:
            if session is not None:
                session.close()

    def _decision(
        self,
        *,
        request: PublishRequest,
        decision_type: PublishDecisionType,
        reason_code: PublishReasonCode,
        normalized_fingerprint: str | None,
    ) -> PublishDecision:
        return PublishDecision(
            decision_type=decision_type,
            reason_code=reason_code,
            draft_id=request.draft_id,
            draft_revision=request.draft_revision,
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            normalized_fingerprint=normalized_fingerprint,
            manual_review_reason=None,
            audit_identifiers=(request.request_id,),
        )

    def _manual_review(
        self,
        *,
        request: PublishRequest,
        reason_code: PublishReasonCode,
        normalized_fingerprint: str | None,
        manual_review_reason: str,
    ) -> PublishDecision:
        return PublishDecision(
            decision_type=PublishDecisionType.MANUAL_REVIEW,
            reason_code=reason_code,
            draft_id=request.draft_id,
            draft_revision=request.draft_revision,
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            normalized_fingerprint=normalized_fingerprint,
            manual_review_reason=manual_review_reason,
            audit_identifiers=(request.request_id,),
        )

    def _persistence_failure(self, *, request: PublishRequest) -> PublishDecision:
        return self._manual_review(
            request=request,
            reason_code=PublishReasonCode.MANUAL_REVIEW_REQUIRED,
            normalized_fingerprint=None,
            manual_review_reason="persistence failure",
        )

    def _shape_invalid(self, *, request: PublishRequest | None = None) -> PublishDecision:
        return PublishDecision(
            decision_type=PublishDecisionType.INVALID_INPUT,
            reason_code=PublishReasonCode.MISSING_REQUIRED_FIELD,
            draft_id=ZERO_UUID if request is None else request.draft_id,
            draft_revision=1 if request is None else request.draft_revision,
            request_id=ZERO_UUID if request is None else request.request_id,
            idempotency_key="invalid-shape" if request is None else request.idempotency_key,
            normalized_fingerprint=None,
            manual_review_reason=None,
            audit_identifiers=("invalid-shape",),
        )

    def _lifecycle_for(self, decision_type: PublishDecisionType) -> PublishRequestLifecycle:
        if decision_type == PublishDecisionType.INVALID_INPUT:
            return PublishRequestLifecycle.REJECTED
        if decision_type == PublishDecisionType.UNAUTHORIZED:
            return PublishRequestLifecycle.REJECTED
        if decision_type == PublishDecisionType.RISK_BLOCKED:
            return PublishRequestLifecycle.REJECTED
        if decision_type == PublishDecisionType.DUPLICATE:
            return PublishRequestLifecycle.DUPLICATE
        if decision_type == PublishDecisionType.CONFLICT:
            return PublishRequestLifecycle.CONFLICT
        if decision_type == PublishDecisionType.MANUAL_REVIEW:
            return PublishRequestLifecycle.MANUAL_REVIEW
        return PublishRequestLifecycle.READY

    def _authorization_value(self, request: PublishRequest) -> str:
        return cast(PublishAuthorizationState, request.authorization_state).value

    def _risk_value(self, request: PublishRequest) -> str:
        return cast(PublishRiskState, request.risk_state).value
