from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Symbol, Trade, TradeStatus
from app.schemas.common import TradeCreate, TradeUpdate


def calc_pnl(side: str, entry: Decimal, exit_: Decimal, qty: Decimal, fees: Decimal) -> tuple[Decimal, Decimal, int]:
    diff = (exit_ - entry) if side == "long" else (entry - exit_)
    gross = diff * qty
    net = gross - fees
    return gross, net, 0


class TradeService:
    def __init__(self, db: Session):
        self.db = db

    def _get_or_create_symbol(self, symbol_id: int | None = None, ticker: str | None = None, name: str | None = None) -> Symbol:
        if symbol_id is not None:
            symbol = self.db.get(Symbol, symbol_id)
            if symbol:
                return symbol
        if ticker:
            existing = self.db.execute(select(Symbol).where(Symbol.ticker == ticker)).scalar_one_or_none()
            if existing:
                return existing
            symbol = Symbol(ticker=ticker, name=name or ticker)
            self.db.add(symbol)
            self.db.flush()
            return symbol
        raise ValueError("symbol is required")

    def create_trade(self, payload: TradeCreate, user_id: int = 1) -> Trade:
        symbol = self._get_or_create_symbol(symbol_id=payload.symbol_id)
        gross = ((payload.exit_price - payload.entry_price) if payload.side.value == "long" else (payload.entry_price - payload.exit_price)) * payload.quantity
        net = gross - payload.fees
        hold = int((payload.exit_time - payload.entry_time).total_seconds() // 60)
        trade = Trade(
            user_id=user_id,
            symbol_id=symbol.id,
            trade_date=payload.trade_date,
            side=payload.side,
            status=TradeStatus.closed,
            entry_time=payload.entry_time,
            exit_time=payload.exit_time,
            entry_price=payload.entry_price,
            exit_price=payload.exit_price,
            quantity=payload.quantity,
            gross_pnl=gross,
            fees=payload.fees,
            net_pnl=net,
            hold_minutes=max(hold, 0),
            strategy_tag=payload.strategy_tag,
            note=payload.note,
            review=payload.review,
        )
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade

    def update_trade(self, trade: Trade, payload: TradeUpdate) -> Trade:
        for field, value in payload.model_dump().items():
            setattr(trade, field, value)
        trade.gross_pnl = ((trade.exit_price - trade.entry_price) if trade.side.value == "long" else (trade.entry_price - trade.exit_price)) * trade.quantity
        trade.net_pnl = trade.gross_pnl - trade.fees
        trade.hold_minutes = int((trade.exit_time - trade.entry_time).total_seconds() // 60)
        trade.updated_at = datetime.utcnow()
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade
