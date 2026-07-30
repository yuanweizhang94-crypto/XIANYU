# Xianyu upstream patch artifacts

## CHG-0016 manual-only verification patch

- Base upstream repository: `zhinianboke/xianyu-auto-reply`
- Base pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Patch file: `bda1a85-manual-only-verification.patch`
- Patch SHA256: `E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE`
- Local patch worktree: `D:/xianyu-upstream-manual-chg0016`
- Patch apply check: `git apply --check --whitespace=error-all --unidiff-zero <patch-file>`

## Artifact Format

Git-generated zero-context unified diff.

Generation command:

```text
git diff --cached --binary --full-index --no-ext-diff
--unified=0 --src-prefix=a/ --dst-prefix=b/ HEAD
```

Reason:

The pinned upstream source contains unchanged whitespace-bearing context lines.
Including those lines in a vendor patch causes repository whitespace checks to
inspect upstream baseline formatting rather than the five-file change itself.

Safety:

- patch hunks are never hand-edited;
- the patch applies only with `--unidiff-zero`;
- clean pinned-SHA apply check is mandatory;
- `--whitespace=error-all` is mandatory;
- applied-source `git diff --check` is mandatory;
- Git blob equivalence must be 5/5;
- exact target file set must remain five files.

## Artifact Generation

Generated from the staged five-file Git diff in a disposable worktree at the
pinned upstream SHA. Patch hunks must not be hand-edited.

## Parseability gate

`git apply --numstat --unidiff-zero <patch>`

## Clean apply gate

`git apply --check --whitespace=error-all --unidiff-zero <patch>`

## Equivalence gate

The staged Git blob IDs after clean application must match the staged Git blob
IDs used to generate the patch for all five files.

## Working-tree note

Raw byte hashes may differ on Windows only because text=auto can expand LF and
CRLF differently. Such a difference is acceptable only when:

- canonical CRLF-to-LF comparison is 5/5;
- BOM and trailing-newline state match;
- no lone CR exists;
- staged Git blob comparison is 5/5.

## Modified upstream files

- `common/services/captcha/manual_verification.py`
- `common/services/captcha/orchestrator.py`
- `websocket/app/core/config.py`
- `websocket/app/services/xianyu/cookie_token_manager.py`
- `tests/test_manual_verification.py`

## Runtime Boundary

The patch adds a default-off `CAPTCHA_MANUAL_ONLY` mode to the upstream captcha
orchestrator. When enabled it opens a visible local browser for the project
owner to complete the official verification page. It does not move the mouse,
type, click, drag, inject trajectories, call remote captcha services, create an
IM implementation, create a Token implementation, create a WebSocket
implementation, create a sender, or create a second automatic-reply executor.

The patch returns only the exact `x5sec` Cookie field for manual verification
and uses upstream `merge_account_cookie_fields` for the automatic-reply Token
path. It does not persist verification URLs, print Cookie values, print Token
values, or alter online chat and automatic-reply Token cache ownership.

## Single-shot and no-auto-retry boundary

The manual listener must run with `AUTO_START_WEBSOCKET=false` and expose only
health/internal control APIs until the project owner explicitly starts a
controlled manual validation. A host websocket process lifetime may open at
most one manual browser. After success, failure, timeout, cancellation, or
unknown redirect, later manual verification calls are consumed and must not open
another browser. If the native Token API still returns platform verification
after the one manual success retry, the patched upstream sets
`manual_verification_not_accepted` and remains disconnected.

## Live defect and fix

Observed live defect marker:
`MANUAL_VERIFICATION_REPEATED_BROWSER_LAUNCH`.

Root causes fixed in this patch:

- `AUTO_START_WEBSOCKET_NOT_DISABLED`
- `EXISTING_X5_COOKIE_FALSE_SUCCESS`
- `MANUAL_BROWSER_NOT_SINGLE_SHOT`
- `MANUAL_LISTENER_LOGS_DISCARDED`

The repaired patch uses a visible isolated temporary browser profile, exact
`x5sec` delta validation, strict `https://h5api.m.goofish.com` URL validation,
single-shot process state, local ignored listener logs, and one native Token
retry after owner-completed manual verification.

## Rollback

Stop the host manual listener, keep Docker websocket stopped, restore the
previous patch artifact from Git, and run the repository validation scripts
before any further live validation. Default replies remain disabled pending
project-owner decision.
