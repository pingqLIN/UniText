# UniText — Secret Handling Guidelines

> 状态：Active
> 用途：定义 password、API key、token、credential 与其他敏感资料的处理边界。

## 1. Core Principle

任何 secret 都不应出现在会被当成模板、样板、review package 或对外分享内容的一般性文件中。

## 2. What Counts as Secret

以下内容一律视为 secret 或敏感 material：

- password
- API key
- token
- session cookie
- private key
- bearer token
- 任何可直接用来验证身分或授权存取的值

## 3. Storage Rules

- 真实 secret 应只保留在使用者本机或受控密钥系统中
- 文件中若需要示意，只能使用 placeholder
- placeholder 应明确标示为 mock / example / redacted
- 不得在 repository 中留下可直接使用的真实 credential

## 4. Documentation Rules

说明文件可以描述：

- secret 应存放在哪类位置
- 哪些工具负责读取 secret
- 如何在 local 环境中载入 secret
- 如何进行 redaction 与轮替

说明文件不应包含：

- 真实值
- 可直接重放的 token
- 个人帐号密码
- 对外可用的 API key

## 5. Template Boundary

若 `UniText` 输出 starter template，则：

- `SECRET_HANDLING_GUIDELINES.md` 可以保留
- 所有真实 secret 必须移除
- 范例必须使用 placeholder
- 所有 path 与 account 资讯必须去识别化

## 6. Review Boundary

若内容被纳入 external review package：

- 只能展示治理逻辑与边界
- 不可包含实际 secret 值
- 不可因为「只是 review」就保留敏感资料

## 7. Operational Checklist

在提交、push、export 或分享前，请先确认：

1. 是否含有真实 credential
2. 是否有 placeholder 未标明
3. 是否有机密片段残留在 log、snapshot 或 example
4. 是否需要 redaction
5. 是否需要从 package 中排除该档案
