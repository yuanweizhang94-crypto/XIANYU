"""Create local deterministic publish boundary tables."""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic.runtime.migration import MigrationContext

revision: str = "0005_xianyu_publish_boundary"
down_revision: str | None = "0004_xianyu_reply_boundary"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_REQUEST_TABLE = "xianyu_publish_requests"
_AUDIT_TABLE = "xianyu_publish_audit_events"
_ATTEMPT_TABLE = "xianyu_publish_attempt_snapshots"
_TABLES = [_ATTEMPT_TABLE, _AUDIT_TABLE, _REQUEST_TABLE]


def upgrade() -> None:
    op.create_table(
        _REQUEST_TABLE,
        sa.Column("request_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("draft_id", sa.String(length=36), nullable=False),
        sa.Column("draft_revision", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False, unique=True),
        sa.Column("normalized_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("decision_type", sa.String(length=32), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("request_lifecycle", sa.String(length=32), nullable=False),
        sa.Column("authorization_state", sa.String(length=16), nullable=False),
        sa.Column("risk_state", sa.String(length=16), nullable=False),
        sa.Column("synthetic_fixture", sa.Boolean(), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_request_id_len"),
        sa.CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_request_draft_id_len"),
        sa.CheckConstraint(
            "draft_revision >= 1",
            name="ck_xianyu_publish_request_revision_positive",
        ),
        sa.CheckConstraint(
            "idempotency_key = trim(idempotency_key) AND "
            "length(idempotency_key) >= 1 AND length(idempotency_key) <= 128",
            name="ck_xianyu_publish_request_idempotency_len",
        ),
        sa.CheckConstraint(
            "length(normalized_fingerprint) = 64",
            name="ck_xianyu_publish_fingerprint_len",
        ),
        sa.CheckConstraint(
            "decision_type IN ('READY','INVALID_INPUT','UNAUTHORIZED','RISK_BLOCKED','DUPLICATE','CONFLICT','MANUAL_REVIEW')",
            name="ck_xianyu_publish_request_decision",
        ),
        sa.CheckConstraint(
            "request_lifecycle IN ('RECEIVED','VALIDATED','REJECTED','READY','DUPLICATE','CONFLICT','MANUAL_REVIEW')",
            name="ck_xianyu_publish_request_lifecycle",
        ),
    )
    op.create_index(
        "ix_xianyu_publish_draft_fingerprint",
        _REQUEST_TABLE,
        ["draft_id", "draft_revision", "normalized_fingerprint"],
        unique=False,
    )

    op.create_table(
        _AUDIT_TABLE,
        sa.Column("event_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("draft_id", sa.String(length=36), nullable=False),
        sa.Column("draft_revision", sa.Integer(), nullable=False),
        sa.Column("decision_type", sa.String(length=32), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("failure_category", sa.String(length=64), nullable=True),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("synthetic_fixture", sa.Boolean(), nullable=False),
        sa.CheckConstraint("length(event_id) = 36", name="ck_xianyu_publish_audit_id_len"),
        sa.CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_audit_request_id_len"),
        sa.CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_audit_draft_id_len"),
        sa.CheckConstraint(
            "draft_revision >= 1",
            name="ck_xianyu_publish_audit_revision_positive",
        ),
        sa.CheckConstraint(
            "event_type = trim(event_type) AND length(event_type) >= 1 AND length(event_type) <= 32",
            name="ck_xianyu_publish_audit_event_type_len",
        ),
    )

    op.create_table(
        _ATTEMPT_TABLE,
        sa.Column("attempt_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("draft_id", sa.String(length=36), nullable=False),
        sa.Column("draft_revision", sa.Integer(), nullable=False),
        sa.Column("normalized_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("attempt_state", sa.String(length=16), nullable=False),
        sa.Column("outcome_type", sa.String(length=16), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sanitized_error_code", sa.String(length=64), nullable=True),
        sa.CheckConstraint("length(attempt_id) = 36", name="ck_xianyu_publish_attempt_id_len"),
        sa.CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_attempt_request_id_len"),
        sa.CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_attempt_draft_id_len"),
        sa.CheckConstraint(
            "draft_revision >= 1",
            name="ck_xianyu_publish_attempt_revision_positive",
        ),
        sa.CheckConstraint(
            "length(normalized_fingerprint) = 64",
            name="ck_xianyu_publish_attempt_fingerprint_len",
        ),
        sa.CheckConstraint(
            "attempt_number >= 1",
            name="ck_xianyu_publish_attempt_number_positive",
        ),
        sa.CheckConstraint(
            "attempt_state IN ('NOT_STARTED','IN_PROGRESS','COMPLETED')",
            name="ck_xianyu_publish_attempt_state",
        ),
        sa.CheckConstraint(
            "outcome_type IN ('SUCCEEDED','FAILED','UNKNOWN','CANCELLED')",
            name="ck_xianyu_publish_attempt_outcome",
        ),
    )
    op.create_index(
        "ix_xianyu_publish_attempt_unknown",
        _ATTEMPT_TABLE,
        ["draft_id", "draft_revision", "normalized_fingerprint", "outcome_type"],
        unique=False,
    )


def downgrade() -> None:
    context = op.get_context()
    if isinstance(context, MigrationContext) and context.as_sql:
        raise RuntimeError("Offline downgrade is not approved for publish tables.")
    connection = op.get_bind()
    for table_name in _TABLES:
        row_count = connection.execute(sa.text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()
        if row_count != 0:
            raise RuntimeError("Publish boundary downgrade requires empty tables.")
    op.drop_index("ix_xianyu_publish_attempt_unknown", table_name=_ATTEMPT_TABLE)
    op.drop_table(_ATTEMPT_TABLE)
    op.drop_table(_AUDIT_TABLE)
    op.drop_index("ix_xianyu_publish_draft_fingerprint", table_name=_REQUEST_TABLE)
    op.drop_table(_REQUEST_TABLE)
