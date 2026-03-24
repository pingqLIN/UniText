# UniText — Secret Handling Guidelines

> 状態：Draft  
> 役割：password、API key、token、credential などの sensitive material を UniText でどこまで扱うか、その境界、操作原則、文書化方法を定義する。

## 1. Purpose

この文書が答えるのは次の問いです。

- 何が secret に当たるか
- secret をどこに置くべきではないか
- UniText では「場所」と「状態」をどう記録すべきか
- いつ CLI config に置けるか、いつ OS secret store や native helper に切り替えるべきか

この文書は単一製品の最終実装を提供するものではありません。UniText が従うべき治理境界を定義するものです。

## 2. Secret Definition

次の内容はすべて `secret` または `sensitive material` と見なします。

- password
- passphrase
- API key
- access token
- refresh token
- session token
- private key
- OAuth client secret
- cookie / session credential
- ユーザーまたはシステムの身元を直接表せる bearer credential

次の内容は通常 secret ではありませんが、sensitive metadata になり得ます。

- endpoint URL
- model name
- provider name
- account email
- feature toggle state
- key exists / missing 状態
- key の最終更新時刻

## 3. Core Principle

UniText の基本原則は次の通りです。

1. `registry/` に secret を置かない
2. `ops/` に再生可能な secret を記録しない
3. `local/` には path / adapter / deployment notes のみを記録し、明文 secret は置かない
4. 真の secret はまず OS-level secret store に置く
5. すぐに OS secret store を使えない場合でも、secret と一般設定は分離する

要するに：

- `registry` は shared truth であり、secret vault ではない
- `ops` は audit trail であり、credential archive ではない
- `local` は wiring overlay であり、plaintext stash ではない

## 4. Storage Policy by Layer

| Layer | Can store secret? | Guidance |
|---|---|---|
| `registry/` | No | canonical definition、schema、adapter hints、resource metadata のみを保存する |
| `ops/` | No | redacted logs、backup metadata、drift report、inventory state のみを保存する |
| `local/` docs | No | secret location の種類は記録してよいが、secret 自体は記録しない |
| CLI config | Conditional | 該当 CLI が config-based secret のみを正式に扱い、リスクが許容できる場合のみ |
| OS secret store | Yes | 優先。例：Windows DPAPI / Credential Manager、macOS Keychain、Linux Secret Service |
| in-memory session | Yes | 短期的な runtime material としては可。ただし唯一の永続化先にしてはいけない |

## 5. Approved Patterns

### 5.1 Best Pattern

商用拡張、デスクトップツール、クロス CLI adapter に適した構成です。

- 非敏感設定は通常の config / storage に置く
- secret は OS secret store に置く
- runtime 起動時に process memory へ注入する
- UI では `stored / missing / last updated` のみを表示し、明文は再表示しない

### 5.2 Acceptable Fallback

当面 OS secret store を使えない場合：

- provider / account ごとに secret を分ける
- secret と一般設定を分離する
- content script / renderer / untrusted context から直接読めないようにする
- audit と export は redacted state のみを表示する
- 文書中で `interim storage model` と明示する

### 5.3 Not Acceptable

次の方法は UniText では不適格と見なします。

- API key を `registry/` に書く
- token を `ops/history/` に書く
- deployment note に完全な key 例を貼る
- secret と一般設定を混ぜて保存し、redaction しない
- review package / template package の export に real key を含める

## 6. Location Recording Rules

文書では「secret がどの層にあるか」は記録してよいですが、secret 値そのものは記録してはいけません。

記録してよい例：

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- `%USERPROFILE%\\.codex\\config.toml` の non-secret settings
- `chrome.storage.local` を non-secret provider settings にのみ使う
- `chrome.storage.session` を短寿命の runtime material に使う

記録してはいけない例：

- 完全な token
- 完全な API key
- 完全な Authorization header
- 直接再生可能な cookie 値

## 7. Documentation Rules

secret handling を文書に書く場合は次を守ってください。

1. storage class のみを記録し、実際の値は記録しない
2. 例は必ず redacted にする
3. やむを得ず例を出す場合は、次のような明確な偽値を使う

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. ある system が現時点で弱いモードしか使えないなら、文書に必ず次を明示する
   - これは暫定方案である
   - 既知の risk は何か
   - 目標の upgrade path は何か

## 8. Audit and Export Rules

review package、template package、inventory export、ops snapshot はすべて次を満たす必要があります。

- secret value を削除する
- 再生可能な credential を削除する
- 必要な redacted state は残す

残してよいもの：

- provider name
- endpoint
- key exists / missing
- key scope または label
- last rotated at
- storage backend type

## 9. Recommendation Ladder

UniText の secret storage 推奨順は次の通りです。

1. `OS secret store`
   - Windows: DPAPI / Credential Manager
   - macOS: Keychain
   - Linux: Secret Service / keyring
2. `native helper / native messaging host`
   - CLI や extension が secret を安全に持続化できない場合
3. `separated local secret store`
   - 一般設定と分離し、untrusted context から直接読めないようにする
4. `runtime session only`
   - 補助としては可。ただし唯一の長期持続化戦略にしてはいけない

## 10. Minimum Checklist

UniText に secret を扱う resource や adapter を追加する前に、少なくとも次を確認してください。

- secret が `registry/` から除外されているか
- secret が `ops/` から除外されているか
- 文書が location / state のみを記録し、value を含まないか
- export / review package に redaction があるか
- 現在の storage backend が記録されているか
- upgrade path が記録されているか

## 11. Practical Guidance for Browser Extensions

browser extension のような場面では、次のように考えます。

- provider settings は extension local storage に置ける
- API key は一般 provider settings と 1 つの共有値として混在させるべきではない
- provider ごとに secret を個別に持つ
- UI は staged draft をサポートし、provider 切り替えや hover / collapse で key を失わないようにする
- より高い security を目指すなら、extension storage だけに頼らず native host + OS secret store に切り替える

## 12. Current UniText Position

現時点での UniText の secret handling に関する正式立場は次の通りです。

- canonical registry は secret を保持しない
- local overlay は secret backend と path type を記録してよい
- operations artifacts は redacted でなければならない
- ある integration がまだ OS secret store につながっていない場合、文書で interim model だと明示する

この文書は次の基準として扱うべきです。

- authoring guidance
- review checklist reference
- 将来の adapter / secret-store integration の baseline
