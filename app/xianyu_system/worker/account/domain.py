"""Pure domain model for local Xianyu account Profiles."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from uuid import UUID


class AccountBoundaryError(Exception):
    """Base error for non-sensitive account-boundary failures."""


class InvalidAccountInput(AccountBoundaryError):
    """Raised when account Profile input violates local invariants."""


class ProfileNotFound(AccountBoundaryError):
    """Raised when a requested Profile does not exist."""


class DuplicateAccountOwnership(AccountBoundaryError):
    """Raised when unique Profile-owned references conflict."""


class InvalidLifecycleTransition(AccountBoundaryError):
    """Raised when a local lifecycle transition is not approved."""


class StaleProfileUpdate(AccountBoundaryError):
    """Raised when optimistic concurrency detects stale data."""


class AccountPersistenceError(AccountBoundaryError):
    """Raised when persistence fails with a sanitized message."""


class ProfileLifecycleStatus(StrEnum):
    """Approved local lifecycle states."""

    PENDING = "PENDING"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


_ALLOWED_TRANSITIONS: dict[ProfileLifecycleStatus, frozenset[ProfileLifecycleStatus]] = {
    ProfileLifecycleStatus.PENDING: frozenset(
        {ProfileLifecycleStatus.ENABLED, ProfileLifecycleStatus.DISABLED}
    ),
    ProfileLifecycleStatus.ENABLED: frozenset({ProfileLifecycleStatus.DISABLED}),
    ProfileLifecycleStatus.DISABLED: frozenset({ProfileLifecycleStatus.ENABLED}),
}


def _normalize_uuid(value: str) -> str:
    try:
        return str(UUID(str(value))).lower()
    except (TypeError, ValueError):
        raise InvalidAccountInput("Profile Identifier must be a valid UUID string.") from None


def _normalize_required_text(value: str, *, field_name: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise InvalidAccountInput(f"{field_name} must be text.")
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidAccountInput(f"{field_name} length is outside the approved range.")
    return normalized


def _normalize_optional_text(
    value: str | None,
    *,
    field_name: str,
    max_length: int,
) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidAccountInput(f"{field_name} must be text when provided.")
    normalized = value.strip()
    if not 1 <= len(normalized) <= max_length:
        raise InvalidAccountInput(f"{field_name} length is outside the approved range.")
    return normalized


def _normalize_lifecycle_status(
    value: ProfileLifecycleStatus | str,
) -> ProfileLifecycleStatus:
    try:
        return value if isinstance(value, ProfileLifecycleStatus) else ProfileLifecycleStatus(value)
    except ValueError:
        raise InvalidAccountInput("Lifecycle status is not approved.") from None


@dataclass(frozen=True, slots=True)
class AccountReference:
    """Immutable local account reference owned by exactly one Profile."""

    profile_id: str
    account_alias: str
    external_account_identifier: str | None = None
    credential_reference: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", _normalize_uuid(self.profile_id))
        object.__setattr__(
            self,
            "account_alias",
            _normalize_required_text(
                self.account_alias,
                field_name="Account Alias",
                max_length=120,
            ),
        )
        object.__setattr__(
            self,
            "external_account_identifier",
            _normalize_optional_text(
                self.external_account_identifier,
                field_name="External Account Identifier",
                max_length=256,
            ),
        )
        object.__setattr__(
            self,
            "credential_reference",
            _normalize_optional_text(
                self.credential_reference,
                field_name="Credential Reference",
                max_length=512,
            ),
        )

    def with_account_alias(self, account_alias: str) -> AccountReference:
        """Return a copy with updated display metadata."""
        return replace(self, account_alias=account_alias)

    def with_external_account_identifier(
        self,
        external_account_identifier: str | None,
    ) -> AccountReference:
        """Return a copy with updated opaque external reference metadata."""
        return replace(self, external_account_identifier=external_account_identifier)

    def with_credential_reference(
        self,
        credential_reference: str | None,
    ) -> AccountReference:
        """Return a copy with updated opaque credential reference metadata."""
        return replace(self, credential_reference=credential_reference)


@dataclass(frozen=True, slots=True)
class Profile:
    """Immutable local account-isolation Profile."""

    profile_id: str
    account_reference: AccountReference
    lifecycle_status: ProfileLifecycleStatus
    row_version: int

    def __post_init__(self) -> None:
        normalized_profile_id = _normalize_uuid(self.profile_id)
        object.__setattr__(self, "profile_id", normalized_profile_id)
        if not isinstance(self.account_reference, AccountReference):
            raise InvalidAccountInput("Account Reference must be provided.")
        if self.account_reference.profile_id != normalized_profile_id:
            raise InvalidAccountInput("Account Reference ownership does not match Profile.")
        object.__setattr__(
            self,
            "lifecycle_status",
            _normalize_lifecycle_status(self.lifecycle_status),
        )
        if not isinstance(self.row_version, int) or self.row_version < 1:
            raise InvalidAccountInput("Row version must be greater than or equal to one.")

    @classmethod
    def create(
        cls,
        *,
        profile_id: str,
        account_alias: str,
        external_account_identifier: str | None = None,
    ) -> Profile:
        """Create a new local Profile in the approved initial state."""
        normalized_profile_id = _normalize_uuid(profile_id)
        return cls(
            profile_id=normalized_profile_id,
            account_reference=AccountReference(
                profile_id=normalized_profile_id,
                account_alias=account_alias,
                external_account_identifier=external_account_identifier,
                credential_reference=None,
            ),
            lifecycle_status=ProfileLifecycleStatus.PENDING,
            row_version=1,
        )

    @property
    def account_alias(self) -> str:
        """Return the owned Account Reference alias."""
        return self.account_reference.account_alias

    @property
    def external_account_identifier(self) -> str | None:
        """Return the owned opaque external account identifier."""
        return self.account_reference.external_account_identifier

    @property
    def credential_reference(self) -> str | None:
        """Return the owned opaque credential reference."""
        return self.account_reference.credential_reference

    def with_account_alias(self, account_alias: str) -> Profile:
        """Return a copy with updated display metadata."""
        return replace(
            self,
            account_reference=self.account_reference.with_account_alias(account_alias),
        )

    def with_external_account_identifier(
        self,
        external_account_identifier: str | None,
    ) -> Profile:
        """Return a copy with updated opaque external reference metadata."""
        return replace(
            self,
            account_reference=self.account_reference.with_external_account_identifier(
                external_account_identifier
            ),
        )

    def with_credential_reference(self, credential_reference: str | None) -> Profile:
        """Return a copy with updated opaque credential reference metadata."""
        return replace(
            self,
            account_reference=self.account_reference.with_credential_reference(
                credential_reference
            ),
        )

    def transition_to(self, lifecycle_status: ProfileLifecycleStatus | str) -> Profile:
        """Return a copy after an approved local lifecycle transition."""
        target = _normalize_lifecycle_status(lifecycle_status)
        if target not in _ALLOWED_TRANSITIONS[self.lifecycle_status]:
            raise InvalidLifecycleTransition("Lifecycle transition is not approved.")
        return replace(self, lifecycle_status=target)
