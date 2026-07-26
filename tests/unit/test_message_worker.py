from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import UUID

import pytest

from xianyu_system.worker.message.domain import (
    DeduplicationConflict,
    InvalidMessageInput,
    InvalidWorkerTransition,
    MessageAuthorizationViolation,
    MessageBoundaryError,
    MessageInternalError,
    MessagePersistenceError,
    MessageProcessingResult,
    MessageProtocolViolation,
    MessageRiskViolation,
    ProfileOwnershipViolation,
    WorkerBlocked,
    WorkerBusy,
    WorkerLifecycleState,
)
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

PROFILE_ID = "00000000-0000-4000-8000-000000000101"
OTHER_PROFILE_ID = "00000000-0000-4000-8000-000000000201"
ACCOUNT_REFERENCE = "synthetic-account-reference"
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


class FakeService:
    def __init__(
        self,
        result: MessageProcessingResult | None = None,
        failure: Exception | None = None,
    ) -> None:
        self.result = result or processing_result()
        self.failure = failure
        self.calls = 0

    def receive(self, _delivery: SyntheticMessageDelivery) -> MessageProcessingResult:
        self.calls += 1
        if self.failure is not None:
            raise self.failure
        return self.result


def processing_result() -> MessageProcessingResult:
    return MessageProcessingResult(
        conversation_id="00000000-0000-4000-8000-000000000301",
        message_id="00000000-0000-4000-8000-000000000302",
        delivery_attempt_id="00000000-0000-4000-8000-000000000303",
        deduplication_decision="NEW",
        created_message=True,
    )


def delivery(**overrides: object) -> SyntheticMessageDelivery:
    values = {
        "profile_id": PROFILE_ID,
        "account_reference": ACCOUNT_REFERENCE,
        "participant_reference": "synthetic-participant",
        "message_content": "synthetic worker content",
        "received_at": NOW,
    }
    values.update(overrides)
    return SyntheticMessageDelivery(**values)  # type: ignore[arg-type]


def message_worker_class():
    from xianyu_system.worker.message.worker import MessageWorker

    return MessageWorker


def wait_for_state(
    worker: object,
    expected: WorkerLifecycleState,
    timeout: float = 2.0,
) -> None:
    deadline = datetime.now(UTC).timestamp() + timeout
    while datetime.now(UTC).timestamp() < deadline:
        if worker.state is expected:
            return
        threading.Event().wait(0.01)
    raise AssertionError(f"worker did not reach {expected}")


def test_worker_start_stop_and_profile_account_scope_are_explicit() -> None:
    service = FakeService()
    MessageWorker = message_worker_class()
    worker = MessageWorker(
        profile_id=PROFILE_ID.upper(),
        account_reference="  synthetic-account-reference  ",
        service=service,  # type: ignore[arg-type]
    )
    assert worker.profile_id == PROFILE_ID
    assert worker.account_reference == ACCOUNT_REFERENCE
    assert worker.state is WorkerLifecycleState.STOPPED
    worker.start()
    assert worker.state is WorkerLifecycleState.RUNNING
    with pytest.raises(InvalidWorkerTransition):
        worker.start()
    result = worker.receive(delivery())
    assert result is service.result
    assert service.calls == 1
    worker.stop()
    assert worker.state is WorkerLifecycleState.STOPPED
    worker.stop()
    assert worker.state is WorkerLifecycleState.STOPPED


def test_worker_rejects_receive_when_stopped_blocked_or_failed() -> None:
    MessageWorker = message_worker_class()
    stopped = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(),  # type: ignore[arg-type]
    )
    with pytest.raises(InvalidWorkerTransition):
        stopped.receive(delivery())
    blocked = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=DeduplicationConflict()),  # type: ignore[arg-type]
    )
    blocked.start()
    with pytest.raises(DeduplicationConflict):
        blocked.receive(delivery())
    with pytest.raises(WorkerBlocked):
        blocked.receive(delivery())
    failed = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=MessagePersistenceError()),  # type: ignore[arg-type]
    )
    failed.start()
    with pytest.raises(MessagePersistenceError):
        failed.receive(delivery())
    with pytest.raises(InvalidWorkerTransition):
        failed.receive(delivery())


