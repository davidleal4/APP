"use client";
import { Line, LineChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export function LineLatency({ data }: { data: Array<{ date: string; p50: number; p95: number }> }) {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line dataKey="p50" stroke="#10b981" />
          <Line dataKey="p95" stroke="#f59e0b" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
