"use client";
import useSWR from 'swr';
import Link from 'next/link';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export default function PipelinesPage() {
  const { data } = useSWR('/api/pipelines', fetcher);
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Pipelines</h1>
      <div className="rounded-lg border bg-card p-4">
        <div className="grid gap-2">
          {data?.map((p: any) => (
            <Link key={p.id} href={`/pipelines/${p.id}`} className="rounded-md border p-3 hover:bg-accent/40">
              <div className="text-sm font-medium">{p.name}</div>
              <div className="text-xs text-muted-foreground">Project: {p.project?.name}</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
