# Dynamic Dummy Mem Guard

A simple service to prevent Oracle Cloud AlwaysFree and similar cloud servers from being reclaimed due to "idle" state.

* Dynamically fills unused RAM with dummy memory.
* Releases memory instantly when needed by real applications.
* Includes systemd service integration, configuration file, CLI status command, and logging.
* Designed for cloud users who want to keep lightweight or rarely-accessed servers online without risking forced shutdown or resource reclamation.

## Features

* Auto-adjusts memory consumption to reach a specified threshold.
* Emergency release of dummy memory when overall usage exceeds a set limit.
* Easy configuration via `/etc/dynamic-dummy-mem/config.ini`.
* Status CLI: `dummy-mem-status` (with `watch` support)
* Logs important events to `/var/log/dynamic-dummy-mem/`.
* Easy installation: distributed as a `.deb` package, ready for service deployment.

## Installation

```
sudo apt install ./dynamic-dummy-mem_x.y.z_all.deb
sudo systemctl start dynamic-dummy-mem
sudo systemctl enable dynamic-dummy-mem
```

## Uninstallation

```
sudo apt remove dynamic-dummy-mem
```

## Status Check

```
dummy-mem-status
watch -n1 dummy-mem-status
```

## Configuration

Edit `/etc/dynamic-dummy-mem/config.ini` and restart the service.

## License

MIT License

## Author & Contact

Kannuki\_san
[GitHub Repository](https://github.com/Kannuki-san/dynamic-dummy-mem)

---

# Dynamic Dummy Mem Guard（日本語）

Oracle Cloud AlwaysFree など、クラウド無料枠サーバーの「アイドル判定によるリソース回収・停止」を防ぐためのシンプルなサービスです。

* 未使用RAMをダミーメモリで自動的に埋める
* 本当に必要な時は即座に解放
* systemdサービス、設定ファイル、CLIコマンド、ログ出力に対応
* 軽量用途や低頻度アクセスのサーバーを落とされたくない全クラウドユーザーに最適

## 主な特徴

* 設定したメモリ閾値まで自動調整
* メモリ使用率が高まった際の非常時全解放機能
* `/etc/dynamic-dummy-mem/config.ini` で簡単設定
* `dummy-mem-status` で状態確認（`watch` との併用可）
* 重要なイベントは `/var/log/dynamic-dummy-mem/` に記録
* `.deb` パッケージでインストールも簡単

## インストール

```
sudo apt install ./dynamic-dummy-mem_x.y.z_all.deb
sudo systemctl start dynamic-dummy-mem
sudo systemctl enable dynamic-dummy-mem
```

## アンインストール

```
sudo apt remove dynamic-dummy-mem
```

## 状態確認

```
dummy-mem-status
watch -n1 dummy-mem-status
```

## 設定

`/etc/dynamic-dummy-mem/config.ini` を編集後、サービスを再起動してください。

## ライセンス

MIT License

## 作者・連絡先

Kannuki\_san
[GitHubリポジトリ](https://github.com/Kannuki-san/dynamic-dummy-mem)
