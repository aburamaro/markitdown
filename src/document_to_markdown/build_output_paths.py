from __future__ import annotations

import os
from pathlib import Path


# 入力ディレクトリ配下の階層を保ったまま、出力先のMarkdownファイルパスを組み立てる。
def build_markdown_output_path(source_path: Path, input_root: Path, output_dir: Path) -> Path:
    if input_root.is_dir():
        relative_path = source_path.relative_to(input_root)
        return output_dir / relative_path.with_suffix(".md")

    return output_dir / f"{source_path.stem}.md"


# 抽出した画像の保存先ディレクトリを組み立てる。
def build_image_output_dir(source_path: Path, input_root: Path, output_dir: Path) -> Path:
    if input_root.is_dir():
        relative_path = source_path.relative_to(input_root).with_suffix("")
        return output_dir / "images" / relative_path

    return output_dir / "images" / source_path.stem


# Markdownファイルから見た画像ファイルの相対パスを作る。
def build_markdown_image_path(markdown_path: Path, image_path: Path) -> str:
    relative_path = os.path.relpath(
        image_path,
        start=markdown_path.parent,
    )

    return Path(relative_path).as_posix()


# 出力前に、既存ファイルの上書き可否を確認する。
def validate_output_path(output_path: Path, overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {output_path}. "
            "Use --overwrite to replace it."
        )
