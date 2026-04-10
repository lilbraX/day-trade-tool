# DB設計

## 設計方針
- users を基点に全データを分離可能にする。
- trades を分析の中心テーブルとし、fills は将来の復元用途で保持。
- tags は多対多で trade_tag_links で接続。

## テーブル

### users
- id (PK)
- email (UNIQUE)
- name
- timezone
- default_fee
- initial_capital
- created_at
- updated_at

### symbols
- id (PK)
- ticker (UNIQUE)
- name
- market
- created_at
- updated_at

### trades
- id (PK)
- user_id (FK users.id)
- symbol_id (FK symbols.id)
- trade_date (date)
- side (enum: long/short)
- status (open/closed)
- entry_time (datetime)
- exit_time (datetime)
- entry_price (numeric)
- exit_price (numeric)
- quantity (numeric)
- gross_pnl (numeric)
- fees (numeric)
- net_pnl (numeric)
- hold_minutes (int)
- strategy_tag (nullable)
- note (nullable)
- review (nullable)
- created_at
- updated_at

Index:
- (user_id, trade_date)
- (user_id, side)
- (symbol_id)

### fills
- id (PK)
- trade_id (FK trades.id)
- executed_at
- side (buy/sell)
- price
- quantity
- fee
- created_at
- updated_at

### trade_tags
- id (PK)
- user_id (FK users.id)
- name
- color
- created_at
- updated_at
- unique(user_id, name)

### trade_tag_links
- trade_id (FK trades.id)
- tag_id (FK trade_tags.id)
- primary key (trade_id, tag_id)

### daily_stats（任意キャッシュ）
- id (PK)
- user_id
- trade_date
- total_pnl
- trade_count
- win_rate
- created_at
- updated_at
- unique(user_id, trade_date)
