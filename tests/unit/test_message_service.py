from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from xianyu_system.worker.message.domain import (
    Conversation,
    DeduplicationConflict,
    DeduplicationDecision,
    DeliveryAttempt,
    MessagePersistenceError,
    MessageRecord,
)
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

PROFILE_ID = "00000000-0000-4000-8000-000000000101"
OTHER_PROFILE_ID = "00000000-0000-4000-8000-000000000201"
ACCOUNT_REFERENCE = "synthetic-account-reference"
OTHER_ACCOUNT_REFERENCE = "synthetic-other-account-reference"
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


class FakeSession:
    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.close_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1

    def close(self) -> None:
        self.close_count += 1


class FakeRepository:
    conversations: list[Conversation] = []
    messages: list[MessageRecord] = []
    attempts: list[DeliveryAttempt] = []
    fail_on_add_message: Exception | None = None
    constructed: list[FakeRepository] = []

    def __init__(self, session: FakeSession) -> None:
        self.session = session
        self.commit_called = False
        FakeRepository.constructed.append(self)

    @classmethod
    def reset(cls) -> None:
        cls.conversations = []
        cls.messages = []
        cls.attempts = []
        cls.fail_on_add_message = None
        cls.constructed = []

    def get_conversation_by_platform_identifier(
        self,
        *,
        profile_id: str,
        account_reference: str,
        platform_conversation_identifier: str,
    ) -> Conversation | None:
        for conversation in self.conversations:
            if (
                conversation.profile_id == profile_id
                and conversation.account_reference == account_reference
                and conversation.platform_conversation_identifier
                == platform_conversation_identifier
            ):
                return conversation
        return None

    def get_conversation_by_id(
        self,
        *,
        conversation_id: str,
        profile_id: str,
        account_reference: str,
    ) -> Conversation | None:
        for conversation in self.conversations:
            if (
                conversation.conversation_id == conversation_id
                and conversation.profile_id == profile_id
                and conversation.account_reference == account_reference
            ):
                return conversation
        return None

    def add_conversation(self, conversation: Conversation) -> None:
        self.conversations.append(conversation)

    def get_message_by_delivery_identity(
        self,
        *,
        profile_id: str,
        account_reference: str,
        delivery_identity: str,
    ) -> MessageRecord | None:
        for message in self.messages:
            if (
                message.profile_id == profile_id
                and message.account_reference == account_reference
                and message.delivery_identity == delivery_identity
            ):
                return message
        return None

    def add_message(self, message: MessageRecord) -> None:
        if self.fail_on_add_message is not None:
            raise self.fail_on_add_message
        self.messages.append(message)

    def add_delivery_attempt(self, attempt: DeliveryAttempt) -> None:
        self.attempts.append(attempt)

    def next_attempt_number(
        self,
        *,
        message_id: str,
        profile_id: str,
        account_reference: str,
    ) -> int:
        matching = [
            attempt
            for attempt in self.attempts
            if attempt.message_id == message_id
            and attempt.profile_id == profile_id
            and attempt.account_reference == account_reference
        ]
        return len(matching) + 1

    def count_conversations(self) -> int:
        return len(self.conversations)

    def count_messages(self) -> int:
        return len(self.messages)

    def count_delivery_attempts(self) -> int:
        return len(self.attempts)


def install_fake(monkeypatch: pytest.MonkeyPatch) -> tuple[FakeSession, object]:
    import xianyu_system.worker.message.service as service_module
    from xianyu_system.worker.message.service import MessageService

    FakeRepository.reset()
    session = FakeSession()
    monkeypatch.setattr(service_module, "MessageRepository", FakeRepository)
    ids = iter(
        [
            UUID("00000000-0000-4000-8000-000000000301"),
            UUID("00000000-0000-4000-8000-000000000302"),
            UUID("00000000-0000-4000-8000-000000000303"),
            UUID("00000000-0000-4000-8000-000000000304"),
            UUID("00000000-0000-4000-8000-000000000305"),
            UUID("00000000-0000-4000-8000-000000000306"),
            UUID("00000000-0000-4000-8000-000000000307"),
            UUID("00000000-0000-4000-8000-000000000308"),
            UUID("00000000-0000-4000-8000-000000000309"),
        ]
    )
    service = MessageService(
        lambda: session,
        identifier_factory=lambda: next(ids),
        clock=lambda: NOW,
    )
    return session, service


def delivery(**overrides: object) -> SyntheticMessageDelivery:
    values = {
        "profile_id": PROFILE_ID,
        "account_reference": ACCOUNT_REFERENCE,
        "participant_reference": "synthetic-participant",
        "message_content": "synthetic local content",
        "received_at": NOW,
        "platform_conversation_identifier": "synthetic-conversation",
        "platform_message_identifier": "synthetic-message",
        "delivery_identity": "synthetic-delivery",
        "platform_timestamp": NOW,
        "correlation_identifier": "synthetic-correlation",
    }
    values.update(overrides)
    return SyntheticMessageDelivery(**values)  # type: ignore[arg-type]


def test_receive_new_uses_uuid4_and_creates_one_conversation_message_and_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    result = service.receive(delivery())
    assert result.deduplication_decision is DeduplicationDecision.NEW
    assert result.created_message is True
    assert UUID(result.conversation_id).version == 4
    assert UUID(result.message_id).version == 4
    assert UUID(result.delivery_attempt_id).version == 4
    assert len(FakeRepository.conversations) == 1
    assert len(FakeRepository.messages) == 1
    assert len(FakeRepository.attempts) == 1
    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert session.close_count == 1


