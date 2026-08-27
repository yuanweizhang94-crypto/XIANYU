# XIANYU × COMPANY_LOCAL_EXECUTION_TOOL
# AI 无缝接手、开发、修复与正常使用长期权威手册

**Authority date: 2026-08-18 00:06（Asia/Taipei / UTC+8）**  
**适用对象：ChatGPT、Codex、其他 AI 开发代理、公司同事、维护人员**  
**用途：正常业务执行、故障判断、Upstream 同步、生产修复、GitHub 维护、Runtime 核验**

> **跨版本接管前置要求**：任何新对话、模型、Agent 或升级后恢复，必须先读取并执行 ZIDONGZHUA 当前 main 的 `docs/UNIVERSAL_AI_HANDOFF_PROTOCOL.md`。该协议要求完整刷新 ZIDONGZHUA + COMPANY_LOCAL_EXECUTION_TOOL + XIANYU，以及当前 Runtime / upstream / 业务真值；只有九域覆盖矩阵达到 `FULL_PROJECT_CONTEXT_READY=true` 后，才允许使用本文件的当前 XIANYU 快照继续执行。
>
> Canonical protocol: `https://github.com/yuanweizhang94-crypto/zidongzhua/blob/main/docs/UNIVERSAL_AI_HANDOFF_PROTOCOL.md`
>
> 本文件是当前 Living Handoff。完整的本轮故障时间线、历史错误路径、根因、修复和真实生产证据见：
>
> - `docs/PROJECT_PROGRESS_2026-08-18.md`
> - `docs/PROJECT_PROGRESS_CURRENT.md`
> - `changes/archive/CHG-0018-account-profile-publish-safety/evidence/20260818-consolidated-project-recovery-reference.md`
>
> **Governance closure (2026-08-27):** current `main` has no executable active Change. CHG-0017 and CHG-0018 are archived historical lines whose old unfinished task markers were superseded by later CHG-0022 through CHG-0034 work. Do not resume old T11/T12/T17; only a newly approved active Change may become executable.

严禁在文档、日志或回复中保存/输出 Cookie、Token、Authorization、密码、API Key、私钥、QR payload、真实客户消息或其他敏感凭据明文。

---

# 0. 当前最终业务状态

```text
AUTO_REPLY_READY=true
AUTO_REPLY_ONLINE_COUNT=6
AUTO_REPLY_ALL_ENABLED_ONLINE=true

PUBLISH_READY=true
PRODUCTION_BUSINESS_READY=true

CHAT_OPTIONAL=true
```

当前正常业务已经可以正式使用：

1. 自动回复；
2. Material 导入；
3. 单商品发布；
4. 串行批量发布；
5. Publish 状态追踪；
6. 发布后 authoritative item sync。

Chat 已恢复为 latest-upstream-native 语义，但部分账号仍可能被平台验证拦截。Chat 不得再阻塞 Auto Reply 或 Publish。

---

# 1. 当前关键基线

## XIANYU

生产 Publish 恢复代码基线：

`4df4352ab0ee8dbf32c07e81acd75998e6b3b25d`

该版本已完成真实生产 Publish Canary 并成功创建真实商品。

## Upstream

XIANYU upstream：

`https://github.com/zhinianboke/xianyu-auto-reply`

本轮 Publish 恢复时实际 fetch 的 upstream：

`742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`

提交标题：

`完善商品发布`

Chat 恢复阶段曾以：

`bf252be357f5e4261b04ce2b7419c5574aaf1b55`

作为当时 latest upstream Chat authority。

任何未来任务开始时都必须重新 fetch；不得假定以上 SHA 仍是当前最新 upstream。

## COMPANY_LOCAL_EXECUTION_TOOL

用户显示名称：

`笔记本本地执行工具`

仓库：

`https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL`

本轮 Publish status 语义修复持久化 commit：

`50c46238d9c06dab03c31c60164f2728e6a84202`

定位：ChatGPT ↔ Windows 执行桥 + XIANYU Thin Business Adapter。

它不是 XIANYU，不得重新实现 Publisher、Account、Cookie、Session、Profile、Material、Category、WebSocket、Scheduler。

---

