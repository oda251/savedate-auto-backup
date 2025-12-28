# 概要

ユーザが指定したフォルダ群を変更検知し、自動的にバックアップする Python プログラム

# 注意点
wslからでは動きません、windowsで直接動かします
macは未検証

# 使い方

## 前提

- python 実行環境がある（コマンド実行例は uv を使用）

## 準備 1: 依存ライブラリのインストール

```shell
uv venv
source .venv/bin/activate
uv pip install -r ./requirements.txt
```

## 準備 2: 個人用設定

target-files.yaml に

1. バックアップしたいフォルダ
2. バックアップ先のフォルダ

を記載する

```yaml
# Target folders to backup
"target-folders":
  # ---- ここを編集する ---
  # 書き方
  # {任意の名前}: {バックアップしたいフォルダのパス}
  "a-certein-game": "C:\\Users\\{user}\\AppData\\path\\to\\save\\folder"
  # ----------------------
# Destination folder for backups
# --- ここを編集する ---
# バックアップを記録する先のパスを指定
"backup-folder": "C:\\Users\\odada\\save-backup"
# ---
```

## 起動

```shell
uv run main.py
```

# プログラムの振る舞い

1. 起動
2. `target-folders.yaml`を読み込む
3. `target-folders`に記載のパスについて、フォルダ/ファイルの変更を監視
4. 変更のあったフォルダを`$backup-folder/{target-foldersのパラメータ名}/{変更のあった日時}`にコピー
