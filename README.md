# PROFINET Configurator

このコンテナは、Web UIからPROFINETスレーブのStation NameとIPアドレスを設定するためのツールです。`profi-dcp` の `identify` 機能を使ってMACアドレスを自動検出できます。

## 機能

- MACアドレスの自動検出（identify）
- Station NameとIPアドレスの設定（set-name, set-ip）

## 使用方法

1. `docker-compose up --build` で起動
2. ブラウザで `http://<UC20-M3000のIP>:5000` にアクセス
3. NICのIPアドレスを入力して「検索」ボタンを押すと、MACアドレスが検出されます
4. 検出されたMACアドレスを使ってStation NameやIPアドレスを設定できます
