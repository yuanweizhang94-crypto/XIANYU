from __future__ import annotations

from pathlib import Path
from typing import cast

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from xianyu_system.api.health import HEALTH_PATH
from xianyu_system.core.config import ApplicationSettings

WEB_PACKAGE_PATH = Path(__file__).resolve().parent
TEMPLATES_PATH = WEB_PACKAGE_PATH / "templates"
STATIC_PATH = WEB_PACKAGE_PATH / "static"

HOME_PATH = "/"
STATIC_URL_PATH = "/static"
STATIC_ROUTE_NAME = "static"
HOME_ROUTE_NAME = "home"

router = APIRouter()


def create_templates() -> Jinja2Templates:
    """Create one Jinja2 template environment for one application instance."""
    return Jinja2Templates(directory=str(TEMPLATES_PATH))


@router.get(
    HOME_PATH,
    response_class=HTMLResponse,
    include_in_schema=False,
    name=HOME_ROUTE_NAME,
)
def get_home(request: Request) -> Response:
    settings = cast(ApplicationSettings, request.app.state.settings)
    templates = cast(Jinja2Templates, request.app.state.web_templates)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "service": settings.app_title,
            "version": settings.app_version,
            "environment": settings.environment,
            "health_path": HEALTH_PATH,
        },
    )


def register_web(app: FastAPI) -> None:
    """Register one isolated web boundary on one application instance."""
    templates = create_templates()
    app.state.web_templates = templates

    app.mount(
        STATIC_URL_PATH,
        StaticFiles(
            directory=str(STATIC_PATH),
            html=False,
            check_dir=True,
            follow_symlink=False,
        ),
        name=STATIC_ROUTE_NAME,
    )
    app.include_router(router)


__all__ = [
    "HOME_PATH",
    "HOME_ROUTE_NAME",
    "STATIC_PATH",
    "STATIC_ROUTE_NAME",
    "STATIC_URL_PATH",
    "TEMPLATES_PATH",
    "WEB_PACKAGE_PATH",
    "create_templates",
    "get_home",
    "register_web",
    "router",
]
