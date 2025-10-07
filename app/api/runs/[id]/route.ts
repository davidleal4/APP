import { prisma } from '@/lib/db/prisma';

export async function GET(_: Request, { params }: { params: { id: string } }) {
  const run = await prisma.run.findUnique({ where: { id: params.id }, include: { steps: true, pipeline: true } });
  if (!run) return new Response('Not found', { status: 404 });
  return Response.json(run);
}
