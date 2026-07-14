from __future__ import annotations

import shutil
from pathlib import Path


# 変換時に抽出した画像一式を、最終Markdown側のディレクトリへコピーする。
def copy_final_images(
        source_dir: Path,
        destination_dir: Path,
        overwrite: bool
) -> None:
    if not source_dir.exists():
        return

    if destination_dir.exists() and not overwrite:
        raise FileExistsError(
            f"Final image directory already exists: {destination_dir}. "
            "Use --overwrite to replace it."
        )

    if destination_dir.exists():
        # 上書き時は古い画像が残らないよう、ディレクトリ単位で置き換える。
        shutil.rmtree(destination_dir)

    shutil.copytree(source_dir, destination_dir)
