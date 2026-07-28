from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCOUNT_REVISION = "0002_xianyu_account_boundary"
BASELINE_REVISION = "0001_core_baseline"
ACCOUNT_TABLE = "xianyu_account_profiles"
PROFILE_ID = "11111111-1111-4111-8111-111111111111"
OTHER_PROFILE_ID = "22222222-2222-4222-8222-222222222222"


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


def test_account_projection_schema_matches_approved_columns_and_constraints() -> None:
    run_isolated_account_python(
        """
        from xianyu_system.core.database import Base
        from xianyu_system.worker.account.persistence import account_profiles_table

        columns = account_profiles_table.c
        assert list(columns.keys()) == [
            'profile_id',
            'account_alias',
            'external_account_identifier',
            'credential_reference',
            'lifecycle_status',
            'row_version',
        ]
        assert columns.profile_id.primary_key is True
        assert columns.external_account_identifier.unique is True
        assert columns.credential_reference.unique is True
        assert columns.row_version.nullable is False
        assert account_profiles_table.metadata is Base.metadata

        constraints = {
            constraint.name: str(constraint.sqltext)
            for constraint in account_profiles_table.constraints
            if hasattr(constraint, 'sqltext')
        }
        combined = '\\n'.join(constraints.values()).lower()
        assert 'lifecycle_status' in combined
        assert 'trim(account_alias)' in combined
        assert 'trim(external_account_identifier)' in combined
        assert 'trim(credential_reference)' in combined
        assert 'json' not in combined
        assert 'blob' not in combined
        assert 'secret' not in combined
        """
    )


def test_account_migration_is_single_linear_head_and_matches_metadata() -> None:
    run_isolated_account_python(
        """
        from pathlib import Path

        from alembic.script import ScriptDirectory

        from xianyu_system.core.database import build_alembic_config
        from xianyu_system.worker.account.persistence import account_profiles_table

        account_revision = '0002_xianyu_account_boundary'
        baseline_revision = '0001_core_baseline'
        message_revision = '0003_xianyu_message_boundary'
        reply_revision = '0004_xianyu_reply_boundary'
        publish_revision = '0005_xianyu_publish_boundary'
        schedule_revision = '0006_xianyu_schedule_boundary'
        script = ScriptDirectory.from_config(build_alembic_config())
        assert script.get_heads() == [schedule_revision]
        revision = script.get_revision(account_revision)
        assert revision is not None
        assert revision.down_revision == baseline_revision

        migration_source = Path(
            'migrations/versions/0002_xianyu_account_boundary.py'
        ).read_text(encoding='utf-8')
        orm_constraint_names = {
            constraint.name
            for constraint in account_profiles_table.constraints
            if hasattr(constraint, 'sqltext')
        }
        for constraint_name in orm_constraint_names:
            assert constraint_name in migration_source
        for required_fragment in [
            'trim(account_alias)',
            'trim(external_account_identifier)',
            'trim(credential_reference)',
            'lifecycle_status IN',
            'row_version >= 1',
        ]:
            assert required_fragment in migration_source
        assert migration_source.count('op.create_table') == 1
        assert 'account_reference_id' not in migration_source
        """
    )


def test_fresh_upgrade_and_empty_downgrade_round_trip(tmp_path: Path) -> None:
    run_isolated_account_python(
        """
        from pathlib import Path

        from sqlalchemy import inspect

        from xianyu_system.core.database import (
            dispose_database,
            downgrade_database,
            get_current_revision,
            initialize_database,
            upgrade_database,
        )

        account_revision = '0002_xianyu_account_boundary'
        baseline_revision = '0001_core_baseline'
        account_table = 'xianyu_account_profiles'
        resources = initialize_database(Path(__DATABASE_PATH__))
        try:
            upgrade_database(resources, account_revision)
            assert get_current_revision(resources) == account_revision
            assert set(inspect(resources.engine).get_table_names()) == {
                'alembic_version',
                account_table,
            }

            downgrade_database(resources, baseline_revision)
            assert get_current_revision(resources) == baseline_revision
            assert set(inspect(resources.engine).get_table_names()) == {'alembic_version'}
        finally:
            dispose_database(resources)
        """.replace(
            "__DATABASE_PATH__",
            repr(str(tmp_path / "account-migration-round-trip.db")),
        )
    )


