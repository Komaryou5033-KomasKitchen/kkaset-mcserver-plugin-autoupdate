# 🎮 KKASET Minecraft Plugin Auto-Update

## 現在開発中です（v0.1.0）

Minecraft サーバーのプラグイン・MOD を自動で検出し、更新通知を行い、管理者の承認後に自動で更新するツール。

Paper、Spigot、Forge、Fabric、Arclight、Mohist、BungeeCord、Velocity に対応し、バージョン 1.12.2 から最新版まで利用可能です。

## ✨ 主な機能

- 🔍 **自動検出**: インストール済みプラグイン/MOD を自動スキャン
- 📦 **複数リポジトリ対応**: SpigotMC、Bukkit、Modrinth、CurseForge、Hangar から最新版を自動取得
- 🔔 **更新通知**: Discord、コンソール出力で更新をお知らせ
- ✅ **管理者承認**: Web UI で分かりやすく更新を確認・承認
- 🚀 **自動更新**: 承認後、自動でダウンロード・インストール・再起動
- 🌐 **複数サーバー対応**: 同一マシン、リモートマシン両対応
- 💾 **自動バックアップ**: 更新前に自動でバックアップを作成
- 🖥️ **Web UI**: ブラウザで簡単管理

## 🎯 対応環境

### Minecraftサーバータイプ
- ✅ Paper / Spigot
- ✅ Forge / Fabric
- ✅ Arclight / Mohist
- ✅ BungeeCord / Velocity

### バージョン
- ✅ 1.12.2 ～ 最新版（26.1.2以降も対応予定）

### デプロイ方式
- ✅ 同一マシン上のサーバー
- ✅ リモートマシン上のサーバー（SSH接続）

## 📋 要件

- Python 3.9+
- RCON が有効なMinecraftサーバー
- （オプション）SSH アクセス（リモートサーバーの場合）
- （オプション）Discord Webhook URL（通知機能）

## 🚀 クイックスタート

### インストール

```bash
git clone https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate.git
cd kkaset-mcserver-plugin-autoupdate
pip install -r requirements.txt
```

### 初期設定

```bash
python src/main.py --setup
```

### 実行

```bash
python src/main.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

## 📝 設定ファイル（config/servers.yaml）

```yaml
servers:
  lobby:
    name: "ロビー"
    version: "1.21.6"
    server_type: "paper"
    type: "local"
    plugin_path: "/opt/minecraft/lobby/plugins"
    rcon:
      enabled: true
      host: "localhost"
      port: 25575
      password: "rcon_password"
    auto_restart: true
    notification:
      discord: true
      console: true
```

詳細は [設定ガイド](./docs/configuration.md) を参照してください。

## 🌐 Web UI

```
http://localhost:5000/
```

- サーバーの状態確認
- 更新待機中のプラグイン確認・承認
- 手動更新チェック
- バックアップ管理
- ログ表示

## 📦 サポートするプラグインソース

- **SpigotMC**: https://www.spigotmc.org/
- **Bukkit**: https://dev.bukkit.org/
- **Modrinth**: https://modrinth.com/
- **CurseForge**: https://www.curseforge.com/
- **Hangar** (Paper): https://hangar.papermc.io/

## 🔐 セキュリティについて

- RCON 接続はパスワード認証で保護されます
- リモートサーバー接続は SSH で暗号化されます
- 設定ファイル内のパスワードは **環境変数** の使用を強く推奨します

詳細は [セキュリティガイド](./docs/security.md) を参照してください。

## 📚 ドキュメント

- [インストールガイド](./docs/installation.md)
- [設定ガイド](./docs/configuration.md)
- [セキュリティガイド](./docs/security.md)
- [トラブルシューティング](./docs/troubleshooting.md)
- [API リファレンス](./docs/api_reference.md)

## 🤝 貢献

バグ報告や機能リクエストは [Issues](https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate/issues) をご利用ください。

プルリクエストも大歓迎です！

## 💰 Patreon

より早い更新や先行版を希望される方は、Patreon をご検討ください。

[Komaryou5033 on Patreon](https://www.patreon.com/cw/Komaryou5033)

## 📄 ライセンス

Komaryou5033 Custom License (KCL) - 詳細は [LICENSE](./LICENSE) を参照してください。

本ソフトウェアは商用・非商用を問わず自由に利用できます。再配布の際は、可能であれば公式配布をお願いします。

## 📞 サポート

- 🐛 バグ報告: [Issues](https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate/issues)
- 💬 質問: [Discussions](https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate/discussions)
- 🎮 Discord: お持ちのサーバーをお知らせください

---

**Made with ❤️ by Komaryou5033**
