from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

BASE_SHA256 = "4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1"
FIXED_SHA256 = "326750c9383b392e58f6f864906359d2c7b2f6377519d698adf46852ca2c1d6e"
RETRY_COOLDOWN_MS = 15_000

OLD_REF = "autoChatOnce=n.useRef(new Set)"
NEW_REF = "autoChatRetryAt=n.useRef(new Map)"

OLD_EFFECT = 'n.useEffect(()=>{for(const e of l)e.connected||e.status!=="active"||e.runtime_connected||e.connection_state!=="connected"||!e.token_ready||["LOGIN_REQUIRED","PLATFORM_VERIFICATION_REQUIRED","SESSION_EXPIRED"].includes(e.chat_state||"")||autoChatOnce.current.has(e.account_id)||w.current.has(e.account_id)||(autoChatOnce.current.add(e.account_id),ys(e.account_id))},[l]);'

NEW_EFFECT = 'n.useEffect(()=>{const e=Date.now();for(const t of l){if(t.connected||t.status!=="active"||t.runtime_connected||t.connection_state!=="connected"||!t.token_ready||["LOGIN_REQUIRED","PLATFORM_VERIFICATION_REQUIRED","SESSION_EXPIRED"].includes(t.chat_state||"")||w.current.has(t.account_id))continue;const c=autoChatRetryAt.current.get(t.account_id)||0;e-c<15e3||(autoChatRetryAt.current.set(t.account_id,e),w.current.add(t.account_id),At(t.account_id).catch(()=>{}).finally(()=>{w.current.delete(t.account_id),J(1,!0)}))}},[l,J]);'

REQUIRED_SPINNER_FIX = "normalizeChatAccounts"
REQUIRED_CACHE_FIX = "Pe.current[e]={convs:y,hasMore:g.hasMore,cursor:g.nextCursor},T(y)"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def should_auto_connect(
    account: dict[str, Any],
    *,
    last_attempt_ms: int = 0,
    now_ms: int,
    inflight: bool = False,
) -> bool:
    if account.get("connected"):
        return False
    if account.get("status") != "active":
        return False
    if account.get("runtime_connected"):
        return False
    if account.get("connection_state") != "connected":
        return False
    if not account.get("token_ready"):
        return False
    if str(account.get("chat_state") or "") in {
        "LOGIN_REQUIRED",
        "PLATFORM_VERIFICATION_REQUIRED",
        "SESSION_EXPIRED",
    }:
        return False
    if inflight:
        return False
    return now_ms - last_attempt_ms >= RETRY_COOLDOWN_MS


def transform_text(text: str) -> str:
    if REQUIRED_SPINNER_FIX not in text:
        raise ValueError("required spinner-convergence fix is missing")
    if REQUIRED_CACHE_FIX not in text:
        raise ValueError("required account-cache convergence fix is missing")
    if text.count(OLD_REF) != 1:
        raise ValueError(f"expected one autoChatOnce preimage, found {text.count(OLD_REF)}")
    if text.count(OLD_EFFECT) != 1:
        raise ValueError(f"expected one auto-connect effect preimage, found {text.count(OLD_EFFECT)}")
    return text.replace(OLD_REF, NEW_REF, 1).replace(OLD_EFFECT, NEW_EFFECT, 1)


def patch_bytes(data: bytes) -> bytes:
    if sha256_bytes(data) != BASE_SHA256:
        raise ValueError("input chunk SHA256 does not match locked production preimage")
    fixed = transform_text(data.decode("utf-8")).encode("utf-8")
    if sha256_bytes(fixed) != FIXED_SHA256:
        raise ValueError("patched chunk SHA256 does not match locked production output")
    return fixed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply XIANYU ChatNew reconnect-convergence follow-up."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fixed = patch_bytes(args.input.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(fixed)
    print(f"BASE_SHA256={BASE_SHA256}")
    print(f"FIXED_SHA256={FIXED_SHA256}")
    print("XIANYU_CHAT_RECONNECT_CONVERGENCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
