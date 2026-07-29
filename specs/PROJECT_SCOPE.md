# Project Scope

## Final business goal

XIANYU is intended to support product templates, immediate or scheduled Xianyu listing, customer inquiry receipt, fixed-script replies, WeCom customer-service guidance, WeCom website-link sending, AI fallback for uncovered questions, and human transfer for sensitive issues.

## First-version scope

The first-version architecture direction includes modular-monolith Core, one worker per Xianyu account, one Chrome Profile per account, SQLite WAL, fixed rules first, and AI fallback.

`CHG-0001-project-baseline` only establishes governance and specification baseline; it does not implement first-version business capability.

## Do not build in this change

- Real Xianyu login.
- Xianyu WebSocket.
- Xianyu message sending.
- Playwright publishing.
- WeCom API.
- AI Provider.
- FastAPI routes.
- SQLite business tables.
- Browser installation.
- Real Xianyu account access.

## Security boundaries

- Do not bypass CAPTCHA, face verification, platform verification, or risk controls.
- Do not modify device fingerprints.
- Do not rotate proxy IPs to avoid detection.
- Do not commit Cookie, Token, Secret, or real customer data.
- Stop when risk or permissions are uncertain.

## Non-goals

Redis, Celery, MySQL, PostgreSQL, React, n8n, OpenClaw runtime, vector databases, LangChain complex agents, Kubernetes, and multi-tenancy are not part of the first phase.

## Capability phase order

1. CHG-0001: repository governance baseline.
2. CHG-0002: Core application skeleton.
3. Later approved changes: database, account, message, reply, publish, schedule, WeCom, AI, and health-monitor capabilities.


## Current CHG-0007 review state

CHG-0007 is in VERIFYING for final PR review preparation. CAP-XY-SCHEDULE is verified only for the local deterministic one-time Schedule boundary and synthetic fixtures. It does not provide real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedules, or external queue behavior. PR #8 remains Draft until final administration and Ready transition gates pass.

After CHG-0007 is merged and archived, the next separately authorized project-owner decision should prioritize a supervised real Xianyu integration feasibility spike before adding more WeCom or AI abstractions. That future spike should start with low-risk, single-account, human-supervised, fail-closed checks for login state and page reachability, without committing Credential material or using real customer data. This roadmap note does not create or authorize CHG-0008.


## CHG-0007 final PR administration

CHG-0007 final PR administration is complete. CAP-XY-SCHEDULE remains verified only for local deterministic one-time Schedule behavior with synthetic fixtures. PR #8 remains Draft until the final administration commit passes CI and the Ready transition is performed. Merge, archive, branch deletion, CHG-0008 creation, real Xianyu access, real scheduled publishing, browser automation, Credential handling, WeCom, AI, Redis, Celery, recurring schedules, and external queue behavior remain unauthorized until their separate gates or future approvals.


## CHG-0007 archived Schedule boundary

CHG-0007 is complete and archived after PR #8 merged through normal two-parent merge commit `4da2dbea8da9ec80819d04906e987e5856653ae9`. CAP-XY-SCHEDULE is verified only for local deterministic one-time Schedule behavior with synthetic fixtures. The repository has local Account, Message, Reply, Publish, and Schedule boundaries, but they remain deterministic local logic and cannot operate the real Xianyu platform. The next separately authorized project-owner decision should prioritize a supervised real Xianyu integration feasibility spike before WeCom and AI. That future spike should be low-risk, single-account, human-supervised, fail-closed, and should stop at CAPTCHA, face verification, platform verification, or risk controls. This roadmap note does not create or authorize CHG-0008.


## CHG-0008 upstream integration foundation draft

CHG-0008 is created as a governance and clean-room adapter foundation change. It may document product roadmap, anti-drift rules, pinned upstream audit facts, integration maturity, and an offline synthetic Xianyu adapter contract. It does not authorize real Xianyu login, real network access, browser automation, Credential handling, upstream code import, WeCom, AI, dependency changes, workflow changes, or CHG-0009.

## CHG-0008 upstream pilot anti-drift rules

- Before adding a new Xianyu capability, check existing Account, Message, Reply, Publish, and Schedule boundaries and reuse their facts instead of reimplementing them.
- Do not create large adapter abstractions, fake sessions, mapping DTOs, or new runtimes only because they may be useful later.
- Pin upstream repositories to exact commits before audit or execution; never silently follow floating main or master.
- Do not copy upstream source code, deployment scripts, protocol constants, signing logic, decryption logic, or Cookie examples into this repository.
- Local verified capability means deterministic local evidence only; it does not mean live Xianyu operation works.
- Stop on CAPTCHA, slider, face verification, device verification, risk-control prompts, unknown outcomes, or uncertain permissions.
- CHG-0008 is an upstream pilot governance and evidence change. It must not create CHG-0009 or `app/xianyu_system/adapters/xianyu/` without later pilot evidence proving a specific interface is needed.

## CHG-0008 archived upstream integration foundation

CHG-0008 is archived after PR #9 merged through normal two-parent merge commit `e7a9205dfeafd8b5e0f617f1855ecc4a33d6441c`. The upstream Pilot produced supervised P0-P6 evidence and the decision `WRAP`. The next separately authorized step may create CHG-0009 for a minimal localhost-only upstream wrapper. CHG-0008 itself does not make live Xianyu operation generally available in the main repository.

## CHG-0009 upstream wrapper MVP

CHG-0009 is authorized to implement a minimal localhost-only wrapper around the independently running upstream Pilot. Scope is limited to health, account status, listener control, recent inbound message observation, and one manually confirmed test reply. It does not authorize product publishing, delisting, orders, refunds, ratings, scheduler, crawler, promotion, updater, AI automatic replies, automatic delivery, public services, or copying upstream source code.
