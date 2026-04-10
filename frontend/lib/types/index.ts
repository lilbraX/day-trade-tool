export type XY = { x: string; y: number };
export type Dist = { bucket: string; count: number };
export type HoldPoint = { hold_minutes: number; pnl: number };

export type Trade = {
  id: number;
  trade_date: string;
  side: "long" | "short";
  entry_time: string;
  exit_time: string;
  entry_price: number;
  exit_price: number;
  quantity: number;
  gross_pnl: number;
  fees: number;
  net_pnl: number;
  hold_minutes: number;
  strategy_tag?: string;
  note?: string;
  review?: string;
  symbol: { id: number; ticker: string; name: string; market: string };
  tags: { id: number; name: string; color: string }[];
};

export type Summary = {
  total_pnl: number;
  win_rate: number;
  avg_win: number;
  avg_loss: number;
  payoff_ratio: number | null;
  profit_factor: number | null;
  max_drawdown: number;
  max_win_streak: number;
  max_loss_streak: number;
  trade_count: number;
  avg_hold_minutes: number;
};
