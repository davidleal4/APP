import { prisma } from '@/lib/db/prisma';
import { z } from 'zod';
import { NextRequest } from 'next/server';

export async function GET() {
  const prompts = await prisma.prompt.findMany({});
  return Response.json(prompts);
}

const schema = z.object({ organizationId: z.string(), name: z.string(), content: z.string(), variables: z.any(), tags: z.array(z.string()).default([]) });
export async function POST(req: NextRequest) {
  const data = schema.parse(await req.json());
  const created = await prisma.prompt.create({ data: { ...data, version: 1 } });
  return Response.json(created);
}
