from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConversionResult:
    source_path: Path
    output_path: Path
    is_success: bool
    error_message: str | None = None


# 変換結果の成功数・失敗数と、失敗したファイルの理由をログに出す。
def show_conversion_summary(results: Iterable[ConversionResult]) -> None:
    result_list = list(results)

    success_count = sum(result.is_success for result in result_list)
    failure_count = len(result_list) - success_count

    if failure_count == 0:
        logger.info(
            "[SUCCESS] Done. success=%s failure=%s",
            success_count,
            failure_count
        )
    else:
        logger.info(
            "[FAILED] Done. success=%s failure=%s",
            success_count,
            failure_count
        )

    if failure_count > 0:
        logger.info("[FAILED] Failed files:")

        for result in result_list:
            if not result.is_success:
                logger.info(
                    "- %s: %s",
                    result.source_path,
                    result.error_message
                )
