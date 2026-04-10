[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> 状態：Active Baseline
> 用途：shared surfaces 上の workspace-sensitive metadata を検出するルール、その保守方法、そして検証境界を定義する。

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` は authoring repo と exported starter package が共有するルールソースであり、次の drift を減らすために使われます。

- shared docs にローカルの絶対パスが混入する
- shared scripts に live workspace hostname が混入する
- shared governance files に live redirect URI や Cloudflare IDs が混入する
- boundary verify と template verify が異なるルールセットを使ってしまう

この文書が答えるのは次の点です。

- ルールファイルの各セクションが何を意味するか
- いつ新しいルールを追加すべきか
- sanitized placeholder まで live metadata と誤検知しないためにどうするか
- ルール調整後にどの検証を走らせるべきか

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` には現在 4 つのトップレベル区分があります。

- `shared_surface_scope`
  - repo-side boundary verify が既定で走査する tracked shared surfaces を定義する
- `path_rules`
  - tracked path 自体が shared surface に現れてはいけない条件を定義する
- `content_patterns`
  - どの文字列内容を workspace-sensitive metadata と見なすかを定義する
- `self_test_cases`
  - regex の変更後に静かな回帰が起きないよう、正負の自動ケースを定義する

## 3. Maintenance Rules

- 新しい shared governance doc または shared control script を追加し、それが repo-side boundary review の対象なら、`shared_surface_scope` にも追加する
- 新しい live metadata 類型を追加する場合は、まず `content_patterns`、次に対応する `self_test_cases` を追加する
- ある placeholder を安全な例として扱うなら、`expected_labels = []` の self-test case を必ず追加する
- ある regex が script 内のルール文字列として出現するだけなら、`skip_script_pattern_lines` を明示する
- 誤検知を解消するために authoring-only や operations-only の path を `shared_surface_scope` に入れてはいけない。先に文書配置が誤っていないか確認する

## 4. Required Validation

`WORKSPACE_SENSITIVE_METADATA_RULES.json` を調整したら、少なくとも次を再実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

今回の変更が starter baseline に影響する場合は、さらに次も実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

このルール群の目的は次の通りです。

- shared surface 上で安定して保守でき、検証可能な heuristic controls を提供する

これは次のものではありません。

- あらゆる secret 類型に対する完全な schema validator
- すべての infrastructure provider を対象にした汎用 DLP システム
- local-only / ops-only 領域を全面スキャンするツール

将来 metadata 類型が増え続けるなら、次にやるべきことはルールソースとケースの拡張であって、live references を shared registry に戻すことではありません。
