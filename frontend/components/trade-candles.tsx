"use client";

import { createChart } from "lightweight-charts";
import { useEffect, useRef } from "react";

export function TradeCandles({ data }: { data: { time: number; open: number; high: number; low: number; close: number }[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, { layout: { background: { color: "#0f172a" }, textColor: "#e2e8f0" }, width: ref.current.clientWidth, height: 320 });
    const series = chart.addCandlestickSeries();
    series.setData(data as never);
    return () => chart.remove();
  }, [data]);

  return <div ref={ref} />;
}
