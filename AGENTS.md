# Repository Agent Rules

These rules apply to any AI or automation agent and are not specific to one vendor or model.

## P0 non-negotiable rule: upstream first, never reinvent an existing wheel

- After safety, legality, credentials, permissions, platform-verification boundaries, and explicit project-owner instructions, this is the highest development priority. It outranks speed, convenience, refactoring preferences, architecture ambition, future scalability, and feature expansion.
- Before proposing or writing any Xianyu code, inspect the upstream feature description, pinned upstream implementation, relevant newer upstream commits/issues, and the existing local implementation record. Do not design a local replacement first.
- The mandatory decision order is: reuse the exact upstream function or native workflow -> configure the existing upstream capability -> apply the smallest auditable fix to the upstream path -> add a thin operations-only wrapper -> build a local exception only as the final approved resort.
- If upstream already contains the needed method, service, model, route, UI, task, lock, cache, profile, log, or workflow, use it directly. If it contains the correct path with a confirmed defect, repair that path without replacing its execution owner or duplicating its data model.
- A claim that upstream lacks a solution is invalid until the active work record lists the searched README/docs, UI, routes, services, models, workers, scheduler tasks, tests, configuration, logs, issues, and commits relevant to the capability.
- New services, tables, APIs, workers, queues, schedulers, browser managers, Token implementations, Cookie implementations, login implementations, sender implementations, or execution owners are forbidden while an existing path can be reused or minimally repaired.
- Every development task must record the reuse decision as one of `ADOPT_UPSTREAM`, `CONFIGURE_UPSTREAM`, `PATCH_UPSTREAM`, `WRAP_FOR_OPERATIONS`, or approved `BUILD_LOCAL_EXCEPTION`, together with duplicate-development risk and rollback.
- Any minimal patch must preserve upstream APIs, return shapes, data ownership, UI workflow, and execution ownership wherever possible, and must include a default-off or otherwise deterministic rollback path when runtime behavior changes.
- When upstream later provides an equivalent capability, overlapping local code must be reviewed for retirement rather than expanded.
- The current formal direction and capability disposition are recorded in `docs/FORMAL_DEVELOPMENT_DIRECTION.md`. A future Change may refine implementation details but may not weaken this P0 rule.

## Highest delivery priority: smallest safe solution, no duplicate development

- After safety, legality, credentials, permissions, and explicit project-owner boundaries, the highest delivery priority is to complete the user's stated business outcome with the smallest proven, reversible change.
- Before editing code or configuration, write a three-line execution contract in the active work record: `User outcome`, `Confirmed blocker`, and `Smallest success test`. Work outside that contract is forbidden unless new evidence makes expansion unavoidable.
- Use this order: existing native path -> configuration correction -> minimal defect fix -> reuse a proven local component -> new component as the last resort.
- Fix only confirmed defects. Do not add speculative architecture, generic abstractions, unrelated hardening, cleanup, or future-facing features during a repair.
- Do not add a new service, helper, bridge, UI, API, table, model, dependency, runtime, worker, sender, or execution owner when an existing path can be corrected.
- Do not repeat an upstream audit, local-history audit, or root-cause investigation that is already recorded and still valid. Re-open it only when new evidence directly contradicts the recorded conclusion.
- Do not create a parallel Change, PR, implementation, fallback runtime, or temporary executor for the same blocker.
- Use one controlled reproduction, then targeted tests for the confirmed defect. Run full repository validation only after the targeted test passes. Repeated live retries are forbidden.
- Stop at the first new blocker. Report the exact evidence and the smallest next action; do not improvise another layer of development.
- Any unavoidable scope expansion or new runtime component requires explicit project-owner approval and recorded evidence explaining why configuration, an existing function, or a minimal patch cannot solve the problem.
- Documentation, CI success, or a merged PR does not prove the user's business outcome. Do not mark work complete while the original blocker still exists.
- Progress reports must use plain language: what is blocked, what exact change is being made, what result was observed, and whether the owner must act.

## Required behavior

