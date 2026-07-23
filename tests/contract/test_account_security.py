from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import clear_mappers

from xianyu_system.core.database import Base, dispose_database, initialize_database

ROOT = Path(__file__).resolve().parents[2]
ACCOUNT_ROOT = ROOT / "app" / "xianyu_system" / "worker" / "account"


@pytest.fixture(scope="module", autouse=True)
def cleanup_account_metadata_after_module() -> object:
    yield
    clear_mappers()
    if "xianyu_account_profiles" in Base.metadata.tables:
        Base.metadata.remove(Base.metadata.tables["xianyu_account_profiles"])
    for module_name in [
        "xianyu_system.worker.account",
        "xianyu_system.worker.account.persistence",
        "xianyu_system.worker.account.service",
    ]:
        sys.modules.pop(module_name, None)


def test_public_account_package_exposes_only_approved_non_persistence_surface() -> None:
    import xianyu_system.worker.account as account_package

    public_names = set(account_package.__all__)
    assert {
        "AccountReference",
        "AccountService",
        "Profile",
        "ProfileLifecycleStatus",
        "AccountBoundaryError",
        "InvalidAccountInput",
        "ProfileNotFound",
        "DuplicateAccountOwnership",
        "InvalidLifecycleTransition",
        "StaleProfileUpdate",
        "AccountPersistenceError",
    } <= public_names
    forbidden = {
        "_AccountProfileRecord",
        "account_profiles_table",
        "AccountProfileRepository",
        "Session",
        "Table",
        "Column",
        "MigrationContext",
    }
    assert public_names.isdisjoint(forbidden)
    for name in forbidden:
        assert not hasattr(account_package, name)


def test_account_sources_contain_no_external_integration_or_secret_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            ACCOUNT_ROOT / "__init__.py",
            ACCOUNT_ROOT / "domain.py",
            ACCOUNT_ROOT / "persistence.py",
            ACCOUNT_ROOT / "service.py",
        ]
    )
    forbidden_tokens = [
        "fastapi",
        "apirouter",
        "httpx",
        "requests",
        "playwright",
        "selenium",
        "browser profile",
        "cookie",
        "token",
        "password",
        "secret material",
        "secure storage",
        "credential provider",
        "backgroundscheduler",
        "create_engine",
        "sessionmaker(",
        ".commit(",
    ]
    for token in forbidden_tokens:
        assert token not in combined


def test_sanitized_service_errors_do_not_expose_reference_values_or_sql(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resources = initialize_database(tmp_path / "account-security-sanitized.db")
    try:
        from xianyu_system.worker.account import (
            AccountPersistenceError,
            AccountService,
            DuplicateAccountOwnership,
        )
        from xianyu_system.worker.account.persistence import AccountProfileRepository
        from xianyu_system.worker.account.persistence import account_profiles_table

        account_profiles_table.create(resources.engine)
        service = AccountService(resources.session_factory)
        alpha = service.create_profile(account_alias="synthetic-profile-alpha")
        beta = service.create_profile(
            account_alias="synthetic-profile-beta",
            external_account_identifier="synthetic-external-reference-beta",
        )

        with pytest.raises(DuplicateAccountOwnership) as duplicate_error:
            service.set_external_account_identifier(
                alpha.profile_id,
                external_account_identifier="synthetic-external-reference-beta",
                expected_version=alpha.row_version,
            )
        assert "synthetic-external-reference-beta" not in str(duplicate_error.value)

        def raise_sqlalchemy_error(
            self: AccountProfileRepository,
            *args: object,
            **kwargs: object,
        ) -> object:
            raise SQLAlchemyError(
                "SELECT synthetic-credential-reference-alpha FROM browser_cookie_table"
            )

        monkeypatch.setattr(AccountProfileRepository, "save", raise_sqlalchemy_error)
        with pytest.raises(AccountPersistenceError) as persistence_error:
            service.rename_profile(
                beta.profile_id,
                account_alias="synthetic-profile-mutated",
                expected_version=beta.row_version,
            )

        error_text = str(persistence_error.value)
        assert "SELECT" not in error_text
        assert "browser_cookie_table" not in error_text
        assert "synthetic-credential-reference-alpha" not in error_text
        assert persistence_error.value.__cause__ is None
    finally:
        dispose_database(resources)


def test_account_tests_and_change_docs_use_only_synthetic_non_secret_fixtures() -> None:
    checked_paths = [
        ROOT / "tests" / "unit" / "test_account_domain.py",
        ROOT / "tests" / "unit" / "test_account_service.py",
        ROOT / "tests" / "contract" / "test_account_persistence.py",
        ROOT / "tests" / "contract" / "test_account_security.py",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in checked_paths)

    forbidden_literals = [
        "cookie" + "=",
        "token" + "=",
        "password" + "=",
        "authorization" + ":",
        "api" + "_key",
        "api" + "-key",
        "customer" + "@example.com",
        "phone" + "_number",
        "user" + "-data-dir",
        "chrome" + " profile",
    ]
    for literal in forbidden_literals:
        assert literal not in combined
    assert "synthetic-profile-alpha" in combined
    assert "synthetic-credential-reference-alpha" in combined
