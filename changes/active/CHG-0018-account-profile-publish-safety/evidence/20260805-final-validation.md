# CHG-0018 Final Validation Evidence

Change ID: CHG-0018-account-profile-publish-safety
Status: IMPLEMENTING
Evidence date: 2026-08-05

## Scope

- P0: account credential safety and false-disable prevention.
- P1-P4: account persistent Profile publish readiness, Profile initialization boundaries, shared read-only preflight, and canonical browser lock usage.
- Production operations executed: none.
- PR #26 state changed: no.
- CHG-0017 T17 executed: no.
- Archive or merge executed: no.

## Patch artifact

- Path: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`
- SHA256: `8FA58C8F2674EE7A16C36689F962612DC1619C211ACAA390105778A64CD20EEE`
- Applies after: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0017-reply-identity-allowlist.patch`
- Patch parse check: passed with `git apply --numstat --unidiff-zero`.
- Patch staged-base apply check: passed with `git apply --check --cached --whitespace=error-all --unidiff-zero`.
- Patch diff check: passed for the CHG-0018 patch artifact.

## Upstream tests

- `python -m py_compile backend-web\app\services\xianyu_publisher.py common\services\xianyu_publish_service.py common\services\publish_execution_service.py`: passed.
- `python -m pytest tests/test_chg0018_credential_safety.py tests/test_chg0018_profile_publish_readiness.py -q`: passed.
- `python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0017_reply_allowlist.py tests/test_chg0017_ai_prompt_validation.py tests/test_chg0017_gemini_response_parser.py tests/test_chg0018_credential_safety.py tests/test_chg0018_profile_publish_readiness.py -q`: 68 passed.
- `npm run build`: passed.
- `npm run lint`: command exists, but no ESLint config file exists in the upstream frontend checkout. Recorded as a non-blocking upstream tooling gap.

## Repository validation

- `python -m pytest changes\active\CHG-0018-account-profile-publish-safety\tests\test_acceptance.py -q`: 7 passed.
- `python scripts/validate_change.py`: passed.
- `python scripts/verify_repository.py`: 594 passed, repository verification passed.
- `python scripts/detect_duplicate_capabilities.py`: passed.
- `python scripts/security_scan.py`: passed.
- `python -m ruff check .`: passed.
- `python -m mypy scripts app`: passed.
- `python -m pip check`: passed.
- `python -m pytest --collect-only -q`: 594 tests collected.
- `git diff --check`: passed with Windows line-ending warnings only.
- Known warning baseline: Starlette/httpx deprecation warning from FastAPI TestClient.

## Safety

- Raw password values recorded in evidence: no.
- Cookie, Token, API key, account identifier, customer message, item identifier, or browser Profile recorded in evidence: no.
- New database table, service, queue, Browser Broker, sender, Token implementation, or WebSocket implementation added: no.
- Real account operation, QR login, password login, automatic reply, message send, or true publish executed: no.
