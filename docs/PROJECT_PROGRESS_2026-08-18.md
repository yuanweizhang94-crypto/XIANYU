# XIANYU 项目进展与故障恢复记录

时间基线：2026-08-18 00:06（Asia/Taipei / UTC+8）

本文作为 XIANYU 后续 AI / 开发 / 运维接手时的项目进度参考，记录本轮围绕 Chat、QR、Token、Auto Reply、WebSocket、商品发布所经历的问题、排查路径、已证实根因、修复方案、生产验证和当前正式运行规则。

> 安全边界：本文不记录 Cookie、Token、Authorization、密码、API Key、私钥、QR payload、真实客户消息或其他敏感凭据明文。

## 1. 当前最终生产结论

截至本记录：

- `AUTO_REPLY_ONLINE_COUNT=6`
- `AUTO_REPLY_ALL_ENABLED_ONLINE=true`
- `TOKEN_REFRESH_STORM_REGRESSION=false`
- `WEBSOCKET_PID1=docker-init`
- `WEBSOCKET_ZOMBIES=0`
- `PUBLISH_READY=true`
- `PRODUCTION_BUSINESS_READY=true`
- Chat 已恢复为 latest-upstream-native 架构，但部分账号仍可能被平台验证拦截；Chat 不再作为自动回复和商品发布的阻塞条件。

当前生产 Publish 已完成真实 Canary：

- `CANARY_ACCOUNT=2214313339860`
- `CANARY_OPERATION_ID=726f0127565f`
- `CANARY_BATCH_ID=6ce619b8-58b1-48fd-995a-44f2c5fd0684`
- `CANARY_PUBLISHER_TYPE=XianyuPersonalPublisher`
- `CANARY_ENTERED_LATEST_UPSTREAM_PUBLISHER=true`
- `CANARY_INITIAL_STATUS=SUBMITTED`
- `CANARY_FINAL_STATUS=SUCCESS`
- `CANARY_PLATFORM_ITEM_ID=1076024597942`
- `CANARY_AUTHORITATIVE_SYNC_CONFIRMED=true`
- `REAL_CANARY_SUCCESS=true`
- `REAL_PRODUCTS_PUBLISHED=1`

当前 XIANYU 已持久化修复 SHA：

- `XIANYU_SHA=4df4352ab0ee8dbf32c07e81acd75998e6b3b25d`
- 当前 Publish 对齐 upstream：`742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`
- COMPANY_LOCAL_EXECUTION_TOOL 对应状态修复 commit：`50c46238d9c06dab03c31c60164f2728e6a84202`

## 2. 本轮问题时间线

### 2.1 Chat / Token / PVR 问题最初表现

生产中 6 个 enabled 账号 Auto Reply 可以持续 ONLINE，但“在线聊天”页面多个账号显示“需平台验证”。早期 XIANYU 曾存在一套额外 Chat readiness / PVR 状态机，历史 PVR 元数据会在真正调用 upstream Chat 前直接短路，导致看起来像平台持续拒绝，但实际最新 upstream Chat 根本没有机会运行。

修复方向不是继续增强 PVR，而是回到 `UPSTREAM_FIRST`：让 latest upstream Chat 自己成为唯一权威。

### 2.2 恢复 latest upstream Chat

对 Chat 相关文件做窄范围 upstream diff，移除 XIANYU 额外的：

- 旧 Chat readiness state machine；
- 旧 PVR short-circuit；
- waiting-user Chat gate；
- Chat auth fingerprint；
- manual verification wrapper；
- 前端永久 PVR render gate。

保留与 Chat 无关、已经生产验证有效的：

- Auto Reply reconnect / Token storm 修复；
- WebSocket PID/zombie 修复；
- QR upstream-native 语义；
- disabled account isolation 等独立安全修复。

恢复后 Canary 真正进入 latest upstream Chat，证明旧 XIANYU PVR 不再挡路。

### 2.3 跨账号 fresh `FAIL_SYS_USER_VALIDATE`

在 `2214313339860` 和 `2217936413500` 上分别做严格单账号 Canary，两者都真实进入 latest upstream Chat 后返回：

`Local Token -> FAIL_SYS_USER_VALIDATE -> upstream bounded verification -> Baxia 300`

因此确认这不是第一个账号独有状态，也不是旧 XIANYU PVR 假状态，而是 fresh upstream-native 平台验证结果。

停止继续批量测试，避免跨账号集中 Token/CAPTCHA 活动放大平台风险。

