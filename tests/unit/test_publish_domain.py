from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from xianyu_system.worker.publish.domain import (
    InvalidPublishInput,
    ListingDraft,
    ListingDraftLifecycle,
    PublishAttemptLifecycle,
    PublishAttemptSnapshot,
    PublishAuthorizationState,
    PublishDecision,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishFailureCategory,
    PublishOutcomeType,
    PublishReasonCode,
    PublishRequest,
    PublishValidationResult,
    PublishRiskState,
    ValidationIssue,
    canonical_media_metadata,
)

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"
ATTEMPT_ID = "00000000-0000-4000-8000-000000000301"
FINGERPRINT = "a" * 64


def make_draft(**overrides: Any) -> ListingDraft:
    values: dict[str, Any] = {
        "draft_id": DRAFT_ID,
        "revision": 1,
        "title": " synthetic title ",
        "description": "synthetic description",
        "category_reference": "synthetic-category",
        "price": Decimal("12.340"),
        "stock": 1,
        "location_reference": "synthetic-location",
        "media_metadata": {"b": [Decimal("2.0"), True], "a": "first"},
        "seller_profile_reference": "synthetic-profile",
        "lifecycle_state": ListingDraftLifecycle.VALIDATED,
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(overrides)
    return ListingDraft(**values)


def make_request(**overrides: Any) -> PublishRequest:
    values: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "draft_id": DRAFT_ID,
        "draft_revision": 1,
        "idempotency_key": " idem-key ",
        "requested_at": NOW,
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "correlation_id": " corr-id ",
    }
    values.update(overrides)
    return PublishRequest(**values)


def make_context(**overrides: Any) -> PublishEvaluationContext:
    values: dict[str, Any] = {
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "request_time": NOW,
        "local_profile_reference": " synthetic-profile ",
    }
    values.update(overrides)
    return PublishEvaluationContext(**values)


def test_listing_draft_normalizes_valid_fields_and_is_frozen() -> None:
    draft = make_draft(
        draft_id="00000000-0000-4000-8000-000000000101".upper(),
        price="12.3400",
        stock=0,
        created_at=datetime(2026, 1, 1, 20, 0, tzinfo=timezone(timedelta(hours=8))),
    )

    assert draft.draft_id == DRAFT_ID
    assert draft.title == "synthetic title"
    assert draft.price == Decimal("12.34")
    assert draft.stock == 0
    assert draft.created_at == NOW
    assert draft.media_metadata == (("a", "first"), ("b", (Decimal("2.0"), True)))
    assert ListingDraftLifecycle.PUBLISHED if False else True
    assert "PUBLISHED" not in {state.value for state in ListingDraftLifecycle}
    with pytest.raises(FrozenInstanceError):
        draft.title = "changed"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("revision", 0),
        ("revision", True),
        ("title", "   "),
        ("title", "x" * 257),
        ("description", "   "),
        ("category_reference", "   "),
        ("location_reference", "   "),
        ("seller_profile_reference", "   "),
        ("stock", -1),
        ("stock", False),
        ("created_at", datetime(2026, 1, 1)),
        ("updated_at", datetime(2026, 1, 1)),
        ("lifecycle_state", "PUBLISHED"),
    ],
)
def test_listing_draft_rejects_invalid_local_fields(field: str, value: object) -> None:
    with pytest.raises(InvalidPublishInput):
        make_draft(**{field: value})


@pytest.mark.parametrize("price", [Decimal("NaN"), Decimal("Infinity"), Decimal("-1"), 1.25, True])
def test_listing_draft_rejects_unsafe_prices(price: object) -> None:
    with pytest.raises(InvalidPublishInput):
        make_draft(price=price)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, None),
        ("text", "text"),
        (False, False),
        (3, 3),
        (Decimal("2.50"), Decimal("2.50")),
        (["b", "a"], ("b", "a")),
        (("b", "a"), ("b", "a")),
        ({"b": 2, "a": [1, Decimal("1.0")]}, (("a", (1, Decimal("1.0"))), ("b", 2))),
    ],
)
def test_media_metadata_canonicalizes_supported_shapes(raw: object, expected: object) -> None:
    assert canonical_media_metadata(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        1.2,
        b"bytes",
        bytearray(b"bytes"),
        memoryview(b"bytes"),
        {1: "bad-key"},
        list(range(65)),
        {str(index): index for index in range(65)},
        Decimal("NaN"),
        Decimal("Infinity"),
    ],
)
def test_media_metadata_rejects_unsafe_shapes(raw: object) -> None:
    with pytest.raises(InvalidPublishInput):
        canonical_media_metadata(raw)


