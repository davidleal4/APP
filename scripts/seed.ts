import { PrismaClient, Plan, Role, RunStatus, DatasetKind, IntegrationProvider, SubscriptionStatus } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('Seeding en-AI demo data...');

  // Organizations
  const orgs = await Promise.all([
    prisma.organization.upsert({ where: { slug: 'alpha' }, update: {}, create: { name: 'Alpha Labs', slug: 'alpha', plan: Plan.PRO, seats: 10 } }),
    prisma.organization.upsert({ where: { slug: 'beta' }, update: {}, create: { name: 'Beta Systems', slug: 'beta', plan: Plan.TEAM, seats: 25 } }),
    prisma.organization.upsert({ where: { slug: 'gamma' }, update: {}, create: { name: 'Gamma AI', slug: 'gamma', plan: Plan.FREE, seats: 5 } }),
  ]);

  // Users
  const passwordHash = await bcrypt.hash('password', 10);
  const users = await Promise.all([
    prisma.user.upsert({ where: { email: 'owner@enai.local' }, update: {}, create: { email: 'owner@enai.local', name: 'Owner One', passwordHash, currentOrganizationId: orgs[0].id } }),
    prisma.user.upsert({ where: { email: 'admin@enai.local' }, update: {}, create: { email: 'admin@enai.local', name: 'Admin Two', passwordHash, currentOrganizationId: orgs[0].id } }),
    prisma.user.upsert({ where: { email: 'editor@enai.local' }, update: {}, create: { email: 'editor@enai.local', name: 'Editor Three', passwordHash, currentOrganizationId: orgs[0].id } }),
    prisma.user.upsert({ where: { email: 'viewer@enai.local' }, update: {}, create: { email: 'viewer@enai.local', name: 'Viewer Four', passwordHash, currentOrganizationId: orgs[1].id } }),
    prisma.user.upsert({ where: { email: 'analyst@enai.local' }, update: {}, create: { email: 'analyst@enai.local', name: 'Analyst Five', passwordHash, currentOrganizationId: orgs[1].id } }),
    prisma.user.upsert({ where: { email: 'guest@enai.local' }, update: {}, create: { email: 'guest@enai.local', name: 'Guest Six', passwordHash, currentOrganizationId: orgs[2].id } }),
  ]);

  // Memberships
  await prisma.membership.createMany({
    skipDuplicates: true,
    data: [
      { userId: users[0].id, organizationId: orgs[0].id, role: Role.OWNER },
      { userId: users[1].id, organizationId: orgs[0].id, role: Role.ADMIN },
      { userId: users[2].id, organizationId: orgs[0].id, role: Role.EDITOR },
      { userId: users[3].id, organizationId: orgs[1].id, role: Role.VIEWER },
      { userId: users[4].id, organizationId: orgs[1].id, role: Role.EDITOR },
      { userId: users[5].id, organizationId: orgs[2].id, role: Role.ADMIN },
    ],
  });

  // Projects
  const projectNames = ['SEO Optimizer', 'Meeting Minutes', 'RAG Triage', 'Summarizer', 'Ops Copilot', 'QA Evaluator', 'Data Labeler', 'Content Studio'];
  const projects = await Promise.all(projectNames.map((name, i) => prisma.project.create({
    data: {
      organizationId: orgs[i % orgs.length].id,
      name,
      description: `${name} project description`,
      tags: i % 2 === 0 ? ['prod', 'llm'] : ['eval', 'etl'],
      isSaved: i % 3 === 0,
      createdByUserId: users[i % users.length].id
    }
  })));

  // Pipelines with nodes/edges
  const nodeTypes = ['LLM','Transform','Evaluate','Loop','HTTP','Tool','Code','Branch','Merge','Memory','Delay','Webhook'];
  const pipelines = [] as { id: string }[];

  for (let i = 0; i < 12; i++) {
    const project = projects[i % projects.length];
    const pipeline = await prisma.pipeline.create({
      data: {
        projectId: project.id,
        name: `Pipeline ${i + 1}`,
        description: `Demo pipeline ${i + 1}`,
        version: 1,
        isPublic: i % 4 === 0,
        jsonSchema: { version: 1, createdBy: 'seed' },
        createdByUserId: users[(i + 1) % users.length].id
      }
    });

    const nodes = await Promise.all(
      Array.from({ length: 8 + (i % 5) }).map((_, n) => prisma.pipelineNode.create({
        data: {
          pipelineId: pipeline.id,
          type: nodeTypes[n % nodeTypes.length],
          label: `${nodeTypes[n % nodeTypes.length]} ${n + 1}`,
          x: 150 * n,
          y: 80 * (n % 4),
          config: { temperature: 0.7, budget: 0.01 * (n + 1) },
          version: 1,
        }
      }))
    );

    for (let e = 1; e < nodes.length; e++) {
      await prisma.pipelineEdge.create({
        data: {
          pipelineId: pipeline.id,
          sourceNodeId: nodes[e - 1].id,
          targetNodeId: nodes[e].id,
          condition: e % 4 === 0 ? { expression: 'score > 0.9' } : null,
        }
      });
    }

    pipelines.push(pipeline);
  }

  // Runs + steps
  for (const pipeline of pipelines) {
    for (let r = 0; r < 12; r++) {
      const running = await prisma.run.create({
        data: {
          pipelineId: pipeline.id,
          startedAt: new Date(Date.now() - Math.floor(Math.random() * 5) * 86400000),
          status: r % 7 === 0 ? RunStatus.FAILED : RunStatus.SUCCESS,
          tokenIn: 200 + r * 5,
          tokenOut: 180 + r * 4,
          costUSD: (0.02 + r * 0.001).toFixed(4) as unknown as number,
          error: r % 7 === 0 ? 'RateLimitExceeded' : null,
          finishedAt: new Date(),
        }
      });
      const steps = await prisma.pipelineNode.findMany({ where: { pipelineId: pipeline.id }, take: 6 });
      for (const [idx, node] of steps.entries()) {
        await prisma.runStep.create({
          data: {
            runId: running.id,
            nodeId: node.id,
            input: { text: 'Hello' },
            output: { text: `Output ${idx}` },
            tokenIn: 20 + idx * 2,
            tokenOut: 18 + idx * 2,
            durationMs: 100 + idx * 40,
            error: idx === 3 && r % 7 === 0 ? 'HTTP 429' : null,
          }
        });
      }
    }
  }

  // Prompts
  for (let i = 0; i < 10; i++) {
    await prisma.prompt.create({
      data: {
        organizationId: orgs[i % orgs.length].id,
        name: `Prompt ${i + 1}`,
        content: 'Summarize: {{text}} with tone {{tone}}',
        variables: { text: '', tone: 'neutral' },
        tests: [{ input: { text: 'Example', tone: 'formal' }, expect: { contains: 'Summary' } }],
        version: 1,
        tags: i % 2 === 0 ? ['seo', 'eval'] : ['rag']
      }
    });
  }

  // Datasets
  await prisma.dataset.createMany({
    data: [
      { organizationId: orgs[0].id, name: 'eval_blog_titles.json', description: 'Blog titles eval', items: [{ title: 'Great Post' }], kind: DatasetKind.EVAL },
      { organizationId: orgs[1].id, name: 'meeting_notes.csv', description: 'Meeting notes', items: [{ row: 'Alice, did X' }], kind: DatasetKind.CORPUS },
    ]
  });

  // Integrations
  await prisma.integration.createMany({
    data: [
      { organizationId: orgs[0].id, provider: IntegrationProvider.OPENAI, config: { model: 'gpt-4o' } },
      { organizationId: orgs[1].id, provider: IntegrationProvider.ANTHROPIC, config: { model: 'claude-3' } },
      { organizationId: orgs[2].id, provider: IntegrationProvider.GOOGLE, config: { model: 'gemini-pro' } },
      { organizationId: orgs[0].id, provider: IntegrationProvider.STRIPE, config: { customer: 'cus_test' } },
    ],
    skipDuplicates: true
  });

  // Subscription + credits
  await prisma.subscription.upsert({
    where: { organizationId: orgs[0].id },
    update: {},
    create: {
      organizationId: orgs[0].id,
      stripeCustomerId: 'cus_seed',
      stripeSubId: 'sub_seed',
      plan: Plan.PRO,
      status: SubscriptionStatus.ACTIVE,
    }
  });
  await prisma.creditLedger.createMany({
    data: [
      { organizationId: orgs[0].id, delta: 100000, reason: 'seed credits' },
      { organizationId: orgs[1].id, delta: 50000, reason: 'seed credits' },
      { organizationId: orgs[2].id, delta: 10000, reason: 'seed credits' },
    ]
  });

  // Audit logs
  await prisma.auditLog.create({ data: { organizationId: orgs[0].id, actorUserId: users[0].id, action: 'SEED', targetType: 'SYSTEM', targetId: 'seed', metadata: { ok: true } } });

  console.log('Seed complete.');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
