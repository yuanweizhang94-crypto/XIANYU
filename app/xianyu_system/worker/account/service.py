"""Account use cases and transaction coordination."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from xianyu_system.worker.account.domain import (
    AccountPersistenceError,
    DuplicateAccountOwnership,
    InvalidLifecycleTransition,
    Profile,
    ProfileLifecycleStatus,
    ProfileNotFound,
)
from xianyu_system.worker.account.persistence import AccountProfileRepository

T = TypeVar("T")


class AccountService:
    """Application service for local account Profile use cases."""

    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory

    def create_profile(
        self,
        *,
        account_alias: str,
        external_account_identifier: str | None = None,
    ) -> Profile:
        profile = Profile.create(
            profile_id=str(uuid.uuid4()),
            account_alias=account_alias,
            external_account_identifier=external_account_identifier,
        )

        def operation(repository: AccountProfileRepository) -> Profile:
            repository.add(profile)
            return profile

        return self._write(operation)

    def get_profile(self, profile_id: str) -> Profile:
        try:
            with self._session_factory() as session:
                repository = AccountProfileRepository(session)
                profile = repository.get(profile_id)
                if profile is None:
                    raise ProfileNotFound("Profile was not found.")
                return profile
        except ProfileNotFound:
            raise
        except SQLAlchemyError:
            raise AccountPersistenceError("Account persistence operation failed.") from None

    def list_profiles(self) -> tuple[Profile, ...]:
        try:
            with self._session_factory() as session:
                return AccountProfileRepository(session).list()
        except SQLAlchemyError:
            raise AccountPersistenceError("Account persistence operation failed.") from None

    def rename_profile(
        self,
        profile_id: str,
        *,
        account_alias: str,
        expected_version: int,
    ) -> Profile:
        return self._mutate_existing(
            profile_id,
            expected_version=expected_version,
            mutate=lambda profile: profile.with_account_alias(account_alias),
        )

    def set_external_account_identifier(
        self,
        profile_id: str,
        *,
        external_account_identifier: str | None,
        expected_version: int,
    ) -> Profile:
        return self._mutate_existing(
            profile_id,
            expected_version=expected_version,
            mutate=lambda profile: profile.with_external_account_identifier(
                external_account_identifier
            ),
        )

    def set_credential_reference(
        self,
        profile_id: str,
        *,
        credential_reference: str | None,
        expected_version: int,
    ) -> Profile:
        return self._mutate_existing(
            profile_id,
            expected_version=expected_version,
            mutate=lambda profile: profile.with_credential_reference(credential_reference),
        )

    def set_lifecycle_status(
        self,
        profile_id: str,
        *,
        lifecycle_status: ProfileLifecycleStatus | str,
        expected_version: int,
    ) -> Profile:
        try:
            target = (
                lifecycle_status
                if isinstance(lifecycle_status, ProfileLifecycleStatus)
                else ProfileLifecycleStatus(lifecycle_status)
            )
        except ValueError:
            raise InvalidLifecycleTransition("Lifecycle transition is not approved.") from None

        return self._mutate_existing(
            profile_id,
            expected_version=expected_version,
            mutate=lambda profile: profile.transition_to(target),
        )

    def _mutate_existing(
        self,
        profile_id: str,
        *,
        expected_version: int,
        mutate: Callable[[Profile], Profile],
    ) -> Profile:
        def operation(repository: AccountProfileRepository) -> Profile:
            existing = repository.get(profile_id)
            if existing is None:
                raise ProfileNotFound("Profile was not found.")
            updated = mutate(existing)
            return repository.save(updated, expected_version=expected_version)

        return self._write(operation)

    def _write(self, operation: Callable[[AccountProfileRepository], T]) -> T:
        try:
            with self._session_factory.begin() as session:
                return operation(AccountProfileRepository(session))
        except IntegrityError:
            raise DuplicateAccountOwnership("Profile ownership conflict was detected.") from None
        except (DuplicateAccountOwnership, InvalidLifecycleTransition, ProfileNotFound):
            raise
        except SQLAlchemyError:
            raise AccountPersistenceError("Account persistence operation failed.") from None
