from app.utils.metrics import compute_summary


def test_compute_summary():
    result = compute_summary([100, -50, 200, -150, 30], [10, 20, 30, 40, 50])
    assert result["total_pnl"] == 130
    assert result["trade_count"] == 5
    assert result["max_drawdown"] >= 0
    assert result["max_win_streak"] >= 1
    assert result["max_loss_streak"] >= 1