- Do not rely on old chats, model memory, or external memory.
- Run `python scripts/project_context.py` before development.
- Treat `changes/active/`, `specs/`, `docs/adr/`, `contracts/`, `generated/PROJECT_STATE.json`, `scripts/`, and `tests/` as the fact sources.
- Specific change scope must be read only from the current active change proposal, design, tasks, and acceptance files.
- Root `AGENTS.md` must not store the feature boundary for any specific change.
- The current active change `acceptance.md` has priority for defining what is allowed and forbidden in the current work.
- DRAFT status is read-and-review only and must not be implemented.
- APPROVED, IMPLEMENTING, and VERIFYING are executable statuses.
- Do not modify business code when there is no executable active change.
- Execute only the current executable active change.
- Complete only one unfinished task at a time.
- Search existing implementation, specs, ADRs, scripts, tests, and archived change research before adding new work.
- Do not implement the same capability in parallel paths.
- Do not manually edit generated files, especially `generated/PROJECT_STATE.json`.
- Do not add unapproved dependencies.
- Stop and fail closed when risk, credentials, permissions, platform verification, or scope is uncertain.
- Do not commit Cookie, Token, Secret, private keys, real customer data, or browser Profiles.
- Do not hardcode any specific change identifier in this file.
- Run `python scripts/verify_repository.py` after completion.

## Mandatory GitHub delivery and persistence

- GitHub is the formal persistence authority for XIANYU source code, vendor patches, tests, governance, sanitized evidence, commit identity, and release history. A repair that exists only in a local checkout or production runtime is not a complete software delivery.
- When the project owner authorizes GitHub persistence for the current task, a verified source change must not stop at local source changes, runtime deployment, passing tests, or a local commit. Complete the authorized delivery as: development/repair -> targeted tests -> repository verification -> review exact diff -> stage only current-task files -> local commit -> push -> verify the remote branch SHA -> delivery complete.
- GitHub persistence and production deployment are separate operations. Do not treat a successful deployment as proof of GitHub delivery, and do not redeploy production merely to complete a GitHub push.
- Before staging, distinguish and report `PRE_EXISTING_DIRTY_FILES`, `THIS_RUN_CHANGED_FILES`, and `COMMITTED_FILES`. Never use `git add .` or `git add -A` blindly when pre-existing dirty files exist. Stage only the exact current-task paths, and do not reset, restore, clean, stash away, or otherwise destroy unrelated dirty work.
- `git push --force` and `git push --force-with-lease` are forbidden unless the project owner separately and explicitly authorizes that exact history rewrite. Do not rewrite branch history, overwrite another contributor's remote work, blind-reset a branch, or delete old dirty files merely to make a push easier.
- A push is complete only after the exact `LOCAL_COMMIT_SHA` is compared with the exact `REMOTE_BRANCH_SHA` for the intended branch and they are equal. Terminal text such as `Everything up-to-date` or `Push successful` is not sufficient verification by itself.
- On the production laptop, the preferred verified Git transport is GitHub's official SSH service over port 443: host `ssh.github.com`, port `443`, repository URL form `ssh://git@ssh.github.com:443/<owner>/<repo>.git`. The standard `github.com` HTTPS Git path has shown path-specific instability on this laptop, so do not repeatedly re-debug or prefer that path while the verified SSH-over-443 path remains healthy.
- Do not modify the existing `origin` remote merely to use SSH over 443. Use a one-time SSH URL and, when needed, a process-scoped `GIT_SSH_COMMAND` for the push and remote-SHA verification.
- The laptop GitHub SSH identity is machine-local credential material. Baseline: `SSH_KEY_CONFIGURED=true`; local key reference: `$HOME/.ssh/id_ed25519_xianyu`. The path may be recorded, but the private key content must never be read, printed, copied, logged, included in evidence or handoff packages, or committed. Never commit `.ssh`, private keys, PEM files, Tokens, Cookies, Authorization values, passwords, API keys, or other credentials.
- SSH identity checks are limited to key existence, public-key inspection, and authentication tests. Never use `Get-Content`, `cat`, or equivalent commands on the private key. If the configured key file is missing, report the missing identity and stop; do not generate a second key unless the project owner explicitly authorizes it.
- On first use of an SSH host, or whenever a host key changes, verify the presented GitHub host fingerprint against GitHub's official published fingerprint before accepting it. Never blindly accept an unknown or changed SSH host key.
- If application development and local commit creation are already complete but GitHub transport fails, preserve the exact local commit. Do not re-develop, regenerate the same patch, or create a replacement commit solely because push failed; resume by pushing the original commit when transport recovers.
- If the remote branch has advanced unexpectedly, stop before pushing. Record `LOCAL_COMMIT_SHA` and `REMOTE_BRANCH_SHA`, inspect the divergence, and obtain or apply the appropriate merge/rebase decision without force-pushing.
- Ordinary source and documentation changes must pass `git diff --check`. An immutable `.patch` artifact whose SHA256 is already locked is a different artifact type: if the outer diff check fails only because the patch text faithfully contains original trailing whitespace, do not edit the locked patch just to make the outer check green. Validate it with the recorded `PATCH_SHA256`, clean-apply verification, and content-equivalence checks instead.

