# 2026-08-19 商品平台状态与异常标题修复

## Execution contract

- User outcome: 商品管理页不得把平台真实非在售商品显示为“在售”；`【核心服务】` 异常测试标题不得继续作为正常商品出现；现有“检查平台状态”按钮必须恢复可用。
- Confirmed blocker 1: 生产 `ItemService._active_item_platform_metadata()` 对 `ItemInfoManager.get_item_list_info()` 返回项无条件写入 `platform_status=ACTIVE`，即使原始 `item_status=-9`。
- Confirmed blocker 2: `/api/v1/items/check-platform-status` 仍调用已被 upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` Publisher 架构替换时遗漏的 `probe_account_publish_restriction()`，运行时曾触发 ImportError。
- Confirmed blocker 3: 当前 batch `PublishExecutorService` 有 3 处 `await session.refresh(account)`，方法中不存在局部变量 `session`，导致账号能力检测后在平台请求前失败：`name 'session' is not defined`。
- Smallest success test: 不新增第二套状态系统、Publisher、浏览器、Token、Cookie 或 Session owner；复用 upstream 原始 `item_status`、现有 `detect_publish_account_capability()` 与现有 `self.session`。

## Upstream-first / reuse decision

- Current formal Publisher authority: upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- `ItemInfoManager` 已返回平台原始 `item_status`，无需第二个状态爬虫。
- 当前 upstream Publish service 已有 `detect_publish_account_capability()`，因此恢复状态检查时只加 read-only compatibility wrapper，不恢复旧 Browser preflight owner。
- Reuse decision: `PATCH_UPSTREAM` / `WRAP_FOR_OPERATIONS`，只修既有路径。

## Runtime repair

### Item platform-status mapping

`raw item_status == 0` 才允许写：

- `platform_status=ACTIVE`
- `platform_status_reason=seen_with_active_raw_item_status`

任意非空且非 0 的 raw status（例如 `-9`）写为非 ACTIVE：

- `platform_status=NOT_IN_ACTIVE_LIST`
- `platform_status_reason=raw_platform_item_status_not_active:<raw>`

缺少 raw status 时写 `UNKNOWN`，不猜测为 ACTIVE。

同一修复已加载到：

- `xianyu_chg0017_backend_web`
- `xianyu_chg0017_scheduler`

避免 Scheduler 后台同步把 Backend 已纠正的状态重新覆盖成 ACTIVE。

### Platform-status check compatibility

恢复 `probe_account_publish_restriction()` 的 read-only compatibility wrapper，内部复用当前 upstream `detect_publish_account_capability()`；不创建真实商品，不恢复旧 Browser publish preflight。

正式 `/api/v1/items/check-platform-status` 已从 ImportError 恢复到 HTTP 200 / `success=true`。

### Batch Publisher session refresh regression

`backend-web/app/services/publish_execution_service.py` 中 3 处错误：

```text
await session.refresh(account)
```

修为既有 service owner：

```text
await self.session.refresh(account)
```

一次真实安全恢复验证中，修复前任务在平台请求前失败，`PRODUCT_CREATED=false`；修复后 A 发布得到真实 ITEM_ID `1074563631284`、`AUTHORITATIVE_SYNC_CONFIRMED=true`。

## Abnormal title cleanup result

用户截图中的 `【核心服务】` 来自上一轮被放到 description 首行的测试文案，不是正式标题策略。

最终平台/本地处理：

- 欧阳 `2196106636`
  - `1074545795472`：已正式下架，随后本地异常测试记录删除。
  - `1074546343405`：已正式下架，随后本地异常测试记录删除。
  - `1077427864691`：已正式下架，随后本地异常测试记录删除。
  - 当前 `core_service_local_count=0`。
  - 当前确认 ACTIVE 的正式 CODEX：`1074563631284`，标题 `CODEX PLUS月卡｜自己账号｜1个月售后保障｜编程AI`，¥139，raw `item_status=0`。
  - 新 B `1074568339846` 虽 Publisher SUCCESS，但平台读回 raw `item_status=-9`，因此不算在售，也没有继续盲重试。
- 丸子 `2214313339860`
  - `1075397682483`：平台 raw `item_status=-9`，本地异常测试记录删除。
  - 当前 `core_service_local_count=0`。
  - 新版 ¥139 CODEX A/B/C 仍可见；历史旧价商品的下架请求返回 `FAIL_BIZ_IDLE_USER_UNAUTHORIZED`，未盲重试。该价格历史清理是独立业务状态问题，不再伪装成本轮“核心服务”标题修复已解决。

因此商品管理页刷新后不再存在本地 `【核心服务】` 商品行。

## Temporary experiment rollback

排查期间曾临时加入普通卖家 `editDetail/edit` 文本编辑实验入口。欧阳被 upstream 能力检测确认是鱼小铺账号，实验入口在提交前即安全拒绝，未修改任何商品。

该实验代码已完全从生产运行时撤回：

- OpenAPI `TEXT_ROUTE_PRESENT=false`
- `edit_personal_item_text` wrapper 不存在
- 个人卖家 publisher 已恢复原文件
- 实验代码不包含在持久化 patch 中

## Production verification

- Backend health: HTTP 200 after targeted restart.
- `RAW_STATUS_GATE_OK=true`.
- `SCHEDULER_RAW_STATUS_GATE_OK=true`.
- `PROBE_PRESENT=true`.
- `TEXT_WRAPPER_PRESENT=false`.
- `TEXT_ROUTE_PRESENT=false`.
- `SELF_SESSION_REFRESH_COUNT=3`.
- `UNDEFINED_SESSION_REFRESH_COUNT=0`.
- Both target accounts: `core_service_local_count=0`.

## Persistence artifact

- Patch: `vendor/patches/xianyu-auto-reply/742fb58-chg0018-item-platform-status-publish-session-followup.patch`
- Manifest: `vendor/patches/xianyu-auto-reply/742fb58-chg0018-item-platform-status-publish-session-followup.json`
- Canonical LF-normalized Patch SHA256: `2D27EAE393035220C9E8DD7578197F59FE88FD2A2D6C7451CDC6866BDEFE37BD`. Windows worktree checkout may materialize CRLF, so integrity validation normalizes CRLF to LF before hashing; committed Git blob and LF-normalized checkout bytes are identical.
- Clean apply: PASS against the exact captured pre-fix runtime source copies.
- Text-normalized source equivalence after apply: PASS for all 3 target files.

## Safety / side effects

- No Cookie/Token/Authorization/password/QR payload persisted in evidence or patch.
- No CAPTCHA/slider/identity bypass.
- UNKNOWN outcomes were not blindly retried.
- Abnormal-item platform actions were scoped to known test/replacement ITEM_IDs.
- Temporary editor experiment performed no platform mutation and was removed.

## Verification commands

- `pytest tests/unit/test_chg0018_item_platform_status_publish_session_followup.py -q` -> `5 passed`.
- Non-patch current-task files `git diff --check` -> PASS. The locked `.patch` artifact reports 5 trailing-whitespace lines because the captured runtime source preserves CRLF blank lines; per repository rules the locked patch is not rewritten merely to satisfy outer diff-check. Patch integrity is instead verified by canonical LF-normalized SHA256, clean-apply, and text-normalized source equivalence.
- Runtime Python compile for the four touched production modules -> PASS.
- `python scripts/verify_repository.py` in the original dirty checkout reached the repository security scan and stopped on pre-existing untracked temporary source copies under `tmp/auth-cookie-baseline/` and `tmp/publish_restore/context/`. Those directories were present before this task and were not modified or deleted by this repair.
- Full verification was then rerun in an isolated worktree based on the current remote feature branch. Result: `654 passed, 5 failed, 1 warning`. The 5 failures are unrelated worktree-portability failures: four pre-existing patch-hash tests hash CRLF-materialized worktree bytes instead of canonical committed/LF bytes, and `tests/unit/test_database.py::test_alembic_paths_are_repository_constants` expects the repository root to be exactly `D:/xianyu`, which is false in an isolated worktree. The current-task targeted regression remains `5/5 PASS`; no current-task assertion failed.
