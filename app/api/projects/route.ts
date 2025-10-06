import { prisma } from '@/lib/db/prisma';
import { NextRequest } from 'next/server';
import { z } from 'zod';

export async function GET() {
  const projects = await prisma.project.findMany({ include: { pipelines: true } });
  return Response.json(projects);
}

const createSchema = z.object({
  organizationId: z.string(),
  name: z.string().min(1),
  description: z.string().optional(),
  tags: z.array(z.string()).default([])
});

export async function POST(req: NextRequest) {
  const data = createSchema.parse(await req.json());
  const project = await prisma.project.create({ data });
  return Response.json(project);
}