def test_receive_duplicate_reuses_message_and_increments_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    first = service.receive(delivery())
    second = service.receive(
        delivery(
            received_at=datetime(2026, 1, 1, 12, 1, tzinfo=UTC),
            correlation_identifier="synthetic-second-correlation",
        )
    )
    assert second.deduplication_decision is DeduplicationDecision.DUPLICATE
    assert second.created_message is False
    assert second.conversation_id == first.conversation_id
    assert second.message_id == first.message_id
    assert len(FakeRepository.conversations) == 1
    assert len(FakeRepository.messages) == 1
    assert len(FakeRepository.attempts) == 2
    assert FakeRepository.attempts[1].attempt_number == 2
    assert session.commit_count == 2
    assert session.rollback_count == 0
    assert session.close_count == 2


def test_receive_indeterminate_creates_separate_messages_without_content_collapse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    first = service.receive(delivery(delivery_identity=None))
    second = service.receive(
        delivery(
            delivery_identity=None,
            received_at=datetime(2026, 1, 1, 12, 0, 1, tzinfo=UTC),
        )
    )
    assert first.deduplication_decision is DeduplicationDecision.INDETERMINATE
    assert second.deduplication_decision is DeduplicationDecision.INDETERMINATE
    assert first.message_id != second.message_id
    assert len(FakeRepository.messages) == 2
    assert len(FakeRepository.attempts) == 2
    assert session.commit_count == 2


def test_receive_content_conflict_rolls_back_without_overwrite(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    service.receive(delivery())
    before = (
        len(FakeRepository.conversations),
        len(FakeRepository.messages),
        len(FakeRepository.attempts),
        FakeRepository.messages[0].message_content,
    )
    with pytest.raises(DeduplicationConflict):
        service.receive(delivery(message_content="synthetic changed content"))
    assert (
        len(FakeRepository.conversations),
        len(FakeRepository.messages),
        len(FakeRepository.attempts),
        FakeRepository.messages[0].message_content,
    ) == before
    assert session.rollback_count == 1
    assert session.commit_count == 1
    assert session.close_count == 2


def test_receive_conversation_conflict_rolls_back_without_new_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    service.receive(delivery())
    before = (
        len(FakeRepository.conversations),
        len(FakeRepository.messages),
        len(FakeRepository.attempts),
    )
    with pytest.raises(DeduplicationConflict):
        service.receive(delivery(platform_conversation_identifier="synthetic-other-conversation"))
    assert (
        len(FakeRepository.conversations),
        len(FakeRepository.messages),
        len(FakeRepository.attempts),
    ) == before
    assert session.rollback_count == 1
    assert session.commit_count == 1


def test_platform_message_identifier_alone_is_not_a_deduplication_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    first = service.receive(
        delivery(
            delivery_identity=None,
            platform_message_identifier="synthetic-shared-platform-message",
        )
    )
    second = service.receive(
        delivery(
            delivery_identity=None,
            platform_message_identifier="synthetic-shared-platform-message",
        )
    )
    assert first.message_id != second.message_id
    assert len(FakeRepository.messages) == 2
    assert len(FakeRepository.attempts) == 2
    assert session.commit_count == 2


def test_delivery_identity_lookup_is_profile_and_account_scoped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    first = service.receive(delivery())
    other_profile = service.receive(delivery(profile_id=OTHER_PROFILE_ID))
    other_account = service.receive(delivery(account_reference=OTHER_ACCOUNT_REFERENCE))
    assert first.message_id != other_profile.message_id
    assert first.message_id != other_account.message_id
    assert len(FakeRepository.messages) == 3
    assert len(FakeRepository.conversations) == 3
    assert session.commit_count == 3


def test_persistence_failures_are_sanitized_rolled_back_and_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    FakeRepository.fail_on_add_message = IntegrityError(
        "SELECT synthetic local content",
        {},
        Exception("token table"),
    )
    with pytest.raises(MessagePersistenceError) as integrity_error:
        service.receive(delivery())
    assert integrity_error.value.__cause__ is None
    assert "SELECT" not in str(integrity_error.value)
    assert "synthetic local content" not in str(integrity_error.value)
    assert session.commit_count == 0
    assert session.rollback_count == 1
    assert session.close_count == 1
    FakeRepository.reset()
    session.rollback_count = 0
    session.close_count = 0
    FakeRepository.fail_on_add_message = SQLAlchemyError(
        "SELECT synthetic local content FROM token table"
    )
    with pytest.raises(MessagePersistenceError) as sqlalchemy_error:
        service.receive(delivery())
    assert sqlalchemy_error.value.__cause__ is None
    assert "SELECT" not in str(sqlalchemy_error.value)
    assert "synthetic local content" not in str(sqlalchemy_error.value)
    assert session.commit_count == 0
    assert session.rollback_count == 1
    assert session.close_count == 1


def test_service_owns_commit_and_repository_never_commits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, service = install_fake(monkeypatch)
    service.receive(delivery())
    repository = FakeRepository.constructed[0]
    assert not hasattr(repository, "commit")
    assert repository.commit_called is False
    assert session.commit_count == 1
    assert session.rollback_count == 0
    with pytest.raises(DeduplicationConflict):
        service.receive(delivery(message_content="synthetic changed content"))
    assert session.commit_count == 1
    assert session.rollback_count == 1
    assert session.close_count == 2
