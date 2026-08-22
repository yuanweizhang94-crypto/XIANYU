from hashlib import sha256
from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0023-readiness-owner-deltas.patch"
EVIDENCE = CHANGE / "evidence/20260823-runtime-acceptance-and-formal-persistence.md"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_is_locked_two_owner_artifact():
    raw = PATCH.read_bytes().replace(b"\r\n", b"\n")
    text = raw.decode("ascii")
    assert sha256(raw).hexdigest() == "e6808621fd86ade619dff2be622f9c419feca7436542ca004854210f266adc24"
    assert text.count("GIT binary patch") == 2
    assert text.count("diff --git ") == 2
    assert "diff --git a/backend-web/app/api/routes/cookies.py b/backend-web/app/api/routes/cookies.py" in text
    assert "diff --git a/websocket/app/services/xianyu/cookie_manager.py b/websocket/app/services/xianyu/cookie_manager.py" in text
    assert "index a4ed1c0ec5d2a5bad29ba69aefbad71d46d089c0..fbbfbd93aa5fbd97a6e11b00d4c756fb3853737b 100644" in text
    assert "index 13223958a1439bbafa6d7e1bc834f69e4580f304..76cfd2f200d6d1c23d48d74cd38cdc13dfff65a1 100644" in text


def test_patch_excludes_non_chg0023_owners():
    text = patch_text()
    forbidden = (
        "xianyu_async.py",
        "cookie_token_manager.py",
        "internal.py",
        "password_login.py",
        "account_cookie_service.py",
        "cookie_refresh.py",
        "xianyu_mtop.py",
        "chat_new.py",
        "im_session_manager.py",
        "im_client.py",
    )
    for marker in forbidden:
        assert marker not in text


def test_backend_authoritative_blockers_are_executable_acceptance_proven():
    text = EVIDENCE.read_text(encoding="utf-8")
    assert "BACKEND_SCOPE_VALID=true" in text
    assert "CHG0023_BACKEND_TARGETED=6/6_PASS" in text
    assert "QR_FALSE_GREEN_STATIC_COUNT=0" in text
    assert "authoritative platform-verification, HUMAN_QR/no-credentials, and expired-Session blockers before `connected + token_ready -> ONLINE`" in text


def test_websocket_existing_owner_producer_is_executable_acceptance_proven():
    text = EVIDENCE.read_text(encoding="utf-8")
    assert "WEBSOCKET_SCOPE_VALID=true" in text
    assert "TOKEN_READY_PRODUCER=3/3_PASS" in text
    assert "INTERNAL_ENDPOINT_PASSTHROUGH=PASS" in text
    assert '`token_ready=false` by default and `token_ready=bool(getattr(instance, "current_token", None))`' in text


def test_formal_evidence_records_provenance_and_runtime_acceptance():
    text = EVIDENCE.read_text(encoding="utf-8")
    required = (
        "RUNTIME_ACCEPTANCE=PASS",
        "CHG0022_PRODUCTION_DELTA_PROVENANCE=PASS",
        "BACKEND_PREIMAGE_CORRECTION=PASS",
        "CUMULATIVE_SCOPE_EXPANSION=false",
        "UNEXPLAINED_NON_CHG0023_DELTA=false",
        "ATTEMPT_1_EVIDENCE_PRESERVED=true",
        "ATTEMPT_2_EVIDENCE_RECORDED=true",
        "QR_FALSE_GREEN_COUNT=0",
    )
    for marker in required:
        assert marker in text