### 2.4 冷却后 Chat 成功恢复一号 Canary

停止所有 Chat Connect / Local Token / CAPTCHA 活动约 10 小时 19 分钟后，仅处理 `2214313339860`：

1. upstream-native 官方 QR 成功；
2. authoritative Cookie 更新；
3. QR 本身不触发 Chat eager auth；
4. 单次 Chat lazy connect；
5. cache expired；
6. 一次 Local Token；
7. 首先 `FAIL_SYS_USER_VALIDATE`；
8. upstream bounded verification 第一次 Baxia 300；
9. 第二次 bounded attempt PASS；
10. Token SUCCESS；
11. Chat READY；
12. Conversation List SUCCESS；
13. Auto Reply 仍保持 6/6 ONLINE；
14. Remote Token = 0。

这证明：

- `FAIL_SYS_USER_VALIDATE` 不能直接映射为 `QR_REQUIRED`；
- upstream 自带 bounded verification 有真实恢复成功案例；
- Chat 和 Auto Reply 必须保持独立。

### 2.5 其他账号 fresh QR 后仍被平台拦截

后续对部分账号做 fresh QR：

- `2196106636`：QR SUCCESS、authoritative Cookie updated、Auto Reply ONLINE；Chat 仍 `FAIL_SYS_USER_VALIDATE -> BAXIA_300 x3`，NOT READY。
- `1034641456`：QR finalization 最终 SUCCESS、authoritative Cookie updated；单次 Chat lazy connect 仍 `FAIL_SYS_USER_VALIDATE -> BAXIA_300 x3`，NOT READY。
- `2219319284219` 曾出现二维码已扫但 QR session 未完成 finalization / 本地无法继续追踪的情况，说明“扫码动作”不等于“authoritative Cookie 已成功更新”。

另发现：如果“在线聊天”页面一直开着，扫码成功后前端页面可能自行触发 Chat connect。关闭在线聊天标签页后，确认：

- `POST_CLOSE_CHAT_CONNECTS=0`
- `POST_CLOSE_LOCAL_TOKEN_CALLS=0`
- `POST_CLOSE_CAPTCHA_CALLS=0`

因此后续扫码时应关闭 Chat 页面，等 QR 真正 finalization 后再按需做一次 Chat lazy connect。

### 2.6 Chat 当前正式业务决策

在线聊天不是当前核心业务阻塞项。正式业务优先级改为：

1. Auto Reply；
2. 商品发布；
3. Chat 作为可选能力单独维护。

不得为了 Chat 平台验证问题破坏已经健康的 Auto Reply 或 Publish。

## 3. Auto Reply / WebSocket 已解决问题

### 3.1 Token refresh storm

历史生产曾出现每账号数百次 Token 请求的 maintenance storm。根因是 live WebSocket 已经健康时，后台 maintenance 仍主动刷新 Token，并在失败后快速再次走完整认证。

最终规则：

- live WS maintenance 不主动刷新 Token；
- ordinary disconnect 只做 reconnect；
- Token single-flight；
- 不允许并行全认证；
- Chat PVR 不得清理健康 Auto Reply 正在使用的 token。

当前验证：

- `LIVE_WS_MAINTENANCE_TOKEN_REFRESH=0`
- `TOKEN_REFRESH_STORM_REGRESSION=false`
- `PARALLEL_TOKEN_REFRESH=0`
- `UNEXPECTED_FULL_AUTH_RETRY=0`

### 3.2 WebSocket PID/zombie 积压

历史 WebSocket 容器曾出现约 2 万 PIDs、数 GiB 内存占用，stop/start 后才能恢复。根因是容器 PID1 不能可靠回收 Chromium/crashpad 僵尸进程。

正式修复：WebSocket service 使用 init reaper。

当前硬性不变量：

- `PID1=docker-init`
- `zombies=0`

不得删除该 runtime/compose 配置。

## 4. QR 登录语义回归与修复

### 4.1 XIANYU 曾错误增强 QR success

上游 QR 原生语义是：

`QR SUCCESS -> upsert authoritative account/Cookie -> WebSocket start/restart -> return success`

XIANYU 一度额外加入：

`QR -> Chat invalidation -> Chat get_or_connect -> Local Token -> CAPTCHA -> Conversation List -> Publish preflight -> Round2 convergence`

这导致“刚扫码成功，马上又触发 Token/PVR/Baxia”。

### 4.2 最终规则

已删除 QR eager convergence，并形成永久不变量：

