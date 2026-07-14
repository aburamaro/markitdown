# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリの作成
WORKDIR /work_dir

# Pythonの依存関係をインストール
COPY requirements.txt /work_dir/

# OSパッケージ更新
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pipの更新&ライブラリのインストール
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# ツール本体をコンテナにコピー
COPY . /work_dir/