# 2026-09-21 multi-account Session lifecycle evidence

All Cookie and Token values are excluded. Only fingerprints, lengths, counts, timestamps and states are retained.

## Formal UI status source

Session已失效 is synthesized by Backend business capabilities and Chat status from xy_accounts.metadata.session_maintenance, passed through classify_session_failure_evidence. It is not derived directly from the account table status or Cookie length.

## Affected accounts

701229202 and 1835476245 were created by QR on 2026-09-20. Both retained 18 Cookie fields.

At 2026-09-21 14:51 local time, in the same scheduled API Cookie renewal batch:
- 1835476245 -> human_qr_required, OFFICIAL_RENEWAL_FAILED_SAFE_MTOP_SESSION_EXPIRED
- 701229202 -> human_qr_required, same failure

Both canonical browser checks showed visible login UI. Both metadata records store HUMAN_QR_REQUIRED and bind the QR-required marker to the current Cookie fingerprint.

Neither account has stored username or password credentials.

## Controls

2221384086829 and 1951966327 were current recent real Auto Reply success controls. Their browser Session state remained REAL_BROWSER_LOGIN_READY. Their Cookie field counts were 30 and 27.

## QR lineage defect

The QR manager uses httpx against h5api and passport endpoints. It accumulates only resp.cookies from those HTTP responses. On confirmed QR login, that accumulated dictionary is marshalled and handed to AccountService.upsert_account_from_qr.

Before CHG-0040, QR upsert safe-probes and persists that candidate without first establishing the canonical Goofish browser Cookie lineage.

The existing CookieRenewBrowserService already injects a Cookie candidate into the per-account persistent browser Profile, opens Goofish, obtains browser Cookies, merges browser fields into the original candidate and preserves original-only fields. Session health already persists any browser-health Cookie deltas through authoritative CAS.

Therefore the missing lifecycle edge is QR finalization to browser enrichment before first durable persistence.

## CHG0039 production activation

The WebSocket production image was switched to xianyu-chg0039-websocket:token-invalidation-recovery-20260920-r1. Runtime source contains the explicit invalidation guard. Eight instances rehydrated; six normal accounts connected automatically. The two affected accounts remained disconnected with human_qr_required, which is expected from their independent hard Session expiry.

No account restart endpoint was called for any normal account.
