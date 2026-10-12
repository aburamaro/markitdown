from __future__ import annotations

from pathlib import Path

from markitdown import MarkItDown

from document_to_markdown.build_output_paths import validate_output_path


# MarkItDownで入力ファイルをMarkdown本文に変換する。
def convert_file_to_markdown(converter: MarkItDown, source_path: Path) -> str:
    # MarkItDownへファイルパスを渡し、変換結果の本文を取り出す。
    converted_document = converter.convert(str(source_path))
    return converted_document.text_content


# Markdown文字列をUTF-8で保存する。
def write_markdown_file(
    output_path: Path,
    markdown_text: str,
    overwrite: bool,
) -> None:
    # 書き込み前に、既存ファイルを意図せず上書きしないか確認する。
    validate_output_path(output_path=output_path, overwrite=overwrite)

    # 出力ディレクトリがない場合でも、利用者が事前作成しなくて済むようにする。
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_text, encoding="utf-8")
