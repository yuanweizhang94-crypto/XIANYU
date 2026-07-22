from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from pydantic_settings import BaseSettings

from xianyu_system.core.config import ApplicationSettings

ROOT = Path(__file__).resolve().parents[2]
SUPPORTED_ENV_VARS = [
    "XIANYU_ENVIRONMENT",
    "XIANYU_APP_TITLE",
    "XIANYU_APP_VERSION",
    "XIANYU_DEBUG",
    "XIANYU_LOG_LEVEL",
    "XIANYU_DATABASE_PATH",
    "xianyu_environment",
    "xianyu_app_title",
    "xianyu_app_version",
    "xianyu_debug",
    "xianyu_log_level",
    "xianyu_database_path",
]
FORBIDDEN_FIELD_PARTS = {
    "secret",
    "token",
    "cookie",
    "password",
    "credential",
    "profile",
    "wecom",
    "api_key",
    "captcha",
}


def clear_supported_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in SUPPORTED_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_default_settings_are_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)

    settings = ApplicationSettings()

    assert settings.environment == "local"
    assert settings.app_title == "XIANYU"
    assert settings.app_version == "0.1.0"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.database_path == Path("data/xianyu.db")


def test_environment_values_are_typed_without_creating_database(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_supported_environment(monkeypatch)
    database_path = tmp_path / "temporary" / "custom.db"
    monkeypatch.setenv("XIANYU_DEBUG", "true")
    monkeypatch.setenv("XIANYU_DATABASE_PATH", str(database_path))

    settings = ApplicationSettings()

    assert settings.debug is True
    assert isinstance(settings.database_path, Path)
    assert settings.database_path == database_path
    assert not database_path.exists()
    assert not database_path.parent.exists()


def test_environment_variables_require_xianyu_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("APP_TITLE", "WRONG")

    settings = ApplicationSettings()

    assert settings.debug is False
    assert settings.app_title == "XIANYU"


def test_environment_variable_names_are_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("xianyu_debug", "true")

    assert ApplicationSettings().debug is True


def test_explicit_constructor_values_override_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("XIANYU_DEBUG", "true")

    assert ApplicationSettings(debug=False).debug is False


def test_invalid_environment_name_fails_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("XIANYU_ENVIRONMENT", "production")

    with pytest.raises(ValidationError):
        ApplicationSettings()


def test_invalid_log_level_fails_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("XIANYU_LOG_LEVEL", "TRACE")

    with pytest.raises(ValidationError):
        ApplicationSettings()


def test_unknown_explicit_field_fails_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)

    with pytest.raises(ValidationError):
        ApplicationSettings(**{"unknown_option": True})


def test_settings_are_immutable(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    settings = ApplicationSettings()

    with pytest.raises(ValidationError):
        settings.debug = True


def test_dotenv_file_is_not_loaded_automatically(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_supported_environment(monkeypatch)
    (tmp_path / ".env").write_text("XIANYU_DEBUG=true\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert ApplicationSettings().debug is False


def test_database_path_parent_is_not_created(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    clear_supported_environment(monkeypatch)
    database_path = tmp_path / "missing" / "test.db"

    settings = ApplicationSettings(database_path=database_path)

    assert settings.database_path == database_path
    assert not database_path.exists()
    assert not database_path.parent.exists()


def test_multiple_settings_instances_are_isolated(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)

    first = ApplicationSettings()
    second = ApplicationSettings()

    assert first is not second
    assert first.model_dump() == second.model_dump()


def test_settings_fields_do_not_include_sensitive_platform_names() -> None:
    field_names = set(ApplicationSettings.model_fields)

    assert field_names == {
        "environment",
        "app_title",
        "app_version",
        "debug",
        "log_level",
        "database_path",
    }
    assert all(
        forbidden not in field_name
        for field_name in field_names
        for forbidden in FORBIDDEN_FIELD_PARTS
    )


def test_application_settings_extends_base_settings() -> None:
    assert issubclass(ApplicationSettings, BaseSettings)


def test_settings_config_declares_chg_0002_boundaries() -> None:
    config = ApplicationSettings.model_config

    assert config["env_prefix"] == "XIANYU_"
    assert config["case_sensitive"] is False
    assert config["frozen"] is True
    assert config["env_file"] is None
    assert config["extra"] == "forbid"


def test_import_config_has_no_file_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    result = subprocess.run(
        [sys.executable, "-c", "import xianyu_system.core.config"],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stderr == ""
    assert not (tmp_path / "data").exists()
    assert not (tmp_path / "logs").exists()
    assert not (tmp_path / ".env").exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []
