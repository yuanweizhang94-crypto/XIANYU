# CAP-CORE-CONFIG

## Purpose

Provide the single typed configuration boundary for the modular-monolith Core without reading or storing real platform secrets.

## Current implementation change

- Active change: none; verification recorded by CHG-0002-core-application T14.
- Registry status: verified.
- Last verified commit: `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.

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
- `changes/archive/CHG-0002-core-application/tests/test_acceptance.py`

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
- Capability remained `implementing` until full CHG-0002 verification passed in T14.

## T13 registry decision

- Registry implementation and verification paths now point to exact repository files.
- Paths are repository-relative, deterministic, and verified to exist.
- The capability remained `implementing` until T14 verification.
- `active_change` remained `CHG-0002-core-application` until T14 verification.
- `last_verified_commit` remained unset until T14 complete verification.
- T13 does not change runtime behavior or configuration fields.

## T14 verification decision

- Complete local verification passed for candidate commit `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.
- The registry status is now `verified`.
- The capability is no longer bound through `active_change`.
- `last_verified_commit` is `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.
- The verified scope is limited to typed Core configuration, safe environment overrides, application-factory injection, and the registered verification paths.
- No external platform credentials, secret manager integration, or production deployment configuration is included.

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
