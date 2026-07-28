"""Validation helpers for local deterministic Schedule requests."""

from __future__ import annotations

from dataclasses import dataclass

from xianyu_system.schedule.domain import ScheduleRequest, ScheduleValidationIssue
from xianyu_system.schedule.fingerprint import compute_schedule_fingerprint


@dataclass(frozen=True, slots=True)
class ScheduleValidationResult:
    is_valid: bool
    normalized_fingerprint: str | None
    issues: tuple[ScheduleValidationIssue, ...]


class ScheduleValidator:
    """Validate already-normalized ScheduleRequest objects without side effects."""

    def validate(self, request: object) -> ScheduleValidationResult:
        if not isinstance(request, ScheduleRequest):
            return ScheduleValidationResult(
                is_valid=False,
                normalized_fingerprint=None,
                issues=(ScheduleValidationIssue("request", "Schedule request shape is invalid."),),
            )
        return ScheduleValidationResult(
            is_valid=True,
            normalized_fingerprint=compute_schedule_fingerprint(request),
            issues=(),
        )
