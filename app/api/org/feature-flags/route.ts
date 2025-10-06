import { prisma } from '@/lib/db/prisma';

export async function GET() {
  const orgs = await prisma.organization.findMany({ select: { id: true, name: true, featureFlags: true } });
  return Response.json(orgs);
}

export async function POST(req: Request) {
  const { organizationId, flags } = await req.json();
  const updated = await prisma.organization.update({ where: { id: organizationId }, data: { featureFlags: flags } });
  return Response.json({ id: updated.id, featureFlags: updated.featureFlags });
}
