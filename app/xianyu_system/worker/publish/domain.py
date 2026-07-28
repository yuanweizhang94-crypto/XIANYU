"""Pure domain model for the local deterministic Publish boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from uuid import UUID

type JsonScalar = str | int | Decimal | bool | None
type JsonValue = JsonScalar | tuple["JsonValue", ...] | tuple[tuple[str, "JsonValue"], ...]

MAX_LOCAL_TEXT_LENGTH = 4096
MAX_LOCAL_REFERENCE_LENGTH = 512
MAX_LOCAL_IDEMPOTENCY_KEY_LENGTH = 128
MAX_SAFE_DETAIL_LENGTH = 96


class PublishBoundaryError(Exception):
    """Base error for sanitized local publish-boundary failures."""


class InvalidPublishInput(PublishBoundaryError):
    """Raised when local publish input violates deterministic invariants."""


class PublishPersistenceError(PublishBoundaryError):
    """Raised when local persistence fails with a sanitized message."""


class PublishDecisionType(StrEnum):
    READY = "READY"
    INVALID_INPUT = "INVALID_INPUT"
    UNAUTHORIZED = "UNAUTHORIZED"
    RISK_BLOCKED = "RISK_BLOCKED"
    DUPLICATE = "DUPLICATE"
    CONFLICT = "CONFLICT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class PublishReasonCode(StrEnum):
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_FIELD_VALUE = "INVALID_FIELD_VALUE"
    UNSUPPORTED_CATEGORY = "UNSUPPORTED_CATEGORY"
    INVALID_PRICE = "INVALID_PRICE"
    INVALID_STOCK = "INVALID_STOCK"
    INVALID_LOCATION = "INVALID_LOCATION"
    INVALID_MEDIA_METADATA = "INVALID_MEDIA_METADATA"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    AUTHORIZATION_UNKNOWN = "AUTHORIZATION_UNKNOWN"
    RISK_BLOCKED = "RISK_BLOCKED"
    RISK_UNKNOWN = "RISK_UNKNOWN"
    IDEMPOTENCY_REPLAY = "IDEMPOTENCY_REPLAY"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    DUPLICATE_DRAFT = "DUPLICATE_DRAFT"
    UNKNOWN_PREVIOUS_OUTCOME = "UNKNOWN_PREVIOUS_OUTCOME"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY = "READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY"


class PublishAuthorizationState(StrEnum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    UNKNOWN = "UNKNOWN"


class PublishRiskState(StrEnum):
    CLEAR = "CLEAR"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class ListingDraftLifecycle(StrEnum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    READY_FOR_MANUAL_REVIEW = "READY_FOR_MANUAL_REVIEW"
    ARCHIVED = "ARCHIVED"


class PublishRequestLifecycle(StrEnum):
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    READY = "READY"
    DUPLICATE = "DUPLICATE"
    CONFLICT = "CONFLICT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class PublishAttemptLifecycle(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class PublishOutcomeType(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    CANCELLED = "CANCELLED"


class PublishFailureCategory(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    RISK_BLOCKED = "RISK_BLOCKED"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    DUPLICATE_REQUEST = "DUPLICATE_REQUEST"
    PERSISTENCE_ERROR = "PERSISTENCE_ERROR"
    ADAPTER_ERROR = "ADAPTER_ERROR"
    TIMEOUT = "TIMEOUT"
    UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME"
    CANCELLED = "CANCELLED"


def normalize_uuid(value: str, *, field_name: str) -> str:
    try:
        return str(UUID(str(value))).lower()
    except (TypeError, ValueError):
        raise InvalidPublishInput(f"{field_name} must be a valid UUID string.") from None


def normalize_required_text(value: str, *, field_name: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise InvalidPublishInput(f"{field_name} must be text.")
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidPublishInput(f"{field_name} length is outside the local safe range.")
    return normalized


def normalize_optional_text(
    value: str | None,
    *,
    field_name: str,
    max_length: int,
) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidPublishInput(f"{field_name} must be text when provided.")
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidPublishInput(f"{field_name} length is outside the local safe range.")
    return normalized


def normalize_utc_datetime(value: datetime, *, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise InvalidPublishInput(f"{field_name} must be timezone-aware.")
    return value.astimezone(UTC)


def normalize_positive_int(value: int, *, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise InvalidPublishInput(f"{field_name} must be a positive integer.")
    return value


def normalize_non_negative_int(value: int, *, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise InvalidPublishInput(f"{field_name} must be a non-negative integer.")
    return value


def normalize_price(value: Decimal | str | int) -> Decimal:
    if isinstance(value, bool | float):
        raise InvalidPublishInput("Price must use a precise decimal value.")
    try:
        price = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InvalidPublishInput("Price must use a precise decimal value.") from None
    if not price.is_finite() or price < Decimal("0"):
        raise InvalidPublishInput("Price is outside the local safe range.")
    return price.normalize()


def normalize_enum[T: StrEnum](value: T | str, enum_type: type[T], *, field_name: str) -> T:
    if isinstance(value, enum_type):
        return value
    if isinstance(value, str):
        try:
            return enum_type(value)
        except ValueError:
            pass
    raise InvalidPublishInput(f"{field_name} is not approved.")


def canonical_media_metadata(value: object, *, depth: int = 0) -> JsonValue:
    if depth > 8:
        raise InvalidPublishInput("Media metadata nesting is outside the local safe range.")
    if value is None or isinstance(value, str | bool):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise InvalidPublishInput("Media metadata number is not finite.")
        return value.normalize()
    if isinstance(value, float | bytes | bytearray | memoryview):
        raise InvalidPublishInput("Media metadata contains an unsupported value.")
    if isinstance(value, list | tuple):
        if len(value) > 64:
            raise InvalidPublishInput("Media metadata sequence is outside the local safe range.")
        return tuple(canonical_media_metadata(item, depth=depth + 1) for item in value)
    if isinstance(value, Mapping):
        items: list[tuple[str, JsonValue]] = []
        for raw_key, raw_item in value.items():
            if not isinstance(raw_key, str):
                raise InvalidPublishInput("Media metadata keys must be text.")
            key = normalize_required_text(
                raw_key,
                field_name="Media metadata key",
                max_length=128,
            )
            items.append((key, canonical_media_metadata(raw_item, depth=depth + 1)))
        if len(items) > 64:
            raise InvalidPublishInput("Media metadata object is outside the local safe range.")
        return tuple(sorted(items, key=lambda pair: pair[0]))
    raise InvalidPublishInput("Media metadata contains an unsupported value.")


@dataclass(frozen=True, slots=True)
class ListingDraft:
    draft_id: str
    revision: int
    title: str
    description: str
    category_reference: str
    price: Decimal | str | int
    stock: int
    location_reference: str
    media_metadata: object
    seller_profile_reference: str
    lifecycle_state: ListingDraftLifecycle | str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "draft_id", normalize_uuid(self.draft_id, field_name="Draft ID"))
        object.__setattr__(self, "revision", normalize_positive_int(self.revision, field_name="Revision"))
        object.__setattr__(
            self,
            "title",
            normalize_required_text(self.title, field_name="Title", max_length=256),
        )
        object.__setattr__(
            self,
            "description",
            normalize_required_text(
                self.description,
                field_name="Description",
                max_length=MAX_LOCAL_TEXT_LENGTH,
            ),
        )
        object.__setattr__(
            self,
            "category_reference",
            normalize_required_text(
                self.category_reference,
                field_name="Category reference",
                max_length=MAX_LOCAL_REFERENCE_LENGTH,
            ),
        )
        object.__setattr__(self, "price", normalize_price(self.price))
        object.__setattr__(self, "stock", normalize_non_negative_int(self.stock, field_name="Stock"))
        object.__setattr__(
            self,
            "location_reference",
            normalize_required_text(
                self.location_reference,
                field_name="Location reference",
                max_length=MAX_LOCAL_REFERENCE_LENGTH,
            ),
        )
        object.__setattr__(self, "media_metadata", canonical_media_metadata(self.media_metadata))
        object.__setattr__(
            self,
            "seller_profile_reference",
            normalize_required_text(
                self.seller_profile_reference,
                field_name="Seller profile reference",
                max_length=MAX_LOCAL_REFERENCE_LENGTH,
            ),
        )
        object.__setattr__(
            self,
            "lifecycle_state",
            normalize_enum(
                self.lifecycle_state,
                ListingDraftLifecycle,
                field_name="Listing lifecycle",
            ),
        )
        object.__setattr__(
            self,
            "created_at",
            normalize_utc_datetime(self.created_at, field_name="Created at"),
        )
        object.__setattr__(
            self,
            "updated_at",
            normalize_utc_datetime(self.updated_at, field_name="Updated at"),
        )


@dataclass(frozen=True, slots=True)
class PublishRequest:
    request_id: str
    draft_id: str
    draft_revision: int
    idempotency_key: str
    requested_at: datetime
    authorization_state: PublishAuthorizationState | str
    risk_state: PublishRiskState | str
    synthetic_fixture: bool
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", normalize_uuid(self.request_id, field_name="Request ID"))
        object.__setattr__(self, "draft_id", normalize_uuid(self.draft_id, field_name="Draft ID"))
        object.__setattr__(
            self,
            "draft_revision",
            normalize_positive_int(self.draft_revision, field_name="Draft revision"),
        )
        object.__setattr__(
            self,
            "idempotency_key",
            normalize_required_text(
                self.idempotency_key,
                field_name="Idempotency key",
                max_length=MAX_LOCAL_IDEMPOTENCY_KEY_LENGTH,
            ),
        )
        object.__setattr__(
            self,
            "requested_at",
            normalize_utc_datetime(self.requested_at, field_name="Requested at"),
        )
        object.__setattr__(
            self,
            "authorization_state",
            normalize_enum(
                self.authorization_state,
                PublishAuthorizationState,
                field_name="Authorization state",
            ),
        )
        object.__setattr__(
            self,
            "risk_state",
            normalize_enum(self.risk_state, PublishRiskState, field_name="Risk state"),
        )
        if not isinstance(self.synthetic_fixture, bool):
            raise InvalidPublishInput("Synthetic fixture flag must be boolean.")
        object.__setattr__(
            self,
            "correlation_id",
            normalize_optional_text(
                self.correlation_id,
                field_name="Correlation ID",
                max_length=128,
            ),
        )


@dataclass(frozen=True, slots=True)
class PublishEvaluationContext:
    authorization_state: PublishAuthorizationState | str
    risk_state: PublishRiskState | str
    synthetic_fixture: bool
    request_time: datetime
    local_profile_reference: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "authorization_state",
            normalize_enum(
                self.authorization_state,
                PublishAuthorizationState,
                field_name="Context authorization state",
            ),
        )
        object.__setattr__(
            self,
            "risk_state",
            normalize_enum(self.risk_state, PublishRiskState, field_name="Context risk state"),
        )
        if not isinstance(self.synthetic_fixture, bool):
            raise InvalidPublishInput("Context synthetic fixture flag must be boolean.")
        object.__setattr__(
            self,
            "request_time",
            normalize_utc_datetime(self.request_time, field_name="Context request time"),
        )
        object.__setattr__(
            self,
            "local_profile_reference",
            normalize_required_text(
                self.local_profile_reference,
                field_name="Local profile reference",
                max_length=MAX_LOCAL_REFERENCE_LENGTH,
            ),
        )


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    field: str
    reason_code: PublishReasonCode
    failure_category: PublishFailureCategory
    safe_detail: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "field",
            normalize_required_text(self.field, field_name="Issue field", max_length=64),
        )
        object.__setattr__(
            self,
            "reason_code",
            normalize_enum(self.reason_code, PublishReasonCode, field_name="Issue reason"),
        )
        object.__setattr__(
            self,
            "failure_category",
            normalize_enum(
                self.failure_category,
                PublishFailureCategory,
                field_name="Issue failure category",
            ),
        )
        object.__setattr__(
            self,
            "safe_detail",
            normalize_required_text(
                self.safe_detail,
                field_name="Issue safe detail",
                max_length=MAX_SAFE_DETAIL_LENGTH,
            ),
        )


@dataclass(frozen=True, slots=True)
class PublishValidationResult:
    is_valid: bool
    issues: tuple[ValidationIssue, ...]
    normalized_fingerprint: str | None
    reason_codes: tuple[PublishReasonCode, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.is_valid, bool):
            raise InvalidPublishInput("Validation result flag must be boolean.")
        if not isinstance(self.issues, tuple) or not all(
            isinstance(issue, ValidationIssue) for issue in self.issues
        ):
            raise InvalidPublishInput("Validation issues must be an immutable sequence.")
        object.__setattr__(
            self,
            "reason_codes",
            tuple(
                normalize_enum(code, PublishReasonCode, field_name="Validation reason")
                for code in self.reason_codes
            ),
        )
        if self.is_valid and not self.normalized_fingerprint:
            raise InvalidPublishInput("Valid input requires a fingerprint.")
        if not self.is_valid and self.normalized_fingerprint is not None:
            raise InvalidPublishInput("Invalid input must not carry a fingerprint.")


@dataclass(frozen=True, slots=True)
class PublishDecision:
    decision_type: PublishDecisionType
    reason_code: PublishReasonCode
    draft_id: str
    draft_revision: int
    request_id: str
    idempotency_key: str
    normalized_fingerprint: str | None
    manual_review_reason: str | None
    audit_identifiers: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "decision_type",
            normalize_enum(self.decision_type, PublishDecisionType, field_name="Decision type"),
        )
        object.__setattr__(
            self,
            "reason_code",
            normalize_enum(self.reason_code, PublishReasonCode, field_name="Decision reason"),
        )
        object.__setattr__(self, "draft_id", normalize_uuid(self.draft_id, field_name="Draft ID"))
        object.__setattr__(
            self,
            "draft_revision",
            normalize_positive_int(self.draft_revision, field_name="Draft revision"),
        )
        object.__setattr__(self, "request_id", normalize_uuid(self.request_id, field_name="Request ID"))
        object.__setattr__(
            self,
            "idempotency_key",
            normalize_required_text(
                self.idempotency_key,
                field_name="Idempotency key",
                max_length=MAX_LOCAL_IDEMPOTENCY_KEY_LENGTH,
            ),
        )
        if self.normalized_fingerprint is not None:
            object.__setattr__(
                self,
                "normalized_fingerprint",
                normalize_required_text(
                    self.normalized_fingerprint,
                    field_name="Normalized fingerprint",
                    max_length=64,
                ),
            )
        manual_review_reason = normalize_optional_text(
            self.manual_review_reason,
            field_name="Manual review reason",
            max_length=MAX_SAFE_DETAIL_LENGTH,
        )
        if self.decision_type != PublishDecisionType.MANUAL_REVIEW and manual_review_reason is not None:
            raise InvalidPublishInput("Only manual-review decisions may include manual review text.")
        object.__setattr__(self, "manual_review_reason", manual_review_reason)
        object.__setattr__(
            self,
            "audit_identifiers",
            tuple(
                normalize_required_text(identifier, field_name="Audit identifier", max_length=128)
                for identifier in self.audit_identifiers
            ),
        )


@dataclass(frozen=True, slots=True)
class PublishAttemptSnapshot:
    attempt_id: str
    request_id: str
    attempt_number: int
    attempt_state: PublishAttemptLifecycle | str
    outcome_type: PublishOutcomeType | str
    started_at: datetime
    completed_at: datetime | None = None
    sanitized_error_code: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempt_id", normalize_uuid(self.attempt_id, field_name="Attempt ID"))
        object.__setattr__(self, "request_id", normalize_uuid(self.request_id, field_name="Request ID"))
        object.__setattr__(
            self,
            "attempt_number",
            normalize_positive_int(self.attempt_number, field_name="Attempt number"),
        )
        object.__setattr__(
            self,
            "attempt_state",
            normalize_enum(
                self.attempt_state,
                PublishAttemptLifecycle,
                field_name="Attempt state",
            ),
        )
        object.__setattr__(
            self,
            "outcome_type",
            normalize_enum(self.outcome_type, PublishOutcomeType, field_name="Outcome type"),
        )
        object.__setattr__(
            self,
            "started_at",
            normalize_utc_datetime(self.started_at, field_name="Attempt started at"),
        )
        if self.completed_at is not None:
            object.__setattr__(
                self,
                "completed_at",
                normalize_utc_datetime(self.completed_at, field_name="Attempt completed at"),
            )
        object.__setattr__(
            self,
            "sanitized_error_code",
            normalize_optional_text(
                self.sanitized_error_code,
                field_name="Sanitized error code",
                max_length=64,
            ),
        )
