from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0037-opencv-headless-runtime-dependency.patch"
README = ROOT / "vendor/patches/xianyu-auto-reply/README.md"
CHANGE = ROOT / "changes/active/CHG-0037-opencv-headless-runtime-dependency"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_dependency_patch_is_single_file_and_exact_pin() -> None:
    text = _text(PATCH)
    assert text.count("diff --git ") == 1
    assert "diff --git a/backend-web/pyproject.toml b/backend-web/pyproject.toml" in text
    assert '-    "opencv-python-headless>=4.10.0",' in text
    assert '+    "opencv-python-headless==5.0.0.93",' in text
    assert '+    "opencv-python' not in text.replace(
        '+    "opencv-python-headless==5.0.0.93",', ""
    )


def test_dependency_patch_does_not_touch_business_runtime_files() -> None:
    text = _text(PATCH)
    forbidden = (
        "publish_execution_service.py",
        "xianyu_personal_publisher.py",
        "xianyu_direct_publisher.py",
        "xianyu_publish_service.py",
        "cookies.py",
        "ProductMaterial",
        "frontend/",
        "websocket/",
        "scheduler/",
    )
    for marker in forbidden:
        assert marker not in text


def test_vendor_registry_records_real_dependency_authority() -> None:
    text = _text(README)
    assert "## CHG-0037 OpenCV headless Runtime dependency persistence" in text
    assert "backend-web/pyproject.toml" in text
    assert "backend-web/Dockerfile" in text
    assert "opencv-python-headless==5.0.0.93" in text
    assert "cv2==5.0.0" in text


def test_change_contract_keeps_zero_platform_write_boundary() -> None:
    proposal = _text(CHANGE / "proposal.md")
    design = _text(CHANGE / "design.md")
    acceptance = _text(CHANGE / "acceptance.md")
    combined = "\n".join((proposal, design, acceptance))
    assert "BUSINESS_SOURCE_LOGIC_CHANGED=false" in proposal
    assert "PLATFORM_WRITE_GUARD_ACTIVE=true" in design
    assert "REAL_PUBLISH_HTTP_REQUEST_COUNT=0" in combined
    assert "REAL_ITEM_CREATE_COUNT=0" in combined
    assert "REAL_XIANYU_PUBLISH_EXECUTED=false" in acceptance


def test_change_records_existing_dependency_owner_not_duplicate_owner() -> None:
    design = _text(CHANGE / "design.md")
    assert (
        "CURRENT_BACKEND_DEPENDENCY_AUTHORITY=upstream backend-web/pyproject.toml "
        "consumed by upstream backend-web/Dockerfile"
    ) in design
    assert "Decision: PATCH_UPSTREAM" in design
