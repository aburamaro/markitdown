# Document to Final Markdown Pipeline

PDFやOfficeファイルをMarkItDownでMarkdownへ変換し、その結果をGitHub Copilot SDKで読みやすいMarkdownへ整形するPython CLIです。

`python src/main.py` の1回の実行で、変換と整形を順番に行います。

標準のディレクトリ、Copilotモデル、対応拡張子はプロジェクト直下の
`config.yml` で変更できます。

## 処理フロー

```text
input_files_dir/
    ↓ MarkItDown
convert_markdown_dir/
    ↓ GitHub Copilot SDK + .github/prompts/format_markdown_prompt.md
final_markdown_dir/
```

各段階で入力側のサブディレクトリ構造を維持します。抽出画像はMarkdownと同じ階層の `images/<文書名>/` に配置され、最終版側にもコピーされます。

```text
input_files_dir/
└── reports/
    └── sample.pdf

convert_markdown_dir/
└── reports/
    ├── sample.md
    └── images/
        └── sample/
            └── page_001_image_001.png

final_markdown_dir/
└── reports/
    ├── sample.md
    └── images/
        └── sample/
            └── page_001_image_001.png
```

## 必要環境

- Python 3.11以上
- GitHub Copilotを利用できるGitHubアカウント、またはSDKで利用可能なトークン
- devcontainer（推奨）

```bash
pip install -r requirements.txt
```

## Copilot認証

Copilot CLIでログイン済みの場合、SDKはその認証情報を使用します。コンテナや自動実行では、次のいずれかの環境変数を利用できます。

```text
COPILOT_GITHUB_TOKEN（推奨）
GH_TOKEN
GITHUB_TOKEN
```

トークンや文書内容の取り扱いは、所属組織のセキュリティポリシーに従ってください。変換後のMarkdown本文は、整形のためGitHub Copilotへ送信されます。

## 使い方

基本実行:

```bash
python src/main.py
```

入力ファイルを直接指定:

```bash
python src/main.py input_files_dir/sample.pdf
```

既存の変換結果と最終結果を上書き:

```bash
python src/main.py --overwrite
```

出力先を変更:

```bash
python src/main.py \
  --convert-output-dir convert_markdown_dir \
  --final-output-dir final_markdown_dir
```

モデルまたは整形プロンプトを変更:

```bash
python src/main.py \
  --copilot-model auto \
  --format-prompt .github/prompts/format_markdown_prompt.md
```

別の設定ファイルを使用:

```bash
python src/main.py --config path/to/config.yml
```

`--convert-output-dir` などのコマンドラインオプションを指定した場合は、
`config.yml` の値よりコマンドラインの値が優先されます。

画像を抽出しない:

```bash
python src/main.py --no-extract-images
```

詳細ログ:

```bash
python src/main.py --verbose
```

すべてのオプション:

```bash
python src/main.py --help
```

## 対応拡張子

- `.pdf`
- `.docx`, `.doc`
- `.pptx`
- `.xlsx`, `.xls`
- `.csv`
- `.html`, `.htm`
- `.txt`, `.json`, `.xml`

画像抽出はPDF、DOCX、PPTX、XLSX、HTMLに対応しています。旧Officeバイナリ形式の `.doc` と `.xls` は本文変換の対象ですが、画像抽出には対応していません。

## 主なモジュール

- `src/document_to_markdown/`: MarkItDown変換と画像抽出
- `src/markdown_formatting/`: Copilot SDKによる整形、最終版保存、画像コピー
- `.github/prompts/format_markdown_prompt.md`: Markdown整形指示
- `config.yml`: パス、モデル、対象ファイル形式の標準設定

複数ファイルのうち1件が失敗しても残りの処理は継続し、最後に成功・失敗件数を表示します。
