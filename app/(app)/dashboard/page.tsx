import { AreaTokens } from '@/components/charts/AreaTokens';
import { BarErrors } from '@/components/charts/BarErrors';
import { LineLatency } from '@/components/charts/LineLatency';

export default function DashboardPage() {
  const tokens = Array.from({ length: 7 }).map((_, i) => ({
    date: `D${i+1}`,
    openai: 1200 + i * 100,
    anthropic: 800 + i * 60,
    google: 900 + i * 80,
    deepseek: 600 + i * 50,
  }));
  const errors = [
    { type: 'LLM', errors: 12 },
    { type: 'HTTP', errors: 7 },
    { type: 'Evaluate', errors: 3 },
  ];
  const latency = Array.from({ length: 10 }).map((_, i) => ({ date: `D${i+1}`, p50: 350 + i * 5, p95: 800 + i * 10 }));

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-lg border bg-card p-4">KPI: Total Runs 150</div>
        <div className="rounded-lg border bg-card p-4">KPI: Success Rate 91%</div>
        <div className="rounded-lg border bg-card p-4">KPI: Avg Latency 420ms</div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-lg border bg-card p-4">
          <div className="mb-2 text-sm font-semibold">Tokens by provider</div>
          <AreaTokens data={tokens} />
        </div>
        <div className="rounded-lg border bg-card p-4">
          <div className="mb-2 text-sm font-semibold">Errors by node type</div>
          <BarErrors data={errors} />
        </div>
      </div>
      <div className="rounded-lg border bg-card p-4">
        <div className="mb-2 text-sm font-semibold">Latency</div>
        <LineLatency data={latency} />
      </div>
    </div>
  );
}