# 2. 永久 Source of Truth 顺序

冲突时按以下顺序刷新并判断：

```text
CURRENT_GITHUB
-> CURRENT_LOCAL
-> CURRENT_RUNTIME
-> CURRENT_UPSTREAM
-> historical docs/chat
```

不得因为 GitHub HEAD 已推进，就直接声称 production runtime 已部署同一 SHA。

必须区分：

- repository documentation/test HEAD；
- production runtime code base；
- actual latest upstream SHA。

---

# 3. 永久 Upstream First 决策顺序

```text
ADOPT_UPSTREAM
-> CONFIGURE_UPSTREAM
-> PATCH_UPSTREAM
-> WRAP_FOR_OPERATIONS
-> BUILD_LOCAL_EXCEPTION
```

任何新增代码前必须先证明：

- upstream 当前没有现成能力；
- local 当前没有可复用能力；
- runtime 不是只是没加载已有实现；
- 不是配置、数据、Session、账号状态或平台官方限制；
- 修改现有最小函数仍不能解决。

证明不了：

`NEW_IMPLEMENTATION_ALLOWED=false`

---

# 4. 当前正式商品发布架构——已替换旧 Browser Publisher 结论

## 4.1 正常业务入口

正式路径：

```text
用户/ChatGPT
-> 笔记本本地执行工具
-> receive_attachment
-> xianyu_material_import
-> XIANYU Material
-> xianyu_publish_single / batch
-> XIANYU Backend
-> execute_single_publish
-> detect_publish_account_capability
-> XianyuDirectPublisher / XianyuPersonalPublisher
-> MTOP
-> platform item
-> Publish Log
-> authoritative item sync
```

## 4.2 当前 upstream Publisher ownership

鱼小铺：

`XianyuDirectPublisher`

普通卖家：

`XianyuPersonalPublisher`

正常 Direct Publish：

```text
NORMAL_SINGLE_PUBLISH_BROWSER_OWNER=false
NORMAL_BATCH_PUBLISH_BROWSER_OWNER=false
NORMAL_PUBLISH_REQUIRES_BROWSER=false
REAL_BROWSER_LOGIN_READY_CHECKS_ON_NORMAL_PUBLISH=0
PLAYWRIGHT_STARTS_ON_NORMAL_DIRECT_PUBLISH=0
LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true
```

## 4.3 永久禁止回归到旧门禁

旧 CHG-0017/CHG-0018 的 Browser / Persistent Profile / Playwright Publisher 修复属于**旧 upstream 架构的历史正确修复**。

上游后来已把正常发布改为 Direct MTop Publisher。

因此永久规则：

```text
REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true
OLD_BROWSER_PUBLISH_PATCH_IS_HISTORICAL_ONLY=true
PUBLISH_ACCOUNT_CAPABILITY_ROUTING_PRESERVED=true
```

禁止再把以下条件加回正常 Direct Publish 前面：

- `REAL_BROWSER_LOGIN_READY`
- Persistent Profile ready
- Playwright browser session ready
- publish page preflight
- publish form rendered

canonical Profile / Playwright 系统本身可以继续服务其他真正需要它的 upstream 功能，但不得重新成为正常 Direct Publish 的强制前置条件。

---

# 5. Publish 真实生产验证

最终真实 Canary：

```text
CANARY_ACCOUNT=2214313339860
CANARY_OPERATION_ID=726f0127565f
CANARY_BATCH_ID=6ce619b8-58b1-48fd-995a-44f2c5fd0684
CANARY_PUBLISHER_TYPE=XianyuPersonalPublisher
CANARY_ENTERED_LATEST_UPSTREAM_PUBLISHER=true
CANARY_INITIAL_STATUS=SUBMITTED
CANARY_FINAL_STATUS=SUCCESS
CANARY_PLATFORM_ITEM_ID=1076024597942
CANARY_AUTHORITATIVE_SYNC_CONFIRMED=true
REAL_CANARY_SUCCESS=true
REAL_PRODUCTS_PUBLISHED=1
```

因此：

```text
PUBLISH_READY=true
PRODUCTION_BUSINESS_READY=true
```

