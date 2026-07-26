"""Transport-neutral synthetic delivery values for local message receipt."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from xianyu_system.worker.message.domain import (
    normalize_message_content,
    normalize_optional_text,
    normalize_required_text,
    normalize_timestamp,
    normalize_uuid,
)


@dataclass(frozen=True, slots=True)
class SyntheticMessageDelivery:
    """Caller-provided synthetic delivery with no real transport behavior."""

    profile_id: str
    account_reference: str
    participant_reference: str
    message_content: str
    received_at: datetime
    platform_conversation_identifier: str | None = None
    platform_message_identifier: str | None = None
    delivery_identity: str | None = None
    platform_timestamp: datetime | None = None
    synthetic_cursor: str | None = None
    correlation_identifier: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_reference",
            normalize_required_text(self.account_reference, max_length=256),
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
            "platform_conversation_identifier",
            normalize_optional_text(
                self.platform_conversation_identifier,
                max_length=512,
            ),
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
            "platform_timestamp",
            None
            if self.platform_timestamp is None
            else normalize_timestamp(self.platform_timestamp),
        )
        object.__setattr__(
            self,
            "synthetic_cursor",
            normalize_optional_text(self.synthetic_cursor, max_length=512),
        )
        object.__setattr__(
            self,
            "correlation_identifier",
            normalize_optional_text(self.correlation_identifier, max_length=128),
        )


class SyntheticDeliverySource(Protocol):
    """Transport-neutral protocol for local synthetic delivery sources."""

    def next_delivery(self) -> SyntheticMessageDelivery | None:
        """Return a caller-owned synthetic delivery when one is available."""
