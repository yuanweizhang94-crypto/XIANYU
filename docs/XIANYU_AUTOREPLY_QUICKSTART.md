# XIANYU automatic reply quickstart

CHG-0010 adds deterministic automatic reply commands. It does not add an interactive operator workflow.

## Commands

```powershell
python -m xianyu_system autoreply doctor
python -m xianyu_system autoreply start
python -m xianyu_system autoreply status
python -m xianyu_system autoreply stop
python -m xianyu_system autoreply run --once
```

## Configuration

Copy `config/autoreply.example.yaml` to `.local/autoreply.yaml` and edit only local values. `.local` is ignored by Git.

Default committed configuration is disabled. Live sends require both:

- `.local/xianyu-upstream.env` with `XIANYU_ALLOW_LIVE_WRITES=true`.
- `.local/autoreply.yaml` with `enabled: true` and `mode: dedicated-test`.

## Safety

The worker replies only to inbound text messages for allowlisted accounts. It creates a startup watermark so historical messages are not replied, blocks duplicate sends after SUCCESS or UNKNOWN, applies cooldown/rate limits, and records only non-sensitive local state.

Logs and state must not contain full message text, full reply text, Authorization, Cookie, Token, Session, passwords, full account identifiers, contact information, or upstream payloads.
