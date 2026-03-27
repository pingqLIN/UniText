# UniText — Project Modes

> 状态：Template Base
> 目的：区分 authoring repo 与对外提供的 starter/template。

## 1. Two Modes

### Local Development Project

用于作者本人持续开发、纳管、修复与治理。

可包含：

- inventories
- backups
- drift logs
- migration artifacts
- platform-specific notes

### Project Template

用于提供其他人初始化自己的 `UniText` 实例。

应包含：

- 逻辑契约
- 核心文档
- 最小范例
- 平台无关规则

不应包含：

- 本机绝对路径
- 个人使用痕迹
- 备份快照
- drift history
- 单一部署预设值

## 2. Rule Of Thumb

如果某份内容是在描述：

- `UniText 应该如何运作`
  - 它更适合进入 `Project Template`
- `某个作者工作区目前怎么配置`
  - 它更适合留在 `Local Development Project`

## 3. Publishing Rule

当要发布模板时：

1. 保留核心文档与 template-safe examples
2. 移除 local-only state artifacts
3. 移除本机 path / account / machine-specific values
4. 将 reference implementation 改写为抽象 examples
