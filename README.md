# dominai trader journal

日本株デイトレーダー向けの、トレード記録・分析・改善ダッシュボードMVPです。

## 概要
- FastAPI + Next.js + PostgreSQL 構成
- トレード入力・一覧・詳細・CSVインポート
- KPI分析（総損益、勝率、PF、最大DD、連勝/連敗など）
- ダークテーマの分析ダッシュボード

## 技術スタック
- Frontend: Next.js(App Router), TypeScript, Recharts, lightweight-charts
- Backend: FastAPI, SQLAlchemy, Pydantic, pandas
- DB: PostgreSQL
- Infra: Docker Compose

## セットアップ手順
```bash
cp .env.example .env
docker compose up --build
```

## 環境変数
- `APP_NAME`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `NEXT_PUBLIC_API_BASE`
- `DEFAULT_USER_EMAIL`

## 起動方法
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## テスト方法
```bash
# backend
cd backend && pytest

# frontend
cd frontend && npm install && npm run test
```

## ディレクトリ構成
```text
.
├── backend/
│   ├── app/
│   │   ├── api/              # ルーティング
│   │   ├── services/         # 業務ロジック
│   │   ├── repositories/     # DBアクセス
│   │   ├── utils/            # pure function
│   │   ├── models/           # SQLAlchemyモデル
│   │   └── seed/             # シード
│   └── tests/
├── frontend/
│   ├── app/                  # Next.js pages
│   ├── components/
│   └── lib/
└── docs/
    ├── requirements.md
    ├── architecture.md
    └── schema.md
```

## CSVフォーマット
列:
- `trade_date`
- `ticker`
- `symbol_name`
- `side` (`long`/`short`)
- `entry_time`
- `exit_time`
- `entry_price`
- `exit_price`
- `quantity`
- `fee`
- `tags` (例: `breakout|fomo`)
- `note`

## e2e的な確認手順
1. `docker compose up --build`
2. DashboardでKPIと4種グラフが表示されることを確認
3. Tradesでフィルタし、詳細遷移を確認
4. ImportでCSVを投入し、成功/失敗理由を確認

## 今後の拡張方針
1. broker別CSVアダプタ拡張
2. 認証追加（複数ユーザー）
3. fills起点のトレード復元ロジック実装
4. 実マーケットデータ連携（1分足/5分足）

## 未実装項目（MVP以降）
- 設定値の永続化API
- Trade detailのentry/exit marker厳密描画
- 高度なCSVマッピングUI
- E2E自動テスト
