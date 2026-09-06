# PDF / Office to Markdown Converter

`markitdown` を使って、PDFやOfficeファイルをMarkdownへ変換するPythonスクリプトです。

`input_files_dir/` に配置したファイルを読み込み、MarkItDownによる変換結果を
`convert_markdown_dir/` に出力します。プロンプトで手動整形した最終成果物は
`final_markdown_dir/` に配置します。

PythonコードはMarkItDownによる変換までを担当します。Copilot SDKや外部LLM APIを
呼び出す処理は含みません。

PDFだけでなく、DOCX / PPTX / XLSXなどのOfficeファイルも扱いやすいように、対象拡張子・入力収集・変換・保存処理を分けています。

## 必要環境

- Python 3.10以上
- markitdown
- PyMuPDF
- PyYAML
- devcontainer

## ディレクトリ構成

```text
markitdown/
├── input_files_dir/
├── convert_markdown_dir/
├── final_markdown_dir/
├── config.yml
├── src/
│   ├── main.py
│   └── document_to_markdown/
│       ├── __init__.py
│       ├── build_output_paths.py
│       ├── find_input_files.py
│       ├── parse_command_line.py
│       ├── run_convert.py
│       ├── settings.py
│       ├── show_conversion_summary.py
│       ├── write_markdown_output.py
│       └── image_output/
│           ├── __init__.py
│           ├── append_image_links.py
│           ├── extract_html_images.py
│           ├── extract_images_from_file.py
│           ├── extract_office_images.py
│           ├── extract_pdf_images.py
│           └── image_files.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

`practice_markdown` コンテナ内で、上記の `markitdown/` プロジェクトディレクトリを開いて作業する想定です。

## インストール

Dev Containerを使用する場合、`requirements.txt` の依存関係はイメージのビルド時に
自動でインストールされます。依存関係を変更した場合は、Dev Containerを再ビルド
してください。

Dev Containerを使用しない場合は、以下の手順でインストールします。

### requirements.txtを使う場合

`requirements.txt` に以下を記載します。

```txt
markitdown[all]
pymupdf
PyYAML
```

その後、依存関係をインストールします。

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 直接インストールする場合

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install "markitdown[all]"
pip install pymupdf
pip install PyYAML
```

## 使い方

### 基本の変換

```bash
python src/main.py
```

`input_files_dir/` 配下の対応ファイルを再帰的に探し、
`convert_markdown_dir/` にMarkdownファイルを出力します。

たとえば以下のように配置します。

```text
input_files_dir/
├── sample.pdf
├── meeting.docx
└── report.xlsx
```

実行後は以下のように出力されます。

```text
convert_markdown_dir/
├── sample.md
├── meeting.md
└── report.md
```

PDFやOfficeファイル内に画像が含まれている場合は、画像ファイルも
`convert_markdown_dir/images/` 配下に書き出され、Markdown末尾に画像リンクが
追加されます。

PDFの画像リンクはページ別に分けられ、同じページ内ではPDF上の座標をもとに、上から下、左から右の順に並べます。

```text
convert_markdown_dir/
├── sample.md
└── images/
    └── sample/
        ├── page_001_image_001.png
        └── page_002_image_001.jpeg
```

Markdownには以下のようなリンクが追加されます。

```md
## Extracted Images

### Page 1

![sample page 1 image 1](images/sample/page_001_image_001.png)
```

DOCX / PPTX / XLSXやHTML内の画像は、以下のようにファイル内の埋め込み画像として末尾に追加されます。

```md
## Extracted Images

### Embedded Images

![meeting embedded image 1](images/meeting/media_001_image1.png)
```

### サブディレクトリを含めて変換

入力側にサブディレクトリがある場合は、出力側でも同じ階層を保ちます。

```text
input_files_dir/
└── 2026/
    └── sample.pdf
```

```text
convert_markdown_dir/
└── 2026/
    └── sample.md
```

### 入力ファイルを直接指定する

```bash
python src/main.py ./input_files_dir/sample.pdf
```

### 入力・出力ディレクトリを指定する

```bash
python src/main.py ./input_files_dir -o ./convert_markdown_dir
```

### 既存のMarkdownを上書きする

```bash
python src/main.py --overwrite
```

### 詳細ログを出す

```bash
python src/main.py -v
```

### 画像の抽出をしない

本文だけMarkdown化したい場合は、画像抽出を無効にできます。

```bash
python src/main.py --no-extract-images
```

## Copilot Chatで最終版を作る

MarkItDownによる変換が完了したら、GitHub Copilot Chatで
`.github/prompts/format_markdown_prompt.md` を使用し、整形対象として
`convert_markdown_dir/` 内のMarkdownファイルを指定します。

この整形はPython CLIから自動実行しません。Copilot Chatにプロンプトを適用して
手動で実行し、生成された最終ファイルが `final_markdown_dir/` に保存されたことを
確認してください。最終ファイルには `v0.1` などのリビジョンを付けます。

