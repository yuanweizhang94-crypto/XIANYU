"""Create local synthetic message boundary tables."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic.runtime.migration import MigrationContext

revision: str = "0003_xianyu_message_boundary"
down_revision: str | None = "0002_xianyu_account_boundary"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CONVERSATION_TABLE = "xianyu_message_conversations"
_MESSAGE_TABLE = "xianyu_message_records"
_ATTEMPT_TABLE = "xianyu_message_delivery_attempts"


def upgrade() -> None:
    """Create the local synthetic message projection."""
    op.create_table(
        _CONVERSATION_TABLE,
        sa.Column("conversation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("platform_conversation_identifier", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["xianyu_account_profiles.profile_id"],
            name="fk_xianyu_message_conversation_profile",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "conversation_id",
            "profile_id",
            "account_reference",
            name="uq_xianyu_message_conversation_owner",
        ),
        sa.UniqueConstraint(
            "profile_id",
            "account_reference",
            "platform_conversation_identifier",
            name="uq_xianyu_message_conversation_platform_profile",
        ),
        sa.CheckConstraint("length(conversation_id) = 36", name="ck_xianyu_message_conversation_id_len"),
        sa.CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_conversation_profile_len"),
        sa.CheckConstraint(
            "account_reference = trim(account_reference) AND "
            "length(account_reference) >= 1 AND length(account_reference) <= 256",
            name="ck_xianyu_message_conversation_account_len",
        ),
        sa.CheckConstraint(
            "platform_conversation_identifier IS NULL OR "
            "(platform_conversation_identifier = trim(platform_conversation_identifier) AND "
            "length(platform_conversation_identifier) >= 1 AND "
            "length(platform_conversation_identifier) <= 512)",
            name="ck_xianyu_message_conversation_platform_len",
        ),
    )

    op.create_table(
        _MESSAGE_TABLE,
        sa.Column("message_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("conversation_id", sa.String(length=36), nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("platform_message_identifier", sa.String(length=512), nullable=True),
        sa.Column("delivery_identity", sa.String(length=512), nullable=True),
        sa.Column("participant_reference", sa.String(length=512), nullable=False),
        sa.Column("message_content", sa.String(length=4096), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("platform_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deduplication_decision", sa.String(length=16), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id", "profile_id", "account_reference"],
            [
                "xianyu_message_conversations.conversation_id",
                "xianyu_message_conversations.profile_id",
                "xianyu_message_conversations.account_reference",
            ],
            name="fk_xianyu_message_record_conversation_owner",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "message_id",
            "profile_id",
            "account_reference",
            name="uq_xianyu_message_record_owner",
        ),
        sa.UniqueConstraint(
            "profile_id",
            "account_reference",
            "delivery_identity",
            name="uq_xianyu_message_record_delivery_identity",
        ),
        sa.CheckConstraint("length(message_id) = 36", name="ck_xianyu_message_record_id_len"),
        sa.CheckConstraint("length(conversation_id) = 36", name="ck_xianyu_message_record_conversation_len"),
        sa.CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_record_profile_len"),
        sa.CheckConstraint(
            "account_reference = trim(account_reference) AND "
            "length(account_reference) >= 1 AND length(account_reference) <= 256",
            name="ck_xianyu_message_record_account_len",
        ),
        sa.CheckConstraint(
            "platform_message_identifier IS NULL OR "
            "(platform_message_identifier = trim(platform_message_identifier) AND "
            "length(platform_message_identifier) >= 1 AND length(platform_message_identifier) <= 512)",
            name="ck_xianyu_message_record_platform_len",
        ),
        sa.CheckConstraint(
            "delivery_identity IS NULL OR "
            "(delivery_identity = trim(delivery_identity) AND "
            "length(delivery_identity) >= 1 AND length(delivery_identity) <= 512)",
            name="ck_xianyu_message_record_delivery_len",
        ),
        sa.CheckConstraint(
            "participant_reference = trim(participant_reference) AND "
            "length(participant_reference) >= 1 AND length(participant_reference) <= 512",
            name="ck_xianyu_message_record_participant_len",
        ),
        sa.CheckConstraint(
            "length(message_content) >= 1 AND length(message_content) <= 4096 AND "
            "length(trim(message_content)) >= 1",
            name="ck_xianyu_message_record_content_len",
        ),
        sa.CheckConstraint(
            "deduplication_decision IN ('NEW', 'INDETERMINATE')",
            name="ck_xianyu_message_record_dedup_decision",
        ),
    )

    op.create_table(
        _ATTEMPT_TABLE,
        sa.Column("delivery_attempt_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("message_id", sa.String(length=36), nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("outcome_class", sa.String(length=16), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("correlation_identifier", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id", "profile_id", "account_reference"],
            [
                "xianyu_message_records.message_id",
                "xianyu_message_records.profile_id",
                "xianyu_message_records.account_reference",
            ],
            name="fk_xianyu_message_attempt_message_owner",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "message_id",
            "profile_id",
            "account_reference",
            "attempt_number",
            name="uq_xianyu_message_attempt_number",
        ),
        sa.CheckConstraint("length(delivery_attempt_id) = 36", name="ck_xianyu_message_attempt_id_len"),
        sa.CheckConstraint("length(message_id) = 36", name="ck_xianyu_message_attempt_message_len"),
        sa.CheckConstraint("length(profile_id) = 36", name="ck_xianyu_message_attempt_profile_len"),
        sa.CheckConstraint(
            "account_reference = trim(account_reference) AND "
            "length(account_reference) >= 1 AND length(account_reference) <= 256",
            name="ck_xianyu_message_attempt_account_len",
        ),
        sa.CheckConstraint(
            "outcome_class IN ('NEW', 'DUPLICATE', 'INDETERMINATE')",
            name="ck_xianyu_message_attempt_outcome",
        ),
        sa.CheckConstraint("attempt_number >= 1", name="ck_xianyu_message_attempt_number_positive"),
        sa.CheckConstraint(
            "reason_code IS NULL OR "
            "(reason_code = trim(reason_code) AND length(reason_code) >= 1 AND length(reason_code) <= 64)",
            name="ck_xianyu_message_attempt_reason_len",
        ),
        sa.CheckConstraint(
            "correlation_identifier IS NULL OR "
            "(correlation_identifier = trim(correlation_identifier) AND "
            "length(correlation_identifier) >= 1 AND length(correlation_identifier) <= 128)",
            name="ck_xianyu_message_attempt_correlation_len",
        ),
    )


def downgrade() -> None:
    """Drop local synthetic message tables only when empty."""
    context = op.get_context()
    if isinstance(context, MigrationContext) and context.as_sql:
        raise RuntimeError("Offline downgrade is not approved for message tables.")

    connection = op.get_bind()
    for table_name in [_ATTEMPT_TABLE, _MESSAGE_TABLE, _CONVERSATION_TABLE]:
        row_count = connection.execute(sa.text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()
        if row_count != 0:
            raise RuntimeError("Message boundary downgrade requires empty tables.")

    op.drop_table(_ATTEMPT_TABLE)
    op.drop_table(_MESSAGE_TABLE)
    op.drop_table(_CONVERSATION_TABLE)
