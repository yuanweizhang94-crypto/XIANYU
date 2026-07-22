from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from xianyu_system.api.router import api_router
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import dispose_database, initialize_database
from xianyu_system.core.logging import configure_logging, shutdown_logging
from xianyu_system.core.scheduler import (
    SCHEDULER_TIMEZONE,
    create_scheduler,
    shutdown_scheduler,
    start_scheduler,
)

LifespanHandler = Callable[[FastAPI], AbstractAsyncContextManager[None]]


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Configure per-application infrastructure for the FastAPI lifespan."""
    settings = app.state.settings
    logger_name = f"xianyu.application.{id(app)}"
    logger = configure_logging(level=settings.log_level, logger_name=logger_name)
    app.state.logger = logger
    database = None
    scheduler = None
    logger.info(
        "Application startup",
        extra={"event": "application.startup", "environment": settings.environment},
    )
    try:
        database = initialize_database(settings.database_path)
        app.state.database = database
        logger.info(
            "Database ready",
            extra={"event": "database.ready", "journal_mode": "wal"},
        )

        try:
            scheduler = create_scheduler(logger=logger)
            start_scheduler(scheduler)
            app.state.scheduler = scheduler
            logger.info(
                "Scheduler ready",
                extra={
                    "event": "scheduler.ready",
                    "running": scheduler.running,
                    "job_count": len(scheduler.get_jobs()),
                    "timezone": str(SCHEDULER_TIMEZONE),
                },
            )
            try:
                yield
            finally:
                shutdown_error: BaseException | None = None
                if scheduler is not None:
                    try:
                        shutdown_scheduler(scheduler)
                    except Exception as exc:
                        shutdown_error = exc
                app.state.scheduler = None
                logger.info(
                    "Scheduler shutdown",
                    extra={
                        "event": "scheduler.shutdown",
                        "running": False,
                        "job_count": 0,
                    },
                )
                if shutdown_error is not None:
                    raise shutdown_error
        except Exception:
            active_scheduler = getattr(app.state, "scheduler", None)
            app.state.scheduler = None
            if scheduler is not None and active_scheduler is scheduler:
                shutdown_scheduler(scheduler)
            raise
        finally:
            logger.info("Database shutdown", extra={"event": "database.shutdown"})
            if database is not None:
                dispose_database(database)
            app.state.database = None
    finally:
        if database is None:
            app.state.database = None
        if scheduler is None:
            app.state.scheduler = None
        logger.info(
            "Application shutdown",
            extra={"event": "application.shutdown", "environment": settings.environment},
        )
        shutdown_logging(logger)


def compose_lifespan(custom_lifespan: LifespanHandler | None) -> LifespanHandler:
    """Compose project-managed infrastructure with an optional caller lifespan."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        async with application_lifespan(app):
            if custom_lifespan is None:
                yield
            else:
                async with custom_lifespan(app):
                    yield

    return lifespan


def create_application(
    *,
    lifespan: LifespanHandler | None = None,
    settings: ApplicationSettings | None = None,
) -> FastAPI:
    """Create an isolated XIANYU FastAPI application instance."""
    resolved_settings = settings if settings is not None else ApplicationSettings()

    app = FastAPI(
        title=resolved_settings.app_title,
        version=resolved_settings.app_version,
        debug=resolved_settings.debug,
        lifespan=compose_lifespan(lifespan),
    )
    app.state.settings = resolved_settings
    app.include_router(api_router)
    return app
