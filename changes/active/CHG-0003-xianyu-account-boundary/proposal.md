# CHG-0003 Proposal

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Purpose

Prepare a formally reviewable boundary for Xianyu account and Profile isolation.

## Target capability

- CAP-XY-ACCOUNT

## Current authorization

The project owner approved CHG-0003 for controlled, one-task-at-a-time execution.

T1 and T2 are complete.

The account and Profile isolation terminology is finalized.

T3 is the next executable task and must be performed separately.

No runtime implementation, real account access, Credential Reference implementation, Session Material handling, browser integration, capability binding, Ready-for-review, auto-merge, or merge is authorized.

## Goals

- Define account and Profile isolation terminology.
- Define synthetic configuration and validation boundaries.
- Define security, permission, lifecycle, and failure behavior.
- Define future acceptance criteria before runtime implementation.
- Preserve fail-closed behavior when account state or permission is uncertain.

## T2 terminology outcome

- Platform Account means the real external account.
- Account Reference means the repository-owned non-secret logical reference.
- Profile means the local isolation boundary and does not mean a browser profile.
- Profile Identifier is the canonical local identity.
- Account Alias is display-only metadata.
- External Account Identifier is optional untrusted reference metadata.
- Credential Reference is an opaque reference and never a secret value.
- Session Material is sensitive and remains outside the approved boundary.
- Profile-scoped State belongs to exactly one Profile.
- Isolation Boundary prohibits cross-Profile mutable-state or secret reuse.
- Synthetic Fixture is the only allowed test data category.

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
- No runtime implementation during the T2 terminology transition.
- No runtime implementation before T3-T5 have been completed and their decisions have been formally recorded.

## Execution boundary

Only one unfinished task may be executed at a time.

This execution completes T2 only.

T3 must not begin in the same execution.

Runtime implementation remains prohibited until T3-T5 are complete and all approved decisions are recorded.
