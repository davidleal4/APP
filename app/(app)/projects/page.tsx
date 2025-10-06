"use client";
import useSWR from 'swr';
import Link from 'next/link';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export default function ProjectsPage() {
  const { data } = useSWR('/api/projects', fetcher);
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Projects</h1>
      <div className="rounded-lg border bg-card p-4 grid md:grid-cols-3 gap-3">
        {data?.map((p: any) => (
          <Link key={p.id} href={`/projects/${p.id}`} className="rounded-md border p-3 hover:bg-accent/40">
            <div className="text-sm font-semibold">{p.name}</div>
            <div className="text-xs text-muted-foreground">Pipelines: {p.pipelines?.length ?? 0}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
