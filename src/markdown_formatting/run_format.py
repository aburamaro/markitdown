from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from copilot import CopilotClient

from document_to_markdown.build_output_paths import validate_output_path
from markdown_formatting.build_final_output_paths import (
    build_converted_image_dir,
    build_final_image_dir,
    build_final_markdown_path,
)
from markdown_formatting.copy_final_images import copy_final_images
from markdown_formatting.format_with_copilot import format_with_copilot


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FormattingResult:
    source_path: Path
    output_path: Path
    is_success: bool
    error_message: str | None = None


# 変換済みMarkdownを順番に整形し、ファイルごとの結果を返す。
async def format_converted_files(
    converted_paths: list[Path],
    convert_output_dir: Path,
    final_output_dir: Path,
    prompt_path: Path,
    model: str,
    overwrite: bool,
) -> list[FormattingResult]:
    if not converted_paths:
        return []

    if not prompt_path.is_file():
        raise FileNotFoundError(
            f"Formatting prompt does not exist: {prompt_path}"
        )

    # 全ファイルで共通利用するプロンプトとCopilotクライアントを準備する。
    format_instructions = prompt_path.read_text(encoding="utf-8")
    client = CopilotClient()
    results: list[FormattingResult] = []

    # バッチ全体で1つのクライアントを起動し、通信資源を使い回す。
    await client.start()
    try:
        for converted_path in converted_paths:
            # 変換用ディレクトリからの相対階層を最終出力にも引き継ぐ。
            final_path = build_final_markdown_path(
                converted_path=converted_path,
                convert_output_dir=convert_output_dir,
                final_output_dir=final_output_dir,
            )
            try:
                logger.info(
                    "[START] Formatting with Copilot: %s", converted_path
                )
                # 出力可否を確認してから、CopilotへMarkdown整形を依頼する。
                validate_output_path(final_path, overwrite)
                formatted_text = await format_with_copilot(
                    client=client,
                    format_instructions=format_instructions,
                    markdown_text=converted_path.read_text(encoding="utf-8"),
                    model=model,
                )

                # 整形済み本文を保存し、対応する抽出画像も最終出力へ移す。
                final_path.parent.mkdir(parents=True, exist_ok=True)
                final_path.write_text(formatted_text, encoding="utf-8")
                copy_final_images(
                    source_dir=build_converted_image_dir(converted_path),
                    destination_dir=build_final_image_dir(final_path),
                    overwrite=overwrite,
                )
                logger.info("[SUCCESS] Final Markdown saved: %s", final_path)
                results.append(
                    FormattingResult(converted_path, final_path, True)
                )
            except Exception as error:
                # 1件の失敗でバッチを止めず、残りのMarkdown処理を継続する。
                logger.error(
                    "[FAILED] Failed to format %s: %s",
                    converted_path,
                    error
                )
                results.append(
                    FormattingResult(
                        converted_path,
                        final_path,
                        False,
                        str(error)
                    )
                )
    finally:
        # 途中で例外が起きても、Copilotクライアントを確実に停止する。
        await client.stop()

    return results


# Copilot整形の成功数・失敗数と、失敗理由をログへ表示する。
def show_formatting_summary(results: list[FormattingResult]) -> None:
    failures = [result for result in results if not result.is_success]
    logger.info(
        "[%s] Copilot formatting done. success=%s failure=%s",
        "SUCCESS" if not failures else "FAILED",
        len(results) - len(failures),
        len(failures),
    )
    for result in failures:
        logger.info("- %s: %s", result.source_path, result.error_message)