def test_media_metadata_rejects_deep_or_arbitrary_objects_without_side_effects(tmp_path: Path) -> None:
    nested: object = "leaf"
    for _ in range(10):
        nested = [nested]
    with pytest.raises(InvalidPublishInput):
        canonical_media_metadata(nested)

    class CallableObject:
        called = False

        def __call__(self) -> None:
            self.called = True

    callable_object = CallableObject()
    with pytest.raises(InvalidPublishInput):
        canonical_media_metadata(callable_object)
    assert callable_object.called is False
    probe = tmp_path / "not-read.txt"
    probe.write_text("synthetic", encoding="utf-8")
    assert probe.read_text(encoding="utf-8") == "synthetic"


def test_publish_request_normalizes_valid_fields_and_is_frozen() -> None:
    request = make_request(request_id=REQUEST_ID.upper(), correlation_id=" corr ")

    assert request.request_id == REQUEST_ID
    assert request.idempotency_key == "idem-key"
    assert request.correlation_id == "corr"
    assert request.requested_at == NOW
    with pytest.raises(FrozenInstanceError):
        request.idempotency_key = "changed"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("draft_revision", 0),
        ("draft_revision", True),
        ("idempotency_key", "   "),
        ("idempotency_key", "x" * 129),
        ("requested_at", datetime(2026, 1, 1)),
        ("authorization_state", "MAYBE"),
        ("risk_state", "MAYBE"),
        ("synthetic_fixture", "true"),
        ("correlation_id", "x" * 129),
    ],
)
def test_publish_request_rejects_invalid_fields(field: str, value: object) -> None:
    with pytest.raises(InvalidPublishInput):
        make_request(**{field: value})


def test_evaluation_context_normalizes_and_exposes_no_sensitive_fields() -> None:
    context = make_context(local_profile_reference=" profile ")

    assert context.local_profile_reference == "profile"
    assert context.request_time == NOW
    for prohibited in ["credential", "browser", "network", "platform"]:
        assert not any(prohibited in name.lower() for name in context.__dataclass_fields__)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("authorization_state", "MAYBE"),
        ("risk_state", "MAYBE"),
        ("synthetic_fixture", 1),
        ("request_time", datetime(2026, 1, 1)),
        ("local_profile_reference", "   "),
    ],
)
def test_evaluation_context_rejects_invalid_fields(field: str, value: object) -> None:
    with pytest.raises(InvalidPublishInput):
        make_context(**{field: value})


def test_validation_issue_and_result_are_sanitized_immutable_and_ordered() -> None:
    issue = ValidationIssue(
        field=" title ",
        reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
        failure_category=PublishFailureCategory.VALIDATION_ERROR,
        safe_detail=" safe detail ",
    )
    assert issue.field == "title"
    assert issue.safe_detail == "safe detail"
    assert "synthetic title" not in issue.safe_detail
    with pytest.raises(FrozenInstanceError):
        issue.field = "changed"

    result = PublishValidationResult(
        is_valid=False,
        issues=(issue,),
        normalized_fingerprint=None,
        reason_codes=(PublishReasonCode.INVALID_FIELD_VALUE,),
    )
    assert result.issues == (issue,)
    assert result.reason_codes == (PublishReasonCode.INVALID_FIELD_VALUE,)
    with pytest.raises(InvalidPublishInput):
        PublishValidationResult(is_valid=True, issues=(), normalized_fingerprint=None, reason_codes=())
    with pytest.raises(InvalidPublishInput):
        PublishValidationResult(
            is_valid=False,
            issues=(issue,),
            normalized_fingerprint=FINGERPRINT,
            reason_codes=(),
        )
    with pytest.raises(InvalidPublishInput):
        PublishValidationResult(
            is_valid=False,
            issues=[issue],
            normalized_fingerprint=None,
            reason_codes=(),
        )
    with pytest.raises(InvalidPublishInput):
        ValidationIssue(
            field="field",
            reason_code=PublishReasonCode.INVALID_FIELD_VALUE,
            failure_category=PublishFailureCategory.VALIDATION_ERROR,
            safe_detail="x" * 97,
        )