没有新直接 Runtime 证据，禁止重新宣称 Publisher 未验证或回退到旧 Browser 发布架构。

---

# 6. Publish 状态语义——永久规则

正式状态：

- `SUBMITTED`
- `RUNNING`
- `SUCCESS`
- `FAILED`
- `UNKNOWN`

Backend HTTP 200 / “任务已提交”只能是：

`SUBMITTED`

SUCCESS 必须至少存在：

- `platform_item_id`
- `item_url`
- `AUTHORITATIVE_SYNC_CONFIRMED=true`

永久规则：

```text
HTTP_200_IS_NOT_SUCCESS=true
UNKNOWN_NEVER_BLIND_RETRY=true
NO_AUTOMATIC_REAL_PUBLISH_RETRY=true
ACTIVE_REAL_BATCH_EXECUTORS_MAX=1
```

`xianyu_publish_status` authoritative 优先级：

1. operation authoritative terminal state；
2. Publish Log terminal result；
3. platform item / authoritative catalog evidence；
4. batch/task current state；
5. active runtime；
6. 最后才 UNKNOWN。

已修复：

`FAILED + no batch_id -> FAILED`

不能再因为 batch_id 缺失把 authoritative FAILED 错误降级为 UNKNOWN。

---

# 7. 账号选择与发布安全边界

永久保持：

```text
STRICT_SELECTED_ACCOUNT=true
OWNER_SCOPE_PRESERVED=true
AUTHORITATIVE_COOKIE_ONLY=true
NO_AUTOMATIC_REAL_PUBLISH_RETRY=true
ACTIVE_REAL_BATCH_EXECUTORS_MAX=1
```

发布失败时：

- 不自动换另一个账号；
- 不自动重发第二件；
- 不因为 UNKNOWN 盲重试；
- 不建立第二套 Publisher；
- 不绕开 Material / Backend / Business Adapter。

正常真实发布禁止使用临时业务旁路：

- run_program
- container_run
- 临时 Python/Node
- direct import `execute_single_publish`
- direct import Publisher
- 临时 Playwright

---

# 8. 历史 stale Publish 状态已收口

曾存在两条约 164 小时的 legacy `publishing`：

- legacy log #106 / account `2804730247`
- legacy log #107 / account `2219319284219`

均无 operation_id / batch_id / platform item identity，authoritative catalog exact match=0，且无活动 Publisher。

最终安全收敛：

```text
FINAL_STATUS=FAILED
REPUBLISHED=false
STUCK_RUNNING_TASKS_AFTER=0
UNKNOWN_STATUS_COUNT_AFTER=0
ACTIVE_REAL_BATCH_EXECUTORS=0
```

不得重新发布这两条历史记录。

---

# 9. Chat 当前正式架构

```text
CURRENT_CHAT_ARCHITECTURE=LATEST_UPSTREAM_NATIVE
CHAT_OPTIONAL=true
AUTO_REPLY_AND_CHAT_INDEPENDENT=true
REMOTE_TOKEN_REQUIRED=false
```

正式 Chat 路径：

```text
user actually opens/invokes Chat
-> cache-first
-> valid cache reuse
-> cache miss/expired: existing upstream get_or_connect
-> existing upstream Local Token owner if required
-> existing upstream bounded verification if required
-> IM connect/register
-> conversation list
```

永久禁止恢复：

- 第二套 Chat state machine；
- 第二套 Token owner；
- 第二套 PVR lifecycle；
- 旧 XIANYU PVR short-circuit；
- waiting-user Chat gate；
- QR -> eager Chat auth convergence；
- Round2 duplicate auth owner。

---

# 10. `FAIL_SYS_USER_VALIDATE` 正式语义

`FAIL_SYS_USER_VALIDATE` / `RGV587` 是 fresh platform verification / risk 结果。

它不是：

- `QR_REQUIRED`
- `HUMAN_QR_REQUIRED`
- 登录必然失效的证明

真实成功证据曾证明：

```text
FAIL_SYS_USER_VALIDATE
-> upstream bounded verification
-> first Baxia 300
-> later bounded attempt PASS
-> Token SUCCESS
-> Chat READY
```

因此不得直接把平台验证映射成扫码。

