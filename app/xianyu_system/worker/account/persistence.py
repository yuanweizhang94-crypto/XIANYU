"""SQLAlchemy projection and Repository for local account Profiles."""

from __future__ import annotations

from typing import Any, cast

from sqlalchemy import CheckConstraint, Column, Integer, String, Table, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from xianyu_system.core.database import Base
from xianyu_system.worker.account.domain import (
    AccountReference,
    Profile,
    ProfileLifecycleStatus,
    StaleProfileUpdate,
)

account_profiles_table = Table(
    "xianyu_account_profiles",
    Base.metadata,
    Column("profile_id", String(36), primary_key=True, nullable=False),
    Column("account_alias", String(120), nullable=False),
    Column("external_account_identifier", String(256), nullable=True, unique=True),
    Column("credential_reference", String(512), nullable=True, unique=True),
    Column("lifecycle_status", String(16), nullable=False),
    Column("row_version", Integer, nullable=False),
    CheckConstraint("length(profile_id) = 36", name="ck_xianyu_account_profile_id_length"),
    CheckConstraint(
        "account_alias = trim(account_alias) AND "
        "length(account_alias) >= 1 AND length(account_alias) <= 120",
        name="ck_xianyu_account_alias_length",
    ),
    CheckConstraint(
        "external_account_identifier IS NULL OR "
        "(external_account_identifier = trim(external_account_identifier) AND "
        "length(external_account_identifier) >= 1 AND "
        "length(external_account_identifier) <= 256)",
        name="ck_xianyu_account_external_identifier_length",
    ),
    CheckConstraint(
        "credential_reference IS NULL OR "
        "(credential_reference = trim(credential_reference) AND "
        "length(credential_reference) >= 1 AND length(credential_reference) <= 512)",
        name="ck_xianyu_account_credential_reference_length",
    ),
    CheckConstraint(
        "lifecycle_status IN ('PENDING', 'ENABLED', 'DISABLED')",
        name="ck_xianyu_account_lifecycle_status",
    ),
    CheckConstraint("row_version >= 1", name="ck_xianyu_account_row_version"),
    extend_existing=True,
)


class _AccountProfileRecord:
    profile_id: str
    account_alias: str
    external_account_identifier: str | None
    credential_reference: str | None
    lifecycle_status: str
    row_version: int


Base.registry.map_imperatively(_AccountProfileRecord, account_profiles_table)


def _record_to_profile(record: _AccountProfileRecord) -> Profile:
    return Profile(
        profile_id=record.profile_id,
        account_reference=AccountReference(
            profile_id=record.profile_id,
            account_alias=record.account_alias,
            external_account_identifier=record.external_account_identifier,
            credential_reference=record.credential_reference,
        ),
        lifecycle_status=ProfileLifecycleStatus(record.lifecycle_status),
        row_version=record.row_version,
    )


def _profile_values(profile: Profile) -> dict[str, Any]:
    return {
        "profile_id": profile.profile_id,
        "account_alias": profile.account_alias,
        "external_account_identifier": profile.external_account_identifier,
        "credential_reference": profile.credential_reference,
        "lifecycle_status": profile.lifecycle_status.value,
        "row_version": profile.row_version,
    }


class AccountProfileRepository:
    """Concrete Repository participating in caller-owned Sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, profile: Profile) -> None:
        record = _AccountProfileRecord()
        for key, value in _profile_values(profile).items():
            setattr(record, key, value)
        self._session.add(record)
        self._session.flush()

    def get(self, profile_id: str) -> Profile | None:
        normalized_profile_id = Profile.create(
            profile_id=profile_id,
            account_alias="synthetic-normalization-only",
        ).profile_id
        record = self._session.get(_AccountProfileRecord, normalized_profile_id)
        if record is None:
            return None
        return _record_to_profile(record)

    def list(self) -> tuple[Profile, ...]:
        records = self._session.scalars(
            select(_AccountProfileRecord).order_by(account_profiles_table.c.profile_id)
        ).all()
        return tuple(_record_to_profile(record) for record in records)

    def save(
        self,
        profile: Profile,
        *,
        expected_version: int,
    ) -> Profile:
        next_version = expected_version + 1
        result = cast(
            CursorResult[Any],
            self._session.execute(
                update(account_profiles_table)
            .where(account_profiles_table.c.profile_id == profile.profile_id)
            .where(account_profiles_table.c.row_version == expected_version)
            .values(
                account_alias=profile.account_alias,
                external_account_identifier=profile.external_account_identifier,
                credential_reference=profile.credential_reference,
                lifecycle_status=profile.lifecycle_status.value,
                row_version=next_version,
            )
        ),
        )
        if result.rowcount != 1:
            raise StaleProfileUpdate("Profile update used a stale row version.")
        self._session.flush()
        return Profile(
            profile_id=profile.profile_id,
            account_reference=profile.account_reference,
            lifecycle_status=profile.lifecycle_status,
            row_version=next_version,
        )
