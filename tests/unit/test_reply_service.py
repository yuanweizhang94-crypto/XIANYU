from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    initialize_database,
    upgrade_database,
)
from xianyu_system.reply.domain import (
    NormalizationFlag,
    ReplyAuthorizationState,
    ReplyCondition,
    ReplyDecisionType,
    ReplyLifecycleState,
    ReplyPersistenceError,
    ReplyPriority,
    ReplyReasonCode,
    ReplyRiskState,
    ReplyRule,
    ReplyTemplate,
    TemplateVariableName,
)
from xianyu_system.reply.persistence import (
    ReplyAuditRepository,
    ReplyRuleRepository,
    ReplyTemplateRepository,
)
from xianyu_system.reply.service import ReplyService
from xianyu_system.worker.account.service import AccountService
from xianyu_system.worker.message.service import MessageService
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

NOW = datetime(2026, 1, 1, tzinfo=UTC)
PROFILE_ALIAS = "reply-service-profile"
ACCOUNT_REFERENCE = "reply-service-account"
CONVERSATION_KEY = "reply-service-conversation"
RULE_ID = "00000000-0000-4000-8000-000000000401"
RULE_ID_2 = "00000000-0000-4000-8000-000000000402"
TEMPLATE_ID = "00000000-0000-4000-8000-000000000403"
TEMPLATE_ID_2 = "00000000-0000-4000-8000-000000000404"


@dataclass(frozen=True)
class ReplySource:
    profile_id: str
    account_reference: str
    conversation_id: str
    message_id: str
    message_content: str
    language_hint: str = "zh-cn"
    is_synthetic: bool = True
    reply_authorization_state: ReplyAuthorizationState = (
        ReplyAuthorizationState.EXPLICITLY_AUTHORIZED
    )
    reply_risk_state: ReplyRiskState = ReplyRiskState.LOW
    reply_suppression_asserted: bool = False
    reply_sensitive_topic_asserted: bool = False
    reply_human_transfer_requested: bool = False
    correlation_identifier: str = "reply-correlation"


@pytest.fixture()
def resources(tmp_path: Path):
    db = initialize_database(tmp_path / "reply-service.db")
    upgrade_database(db)
    try:
        yield db
    finally:
        dispose_database(db)


def seed_message(resources: DatabaseResources, content: str = "你好，想购买A款") -> ReplySource:
    profile = AccountService(resources.session_factory).create_profile(account_alias=PROFILE_ALIAS)
    result = MessageService(resources.session_factory).receive(
        SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=ACCOUNT_REFERENCE,
            participant_reference="synthetic-participant",
            message_content=content,
            received_at=NOW,
            platform_conversation_identifier=CONVERSATION_KEY,
            platform_message_identifier="reply-message",
            delivery_identity="reply-delivery",
            platform_timestamp=NOW,
            correlation_identifier="reply-message-correlation",
        )
    )
    return ReplySource(
        profile_id=profile.profile_id,
        account_reference=ACCOUNT_REFERENCE,
        conversation_id=result.conversation_id,
        message_id=result.message_id,
        message_content=content,
    )


def seed_rule(
    resources: DatabaseResources,
    *,
    profile_id: str,
    template_id: str = TEMPLATE_ID,
    rule_id: str = RULE_ID,
    template_state: ReplyLifecycleState = ReplyLifecycleState.ENABLED,
    script: str = "固定回复 {account_reference}",
    allowlist: tuple[str, ...] = ("account_reference",),
    priority: int = 0,
    condition_id: str = "00000000-0000-4000-8000-000000000499",
) -> None:
    with resources.session_factory() as session:
        template_repository = ReplyTemplateRepository(session)
        rule_repository = ReplyRuleRepository(session)
        template_repository.add_template(
            ReplyTemplate(
                template_id=template_id,
                version=1,
                profile_id=profile_id,
                account_reference=ACCOUNT_REFERENCE,
                lifecycle_state=template_state,
                script_text=script,
                variable_allowlist=tuple(TemplateVariableName(item) for item in allowlist),
                row_version=1,
                created_at=NOW,
                updated_at=NOW,
            )
        )
        rule_repository.add_rule(
            ReplyRule(
                rule_id=rule_id,
                version=1,
                profile_id=profile_id,
                account_reference=ACCOUNT_REFERENCE,
                lifecycle_state=ReplyLifecycleState.ENABLED,
                template_id=template_id,
                template_version=1,
                priority=ReplyPriority(priority),
                row_version=1,
                created_at=NOW,
                updated_at=NOW,
            )
        )
        rule_repository.add_condition(
            condition_id=condition_id,
            condition=ReplyCondition(
                rule_id=rule_id,
                rule_version=1,
                field_name="content_text",
                operator="contains",
                expected_value="购买A款",
                normalization_flags=(NormalizationFlag.TRIM, NormalizationFlag.NFKC),
            ),
        )
        session.commit()


