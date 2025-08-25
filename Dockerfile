# ベースイメージ（例: Python 3.10）
FROM python:3.10-slim

# 作業ディレクトリの作成
WORKDIR /app

# 必要なファイルをコピー
COPY . /app

# 依存パッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# ポート開放（Flaskアプリ用）
EXPOSE 5050

# gunicornでFlaskアプリを起動
CMD ["gunicorn", "-b", "0.0.0.0:5050", "app:app"]
