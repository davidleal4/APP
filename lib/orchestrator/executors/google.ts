import { Executor, ExecutorResult } from '../types';
import { seededRandom, estimateCost } from '../utils';

export const googleExecutor: Executor = async ({ nodeId, label, runId }) => {
  const rnd = seededRandom(`goog:${runId}:${nodeId}:${label}`);
  const tokensIn = 40 + Math.floor(rnd() * 50);
  const tokensOut = 60 + Math.floor(rnd() * 90);
  const costUSD = estimateCost(tokensIn + tokensOut, 0.004);
  const text = `Gemini response (${label})`;
  await new Promise((r) => setTimeout(r, 120 + Math.floor(rnd() * 250)));
  const result: ExecutorResult = { text, tokensIn, tokensOut, costUSD, outputVars: { text } };
  return result;
};
