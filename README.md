# 📝 Flask TODOリストアプリケーション

このアプリケーションは、FlaskとSQLiteを使って構築されたシンプルなTODOリスト管理ツールです。タスクの追加、編集、削除、並べ替え、完了管理が可能です。

## 🚀 特徴

- タスクの追加・編集・削除
- タスクの締切、重要度の設定
- タスク完了チェックと完了日管理
- タスクの並べ替え（ドラッグ＆ドロップ前提）
- 完了タスクの一括削除
- エラーハンドリング（404ページ）

## 🛠 使用技術

- Python 3
- Flask
- SQLite3
- HTML/Jinja2テンプレート
- JavaScript (フロントエンドでの並べ替え等を想定)
- Renderへのデプロイを前提とした構成（`/opt/render/` ディレクトリ）

## 📂 ディレクトリ構成（想定）

```
.
├── app.py
├── templates/
│   ├── index.html
│   ├── add.html
│   ├── edit.html
│   └── 404.html
└── todo.db （実行時に自動作成）
```

## ⚙️ セットアップ方法

1. リポジトリをクローン：
    ```bash
    git clone https://github.com/yourusername/todo-flask-app.git
    cd todo-flask-app
    ```

2. 仮想環境を作成・有効化（任意）：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. 必要なパッケージをインストール：
    ```bash
    pip install Flask
    ```

4. アプリを起動：
    ```bash
    python app.py
    ```

5. ブラウザで開く：
    ```
    http://localhost:5000
    ```

## 🔧 APIエンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| `GET`   | `/`  | タスク一覧表示 |
| `GET/POST` | `/add` | 新規タスクの追加 |
| `GET/POST` | `/edit/<task_id>` | タスク編集 |
| `POST`  | `/update_order` | タスクの並び順を更新 |
| `DELETE` | `/delete_task/<task_id>` | 単一タスクの削除 |
| `DELETE` | `/delete_completed_tasks` | 完了済みタスクの一括削除 |
| `POST` | `/complete_task` | タスクの完了状態を切替（JSON） |
| `POST` | `/complete` | タスクを完了に設定（フォーム） |

## 🗃 データベース構造

テーブル名：`task`

| カラム名 | 型 | 説明 |
|----------|----|------|
| `id` | INTEGER | 主キー（自動採番） |
| `title` | TEXT | タスクのタイトル |
| `memo` | TEXT | メモ |
| `deadline` | TEXT | 締切日 |
| `important` | INTEGER | 重要度（0 or 1） |
| `created_at` | TEXT | 作成日時 |
| `updated_at` | TEXT | 更新日時 |
| `position` | INTEGER | 並び順 |
| `completed_at` | TEXT | 完了日時（NULLなら未完了） |

## 🖥 Renderへのデプロイについて

Renderの永続化ディレクトリ `/opt/render/` に対応するように、SQLiteの保存パスを設定しています。デプロイ時には環境変数などに応じてパスの調整が必要です。
