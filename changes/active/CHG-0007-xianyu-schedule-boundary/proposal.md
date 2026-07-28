# CHG-0007 Proposal

Status: APPROVED
Change ID: CHG-0007-xianyu-schedule-boundary

## Purpose

Create a narrow local deterministic scheduling boundary for Xianyu publish requests.

## Draft posture

This DRAFT exists only for governance and review input. DRAFT status does not authorize T1 or Runtime implementation.

## Initial scope

The proposed scope is a one-time schedule capability for immediate or specified UTC execution. It may persist schedule state, validate deterministic inputs, support idempotency and cancellation, claim dispatch atomically, and call the existing local Publish boundary explicitly.

## Explicit exclusions

- No Schedule package is created by DRAFT alone.
- No Migration is created by DRAFT alone.
- Registry is not modified by DRAFT.
- Core scheduler is not modified.
- No real Xianyu platform access.
- No recurring schedule, CRON, interval, calendar, holiday, or user timezone UI.
- No Credential, Cookie, Token, Secret, Password, Session, or browser Profile handling.
- No browser automation or Playwright.
- No WeCom, AI, operations console, Redis, Celery, or external queue.

## Approval requirement

Entering APPROVED requires explicit project-owner authorization. Runtime work remains blocked until the relevant ordered tasks approve its boundaries.


## T1 approval record

This instruction is the explicit project-owner authorization for CHG-0007 T1 through T9, executed in order.

T6 may implement only the approved local deterministic Schedule boundary. It does not authorize real Xianyu access, browser automation, Playwright, Credential handling, WeCom, AI, operations-console work, recurring schedules, Redis, Celery, or external queues.

Merge, archive, and branch deletion remain gated by the later exact CI, PR, merge, post-merge, and archive checks in this change.


## T2 terminology decision

Schedule Request means a local request to run exactly one Publish boundary call either immediately or at an explicit UTC run_at time. Trigger is IMMEDIATE or RUN_AT_UTC. Schedule Decision is the deterministic validation result. Dispatch is the local atomic claim of a due schedule. UTC is mandatory for all stored instants. Grace window is a finite misfire allowance in seconds; outside grace the item becomes MISFIRED and is not published. Cancellation is a terminal local state before claim.
