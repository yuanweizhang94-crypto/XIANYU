"""Non-secret data models for the upstream Pilot wrapper."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class UpstreamResultState(StrEnum):
    SUCCESS = "SUCCESS"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class UpstreamHealth:
    backend_ok: bool
    listener_api_ok: bool
    listener_connected: bool
    detail: str = ""


@dataclass(frozen=True)
class UpstreamAccountStatus:
    account_ref: str
    logged_in: bool
    listener_state: str


@dataclass(frozen=True)
class NormalizedInboundMessage:
    internal_message_id: str
    account_ref: str
    conversation_ref: str
    upstream_message_ref: str
    sender_ref: str
    direction: str
    received_at: str | None
    message_type: str
    text: str
    source: str = "PILOT_READONLY_FALLBACK"


@dataclass(frozen=True)
class ConfirmedReplyRequest:
    internal_message_id: str
    text: str
    confirm: bool


@dataclass(frozen=True)
class UpstreamActionResult:
    state: UpstreamResultState
    operation_id: str
    detail: str = ""
