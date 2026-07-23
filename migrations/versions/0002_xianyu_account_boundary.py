"""Create the minimal local account Profile table."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic.runtime.migration import MigrationContext

revision: str = "0002_xianyu_account_boundary"
down_revision: str | None = "0001_core_baseline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE_NAME = "xianyu_account_profiles"


def upgrade() -> None:
    """Create the approved local account Profile projection."""
    op.create_table(
        _TABLE_NAME,
        sa.Column("profile_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("account_alias", sa.String(length=120), nullable=False),
        sa.Column("external_account_identifier", sa.String(length=256), nullable=True),
        sa.Column("credential_reference", sa.String(length=512), nullable=True),
        sa.Column("lifecycle_status", sa.String(length=16), nullable=False),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "length(profile_id) = 36",
            name="ck_xianyu_account_profile_id_length",
        ),
        sa.CheckConstraint(
            "account_alias = trim(account_alias) AND "
            "length(account_alias) >= 1 AND length(account_alias) <= 120",
            name="ck_xianyu_account_alias_length",
        ),
        sa.CheckConstraint(
            "external_account_identifier IS NULL OR "
            "(external_account_identifier = trim(external_account_identifier) AND "
            "length(external_account_identifier) >= 1 AND "
            "length(external_account_identifier) <= 256)",
            name="ck_xianyu_account_external_identifier_length",
        ),
        sa.CheckConstraint(
            "credential_reference IS NULL OR "
            "(credential_reference = trim(credential_reference) AND "
            "length(credential_reference) >= 1 AND length(credential_reference) <= 512)",
            name="ck_xianyu_account_credential_reference_length",
        ),
        sa.CheckConstraint(
            "lifecycle_status IN ('PENDING', 'ENABLED', 'DISABLED')",
            name="ck_xianyu_account_lifecycle_status",
        ),
        sa.CheckConstraint("row_version >= 1", name="ck_xianyu_account_row_version"),
        sa.UniqueConstraint(
            "external_account_identifier",
            name="uq_xianyu_account_external_identifier",
        ),
        sa.UniqueConstraint(
            "credential_reference",
            name="uq_xianyu_account_credential_reference",
        ),
    )


def downgrade() -> None:
    """Drop the local account Profile projection only when it is empty."""
    context = op.get_context()
    if isinstance(context, MigrationContext) and context.as_sql:
        raise RuntimeError("Offline downgrade is not approved for account profiles.")

    connection = op.get_bind()
    row_count = connection.execute(sa.text(f"SELECT COUNT(*) FROM {_TABLE_NAME}")).scalar_one()
    if row_count != 0:
        raise RuntimeError("Account profile downgrade requires an empty table.")

    op.drop_table(_TABLE_NAME)
