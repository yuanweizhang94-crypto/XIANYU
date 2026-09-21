from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0040-qr-cookie-browser-lineage-enrichment.patch"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chg0040_acceptance_contract():
    patch = _text(PATCH)
    acceptance = _text(CHANGE / "acceptance.md")
    assert "cookie_renew_browser_service.renew(cookies, browser_account_id)" in patch
    assert "QR_COOKIE_BROWSER_ENRICHMENT_FAILED" in patch
    assert "DYNAMIC_SUCCESS_CASE=PASS" in acceptance
    assert "DYNAMIC_NEW_ACCOUNT_CANONICAL_COOKIE_PERSISTED=PASS" in acceptance
    assert "DYNAMIC_EXISTING_CANONICAL_PRESERVATION=PASS" in acceptance
    assert "DYNAMIC_CAS_EXPECTED_FINGERPRINT=PASS" in acceptance
    assert "DYNAMIC_FAIL_CLOSED_DB_COMMIT_COUNT=0" in acceptance


def test_chg0040_hard_expiry_requires_new_qr_lineage():
    proposal = _text(CHANGE / "proposal.md")
    acceptance = _text(CHANGE / "acceptance.md")
    assert "PLATFORM_SESSION_HARD_EXPIRED=true" in acceptance
    assert "HUMAN_QR_REQUIRED=true" in acceptance
    assert "qualified QR evidence correctly blocks blind renewal" in proposal
