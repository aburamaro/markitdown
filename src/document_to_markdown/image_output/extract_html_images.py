from __future__ import annotations

import base64
import binascii
import logging
import mimetypes
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from document_to_markdown.build_output_paths import validate_output_path
from document_to_markdown.image_output.extract_images import ExtractedImage


logger = logging.getLogger(__name__)


class HtmlImageParser(HTMLParser):
    # HTML解析中に見つけた画像参照を保持する。
    def __init__(self) -> None:
        super().__init__()
        self.image_sources: list[str] = []

    # HTML内のimgタグからsrc属性だけを順番に集める。
    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() != "img":
            return

        attrs_by_name = {name.lower(): value for name, value in attrs}
        image_source = attrs_by_name.get("src")

        if image_source:
            self.image_sources.append(image_source)


# data URIの画像をデコードし、画像バイト列と拡張子を返す。
def decode_data_uri_image(image_source: str) -> tuple[bytes, str] | None:
    if not image_source.startswith("data:image/"):
        return None

    header, _, encoded_data = image_source.partition(",")
    if not encoded_data:
        return None

    media_type = header.removeprefix("data:").split(";", maxsplit=1)[0]
    guessed_extension = mimetypes.guess_extension(media_type) or ".png"

    try:
        return base64.b64decode(encoded_data), guessed_extension.lstrip(".")
    except binascii.Error:
        logger.warning("Failed to decode data URI image.")
        return None


# HTMLのimgタグが参照するローカル画像パスを解決する。
def resolve_local_html_image_path(
    html_path: Path,
    image_source: str,
) -> Path | None:
    parsed_source = urlparse(image_source)

    if parsed_source.scheme in {"http", "https"}:
        logger.info("Skip remote HTML image: %s", image_source)
        return None

    if parsed_source.scheme == "file":
        return Path(unquote(parsed_source.path))

    if parsed_source.scheme:
        logger.info("Skip unsupported HTML image source: %s", image_source)
        return None

    local_path = Path(unquote(parsed_source.path))
    if not local_path.is_absolute():
        local_path = html_path.parent / local_path

    return local_path


# HTML内のimgタグから、ローカル画像やdata URI画像を抽出する。
def extract_html_images(
    source_path: Path,
    image_output_dir: Path,
    overwrite: bool,
) -> list[ExtractedImage]:
    # HTMLを解析し、imgタグのsrc属性を出現順に収集する。
    parser = HtmlImageParser()
    parser.feed(source_path.read_text(encoding="utf-8", errors="ignore"))

    extracted_images: list[ExtractedImage] = []

    for image_index, image_source in enumerate(parser.image_sources, start=1):
        # data URIとローカルファイル参照を分けて処理する。
        decoded_image = decode_data_uri_image(image_source)

        if decoded_image:
            image_bytes, image_extension = decoded_image
            image_path = image_output_dir / (
                f"html_image_{image_index:03d}.{image_extension}"
            )

            validate_output_path(output_path=image_path, overwrite=overwrite)
            image_path.parent.mkdir(parents=True, exist_ok=True)
            image_path.write_bytes(image_bytes)

        else:
            source_image_path = resolve_local_html_image_path(
                html_path=source_path,
                image_source=image_source,
            )

            if source_image_path is None or not source_image_path.exists():
                logger.warning("Skip missing HTML image: %s", image_source)
                continue

            image_path = image_output_dir / (
                f"html_image_{image_index:03d}_{source_image_path.name}"
            )

            validate_output_path(output_path=image_path, overwrite=overwrite)
            image_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_image_path, image_path)

        extracted_images.append(
            ExtractedImage(
                image_path=image_path,
                markdown_alt_text=(
                    f"{source_path.stem} html image {image_index}"
                ),
                section_title="HTML Images",
                sort_index=image_index,
                x0=0,
                y0=0,
            )
        )

    return extracted_images