def test_nonempty_downgrade_fails_closed_and_preserves_profile(
    tmp_path: Path,
) -> None:
    run_isolated_account_python(
        """
        from pathlib import Path

        import pytest
        from sqlalchemy import text

        from xianyu_system.core.database import (
            dispose_database,
            downgrade_database,
            get_current_revision,
            initialize_database,
            upgrade_database,
        )

        account_revision = '0002_xianyu_account_boundary'
        baseline_revision = '0001_core_baseline'
        profile_id = '11111111-1111-4111-8111-111111111111'
        resources = initialize_database(Path(__DATABASE_PATH__))
        try:
            upgrade_database(resources, account_revision)
            with resources.engine.begin() as connection:
                connection.execute(
                    text('''
                        INSERT INTO xianyu_account_profiles (
                            profile_id,
                            account_alias,
                            external_account_identifier,
                            credential_reference,
                            lifecycle_status,
                            row_version
                        ) VALUES (
                            :profile_id,
                            :account_alias,
                            :external_account_identifier,
                            :credential_reference,
                            :lifecycle_status,
                            :row_version
                        )
                    '''),
                    {
                        'profile_id': profile_id,
                        'account_alias': 'synthetic-profile-alpha',
                        'external_account_identifier': 'synthetic-external-reference-alpha',
                        'credential_reference': None,
                        'lifecycle_status': 'PENDING',
                        'row_version': 1,
                    },
                )

            with pytest.raises(RuntimeError):
                downgrade_database(resources, baseline_revision)

            assert get_current_revision(resources) == account_revision
            with resources.engine.connect() as connection:
                stored = connection.execute(
                    text('''
                        SELECT external_account_identifier
                        FROM xianyu_account_profiles
                        WHERE profile_id = :profile_id
                    '''),
                    {'profile_id': profile_id},
                ).scalar_one()
            assert stored == 'synthetic-external-reference-alpha'
        finally:
            dispose_database(resources)
        """.replace(
            "__DATABASE_PATH__",
            repr(str(tmp_path / "account-nonempty-downgrade.db")),
        )
    )


def test_repository_add_flushes_without_independent_commit(tmp_path: Path) -> None:
    run_isolated_account_python(
        f"""
        from pathlib import Path

        from xianyu_system.core.database import Base, dispose_database, initialize_database
        from xianyu_system.worker.account.domain import AccountReference, Profile
        from xianyu_system.worker.account.domain import ProfileLifecycleStatus
        from xianyu_system.worker.account.persistence import AccountProfileRepository

        profile_id = '{PROFILE_ID}'
        resources = initialize_database(
            Path({str(tmp_path / "account-repository-no-commit.db")!r})
        )
        try:
            Base.metadata.create_all(resources.engine)
            profile = Profile(
                profile_id=profile_id,
                account_reference=AccountReference(
                    profile_id=profile_id,
                    account_alias='synthetic-profile-alpha',
                ),
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                row_version=1,
            )
            session = resources.session_factory()
            try:
                AccountProfileRepository(session).add(profile)
                assert AccountProfileRepository(session).get(profile_id) is not None
            finally:
                session.close()

            with resources.session_factory() as verification_session:
                assert AccountProfileRepository(verification_session).get(profile_id) is None
        finally:
            dispose_database(resources)
        """
    )


def test_repository_round_trip_preserves_account_reference_and_stable_order(
    tmp_path: Path,
) -> None:
    run_isolated_account_python(
        f"""
        from pathlib import Path

        from xianyu_system.core.database import Base, dispose_database, initialize_database
        from xianyu_system.worker.account.domain import AccountReference, Profile
        from xianyu_system.worker.account.domain import ProfileLifecycleStatus
        from xianyu_system.worker.account.persistence import AccountProfileRepository

        profile_id = '{PROFILE_ID}'
        other_profile_id = '{OTHER_PROFILE_ID}'

        def make_profile(profile_id, alias, external=None, credential=None):
            return Profile(
                profile_id=profile_id,
                account_reference=AccountReference(
                    profile_id=profile_id,
                    account_alias=alias,
                    external_account_identifier=external,
                    credential_reference=credential,
                ),
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                row_version=1,
            )

        resources = initialize_database(Path({str(tmp_path / "account-round-trip.db")!r}))
        try:
            Base.metadata.create_all(resources.engine)
            alpha = make_profile(
                other_profile_id,
                'synthetic-profile-beta',
                credential='synthetic-credential-reference-beta',
            )
            beta = make_profile(
                profile_id,
                'synthetic-profile-alpha',
                external='synthetic-external-reference-alpha',
            )
            with resources.session_factory.begin() as session:
                repository = AccountProfileRepository(session)
                repository.add(alpha)
                repository.add(beta)

            with resources.session_factory() as session:
                repository = AccountProfileRepository(session)
                stored = repository.get(profile_id)
                profiles = repository.list()

            assert stored is not None
            assert isinstance(stored.account_reference, AccountReference)
            assert stored.account_reference.profile_id == stored.profile_id
            assert stored.external_account_identifier == 'synthetic-external-reference-alpha'
            assert [profile.profile_id for profile in profiles] == [
                profile_id,
                other_profile_id,
            ]
        finally:
            dispose_database(resources)
        """
    )


