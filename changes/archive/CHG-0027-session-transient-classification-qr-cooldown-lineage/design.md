# CHG-0027 Design

Status: ARCHIVED

Change ID: CHG-0027-session-transient-classification-qr-cooldown-lineage

## Authoritative failure classification

`SESSION_RENEW_FAILED` is a lifecycle outcome, not intrinsically fatal evidence. Existing consumers must classify from the underlying authoritative reason:

- explicit fatal: `SAFE_MTOP_SESSION_EXPIRED`, `FAIL_SYS_SESSION_EXPIRED`, explicit login-required, explicit credential-invalid/expired -> `SESSION_EXPIRED` or `LOGIN_REQUIRED`.
- transient/retryable: `SAFE_MTOP_NETWORK_ERROR`, timeout, connection/transport/upstream temporary errors, generic retryable errors -> existing `TEMPORARY_FAILURE` / checking/retry-later semantics.
- platform verification remains a separate explicit-evidence state and is never inferred from unknown/transient failure.

A newer settled authoritative `AUTH_VALID` result outranks stale transient failure metadata. Connected/token-ready runtime evidence cannot override explicit fatal Session evidence; conversely stale transient failure cannot override newer AUTH_VALID.

The classification is centralized in the existing status composition layer and reused by Auto Reply, Chat, and Publish capability consumers. No Frontend account-specific workaround is allowed.

## Session-expired cooldown lineage

Reuse existing `cookie_fingerprint()` as the authoritative lineage marker. The Session-expired cooldown record becomes account-scoped and lineage-scoped:

`account_id -> {marked_at, cookie_fingerprint}`

`mark_account_session_expired` records the fingerprint of the exact Cookie lineage that produced explicit expired evidence. `is_account_session_cooled` receives the current authoritative Cookie and returns active only when the current fingerprint equals the recorded fingerprint and the 300-second TTL remains active. If the fingerprint differs, the stale Session-expired cooldown is deleted for that account only.

This naturally handles QR success: authoritative QR Cookie commit changes the Cookie fingerprint, so the old pre-QR expired cooldown cannot apply to the new lineage. It also remains restart-safe: the current implementation's cooldown is process-local and does not persist across Scheduler restart; no restart path may reconstruct a stale cooldown from historical logs. No unrelated rate-limit/PVR/CAPTCHA/password-error cooldown is cleared.

CAS failure or failed QR finalization does not change the authoritative Cookie fingerprint, so the old cooldown remains valid until actual Cookie lineage changes or TTL expires.

## Component ownership

Backend: existing account/status and Chat status adapters.
Scheduler/common: existing Session-expired cooldown utility and its current consumers.
Frontend: unchanged unless later source evidence proves it independently hardcodes the wrong state.
WebSocket: unchanged.
Publisher owner: unchanged; only capability truth is consumed.

## Deployment

Build only source-changed components. Backend and Scheduler replacements are serial. Before each replacement lock rollback image/container identity, source-image hashes, config/network/mount identity, and health. UNKNOWN replacement outcome triggers read-only identity/health recovery; no blind retry.

## Acceptance safety

No QR, password login, manual Chat connect, Cookie/Token refresh for acceptance, real message send, real product publish/edit, or Item Sync. Synthetic reply/publish tests must mock outbound/submit transport.

## Final persistence topology

The cumulative Vendor Patch preserves component-specific lineage with two explicit roots:

- `backend/` replays over the accepted Backend preimages.
- `scheduler/` replays over the accepted Scheduler preimages.

The two historical `common/utils/cookie_refresh.py` preimages are intentionally not unified. Backend preimage SHA256 is `eb9f4abdc03ac6f2852d8efd3e1b4523fc502e0374d507f0f42c445ca31d9d65`; Scheduler preimage SHA256 is `829810f1183a281cd94b2d239be188a8cd1b82a31e5437403a8357259063ed04`. The accepted Scheduler source already contained 19 pre-existing writable-runtime drift files; the final patch includes only the 12 Scheduler paths actually changed by CHG0027 and the 4 Backend paths actually changed by CHG0027.

## Follow-up ownership

Publisher READY convergence is a later product-capability Change. It must audit the existing upstream/current producer and consumer owners before proposing any writer. The current Publisher executor remains unchanged.

Fixed-target visual inspection is a separate COMPANY infrastructure prerequisite limited to read-only inspection of the production Xianyu Frontend target. Arbitrary localhost, arbitrary ports, private URLs, raw CDP bypass, and write operations remain forbidden.
