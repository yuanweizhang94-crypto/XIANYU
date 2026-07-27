"""SQLAlchemy projection and repositories for local deterministic replies."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Table,
    and_,
    func,
    select,
)
from sqlalchemy.orm import Session

from xianyu_system.core.database import Base
from xianyu_system.reply.domain import (
    ReplyAuditEvent,
    ReplyCondition,
    ReplyLifecycleState,
    ReplyPriority,
    ReplyRule,
    ReplyRuleSnapshot,
    ReplyTemplate,
    TemplateVariableName,
    flags_from_canonical,
    validate_lifecycle_transition,
)

reply_template_table = Table(
    "xianyu_reply_templates",
    Base.metadata,
    Column("template_id", String(36), primary_key=True, nullable=False),
    Column("version", Integer, primary_key=True, nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("lifecycle_state", String(16), nullable=False),
    Column("script_text", String(2048), nullable=False),
    Column("variable_allowlist", String(1024), nullable=False),
    Column("row_version", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    ForeignKeyConstraint(
        ["profile_id"],
        ["xianyu_account_profiles.profile_id"],
        name="fk_xianyu_reply_template_profile",
        ondelete="RESTRICT",
    ),
    CheckConstraint("length(template_id) = 36", name="ck_xianyu_reply_template_id_len"),
    CheckConstraint("version >= 1", name="ck_xianyu_reply_template_version_positive"),
    CheckConstraint("row_version >= 1", name="ck_xianyu_reply_template_row_version_positive"),
    CheckConstraint(
        "lifecycle_state IN ('DRAFT','ENABLED','DISABLED','ARCHIVED')",
        name="ck_xianyu_reply_template_lifecycle",
    ),
    CheckConstraint(
        "account_reference = trim(account_reference) AND length(account_reference) >= 1 AND length(account_reference) <= 256",
        name="ck_xianyu_reply_template_account_len",
    ),
    CheckConstraint(
        "length(script_text) >= 1 AND length(script_text) <= 2048 AND length(trim(script_text)) >= 1",
        name="ck_xianyu_reply_template_script_len",
    ),
    extend_existing=True,
)

reply_rule_table = Table(
    "xianyu_reply_rules",
    Base.metadata,
    Column("rule_id", String(36), primary_key=True, nullable=False),
    Column("version", Integer, primary_key=True, nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("name", String(128), nullable=True),
    Column("lifecycle_state", String(16), nullable=False),
    Column("template_id", String(36), nullable=False),
    Column("template_version", Integer, nullable=False),
    Column("priority", Integer, nullable=False),
    Column("row_version", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    ForeignKeyConstraint(
        ["profile_id"],
        ["xianyu_account_profiles.profile_id"],
        name="fk_xianyu_reply_rule_profile",
        ondelete="RESTRICT",
    ),
    ForeignKeyConstraint(
        ["template_id", "template_version"],
        ["xianyu_reply_templates.template_id", "xianyu_reply_templates.version"],
        name="fk_xianyu_reply_rule_template_version",
        ondelete="RESTRICT",
    ),
    CheckConstraint("length(rule_id) = 36", name="ck_xianyu_reply_rule_id_len"),
    CheckConstraint("version >= 1", name="ck_xianyu_reply_rule_version_positive"),
    CheckConstraint("row_version >= 1", name="ck_xianyu_reply_rule_row_version_positive"),
    CheckConstraint("priority >= 0", name="ck_xianyu_reply_rule_priority_non_negative"),
    CheckConstraint(
        "lifecycle_state IN ('DRAFT','ENABLED','DISABLED','ARCHIVED')",
        name="ck_xianyu_reply_rule_lifecycle",
    ),
    CheckConstraint(
        "account_reference = trim(account_reference) AND length(account_reference) >= 1 AND length(account_reference) <= 256",
        name="ck_xianyu_reply_rule_account_len",
    ),
    CheckConstraint(
        "name IS NULL OR (name = trim(name) AND length(name) >= 1 AND length(name) <= 128)",
        name="ck_xianyu_reply_rule_name_len",
    ),
    extend_existing=True,
)
Index(
    "uq_xianyu_reply_rule_one_enabled_version",
    reply_rule_table.c.profile_id,
    reply_rule_table.c.account_reference,
    reply_rule_table.c.rule_id,
    unique=True,
    sqlite_where=reply_rule_table.c.lifecycle_state == "ENABLED",
)

reply_condition_table = Table(
    "xianyu_reply_conditions",
    Base.metadata,
    Column("condition_id", String(36), primary_key=True, nullable=False),
    Column("rule_id", String(36), nullable=False),
    Column("rule_version", Integer, nullable=False),
    Column("sequence", Integer, nullable=False),
    Column("field_name", String(64), nullable=False),
    Column("operator", String(32), nullable=False),
    Column("expected_value", String(512), nullable=False),
    Column("normalization", String(32), nullable=False),
    Column("case_sensitive", Integer, nullable=False),
    ForeignKeyConstraint(
        ["rule_id", "rule_version"],
        ["xianyu_reply_rules.rule_id", "xianyu_reply_rules.version"],
        name="fk_xianyu_reply_condition_rule_version",
        ondelete="RESTRICT",
    ),
    CheckConstraint("length(condition_id) = 36", name="ck_xianyu_reply_condition_id_len"),
    CheckConstraint("rule_version >= 1", name="ck_xianyu_reply_condition_rule_version_positive"),
    CheckConstraint("sequence >= 1", name="ck_xianyu_reply_condition_sequence_positive"),
    CheckConstraint(
        "field_name IN ('content_text','language_hint')", name="ck_xianyu_reply_condition_field"
    ),
    CheckConstraint(
        "operator IN ('equals','contains','starts_with','ends_with')",
        name="ck_xianyu_reply_condition_operator",
    ),
    CheckConstraint(
        "length(expected_value) >= 1 AND length(expected_value) <= 512 AND length(trim(expected_value)) >= 1",
        name="ck_xianyu_reply_condition_expected_len",
    ),
    CheckConstraint(
        "normalization IN ('','NFKC','TRIM','NFKC,TRIM')",
        name="ck_xianyu_reply_condition_normalization",
    ),
    CheckConstraint("case_sensitive IN (0,1)", name="ck_xianyu_reply_condition_case_sensitive"),
    extend_existing=True,
)
Index(
    "ix_xianyu_reply_condition_rule_version",
    reply_condition_table.c.rule_id,
    reply_condition_table.c.rule_version,
    reply_condition_table.c.sequence,
)

reply_audit_event_table = Table(
    "xianyu_reply_audit_events",
    Base.metadata,
    Column("audit_event_id", String(36), primary_key=True, nullable=False),
    Column("profile_id", String(36), nullable=False),
    Column("account_reference", String(256), nullable=False),
    Column("conversation_id", String(36), nullable=False),
    Column("message_id", String(36), nullable=False),
    Column("rule_id", String(36), nullable=True),
    Column("rule_version", Integer, nullable=True),
    Column("template_id", String(36), nullable=True),
    Column("template_version", Integer, nullable=True),
    Column("decision_type", String(16), nullable=False),
    Column("reason_code", String(64), nullable=False),
    Column("failure_category", String(64), nullable=True),
    Column("occurred_at", DateTime(timezone=True), nullable=False),
    Column("correlation_identifier", String(128), nullable=True),
    ForeignKeyConstraint(
        ["message_id", "profile_id", "account_reference"],
        [
            "xianyu_message_records.message_id",
            "xianyu_message_records.profile_id",
            "xianyu_message_records.account_reference",
        ],
        name="fk_xianyu_reply_audit_message_owner",
        ondelete="RESTRICT",
    ),
    ForeignKeyConstraint(
        ["rule_id", "rule_version"],
        ["xianyu_reply_rules.rule_id", "xianyu_reply_rules.version"],
        name="fk_xianyu_reply_audit_rule_version",
        ondelete="RESTRICT",
    ),
    ForeignKeyConstraint(
        ["template_id", "template_version"],
        ["xianyu_reply_templates.template_id", "xianyu_reply_templates.version"],
        name="fk_xianyu_reply_audit_template_version",
        ondelete="RESTRICT",
    ),
    CheckConstraint("length(audit_event_id) = 36", name="ck_xianyu_reply_audit_id_len"),
    CheckConstraint(
        "(rule_id IS NULL AND rule_version IS NULL) OR (rule_id IS NOT NULL AND rule_version IS NOT NULL)",
        name="ck_xianyu_reply_audit_rule_pair",
    ),
    CheckConstraint(
        "(template_id IS NULL AND template_version IS NULL) OR (template_id IS NOT NULL AND template_version IS NOT NULL)",
        name="ck_xianyu_reply_audit_template_pair",
    ),
    CheckConstraint(
        "decision_type IN ('REPLY','NO_MATCH','CONFLICT','ESCALATE','SUPPRESSED','INVALID_INPUT')",
        name="ck_xianyu_reply_audit_decision",
    ),
    CheckConstraint(
        "failure_category IS NULL OR (failure_category = trim(failure_category) AND length(failure_category) >= 1 AND length(failure_category) <= 64)",
        name="ck_xianyu_reply_audit_failure_len",
    ),
    extend_existing=True,
)
Index(
    "ix_xianyu_reply_audit_message",
    reply_audit_event_table.c.message_id,
    reply_audit_event_table.c.profile_id,
    reply_audit_event_table.c.account_reference,
)


class _TemplateRecord:
    template_id: str
    version: int
    profile_id: str
    account_reference: str
    lifecycle_state: str
    script_text: str
    variable_allowlist: str
    row_version: int
    created_at: datetime
    updated_at: datetime


class _RuleRecord:
    rule_id: str
    version: int
    profile_id: str
    account_reference: str
    name: str | None
    lifecycle_state: str
    template_id: str
    template_version: int
    priority: int
    row_version: int
    created_at: datetime
    updated_at: datetime


class _ConditionRecord:
    condition_id: str
    rule_id: str
    rule_version: int
    sequence: int
    field_name: str
    operator: str
    expected_value: str
    normalization: str
    case_sensitive: int


class _AuditRecord:
    audit_event_id: str
    profile_id: str
    account_reference: str
    conversation_id: str
    message_id: str
    rule_id: str | None
    rule_version: int | None
    template_id: str | None
    template_version: int | None
    decision_type: str
    reason_code: str
    failure_category: str | None
    occurred_at: datetime
    correlation_identifier: str | None


Base.registry.map_imperatively(_TemplateRecord, reply_template_table)
Base.registry.map_imperatively(_RuleRecord, reply_rule_table)
Base.registry.map_imperatively(_ConditionRecord, reply_condition_table)
Base.registry.map_imperatively(_AuditRecord, reply_audit_event_table)


def _aware(value: datetime | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _allowlist_text(values: tuple[TemplateVariableName, ...]) -> str:
    return ",".join(item.value for item in values)


def _allowlist_values(value: str) -> tuple[TemplateVariableName, ...]:
    if value == "":
        return ()
    return tuple(TemplateVariableName(part) for part in value.split(","))


def _set_values(record: object, values: dict[str, Any]) -> None:
    for key, value in values.items():
        setattr(record, key, value)


def _template_values(template: ReplyTemplate) -> dict[str, Any]:
    return {
        "template_id": template.template_id,
        "version": template.version,
        "profile_id": template.profile_id,
        "account_reference": template.account_reference,
        "lifecycle_state": template.lifecycle_state.value,
        "script_text": template.script_text,
        "variable_allowlist": _allowlist_text(template.variable_allowlist),
        "row_version": template.row_version,
        "created_at": template.created_at,
        "updated_at": template.updated_at,
    }


def _rule_values(rule: ReplyRule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "version": rule.version,
        "profile_id": rule.profile_id,
        "account_reference": rule.account_reference,
        "name": rule.name,
        "lifecycle_state": rule.lifecycle_state.value,
        "template_id": rule.template_id,
        "template_version": rule.template_version,
        "priority": rule.priority.value,
        "row_version": rule.row_version,
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }


def _condition_values(condition_id: str, condition: ReplyCondition) -> dict[str, Any]:
    return {
        "condition_id": condition_id,
        "rule_id": condition.rule_id,
        "rule_version": condition.rule_version,
        "sequence": condition.sequence,
        "field_name": condition.field_name,
        "operator": condition.operator,
        "expected_value": condition.expected_value,
        "normalization": condition.canonical_normalization,
        "case_sensitive": 1 if condition.case_sensitive else 0,
    }


def _audit_values(event: ReplyAuditEvent) -> dict[str, Any]:
    ids = event.identifiers
    return {
        "audit_event_id": event.audit_event_id,
        "profile_id": ids.profile_id,
        "account_reference": ids.account_reference,
        "conversation_id": ids.conversation_id,
        "message_id": ids.message_id,
        "rule_id": event.rule_id,
        "rule_version": event.rule_version,
        "template_id": event.template_id,
        "template_version": event.template_version,
        "decision_type": event.decision_type.value,
        "reason_code": event.reason_code.value,
        "failure_category": event.failure_category,
        "occurred_at": event.occurred_at,
        "correlation_identifier": event.correlation_identifier,
    }


def _record_to_template(record: _TemplateRecord) -> ReplyTemplate:
    return ReplyTemplate(
        template_id=record.template_id,
        version=record.version,
        profile_id=record.profile_id,
        account_reference=record.account_reference,
        lifecycle_state=ReplyLifecycleState(record.lifecycle_state),
        script_text=record.script_text,
        variable_allowlist=_allowlist_values(record.variable_allowlist),
        row_version=record.row_version,
        created_at=_aware(record.created_at),
        updated_at=_aware(record.updated_at),
    )


def _record_to_rule(record: _RuleRecord) -> ReplyRule:
    return ReplyRule(
        rule_id=record.rule_id,
        version=record.version,
        profile_id=record.profile_id,
        account_reference=record.account_reference,
        lifecycle_state=ReplyLifecycleState(record.lifecycle_state),
        template_id=record.template_id,
        template_version=record.template_version,
        priority=ReplyPriority(record.priority),
        row_version=record.row_version,
        created_at=_aware(record.created_at),
        updated_at=_aware(record.updated_at),
        name=record.name,
    )


def _record_to_condition(record: _ConditionRecord) -> ReplyCondition:
    return ReplyCondition(
        rule_id=record.rule_id,
        rule_version=record.rule_version,
        field_name=record.field_name,
        operator=record.operator,
        expected_value=record.expected_value,
        normalization_flags=flags_from_canonical(record.normalization),
        case_sensitive=bool(record.case_sensitive),
        sequence=record.sequence,
    )


class ReplyTemplateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_template(self, template: ReplyTemplate) -> None:
        record = _TemplateRecord()
        _set_values(record, _template_values(template))
        self._session.add(record)
        self._session.flush()

    def get_template(
        self, *, template_id: str, template_version: int, profile_id: str, account_reference: str
    ) -> ReplyTemplate | None:
        record = self._session.scalars(
            select(_TemplateRecord)
            .where(reply_template_table.c.template_id == template_id)
            .where(reply_template_table.c.version == template_version)
            .where(reply_template_table.c.profile_id == profile_id)
            .where(reply_template_table.c.account_reference == account_reference)
        ).one_or_none()
        return None if record is None else _record_to_template(record)

    def transition_template(
        self, *, template_id: str, version: int, target: ReplyLifecycleState
    ) -> None:
        record = self._session.get(
            _TemplateRecord, {"template_id": template_id, "version": version}
        )
        if record is None:
            raise LookupError("reply template not found")
        record.lifecycle_state = validate_lifecycle_transition(record.lifecycle_state, target).value
        record.row_version += 1
        record.updated_at = datetime.now(UTC)
        self._session.flush()


class ReplyRuleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_rule(self, rule: ReplyRule) -> None:
        if rule.lifecycle_state == ReplyLifecycleState.ENABLED and self._enabled_rule_exists(rule):
            raise ReplyValueError()
        record = _RuleRecord()
        _set_values(record, _rule_values(rule))
        self._session.add(record)
        self._session.flush()

    def add_condition(self, *, condition_id: str, condition: ReplyCondition) -> None:
        record = _ConditionRecord()
        _set_values(record, _condition_values(condition_id, condition))
        self._session.add(record)
        self._session.flush()

    def transition_rule(self, *, rule_id: str, version: int, target: ReplyLifecycleState) -> None:
        record = self._session.get(_RuleRecord, {"rule_id": rule_id, "version": version})
        if record is None:
            raise LookupError("reply rule not found")
        target_state = validate_lifecycle_transition(record.lifecycle_state, target)
        if target_state == ReplyLifecycleState.ENABLED and self._enabled_rule_exists(
            _record_to_rule(record)
        ):
            raise ReplyValueError()
        record.lifecycle_state = target_state.value
        record.row_version += 1
        record.updated_at = datetime.now(UTC)
        self._session.flush()

    def list_enabled_snapshots(
        self, *, profile_id: str, account_reference: str
    ) -> tuple[ReplyRuleSnapshot, ...]:
        records = list(
            self._session.scalars(
                select(_RuleRecord)
                .where(reply_rule_table.c.profile_id == profile_id)
                .where(reply_rule_table.c.account_reference == account_reference)
                .where(reply_rule_table.c.lifecycle_state == ReplyLifecycleState.ENABLED.value)
            )
        )
        snapshots: list[ReplyRuleSnapshot] = []
        for record in records:
            condition_records = self._session.scalars(
                select(_ConditionRecord)
                .where(reply_condition_table.c.rule_id == record.rule_id)
                .where(reply_condition_table.c.rule_version == record.version)
                .order_by(reply_condition_table.c.sequence)
            ).all()
            snapshots.append(
                ReplyRuleSnapshot(
                    rule_id=record.rule_id,
                    rule_version=record.version,
                    template_id=record.template_id,
                    template_version=record.template_version,
                    lifecycle_state=ReplyLifecycleState(record.lifecycle_state),
                    priority=record.priority,
                    conditions=tuple(_record_to_condition(item) for item in condition_records),
                )
            )
        return tuple(snapshots)

    def _enabled_rule_exists(self, rule: ReplyRule) -> bool:
        count = self._session.scalar(
            select(func.count())
            .select_from(reply_rule_table)
            .where(
                and_(
                    reply_rule_table.c.profile_id == rule.profile_id,
                    reply_rule_table.c.account_reference == rule.account_reference,
                    reply_rule_table.c.rule_id == rule.rule_id,
                    reply_rule_table.c.lifecycle_state == ReplyLifecycleState.ENABLED.value,
                    reply_rule_table.c.version != rule.version,
                )
            )
        )
        return bool(count)


class ReplyAuditRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_audit_event(self, event: ReplyAuditEvent) -> None:
        record = _AuditRecord()
        _set_values(record, _audit_values(event))
        self._session.add(record)
        self._session.flush()

    def count_audit_events(self) -> int:
        return int(
            self._session.scalar(select(func.count()).select_from(reply_audit_event_table)) or 0
        )


class ReplyValueError(ValueError):
    """Internal sanitized invalid persisted reply state."""
