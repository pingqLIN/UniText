# UniText — Operations

> 状態：Template Base
> 役割：adapter / operations control plane の責務、delivery 規則、安全境界を定義する。

すべての delivery と mutation は、`UniText` の純文本 registry / spec 契約を source of truth として扱うべきです。

操作が password、API key、token、credential などの sensitive material に触れる場合は、`SECRET_HANDLING_GUIDELINES.md` も同時に遵守してください。

## 1. Scope

この文書が扱うのは次の項目です。

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- drift / repair
- logical-to-physical mapping

この文書が扱わないのは次の項目です。

- shared resource metadata schema
- 単一 platform の唯一実装方式
- 本機 authoring repo の履歴状態

## 2. Delivery Modes

| Mode | When to use |
|---|---|
| `pointer` | discovery または非機械登録型の資源 |
| `mirror` | CLI がローカル副本を必要とする、または symlink が不安定な場合 |
| `symlink` | CLI が固定パスを必要とし、環境が安定した link をサポートする場合 |
| `native-config` | CLI に資源を登録する正式な設定入口がある場合 |

`delivery mode` は資源の固定属性ではなく、操作時に adapter が解釈します。

## 3. Delivery Resolution Rules

adapter は次の優先順位で判断すべきです。

1. 正式な設定入口があるなら、まず `native-config`
2. 固定パスが必要で platform が安定した link をサポートするなら `symlink`
3. symlink を安全に使えないなら `mirror`
4. 主用途が discovery または入口であれば `pointer`

## 4. Delivery Triggers

delivery は明示的な trigger でのみ開始できます。

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Safety Rules

### Dry-Run First

次の操作は dry-run plan を先に出すべきです。

- `adopt`
- `repair`
- 既存状態を上書きする `sync`

### Backup Before Mutation

すべての破壊的操作には次が必要です。

- backup または同等の復元点
- 追跡可能な操作記録
- 失敗時の停止条件

### No Silent Canonicalization

同名異内容の資源が見つかった場合。

- review で止める
- operator が canonical source を明示的に決定する

## 6. Adoption Flow

1. `SCAN`
   - 候補 source を走査し、adopt 可能な資源と readiness 状態を列挙する
2. `REVIEW`
   - review checklist に従い、metadata、内容品質、canonical source の妥当性を確認する
3. `DRY-RUN`
   - adopt または delivery がどの target をどう変更するか、backup が必要かを事前に確認する
4. `ADOPT`
   - source 内容を registry の canonical location に書き込む。既存内容を上書きする場合は先に backup を取る
5. `DELIVER`
   - adapter が registry 内容を対応する CLI に届ける。既存状態を上書きする場合は log と backup を保持する
   - CLI が `native-config` をサポートするなら、`bootstrap` 段階で machine-local config に書き込めるが、canonical definition は常に `registry/` に残す
6. `VERIFY`
   - ファイル存在、path 解決、delivery mode、target CLI の読み込み条件を検証する

## 6.1 First-Run Baseline

新規 template 使用者が macOS / Linux / Windows で最小初期化を完了できるようにするには、少なくとも次を提供すべきです。

- cross-platform `bootstrap`
- cross-platform `verify`
- 持ち運び可能な repo backup 流れ
- 実際に動く最小 MCP baseline

## 7. Operations State

次の内容は shared resources ではなく operations state です。

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

これらは `/operations` に置くべきであり、`/registry` に混ぜるべきではありません。

## 8. Logical-to-Physical Mapping

論理 path は安定した契約であり、物理 path は deployment-specific mapping です。

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | canonical skill sources | shared directory、repo subdir、mounted path |
| `/registry/mcp` | canonical MCP definitions | config folder、generated manifest root |
| `/registry/agents` | canonical agent instruction roots | agent profiles directory、shared prompt library |
| `/registry/workflow` | workflow docs / runbooks | workflow folder、project-local docs |
| `/operations` | inventories、backups、drift logs | ops folder、state store、audit directory |
