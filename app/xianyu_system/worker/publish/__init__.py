"""Lazy public surface for the local deterministic Publish boundary."""

from __future__ import annotations

from typing import Any

_DOMAIN_EXPORTS = {
    "InvalidPublishInput",
    "ListingDraft",
    "ListingDraftLifecycle",
    "PublishAttemptLifecycle",
    "PublishAttemptSnapshot",
    "PublishAuthorizationState",
    "PublishBoundaryError",
    "PublishDecision",
    "PublishDecisionType",
    "PublishEvaluationContext",
    "PublishFailureCategory",
    "PublishOutcomeType",
    "PublishPersistenceError",
    "PublishReasonCode",
    "PublishRequest",
    "PublishRequestLifecycle",
    "PublishValidationResult",
    "ValidationIssue",
}

__all__ = sorted(
    [
        *_DOMAIN_EXPORTS,
        "PublishRepository",
        "PublishService",
        "PublishValidator",
        "compute_publish_fingerprint",
    ]
)


def __getattr__(name: str) -> Any:
    if name in _DOMAIN_EXPORTS:
        from xianyu_system.worker.publish import domain

        return getattr(domain, name)
    if name == "compute_publish_fingerprint":
        from xianyu_system.worker.publish.fingerprint import compute_publish_fingerprint

        return compute_publish_fingerprint
    if name == "PublishValidator":
        from xianyu_system.worker.publish.validation import PublishValidator

        return PublishValidator
    if name == "PublishRepository":
        from xianyu_system.worker.publish.persistence import PublishRepository

        return PublishRepository
    if name == "PublishService":
        from xianyu_system.worker.publish.service import PublishService

        return PublishService
    raise AttributeError(name)
