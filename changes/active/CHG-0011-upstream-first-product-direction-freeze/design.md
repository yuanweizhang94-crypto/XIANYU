Change ID: CHG-0011-upstream-first-product-direction-freeze
Status: VERIFYING
# Design

## Direction freeze

The architecture owner split is now explicit:

- `zhinianboke/xianyu-auto-reply` pinned deployment is the business app and execution engine for Xianyu account login, Cookies, WebSocket, online chat, keyword reply, default reply, product-specific reply, AI reply, context, intent, bargain handling, and message send execution.
- `D:/xianyu` is the control layer for safety, governance, operational wrappers, validation, release checks, secret scanning, backup/restore orchestration, and upgrade governance.

Future feature work must use the priority order documented in `docs/UPSTREAM_FIRST_POLICY.md`.

## Governance implementation

The validator enforces upstream-first fields on the single active change. It fails closed when required fields are missing, when a reuse decision is absent or invalid, when `BUILD_LOCAL_EXCEPTION` lacks an ADR reference, or when an upstream-adopt decision is combined with a local rewrite plan.

## Documentation implementation

- `docs/UPSTREAM_CAPABILITY_MATRIX.md` records pinned-upstream evidence and decisions.
- `docs/LOCAL_COMPONENT_DISPOSITION.md` records the final disposition of CHG-0009/CHG-0010 local overlap.
- `docs/UPSTREAM_FIRST_POLICY.md` records the decision hierarchy and exception criteria.
- `AGENTS.md`, `README.md`, `specs/PROJECT_SCOPE.md`, `specs/SYSTEM_ARCHITECTURE.md`, and `specs/PRODUCT_ROADMAP.yaml` carry the permanent product direction.

## Upstream capability audit

Pinned upstream `D:/xianyu-upstream-pilot` was audited at `bda1a859df63fa5f24e51398fa80a23490bb6dfc` by reading implementation files for account, keyword, default reply, AI, WebSocket, message filtering, reply logs, and frontend management pages. Evidence is summarized in `docs/UPSTREAM_CAPABILITY_MATRIX.md`.

## Pinned upstream evidence

- Upstream path: `D:/xianyu-upstream-pilot`
- Expected SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Actual SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Upstream tracked source modified by this change: no

## Existing local implementation search

`D:/xianyu` was searched for `autoreply`, `rule`, `keyword`, `fallback`, `watermark`, `cooldown`, `rate.limit`, `send_confirmed_reply`, `NormalizedInboundMessage`, `UpstreamClient`, and `listener` under `app`, `tests`, `docs`, and `changes`. Existing overlap is documented in `docs/LOCAL_COMPONENT_DISPOSITION.md`.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate implementation risk

High for automatic reply, keyword matching, AI reply, context, message receiving, and send execution because pinned upstream already contains the business application and execution engine. This change freezes duplicate local expansion and requires future changes to adopt, configure, patch, or operationally wrap upstream before considering local exceptions.

## Why upstream cannot satisfy the requirement

Not applicable for this governance change. The requirement is not to implement a business feature; it is to document upstream capabilities and enforce upstream-first governance. Future `BUILD_LOCAL_EXCEPTION` requests must prove upstream cannot satisfy their feature requirement.

## Approved exception ADR

Not applicable. No `BUILD_LOCAL_EXCEPTION` is requested by CHG-0011.

## Component owner

- Business application and execution engine: pinned `zhinianboke/xianyu-auto-reply` deployment.
- Safety, governance, operations, validation, and release control layer: `D:/xianyu`.

## Retirement plan for overlapping local code

CHG-0010 local autoreply worker is frozen and deprecated by policy. CHG-0015 is reserved for evaluating and retiring duplicate local autoreply worker behavior after upstream native fixed-template and AI reply validation passes.
