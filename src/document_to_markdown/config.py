from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yml"


@dataclass(frozen=True)
class AppConfig:
    input_dir: Path
    convert_output_dir: Path
    final_output_dir: Path
    format_prompt: Path
    copilot_model: str
    supported_extensions: frozenset[str]
    openxml_extensions: frozenset[str]
    html_extensions: frozenset[str]


# 指定された必須キーを取得し、未定義の場合は設定箇所を示して通知する。
def _required(mapping: dict[str, Any], key: str, location: str) -> Any:
    try:
        return mapping[key]
    except KeyError as error:
        message = f"Missing configuration key: {location}.{key}"
        raise ValueError(message) from error


# YAMLから読み込んだ値がマッピング形式であることを確認する。
def _mapping(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"Configuration value must be a mapping: {location}")
    return value


# 拡張子リストを検証し、大文字と小文字を区別しない集合へ変換する。
def _extensions(value: Any, location: str) -> frozenset[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(
            f"Configuration value must be a non-empty list: {location}"
        )
    if not all(
        isinstance(item, str) and item.startswith(".")
        for item in value
    ):
        raise ValueError(
            f"Extensions must be strings beginning with '.': {location}"
        )
    return frozenset(item.lower() for item in value)


# YAML設定ファイルを読み込み、検証済みのアプリケーション設定を返す。
def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    """YAML設定ファイルを読み込み、アプリケーション設定へ変換する。"""
    try:
        # YAML本文をPythonの辞書やリストとして安全に読み込む。
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        message = f"Configuration file does not exist: {config_path}"
        raise FileNotFoundError(message) from error
    except yaml.YAMLError as error:
        message = f"Invalid YAML in configuration file {config_path}: {error}"
        raise ValueError(message) from error

    # 各設定セクションの存在とマッピング形式を順番に検証する。
    root = _mapping(raw, "config")
    paths = _mapping(_required(root, "paths", "config"), "paths")
    copilot = _mapping(_required(root, "copilot", "config"), "copilot")
    file_types = _mapping(
        _required(root, "file_types", "config"),
        "file_types",
    )
    image_extraction = _mapping(
        _required(file_types, "image_extraction", "file_types"),
        "file_types.image_extraction",
    )

    # Copilotモデルが空でない文字列として定義されているか確認する。
    model = _required(copilot, "model", "copilot")
    if not isinstance(model, str) or not model:
        raise ValueError(
            "Configuration value must be a non-empty string: copilot.model"
        )

    # 検証済みの値を、呼び出し側で扱いやすいAppConfigへ変換する。
    return AppConfig(
        input_dir=Path(_required(paths, "input_dir", "paths")),
        convert_output_dir=Path(
            _required(paths, "convert_output_dir", "paths")
        ),
        final_output_dir=Path(_required(paths, "final_output_dir", "paths")),
        format_prompt=Path(_required(paths, "format_prompt", "paths")),
        copilot_model=model,
        supported_extensions=_extensions(
            _required(file_types, "supported", "file_types"),
            "file_types.supported",
        ),
        openxml_extensions=_extensions(
            _required(
                image_extraction,
                "openxml",
                "file_types.image_extraction",
            ),
            "file_types.image_extraction.openxml",
        ),
        html_extensions=_extensions(
            _required(image_extraction, "html", "file_types.image_extraction"),
            "file_types.image_extraction.html",
        ),
    )
