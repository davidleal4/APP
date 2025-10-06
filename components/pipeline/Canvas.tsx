"use client";
import React from 'react';
import ReactFlow, { Background, Controls, MiniMap, addEdge, Connection, Edge, Node } from 'reactflow';
import 'reactflow/dist/style.css';

export function Canvas() {
  const [nodes, setNodes] = React.useState<Node[]>([]);
  const [edges, setEdges] = React.useState<Edge[]>([]);

  const onConnect = React.useCallback((connection: Connection) => setEdges((eds) => addEdge(connection, eds)), []);

  return (
    <div className="h-[calc(100vh-120px)]">
      <ReactFlow nodes={nodes} edges={edges} onConnect={onConnect} fitView>
        <Controls />
        <MiniMap />
        <Background gap={16} />
      </ReactFlow>
    </div>
  );
}
