from __future__ import annotations

from pathlib import Path

import yaml

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
