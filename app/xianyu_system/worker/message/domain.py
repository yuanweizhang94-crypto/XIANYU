"""Pure domain model for local synthetic Message receipt."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID


class DeduplicationDecision(StrEnum):
    """Approved deduplication decisions."""

    NEW = "NEW"
    DUPLICATE = "DUPLICATE"
    INDETERMINATE = "INDETERMINATE"
    CONFLICT = "CONFLICT"


class WorkerLifecycleState(StrEnum):
    """Approved local Worker lifecycle states."""

    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class MessageErrorCode(StrEnum):
    """Stable sanitized message-boundary error codes."""

    MESSAGE_ERROR = "MESSAGE_ERROR"
    MESSAGE_VALIDATION_ERROR = "MESSAGE_VALIDATION_ERROR"
    MESSAGE_OWNERSHIP_ERROR = "MESSAGE_OWNERSHIP_ERROR"
    MESSAGE_AUTHORIZATION_ERROR = "MESSAGE_AUTHORIZATION_ERROR"
    MESSAGE_RISK_ERROR = "MESSAGE_RISK_ERROR"
    MESSAGE_PROTOCOL_ERROR = "MESSAGE_PROTOCOL_ERROR"
    MESSAGE_DEDUPLICATION_CONFLICT = "MESSAGE_DEDUPLICATION_CONFLICT"
    MESSAGE_BUSY = "MESSAGE_BUSY"
    MESSAGE_PERSISTENCE_ERROR = "MESSAGE_PERSISTENCE_ERROR"
    MESSAGE_INTERNAL_ERROR = "MESSAGE_INTERNAL_ERROR"


class MessageBoundaryError(Exception):
    """Base sanitized error for the local message boundary."""

    code = MessageErrorCode.MESSAGE_ERROR
    message = "Message boundary operation failed."

    def __init__(self) -> None:
        super().__init__(self.message)


class InvalidMessageInput(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_VALIDATION_ERROR
    message = "Message input is invalid."


class ProfileOwnershipViolation(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_OWNERSHIP_ERROR
    message = "Message ownership is invalid."


class MessageAuthorizationViolation(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_AUTHORIZATION_ERROR
    message = "Message authorization boundary failed."


class MessageRiskViolation(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_RISK_ERROR
    message = "Message risk boundary failed."


class MessageProtocolViolation(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_PROTOCOL_ERROR
    message = "Message protocol boundary failed."


class DeduplicationConflict(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_DEDUPLICATION_CONFLICT
    message = "Message deduplication conflict."


class InvalidWorkerTransition(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_VALIDATION_ERROR
    message = "Worker lifecycle transition is invalid."


class WorkerBusy(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_BUSY
    message = "Message worker is busy."


class WorkerBlocked(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_OWNERSHIP_ERROR
    message = "Message worker is blocked."


class MessagePersistenceError(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_PERSISTENCE_ERROR
    message = "Message persistence operation failed."


class MessageInternalError(MessageBoundaryError):
    code = MessageErrorCode.MESSAGE_INTERNAL_ERROR
    message = "Message internal operation failed."


def normalize_uuid(value: str | UUID) -> str:
    """Normalize a UUID to canonical lowercase text."""
    try:
        return str(value if isinstance(value, UUID) else UUID(str(value))).lower()
    except (TypeError, ValueError, AttributeError):
        raise InvalidMessageInput() from None


def normalize_required_text(value: str, *, max_length: int) -> str:
    """Normalize non-empty text while preserving internal whitespace."""
    if not isinstance(value, str):
        raise InvalidMessageInput()
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidMessageInput()
    return normalized


def normalize_optional_text(value: str | None, *, max_length: int) -> str | None:
    """Normalize optional non-empty text."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidMessageInput()
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidMessageInput()
    return normalized


def normalize_message_content(value: str) -> str:
    """Normalize approved inert Message Content text."""
    if not isinstance(value, str):
        raise InvalidMessageInput()
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    if not 1 <= len(normalized) <= 4096 or normalized.strip() == "":
        raise InvalidMessageInput()
    return normalized


def normalize_timestamp(value: datetime) -> datetime:
    """Normalize an aware timestamp to UTC."""
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise InvalidMessageInput()
    return value.astimezone(UTC)


def _normalize_deduplication_decision(
    value: DeduplicationDecision | str,
) -> DeduplicationDecision:
    try:
        decision = value if isinstance(value, DeduplicationDecision) else DeduplicationDecision(value)
    except ValueError:
        raise InvalidMessageInput() from None
    return decision


