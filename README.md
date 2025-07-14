# Marp プレゼンテーションプロジェクト 基本ガイド

## 概要

Marp CLI ＋ カスタムCSS（`advanced`テーマ）で高速＆美しいMarkdownスライドを作成できるテンプレートです。

## プロジェクト構成

```
my-marp-project/
├── slides/              # スライド生成用Markdownファイル格納先
│   └── css-showcase.md  
├── themes/              # カスタムテーマファイル格納先
│   └── advanced.css
├── marp_converter_app/  # 配布用Marp変換ミニアプリ（Windows向け）
│   ├── generate-ppt.py  # Windows環境専用のGUI変換ツール
│   └── config.json      # 初回実行時に生成される設定ファイル
├── package.json         # プロジェクト設定
└── README.md           # このファイル
```

---

## 🚀 セットアップ手順

1. **依存インストール**
    ```sh
    npm install
    ```

2. **Marpテーマ・スライドディレクトリを必要に応じて編集**

---

## 🛠️ 主要スクリプト

| コマンド                   | 内容                                                    |
| -------------------------- | ------------------------------------------------------- |
| `npm run web`              | HTMLスライド一括出力（output/ 配下に出力）             |
| `npm run ppt`              | PowerPoint（.pptx）形式で出力                          |
| `npm run pdf`              | PDF形式で出力                                           |
| `npm run preview`          | ローカルでライブプレビュー（ホットリロード対応）        |
| `npm run ppt:win`          | Windows環境用PowerPoint出力                             |
| `npm run web:win`          | Windows環境用HTML出力                                   |

---

## 🪟 Windows向けGUIツール

`marp_converter_app/generate-ppt.py` は**Windows環境専用**のGUI変換ツールです。

### 特徴
- ファイル選択ダイアログで簡単操作
- テーマの自動検出と選択
- 出力先ディレクトリの設定
- Marp CLIの自動インストール機能
- 日本語対応

### 動作環境
- **Windows 10/11 専用**
- Python 3.7以降
- Node.js と npm がインストール済み

### 使用方法
1. `python generate-ppt.py` を実行
2. 初回は使用するテーマCSSファイルを選択
3. 変換したいMarkdownファイルを選択
4. 自動でPPTXファイルが生成されます

---

## 🎨 カスタムテーマ（advanced.css）の特徴

- フォントサイズや色をCSS変数で一元管理
- 見出し・リスト・テーブル・ボックス・カスタムブロック等の統一デザイン
- リストのネスト右ズレ抑制、チェックリスト（- [ ]）だけlist-style解除対応
- タイトル・h1～h3・p・ul/ol/li など、全て変数・クラスで細かく制御可
- Marpスライドをそのまま「美しいブランド資料」にできる汎用設計

---

## 📝 スライドの作り方

1. **slides/ にMarkdownファイルを追加**
    - 例: `slides/sample.md`

2. **テーマ指定**
    - マークダウン冒頭に  
      ```
      ---
      marp: true
      theme: advanced
      ---
      ```
      を記述

3. **コマンドで出力**
    - 例：`npm run web` でHTMLスライド一括生成

---

## 📐 カスタムCSSの主要ポイント抜粋

- サイズ・色・余白などは`themes/advanced.css`の`:root`で調整
- h2はデフォルトで左側に線を表示。`.no-bar`クラスでバーなしも可
- チェックリスト（- [ ]）だけlist-style解除＆左詰め
- クラスによる柔軟なフォントサイズ・配色コントロール（`.text-xl`等）

---

## 参考リンク

- [Marp公式ドキュメント](https://marp.app/)
- [Marpit CSS仕様](https://marpit.marp.app/theme-css)
- [Markdown記法ガイド](https://www.markdownguide.org/)

---

**作成日:** 2025年7月10日
**更新日:** 2025年7月14日
**バージョン:** 1.0.0