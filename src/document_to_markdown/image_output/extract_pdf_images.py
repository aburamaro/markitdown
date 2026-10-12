from __future__ import annotations

from pathlib import Path

from document_to_markdown.build_output_paths import validate_output_path
from document_to_markdown.image_output.extract_images import ExtractedImage

try:
    import fitz
except ImportError:
    fitz = None


# PyMuPDFを使ってPDF内の画像をファイルとして書き出す。
def extract_pdf_images(
    source_path: Path,
    image_output_dir: Path,
    overwrite: bool,
) -> list[ExtractedImage]:
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF is required to extract PDF images. "
            "Install it with: pip install pymupdf"
        )

    extracted_images: list[ExtractedImage] = []

    # PDFを開き、ページ単位で画像と表示位置を取得する。
    with fitz.open(source_path) as document:
        for page_index in range(document.page_count):
            page = document.load_page(page_index)
            image_entries = page.get_images(full=True)
            image_entries_with_position = []

            for image_entry in image_entries:
                xref = image_entry[0]
                image_rects = page.get_image_rects(xref)

                # 同じ画像が複数箇所に表示される場合は、
                # それぞれ別の表示位置として扱う。
                if image_rects:
                    for image_rect in image_rects:
                        image_entries_with_position.append((image_entry, image_rect))
                else:
                    # 位置情報が取れないPDFでも、画像抽出自体は継続できるようにする。
                    image_entries_with_position.append(
                        (image_entry, fitz.Rect(0, 0, 0, 0))
                    )

            image_entries_with_position.sort(
                key=lambda item: (round(item[1].y0, 2), round(item[1].x0, 2))
            )

            for image_index, (image_entry, image_rect) in enumerate(
                image_entries_with_position,
                start=1,
            ):
                xref = image_entry[0]
                image_data = document.extract_image(xref)
                image_bytes = image_data["image"]
                image_extension = image_data.get("ext", "png")

                image_path = image_output_dir / (
                    f"page_{page_index + 1:03d}_image_{image_index:03d}."
                    f"{image_extension}"
                )

                validate_output_path(
                    output_path=image_path,
                    overwrite=overwrite,
                )
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image_path.write_bytes(image_bytes)

                extracted_images.append(
                    ExtractedImage(
                        image_path=image_path,
                        markdown_alt_text=(
                            f"{source_path.stem} page {page_index + 1} "
                            f"image {image_index}"
                        ),
                        section_title=f"Page {page_index + 1}",
                        sort_index=page_index + 1,
                        x0=image_rect.x0,
                        y0=image_rect.y0,
                    )
                )

    return extracted_images
