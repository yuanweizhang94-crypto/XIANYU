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