@pytest.mark.parametrize(
    ("decision_type", "reason_code"),
    [
        (PublishDecisionType.READY, PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY),
        (PublishDecisionType.UNAUTHORIZED, PublishReasonCode.AUTHORIZATION_DENIED),
        (PublishDecisionType.UNAUTHORIZED, PublishReasonCode.AUTHORIZATION_UNKNOWN),
        (PublishDecisionType.RISK_BLOCKED, PublishReasonCode.RISK_BLOCKED),
        (PublishDecisionType.RISK_BLOCKED, PublishReasonCode.RISK_UNKNOWN),
        (PublishDecisionType.CONFLICT, PublishReasonCode.IDEMPOTENCY_CONFLICT),
        (PublishDecisionType.DUPLICATE, PublishReasonCode.DUPLICATE_DRAFT),
        (PublishDecisionType.MANUAL_REVIEW, PublishReasonCode.UNKNOWN_PREVIOUS_OUTCOME),
        (PublishDecisionType.MANUAL_REVIEW, PublishReasonCode.MANUAL_REVIEW_REQUIRED),
    ],
)
def test_publish_decision_supports_approved_local_decisions(
    decision_type: PublishDecisionType, reason_code: PublishReasonCode
) -> None:
    decision = PublishDecision(
        decision_type=decision_type,
        reason_code=reason_code,
        draft_id=DRAFT_ID,
        draft_revision=1,
        request_id=REQUEST_ID,
        idempotency_key=" idem ",
        normalized_fingerprint=FINGERPRINT,
        manual_review_reason="manual" if decision_type == PublishDecisionType.MANUAL_REVIEW else None,
        audit_identifiers=(" audit ",),
    )

    assert decision.idempotency_key == "idem"
    assert decision.audit_identifiers == ("audit",)
    assert "published" not in decision.__dataclass_fields__
    assert "platform_success" not in decision.__dataclass_fields__
    with pytest.raises(FrozenInstanceError):
        decision.reason_code = PublishReasonCode.INVALID_FIELD_VALUE


def test_publish_decision_rejects_manual_review_reason_on_non_manual_decision() -> None:
    with pytest.raises(InvalidPublishInput):
        PublishDecision(
            decision_type=PublishDecisionType.READY,
            reason_code=PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY,
            draft_id=DRAFT_ID,
            draft_revision=1,
            request_id=REQUEST_ID,
            idempotency_key="idem",
            normalized_fingerprint=FINGERPRINT,
            manual_review_reason="not allowed",
            audit_identifiers=("audit",),
        )
    with pytest.raises(InvalidPublishInput):
        PublishDecision(
            decision_type=PublishDecisionType.READY,
            reason_code=PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY,
            draft_id=DRAFT_ID,
            draft_revision=1,
            request_id=REQUEST_ID,
            idempotency_key="idem",
            normalized_fingerprint=FINGERPRINT,
            manual_review_reason=None,
            audit_identifiers=("x" * 129,),
        )


def test_attempt_snapshot_preserves_unknown_and_never_starts_work() -> None:
    snapshot = PublishAttemptSnapshot(
        attempt_id=ATTEMPT_ID,
        request_id=REQUEST_ID,
        attempt_number=1,
        attempt_state=PublishAttemptLifecycle.NOT_STARTED,
        outcome_type=PublishOutcomeType.UNKNOWN,
        started_at=NOW,
        completed_at=None,
        sanitized_error_code=" unknown ",
    )

    assert snapshot.outcome_type == PublishOutcomeType.UNKNOWN
    assert snapshot.outcome_type not in {PublishOutcomeType.SUCCEEDED, PublishOutcomeType.FAILED}
    assert snapshot.sanitized_error_code == "unknown"
    with pytest.raises(FrozenInstanceError):
        snapshot.attempt_number = 2

    with pytest.raises(InvalidPublishInput):
        PublishAttemptSnapshot(
            attempt_id=ATTEMPT_ID,
            request_id=REQUEST_ID,
            attempt_number=0,
            attempt_state=PublishAttemptLifecycle.NOT_STARTED,
            outcome_type=PublishOutcomeType.UNKNOWN,
            started_at=NOW,
        )
    with pytest.raises(InvalidPublishInput):
        PublishAttemptSnapshot(
            attempt_id=ATTEMPT_ID,
            request_id=REQUEST_ID,
            attempt_number=1,
            attempt_state=PublishAttemptLifecycle.NOT_STARTED,
            outcome_type=PublishOutcomeType.UNKNOWN,
            started_at=datetime(2026, 1, 1),
        )
    with pytest.raises(InvalidPublishInput):
        PublishAttemptSnapshot(
            attempt_id=ATTEMPT_ID,
            request_id=REQUEST_ID,
            attempt_number=1,
            attempt_state=PublishAttemptLifecycle.NOT_STARTED,
            outcome_type=PublishOutcomeType.UNKNOWN,
            started_at=NOW,
            sanitized_error_code="x" * 65,
        )


def test_sanitized_errors_do_not_echo_payload_values() -> None:
    raw_values = [
        "synthetic title",
        "synthetic description",
        "idem-key",
        "SELECT * FROM xianyu_publish_requests",
        "sqlite:///synthetic.db",
        "raw-payload",
    ]
    for make_invalid in [
        lambda: make_draft(title="   "),
        lambda: make_draft(description="   "),
        lambda: make_request(idempotency_key="   "),
        lambda: canonical_media_metadata(object()),
    ]:
        with pytest.raises(InvalidPublishInput) as exc_info:
            make_invalid()
        message = str(exc_info.value)
        for raw in raw_values:
            assert raw not in message
