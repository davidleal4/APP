import { prisma } from '@/lib/db/prisma';
import { Role } from '@prisma/client';

export async function GET() {
  const members = await prisma.membership.findMany({ include: { user: true, organization: true } });
  return Response.json(members);
}

export async function POST(req: Request) {
  const { userId, organizationId, role } = await req.json();
  const updated = await prisma.membership.upsert({ where: { userId_organizationId: { userId, organizationId } }, update: { role: role as Role }, create: { userId, organizationId, role: role as Role } });
  return Response.json(updated);
}
