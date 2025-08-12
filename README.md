# profinet-configurator

このコンテナは、UC20-M3000上でPROFINETスレーブのStation NameとIPアドレスをWeb UIから設定するためのツールです。

## 構成

- FlaskベースのWeb UI
- `profi-dcp`ライブラリによるDCP通信
- Dockerfileとdocker-composeによるPortainer対応

## 使用方法

1. GitHubにこのフォルダをアップロード
2. Portainerで「GitHubからStackを作成」
3. UC20-M3000のNIC名（例: `eth0`）を確認して `app.py` に反映

## 注意

- `network_mode: host` と `privileged: true` が必要です
- `profi-dcp` はPROFINET DCP通信を行うためのPythonライブラリです
