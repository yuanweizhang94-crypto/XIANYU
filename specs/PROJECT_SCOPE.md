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
