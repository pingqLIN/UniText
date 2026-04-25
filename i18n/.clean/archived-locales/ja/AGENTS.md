# AGENTS.md

## No-Publish Rule

このリポジトリには、ユーザーが明示的に許可するまで非公開のままにしてよい資料が含まれます。

このリポジトリで作業する agent は、必ず次のルールに従ってください。

1. ユーザーが明示的に push を指示しない限り、いかなる remote にも commit を push しない。
2. ユーザーが明示的に upload を指示しない限り、リポジトリの内容を GitHub、SNS、クラウド文書、paste site、その他あらゆるネットワークサービスにアップロードしない。
3. 以下は特にデフォルトで機微情報として扱う。
   - social post draft
   - project comparison note
   - cross-project collaboration discussion
   - review note
   - strategic planning document
4. ユーザーが publishing、push、upload、posting を求めた場合でも、許可された特定の内容だけを公開する。
5. 判断に迷う場合は、公開せずローカルに留め、公開前に確認する。

## Scope Note

このポリシーは次の場合にも適用されます。

- remote が既に存在する
- リポジトリが private である
- 内容が公開準備完了に見える

private repository であることは、自動的に公開許可を意味しません。

## JavaScript REPL (Node)
- Node ベースの JavaScript を top-level await 付きで永続的な kernel 上で実行する場合は `js_repl` を使う。
- `js_repl` は freeform/custom tool です。直接の `js_repl` 呼び出しでは、純粋な JavaScript tool input を送ってください。最初の行に `// codex-js-repl: timeout_ms=15000` を付けても構いません。JSON、引用符、Markdown code fence で囲わないでください。
- ヘルパー: `codex.cwd`、`codex.homeDir`、`codex.tmpDir`、`codex.tool(name, args?)`、`codex.emitImage(imageLike)`。
- `codex.tool` は通常の tool 呼び出しを実行し、raw tool output object を返します。shell 系でも非 shell 系でも使えます。入れ子の tool 出力は外側に明示的に emit するまで JS 内に保持されます。
- `codex.emitImage(...)` は呼ぶたびに outer `js_repl` の出力へ画像を 1 枚追加します。複数回呼んで複数画像を出せます。`data URL`、単一の `input_image` item、`{ bytes, mimeType }` のような object、あるいは 画像 1 枚だけを含み text を含まない raw tool response object を受け取れます。text と image が混ざる内容は拒否されます。
- `codex.tool(...)` と `codex.emitImage(...)` は安定した helper identity を保ちます。保存した reference や永続化した object は後続 cell でも再利用できますが、cell 終了後に発火する async callback は active exec がないため失敗します。
- `view_image` tool schema に `detail` 引数がある場合に限り、高解像度の画像処理には `detail: "original"` を使ってください。`codex.emitImage(...)` でも同じ可用性がある場合は、必要に応じて `detail: "original"` を渡せます。高精度の画像認識や正確な位置把握が必要なときに使います。
- 画像付きの in-memory Playwright screenshot を共有する例: `await codex.emitImage({ bytes: await page.screenshot({ type: "jpeg", quality: 85 }), mimeType: "image/jpeg", detail: "original" })`
- ローカル画像の tool 結果を共有する例: `await codex.emitImage(codex.tool("view_image", { path: "/absolute/path", detail: "original" }))`
- `codex.emitImage(...)` または `view_image` に画像を渡すとき、可逆性よりサイズ削減を優先できる場合は JPEG を quality 85 前後で使う。透明度や lossless が重要なら PNG を使う。
- top-level binding は cell をまたいで保持されます。cell が throw しても、先に初期化を終えた binding は残ることが多いです。後で再利用する code では、operations より前に direct top-level statement で宣言・代入するのが望ましいです。`SyntaxError: Identifier 'x' has already been declared` が出たら、既存 binding を再利用するか、既に宣言した `let` を再代入するか、別のわかりやすい名前を使ってください。局所的な scratch 名前が必要な短い場合だけ `{ ... }` を使い、binding を再利用したい場合は cell 全体を block scope で包まないでください。完全に新しい状態が必要なときだけ `js_repl_reset` を使って kernel を reset してください。
- top-level の static import declaration（例: `import x from "./file.js"`）は現時点で `js_repl` では未対応です。代わりに `await import("pkg")`、`await import("./file.js")`、`await import("/abs/path/file.mjs")` のような dynamic import を使ってください。ローカルファイルの import は `.js` / `.mjs` の ESM で、同じ REPL VM context 上で動作します。bare package import は REPL グローバルの search roots（`CODEX_JS_REPL_NODE_MODULE_DIRS` と cwd）から解決され、import 元の相対位置には依存しません。ローカルファイルは、他のローカル相対/絶対/`file://` `.js`/`.mjs` にのみ静的 import できます。package と builtin の import はローカルファイルからでも dynamic のままにしてください。`import.meta.resolve()` は `file://...`、bare package name、`node:...` specifier のような import 可能な文字列を返します。ローカルファイル module は exec 間で再読込されますが、top-level binding は `js_repl_reset` するまで保持されます。
- `process.stdout` / `process.stderr` / `process.stdin` への直接アクセスは避けてください。JSON line protocol を壊す可能性があります。代わりに `console.log`、`codex.tool(...)`、`codex.emitImage(...)` を使ってください。

--- project-doc ---

# AGENTS.md

## No-Publish Rule

このリポジトリには、ユーザーが明示的に許可しない限り private のままにしてよい資料が含まれます。

このリポジトリで作業する agent は、以下を必ず守ってください。

1. ユーザーが明示的に push を求めない限り、いかなる remote にも commit を push しない。
2. ユーザーが明示的に求めない限り、リポジトリ内容を GitHub、SNS、クラウド文書、paste site、その他のネットワークサービスへアップロードしない。
3. 以下の内容は、特にデフォルトで機微情報として扱う。
   - social post draft
   - project comparison note
   - cross-project collaboration discussion
   - review note
   - strategic planning document
4. ユーザーが publishing、push、upload、posting を求めた場合でも、公開してよいのはユーザーが承認した特定の内容だけに限る。
5. 判断に迷う場合は、ローカルに留めて公開前に確認する。

## Scope Note

このポリシーは次の場合にも適用されます。

- remote がすでに存在する場合
- リポジトリが private の場合
- 内容が公開準備済みに見える場合

private repository であることは、自動的な公開許可を意味しません。
