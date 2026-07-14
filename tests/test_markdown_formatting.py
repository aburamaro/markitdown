from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from markdown_formatting.clean_copilot_response import clean_copilot_response
from markdown_formatting.copy_final_images import copy_final_images


class MarkdownFormattingTests(unittest.TestCase):
    def test_surrounding_markdown_fence_is_removed(self) -> None:
        response = "```markdown\n# Title\n\nBody\n```"
        self.assertEqual(clean_copilot_response(response), "# Title\n\nBody\n")

    def test_images_are_copied_and_overwritten_as_one_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "converted" / "images" / "sample"
            destination = root / "final" / "images" / "sample"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (source / "current.png").write_bytes(b"current")
            (destination / "stale.png").write_bytes(b"stale")

            copy_final_images(source, destination, overwrite=True)

            self.assertEqual(
                (destination / "current.png").read_bytes(), b"current"
            )
            self.assertFalse((destination / "stale.png").exists())


if __name__ == "__main__":
    unittest.main()
