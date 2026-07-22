from __future__ import annotations

from pathlib import Path
from typing import Literal, cast

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter, FastAPI, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from xianyu_system.core.config import ApplicationSettings, EnvironmentName
from xianyu_system.core.database import DatabaseResources
from xianyu_system.core.scheduler import SCHEDULER_TIMEZONE

HEALTH_PATH = "/health"

OverallHealthStatus = Literal["ok", "degraded"]
ComponentHealthStatus = Literal["ok", "unavailable"]
JournalMode = Literal["wal"]
SchedulerTimezone = Literal["UTC"]


class DatabaseHealth(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: ComponentHealthStatus
    connected: bool
    journal_mode: JournalMode | None


class SchedulerHealth(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: ComponentHealthStatus
    running: bool
    job_count: int = Field(ge=0)
    timezone: SchedulerTimezone


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: OverallHealthStatus
    service: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=50)
    environment: EnvironmentName
    database: DatabaseHealth
    scheduler: SchedulerHealth


def unavailable_database_health() -> DatabaseHealth:
    return DatabaseHealth(status="unavailable", connected=False, journal_mode=None)


def collect_database_health(resources: DatabaseResources | None) -> DatabaseHealth:
    """Collect read-only database health from existing application resources."""
    if resources is None:
        return unavailable_database_health()

    try:
        with resources.engine.connect() as connection:
            connected = connection.exec_driver_sql("SELECT 1").scalar_one() == 1
            journal_mode = str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()).lower()
    except Exception:
        return unavailable_database_health()

    if connected and journal_mode == "wal":
        return DatabaseHealth(status="ok", connected=True, journal_mode="wal")
    return unavailable_database_health()


def collect_scheduler_health(scheduler: BackgroundScheduler | None) -> SchedulerHealth:
    """Collect read-only scheduler health from an existing scheduler."""
    timezone = cast(SchedulerTimezone, str(SCHEDULER_TIMEZONE))
    if scheduler is None:
        return SchedulerHealth(status="unavailable", running=False, job_count=0, timezone=timezone)

    try:
        running = scheduler.running
        job_count = len(scheduler.get_jobs())
    except Exception:
        return SchedulerHealth(status="unavailable", running=False, job_count=0, timezone=timezone)

    if running:
        return SchedulerHealth(status="ok", running=True, job_count=job_count, timezone=timezone)
    return SchedulerHealth(status="unavailable", running=False, job_count=0, timezone=timezone)


def safe_default_settings() -> ApplicationSettings:
    return ApplicationSettings.model_construct(
        environment="local",
        app_title="XIANYU",
        app_version="0.1.0",
        debug=False,
        log_level="INFO",
        database_path=Path("data/xianyu.db"),
    )


def collect_health(app: FastAPI) -> HealthResponse:
    """Aggregate safe local Core health without creating infrastructure."""
    settings = getattr(app.state, "settings", None)
    if not isinstance(settings, ApplicationSettings):
        settings = safe_default_settings()

    database = collect_database_health(cast(DatabaseResources | None, getattr(app.state, "database", None)))
    scheduler = collect_scheduler_health(getattr(app.state, "scheduler", None))
    status: OverallHealthStatus = (
        "ok" if database.status == "ok" and scheduler.status == "ok" else "degraded"
    )
    return HealthResponse(
        status=status,
        service=settings.app_title,
        version=settings.app_version,
        environment=settings.environment,
        database=database,
        scheduler=scheduler,
    )


router = APIRouter()


@router.get(
    HEALTH_PATH,
    response_model=HealthResponse,
    status_code=200,
    tags=["health"],
    summary="Get Core health",
    description="Report read-only local Core health without external service checks.",
    operation_id="get_health",
    response_description="Core infrastructure is healthy.",
    responses={
        503: {
            "model": HealthResponse,
            "description": "One or more local Core components are unavailable.",
        }
    },
)
def get_health(request: Request, response: Response) -> HealthResponse:
    health = collect_health(request.app)
    if health.status == "degraded":
        response.status_code = 503
    return health


__all__ = [
    "HEALTH_PATH",
    "DatabaseHealth",
    "SchedulerHealth",
    "HealthResponse",
    "collect_database_health",
    "collect_scheduler_health",
    "collect_health",
    "router",
]
