# UniText — Template Release Checklist

> 用途：template package を出力または発行する前に、最小限の cleanup が終わっているかを素早く確認する。

## 1. Docs

- [ ] `README.md` は作者個人の背景に依存せず理解できる
- [ ] `INDEX.md` は discovery の入口として使える
- [ ] `PROJECT_MODES.md` が template と authoring workspace を明確に区別している
- [ ] `SECRET_HANDLING_GUIDELINES.md` が secret の境界を定義し、実 credential を含んでいない
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` が更新されている
- [ ] `MILESTONES.md` が現在の phase 状態を反映している

## 2. Cleanup Boundaries

- [ ] template package に `backup/` が含まれない
- [ ] template package に `recovered_*` が含まれない
- [ ] template package に `.bak_*` が含まれない
- [ ] template package に `ops/history/` が含まれない
- [ ] template package に review-only docs が含まれない
- [ ] template package に machine-specific absolute path が含まれない

## 3. Examples

- [ ] generic skill example が少なくとも 1 つある
- [ ] generic agent example が少なくとも 1 つある
- [ ] generic mcp example が少なくとも 1 つある
- [ ] generic workflow example が少なくとも 1 つある
- [ ] generic local overlay skeleton が少なくとも 1 つある
- [ ] starter package に cross-platform `bootstrap -> verify` path がある

## 4. Validation

- [ ] `health-check.ps1` が通る
- [ ] `export-template-package.ps1 -DryRun` で package 内容を列挙できる
- [ ] `export-template-package.ps1` で package を正常に生成できる
- [ ] `verify-template-package.ps1` が通る
- [ ] `bootstrap.py --dry-run` で clean environment における initialization 内容を事前確認できる
- [ ] `verify-bootstrap.py` で first-run wiring を検証できる
- [ ] package に `manifest.json` が含まれる
- [ ] package に `release.json` が含まれる

## 5. Release Call

以上をすべて満たしたら、次のように見なせます。

**template release candidate として扱うのに適している**

local-only の境界が不明瞭、examples が不十分、CLI 検証が足りない場合は、次のまま扱うべきです。

**template release cleanup baseline**
