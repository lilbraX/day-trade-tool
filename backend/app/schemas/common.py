from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.models import TradeSide


class TagOut(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True


class SymbolOut(BaseModel):
    id: int
    ticker: str
    name: str
    market: str

    class Config:
        from_attributes = True


class TradeBase(BaseModel):
    symbol_id: int
    trade_date: date
    side: TradeSide
    entry_time: datetime
    exit_time: datetime
    entry_price: Decimal = Field(gt=0)
    exit_price: Decimal = Field(gt=0)
    quantity: Decimal = Field(gt=0)
    fees: Decimal = Field(default=Decimal("0"))
    strategy_tag: str | None = None
    note: str | None = None
    review: str | None = None
    tag_ids: list[int] = []


class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    pass


class TradeOut(BaseModel):
    id: int
    symbol: SymbolOut
    trade_date: date
    side: TradeSide
    entry_time: datetime
    exit_time: datetime
    entry_price: Decimal
    exit_price: Decimal
    quantity: Decimal
    gross_pnl: Decimal
    fees: Decimal
    net_pnl: Decimal
    hold_minutes: int
    strategy_tag: str | None
    note: str | None
    review: str | None
    tags: list[TagOut]

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total_pnl: float
    win_rate: float
    avg_win: float
    avg_loss: float
    payoff_ratio: float | None
    profit_factor: float | None
    max_drawdown: float
    max_win_streak: int
    max_loss_streak: int
    trade_count: int
    avg_hold_minutes: float


class XYPoint(BaseModel):
    x: str
    y: float


class ScatterPoint(BaseModel):
    hold_minutes: int
    pnl: float


class DistributionBin(BaseModel):
    bucket: str
    count: int


class CsvImportResult(BaseModel):
    success_count: int
    error_count: int
    errors: list[dict]


class CsvPreviewRow(BaseModel):
    row_number: int
    trade_date: str
    ticker: str
    side: str
    note: str | None
class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    color: str = Field(default="#38bdf8", pattern=r"^#[0-9a-fA-F]{6}$")


class TagOut(BaseModel):
    id: int
    name: str
    color: str

    model_config = {"from_attributes": True}
