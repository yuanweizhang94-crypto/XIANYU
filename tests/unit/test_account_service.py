from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy.exc import SQLAlchemyError

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    initialize_database,
)


def build_account_service(tmp_path: Path) -> tuple[DatabaseResources, object]:
    from xianyu_system.worker.account import AccountService
    from xianyu_system.worker.account.persistence import account_profiles_table

    resources = initialize_database(tmp_path / "account-service.db")
    account_profiles_table.create(resources.engine)
    return resources, AccountService(resources.session_factory)



def account_errors() -> tuple[type[Exception], ...]:
    from xianyu_system.worker.account import (
        AccountPersistenceError,
        DuplicateAccountOwnership,
        InvalidLifecycleTransition,
        ProfileNotFound,
        StaleProfileUpdate,
    )

    return (
        AccountPersistenceError,
        DuplicateAccountOwnership,
        InvalidLifecycleTransition,
        ProfileNotFound,
        StaleProfileUpdate,
    )


def repository_type() -> type[object]:
    from xianyu_system.worker.account.persistence import AccountProfileRepository

    return AccountProfileRepository


def lifecycle_status() -> type[object]:
    from xianyu_system.worker.account import ProfileLifecycleStatus

    return ProfileLifecycleStatus


def test_create_profile_uses_uuid4_and_persists_one_profile(tmp_path: Path) -> None:
    ProfileLifecycleStatus = lifecycle_status()
    resources, service = build_account_service(tmp_path)
    try:
        profile = service.create_profile(
            account_alias=" synthetic-profile-alpha ",
            external_account_identifier=" synthetic-external-reference-alpha ",
        )
        stored = service.get_profile(profile.profile_id)

        assert UUID(profile.profile_id).version == 4
        assert profile.profile_id == profile.profile_id.lower()
        assert profile.account_reference.profile_id == profile.profile_id
        assert profile.account_alias == "synthetic-profile-alpha"
        assert profile.external_account_identifier == "synthetic-external-reference-alpha"
        assert profile.lifecycle_status is ProfileLifecycleStatus.PENDING
        assert profile.row_version == 1
        assert stored == profile
    finally:
        dispose_database(resources)


def test_get_and_list_profiles_return_expected_profiles(tmp_path: Path) -> None:
    resources, service = build_account_service(tmp_path)
    try:
        beta = service.create_profile(account_alias="synthetic-profile-beta")
        alpha = service.create_profile(account_alias="synthetic-profile-alpha")

        assert service.get_profile(alpha.profile_id) == alpha
        profiles = service.list_profiles()
        assert [profile.profile_id for profile in profiles] == sorted(
            [alpha.profile_id, beta.profile_id]
        )
        assert profiles[0].account_reference is not profiles[1].account_reference
    finally:
        dispose_database(resources)


def test_missing_profile_raises_sanitized_not_found(tmp_path: Path) -> None:
    ProfileNotFound = account_errors()[3]
    resources, service = build_account_service(tmp_path)
    try:
        missing_id = "11111111-1111-4111-8111-111111111111"
        with pytest.raises(ProfileNotFound) as error:
            service.get_profile(missing_id)

        assert missing_id not in str(error.value)
        assert "synthetic-credential-reference-alpha" not in str(error.value)
    finally:
        dispose_database(resources)


def test_profile_metadata_mutations_increment_version_and_preserve_identity(
    tmp_path: Path,
) -> None:
    resources, service = build_account_service(tmp_path)
    try:
        original = service.create_profile(
            account_alias="synthetic-profile-alpha",
            external_account_identifier="synthetic-external-reference-alpha",
        )

        renamed = service.rename_profile(
            original.profile_id,
            account_alias="synthetic-profile-beta",
            expected_version=original.row_version,
        )
        external_cleared = service.set_external_account_identifier(
            original.profile_id,
            external_account_identifier=None,
            expected_version=renamed.row_version,
        )
        external_set = service.set_external_account_identifier(
            original.profile_id,
            external_account_identifier="synthetic-external-reference-beta",
            expected_version=external_cleared.row_version,
        )
        credential_set = service.set_credential_reference(
            original.profile_id,
            credential_reference="synthetic-credential-reference-alpha",
            expected_version=external_set.row_version,
        )
        credential_cleared = service.set_credential_reference(
            original.profile_id,
            credential_reference=None,
            expected_version=credential_set.row_version,
        )

        versions = [
            original.row_version,
            renamed.row_version,
            external_cleared.row_version,
            external_set.row_version,
            credential_set.row_version,
            credential_cleared.row_version,
        ]
        assert versions == [1, 2, 3, 4, 5, 6]
        assert credential_cleared.profile_id == original.profile_id
        assert credential_cleared.account_reference.profile_id == original.profile_id
        assert credential_cleared.account_alias == "synthetic-profile-beta"
        assert credential_cleared.external_account_identifier == "synthetic-external-reference-beta"
        assert credential_cleared.credential_reference is None
    finally:
        dispose_database(resources)


