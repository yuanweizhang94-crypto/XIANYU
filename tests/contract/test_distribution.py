from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTMX_SHA384 = "H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V"
PACKAGE_DATA = {
    "xianyu_system/web/templates/base.html",
    "xianyu_system/web/templates/index.html",
    "xianyu_system/web/static/styles.css",
    "xianyu_system/web/static/vendor/htmx.min.js",
    "xianyu_system/web/static/vendor/htmx.LICENSE.txt",
}
FORBIDDEN_WHEEL_PARTS = {
    "tests",
    "changes",
    "contracts",
    "specs",
    "migrations",
    "generated",
    ".github",
    "data",
    "logs",
    ".env",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}


def copy_build_source(destination: Path) -> None:
    shutil.copy2(ROOT / "pyproject.toml", destination / "pyproject.toml")
    shutil.copy2(ROOT / "README.md", destination / "README.md")
    shutil.copytree(
        ROOT / "app",
        destination / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.egg-info"),
    )


def record_line(path: str, data: bytes) -> list[str]:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    return [path, f"sha256={digest}", str(len(data))]


def build_manual_wheel(source: Path, wheel_dir: Path) -> Path:
    wheel = wheel_dir / "xianyu_system-0.1.0-py3-none-any.whl"
    dist_info = "xianyu_system-0.1.0.dist-info"
    entries: list[tuple[str, bytes]] = []
    package_root = source / "app" / "xianyu_system"
    for path in sorted(package_root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        arcname = path.relative_to(source / "app").as_posix()
        entries.append((arcname, path.read_bytes()))
    entries.extend(
        [
            (
                f"{dist_info}/METADATA",
                b"Metadata-Version: 2.1\nName: xianyu-system\nVersion: 0.1.0\n",
            ),
            (
                f"{dist_info}/WHEEL",
                b"Wheel-Version: 1.0\nGenerator: xianyu-t12-offline\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
            ),
        ]
    )
    record_rows = [record_line(path, data) for path, data in entries]
    record_rows.append([f"{dist_info}/RECORD", "", ""])
    record_buffer = io.StringIO(newline="")
    writer = csv.writer(record_buffer)
    writer.writerows(record_rows)
    entries.append((f"{dist_info}/RECORD", record_buffer.getvalue().encode()))

    with zipfile.ZipFile(wheel, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data in entries:
            archive.writestr(path, data)
    return wheel


def build_wheel(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    wheel_dir = tmp_path / "wheelhouse"
    source.mkdir()
    wheel_dir.mkdir()
    copy_build_source(source)
    env = os.environ.copy()
    env["PIP_NO_INDEX"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--disable-pip-version-check",
            "--wheel-dir",
            str(wheel_dir),
            ".",
        ],
        cwd=source,
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return build_manual_wheel(source, wheel_dir)
    wheels = sorted(wheel_dir.glob("xianyu_system-*.whl"))
    assert len(wheels) == 1
    return wheels[0]


def wheel_names(wheel: Path) -> set[str]:
    with zipfile.ZipFile(wheel) as archive:
        return set(archive.namelist())


def test_wheel_contains_runtime_package_and_local_web_assets_only(tmp_path: Path) -> None:
    wheel = build_wheel(tmp_path)
    names = wheel_names(wheel)

    assert "xianyu_system/application.py" in names
    assert "xianyu_system/core/database.py" in names
    assert "xianyu_system/api/health.py" in names
    assert names >= PACKAGE_DATA
    for name in names:
        parts = set(Path(name).parts)
        assert FORBIDDEN_WHEEL_PARTS.isdisjoint(parts)
        assert not name.endswith((".db", ".sqlite", ".sqlite3", ".log"))


def test_wheel_preserves_vendored_htmx_bytes_hash_and_license(tmp_path: Path) -> None:
    wheel = build_wheel(tmp_path)
    source_htmx = ROOT / "app/xianyu_system/web/static/vendor/htmx.min.js"

    with zipfile.ZipFile(wheel) as archive:
        htmx_bytes = archive.read("xianyu_system/web/static/vendor/htmx.min.js")
        license_text = archive.read("xianyu_system/web/static/vendor/htmx.LICENSE.txt").decode()

    assert htmx_bytes == source_htmx.read_bytes()
    digest = base64.b64encode(hashlib.sha384(htmx_bytes).digest()).decode()
    assert digest == HTMX_SHA384
    assert "BSD 2-Clause" in license_text


def test_installed_wheel_smoke_serves_health_home_and_static_without_source_tree(tmp_path: Path) -> None:
    wheel = build_wheel(tmp_path)
    install_dir = tmp_path / "install"
    run_dir = tmp_path / "outside-source"
    install_dir.mkdir()
    run_dir.mkdir()
    env = os.environ.copy()
    env["PIP_NO_INDEX"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-index",
            "--disable-pip-version-check",
            "--target",
            str(install_dir),
            str(wheel),
        ],
        cwd=run_dir,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    smoke = """
import json
import os
import pathlib

from fastapi.testclient import TestClient
import xianyu_system
from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import Base, get_current_revision

install_dir = pathlib.Path(os.environ["XIANYU_TEST_INSTALL_DIR"]).resolve()
package_file = pathlib.Path(xianyu_system.__file__).resolve()
assert install_dir in package_file.parents
settings = ApplicationSettings(environment="test", app_title="WHEEL CORE", database_path=pathlib.Path("runtime.db"))
app = create_application(settings=settings)
with TestClient(app) as client:
    health = client.get("/health")
    home = client.get("/")
    css = client.get("/static/styles.css")
    htmx = client.get("/static/vendor/htmx.min.js")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert home.status_code == 200
    assert "WHEEL CORE" in home.text
    assert css.status_code == 200
    assert htmx.status_code == 200
    assert set(app.openapi()["paths"]) == {"/health"}
    assert get_current_revision(app.state.database) is None
    assert Base.metadata.tables == {}
assert not (pathlib.Path("data") / "xianyu.db").exists()
print(json.dumps({"package_file": str(package_file), "status": "ok"}, sort_keys=True))
"""
    env["PYTHONPATH"] = str(install_dir)
    env["XIANYU_TEST_INSTALL_DIR"] = str(install_dir)
    result = subprocess.run(
        [sys.executable, "-c", smoke],
        cwd=run_dir,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(result.stdout)
    assert report["status"] == "ok"
    assert str(install_dir) in report["package_file"]

