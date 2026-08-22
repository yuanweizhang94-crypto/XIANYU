from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
PROPOSAL = CHANGE / "proposal.md"
DESIGN = CHANGE / "design.md"
ACCEPTANCE = CHANGE / "acceptance.md"
EVIDENCE = CHANGE / "evidence/20260823-item-sync-no-auth-recovery-capability-audit.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_existing_owner_only_and_reuse_decision_are_locked():
    proposal = read(PROPOSAL)
    design = read(DESIGN)
    assert "CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`" in proposal
    assert "REUSE_DECISION=PATCH_EXISTING_OWNER" in proposal
    assert "EXISTING_OWNER_ONLY=true" in design
    assert "NO_DUPLICATE_OWNER=true" in design


def test_both_auth_recovery_callsites_are_locked():
    proposal = read(PROPOSAL)
    evidence = read(EVIDENCE)
    for text in (proposal, evidence):
        assert "AUTH_RECOVERY_CALLSITE_COUNT=2" in text
        assert "CALLSITE_1=FIRST_PAGE_CATALOG_FAILURE" in text
        assert "CALLSITE_2=MISSING_ITEM_AUTHORITATIVE_RECONCILIATION" in text


def test_default_and_public_caller_contract_are_locked():
    design = read(DESIGN)
    acceptance = read(ACCEPTANCE)
    assert "DEFAULT_BEHAVIOR_PRESERVED=true" in design
    assert "PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false" in design
    assert "DEFAULT_BEHAVIOR_PRESERVED=true" in acceptance
    assert "PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false" in acceptance


def test_remote_listing_mutation_and_unknown_retry_are_forbidden():
    proposal = read(PROPOSAL)
    acceptance = read(ACCEPTANCE)
    assert "REMOTE_LISTING_MUTATION_FORBIDDEN=true" in proposal
    assert "UNKNOWN_NEVER_BLIND_RETRY=true" in proposal
    assert "REMOTE_LISTING_MUTATION_FORBIDDEN=true" in acceptance
    assert "UNKNOWN_NEVER_BLIND_RETRY=true" in acceptance


def test_bootstrap_does_not_claim_runtime_implementation():
    acceptance = read(ACCEPTANCE)
    evidence = read(EVIDENCE)
    assert "RUNTIME_SOURCE_CHANGED=false" in acceptance
    assert "COMPANY_RUNTIME_SOURCE_CHANGED=false" in acceptance
    assert "ITEM_SYNC_INVOCATION_COUNT=0" in evidence
    assert "REMOTE_ITEM_READ_COUNT=0" in evidence
    assert "SESSION_MAINTAIN_CALL_COUNT=0" in evidence
    assert "PRODUCTION_CONTAINER_MUTATION_COUNT=0" in evidence
