from pathlib import Path


CHANGE_ID = "CHG-0034-fixed-target-browser-ui"
ROOT = Path(__file__).resolve().parents[4]


def _change_dir() -> Path:
    for base in (ROOT / "changes" / "active", ROOT / "changes" / "archive"):
        candidate = base / CHANGE_ID
        if candidate.exists():
            return candidate
    raise AssertionError(f"{CHANGE_ID} not found")


CHANGE_DIR = _change_dir()


def test_chg0034_zero_action_gates_are_recorded() -> None:
    acceptance = (CHANGE_DIR / "acceptance.md").read_text(encoding="utf-8")

    for marker in (
        "`BROWSER_INVOCATIONS=0`",
        "`PLATFORM_ACTION_INVOCATIONS=0`",
        "`DEPLOY_INVOCATIONS=0`",
        "`COMMIT_INVOCATIONS=0`",
        "`PUSH_INVOCATIONS=0`",
        "`PRODUCTION_MUTATION_COUNT=0`",
        "`SECRET_VALUE_PRINTED=false`",
    ):
        assert marker in acceptance


def test_chg0034_fixed_target_and_required_pages_are_recorded() -> None:
    acceptance = (CHANGE_DIR / "acceptance.md").read_text(encoding="utf-8")

    assert "`FIXED_TARGET_URL=http://127.0.0.1:19000/`" in acceptance
    for route in ("/", "/accounts", "/items", "/chat", "/ai-reply", "/service"):
        assert route in acceptance


def test_chg0034_reuse_decision_is_operations_wrapper() -> None:
    proposal = (CHANGE_DIR / "proposal.md").read_text(encoding="utf-8")

    assert "Decision: WRAP_FOR_OPERATIONS" in proposal
    assert "does not create a new frontend" in proposal


def test_chg0034_readiness_checkpoint_records_runtime_facts() -> None:
    evidence = (CHANGE_DIR / "evidence" / "20260825-readiness-checkpoint.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        "FIXED_TARGET_HEAD_STATUS=200",
        "FIXED_TARGET_CACHE_CONTROL=no-store, must-revalidate, no-cache",
        "SAME_ORIGIN_HEALTH_STATUS=200",
        "DIRECT_WEBSOCKET_HEALTH_STATUS=200",
        "RUNTIME_CHAT_CHUNK_CONTAINS_WS=true",
        "AUTH_SYNC_PATH=/internal/xianyu-auth-sync",
        "PRE_BROWSER_CODE_PATCH_NEEDED=false",
        "PRE_BROWSER_DEPLOY_NEEDED=false",
    ):
        assert marker in evidence


def test_chg0034_readiness_checkpoint_preserves_zero_action_scope() -> None:
    evidence = (CHANGE_DIR / "evidence" / "20260825-readiness-checkpoint.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        "BROWSER_INVOCATIONS=0",
        "PLATFORM_ACTION_INVOCATIONS=0",
        "DEPLOY_INVOCATIONS=0",
        "COMMIT_INVOCATIONS=0",
        "PUSH_INVOCATIONS=0",
        "PRODUCTION_MUTATION_COUNT=0",
        "SECRET_VALUES_WRITTEN_TO_CHANGE_FILES=false",
    ):
        assert marker in evidence
