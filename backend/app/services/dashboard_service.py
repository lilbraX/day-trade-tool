import math
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
        return [
            {"hold_minutes": t.hold_minutes, "pnl": float(t.net_pnl)}
            for t in self._trades(start_date, end_date)
        ]

    def pnl_distribution(self, start_date: date | None, end_date: date | None) -> list[dict]:
        """
        ビン幅をデータの範囲から動的に決定する。
        Sturges則: bins = ceil(1 + log2(n)) を参考に 10〜20本程度に収める。
        """
        trades = self._trades(start_date, end_date)
        if not trades:
            return []

        pnls = [float(t.net_pnl) for t in trades]
        min_pnl, max_pnl = min(pnls), max(pnls)
        spread = max_pnl - min_pnl

        if spread == 0:
            return [{"bucket": f"{int(min_pnl)}", "count": len(pnls)}]

        # Sturges則でビン数を決め、キリの良い幅に丸める
        n_bins = max(5, math.ceil(1 + math.log2(len(pnls))))
        raw_width = spread / n_bins

        # 幅をキリの良い数値に丸める（100, 500, 1000, 5000, 10000, ...）
        magnitude = 10 ** math.floor(math.log10(raw_width))
        bin_width = math.ceil(raw_width / magnitude) * magnitude

        # ビン境界を計算
        start_bin = math.floor(min_pnl / bin_width) * bin_width
        bins: dict[str, int] = defaultdict(int)
        for pnl in pnls:
            idx = math.floor((pnl - start_bin) / bin_width)
            lo = int(start_bin + idx * bin_width)
            hi = int(lo + bin_width - 1)
            bins[f"{lo}~{hi}"] += 1

        return [{"bucket": k, "count": v} for k, v in sorted(bins.items(), key=lambda x: int(x[0].split("~")[0]))]
