from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yml"


# YAML設定ファイルを読み込み、ルート要素がマッピングか検証する。
def _load_config(config_path: Path) -> dict[str, Any]:
    try:
        loaded_config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise RuntimeError(f"Configuration file not found: {config_path}") from error
    except yaml.YAMLError as error:
        raise RuntimeError(
            f"Failed to parse configuration file: {config_path}"
        ) from error

    if not isinstance(loaded_config, dict):
        raise ValueError("The root of config.yml must be a mapping.")

    return loaded_config


# 指定した設定値をマッピングとして取得する。
def _get_mapping(config: dict[str, Any], key: str) -> dict[str, Any]:
    value = config.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"config.yml: '{key}' must be a mapping.")
    return value


# 指定したディレクトリ設定をPathとして取得する。
def _get_path(config: dict[str, Any], key: str) -> Path:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"config.yml: '{key}' must be a non-empty path.")
    return Path(value)


# 拡張子一覧を検証し、大文字小文字を統一した集合として取得する。
def _get_extensions(config: dict[str, Any], key: str) -> frozenset[str]:
    value = config.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"config.yml: '{key}' must be a non-empty list.")
    if not all(isinstance(item, str) and item.startswith(".") for item in value):
        raise ValueError(f"config.yml: every value in '{key}' must start with '.'.")

    return frozenset(item.lower() for item in value)


# 起動時にconfig.ymlを一度だけ読み込み、用途別の設定を取り出す。
_CONFIG = _load_config(CONFIG_PATH)
_DIRECTORIES = _get_mapping(_CONFIG, "directories")
_IMAGE_EXTRACTION = _get_mapping(_CONFIG, "image_extraction")

DEFAULT_INPUT_DIR = _get_path(_DIRECTORIES, "input")
DEFAULT_CONVERTED_DIR = _get_path(_DIRECTORIES, "converted")
DEFAULT_FINAL_DIR = _get_path(_DIRECTORIES, "final")

SUPPORTED_EXTENSIONS = _get_extensions(_CONFIG, "supported_extensions")
PDF_EXTENSIONS = _get_extensions(_IMAGE_EXTRACTION, "pdf_extensions")
OPENXML_EXTENSIONS = _get_extensions(_IMAGE_EXTRACTION, "openxml_extensions")
HTML_EXTENSIONS = _get_extensions(_IMAGE_EXTRACTION, "html_extensions")
