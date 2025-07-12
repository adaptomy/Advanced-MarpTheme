---
marp: true
theme: custom
size: 4:3
paginate: true
---

<!-- _class: title -->

# カスタムCSS早見表

全スタイル・コンポーネント完全ガイド
2025年7月11日

---

<!-- _class: agenda -->

# 目次

<div class="step-nav">
  <div class="step-box active">01</div>
  <div class="step-arrow active"></div>
  <span class="step-text">タイトル・目次スライド</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">02</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">見出しとテキストスタイル</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">03</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">リストとボックス要素</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">04</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">テーブルとデータ表示</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">05</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">ナビゲーション要素</span>
</div>

---

<!-- _class: agenda -->

# 目次

<div class="step-nav">
  <div class="step-box inactive">06</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">グラフ・チャート（組み合わせ）</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">07</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">特殊要素</span>
</div>

---

<div class="chapter-number">02</div>

# 見出しとテキストスタイル

## このページでは全ての見出しレベルを確認できます

### 小見出し（H3）はこのようなスタイルです

通常のテキストはこのような表示になります。日本語フォント（Noto Sans JP）が適用され、読みやすい行間で表示されます。

**太字テキスト**や*斜体テキスト*、`インラインコード`なども使用可能です。

> 引用テキストも美しく表示されます。重要なポイントを強調する際に使用してください。

---

<div class="chapter-number">03-1</div>

# リストとボックス要素

## 箇条書きリスト

- 第一レベルの箇条書き項目
- もう一つの重要なポイント
  - ネストされた項目（第二レベル）
  - 別のサブ項目
- 最後の主要項目

## 番号付きリスト

1. 最初のステップ
2. 次のプロセス
3. 最終段階
   1. サブステップA
   2. サブステップB

---

<div class="chapter-number">03-2</div>

# ボックス要素とハイライト

## 基本のハイライトボックス

<div class="box">
環境への取り組み
</div>

- CO2削減目標の達成
- 再生可能エネルギーの活用
- サーキュラーエコノミーの推進

<div class="custom-block info">
重要なアナウンス
</div>

- 新製品リリース情報
- 業績ハイライト
- 戦略的パートナーシップ

---

## 💁メッセージの表示

<div class="center-content">
<h1>インパクトあるメッセージを書こう！</h1>
</div>

---

<div class="chapter-number">04-1</div>

# テーブルとデータ表示

## 基本的なテーブル

| 製品カテゴリ | Q1売上 | Q2売上 | Q3予想 | 成長率 |
|--------------|--------:|--------:|--------:|--------:|
| **ソフトウェア** | 850 | 926 | 975 | +5.0% |
| モバイルアプリ | 580 | 621 | 660 | +6.1% |
| Webサービス | 180 | 194 | 200 | +3.0% |
| **ハードウェア** | 650 | 682 | 687 | +0.7% |
| IoTデバイス | 160 | 180 | 200 | +10.7% |

---

<div class="chapter-number">04-2</div>

# より複雑なテーブル

## プロジェクト進捗データ

| タスク | 単位 | 計画 | 実績 | 進捗率 | 完了予定 | ステータス |
|--------|:------:|------:|------:|--------:|:----------:|:------------:|
| **設計** | 時間 | 240 | 220 | 92% | 完了 | ✅ |
| **開発** | 時間 | 480 | 360 | 75% | 7月末 | 🔄 |
| **テスト** | 時間 | 160 | 80 | 50% | 8月中旬 | ⏳ |
| **リリース** | - | - | - | 0% | 8月末 | 📅 |
| **ドキュメント** | ページ | 50 | 35 | 70% | 9月初旬 | 📝 |

---

<div class="chapter-number">05-1</div>

# ナビゲーション要素

## ステップナビゲーションの様々な状態

### アクティブ状態
<div class="step-nav">
  <div class="step-box active">01</div>
  <div class="step-arrow active"></div>
  <span class="step-text">現在進行中のフェーズ</span>
</div>

### 非アクティブ状態
<div class="step-nav">
  <div class="step-box inactive">02</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">今後実施予定のフェーズ</span>
</div>

### 完了状態
<div class="step-nav">
  <div class="step-box active">✓</div>
  <div class="step-arrow active"></div>
  <span class="step-text completed">完了済みフェーズ</span>
</div>

---

<div class="chapter-number">05-2</div>

# 進捗表示とコンビネーション

## 複数の進捗表示

<div class="progress-container">
  <div class="progress-text">🎯 第1四半期の達成状況</div>
</div>

<div class="step-nav">
  <div class="step-box active">Q1</div>
  <div class="step-arrow active"></div>
  <span class="step-text">市場調査・競合分析</span>
</div>

<div class="step-nav">
  <div class="step-box active">Q2</div>
  <div class="step-arrow active"></div>
  <span class="step-text">製品開発・プロトタイプ</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">Q3</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">マーケティング戦略</span>
</div>

