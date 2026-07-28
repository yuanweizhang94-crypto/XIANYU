"""Deterministic fingerprinting for approved local Schedule input."""

from __future__ import annotations

import hashlib
import json
from typing import Any, cast

from xianyu_system.schedule.domain import ScheduleRequest, ScheduleTriggerType


def _payload(request: ScheduleRequest) -> dict[str, Any]:
    trigger = cast(ScheduleTriggerType, request.trigger_type)
    return {
        "schedule_id": request.schedule_id,
        "publish_request_id": request.publish_request_id,
        "idempotency_key": request.idempotency_key,
        "trigger_type": trigger.value,
        "requested_at": request.requested_at.isoformat(),
        "run_at": None if request.run_at is None else request.run_at.isoformat(),
        "misfire_grace_seconds": request.misfire_grace_seconds,
        "synthetic_fixture": request.synthetic_fixture,
        "correlation_id": request.correlation_id,
    }


def compute_schedule_fingerprint(request: ScheduleRequest) -> str:
    """Return a stable SHA-256 fingerprint for local one-time schedule input."""
    encoded = json.dumps(_payload(request), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
