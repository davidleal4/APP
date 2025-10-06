import { NextRequest } from 'next/server';
import { prisma } from '@/lib/db/prisma';

const templates = [
  {
    id: 'seo-feedback-loop',
    name: 'SEO Feedback Loop',
    description: 'OpenAI → Transform → Evaluate → Loop until score ≥ 0.9 → Publish',
    nodes: [
      { type: 'LLM', label: 'Draft', x: 0, y: 0, config: { temperature: 0.7 } },
      { type: 'Transform', label: 'Polish', x: 200, y: 0, config: {} },
      { type: 'Evaluate', label: 'Quality', x: 400, y: 0, config: { target: 0.9 } },
      { type: 'Loop', label: 'Loop', x: 600, y: 0, config: { maxIterations: 5 } },
      { type: 'Webhook', label: 'Publish', x: 800, y: 0, config: { url: 'https://example.com' } }
    ]
  },
  {
    id: 'tri-model-summarizer',
    name: 'Tri-Model Summarizer',
    description: 'Anthropic + DeepSeek + Gemini → Merge → Evaluate → Selector → Output',
    nodes: [
      { type: 'LLM', label: 'Anthropic', x: 0, y: 0, config: {} },
      { type: 'LLM', label: 'DeepSeek', x: 0, y: 120, config: {} },
      { type: 'LLM', label: 'Gemini', x: 0, y: 240, config: {} },
      { type: 'Merge', label: 'Merge', x: 260, y: 120, config: {} },
      { type: 'Evaluate', label: 'Rank', x: 480, y: 120, config: {} }
    ]
  },
  {
    id: 'rag-triage',
    name: 'RAG Triage',
    description: 'Embedding → Memory Query → LLM → Tool (HTTP) → Branch',
    nodes: [
      { type: 'Embedding', label: 'Embed', x: 0, y: 0, config: {} },
      { type: 'Memory', label: 'Query', x: 200, y: 0, config: {} },
      { type: 'LLM', label: 'Draft', x: 400, y: 0, config: {} },
      { type: 'HTTP', label: 'Fetch', x: 600, y: 0, config: { url: 'https://api.example.com' } },
      { type: 'Branch', label: 'Branch', x: 800, y: 0, config: { expression: 'score > 0.7' } }
    ]
  }
];

export async function GET() {
  return Response.json(templates.map(({ nodes, ...t }) => t));
}

export async function POST(req: NextRequest) {
  const { projectId, templateId } = await req.json();
  const tpl = templates.find((t) => t.id === templateId);
  if (!tpl) return new Response('Not found', { status: 404 });

  const created = await prisma.$transaction(async (tx) => {
    const pipeline = await tx.pipeline.create({ data: { projectId, name: tpl.name, description: tpl.description, jsonSchema: { templateId: tpl.id } } });
    const nodes = await Promise.all(tpl.nodes.map((n, i) => tx.pipelineNode.create({ data: { pipelineId: pipeline.id, type: n.type, label: n.label, x: n.x, y: n.y, config: n.config, version: 1 } })));
    for (let i = 1; i < nodes.length; i++) {
      await tx.pipelineEdge.create({ data: { pipelineId: pipeline.id, sourceNodeId: nodes[i - 1].id, targetNodeId: nodes[i].id } });
    }
    return pipeline;
  });
  return Response.json(created);
}
