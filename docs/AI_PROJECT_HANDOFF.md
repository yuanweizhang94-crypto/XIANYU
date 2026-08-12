# XIANYU × COMPANY_LOCAL_EXECUTION_TOOL
# AI 无缝接手、开发、修复与正常使用长期权威手册

**文档定位：Living Handoff / AI Bootstrap / 项目长期记忆基线**  
**首次建立时间基线：2026-08-12 22:45（Asia/Taipei / UTC+8）**  
**适用对象：ChatGPT、Codex、其他 AI 开发代理、公司同事、维护人员**  
**适用任务：正常业务执行、故障判断、项目开发、Upstream 同步、生产修复、GitHub 维护、运行时核验**

## 0. 永久有效原则

本文件不是把某个时间点的 Commit、PID、账号 Session、镜像 ID 永久写死，而是定义一个长期有效的“权威刷新协议”。

任何时候发生冲突，权威优先级固定为：

1. 当前 GitHub 仓库最新状态
2. 当前本地 checkout 的真实 Git 状态
3. 当前生产 Runtime 实际加载的源码、镜像、配置和服务状态
4. 仓库根目录 `AGENTS.md`
5. 当前 README / docs
6. 本文件中带时间戳的 Snapshot
7. 旧聊天记录、旧记忆、旧截图

固定流程：

`GITHUB_CURRENT → LOCAL_CURRENT → RUNTIME_CURRENT → 再使用历史上下文`

如果 GitHub、Local、Runtime 与本文件 Snapshot 冲突，以当前真实状态为准，并更新 Snapshot。

---

# 1. 三个项目/来源

## 1.1 XIANYU 用户仓库

`https://github.com/yuanweizhang94-crypto/XIANYU`

XIANYU 是真正负责闲鱼业务的系统，负责：

- Account
- DB Cookie
- Session
- canonical Profile
- Material
- Publisher
- Category
- Playwright
- WebSocket
- Scheduler
- 发布日志
- 商品同步
- 闲鱼官方业务页面交互

原则：

`UPSTREAM_FIRST=true`

## 1.2 XIANYU Upstream

`https://github.com/zhinianboke/xianyu-auto-reply`

公开 upstream 当前 README 将项目描述为基于 FastAPI、React、MySQL、Redis、Playwright 的闲鱼多账号自动化系统，并公开列出账号管理、Cookie维护/登录续期、素材库、商品发布、发布日志、WebSocket、Scheduler 等能力。

因此任何 AI 准备在 XIANYU 中新增登录续期、Cookie 维护、Material、Publisher、Playwright、WebSocket、Scheduler 等能力前，必须先检查 upstream 当前实现。

UPSTREAM_FIRST 不等于整文件覆盖本地。

正确：

`读取 upstream → 比较 local → 保留本地已验证增强 → 只同步真正缺失部分`

## 1.3 COMPANY_LOCAL_EXECUTION_TOOL

`https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL`

用户显示名称：

`笔记本本地执行工具`

内部定位：

`COMPANY_LOCAL_EXECUTION_TOOL`

职责：

- ChatGPT ↔ Windows 执行桥
- MCP
- Proxy
- Runner
- Supervisor
- Cloudflare Tunnel 接入
- 文件桥
- ChatGPT 附件接收
- 本地维护能力
- XIANYU Thin Business Adapter

它不是 XIANYU，不得重新实现：

- Publisher
- Account
- Cookie lifecycle
- Session lifecycle
- Profile Manager
- Material Service
- Category System
- 闲鱼 Playwright 业务流程

原则：

`THIN_ADAPTER_ONLY=true`

## 1.4 COMPANY_LOCAL_EXECUTION_TOOL 的 Upstream

截至 2026-08-12，没有定义一个类似 XIANYU → zhinianboke/xianyu-auto-reply 的正式业务 Upstream 仓库。

COMPANY_LOCAL_EXECUTION_TOOL 是用户自有基础设施仓库。DevSpace、Cloudflare Tunnel、Node/Python 等属于依赖，不应擅自称为本项目 Upstream。

以后如果 GitHub 的 `AGENTS.md` / `README.md` 正式声明 upstream/fork 来源，以 GitHub 最新声明为准并更新本节。

---

# 2. 两个项目的关系

正式关系：

