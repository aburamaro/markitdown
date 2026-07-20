from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ExtractedImage:
    image_path: Path
    markdown_alt_text: str
    section_title: str
    sort_index: int
    x0: float
    y0: float


# 抽出した画像を、セクション、表示順、上から下、左から右の順に並べる。
def sort_extracted_images(
    extracted_images: list[ExtractedImage],
) -> list[ExtractedImage]:
    return sorted(
        extracted_images,
        key=lambda image: (
            image.sort_index,
            round(image.y0, 2),
            round(image.x0, 2),
            image.image_path.name,
        ),
    )
