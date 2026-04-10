# dominai trader journal 要件定義（MVP）

## 1. 全体方針
- プロダクト名は定数化し、将来変更しやすくする。
- 価値の中心は「記録」ではなく「定量分析と改善アクション抽出」。
- 設計順序は **設計 → 実装 → テスト → 修正 → ドキュメント更新**。
- MVPは single-user mode 前提だが、DBは multi-user 拡張可能な構造にする。

## 2. ユーザー課題
- 勝率だけでは判断が歪む（平均勝ち・平均負け・PF等が見えない）。
- 時間帯・銘柄・タグ別の癖が把握できない。
- 反省（レビュー）が次回トレードへ接続されない。

## 3. MVP対象機能
1. Dashboard
   - 期間フィルタ（today/week/month/custom）
   - KPIカード（総損益、勝率、平均勝ち/負け、PF、最大DD、連勝/連敗、平均保有時間、トレード数）
   - 日別損益、損益分布、時間帯別損益、保有時間vs損益、直近トレード
2. Trades List
   - 検索、フィルタ（勝敗、side、ticker、tag、日付）、ソート
3. Trade Detail
   - 基本情報、損益、保有時間、メモ、レビュー、タグ
   - ローソク足（ダミーOHLCV）に entry/exit マーカー表示
4. Import
   - CSVアップロード、プレビュー、バリデーション、結果表示（成功/失敗理由）
5. Settings
   - アプリ名、手数料、タイムゾーン、初期資金、表示設定

## 4. 非機能要件
- UI: ダークテーマ、高コントラスト、利益=緑/損失=赤、デスクトップ優先レスポンシブ。
- パフォーマンス: KPIレスポンス 500ms 目標（ローカル/シード規模）。
- 保守性: サービス層とリポジトリ層を分離、計算ロジックを pure function 化。
- 型安全: TS/Pydantic により I/O境界を厳密化。

## 5. API要件（MVP）
- GET /health
- GET /api/dashboard/summary
- GET /api/dashboard/daily-pnl
- GET /api/dashboard/pnl-distribution
- GET /api/dashboard/performance-by-time-slot
- GET /api/dashboard/hold-vs-pnl
- GET /api/trades
- POST /api/trades
- GET /api/trades/{id}
- PUT /api/trades/{id}
- DELETE /api/trades/{id}
- POST /api/import/csv
- GET /api/symbols
- GET /api/tags
- POST /api/tags

## 6. CSVフォーマット（共通）
必須/準必須列:
- trade_date, ticker, symbol_name, side, entry_time, exit_time,
  entry_price, exit_price, quantity, fee, tags, note

バリデーション:
- 日時型妥当性
- 数値型妥当性
- side ∈ {long, short}
- quantity > 0
- entry_time <= exit_time

## 7. 完了条件（Definition of Done）
- Docker compose で frontend/backend/db が起動。
- シード投入後、29件以上のトレードで全グラフが描画。
- 必須APIがSwaggerで確認可能。
- 主要計算ロジック/CSVインポート/フロント重要箇所のテストが通る。
- READMEにセットアップ/テスト/CSV仕様/拡張方針を記載。
