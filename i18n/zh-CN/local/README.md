# Local Overlay

这个目录承载的是 **本机部署、脚本、路径对照与其他非核心覆盖层**。

它的设计目的很单纯：

- 不让本机配置污染根目录的核心概念
- 让本机修编可以集中管理
- 让整个 `local/` 在必要时可以被直接删除并重建

## Contents

- `docs/`
  - 本机部署相关说明与对照文件
- `scripts/`
  - 本机执行用脚本

## Current Files

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - 重构前保留下来的 authoring 强化版核心文档
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - 当前本机 MCP 部署与对接说明
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - 当前部署的路径参考与历史对照
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - 当前本机 workflow 对接说明
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - 本机同步脚本

## Rule

若某份内容描述的是：

- 这个系统应该如何运作
  - 它不应放在 `local/`
- 这个实例目前怎么配置
  - 它应放在 `local/`
