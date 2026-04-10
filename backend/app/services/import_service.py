import io
from datetime import datetime
from decimal import Decimal

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Symbol, Trade, TradeSide, TradeStatus, TradeTag
from app.utils.csv_parser import REQUIRED_COLUMNS, validate_row


class ImportService:
    def __init__(self, db: Session):
        self.db = db

    def import_csv(self, content: bytes, user_id: int = 1) -> dict:
        df = pd.read_csv(io.BytesIO(content))
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            return {"success_count": 0, "error_count": len(df), "errors": [{"row": 0, "reason": f"missing columns: {', '.join(sorted(missing))}"}]}

        success = 0
        errors: list[dict] = []

        for i, row in df.iterrows():
            data = row.to_dict()
            row_errors = validate_row(data)
            if row_errors:
                errors.append({"row": int(i) + 2, "reason": "; ".join(row_errors)})
                continue

            ticker = str(data["ticker"])
            symbol = self.db.execute(select(Symbol).where(Symbol.ticker == ticker)).scalar_one_or_none()
            if not symbol:
                symbol = Symbol(ticker=ticker, name=str(data["symbol_name"]))
                self.db.add(symbol)
                self.db.flush()

            entry_time = datetime.fromisoformat(str(data["entry_time"]))
            exit_time = datetime.fromisoformat(str(data["exit_time"]))
            entry_price = Decimal(str(data["entry_price"]))
            exit_price = Decimal(str(data["exit_price"]))
            qty = Decimal(str(data["quantity"]))
            fee = Decimal(str(data["fee"]))
            side = str(data["side"]).lower()

            gross = ((exit_price - entry_price) if side == "long" else (entry_price - exit_price)) * qty
            net = gross - fee
            hold = int((exit_time - entry_time).total_seconds() // 60)

            trade = Trade(
                user_id=user_id,
                symbol_id=symbol.id,
                trade_date=datetime.fromisoformat(str(data["trade_date"])) .date(),
                side=TradeSide(side),
                status=TradeStatus.closed,
                entry_time=entry_time,
                exit_time=exit_time,
                entry_price=entry_price,
                exit_price=exit_price,
                quantity=qty,
                gross_pnl=gross,
                fees=fee,
                net_pnl=net,
                hold_minutes=max(hold, 0),
                note=str(data.get("note", "")),
            )
            self.db.add(trade)
            self.db.flush()

            tags_raw = str(data.get("tags", "")).strip()
            if tags_raw:
                for name in [t.strip() for t in tags_raw.split("|") if t.strip()]:
                    tag = self.db.execute(select(TradeTag).where(TradeTag.user_id == user_id, TradeTag.name == name)).scalar_one_or_none()
                    if not tag:
                        tag = TradeTag(user_id=user_id, name=name, color="#64748b")
                        self.db.add(tag)
                        self.db.flush()
                    trade.tags.append(tag)

            success += 1

        self.db.commit()
        return {"success_count": success, "error_count": len(errors), "errors": errors}
