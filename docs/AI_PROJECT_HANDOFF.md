# XIANYU AI Project Handoff

Authority date: 2026-08-19 15:26 (Asia/Taipei / UTC+8)

> 本文件只保存 XIANYU 当前技术真值、已解决边界和接管入口。旧故障时间线、旧 SHA、旧架构分析继续保留在 `changes/active/.../evidence/`、Git 历史和专项测试中，不再在 Living Handoff 里重复展开。
>
> 新对话先执行 ZIDONGZHUA 当前 main 的 `docs/UNIVERSAL_AI_HANDOFF_PROTOCOL.md`，再刷新 XIANYU GitHub / Local / Runtime / upstream。仓库 HEAD、生产 Runtime、upstream 必须分开判断。

## 1. 当前代码与 Runtime 权威

当前生产修复线：

```text
ACTIVE_BRANCH=feat/CHG-0018-account-profile-publish-safety
LAST_PRODUCTION_CODE_BASE_SHA=2c1f18fc57ff62a72d632348b39e074845aa39a7
CURRENT_BRANCH_HEAD_MUST_BE_REFETCHED=true
UPSTREAM_FIRST=true
CURRENT_RUNTIME_FIRST=true
NO_DUPLICATE_DEVELOPMENT=true
NO_CROSS_SUBSYSTEM_REGRESSION=true
```

`LAST_PRODUCTION_CODE_BASE_SHA` 只是最近完成 Runtime 验证的代码基线；后续 docs-only commit 会继续推进 branch HEAD，但不等于生产代码再次变化。不得因为 main/branch HEAD 与 Runtime SHA 不同就自动回退或重复修复。

## 2. 当前正式 Publisher 架构

```text
xianyu_publish_single
→ XIANYU Backend
→ execute_single_publish
→ detect_publish_account_capability
→ XianyuDirectPublisher / XianyuPersonalPublisher
→ MTOP
→ Publish Log
→ authoritative item sync
```

永久：

```text
NORMAL_PUBLISH_REQUIRES_BROWSER=false
REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true
PLAYWRIGHT_PROFILE_IS_NOT_NORMAL_PUBLISH_GATE=true
HTTP_200_IS_NOT_PUBLISH_SUCCESS=true
UNKNOWN_NEVER_BLIND_RETRY=true
```

SUCCESS 至少要求 `platform_item_id`、`item_url` 或 `AUTHORITATIVE_SYNC_CONFIRMED=true`。

## 3. 当前 Session / Cookie authority

2026-08-19 Session/Cookie authority closure 已完成并生产验证：

```text
SESSION_COOKIE_AUTHORITY_CLOSURE=PASS
UNKNOWN_COOKIE_WRITERS=0
MISSING_EXPECTED_BASELINE_CALLERS=0
STALE_COOKIE_OVERWRITE_BLOCKED=true
PER_ACCOUNT_RENEW_SINGLE_FLIGHT=true
EVIDENCE_QUALIFIED_QR_STICKY=true
```

正式规则：

```text
renew/login candidate
→ safe publisher-equivalent MTOP auth validation
→ valid only
→ stale/CAS protection
→ authoritative Cookie commit
```

未通过 safe MTOP auth 的 candidate 不得成为 authoritative Cookie。旧 renewal 不得覆盖更新的 QR 登录态。

只有同时满足：

```text
AUTHORITATIVE_AUTH_INVALID
+ OFFICIAL_RENEWAL_FAILED
+ SAFE_PUBLISHER_EQUIVALENT_MTOP_AUTH_FAILED
```

才允许判 `HUMAN_QR_REQUIRED`。

Browser/Profile stale、Chat not ready、BAXIA、`FAIL_SYS_USER_VALIDATE` 均不能单独触发 QR。

## 4. 当前账号 Session 真值

```text
2196106636=AUTH_VALID
2214313339860=AUTH_VALID
1034641456=HUMAN_QR_REQUIRED
2219319284219=HUMAN_QR_REQUIRED
2858469041=HUMAN_QR_REQUIRED+DISABLED
2217936413500=PLATFORM_PUBLISH_RESTRICTED
```

`2858469041` 扫码后必须单独只读确认 disabled 原因，禁止仅因 QR success 自动 enable。

## 5. Auto Reply / WebSocket / Chat 当前边界

```text
AUTO_REPLY_AND_CHAT_INDEPENDENT=true
CHAT_OPTIONAL=true
QR_EAGER_CHAT_AUTH=false
```

最新 Session closure 后生产回归：

