from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest

from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishReasonCode,
    PublishRequest,
    PublishRiskState,
)
from xianyu_system.worker.publish.service import PublishService
from xianyu_system.worker.publish.validation import PublishValidator

NOW = datetime(2026, 1, 1, tzinfo=UTC)
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"


def draft(**overrides: Any) -> ListingDraft:
    values: dict[str, Any] = {
        "draft_id": DRAFT_ID,
        "revision": 1,
        "title": "synthetic title",
        "description": "synthetic description",
        "category_reference": "synthetic-category",
        "price": Decimal("12.34"),
        "stock": 1,
        "location_reference": "synthetic-location",
        "media_metadata": {"a": "synthetic"},
        "seller_profile_reference": "synthetic-profile",
        "lifecycle_state": ListingDraftLifecycle.VALIDATED,
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(overrides)
    return ListingDraft(**values)


def request(**overrides: Any) -> PublishRequest:
    values: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "draft_id": DRAFT_ID,
        "draft_revision": 1,
        "idempotency_key": "idem-key",
        "requested_at": NOW,
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "correlation_id": "corr-id",
    }
    values.update(overrides)
    return PublishRequest(**values)


def context(**overrides: Any) -> PublishEvaluationContext:
    values: dict[str, Any] = {
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "request_time": NOW,
        "local_profile_reference": "synthetic-profile",
    }
    values.update(overrides)
    return PublishEvaluationContext(**values)


def invalid_decision_for(
    request_overrides: dict[str, Any] | None = None,
    context_overrides: dict[str, Any] | None = None,
    draft_overrides: dict[str, Any] | None = None,
):
    validator = PublishValidator()
    req = request(**(request_overrides or {}))
    result = validator.validate(draft(**(draft_overrides or {})), req, context(**(context_overrides or {})))
    assert result.is_valid is False
    return validator.decision_for_invalid_result(req, result), result


def test_service_rejects_wrong_shapes_before_validation() -> None:
    service = PublishService(lambda: pytest.fail("session should not be requested"))

    assert service.evaluate(object(), request(), context()).decision_type == PublishDecisionType.INVALID_INPUT
    assert service.evaluate(draft(), object(), context()).decision_type == PublishDecisionType.INVALID_INPUT
    assert service.evaluate(draft(), request(), object()).decision_type == PublishDecisionType.INVALID_INPUT


def test_validator_rejects_synthetic_fixture_mismatches_before_later_checks() -> None:
    decision, result = invalid_decision_for({"synthetic_fixture": False})
    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert decision.reason_code == PublishReasonCode.INVALID_FIELD_VALUE
    assert result.normalized_fingerprint is None
    assert result.reason_codes == (PublishReasonCode.INVALID_FIELD_VALUE,)

    decision, _ = invalid_decision_for(context_overrides={"synthetic_fixture": False})
    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert decision.reason_code == PublishReasonCode.INVALID_FIELD_VALUE


def test_validator_rejects_draft_identity_before_authorization_or_risk() -> None:
    decision, result = invalid_decision_for(
        request_overrides={
            "authorization_state": PublishAuthorizationState.DENIED,
            "risk_state": PublishRiskState.BLOCKED,
        },
        context_overrides={
            "authorization_state": PublishAuthorizationState.DENIED,
            "risk_state": PublishRiskState.BLOCKED,
        },
        draft_overrides={"revision": 2},
    )

    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert decision.reason_code == PublishReasonCode.INVALID_FIELD_VALUE
    assert result.issues[0].field == "draft_revision"


def test_validator_rejects_authorization_and_risk_context_mismatch_fail_closed() -> None:
    decision, result = invalid_decision_for(
        {"authorization_state": PublishAuthorizationState.DENIED},
        {"authorization_state": PublishAuthorizationState.AUTHORIZED},
    )
    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert result.issues[0].field == "authorization_state"

    decision, result = invalid_decision_for(
        {"risk_state": PublishRiskState.BLOCKED},
        {"risk_state": PublishRiskState.CLEAR},
    )
    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert result.issues[0].field == "risk_state"


@pytest.mark.parametrize(
    ("authorization", "reason"),
    [
        (PublishAuthorizationState.DENIED, PublishReasonCode.AUTHORIZATION_DENIED),
        (PublishAuthorizationState.UNKNOWN, PublishReasonCode.AUTHORIZATION_UNKNOWN),
    ],
)
def test_validator_maps_authorization_failures_to_unauthorized(
    authorization: PublishAuthorizationState, reason: PublishReasonCode
) -> None:
    decision, result = invalid_decision_for(
        {"authorization_state": authorization}, {"authorization_state": authorization}
    )

    assert decision.decision_type == PublishDecisionType.UNAUTHORIZED
    assert decision.reason_code == reason
    assert result.normalized_fingerprint is None


@pytest.mark.parametrize(
    ("risk", "reason"),
    [
        (PublishRiskState.BLOCKED, PublishReasonCode.RISK_BLOCKED),
        (PublishRiskState.UNKNOWN, PublishReasonCode.RISK_UNKNOWN),
    ],
)
def test_validator_maps_risk_failures_to_risk_blocked(
    risk: PublishRiskState, reason: PublishReasonCode
) -> None:
    decision, result = invalid_decision_for({"risk_state": risk}, {"risk_state": risk})

    assert decision.decision_type == PublishDecisionType.RISK_BLOCKED
    assert decision.reason_code == reason
    assert result.normalized_fingerprint is None


def test_authorization_failure_precedes_risk_failure() -> None:
    decision, result = invalid_decision_for(
        {
            "authorization_state": PublishAuthorizationState.DENIED,
            "risk_state": PublishRiskState.BLOCKED,
        },
        {
            "authorization_state": PublishAuthorizationState.DENIED,
            "risk_state": PublishRiskState.BLOCKED,
        },
    )

    assert decision.decision_type == PublishDecisionType.UNAUTHORIZED
    assert decision.reason_code == PublishReasonCode.AUTHORIZATION_DENIED
    assert result.issues[0].field == "authorization_state"


def test_valid_synthetic_authorized_clear_result_has_fingerprint_but_not_ready_decision() -> None:
    result = PublishValidator().validate(draft(), request(), context())

    assert result.is_valid is True
    assert result.issues == ()
    assert result.normalized_fingerprint is not None
    assert len(result.normalized_fingerprint) == 64
    assert result.reason_codes == ()


def test_validation_safe_detail_is_stable_and_does_not_echo_input_values() -> None:
    _decision, result = invalid_decision_for({"synthetic_fixture": False})

    detail = result.issues[0].safe_detail
    assert detail == "synthetic fixture must be true"
    for raw_value in ["synthetic title", "synthetic description", "idem-key", "corr-id"]:
        assert raw_value not in detail