`用户 → ChatGPT → COMPANY_LOCAL_EXECUTION_TOOL → 当前运行的 XIANYU → Goofish/闲鱼官方路径`

COMPANY_LOCAL_EXECUTION_TOOL 负责：

“怎么安全地把 ChatGPT 的意图、文件和正式业务调用送到 Windows / XIANYU。”

XIANYU 负责：

“真正怎样维护账号、Session、Cookie/Profile、Material、Publisher、分类、Playwright、WebSocket、Scheduler 和平台业务。”

一句话：

**本地执行工具是桥，XIANYU 是业务系统。**

---

# 3. 本地与 Runtime

## 3.1 XIANYU

最近已知本地 checkout：

`D:\xianyu`

任何 AI 开始开发时必须重新确认：

`git rev-parse --show-toplevel`
`git remote -v`
`git branch --show-current`
`git rev-parse HEAD`
`git status -sb`

不得把任何路径或 SHA 永久当成当前状态。

## 3.2 COMPANY_LOCAL_EXECUTION_TOOL 运行组件

当前长期基线：

DevSpace：

`D:\TikTok_Auto\devspace`

Proxy / Runner：

`D:\TikTok_Auto\devspace_proxy`

Proxy：

`D:\TikTok_Auto\devspace_proxy\proxy.cjs`

Runner：

`D:\TikTok_Auto\devspace_proxy\mcp_runner.cjs`

附件：

`D:\ChatGPT-Transfers`

公网 MCP：

`https://exec.imzyw.com/mcp`

本地端点：

- Proxy: `127.0.0.1:7681`
- DevSpace: `127.0.0.1:7676`
- Cloudflared readiness/metrics: `127.0.0.1:20241`

这些是运行组件路径。COMPANY_LOCAL_EXECUTION_TOOL 当前 Git checkout 根目录必须在维护任务开始时通过 Git 重新确认。

---

# 4. 正常 XIANYU 商品发布唯一流程

默认：

`BUSINESS_EXECUTION=true`

正式路径：

`用户上传图片`
→ `ChatGPT`
→ `笔记本本地执行工具`
→ `receive_attachment`
→ `D:\ChatGPT-Transfers`
→ `xianyu_material_import`
→ `XIANYU Material / material_id`
→ `xianyu_publish_single`
→ `XIANYU Backend`
→ `POST /api/v1/product-publish/publish/batch`
→ `BATCH_SIZE=1`
→ `PublishExecutorService`
→ `execute_single_publish`
→ `publish_single_item`
→ `XianyuPublisher`
→ `DB latest Cookie + canonical Profile`
→ `Playwright`
→ `goofish.com/publish`
→ `平台真实 UI`
→ `真实发布请求`
→ `platform_item_id / item_url`

永久禁止真实发布使用：

- run_program
- container_run
- 临时 Python
- 临时 Node
- direct import execute_single_publish
- direct import XianyuPublisher
- 临时 Playwright
- 自己拼 Goofish 发布请求
- 绕过 Material
- 绕过 Backend
- 第二套 Publisher

永久：

`RUN_PROGRAM_REAL_PUBLISH=false`
`CONTAINER_RUN_REAL_PUBLISH=false`
`DIRECT_IMPORT_REAL_PUBLISH=false`

run_program 只可用于明确授权的 COMPANY_LOCAL_EXECUTION_TOOL 自身基础设施维修，不得扩张成业务旁路。

---

# 5. Attachment 与 Material

正式附件工具：

`receive_attachment`

保存：

`D:\ChatGPT-Transfers`

长期基线：

JPEG / PNG / WEBP，Attachment 层 25MB 上限，带路径穿越、MIME、文件大小校验。

XIANYU upload/images 还有独立限制。

正式 Material 工具：

`xianyu_material_import`

Material 是完整商品模板，不只是图片。

正确：

`Attachment → XIANYU upload/images → ProductMaterialService → Material → material_id`

禁止伪造 material_id，禁止因为发布失败反复重建相同 Material，禁止跳过 Material Bridge。

---

# 6. Publish 状态语义

正式状态：

- SUBMITTED
- RUNNING
- SUCCESS
- FAILED
- UNKNOWN

Backend `/publish/batch` HTTP 200 只能表示：

`SUBMITTED`

SUCCESS 必须至少有：

