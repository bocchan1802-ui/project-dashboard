# 🎩 ぼっちゃんプロジェクト管理ダッシュボード

マスターのためのプロジェクト管理ダッシュボード

## 機能

- 📊 **プロジェクト一覧**: タイル形式で見やすく表示
- 🏷️ **ステータス管理**: 完了/進行中/計画中
- 🔗 **URL表示**: 公開URLをワンクリックでアクセス
- 💬 **コメント**: 各プロジェクトにコメント追加可能
- 📱 **レスポンシブ**: モバイル対応

## デプロイ方法

### Cloudflare Pagesでホストする場合

1. GitHubにpush
2. Cloudflare Dashboard → Pages → 「プロジェクトを作成」
3. GitHubリポジトリを選択
4. フレームワークプリセット: なし（静的サイト）
5. ビルドコマンド: （空）
6. 出力ディレクトリ: `/`
7. 「保存してデプロイ」

## プロジェクト追加方法

`index.html`内の`projects`配列に追加：

```javascript
{
    id: 9,
    title: "🚀 新しいプロジェクト",
    description: "プロジェクトの説明",
    status: "in-progress", // completed, in-progress, planned
    tags: ["Tag1", "Tag2"],
    links: [
        { type: "primary", label: "🚀 公開URL", url: "https://..." },
        { type: "secondary", label: "📁 GitHub", url: "https://github.com/..." }
    ],
    comments: [
        { text: "コメント内容", date: "2026-02-12" }
    ]
}
```

## 現在のプロジェクト

| プロジェクト | ステータス | URL |
|------------|-----------|-----|
| 🎮 エフェクト満載テトリス | ✅ 完了 | https://856ecba9.tetris-effects.pages.dev |
| 🤖 Telegram ボイスチャットボット | ✅ 完了 | @keiichiclawdbot |
| 🎨 ゲームプロンプト生成システム | ✅ 完了 | - |
| 📰 AIニュース監視システム | ✅ 完了 | - |
| 🔧 Codex CLI セットアップ | ✅ 完了 | - |
| ☁️ Cloudflare環境構築 | ✅ 完了 | - |
| 🎙️ Voicevox セットアップ | ✅ 完了 | - |
| 📱 iOS React Native 音声アプリ | 📋 計画中 | - |

## 技術スタック

- HTML5
- CSS3 (Flexbox/Grid, backdrop-filter)
- Vanilla JavaScript
- Google Fonts (Noto Sans JP)
