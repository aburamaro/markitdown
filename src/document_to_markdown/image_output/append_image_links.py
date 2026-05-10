from __future__ import annotations

from pathlib import Path

from document_to_markdown.build_output_paths import build_markdown_image_path
from document_to_markdown.image_output.extract_images import (
    ExtractedImage,
    sort_extracted_images,
)


# 抽出した画像へのリンクをMarkdown末尾に追加する。
def append_image_links(
    markdown_text: str,
    markdown_path: Path,
    extracted_images: list[ExtractedImage],
) -> str:
    if not extracted_images:
        return markdown_text

    image_lines = ["", "", "## Extracted Images", ""]
    current_section_title: str | None = None

    for extracted_image in sort_extracted_images(extracted_images):
        if extracted_image.section_title != current_section_title:
            current_section_title = extracted_image.section_title
            image_lines.append(f"### {current_section_title}")
            image_lines.append("")

        image_link = build_markdown_image_path(
            markdown_path=markdown_path,
            image_path=extracted_image.image_path,
        )
        image_lines.append(f"![{extracted_image.markdown_alt_text}]({image_link})")
        image_lines.append("")

    return markdown_text.rstrip() + "\n".join(image_lines)
