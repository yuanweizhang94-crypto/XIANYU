Change ID: CHG-0011-upstream-first-product-direction-freeze
Status: ARCHIVED
# Proposal

## Title

CHG-0011 upstream-first product direction freeze

## Owner approval

The project owner authorized a governance-only product direction freeze after CHG-0010. The explicit direction is upstream-first: pinned `zhinianboke/xianyu-auto-reply` is the business application and execution engine, while this repository owns safety, governance, operations, validation, and release control. The project owner also authorized stopping the current local autoreply worker before starting this change.

## Goal

Document the pinned upstream capability inventory, classify existing local overlap, lock the product roadmap to upstream-native validation phases, and mechanically prevent future changes from entering implementation without upstream audit and reuse decisions.

## Non-goals

- No new autoreply engine, keyword engine, AI reply engine, context store, multi-account scheduler, Web UI, business API, product operation, order operation, delivery operation, or refund operation.
- No platform messages, no test sends, no listener restart, no scheduler, no crawler, no promotion, no updater.
- No upstream checkout, pull, upgrade, source modification, source copy, image pull, or remote deployment script.
- No CHG-0012 creation.

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
