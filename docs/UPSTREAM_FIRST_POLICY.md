# Upstream First Policy

Change: CHG-0011-upstream-first-product-direction-freeze

## Mandatory search before implementation

Before any feature implementation enters `IMPLEMENTING`, the change owner must search both:

1. `D:/xianyu` current implementation, tests, specs, ADRs, scripts, and active/archive changes.
2. `D:/xianyu-upstream-pilot` pinned upstream implementation at the recorded SHA.

The search must cover UI, API, service, data model, worker, scheduler, and frontend evidence when relevant.

## Decision hierarchy

1. `ADOPT_UPSTREAM`: use the pinned upstream native capability directly.
2. `CONFIGURE_UPSTREAM`: configure the pinned upstream native capability without source changes.
3. `PATCH_UPSTREAM`: make a small auditable upstream patch or fork when native behavior is nearly sufficient.
4. `WRAP_FOR_OPERATIONS`: add governance, safety, validation, monitoring, backup, restore, or upgrade orchestration around upstream.
5. `BUILD_LOCAL_EXCEPTION`: last resort only.

## `BUILD_LOCAL_EXCEPTION` conditions

A local build exception is allowed only when all conditions are true:

1. Pinned upstream source was searched.
2. Upstream UI, API, service, and data model were searched.
3. The capability is absent or has an unacceptable security defect.
4. Configuration cannot solve the requirement.
5. A small upstream patch cannot solve the requirement.
6. An operations wrapper cannot solve the requirement.
7. There is explicit user value.
8. A separate accepted ADR is referenced.
9. There is a retirement or upstream-contribution plan.
10. The project owner explicitly authorizes the exception.

If any condition is missing, local implementation is forbidden.

## Automatic reply executor rule

Two automatic-reply send executors must never run at the same time. The formal automatic-reply executor must be explicit in `specs/SYSTEM_ARCHITECTURE.md`. After this change, the target formal executor is the upstream native automatic-reply service; local CHG-0010 worker execution is deprecated and must not be expanded.

## Change entry gate

A Change without a capability matrix reference, pinned upstream evidence, existing local implementation search, reuse decision, duplicate implementation risk assessment, component owner, and retirement plan for overlapping local code cannot enter `IMPLEMENTING`.
