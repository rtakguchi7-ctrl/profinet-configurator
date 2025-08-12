# profinet-configurator

PROFINETスレーブのStation NameとIPアドレスをWeb UIから設定できるツールです。`profi-dcp` の `identify` 機能を使ってMACアドレスを自動検出する検索ボタンも搭載しています。

## 機能

- Station NameとIPアドレスの設定
- MACアドレスの自動検出（検索ボタン）
- NIC選択（eth-4 / eth-5）

## 起動方法

1. UC20-M3000にこのリポジトリをクローンまたはZIP展開
2. `docker-compose up --build` で起動
3. ブラウザで `http://<UC20-M3000のIP>:5000` にアクセス
