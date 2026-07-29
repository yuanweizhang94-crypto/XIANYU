"""Local non-sensitive state and idempotency for automatic reply."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

TERMINAL_BLOCKING_RESULTS = {"SUCCESS", "UNKNOWN"}


def now_epoch() -> float:
    return time.time()


@dataclass
class AutoreplyState:
    path: Path
    processed: dict[str, dict[str, Any]] = field(default_factory=dict)
    historical: set[str] = field(default_factory=set)
    counters: dict[str, int] = field(default_factory=lambda: {"success": 0, "skipped": 0, "failed": 0, "unknown": 0})
    listener_owned: bool = False
    started_at: float | None = None
    last_poll_at: float | None = None
    last_success_at: float | None = None

    @classmethod
    def load(cls, path: Path) -> AutoreplyState:
        if not path.exists():
            return cls(path=path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        state = cls(path=path)
        state.processed = dict(raw.get("processed") or {})
        state.historical = set(raw.get("historical") or [])
        state.counters.update({k: int(v) for k, v in dict(raw.get("counters") or {}).items()})
        state.listener_owned = bool(raw.get("listener_owned", False))
        state.started_at = raw.get("started_at")
        state.last_poll_at = raw.get("last_poll_at")
        state.last_success_at = raw.get("last_success_at")
        return state

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "processed": self.processed,
            "historical": sorted(self.historical),
            "counters": self.counters,
            "listener_owned": self.listener_owned,
            "started_at": self.started_at,
            "last_poll_at": self.last_poll_at,
            "last_success_at": self.last_success_at,
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8", newline="\n")
        tmp.replace(self.path)

    def mark_historical(self, keys: set[str]) -> None:
        self.historical.update(keys)
        self.save()

    def has_blocking_record(self, key: str) -> bool:
        record = self.processed.get(key)
        return bool(record and record.get("result") in TERMINAL_BLOCKING_RESULTS)

    def record(self, key: str, *, result: str, rule_id: str | None, operation_id: str | None) -> None:
        current = now_epoch()
        self.processed[key] = {
            "result": result,
            "rule_id": rule_id,
            "operation_id": operation_id,
            "timestamp": current,
        }
        if result == "SUCCESS":
            self.counters["success"] = self.counters.get("success", 0) + 1
            self.last_success_at = current
        elif result == "UNKNOWN":
            self.counters["unknown"] = self.counters.get("unknown", 0) + 1
        elif result == "SKIPPED":
            self.counters["skipped"] = self.counters.get("skipped", 0) + 1
        else:
            self.counters["failed"] = self.counters.get("failed", 0) + 1
        self.save()
