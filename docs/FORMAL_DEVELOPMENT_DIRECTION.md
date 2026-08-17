# XIANYU 正式精简开发方向

## 文档状态

- 方向状态：项目所有者确认的正式开发方向。
- 本文用途：约束后续调查、设计、开发、测试、交付和扩容，防止重复开发和过度开发。
- 本文不授权：生产修改、账号操作、扫码、平台验证、商品发布、消息发送、启动第二执行器、PR Ready、T17、归档或合并。
- 当前仓库分支：`feat/CHG-0017-upstream-native-auto-ai-delivery`。
- 当前PR：`#26`，必须继续保持 Draft / Open / Unmerged，除非项目所有者另行明确授权。
- XIANYU固定基线：`67d3780dddd73804e7e699b5aa4aef5c74ac17ca`。
- 当前部署所依据的上游固定SHA：`4c5e1ac5f532c7313365d70409ae115305de8a55`。
- 2026-08-05核对的上游 `main`：`7c5487dcf1b8b93e1996f9fc4cd651926d493a53`。该SHA仅用于查找已有修复和理解上游方向，不代表已经部署。
- 笔记本：当前生产执行环境。
- 公司台式机：开发、修复和普通核心运行环境；涉及同一闲鱼账号的WebSocket、自动回复、AI副作用、Scheduler副作用和发布执行必须保持关闭，直到完成明确的主机交接。

## P0：永久最高级开发原则

除安全、合法性、凭据、权限、平台人工验证边界和项目所有者明确指令外，以下原则永远排在所有开发目标之前：

> 上游已经有的方法、代码、服务、模型、接口、页面、任务、缓存、锁、Profile、日志或工作流，必须直接使用；存在明确缺陷时，只修复原有路径；禁止自己另造一套轮子，禁止重复开发，禁止为了未来可能需要而过度设计。

所有任务必须依次选择：

1. `ADOPT_UPSTREAM`：直接采用上游原生功能和原生工作流。
2. `CONFIGURE_UPSTREAM`：只修配置或运行方式，不改代码。
3. `PATCH_UPSTREAM`：在原有执行路径上做最小、可审计、可回滚的缺陷修复。
4. `WRAP_FOR_OPERATIONS`：只允许增加安全、治理、验证、监控、备份、恢复、诊断、升级控制或极薄的兼容层。
5. `BUILD_LOCAL_EXCEPTION`：只有上游确实没有能力、配置不能解决、最小补丁不能解决、运营包装不能解决，并且项目所有者明确批准后才允许。

禁止先设计本地方案，再去上游寻找理由。正确顺序必须是：

```text
上游功能说明和原生流程
→ 固定SHA源码、测试和配置
→ 上游最新提交、Issues和评论中是否已有修复
→ 直接采用或配置
→ 修复确认的上游缺陷
→ 只有证据证明仍有缺口时才考虑本地例外
```

## 每次开发前的强制记录

任何新Change进入 `IMPLEMENTING` 前，都必须先写清楚：

- `User outcome`：用户真正等待的业务结果。
- `Confirmed blocker`：当前唯一已证实的阻塞点。
- `Smallest success test`：能够证明阻塞消失的最小安全测试。
- 上游功能名称和原生用户流程。
- 当前固定上游SHA和具体证据路径。
- 上游最新代码、Issues、评论中是否已有同类修复。
- 选定的复用决策。
- 如果不直接采用上游，为什么配置和最小补丁都不够。
- 重复开发风险。
- 执行所有者。
- 回滚方法。
- 停止条件。

没有这些记录，不得开始写业务代码。

## 已确认的当前问题

当前批量发布共9个账号：

- 原始成功：4个。
- 原始失败：5个。
- 其中1个已通过API Cookie续期和官方快速进入恢复。
- 仍失败：4个。
- 这4个账号当前共同证据是缺少持久化浏览器Profile，发布器又使用临时浏览器上下文。
- 当前主要错误表现为 `publish_form_not_rendered`，但该名称只是结果分类，不应被当成唯一根因。
- 当前没有证据证明这4个失败账号主要由代理、IP或需要新Token系统造成。

因此，正式开发必须优先修复“账号登录续期环境”和“商品发布环境”没有复用同一个账号Profile的问题，不得先扩建代理池、指纹系统、大型队列或分布式架构。

## Token服务的正式定位

### 远程Token服务是什么

