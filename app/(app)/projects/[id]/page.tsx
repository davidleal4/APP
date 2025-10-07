export default function ProjectDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Project {params.id}</h1>
      <div className="rounded-lg border bg-card p-4">Tabs: Overview | Pipelines | Runs | Prompts | Datasets | Team | Settings (stub)</div>
    </div>
  );
}
