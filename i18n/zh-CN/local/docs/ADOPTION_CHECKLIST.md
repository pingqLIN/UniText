# Adoption Review Checklist

> 状态：Active
> 用途：定义 adoption flow 中 `REVIEW` 步骤的最小检查标准。

## Required

- [ ] 目录名称符合 `id` 规则
- [ ] `SKILL.md` 存在
- [ ] `SKILL.md` 以 frontmatter 开头
- [ ] frontmatter 至少包含 `name` 与 `description`
- [ ] `canonical_location` 可合理对应到 `/registry/{type}/{id}`
- [ ] 无明显损坏、空白或截断内容

## Recommended

- [ ] 有 `LICENSE.txt` 或等价授权说明
- [ ] 有清楚的 Usage、Workflow 或 Process 段落
- [ ] 无硬编码的个人帐号与本机绝对路径
- [ ] 若含 scripts / references，路径关系清楚且可被 agent 发现

## Review Outcome

- `approve`
  - 可直接进入 `DRY-RUN`
- `needs-fix`
  - 需先补 metadata 或清理内容
- `hold`
  - 有 canonical source 争议或内容品质问题，不可进入 `ADOPT`
