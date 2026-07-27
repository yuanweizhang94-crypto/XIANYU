from __future__ import annotations

from dataclasses import dataclass

import pytest

from xianyu_system.reply.domain import (
    ReplyAuthorizationState,
    ReplyMappingError,
    ReplyRiskState,
)
from xianyu_system.reply.mapper import ReplyMessageMapper

PROFILE_ID = "00000000-0000-4000-8000-000000000301"
CONVERSATION_ID = "00000000-0000-4000-8000-000000000302"
MESSAGE_ID = "00000000-0000-4000-8000-000000000303"


@dataclass
class SourceMessage:
    profile_id: str = PROFILE_ID
    account_reference: str = "acct"
    conversation_id: str = CONVERSATION_ID
    message_id: str = MESSAGE_ID
    message_content: str = "synthetic message"
    language_hint: str = "zh"
    is_synthetic: bool = True
    reply_authorization_state: ReplyAuthorizationState = (
        ReplyAuthorizationState.EXPLICITLY_AUTHORIZED
    )
    reply_risk_state: ReplyRiskState = ReplyRiskState.LOW
    reply_suppression_asserted: bool = False
    reply_sensitive_topic_asserted: bool = False
    reply_human_transfer_requested: bool = False
    correlation_identifier: str = "corr-1"


def test_mapper_projects_only_approved_fields_without_mutation() -> None:
    source = SourceMessage()
    before = source.__dict__.copy()
    context = ReplyMessageMapper().map_message(source)
    assert context.identifiers.profile_id == PROFILE_ID
    assert context.content_text == "synthetic message"
    assert context.language_hint == "zh"
    assert context.is_synthetic is True
    assert source.__dict__ == before


def test_mapper_preserves_synthetic_flag_and_local_states() -> None:
    context = ReplyMessageMapper().map_message(
        SourceMessage(is_synthetic=False, reply_risk_state=ReplyRiskState.BLOCKED)
    )
    assert context.is_synthetic is False
    assert context.risk_state == ReplyRiskState.BLOCKED


def test_mapper_fail_closed_for_missing_identifiers_and_unsupported_shape() -> None:
    with pytest.raises(ReplyMappingError):
        ReplyMessageMapper().map_message(object())
    with pytest.raises(ReplyMappingError):
        ReplyMessageMapper().map_message(SourceMessage(message_id="missing"))


def test_mapper_does_not_modify_message_boundary_semantics() -> None:
    source = SourceMessage(message_content="原始内容")
    context = ReplyMessageMapper().map_message(source)
    assert source.message_content == "原始内容"
    assert context.content_text == "原始内容"
