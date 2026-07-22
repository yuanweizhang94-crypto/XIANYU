# CHG-0003 Proposal

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Purpose

Prepare a formally reviewable boundary for Xianyu account and Profile isolation.

## Target capability

- CAP-XY-ACCOUNT

## Current authorization

The project owner explicitly approved CHG-0003 for controlled, task-by-task execution.

T1 is complete.

T2 is the next executable task, but T2 must be performed in a later, separate execution.

This approval does not authorize runtime implementation, real account access, Cookie or Token handling, browser Profile loading, external platform access, capability binding, Ready-for-review, or merge.

## Goals

- Define account and Profile isolation terminology.
- Define synthetic configuration and validation boundaries.
- Define security, permission, lifecycle, and failure behavior.
- Define future acceptance criteria before runtime implementation.
- Preserve fail-closed behavior when account state or permission is uncertain.

## Non-goals

- No real Xianyu login.
- No real Cookie, Token, Secret, QR code, SMS code, account, customer, or browser data.
- No browser automation.
- No Playwright or Selenium.
- No runtime account worker.
- No database business tables or migrations.
- No API route.
- No external network request.
- No registry capability binding.
- No runtime implementation during the T1 approval transition.
- No runtime implementation before T2-T5 have been completed and their decisions have been formally recorded.

## Execution boundary

Only one unfinished task may be executed at a time.

This approval transition completes T1 only.

T2 must not begin in the same execution.

Runtime implementation remains prohibited until T2-T5 have finalized and approved the terminology, security, persistence, migration, module ownership, and testing boundaries.
