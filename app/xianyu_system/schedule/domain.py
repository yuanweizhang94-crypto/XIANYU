"""Pure domain model for one-time local deterministic Schedule decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

MAX_IDEMPOTENCY_KEY_LENGTH = 128
MAX_REFERENCE_LENGTH = 128
MAX_REASON_LENGTH = 256
MIN_GRACE_SECONDS = 0
MAX_GRACE_SECONDS = 3600


class ScheduleBoundaryError(Exception):
    """Base error for sanitized local schedule-boundary failures."""


class InvalidScheduleInput(ScheduleBoundaryError):
    """Raised when local schedule input violates deterministic invariants."""


class SchedulePersistenceError(ScheduleBoundaryError):
    """Raised when local schedule persistence fails with a sanitized message."""


class ScheduleTriggerType(StrEnum):
    IMMEDIATE = "IMMEDIATE"
    RUN_AT_UTC = "RUN_AT_UTC"


class ScheduleLifecycle(StrEnum):
    PENDING = "PENDING"
    CLAIMED = "CLAIMED"
    DISPATCHED = "DISPATCHED"
    CANCELLED = "CANCELLED"
    MISFIRED = "MISFIRED"
    FAILED = "FAILED"
    NEEDS_MANUAL_REVIEW = "NEEDS_MANUAL_REVIEW"


class ScheduleDecisionType(StrEnum):
    ACCEPTED = "ACCEPTED"
    INVALID_INPUT = "INVALID_INPUT"
    DUPLICATE = "DUPLICATE"
    CONFLICT = "CONFLICT"
    CANCELLED = "CANCELLED"
    MISFIRED = "MISFIRED"
    DISPATCHED = "DISPATCHED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class ScheduleDispatchOutcome(StrEnum):
    NOT_DUE = "NOT_DUE"
    CLAIMED = "CLAIMED"
    DISPATCHED = "DISPATCHED"
    MISFIRED = "MISFIRED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NOT_FOUND = "NOT_FOUND"


class ScheduleCancellationReason(StrEnum):
    USER_REQUESTED = "USER_REQUESTED"
    REPLACED_BY_NEWER_REQUEST = "REPLACED_BY_NEWER_REQUEST"
    LOCAL_VALIDATION_FAILED = "LOCAL_VALIDATION_FAILED"


def normalize_uuid(value: str, *, field_name: str) -> str:
    try:
        return str(UUID(str(value))).lower()
    except (TypeError, ValueError):
        raise InvalidScheduleInput(f"{field_name} must be a valid UUID string.") from None


def normalize_text(value: str, *, field_name: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise InvalidScheduleInput(f"{field_name} must be text.")
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidScheduleInput(f"{field_name} length is outside the local safe range.")
    return normalized


def normalize_optional_text(value: str | None, *, field_name: str, max_length: int) -> str | None:
    if value is None:
        return None
    return normalize_text(value, field_name=field_name, max_length=max_length)


def normalize_utc_datetime(value: datetime, *, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise InvalidScheduleInput(f"{field_name} must be timezone-aware.")
    normalized = value.astimezone(UTC)
    if normalized.tzinfo is not UTC:
        normalized = normalized.replace(tzinfo=UTC)
    return normalized


def normalize_grace_seconds(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidScheduleInput("Grace seconds must be an integer.")
    if not MIN_GRACE_SECONDS <= value <= MAX_GRACE_SECONDS:
        raise InvalidScheduleInput("Grace seconds are outside the approved local range.")
    return value


def normalize_enum[T: StrEnum](value: T | str, enum_type: type[T], *, field_name: str) -> T:
    if isinstance(value, enum_type):
        return value
    if isinstance(value, str):
        try:
            return enum_type(value)
        except ValueError:
            pass
    raise InvalidScheduleInput(f"{field_name} is not approved.")


@dataclass(frozen=True, slots=True)
class ScheduleRequest:
    schedule_id: str
    publish_request_id: str
    idempotency_key: str
    trigger_type: ScheduleTriggerType | str
    requested_at: datetime
    run_at: datetime | None
    misfire_grace_seconds: int
    synthetic_fixture: bool
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "schedule_id", normalize_uuid(self.schedule_id, field_name="Schedule ID"))
        object.__setattr__(
            self,
            "publish_request_id",
            normalize_uuid(self.publish_request_id, field_name="Publish request ID"),
        )
        object.__setattr__(
            self,
            "idempotency_key",
            normalize_text(
                self.idempotency_key,
                field_name="Schedule idempotency key",
                max_length=MAX_IDEMPOTENCY_KEY_LENGTH,
            ),
        )
        trigger = normalize_enum(self.trigger_type, ScheduleTriggerType, field_name="Schedule trigger")
        object.__setattr__(self, "trigger_type", trigger)
        object.__setattr__(
            self,
            "requested_at",
            normalize_utc_datetime(self.requested_at, field_name="Requested at"),
        )
        normalized_run_at = None if self.run_at is None else normalize_utc_datetime(self.run_at, field_name="Run at")
        if trigger == ScheduleTriggerType.RUN_AT_UTC and normalized_run_at is None:
            raise InvalidScheduleInput("RUN_AT_UTC schedules require run_at.")
        if trigger == ScheduleTriggerType.IMMEDIATE and normalized_run_at is not None:
            raise InvalidScheduleInput("IMMEDIATE schedules must not include run_at.")
        object.__setattr__(self, "run_at", normalized_run_at)
        object.__setattr__(self, "misfire_grace_seconds", normalize_grace_seconds(self.misfire_grace_seconds))
        if not isinstance(self.synthetic_fixture, bool):
            raise InvalidScheduleInput("Synthetic fixture flag must be boolean.")
        object.__setattr__(
            self,
            "correlation_id",
            normalize_optional_text(
                self.correlation_id,
                field_name="Correlation ID",
                max_length=MAX_REFERENCE_LENGTH,
            ),
        )

    @property
    def due_at(self) -> datetime:
        return self.requested_at if self.trigger_type == ScheduleTriggerType.IMMEDIATE else self.run_at  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class ScheduleValidationIssue:
    field: str
    message: str


@dataclass(frozen=True, slots=True)
class ScheduleDecision:
    schedule_id: str
    publish_request_id: str
    idempotency_key: str
    decision_type: ScheduleDecisionType
    lifecycle: ScheduleLifecycle
    due_at: datetime | None
    normalized_fingerprint: str | None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class ScheduleDispatchResult:
    schedule_id: str
    outcome: ScheduleDispatchOutcome
    lifecycle: ScheduleLifecycle | None
    publish_decision_type: str | None = None
    reason: str | None = None
