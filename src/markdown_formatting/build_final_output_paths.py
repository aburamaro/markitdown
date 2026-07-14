from __future__ import annotations

from pathlib import Path


# 変換用ディレクトリ内の階層を保って、最終Markdownの出力先を組み立てる。
def build_final_markdown_path(
    converted_path: Path,
    convert_output_dir: Path,
    final_output_dir: Path,
) -> Path:
    relative_path = converted_path.relative_to(convert_output_dir)
    return final_output_dir / relative_path


# 変換済みMarkdownに対応する、抽出画像ディレクトリを組み立てる。
def build_converted_image_dir(converted_path: Path) -> Path:
    return converted_path.parent / "images" / converted_path.stem


# 最終Markdownに対応する、画像コピー先ディレクトリを組み立てる。
def build_final_image_dir(final_path: Path) -> Path:
    return final_path.parent / "images" / final_path.stem
