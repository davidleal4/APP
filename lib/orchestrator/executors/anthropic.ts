import { Executor, ExecutorResult } from '../types';
import { seededRandom, estimateCost } from '../utils';

export const anthropicExecutor: Executor = async ({ nodeId, label, inputVars, runId }) => {
  const rnd = seededRandom(`anth:${runId}:${nodeId}:${label}`);
  const tokensIn = 60 + Math.floor(rnd() * 60);
  const tokensOut = 70 + Math.floor(rnd() * 120);
  const costUSD = estimateCost(tokensIn + tokensOut, 0.006);
  const text = `Anthropic response (${label})`; 
  const result: ExecutorResult = { text, tokensIn, tokensOut, costUSD, outputVars: { text } };
  await new Promise((r) => setTimeout(r, 160 + Math.floor(rnd() * 320)));
  return result;
};
