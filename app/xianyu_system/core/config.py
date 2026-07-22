from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentName = Literal["local", "test"]
LogLevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class ApplicationSettings(BaseSettings):
    """Typed, immutable settings for the local XIANYU Core."""

    model_config = SettingsConfigDict(
        env_prefix="XIANYU_",
        case_sensitive=False,
        validate_default=True,
        extra="forbid",
        frozen=True,
        env_file=None,
        str_strip_whitespace=True,
    )

    environment: EnvironmentName = "local"
    app_title: str = Field(default="XIANYU", min_length=1, max_length=100)
    app_version: str = Field(default="0.1.0", min_length=1, max_length=50)
    debug: bool = False
    log_level: LogLevelName = "INFO"
    database_path: Path = Path("data/xianyu.db")


__all__ = [
    "ApplicationSettings",
    "EnvironmentName",
    "LogLevelName",
]
