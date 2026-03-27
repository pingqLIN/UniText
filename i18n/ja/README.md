[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](../zh-CN/README.md) | [日本語](README.md) | [Deutsch](../de/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [한국어](../ko/README.md) | [Italiano](../it/README.md)

# UniText

> **複数の AI CLI 向けの text-native、registry-first な shared resource hub。**
>
> 純文本を共有インターフェースとして、Claude Code、Codex、Gemini CLI などのツールが同じ資源定義を共有できるようにします。

## 2026-03-27 同期注記

この翻訳で優先して読むべき current baseline は次の通りです。

- support labels は `verified` / `partial` / `target`
- `Copilot CLI` は `target` / `adapter pending`
- material sets は `authoring review shortlist` / `public release subset` / `local-only validation materials`

この翻訳と英語主文書の間に差分がある場合は、[English README](../../README.md) を authoritative version として扱ってください。

---

## なぜこれが必要か

複数の AI CLI ツールを使うと、資源はすぐに散らばります。

- 同じ skill が 3 か所に、それぞれ少しずつ違う状態で定義される
- 他のツールでは読めない形式の MCP server config がある
- ある CLI しか知らない agent instructions がある
- どのコピーが canonical なのか判別できない

UniText は、単一の shared registry と治理された delivery layer でこれを解決します。**1 つの定義。すべてのツール。**

---

## 仕組み

```
UniText/
├── registry/          ← canonical definitions（何が存在するか）
│   ├── skills/        ← 共有 skill 定義
│   ├── mcp/           ← MCP server 定義
│   ├── agents/        ← agent instructions と persona
│   └── workflow/      ← runbook、plan、慣例
│
├── local/             ← deployment overlay（この環境でどう配線されているか）
│   ├── docs/          ← path map、deployment notes
│   └── scripts/       ← このマシン用の sync scripts
│
└── ops/               ← operations state（shared resources ではない）
    └── history/       ← タイムスタンプ付き audit trail
```

`registry/` 層は platform-agnostic です。OS 固有の absolute path ではなく、論理 canonical path（`/registry/skills`、`/registry/mcp`）を使います。`local/` 層がそれらを実際のマシン上の場所に解決します。

---

## アーキテクチャ

**Registry-first, adapter-enabled, operations-governed.**

| Layer | Role |
|-------|------|
| **Registry** | 共有資源が何か、その canonical identity は何かを定義する |
| **Adapter** | registry 内容を各 CLI に届ける（mirror、symlink、native-config、pointer） |
| **Operations** | 変更をいつ、どう行うかを管理する。backup、dry-run、audit trail 付き |

### Resource Types

| Type | Logical Root | What Goes Here |
|------|-------------|----------------|
| `skills` | `/registry/skills` | AI agent が使う共有 skill 定義 |
| `mcp` | `/registry/mcp` | cross-CLI の MCP server 定義 |
| `agents` | `/registry/agents` | agent instructions、persona、system prompts |
| `workflow` | `/registry/workflow` | runbook、planning templates、慣例 |

### Delivery Modes

各 resource は、CLI の能力に応じて異なる方法で届けられます。

- `pointer` — discovery のみで、内容はコピーしない
- `mirror` — robocopy / rsync によるローカルコピー
- `symlink` — canonical source への固定パスリンク
- `native-config` — CLI 自身の設定形式で登録する

---

## はじめ方

### 1. このリポジトリを fork するか clone する

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. 最初の resource を追加する

`registry/skills/` に skill を作成します。

```
registry/skills/my-skill/
└── SKILL.md
```

最小構成の `SKILL.md`：

```yaml
---
name: my-skill
description: What this skill does in one line
---

## Usage

Instructions for the AI agent...
```

### 3. カタログに登録する

`INDEX.md` に entry を追加します。

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. ローカル CLI wiring を bootstrap する

クロスプラットフォームの bootstrap path を優先してください。

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` は共有 skills target を揃え、Codex の `skills_path` を更新し、bundled MCP baseline 用の project-local `.mcp.json` を書き込みます。`sync-skills.ps1` は、Windows PowerShell の参照実装として引き続き利用できます。

---

## サポートされる CLI

この repository では 3 種類の support label を使います。

- `verified`
  - 記載された範囲に対して、repo 内に再現可能な証拠がある
- `partial`
  - 一部の検証はあるが、repo はまだ full end-to-end coverage を主張していない
- `target`
  - 目標面として定義されているだけで、この repo ではまだ検証されていない

| CLI | Support Class | Verification Scope | Notes |
|-----|---------------|--------------------|-------|
| **Claude Code** | `verified` | `delivery path verified` | `.claude/settings.json`、project-local `.mcp.json`、shared skills の delivery path は maintained baseline に含まれるが、まだ end-to-end task verification を主張していない |
| **Gemini CLI** | `verified` | `delivery path verified` | shared skills の delivery path は maintained baseline に含まれるが、end-to-end interaction は現時点で主張していない |
| **Codex** | `partial` | `bootstrap path defined` | native config wiring は `bootstrap.py` と `config.toml` で実装されているが、fresh machine で完全に再現可能な end-to-end bootstrap verification はまだ主張していない |
| **Copilot CLI** | `target` | `adapter pending` | stable な repo-level adapter path が定義された後に、shared MCP / skill baseline を消費する想定 |

[template/examples/local/README.md](../../template/examples/local/README.md) と `template/examples/local/docs/PATH_MAP.template.md` を参照してください。
[local/docs/SUPPORT_PROOF_MATRIX.md](../../local/docs/SUPPORT_PROOF_MATRIX.md) は support claim と proof artifact の対応表です。

authoring workspace をそのまま使うのではなく、clean な starter project に再構成したい場合は [REBUILD_AS_NEW_PROJECT.md](../../REBUILD_AS_NEW_PROJECT.md) を参照してください。

### Cross-Platform Baseline

GitHub-hosted の starter template は、現在 verified と言える範囲より広い target surface を持ちます。

| Platform | Support Class | Verification Scope | Notes |
|----------|---------------|--------------------|-------|
| `Windows` | `verified` | `authoring + export baseline verified` | 現在の scripts、review export flow、template export flow は Windows 上で維持・再検証されている |
| `macOS` | `target` | `template target` | Python ベースの `bootstrap -> verify` path は portable に設計されているが、この repo はまだ反復的な macOS evidence を主張していない |
| `Linux` | `target` | `template target` | Python ベースの `bootstrap -> verify` path は portable に設計されているが、この repo はまだ反復的な Linux evidence を主張していない |

tracked `.mcp.json` は fresh clone 向けの relative-path seed です。サポートされる first-run path は引き続き次の通りです。

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

この README にある platform は、明示的にそう書かれていない限り `end-to-end verified` と読んではいけません。

### Current Material Sets

UniText は現在、3 つの material set を区別しています。

- `authoring review shortlist`
  - maintainer が candidate skills を review / compare するための working set
- `public release subset`
  - exported review package に含められる GitHub-backed かつ publicly redistributable な subset
- `local-only validation materials`
  - maintainer local で dry-run validation に使われることはあるが、public release surface には入らない素材

これらが一致しない場合、release truth は authoring workspace ではなく exported package です。

---

## Governance Rules

UniText は **no silent changes** ポリシーを適用します。

1. **Explicit triggers only** — `bootstrap`、`sync`、`adopt`、`repair`
2. **Backup before any mutation** — 破壊的操作はすべて timestamp 付き snapshot を `ops/` に作成する
3. **Dry-run before delivery** — 変更前に何が変わるかをプレビューする
4. **Conflict stops the flow** — 同じ resource の 2 つの version が異なるなら、人のレビューのために停止する
5. **Full audit trail** — すべての operation を `ops/history/` に記録する

正式な adoption flow は次の通りです。`SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentation

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | discovery の入口。どの資源が存在し、どこにあるかを示す |
| [VISION.md](VISION.md) | architecture principles と design rationale |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | すべての shared resources の metadata contract |
| [OPERATIONS.md](OPERATIONS.md) | delivery modes、triggers、安全ルール |
| [PROJECT_MODES.md](PROJECT_MODES.md) | authoring repo と project template の区別 |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | secret の保存、redaction、password / API key の扱い境界 |
| [MILESTONES.md](MILESTONES.md) | 定量化された phase goals と external-review readiness checkpoints |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | 現在の review wave のための `8 + 4` 精選 skills 集 |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | reviewer-facing な scope、reading order、repeatable package export flow |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | 外部審査者向けの submission note |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | 素早く把握するための short-form review summary |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | template release cleanup の scope、除外項目、export flow |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | starter package 用の pre-release cleanup checklist |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | UniText が skill-0 と decomposition / primitive-extraction project としてどう協業できるかの概念メモ |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | agent と collaborator 向けの local-first publishing boundary |

読書順：`EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## 2つの使い方

### スターター template として使う

この repo を fork してください。`ops/history/`、`backup/`、このマシン固有の `local/` パスを削除します。`registry/` に独自の skills と MCP definitions を入れ、`local/scripts/` を自分の環境に合わせて接続します。

### Reference implementation として使う

コア文書を読んで architecture を理解します。registry 構造、resource spec、delivery modes、operations audit trail といった pattern を自分の環境に適用してください。

---

## Design Principles

- **Registry first** — まず定義し、その後で届ける
- **Discovery before automation** — 同期する前に、何が存在するかを把握する
- **Platform-agnostic contracts** — spec では論理 path を使い、絶対 path は local overlay にのみ置く
- **Minimum viable metadata** — `id`、`type`、`canonical_location`、`status` があれば開始できる
- **Safe mutation** — dry-run + backup + explicit trigger を常に行う
- **AI as consumer** — model は registry を読み、動作する。delivery guarantee の所有者ではない

---

## Status

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active — `skills/`、`mcp/`、`workflow/`、`agents/` roots が存在 |
| Skills registry | Active baseline — first canonical batch は adoption 済み、より広い adoption は進行中 |
| Agents registry | Active seed — `registry-curator` entry が作成済み |
| MCP registry | Active baseline — canonical definition と runnable read-only server が存在 |
| Workflow registry | Draft seed — workflow doc と plan template が存在 |
| Operations audit trail | Active |
| Sync, bootstrap, and review scripts | `local/scripts/` で active baseline |
| External review package | Active baseline — reviewer guide と export script が存在 |
| Template release cleanup | Release candidate — template package guide、checklist、export + verify scripts、generic examples、local overlay skeleton が存在 |

---

## License

MIT

---

*複数の AI tool を使い、単一の source of truth を求める人向け。*

