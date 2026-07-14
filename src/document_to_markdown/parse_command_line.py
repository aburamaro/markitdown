from __future__ import annotations

import argparse
import logging
from pathlib import Path

from document_to_markdown.config import (
    DEFAULT_CONFIG_PATH,
    load_config,
)


# コマンドライン引数に応じてログ出力の詳しさを切り替える。
def configure_logging(verbose: bool) -> None:
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )


# コマンドライン引数を定義し、実行時の設定値として読み取る。
def parse_command_line() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH
    )
    config_args, _ = config_parser.parse_known_args()
    config = load_config(config_args.config)

    parser = argparse.ArgumentParser(
        description=(
            "Convert documents with MarkItDown, "
            "then format the generated Markdown "
            "with the GitHub Copilot SDK."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=config_args.config,
        help=(
            "Path to YAML configuration file. "
            f"Default: {DEFAULT_CONFIG_PATH}"
        ),
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        type=Path,
        default=config.input_dir,
        help=(
            "PDF / Office file path or directory path. "
            f"Default: {config.input_dir}"
        ),
    )

    parser.add_argument(
        "--convert-output-dir",
        type=Path,
        default=config.convert_output_dir,
        help=(
            "Directory for MarkItDown conversion results. "
            f"Default: {config.convert_output_dir}"
        ),
    )

    parser.add_argument(
        "--final-output-dir",
        type=Path,
        default=config.final_output_dir,
        help=(
            "Directory for Copilot-formatted final Markdown files. "
            f"Default: {config.final_output_dir}"
        ),
    )

    parser.add_argument(
        "--format-prompt",
        type=Path,
        default=config.format_prompt,
        help=(
            "Path to the prompt file for Copilot formatting. "
            f"Default: {config.format_prompt}"
        ),
    )

    parser.add_argument(
        "--copilot-model",
        default=config.copilot_model,
        help=f"Copilot model name. Default: {config.copilot_model}",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing converted and final files.",
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

    args = parser.parse_args()
    args.app_config = config
    return args
