# Upstream First Policy

Change: CHG-0011-upstream-first-product-direction-freeze

## Purpose

The original upstream project is the product application and business execution engine. This repository is the safety, governance, operations, validation, evidence, and release-control layer. Development must not drift into rebuilding capabilities that upstream already provides.

## Highest-priority minimum-change and time-protection gate

After safety, legality, credentials, permissions, and explicit project-owner boundaries, the first priority is to deliver the user's stated business outcome with the smallest proven and reversible intervention.

Before any design, repair, implementation, or validation work begins, the active work record must state:

- `User outcome`: the concrete result the user is waiting for;
- `Confirmed blocker`: the single current fact preventing that result;
- `Minimal intervention`: the smallest existing path, configuration change, or defect fix that can remove the blocker;
- `Smallest success test`: the shortest safe test that proves the blocker is removed;
- `Stop condition`: the first result that requires stopping rather than expanding scope.

The following rules are mandatory:

1. Correct an existing path before creating a new path.
2. Prefer configuration over source changes, and a minimal patch over a wrapper or new component.
3. Repair only confirmed defects. Do not combine a repair with unrelated refactoring, architecture cleanup, generic hardening, future features, or aesthetic redesign.
4. Do not create a new service, helper, bridge, UI, API, model, table, dependency, runtime, worker, sender, or execution owner unless recorded evidence proves that the existing path cannot be corrected.
5. More than one new runtime component, or any new execution owner, requires explicit project-owner approval before implementation.
6. Do not repeat an upstream or local-history audit that is already recorded and remains valid. New evidence must directly contradict the prior conclusion before the audit is reopened.
7. Do not create parallel Changes, PRs, fallbacks, temporary executors, or alternate implementations for the same blocker.
8. Use one controlled reproduction, then targeted tests for the confirmed defect. Repeated live retries are forbidden. Full validation follows only after targeted tests pass.
9. Stop at the first new blocker and report the exact evidence plus the smallest next action. Do not improvise another platform or abstraction.
10. A merged PR, completed documentation, or green CI is not completion when the original user outcome is still blocked.
11. When an implementation proves too broad or introduces a new failure mode, reduce it in the same Change. Do not answer a narrow defect by creating another architecture layer.
12. Time waste caused by repeated investigation, duplicate implementation, unnecessary scope growth, or speculative development is a governance failure and must be corrected before more code is added.

For a runtime defect, the default allowed scope is one existing execution path and the tests needed to prove its repair. Any larger scope must document why the smaller options failed and must receive explicit project-owner approval.

## Mandatory evidence order

Before any Xianyu feature is designed, implemented, repaired, or live-validated, the change owner must follow this order:

1. Read the original upstream feature description and intended workflow. Search upstream README/docs, UI labels and help text, API descriptions, release notes, issues, and commits where available.
2. Inspect the pinned upstream implementation at the recorded SHA, including relevant frontend, route, service, model, worker, scheduler, tests, logs, and configuration.
3. Write the upstream-native workflow and expected evidence into the active Change. This includes the feature name, pinned SHA, evidence paths, configuration entry points, execution service, expected status/log signals, and known limits.
4. Plan development and validation around that native workflow.
5. Search prior local implementations, archived Changes, ADRs, experiments, tests, and research only when upstream does not contain the capability or does not address the observed problem.

The pinned upstream checkout is the deployed/runtime source of truth. Newer upstream code may be inspected to locate an existing upstream fix or clarify intended behavior, but it must not be silently treated as deployed or copied wholesale.

## Mandatory search before implementation

Before any feature implementation enters `IMPLEMENTING`, the change owner must search both:

1. `D:/xianyu-upstream-pilot` pinned upstream implementation at the recorded SHA, starting from upstream feature descriptions and then source evidence.
2. `D:/xianyu` current implementation, tests, specs, ADRs, scripts, active/archive changes, and previous research as a secondary fallback source.

The upstream search must cover UI, API, service, data model, worker, scheduler, frontend, tests, configuration, and logs when relevant.

A statement that a capability or fix is absent from upstream must record what documentation, paths, symbols, UI, routes, tests, issues, and commits were searched. An unsupported `NOT_FOUND` conclusion is not sufficient evidence.

## Mandatory gate before validation

Validation is not independent from upstream research. Before a functional or live validation begins, the active Change must state:

- the upstream feature being validated;
- the upstream-native user workflow;
- the pinned source paths that implement it;
- the service or process that owns execution;
- the configuration required for the test;
- the expected status transitions, logs, database evidence, and cleanup behavior;
- whether a newer upstream fix exists and whether the pinned deployment contains it;
- the duplicate executor or duplicate implementation risks.

Validation must first exercise the native documented path. A test must not introduce a new sender, worker, API, runtime, protocol implementation, or local business engine merely because the native path is currently failing.

When an unexpected problem occurs:

1. Re-check the pinned upstream feature workflow and implementation.
2. Search newer upstream commits/issues for the same problem or an existing fix.
3. Only if upstream has no corresponding capability or solution, search this repository's previous development and research for a reusable local approach.
4. If neither source contains a safe solution, stop and create a separately approved investigation or exception decision instead of improvising production code.

## Decision hierarchy

1. `ADOPT_UPSTREAM`: use the pinned upstream native capability directly.
2. `CONFIGURE_UPSTREAM`: configure the pinned upstream native capability without source changes.
3. `PATCH_UPSTREAM`: make a small auditable upstream patch or fork when native behavior is nearly sufficient. Prefer a narrowly extracted upstream fix when a later upstream commit already solves the exact problem.
4. `WRAP_FOR_OPERATIONS`: add governance, safety, validation, monitoring, backup, restore, diagnostics, or upgrade orchestration around upstream.
5. `BUILD_LOCAL_EXCEPTION`: last resort only.

## Reuse record required in every Change

Before entering `IMPLEMENTING` or `VERIFYING`, every Change involving a Xianyu capability must record:

- upstream repository and pinned SHA;
- upstream feature description references;
- pinned upstream code/test/config evidence;
- native workflow and execution owner;
- capability-matrix row;
- current deployment status;
- selected reuse decision;
- duplicate-development risk;
- prior local research consulted, when and only when upstream is absent or insufficient;
- rollback, retirement, or upstream-contribution plan for any overlap.

Missing evidence blocks implementation and validation.

## `BUILD_LOCAL_EXCEPTION` conditions

A local build exception is allowed only when all conditions are true:

1. Original upstream feature descriptions were searched.
2. Pinned upstream source was searched.
3. Upstream UI, API, service, data model, tests, configuration, and relevant history were searched.
4. The capability is absent or has an unacceptable security defect.
5. Configuration cannot solve the requirement.
6. A small upstream patch cannot solve the requirement.
7. An operations wrapper cannot solve the requirement.
8. Existing local and archived research was reviewed for reuse.
9. There is explicit user value.
10. A separate accepted ADR is referenced.
11. There is a retirement or upstream-contribution plan.
12. The project owner explicitly authorizes the exception.

If any condition is missing, local implementation is forbidden.

## Automatic reply executor rule

Two automatic-reply send executors must never run at the same time. The formal automatic-reply executor must be explicit in `specs/SYSTEM_ARCHITECTURE.md`. After this change, the target formal executor is the upstream native automatic-reply service; local CHG-0010 worker execution is deprecated and must not be expanded.

## Change entry gate

A Change without a capability matrix reference, upstream feature-description evidence, pinned upstream evidence, native workflow, existing local implementation search, reuse decision, duplicate implementation risk assessment, component owner, and retirement plan for overlapping local code cannot enter `IMPLEMENTING` or `VERIFYING`.
