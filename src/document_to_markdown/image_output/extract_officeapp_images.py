from __future__ import annotations

import zipfile
from pathlib import Path

from document_to_markdown.build_output_paths import validate_output_path
from document_to_markdown.image_output.extract_images import ExtractedImage


# Office Open XML形式の内部mediaディレクトリから画像を抽出する。
def extract_office_images(
    source_path: Path,
    image_output_dir: Path,
    overwrite: bool,
) -> list[ExtractedImage]:
    extracted_images: list[ExtractedImage] = []

    # Office Open XMLファイルをZIPアーカイブとして開く。
    with zipfile.ZipFile(source_path) as archive:
        media_names = [
            file_name
            for file_name in archive.namelist()
            if "/media/" in file_name and not file_name.endswith("/")
        ]

        for image_index, media_name in enumerate(sorted(media_names), start=1):
            image_name = Path(media_name).name
            image_path = image_output_dir / (f"media_{image_index:03d}_{image_name}")

            validate_output_path(output_path=image_path, overwrite=overwrite)
            image_path.parent.mkdir(parents=True, exist_ok=True)

            with archive.open(media_name) as source_file:
                image_path.write_bytes(source_file.read())

            extracted_images.append(
                ExtractedImage(
                    image_path=image_path,
                    markdown_alt_text=(
                        f"{source_path.stem} embedded image {image_index}"
                    ),
                    section_title="Embedded Images",
                    sort_index=image_index,
                    x0=0,
                    y0=0,
                )
            )

    return extracted_images