def test_worker_blocks_profile_and_account_mismatches_before_service_call() -> None:
    service = FakeService()
    MessageWorker = message_worker_class()
    worker = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=service,  # type: ignore[arg-type]
    )
    worker.start()
    with pytest.raises(ProfileOwnershipViolation):
        worker.receive(delivery(profile_id=OTHER_PROFILE_ID))
    assert worker.state is WorkerLifecycleState.BLOCKED
    assert service.calls == 0
    with pytest.raises(InvalidWorkerTransition):
        worker.stop()
    worker.reset()
    worker.start()
    with pytest.raises(ProfileOwnershipViolation):
        worker.receive(delivery(account_reference="synthetic-other-account-reference"))
    assert service.calls == 0


def test_worker_failure_mapping_sets_blocked_failed_or_running() -> None:
    MessageWorker = message_worker_class()
    blocking_failures = [
        ProfileOwnershipViolation(),
        MessageAuthorizationViolation(),
        MessageRiskViolation(),
        MessageProtocolViolation(),
        DeduplicationConflict(),
    ]
    for failure in blocking_failures:
        worker = MessageWorker(
            profile_id=PROFILE_ID,
            account_reference=ACCOUNT_REFERENCE,
            service=FakeService(failure=failure),  # type: ignore[arg-type]
        )
        worker.start()
        with pytest.raises(type(failure)):
            worker.receive(delivery())
        assert worker.state is WorkerLifecycleState.BLOCKED
    failed_failures = [MessagePersistenceError(), MessageInternalError()]
    for failure in failed_failures:
        worker = MessageWorker(
            profile_id=PROFILE_ID,
            account_reference=ACCOUNT_REFERENCE,
            service=FakeService(failure=failure),  # type: ignore[arg-type]
        )
        worker.start()
        with pytest.raises(type(failure)):
            worker.receive(delivery())
        assert worker.state is WorkerLifecycleState.FAILED
    invalid = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=InvalidMessageInput()),  # type: ignore[arg-type]
    )
    invalid.start()
    with pytest.raises(InvalidMessageInput):
        invalid.receive(delivery())
    assert invalid.state is WorkerLifecycleState.RUNNING


def test_worker_sanitizes_unknown_boundary_and_unexpected_failures() -> None:
    MessageWorker = message_worker_class()
    boundary = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=MessageBoundaryError()),  # type: ignore[arg-type]
    )
    boundary.start()
    with pytest.raises(MessageInternalError) as boundary_error:
        boundary.receive(delivery())
    assert boundary.state is WorkerLifecycleState.FAILED
    assert boundary_error.value.__cause__ is None
    unexpected = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=RuntimeError("synthetic hidden failure")),  # type: ignore[arg-type]
    )
    unexpected.start()
    with pytest.raises(MessageInternalError) as unexpected_error:
        unexpected.receive(delivery())
    assert unexpected.state is WorkerLifecycleState.FAILED
    assert unexpected_error.value.__cause__ is None
    assert "synthetic hidden failure" not in str(unexpected_error.value)


def test_worker_requires_explicit_reset_and_has_zero_automatic_recovery() -> None:
    from xianyu_system.worker.message.worker import (
        AUTOMATIC_PROCESSING_RETRIES,
        AUTOMATIC_RECONNECT_ATTEMPTS,
    )

    assert AUTOMATIC_PROCESSING_RETRIES == 0
    assert AUTOMATIC_RECONNECT_ATTEMPTS == 0
    MessageWorker = message_worker_class()
    blocked = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=DeduplicationConflict()),  # type: ignore[arg-type]
    )
    blocked.start()
    with pytest.raises(DeduplicationConflict):
        blocked.receive(delivery())
    with pytest.raises(InvalidWorkerTransition):
        blocked.stop()
    blocked.reset()
    assert blocked.state is WorkerLifecycleState.STOPPED
    failed = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=FakeService(failure=MessagePersistenceError()),  # type: ignore[arg-type]
    )
    failed.start()
    with pytest.raises(MessagePersistenceError):
        failed.receive(delivery())
    with pytest.raises(InvalidWorkerTransition):
        failed.stop()
    failed.reset()
    assert failed.state is WorkerLifecycleState.STOPPED
    assert isinstance(UUID(failed.profile_id), UUID)
    with pytest.raises(InvalidWorkerTransition):
        failed.reset()


