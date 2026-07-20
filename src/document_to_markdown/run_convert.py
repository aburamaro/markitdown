from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from markitdown import MarkItDown

from document_to_markdown.build_output_paths import (
    build_image_output_dir,
    build_markdown_output_path,
    validate_output_path,
)
from document_to_markdown.find_input_files import find_input_files
from document_to_markdown.image_output.append_image_links import (
    append_image_links,
)
from document_to_markdown.image_output.extract_images_from_file import (
    extract_images_from_file,
)
from document_to_markdown.parse_command_line import (
    configure_logging,
    parse_command_line,
)
from document_to_markdown.show_conversion_summary import (
    ConversionResult,
    show_conversion_summary,
)
from document_to_markdown.write_markdown_output import (
    convert_file_to_markdown,
    write_markdown_file,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConversionConfig:
    input_path: Path
    output_dir: Path
    overwrite: bool = False
    extract_images: bool = True


# 1ファイルをMarkdownへ変換し、成功・失敗をConversionResultとして返す。
def convert_one_file(
    converter: MarkItDown,
    source_path: Path,
    config: ConversionConfig,
) -> ConversionResult:
    # 入力階層を維持したMarkdownの保存先を決める。
    output_path = build_markdown_output_path(
        source_path=source_path,
        input_root=config.input_path,
        output_dir=config.output_dir,
    )

    try:
        logger.info("[START] Converting: %s", source_path)

        validate_output_path(
            output_path=output_path,
            overwrite=config.overwrite,
        )

        # MarkItDownで本文をMarkdownへ変換する。
        markdown_text = convert_file_to_markdown(
            converter=converter,
            source_path=source_path,
        )

        if config.extract_images:
            # 対応形式では画像も抽出し、Markdown末尾へリンクを追加する。
            image_output_dir = build_image_output_dir(
                source_path=source_path,
                input_root=config.input_path,
                output_dir=config.output_dir,
            )
            extracted_images = extract_images_from_file(
                source_path=source_path,
                image_output_dir=image_output_dir,
                overwrite=config.overwrite,
            )
            markdown_text = append_image_links(
                markdown_text=markdown_text,
                markdown_path=output_path,
                extracted_images=extracted_images,
            )

        # AI整形は行わず、変換直後のMarkdownを保存する。
        write_markdown_file(
            output_path=output_path,
            markdown_text=markdown_text,
            overwrite=config.overwrite,
        )

        logger.info("[SUCCESS] Saved: %s", output_path)

        return ConversionResult(
            source_path=source_path,
            output_path=output_path,
            is_success=True,
        )

    except Exception as error:
        # バッチ変換では1件の失敗で全体を止めず、最後に失敗一覧を確認できるようにする。
        logger.error("[FAILED] Failed to convert %s: %s", source_path, error)

        return ConversionResult(
            source_path=source_path,
            output_path=output_path,
            is_success=False,
            error_message=str(error),
        )


# 設定に従って入力ファイルを収集し、MarkItDownのインスタンスを使い回して変換する。
def convert_files(config: ConversionConfig) -> list[ConversionResult]:
    # config.ymlで許可された入力ファイルだけを収集する。
    input_files = find_input_files(config.input_path)

    # 変換器はファイルごとに作り直さず、バッチ内で再利用する。
    converter = MarkItDown()

    logger.info("[START] Found %s file(s) to convert.", len(input_files))

    return [
        convert_one_file(
            converter=converter,
            source_path=file_path,
            config=config,
        )
        for file_path in input_files
    ]


# スクリプト全体の入口。引数解析、ログ設定、変換、結果表示を順に実行する。
def main() -> None:
    # CLI引数を読み込んでからログ出力を初期化する。
    args = parse_command_line()
    configure_logging(verbose=args.verbose)

    config = ConversionConfig(
        input_path=args.input_path,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
        extract_images=not args.no_extract_images,
    )

    # MarkItDown変換を実行し、処理結果だけをログ表示する。
    results = convert_files(config)
    show_conversion_summary(results)
