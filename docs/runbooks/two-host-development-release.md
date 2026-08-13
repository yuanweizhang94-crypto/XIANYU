# Two-Host Development and Release Runbook

Owner decision recorded: 2026-08-05

Operational model status: adopted

Desktop parity status: not yet verified

## Execution Contract

User outcome: Keep the laptop as the stable production host while using the company desktop for future development and repair work.

Confirmed blocker: The laptop contains the latest runtime-verified candidate source and active production deployment, while the desktop has an upstream checkout and containers but has not been proven equivalent to the laptop.

Smallest success test: The desktop checks out one exact GitHub commit, reproduces the approved patched source and offline tests in an isolated disabled runtime, and produces a parity report without copying production credentials or starting a second live executor.

## Host Roles

### Laptop: production authority

The laptop is the only host authorized by this runbook to operate the current production Xianyu accounts and side-effecting runtime.

It owns:

- active production containers;
- locally provisioned account authentication;
- production database and runtime volumes;
- final controlled deployment verification;
- rollback to the previously recorded production commit and image set.

Normal feature development should not occur directly in the laptop production checkout. If an urgent production repair is unavoidable, its exact source diff must be reconciled back to GitHub before the repair is considered durable.

### Company desktop: development and repair authority

The desktop is the preferred host for future source changes, defect repair, targeted tests, patch generation, clean builds, and pre-release validation.

By default it must remain non-production:

- no production Cookie, Token, API key, browser profile, database, Redis/MySQL volume, or customer data;
- no production account login;
- no automatic WebSocket startup for production accounts;
- no automatic reply sender;
- no product publish, edit, unpublish, delete, order, refund, shipping, or rating action;
- no shared production ports or Compose project name.

Any live desktop validation requires a separate exact owner authorization defining the account, action, object, count, rollback, and stop condition.

### GitHub: code and handoff authority

GitHub is the canonical source for source code, vendor patches, tests, governance documents, sanitized evidence, commit identity, and release history.

A local runtime result that cannot be reproduced from one exact GitHub commit is operational evidence only and is not a completed software delivery.

### GitHub transport on production laptop

The production laptop uses GitHub official SSH over port 443 as its verified delivery transport.

- Laptop GitHub account: `yuanweizhang94-crypto`.
- Host: `ssh.github.com`.
- Port: `443`.
- XIANYU repository URL: `ssh://git@ssh.github.com:443/yuanweizhang94-crypto/XIANYU.git`.
- The existing `origin` remote does not need to change; use a one-time SSH URL and a process-scoped `GIT_SSH_COMMAND` when needed.
- Local SSH identity reference: `~/.ssh/id_ed25519_xianyu` (`SSH_KEY_CONFIGURED=true`).
- Before delivery is complete, the exact local commit SHA must equal the exact remote branch SHA.
- The standard `github.com` HTTPS Git path is not the preferred laptop push transport after the observed path-specific failure; `api.github.com` availability does not prove the Git HTTPS path is healthy.
- Do not re-debug the known HTTPS path on every repair while SSH over 443 remains healthy. If SSH over 443 fails, diagnose transport or identity only; do not reopen completed application development.
- If transport fails after a verified local commit exists, preserve that exact commit and resume its push later rather than recreating the change.
- If the remote branch has advanced, stop and compare local and remote SHAs. Do not force-push.

The local SSH identity is machine-local credential material. Only its path, public-key material, and authentication result may be inspected or recorded. Secret key contents must never be read, printed, committed, logged, placed in evidence, handoff packages, or AI output. On first use or host-key change, verify the presented fingerprint against GitHub's official published fingerprint before accepting it.

A GitHub-persistent repair is not complete at "code fixed" or "tests passed". The delivery sequence is: repair -> targeted tests -> repository verification -> exact diff review -> stage only current-task files -> local commit -> SSH-over-443 push -> remote SHA verification. Production deployment remains a separate operation.

## Single-Executor Invariant

Two automatic-reply, WebSocket, AI-reply, or publish executors must never operate the same production account at the same time.

Before any authorized host-role switch:

1. identify the currently active production host;
2. stop and verify the old executor;
3. observe a quiet period appropriate to the action;
4. confirm the new host uses the approved commit and runtime configuration;
5. start only the explicitly authorized executor;
6. verify one controlled event;
7. retain a tested rollback path.

A host-role switch is not part of routine code synchronization.

## Permitted Transfer Material

The following may move through GitHub after review:

