"""Create local deterministic reply boundary tables."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic.runtime.migration import MigrationContext

revision: str = "0004_xianyu_reply_boundary"
down_revision: str | None = "0003_xianyu_message_boundary"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TEMPLATE_TABLE = "xianyu_reply_templates"
_RULE_TABLE = "xianyu_reply_rules"
_CONDITION_TABLE = "xianyu_reply_conditions"
_AUDIT_TABLE = "xianyu_reply_audit_events"
_TABLES = [_AUDIT_TABLE, _CONDITION_TABLE, _RULE_TABLE, _TEMPLATE_TABLE]


def upgrade() -> None:
    op.create_table(
        _TEMPLATE_TABLE,
        sa.Column("template_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("version", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("lifecycle_state", sa.String(length=16), nullable=False),
        sa.Column("script_text", sa.String(length=2048), nullable=False),
        sa.Column("variable_allowlist", sa.String(length=1024), nullable=False),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["xianyu_account_profiles.profile_id"],
            name="fk_xianyu_reply_template_profile",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("length(template_id) = 36", name="ck_xianyu_reply_template_id_len"),
        sa.CheckConstraint("version >= 1", name="ck_xianyu_reply_template_version_positive"),
        sa.CheckConstraint(
            "row_version >= 1", name="ck_xianyu_reply_template_row_version_positive"
        ),
        sa.CheckConstraint(
            "lifecycle_state IN ('DRAFT','ENABLED','DISABLED','ARCHIVED')",
            name="ck_xianyu_reply_template_lifecycle",
        ),
        sa.CheckConstraint(
            "account_reference = trim(account_reference) AND length(account_reference) >= 1 AND length(account_reference) <= 256",
            name="ck_xianyu_reply_template_account_len",
        ),
        sa.CheckConstraint(
            "length(script_text) >= 1 AND length(script_text) <= 2048 AND length(trim(script_text)) >= 1",
            name="ck_xianyu_reply_template_script_len",
        ),
    )
    op.create_table(
        _RULE_TABLE,
        sa.Column("rule_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("version", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("lifecycle_state", sa.String(length=16), nullable=False),
        sa.Column("template_id", sa.String(length=36), nullable=False),
        sa.Column("template_version", sa.Integer(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["xianyu_account_profiles.profile_id"],
            name="fk_xianyu_reply_rule_profile",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["template_id", "template_version"],
            ["xianyu_reply_templates.template_id", "xianyu_reply_templates.version"],
            name="fk_xianyu_reply_rule_template_version",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("length(rule_id) = 36", name="ck_xianyu_reply_rule_id_len"),
        sa.CheckConstraint("version >= 1", name="ck_xianyu_reply_rule_version_positive"),
        sa.CheckConstraint("row_version >= 1", name="ck_xianyu_reply_rule_row_version_positive"),
        sa.CheckConstraint("priority >= 0", name="ck_xianyu_reply_rule_priority_non_negative"),
        sa.CheckConstraint(
            "lifecycle_state IN ('DRAFT','ENABLED','DISABLED','ARCHIVED')",
            name="ck_xianyu_reply_rule_lifecycle",
        ),
        sa.CheckConstraint(
            "account_reference = trim(account_reference) AND length(account_reference) >= 1 AND length(account_reference) <= 256",
            name="ck_xianyu_reply_rule_account_len",
        ),
        sa.CheckConstraint(
            "name IS NULL OR (name = trim(name) AND length(name) >= 1 AND length(name) <= 128)",
            name="ck_xianyu_reply_rule_name_len",
        ),
    )
    op.create_index(
        "uq_xianyu_reply_rule_one_enabled_version",
        _RULE_TABLE,
        ["profile_id", "account_reference", "rule_id"],
        unique=True,
        sqlite_where=sa.text("lifecycle_state = 'ENABLED'"),
    )
    op.create_table(
        _CONDITION_TABLE,
        sa.Column("condition_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("rule_id", sa.String(length=36), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("field_name", sa.String(length=64), nullable=False),
        sa.Column("operator", sa.String(length=32), nullable=False),
        sa.Column("expected_value", sa.String(length=512), nullable=False),
        sa.Column("normalization", sa.String(length=32), nullable=False),
        sa.Column("case_sensitive", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["rule_id", "rule_version"],
            ["xianyu_reply_rules.rule_id", "xianyu_reply_rules.version"],
            name="fk_xianyu_reply_condition_rule_version",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("length(condition_id) = 36", name="ck_xianyu_reply_condition_id_len"),
        sa.CheckConstraint(
            "rule_version >= 1", name="ck_xianyu_reply_condition_rule_version_positive"
        ),
        sa.CheckConstraint("sequence >= 1", name="ck_xianyu_reply_condition_sequence_positive"),
        sa.CheckConstraint(
            "field_name IN ('content_text','language_hint')", name="ck_xianyu_reply_condition_field"
        ),
        sa.CheckConstraint(
            "operator IN ('equals','contains','starts_with','ends_with')",
            name="ck_xianyu_reply_condition_operator",
        ),
        sa.CheckConstraint(
            "length(expected_value) >= 1 AND length(expected_value) <= 512 AND length(trim(expected_value)) >= 1",
            name="ck_xianyu_reply_condition_expected_len",
        ),
        sa.CheckConstraint(
            "normalization IN ('','NFKC','TRIM','NFKC,TRIM')",
            name="ck_xianyu_reply_condition_normalization",
        ),
        sa.CheckConstraint(
            "case_sensitive IN (0,1)", name="ck_xianyu_reply_condition_case_sensitive"
        ),
    )
    op.create_index(
        "ix_xianyu_reply_condition_rule_version",
        _CONDITION_TABLE,
        ["rule_id", "rule_version", "sequence"],
        unique=False,
    )
    op.create_table(
        _AUDIT_TABLE,
        sa.Column("audit_event_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("account_reference", sa.String(length=256), nullable=False),
        sa.Column("conversation_id", sa.String(length=36), nullable=False),
        sa.Column("message_id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=36), nullable=True),
        sa.Column("rule_version", sa.Integer(), nullable=True),
        sa.Column("template_id", sa.String(length=36), nullable=True),
        sa.Column("template_version", sa.Integer(), nullable=True),
        sa.Column("decision_type", sa.String(length=16), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("failure_category", sa.String(length=64), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("correlation_identifier", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id", "profile_id", "account_reference"],
            [
                "xianyu_message_records.message_id",
                "xianyu_message_records.profile_id",
                "xianyu_message_records.account_reference",
            ],
            name="fk_xianyu_reply_audit_message_owner",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["rule_id", "rule_version"],
            ["xianyu_reply_rules.rule_id", "xianyu_reply_rules.version"],
            name="fk_xianyu_reply_audit_rule_version",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["template_id", "template_version"],
            ["xianyu_reply_templates.template_id", "xianyu_reply_templates.version"],
            name="fk_xianyu_reply_audit_template_version",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("length(audit_event_id) = 36", name="ck_xianyu_reply_audit_id_len"),
        sa.CheckConstraint(
            "(rule_id IS NULL AND rule_version IS NULL) OR (rule_id IS NOT NULL AND rule_version IS NOT NULL)",
            name="ck_xianyu_reply_audit_rule_pair",
        ),
        sa.CheckConstraint(
            "(template_id IS NULL AND template_version IS NULL) OR (template_id IS NOT NULL AND template_version IS NOT NULL)",
            name="ck_xianyu_reply_audit_template_pair",
        ),
        sa.CheckConstraint(
            "decision_type IN ('REPLY','NO_MATCH','CONFLICT','ESCALATE','SUPPRESSED','INVALID_INPUT')",
            name="ck_xianyu_reply_audit_decision",
        ),
        sa.CheckConstraint(
            "failure_category IS NULL OR (failure_category = trim(failure_category) AND length(failure_category) >= 1 AND length(failure_category) <= 64)",
            name="ck_xianyu_reply_audit_failure_len",
        ),
    )
    op.create_index(
        "ix_xianyu_reply_audit_message",
        _AUDIT_TABLE,
        ["message_id", "profile_id", "account_reference"],
        unique=False,
    )


def downgrade() -> None:
    context = op.get_context()
    if isinstance(context, MigrationContext) and context.as_sql:
        raise RuntimeError("Offline downgrade is not approved for reply tables.")
    connection = op.get_bind()
    for table_name in _TABLES:
        row_count = connection.execute(sa.text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()
        if row_count != 0:
            raise RuntimeError("Reply boundary downgrade requires empty tables.")
    op.drop_index("ix_xianyu_reply_audit_message", table_name=_AUDIT_TABLE)
    op.drop_table(_AUDIT_TABLE)
    op.drop_index("ix_xianyu_reply_condition_rule_version", table_name=_CONDITION_TABLE)
    op.drop_table(_CONDITION_TABLE)
    op.drop_index("uq_xianyu_reply_rule_one_enabled_version", table_name=_RULE_TABLE)
    op.drop_table(_RULE_TABLE)
    op.drop_table(_TEMPLATE_TABLE)
