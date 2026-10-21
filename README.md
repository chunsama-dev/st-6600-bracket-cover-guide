# ST-6600 ブラケットカバー交換ガイド（V2・日英2言語）

著者・写真・整備記録：**chunsama**

GitHub Pages向けの静的な技術記事です。日本語版と英語版があり、HTML / CSS / JavaScriptのみで動作します。npmやビルドは不要です。

| 言語 | ファイル | 公開パスの例（プロジェクトサイト） |
|---|---|---|
| 日本語 | `index.html` | `/st-6600-bracket-cover-guide/` |
| English | `en/index.html` | `/st-6600-bracket-cover-guide/en/` |

両ページのヘッダーに「日本語 | English」の切替があります。通常のリンクなのでJavaScript無効でも動作し、ブラウザ言語による自動リダイレクトはしません。

## V2の変更点

- **技術訂正**：ST-6600のカバー交換で、シフトワイヤーの取り外しは不要だった（所有者の実作業による一次情報）。シフトワイヤー脱着を交換手順から外し、試行錯誤中に行ったシフトインナー2本の交換は「08 追加整備」へ移動。
- カバー交換に関連して脱着・交換したもの（バーテープ、前後ブレーキインナー）を明記。部品表を「カバー交換に必要／今回の作業方法で交換・使用／追加整備」に区分。
- 英語版 `en/index.html` を追加（全文対応。H1：Shimano Ultegra ST-6600 Hood Replacement Guide）。
- 言語切替UI、`hreflang`、言語別のtitle・description・OGP・Article（`inLanguage`）を実装。
- `tools/configure-site.py` を日英両ページ・多言語サイトマップに対応。
- 画像は前工程の加工済みファイルをそのまま共用（再加工なし）。

詳細は `AUDIT.md` を参照してください。

## まず表示する

`en/` や `../` へのリンクはGitHub Pagesでのきれいな公開URLに合わせています。ローカルで確認する場合は、ファイルを直接開くより簡易サーバーを使うと公開時と同じ動作になります。

```sh
# このフォルダの1つ上の階層で実行し、
python3 -m http.server 8000
# ブラウザで http://localhost:8000/st-6600-bracket-cover-guide/ を開く
```

`index.html` を直接開いても本文・画像は表示されますが、言語切替リンクはブラウザによってフォルダ一覧を表示します（公開時は問題ありません）。

## GitHub Pagesで公開する

1. `st-6600-bracket-cover-guide` というリポジトリを用意します。
2. ZIPの**中身**をリポジトリのルートへ追加します。`index.html` と `en/` がリポジトリ直下に来るようにしてください。元写真・未加工の写真は追加しません。
3. リポジトリの **Settings → Pages** を開きます。
4. **Build and deployment → Source → Deploy from a branch** を選びます。
5. ブランチを `main`、フォルダを `/ (root)` にして保存します。
6. Pages画面で実際の公開URLを確認します。
7. 下記のURL設定を行い、変更されたファイルをコミットします。
8. 公開ページで両言語の表示、画像、目次、写真拡大、言語切替を確認します。

著者表記はchunsamaで統一しています。ただし、GitHubの所有者名、コミット履歴、公開URL（`ユーザー名.github.io`）などサービス側の表示は別です。HTML上の著者名だけで匿名性が保証されるわけではありません。

## 公開URLの設定（SEO用）

納品時点で公開URLは未確定のため、架空のURLは埋め込んでいません。未設定の状態でも、`hreflang` は相対URLで日英を相互参照しています。

Python 3が使える環境で、このフォルダから次を実行してください。URLには**Pages画面で確認した日本語版（サイトルート）の実際のURL**を入力します。

```sh
python3 tools/configure-site.py --url 'ここを実際のHTTPS公開URLに置換'
```

プロジェクト名のサブディレクトリを含め、`index.html` は付けません。末尾の `/` は自動補完されます。英語版のURLは `<指定URL>en/` として自動設定されます。何度実行しても重複しません。

更新されるファイル：

- `index.html` / `en/index.html`：言語別canonical、絶対URLの `hreflang`（ja / en / x-default）、og:url、og:image、ArticleのURL・画像・翻訳関係（`workTranslation` / `translationOfWork`）
- `sitemap.xml`：日本語版・英語版の2URLと、`xhtml:link` による相互の言語代替
- `robots.txt`：サイトマップのURL

`x-default` は、日英以外の言語の読者向けに英語版を指定しています。変更したい場合は `tools/configure-site.py` の該当行を編集してください。

注意：GitHub Pagesのプロジェクトサイトでは、`robots.txt` がドメイン直下ではなくサブディレクトリに置かれるため、検索エンジンはこのファイルを読みません。サイトマップはSearch Consoleなどから直接送信してください。未設定の `sitemap.xml` はURLを含まない待機状態なので、設定前に送信しないでください。

## ファイル

- `index.html`：日本語版の記事本文、写真、目次、FAQ、出典9件
- `en/index.html`：英語版（同等の内容・写真・表・FAQ・出典）
- `assets/css/style.css`：PC・スマートフォン・印刷向けスタイル（両言語共通）。末尾にV2の追加分（言語切替、部品区分タグ、英語版の文字組み）
- `assets/js/main.js`：写真拡大、現在の章の目次強調（両言語共通・変更なし）
- `assets/images/`：プライバシー処理済みWebP写真14枚（両言語共通・変更なし）
- `assets/favicon.svg`：文字によるサイトアイコン
- `IMAGE-LIST.md`：加工済み写真一覧
- `AUDIT.md`：V2の修正内容・確認結果・未確認事項
- `tools/configure-site.py`：実際の公開URLを設定する補助ツール
- `.nojekyll`：Jekyll変換を無効化

## 編集と画像の注意

本文はHTMLに直接あります。日本語版を修正したら、英語版にも同じ事実を反映してください。外部フォント、解析タグ、広告、外部JavaScriptは読み込みません。

掲載写真は手作業の被写体マスク、トリミング、画像ごとに調整したガウスぼかし、中性色の遮蔽を組み合わせています。画像生成・部品の描き直しは行っていません。Exif・GPS・XMP情報は含めていません。元写真はこの成果物に同梱していません。

機械部品の一部は元写真からピントが甘く、背景処理で鮮明化したものではありません。完成車写真は背景保護のため細いスポーク周辺の境界に処理跡があります。スポーク組みや車輪構造の解説用画像としては扱っていません。

写真・整備記録の権利は提供者に帰属します。第三者向けの再配布ライセンスは設定していません。SHIMANO公式サイトではありません。

公開設定の参照：[GitHub公式ドキュメント](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)（2026年10月22日確認）。
