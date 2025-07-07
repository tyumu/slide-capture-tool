# スライド動画自動キャプチャツール

動画からスライドの変化を自動検出し、スライドごとに画像として保存するPythonツールです。

## 機能

- 動画のスライド変化を自動検出
- スライドに書き込みがある場合でも適切にキャプチャ
- 実行ごとに新しいフォルダを作成して整理
- 設定可能な類似度閾値と検出パラメータ
- 履歴機能により書き込み前の状態を保存

## 必要な環境

- Python 3.7以上
- Google Chrome ブラウザ
- Windows/macOS/Linux

## インストール

1. このリポジトリをクローンまたはダウンロード
```bash
git clone https://github.com/yourusername/slide-capture-tool.git
cd slide-capture-tool
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

## 使用方法

1. **設定の編集**
   - `slide_capture.py`を開き、`VIDEO_URL`に対象の動画URLを設定
   - 必要に応じて他の設定項目も調整

2. **実行**
```bash
python slide_capture.py
```

3. **操作手順**
   - ブラウザが自動で開きます
   - 動画を再生し、フルスクリーンなど最適な表示状態にします
   - コンソールでEnterキーを押して監視を開始
   - Ctrl+Cで監視を終了

## 設定項目

### 基本設定
- `VIDEO_URL`: 対象の動画URL
- `OUTPUT_DIR`: 画像保存先フォルダ名
- `SIMILARITY_THRESHOLD`: 類似度閾値（0.0-1.0、推奨値0.75-0.85）
- `CHECK_INTERVAL_SECONDS`: チェック間隔（秒）

### 高度な設定
- `CROP_BOX`: 比較範囲の指定（動画の再生バーなどを除外）
- `HISTORY_SECONDS`: 履歴保存時間（秒）
- `MAX_HISTORY_FRAMES`: 履歴の最大フレーム数
- `CHANGE_CONFIRMATION_COUNT`: 変化検出の確認回数

## 出力

画像は`slides_output/session_YYYYMMDD_HHMMSS/`フォルダに保存されます。

例：
```
slides_output/
├── session_20250707_141530/
│   ├── slide_001.png
│   ├── slide_002.png
│   └── slide_003.png
└── session_20250707_143020/
    ├── slide_001.png
    └── slide_002.png
```

## トラブルシューティング

### ChromeDriverのエラー
- 自動ダウンロードに失敗する場合は、手動でChromeDriverをダウンロードし、スクリプトと同じフォルダに配置してください
- [ChromeDriver公式サイト](https://chromedriver.chromium.org/)

### 検出精度の調整
- スライド変化が検出されない場合：`SIMILARITY_THRESHOLD`を下げる（0.70-0.80）
- 誤検出が多い場合：`SIMILARITY_THRESHOLD`を上げる（0.85-0.95）
- `CHANGE_CONFIRMATION_COUNT`を増やすと誤検出を減らせます

### メモリ使用量
- `MAX_HISTORY_FRAMES`を調整してメモリ使用量を制御できます

## 技術仕様

- **画像比較**: 構造的類似度指数（SSIM）を使用
- **WebDriver**: Selenium + ChromeDriver
- **画像処理**: OpenCV + scikit-image
- **対応フォーマット**: PNG形式で保存

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 更新履歴

- v1.0.0: 初回リリース
  - 基本的なスライド検出機能
  - 履歴機能
  - セッション別フォルダ作成

## 関連リンク

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [scikit-image Documentation](https://scikit-image.org/)
