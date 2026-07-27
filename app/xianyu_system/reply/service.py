"""Reply decision service and logical transaction coordination."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from xianyu_system.reply.domain import (
    ReplyAuditEvent,
    ReplyBoundaryError,
    ReplyDecision,
    ReplyDecisionType,
    ReplyEvaluationContext,
    ReplyMappingError,
    ReplyPersistenceError,
    ReplyReasonCode,
    ReplyRenderedText,
    ReplyRenderError,
    ReplySourceMessage,
    ReplyTemplateRenderInput,
)
from xianyu_system.reply.evaluator import DeterministicReplyEvaluator
from xianyu_system.reply.mapper import ReplyMessageMapper
from xianyu_system.reply.persistence import (
    ReplyAuditRepository,
    ReplyRuleRepository,
    ReplyTemplateRepository,
)
from xianyu_system.reply.renderer import FixedScriptTemplateRenderer


def utc_clock() -> datetime:
    return datetime.now(UTC)


class ReplyService:
    """Application service for deterministic local reply decisions only."""

    def __init__(
        self,
        session_factory: Callable[[], Session],
        *,
        mapper: ReplyMessageMapper | None = None,
        evaluator: DeterministicReplyEvaluator | None = None,
        renderer: FixedScriptTemplateRenderer | None = None,
        identifier_factory: Callable[[], UUID] = uuid.uuid4,
        clock: Callable[[], datetime] = utc_clock,
    ) -> None:
        self._session_factory = session_factory
        self._mapper = mapper or ReplyMessageMapper()
        self._evaluator = evaluator or DeterministicReplyEvaluator()
        self._renderer = renderer or FixedScriptTemplateRenderer()
        self._identifier_factory = identifier_factory
        self._clock = clock

    def decide(self, message: ReplySourceMessage) -> ReplyDecision:
        try:
            context = self._mapper.map_message(message)
        except ReplyMappingError:
            return ReplyDecision(
                decision_type=ReplyDecisionType.INVALID_INPUT,
                reason_code=ReplyReasonCode.MISSING_REQUIRED_INPUT,
            )
        session = self._session_factory()
        try:
            decision = self._decide_with_session(session, context)
            session.commit()
            return decision
        except (IntegrityError, SQLAlchemyError, ValueError):
            session.rollback()
            raise ReplyPersistenceError() from None
        except ReplyBoundaryError:
            session.rollback()
            raise
        finally:
            session.close()

    def count_audit_events(self) -> int:
        with self._session_factory() as session:
            return ReplyAuditRepository(session).count_audit_events()

    def _decide_with_session(
        self, session: Session, context: ReplyEvaluationContext
    ) -> ReplyDecision:
        rule_repository = ReplyRuleRepository(session)
        template_repository = ReplyTemplateRepository(session)
        audit_repository = ReplyAuditRepository(session)
        result = self._evaluator.evaluate(
            context,
            rule_repository.list_enabled_snapshots(
                profile_id=context.identifiers.profile_id,
                account_reference=context.identifiers.account_reference,
            ),
        )
        rendered_text: ReplyRenderedText | None = None
        decision_type = result.decision_type
        reason_code = result.reason_code
        if result.decision_type == ReplyDecisionType.REPLY:
            template = template_repository.get_template(
                template_id=result.template_id or "",
                template_version=result.template_version or 0,
                profile_id=context.identifiers.profile_id,
                account_reference=context.identifiers.account_reference,
            )
            if template is None or not template.is_enabled:
                decision_type = ReplyDecisionType.INVALID_INPUT
                reason_code = ReplyReasonCode.MISSING_TEMPLATE
            else:
                try:
                    rendered_text = self._renderer.render(
                        ReplyTemplateRenderInput(
                            template=template,
                            variables={
                                "account_reference": context.identifiers.account_reference,
                                "conversation_id": context.identifiers.conversation_id,
                            },
                        )
                    )
                except ReplyRenderError as exc:
                    decision_type = ReplyDecisionType.INVALID_INPUT
                    reason_code = exc.reason_code or ReplyReasonCode.FORBIDDEN_PLACEHOLDER
        decision = ReplyDecision(
            decision_type=decision_type,
            reason_code=reason_code,
            identifiers=context.identifiers,
            rule_id=result.rule_id,
            rule_version=result.rule_version,
            template_id=result.template_id,
            template_version=result.template_version,
            rendered_text=rendered_text,
        )
        audit_repository.add_audit_event(
            ReplyAuditEvent(
                audit_event_id=str(self._identifier_factory()),
                identifiers=context.identifiers,
                decision_type=decision.decision_type,
                reason_code=decision.reason_code,
                occurred_at=self._clock(),
                rule_id=decision.rule_id,
                rule_version=decision.rule_version,
                template_id=decision.template_id,
                template_version=decision.template_version,
                failure_category=(
                    None
                    if decision.decision_type == ReplyDecisionType.REPLY
                    else decision.reason_code.value
                ),
                correlation_identifier=context.correlation_identifier,
            )
        )
        return decision
