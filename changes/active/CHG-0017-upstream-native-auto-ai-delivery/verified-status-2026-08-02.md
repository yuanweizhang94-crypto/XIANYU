# CHG-0017 当前状态与已验证功能

更新时间：2026-08-02

Change：`CHG-0017-upstream-native-auto-ai-delivery`

分支：`feat/CHG-0017-upstream-native-auto-ai-delivery`

PR：`#26`，保持 `Draft / Open / Unmerged`

## 1. 当前结论

CHG-0017 已完成上游原生自动回复、Gemini AI 回复、多账号运行、原生管理界面和单商品发布链路的阶段性真实验证。

ACCOUNT-A 的商品发布链路已经完成一次受控真实发布闭环：发布请求成功发出、平台返回成功、商品同步发现对应新商品、获得商品标识，且没有创建重复商品。

本 Change 暂不归档、不合并。后续继续测试其他上游原生功能，并在每一项功能通过真实验证后补充本文件和相关 acceptance evidence。

## 2. 已真实验证成功的功能

### 2.1 账号与 WebSocket

- 上游原生账号任务可以启动、停止和恢复。
- ACCOUNT-A 的上游原生 WebSocket 已验证 `running / connected`。
- 多账号运行已验证：两个账号可以同时在线。
- 单账号停止/启动隔离已验证：停止一个账号不会停止另一个账号。
- 服务重启后的启用账号恢复路径已验证。
- 账号管理页面可以展示候选运行时中的启用和在线状态。
- 在线聊天页面可以加载上游原生账号和会话；验证过程中未主动向非测试客户发送消息。

### 2.2 关键词与自动回复基础链路

- 上游原生关键词回复受控测试已通过。
- 回复决策仍复用上游原生 sender、Token、WebSocket、日志和账号任务，不创建第二套自动回复系统。
- 重复消息保护已验证：重复测试消息不会产生第二次成功回复。
- 一键停止已验证：账号停止后测试消息不会触发自动回复。
- 重连恢复已验证：账号重新连接后可以恢复受控回复。
- 回滚演练已验证：AI 和运行任务可停止并恢复，停止期间没有产生额外发送。

说明：默认回复管理页面和配置能力可用，但当前最终运行状态中启用的默认回复数量为 0；不能把“页面可用”写成“默认回复真实发送已验证”。

### 2.3 Gemini AI 回复

- Gemini Provider 调用通过。
- 已验证模型配置链路，包括 Provider、Base URL、模型名称、账号级设置和产品级提示词。
- Provider 零发送测试通过：测试 Provider 时不会调用平台 sender。
- 商品上下文进入 AI 回复的链路已验证，`context_used=true`。
- 受控真实 AI 回复成功。
- 回复为简体中文，并通过完整性和质量门禁。
- Gemini 响应解析已覆盖：忽略 thought parts、合并最终文本、检查 `finishReason`、拒绝截断输出。
- AI 回复和 Provider 测试复用同一解析及质量门禁。
- 账号级自定义提示词按 JSON 对象校验；产品级 AI 提示词保持纯文本。
- 未出现模板、Markdown、JSON、重复回复、非白名单发送或主动联系客户泄漏。

当前已使用并验证的 Gemini 配置记录为：

- Base URL：`https://generativelanguage.googleapis.com`
- Model：`gemini-3.6-flash`
- API Key：仅记录为存在且已脱敏，仓库不得保存明文。

### 2.4 原生管理界面

已验证候选前端和候选后端配套运行，以下页面或能力可正常打开和读取候选运行状态：

- 账号管理
- 在线聊天
- 系统设置
- AI 设置
- 关键词管理
- 自动回复日志

AI 设置界面已验证包含：

- AI 开关
- Provider
- Base URL
- API Key
- Model
- Prompt
- Test
- Save

### 2.5 Cookie 续期与登录状态

ACCOUNT-A：

- 上游原生 API 续期成功。
- 数据库 Cookie 增量写回成功。
- 更新了 5 个 Cookie 字段。
- 长登录字段恢复。
- 账号身份字段未变化。
- Cookie、Token 和身份明文未写入日志或仓库。

ACCOUNT-B：

- 接口续期和 browser-renew 没有恢复完整长登录状态。
- 不完整 Cookie 没有写回数据库。
- 当前必须由账号所有者在上游账号管理界面使用官方扫码登录，并完成可能出现的扫码、人脸或验证码验证。
- ACCOUNT-B 状态为 `OWNER_INTERACTIVE_VERIFICATION_REQUIRED`。

### 2.6 商品同步与商品身份核验

- 上游原生商品同步可用于发布前后商品数量和身份回查。
- 已验证同步商品与发布素材之间的标题、描述、价格、时间和账号归属对比流程。
- 已确认一次历史同步商品与当前发布尝试无关，因此允许进行唯一一次受控发布重试。
- 发布后同步发现一件与本次素材和时间窗口匹配的新商品。
- 新商品已归属于本次受控发布尝试。
- 已获得商品标识，但完整商品 ID 不写入治理文档和公开日志。
- 未创建重复商品。

### 2.7 商品发布链路

ACCOUNT-A 商品发布链路已完成一次真实成功验证。

已确认并修复的上游发布问题：

1. 官方 passport “快速进入” iframe 阻断发布表单，原发布器没有处理。
2. 发布页表单不渲染时原错误分类不准确。
3. 商品发布 User-Agent 与运行 Chromium 环境不一致。
4. Cookie 被重复注入。
5. 商品描述含 Emoji 时被平台客户端在请求发出前拒绝。
6. 描述自动填写需要使用 Playwright 原生操作并触发 React 安全事件。
7. 原发布错误信息过于模糊，不能区分登录、表单、客户端校验和请求阶段。

最终受控发布验证结果：

