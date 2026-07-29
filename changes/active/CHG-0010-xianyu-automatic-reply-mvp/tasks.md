Change ID: CHG-0010-xianyu-automatic-reply-mvp
Status: IMPLEMENTING
# Tasks

- [x] T1 Record owner direction correction and automatic-reply scope
- [x] T2 Define deterministic autoreply configuration and safety gates
- [x] T3 Implement autoreply worker, state, idempotency, and CLI
- [x] T4 Add unit, security, and acceptance coverage
- [x] T5 Add quickstart documentation
- [x] T6 Run complete local verification
- [x] T7 Execute supervised real automatic reply validation
- [x] T8 Publish PR and complete final administration

## Current progress

Completed tasks: 8 / 8
Next task: None

## T1 evidence

The project owner explicitly rejected the manual operator workflow direction and authorized a deterministic automatic reply MVP for a dedicated test account. CHG-0009 PR #10 was merged before this change began, CHG-0009 was archived, and CHG-0010 starts from latest `origin/main`.


## T2-T5 evidence

Deterministic local autoreply configuration is implemented with disabled defaults, dedicated-test mode, account allowlist, ordered exact/contains rules, optional fallback, cooldowns, hourly limits, startup watermark, local state, and credential redaction. The worker is implemented under `app/xianyu_system/worker/autoreply/`, reuses CHG-0009 Wrapper sends and listener control, and exposes `doctor`, `run`, `start`, `status`, and `stop`. Example configuration is committed at `config/autoreply.example.yaml`; the real local config remains under ignored `.local/autoreply.yaml`. Unit coverage in `tests/unit/test_autoreply.py` covers 30 automatic reply safety and process boundaries. Quickstart documentation is available at `docs/XIANYU_AUTOREPLY_QUICKSTART.md`.


## T6 evidence

Complete local verification passed before live supervised validation:

- `python -m pytest tests/unit/test_autoreply.py -q` passed with 30 tests.
- `python -m ruff check app/xianyu_system/worker/autoreply tests/unit/test_autoreply.py app/xianyu_system/__main__.py` passed.
- `python -m mypy app/xianyu_system/worker/autoreply app/xianyu_system/__main__.py tests/unit/test_autoreply.py` passed.
- `python scripts/verify_repository.py` passed with 561 tests.
- `python scripts/generate_state.py`, `python scripts/project_context.py`, `python scripts/validate_change.py`, `python -m pytest -W error`, `python -m ruff check .`, `python scripts/security_scan.py`, `python -m mypy app/xianyu_system`, and `git diff --check` passed.
- `python -m xianyu_system autoreply --help`, `python -m xianyu_system autoreply doctor`, and `python -m xianyu_system autoreply status` passed with default disabled configuration and no secret output.


## T7 evidence

Supervised live automatic reply validation passed on the dedicated test account without per-message manual selection, reply typing, or SEND confirmation:

- The local test configuration was enabled only under `.local/autoreply.yaml`, which is ignored by Git.
- `python -m xianyu_system autoreply start --config .local/autoreply.yaml` started one managed local worker and reused the CHG-0009 listener boundary.
- Before the owner sent the test message, `doctor` and `status` reported healthy backend, connected listener, logged-in account, and no blocked reason.
- After the owner sent exactly one inbound test message, the worker matched rule `chg-0010-live-test`, sent one automatic ACK, and recorded `SUCCESS`.
- Observed counts: inbound match count = 1, rule match count = 1, automatic reply result = SUCCESS, platform ACK count = 1, duplicate reply count = 0, extra reply count = 0, historical messages replied = 0, other conversations affected = 0.
- A second polling window kept platform ACK count at 1, confirming idempotency prevented duplicate sends.
- The worker was stopped, its owned listener was stopped, and local test config was restored to `enabled: false`.
- No credentials, full account identifiers, full conversation identifiers, Cookie, Token, Session, or Authorization values were printed or committed.


## T8 evidence

Final PR administration completed for CHG-0010:

- Draft PR #11 was created: `https://github.com/yuanweizhang94-crypto/XIANYU/pull/11`.
- The branch `feat/CHG-0010-xianyu-automatic-reply-mvp` was pushed to GitHub.
- The PR documents automatic reply behavior without per-message manual selection, deterministic rule configuration, startup watermark, idempotency, UNKNOWN no-retry handling, cooldowns, rate limits, credential boundaries, background process management, live supervised validation, disabled default, and non-goals.
- CHG-0010 remains unmerged. No auto-merge was enabled. No CHG-0011 was created.
