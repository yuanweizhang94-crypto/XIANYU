from __future__ import annotations

import importlib
import io
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import pytest

from xianyu_system.core import logging as project_logging
from xianyu_system.core.logging import (
    REDACTED_VALUE,
    ManagedStreamHandler,
    configure_logging,
    redact_value,
    shutdown_logging,
)
from xianyu_system.core.scheduler import create_scheduler, shutdown_scheduler, start_scheduler

ROOT = Path(__file__).resolve().parents[2]
SENSITIVE_VALUE = "synthetic" + "-value"
LONG_SENSITIVE_VALUE = "synthetic" + "-value-that-must-not-leak"


def logger_name(suffix: str) -> str:
    return f"xianyu.test.{suffix}.{id(object())}"


def parsed_lines(stream: io.StringIO) -> list[dict[str, object]]:
    lines = [line for line in stream.getvalue().splitlines() if line]
    return [json.loads(line) for line in lines]


def test_json_log_record_is_single_line_with_required_fields() -> None:
    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name=logger_name("json"), stream=stream)

    logger.info("hello world")
    shutdown_logging(logger)

    lines = stream.getvalue().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert set(data) >= {"timestamp", "level", "logger", "message"}
    assert str(data["timestamp"]).endswith("Z")
    assert "T" in str(data["timestamp"])
    assert data["level"] == "INFO"
    assert str(data["logger"]).startswith("xianyu.test.json")
    assert data["message"] == "hello world"


def test_log_level_filtering_info_and_error() -> None:
    info_stream = io.StringIO()
    info_logger = configure_logging(level="INFO", logger_name=logger_name("info"), stream=info_stream)
    info_logger.debug("hidden")
    info_logger.info("visible")
    shutdown_logging(info_logger)
    assert [item["message"] for item in parsed_lines(info_stream)] == ["visible"]

    error_stream = io.StringIO()
    error_logger = configure_logging(level="ERROR", logger_name=logger_name("error"), stream=error_stream)
    error_logger.warning("hidden")
    error_logger.error("visible-error")
    shutdown_logging(error_logger)
    assert [item["message"] for item in parsed_lines(error_stream)] == ["visible-error"]


def test_extra_fields_are_preserved_and_nested_sensitive_values_redacted() -> None:
    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name=logger_name("extra"), stream=stream)

    logger.info(
        "Example",
        extra={
            "event": "example.event",
            "account": "demo",
            "metadata": {"token": SENSITIVE_VALUE, "result": "ok"},
        },
    )
    shutdown_logging(logger)

    data = parsed_lines(stream)[0]
    assert data["event"] == "example.event"
    assert data["account"] == "demo"
    assert data["metadata"] == {"token": REDACTED_VALUE, "result": "ok"}
    assert SENSITIVE_VALUE not in stream.getvalue()


def test_redact_value_recurses_through_nested_containers() -> None:
    value = {
        "token": SENSITIVE_VALUE,
        "nested": {
            "password": SENSITIVE_VALUE,
            "items": [
                {"cookie": SENSITIVE_VALUE},
                ({"authorization": SENSITIVE_VALUE}, {"api_key": SENSITIVE_VALUE}),
                {"client_secret": SENSITIVE_VALUE},
            ],
        },
    }

    redacted = redact_value(value)

    assert json.dumps(redacted).count(REDACTED_VALUE) == 6
    assert SENSITIVE_VALUE not in json.dumps(redacted)


def test_sensitive_field_names_are_case_and_separator_insensitive() -> None:
    value = {
        "TOKEN": SENSITIVE_VALUE,
        "Access-Token": SENSITIVE_VALUE,
        "client_secret": SENSITIVE_VALUE,
        "API_KEY": SENSITIVE_VALUE,
        "Authorization": SENSITIVE_VALUE,
    }

    assert redact_value(value) == {
        "TOKEN": REDACTED_VALUE,
        "Access-Token": REDACTED_VALUE,
        "client_secret": REDACTED_VALUE,
        "API_KEY": REDACTED_VALUE,
        "Authorization": REDACTED_VALUE,
    }


def test_non_sensitive_fields_are_not_over_redacted() -> None:
    value = {
        "monkey": "banana",
        "tokenizer": "enabled",
        "account_id": "acct-123",
        "event": "safe.event",
        "status": "ok",
        "password_policy_enabled": True,
    }

    assert redact_value(value) == value


def test_message_text_redacts_key_value_and_header_patterns() -> None:
    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name=logger_name("message"), stream=stream)
    message = " ".join(
        [
            "token=" + LONG_SENSITIVE_VALUE,
            "password: " + LONG_SENSITIVE_VALUE,
            "Authorization: Bearer " + LONG_SENSITIVE_VALUE,
            "Cookie: session=" + LONG_SENSITIVE_VALUE,
            "api_key=" + LONG_SENSITIVE_VALUE,
        ]
    )

    logger.info(message)
    shutdown_logging(logger)

    output = stream.getvalue()
    data = parsed_lines(stream)[0]
    assert LONG_SENSITIVE_VALUE not in output
    assert REDACTED_VALUE in str(data["message"])


