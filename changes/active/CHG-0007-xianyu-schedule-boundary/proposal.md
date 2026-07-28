# CHG-0007 Proposal

Status: DRAFT
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
