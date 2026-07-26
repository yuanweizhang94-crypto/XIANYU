from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID

import pytest

from xianyu_system.worker.message.domain import (
    Conversation,
    DeduplicationConflict,
    DeduplicationDecision,
    DeliveryAttempt,
    InvalidMessageInput,
    InvalidWorkerTransition,
    MessageAuthorizationViolation,
    MessageBoundaryError,
    MessageErrorCode,
    MessageInternalError,
    MessagePersistenceError,
    MessageProcessingResult,
    MessageProtocolViolation,
    MessageRecord,
    MessageRiskViolation,
    ProfileOwnershipViolation,
    WorkerBlocked,
    WorkerBusy,
    WorkerLifecycleState,
    normalize_message_content,
    normalize_optional_text,
    normalize_required_text,
    normalize_timestamp,
    normalize_uuid,
)

PROFILE_ID = "00000000-0000-4000-8000-000000000101"
CONVERSATION_ID = "00000000-0000-4000-8000-000000000102"
MESSAGE_ID = "00000000-0000-4000-8000-000000000103"
ATTEMPT_ID = "00000000-0000-4000-8000-000000000104"
ACCOUNT_REFERENCE = "synthetic-account-reference"
PARTICIPANT_REFERENCE = "synthetic-participant-reference"
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def test_message_enums_expose_exact_approved_values() -> None:
    assert [item.value for item in DeduplicationDecision] == [
        "NEW",
        "DUPLICATE",
        "INDETERMINATE",
        "CONFLICT",
    ]
    assert [item.value for item in WorkerLifecycleState] == [
        "STOPPED",
        "STARTING",
        "RUNNING",
        "STOPPING",
        "BLOCKED",
        "FAILED",
    ]
    assert [item.value for item in MessageErrorCode] == [
        "MESSAGE_ERROR",
        "MESSAGE_VALIDATION_ERROR",
        "MESSAGE_OWNERSHIP_ERROR",
        "MESSAGE_AUTHORIZATION_ERROR",
        "MESSAGE_RISK_ERROR",
        "MESSAGE_PROTOCOL_ERROR",
        "MESSAGE_DEDUPLICATION_CONFLICT",
        "MESSAGE_BUSY",
        "MESSAGE_PERSISTENCE_ERROR",
        "MESSAGE_INTERNAL_ERROR",
    ]


def test_message_errors_have_stable_sanitized_codes_and_text() -> None:
    errors = [
        (MessageBoundaryError(), MessageErrorCode.MESSAGE_ERROR, "Message boundary operation failed."),
        (InvalidMessageInput(), MessageErrorCode.MESSAGE_VALIDATION_ERROR, "Message input is invalid."),
        (ProfileOwnershipViolation(), MessageErrorCode.MESSAGE_OWNERSHIP_ERROR, "Message ownership is invalid."),
        (MessageAuthorizationViolation(), MessageErrorCode.MESSAGE_AUTHORIZATION_ERROR, "Message authorization boundary failed."),
        (MessageRiskViolation(), MessageErrorCode.MESSAGE_RISK_ERROR, "Message risk boundary failed."),
        (MessageProtocolViolation(), MessageErrorCode.MESSAGE_PROTOCOL_ERROR, "Message protocol boundary failed."),
        (DeduplicationConflict(), MessageErrorCode.MESSAGE_DEDUPLICATION_CONFLICT, "Message deduplication conflict."),
        (InvalidWorkerTransition(), MessageErrorCode.MESSAGE_VALIDATION_ERROR, "Worker lifecycle transition is invalid."),
        (WorkerBusy(), MessageErrorCode.MESSAGE_BUSY, "Message worker is busy."),
        (WorkerBlocked(), MessageErrorCode.MESSAGE_OWNERSHIP_ERROR, "Message worker is blocked."),
        (MessagePersistenceError(), MessageErrorCode.MESSAGE_PERSISTENCE_ERROR, "Message persistence operation failed."),
        (MessageInternalError(), MessageErrorCode.MESSAGE_INTERNAL_ERROR, "Message internal operation failed."),
    ]
    forbidden = [
        "Synthetic Message Content",
        "Cookie",
        "Token",
        "Secret",
        "Session",
        "SQL",
        "synthetic-external-identifier",
    ]
    for error, code, text in errors:
        assert error.code is code
        assert str(error) == text
        assert error.__cause__ is None
        for item in forbidden:
            assert item not in repr(error)
            assert item not in str(error)


