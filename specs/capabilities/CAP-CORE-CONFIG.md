# CAP-CORE-CONFIG

## Purpose

Provide the single typed configuration boundary for the modular-monolith Core without reading or storing real platform secrets.

## Current implementation change

- Active change: CHG-0002-core-application.
- Registry status during implementation: implementing.
- Final status after acceptance: verified.

## Registered implementation paths

- `app/xianyu_system/core/config.py`
- `app/xianyu_system/application.py`

## Registered verification paths

- `tests/unit/test_config.py`
- `tests/unit/test_application_factory.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_core_runtime.py`
- `tests/contract/test_distribution.py`
- `tests/contract/test_security_boundary.py`
- `changes/active/CHG-0002-core-application/tests/test_acceptance.py`

## Requirements

- Provide a typed Pydantic Settings configuration entry point.
- Support environment variables and explicit test overrides.
- Avoid module-import side effects.
- Do not read real Cookie, Token, Secret, Password, browser profile, or platform account credentials.
- Keep configuration replaceable for repeated application creation in tests.

## T5 implementation decisions

- Implementation file: `app/xianyu_system/core/config.py`.
- Settings type: `ApplicationSettings`.
- Environment prefix: `XIANYU_`.
- Explicit constructor values override environment values.
- Environment values override defaults.
- Settings are immutable.
- `.env` files are not automatically loaded.
- No secret-bearing platform fields exist in CHG-0002 Core settings.
- Application factory stores resolved settings in `app.state.settings`.
- Capability remains `implementing` until full CHG-0002 verification.

## T13 registry decision

- Registry implementation and verification paths now point to exact repository files.
- Paths are repository-relative, deterministic, and verified to exist.
- The capability remains `implementing`.
- `active_change` remains `CHG-0002-core-application`.
- `last_verified_commit` remains unset until T14 complete verification.
- T13 does not change runtime behavior or configuration fields.

## Acceptance criteria

- Configuration can be constructed for local default usage.
- Tests can override database path and other runtime settings without touching real files.
- Sensitive field names are not logged in plaintext.
- `CAP-CORE-CONFIG` is updated to verified only after CHG-0002 implementation and validation are complete.

## Security boundaries

- Do not hold real Cookie, Token, Secret, Password, customer data, or browser credentials.
- Do not bypass platform verification or risk controls.
- Do not access real external accounts.

## Out of scope

- Real external platform configuration.
- Secret manager integration.
- Production deployment configuration.
- Xianyu, WeCom, or AI provider credentials.
