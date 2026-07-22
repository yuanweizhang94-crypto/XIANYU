# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T3 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED in proposal, design, tasks, and acceptance.

3. T1, T2, and T3 are complete.

4. T4-T9 remain incomplete.

5. generated/PROJECT_STATE.json reports three completed tasks.

6. generated/PROJECT_STATE.json reports T4 as next_task.

7. All T2 canonical terminology and invariants remain intact.

8. Secret Material is formally classified and prohibited from repository and ordinary application persistence.

9. Sensitive Non-secret Metadata is formally classified.

10. Secure Storage Boundary requirements are defined without choosing or implementing a provider.

11. Credential References are Profile-owned, opaque, and secret-free.

12. Cross-Profile Credential Reference reuse is prohibited.

13. Future resolution requires explicit Profile Identifier, Credential Reference, purpose, authorization, and risk decision.

14. Credential Resolution Status values are defined.

15. Operation Authorization Status values are defined.

16. Only RESOLVED plus AUTHORIZED permits a future operation.

17. UNKNOWN, MISSING, UNAVAILABLE, INVALID, EXPIRED, REVOKED, VERIFICATION_REQUIRED, PERMISSION_DENIED, and RISK_BLOCKED fail closed.

18. Platform verification and risk controls may not be bypassed.

19. Secret Material is prohibited from logs, errors, audit events, traces, metrics, snapshots, URLs, command-line arguments, environment variables, databases, migrations, and tests.

20. Full Credential References and External Account Identifiers are prohibited from logs.

21. Provider errors must be sanitized before crossing the provider boundary.

22. Rotation, revocation, expiration, and replacement may not cause implicit fallback or cross-Profile reuse.

23. Only Synthetic Fixtures are allowed in tests.

24. T4 persistence and migration decisions remain deferred.

25. T5 provider, module, worker, API, process, and runtime ownership decisions remain deferred.

26. T6 runtime implementation remains deferred.

27. CAP-XY-ACCOUNT remains planned and unbound.

28. CAP-XY-ACCOUNT retains no implementation or test evidence paths.

29. No runtime, API, contract, migration, dependency, CI, registry, capability specification, archived change, or permanent test file is modified.

30. No real account, credential, Cookie, Token, password, browser directory, customer data, or Session Material is added.

31. PR #3 remains Draft, open, and unmerged.

32. Auto-merge remains disabled.

33. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1, T2, and T3 are complete.

T4 is the next executable task and must be performed separately.

This execution does not authorize persistence, database changes, migrations, provider selection, provider integration, API changes, worker changes, browser integration, account access, Secret Material handling, capability binding, Ready-for-review, auto-merge, or merge.
