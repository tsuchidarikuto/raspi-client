# PortAudioライブラリエラーの解決方法

## エラー内容
```
ImportError: libportaudio.so.2: cannot open shared object file: No such file or directory
```

## 解決方法

### 1. セットアップスクリプトの実行
```bash
chmod +x setup-raspi.sh
./setup-raspi.sh
```

### 2. 手動でのライブラリインストール
```bash
# PortAudioライブラリをインストール
sudo apt-get update
sudo apt-get install -y portaudio19-dev libportaudio2 libportaudiocpp0

# ライブラリキャッシュを更新
sudo ldconfig
```

### 3. シンボリックリンクの作成
```bash
# アーキテクチャに応じたパスでリンクを作成
sudo ln -sf /usr/lib/$(uname -m)-linux-gnu/libportaudio.so /usr/lib/$(uname -m)-linux-gnu/libportaudio.so.2
```

### 4. ライブラリパスの設定
```bash
# 一時的な解決策
export LD_LIBRARY_PATH=/usr/lib/$(uname -m)-linux-gnu:$LD_LIBRARY_PATH

# 永続的な解決策（.bashrcに追加）
echo 'export LD_LIBRARY_PATH=/usr/lib/$(uname -m)-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 5. PyAudioのシステムパッケージ使用
```bash
# pipではなくaptでPyAudioをインストール
sudo apt-get install -y python3-pyaudio
```

### 6. それでも解決しない場合
1. システムを再起動
   ```bash
   sudo reboot
   ```

2. ライブラリの再インストール
   ```bash
   sudo apt-get install --reinstall libportaudio2
   ```

3. インストールされているライブラリの確認
   ```bash
   # PortAudioライブラリの場所を確認
   find /usr -name "libportaudio*" 2>/dev/null
   
   # 動的リンクの依存関係を確認
   ldd $(python3 -c "import _portaudio; print(_portaudio.__file__)")
   ```

## 注意事項
- Raspberry Piのアーキテクチャ（armhf/aarch64）によってライブラリパスが異なる場合があります
- `python3-pyaudio`パッケージを使用することで、コンパイル関連の問題を回避できます
- 仮想環境を使用している場合は、システムパッケージへのアクセスを許可する必要があります