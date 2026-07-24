"""SQLAlchemy projection and Repository for local synthetic messages."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    String,
    Table,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import Session

from xianyu_system.core.database import Base
from xianyu_system.worker.message.domain import (
    Conversation,
    DeduplicationDecision,
    DeliveryAttempt,
    MessageRecord,
)

conversation_table = Table(
    "xianyu_message_conversations",
    Base.metadata,
    Column("conversation_id", String(36), primary_key=True, nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("platform_conversation_identifier", String(512), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    ForeignKeyConstraint(
        ["profile_id"],
        ["xianyu_account_profiles.profile_id"],
        name="fk_xianyu_message_conversation_profile",
        ondelete="RESTRICT",
    ),
    UniqueConstraint(
        "conversation_id",
        "profile_id",
        "account_reference",
        name="uq_xianyu_message_conversation_owner",
    ),
    UniqueConstraint(
        "profile_id",
        "account_reference",
        "platform_conversation_identifier",
        name="uq_xianyu_message_conversation_platform_profile",
    ),
    CheckConstraint("length(conversation_id) = 36", name="ck_xianyu_message_conversation_id_len"),
    CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_conversation_profile_len"),
    CheckConstraint(
        "account_reference = trim(account_reference) AND "
        "length(account_reference) >= 1 AND length(account_reference) <= 256",
        name="ck_xianyu_message_conversation_account_len",
    ),
    CheckConstraint(
        "platform_conversation_identifier IS NULL OR "
        "(platform_conversation_identifier = trim(platform_conversation_identifier) AND "
        "length(platform_conversation_identifier) >= 1 AND "
        "length(platform_conversation_identifier) <= 512)",
        name="ck_xianyu_message_conversation_platform_len",
    ),
    extend_existing=True,
)

message_table = Table(
    "xianyu_message_records",
    Base.metadata,
    Column("message_id", String(36), primary_key=True, nullable=False),
    Column("conversation_id", String(36), nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("platform_message_identifier", String(512), nullable=True),
    Column("delivery_identity", String(512), nullable=True),
    Column("participant_reference", String(512), nullable=False),
    Column("message_content", String(4096), nullable=False),
    Column("received_at", DateTime(timezone=True), nullable=False),
    Column("platform_timestamp", DateTime(timezone=True), nullable=True),
    Column("deduplication_decision", String(16), nullable=False),
    ForeignKeyConstraint(
        ["conversation_id", "profile_id", "account_reference"],
        [
            "xianyu_message_conversations.conversation_id",
            "xianyu_message_conversations.profile_id",
            "xianyu_message_conversations.account_reference",
        ],
        name="fk_xianyu_message_record_conversation_owner",
        ondelete="RESTRICT",
    ),
    UniqueConstraint(
        "message_id",
        "profile_id",
        "account_reference",
        name="uq_xianyu_message_record_owner",
    ),
    UniqueConstraint(
        "profile_id",
        "account_reference",
        "delivery_identity",
        name="uq_xianyu_message_record_delivery_identity",
    ),
    CheckConstraint("length(message_id) = 36", name="ck_xianyu_message_record_id_len"),
    CheckConstraint("length(conversation_id) = 36", name="ck_xianyu_message_record_conversation_len"),
    CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_record_profile_len"),
    CheckConstraint(
        "account_reference = trim(account_reference) AND "
        "length(account_reference) >= 1 AND length(account_reference) <= 256",
        name="ck_xianyu_message_record_account_len",
    ),
    CheckConstraint(
        "platform_message_identifier IS NULL OR "
        "(platform_message_identifier = trim(platform_message_identifier) AND "
        "length(platform_message_identifier) >= 1 AND "
        "length(platform_message_identifier) <= 512)",
        name="ck_xianyu_message_record_platform_len",
    ),
    CheckConstraint(
        "delivery_identity IS NULL OR "
        "(delivery_identity = trim(delivery_identity) AND "
        "length(delivery_identity) >= 1 AND length(delivery_identity) <= 512)",
        name="ck_xianyu_message_record_delivery_len",
    ),
    CheckConstraint(
        "participant_reference = trim(participant_reference) AND "
        "length(participant_reference) >= 1 AND length(participant_reference) <= 512",
        name="ck_xianyu_message_record_participant_len",
    ),
    CheckConstraint(
        "length(message_content) >= 1 AND length(message_content) <= 4096 AND "
        "length(trim(message_content)) >= 1",
        name="ck_xianyu_message_record_content_len",
    ),
    CheckConstraint(
        "deduplication_decision IN ('NEW', 'INDETERMINATE')",
        name="ck_xianyu_message_record_dedup_decision",
    ),
    extend_existing=True,
)

delivery_attempt_table = Table(
    "xianyu_message_delivery_attempts",
    Base.metadata,
    Column("delivery_attempt_id", String(36), primary_key=True, nullable=False),
    Column("message_id", String(36), nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("attempted_at", DateTime(timezone=True), nullable=False),
    Column("outcome_class", String(16), nullable=False),
    Column("reason_code", String(64), nullable=True),
    Column("attempt_number", Integer, nullable=False),
    Column("correlation_identifier", String(128), nullable=True),
    ForeignKeyConstraint(
        ["message_id", "profile_id", "account_reference"],
        [
            "xianyu_message_records.message_id",
            "xianyu_message_records.profile_id",
            "xianyu_message_records.account_reference",
        ],
        name="fk_xianyu_message_attempt_message_owner",
        ondelete="RESTRICT",
    ),
    UniqueConstraint(
        "message_id",
        "profile_id",
        "account_reference",
        "attempt_number",
        name="uq_xianyu_message_attempt_number",
    ),
    CheckConstraint("length(delivery_attempt_id) = 36", name="ck_xianyu_message_attempt_id_len"),
    CheckConstraint("length(message_id) = 36", name="ck_xianyu_message_attempt_message_len"),
    CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_attempt_profile_len"),
    CheckConstraint(
        "account_reference = trim(account_reference) AND "
        "length(account_reference) >= 1 AND length(account_reference) <= 256",
        name="ck_xianyu_message_attempt_account_len",
    ),
    CheckConstraint(
        "outcome_class IN ('NEW', 'DUPLICATE', 'INDETERMINATE')",
        name="ck_xianyu_message_attempt_outcome",
    ),
    CheckConstraint("attempt_number >= 1", name="ck_xianyu_message_attempt_number_positive"),
    CheckConstraint(
        "reason_code IS NULL OR "
        "(reason_code = trim(reason_code) AND length(reason_code) >= 1 AND length(reason_code) <= 64)",
        name="ck_xianyu_message_attempt_reason_len",
    ),
    CheckConstraint(
        "correlation_identifier IS NULL OR "
        "(correlation_identifier = trim(correlation_identifier) AND "
        "length(correlation_identifier) >= 1 AND length(correlation_identifier) <= 128)",
        name="ck_xianyu_message_attempt_correlation_len",
    ),
    extend_existing=True,
)


class _ConversationRecord:
    conversation_id: str
    profile_id: str
    account_reference: str
    platform_conversation_identifier: str | None
    created_at: datetime


class _MessageRecord:
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
    deduplication_decision: str


class _DeliveryAttemptRecord:
    delivery_attempt_id: str
    message_id: str
    profile_id: str
    account_reference: str
    attempted_at: datetime
    outcome_class: str
    reason_code: str | None
    attempt_number: int
    correlation_identifier: str | None


Base.registry.map_imperatively(_ConversationRecord, conversation_table)
Base.registry.map_imperatively(_MessageRecord, message_table)
Base.registry.map_imperatively(_DeliveryAttemptRecord, delivery_attempt_table)


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _conversation_values(conversation: Conversation) -> dict[str, Any]:
    return {
        "conversation_id": conversation.conversation_id,
        "profile_id": conversation.profile_id,
        "account_reference": conversation.account_reference,
        "platform_conversation_identifier": conversation.platform_conversation_identifier,
        "created_at": conversation.created_at,
    }


def _message_values(message: MessageRecord) -> dict[str, Any]:
    return {
        "message_id": message.message_id,
        "conversation_id": message.conversation_id,
        "profile_id": message.profile_id,
        "account_reference": message.account_reference,
        "platform_message_identifier": message.platform_message_identifier,
        "delivery_identity": message.delivery_identity,
        "participant_reference": message.participant_reference,
        "message_content": message.message_content,
        "received_at": message.received_at,
        "platform_timestamp": message.platform_timestamp,
        "deduplication_decision": message.deduplication_decision.value,
    }


def _attempt_values(attempt: DeliveryAttempt) -> dict[str, Any]:
    return {
        "delivery_attempt_id": attempt.delivery_attempt_id,
        "message_id": attempt.message_id,
        "profile_id": attempt.profile_id,
        "account_reference": attempt.account_reference,
        "attempted_at": attempt.attempted_at,
        "outcome_class": attempt.outcome_class.value,
        "reason_code": attempt.reason_code,
        "attempt_number": attempt.attempt_number,
        "correlation_identifier": attempt.correlation_identifier,
    }


def _record_to_conversation(record: _ConversationRecord) -> Conversation:
    return Conversation(
        conversation_id=record.conversation_id,
        profile_id=record.profile_id,
        account_reference=record.account_reference,
        platform_conversation_identifier=record.platform_conversation_identifier,
        created_at=_aware(record.created_at) or datetime.now(UTC),
    )


def _record_to_message(record: _MessageRecord) -> MessageRecord:
    return MessageRecord(
        message_id=record.message_id,
        conversation_id=record.conversation_id,
        profile_id=record.profile_id,
        account_reference=record.account_reference,
        platform_message_identifier=record.platform_message_identifier,
        delivery_identity=record.delivery_identity,
        participant_reference=record.participant_reference,
        message_content=record.message_content,
        received_at=_aware(record.received_at) or datetime.now(UTC),
        platform_timestamp=_aware(record.platform_timestamp),
        deduplication_decision=DeduplicationDecision(record.deduplication_decision),
    )


class MessageRepository:
    """Concrete Repository participating in caller-owned Sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_conversation_by_platform_identifier(
        self,
        *,
        profile_id: str,
        account_reference: str,
        platform_conversation_identifier: str,
    ) -> Conversation | None:
        record = self._session.scalars(
            select(_ConversationRecord)
            .where(conversation_table.c.profile_id == profile_id)
            .where(conversation_table.c.account_reference == account_reference)
            .where(
                conversation_table.c.platform_conversation_identifier
                == platform_conversation_identifier
            )
        ).one_or_none()
        return None if record is None else _record_to_conversation(record)

    def add_conversation(self, conversation: Conversation) -> None:
        record = _ConversationRecord()
        for key, value in _conversation_values(conversation).items():
            setattr(record, key, value)
        self._session.add(record)
        self._session.flush()

    def get_message_by_delivery_identity(
        self,
        *,
        profile_id: str,
        account_reference: str,
        delivery_identity: str,
    ) -> MessageRecord | None:
        record = self._session.scalars(
            select(_MessageRecord)
            .where(message_table.c.profile_id == profile_id)
            .where(message_table.c.account_reference == account_reference)
            .where(message_table.c.delivery_identity == delivery_identity)
        ).one_or_none()
        return None if record is None else _record_to_message(record)

    def add_message(self, message: MessageRecord) -> None:
        record = _MessageRecord()
        for key, value in _message_values(message).items():
            setattr(record, key, value)
        self._session.add(record)
        self._session.flush()

    def add_delivery_attempt(self, attempt: DeliveryAttempt) -> None:
        record = _DeliveryAttemptRecord()
        for key, value in _attempt_values(attempt).items():
            setattr(record, key, value)
        self._session.add(record)
        self._session.flush()

    def next_attempt_number(
        self,
        *,
        message_id: str,
        profile_id: str,
        account_reference: str,
    ) -> int:
        current = self._session.scalar(
            select(func.max(delivery_attempt_table.c.attempt_number))
            .where(delivery_attempt_table.c.message_id == message_id)
            .where(delivery_attempt_table.c.profile_id == profile_id)
            .where(delivery_attempt_table.c.account_reference == account_reference)
        )
        return int(current or 0) + 1

    def count_conversations(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(conversation_table)) or 0)

    def count_messages(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(message_table)) or 0)

    def count_delivery_attempts(self) -> int:
        return int(
            self._session.scalar(select(func.count()).select_from(delivery_attempt_table))
            or 0
        )