- `QR_EAGER_CHAT_AUTH=false`
- QR 只负责登录和 authoritative Cookie；
- downstream Chat / Publish 保持 lazy；
- 不允许恢复第二套 QR consumer convergence。

## 5. 商品发布：历史上怎么修好、后来为什么又坏

### 5.1 旧版 Publisher 架构

早期 upstream 正常发布链是：

`publish_single_item -> XianyuPublisher -> Playwright -> 注入 Cookie -> 打开 goofish 发布页 -> 填表 -> 点击发布`

因此当时 XIANYU 围绕 Browser / Persistent Profile 做修复是合理的，包括：

- canonical persistent profile；
- browser lock / global browser slot；
- 同一 concrete browser context 做 preflight + publish；
- 发布页等待时间；
- 登录页 / verification / page structure 状态分类；
- 禁止自动真实发布重试；
- emoji / React input 提交兼容。

历史上有真实发布成功证据：`actual_item_created=true`、`item_id_present=true`、`duplicate_item_created=false`。

### 5.2 Upstream 发布架构发生重大变化

2026-08-12 起 upstream 把正常发布从 Playwright 改为 Direct MTop Publisher。之后又继续加入普通卖家能力分流。

到 upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`，正式架构已经是：

`execute_single_publish`
`-> detect_publish_account_capability`
`-> fish shop: XianyuDirectPublisher`
`-> personal seller: XianyuPersonalPublisher`
`-> mtop.idle.pc.idleitem.publish`
`-> item_id/item_url`
`-> Publish Log`
`-> authoritative item sync`

正常 Direct Publish 不再依赖 Playwright。

### 5.3 XIANYU 当时为什么“发布失败”

XIANYU 仍保留旧 Browser 时代的 `REAL_BROWSER_LOGIN_READY` 前置门禁。

因此 Canary 出现：

`REAL_BROWSER_LOGIN_READY=false -> FAILED -> 未进入 Publisher`

这并不能证明 upstream Publisher 失败，因为真正 Publisher 根本没有运行。

这是本轮最终确认的关键架构回归：

> 上游已经换成 Direct API 发布，但 XIANYU 仍拿旧 Playwright/Browser 的前置条件阻挡新的 Publisher。

### 5.4 恢复 latest upstream Publish

最终执行：

- fetch latest upstream；
- 只审计 Publish surface；
- 找到并移除正常 single/batch publish 前的 stale browser gate；
- 采用 upstream latest publish dependency；
- shared files 仅保留独立且已有证据的 XIANYU 安全修复；
- 保持 selected account / owner scope / authoritative Cookie / no auto retry / serial batch / strict success semantics；
- 恢复账号 capability detection；
- fish shop -> `XianyuDirectPublisher`；
- personal seller -> `XianyuPersonalPublisher`。

当前明确：

- `NORMAL_SINGLE_PUBLISH_BROWSER_OWNER=false`
- `NORMAL_BATCH_PUBLISH_BROWSER_OWNER=false`
- `NORMAL_PUBLISH_REQUIRES_BROWSER=false`
- `REAL_BROWSER_LOGIN_READY_CHECKS_ON_NORMAL_PUBLISH=0`
- `PLAYWRIGHT_STARTS_ON_NORMAL_DIRECT_PUBLISH=0`
- `LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true`

### 5.5 真实 Publish Canary 成功

恢复后，真实 Canary：

`2214313339860`
`-> xianyu_publish_single`
`-> Backend`
`-> execute_single_publish`
`-> detect_publish_account_capability`
`-> XianyuPersonalPublisher`
`-> MTOP`
`-> SUBMITTED`
`-> SUCCESS`
`-> platform item id = 1076024597942`
`-> authoritative sync confirmed`

因此可以正式声明：

- `REAL_CANARY_SUCCESS=true`
- `PUBLISH_READY=true`
- `PRODUCTION_BUSINESS_READY=true`

## 6. Publish 状态语义修复

本轮还确认并修复了 `xianyu_publish_status` 的状态查询问题：

历史 operation 已经有 authoritative terminal `FAILED`，但如果 `batch_id` 不存在，旧逻辑可能只读返回 `UNKNOWN`。

最终优先级规则：

1. operation authoritative terminal state；
2. Publish Log authoritative terminal result；
3. platform item identity / authoritative catalog evidence；
4. batch/task current state；
5. active runtime；
6. 最后才 `UNKNOWN`。

硬性规则：

- `FAILED + no batch_id -> FAILED`
- `SUCCESS` 仍必须存在严格真实证据；
- HTTP 200 / “任务已提交”只能算 `SUBMITTED`；
- SUCCESS 至少要求 `platform_item_id`、`item_url` 或 `AUTHORITATIVE_SYNC_CONFIRMED=true`；
- UNKNOWN 不得触发自动重新发布。

## 7. 历史 stale publishing 清理

只读验收曾发现两条约 164 小时的历史 `publishing`：

- legacy log #106 / account `2804730247`
- legacy log #107 / account `2219319284219`

两者均无 operation_id / batch_id / platform_item_id / item_url，authoritative catalog exact match=0，且无活动 Publisher，最终安全收敛为 `FAILED`，没有重新发布。

结果：

- `STUCK_RUNNING_TASKS_AFTER=0`
- `UNKNOWN_STATUS_COUNT_AFTER=0`
- `ACTIVE_REAL_BATCH_EXECUTORS=0`

## 8. 当前正式架构与不可回退规则

### 8.1 Chat

- latest upstream Chat 是唯一权威；
- cache-first + lazy connect；
- `FAIL_SYS_USER_VALIDATE` 是平台验证，不是 QR_REQUIRED；
- ordinary disconnect -> reconnect；
- 只有 authoritative login/session failure 才允许 HUMAN_QR_REQUIRED；
- 不得恢复第二 Chat / Token / Session / PVR owner。

### 8.2 QR

- `QR SUCCESS -> upsert authoritative account/Cookie -> Auto Reply WS start/restart -> return success`
- `QR_EAGER_CHAT_AUTH=false`
- 不得自动 Chat / Token / CAPTCHA / Publish preflight。

### 8.3 Auto Reply

- live WS 不主动 Token refresh；
- Chat auth failure 不得破坏 Auto Reply；
- ordinary WS disconnect reconnect；
- WebSocket PID1 必须为 docker-init，zombies=0。

### 8.4 Publish

正式业务链：

`ChatGPT -> COMPANY_LOCAL_EXECUTION_TOOL -> xianyu_material_import -> xianyu_publish_single / batch -> XIANYU Backend -> latest upstream Publish -> platform`

永久不变量：

- `LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true`
- `NORMAL_DIRECT_PUBLISH_REQUIRES_BROWSER=false`
- `REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true`
- `OLD_BROWSER_PUBLISH_PATCH_IS_HISTORICAL_ONLY=true`
- `PUBLISH_ACCOUNT_CAPABILITY_ROUTING_PRESERVED=true`
- selected account 严格，不自动换账号；
- owner scope 严格；
- authoritative Cookie only；
- real publish 不自动 retry；
- `ACTIVE_REAL_BATCH_EXECUTORS_MAX=1`；
- strict success semantics；
- UNKNOWN 不允许引发自动 republish。

## 9. 当前业务可用性

正式业务状态：

```text
AUTO_REPLY_READY=true
PUBLISH_READY=true
CHAT_OPTIONAL=true
PRODUCTION_BUSINESS_READY=true
```

因此后续优先进入正常业务运营，不再因为部分 Chat 账号平台验证问题阻塞：

- 自动回复；
- 商品素材导入；
- 单商品发布；
- 串行批量发布；
- 发布状态追踪；
- 发布后 authoritative item sync。

## 10. 后续 AI / 开发接手顺序

后续任何 AI 在修改 XIANYU 前必须先：

1. 读取 `AGENTS.md`；
2. 读取 `docs/AI_PROJECT_HANDOFF.md`；
3. 读取本文；
4. fetch 当前 latest upstream；
5. 明确区分 repository HEAD 与实际 production runtime；
6. 先确认是否为 upstream 已经解决的问题；
7. 不得把旧架构约束重新加到 upstream 新架构前面。

最重要经验：

> 修复时不能只围绕“当前报错字段”继续打补丁，必须先确认 upstream 当前真实架构是否已经变化。Chat 的旧 PVR gate 和 Publish 的旧 REAL_BROWSER_LOGIN_READY gate 都属于同一类问题：XIANYU 曾经正确修过旧架构，但上游演进后，旧修复继续作为前置门禁，反而阻止了新的 upstream-native 路径。

后续的默认决策顺序保持：

`ADOPT_UPSTREAM -> CONFIGURE_UPSTREAM -> PATCH_UPSTREAM -> WRAP_FOR_OPERATIONS -> BUILD_LOCAL_EXCEPTION`
