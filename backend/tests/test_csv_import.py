from app.utils.csv_parser import validate_row


def test_validate_row_ok():
    errors = validate_row(
        {
            "trade_date": "2026-01-01",
            "ticker": "7203",
            "symbol_name": "TOYOTA",
            "side": "long",
            "entry_time": "2026-01-01T09:00:00",
            "exit_time": "2026-01-01T09:10:00",
            "entry_price": "100",
            "exit_price": "101",
            "quantity": "100",
            "fee": "10",
            "tags": "breakout",
            "note": "ok",
        }
    )
    assert errors == []


def test_validate_row_error():
    errors = validate_row(
        {
            "trade_date": "bad",
            "side": "foo",
            "entry_time": "x",
            "exit_time": "y",
            "entry_price": "a",
            "exit_price": "b",
            "quantity": "c",
            "fee": "d",
        }
    )
    assert len(errors) >= 4
