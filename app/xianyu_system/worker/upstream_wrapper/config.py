"""Configuration for the localhost-only upstream Pilot wrapper."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

_ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


class UpstreamWrapperConfigError(ValueError):
    """Raised when wrapper configuration is unsafe or incomplete."""


def _as_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise UpstreamWrapperConfigError("invalid boolean configuration")


def _load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _require_loopback(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in _ALLOWED_HOSTS:
        raise UpstreamWrapperConfigError("upstream URL must be loopback-only")
    return url.rstrip("/")


@dataclass(frozen=True)
class UpstreamWrapperConfig:
    backend_base_url: str = "http://127.0.0.1:18089"
    listener_base_url: str = "http://127.0.0.1:18090"
    backend_auth_header: str | None = None
    wrapper_mode: str = "pilot"
    require_manual_confirmation: bool = True
    allow_live_writes: bool = False
    request_timeout_seconds: float = 5.0
    read_retries: int = 1
    audit_path: Path = Path(".local/upstream-wrapper-audit.jsonl")
    pilot_root: Path = Path("D:/xianyu-upstream-pilot")

    def __post_init__(self) -> None:
        _require_loopback(self.backend_base_url)
        _require_loopback(self.listener_base_url)
        if self.wrapper_mode != "pilot":
            raise UpstreamWrapperConfigError("only pilot wrapper mode is supported")
        if self.request_timeout_seconds <= 0 or self.request_timeout_seconds > 30:
            raise UpstreamWrapperConfigError("timeout must be between 0 and 30 seconds")
        if self.read_retries < 0 or self.read_retries > 3:
            raise UpstreamWrapperConfigError("read retries must be between 0 and 3")

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> UpstreamWrapperConfig:
        file_values = _load_env_file(env_file or Path(".local/xianyu-upstream.env"))

        def value(name: str, default: str | None = None) -> str | None:
            return os.environ.get(name, file_values.get(name, default))

        mode = value("XIANYU_WRAPPER_MODE", "pilot") or "pilot"
        if mode != "pilot":
            raise UpstreamWrapperConfigError("only pilot wrapper mode is supported")
        read_retries = int(value("XIANYU_UPSTREAM_READ_RETRIES", "1") or "1")
        if read_retries < 0 or read_retries > 3:
            raise UpstreamWrapperConfigError("read retries must be between 0 and 3")
        timeout = float(value("XIANYU_UPSTREAM_TIMEOUT_SECONDS", "5") or "5")
        if timeout <= 0 or timeout > 30:
            raise UpstreamWrapperConfigError("timeout must be between 0 and 30 seconds")
        return cls(
            backend_base_url=_require_loopback(value("XIANYU_UPSTREAM_BACKEND_URL", cls.backend_base_url) or cls.backend_base_url),
            listener_base_url=_require_loopback(value("XIANYU_UPSTREAM_LISTENER_URL", cls.listener_base_url) or cls.listener_base_url),
            backend_auth_header=value("XIANYU_UPSTREAM_AUTH_HEADER"),
            wrapper_mode=mode,
            require_manual_confirmation=_as_bool(value("XIANYU_REQUIRE_MANUAL_CONFIRMATION"), default=True),
            allow_live_writes=_as_bool(value("XIANYU_ALLOW_LIVE_WRITES"), default=False),
            request_timeout_seconds=timeout,
            read_retries=read_retries,
            audit_path=Path(value("XIANYU_WRAPPER_AUDIT_PATH", ".local/upstream-wrapper-audit.jsonl") or ".local/upstream-wrapper-audit.jsonl"),
            pilot_root=Path(value("XIANYU_UPSTREAM_PILOT_ROOT", "D:/xianyu-upstream-pilot") or "D:/xianyu-upstream-pilot"),
        )
