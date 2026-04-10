import Link from "next/link";

import { Nav } from "@/components/nav";
import { apiGet } from "@/lib/api/client";
import { Trade } from "@/lib/types";

export default async function TradesPage({ searchParams }: { searchParams: { side?: string; ticker?: string } }) {
  const params = new URLSearchParams();
  if (searchParams.side) params.set("side", searchParams.side);
  if (searchParams.ticker) params.set("ticker", searchParams.ticker);
  const query = params.toString();
  const trades = await apiGet<Trade[]>(`/trades${query ? `?${query}` : ""}`);

  return (
    <>
      <Nav />
      <form className="inline" method="get" style={{ marginBottom: 12 }}>
        <select name="side" defaultValue={searchParams.side ?? ""}><option value="">all sides</option><option value="long">long</option><option value="short">short</option></select>
        <input name="ticker" placeholder="ticker" defaultValue={searchParams.ticker ?? ""} />
        <button type="submit">filter</button>
      </form>
      <div className="card">
        <table>
          <thead><tr><th>ID</th><th>Date</th><th>Ticker</th><th>Side</th><th>Hold</th><th>NetPnL</th></tr></thead>
          <tbody>
            {trades.map((t) => (
              <tr key={t.id}>
                <td><Link href={`/trades/${t.id}`}>{t.id}</Link></td>
                <td>{t.trade_date}</td><td>{t.symbol.ticker}</td><td>{t.side}</td><td>{t.hold_minutes}</td>
                <td className={t.net_pnl >= 0 ? "profit" : "loss"}>{t.net_pnl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
