from collections.abc import Sequence


def _safe_div(a: float, b: float) -> float | None:
    return None if b == 0 else a / b


def compute_summary(pnls: Sequence[float], holds: Sequence[int]) -> dict:
    trade_count = len(pnls)
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    total_pnl = sum(pnls)
    win_rate = (len(wins) / trade_count * 100) if trade_count else 0.0
    avg_win = (sum(wins) / len(wins)) if wins else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0
    payoff_ratio = _safe_div(avg_win, abs(avg_loss)) if avg_loss != 0 else None
    gross_profit = sum(wins)
    gross_loss = sum(losses)
    profit_factor = _safe_div(gross_profit, abs(gross_loss)) if gross_loss != 0 else None

    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    max_win_streak = 0
    max_loss_streak = 0
    cur_win = 0
    cur_loss = 0

    for pnl in pnls:
        cumulative += pnl
        if cumulative > peak:
            peak = cumulative
        drawdown = peak - cumulative
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        if pnl > 0:
            cur_win += 1
            cur_loss = 0
        elif pnl < 0:
            cur_loss += 1
            cur_win = 0
        else:
            cur_win = 0
            cur_loss = 0

        max_win_streak = max(max_win_streak, cur_win)
        max_loss_streak = max(max_loss_streak, cur_loss)

    avg_hold = (sum(holds) / len(holds)) if holds else 0.0

    return {
        "total_pnl": round(total_pnl, 2),
        "win_rate": round(win_rate, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "payoff_ratio": round(payoff_ratio, 2) if payoff_ratio is not None else None,
        "profit_factor": round(profit_factor, 2) if profit_factor is not None else None,
        "max_drawdown": round(max_drawdown, 2),
        "max_win_streak": max_win_streak,
        "max_loss_streak": max_loss_streak,
        "trade_count": trade_count,
        "avg_hold_minutes": round(avg_hold, 2),
    }
