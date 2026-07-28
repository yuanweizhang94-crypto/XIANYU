"""Deterministic canonicalization and fingerprinting for local publish input."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from typing import Any, cast

from xianyu_system.worker.publish.domain import (
    JsonValue,
    ListingDraft,
    PublishAuthorizationState,
    PublishEvaluationContext,
    PublishRequest,
    PublishRiskState,
)


def _decimal_to_text(value: Decimal) -> str:
    normalized = value.normalize()
    if normalized == normalized.to_integral():
        return format(normalized.quantize(Decimal(1)), "f")
    return format(normalized, "f")


def _canonical_json_value(value: JsonValue) -> Any:
    if isinstance(value, Decimal):
        return {"decimal": _decimal_to_text(value)}
    if isinstance(value, tuple):
        if all(isinstance(item, tuple) and len(item) == 2 for item in value):
            mapped: dict[str, Any] = {}
            pairs = cast(tuple[tuple[str, JsonValue], ...], value)
            for pair in pairs:
                key, item = pair
                mapped[str(key)] = _canonical_json_value(item)
            return mapped
        return [_canonical_json_value(item) for item in value]
    return value


def _canonical_payload(
    draft: ListingDraft,
    request: PublishRequest,
    context: PublishEvaluationContext,
) -> dict[str, Any]:
    authorization_state = cast(PublishAuthorizationState, request.authorization_state)
    risk_state = cast(PublishRiskState, request.risk_state)
    return {
        "authorization_state": authorization_state.value,
        "category_reference": draft.category_reference,
        "description": draft.description,
        "draft_id": draft.draft_id,
        "draft_revision": request.draft_revision,
        "local_profile_reference": context.local_profile_reference,
        "location_reference": draft.location_reference,
        "media_metadata": _canonical_json_value(cast(JsonValue, draft.media_metadata)),
        "price": _decimal_to_text(cast(Decimal, draft.price)),
        "risk_state": risk_state.value,
        "seller_profile_reference": draft.seller_profile_reference,
        "stock": draft.stock,
        "synthetic_fixture": request.synthetic_fixture and context.synthetic_fixture,
        "title": draft.title,
    }


def compute_publish_fingerprint(
    draft: ListingDraft,
    request: PublishRequest,
    context: PublishEvaluationContext,
) -> str:
    """Return a stable SHA-256 fingerprint for approved local semantic input."""
    payload = _canonical_payload(draft, request, context)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