- 发布页加载成功。
- 发布表单正常渲染。
- 图片上传完成。
- 商品描述状态有效。
- 分类已选择。
- 价格有效。
- 地址已选择。
- 发货、包邮和交易方式状态有效。
- 浏览器原生表单校验通过。
- React 表单状态有效。
- 发布按钮存在、可见、启用且 trial click 通过。
- 发布请求真实发出。
- 平台响应成功。
- 发布后商品同步数量增加 1。
- 新商品可归属于本次发布尝试。
- `actual_item_created=true`。
- `item_id_present=true`。
- `duplicate_item_created=false`。
- `publish_retest=pass`。

已采用的最小修复方向：

- 处理官方 quick-enter iframe。
- 发布文本进入页面前清理平台不兼容 Emoji。
- 使用 Playwright/React-safe 方式填写商品描述。
- 对齐发布 User-Agent 与实际 Chromium。
- 去除重复 Cookie 注入。
- 保留脱敏发布诊断。
- 将客户端校验错误分类为具体 `platform_client_validation_error`，并记录脱敏阻塞字段和原因。

## 3. 测试与候选运行时

本轮商品发布最终验证记录：

- 发布相关定向测试：`12 passed`
- `python scripts/validate_change.py`：通过
- `python scripts/verify_repository.py`：`599 passed`
- 既有 Starlette/httpx warning：1 个，不是本轮引入
- 前端未修改，`frontend_build=not_required`

候选运行时：

- Compose project：`xianyu_chg0017_candidate`
- 已重建服务：`backend-web`
- `candidate_image_rebuilt=true`
- `runtime_hotpatched=false`
- `reproducible_deployment=true`
- `runtime_container_updated=true`
- `runtime_code_verified=true`
- backend-web 健康
- 已观察端口：`19000 / 28089 / 28090`

## 4. 安全与治理状态

已确认：

- 未输出 Cookie 明文。
- 未输出 Token 明文。
- 未提交 API Key。
- 未记录完整商品 ID。
- 未记录完整账号 ID。
- 未记录 Authorization 或完整请求 Header。
- 未跨账号复制 Cookie。
- 未绕过扫码、人脸、验证码或平台安全验证。
- 未向非白名单客户发送测试消息。
- 未创建第二套 Token、WebSocket、sender、AI Provider、自动回复或商品发布系统。

GitHub 治理状态：

- PR #26：`Draft / Open / Unmerged`
- 不执行 archive。
- 不执行 T17。
- 不在本次状态记录中授权 merge。

## 5. 重要代码同步说明

本文件记录的是已经在本地候选源码和可复现候选镜像中完成的真实运行验证结果。

商品发布最终修复涉及的候选源码至少包括：

- `backend-web/app/services/xianyu_publisher.py`
- `common/services/publish_execution_service.py`（此前诊断增强涉及）
- `tests/test_chg0017_publish_login_submit.py`

在 PR #26 最终合并前，必须把本地候选源码的准确最终 diff 与 GitHub 分支逐文件核对，并确保：

1. GitHub 分支包含运行时实际验证过的最终代码，而不只是本文档。
2. 定向测试、`validate_change.py`、`verify_repository.py` 和 GitHub Actions 在同一提交上通过。
3. 候选镜像可以从该 GitHub 提交可复现构建。
4. 不把本地 evidence、Cookie、Token、API Key、账号标识或测试商品敏感信息提交到仓库。

在完成上述代码对齐前，PR #26 必须继续保持 Draft，不得合并。

## 6. 尚未完成或需要继续测试的内容

- ACCOUNT-B 官方扫码登录、完整 Cookie 恢复、身份核验、数据库写回和 WebSocket 恢复。
- ACCOUNT-B 发布页只读登录状态检查。
- 默认回复真实发送验证。
- 图片回复、商品卡片、订单、退款、物流、评价等高副作用路径。
- 批量商品发布。
- 商品编辑、上下架和删除。
- 商品发布失败重试、幂等和重复保护的更多边界场景。
- 更多平台客户端校验场景，例如特殊字符、超长描述、价格边界、分类变化、地址变化和图片失败。
- 长时间运行、断网恢复、容器重启、浏览器资源释放和并发账号压力。
- 前端完整回归和不同浏览器访问验证。
- 最终代码 diff 对齐、GitHub CI、PR review、archive 和 merge。

## 7. 后续工作规则

后续测试继续遵守：

- 优先复用上游原生能力。
- 顺序为 `CONFIGURE_UPSTREAM > PATCH_CONFIRMED_UPSTREAM_DEFECT > WRAP_FOR_OPERATIONS`。
- 真实发布、订单、退款、物流、评价、消息发送和账号登录均属于有副作用操作，必须限定账号、对象和次数。
- 每次真实商品发布前先执行商品同步和重复检查。
- 任何未知发布结果不得自动重试。
- 官方验证必须由账号所有者本人完成，不自动绕过。
- 所有 evidence 必须脱敏，敏感 evidence 保持本地未提交。
- 每完成一项功能，更新本文件、acceptance evidence 和 PR #26 描述。

## 8. 当前阶段标签

```text
ACCOUNT-A_PRODUCT_PUBLISH=VERIFIED_PASS
ACCOUNT-A_WEBSOCKET=RUNNING_CONNECTED
ACCOUNT-A_AI_REPLY=VERIFIED_PASS
MULTI_ACCOUNT_RUNTIME=VERIFIED_PASS
ACCOUNT-B_LOGIN=OWNER_INTERACTIVE_VERIFICATION_REQUIRED
CANDIDATE_RUNTIME=REPRODUCIBLE
PR_26=DRAFT_OPEN_UNMERGED
T17=NOT_AUTHORIZED
NEXT=CONTINUE_FEATURE_VALIDATION
```
