FROM python:3.12-slim

# OSパッケージ更新 + git install
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの作成
WORKDIR /work_dir

# Pythonの依存関係をインストール
COPY requirements.txt .

RUN pip install --upgrade pip
