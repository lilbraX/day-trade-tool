"""
Seed script: 35 trades across 4 symbols with realistic P&L distribution.
Win rate ~57%, PF ~1.4 so dashboard charts look meaningful.
"""
from datetime import datetime, timedelta
from decimal import Decimal
import random

from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.models import Symbol, Trade, TradeSide, TradeStatus, TradeTag, TradeTagLink, User

# 再現性のため固定シード
random.seed(42)

# 勝ち/負けパターン: 勝率57% (20勝15敗), PF ≒ 1.4 になるよう設計
# 利益: +8,000〜+45,000  損失: -6,000〜-22,000
WIN_MOVES  = [8, 10, 12, 15, 18, 22, 28, 35, 42, 45]  # 円/株（×株数で損益）
LOSS_MOVES = [-6, -7, -8, -10, -12, -15, -18, -20, -22]

RESULT_PATTERN = (
    [True]  * 20 +  # 20勝
    [False] * 15    # 15敗
)
random.shuffle(RESULT_PATTERN)

TICKERS = [
    ("7203", "トヨタ自動車",   "TSE", Decimal("3200")),
    ("9984", "ソフトバンクG",  "TSE", Decimal("8500")),
    ("6758", "ソニーグループ", "TSE", Decimal("12400")),
    ("8306", "三菱UFJ",        "TSE", Decimal("1420")),
    ("6861", "キーエンス",     "TSE", Decimal("65000")),
]

TAGS_DEF = [
    ("breakout",  "#10b981"),
    ("reversal",  "#f59e0b"),
    ("fomo",      "#ef4444"),
    ("pullback",  "#3b82f6"),
    ("gap-play",  "#8b5cf6"),
]


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # ── ユーザー ──────────────────────────────────────────────
        user = db.execute(
            select(User).where(User.email == "demo@example.com")
        ).scalar_one_or_none()
        if not user:
            user = User(email="demo@example.com", name="Demo User")
            db.add(user)
            db.commit()
            db.refresh(user)

        # ── 銘柄 ─────────────────────────────────────────────────
        symbols: list[Symbol] = []
        for ticker, name, market, _ in TICKERS:
            s = db.execute(select(Symbol).where(Symbol.ticker == ticker)).scalar_one_or_none()
            if not s:
                s = Symbol(ticker=ticker, name=name, market=market)
                db.add(s)
                db.flush()
            symbols.append(s)

        # ── タグ ─────────────────────────────────────────────────
        tags: list[TradeTag] = []
        for name, color in TAGS_DEF:
            t = db.execute(
                select(TradeTag).where(TradeTag.user_id == user.id, TradeTag.name == name)
            ).scalar_one_or_none()
            if not t:
                t = TradeTag(user_id=user.id, name=name, color=color)
                db.add(t)
                db.flush()
            tags.append(t)

        db.commit()

        # 既にトレードがあればスキップ
        if db.execute(select(Trade)).scalars().first():
            return

        # ── トレード生成 ──────────────────────────────────────────
        # 20営業日（2026-02-10〜2026-03-06）に35トレードを分散
        base_day = datetime(2026, 2, 10)
        business_days = [base_day + timedelta(days=d) for d in range(28) if (base_day + timedelta(days=d)).weekday() < 5]

        hold_choices = [5, 8, 12, 18, 25, 35, 50, 70, 95, 130]

        for i in range(35):
            sym_ticker, _, _, base_price = TICKERS[i % len(TICKERS)]
            sym = next(s for s in symbols if s.ticker == sym_ticker)

            day = business_days[i % len(business_days)]
            # 前場(9:05-11:30) / 後場(12:30-15:20) を交互
            if i % 3 == 0:
                entry = day.replace(hour=random.randint(9, 11), minute=random.randint(5, 55))
            elif i % 3 == 1:
                entry = day.replace(hour=random.randint(12, 14), minute=random.randint(30, 59))
            else:
                entry = day.replace(hour=9, minute=random.randint(5, 30))

            hold = random.choice(hold_choices)
            exit_t = entry + timedelta(minutes=hold)

            side = TradeSide.long if i % 2 == 0 else TradeSide.short

            # 株価にランダムな揺れを加える
            price_base = base_price + Decimal(str(random.randint(-50, 50)))
            entry_price = price_base

            is_win = RESULT_PATTERN[i]
            move_per_share = Decimal(str(
                random.choice(WIN_MOVES) if is_win else random.choice(LOSS_MOVES)
            ))

            if side == TradeSide.long:
                exit_price = entry_price + move_per_share
            else:
                exit_price = entry_price - move_per_share

            qty = Decimal(str(random.choice([100, 200, 300, 500])))
            fee = Decimal("120")

            if side == TradeSide.long:
                gross = (exit_price - entry_price) * qty
            else:
                gross = (entry_price - exit_price) * qty

            net = gross - fee

            trade = Trade(
                user_id=user.id,
                symbol_id=sym.id,
                trade_date=entry.date(),
                side=side,
                status=TradeStatus.closed,
                entry_time=entry,
                exit_time=exit_t,
                entry_price=entry_price,
                exit_price=exit_price,
                quantity=qty,
                gross_pnl=gross,
                fees=fee,
                net_pnl=net,
                hold_minutes=hold,
                strategy_tag=TAGS_DEF[i % len(TAGS_DEF)][0],
                note=f"シードトレード #{i + 1}",
                review="損切りをもっと早く" if net < 0 else "良いエグジット",
            )
            db.add(trade)
            db.flush()

            # タグを2つまで紐付け
            assigned_tags = random.sample(tags, k=min(2, len(tags)))
            for tag in assigned_tags:
                db.add(TradeTagLink(trade_id=trade.id, tag_id=tag.id))

        db.commit()
        print(f"✅ Seed complete: 35 trades inserted for user_id={user.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
