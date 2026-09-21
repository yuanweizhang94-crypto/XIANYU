# CHG-0040 Tasks

Change ID: CHG-0040-qr-cookie-browser-lineage-enrichment
Status: VERIFYING

- [x] T1 Locate formal Session invalid capability calculation and canonical failure classifier.
- [x] T2 Prove both affected accounts share the same hard Session-expiry evidence and same hourly batch.
- [x] T3 Compare affected Cookie lineages against two current normal controls.
- [x] T4 Prove QR passport manager persists only accumulated HTTP response Cookie fields.
- [x] T5 Prove existing browser health already persists browser Cookie deltas.
- [x] T6 Reuse CookieRenewBrowserService in the QR Account persistence owner before any durable Cookie write.
- [x] T7 Build isolated backend candidate and compile patched source.
- [x] T8 Dynamic-test enrichment-before-CAS and fail-closed-before-commit behavior.
- [x] T9 Add and pass repository targeted/regression tests, validate_change, diff checks, security scan and repository verification.
- [ ] T10 Activate the minimal Backend production image and verify normal account health reconverges.
- [ ] T11 Perform one human QR recovery for each hard-expired affected account through the repaired path (deferred non-blocking; user explicitly forbids QR recovery in this round).
- [ ] T12 Verify both affected accounts Session, WS, Chat and Auto Reply runtime readiness (deferred non-blocking until future authorized QR recovery).
- [ ] T13 Commit, push and verify local equals github-ssh443/main.

## Reuse decision

Decision: PATCH_UPSTREAM
