"use client";
import { Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export function AreaTokens({ data }: { data: Array<{ date: string; openai: number; anthropic: number; google: number; deepseek: number }> }) {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ left: 8, right: 8, top: 8 }}>
          <defs>
            <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#60a5fa" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#60a5fa" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="openai" stackId="1" stroke="#60a5fa" fill="url(#g1)" />
          <Area type="monotone" dataKey="anthropic" stackId="1" stroke="#f59e0b" fillOpacity={0.3} fill="#f59e0b" />
          <Area type="monotone" dataKey="google" stackId="1" stroke="#22c55e" fillOpacity={0.3} fill="#22c55e" />
          <Area type="monotone" dataKey="deepseek" stackId="1" stroke="#a78bfa" fillOpacity={0.3} fill="#a78bfa" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
