"""Reply-side read-only mapper from verified local Message values."""

from __future__ import annotations

from typing import Any

from xianyu_system.reply.domain import (
    ReplyAuditIdentifiers,
    ReplyAuthorizationState,
    ReplyBoundaryError,
    ReplyEvaluationContext,
    ReplyMappingError,
    ReplyRiskState,
    ReplySourceMessage,
)


class ReplyMessageMapper:
    """Project approved Message fields without mutating the source object."""

    def map_message(self, message: ReplySourceMessage) -> ReplyEvaluationContext:
        try:
            identifiers = ReplyAuditIdentifiers(
                profile_id=message.profile_id,
                account_reference=message.account_reference,
                conversation_id=message.conversation_id,
                message_id=message.message_id,
            )
            return ReplyEvaluationContext(
                identifiers=identifiers,
                content_text=message.message_content,
                language_hint=_optional_text(message, "language_hint"),
                is_synthetic=bool(getattr(message, "is_synthetic", False)),
                authorization_state=_enum_value(
                    message,
                    "reply_authorization_state",
                    ReplyAuthorizationState.UNKNOWN,
                ),
                risk_state=_enum_value(message, "reply_risk_state", ReplyRiskState.UNKNOWN),
                suppression_asserted=bool(getattr(message, "reply_suppression_asserted", False)),
                sensitive_topic_asserted=bool(
                    getattr(message, "reply_sensitive_topic_asserted", False)
                ),
                human_transfer_requested=bool(
                    getattr(message, "reply_human_transfer_requested", False)
                ),
                correlation_identifier=_optional_text(message, "correlation_identifier"),
            )
        except (AttributeError, TypeError, ValueError, ReplyBoundaryError):
            raise ReplyMappingError() from None


def _optional_text(message: ReplySourceMessage, name: str) -> str | None:
    value = getattr(message, name, None)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ReplyMappingError()
    return value


def _enum_value(message: ReplySourceMessage, name: str, default: Any) -> Any:
    return getattr(message, name, default)
