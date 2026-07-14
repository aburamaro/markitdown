from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from document_to_markdown.build_output_paths import (
    build_image_output_dir,
    build_markdown_output_path,
)
from markdown_formatting.build_final_output_paths import (
    build_final_markdown_path,
)


class OutputPathTests(unittest.TestCase):
    def test_nested_document_keeps_requested_directory_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            input_dir = root / "input_files_dir"
            source_path = input_dir / "reports" / "sample.pdf"
            source_path.parent.mkdir(parents=True)
            source_path.touch()
            convert_dir = root / "convert_markdown_dir"
            final_dir = root / "final_markdown_dir"

            converted_path = build_markdown_output_path(
                source_path, input_dir, convert_dir
            )

            self.assertEqual(
                converted_path,
                convert_dir / "reports" / "sample.md",
            )
            self.assertEqual(
                build_image_output_dir(source_path, input_dir, convert_dir),
                convert_dir / "reports" / "images" / "sample",
            )
            self.assertEqual(
                build_final_markdown_path(
                    converted_path,
                    convert_dir,
                    final_dir
                ),
                final_dir / "reports" / "sample.md",
            )


if __name__ == "__main__":
    unittest.main()