## 対応拡張子

現在のスクリプトでは以下を対象にしています。

- `.pdf`
- `.docx`
- `.doc`
- `.pptx`
- `.xlsx`
- `.xls`
- `.csv`
- `.html`
- `.htm`
- `.txt`
- `.json`
- `.xml`

対象を増やしたい場合は、`config.yml` の `supported_extensions` に拡張子を
追加してください。画像抽出も行う形式は、`image_extraction` 内の対応する一覧にも
追加します。

## 画像抽出の対応状況

| 拡張子 | 画像抽出 | 補足 |
|---|---:|---|
| `.pdf` | 対応 | PyMuPDFで画像を抽出し、ページ別・座標順に並べます。 |
| `.docx` | 対応 | Office Open XML内の `media/` 画像を抽出します。 |
| `.pptx` | 対応 | Office Open XML内の `media/` 画像を抽出します。 |
| `.xlsx` | 対応 | Office Open XML内の `media/` 画像を抽出します。 |
| `.html` / `.htm` | 一部対応 | ローカル画像参照とdata URI画像を抽出します。リモートURL画像はダウンロードしません。 |
| `.doc` | 非対応 | 旧Officeバイナリ形式です。LibreOfficeなどで `.docx` に変換してから実行してください。 |
| `.xls` | 非対応 | 旧Officeバイナリ形式です。LibreOfficeなどで `.xlsx` に変換してから実行してください。 |
| `.csv` / `.txt` / `.json` / `.xml` | 非対応 | 通常は画像埋め込みを持たないテキスト形式として扱います。 |

## スクリプトの設計方針

- 関数ごとの責務を小さくする
- コマンドライン解析、入力収集、変換、保存、結果表示を分離する
- 画像抽出をMarkdown変換処理から独立させる
- 型ヒントを使う
- `print` ではなく `logging` を使う
- 1ファイルの失敗で全体の変換を止めない
- 後から対応拡張子を増やしやすくする

## モジュール構成

| ファイル | 役割 |
|---|---|
| `src/main.py` | ツールの実行入口です。 |
| `src/document_to_markdown/run_convert.py` | 変換処理全体の流れを書いています。 |
| `config.yml` | 入力・出力ディレクトリ、対応拡張子、画像抽出対象を定義します。 |
| `src/document_to_markdown/settings.py` | `config.yml` を読み込み、設定値を検証します。 |
| `src/document_to_markdown/parse_command_line.py` | コマンドライン引数を読む処理です。 |
| `src/document_to_markdown/find_input_files.py` | `input_files_dir/` から対象ファイルを探す処理です。 |
| `src/document_to_markdown/write_markdown_output.py` | MarkItDownでMarkdown本文を作成し、Markdownファイルとして保存する処理です。 |
| `src/document_to_markdown/show_conversion_summary.py` | 成功件数・失敗件数・失敗理由を表示する処理です。 |
| `src/document_to_markdown/build_output_paths.py` | Markdown出力先、画像出力先、Markdown内の画像相対パスを作る処理です。 |
| `src/document_to_markdown/image_output/extract_images_from_file.py` | 画像抽出の共通処理や、ファイル形式ごとの呼び分け処理です。 |
| `src/document_to_markdown/image_output/extract_pdf_images.py` | PDFから画像を抽出する処理です。 |
| `src/document_to_markdown/image_output/extract_office_images.py` | `.docx` / `.pptx` / `.xlsx` から画像を抽出する処理です。 |
| `src/document_to_markdown/image_output/extract_html_images.py` | HTMLの `img` タグから画像を抽出する処理です。 |
| `src/document_to_markdown/image_output/append_image_links.py` | 抽出した画像リンクをMarkdown末尾に追加する処理です。 |
| `src/document_to_markdown/image_output/image_files.py` | 抽出画像のデータ構造と並び替え処理です。 |

## 注意点

変換品質は元ファイルの構造や `markitdown` 側の対応状況に依存します。

スキャンPDFなど、文字情報を持たないPDFでは期待通りにMarkdown化できない場合があります。その場合はOCR対応のワークフローを別途検討してください。

`convert_markdown_dir/` に同名のMarkdownファイルが存在する場合、標準では
上書きしません。上書きしたい場合は `--overwrite` を付けて実行してください。

PDF内の画像は、PDFに埋め込まれている画像オブジェクトをPyMuPDFで抽出します。ページ全体の見た目をスクリーンショット化する処理ではないため、PDFの作りによっては期待した単位で画像が抽出されない場合があります。

画像の並び順はページ番号とPDF上の座標をもとに整列します。ただし、PDF内部の構造によって座標情報が不完全な場合は、見た目上の順序と完全には一致しない可能性があります。

DOCX / PPTX / XLSXの画像は、ファイル内部に保存されている画像ファイルを抽出します。本文中の正確な位置へ自動挿入する処理ではありません。
