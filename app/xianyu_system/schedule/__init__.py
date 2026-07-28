"""Lazy public surface for the local deterministic Schedule boundary."""

from __future__ import annotations

__all__ = [
    "ScheduleCancellationReason",
    "ScheduleDecision",
    "ScheduleDecisionType",
    "ScheduleDispatchOutcome",
    "ScheduleDispatchResult",
    "ScheduleLifecycle",
    "ScheduleRequest",
    "ScheduleTriggerType",
    "ScheduleValidationIssue",
    "compute_schedule_fingerprint",
    "ScheduleService",
]


def __getattr__(name: str) -> object:
    if name in {
        "ScheduleCancellationReason",
        "ScheduleDecision",
        "ScheduleDecisionType",
        "ScheduleDispatchOutcome",
        "ScheduleDispatchResult",
        "ScheduleLifecycle",
        "ScheduleRequest",
        "ScheduleTriggerType",
        "ScheduleValidationIssue",
    }:
        from xianyu_system.schedule import domain

        return getattr(domain, name)
    if name == "compute_schedule_fingerprint":
        from xianyu_system.schedule.fingerprint import compute_schedule_fingerprint

        return compute_schedule_fingerprint
    if name == "ScheduleService":
        from xianyu_system.schedule.service import ScheduleService

        return ScheduleService
    raise AttributeError(name)
