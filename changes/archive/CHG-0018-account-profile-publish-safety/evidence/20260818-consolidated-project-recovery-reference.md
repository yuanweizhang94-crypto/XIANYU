# 2026-08-18 Consolidated Project Recovery Reference

This evidence pointer records that the full cross-subsystem recovery narrative for the current XIANYU production state has been consolidated into:

- `docs/PROJECT_PROGRESS_2026-08-18.md`
- `docs/PROJECT_PROGRESS_2026-08-18_INDEX.md`
- `docs/PROJECT_PROGRESS_LATEST.md`

The consolidated record covers the complete recovery chain discussed and proven during this operating cycle: Chat latest-upstream restoration, legacy PVR removal, QR upstream-native restoration, platform verification/cooldown evidence, Auto Reply token-storm protection, WebSocket init-reaper stability, stale publish-state cleanup, removal of the obsolete browser-readiness publish gate, restoration of latest-upstream direct/personal MTop publishing, strict publish status semantics, and the final real successful publish canary.

Current business state recorded by the consolidated reference:

```text
AUTO_REPLY_READY=true
PUBLISH_READY=true
CHAT_OPTIONAL=true
PRODUCTION_BUSINESS_READY=true
```

No secret values, raw Cookie/Token data, Authorization headers, passwords, QR payloads or real customer messages are stored in this evidence record.
