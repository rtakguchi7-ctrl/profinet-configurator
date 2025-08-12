# PROFINET Configurator

このアプリは、Web UIからPROFINETスレーブのStation NameとIPアドレスを設定するためのFlaskベースのツールです。`profi-dcp` CLIを内部で呼び出して設定を行います。

## 使用方法

1. MACアドレス、Station Name、IPアドレス、サブネットマスク、ゲートウェイ、NIC名（eth-4 または eth-5）を入力
2. 「送信」ボタンを押すと、設定がDCPパケットで送信されます

## 起動方法

1. `docker-compose.yml` を使ってコンテナをビルド・起動します：
   docker-compose up --build
2. ブラウザで http://<UC20-M3000のIP>:5000 にアクセス
