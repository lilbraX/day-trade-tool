import { DistributionChart, DailyPnlChart, HoldVsPnlChart, TimeSlotChart } from "@/components/charts";
import { KpiCards } from "@/components/kpi-cards";
import { Nav } from "@/components/nav";
import { apiGet } from "@/lib/api/client";
import { Dist, HoldPoint, Summary, Trade, XY } from "@/lib/types";

export default async function DashboardPage() {
  const [summary, daily, dist, timeSlot, hold, trades] = await Promise.all([
    apiGet<Summary>("/dashboard/summary"),
    apiGet<XY[]>("/dashboard/daily-pnl"),
    apiGet<Dist[]>("/dashboard/pnl-distribution"),
    apiGet<XY[]>("/dashboard/performance-by-time-slot"),
    apiGet<HoldPoint[]>("/dashboard/hold-vs-pnl"),
    apiGet<Trade[]>("/trades"),
  ]);

  return (
    <>
      <Nav />
      <KpiCards summary={summary} />
      <div className="grid" style={{ gridTemplateColumns: "1fr 1fr", marginTop: 16 }}>
        <DistributionChart data={dist} />
        <TimeSlotChart data={timeSlot} />
        <HoldVsPnlChart data={hold} />
        <DailyPnlChart data={daily} />
      </div>
      <div className="card" style={{ marginTop: 16 }}>
        <h3>直近トレード</h3>
        <table>
          <thead><tr><th>Date</th><th>Ticker</th><th>Side</th><th>NetPnL</th></tr></thead>
          <tbody>{trades.slice(-10).reverse().map((t) => <tr key={t.id}><td>{t.trade_date}</td><td>{t.symbol.ticker}</td><td>{t.side}</td><td className={t.net_pnl >= 0 ? "profit" : "loss"}>{t.net_pnl}</td></tr>)}</tbody>
        </table>
      </div>
    </>
  );
}
