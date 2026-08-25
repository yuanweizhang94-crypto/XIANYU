import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
EVIDENCE = CHANGE / "evidence/20260825-phase1-read-only-gates.md"
PHASE2B_EVIDENCE = CHANGE / "evidence/20260825-phase2b-acceptance-grade-repair.md"
PHASE3_EVIDENCE = CHANGE / "evidence/20260825-phase3-pre-pr-implementation-closure.md"
REQUIRED_DOCS = ("proposal.md", "design.md", "tasks.md", "acceptance.md")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_required_docs_have_consistent_identity_and_status():
    expected = "Change ID: CHG-0030-fresh-item-sync-controlled-canary"
    for name in REQUIRED_DOCS:
        text = _text(CHANGE / name)
        assert expected in text
        assert "Status: IMPLEMENTING" in text


def test_execution_contract_and_no_go_decision_are_locked():
    proposal = _text(CHANGE / "proposal.md")
    acceptance = _text(CHANGE / "acceptance.md")
    evidence = _text(EVIDENCE)
    for marker in (
        "User outcome: one controlled Fresh Item Sync canary",
        "Confirmed blocker: selected capability and trace identity are not yet explicit",
        "Smallest success test: one selected eligible account",
        "PRODUCTION_ITEM_SYNC_CANARY_GO=false",
        "ITEM_SYNC_INVOCATION_ALLOWED=false",
    ):
        assert marker in proposal or marker in acceptance or marker in evidence


def test_existing_owner_is_adopted_without_second_item_sync_owner():
    proposal = _text(CHANGE / "proposal.md")
    evidence = _text(EVIDENCE)
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "UPSTREAM_OWNER=`ItemService.fetch_all_items_from_account`" in evidence
    assert "NEW_ITEM_SYNC_OWNER_CREATED=false" in evidence
    assert "MANUAL_REMOTE_READ_PLUS_DB_UPSERT_BYPASS_CREATED=false" in evidence
    assert "SINGLE_PAGE_PRIMITIVE_USED_AS_OWNER=false" in evidence


def test_company_adapter_trace_identity_gate_is_red():
    evidence = _text(EVIDENCE)
    phase2b = _text(PHASE2B_EVIDENCE)
    for marker in (
        "LIVE_SCHEMA_FIELDS=`account_id,page_size,max_pages`",
        "LIVE_SCHEMA_TASK_ID_FIELD_PRESENT=false",
        "LIVE_SCHEMA_REQUEST_ID_FIELD_PRESENT=false",
        "LIVE_SCHEMA_TRACE_ID_FIELD_PRESENT=false",
        "LIVE_SCHEMA_OPERATION_ID_FIELD_PRESENT=false",
        "TRACKABLE_SYNC_STATUS_TOOL_FOUND=false",
        "TRACKABLE_ITEM_SYNC_OPERATION_LEDGER_FOUND=false",
        "TRACE_IDENTITY_AVAILABLE=PATCH_ARTIFACT_AVAILABLE_NOT_DEPLOYED",
        "TRACE_IDENTITY_GATE=BACKEND_CONTRACT_PATCHED_NOT_DEPLOYED_ADAPTER_NOT_PASSTHROUGH",
    ):
        assert marker in evidence
    for marker in (
        "TRACE_IDENTITY_AVAILABLE=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED",
        "LOG_EVENT_ACCEPTED=CHG0030_ITEM_SYNC_OPERATION_ACCEPTED",
        "LOG_EVENT_TERMINAL=CHG0030_ITEM_SYNC_TERMINAL_READBACK",
        "CURRENT_COMPANY_ADAPTER_PASSTHROUGH_READY=false",
        "BACKEND_LOG_OBSERVABILITY_PATCH_READY=true",
    ):
        assert marker in phase2b


