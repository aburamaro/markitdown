from __future__ import annotations

import argparse
import logging
from pathlib import Path

from document_to_markdown.settings import DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR


# ログ出力の詳しさをコマンドライン引数に応じて切り替える。
def configure_logging(verbose: bool) -> None:
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )


# コマンドライン引数を定義し、実行時の設定値として読み取る。
def parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF and Office files to Markdown using MarkItDown."
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=(
            "PDF / Office file path or directory path. "
            f"Default: {DEFAULT_INPUT_DIR}"
        ),
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save markdown files. Default: {DEFAULT_OUTPUT_DIR}",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files.",
    )

    parser.add_argument(
        "--no-extract-images",
        action="store_true",
        help="Do not extract images from PDF and Office files.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show debug logs.",
    )

    return parser.parse_args()