def normalize_persisted_message_decision(
    value: DeduplicationDecision | str,
) -> DeduplicationDecision:
    """Normalize a decision approved for persisted Message records."""
    decision = _normalize_deduplication_decision(value)
    if decision not in {
        DeduplicationDecision.NEW,
        DeduplicationDecision.INDETERMINATE,
    }:
        raise InvalidMessageInput()
    return decision


def normalize_attempt_outcome(value: DeduplicationDecision | str) -> DeduplicationDecision:
    """Normalize a decision approved for Delivery Attempt records."""
    decision = _normalize_deduplication_decision(value)
    if decision not in {
        DeduplicationDecision.NEW,
        DeduplicationDecision.DUPLICATE,
        DeduplicationDecision.INDETERMINATE,
    }:
        raise InvalidMessageInput()
    return decision


@dataclass(frozen=True, slots=True)
class Conversation:
    conversation_id: str
    profile_id: str
    account_reference: str
    platform_conversation_identifier: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "conversation_id", normalize_uuid(self.conversation_id))
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(
            self,
            "platform_conversation_identifier",
            normalize_optional_text(
                self.platform_conversation_identifier,
                max_length=512,
            ),
        )
        object.__setattr__(self, "created_at", normalize_timestamp(self.created_at))


@dataclass(frozen=True, slots=True)
class MessageRecord:
    message_id: str
    conversation_id: str
    profile_id: str
    account_reference: str
    platform_message_identifier: str | None
    delivery_identity: str | None
    participant_reference: str
    message_content: str
    received_at: datetime
    platform_timestamp: datetime | None
    deduplication_decision: DeduplicationDecision

    def __post_init__(self) -> None:
        object.__setattr__(self, "message_id", normalize_uuid(self.message_id))
        object.__setattr__(self, "conversation_id", normalize_uuid(self.conversation_id))
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(
            self,
            "platform_message_identifier",
            normalize_optional_text(self.platform_message_identifier, max_length=512),
        )
        object.__setattr__(
            self,
            "delivery_identity",
            normalize_optional_text(self.delivery_identity, max_length=512),
        )
        object.__setattr__(
            self,
            "participant_reference",
            normalize_required_text(self.participant_reference, max_length=512),
        )
        object.__setattr__(
            self,
            "message_content",
            normalize_message_content(self.message_content),
        )
        object.__setattr__(self, "received_at", normalize_timestamp(self.received_at))
        object.__setattr__(
            self,
            "platform_timestamp",
            None
            if self.platform_timestamp is None
            else normalize_timestamp(self.platform_timestamp),
        )
        object.__setattr__(
            self,
            "deduplication_decision",
            normalize_persisted_message_decision(self.deduplication_decision),
        )


@dataclass(frozen=True, slots=True)
class DeliveryAttempt:
    delivery_attempt_id: str
    message_id: str
    profile_id: str
    account_reference: str
    attempted_at: datetime
    outcome_class: DeduplicationDecision
    reason_code: str | None
    attempt_number: int
    correlation_identifier: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "delivery_attempt_id", normalize_uuid(self.delivery_attempt_id))
        object.__setattr__(self, "message_id", normalize_uuid(self.message_id))
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(self, "attempted_at", normalize_timestamp(self.attempted_at))
        object.__setattr__(self, "outcome_class", normalize_attempt_outcome(self.outcome_class))
        object.__setattr__(
            self,
            "reason_code",
            normalize_optional_text(self.reason_code, max_length=64),
        )
        if not isinstance(self.attempt_number, int) or self.attempt_number < 1:
            raise InvalidMessageInput()
        object.__setattr__(
            self,
            "correlation_identifier",
            normalize_optional_text(self.correlation_identifier, max_length=128),
        )


@dataclass(frozen=True, slots=True)
class MessageProcessingResult:
    conversation_id: str
    message_id: str
    delivery_attempt_id: str
    deduplication_decision: DeduplicationDecision
    created_message: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "conversation_id", normalize_uuid(self.conversation_id))
        object.__setattr__(self, "message_id", normalize_uuid(self.message_id))
        object.__setattr__(
            self,
            "delivery_attempt_id",
            normalize_uuid(self.delivery_attempt_id),
        )
        object.__setattr__(
            self,
            "deduplication_decision",
            _normalize_deduplication_decision(self.deduplication_decision),
        )
        if not isinstance(self.created_message, bool):
            raise InvalidMessageInput()
