"""Pure domain model for the local deterministic Reply boundary."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SUPPORTED_CONDITION_FIELDS = frozenset({"content_text", "language_hint"})
_ALLOWED_TRANSITIONS = frozenset(
    {
        ("DRAFT", "ENABLED"),
        ("ENABLED", "DISABLED"),
        ("DISABLED", "ENABLED"),
        ("DRAFT", "ARCHIVED"),
        ("DISABLED", "ARCHIVED"),
    }
)


class ReplyDecisionType(StrEnum):
    REPLY = "REPLY"
    NO_MATCH = "NO_MATCH"
    CONFLICT = "CONFLICT"
    ESCALATE = "ESCALATE"
    SUPPRESSED = "SUPPRESSED"
    INVALID_INPUT = "INVALID_INPUT"


class ReplyReasonCode(StrEnum):
    READY_TO_REPLY = "READY_TO_REPLY"
    NO_RULE_MATCHED = "NO_RULE_MATCHED"
    DUPLICATE_HIGHEST_PRIORITY_MATCH = "DUPLICATE_HIGHEST_PRIORITY_MATCH"
    AUTHORIZATION_UNKNOWN = "AUTHORIZATION_UNKNOWN"
    RISK_UNKNOWN = "RISK_UNKNOWN"
    SAFETY_SUPPRESSED = "SAFETY_SUPPRESSED"
    SENSITIVE_TOPIC = "SENSITIVE_TOPIC"
    HUMAN_TRANSFER_REQUIRED = "HUMAN_TRANSFER_REQUIRED"
    UNSUPPORTED_LANGUAGE = "UNSUPPORTED_LANGUAGE"
    MISSING_REQUIRED_INPUT = "MISSING_REQUIRED_INPUT"
    UNSUPPORTED_FIELD = "UNSUPPORTED_FIELD"
    UNSUPPORTED_OPERATOR = "UNSUPPORTED_OPERATOR"
    EMPTY_CONDITION_SET = "EMPTY_CONDITION_SET"
    INVALID_PRIORITY = "INVALID_PRIORITY"
    MISSING_TEMPLATE = "MISSING_TEMPLATE"
    MISSING_TEMPLATE_VARIABLE = "MISSING_TEMPLATE_VARIABLE"
    FORBIDDEN_PLACEHOLDER = "FORBIDDEN_PLACEHOLDER"
    PERSISTENCE_FAILURE = "PERSISTENCE_FAILURE"


class ReplyLifecycleState(StrEnum):
    DRAFT = "DRAFT"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"


class ReplyAuthorizationState(StrEnum):
    EXPLICITLY_AUTHORIZED = "EXPLICITLY_AUTHORIZED"
    UNKNOWN = "UNKNOWN"
    EXPIRED = "EXPIRED"
    DENIED = "DENIED"
    REVOKED = "REVOKED"
    VERIFICATION_REQUIRED = "VERIFICATION_REQUIRED"


class ReplyRiskState(StrEnum):
    LOW = "LOW"
    ALLOWED = "ALLOWED"
    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    PENDING_REVIEW = "PENDING_REVIEW"
    THROTTLED = "THROTTLED"
    BLOCKED = "BLOCKED"


class ConditionOperator(StrEnum):
    EQUALS = "equals"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


class NormalizationFlag(StrEnum):
    TRIM = "TRIM"
    NFKC = "NFKC"


class ReplyErrorCode(StrEnum):
    REPLY_ERROR = "REPLY_ERROR"
    REPLY_VALIDATION_ERROR = "REPLY_VALIDATION_ERROR"
    REPLY_MAPPING_ERROR = "REPLY_MAPPING_ERROR"
    REPLY_RENDER_ERROR = "REPLY_RENDER_ERROR"
    REPLY_PERSISTENCE_ERROR = "REPLY_PERSISTENCE_ERROR"


class ReplyBoundaryError(Exception):
    code = ReplyErrorCode.REPLY_ERROR
    reason_code: ReplyReasonCode | None = None
    message = "Reply boundary operation failed."

    def __init__(self, *, reason_code: ReplyReasonCode | None = None) -> None:
        self.reason_code = reason_code or self.reason_code
        super().__init__(self.message)


class InvalidReplyInput(ReplyBoundaryError):
    code = ReplyErrorCode.REPLY_VALIDATION_ERROR
    message = "Reply input is invalid."


class ReplyMappingError(ReplyBoundaryError):
    code = ReplyErrorCode.REPLY_MAPPING_ERROR
    reason_code = ReplyReasonCode.MISSING_REQUIRED_INPUT
    message = "Reply source projection is invalid."


class ReplyRenderError(ReplyBoundaryError):
    code = ReplyErrorCode.REPLY_RENDER_ERROR
    message = "Reply template rendering failed."


class ReplyPersistenceError(ReplyBoundaryError):
    code = ReplyErrorCode.REPLY_PERSISTENCE_ERROR
    reason_code = ReplyReasonCode.PERSISTENCE_FAILURE
    message = "Reply persistence operation failed."


def _invalid(reason: ReplyReasonCode = ReplyReasonCode.MISSING_REQUIRED_INPUT) -> InvalidReplyInput:
    return InvalidReplyInput(reason_code=reason)


def normalize_uuid(value: str | UUID) -> str:
    try:
        return str(value if isinstance(value, UUID) else UUID(str(value))).lower()
    except (TypeError, ValueError, AttributeError):
        raise _invalid() from None


def normalize_required_text(value: str, *, max_length: int) -> str:
    if not isinstance(value, str):
        raise _invalid()
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise _invalid()
    return normalized


def normalize_optional_text(value: str | None, *, max_length: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise _invalid()
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise _invalid()
    return normalized


def normalize_timestamp(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise _invalid()
    return value.astimezone(UTC)


def normalize_positive_version(value: int) -> int:
    if not isinstance(value, int) or value < 1:
        raise _invalid()
    return value


def normalize_row_version(value: int) -> int:
    return normalize_positive_version(value)


def normalize_priority(value: int) -> int:
    if not isinstance(value, int) or value < 0:
        raise _invalid(ReplyReasonCode.INVALID_PRIORITY)
    return value


def normalize_lifecycle(value: ReplyLifecycleState | str) -> ReplyLifecycleState:
    try:
        return value if isinstance(value, ReplyLifecycleState) else ReplyLifecycleState(str(value))
    except ValueError:
        raise _invalid() from None


def normalize_decision_type(value: ReplyDecisionType | str) -> ReplyDecisionType:
    try:
        return value if isinstance(value, ReplyDecisionType) else ReplyDecisionType(str(value))
    except ValueError:
        raise _invalid() from None


def normalize_reason_code(value: ReplyReasonCode | str) -> ReplyReasonCode:
    try:
        return value if isinstance(value, ReplyReasonCode) else ReplyReasonCode(str(value))
    except ValueError:
        raise _invalid() from None


def normalize_normalization_flags(
    values: tuple[NormalizationFlag | str, ...],
) -> tuple[NormalizationFlag, ...]:
    flags: list[NormalizationFlag] = []
    for value in values:
        try:
            flag = value if isinstance(value, NormalizationFlag) else NormalizationFlag(str(value))
        except ValueError:
            raise _invalid() from None
        if flag not in flags:
            flags.append(flag)
    return tuple(sorted(flags, key=lambda item: item.value))


def canonical_normalization_flags(values: tuple[NormalizationFlag | str, ...]) -> str:
    return ",".join(flag.value for flag in normalize_normalization_flags(values))


def flags_from_canonical(value: str) -> tuple[NormalizationFlag, ...]:
    if value == "":
        return ()
    return normalize_normalization_flags(tuple(value.split(",")))


def normalize_text_for_condition(
    value: str,
    *,
    flags: tuple[NormalizationFlag | str, ...],
    case_sensitive: bool,
) -> str:
    if not isinstance(value, str):
        raise _invalid()
    result = value
    normalized_flags = normalize_normalization_flags(flags)
    if NormalizationFlag.TRIM in normalized_flags:
        result = result.strip()
    if NormalizationFlag.NFKC in normalized_flags:
        result = unicodedata.normalize("NFKC", result)
    if not case_sensitive:
        result = result.casefold()
    return result


def validate_lifecycle_transition(
    current: ReplyLifecycleState | str,
    target: ReplyLifecycleState | str,
) -> ReplyLifecycleState:
    current_state = normalize_lifecycle(current)
    target_state = normalize_lifecycle(target)
    if current_state == ReplyLifecycleState.ARCHIVED:
        raise _invalid()
    if (current_state.value, target_state.value) not in _ALLOWED_TRANSITIONS:
        raise _invalid()
    return target_state


def condition_field_supported(field_name: str) -> bool:
    return field_name in SUPPORTED_CONDITION_FIELDS


@dataclass(frozen=True, slots=True)
class ReplyPriority:
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", normalize_priority(self.value))


@dataclass(frozen=True, slots=True)
class TemplateVariableName:
    value: str

    def __post_init__(self) -> None:
        value = normalize_required_text(self.value, max_length=64)
        if not _IDENTIFIER_RE.fullmatch(value):
            raise _invalid(ReplyReasonCode.FORBIDDEN_PLACEHOLDER)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True)
class ReplyRenderedText:
    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise _invalid()
        normalized = self.text.replace("\r\n", "\n").replace("\r", "\n")
        if not 1 <= len(normalized) <= 2048 or normalized.strip() == "":
            raise _invalid()
        object.__setattr__(self, "text", normalized)


@dataclass(frozen=True, slots=True)
class ReplyAuditIdentifiers:
    profile_id: str
    account_reference: str
    conversation_id: str
    message_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(self, "conversation_id", normalize_uuid(self.conversation_id))
        object.__setattr__(self, "message_id", normalize_uuid(self.message_id))


@dataclass(frozen=True, slots=True)
class ReplyCondition:
    rule_id: str
    rule_version: int
    field_name: str
    operator: str
    expected_value: str
    normalization_flags: tuple[NormalizationFlag, ...]
    case_sensitive: bool = False
    sequence: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", normalize_uuid(self.rule_id))
        object.__setattr__(self, "rule_version", normalize_positive_version(self.rule_version))
        object.__setattr__(
            self, "field_name", normalize_required_text(self.field_name, max_length=64)
        )
        object.__setattr__(self, "operator", normalize_required_text(self.operator, max_length=32))
        object.__setattr__(
            self, "expected_value", normalize_required_text(self.expected_value, max_length=512)
        )
        object.__setattr__(
            self, "normalization_flags", normalize_normalization_flags(self.normalization_flags)
        )
        if (
            not isinstance(self.case_sensitive, bool)
            or not isinstance(self.sequence, int)
            or self.sequence < 1
        ):
            raise _invalid()

    @property
    def canonical_normalization(self) -> str:
        return canonical_normalization_flags(self.normalization_flags)


@dataclass(frozen=True, slots=True)
class ReplyTemplate:
    template_id: str
    version: int
    profile_id: str
    account_reference: str
    lifecycle_state: ReplyLifecycleState
    script_text: str
    variable_allowlist: tuple[TemplateVariableName, ...]
    row_version: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "template_id", normalize_uuid(self.template_id))
        object.__setattr__(self, "version", normalize_positive_version(self.version))
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(self, "lifecycle_state", normalize_lifecycle(self.lifecycle_state))
        object.__setattr__(
            self, "script_text", normalize_required_text(self.script_text, max_length=2048)
        )
        object.__setattr__(
            self,
            "variable_allowlist",
            tuple(
                v if isinstance(v, TemplateVariableName) else TemplateVariableName(str(v))
                for v in self.variable_allowlist
            ),
        )
        object.__setattr__(self, "row_version", normalize_row_version(self.row_version))
        object.__setattr__(self, "created_at", normalize_timestamp(self.created_at))
        object.__setattr__(self, "updated_at", normalize_timestamp(self.updated_at))

    @property
    def is_enabled(self) -> bool:
        return self.lifecycle_state == ReplyLifecycleState.ENABLED


@dataclass(frozen=True, slots=True)
class ReplyRule:
    rule_id: str
    version: int
    profile_id: str
    account_reference: str
    lifecycle_state: ReplyLifecycleState
    template_id: str
    template_version: int
    priority: ReplyPriority
    row_version: int
    created_at: datetime
    updated_at: datetime
    name: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", normalize_uuid(self.rule_id))
        object.__setattr__(self, "version", normalize_positive_version(self.version))
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
        )
        object.__setattr__(self, "lifecycle_state", normalize_lifecycle(self.lifecycle_state))
        object.__setattr__(self, "template_id", normalize_uuid(self.template_id))
        object.__setattr__(
            self, "template_version", normalize_positive_version(self.template_version)
        )
        object.__setattr__(
            self,
            "priority",
            self.priority
            if isinstance(self.priority, ReplyPriority)
            else ReplyPriority(int(self.priority)),
        )
        object.__setattr__(self, "row_version", normalize_row_version(self.row_version))
        object.__setattr__(self, "created_at", normalize_timestamp(self.created_at))
        object.__setattr__(self, "updated_at", normalize_timestamp(self.updated_at))
        object.__setattr__(self, "name", normalize_optional_text(self.name, max_length=128))

    @property
    def is_enabled(self) -> bool:
        return self.lifecycle_state == ReplyLifecycleState.ENABLED


@dataclass(frozen=True, slots=True)
class ReplyEvaluationContext:
    identifiers: ReplyAuditIdentifiers
    content_text: str
    language_hint: str | None
    is_synthetic: bool
    authorization_state: ReplyAuthorizationState
    risk_state: ReplyRiskState
    suppression_asserted: bool = False
    sensitive_topic_asserted: bool = False
    human_transfer_requested: bool = False
    correlation_identifier: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.identifiers, ReplyAuditIdentifiers):
            raise _invalid()
        object.__setattr__(
            self, "content_text", normalize_required_text(self.content_text, max_length=4096)
        )
        object.__setattr__(
            self, "language_hint", normalize_optional_text(self.language_hint, max_length=32)
        )
        if not isinstance(self.is_synthetic, bool):
            raise _invalid()
        try:
            authorization = (
                self.authorization_state
                if isinstance(self.authorization_state, ReplyAuthorizationState)
                else ReplyAuthorizationState(str(self.authorization_state))
            )
            risk = (
                self.risk_state
                if isinstance(self.risk_state, ReplyRiskState)
                else ReplyRiskState(str(self.risk_state))
            )
        except ValueError:
            raise _invalid() from None
        object.__setattr__(self, "authorization_state", authorization)
        object.__setattr__(self, "risk_state", risk)
        for name in [
            "suppression_asserted",
            "sensitive_topic_asserted",
            "human_transfer_requested",
        ]:
            if not isinstance(getattr(self, name), bool):
                raise _invalid()
        object.__setattr__(
            self,
            "correlation_identifier",
            normalize_optional_text(self.correlation_identifier, max_length=128),
        )


@dataclass(frozen=True, slots=True)
class ReplyRuleSnapshot:
    rule_id: str
    rule_version: int
    template_id: str
    template_version: int
    lifecycle_state: ReplyLifecycleState
    priority: int
    conditions: tuple[ReplyCondition, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", normalize_uuid(self.rule_id))
        object.__setattr__(self, "rule_version", normalize_positive_version(self.rule_version))
        object.__setattr__(self, "template_id", normalize_uuid(self.template_id))
        object.__setattr__(
            self, "template_version", normalize_positive_version(self.template_version)
        )
        object.__setattr__(self, "lifecycle_state", normalize_lifecycle(self.lifecycle_state))
        if not isinstance(self.priority, int):
            raise _invalid(ReplyReasonCode.INVALID_PRIORITY)
        object.__setattr__(self, "conditions", tuple(self.conditions))


@dataclass(frozen=True, slots=True)
class ReplyEvaluationResult:
    decision_type: ReplyDecisionType
    reason_code: ReplyReasonCode
    rule_id: str | None = None
    rule_version: int | None = None
    template_id: str | None = None
    template_version: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_type", normalize_decision_type(self.decision_type))
        object.__setattr__(self, "reason_code", normalize_reason_code(self.reason_code))
        _normalize_optional_pair(self, "rule_id", "rule_version")
        _normalize_optional_pair(self, "template_id", "template_version")


@dataclass(frozen=True, slots=True)
class ReplyDecision:
    decision_type: ReplyDecisionType
    reason_code: ReplyReasonCode
    identifiers: ReplyAuditIdentifiers | None = None
    rule_id: str | None = None
    rule_version: int | None = None
    template_id: str | None = None
    template_version: int | None = None
    rendered_text: ReplyRenderedText | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_type", normalize_decision_type(self.decision_type))
        object.__setattr__(self, "reason_code", normalize_reason_code(self.reason_code))
        if self.identifiers is not None and not isinstance(self.identifiers, ReplyAuditIdentifiers):
            raise _invalid()
        _normalize_optional_pair(self, "rule_id", "rule_version")
        _normalize_optional_pair(self, "template_id", "template_version")
        if self.rendered_text is not None and not isinstance(self.rendered_text, ReplyRenderedText):
            raise _invalid()


@dataclass(frozen=True, slots=True)
class ReplyAuditEvent:
    audit_event_id: str
    identifiers: ReplyAuditIdentifiers
    decision_type: ReplyDecisionType
    reason_code: ReplyReasonCode
    occurred_at: datetime
    rule_id: str | None = None
    rule_version: int | None = None
    template_id: str | None = None
    template_version: int | None = None
    failure_category: str | None = None
    correlation_identifier: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "audit_event_id", normalize_uuid(self.audit_event_id))
        if not isinstance(self.identifiers, ReplyAuditIdentifiers):
            raise _invalid()
        object.__setattr__(self, "decision_type", normalize_decision_type(self.decision_type))
        object.__setattr__(self, "reason_code", normalize_reason_code(self.reason_code))
        object.__setattr__(self, "occurred_at", normalize_timestamp(self.occurred_at))
        _normalize_optional_pair(self, "rule_id", "rule_version")
        _normalize_optional_pair(self, "template_id", "template_version")
        object.__setattr__(
            self, "failure_category", normalize_optional_text(self.failure_category, max_length=64)
        )
        object.__setattr__(
            self,
            "correlation_identifier",
            normalize_optional_text(self.correlation_identifier, max_length=128),
        )


@dataclass(frozen=True, slots=True)
class ReplyTemplateRenderInput:
    template: ReplyTemplate
    variables: dict[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.template, ReplyTemplate):
            raise _invalid(ReplyReasonCode.MISSING_TEMPLATE)
        normalized: dict[str, str] = {}
        for key, value in self.variables.items():
            name = TemplateVariableName(str(key)).value
            if not isinstance(value, str):
                raise _invalid(ReplyReasonCode.MISSING_TEMPLATE_VARIABLE)
            normalized[name] = value
        object.__setattr__(self, "variables", normalized)


def _normalize_optional_pair(obj: object, id_name: str, version_name: str) -> None:
    raw_id = getattr(obj, id_name)
    raw_version = getattr(obj, version_name)
    if (raw_id is None) != (raw_version is None):
        raise _invalid()
    if raw_id is not None:
        object.__setattr__(obj, id_name, normalize_uuid(raw_id))
        object.__setattr__(obj, version_name, normalize_positive_version(raw_version or 0))


class ReplyRuleRepository(Protocol):
    def list_enabled_snapshots(
        self, *, profile_id: str, account_reference: str
    ) -> tuple[ReplyRuleSnapshot, ...]: ...


class ReplyTemplateRepository(Protocol):
    def get_template(
        self, *, template_id: str, template_version: int, profile_id: str, account_reference: str
    ) -> ReplyTemplate | None: ...


class ReplyAuditRepository(Protocol):
    def add_audit_event(self, event: ReplyAuditEvent) -> None: ...


class ReplyEvaluator(Protocol):
    def evaluate(
        self, context: ReplyEvaluationContext, snapshots: tuple[ReplyRuleSnapshot, ...]
    ) -> ReplyEvaluationResult: ...


class ReplyTemplateRenderer(Protocol):
    def render(self, render_input: ReplyTemplateRenderInput) -> ReplyRenderedText: ...


class ReplySourceMessage(Protocol):
    profile_id: str
    account_reference: str
    conversation_id: str
    message_id: str
    message_content: str


class ReplyContextMapper(Protocol):
    def map_message(self, message: ReplySourceMessage) -> ReplyEvaluationContext: ...


class ReplyDecisionService(Protocol):
    def decide(self, message: ReplySourceMessage) -> ReplyDecision: ...