充值使用的远程Token服务是闲鱼IM/WebSocket `accessToken` 和配套 `device_id` 的兜底获取服务，不是长期Cookie，不是商品发布权限，也不是浏览器登录环境。

当前上游链路已经实现：

```text
先读Token缓存
→ 缓存有效则直接使用
→ 缓存无效则先调用本地网页Token接口
→ 本地失败后才调用远程Token服务
→ 成功后缓存Token、device_id和过期时间
→ 记录远程Token风险日志
```

### 它能够减少的问题

- 本地Token接口失败导致WebSocket无法注册。
- 账号离线、收不到买家消息和自动回复中断。
- 本地接口临时异常时反复人工处理。
- 缓存有效时重复调用和重复消耗远程额度。

### 它不能解决的问题

- Cookie完全失效。
- 扫码、密码登录、人脸或官方安全验证。
- 浏览器Profile缺失。
- `publish_form_not_rendered`。
- 商品发布页登录态和表单问题。
- IP、代理和商品流量问题。

### 安全边界

远程Token调用会把账号完整Cookie发送到配置的第三方服务。必须把该服务视为高敏感外部依赖：

- 不在日志、报告、Git或聊天中输出Cookie、Token、API密钥和完整响应。
- 不新建第二套远程Token客户端、Token缓存或Token定时器。
- 服务商保存Cookie的规则、扣费规则和失败是否扣费不由仓库代码证明，必须以服务商说明和账单为准。
- 远程服务失败不能破坏原Cookie或绕过官方验证。

## 已有能力的正式处置

下列能力已经由上游或当前XIANYU治理层提供，后续禁止平行重做：

| 能力 | 已有实现 | 正式决定 | 禁止重复开发 |
|---|---|---|---|
| 本地Token获取 | 上游网页Token接口、签名和 `_m_h5_tk` 更新 | `ADOPT_UPSTREAM` | 新Token协议、签名或本地取Token服务 |
| 远程Token兜底 | 本地优先、远程回退、超时和重试 | `ADOPT_UPSTREAM` | 第二套远程Token客户端或自动切换平台 |
| Token/device_id缓存 | 上游缓存、过期时间和启动复用 | `ADOPT_UPSTREAM` | 新Token缓存表、新device_id系统 |
| Token定时维护 | WebSocket刷新循环和上游Scheduler任务 | `CONFIGURE_UPSTREAM` | 第三套Token定时器 |
| Cookie维护 | API续期、浏览器快速进入、密码登录和Cookie合并 | `ADOPT_UPSTREAM` | 新Cookie续期系统或Cookie保险库 |
| 扫码和密码登录 | 上游QR、密码、验证状态、账号创建/更新 | `ADOPT_UPSTREAM` | 新扫码页面、新登录服务 |
| 持久化Profile | 上游续期浏览器使用 `browser_data/user_{account_id}` | `ADOPT_UPSTREAM` | 第二套Profile目录、Profile复制系统 |
| 同账号浏览器锁 | 上游账号级浏览器锁 | `ADOPT_UPSTREAM` | 新账号锁管理器 |
| 全局浏览器槽位 | 上游有界并发槽位，默认安全并发为1 | `ADOPT_UPSTREAM` | RabbitMQ、Celery或新的浏览器队列平台 |
| 账号状态和暂停 | 上游 `status`、禁用原因、暂停和在线状态 | `ADOPT_UPSTREAM` | 第二套账号主状态表 |
| 账号备注 | 上游 `XYAccount.remark`、API和账户页面编辑 | `ADOPT_UPSTREAM` | 新联系人表作为首期方案 |
| 权限和归属 | 上游 `owner_id`、管理员和账号作用域 | `ADOPT_UPSTREAM` | 新权限平台 |
| 发布原生流程 | 上游 `detect_publish_account_capability -> XianyuDirectPublisher / XianyuPersonalPublisher -> mtop` | `ADOPT_UPSTREAM`；旧 `XianyuPublisher`/Playwright 仅保留 legacy/其他真实调用 | 在正常 single/batch 前重新加入 `REAL_BROWSER_LOGIN_READY`/Profile/Playwright 门禁，或新建第二 Publisher |
| Browser/Profile 发布诊断 | CHG-0017/CHG-0018 历史 Browser Publisher 诊断仍可服务真正需要浏览器的 legacy 调用 | `HISTORICAL_COMPATIBILITY_ONLY`，不是正常 single/batch 发布前置条件 | 将 Browser/Profile readiness 重新提升为 latest direct/personal publish 的全局门禁 |
| 发布幂等和审核 | XIANYU `PublishService` 已有幂等、重复检测、授权、风险和人工审核决策 | `ADOPT_LOCAL_GOVERNANCE` | 第二套发布幂等、审核和审计系统 |
| 风控日志 | 上游登录、续期和远程Token风险日志 | `ADOPT_UPSTREAM` | 新风控日志平台 |
| 数据库备份 | 上游定时压缩备份和保留策略 | `CONFIGURE_UPSTREAM` | 新备份平台；只需后续验证恢复 |
| WebSocket和消息 | 上游连接、接收、解析、自动回复和发送 | `ADOPT_UPSTREAM` | 本地IM协议、第二发送器、第二自动回复执行器 |

