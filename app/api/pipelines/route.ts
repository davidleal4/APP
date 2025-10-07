import { prisma } from '@/lib/db/prisma';
import { NextRequest } from 'next/server';
import { z } from 'zod';

export async function GET() {
  const pipelines = await prisma.pipeline.findMany({ include: { project: true } });
  return Response.json(pipelines);
}

const createSchema = z.object({
  projectId: z.string(),
  name: z.string().min(1),
  description: z.string().optional(),
  jsonSchema: z.any()
});

export async function POST(req: NextRequest) {
  const data = createSchema.parse(await req.json());
  const pipeline = await prisma.pipeline.create({ data: { ...data } });
  return Response.json(pipeline);
}