<div class="step-nav">
  <div class="step-box inactive">Q4</div>
  <div class="step-arrow inactive"></div>
  <span class="step-text">商用化・市場投入</span>
</div>

---

<div class="chapter-number">06</div>

# 混合レイアウト例

## データとハイライトの組み合わせ

### 主要パフォーマンス指標

<div class="custom-block success">
ユーザー満足度: 95%
</div>

| 指標 | 目標 | 実績 | 達成率 |
|-----|------|------|--------|
| 月間アクティブユーザー | 10,000 | 12,500 | **125%** |
| システム稼働率 | 99.5% | 99.8% | **100%** |

---

<div class="box blue">
目標を大幅に上回る成果
</div>

### 今後の重点施策

1. **技術基盤の強化**
   - クラウドインフラの最適化
   - セキュリティ強化対策

2. **ユーザーエクスペリエンス向上**
   - UI/UXの改善
   - モバイル対応の強化

---

<div class="chapter-number">07</div>

# 特殊要素とコード表示

## インラインコードとコードブロック

CSS変数の使用例：`var(--ff-accent)`

```css
/* カスタム変数 */
:root {
  --ff-accent: #009944;
  --ff-bg: #ffffff;
  --ff-text: #333333;
}

/* 使用例 */
.highlight {
  color: var(--ff-accent);
  background: var(--ff-bg);
}
```

---

<div class="chapter-number">06</div>

# グラフ・チャート

## 統計ボックス + 棒グラフ組み合わせ例

<div class="stats-grid compact">
  <div class="stat-box compact">
    <span class="stat-number compact">12,500</span>
    <div class="stat-label compact">月間アクティブユーザー</div>
    <div class="stat-change compact positive">+25.3% ↗</div>
  </div>
  
  <div class="stat-box compact">
    <span class="stat-number compact">99.8%</span>
    <div class="stat-label compact">システム稼働率</div>
    <div class="stat-change compact positive">+0.3% ↗</div>
  </div>
</div>

<div class="chart-title compact">月間パフォーマンス</div>

<div class="bar-chart flexible">
  <div class="bar bar1" style="height: 60%;">
    <div class="bar-value">60</div>
    <div class="bar-label">1月</div>
  </div>
  <div class="bar bar2" style="height: 80%;">
    <div class="bar-value">80</div>
    <div class="bar-label">2月</div>
  </div>
  <div class="bar bar3" style="height: 45%;">
    <div class="bar-value">45</div>
    <div class="bar-label">3月</div>
  </div>
  <div class="bar bar4" style="height: 90%;">
    <div class="bar-value">90</div>
    <div class="bar-label">4月</div>
  </div>
</div>

---

<div class="chapter-number">06-2</div>

# 統計ボックス単独使用例

## 重要指標のハイライト表示

<div class="stats-grid">
  <div class="stat-box">
    <span class="stat-number">15,840</span>
    <div class="stat-label">月間アクティブユーザー</div>
    <div class="stat-change positive">+18.2% ↗</div>
  </div>
  
  <div class="stat-box">
    <span class="stat-number">99.9%</span>
    <div class="stat-label">システム稼働率</div>
    <div class="stat-change positive">+0.1% ↗</div>
  </div>
  
  <div class="stat-box">
    <span class="stat-number">3.2sec</span>
    <div class="stat-label">平均応答時間</div>
    <div class="stat-change negative">+0.2sec ↗</div>
  </div>
  
  <div class="stat-box">
    <span class="stat-number">97%</span>
    <div class="stat-label">ユーザー満足度</div>
    <div class="stat-change positive">+3% ↗</div>
  </div>
</div>

---

<div class="chapter-number">06-3</div>

# 棒グラフ単独使用例

<div class="chart-title">四半期業績推移</div>
<div class="chart-subtitle">2024年度売上実績（単位：百万円）</div>

<div class="bar-chart">
  <div class="bar bar1" style="height: 65%;">
    <div class="bar-value">650</div>
    <div class="bar-label">Q1</div>
  </div>
  <div class="bar bar2" style="height: 85%;">
    <div class="bar-value">850</div>
    <div class="bar-label">Q2</div>
  </div>
  <div class="bar bar3" style="height: 50%;">
    <div class="bar-value">500</div>
    <div class="bar-label">Q3</div>
  </div>
  <div class="bar bar4" style="height: 95%;">
    <div class="bar-value">950</div>
    <div class="bar-label">Q4<br>（予想）</div>
  </div>
  <div class="bar bar5" style="height: 74%;">
    <div class="bar-value">738</div>
    <div class="bar-label">平均</div>
  </div>
</div>

---

<div class="chapter-number">07</div>

# 特殊要素とコード表示

## 特殊文字と絵文字

- ✅ 完了項目
- ⚠️ 注意が必要
- 📊 データ分析
- 🎯 目標設定
- 🚀 成長戦略

---

<!-- _class: title -->

<div class=center-content>
<h1>以上で案内は終了です</h1>
</div>