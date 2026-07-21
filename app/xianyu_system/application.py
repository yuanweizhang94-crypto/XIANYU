from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

APP_TITLE = "XIANYU"
APP_VERSION = "0.1.0"

LifespanHandler = Callable[[FastAPI], AbstractAsyncContextManager[None]]


@asynccontextmanager
async def application_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Default no-op lifespan extended by later approved tasks."""
    yield


def create_application(*, lifespan: LifespanHandler | None = None) -> FastAPI:
    """Create an isolated XIANYU FastAPI application instance."""
    return FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        lifespan=lifespan or application_lifespan,
    )