def prepare(resources: DatabaseResources, *, content: str = "你好，想购买A款") -> ReplySource:
    return seed_message(resources, content)


def count_audit(resources: DatabaseResources) -> int:
    with resources.session_factory() as session:
        return ReplyAuditRepository(session).count_audit_events()


def test_service_creates_unique_reply_decision_and_audit(resources: DatabaseResources) -> None:
    source = prepare(resources)
    seed_rule(resources, profile_id=source.profile_id)
    decision = ReplyService(resources.session_factory).decide(source)
    assert decision.decision_type == ReplyDecisionType.REPLY
    assert decision.rule_id == RULE_ID
    assert decision.rule_version == 1
    assert decision.rendered_text is not None
    assert decision.rendered_text.text == "固定回复 reply-service-account"
    assert count_audit(resources) == 1


def test_service_non_reply_flow_does_not_load_template(resources: DatabaseResources) -> None:
    source = prepare(resources, content="其他问题")
    decision = ReplyService(resources.session_factory).decide(source)
    assert decision.decision_type == ReplyDecisionType.NO_MATCH
    assert decision.rendered_text is None
    assert count_audit(resources) == 1


def test_service_missing_or_disabled_template_is_invalid_input(
    resources: DatabaseResources,
) -> None:
    source = prepare(resources)
    seed_rule(resources, profile_id=source.profile_id, template_state=ReplyLifecycleState.DISABLED)
    decision = ReplyService(resources.session_factory).decide(source)
    assert decision.decision_type == ReplyDecisionType.INVALID_INPUT
    assert decision.reason_code == ReplyReasonCode.MISSING_TEMPLATE


def test_service_render_failure_does_not_fallback_to_another_rule(
    resources: DatabaseResources,
) -> None:
    source = prepare(resources)
    seed_rule(
        resources,
        profile_id=source.profile_id,
        script="固定回复 {forbidden}",
        allowlist=("account_reference",),
    )
    seed_rule(
        resources,
        profile_id=source.profile_id,
        template_id=TEMPLATE_ID_2,
        rule_id=RULE_ID_2,
        script="备用 {account_reference}",
        priority=5,
        condition_id="00000000-0000-4000-8000-000000000497",
    )
    decision = ReplyService(resources.session_factory).decide(source)
    assert decision.decision_type == ReplyDecisionType.INVALID_INPUT
    assert decision.reason_code == ReplyReasonCode.FORBIDDEN_PLACEHOLDER
    assert decision.rule_id == RULE_ID
    assert count_audit(resources) == 1


def test_service_incomplete_identifier_returns_no_invalid_audit(
    resources: DatabaseResources,
) -> None:
    invalid_source = ReplySource(
        profile_id="not-a-uuid",
        account_reference=ACCOUNT_REFERENCE,
        conversation_id="missing",
        message_id="missing",
        message_content="你好",
    )
    decision = ReplyService(resources.session_factory).decide(invalid_source)
    assert decision.decision_type == ReplyDecisionType.INVALID_INPUT
    assert decision.reason_code == ReplyReasonCode.MISSING_REQUIRED_INPUT
    assert count_audit(resources) == 0


def test_service_rolls_back_on_repository_failure(
    resources: DatabaseResources,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = prepare(resources)

    def fail_repository(*args: object, **kwargs: object) -> object:
        raise SQLAlchemyError("synthetic repository failure")

    monkeypatch.setattr(ReplyRuleRepository, "list_enabled_snapshots", fail_repository)
    with pytest.raises(ReplyPersistenceError):
        ReplyService(resources.session_factory).decide(source)
    assert count_audit(resources) == 0


def test_service_rolls_back_on_audit_failure(
    resources: DatabaseResources,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = prepare(resources)
    seed_rule(resources, profile_id=source.profile_id)

    def fail_audit(*args: object, **kwargs: object) -> object:
        raise SQLAlchemyError("synthetic audit failure")

    monkeypatch.setattr(ReplyAuditRepository, "add_audit_event", fail_audit)
    with pytest.raises(ReplyPersistenceError):
        ReplyService(resources.session_factory).decide(source)
    assert count_audit(resources) == 0


def test_identifier_factory_and_commit_are_owned_by_service(resources: DatabaseResources) -> None:
    source = prepare(resources)
    seed_rule(resources, profile_id=source.profile_id)
    fixed_id = UUID("00000000-0000-4000-8000-000000000498")
    ReplyService(resources.session_factory, identifier_factory=lambda: fixed_id).decide(source)
    with resources.session_factory() as session:
        rows = (
            session.execute(text("SELECT audit_event_id FROM xianyu_reply_audit_events"))
            .scalars()
            .all()
        )
    assert rows == [str(fixed_id)]
