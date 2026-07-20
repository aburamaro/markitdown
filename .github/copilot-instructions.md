# Copilot Instructions

## プロジェクト概要

このプロジェクトは、PDF、Office、HTML、テキスト系ファイルをMarkdownへ変換するローカル実行用のPython CLIツールです。

入力ファイルは `input_files_dir/` に配置します。  
MarkItDownによる変換結果は `convert_markdown_dir/` に出力します。
利用者がGitHub Copilot Chatで手動整形した最終版は
`final_markdown_dir/` に出力します。

対応ファイルに画像が含まれている場合は、画像ファイルを抽出し、生成したMarkdownの末尾に画像リンクを追加します。

## GitHub Copilot Chatによる手動整形

- Python CLIの責務は、MarkItDownによるMarkdown変換と画像抽出までです。
- PythonコードからCopilot SDKやLLM APIを呼び出さないでください。
- AI整形は、利用者が `.github/prompts/format_markdown_prompt.md` を使って
  GitHub Copilot Chat上で手動実行します。
- 整形後のMarkdownは `final_markdown_dir/` に新規ファイルとして保存します。
- APIキーや認証情報をリポジトリに保存しないでください。

## 実行方法

プロジェクトルートから以下を実行します。

```bash
python src/main.py
```

依存関係は以下でインストールします。

```bash
pip install -r requirements.txt
```

## ディレクトリ構成

- `src/main.py` はCLIの実行入口です。
- `config.yml` は標準のディレクトリや対応拡張子を管理します。
- `src/document_to_markdown/settings.py` は設定を読み込み、検証します。
- `src/document_to_markdown/run_convert.py` は変換処理全体の流れを制御します。
- `src/document_to_markdown/parse_command_line.py` はコマンドライン引数を解析します。
- `src/document_to_markdown/find_input_files.py` は入力パス配下から対応ファイルを探します。
- `src/document_to_markdown/build_output_paths.py` はMarkdown出力先、画像出力先、上書き可否を管理します。
- `src/document_to_markdown/write_markdown_output.py` はMarkItDownによる変換とMarkdownファイル保存を担当します。
- `src/document_to_markdown/show_conversion_summary.py` は変換結果のログ表示を担当します。
- `src/document_to_markdown/image_output/` は画像抽出とMarkdown画像リンク生成を担当します。

## コーディング方針

- Pythonの型ヒントを使用してください。
- ファイルパス処理には `pathlib.Path` を使用してください。
- `print` ではなく `logging` を使用してください。
- 関数は小さく保ち、1つの責務に集中させてください。
- 名前は明確な `snake_case` にしてください。
- ファイル名は、そのファイルが行う処理を説明する名前にしてください。
- `utils.py`、`helpers.py`、`common.py`、`misc.py` のような曖昧なモジュール名は避けてください。

## 設計ルール

- 設定値は `config.yml` に集約してください。
- CLI引数解析と変換処理は分離してください。
- Markdown変換処理と画像抽出処理は分離してください。
- PDF、Office、HTMLの画像抽出処理を1つの大きな関数にまとめないでください。
- 新しいファイル形式を変換対象に追加する場合は、`config.yml` の
  `supported_extensions` を更新してください。
- 新しいファイル形式の画像抽出に対応する場合は、`image_output/` 配下に専用モジュールを追加してください。

## Markdown出力ルール

- `## Extracted Images` セクションを削除しないでください。
- `![...](images/...)` 形式のMarkdown画像リンクを削除しないでください。
- 画像パスは、生成されたMarkdownファイルからの相対パスとして維持してください。
- 整形時に、抽出画像への参照を削除しないでください。
- 明示的に依頼されない限り、元文書の内容を要約・改変しないでください。

## エラーハンドリングとログ

- エラーメッセージには、対象ファイルパスを含めてください。
- 複数ファイル変換時は、1ファイルが失敗しても全体の処理を継続してください。
- CLI出力を読みやすくするため、`[START]`、`[SUCCESS]`、`[FAILED]` のようなログラベルを使用してください。
- 変換失敗を黙って無視しないでください。

## テストと確認

コード変更後は、以下を実行してください。

```bash
python3 -m compileall -q src
```

依存関係がインストール済みの場合は、以下も確認してください。

```bash
python src/main.py --help
```