- platform_item_id
- item_url
- AUTHORITATIVE_SYNC_CONFIRMED=true

502 / timeout 永久规则：

`STOP NEW EXECUTION → READ-ONLY STATUS RECOVERY → SUCCESS / FAILED / UNKNOWN`

UNKNOWN 绝对禁止盲目重试。

---

# 7. Session / Account

以下不能单独证明账号可发布：

- ACCOUNT_RECORD_HEALTHY
- COOKIE_PRESENT
- PROFILE_PRESENT

最终权威：

`REAL_BROWSER_LOGIN_READY`

真实 Playwright 页面高于 DB 推测。

生产 Session 生命周期：

`Account → DB latest Cookie → canonical Profile(browser_data/user_<account_id>) → Session health → existing renew service → DB Cookie update → canonical Profile sync → REAL_BROWSER_LOGIN_READY`

2026-08-12 收口时统一后台入口基线：

`API_COOKIE_RENEW_ENABLED=true`

历史周期：

`3600 seconds`

重叠 Scheduler 入口保持关闭的原则是避免多个 Renew 服务抢同一账号/Profile。当前实际开关必须以 GitHub + Runtime 最新配置为准。

如果真实页面出现官方 QR：

`HUMAN_QR_REQUIRED=true`

禁止 QR 绕过、跨账号 Cookie/Profile。

批量业务应跳过该账号并选择下一个 `REAL_BROWSER_LOGIN_READY=true` 账号。

---

# 8. Browser Lock

历史 browser_busy 根因曾是：

`STALE_BROWSER_LOCK_OR_CLEANUP_GAP`

已完成：

- stale SingletonLock cleanup
- RLock finally release
- lock owner metadata
- diagnostic persistence

同账号：

`ACTIVE_BROWSER_OPERATIONS_MAX=1`

Publisher、Renew、QR/Profile Sync 必须共享账号级互斥。

没有新证据禁止再造第二套 Browser/Profile Manager。

---

# 9. 分类事故与最终修复

必须长期记住：

历史连续 `no_supported_category` 的最终根因不是 Auth、Material、Session、账号，也不是平台完全没有分类。

根因是本地 CHG-0018 后续逻辑把 `SELECTED_CONFIRMED` 变成过度严格硬门槛。

错误逻辑：

`click candidate → 要求分类字段文字立即 == candidate → false → reject → all rejected → no_supported_category`

但真实平台 UI 成功可能表现为：

- popup close
- next-level category appears
- breadcrumb changes
- selected/checked/active
- internal category value changes
- category field changes

最终正式模型：

`PLATFORM_UI_FIRST=true`

分类状态机：

- FINAL_SELECTED
- NEXT_LEVEL_REQUIRED
- CLICK_NOT_EFFECTIVE
- PC_WEB_UNSUPPORTED
- LOGIN_REQUIRED
- PLATFORM_VERIFICATION_REQUIRED

本地 semantic/category mapping 只允许排序、辅助、诊断、高置信明显错误 Fail Closed。

以下不能单独导致 no_supported_category：

- LOCAL_MAPPING_MISS
- SEMANTIC_GATE_MISS
- SELECTED_CLASS_NOT_FOUND

---

# 10. PC Web 分类限制

如果平台真实页面明确：

`网页版暂不支持发布此分类`

正式状态：

`CATEGORY_WEB_UNSUPPORTED`

必须 Fail Closed。

禁止：

- 强制 categoryId
- 强制 channelCatId
- 错误分类
- 伪造分类
- 绕过平台限制

这是：

`OFFICIAL_PLATFORM_LIMITATION`

不是开发需求。

---

# 11. Upstream 与本地 Publisher

原则：

`UPSTREAM_FLOW + LOCAL_VERIFIED_SAFETY`

不能无脑整文件覆盖 upstream。

本地已经存在经生产验证的安全增强，例如：

- PC Web unsupported Fail Closed
- 去除重复分类流程
- 发布状态治理
- browser/account lock
- diagnostics
- category UI state machine

同步 upstream：

`FETCH → DIFF → 找 upstream 新能力 → 找 local 已领先修复 → 只同步真正缺失部分 → tests → runtime activation`

禁止：

`checkout upstream file → overwrite local`

---

# 12. 2026-08-12 生产验证 Snapshot

该 Snapshot 只用于历史迁移，不代表未来当前状态。

