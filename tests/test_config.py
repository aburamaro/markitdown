from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from document_to_markdown.config import load_config


class ConfigTests(unittest.TestCase):
    def test_loads_yaml_configuration(self) -> None:
        yaml_text = """
paths:
  input_dir: documents
  convert_output_dir: converted
  final_output_dir: final
  format_prompt: prompt.md
copilot:
  model: test-model
file_types:
  supported: [.PDF, .txt]
  image_extraction:
    openxml: [.docx]
    html: [.html]
"""
        with tempfile.TemporaryDirectory() as temporary_dir:
            config_path = Path(temporary_dir) / "config.yml"
            config_path.write_text(yaml_text, encoding="utf-8")

            config = load_config(config_path)

        self.assertEqual(config.input_dir, Path("documents"))
        self.assertEqual(config.copilot_model, "test-model")
        self.assertEqual(config.supported_extensions, frozenset({".pdf", ".txt"}))

    def test_rejects_extension_without_leading_dot(self) -> None:
        yaml_text = """
paths:
  input_dir: documents
  convert_output_dir: converted
  final_output_dir: final
  format_prompt: prompt.md
copilot:
  model: auto
file_types:
  supported: [pdf]
  image_extraction:
    openxml: [.docx]
    html: [.html]
"""
        with tempfile.TemporaryDirectory() as temporary_dir:
            config_path = Path(temporary_dir) / "config.yml"
            config_path.write_text(yaml_text, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "beginning with"):
                load_config(config_path)


if __name__ == "__main__":
    unittest.main()
