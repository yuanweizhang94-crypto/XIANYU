# XIANYU 2026-08-18 项目进度索引

当前完整项目恢复记录：

- `docs/PROJECT_PROGRESS_2026-08-18.md`

当前正式业务状态：

```text
AUTO_REPLY_READY=true
PUBLISH_READY=true
CHAT_OPTIONAL=true
PRODUCTION_BUSINESS_READY=true
```

当前关键代码/文档基线：

- XIANYU Publish 恢复提交：`4df4352ab0ee8dbf32c07e81acd75998e6b3b25d`
- 当前采用的 upstream Publish 基线：`742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`
- COMPANY_LOCAL_EXECUTION_TOOL 发布状态语义修复：`50c46238d9c06dab03c31c60164f2728e6a84202`
- 完整进度记录首次持久化 commit：`b2deac2f639d9d53c34aec849365acf7bdfbdb92`

后续接手顺序：

1. `AGENTS.md`
2. `docs/AI_PROJECT_HANDOFF.md`
3. `docs/PROJECT_PROGRESS_2026-08-18.md`
4. fetch 当前 upstream main
5. 核对 production runtime SHA，不得仅按 repository HEAD 推断部署状态

永久禁止回归：

- QR eager Chat auth
- 旧 XIANYU PVR short-circuit
- live Auto Reply Token refresh storm
- WebSocket 无 init reaper 导致 zombie/PID 堆积
- 正常 Direct Publish 前置 `REAL_BROWSER_LOGIN_READY`
- 正常 Direct Publish 强制 Playwright / Persistent Profile
- HTTP 200/任务已提交直接标记 SUCCESS
- UNKNOWN 自动触发重复发布