最终分类修复加载生产 Runtime 后：

- Material 9 → SUCCESS → platform_item_id `1075653752858`
- Material 8 → SUCCESS → platform_item_id `1074662425907`
- Material 7 → SUCCESS → platform_item_id `1073635950977`
- Material 6 → SUCCESS → platform_item_id `1073637026044`
- Material 10 → CATEGORY_WEB_UNSUPPORTED

`TOTAL=5`
`SUCCESS=4`
`FAILED=1`
`REAL_PRODUCTS_CREATED=4`

证明当时 Publish、Session、Category UI-first 主链已经可用，且平台限制能正确 Fail Closed。

---

# 13. 已解决问题，不得无证据重开

COMPANY_LOCAL_EXECUTION_TOOL：

- Proxy orphan
- EADDRINUSE retry storm
- Runner ownership / cleanup
- Supervisor single-instance
- Attachment Bridge
- Backend JWT Sync
- Business Adapter
- 502 / UNKNOWN 语义

XIANYU：

- Material Bridge
- HTTP 200 ≠ SUCCESS
- browser_busy stale lock
- QR Profile Sync
- DB/Profile Cookie Sync
- Session maintenance lifecycle
- pre-publish real browser readiness
- semantic hard gate
- overrestrictive SELECTED_CONFIRMED
- duplicate category selection
- final category UI state machine

原则：

`NEW_EVIDENCE_REQUIRED_TO_REOPEN=true`

---

# 14. 写代码前强制门禁

任何 AI 写任何代码前必须证明：

1. 当前 upstream 没有可复用的现成功能。
2. 当前 local 没有可复用的现成功能。
3. 当前 Runtime 不是仅没有加载已有实现。
4. 不是配置问题。
5. 不是数据问题。
6. 不是 Session / Account 状态问题。
7. 不是平台官方限制。
8. 不是现有功能调用方式错误。
9. 不是旧镜像/旧容器/旧进程。
10. 修改现有最小函数确实必要。

不能证明：

`NEW_IMPLEMENTATION_ALLOWED=false`

---

# 15. 开发顺序

`OBSERVE`
→ `CLASSIFY RESPONSIBLE LAYER`
→ `READ AGENTS.md`
→ `CHECK CURRENT GITHUB`
→ `CHECK UPSTREAM`
→ `CHECK LOCAL`
→ `CHECK RUNTIME`
→ `ROOT CAUSE`
→ `REUSE EXISTING CAPABILITY`
→ `MINIMAL PATCH ONLY IF REQUIRED`
→ `TARGETED TESTS`
→ `RELATED REGRESSION`
→ `REPOSITORY VERIFY`
→ `RUNTIME ACTIVATION`
→ `STOP`

禁止：

`Patch → Try real product → Patch → Try real product`

同一问题连续两个修复仍未解决，必须停止 Patch 叠加，做：

`CURRENT_UPSTREAM vs CURRENT_LOCAL vs CURRENT_RUNTIME`

三方精确对照。

---

# 16. 责任层

MCP / Proxy / Runner / Tunnel：

`COMPANY_LOCAL_EXECUTION_TOOL`

Attachment 落盘：

`COMPANY_LOCAL_EXECUTION_TOOL`

Adapter / Backend JWT Bridge：

主要是 `COMPANY_LOCAL_EXECUTION_TOOL` 边界，但不得借此重写 XIANYU 业务。

Material / Account / Cookie / Session / Profile / Publisher / Category / Scheduler / WebSocket：

`XIANYU`

QR / Slider / Face / 官方认证：

`Official Platform + Human Interaction`

CATEGORY_WEB_UNSUPPORTED：

`Official Platform Limitation`

---

# 17. BUSINESS_EXECUTION 与 DEVELOPMENT

用户说：

- 发布商品
- 继续发布
- 上传这些图
- 查发布状态

默认：

`BUSINESS_EXECUTION`

不要自动升级成源码审计、Upstream Sync、Repair、Canary、Docker Rebuild 或重构。

只有正式调用返回新的系统级证据才进入 Repair。

---

# 18. Runtime First

代码修复不等于生产修复。

如果是 image-baked source：

`modify source → tests → build necessary image only → replace necessary container only → health check → verify runtime source/hash`