def test_uuid_normalization_canonicalizes_supported_values() -> None:
    value = UUID("00000000-0000-4000-8000-00000000abcd")
    assert normalize_uuid(value) == "00000000-0000-4000-8000-00000000abcd"
    assert normalize_uuid("00000000-0000-4000-8000-00000000ABCD") == (
        "00000000-0000-4000-8000-00000000abcd"
    )


def test_uuid_normalization_rejects_invalid_values() -> None:
    with pytest.raises(InvalidMessageInput):
        normalize_uuid("not-a-uuid")
    with pytest.raises(InvalidMessageInput):
        normalize_uuid(object())  # type: ignore[arg-type]


def test_required_and_optional_text_normalization_enforces_boundaries() -> None:
    assert normalize_required_text("  synthetic account  ", max_length=32) == "synthetic account"
    assert normalize_optional_text(None, max_length=32) is None
    assert normalize_optional_text("  synthetic optional  ", max_length=32) == "synthetic optional"
    with pytest.raises(InvalidMessageInput):
        normalize_required_text("   ", max_length=32)
    with pytest.raises(InvalidMessageInput):
        normalize_required_text("x" * 33, max_length=32)
    with pytest.raises(InvalidMessageInput):
        normalize_required_text(123, max_length=32)  # type: ignore[arg-type]
    with pytest.raises(InvalidMessageInput):
        normalize_optional_text("   ", max_length=32)


def test_message_content_normalizes_newlines_and_preserves_inert_text() -> None:
    content = "  <b>synthetic</b> ${not_template}\r\nSELECT text\rShell text  "
    assert normalize_message_content(content) == (
        "  <b>synthetic</b> ${not_template}\nSELECT text\nShell text  "
    )


def test_message_content_rejects_blank_non_string_and_over_limit() -> None:
    with pytest.raises(InvalidMessageInput):
        normalize_message_content("   ")
    with pytest.raises(InvalidMessageInput):
        normalize_message_content(123)  # type: ignore[arg-type]
    with pytest.raises(InvalidMessageInput):
        normalize_message_content("x" * 4097)


def test_timestamp_normalization_requires_awareness_and_returns_utc() -> None:
    offset_timestamp = datetime(2026, 1, 1, 20, 0, tzinfo=timezone(timedelta(hours=8)))
    assert normalize_timestamp(offset_timestamp) == datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    with pytest.raises(InvalidMessageInput):
        normalize_timestamp(datetime(2026, 1, 1, 12, 0))
    with pytest.raises(InvalidMessageInput):
        normalize_timestamp("2026-01-01")  # type: ignore[arg-type]


def test_conversation_is_immutable_normalized_and_profile_scoped() -> None:
    conversation = Conversation(
        conversation_id=CONVERSATION_ID.upper(),
        profile_id=PROFILE_ID.upper(),
        account_reference="  synthetic-account-reference  ",
        platform_conversation_identifier="  synthetic-conversation  ",
        created_at=NOW,
    )
    assert conversation.conversation_id == CONVERSATION_ID
    assert conversation.profile_id == PROFILE_ID
    assert conversation.account_reference == ACCOUNT_REFERENCE
    assert conversation.platform_conversation_identifier == "synthetic-conversation"
    with pytest.raises(FrozenInstanceError):
        conversation.account_reference = "mutated"  # type: ignore[misc]
    with pytest.raises(InvalidMessageInput):
        Conversation(CONVERSATION_ID, PROFILE_ID, " ", None, NOW)


