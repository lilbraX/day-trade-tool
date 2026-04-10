from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Symbol, Trade, TradeTag, User
from app.repositories.trade_repository import TradeRepository
from app.schemas.common import CsvImportResult, DashboardSummary, TradeCreate, TradeOut, TradeUpdate
from app.services.dashboard_service import DashboardService
from app.services.import_service import ImportService
from app.services.trade_service import TradeService

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).summary(start_date, end_date)


@router.get("/dashboard/daily-pnl")
def dashboard_daily(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).daily_pnl(start_date, end_date)


@router.get("/dashboard/pnl-distribution")
def dashboard_dist(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).pnl_distribution(start_date, end_date)


@router.get("/dashboard/performance-by-time-slot")
def dashboard_time(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).time_slot(start_date, end_date)


@router.get("/dashboard/hold-vs-pnl")
def dashboard_hold(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).hold_vs_pnl(start_date, end_date)


@router.get("/trades", response_model=list[TradeOut])
def list_trades(
    start_date: date | None = None,
    end_date: date | None = None,
    side: str | None = None,
    ticker: str | None = None,
    db: Session = Depends(get_db),
):
    return TradeRepository(db).list(start_date, end_date, side, ticker)


@router.post("/trades", response_model=TradeOut)
def create_trade(payload: TradeCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return TradeService(db).create_trade(payload, user.id)


@router.get("/trades/{trade_id}", response_model=TradeOut)
def get_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = TradeRepository(db).get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    return trade


@router.put("/trades/{trade_id}", response_model=TradeOut)
def update_trade(trade_id: int, payload: TradeUpdate, db: Session = Depends(get_db)):
    repo = TradeRepository(db)
    trade = repo.get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    return TradeService(db).update_trade(trade, payload)


@router.delete("/trades/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    repo = TradeRepository(db)
    trade = repo.get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")
    repo.delete(trade)
    return {"deleted": True}


@router.post("/import/csv", response_model=CsvImportResult)
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    content = await file.read()
    return ImportService(db).import_csv(content, user.id)


@router.get("/symbols")
def list_symbols(db: Session = Depends(get_db)):
    return db.execute(select(Symbol).order_by(Symbol.ticker)).scalars().all()


@router.get("/tags")
def list_tags(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.execute(select(TradeTag).where(TradeTag.user_id == user.id)).scalars().all()


@router.post("/tags")
def create_tag(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tag = TradeTag(user_id=user.id, name=payload["name"], color=payload.get("color", "#38bdf8"))
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/trades/{trade_id}/ohlcv")
def trade_ohlcv(trade_id: int):
    points = []
    base = 1000 + trade_id * 5
    for i in range(60):
        o = base + (i % 5) * 2
        c = o + (1 if i % 2 == 0 else -2)
        h = max(o, c) + 3
        l = min(o, c) - 3
        points.append({"time": i, "open": o, "high": h, "low": l, "close": c})
    return points
