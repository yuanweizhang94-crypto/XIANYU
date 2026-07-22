from __future__ import annotations

import json
import logging
import re
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import TextIO

REDACTED_VALUE = "[REDACTED]"

SENSITIVE_FIELD_NAMES = {
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "cookie",
    "set_cookie",
    "password",
    "passwd",
    "credential",
    "credentials",
    "authorization",
    "proxy_authorization",
    "api_key",
    "apikey",
    "private_key",
    "client_secret",
}
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
SENSITIVE_TEXT_KEY_PATTERN = (
    r"access[-_]?token|refresh[-_]?token|set[-_]?cookie|proxy[-_]?authorization|"
    r"api[-_]?key|private[-_]?key|client[-_]?secret|authorization|credentials?|"
    r"password|passwd|secret|token|cookie"
)
KEY_VALUE_PATTERN = re.compile(
    rf"(?i)\b(?P<key>{SENSITIVE_TEXT_KEY_PATTERN})\b\s*=\s*(?P<value>[^\s,;]+)"
)
HEADER_PATTERN = re.compile(
    rf"(?i)\b(?P<key>{SENSITIVE_TEXT_KEY_PATTERN})\b\s*:\s*(?P<value>[^\r\n,;]+)"
)
STANDARD_LOG_RECORD_KEYS = set(
    logging.LogRecord(
        name="",
        level=0,
        pathname="",
        lineno=0,
        msg="",
        args=(),
        exc_info=None,
    ).__dict__
) | {"message", "asctime"}


class ManagedStreamHandler(logging.StreamHandler[TextIO]):
    """Stream handler owned by XIANYU logging configuration."""


class StructuredJsonFormatter(logging.Formatter):
    """Format log records as single-line JSON with redaction."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": redact_text(record.getMessage()),
        }

        for key, value in record.__dict__.items():
            if key in STANDARD_LOG_RECORD_KEYS or key.startswith("_"):
                continue
            payload[key] = redact_value(value, field_name=key)

        if record.exc_info:
            payload["exception"] = redact_text(self.formatException(record.exc_info))

        safe_payload = {key: to_jsonable(value) for key, value in payload.items()}
        return json.dumps(safe_payload, ensure_ascii=False, separators=(",", ":"))


def normalize_field_name(field_name: str) -> str:
    return field_name.lower().replace("-", "_")


def is_sensitive_field_name(field_name: str | None) -> bool:
    if field_name is None:
        return False
    return normalize_field_name(field_name) in SENSITIVE_FIELD_NAMES


def redact_text(text: object) -> str:
    redacted = str(text)
    redacted = KEY_VALUE_PATTERN.sub(lambda match: f"{match.group('key')}={REDACTED_VALUE}", redacted)
    redacted = HEADER_PATTERN.sub(lambda match: f"{match.group('key')}: {REDACTED_VALUE}", redacted)
    return redacted


def redact_value(value: object, *, field_name: str | None = None) -> object:
    if is_sensitive_field_name(field_name):
        return REDACTED_VALUE
    if isinstance(value, Mapping):
        return {str(key): redact_value(item, field_name=str(key)) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, set):
        return [redact_value(item) for item in sorted(value, key=repr)]
    if isinstance(value, str):
        return redact_text(value)
    return value


def to_jsonable(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, set):
        return [to_jsonable(item) for item in sorted(value, key=repr)]
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value


def level_number(level: str) -> int:
    normalized = level.upper()
    if normalized not in LOG_LEVELS:
        supported = ", ".join(sorted(LOG_LEVELS))
        raise ValueError(f"Unsupported log level {level!r}; expected one of: {supported}")
    return LOG_LEVELS[normalized]


def configure_logging(
    *,
    level: str,
    logger_name: str,
    stream: TextIO | None = None,
) -> logging.Logger:
    resolved_level = level_number(level)
    logger = logging.getLogger(logger_name)

    for handler in list(logger.handlers):
        if isinstance(handler, ManagedStreamHandler):
            logger.removeHandler(handler)
            handler.flush()
            handler.close()

    handler = ManagedStreamHandler(stream if stream is not None else sys.stderr)
    handler.setFormatter(StructuredJsonFormatter())
    handler.setLevel(resolved_level)

    logger.setLevel(resolved_level)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def shutdown_logging(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        if isinstance(handler, ManagedStreamHandler):
            logger.removeHandler(handler)
            handler.flush()
            handler.close()


__all__ = [
    "ManagedStreamHandler",
    "REDACTED_VALUE",
    "StructuredJsonFormatter",
    "configure_logging",
    "redact_value",
    "shutdown_logging",
]
