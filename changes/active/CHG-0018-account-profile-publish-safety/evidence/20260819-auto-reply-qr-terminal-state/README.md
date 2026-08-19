# 2026-08-19 Auto Reply QR terminal-state repair

Decision: `PATCH_UPSTREAM`. No new service, Token implementation, Cookie owner, or reconnect owner is introduced.

User outcome: keep Ouyang Auto Reply recoverable through the existing upstream remote Token fallback, while accounts whose exact authoritative Cookie is already evidence-qualified `HUMAN_QR_REQUIRED` must stop showing indefinite `恢复中`.

Confirmed blocker: Auto Reply `refresh_token()` did not check the authoritative Session QR marker before Token/CAPTCHA/password-login work, and the main loop did not terminate the reconnect runtime when `human_qr_required` was returned.

Smallest success test:
- `2196106636` (欧阳): remote Token fallback succeeds, current authoritative Cookie remains unchanged/MTOP-valid, WebSocket reconnects from cache.
- `1034641456` (黑人): `token_state=human_qr_required`, `human_qr_required=true`, `reconnect_active=false`.
- `2219319284219` (王侠): same terminal waiting state as above.

Production evidence after targeted WebSocket reload:
```text
2196106636 connected=true token_state=success_from_cache qr=false platform_verify=false reconnect_active=false
1034641456 connected=false token_state=human_qr_required qr=true platform_verify=false reconnect_active=false
2219319284219 connected=false token_state=human_qr_required qr=true platform_verify=false reconnect_active=false
connection_stats total=6 connected=4
```

Safety:
- authoritative Cookie write for Ouyang: none.
- no QR action was performed.
- no product publish/message/item mutation.
- QR-required accounts no longer spend Token/CAPTCHA/password-login recovery attempts for the same authoritative Cookie.

Runtime file SHA256:
- `websocket/rootfs/websocket/app/services/xianyu/cookie_token_manager.py` `5b4117066d1630af88108dc219f0f3e6d9be76814c1f22230694ebecfad437bd`
- `websocket/rootfs/websocket/app/services/xianyu/xianyu_async.py` `e303115d33766fdaf6962e4db9c394b310ff54c103fc2d2b5f52dd816b094628`

Repository verification note:
- `python scripts/verify_repository.py` reached pytest and produced `645 passed / 14 failed`.
- The 14 failures are pre-existing latest-remote baseline issues in AI handoff encoding/regression invariant text, locked vendor patch byte hashes under Windows checkout normalization, and worktree Alembic path binding; this evidence-only change does not modify those files.
- Runtime targeted validation for this repair is the production status readback above plus `py_compile` on both modified WebSocket files.
