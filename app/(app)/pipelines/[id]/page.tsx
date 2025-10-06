"use client";
import React from 'react';
import { Button } from '@/components/ui/button';
import { NodePalette } from '@/components/pipeline/NodePalette';
import { NodeInspector } from '@/components/pipeline/NodeInspector';
import { Canvas } from '@/components/pipeline/Canvas';
import { RunConsole } from '@/components/pipeline/RunConsole';

export default function PipelineEditorPage({ params }: { params: { id: string } }) {
  const [runId, setRunId] = React.useState<string | undefined>(undefined);

  const run = async () => {
    const res = await fetch(`/api/pipelines/${params.id}/run`, { method: 'POST', body: JSON.stringify({}) });
    const json = await res.json();
    setRunId(json.runId);
  };

  return (
    <div className="grid grid-cols-12 gap-3 p-3">
      <div className="col-span-12 lg:col-span-2 space-y-3">
        <NodePalette />
        <Button onClick={run} className="w-full">Run</Button>
      </div>
      <div className="col-span-12 lg:col-span-7">
        <Canvas />
      </div>
      <div className="col-span-12 lg:col-span-3 space-y-3">
        <NodeInspector />
        <RunConsole runId={runId} />
      </div>
    </div>
  );
}
