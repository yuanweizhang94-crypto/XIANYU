"""Create local deterministic schedule boundary tables."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic.runtime.migration import MigrationContext

revision: str = "0006_xianyu_schedule_boundary"
down_revision: str | None = "0005_xianyu_publish_boundary"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_REQUEST_TABLE = "xianyu_schedule_requests"
_AUDIT_TABLE = "xianyu_schedule_audit_events"
_TABLES = [_AUDIT_TABLE, _REQUEST_TABLE]


def upgrade() -> None:
    op.create_table(
        _REQUEST_TABLE,
        sa.Column("schedule_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("publish_request_id", sa.String(length=36), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False, unique=True),
        sa.Column("trigger_type", sa.String(length=16), nullable=False),
        sa.Column("lifecycle", sa.String(length=32), nullable=False),
        sa.Column("normalized_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("misfire_grace_seconds", sa.Integer(), nullable=False),
        sa.Column("synthetic_fixture", sa.Boolean(), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reason", sa.String(length=256), nullable=True),
        sa.CheckConstraint("length(schedule_id) = 36", name="ck_xianyu_schedule_id_len"),
        sa.CheckConstraint("length(publish_request_id) = 36", name="ck_xianyu_schedule_publish_id_len"),
        sa.CheckConstraint(
            "idempotency_key = trim(idempotency_key) AND length(idempotency_key) >= 1 AND length(idempotency_key) <= 128",
            name="ck_xianyu_schedule_idempotency_len",
        ),
        sa.CheckConstraint("trigger_type IN ('IMMEDIATE','RUN_AT_UTC')", name="ck_xianyu_schedule_trigger"),
        sa.CheckConstraint(
            "lifecycle IN ('PENDING','CLAIMED','DISPATCHED','CANCELLED','MISFIRED','FAILED','NEEDS_MANUAL_REVIEW')",
            name="ck_xianyu_schedule_lifecycle",
        ),
        sa.CheckConstraint("length(normalized_fingerprint) = 64", name="ck_xianyu_schedule_fingerprint_len"),
        sa.CheckConstraint(
            "misfire_grace_seconds >= 0 AND misfire_grace_seconds <= 3600",
            name="ck_xianyu_schedule_grace_range",
        ),
    )
    op.create_index(
        "ix_xianyu_schedule_due_pending",
        _REQUEST_TABLE,
        ["lifecycle", "due_at"],
        unique=False,
    )
    op.create_index(
        "ix_xianyu_schedule_publish",
        _REQUEST_TABLE,
        ["publish_request_id"],
        unique=False,
    )
    op.create_table(
        _AUDIT_TABLE,
        sa.Column("event_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("schedule_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("from_lifecycle", sa.String(length=32), nullable=True),
        sa.Column("to_lifecycle", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=256), nullable=True),
        sa.CheckConstraint("length(event_id) = 36", name="ck_xianyu_schedule_audit_id_len"),
        sa.CheckConstraint("length(schedule_id) = 36", name="ck_xianyu_schedule_audit_schedule_id_len"),
        sa.CheckConstraint(
            "event_type = trim(event_type) AND length(event_type) >= 1 AND length(event_type) <= 32",
            name="ck_xianyu_schedule_audit_event_type_len",
        ),
    )


def downgrade() -> None:
    context = op.get_context()
    if isinstance(context, MigrationContext) and context.as_sql:
        raise RuntimeError("Offline downgrade is not approved for schedule tables.")
    connection = op.get_bind()
    for table_name in _TABLES:
        row_count = connection.execute(sa.text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()
        if row_count != 0:
            raise RuntimeError("Schedule boundary downgrade requires empty tables.")
    op.drop_table(_AUDIT_TABLE)
    op.drop_index("ix_xianyu_schedule_publish", table_name=_REQUEST_TABLE)
    op.drop_index("ix_xianyu_schedule_due_pending", table_name=_REQUEST_TABLE)
    op.drop_table(_REQUEST_TABLE)
