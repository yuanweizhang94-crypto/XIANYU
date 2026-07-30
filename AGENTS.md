# Repository Agent Rules

These rules apply to any AI or automation agent and are not specific to one vendor or model.

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
