from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import pytest
from sqlalchemy import Integer, String, inspect, text
from sqlalchemy.exc import IntegrityError

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)
from xianyu_system.reply.domain import (
    NormalizationFlag,
    ReplyAuditEvent,
    ReplyAuditIdentifiers,
    ReplyCondition,
    ReplyDecisionType,
    ReplyLifecycleState,
    ReplyPriority,
    ReplyReasonCode,
    ReplyRule,
    ReplyTemplate,
    TemplateVariableName,
)
from xianyu_system.reply.persistence import (
    ReplyAuditRepository,
    ReplyRuleRepository,
    ReplyTemplateRepository,
    reply_audit_event_table,
    reply_condition_table,
    reply_rule_table,
    reply_template_table,
)
from xianyu_system.worker.account.service import AccountService
from xianyu_system.worker.message.service import MessageService
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

NOW = datetime(2026, 1, 1, tzinfo=UTC)
REPLY_REVISION = "0004_xianyu_reply_boundary"
PUBLISH_REVISION = "0005_xianyu_publish_boundary"
MESSAGE_REVISION = "0003_xianyu_message_boundary"
PROFILE_ALIAS = "reply-persistence-profile"
ACCOUNT_REFERENCE = "reply-persistence-account"
RULE_ID = "00000000-0000-4000-8000-000000000501"
TEMPLATE_ID = "00000000-0000-4000-8000-000000000502"
CONDITION_ID = "00000000-0000-4000-8000-000000000503"
AUDIT_ID = "00000000-0000-4000-8000-000000000504"


def setup_resources(tmp_path: Path) -> DatabaseResources:
    resources = initialize_database(tmp_path / "reply-persistence.db")
    upgrade_database(resources)
    return resources


def seed_owner_message(resources: DatabaseResources) -> tuple[str, str, str]:
    profile = AccountService(resources.session_factory).create_profile(account_alias=PROFILE_ALIAS)
    result = MessageService(resources.session_factory).receive(
        SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=ACCOUNT_REFERENCE,
            participant_reference="synthetic-participant",
            message_content="你好，购买A款",
            received_at=NOW,
            platform_conversation_identifier="reply-contract-conversation",
            platform_message_identifier="reply-contract-message",
            delivery_identity="reply-contract-delivery",
            platform_timestamp=NOW,
        )
    )
    return profile.profile_id, result.conversation_id, result.message_id


