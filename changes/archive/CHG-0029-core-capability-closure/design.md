# CHG-0029 Design

Change ID: CHG-0029-core-capability-closure
Status: ARCHIVED

## Design Intent

Run a runtime-first closure loop for automatic reply, online chat, and product publish using the existing owners. Source is changed only if runtime-current evidence proves a defect that cannot be solved by activating already-merged code.

## Execution Order

1. CURRENT_GITHUB: verify `origin/main` and this worktree start at `4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89` or a trusted descendant.
2. CURRENT_LOCAL: verify CHG-0028 is archived and CHG-0029 is the only active Change.
3. CURRENT_RUNTIME: record Docker image/container/port/mount/health/source hashes without secrets.
4. CURRENT_ACCOUNT_COHORT: run read-only account/status/log probes with identifiers sanitized or summarized.
5. EXISTING_OWNER: map each capability to existing Backend/WebSocket/Scheduler owners.
6. ROOT_CAUSE: classify stale runtime, account/human gate, platform limitation, transient, or code defect.
7. MINIMAL_FIX: activate current source/patch or patch existing owner only when needed.
8. TESTS/REGRESSIONS: run focused deterministic tests and CHG0022/23/26/27/28 regressions.
9. DEPLOY/HEALTH/RUNTIME_HASH: scoped service replacement, health checks, and in-container source verification.
10. GIT/PR/CI/MERGE: exact-path staging and normal GitHub delivery for any source/evidence changes.

## Runtime Activation Design

Product publish CHG-0028 is expected to require Backend-only activation if runtime lacks `backend-web/app/api/routes/product_publish_capability.py` or the CHG-0028 `cookies.py` on-demand contract. Automatic reply and online chat require read-only evidence first; if their current images already match CHG0023/26/27 accepted sources and health/cohort checks pass, no rebuild is done.

## Tests

Focused repository tests:

- CHG-0029 active acceptance tests;
- CHG-0028 selected-account on-demand patch artifact tests;
- CHG-0026 and CHG-0027 archived acceptance regressions;
- CHG-0022 token/network classification unit tests when WebSocket classification is touched or revalidated;
- `ruff`, `security_scan`, `git diff --check`, and repository verification with existing CHG0020 debt classified separately.

Runtime tests:

- HTTP health for Backend, WebSocket, Scheduler, and Frontend;
- in-container source/hash readback for changed files;
- selected-account route existence without real MTOP unless separately authorized;
- account-list/global publish contract is `ON_DEMAND`/`NOT_CHECKED`;
- sanitized log/activity scans for reconnect loops, token storm, QR fail-closed, and worker silence/backlog.

## Rollback

Before replacing any container, record current container ID, image digest, image tag, ports, mounts, restart policy, command, health, and target source hashes. Roll back by recreating the affected service with the recorded preimage only. Do not roll back unrelated services.