## Mandatory upstream evidence before design, development, repair, or validation

- Before proposing, designing, implementing, repairing, or live-validating a Xianyu capability, first inspect the original upstream project's feature description and intended workflow. Evidence may include upstream README/docs, UI labels and help text, API routes, models, services, tests, release notes, issues, and commits.
- The pinned upstream SHA and pinned checkout are the runtime source of truth. Newer upstream branches or commits may be inspected only to identify an already-existing fix or intended behavior; they must not be silently adopted or treated as deployed behavior.
- Record the upstream feature name, pinned SHA, evidence paths, documented/native workflow, configuration points, execution service, and expected logs or status signals in the active Change before implementation or validation begins.
- Validation must exercise the upstream-native documented path first. Do not invent a replacement API, sender, worker, service, data model, or workflow merely to make a test pass.
- If upstream already provides the capability, use `ADOPT_UPSTREAM`, `CONFIGURE_UPSTREAM`, or a minimal auditable `PATCH_UPSTREAM` decision. Local parallel development is forbidden.
- Only when the original upstream does not provide the capability or does not address the observed problem may prior `D:/xianyu` implementations, archived changes, ADRs, experiments, tests, and research be considered as fallback evidence.
- A claim that upstream lacks a capability or fix must cite the searched documentation and source areas. "Not found" without recorded search evidence is not sufficient.
- No Change may enter implementation, repair, or live validation without both an upstream evidence record and a duplicate-development assessment.

## CHG-0008 upstream pilot anti-drift rules

- Before adding a new Xianyu capability, check existing Account, Message, Reply, Publish, and Schedule boundaries and reuse their facts instead of reimplementing them.
- Do not create large adapter abstractions, fake sessions, mapping DTOs, or new runtimes only because they may be useful later.
- Pin upstream repositories to exact commits before audit or execution; never silently follow floating main or master.
- Do not copy upstream source code, deployment scripts, protocol constants, signing logic, decryption logic, or Cookie examples into this repository.
- Local verified capability means deterministic local evidence only; it does not mean live Xianyu operation works.
- Stop on CAPTCHA, slider, face verification, device verification, risk-control prompts, unknown outcomes, or uncertain permissions.
- CHG-0008 is an upstream pilot governance and evidence change. It must not create CHG-0009 or `app/xianyu_system/adapters/xianyu/` without later pilot evidence proving a specific interface is needed.

## Upstream-first product direction

- Before creating or implementing any feature, search both `D:/xianyu` and the pinned upstream checkout at `D:/xianyu-upstream-pilot`.
- Inspect upstream feature documentation and native workflow before reading local fallback solutions. The required order is: upstream description -> pinned upstream implementation/tests -> upstream-native validation plan -> prior local research only when upstream is absent or insufficient.
- If pinned upstream has an equivalent capability, the Change must `ADOPT_UPSTREAM`, `CONFIGURE_UPSTREAM`, or `PATCH_UPSTREAM` instead of creating a parallel implementation in this repository.
- `WRAP_FOR_OPERATIONS` is allowed only for safety, governance, operations, validation, monitoring, backup, restore, diagnostics, and upgrade control around the upstream engine.
- `BUILD_LOCAL_EXCEPTION` is the last resort and requires pinned upstream evidence, local search evidence, duplicate-risk analysis, a referenced approved ADR, project-owner approval, component ownership, and a retirement or upstream-contribution plan.
- Two automatic-reply send executors must never run at the same time.
- The formal automatic-reply sole executor must be explicit in architecture documentation before any live automatic reply validation.
- A Change without a capability matrix reference, upstream feature-description evidence, pinned source evidence, native validation workflow, and reuse decision must not enter `IMPLEMENTING` or `VERIFYING`.
