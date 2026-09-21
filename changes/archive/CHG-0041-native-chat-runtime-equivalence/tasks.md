# CHG-0041 Tasks

Change ID: CHG-0041-native-chat-runtime-equivalence
Status: ARCHIVED

- [x] T1 Refresh current enabled account set and Native runtime truth.
- [x] T2 Recover the real enable timeline for 2219319284219.
- [x] T3 Prove enable already triggers start_account and Native WS readiness.
- [x] T4 Prove Backend shared-Native Chat calls fail at missing WebSocket internal endpoints.
- [x] T5 Compare upstream, local production-equivalent source and current runtime.
- [x] T6 Build an isolated candidate from the exact CHG0039 runtime preimage with Chat RPC additions only.
- [x] T7 Prove candidate routes delegate to the existing Native owner and reuse mid-future correlation.
- [x] T8 Prove CHG0038 registration and CHG0039 invalidation invariants are retained.
- [x] T9 Add repository regression tests and pass targeted/full/validate/diff/security/repository verification.
- [x] T10 Activate only the WebSocket service candidate and verify current enabled accounts converge automatically.
- [x] T11 Verify 2219319284219 Native Chat conversation read no longer returns 404 and shared owner is ready.
- [x] T12 Verify disabled accounts have zero runtime and duplicate runtime count is zero.
- [x] T13 Update authority, commit, push and verify local equals github-ssh443/main.

## Reuse decision

Decision: PATCH_UPSTREAM
