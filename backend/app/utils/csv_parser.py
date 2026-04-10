from datetime import datetime

REQUIRED_COLUMNS = {
    "trade_date",
    "ticker",
    "symbol_name",
    "side",
    "entry_time",
    "exit_time",
    "entry_price",
    "exit_price",
    "quantity",
    "fee",
    "tags",
    "note",
}


def validate_row(row: dict) -> list[str]:
    errors: list[str] = []
    side = str(row.get("side", "")).lower()
    if side not in {"long", "short"}:
        errors.append("side must be long or short")

    for field in ["entry_price", "exit_price", "quantity", "fee"]:
        try:
            float(row[field])
        except Exception:
            errors.append(f"{field} must be numeric")

    try:
        entry = datetime.fromisoformat(str(row["entry_time"]))
        exit_ = datetime.fromisoformat(str(row["exit_time"]))
        if entry > exit_:
            errors.append("entry_time must be <= exit_time")
    except Exception:
        errors.append("entry_time/exit_time must be ISO datetime")

    try:
        datetime.fromisoformat(str(row["trade_date"]))
    except Exception:
        errors.append("trade_date must be ISO date")

    return errors
