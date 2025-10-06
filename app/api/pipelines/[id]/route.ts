import { prisma } from '@/lib/db/prisma';
import { NextRequest } from 'next/server';
import { z } from 'zod';

export async function GET(_: NextRequest, { params }: { params: { id: string } }) {
  const pipeline = await prisma.pipeline.findUnique({ where: { id: params.id }, include: { nodes: true, edges: true, project: true } });
  if (!pipeline) return new Response('Not found', { status: 404 });
  return Response.json(pipeline);
}

const updateSchema = z.object({
  name: z.string().optional(),
  description: z.string().optional(),
  jsonSchema: z.any().optional(),
  version: z.number().optional(),
  nodes: z.array(z.object({ id: z.string(), x: z.number(), y: z.number(), label: z.string().optional(), config: z.any().optional() })).optional(),
  edges: z.array(z.object({ id: z.string(), sourceNodeId: z.string(), targetNodeId: z.string(), condition: z.any().optional() })).optional()
});

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const data = updateSchema.parse(await req.json());
  const updates: any = {};
  if (data.name !== undefined) updates.name = data.name;
  if (data.description !== undefined) updates.description = data.description;
  if (data.jsonSchema !== undefined) updates.jsonSchema = data.jsonSchema;
  if (data.version !== undefined) updates.version = data.version;

  const result = await prisma.$transaction(async (tx) => {
    const updated = await tx.pipeline.update({ where: { id: params.id }, data: updates });
    if (data.nodes) {
      await Promise.all(data.nodes.map((n) => tx.pipelineNode.update({ where: { id: n.id }, data: { x: n.x, y: n.y, label: n.label, config: n.config as any } })));
    }
    if (data.edges) {
      await Promise.all(data.edges.map((e) => tx.pipelineEdge.update({ where: { id: e.id }, data: { sourceNodeId: e.sourceNodeId, targetNodeId: e.targetNodeId, condition: e.condition as any } })));
    }
    return updated;
  });
  return Response.json(result);
}
