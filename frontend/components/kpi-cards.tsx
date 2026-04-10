import { Summary } from "@/lib/types";

const fmt = (v: number, decimals = 0) =>
  v.toLocaleString("ja-JP", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });

type Metric = {
  key: keyof Summary;
  label: string;
  format: (v: number) => string;
  colorize: boolean;
};

const metrics: Metric[] = [
  { key: "total_pnl",        label: "総損益",        format: (v) => `¥${fmt(v)}`,    colorize: true  },
  { key: "win_rate",         label: "勝率",           format: (v) => `${fmt(v, 1)}%`, colorize: false },
  { key: "avg_win",          label: "平均利益",       format: (v) => `¥${fmt(v)}`,    colorize: true  },
  { key: "avg_loss",         label: "平均損失",       format: (v) => `¥${fmt(v)}`,    colorize: true  },
  { key: "payoff_ratio",     label: "ペイオフ比",     format: (v) => fmt(v, 2),        colorize: false },
  { key: "profit_factor",    label: "PF",             format: (v) => fmt(v, 2),        colorize: false },
  { key: "max_drawdown",     label: "最大DD",         format: (v) => `¥${fmt(v)}`,    colorize: false },
  { key: "max_win_streak",   label: "最大連勝",       format: (v) => `${v}連`,        colorize: false },
  { key: "max_loss_streak",  label: "最大連敗",       format: (v) => `${v}連`,        colorize: false },
  { key: "trade_count",      label: "トレード数",     format: (v) => `${v}件`,        colorize: false },
  { key: "avg_hold_minutes", label: "平均保有(分)",   format: (v) => fmt(v, 1),        colorize: false },
];

export function KpiCards({ summary }: { summary: Summary }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
        gap: "12px",
        padding: "16px",
      }}
    >
      {metrics.map((m) => {
        const raw = summary[m.key];
        const numeric = typeof raw === "number" ? raw : null;
        const display = numeric !== null ? m.format(numeric) : "-";
        const colorClass =
          m.colorize && numeric !== null ? (numeric >= 0 ? "profit" : "loss") : "";

        return (
          <div className={`card kpi ${colorClass}`} key={m.key}>
            <span className="label">{m.label}</span>
            <span className={`value ${colorClass}`}>{display}</span>
          </div>
        );
      })}
    </div>
  );
}
