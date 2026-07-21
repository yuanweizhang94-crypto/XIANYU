# CAP-CORE-CONFIG

## Purpose

Provide the single typed configuration boundary for the modular-monolith Core without reading or storing real platform secrets.

## Current implementation change

- Active change: CHG-0002-core-application.
- Registry status during implementation: implementing.
- Final status after acceptance: verified.

## Planned implementation paths

- `app/xianyu_system/core/config.py`
- `app/xianyu_system/application.py` for dependency injection into the application factory.

## Planned test paths

- `tests/unit/` for configuration parsing and override behavior.
- `changes/active/CHG-0002-core-application/tests/` for CHG-0002 acceptance coverage.

## Requirements

- Provide a typed Pydantic Settings configuration entry point.
- Support environment variables and explicit test overrides.
- Avoid module-import side effects.
- Do not read real Cookie, Token, Secret, Password, browser profile, or platform account credentials.
- Keep configuration replaceable for repeated application creation in tests.

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
