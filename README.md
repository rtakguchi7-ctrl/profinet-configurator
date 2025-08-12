# PROFINET Configurator

UC20-M3000上でPROFINETスレーブのStation NameとIPアドレスをWeb UIから設定するためのコンテナです。

## 使用方法

1. PortainerでGitHubからStackを作成
2. Web UIにアクセス（http://<UC20-M3000のIP>:5000）
3. MACアドレス、Station Name、IPアドレスなどを入力
4. 使用するNIC（eth-4 または eth-5）を選択
5. 「送信」で設定を適用

## 注意

- UC20-M3000のNIC名に合わせて `eth-4` または `eth-5` を選択してください。
- `network_mode: host` と `privileged: true` が必要です。
