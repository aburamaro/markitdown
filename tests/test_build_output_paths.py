from pathlib import Path

import pytest

from document_to_markdown.build_output_paths import (
    build_image_output_dir,
    build_markdown_image_path,
    build_markdown_output_path,
    validate_output_path,
)


def test_build_markdown_output_path_keeps_directory_structure(
    tmp_path: Path,
) -> None:
    input_root = tmp_path / "input"
    source_path = input_root / "reports" / "sample.pdf"
    output_dir = tmp_path / "converted"

    source_path.parent.mkdir(parents=True)
    source_path.write_text("dummy", encoding="utf-8")

    assert (
        build_markdown_output_path(
            source_path=source_path,
            input_root=input_root,
            output_dir=output_dir,
        )
        == output_dir / "reports" / "sample.md"
    )


def test_build_image_output_dir_keeps_directory_structure(
    tmp_path: Path,
) -> None:
    input_root = tmp_path / "input"
    source_path = input_root / "reports" / "sample.pdf"
    output_dir = tmp_path / "converted"

    source_path.parent.mkdir(parents=True)
    source_path.write_text("dummy", encoding="utf-8")

    assert (
        build_image_output_dir(
            source_path=source_path,
            input_root=input_root,
            output_dir=output_dir,
        )
        == output_dir / "images" / "reports" / "sample"
    )


def test_build_markdown_image_path_uses_markdown_relative_path() -> None:
    markdown_path = Path("converted/reports/sample.md")
    image_path = Path("converted/images/reports/sample/image_001.png")

    assert (
        build_markdown_image_path(
            markdown_path=markdown_path,
            image_path=image_path,
        )
        == "../images/reports/sample/image_001.png"
    )


def test_validate_output_path_rejects_existing_file_without_overwrite(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "sample.md"
    output_path.write_text("already exists", encoding="utf-8")

    with pytest.raises(FileExistsError):
        validate_output_path(output_path=output_path, overwrite=False)


def test_validate_output_path_allows_existing_file_with_overwrite(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "sample.md"
    output_path.write_text("already exists", encoding="utf-8")

    validate_output_path(output_path=output_path, overwrite=True)
