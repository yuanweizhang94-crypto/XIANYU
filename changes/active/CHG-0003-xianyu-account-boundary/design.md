# CHG-0003 Design

Status: DRAFT
Change ID: CHG-0003-xianyu-account-boundary

## Design state

No runtime design is approved.

This document records questions and constraints for later review.

## Proposed boundary

The future account boundary may describe:

- Account identity metadata.
- Profile isolation metadata.
- Profile lifecycle states.
- Synthetic import validation.
- Permission and risk-state handling.
- Secret-reference interfaces without storing real secret values.
- Fail-closed behavior.

## Required decisions before approval

- Exact account and Profile terminology.
- Whether profile metadata is persistent.
- Whether encryption or operating-system credential storage is needed.
- Allowed import formats.
- Account state transitions.
- Error and audit behavior.
- API and worker ownership boundaries.
- Database and migration requirements.
- Testing strategy.

## Security constraints

- Never commit real credentials.
- Never load real browser profiles in tests.
- Never bypass platform verification or risk controls.
- Never guess missing account state.
- Never log Cookie, Token, Secret, Password, authorization data, or customer data.
- Use synthetic fixtures only.

## Current implementation

None.

## Approval boundary

No implementation task may begin until this change is explicitly approved.
