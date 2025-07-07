# 変更履歴

このファイルは、プロジェクトの重要な変更を記録しています。

## [1.0.0] - 2025-07-07

### 追加
- 初回リリース
- 基本的なスライド検出機能
- SSIM（構造的類似度指数）を使用した画像比較
- Selenium WebDriverによるブラウザ自動化
- 履歴機能による書き込み前状態の保存
- セッション別フォルダ作成機能
- 設定可能な類似度閾値
- 変化検出の安定性向上機能
- ChromeDriverの自動ダウンロード機能
- 手動ChromeDriverフォールバック機能

### 機能
- 動画のスライド変化を自動検出
- PNG形式での画像保存
- 実行ごとの新しいフォルダ作成
- カスタマイズ可能な設定項目
- クロッピング機能（比較範囲指定）
- メモリ使用量制御
- 連続変化検出による誤検出防止

### 設定項目
- `VIDEO_URL`: 動画URL
- `OUTPUT_DIR`: 保存先フォルダ
- `SIMILARITY_THRESHOLD`: 類似度閾値（0.80）
- `CHECK_INTERVAL_SECONDS`: チェック間隔（1.0秒）
- `CROP_BOX`: 比較範囲指定
- `HISTORY_SECONDS`: 履歴保存時間（1.5秒）
- `MAX_HISTORY_FRAMES`: 最大履歴フレーム数（10）
- `CHANGE_CONFIRMATION_COUNT`: 変化確認回数（2回）

### 技術仕様
- Python 3.7+対応
- OpenCV 4.8.1.78
- Selenium 4.15.2
- scikit-image 0.21.0
- numpy 1.24.3
- webdriver-manager 4.0.1
