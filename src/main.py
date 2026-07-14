from __future__ import annotations

import asyncio

from document_to_markdown.parse_command_line import (
    configure_logging,
    parse_command_line,
)
from document_to_markdown.run_convert import ConversionConfig, convert_files
from document_to_markdown.show_conversion_summary import (
    show_conversion_summary,
)
from markdown_formatting.run_format import (
    format_converted_files,
    show_formatting_summary,
)


# 文書変換からCopilotによるMarkdown整形までの一連の処理を実行する。
async def run_pipeline() -> int:
    # 実行時の引数を読み取り、指定に応じたログレベルを設定する。
    args = parse_command_line()
    configure_logging(verbose=args.verbose)

    # 入力文書をMarkdownへ変換し、ファイルごとの結果を表示する。
    conversion_results = convert_files(
        ConversionConfig(
            input_path=args.input_path,
            output_dir=args.convert_output_dir,
            overwrite=args.overwrite,
            extract_images=not args.no_extract_images,
            supported_extensions=args.app_config.supported_extensions,
            openxml_extensions=args.app_config.openxml_extensions,
            html_extensions=args.app_config.html_extensions,
        )
    )
    show_conversion_summary(conversion_results)

    # 変換に成功したMarkdownだけを、Copilotによる整形処理へ渡す。
    converted_paths = [
        result.output_path
        for result in conversion_results
        if result.is_success
    ]
    formatting_results = await format_converted_files(
        converted_paths=converted_paths,
        convert_output_dir=args.convert_output_dir,
        final_output_dir=args.final_output_dir,
        prompt_path=args.format_prompt,
        model=args.copilot_model,
        overwrite=args.overwrite,
    )
    show_formatting_summary(formatting_results)

    # どちらかの処理に失敗があれば、異常終了を表す終了コード1を返す。
    has_failure = any(not result.is_success for result in conversion_results)
    has_failure = has_failure or any(
        not result.is_success for result in formatting_results
    )
    return 1 if has_failure else 0


if __name__ == "__main__":
    # 非同期パイプラインを実行し、戻り値をプロセスの終了コードとして返す。
    raise SystemExit(asyncio.run(run_pipeline()))
