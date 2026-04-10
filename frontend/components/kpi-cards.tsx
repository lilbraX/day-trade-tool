import { Summary } from "@/lib/types";

const metrics: { key: keyof Summary; label: string }[] = [
  { key: "total_pnl", label: "総損益" },
  { key: "win_rate", label: "勝率(%)" },
  { key: "avg_win", label: "平均勝ち" },
  { key: "avg_loss", label: "平均負け" },
  { key: "payoff_ratio", label: "ペイオフ" },
  { key: "profit_factor", label: "PF" },
  { key: "max_drawdown", label: "最大DD" },
  { key: "trade_count", label: "トレード数" },
  { key: "avg_hold_minutes", label: "平均保有(分)" },
];

export function KpiCards({ summary }: { summary: Summary }) {
  return (
    <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))" }}>
      {metrics.map((m) => {
        const value = summary[m.key];
        const numeric = typeof value === "number" ? value : 0;
        const cls = m.key.includes("pnl") || m.key.includes("avg_") ? (numeric >= 0 ? "profit" : "loss") : "";
        return (
          <div className="card kpi" key={m.key}>
            <span className="label">{m.label}</span>
            <span className={`value ${cls}`}>{value ?? "-"}</span>
          </div>
        );
      })}
    </div>
  );
}
