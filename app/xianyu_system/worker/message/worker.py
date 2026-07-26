"""Local synchronous Profile-scoped Message Worker."""

from __future__ import annotations

from threading import Lock

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
    normalize_required_text,
    normalize_uuid,
)
from xianyu_system.worker.message.service import MessageService
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

AUTOMATIC_RECONNECT_ATTEMPTS = 0
AUTOMATIC_PROCESSING_RETRIES = 0


class MessageWorker:
    """Explicitly controlled local synchronous Worker for one Profile."""

    def __init__(
        self,
        *,
        profile_id: str,
        account_reference: str,
        service: MessageService,
    ) -> None:
        self._profile_id = normalize_uuid(profile_id)
        self._account_reference = normalize_required_text(
            account_reference,
            max_length=256,
        )
        self._service = service
        self._state = WorkerLifecycleState.STOPPED
        self._inflight = Lock()

    @property
    def profile_id(self) -> str:
        return self._profile_id

    @property
    def account_reference(self) -> str:
        return self._account_reference

    @property
    def state(self) -> WorkerLifecycleState:
        return self._state

    def start(self) -> None:
        if self._state is not WorkerLifecycleState.STOPPED:
            raise InvalidWorkerTransition()
        self._state = WorkerLifecycleState.STARTING
        self._state = WorkerLifecycleState.RUNNING

    def stop(self) -> None:
        if self._state is WorkerLifecycleState.STOPPED:
            return
        if self._state is not WorkerLifecycleState.RUNNING:
            raise InvalidWorkerTransition()
        self._state = WorkerLifecycleState.STOPPING
        acquired = self._inflight.acquire(blocking=True)
        if acquired:
            self._inflight.release()
        self._state = WorkerLifecycleState.STOPPED

    def reset(self) -> None:
        if self._state not in {
            WorkerLifecycleState.BLOCKED,
            WorkerLifecycleState.FAILED,
        }:
            raise InvalidWorkerTransition()
        self._state = WorkerLifecycleState.STOPPED

    def receive(
        self,
        delivery: SyntheticMessageDelivery,
    ) -> MessageProcessingResult:
        if self._state is WorkerLifecycleState.BLOCKED:
            raise WorkerBlocked()
        if self._state is not WorkerLifecycleState.RUNNING:
            raise InvalidWorkerTransition()
        if delivery.profile_id != self._profile_id:
            self._state = WorkerLifecycleState.BLOCKED
            raise ProfileOwnershipViolation()
        if delivery.account_reference != self._account_reference:
            self._state = WorkerLifecycleState.BLOCKED
            raise ProfileOwnershipViolation()
        if not self._inflight.acquire(blocking=False):
            raise WorkerBusy()
        try:
            return self._service.receive(delivery)
        except InvalidMessageInput:
            raise
        except ProfileOwnershipViolation:
            self._state = WorkerLifecycleState.BLOCKED
            raise
        except MessageAuthorizationViolation:
            self._state = WorkerLifecycleState.BLOCKED
            raise
        except MessageRiskViolation:
            self._state = WorkerLifecycleState.BLOCKED
            raise
        except MessageProtocolViolation:
            self._state = WorkerLifecycleState.BLOCKED
            raise
        except DeduplicationConflict:
            self._state = WorkerLifecycleState.BLOCKED
            raise
        except MessagePersistenceError:
            self._state = WorkerLifecycleState.FAILED
            raise
        except MessageInternalError:
            self._state = WorkerLifecycleState.FAILED
            raise
        except MessageBoundaryError:
            self._state = WorkerLifecycleState.FAILED
            raise MessageInternalError() from None
        except Exception:
            self._state = WorkerLifecycleState.FAILED
            raise MessageInternalError() from None
        finally:
            self._inflight.release()
