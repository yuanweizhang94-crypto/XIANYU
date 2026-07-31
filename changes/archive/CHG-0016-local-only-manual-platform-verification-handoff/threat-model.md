Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: ARCHIVED
# Threat Model

## Threats and controls

| Threat | Preventive control | Detection | Cleanup | Acceptance test |
|---|---|---|---|---|
| verification URL leakage | memory-only URL, no logs, no DB, no remote response | log scan and response schema test | expire task and clear memory | URL never logged |
| Cookie leakage | no value output, no Cookie files retained | redaction tests | delete temporary profile | Cookie value never logged |
| arbitrary URL injection | official host allowlist, no user-provided URL | route validation | cancel task | URL host allowlist |
| wrong-account Cookie write | owner scope plus account row ID | audit owner/account mismatch | reject merge | wrong-account write blocked |
| task hijacking | auth, CSRF, opaque task ID | audit actor and owner | cancel compromised task | owner scope |
| stale task replay | single-use ID and TTL | replay attempt log | expire task | TTL expiry |
| concurrent tasks | one global task and one per account | lock contention audit | cancel duplicate | one-task-per-account |
| local helper exposed to LAN | loopback-only binding | socket binding check | stop helper | loopback restriction |
| browser profile persistence | temporary profile lifecycle | filesystem cleanup check | delete profile | timeout cleanup |
| process left running | process owner and timeout | process scan | kill only owned helper/browser | cancel cleanup |
| hidden automatic interaction | structural ban on mouse/keyboard/click/drag solvers | import/call scan | fail closed | no automatic browser interaction |
| remote solver accidental fallback | configuration and import ban | network/client scan | fail closed | remote captcha client absent |
| logs containing secrets | structured redaction and allowlist | secret scan | purge generated local evidence only if approved | URL/Cookie never logged |
| platform response persistence | response body not stored | storage scan | clear task memory | no raw response persisted |
| account owner change during task | owner recheck before merge | owner mismatch audit | cancel task | owner scope change blocks |
| completion forged without Cookie proof | require expected Cookie delta | missing delta detection | fail task | complete without expected Cookie blocked |

## Upstream capability audit

Pinned/latest upstream do not satisfy the local owner-only manual handoff requirement.

## Pinned upstream evidence

Pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing local implementation search

No local manual bridge was found.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The handoff must not implement IM, Token, WebSocket, sender, automatic reply, AI reply, or browser solving.

## Why upstream cannot satisfy the requirement

Upstream provides automated or remote-solving paths rather than a pure manual local handoff.

## Approved exception ADR

Not applicable.

## Component owner

Manual handoff is operations-only; upstream keeps runtime ownership.

## Retirement plan for overlapping local code

Keep CHG-0010 frozen/deprecated and avoid overlapping sender behavior.

## Blocked closeout threat assessment

CHG-0016 closes with `MANUAL_VERIFICATION_NOT_ACCEPTED`. The remaining risk is
not solved by more local slider research. Follow-up delivery must rely on
upstream-native Token and account operation in a normal logged-in state, and
must fail closed if the platform again requires login, slider, face, device, or
other strong verification.

No message send, customer content, Cookie, Token, API key, account ID, complete
verification URL, browser profile, or raw platform response is committed by this
closeout.
