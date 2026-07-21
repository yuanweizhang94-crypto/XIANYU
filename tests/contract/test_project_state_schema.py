from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from scripts.generate_state import build_project_state

ROOT = Path(__file__).resolve().parents[2]


def test_project_state_conforms_to_schema() -> None:
    state = build_project_state(ROOT)
    schema = json.loads((ROOT / "contracts" / "schemas" / "project-state.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(state, schema)
