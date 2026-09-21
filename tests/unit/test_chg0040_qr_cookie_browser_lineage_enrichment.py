from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0040-qr-cookie-browser-lineage-enrichment.patch"
CHANGE = ROOT / "changes/archive/CHG-0040-qr-cookie-browser-lineage-enrichment"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_scope_is_only_account_service():
    text = patch_text()
    assert text.count("diff --git ") == 1
    assert (
        "diff --git a/backend-web/app/services/account_service.py "
        "b/backend-web/app/services/account_service.py"
    ) in text
    assert "auto_reply_service.py" not in text
    assert "cookie_token_manager.py" not in text
    assert "xianyu_publisher.py" not in text


def test_qr_cookie_browser_enrichment_precedes_persistence():
    text = patch_text()
    assert "cookie_renew_browser_service.renew(cookies, browser_account_id)" in text
    assert "QR_COOKIE_BROWSER_ENRICHMENT_FAILED" in text
    assert "cookies = str(browser_result.new_cookies_str)" in text
    removed = [line for line in text.splitlines() if line.startswith("-") and not line.startswith("---")]
    assert removed == []


def test_existing_owners_are_reused_without_parallel_lifecycle():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    design = (CHANGE / "design.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "No new Session owner." in design
    assert "No new Cookie store." in design
    assert "No new Token owner." in design
    assert "validate_and_commit_authoritative_cookie_candidate" in design


def test_existing_canonical_fields_are_preserved_before_browser_enrichment():
    text = patch_text()
    assert "canonical_fields = trans_cookies(account.cookie)" in text
    assert "canonical_fields.update(trans_cookies(cookies))" in text
    assert text.index("canonical_fields.update(trans_cookies(cookies))") < text.index(
        "cookie_renew_browser_service.renew(cookies, browser_account_id)"
    )


def test_cas_generation_and_fail_closed_dynamic_evidence_is_recorded():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "DYNAMIC_CAS_EXPECTED_FINGERPRINT=PASS" in acceptance
    assert "DYNAMIC_EXISTING_CANONICAL_PRESERVATION=PASS" in acceptance
    assert "DYNAMIC_FAIL_CLOSED_DB_COMMIT_COUNT=0" in acceptance


def test_patch_has_no_background_enable_or_login_path():
    text = patch_text()
    assert text.count("diff --git ") == 1
    assert "AUTO_START" not in text
    assert "startup" not in text.lower()
    assert "account.status" not in text
    assert "qr_login_manager.generate_qr_code" not in text


def test_regression_contract_preserves_token_and_reconnect_semantics():
    design = (CHANGE / "design.md").read_text(encoding="utf-8")
    assert "Token refresh logic is untouched." in design
    assert "CHG0039 explicit invalidation logic remains active and independent." in design
    assert "Ordinary reconnect never forces login or Token refresh." in design