```text
AUTO_REPLY=5/5 enabled connected
WEBSOCKET_ZOMBIES=0
ORDERS=PASS
CHAT_READ_PATH=PASS
ITEM_OFFICIAL_READ=PASS
SCHEDULER=HEALTHY
BACKEND=HEALTHY
```

永久禁止：

- Chat failure 清理健康 Auto Reply 登录态；
- QR success 自动触发 Chat/Token/CAPTCHA；
- live WebSocket Token refresh storm；
- 修 Session 时顺手重写 Publisher/Orders/Chat。

## 6. 商品平台状态权威

2026-08-19 已修复 `item_status=-9` 被误标 ACTIVE，以及 Scheduler 后台覆盖错误状态的问题。

正式唯一规则：

```text
FINAL_ACTIVE = platform item_status == 0
PUBLISHER_SUCCESS != PLATFORM_ACTIVE
ITEM_ID_RETURNED != PLATFORM_ACTIVE
SYNC_SUCCESS != PLATFORM_ACTIVE
```

`item_status=-9`、`NOT_IN_ACTIVE_LIST` 等非 0 状态不得进入真实 ACTIVE 商品映射和履约范围。

“检查平台状态”已改为复用当前 upstream `detect_publish_account_capability()`；不得恢复已删除的 `probe_account_publish_restriction`。

Publisher 中错误的 `session.refresh(account)` 回归已修正为 `self.session.refresh(account)`；无新 Runtime 反证不得重复立项。

## 7. 已解决事项：禁止无证据重开

以下已有生产/测试证据，默认 `RESOLVED`：

- 旧 Browser/Profile/Playwright Publisher gate。
- Chat/PVR 额外 short-circuit 与 QR eager convergence。
- Auto Reply Token refresh storm。
- WebSocket PID/zombie 积压。
- stale publish status / HTTP200-success / UNKNOWN blind retry 语义。
- Session renewal candidate 未验证即写 authoritative Cookie。
- stale renewal 覆盖新 QR Cookie。
- 多条 Cookie writer 绕过统一 authority contract。
- `item_status=-9` ACTIVE 误判。
- Scheduler 商品状态覆盖回归。
- 平台状态检查旧函数 ImportError。
- Publisher `session.refresh` 错误引用。
- `【核心服务】` 异常测试商品被当有效商品的问题。

重新打开必须同时记录：

```text
NEW_DIRECT_RUNTIME_EVIDENCE=true
OLD_RESOLUTION_CONTRADICTED=true
FIRST_DIVERGENCE=
```

否则 `DO_NOT_REOPEN_RESOLVED_WORK=true`。

## 8. 修复纪律

任何 Repair/Development：

```text
PRE_CHANGE_BASELINE
→ IMPACT_MATRIX
→ CURRENT_UPSTREAM vs CURRENT_LOCAL vs CURRENT_RUNTIME
→ FIRST_DIVERGENCE
→ MINIMAL_PATCH
→ TARGETED_TESTS
→ RELATED_REGRESSION_TESTS
→ TARGETED_RUNTIME_ACTIVATION
→ POST_CHANGE_MATRIX
→ GITHUB PERSISTENCE
```

如果 A 修好但 B/C/D 原正常功能变坏：

```text
ACCEPTANCE=FAILED_REGRESSION
```

禁止继续叠补丁掩盖新回归，必须回滚或重新定位 FIRST_DIVERGENCE。

## 9. 当前下一步

XIANYU 当前没有剩余 Session 代码修复任务。

下一步是业务恢复：

1. 用户仅对 `1034641456`、`2219319284219`、`2858469041` 做官方 QR。
2. QR 后只读验证 authoritative auth + safe MTOP，不重新修 Session。
3. 判断 `2858469041` disabled 原因。
4. 健康账号继续正常 CODEX Publisher 业务；最终 ACTIVE 必须以 `item_status==0` 读回确认。

经营层商品数量、价格、ITEM_ID、Chain 映射和 NEXT TASK 以 ZIDONGZHUA `docs/CURRENT_STATE.md` 为权威，不在 XIANYU handoff 维护第二份。

## 10. 历史证据位置

历史细节按需读取，不要默认全量重跑：

- `changes/active/CHG-0018-account-profile-publish-safety/evidence/`
- Session/Cookie closure evidence：`changes/active/CHG-0018-account-profile-publish-safety/evidence/20260819-session-cookie-authority-closure/`
- 商品状态修复 evidence：`changes/active/CHG-0018-account-profile-publish-safety/evidence/20260819-item-platform-status-display-repair.md`
- targeted tests / vendor patches / manifests

历史 evidence 用于证明“为什么这样做”，当前 handoff 用于回答“现在是什么状态”。二者不得混用。