# UniText — Template Release Package

> 状態：Active Baseline  
> 用途：template release cleanup の目的、範囲、再生成可能な export flow を定義する。

## 1. Purpose

`UniText` の template release は、作者 workspace をそのまま梱包して出すものではありません。次の条件を満たす一式を出力するべきです。

- core architecture と spec を保持する
- 最小限の利用可能な examples を保持する
- local-only state を除外する
- 履歴的な治理残留物を除外する
- 他の利用者が fork / clone して自分で拡張しやすい

この package の位置づけは次の通りです。

**starter template**

そして次ではありません。

**authoring workspace snapshot**

## 2. Include

現在、template package に含めるべきものは次の通りです。

- コア文書
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- release metadata
  - `manifest.json`
  - `release.json`

## 3. Exclude

template package に含めるべきではないものは次の通りです。

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- 実際の user account、home directory、absolute path
- review-specific docs
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Export Command

repo root で次を実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

既定の出力先：

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

書き込みせず内容だけ確認したい場合は次を使います。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

出力した package を検証する場合は次を使います。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

新しい使用者の first-run では、次の path を推奨します。

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Export Interpretation

export された template package が表すのは次の通りです。

- UniText の core contract
- きれいな starter layout
- 最小限の generic examples セット

それが表さないのは次の通りです。

- 作者の現在の完全な作業状態
- すべての adoption 済み skills
- すべての review / audit 証拠
- 既に完了した local delivery wiring

## 6. Current Interpretation

2026-03-24 時点で `UniText` は次を備えています。

- 外部審査 package
- reviewer-facing entry docs
- template release cleanup baseline
- template package を再生成する export script
- starter local overlay skeleton
- template package verification script
- release metadata
- cross-platform first-run scripts
- portable bundle backup flow

したがって、現在の最も適切な判読は次の通りです。

**template release candidate**

それよりも次のように呼ぶのは適切ではありません。

**authoring workspace snapshot**