def test_message_record_accepts_only_new_or_indeterminate() -> None:
    message = MessageRecord(
        message_id=MESSAGE_ID,
        conversation_id=CONVERSATION_ID,
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        platform_message_identifier="  synthetic-message  ",
        delivery_identity="  synthetic-delivery  ",
        participant_reference="  synthetic-participant-reference  ",
        message_content="synthetic content",
        received_at=NOW,
        platform_timestamp=NOW,
        deduplication_decision="NEW",
    )
    assert message.platform_message_identifier == "synthetic-message"
    assert message.delivery_identity == "synthetic-delivery"
    assert message.participant_reference == PARTICIPANT_REFERENCE
    assert message.deduplication_decision is DeduplicationDecision.NEW
    with pytest.raises(FrozenInstanceError):
        message.message_content = "mutated"  # type: ignore[misc]
    with pytest.raises(InvalidMessageInput):
        MessageRecord(
            MESSAGE_ID,
            CONVERSATION_ID,
            PROFILE_ID,
            ACCOUNT_REFERENCE,
            None,
            None,
            PARTICIPANT_REFERENCE,
            "synthetic content",
            NOW,
            NOW,
            DeduplicationDecision.DUPLICATE,
        )
    with pytest.raises(InvalidMessageInput):
        MessageRecord(
            MESSAGE_ID,
            CONVERSATION_ID,
            PROFILE_ID,
            ACCOUNT_REFERENCE,
            None,
            None,
            PARTICIPANT_REFERENCE,
            "synthetic content",
            NOW,
            NOW,
            DeduplicationDecision.CONFLICT,
        )


def test_delivery_attempt_accepts_only_approved_outcomes_and_positive_attempts() -> None:
    attempt = DeliveryAttempt(
        delivery_attempt_id=ATTEMPT_ID,
        message_id=MESSAGE_ID,
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        attempted_at=NOW,
        outcome_class="DUPLICATE",
        reason_code="  DUPLICATE  ",
        attempt_number=2,
        correlation_identifier="  synthetic-correlation  ",
    )
    assert attempt.outcome_class is DeduplicationDecision.DUPLICATE
    assert attempt.reason_code == "DUPLICATE"
    assert attempt.correlation_identifier == "synthetic-correlation"
    with pytest.raises(FrozenInstanceError):
        attempt.attempt_number = 3  # type: ignore[misc]
    with pytest.raises(InvalidMessageInput):
        DeliveryAttempt(ATTEMPT_ID, MESSAGE_ID, PROFILE_ID, ACCOUNT_REFERENCE, NOW, DeduplicationDecision.CONFLICT, None, 1, None)
    with pytest.raises(InvalidMessageInput):
        DeliveryAttempt(ATTEMPT_ID, MESSAGE_ID, PROFILE_ID, ACCOUNT_REFERENCE, NOW, DeduplicationDecision.NEW, None, 0, None)


def test_processing_result_is_immutable_and_validates_fields() -> None:
    result = MessageProcessingResult(
        conversation_id=CONVERSATION_ID.upper(),
        message_id=MESSAGE_ID.upper(),
        delivery_attempt_id=ATTEMPT_ID.upper(),
        deduplication_decision="CONFLICT",
        created_message=False,
    )
    assert result.conversation_id == CONVERSATION_ID
    assert result.message_id == MESSAGE_ID
    assert result.delivery_attempt_id == ATTEMPT_ID
    assert result.deduplication_decision is DeduplicationDecision.CONFLICT
    assert result.created_message is False
    with pytest.raises(FrozenInstanceError):
        result.created_message = True  # type: ignore[misc]
    with pytest.raises(InvalidMessageInput):
        MessageProcessingResult(CONVERSATION_ID, MESSAGE_ID, ATTEMPT_ID, "UNKNOWN", True)
    with pytest.raises(InvalidMessageInput):
        MessageProcessingResult(CONVERSATION_ID, MESSAGE_ID, ATTEMPT_ID, "NEW", "yes")  # type: ignore[arg-type]
