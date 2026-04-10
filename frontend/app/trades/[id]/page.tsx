import { Nav } from "@/components/nav";
import { TradeCandles } from "@/components/trade-candles";
import { apiGet } from "@/lib/api/client";
import { Trade } from "@/lib/types";

export default async function TradeDetailPage({ params }: { params: { id: string } }) {
  const trade = await apiGet<Trade>(`/trades/${params.id}`);
  const ohlcv = await apiGet<{ time: number; open: number; high: number; low: number; close: number }[]>(`/trades/${params.id}/ohlcv`);

  return (
    <>
      <Nav />
      <div className="grid" style={{ gridTemplateColumns: "1fr 1fr" }}>
        <div className="card">
          <h2>Trade #{trade.id}</h2>
          <p>{trade.trade_date} / {trade.symbol.ticker} / {trade.side}</p>
          <p>Entry: {trade.entry_price} Exit: {trade.exit_price}</p>
          <p>Hold: {trade.hold_minutes}min</p>
          <p className={trade.net_pnl >= 0 ? "profit" : "loss"}>Net PnL: {trade.net_pnl}</p>
          <p>Note: {trade.note || "-"}</p>
          <p>Review: {trade.review || "-"}</p>
        </div>
        <div className="card">
          <h3>Chart (dummy OHLCV)</h3>
          <TradeCandles data={ohlcv} />
        </div>
      </div>
    </>
  );
}
