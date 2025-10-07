"use client";
import { useEffect, useState } from 'react';

export function RunConsole({ runId }: { runId?: string }) {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    if (!runId) return;
    const es = new EventSource(`/api/runs/${runId}/events`);
    es.onmessage = (e) => {
      setLogs((prev) => [...prev, e.data]);
    };
    return () => es.close();
  }, [runId]);

  return (
    <div className="rounded-md border bg-card p-3 h-48 overflow-auto text-xs font-mono">
      {logs.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  );
}
