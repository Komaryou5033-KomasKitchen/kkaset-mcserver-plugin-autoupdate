# セキュリティガイド

## パスワード認証 + IP アドレス接続について

### セキュリティのベストプラクティス

#### 1. 強力なパスワードを使用

推奨される強力なパスワードの例：

```
✅ 良い例
X9mK2$pL7wQ@nR4j
C8hJ1&dF5mN2#wT6

❌ 悪い例
password
123456
minecraft
admin
```

#### 2. 環境変数を使用（強く推奨）

パスワードを直接ファイルに記述する代わりに、環境変数を使用します：

```yaml
# config/servers.yaml
servers:
  lobby:
    rcon:
      password: "${RCON_PASSWORD}"  # 環境変数から取得
```

```bash
# 環境変数を設定
export RCON_PASSWORD="your_strong_password"
export SSH_PASSWORD="your_ssh_password"

# または .env ファイルに記述
# .env
RCON_PASSWORD=your_strong_password
SSH_PASSWORD=your_ssh_password
```

#### 3. RCON パスワード設定

Minecraftサーバーの設定（server.properties）：

```properties
enable-rcon=true
rcon.port=25575
rcon.password=YourStrongRconPassword123!
```

#### 4. リモートサーバー接続

選択肢：

**A. パスワード認証（シンプル）**

```yaml
type: "remote"
ip: "192.168.1.100"
username: "minecraft"
password: "${SSH_PASSWORD}"  # 環境変数から取得
```

**B. 秘密鍵認証（より安全）**

```yaml
type: "remote"
ip: "192.168.1.100"
username: "minecraft"
ssh_key: "${SSH_KEY_PATH}"  # 環境変数から取得
```

#### 5. ファイアウォール設定

RCON ポートを制限：

```bash
# ローカルネットワークのみアクセス許可
sudo ufw allow from 192.168.1.0/24 to any port 25575
```

## ハッキング対策

### 1. 定期的なパスワード変更

最低でも3ヶ月ごとにパスワードを変更してください。

### 2. RCON ポートの変更

デフォルトの 25575 から別のポートに変更：

```properties
rcon.port=19999
```

### 3. アクセス制限

SSH アクセスを IP アドレスで制限：

```bash
Match Address 192.168.1.0/24
  PasswordAuthentication yes
Match Address *
  PasswordAuthentication no
```

### 4. ログ監視

セキュリティログを定期的に確認：

```bash
tail -f logs/plugin_manager.log
```

## Discord Webhook セキュリティ

### Webhook URL の保護

Webhook URL を環境変数で管理：

```yaml
# config/servers.yaml
global:
  discord:
    webhook_url: "${DISCORD_WEBHOOK_URL}"
```

```bash
# .env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

## トラブルシューティング

### 「Connection refused」エラー

RCON が有効になっているか確認：

```properties
# server.properties
enable-rcon=true
rcon.port=25575
```

### 「Authentication failed」エラー

RCON パスワードが正しいか確認：

```bash
# テストコマンド
echo -n "rcon 25575 password list" | nc localhost 25575
```

（準備中）