部分账号 fresh QR + authoritative Cookie 更新后，Chat 仍可能被 Baxia 拒绝。这属于 Chat/platform verification 范围，不得阻塞 Auto Reply / Publish。

---

# 11. QR 正式语义

唯一权威 QR success：

```text
QR SUCCESS
-> upsert authoritative account/Cookie
-> WebSocket Auto Reply start/restart
-> RETURN SUCCESS
```

永久：

`QR_EAGER_CHAT_AUTH=false`

禁止 QR success 后自动触发：

- Chat invalidation
- Chat get_or_connect
- Local Token
- CAPTCHA
- Conversation List
- Publish preflight
- Round2 convergence

“用户手机扫到二维码”不等于 QR finalization 已完成。

只有看到：

```text
QR_LOGIN_SUCCESS=true
AUTHORITATIVE_COOKIE_UPDATED=true
```

才说明该次 QR 已真正完成 authoritative 登录更新。

---

# 12. Auto Reply 已稳定——不要无证据重开

当前：

```text
AUTO_REPLY_ONLINE_COUNT=6
AUTO_REPLY_ALL_ENABLED_ONLINE=true
LIVE_WS_MAINTENANCE_TOKEN_REFRESH=0
TOKEN_REFRESH_STORM_REGRESSION=false
PARALLEL_TOKEN_REFRESH=0
UNEXPECTED_FULL_AUTH_RETRY=0
```

历史曾出现每账号数百次 Token maintenance 请求。

永久规则：

- live WebSocket 不做主动 Token refresh storm；
- ordinary disconnect -> reconnect；
- Chat auth failure 不得清理健康 Auto Reply 的 live token；
- 不做跨账号并行 full-auth。

---

# 13. WebSocket PID/zombie 修复——永久保留

历史 WebSocket 容器曾出现约 2 万 PID 和数 GiB 内存占用。

正式修复：init reaper。

永久生产不变量：

```text
WEBSOCKET_PID1=docker-init
WEBSOCKET_ZOMBIES=0
PID_LEAK_REGRESSION=false
```

禁止删除对应 compose/runtime init 配置。

---

# 14. Chat 与 Publish 的共同经验

本轮最重要的工程教训：

**旧架构上正确的本地修复，在 upstream 演进以后不能继续无条件作为新架构的前置门禁。**

两个已真实发生的例子：

1. Chat：旧 XIANYU PVR metadata 在 latest upstream Chat 前 short-circuit；
2. Publish：旧 `REAL_BROWSER_LOGIN_READY` 在 latest upstream Direct Publisher 前 short-circuit。

因此未来出现问题时，禁止只围绕当前错误字符串继续 Patch。

如果同一问题连续修复仍未解决，必须停止叠 Patch，执行：

```text
CURRENT_UPSTREAM
vs
CURRENT_LOCAL
vs
CURRENT_RUNTIME
```

精确对照。

---

# 15. BUSINESS_EXECUTION 默认模式

用户说：

- 发布商品
- 上传这些图
- 查发布状态
- 继续正常业务

默认：

`TASK_TYPE=BUSINESS_EXECUTION`

不要自动升级成：

- 全仓库审计；
- upstream 大同步；
- Docker 全栈重建；
- Chat 修复；
- Session 重构；
- 新 Publisher；
- 新 Scheduler。

只有正式业务调用返回新的系统级证据，才进入 Repair。

---

# 16. Runtime First

代码修复不等于生产修复。

对 image-baked source：

```text
modify source
-> tests
-> build necessary service only
-> replace necessary container only
-> health check
-> verify runtime source/hash
```

禁止 local 已修、runtime 仍旧时反复用真实商品试错。

---

# 17. 当前正常业务工具

COMPANY_LOCAL_EXECUTION_TOOL 正常 XIANYU 业务优先：

- `receive_attachment`
- `xianyu_material_import`
- `xianyu_publish_single`
- `xianyu_publish_status`
- `xianyu_account_status`

正式关系：

`用户 -> ChatGPT -> 笔记本本地执行工具 -> XIANYU -> 闲鱼官方正常业务路径`

