from __future__ import annotations

from fastapi import APIRouter

from xianyu_system.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)

__all__ = ["api_router"]