def test_database_enforces_uniqueness_concurrency_and_trim_constraints(
    tmp_path: Path,
) -> None:
    run_isolated_account_python(
        """
        from pathlib import Path

        import pytest
        from sqlalchemy import text
        from sqlalchemy.exc import IntegrityError

        from xianyu_system.core.database import Base, dispose_database, initialize_database
        from xianyu_system.worker.account.domain import AccountReference, Profile
        from xianyu_system.worker.account.domain import ProfileLifecycleStatus
        from xianyu_system.worker.account.domain import StaleProfileUpdate
        from xianyu_system.worker.account.persistence import AccountProfileRepository

        profile_id = __PROFILE_ID__
        other_profile_id = __OTHER_PROFILE_ID__

        def make_profile(
            profile_id=profile_id,
            alias='synthetic-profile-alpha',
            external=None,
            credential=None,
        ):
            return Profile(
                profile_id=profile_id,
                account_reference=AccountReference(
                    profile_id=profile_id,
                    account_alias=alias,
                    external_account_identifier=external,
                    credential_reference=credential,
                ),
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                row_version=1,
            )

        resources = initialize_database(
            Path(__DATABASE_PATH__)
        )
        try:
            Base.metadata.create_all(resources.engine)
            insert_sql = text('''
                INSERT INTO xianyu_account_profiles (
                    profile_id,
                    account_alias,
                    external_account_identifier,
                    credential_reference,
                    lifecycle_status,
                    row_version
                ) VALUES (
                    :profile_id,
                    :account_alias,
                    :external_account_identifier,
                    :credential_reference,
                    :lifecycle_status,
                    :row_version
                )
            ''')
            invalid_rows = [
                {
                    'profile_id': '33333333-3333-4333-8333-333333333333',
                    'account_alias': '   ',
                    'external_account_identifier': None,
                    'credential_reference': None,
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': '44444444-4444-4444-8444-444444444444',
                    'account_alias': ' padded-alias ',
                    'external_account_identifier': None,
                    'credential_reference': None,
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': '55555555-5555-4555-8555-555555555555',
                    'account_alias': 'synthetic-profile',
                    'external_account_identifier': ' padded-external ',
                    'credential_reference': None,
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': '66666666-6666-4666-8666-666666666666',
                    'account_alias': 'synthetic-profile',
                    'external_account_identifier': None,
                    'credential_reference': ' padded-credential ',
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
                    'account_alias': 'synthetic-profile-whitespace-external',
                    "external_account_identifier": "   ",
                    "credential_reference": None,
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
                    'account_alias': 'synthetic-profile-whitespace-credential',
                    "external_account_identifier": None,
                    "credential_reference": "   ",
                    'lifecycle_status': 'PENDING',
                    'row_version': 1,
                },
                {
                    'profile_id': '77777777-7777-4777-8777-777777777777',
                    'account_alias': 'synthetic-profile',
                    'external_account_identifier': None,
                    'credential_reference': None,
                    'lifecycle_status': 'AUTHENTICATED',
                    'row_version': 1,
                },
                {
                    'profile_id': '88888888-8888-4888-8888-888888888888',
                    'account_alias': 'synthetic-profile',
                    'external_account_identifier': None,
                    'credential_reference': None,
                    'lifecycle_status': 'PENDING',
                    'row_version': 0,
                },
            ]
            for invalid_row in invalid_rows:
                with pytest.raises(IntegrityError), resources.engine.begin() as connection:
                    connection.execute(insert_sql, invalid_row)

            with resources.session_factory.begin() as session:
                repository = AccountProfileRepository(session)
                repository.add(
                    make_profile(
                        external='synthetic-external-reference-alpha',
                        credential='synthetic-credential-reference-alpha',
                    )
                )
                repository.add(
                    make_profile(
                        profile_id=other_profile_id,
                        alias='synthetic-profile-beta',
                        external='synthetic-external-reference-beta',
                        credential='synthetic-credential-reference-beta',
                    )
                )

            with pytest.raises(IntegrityError), resources.engine.begin() as connection:
                connection.execute(
                    insert_sql,
                    {
                        'profile_id': '99999999-9999-4999-8999-999999999999',
                        'account_alias': 'synthetic-profile-gamma',
                        'external_account_identifier': 'synthetic-external-reference-alpha',
                        'credential_reference': None,
                        'lifecycle_status': 'PENDING',
                        'row_version': 1,
                    },
                )
            with pytest.raises(IntegrityError), resources.engine.begin() as connection:
                connection.execute(
                    insert_sql,
                    {
                        'profile_id': 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
                        'account_alias': 'synthetic-profile-delta',
                        'external_account_identifier': None,
                        'credential_reference': 'synthetic-credential-reference-alpha',
                        'lifecycle_status': 'PENDING',
                        'row_version': 1,
                    },
                )

            with resources.session_factory.begin() as session:
                repository = AccountProfileRepository(session)
                current = repository.get(profile_id)
                assert current is not None
                saved = repository.save(
                    current.with_account_alias('synthetic-profile-updated'),
                    expected_version=current.row_version,
                )
                with pytest.raises(StaleProfileUpdate):
                    repository.save(
                        current.with_account_alias('synthetic-profile-stale'),
                        expected_version=current.row_version,
                    )
                assert saved.row_version == 2
        finally:
            dispose_database(resources)
        """.replace(
            "__PROFILE_ID__",
            repr(PROFILE_ID),
        )
        .replace(
            "__OTHER_PROFILE_ID__",
            repr(OTHER_PROFILE_ID),
        )
        .replace(
            "__DATABASE_PATH__",
            repr(str(tmp_path / "account-database-constraints.db")),
        )
    )