禁止本地代码修了、Runtime 仍旧，却拿真实商品反复试错。

---

# 19. GitHub 长期维护

建议两个仓库都维护：

XIANYU：

- `/AGENTS.md`
- `/README.md`
- `/docs/AI_PROJECT_HANDOFF.md`
- `/docs/CURRENT_PRODUCTION_BASELINE.md`

COMPANY_LOCAL_EXECUTION_TOOL：

- `/AGENTS.md`
- `/README.md`
- `/docs/AI_PROJECT_HANDOFF.md`
- `/docs/XIANYU_USAGE_MODE.md`
- `/docs/DEVELOPMENT_RULES.md`

优先级：

`AGENTS.md = P0`
`README AI Notice = P1`
`AI_PROJECT_HANDOFF = P1`
`dated baseline/history = P2`

重大更新必须更新：

- Git commit
- upstream checked SHA/base
- 修改模块
- Why changed
- Reused existing capability
- 禁止重复开发内容
- Tests
- Runtime activation
- Known blockers
- State semantics
- Security boundaries
- dated production validation

禁止记录 Cookie、JWT、Authorization、密码、API Key、QR payload、客户私密消息、私钥。

---

# 20. 新 AI 无缝接手流程

STEP 1：读 `AGENTS.md`

STEP 2：确认三个地址：

XIANYU origin

`https://github.com/yuanweizhang94-crypto/XIANYU`

XIANYU upstream

`https://github.com/zhinianboke/xianyu-auto-reply`

COMPANY_LOCAL_EXECUTION_TOOL origin

`https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL`

STEP 3：刷新 Git branch / HEAD / status / remotes / upstream。

STEP 4：确认 Local 与 GitHub。

STEP 5：确认 Runtime 镜像/容器/健康/源码与 Local。

STEP 6：输出 `TASK_TYPE=BUSINESS_EXECUTION / REPAIR / DEVELOPMENT`

STEP 7：输出 `FAILURE_REASON` 与 `RESPONSIBLE_LAYER`

STEP 8：检查：

`UPSTREAM_EXISTING_CAPABILITY`
`LOCAL_EXISTING_CAPABILITY`
`RUNTIME_EXISTING_CAPABILITY`

STEP 9：决策：

已有 → REUSE

Runtime stale → ACTIVATE_RUNTIME

已有实现明确 bug → MINIMAL_EXISTING_FUNCTION_FIX

确实不存在 → NEW_IMPLEMENTATION_ALLOWED=true

STEP 10：Targeted + Regression + Verify。

STEP 11：必要时只激活对应 Runtime。

STEP 12：更新 GitHub Handoff，让下一 AI 不重复调查。

---

# 21. 开发前 Precheck 模板

```text
DEVELOPMENT_PRECHECK

TASK_TYPE=
FAILURE_REASON=
RESPONSIBLE_LAYER=

UPSTREAM_REPO=
UPSTREAM_HEAD=
UPSTREAM_EXISTING_CAPABILITY=

LOCAL_REPO=
LOCAL_HEAD=
LOCAL_EXISTING_CAPABILITY=

RUNTIME_VERSION=
RUNTIME_EXISTING_CAPABILITY=
RUNTIME_MATCHES_LOCAL=

CONFIGURATION_ISSUE=
SESSION_OR_DATA_ISSUE=
OFFICIAL_PLATFORM_LIMITATION=

MINIMAL_EXISTING_FUNCTION_TO_CHANGE=
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=

NEW_IMPLEMENTATION_REQUIRED=
NEW_IMPLEMENTATION_ALLOWED=
```

只要：

`NEW_IMPLEMENTATION_ALLOWED != true`

禁止新增系统或平行实现。

---

# 22. 永久禁止无证据创建

- 第二套 Publisher
- 第二套 Login
- 第二套 Session Renew
- 第二套 Profile Manager
- 第二套 Material Service
- 第二套 Category System
- 第二套 Business Adapter
- 第二套 Supervisor
- 第二套 Proxy
- 第二套 Attachment Pipeline

已有能力有 bug：

**修已有能力，不复制。**

---

# 23. 安全与平台边界

禁止：

- CAPTCHA 绕过
- Slider 绕过
- Face Verification 绕过
- QR 绕过
- 强制错误分类
- 强制内部分类 ID 规避平台限制
- 跨账号 Cookie/Profile
- Secrets 输出
- UNKNOWN 盲重试