def test_selected_account_item_sync_eligibility_gate_is_red_without_invocation():
    evidence = _text(EVIDENCE)
    phase2b = _text(PHASE2B_EVIDENCE)
    for marker in (
        "CURRENT_READ_ONLY_ACCOUNT_TOOL=`xianyu_account_status`",
        "ACCOUNT_STATUS_READ_ONLY=true",
        "ACCOUNT_STATUS_ITEM_SYNC_ELIGIBILITY_FIELD_PRESENT=false",
        "ACCOUNT_STATUS_DOES_NOT_PROVE_ITEM_SYNC_SELECTED_ACCOUNT_ELIGIBLE=true",
        "SELECTED_ACCOUNT_MASKED=`22*********60`",
        "SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PATCH_ARTIFACT_AVAILABLE_NOT_DEPLOYED",
        "SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY_GATE=BACKEND_CONTRACT_PATCHED_NOT_DEPLOYED_ADAPTER_NOT_PASSTHROUGH",
    ):
        assert marker in evidence
    for marker in (
        "SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED",
        "ELIGIBILITY_FACT_DISABLED=authoritative",
        "ELIGIBILITY_FACT_CHECKING=authoritative",
        "ELIGIBILITY_FACT_PLATFORM_VERIFICATION=authoritative",
        "ELIGIBILITY_FACT_SESSION_COOKIE_LINEAGE=authoritative",
        "ELIGIBILITY_FACT_TOKEN_READY=authoritative",
        "ELIGIBILITY_UNKNOWN_FAILS_CLOSED=true",
    ):
        assert marker in phase2b


def test_phase2b_patch_uses_real_durable_readback_and_clean_runtime_replay():
    phase2b = _text(PHASE2B_EVIDENCE)
    for marker in (
        "DURABLE_READBACK_SOURCE=xy_catalog_items",
        "DURABLE_READBACK_QUERY_ACTUAL_DB=true",
        "DUPLICATE_COUNT_MEASURED=true",
        "DUPLICATE_COUNT_HARD_CODED=false",
        "UNKNOWN_QUERY_FAILURE_TERMINAL=true",
        "RETRY_ALLOWED_ON_UNKNOWN=false",
        "CLEAN_APPLY_BASE_SHA=8c2723e552bb9f797c73b6c497858bc314549877",
        "PATCH_ARTIFACT_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201",
        "PATCH_REPLAY_APPLY_CHECK_EXIT=0",
        "PATCH_REPLAY_PYTEST=15 passed",
    ):
        assert marker in phase2b


def test_phase3_governance_and_patch_lock_are_recorded():
    phase3 = _text(PHASE3_EVIDENCE)
    readme = _text(ROOT / "vendor/patches/xianyu-auto-reply/README.md")
    for marker in (
        "IMPLEMENTING_CHANGE_ALL_TASKS_COMPLETE=false",
        "PATCH_ARTIFACT_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201",
        "PATCH_ARTIFACT_LOCKED=true",
        "ITEM_SERVICE_RESULT_KEYS=success,message,items,total_count,total_pages,page_size,saved_count,full_active_list_confirmed,platform_status_reconciliation",
        "RUNTIME_UNIQUE_KEY=uk_cat_account_item(account_id,item_id)",
        "ROLLBACK_DB_MIGRATION_REQUIRED=false",
        "DEPLOYMENT_REQUIRED_BEFORE_PREFLIGHT_PASS=true",
    ):
        assert marker in phase3
    assert "## CHG-0030 controlled Fresh Item Sync canary patch" in readme
    assert "SHA256: `595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`" in readme


def test_forbidden_side_effect_counters_remain_zero():
    acceptance = _text(CHANGE / "acceptance.md")
    for marker in (
        "ITEM_SYNC_INVOCATION_COUNT=0",
        "REMOTE_ITEM_READ_COUNT=0",
        "LOCAL_ITEM_WRITE_COUNT=0",
        "REMOTE_LISTING_CREATE_COUNT=0",
        "REMOTE_LISTING_EDIT_COUNT=0",
        "REMOTE_LISTING_OFFLINE_COUNT=0",
        "REMOTE_LISTING_DELETE_COUNT=0",
        "REAL_PRODUCTS_PUBLISHED=0",
        "REAL_PRODUCTS_MODIFIED=0",
        "REAL_MESSAGES_SENT=0",
        "BROWSER_INVOCATION_COUNT=0",
        "PLAYWRIGHT_CDP_INVOCATION_COUNT=0",
        "QR_LOGIN_INVOCATION_COUNT=0",
        "MANUAL_RECONNECT_INVOCATION_COUNT=0",
        "PRODUCTION_ACCOUNT_MUTATION_COUNT=0",
        "PRODUCTION_CONFIG_CHANGE_COUNT=0",
        "PRODUCTION_RESTART_COUNT=0",
        "DIRTY_CHG0018_TOUCHED=0",
    ):
        assert marker in acceptance


def test_generated_project_state_reports_active_chg0030():
    state = json.loads((ROOT / "generated/PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"]["id"] == "CHG-0030-fresh-item-sync-controlled-canary"
    assert state["active_change"]["status"] == "IMPLEMENTING"
    assert state["tasks"]["total"] == 18
    assert state["tasks"]["completed"] < state["tasks"]["total"]
    assert state["tasks"]["next_task"]
