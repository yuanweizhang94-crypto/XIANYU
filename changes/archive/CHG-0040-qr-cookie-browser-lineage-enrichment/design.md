# CHG-0040 Design

Change ID: CHG-0040-qr-cookie-browser-lineage-enrichment
Status: ARCHIVED

## Existing owners

- QR Account persistence: AccountService.upsert_account_from_qr
- Browser Cookie and Profile lifecycle: CookieRenewBrowserService
- Existing-account authoritative Cookie CAS: validate_and_commit_authoritative_cookie_candidate
- Safe auth proof: safe_mtop_auth_probe
- Native Auto Reply: unchanged
- Chat owner: unchanged

No new Session owner.
No new Cookie store.
No new browser process owner.
No new Token owner.

## Minimal behavior

Before the current QR upsert writes any Account or Cookie state:

1. Resolve the existing account ID when recovering an existing account, otherwise use scanned unb as the temporary browser profile identity.
2. For an existing account, merge the current canonical Cookie fields in memory with the fresh QR candidate, with fresh QR values winning; perform no DB write.
3. Call existing cookie_renew_browser_service.renew with that candidate.
4. Require a successful non-empty enriched Cookie candidate.
5. Fail closed with QR_COOKIE_BROWSER_ENRICHMENT_FAILED before any account or Cookie commit if enrichment cannot establish the browser lineage.
6. Feed the enriched candidate into the existing safe-MTOP, CAS and new-account branches unchanged.

This applies automatically to normal QR and shared QR because both call the same AccountService method.

## Invariants

- Fresh login Cookie is browser-enriched before durable persistence.
- Existing-account canonical-only fields are preserved before browser enrichment; fresh QR values override older values.
- Browser cookies then merge into that candidate; original-only fields are preserved by the existing browser-renew service.
- Session refresh does not blindly replace the Cookie with a smaller partial set.
- Token refresh logic is untouched.
- CHG0039 explicit invalidation logic remains active and independent.
- Ordinary reconnect never forces login or Token refresh.
- Normal accounts are never modified by the patch merely because they exist.

## Safety

No QR candidate is persisted when browser enrichment fails.
No Cookie values are logged in evidence.
No normal account is restarted or rewritten by the code path unless that account itself performs a QR login.