Fail Closed 是正常生产行为，不是“功能不够强”。

---

# 24. 两个项目的最简单使用方法

XIANYU：

真正负责闲鱼业务。

普通 AI 不应直接调用内部 Python Publisher 函数。

通过正式 Backend / Business Adapter。

正常发布：

`Material → xianyu_publish_single → Publisher`

COMPANY_LOCAL_EXECUTION_TOOL：

让 ChatGPT 安全操作 Windows 和调用 XIANYU 正式能力。

正常 XIANYU 业务优先：

- receive_attachment
- xianyu_material_import
- xianyu_publish_single
- xianyu_publish_status
- xianyu_account_status

通用执行工具属于基础设施能力，不是正常闲鱼发布入口。

---

# 25. 地址速查

XIANYU：

`https://github.com/yuanweizhang94-crypto/XIANYU`

XIANYU Upstream：

`https://github.com/zhinianboke/xianyu-auto-reply`

COMPANY_LOCAL_EXECUTION_TOOL：

`https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL`

COMPANY_LOCAL_EXECUTION_TOOL 正式业务 Upstream：

`NONE DECLARED AS OF 2026-08-12`

未来如果 GitHub 文档改变，以最新 `AGENTS.md / README` 为准。

---

# 26. Snapshot 与永久规则分离

带时间戳的动态值：

- HEAD SHA
- upstream SHA
- image ID
- PID
- account health
- Session
- Material ID
- Item ID
- Scheduler current switch
- Container state

永久原则：

- 项目职责边界
- UPSTREAM_FIRST
- LOCAL_EXISTING_CAPABILITY_FIRST
- CURRENT_RUNTIME_FIRST
- REUSE_FIRST
- NO_BYPASS
- NO_DUPLICATE_DEVELOPMENT
- MINIMAL_PATCH_ONLY
- FAIL_CLOSED
- BUSINESS_EXECUTION_BY_DEFAULT
- UNKNOWN_NEVER_BLIND_RETRY

发生以下事件必须更新 Snapshot：

- Upstream 大版本同步
- Publisher 变化
- Session lifecycle 变化
- Business Adapter schema 变化
- MCP tool list 变化
- Runtime deployment model 变化
- Repository relocation
- New upstream declared
- Major production incident
- Major production verification

---

# 27. 给其他 AI 的一句话总指令

这是两个已经生产化且职责明确的项目。COMPANY_LOCAL_EXECUTION_TOOL 是 ChatGPT ↔ Windows 的基础设施与 XIANYU 薄适配器；XIANYU 是真正的闲鱼业务系统，并以 zhinianboke/xianyu-auto-reply 为 Upstream。任何正常业务优先调用现有正式工具；任何开发在写代码前必须完成 CURRENT_UPSTREAM vs CURRENT_LOCAL vs CURRENT_RUNTIME 三方确认。证明不了 upstream/local/runtime 都无法复用，就禁止新增实现。已有功能有 bug 就最小修已有功能，禁止平行实现、旁路、重复造轮子和 Patch→Try→Patch→Try。GitHub 最新状态和当前 Runtime 永远高于聊天记忆和本文件的 dated snapshot。

---

# 28. 最终强制原则

```text
GITHUB_CURRENT_IS_SOURCE_OF_TRUTH=true
LOCAL_CURRENT_MUST_BE_VERIFIED=true
RUNTIME_CURRENT_MUST_BE_VERIFIED=true

UPSTREAM_FIRST=true
LOCAL_EXISTING_CAPABILITY_FIRST=true
CURRENT_RUNTIME_FIRST=true
REUSE_FIRST=true

MINIMAL_PATCH_ONLY=true
NO_PARALLEL_IMPLEMENTATION=true
NO_DUPLICATE_DEVELOPMENT=true
NO_BYPASS=true

BUSINESS_EXECUTION_BY_DEFAULT=true

PLATFORM_UI_IS_AUTHORITATIVE=true
PLATFORM_LIMITATION_FAIL_CLOSED=true
UNKNOWN_NEVER_BLIND_RETRY=true

NEW_IMPLEMENTATION_REQUIRES_PROOF=true
```

**任何 AI 如果没有完成 Precheck，就没有权限新增实现。**
