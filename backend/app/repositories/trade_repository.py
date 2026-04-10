from datetime import date

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from app.models.models import Trade


class TradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def query(self) -> Select[tuple[Trade]]:
        return select(Trade).options(joinedload(Trade.symbol), joinedload(Trade.tags)).order_by(Trade.trade_date)

    def list(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
        side: str | None = None,
        ticker: str | None = None,
    ) -> list[Trade]:
        stmt = self.query()
        if start_date:
            stmt = stmt.where(Trade.trade_date >= start_date)
        if end_date:
            stmt = stmt.where(Trade.trade_date <= end_date)
        if side:
            stmt = stmt.where(Trade.side == side)
        if ticker:
            stmt = stmt.where(Trade.symbol.has(ticker=ticker))
        return self.db.execute(stmt).unique().scalars().all()

    def get(self, trade_id: int) -> Trade | None:
        stmt = self.query().where(Trade.id == trade_id)
        return self.db.execute(stmt).unique().scalars().first()

    def save(self, trade: Trade) -> Trade:
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade

    def delete(self, trade: Trade) -> None:
        self.db.delete(trade)
        self.db.commit()
