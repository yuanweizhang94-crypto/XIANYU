"""Local synthetic message receiving boundary package.

Importing this package intentionally avoids importing persistence or registering ORM
metadata. Runtime classes are loaded lazily by name.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "Conversation",
    "DeduplicationDecision",
    "DeduplicationConflict",
    "DeliveryAttempt",
    "InvalidMessageInput",
    "InvalidWorkerTransition",
    "MessageAuthorizationViolation",
    "MessageBoundaryError",
    "MessageErrorCode",
    "MessageInternalError",
    "MessagePersistenceError",
    "MessageProcessingResult",
    "MessageProtocolViolation",
    "MessageRecord",
    "MessageRiskViolation",
    "ProfileOwnershipViolation",
    "SyntheticMessageDelivery",
    "WorkerBlocked",
    "WorkerBusy",
    "WorkerLifecycleState",
    "MessageService",
    "MessageWorker",
]

_DOMAIN_EXPORTS = {
    "Conversation",
    "DeduplicationDecision",
    "DeduplicationConflict",
    "DeliveryAttempt",
    "InvalidMessageInput",
    "InvalidWorkerTransition",
    "MessageAuthorizationViolation",
    "MessageBoundaryError",
    "MessageErrorCode",
    "MessageInternalError",
    "MessagePersistenceError",
    "MessageProcessingResult",
    "MessageProtocolViolation",
    "MessageRecord",
    "MessageRiskViolation",
    "ProfileOwnershipViolation",
    "WorkerBlocked",
    "WorkerBusy",
    "WorkerLifecycleState",
}


def __getattr__(name: str) -> Any:
    if name in _DOMAIN_EXPORTS:
        from xianyu_system.worker.message import domain

        return getattr(domain, name)
    if name == "SyntheticMessageDelivery":
        from xianyu_system.worker.message.transport import SyntheticMessageDelivery

        return SyntheticMessageDelivery
    if name == "MessageService":
        from xianyu_system.worker.message.service import MessageService

        return MessageService
    if name == "MessageWorker":
        from xianyu_system.worker.message.worker import MessageWorker

        return MessageWorker
    raise AttributeError(name)
