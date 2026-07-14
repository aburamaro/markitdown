from __future__ import annotations

from pathlib import Path


# 対象ファイルが存在し、MarkItDownで変換したい拡張子かを判定する。
def is_supported_file(
        file_path: Path,
        supported_extensions: frozenset[str]
) -> bool:
    return (
        file_path.is_file()
        and file_path.suffix.lower() in supported_extensions
    )


# 入力がファイルなら1件、ディレクトリなら配下の対応ファイルを再帰的に集める。
def find_input_files(
    input_path: Path,
    supported_extensions: frozenset[str],
) -> list[Path]:
    if input_path.is_file():
        if not is_supported_file(input_path, supported_extensions):
            raise ValueError(f"Unsupported file type: {input_path}")
        return [input_path]

    if input_path.is_dir():
        files = [
            file_path
            for file_path in sorted(input_path.rglob("*"))
            if is_supported_file(file_path, supported_extensions)
        ]

        if not files:
            raise FileNotFoundError(
                f"No supported files found in: {input_path}"
            )

        return files

    raise FileNotFoundError(f"Input path does not exist: {input_path}")
