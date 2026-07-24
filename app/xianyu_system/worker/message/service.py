"""Message use cases and logical transaction coordination."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from xianyu_system.worker.message.domain import (
    Conversation,
    DeduplicationConflict,
    DeduplicationDecision,
    DeliveryAttempt,
    MessageBoundaryError,
    MessagePersistenceError,
    MessageProcessingResult,
    MessageRecord,
)
from xianyu_system.worker.message.persistence import MessageRepository
from xianyu_system.worker.message.transport import SyntheticMessageDelivery


def utc_clock() -> datetime:
    """Return an aware UTC timestamp."""
    return datetime.now(UTC)


class MessageService:
    """Application service for local synthetic Message receipt."""

    def __init__(
        self,
        session_factory: Callable[[], Session],
        *,
        identifier_factory: Callable[[], UUID] = uuid.uuid4,
        clock: Callable[[], datetime] = utc_clock,
    ) -> None:
        self._session_factory = session_factory
        self._identifier_factory = identifier_factory
        self._clock = clock

    def receive(self, delivery: SyntheticMessageDelivery) -> MessageProcessingResult:
        """Receive one synthetic delivery in one logical transaction."""
        session = self._session_factory()
        try:
            repository = MessageRepository(session)
            result = self._receive(repository, delivery)
            session.commit()
            return result
        except (DeduplicationConflict, MessageBoundaryError):
            session.rollback()
            raise
        except IntegrityError:
            session.rollback()
            raise MessagePersistenceError() from None
        except SQLAlchemyError:
            session.rollback()
            raise MessagePersistenceError() from None
        finally:
            session.close()

    def count_conversations(self) -> int:
        with self._session_factory() as session:
            return MessageRepository(session).count_conversations()

    def count_messages(self) -> int:
        with self._session_factory() as session:
            return MessageRepository(session).count_messages()

    def count_delivery_attempts(self) -> int:
        with self._session_factory() as session:
            return MessageRepository(session).count_delivery_attempts()

    def _receive(
        self,
        repository: MessageRepository,
        delivery: SyntheticMessageDelivery,
    ) -> MessageProcessingResult:
        if delivery.delivery_identity is not None:
            existing = repository.get_message_by_delivery_identity(
                profile_id=delivery.profile_id,
                account_reference=delivery.account_reference,
                delivery_identity=delivery.delivery_identity,
            )
            if existing is not None:
                self._ensure_compatible(existing, delivery)
                attempt = self._create_attempt(
                    repository,
                    message_id=existing.message_id,
                    profile_id=existing.profile_id,
                    account_reference=existing.account_reference,
                    decision=DeduplicationDecision.DUPLICATE,
                    correlation_identifier=delivery.correlation_identifier,
                )
                repository.add_delivery_attempt(attempt)
                return MessageProcessingResult(
                    conversation_id=existing.conversation_id,
                    message_id=existing.message_id,
                    delivery_attempt_id=attempt.delivery_attempt_id,
                    deduplication_decision=DeduplicationDecision.DUPLICATE,
                    created_message=False,
                )

        decision = (
            DeduplicationDecision.NEW
            if delivery.delivery_identity is not None
            else DeduplicationDecision.INDETERMINATE
        )
        conversation = self._get_or_create_conversation(repository, delivery)
        message = MessageRecord(
            message_id=str(self._identifier_factory()),
            conversation_id=conversation.conversation_id,
            profile_id=delivery.profile_id,
            account_reference=delivery.account_reference,
            platform_message_identifier=delivery.platform_message_identifier,
            delivery_identity=delivery.delivery_identity,
            participant_reference=delivery.participant_reference,
            message_content=delivery.message_content,
            received_at=delivery.received_at,
            platform_timestamp=delivery.platform_timestamp,
            deduplication_decision=decision,
        )
        repository.add_message(message)
        attempt = self._create_attempt(
            repository,
            message_id=message.message_id,
            profile_id=message.profile_id,
            account_reference=message.account_reference,
            decision=decision,
            correlation_identifier=delivery.correlation_identifier,
        )
        repository.add_delivery_attempt(attempt)
        return MessageProcessingResult(
            conversation_id=conversation.conversation_id,
            message_id=message.message_id,
            delivery_attempt_id=attempt.delivery_attempt_id,
            deduplication_decision=decision,
            created_message=True,
        )

    def _get_or_create_conversation(
        self,
        repository: MessageRepository,
        delivery: SyntheticMessageDelivery,
    ) -> Conversation:
        if delivery.platform_conversation_identifier is not None:
            existing = repository.get_conversation_by_platform_identifier(
                profile_id=delivery.profile_id,
                account_reference=delivery.account_reference,
                platform_conversation_identifier=delivery.platform_conversation_identifier,
            )
            if existing is not None:
                return existing
        conversation = Conversation(
            conversation_id=str(self._identifier_factory()),
            profile_id=delivery.profile_id,
            account_reference=delivery.account_reference,
            platform_conversation_identifier=delivery.platform_conversation_identifier,
            created_at=self._clock(),
        )
        repository.add_conversation(conversation)
        return conversation

    def _create_attempt(
        self,
        repository: MessageRepository,
        *,
        message_id: str,
        profile_id: str,
        account_reference: str,
        decision: DeduplicationDecision,
        correlation_identifier: str | None,
    ) -> DeliveryAttempt:
        return DeliveryAttempt(
            delivery_attempt_id=str(self._identifier_factory()),
            message_id=message_id,
            profile_id=profile_id,
            account_reference=account_reference,
            attempted_at=self._clock(),
            outcome_class=decision,
            reason_code=decision.value,
            attempt_number=repository.next_attempt_number(
                message_id=message_id,
                profile_id=profile_id,
                account_reference=account_reference,
            ),
            correlation_identifier=correlation_identifier,
        )

    def _ensure_compatible(
        self,
        existing: MessageRecord,
        delivery: SyntheticMessageDelivery,
    ) -> None:
        if existing.profile_id != delivery.profile_id:
            raise DeduplicationConflict()
        if existing.account_reference != delivery.account_reference:
            raise DeduplicationConflict()
        if existing.delivery_identity != delivery.delivery_identity:
            raise DeduplicationConflict()
        if existing.platform_message_identifier != delivery.platform_message_identifier:
            raise DeduplicationConflict()
        if existing.participant_reference != delivery.participant_reference:
            raise DeduplicationConflict()
        if existing.message_content != delivery.message_content:
            raise DeduplicationConflict()
        if existing.platform_timestamp != delivery.platform_timestamp:
            raise DeduplicationConflict()
