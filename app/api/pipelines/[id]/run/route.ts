import { NextRequest } from 'next/server';
import { z } from 'zod';
import { runPipeline } from '@/lib/orchestrator/runner';

const bodySchema = z.object({ inputVars: z.record(z.any()).optional() });

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  const json = await req.json().catch(() => ({}));
  const body = bodySchema.parse(json);
  const result = await runPipeline(params.id, body.inputVars ?? {});
  return Response.json(result);
}