- source code;
- exact vendor patches against a pinned upstream SHA;
- tests using unmistakably synthetic values;
- specifications and runbooks;
- sanitized acceptance evidence;
- file inventories, image digests, commit SHAs, and SHA256 manifests;
- redacted test and validation summaries.

The following must not be copied between computers or committed:

- Cookie, Token, API key, Authorization value, passwords, private keys, or secret files;
- browser profiles, login sessions, device fingerprints, or verification artifacts;
- MySQL/Redis/Docker production volumes;
- production database exports unless a separately approved encrypted backup procedure exists;
- raw customer messages, full account IDs, full item IDs, or unredacted screenshots/logs;
- local `.env`, Compose override secrets, or ignored runtime state.

Accounts required on the laptop must be provisioned through the upstream-native official workflow. They must not be cloned from the desktop.

## Phase 1: Laptop Source Reconciliation

The laptop must reconcile its latest runtime-verified source into the existing CHG-0017 GitHub branch before desktop parity can be claimed.

Required steps:

1. preserve untracked evidence before advancing the local governance checkout;
2. reconcile the checkout with the exact current PR head without destructive reset;
3. inspect the candidate worktree relative to pinned upstream base `4c5e1ac5f532c7313365d70409ae115305de8a55`;
4. replace sensitive-shaped test literals with clearly synthetic values without changing production behavior;
5. regenerate the vendor patch including the final publish source and test delta;
6. add only reviewed sanitized publish evidence;
7. run targeted tests, repository validation, quality checks, and security scan;
8. review the complete staged scope explicitly;
9. commit and push only the approved paths to the existing feature branch;
10. keep PR #26 Draft until same-commit CI and clean rebuild evidence are complete.

The current known missing candidate paths are:

- `backend-web/app/services/xianyu_publisher.py`;
- `common/services/publish_execution_service.py`;
- `tests/test_chg0017_publish_login_submit.py`.

## Phase 2: Desktop Acquisition and Parity Validation

After Phase 1 produces one approved GitHub commit, the desktop must:

1. preserve any existing desktop work before synchronization;
2. fetch the repository without destructive cleanup;
3. compare local branches, staged changes, unstaged changes, untracked files, and container state;
4. create or use an isolated clean checkout at the approved commit;
5. confirm the pinned upstream base SHA;
6. apply the repository vendor patch in a clean upstream worktree;
7. verify the exact patched file set and patch SHA256;
8. install dependencies from the repository-defined setup;
9. run offline targeted tests, repository verification, lint, type checks, and security scan;
10. build desktop development images from that commit;
11. use a distinct Compose project name, volumes, network, and host ports;
12. keep all production side-effect features disabled;
13. produce a sanitized parity report.

Desktop parity requires all of the following:

- exact approved GitHub commit recorded;
- clean patch apply check passed;
- patched file hashes match the recorded manifest;
- offline tests and security gates passed;
- container images are reproducible from the commit;
- no production secret or volume was copied;
- no production executor was started;
- remaining environment-only differences are documented.

## Normal Repair Flow

After desktop parity is verified, normal work follows this direction:

1. reproduce and repair on the desktop in a dedicated branch or worktree;
2. run the smallest targeted offline test;
3. run repository and security gates;
4. review the exact diff;
5. commit and push the approved scope;
6. update or reuse the existing matching pull request;
7. require green CI on the exact commit;
8. on the laptop, preserve production state and pull the exact approved commit;
9. rebuild from that commit rather than copying container files;
10. perform only the explicitly authorized controlled production verification;
11. record the deployed commit, image digests, result, and rollback;
12. return any runtime-confirmed source correction to GitHub immediately.

The normal source direction is:

`desktop development -> GitHub review/CI -> laptop deployment -> sanitized verification evidence -> GitHub`

## Release Record

Every laptop deployment must record, without secrets:

- XIANYU repository commit;
- pinned upstream base SHA;
- vendor patch filename and SHA256;
- candidate image digests;
- offline and CI test results;
- deployment time;
- production host role;
- controlled verification result;
- rollback commit and image set;
- any known environment-only difference.

## Current State At Adoption

- The laptop is currently the active-use production host.
- The desktop already has an upstream project checkout and corresponding containers.
- Desktop equivalence to the laptop has not yet been proven.
- PR #26 remains Draft, Open, and Unmerged.
- The final laptop runtime-verified publish source, test, and sanitized evidence still require reconciliation into GitHub.
- `PR_READY=false`.
- `MERGE_READY=false`.
- T17 archive/delivery remains not authorized.

This runbook records the host and transfer model only. It does not authorize a production host switch, credential transfer, live desktop validation, PR Ready transition, merge, or CHG-0017 archive.
