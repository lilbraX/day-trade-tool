from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TradeSide(str, Enum):
    long = "long"
    short = "short"


class TradeStatus(str, Enum):
    open = "open"
    closed = "closed"


class FillSide(str, Enum):
    buy = "buy"
    sell = "sell"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Tokyo")
    default_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("1000000"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Symbol(Base):
    __tablename__ = "symbols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    market: Mapped[str] = mapped_column(String(64), default="TSE")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TradeTagLink(Base):
    __tablename__ = "trade_tag_links"

    trade_id: Mapped[int] = mapped_column(ForeignKey("trades.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("trade_tags.id"), primary_key=True)


class TradeTag(Base):
    __tablename__ = "trade_tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_tag_user_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    color: Mapped[str] = mapped_column(String(16), default="#38bdf8")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    symbol_id: Mapped[int] = mapped_column(ForeignKey("symbols.id"), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    side: Mapped[TradeSide] = mapped_column(SqlEnum(TradeSide), nullable=False)
    status: Mapped[TradeStatus] = mapped_column(SqlEnum(TradeStatus), default=TradeStatus.closed)
    entry_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    exit_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    entry_price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    exit_price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    gross_pnl: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    fees: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    net_pnl: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    hold_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    strategy_tag: Mapped[str | None] = mapped_column(String(64), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    review: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    symbol: Mapped[Symbol] = relationship()
    tags: Mapped[list[TradeTag]] = relationship("TradeTag", secondary="trade_tag_links")


class Fill(Base):
    __tablename__ = "fills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_id: Mapped[int] = mapped_column(ForeignKey("trades.id"), nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    side: Mapped[FillSide] = mapped_column(SqlEnum(FillSide), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
