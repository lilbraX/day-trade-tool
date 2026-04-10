# 技術設計（MVP）

## 1. システム構成
- Frontend: Next.js App Router + TypeScript + Tailwind + shadcn/ui + Recharts + lightweight-charts
- Backend: FastAPI + SQLAlchemy + Pydantic + pandas
- DB: PostgreSQL
- Infra: docker compose

## 2. アーキテクチャ方針
### Backend
- api: HTTPルーティング
- schemas: request/response DTO
- repositories: DBアクセス
- services: 業務ロジック（集計・CSV取込）
- utils: 純粋関数（指標計算）

### Frontend
- app: ルート/ページ
- components: 画面部品（KPIカード、チャート、テーブル等）
- lib/api: APIクライアント
- lib/types: 型定義
- lib/constants: APP_NAMEなど定数
- URLクエリで一覧・期間フィルタを保持

## 3. データフロー
1. ユーザー入力/CSVアップロード
2. FastAPIでバリデーション
3. DB保存
4. ダッシュボード集計APIでSQL/計算ロジック実行
5. Frontendで可視化

## 4. 指標計算ポリシー
- net_pnlベースで損益評価
- 勝ち: net_pnl > 0
- 負け: net_pnl < 0
- PF: 総利益 / abs(総損失)（総損失ゼロ時はnull）
- 最大DD: 累積損益列の running max との差分最大
- 連勝/連敗: 日付順トレード列に対してランレングス集計

## 5. 将来拡張ポイント
- broker adapter追加（CSV→共通レコード正規化）
- 約定履歴からトレード復元（fills主導）
- 認証方式追加（JWT/OAuth）
- 価格データ取得層の差し替え（ローカルJSON→外部API）
