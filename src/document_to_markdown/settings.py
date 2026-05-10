from __future__ import annotations

from pathlib import Path


# devcontainer内のプロジェクトルートを基準にした、標準の入力・出力ディレクトリ。
DEFAULT_INPUT_DIR = Path("input_files_dir")
DEFAULT_OUTPUT_DIR = Path("output_files_dir")


# MarkItDownでMarkdown化する入力ファイルの対象拡張子。
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc",
    ".pptx",
    ".xlsx",
    ".xls",
    ".csv",
    ".html",
    ".htm",
    ".txt",
    ".json",
    ".xml",
}


# 画像抽出処理を持つファイル形式。
OPENXML_EXTENSIONS = {".docx", ".pptx", ".xlsx"}
HTML_EXTENSIONS = {".html", ".htm"}