def template(
    profile_id: str, state: ReplyLifecycleState = ReplyLifecycleState.ENABLED
) -> ReplyTemplate:
    return ReplyTemplate(
        template_id=TEMPLATE_ID,
        version=1,
        profile_id=profile_id,
        account_reference=ACCOUNT_REFERENCE,
        lifecycle_state=state,
        script_text="固定回复 {account_reference}",
        variable_allowlist=(TemplateVariableName("account_reference"),),
        row_version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def rule(
    profile_id: str, version: int = 1, state: ReplyLifecycleState = ReplyLifecycleState.ENABLED
) -> ReplyRule:
    return ReplyRule(
        rule_id=RULE_ID,
        version=version,
        profile_id=profile_id,
        account_reference=ACCOUNT_REFERENCE,
        lifecycle_state=state,
        template_id=TEMPLATE_ID,
        template_version=1,
        priority=ReplyPriority(0),
        row_version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def condition(version: int = 1) -> ReplyCondition:
    return ReplyCondition(
        rule_id=RULE_ID,
        rule_version=version,
        field_name="content_text",
        operator="contains",
        expected_value="购买A款",
        normalization_flags=(NormalizationFlag.TRIM, NormalizationFlag.NFKC),
    )


def test_reply_tables_columns_keys_foreign_keys_checks_and_indexes(tmp_path: Path) -> None:
    expected_tables = {
        "xianyu_reply_templates": reply_template_table,
        "xianyu_reply_rules": reply_rule_table,
        "xianyu_reply_conditions": reply_condition_table,
        "xianyu_reply_audit_events": reply_audit_event_table,
    }
    assert set(expected_tables) == {
        "xianyu_reply_templates",
        "xianyu_reply_rules",
        "xianyu_reply_conditions",
        "xianyu_reply_audit_events",
    }
    assert [column.name for column in reply_template_table.primary_key.columns] == [
        "template_id",
        "version",
    ]
    assert [column.name for column in reply_rule_table.primary_key.columns] == [
        "rule_id",
        "version",
    ]
    assert "enabled" not in reply_template_table.c
    assert "enabled" not in reply_rule_table.c
    for prohibited in ["metadata", "payload", "raw_payload", "properties", "extras"]:
        assert prohibited not in reply_audit_event_table.c
    assert isinstance(reply_rule_table.c.priority.type, Integer)
    assert isinstance(reply_condition_table.c.field_name.type, String)

    resources = setup_resources(tmp_path)
    try:
        inspector = inspect(resources.engine)
        assert set(inspector.get_table_names()) >= set(expected_tables)
        rule_fks = inspector.get_foreign_keys("xianyu_reply_rules")
        assert any(fk["referred_table"] == "xianyu_reply_templates" for fk in rule_fks)
        condition_fks = inspector.get_foreign_keys("xianyu_reply_conditions")
        assert condition_fks[0]["referred_table"] == "xianyu_reply_rules"
        audit_checks = {
            check["name"] for check in inspector.get_check_constraints("xianyu_reply_audit_events")
        }
        assert "ck_xianyu_reply_audit_rule_pair" in audit_checks
        indexes = {index["name"] for index in inspector.get_indexes("xianyu_reply_rules")}
        assert "uq_xianyu_reply_rule_one_enabled_version" in indexes
    finally:
        dispose_database(resources)


def test_repository_flush_without_commit_and_exact_rule_version_snapshots(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        profile_id, _conversation_id, _message_id = seed_owner_message(resources)
        session = resources.session_factory()
        commit_calls = 0

        def count_commit() -> None:
            nonlocal commit_calls
            commit_calls += 1

        cast(Any, session).commit = count_commit
        templates = ReplyTemplateRepository(session)
        rules = ReplyRuleRepository(session)
        templates.add_template(template(profile_id))
        rules.add_rule(rule(profile_id))
        rules.add_condition(condition_id=CONDITION_ID, condition=condition())
        assert commit_calls == 0
        snapshots = rules.list_enabled_snapshots(
            profile_id=profile_id, account_reference=ACCOUNT_REFERENCE
        )
        assert len(snapshots) == 1
        assert snapshots[0].rule_id == RULE_ID
        assert snapshots[0].rule_version == 1
        session.rollback()
        session.close()
        assert count_rows(resources, "xianyu_reply_rules") == 0
    finally:
        dispose_database(resources)


def count_rows(resources: DatabaseResources, table_name: str) -> int:
    with resources.engine.connect() as connection:
        return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


def test_database_constraints_and_one_enabled_version_per_scope(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        profile_id, _conversation_id, _message_id = seed_owner_message(resources)
        with resources.session_factory() as session:
            templates = ReplyTemplateRepository(session)
            rules = ReplyRuleRepository(session)
            templates.add_template(template(profile_id))
            rules.add_rule(rule(profile_id))
            rules.add_condition(condition_id=CONDITION_ID, condition=condition())
            with pytest.raises(ValueError):
                rules.add_rule(rule(profile_id, version=2))
            session.commit()
        with resources.engine.begin() as connection:
            now_text = NOW.isoformat()
            for sql in [
                "INSERT INTO xianyu_reply_rules (rule_id, version, profile_id, account_reference, lifecycle_state, template_id, template_version, priority, row_version, created_at, updated_at) VALUES ('bad', 0, :profile_id, :account_reference, 'ENABLED', :template_id, 1, -1, 0, :now, :now)",
                "INSERT INTO xianyu_reply_audit_events (audit_event_id, profile_id, account_reference, conversation_id, message_id, rule_id, rule_version, decision_type, reason_code, occurred_at) VALUES (:audit_id, :profile_id, :account_reference, '00000000-0000-4000-8000-000000000599', '00000000-0000-4000-8000-000000000598', :rule_id, NULL, 'NO_MATCH', 'NO_RULE_MATCHED', :now)",
            ]:
                with pytest.raises(IntegrityError):
                    connection.execute(
                        text(sql),
                        {
                            "audit_id": "00000000-0000-4000-8000-000000000597",
                            "profile_id": profile_id,
                            "account_reference": ACCOUNT_REFERENCE,
                            "template_id": TEMPLATE_ID,
                            "rule_id": RULE_ID,
                            "now": now_text,
                        },
                    )
    finally:
        dispose_database(resources)


def test_audit_stores_identifiers_reason_codes_and_no_content_or_rendered_text(
    tmp_path: Path,
) -> None:
    resources = setup_resources(tmp_path)
    try:
        profile_id, conversation_id, message_id = seed_owner_message(resources)
        with resources.session_factory() as session:
            templates = ReplyTemplateRepository(session)
            rules = ReplyRuleRepository(session)
            audit = ReplyAuditRepository(session)
            templates.add_template(template(profile_id))
            rules.add_rule(rule(profile_id))
            event = ReplyAuditEvent(
                audit_event_id=AUDIT_ID,
                identifiers=ReplyAuditIdentifiers(
                    profile_id, ACCOUNT_REFERENCE, conversation_id, message_id
                ),
                decision_type=ReplyDecisionType.NO_MATCH,
                reason_code=ReplyReasonCode.NO_RULE_MATCHED,
                occurred_at=NOW,
                rule_id=RULE_ID,
                rule_version=1,
                template_id=TEMPLATE_ID,
                template_version=1,
                failure_category=ReplyReasonCode.NO_RULE_MATCHED.value,
            )
            audit.add_audit_event(event)
            session.commit()
        with resources.engine.connect() as connection:
            row = (
                connection.execute(text("SELECT * FROM xianyu_reply_audit_events")).mappings().one()
            )
        assert row["message_id"] == message_id
        assert row["reason_code"] == ReplyReasonCode.NO_RULE_MATCHED.value
        assert "message_content" not in row
        assert "rendered_text" not in row
    finally:
        dispose_database(resources)


def test_empty_downgrade_and_nonempty_downgrade_fail_closed(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        downgrade_database(resources, revision=MESSAGE_REVISION)
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert "xianyu_reply_rules" not in inspect(resources.engine).get_table_names()
        upgrade_database(resources)
        assert get_current_revision(resources) == PUBLISH_REVISION
        profile_id, _conversation_id, _message_id = seed_owner_message(resources)
        with resources.session_factory() as session:
            ReplyTemplateRepository(session).add_template(template(profile_id))
            session.commit()
        with pytest.raises(RuntimeError):
            downgrade_database(resources, revision=MESSAGE_REVISION)
        assert get_current_revision(resources) == PUBLISH_REVISION
        assert count_rows(resources, "xianyu_reply_templates") == 1
    finally:
        dispose_database(resources)
