# 2026-08-19 Production WebSocket r4 Compose authority

Decision: `WRAP_FOR_OPERATIONS` around the already verified upstream/runtime patch. No business executor or new service is introduced.

## Execution contract

- User outcome: the Auto Reply Session/remote-Token fixes must survive a future WebSocket container recreation, not only an ordinary restart of the currently patched container.
- Confirmed blocker: the live WebSocket container had the verified runtime source loaded, and rebuildable r4 existed, but the local production `docker-compose.yml` still declared the legacy upstream WebSocket build context and `xianyu-chg0017-websocket:4c5e1ac`. A future compose recreation/build could therefore restore obsolete code.
- Smallest success test: production Compose must name the already validated r4 image as WebSocket authority and must not retain the obsolete WebSocket `build:` stanza that could overwrite that tag from the old source context.

## Applied local production configuration

The existing production compose file was backed up locally, then only the `websocket` service image authority was changed:

```text
WEBSOCKET_IMAGE=xianyu-chg0018-websocket:auth-cookie-closure-20260819-r4
WEBSOCKET_BUILD_PRESENT=false
```

The YAML parses successfully. Backend, MySQL, Redis, Scheduler, Frontend, networks, volumes, ports, environment references, and other services were not changed.

A direct `docker compose config` from the execution identity could not read the protected local `.env`; no attempt was made to expose, copy, or weaken permissions on that file. The current production WebSocket therefore remains the already patched and healthy container, while the persisted compose authority now points future WebSocket recreation to r4.

## r4 authority

`xianyu-chg0018-websocket:auth-cookie-closure-20260819-r4` was built from the closure overlay and passed offline validation:

```text
HASH_MATCH files=18
PY_COMPILE_PASS
WRITER_INVENTORY_PASS missing_expected=0 unknown_direct=0
```

Observed r4 manifest-list digest:

`sha256:20694990c822317ef2b39238cb046493551a4b21d7aca1eb4cf7116c88434fab`

The runtime behavior carried by r4 includes:

- authoritative `HUMAN_QR_REQUIRED` terminal handling;
- valid-Session `PLATFORM_VERIFICATION_REQUIRED` remote-only Token self-heal with safe MTOP gating and 180-second external-request gate;
- password-login-refresh route guard that blocks automatic password-login re-entry for the same evidence-qualified QR Cookie.

## Production verification after the final route guard

Current readback remained:

```text
2196106636 connected=true
2214313339860 connected=true
2217936413500 connected=true
2221501265279 connected=true
1034641456 human_qr_required=true reconnect_active=false
2219319284219 human_qr_required=true reconnect_active=false
connection_stats total=6 connected=4
```

Natural Session-maintenance requests observed after the route guard for both QR-required accounts were accepted by HTTP but terminated immediately at the QR guard; logs showed the `HUMAN_QR_REQUIRED` refusal and did not re-enter standalone password login. Healthy owners continued normal heartbeat responses.

## Locked artifact

Production Compose delta patch SHA256:

`96f096e319a990cdc881c9d25ff027d52dd4421a842539b98acbbc2bd37c9c1b`

## Fresh-worktree regression check

A fresh Windows worktree exposed that the two new patch-lock tests from this same repair chain were hashing checkout bytes directly, so CRLF normalization could make them fail even when the Git blob was unchanged. Those two tests now normalize line endings to LF before computing the locked SHA256. This preserves the same locked artifact hashes while preventing new Windows checkout-only failures.

Validation after that correction:

- the two new repair test modules: `8 passed`;
- full `python scripts/verify_repository.py`: `653 passed / 14 failed / 1 warning`;
- the remaining 14 failures are the same pre-existing latest-remote baseline group (handoff encoding/regression invariant assertions, older historical locked-patch checkout hashes, and isolated-worktree Alembic path binding). This repair chain no longer contributes additional fresh-worktree failures.

## Safety

```text
OTHER_PRODUCTION_SERVICES_RECREATED=0
PRODUCT_ACTIONS=0
PUBLISH_CALLS=0
ITEM_MUTATIONS=0
CUSTOMER_MESSAGES_SENT=0
QR_ACTIONS=0
CREDENTIAL_SECRET_OUTPUT=0
PROTECTED_ENV_PERMISSION_CHANGES=0
```
