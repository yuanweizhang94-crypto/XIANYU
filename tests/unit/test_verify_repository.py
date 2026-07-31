from __future__ import annotations

from pathlib import Path

import yaml

from scripts.security_scan import scan as security_scan
from scripts.verify_repository import check_openapi


def test_generic_openapi_allows_non_empty_paths(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "contracts").mkdir(parents=True)
    openapi = {
        "openapi": "3.1.0",
        "info": {"title": "Temporary API", "version": "0.1.0"},
        "paths": {"/health": {}},
    }
    (root / "contracts" / "openapi.yaml").write_text(
        yaml.safe_dump(openapi, sort_keys=False), encoding="utf-8"
    )

    check_openapi(root)


def test_security_scan_ignores_local_runtime_directory(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    local_file = root / ".local" / "chg0017-apply-check" / "config.py"
    local_file.parent.mkdir(parents=True)
    local_file.write_text(("pass" "word = ") + "super-secret-runtime-copy", encoding="utf-8")

    assert security_scan(root) == []