本地执行工具是桥；XIANYU 是业务系统。

---

# 18. 永久禁止平行系统

无明确证明不得创建：

- 第二套 Publisher
- 第二套 Login
- 第二套 Session Renew
- 第二套 Profile Manager
- 第二套 Material Service
- 第二套 Category System
- 第二套 Chat State Machine
- 第二套 Token Owner
- 第二套 Business Adapter
- 第二套 Supervisor
- 第二套 Proxy
- 第二套 Attachment Pipeline

已有能力有 bug：

**最小修已有能力，不复制。**

---

# 19. 安全与平台边界

禁止：

- CAPTCHA / Slider / Face Verification 绕过；
- QR 绕过；
- Baxia bypass；
- fingerprint spoofing；
- 为规避平台验证而切换代理/IP/VPN；
- 强制错误分类；
- 跨账号 Cookie/Profile；
- secrets 输出；
- UNKNOWN 盲重试。

平台明确限制时 Fail Closed 是正常生产行为。

---

# 20. 后续 AI 接手必读顺序

1. `AGENTS.md`
2. `docs/AI_PROJECT_HANDOFF.md`
3. `docs/PROJECT_PROGRESS_2026-08-18.md`
4. `docs/PROJECT_PROGRESS_CURRENT.md`
5. 当前 GitHub HEAD / status
6. 当前 production runtime
7. fetch current upstream main

不得仅依赖旧对话摘要。

---

# 21. 当前永久不变量摘要

```text
UPSTREAM_FIRST=true
REUSE_FIRST=true
RUNTIME_FIRST=true
MINIMAL_PATCH_ONLY=true
NO_PARALLEL_IMPLEMENTATION=true
BUSINESS_EXECUTION_BY_DEFAULT=true

AUTO_REPLY_READY=true
PUBLISH_READY=true
CHAT_OPTIONAL=true

QR_EAGER_CHAT_AUTH=false
FAIL_SYS_USER_VALIDATE_IS_NOT_QR_REQUIRED=true
AUTO_REPLY_AND_CHAT_INDEPENDENT=true

LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true
NORMAL_DIRECT_PUBLISH_REQUIRES_BROWSER=false
REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true
PUBLISH_ACCOUNT_CAPABILITY_ROUTING_PRESERVED=true
STRICT_SELECTED_ACCOUNT=true
OWNER_SCOPE_PRESERVED=true
AUTHORITATIVE_COOKIE_ONLY=true
NO_AUTOMATIC_REAL_PUBLISH_RETRY=true
ACTIVE_REAL_BATCH_EXECUTORS_MAX=1
HTTP_200_IS_NOT_SUCCESS=true
UNKNOWN_NEVER_BLIND_RETRY=true

WEBSOCKET_PID1=docker-init
WEBSOCKET_ZOMBIES=0
```

完整故障经过和解决路径以 `docs/PROJECT_PROGRESS_2026-08-18.md` 为当前综合历史参考。

---

# 22. 三仓库实时同步与当前治理清理状态

根 `AGENTS.md` 已把 `XIANYU / COMPANY_LOCAL_EXECUTION_TOOL / ZIDONGZHUA` 的对应变动实时同步写为 P0 规则。每次实质执行完成前，必须更新受影响仓库、清理同主题过时/冲突说明、Commit + Push，并以远端 SHA 与本地目标 Commit 一致作为同步完成条件。

2026-08-18 本轮同时清理了一个明确冲突：旧文档/根规则中把 `REAL_BROWSER_LOGIN_READY` 写成正常发布统一门禁的表述，已改为“仅适用于真正需要 Browser/Page Session 的操作；正常 Direct/Personal Publish 使用最新 upstream account-capability routing → MTOP”。

当前仓库 `scripts/verify_repository.py` 仍有一个**本轮之前已存在**的治理失败：`CHG-0020-zidongzhua-market-search` 归档缺少 design/tasks 等要求文件与 upstream-first 字段。该失败已在纯净 `origin/main` worktree 独立复现，不能归因于本轮 P0 文档修改。禁止伪造历史设计/验收文件只为让验证变绿；后续应在有真实历史证据时单独完成 CHG-0020 治理清理。