def test_worker_reentrant_delivery_is_busy_without_second_service_operation() -> None:
    MessageWorker = message_worker_class()
    second_delivery = delivery(message_content="synthetic reentrant content")

    class ReentrantFakeService:
        def __init__(self) -> None:
            self.calls = 0
            self.inner_busy = False
            self.worker = None
            self.result = processing_result()
            self.reentered = False

        def receive(self, _delivery: SyntheticMessageDelivery) -> MessageProcessingResult:
            self.calls += 1
            if not self.reentered:
                self.reentered = True
                assert self.calls == 1
                with pytest.raises(WorkerBusy):
                    self.worker.receive(second_delivery)
                self.inner_busy = True
                assert self.calls == 1
            return self.result

    service = ReentrantFakeService()
    worker = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=service,  # type: ignore[arg-type]
    )
    service.worker = worker
    worker.start()
    outer_result = worker.receive(delivery())
    assert outer_result is service.result
    assert service.inner_busy is True
    assert service.calls == 1
    assert worker.state is WorkerLifecycleState.RUNNING
    assert worker.receive(delivery()).created_message is True
    assert service.calls == 2
    assert worker.state is WorkerLifecycleState.RUNNING


def test_worker_graceful_stop_waits_for_inflight_operation() -> None:
    MessageWorker = message_worker_class()
    entered = threading.Event()
    release = threading.Event()
    receive_done = threading.Event()
    stop_done = threading.Event()
    receive_errors: list[BaseException] = []
    stop_errors: list[BaseException] = []

    class BlockingFakeService:
        def __init__(self) -> None:
            self.calls = 0
            self.result = processing_result()

        def receive(self, _delivery: SyntheticMessageDelivery) -> MessageProcessingResult:
            self.calls += 1
            entered.set()
            if not release.wait(2.0):
                raise AssertionError("synthetic release event was not set")
            return self.result

    service = BlockingFakeService()
    worker = MessageWorker(
        profile_id=PROFILE_ID,
        account_reference=ACCOUNT_REFERENCE,
        service=service,  # type: ignore[arg-type]
    )
    worker.start()

    def run_receive() -> None:
        try:
            assert worker.receive(delivery()) is service.result
        except BaseException as exc:
            receive_errors.append(exc)
        finally:
            receive_done.set()

    def run_stop() -> None:
        try:
            worker.stop()
        except BaseException as exc:
            stop_errors.append(exc)
        finally:
            stop_done.set()

    receive_thread = threading.Thread(target=run_receive, name="synthetic-message-receive")
    stop_thread = threading.Thread(target=run_stop, name="synthetic-message-stop")
    try:
        receive_thread.start()
        assert entered.wait(2.0) is True
        stop_thread.start()
        wait_for_state(worker, WorkerLifecycleState.STOPPING)
        assert stop_done.wait(0.05) is False
        with pytest.raises(InvalidWorkerTransition):
            worker.receive(delivery(message_content="synthetic stopping delivery"))
        release.set()
        receive_thread.join(2.0)
        stop_thread.join(2.0)
        assert receive_done.is_set()
        assert stop_done.is_set()
        assert receive_thread.is_alive() is False
        assert stop_thread.is_alive() is False
        assert receive_errors == []
        assert stop_errors == []
        assert service.calls == 1
        assert worker.state is WorkerLifecycleState.STOPPED
    finally:
        release.set()
        receive_thread.join(2.0)
        stop_thread.join(2.0)
        assert receive_thread.is_alive() is False
        assert stop_thread.is_alive() is False
