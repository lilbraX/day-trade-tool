from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Symbol, Trade, TradeTag, User
from app.repositories.trade_repository import TradeRepository
from app.schemas.common import (
    CsvImportResult,
    DashboardSummary,
    TagCreate,
    TagOut,
    TradeCreate,
    TradeOut,
    TradeUpdate,
)
from app.services.dashboard_service import DashboardService
from app.services.import_service import ImportService
from app.services.trade_service import TradeService

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService(db).summary(start_date, end_date)


@router.get("/dashboard/daily-pnl")
def dashboard_daily(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService(db).daily_pnl(start_date, end_date)


@router.get("/dashboard/pnl-distribution")
def dashboard_dist(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService(db).pnl_distribution(start_date, end_date)


@router.get("/dashboard/performance-by-time-slot")
def dashboard_time(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService(db).time_slot(start_date, end_date)


@router.get("/dashboard/hold-vs-pnl")
def dashboard_hold(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return DashboardService(db).hold_vs_pnl(start_date, end_date)


# ── Trades ───────────────────────────────────────────────────────────────────

@router.get("/trades", response_model=list[TradeOut])
def list_trades(
    start_date: date | None = None,
    end_date: date | None = None,
    side: str | None = None,
    ticker: str | None = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    return TradeRepository(db).list(start_date, end_date, side, ticker, skip=skip, limit=limit)


@router.post("/trades", response_model=TradeOut, status_code=201)
def create_trade(
    payload: TradeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return TradeService(db).create_trade(payload, user.id)


@router.get("/trades/{trade_id}", response_model=TradeOut)
def get_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = TradeRepository(db).get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    return trade


@router.put("/trades/{trade_id}", response_model=TradeOut)
def update_trade(trade_id: int, payload: TradeUpdate, db: Session = Depends(get_db)):
    trade = TradeRepository(db).get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    return TradeService(db).update_trade(trade, payload)


@router.delete("/trades/{trade_id}", status_code=204)
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = TradeRepository(db).get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    TradeRepository(db).delete(trade)


# ── Import ───────────────────────────────────────────────────────────────────

@router.post("/import/csv", response_model=CsvImportResult)
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    content = await file.read()
    return ImportService(db).import_csv(content, user.id)


# ── Symbols ──────────────────────────────────────────────────────────────────

@router.get("/symbols")
def list_symbols(db: Session = Depends(get_db)):
    return db.execute(select(Symbol).order_by(Symbol.ticker)).scalars().all()


# ── Tags ─────────────────────────────────────────────────────────────────────

@router.get("/tags", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.execute(
        select(TradeTag).where(TradeTag.user_id == user.id)
    ).scalars().all()


@router.post("/tags", response_model=TagOut, status_code=201)
def create_tag(
    payload: TagCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag = TradeTag(user_id=user.id, name=payload.name, color=payload.color)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


# ── OHLCV (チャート用) ───────────────────────────────────────────────────────

@router.get("/trades/{trade_id}/ohlcv")
def trade_ohlcv(trade_id: int, timeframe: str = "5m"):
    """
    TODO: 外部データソース（J-Quants API / CSV）に差し替える。
    現在はダミーOHLCVを返す。timeframe は "1m" / "5m" を想定。
    実装方針: get_ohlcv(ticker, date, timeframe) -> list[OhlcvBar] の
    インターフェースを持つ ChartDataProvider を差し込む形にする。
    """
    interval = 1 if timeframe == "1m" else 5
    points = []
    base = 3000 + trade_id * 10
    for i in range(60):
        t = i * interval  # 分
        o = base + (i % 7) * 3
        c = o + (2 if i % 3 == 0 else -3)
        h = max(o, c) + 5
        lw = min(o, c) - 5
        points.append({"time": t, "open": o, "high": h, "low": lw, "close": c})
    return points
