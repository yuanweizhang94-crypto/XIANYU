from __future__ import annotations

import builtins
import os
import socket
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

import pytest

from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishEvaluationContext,
    PublishRequest,
    PublishRiskState,
)
from xianyu_system.worker.publish.fingerprint import compute_publish_fingerprint

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"


def draft(**overrides: Any) -> ListingDraft:
    values: dict[str, Any] = {
        "draft_id": DRAFT_ID,
        "revision": 1,
        "title": "synthetic title",
        "description": "synthetic description",
        "category_reference": "synthetic-category",
        "price": Decimal("12.340"),
        "stock": 1,
        "location_reference": "synthetic-location",
        "media_metadata": {"b": [Decimal("2.0"), True], "a": "first"},
        "seller_profile_reference": "synthetic-profile",
        "lifecycle_state": ListingDraftLifecycle.VALIDATED,
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(overrides)
    return ListingDraft(**values)


def request(**overrides: Any) -> PublishRequest:
    values: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "draft_id": DRAFT_ID,
        "draft_revision": 1,
        "idempotency_key": "idem-key",
        "requested_at": NOW,
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "correlation_id": "corr-id",
    }
    values.update(overrides)
    return PublishRequest(**values)


def context(**overrides: Any) -> PublishEvaluationContext:
    values: dict[str, Any] = {
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "request_time": NOW,
        "local_profile_reference": "synthetic-profile",
    }
    values.update(overrides)
    return PublishEvaluationContext(**values)


def fingerprint(
    draft_overrides: dict[str, Any] | None = None,
    request_overrides: dict[str, Any] | None = None,
    context_overrides: dict[str, Any] | None = None,
) -> str:
    return compute_publish_fingerprint(
        draft(**(draft_overrides or {})),
        request(**(request_overrides or {})),
        context(**(context_overrides or {})),
    )


def test_same_semantic_input_and_mapping_order_produce_same_sha256() -> None:
    first = fingerprint()
    second = fingerprint(
        {"media_metadata": {"a": "first", "b": [Decimal("2.00"), True]}, "price": "12.34"}
    )

    assert first == second
    assert len(first) == 64
    assert first == first.lower()
    assert set(first) <= set("0123456789abcdef")


@pytest.mark.parametrize(
    "request_override",
    [
        {"request_id": "00000000-0000-4000-8000-000000000202"},
        {"idempotency_key": "another-key"},
        {"requested_at": datetime(2026, 1, 2, tzinfo=UTC)},
        {"correlation_id": "another-correlation"},
    ],
)
def test_operational_request_fields_do_not_change_fingerprint(
    request_override: dict[str, Any]
) -> None:
    assert fingerprint() == fingerprint(request_overrides=request_override)


@pytest.mark.parametrize(
    "draft_override",
    [
        {"created_at": datetime(2026, 1, 2, tzinfo=UTC)},
        {"updated_at": datetime(2026, 1, 2, tzinfo=UTC)},
    ],
)
def test_draft_timestamps_do_not_change_fingerprint(draft_override: dict[str, Any]) -> None:
    assert fingerprint() == fingerprint(draft_overrides=draft_override)


@pytest.mark.parametrize(
    "draft_override",
    [
        {"title": "changed title"},
        {"description": "changed description"},
        {"category_reference": "changed-category"},
        {"price": Decimal("13.34")},
        {"stock": 2},
        {"location_reference": "changed-location"},
        {"media_metadata": {"a": "changed"}},
        {"seller_profile_reference": "changed-profile"},
    ],
)
def test_approved_draft_semantics_change_fingerprint(draft_override: dict[str, Any]) -> None:
    assert fingerprint() != fingerprint(draft_overrides=draft_override)


@pytest.mark.parametrize(
    "request_override",
    [
        {"draft_revision": 2},
        {"authorization_state": PublishAuthorizationState.DENIED},
        {"risk_state": PublishRiskState.BLOCKED},
        {"synthetic_fixture": False},
    ],
)
def test_approved_request_semantics_change_fingerprint(
    request_override: dict[str, Any]
) -> None:
    context_override: dict[str, Any] = {}
    if "authorization_state" in request_override:
        context_override["authorization_state"] = request_override["authorization_state"]
    if "risk_state" in request_override:
        context_override["risk_state"] = request_override["risk_state"]
    if "synthetic_fixture" in request_override:
        context_override["synthetic_fixture"] = request_override["synthetic_fixture"]
    assert fingerprint() != fingerprint(request_overrides=request_override, context_overrides=context_override)


def test_context_profile_semantics_change_fingerprint() -> None:
    assert fingerprint() != fingerprint(context_overrides={"local_profile_reference": "other-profile"})


def test_equivalent_utc_timestamp_inputs_remain_normalized_before_fingerprinting() -> None:
    same_in_china = datetime(2026, 1, 1, 20, 0, tzinfo=timezone(timedelta(hours=8)))
    assert fingerprint(draft_overrides={"created_at": same_in_china}) == fingerprint()
    assert fingerprint(request_overrides={"requested_at": same_in_china}) == fingerprint()
    assert fingerprint(context_overrides={"request_time": same_in_china}) == fingerprint()


def test_fingerprint_has_no_environment_file_network_or_user_code_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_getenv(name: str, default: str | None = None) -> str | None:
        raise AssertionError(f"environment access attempted: {name}")

    def fail_open(*args: object, **kwargs: object) -> object:
        raise AssertionError("file access attempted")

    def fail_connect(self: socket.socket, address: object) -> None:
        raise AssertionError(f"network access attempted: {address!r}")

    class UserObject:
        called = False

        def __call__(self) -> None:
            self.called = True

    user_object = UserObject()
    monkeypatch.setattr(os, "getenv", fail_getenv)
    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(socket.socket, "connect", fail_connect)

    assert fingerprint() == fingerprint()
    assert user_object.called is False
