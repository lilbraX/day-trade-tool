"use client";

import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from "recharts";
import { Dist, HoldPoint, XY } from "@/lib/types";

export function DailyPnlChart({ data }: { data: XY[] }) {
  return <ChartCard title="日別損益"><ResponsiveContainer width="100%" height={260}><LineChart data={data}><CartesianGrid stroke="#334155" /><XAxis dataKey="x" /><YAxis /><Tooltip /><Line dataKey="y" stroke="#22c55e" /></LineChart></ResponsiveContainer></ChartCard>;
}

export function TimeSlotChart({ data }: { data: XY[] }) {
  return <ChartCard title="時間帯別パフォーマンス"><ResponsiveContainer width="100%" height={260}><BarChart data={data}><CartesianGrid stroke="#334155" /><XAxis dataKey="x" /><YAxis /><Tooltip /><Bar dataKey="y" fill="#38bdf8" /></BarChart></ResponsiveContainer></ChartCard>;
}

export function DistributionChart({ data }: { data: Dist[] }) {
  return <ChartCard title="損益分布"><ResponsiveContainer width="100%" height={260}><BarChart data={data}><CartesianGrid stroke="#334155" /><XAxis dataKey="bucket" /><YAxis /><Tooltip /><Bar dataKey="count" fill="#a78bfa" /></BarChart></ResponsiveContainer></ChartCard>;
}

export function HoldVsPnlChart({ data }: { data: HoldPoint[] }) {
  return <ChartCard title="保有時間 vs 損益"><ResponsiveContainer width="100%" height={260}><ScatterChart><CartesianGrid stroke="#334155" /><XAxis dataKey="hold_minutes" name="hold" /><YAxis dataKey="pnl" name="pnl" /><Tooltip cursor={{ strokeDasharray: "3 3" }} /><Scatter data={data} fill="#f59e0b" /></ScatterChart></ResponsiveContainer></ChartCard>;
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {children}
    </div>
  );
}
