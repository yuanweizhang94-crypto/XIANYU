# CHG-0003 Design

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Design state

CHG-0003 is approved for controlled, task-by-task execution.

No runtime account design or implementation has been approved yet.

T2-T5 must finalize the terminology, security, persistence, migration, module ownership, and testing boundaries before T6 may begin.

## Proposed boundary

The future account boundary may describe:

- Account identity metadata.
- Profile isolation metadata.
- Profile lifecycle states.
- Synthetic import validation.
- Permission and risk-state handling.
- Secret-reference interfaces without storing real secret values.
- Fail-closed behavior.

## Required decisions before runtime implementation

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

## Execution boundary

The project-owner approval completes T1 only.

T2 is the next executable task.

T2 must be performed in a separate execution.

No runtime implementation may begin before T2-T5 are completed and all approved decisions are recorded in this document.
