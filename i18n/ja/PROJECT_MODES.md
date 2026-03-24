# UniText — Project Modes

> 状態：Template Base
> 目的：authoring repo と対外提供される starter/template を区別する。

## 1. Two Modes

### Local Development Project

作者自身が継続的に開発、納管、修復、治理するためのモードです。

含めてよいもの：

- inventories
- backups
- drift logs
- migration artifacts
- platform-specific notes

### Project Template

他の人が自分の `UniText` 実例を初期化するために提供するモードです。

含めるべきもの：

- 論理契約
- コア文書
- 最小サンプル
- platform-independent ルール

含めるべきでないもの：

- 本機 absolute path
- 個人利用の痕跡
- backup snapshot
- drift history
- 単一 deployment の既定値

## 2. Rule Of Thumb

ある内容が次のどちらを説明しているかで判断します。

- `UniText がどう動くべきか`
  - それは `Project Template` に入れるのが適しています
- `ある作者 workspace が今どう設定されているか`
  - それは `Local Development Project` に残すのが適しています

## 3. Publishing Rule

template を発行するときは次の手順を踏みます。

1. コア文書と template-safe examples を残す
2. local-only state artifacts を削除する
3. 本機 path / account / machine-specific 値を削除する
4. reference implementation を抽象的な examples に書き換える
