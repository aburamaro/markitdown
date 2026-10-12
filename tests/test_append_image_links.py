from pathlib import Path

from document_to_markdown.image_output.append_image_links import (
    append_image_links,
)
from document_to_markdown.image_output.extract_images import ExtractedImage


def test_append_image_links_returns_original_text_without_images() -> None:
    assert (
        append_image_links(
            markdown_text="# Title\n",
            markdown_path=Path("converted/sample.md"),
            extracted_images=[],
        )
        == "# Title\n"
    )


def test_append_image_links_groups_and_sorts_images() -> None:
    markdown = append_image_links(
        markdown_text="# Title\n",
        markdown_path=Path("converted/sample.md"),
        extracted_images=[
            ExtractedImage(
                image_path=Path("converted/images/sample/page_002.png"),
                markdown_alt_text="page 2 image",
                section_title="Page 2",
                sort_index=2,
                x0=0,
                y0=0,
            ),
            ExtractedImage(
                image_path=Path("converted/images/sample/page_001.png"),
                markdown_alt_text="page 1 image",
                section_title="Page 1",
                sort_index=1,
                x0=0,
                y0=0,
            ),
        ],
    )

    assert markdown == (
        "# Title\n\n"
        "## Extracted Images\n\n"
        "### Page 1\n\n"
        "![page 1 image](images/sample/page_001.png)\n\n"
        "### Page 2\n\n"
        "![page 2 image](images/sample/page_002.png)\n"
    )
