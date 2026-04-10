from datetime import datetime, timedelta
from decimal import Decimal
import random

from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.models import Symbol, Trade, TradeSide, TradeStatus, TradeTag, User


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.email == "demo@example.com")).scalar_one_or_none()
        if not user:
            user = User(email="demo@example.com", name="Demo User")
            db.add(user)
            db.commit()
            db.refresh(user)

        tickers = [("7203", "TOYOTA"), ("9984", "SOFTBANK"), ("6758", "SONY"), ("8306", "MUFG")]
        symbols: list[Symbol] = []
        for t, n in tickers:
            s = db.execute(select(Symbol).where(Symbol.ticker == t)).scalar_one_or_none()
            if not s:
                s = Symbol(ticker=t, name=n)
                db.add(s)
                db.flush()
            symbols.append(s)

        for tag_name, color in [("breakout", "#10b981"), ("reversal", "#f59e0b"), ("fomo", "#ef4444")]:
            exists = db.execute(select(TradeTag).where(TradeTag.user_id == user.id, TradeTag.name == tag_name)).scalar_one_or_none()
            if not exists:
                db.add(TradeTag(user_id=user.id, name=tag_name, color=color))

        db.commit()

        existing = db.execute(select(Trade)).scalars().first()
        if existing:
            return

        start_day = datetime(2026, 2, 10, 9, 5)
        for i in range(35):
            sym = symbols[i % len(symbols)]
            entry = start_day + timedelta(days=i % 20, hours=(i * 3) % 6, minutes=(i * 7) % 50)
            hold = random.choice([5, 12, 20, 35, 55, 90, 140])
            exit_t = entry + timedelta(minutes=hold)
            side = TradeSide.long if i % 2 == 0 else TradeSide.short
            entry_price = Decimal(str(900 + (i % 10) * 30 + random.randint(-5, 5)))
            move = Decimal(str(random.choice([-18, -12, -7, 5, 10, 15, 24])))
            exit_price = entry_price + move if side == TradeSide.long else entry_price - move
            qty = Decimal(str(random.choice([100, 200, 300])))
            fee = Decimal("120")
            gross = ((exit_price - entry_price) if side == TradeSide.long else (entry_price - exit_price)) * qty
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
                strategy_tag="opening-range" if i % 3 == 0 else "pullback",
                note=f"seed trade {i+1}",
                review="cut losses faster" if net < 0 else "good execution",
            )
            db.add(trade)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
