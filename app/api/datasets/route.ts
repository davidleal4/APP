import { prisma } from '@/lib/db/prisma';
import { NextRequest } from 'next/server';
import { z } from 'zod';

export async function GET() {
  const datasets = await prisma.dataset.findMany({});
  return Response.json(datasets);
}

const schema = z.object({ organizationId: z.string(), name: z.string(), description: z.string().optional(), items: z.any(), kind: z.enum(['EVAL','CORPUS']) });
export async function POST(req: NextRequest) {
  const data = schema.parse(await req.json());
  const created = await prisma.dataset.create({ data });
  return Response.json(created);
}
