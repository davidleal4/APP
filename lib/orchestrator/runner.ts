import { prisma } from '@/lib/db/prisma';
import { runEmitter } from '@/lib/sse/emitter';
import { openAIExecutor } from './executors/openai';
import { anthropicExecutor } from './executors/anthropic';
import { googleExecutor } from './executors/google';
import { deepseekExecutor } from './executors/deepseek';
import { Executor } from './types';
import { RunStatus } from '@prisma/client';

function pickExecutor(type: string): Executor {
  switch (type) {
    case 'LLM':
      return openAIExecutor;
    case 'Evaluate':
      return anthropicExecutor;
    case 'Transform':
      return googleExecutor;
    default:
      return deepseekExecutor;
  }
}

export async function runPipeline(pipelineId: string, inputVars: Record<string, unknown> = {}) {
  const pipeline = await prisma.pipeline.findUnique({
    where: { id: pipelineId },
    include: { nodes: true, edges: true }
  });
  if (!pipeline) throw new Error('Pipeline not found');

  const run = await prisma.run.create({ data: { pipelineId, status: RunStatus.RUNNING } });
  runEmitter.emit({ type: 'RUN_STARTED', runId: run.id, pipelineId, ts: Date.now() });

  try {
    // naive: walk nodes in insertion order, ignore graph for stub
    let totalIn = 0;
    let totalOut = 0;
    let totalCost = 0;
    const vars = { ...inputVars };

    for (const node of pipeline.nodes) {
      const exec = pickExecutor(node.type);
      runEmitter.emit({ type: 'STEP_STARTED', runId: run.id, nodeId: node.id, label: node.label, ts: Date.now() });
      const res = await exec({ nodeId: node.id, type: node.type as any, label: node.label, config: node.config, inputVars: vars, runId: run.id });
      await prisma.runStep.create({
        data: {
          runId: run.id,
          nodeId: node.id,
          input: vars,
          output: res.outputVars ?? { text: res.text },
          tokenIn: res.tokensIn,
          tokenOut: res.tokensOut,
          durationMs: 100,
        }
      });
      totalIn += res.tokensIn;
      totalOut += res.tokensOut;
      totalCost += res.costUSD;
      Object.assign(vars, res.outputVars);
      runEmitter.emit({ type: 'STEP_FINISHED', runId: run.id, nodeId: node.id, tokenIn: res.tokensIn, tokenOut: res.tokensOut, costUSD: res.costUSD, output: res.outputVars, ts: Date.now() });
    }

    await prisma.run.update({ where: { id: run.id }, data: { status: RunStatus.SUCCESS, tokenIn: totalIn, tokenOut: totalOut, costUSD: totalCost, finishedAt: new Date() } });
    runEmitter.emit({ type: 'RUN_FINISHED', runId: run.id, tokenIn: totalIn, tokenOut: totalOut, costUSD: totalCost, ts: Date.now() });

    return { runId: run.id };
  } catch (err: any) {
    await prisma.run.update({ where: { id: run.id }, data: { status: RunStatus.FAILED, error: String(err), finishedAt: new Date() } });
    runEmitter.emit({ type: 'RUN_FAILED', runId: run.id, error: String(err), ts: Date.now() });
    throw err;
  }
}
