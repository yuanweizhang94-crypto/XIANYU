from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.logging import configure_logging, shutdown_logging

LifespanHandler = Callable[[FastAPI], AbstractAsyncContextManager[None]]


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Configure per-application logging for the FastAPI lifespan."""
    settings = app.state.settings
    logger_name = f"xianyu.application.{id(app)}"
    logger = configure_logging(level=settings.log_level, logger_name=logger_name)
    app.state.logger = logger
    logger.info(
        "Application startup",
        extra={"event": "application.startup", "environment": settings.environment},
    )
    try:
        yield
    finally:
        logger.info(
            "Application shutdown",
            extra={"event": "application.shutdown", "environment": settings.environment},
        )
        shutdown_logging(logger)


def compose_lifespan(custom_lifespan: LifespanHandler | None) -> LifespanHandler:
    """Compose project-managed logging lifespan with an optional caller lifespan."""

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
    return app