def test_exception_text_is_redacted_and_remains_single_line_json() -> None:
    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name=logger_name("exception"), stream=stream)

    try:
        raise RuntimeError("token=" + LONG_SENSITIVE_VALUE)
    except RuntimeError:
        logger.exception("failure password: " + LONG_SENSITIVE_VALUE)
    shutdown_logging(logger)

    lines = stream.getvalue().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert "exception" in data
    assert LONG_SENSITIVE_VALUE not in stream.getvalue()
    assert REDACTED_VALUE in stream.getvalue()


def test_repeated_configuration_replaces_only_managed_handler() -> None:
    first_stream = io.StringIO()
    second_stream = io.StringIO()
    name = logger_name("repeat")

    first_logger = configure_logging(level="INFO", logger_name=name, stream=first_stream)
    second_logger = configure_logging(level="ERROR", logger_name=name, stream=second_stream)
    second_logger.warning("hidden")
    second_logger.error("shown")
    shutdown_logging(second_logger)

    assert first_logger is second_logger
    assert sum(isinstance(handler, ManagedStreamHandler) for handler in second_logger.handlers) == 0
    assert first_stream.getvalue() == ""
    assert [item["message"] for item in parsed_lines(second_stream)] == ["shown"]


def test_external_handlers_are_preserved_by_configure_and_shutdown() -> None:
    class ExternalHandler(logging.Handler):
        def __init__(self) -> None:
            super().__init__()
            self.was_closed = False

        def emit(self, record: logging.LogRecord) -> None:
            return None

        def close(self) -> None:
            self.was_closed = True
            super().close()

    logger = logging.getLogger(logger_name("external"))
    external = ExternalHandler()
    logger.addHandler(external)

    configured = configure_logging(level="INFO", logger_name=logger.name, stream=io.StringIO())
    shutdown_logging(configured)

    assert external in logger.handlers
    assert external.was_closed is False
    logger.removeHandler(external)


def test_root_logger_is_unchanged_by_project_logger_management() -> None:
    root = logging.getLogger()
    original_level = root.level
    original_handlers = list(root.handlers)
    original_propagate = root.propagate

    logger = configure_logging(level="INFO", logger_name=logger_name("root"), stream=io.StringIO())
    shutdown_logging(logger)

    assert root.level == original_level
    assert list(root.handlers) == original_handlers
    assert root.propagate == original_propagate


def test_shutdown_removes_managed_handlers_and_stops_writing_to_stream() -> None:
    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name=logger_name("shutdown"), stream=stream)
    logger.info("before")
    shutdown_logging(logger)
    logger.info("after")

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in logger.handlers)
    assert [item["message"] for item in parsed_lines(stream)] == ["before"]


def test_invalid_level_raises_without_changing_existing_handlers() -> None:
    logger = logging.getLogger(logger_name("invalid"))
    external = logging.StreamHandler(io.StringIO())
    logger.addHandler(external)
    original_handlers = list(logger.handlers)
    original_level = logger.level
    original_propagate = logger.propagate

    with pytest.raises(ValueError):
        configure_logging(level="TRACE", logger_name=logger.name, stream=io.StringIO())

    assert list(logger.handlers) == original_handlers
    assert logger.level == original_level
    assert logger.propagate == original_propagate
    logger.removeHandler(external)


def test_import_and_stringio_configuration_create_no_files(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    script = """
import io
import xianyu_system.core.logging as logging_boundary
stream = io.StringIO()
logger = logging_boundary.configure_logging(
    level='INFO', logger_name='xianyu.test.file.side.effect', stream=stream
)
logger.info('safe')
logging_boundary.shutdown_logging(logger)
"""
    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert not (tmp_path / "logs").exists()
    for pattern in ["*.log", "*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []



def test_scheduler_logs_use_project_json_formatter_and_preserve_root_logger() -> None:
    root = logging.getLogger()
    original_level = root.level
    original_handlers = list(root.handlers)
    original_propagate = root.propagate
    stream = io.StringIO()
    logger = configure_logging(
        level="INFO",
        logger_name=logger_name("scheduler"),
        stream=stream,
    )

    scheduler = create_scheduler(logger=logger)
    try:
        start_scheduler(scheduler)
    finally:
        shutdown_scheduler(scheduler)
        shutdown_logging(logger)

    records = parsed_lines(stream)
    assert records
    assert all(set(record) >= {"timestamp", "level", "logger", "message"} for record in records)
    assert any(record["message"] == "Scheduler started" for record in records)
    assert any(record["message"] == "Scheduler has been shut down" for record in records)
    assert root.level == original_level
    assert list(root.handlers) == original_handlers
    assert root.propagate == original_propagate

def test_logging_module_uses_only_standard_library_imports() -> None:
    source = (ROOT / "app/xianyu_system/core/logging.py").read_text(encoding="utf-8")

    assert "structlog" not in source
    assert "python-json-logger" not in source
    assert "loguru" not in source
    assert "sentry_sdk" not in source
    assert "opentelemetry" not in source
    assert "FileHandler" not in source
    assert "basicConfig(" not in source
    assert "logging.shutdown(" not in source
    assert importlib.import_module("xianyu_system.core.logging") is project_logging