## 商品发布正式方向（2026-08-17 latest upstream）

### 正常 single/batch 发布 owner

当前正式权威是 upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` 的接口发布架构：

```text
明确选择 account_id
→ authoritative owner/account lookup
→ XYAccount authoritative Cookie
→ execute_single_publish
→ detect_publish_account_capability
→ fish shop: XianyuDirectPublisher
→ personal seller: XianyuPersonalPublisher
→ mtop publish
→ platform_item_id / item_url
→ Publish Log
→ authoritative item sync
```

永久规则：

- `LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true`。
- `NORMAL_DIRECT_PUBLISH_REQUIRES_BROWSER=false`。
- `REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true`。
- `NORMAL_SINGLE_PUBLISH_BROWSER_OWNER=false`。
- `NORMAL_BATCH_PUBLISH_BROWSER_OWNER=false`。
- 不得因为账号不是鱼小铺而判定发布不可用；必须按 upstream capability detection 分流到普通卖家 Publisher。
- `FAIL_SYS_USER_VALIDATE`、`RGV587`、punish/captcha/session 错误如果来自 Publish MTOP，必须作为真实 platform publish error 返回，不能转换成 Browser/Profile readiness 失败。

### Browser/Profile 历史能力的保留边界

`XianyuPublisher`、canonical Profile、账号浏览器锁、全局 browser slot、Browser preflight 和历史 CHG-0017/CHG-0018 修复不删除，但它们只服务仍然真实需要 Browser 的 legacy/兼容/其他调用。

它们不得重新成为正常 single/batch Publish 的 owner，也不得在 latest direct/personal Publisher 之前增加：

- `REAL_BROWSER_LOGIN_READY`；
- Persistent Profile ready；
- Playwright session；
- publish-page preflight；
- publish form rendered。

### 正常发布必须保留的 XIANYU 安全语义

- 严格使用用户明确选择的 `account_id`，失败后不自动切换账号。
- `owner_id` 必须与 authoritative account 归属一致。
- 只使用 `XYAccount` 当前 authoritative Cookie；MTOP 原生 Set-Cookie 刷新后继续回写 authoritative Cookie。
- 真实提交不自动重试；`UNKNOWN` 绝不触发自动重发。
- 真实 batch 严格串行，`ACTIVE_REAL_BATCH_EXECUTORS_MAX=1`。
- HTTP 200 / “任务已提交”只能表示 `SUBMITTED`。
- `SUCCESS` 至少要求 `platform_item_id`、`item_url` 或 `AUTHORITATIVE_SYNC_CONFIRMED=true`。
- 发布失败不得影响独立 Auto Reply WebSocket。

### 分类和 Material

分类、规格、视频、运费和地址数据契约直接跟随 latest upstream；不得恢复旧“强制虚拟商品分类”或另建第二套分类系统。`xy_product_materials` 需要的增量字段必须来自 upstream 自带 schema/migration 定义。

## 账户管理的最小增强

账号备注功能上游已经存在，首期不新增联系人表。

正式方向：

- 使用现有 `remark` 字段记录账号实际联系人或负责人。
- 推荐格式：`姓名｜联系代号｜手机尾号`，例如 `张三｜ZS01｜4821`。
- 不在备注中保存身份证号、完整手机号、密码、Cookie、Token、验证码或其他高敏感信息。
- 账户列表单独显示“备注/联系人”列。
- 在现有账户查询中增加备注模糊搜索，而不是另建搜索服务。
- 在扫码、密码登录、人工验证、Profile缺失和发布预检失败页面显示账号备注，便于迅速找到本人。
- 增加基于现有诊断结果的“需要扫码/人工验证”筛选列表。
- 只有出现一人管理大量账号、联系人频繁变更、需要独立联系人权限或一联系人对应多主体等明确需求时，才重新评估联系人实体表。

## 账号状态的最小方案

不得用新的认证状态机替换上游现有 `status`。当前只需要补充少量发布运营信息：

- `profile_exists`
- `publish_ready`
- `last_preflight_at`
- `last_preflight_reason`

首期优先使用动态计算、现有响应字段或低冲突的现有元数据；没有证据证明必须持久化时，不新增表。

如果后续证明这些状态需要高频并发写入、历史查询或独立事务，再单独设计运行状态表。不得把大型状态机作为当前9账号交付前置条件。

## Scheduler和运行方式

### 当前正式方向

- WebSocket自身已有Token刷新和Cookie刷新循环，继续使用。
- 远程Token保持“本地优先、远程兜底”。
- 当前交付阶段不为了Token而直接启动完整Scheduler。
- 完整Scheduler还包含Cookie续期、擦亮、评价、补发货、同步、备份等任务，必须逐项核对配置和副作用后再启用。
- API Cookie续期任务可能打开浏览器、密码登录、更新Cookie、重新启用账号和重启WebSocket，必须与普通Token刷新分开验证。
- 笔记本继续作为唯一生产副作用执行器。
- 公司台式机的WebSocket、自动回复、AI副作用、Scheduler副作用和发布执行继续默认关闭，直到明确主机交接。

### 后续启用顺序

1. 先验证WebSocket内置Token维护稳定。
2. 单独验证Scheduler Token续期任务，不同时启用其他副作用任务。
3. 再逐个评估需要启用的任务。
4. 每个任务必须有独立开关、日志、失败停止条件和回滚。

## 代理、IP和所谓“防风控”方向

当前没有证据证明4个发布失败账号由代理或IP导致，因此以下内容不进入首批正式开发：

- 一账号一代理。
- 代理池和自动换IP。
- 浏览器指纹随机化。
- User-Agent随机化。
- 请求间隔随机化。
- 设备伪装。
- 绕过滑块、人脸或官方验证。

现阶段原则是保持环境稳定、使用官方流程、遇到平台验证立即停止并转人工。

未来实际使用代理前，只评估合法运营所需的固定网络配置，并必须保证代理失败时禁止偷偷直连。该能力需要新的证据和单独批准，不能夹带在Profile修复中。

## 正式实施顺序

### 阶段0：治理和证据冻结

- 保留当前PR #26 Draft状态。
- 本文只记录方向，不把新Profile开发硬塞进CHG-0017当前业务补丁。
- 在真正写代码前创建或批准一个边界清晰的新Change，引用本文和能力矩阵。
- 重新核对固定上游SHA和当时最新上游代码，确认上游是否已经新增Profile发布复用方案。
- 记录当前9账号的脱敏状态：Cookie续期方式、Profile是否存在、预检结果和联系人备注。

### 阶段1：台式机离线开发

- 只改上游发布器取得浏览器上下文的最小位置。
- 复用现有Profile路径、账号锁、全局槽位和CHG-0017诊断。
- 增加默认关闭的Profile发布开关。
- 增加只读预检模式。
- 增加Profile缺失时的初始化调用点。
- 不修改笔记本生产环境，不执行账号操作，不创建商品，不发送消息。

### 阶段2：离线和模拟验证

必须至少覆盖：

- 原临时浏览器路径保持不变并可回退。
- 开关关闭时行为与当前固定基线一致。
- 开关开启时每个账号只使用自己的Profile路径。
- 已有Profile不会被覆盖。
- Profile缺失能返回明确结果。
- 同账号并发被锁阻止。
- 全局槽位限制有效。
- 预检不产生发布请求。
- 现有 `failure_reason` 和 `diagnostics` 不丢失。
- Cookie、Token、完整账号ID和验证链接不进入日志。
- CHG-0017发布测试继续通过。
- `scripts/validate_change.py` 和 `scripts/verify_repository.py` 通过。

### 阶段3：笔记本只读恢复

该阶段必须由项目所有者单独授权后执行：

- 不启动第二执行器。
- 先备份数据库和Profile目录。
- 对当前4个缺失Profile账号逐个使用官方可见登录或现有续期流程补建Profile。
- 每次只处理一个账号。
- 只运行发布预检，不点击发布。
- 遇到扫码、人脸、滑块或其他官方验证，立即停止并根据备注联系本人。
- 不复制其他账号Profile，不借用其他账号Cookie。

### 阶段4：单账号Canary

该阶段也必须单独授权：

- 选择一个已批准账号。
- 发布前再次执行幂等检查、商品重复检查和只读预检。
- 最多一次真实发布尝试。
- 验证发布结果、失败分类、商品归属和无重复商品。
- 失败后不自动换账号、不连续重试、不扩展架构。

### 阶段5：分批交付和扩容

- 先恢复并验证9个账号。
- 稳定后按 `9 → 10 → 25 → 50 → 75 → 100` 分阶段评估。
- 只有实际负载证据证明单进程或单机不足时，才评估WebSocket分片、跨进程租约或更复杂调度。
- 台式机成为同账号执行器前，必须先完成明确的笔记本停止、静默确认和主机交接。届时只实现最小跨主机执行租约，不提前建设分布式平台。

## 每个核心改动的验收条件

### Profile发布复用

- 一个账号只打开自己的Profile。
- 发布器不再额外创建不必要的临时登录环境。
- 现有发布步骤、API和返回字段兼容。
- 开关关闭可以立即回退。

### Profile初始化

- 新账号或缺失账号能建立唯一Profile。
- 已有Profile不被覆盖。
- 初始化只读，无商品和消息副作用。
- 官方验证转人工，不绕过。

### 发布预检

- 不发送发布请求。
- 能区分Profile缺失、未登录、官方验证、表单未渲染和按钮不可用。
- 批量发布只接受 `READY` 账号。
- 诊断完全脱敏。

### 锁和槽位

- 同账号浏览器任务不能并行。
- 初始全局并发为1。
- 超时后明确失败，不绕锁启动。
- 发布、续期和登录恢复共享同一套锁和槽位。

## 回滚要求

- `PUBLISH_USE_ACCOUNT_PROFILE`默认关闭。
- 回滚只需要关闭开关并恢复当前临时上下文路径，不删除Profile和账号数据。
- 不在回滚中覆盖Cookie、不清空数据库、不删除浏览器Profile。
- 任何数据库字段变化必须可向后兼容；首期尽量不新增字段或表。
- 保留固定上游SHA、补丁哈希、旧镜像、数据库备份和Profile备份。
- 出现新平台验证、未知结果、跨账号污染、重复商品、锁失效或无法确认归属时立即停止。

## 明确取消或推迟的开发

当前方向明确不做：

- 新Token服务。
- 新Token缓存。
- 新Token定时器。
- 新device_id系统。
- 新Cookie续期系统。
- 新扫码或密码登录系统。
- 新风控日志平台。
- 新发布器。
- 新发布失败分类平台。
- 新快速进入实现。
- 新发布幂等、审核或审计系统。
- 新数据库备份平台。
- 新WebSocket协议和第二自动回复发送器。
- 新账号权限平台。
- 新联系人表作为首期方案。
- 大型认证状态机。
- RabbitMQ、Celery或独立浏览器队列平台。
- 当前阶段的WebSocket分片和微服务化。
- 当前阶段的一账号一IP、代理池、指纹随机化和规避平台验证方案。

## 完成定义

这条正式方向只有在以下条件同时满足时才算完成交付：

1. 后续开发始终先核对并复用上游，不出现平行轮子。
2. 当前4个缺失Profile账号通过官方流程建立各自Profile，或被明确归类为需要本人处理。
3. 9个账号都能得到脱敏的发布预检结果。
4. 只有 `READY` 账号可以进入正式发布。
5. 发布、续期和登录恢复共用上游账号锁和浏览器槽位。
6. 单账号Canary无重复商品、无跨账号Cookie/Profile污染。
7. 远程Token仍只是本地失败后的兜底，不被误用为Cookie或发布解决方案。
8. 完整Scheduler没有在未审计副作用任务的情况下被整体启用。
9. 笔记本和台式机没有同时运行同账号副作用执行器。
10. 所有日志、证据和Git内容不包含Cookie、Token、API密钥、完整账号ID、完整商品ID、客户消息、二维码内容、验证URL或浏览器Profile。
11. 目标业务结果已经在受控环境中得到证据证明，而不是仅凭文档、CI或PR状态宣布完成。

## 最终一句话方向

保留并复用上游已经成熟的Token、Cookie、登录、续期、Profile、锁、槽位、备注、权限、日志、WebSocket、发布流程和备份能力；当前只在原生发布器上补齐“复用账号Profile、缺失Profile初始化、只读发布预检、接入现有锁和槽位”四个最小缺口，除此之外不造新轮子、不扩架构、不做过度开发。
