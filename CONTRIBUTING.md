# コントリビューションガイドライン

このプロジェクトへの貢献を歓迎します！以下のガイドラインに従ってください。

## 開発環境のセットアップ

1. リポジトリをフォーク
2. ローカルにクローン
```bash
git clone https://github.com/yourusername/slide-capture-tool.git
cd slide-capture-tool
```

3. 仮想環境を作成（推奨）
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

4. 依存関係をインストール
```bash
pip install -r requirements.txt
```

## 貢献の方法

### バグ報告
- GitHubのIssuesを使用してバグを報告してください
- バグの再現手順を明確に記述してください
- 使用している環境（OS、Pythonバージョンなど）を記載してください

### 新機能の提案
- まずIssuesで新機能について議論してください
- 実装前に合意を得ることを推奨します

### プルリクエスト
1. 新しいブランチを作成
```bash
git checkout -b feature/new-feature
```

2. コードを変更
3. テストを実行（該当する場合）
4. コミットメッセージは明確に
5. プルリクエストを作成

## コーディング規約

- PEP 8に従ってください
- 関数とクラスにはdocstringを追加してください
- 変数名は分かりやすく命名してください
- 日本語コメントも歓迎します

## テスト

現在、自動テストはありませんが、以下を手動で確認してください：

- 基本的な機能が動作すること
- 異なる設定値でも動作すること
- エラーハンドリングが適切であること

## リリースプロセス

1. バージョン番号を更新
2. CHANGELOG.mdを更新
3. タグを作成
4. GitHubリリースを作成

## 質問

質問がある場合は、GitHubのIssuesまたはDiscussionsを使用してください。
