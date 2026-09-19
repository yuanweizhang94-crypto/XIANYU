from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any


BASE_SHA256 = "5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b"
FIXED_SHA256 = "4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1"

TERMINAL_LOGIN_STATES = {
    "LOGIN_REQUIRED",
    "PLATFORM_VERIFICATION_REQUIRED",
}
AUTO_CONNECT_BLOCKED_STATES = {
    "LOGIN_REQUIRED",
    "PLATFORM_VERIFICATION_REQUIRED",
    "SESSION_EXPIRED",
}

REPLACEMENTS = [
    (
        'He=a=>a==="PLATFORM_VERIFICATION_REQUIRED"||a==="LOGIN_REQUIRED"||a==="SESSION_EXPIRED"||a==="SESSION_CHECKING"||a==="TOKEN_INITIALIZING"||a==="CONNECTING",Be=a=>{if(a.connected)return"已连接";',
        'He=a=>a==="PLATFORM_VERIFICATION_REQUIRED"||a==="LOGIN_REQUIRED"||a==="SESSION_EXPIRED"||a==="SESSION_CHECKING"||a==="TOKEN_INITIALIZING"||a==="CONNECTING"||a==="DISABLED",Be=a=>{if(a.status!=="active"||a.chat_state==="DISABLED")return"已禁用";if(a.connected||a.runtime_connected&&!["LOGIN_REQUIRED","PLATFORM_VERIFICATION_REQUIRED"].includes(a.chat_state||""))return"已连接";',
    ),
    (
        'const V=n.useRef(0),Le=n.useRef(0),oe=n.useRef(0),de=n.useRef(0),os=n.useRef(()=>{}),Pe=n.useRef({})',
        'const V=n.useRef(0),Le=n.useRef(0),oe=n.useRef(0),de=n.useRef(0),autoChatOnce=n.useRef(new Set),os=n.useRef(()=>{}),Pe=n.useRef({})',
    ),
    (
        'const J=n.useCallback(async(e=1)=>{I(!0);try{const t=await Us(e);o(e===1?t.data:c=>[...c,...t.data]),j(e),x(t.hasMore)}catch(t){a({message:t.message||"获取账号列表失败",type:"error"})}finally{I(!1)}},[a]),hs=',
        'const normalizeChatAccounts=e=>e.map(t=>t.status!=="active"?{...t,connected:!1,chat_state:"DISABLED",chat_reason:"account_disabled"}:t.runtime_connected&&!["LOGIN_REQUIRED","PLATFORM_VERIFICATION_REQUIRED"].includes(t.chat_state||"")?{...t,connected:!0,chat_state:"READY",chat_reason:"chat_runtime_client_ready"}:t),J=n.useCallback(async(e=1,t=!1)=>{t||I(!0);try{const c=await Us(e),i=normalizeChatAccounts(c.data);o(e===1?i:d=>[...d,...i]),j(e),x(c.hasMore)}catch(c){t||a({message:c.message||"获取账号列表失败",type:"error"})}finally{t||I(!1)}},[a]),hs=',
    ),
    (
        'n.useEffect(()=>{J()},[]);const ue=',
        'n.useEffect(()=>{let e=!1,t=null;J();const c=()=>{t=window.setTimeout(async()=>{if(e)return;await J(1,!0),e||c()},5e3)};return c(),()=>{e=!0,t&&clearTimeout(t)}},[J]),n.useEffect(()=>{for(const e of l)e.connected||e.status!=="active"||e.runtime_connected||e.connection_state!=="connected"||!e.token_ready||["LOGIN_REQUIRED","PLATFORM_VERIFICATION_REQUIRED","SESSION_EXPIRED"].includes(e.chat_state||"")||autoChatOnce.current.has(e.account_id)||w.current.has(e.account_id)||(autoChatOnce.current.add(e.account_id),ys(e.account_id))},[l]);const ue=',
    ),
]

CACHEFIX_REQUIRED_SNIPPET = (
    "Pe.current[e]={convs:y,hasMore:g.hasMore,cursor:g.nextCursor},T(y)"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_account(account: dict[str, Any]) -> dict[str, Any]:
    out = dict(account)
    if out.get("status") != "active":
        out.update(
            connected=False,
            chat_state="DISABLED",
            chat_reason="account_disabled",
        )
        return out

    if (
        bool(out.get("runtime_connected"))
        and str(out.get("chat_state") or "") not in TERMINAL_LOGIN_STATES
    ):
        out.update(
            connected=True,
            chat_state="READY",
            chat_reason="chat_runtime_client_ready",
        )
    return out


def status_label(account: dict[str, Any]) -> str:
    account = normalize_account(account)
    state = str(account.get("chat_state") or "")

    if account.get("status") != "active" or state == "DISABLED":
        return "已禁用"
    if bool(account.get("connected")):
        return "已连接"

    return {
        "CONNECTING": "正在恢复账号连接",
        "TOKEN_INITIALIZING": "正在初始化聊天能力",
        "SESSION_CHECKING": "正在检查登录状态",
        "SESSION_EXPIRED": "Session已失效",
        "PLATFORM_VERIFICATION_REQUIRED": "需平台验证",
        "LOGIN_REQUIRED": "需登录",
        "RATE_LIMITED": "请求频繁",
        "CONNECTION_FAILED": "连接失败",
        "TEMPORARY_FAILURE": "暂不可用",
    }.get(state, "未连接")


def should_auto_connect(
    account: dict[str, Any],
    *,
    already_attempted: bool = False,
    connect_inflight: bool = False,
) -> bool:
    state = str(account.get("chat_state") or "")
    return bool(
        not account.get("connected")
        and account.get("status") == "active"
        and not account.get("runtime_connected")
        and account.get("connection_state") == "connected"
        and account.get("token_ready")
        and state not in AUTO_CONNECT_BLOCKED_STATES
        and not already_attempted
        and not connect_inflight
    )


def transform_text(text: str) -> str:
    if CACHEFIX_REQUIRED_SNIPPET not in text:
        raise ValueError("required 2026-09-19 account-cache convergence fix is missing")

    transformed = text
    for old, new in REPLACEMENTS:
        count = transformed.count(old)
        if count != 1:
            raise ValueError(
                f"expected exactly one spinner-convergence preimage, found {count}"
            )
        transformed = transformed.replace(old, new, 1)
    return transformed


def patch_bytes(data: bytes) -> bytes:
    if sha256_bytes(data) != BASE_SHA256:
        raise ValueError("input chunk SHA256 does not match locked production preimage")

    fixed = transform_text(data.decode("utf-8")).encode("utf-8")

    if sha256_bytes(fixed) != FIXED_SHA256:
        raise ValueError("patched chunk SHA256 does not match locked production output")
    return fixed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the 2026-09-19 XIANYU Online Chat account-status "
            "spinner convergence hotfix."
        )
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fixed = patch_bytes(args.input.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(fixed)

    print(f"BASE_SHA256={BASE_SHA256}")
    print(f"FIXED_SHA256={FIXED_SHA256}")
    print("XIANYU_ONLINE_CHAT_SPINNER_FIX=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
