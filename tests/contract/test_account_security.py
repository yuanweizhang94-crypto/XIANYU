from __future__ import annotations

import ast
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCOUNT_ROOT = ROOT / "app" / "xianyu_system" / "worker" / "account"
ACCOUNT_SOURCE_PATHS = [
    ACCOUNT_ROOT / "__init__.py",
    ACCOUNT_ROOT / "domain.py",
    ACCOUNT_ROOT / "persistence.py",
    ACCOUNT_ROOT / "service.py",
    ROOT / "migrations" / "versions" / "0002_xianyu_account_boundary.py",
]
ACCOUNT_TEST_PATHS = [
    ROOT / "tests" / "unit" / "test_account_domain.py",
    ROOT / "tests" / "unit" / "test_account_service.py",
    ROOT / "tests" / "contract" / "test_account_persistence.py",
    ROOT / "tests" / "contract" / "test_account_security.py",
]


def run_isolated_account_python(source: str) -> None:
    isolated_source = "\n".join(
        [
            "import sys",
            "from pathlib import Path",
            f"ROOT = Path({str(ROOT)!r})",
            "sys.path.insert(0, str(ROOT / 'app'))",
            textwrap.dedent(source).strip(),
        ]
    )
    result = subprocess.run(
        [sys.executable, "-c", isolated_source],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_account_public_surface_excludes_persistence_internals() -> None:
    run_isolated_account_python(
        """
        import xianyu_system.worker.account as account_package

        public_names = set(account_package.__all__)
        assert {
            'AccountReference',
            'AccountService',
            'Profile',
            'ProfileLifecycleStatus',
            'AccountBoundaryError',
            'InvalidAccountInput',
            'ProfileNotFound',
            'DuplicateAccountOwnership',
            'InvalidLifecycleTransition',
            'StaleProfileUpdate',
            'AccountPersistenceError',
        } <= public_names
        forbidden = {
            '_AccountProfileRecord',
            'account_profiles_table',
            'AccountProfileRepository',
            'Session',
            'Table',
            'Column',
            'Engine',
            'sessionmaker',
            'MigrationContext',
            'upgrade',
            'downgrade',
        }
        assert public_names.isdisjoint(forbidden)
        for name in forbidden:
            assert not hasattr(account_package, name)
        """
    )


def test_account_sources_have_no_external_integration_or_secret_storage() -> None:
    forbidden_import_roots = {
        "fastapi",
        "requests",
        "httpx",
        "aiohttp",
        "selenium",
        "playwright",
        "keyring",
        "win32cred",
        "subprocess",
        "socket",
    }
    forbidden_call_names = {
        "APIRouter",
        "BackgroundScheduler",
        "Popen",
        "run",
        "create_connection",
    }
    forbidden_attribute_names = {
        "connect",
        "user_data_dir",
        "credential_provider",
        "secure_storage",
    }

    for source_path in ACCOUNT_SOURCE_PATHS:
        tree = ast.parse(source_path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name.split(".", 1)[0] for alias in node.names}
                assert imported.isdisjoint(forbidden_import_roots)
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                assert node.module.split(".", 1)[0] not in forbidden_import_roots
            if isinstance(node, ast.Call):
                function = node.func
                if isinstance(function, ast.Name):
                    assert function.id not in forbidden_call_names
                if isinstance(function, ast.Attribute):
                    assert function.attr not in forbidden_call_names
            if isinstance(node, ast.Attribute):
                assert node.attr not in forbidden_attribute_names

    combined_runtime_source = "\n".join(
        path.read_text(encoding="utf-8-sig").lower() for path in ACCOUNT_SOURCE_PATHS
    )
    for forbidden_text in [
        "browser profile",
        "chrome user-data",
        "credential provider",
        "secure storage provider",
        "scheduler job",
        "cookie read",
        "token read",
        "password read",
        "https://",
        "http://",
    ]:
        assert forbidden_text not in combined_runtime_source

    combined_test_source = "\n".join(
        path.read_text(encoding="utf-8-sig").lower() for path in ACCOUNT_TEST_PATHS
    )
    for forbidden_literal in [
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
    ]:
        assert forbidden_literal not in combined_test_source
    assert "synthetic-profile" in combined_test_source
    assert "synthetic-external-reference" in combined_test_source
    assert "synthetic-credential-reference" in combined_test_source


def test_account_operations_make_no_network_browser_or_credential_store_calls(
    tmp_path: Path,
) -> None:
    run_isolated_account_python(
        f"""
        import socket
        import subprocess
        from pathlib import Path

        from xianyu_system.core.database import dispose_database, initialize_database
        from xianyu_system.worker.account import AccountService, ProfileLifecycleStatus
        from xianyu_system.worker.account.persistence import account_profiles_table

        blocked_calls = []

        def fail_external_call(name):
            def blocked(*args, **kwargs):
                blocked_calls.append(name)
                raise AssertionError(f'Unexpected external call: {{name}}')

            return blocked

        def blocked_home(cls):
            blocked_calls.append('Path.home')
            raise AssertionError('Unexpected external call: Path.home')

        socket.create_connection = fail_external_call('socket.create_connection')
        socket.socket = fail_external_call('socket.socket')
        subprocess.run = fail_external_call('subprocess.run')
        subprocess.Popen = fail_external_call('subprocess.Popen')
        Path.home = classmethod(blocked_home)

        resources = initialize_database(Path({str(tmp_path / 'account-security-runtime.db')!r}))
        try:
            account_profiles_table.create(resources.engine)
            service = AccountService(resources.session_factory)

            profile = service.create_profile(account_alias='synthetic-profile-runtime')
            assert service.get_profile(profile.profile_id) == profile
            assert service.list_profiles() == (profile,)

            renamed = service.rename_profile(
                profile.profile_id,
                account_alias='synthetic-profile-runtime-renamed',
                expected_version=profile.row_version,
            )
            with_external = service.set_external_account_identifier(
                profile.profile_id,
                external_account_identifier='synthetic-external-reference-runtime',
                expected_version=renamed.row_version,
            )
            cleared_external = service.set_external_account_identifier(
                profile.profile_id,
                external_account_identifier=None,
                expected_version=with_external.row_version,
            )
            with_credential = service.set_credential_reference(
                profile.profile_id,
                credential_reference='synthetic-credential-reference-runtime',
                expected_version=cleared_external.row_version,
            )
            cleared_credential = service.set_credential_reference(
                profile.profile_id,
                credential_reference=None,
                expected_version=with_credential.row_version,
            )
            enabled = service.set_lifecycle_status(
                profile.profile_id,
                lifecycle_status=ProfileLifecycleStatus.ENABLED,
                expected_version=cleared_credential.row_version,
            )
            disabled = service.set_lifecycle_status(
                profile.profile_id,
                lifecycle_status=ProfileLifecycleStatus.DISABLED,
                expected_version=enabled.row_version,
            )
            reenabled = service.set_lifecycle_status(
                profile.profile_id,
                lifecycle_status=ProfileLifecycleStatus.ENABLED,
                expected_version=disabled.row_version,
            )

            assert reenabled.lifecycle_status is ProfileLifecycleStatus.ENABLED
            assert reenabled.account_alias == 'synthetic-profile-runtime-renamed'
            assert blocked_calls == []
        finally:
            dispose_database(resources)
        """
    )


def test_account_errors_do_not_expose_sensitive_reference_values(tmp_path: Path) -> None:
    run_isolated_account_python(
        f"""
        from pathlib import Path

        import pytest
        from sqlalchemy.exc import SQLAlchemyError

        from xianyu_system.core.database import dispose_database, initialize_database
        from xianyu_system.worker.account import (
            AccountPersistenceError,
            AccountService,
            DuplicateAccountOwnership,
        )
        from xianyu_system.worker.account.persistence import AccountProfileRepository
        from xianyu_system.worker.account.persistence import account_profiles_table

        resources = initialize_database(Path({str(tmp_path / 'account-security-sanitized.db')!r}))
        try:
            account_profiles_table.create(resources.engine)
            service = AccountService(resources.session_factory)
            alpha = service.create_profile(account_alias='synthetic-profile-alpha')
            beta = service.create_profile(
                account_alias='synthetic-profile-beta',
                external_account_identifier='synthetic-sensitive-external-reference',
            )
            beta_with_credential = service.set_credential_reference(
                beta.profile_id,
                credential_reference='synthetic-sensitive-credential-reference',
                expected_version=beta.row_version,
            )

            with pytest.raises(DuplicateAccountOwnership) as duplicate_external:
                service.set_external_account_identifier(
                    alpha.profile_id,
                    external_account_identifier='synthetic-sensitive-external-reference',
                    expected_version=alpha.row_version,
                )
            assert 'synthetic-sensitive-external-reference' not in str(
                duplicate_external.value
            )
            assert service.get_profile(alpha.profile_id) == alpha

            with pytest.raises(DuplicateAccountOwnership) as duplicate_credential:
                service.set_credential_reference(
                    alpha.profile_id,
                    credential_reference='synthetic-sensitive-credential-reference',
                    expected_version=alpha.row_version,
                )
            assert 'synthetic-sensitive-credential-reference' not in str(
                duplicate_credential.value
            )
            assert service.get_profile(alpha.profile_id) == alpha

            def raise_sqlalchemy_error(self, *args, **kwargs):
                raise SQLAlchemyError(
                    'SELECT synthetic-sensitive-credential-reference '
                    'FROM browser_cookie_table'
                )

            AccountProfileRepository.save = raise_sqlalchemy_error
            with pytest.raises(AccountPersistenceError) as persistence_error:
                service.rename_profile(
                    beta.profile_id,
                    account_alias='synthetic-profile-mutated',
                    expected_version=beta_with_credential.row_version,
                )

            error_text = str(persistence_error.value)
            assert 'SELECT' not in error_text
            assert 'browser_cookie_table' not in error_text
            assert 'synthetic-sensitive-credential-reference' not in error_text
            assert 'synthetic-sensitive-external-reference' not in error_text
            assert 'SQLAlchemyError' not in repr(persistence_error.value)
            assert persistence_error.value.__cause__ is None
            assert service.get_profile(beta.profile_id) == beta_with_credential
        finally:
            dispose_database(resources)
        """
    )
