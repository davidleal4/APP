import { Executor, ExecutorResult } from '../types';
import { seededRandom, estimateCost } from '../utils';

export const deepseekExecutor: Executor = async ({ nodeId, label, runId }) => {
  const rnd = seededRandom(`deep:${runId}:${nodeId}:${label}`);
  const tokensIn = 30 + Math.floor(rnd() * 40);
  const tokensOut = 50 + Math.floor(rnd() * 70);
  const costUSD = estimateCost(tokensIn + tokensOut, 0.0035);
  const text = `DeepSeek response (${label})`;
  await new Promise((r) => setTimeout(r, 100 + Math.floor(rnd() * 200)));
  const result: ExecutorResult = { text, tokensIn, tokensOut, costUSD, outputVars: { text } };
  return result;
};
