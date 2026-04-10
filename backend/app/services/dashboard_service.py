from collections import defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.repositories.trade_repository import TradeRepository
from app.utils.metrics import compute_summary


class DashboardService:
    def __init__(self, db: Session):
        self.repo = TradeRepository(db)

    def _trades(self, start_date: date | None, end_date: date | None):
        return self.repo.list(start_date=start_date, end_date=end_date)

    def summary(self, start_date: date | None, end_date: date | None) -> dict:
        trades = self._trades(start_date, end_date)
        pnls = [float(t.net_pnl) for t in trades]
        holds = [t.hold_minutes for t in trades]
        return compute_summary(pnls, holds)

    def daily_pnl(self, start_date: date | None, end_date: date | None) -> list[dict]:
        bucket: dict[str, float] = defaultdict(float)
        for t in self._trades(start_date, end_date):
            bucket[t.trade_date.isoformat()] += float(t.net_pnl)
        return [{"x": k, "y": round(v, 2)} for k, v in sorted(bucket.items())]

    def time_slot(self, start_date: date | None, end_date: date | None) -> list[dict]:
        bucket: dict[str, float] = defaultdict(float)
        for t in self._trades(start_date, end_date):
            slot = f"{t.entry_time.hour:02d}:00"
            bucket[slot] += float(t.net_pnl)
        return [{"x": k, "y": round(v, 2)} for k, v in sorted(bucket.items())]

    def hold_vs_pnl(self, start_date: date | None, end_date: date | None) -> list[dict]:
        return [{"hold_minutes": t.hold_minutes, "pnl": float(t.net_pnl)} for t in self._trades(start_date, end_date)]

    def pnl_distribution(self, start_date: date | None, end_date: date | None) -> list[dict]:
        bins: dict[str, int] = defaultdict(int)
        for t in self._trades(start_date, end_date):
            pnl = float(t.net_pnl)
            lo = int(pnl // 1000) * 1000
            hi = lo + 999
            bins[f"{lo}~{hi}"] += 1
        return [{"bucket": k, "count": v} for k, v in sorted(bins.items(), key=lambda x: x[0])]
