# インストールガイド

## 要件

- Python 3.9 以上
- pip (Pythonパッケージマネージャー)
- Git
- RCON が有効なMinecraftサーバー

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate.git
cd kkaset-mcserver-plugin-autoupdate
```

### 2. 仮想環境の作成（推奨）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 設定ファイルのセットアップ

```bash
# config/servers.yaml.example をコピー
cp config/servers.yaml.example config/servers.yaml

# config/servers.yaml を編集
vi config/servers.yaml
```

### 5. 環境変数の設定（オプション）

```bash
cp .env.example .env

# .env を編集
vi .env
```

## 実行

### Web UI の起動

```bash
python src/main.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

### 初期設定

```bash
python src/main.py --setup
```

### 手動更新チェック

```bash
python src/main.py --check
```

## トラブルシューティング

### "ModuleNotFoundError: No module named 'flask'"

すべての依存パッケージがインストールされていることを確認してください：

```bash
pip install -r requirements.txt
```

### "FileNotFoundError: Config file not found"

config/servers.yaml が存在することを確認してください：

```bash
cp config/servers.yaml.example config/servers.yaml
```

## 次のステップ

- [設定ガイド](./configuration.md) を読んで、サーバーを設定してください
- [セキュリティガイド](./security.md) を確認して、安全にセットアップしてください
