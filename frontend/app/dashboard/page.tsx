import { Suspense } from "react";
import { DistributionChart, DailyPnlChart, HoldVsPnlChart, TimeSlotChart } from "@/components/charts";
import { KpiCards } from "@/components/kpi-cards";
import { Nav } from "@/components/nav";
import { apiGet } from "@/lib/api/client";
import { Dist, HoldPoint, Summary, Trade, XY } from "@/lib/types";

// ── データフェッチ（個別にエラーを吸収）──────────────────────────
async function safeFetch<T>(fn: () => Promise<T>, fallback: T): Promise<T> {
  try {
    return await fn();
  } catch {
    return fallback;
  }
}

// ── サブコンポーネント ─────────────────────────────────────────────
function RecentTrades({ trades }: { trades: Trade[] }) {
  const recent = [...trades].reverse().slice(0, 10);
  if (recent.length === 0) {
    return (
      <div className="card" style={{ marginTop: 16, padding: 24, textAlign: "center", color: "#6b7280" }}>
        まだトレードがありません
      </div>
    );
  }
  return (
    <div className="card" style={{ marginTop: 16 }}>
      <h3 style={{ marginBottom: 12 }}>直近トレード</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {["日付", "銘柄", "方向", "純損益"].map((h) => (
              <th key={h} style={{ textAlign: "left", padding: "6px 12px", borderBottom: "1px solid #374151" }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {recent.map((t) => (
            <tr key={t.id}>
              <td style={{ padding: "6px 12px" }}>{t.trade_date}</td>
              <td style={{ padding: "6px 12px" }}>{t.symbol.ticker}</td>
              <td style={{ padding: "6px 12px" }}>{t.side.toUpperCase()}</td>
              <td
                style={{ padding: "6px 12px" }}
                className={t.net_pnl >= 0 ? "profit" : "loss"}
              >
                ¥{t.net_pnl.toLocaleString("ja-JP")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── ページ本体 ────────────────────────────────────────────────────
export default async function DashboardPage() {
  const [summary, daily, dist, timeSlot, hold, trades] = await Promise.all([
    safeFetch(() => apiGet<Summary>("/dashboard/summary"), {
      total_pnl: 0, win_rate: 0, avg_win: 0, avg_loss: 0,
      payoff_ratio: null, profit_factor: null, max_drawdown: 0,
      max_win_streak: 0, max_loss_streak: 0, trade_count: 0, avg_hold_minutes: 0,
    }),
    safeFetch(() => apiGet<XY[]>("/dashboard/daily-pnl"), []),
    safeFetch(() => apiGet<Dist[]>("/dashboard/pnl-distribution"), []),
    safeFetch(() => apiGet<XY[]>("/dashboard/performance-by-time-slot"), []),
    safeFetch(() => apiGet<HoldPoint[]>("/dashboard/hold-vs-pnl"), []),
    safeFetch(() => apiGet<Trade[]>("/trades"), []),
  ]);

  return (
    <>
      <Nav />
      <main style={{ padding: "0 16px 32px" }}>
        <Suspense fallback={<div>KPI読み込み中...</div>}>
          <KpiCards summary={summary} />
        </Suspense>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 16,
            marginTop: 16,
          }}
        >
          <DistributionChart data={dist} />
          <TimeSlotChart data={timeSlot} />
          <HoldVsPnlChart data={hold} />
          <DailyPnlChart data={daily} />
        </div>

        <RecentTrades trades={trades} />
      </main>
    </>
  );
}
