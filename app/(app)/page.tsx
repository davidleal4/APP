export default function HomePage() {
  return (
    <div className="p-4 grid grid-cols-12 gap-4">
      <section className="col-span-12 lg:col-span-4 space-y-2">
        <div className="rounded-lg border bg-card p-4">AI Agent (stub)</div>
        <div className="rounded-lg border bg-card p-4">Run Mini-Pipeline (stub)</div>
      </section>
      <section className="col-span-12 lg:col-span-5 space-y-2">
        <div className="rounded-lg border bg-card p-4">Projects Grid (stub)</div>
        <div className="rounded-lg border bg-card p-4">Saved Projects (stub)</div>
      </section>
      <section className="col-span-12 lg:col-span-3 space-y-2">
        <div className="rounded-lg border bg-card p-4">Insights KPIs (stub)</div>
        <div className="rounded-lg border bg-card p-4">Weekly Usage Chart (stub)</div>
        <div className="rounded-lg border bg-card p-4">Top Failing Nodes (stub)</div>
      </section>
    </div>
  );
}
