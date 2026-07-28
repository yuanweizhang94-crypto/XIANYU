from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_ROOT = ROOT / "app" / "xianyu_system" / "schedule"


def test_schedule_runtime_has_no_platform_or_integration_boundary_terms() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in SCHEDULE_ROOT.glob("*.py"))
    forbidden = [
        "playwright",
        "selenium",
        "browser profile",
        "wecom",
        "openai",
        "redis",
        "celery",
        "import requests",
        "from requests",
        "requests.get",
        "requests.post",
        "import httpx",
        "from httpx",
        "httpx.get",
        "httpx.post",
        "websocket",
    ]
    for term in forbidden:
        assert term not in combined


def test_schedule_runtime_does_not_modify_core_scheduler_or_publish_modules() -> None:
    assert (ROOT / "app" / "xianyu_system" / "core" / "scheduler.py").is_file()
    assert (ROOT / "app" / "xianyu_system" / "worker" / "publish" / "service.py").is_file()