def test_lifecycle_mutations_follow_approved_transitions(tmp_path: Path) -> None:
    InvalidLifecycleTransition = account_errors()[2]
    ProfileLifecycleStatus = lifecycle_status()
    resources, service = build_account_service(tmp_path)
    try:
        profile = service.create_profile(account_alias="synthetic-profile-alpha")
        enabled = service.set_lifecycle_status(
            profile.profile_id,
            lifecycle_status=ProfileLifecycleStatus.ENABLED,
            expected_version=profile.row_version,
        )
        disabled = service.set_lifecycle_status(
            profile.profile_id,
            lifecycle_status=ProfileLifecycleStatus.DISABLED,
            expected_version=enabled.row_version,
        )
        reenabled = service.set_lifecycle_status(
            profile.profile_id,
            lifecycle_status="ENABLED",
            expected_version=disabled.row_version,
        )

        assert reenabled.lifecycle_status is ProfileLifecycleStatus.ENABLED
        assert reenabled.row_version == 4
        with pytest.raises(InvalidLifecycleTransition):
            service.set_lifecycle_status(
                profile.profile_id,
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                expected_version=reenabled.row_version,
            )
        assert service.get_profile(profile.profile_id) == reenabled
    finally:
        dispose_database(resources)


def test_stale_update_fails_closed_without_overwriting(tmp_path: Path) -> None:
    StaleProfileUpdate = account_errors()[4]
    resources, service = build_account_service(tmp_path)
    try:
        original = service.create_profile(account_alias="synthetic-profile-alpha")
        old_version = service.get_profile(original.profile_id).row_version
        updated = service.rename_profile(
            original.profile_id,
            account_alias="synthetic-profile-beta",
            expected_version=old_version,
        )

        with pytest.raises(StaleProfileUpdate):
            service.rename_profile(
                original.profile_id,
                account_alias="synthetic-profile-stale",
                expected_version=old_version,
            )

        stored = service.get_profile(original.profile_id)
        assert stored.account_alias == "synthetic-profile-beta"
        assert stored.row_version == updated.row_version
    finally:
        dispose_database(resources)


def test_duplicate_and_persistence_failures_are_sanitized_and_rolled_back(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    AccountPersistenceError, DuplicateAccountOwnership = account_errors()[:2]
    AccountProfileRepository = repository_type()
    resources, service = build_account_service(tmp_path)
    try:
        alpha = service.create_profile(account_alias="synthetic-profile-alpha")
        beta = service.create_profile(account_alias="synthetic-profile-beta")
        beta_external = service.set_external_account_identifier(
            beta.profile_id,
            external_account_identifier="synthetic-external-reference-beta",
            expected_version=beta.row_version,
        )
        beta_credential = service.set_credential_reference(
            beta.profile_id,
            credential_reference="synthetic-credential-reference-beta",
            expected_version=beta_external.row_version,
        )

        with pytest.raises(DuplicateAccountOwnership) as duplicate_external:
            service.set_external_account_identifier(
                alpha.profile_id,
                external_account_identifier="synthetic-external-reference-beta",
                expected_version=alpha.row_version,
            )
        assert "synthetic-external-reference-beta" not in str(duplicate_external.value)
        assert service.get_profile(alpha.profile_id) == alpha

        with pytest.raises(DuplicateAccountOwnership) as duplicate_credential:
            service.set_credential_reference(
                alpha.profile_id,
                credential_reference="synthetic-credential-reference-beta",
                expected_version=alpha.row_version,
            )
        assert "synthetic-credential-reference-beta" not in str(
            duplicate_credential.value
        )
        assert service.get_profile(alpha.profile_id) == alpha

        def raise_persistence_error(
            self: AccountProfileRepository,
            *args: object,
            **kwargs: object,
        ) -> object:
            raise SQLAlchemyError(
                "SELECT synthetic-credential-reference-alpha FROM synthetic-table"
            )

        monkeypatch.setattr(AccountProfileRepository, "save", raise_persistence_error)
        with pytest.raises(AccountPersistenceError) as persistence_error:
            service.rename_profile(
                beta.profile_id,
                account_alias="synthetic-profile-mutated",
                expected_version=beta_credential.row_version,
            )

        text = str(persistence_error.value)
        assert "SELECT" not in text
        assert "synthetic-credential-reference-alpha" not in text
        assert persistence_error.value.__cause__ is None
        assert service.get_profile(beta.profile_id) == beta_credential
    finally:
        dispose_database(resources)
