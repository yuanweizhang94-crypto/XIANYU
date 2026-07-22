from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from xianyu_system.core.config import ApplicationSettings

LifespanHandler = Callable[[FastAPI], AbstractAsyncContextManager[None]]


@asynccontextmanager
async def application_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Default no-op lifespan extended by later approved tasks."""
    yield


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
        lifespan=lifespan or application_lifespan,
    )
    app.state.settings = resolved_settings
    return app
