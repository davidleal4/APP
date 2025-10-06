"use client";
import { Button } from '@/components/ui/button';

const palette = ['LLM', 'Embedding', 'HTTP', 'Tool', 'Code', 'Map', 'Filter', 'Reduce', 'Branch', 'Loop', 'Merge', 'Memory', 'Evaluate', 'Human', 'Delay', 'RateLimit', 'Webhook', 'Stop'];

export function NodePalette() {
  return (
    <div className="space-y-2">
      <div className="text-sm font-semibold">Node Palette</div>
      <div className="grid grid-cols-2 gap-2">
        {palette.map((p) => (
          <Button key={p} variant="outline" className="justify-start">{p}</Button>
        ))}
      </div>
    </div>
  );
}
