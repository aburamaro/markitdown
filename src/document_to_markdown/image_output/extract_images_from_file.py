from __future__ import annotations

from pathlib import Path

from document_to_markdown.image_output.extract_html_images import extract_html_images
from document_to_markdown.image_output.extract_officeapp_images import extract_office_images
from document_to_markdown.image_output.extract_pdf_images import extract_pdf_images
from document_to_markdown.image_output.extract_images import (
    HTML_EXTENSIONS,
    OPENXML_EXTENSIONS,
    ExtractedImage,
)


# ファイル形式に応じた画像抽出処理を呼び分ける。
def extract_images_from_file(
    source_path: Path,
    image_output_dir: Path,
    overwrite: bool,
) -> list[ExtractedImage]:
    file_extension = source_path.suffix.lower()

    if file_extension == ".pdf":
        return extract_pdf_images(
            source_path=source_path,
            image_output_dir=image_output_dir,
            overwrite=overwrite,
        )

    if file_extension in OPENXML_EXTENSIONS:
        return extract_office_images(
            source_path=source_path,
            image_output_dir=image_output_dir,
            overwrite=overwrite,
        )

    if file_extension in HTML_EXTENSIONS:
        return extract_html_images(
            source_path=source_path,
            image_output_dir=image_output_dir,
            overwrite=overwrite,
        )

    return []
