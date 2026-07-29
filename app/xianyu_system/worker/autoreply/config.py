"""Configuration for deterministic local automatic reply."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class AutoreplyConfigError(ValueError):
    """Raised when autoreply configuration is unsafe or invalid."""


@dataclass(frozen=True)
class AutoreplyRule:
    id: str
    reply: str
    exact: str | None = None
    contains: tuple[str, ...] = ()

    def matches(self, text: str) -> bool:
        normalized = text.strip()
        if self.exact is not None and normalized == self.exact:
            return True
        return any(fragment and fragment in normalized for fragment in self.contains)


@dataclass(frozen=True)
class AutoreplyFallback:
    enabled: bool = False
    reply: str = ""


@dataclass(frozen=True)
class AutoreplyConfig:
    enabled: bool = False
    mode: str = "disabled"
    poll_seconds: float = 5.0
    account_allowlist: tuple[str, ...] = ()
    allowed_message_types: tuple[str, ...] = ("text",)
    conversation_cooldown_seconds: int = 30
    max_replies_per_conversation_per_hour: int = 10
    max_replies_per_account_per_hour: int = 100
    state_dir: Path = Path(".local/autoreply")
    rules: tuple[AutoreplyRule, ...] = ()
    fallback: AutoreplyFallback = field(default_factory=AutoreplyFallback)

    def __post_init__(self) -> None:
        if self.mode not in {"disabled", "dedicated-test"}:
            raise AutoreplyConfigError("autoreply mode must be disabled or dedicated-test")
        if self.enabled and self.mode != "dedicated-test":
            raise AutoreplyConfigError("enabled autoreply requires dedicated-test mode")
        if self.poll_seconds <= 0 or self.poll_seconds > 60:
            raise AutoreplyConfigError("poll_seconds must be between 1 and 60")
        if self.conversation_cooldown_seconds < 0 or self.conversation_cooldown_seconds > 3600:
            raise AutoreplyConfigError("conversation cooldown must be finite")
        if self.max_replies_per_conversation_per_hour < 1 or self.max_replies_per_conversation_per_hour > 100:
            raise AutoreplyConfigError("conversation hourly limit must be finite")
        if self.max_replies_per_account_per_hour < 1 or self.max_replies_per_account_per_hour > 1000:
            raise AutoreplyConfigError("account hourly limit must be finite")
        if self.enabled and not self.account_allowlist:
            raise AutoreplyConfigError("enabled autoreply requires an account allowlist")
        if any(not item for item in self.account_allowlist):
            raise AutoreplyConfigError("account allowlist entries must be non-empty")
        if self.enabled and not self.rules and not self.fallback.enabled:
            raise AutoreplyConfigError("enabled autoreply requires at least one rule or fallback")
        for rule in self.rules:
            if not rule.id or not rule.reply:
                raise AutoreplyConfigError("rules require id and reply")
            if rule.exact is None and not rule.contains:
                raise AutoreplyConfigError("rules require exact or contains")
        if self.fallback.enabled and not self.fallback.reply:
            raise AutoreplyConfigError("enabled fallback requires reply")

    @classmethod
    def disabled(cls) -> AutoreplyConfig:
        return cls()

    @classmethod
    def from_file(cls, path: Path) -> AutoreplyConfig:
        if not path.exists():
            return cls.disabled()
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if raw is None:
            return cls.disabled()
        if not isinstance(raw, dict):
            raise AutoreplyConfigError("autoreply config must be an object")
        return cls.from_mapping(raw)

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> AutoreplyConfig:
        rules: list[AutoreplyRule] = []
        for item in raw.get("rules") or []:
            if not isinstance(item, dict):
                raise AutoreplyConfigError("rule must be an object")
            contains = item.get("contains") or []
            if isinstance(contains, str):
                contains = [contains]
            rules.append(
                AutoreplyRule(
                    id=str(item.get("id") or ""),
                    exact=str(item["exact"]) if item.get("exact") is not None else None,
                    contains=tuple(str(value) for value in contains),
                    reply=str(item.get("reply") or ""),
                )
            )
        fallback_raw = raw.get("fallback") or {}
        if not isinstance(fallback_raw, dict):
            raise AutoreplyConfigError("fallback must be an object")
        allowlist = raw.get("account_allowlist") or []
        if isinstance(allowlist, str):
            allowlist = [allowlist]
        message_types = raw.get("allowed_message_types") or ["text"]
        if isinstance(message_types, str):
            message_types = [message_types]
        return cls(
            enabled=bool(raw.get("enabled", False)),
            mode=str(raw.get("mode") or "disabled"),
            poll_seconds=float(raw.get("poll_seconds", 5)),
            account_allowlist=tuple(str(value) for value in allowlist),
            allowed_message_types=tuple(str(value).lower() for value in message_types),
            conversation_cooldown_seconds=int(raw.get("conversation_cooldown_seconds", 30)),
            max_replies_per_conversation_per_hour=int(raw.get("max_replies_per_conversation_per_hour", 10)),
            max_replies_per_account_per_hour=int(raw.get("max_replies_per_account_per_hour", 100)),
            state_dir=Path(str(raw.get("state_dir") or ".local/autoreply")),
            rules=tuple(rules),
            fallback=AutoreplyFallback(
                enabled=bool(fallback_raw.get("enabled", False)),
                reply=str(fallback_raw.get("reply") or ""),
            ),
        )

    def match_reply(self, text: str) -> tuple[str, str] | None:
        for rule in self.rules:
            if rule.matches(text):
                return rule.id, rule.reply
        if self.fallback.enabled:
            return "fallback", self.fallback.reply
        return None
