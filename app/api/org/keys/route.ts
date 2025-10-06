import { prisma } from '@/lib/db/prisma';
import crypto from 'crypto';

export async function GET() {
  const keys = await prisma.apiKey.findMany({ take: 20 });
  return Response.json(keys.map(k => ({ id: k.id, name: k.name, scopes: k.scopes, createdAt: k.createdAt })));
}

export async function POST(req: Request) {
  const { organizationId, name, scopes } = await req.json();
  const plain = `enai_${crypto.randomBytes(16).toString('hex')}`;
  const hashedKey = crypto.createHash('sha256').update(plain).digest('hex');
  const created = await prisma.apiKey.create({ data: { organizationId, name, scopes: scopes ?? [], hashedKey } });
  return Response.json({ id: created.id, key: plain });
}
