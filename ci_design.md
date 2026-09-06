# CI Design

## 背景

このリポジトリは、PDF / OfficeファイルをMarkdownへ変換するPython CLIプロジェクトです。

CIは本業で利用する前の学習・検証を目的として、まずは最小限のチェックをGitHub Actions上で動かします。個人開発のため、最初から多くのツールを入れすぎず、失敗理由を追いやすい構成にします。

## 目的

- GitHub ActionsでCIがどのように動くかを実際に確認する。
- 個別ブランチから`develop`へPull Requestを出したときに、自動チェックが走る状態にする。
- コード品質、単体テスト、Dockerビルド、シークレット混入の基本的な検知を体験する。

## 対象ブランチ

CIの主な実行契機は、個別ブランチから`develop`へのPull Request作成・更新です。

現在の作業ブランチは`add_no_sdk`です。

```yaml
on:
  pull_request:
    branches:
      - develop
```

必要に応じて、手動実行もできるように`workflow_dispatch`を追加します。

```yaml
on:
  pull_request:
    branches:
      - develop
  workflow_dispatch:
```

## 実行環境

- CIサービス: GitHub Actions
- Runner: GitHub-hosted Runner
- OS: `ubuntu-latest`
- Python: Dockerfileのベースイメージに合わせて`3.12`
- パッケージインストール: `requirements.txt`

## CIでチェックする項目

### 1. コードチェック

Pythonの静的なコードチェックには`ruff`を使います。

理由:

- Pythonのlintツールとして導入しやすい。
- 実行が速い。
- 後述のフォーマットチェックも同じツールで扱える。

想定コマンド:

```bash
ruff check .
```

### 2. コードフォーマット

フォーマットチェックにも`ruff format`を使います。

CIでは自動修正ではなく、フォーマット済みかどうかだけを確認します。

想定コマンド:

```bash
ruff format --check .
```

### 3. 型チェック

型チェックには`mypy`を使います。

最初は厳しすぎる設定にせず、`src/`配下を対象にします。外部ライブラリの型定義不足で詰まりすぎる場合は、段階的に設定を調整します。

想定コマンド:

```bash
mypy src --ignore-missing-imports
```

最初は`--ignore-missing-imports`を付け、外部ライブラリ側の型情報不足ではCIを落としにくくします。慣れてきたら`pyproject.toml`に設定を移し、段階的に厳しくします。

## テスト

### 単体テスト

単体テストには`pytest`を使います。

現時点では`tests/`ディレクトリがないため、CI導入時に最小限のテストを追加します。

まずは外部ファイル変換やMarkItDown本体に強く依存しない処理からテスト対象にします。これは、PDFやOfficeファイルの変換結果そのものではなく、入力に対して結果が決まりやすい小さな処理を先に確認するという意味です。

候補:

- 出力パス生成処理
- 入力ファイル探索処理
- Markdownへの画像リンク追加処理
- 設定値のバリデーション処理

想定コマンド:

```bash
pytest
```

## ビルド

### Dockerfileのベストプラクティスチェック

Dockerfileの静的チェックには`hadolint`を使います。

想定コマンド:

```bash
hadolint .devcontainer/Dockerfile
```

Dockerfileは`.devcontainer/Dockerfile`を対象にします。

### Dockerfileがビルドできるか

GitHub Actions上でDockerイメージをビルドします。

想定コマンド:

```bash
docker build -t markitdown-ci -f .devcontainer/Dockerfile .
```

### docker runで問題が発生しなそうか

ビルドしたイメージを使って、最低限の起動確認をします。

CLIプロジェクトなので、まずはヘルプ表示やバージョン表示のような副作用の小さいコマンドを確認対象にするのが扱いやすいです。

候補:

```bash
docker run --rm markitdown-ci python src/main.py --help
```

現在のCLIに`--help`がある場合はそれを使い、なければ追加を検討します。

## セキュリティスキャン

### シークレットスキャン

シークレット混入検知には`gitleaks`を使います。

想定コマンド:

```bash
gitleaks detect --source . --no-git
```

学習用途では、最初は標準ルールで検知の動きを確認します。誤検知が出た場合は、`.gitleaks.toml`で除外ルールを追加します。

## 推奨するWorkflow構成

最初は1つのWorkflowファイルにまとめます。

ファイル:

```text
.github/workflows/ci.yml
```

Jobは学習しやすいように、以下のように分けます。

```text
ci.yml
├── python-check
│   ├── 依存関係インストール
│   ├── ruff check
│   ├── ruff format --check
│   ├── mypy
│   └── pytest
├── docker-check
│   ├── hadolint
│   ├── docker build
│   └── docker run
└── secret-scan
    └── gitleaks
```

Jobを分ける理由:

- どの種類のチェックで失敗したかがGitHub上で見やすい。
- Pythonチェック、Dockerチェック、セキュリティスキャンを独立して理解しやすい。
- 将来的に必要なJobだけを調整しやすい。

## 導入時に追加・変更する想定ファイル

```text
.github/workflows/ci.yml
pyproject.toml
requirements-dev.txt
tests/
```

必要に応じて追加:

```text
.dockerignore
.gitleaks.toml
```

## Python開発用ツールの管理方針

現在の`requirements.txt`はアプリ実行用の依存関係を管理しています。

CI用の開発依存関係は、`requirements-dev.txt`という新しいファイルを追加して管理します。

`requirements-dev.txt`は、アプリを動かすためではなく、開発・CIで使うツールを入れるための依存ファイルです。

```text
ruff
mypy
pytest
```

`requirements.txt`は実行用、`requirements-dev.txt`は開発・CI用、と分けることで役割が分かりやすくなります。

`ruff`や`mypy`の細かい設定は、別途`pyproject.toml`に置きます。

## 段階導入プラン

### Step 1: Pythonチェックと単体テスト

最初に以下を導入します。

- `ruff check`
- `ruff format --check`
- `mypy src`
- `pytest`

この段階で、CIの基本的な流れを確認します。

### Step 2: Dockerチェック

次に`.devcontainer/Dockerfile`を使って、以下をCIに含めます。

- `hadolint .devcontainer/Dockerfile`
- `docker build`
- `docker run`

Dockerfileの場所が`.devcontainer/`配下なので、CIでは`-f .devcontainer/Dockerfile`を指定してビルドします。

### Step 3: シークレットスキャン

最後に`gitleaks`を追加します。

標準ルールで動かし、誤検知や検知対象を確認します。

## 最初のCI完成イメージ

Pull Requestを`develop`向けに作成・更新すると、GitHub Actionsで以下が実行されます。

```text
python-check
  OK: ruff check
  OK: ruff format --check
  OK: mypy src
  OK: pytest

docker-check
  OK: hadolint Dockerfile
  OK: docker build
  OK: docker run

secret-scan
  OK: gitleaks
```

すべて成功したら、最低限の品質確認が通った状態として`develop`へマージできるようにします。

## 不明点・確認したいこと

現時点で確認したい点は以下です。

1. CIで使うPythonバージョンは、Dockerfileに合わせて`3.12`とする。
2. 開発依存関係は`requirements-dev.txt`で管理する。
3. `mypy`は最初から厳格にせず、導入しやすい設定から始める。
4. 単体テストは、まずMarkItDown本体を呼ばない処理から作成する。
