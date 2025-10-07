import { Executor, ExecutorResult } from '../types';
import { seededRandom, estimateCost } from '../utils';

export const openAIExecutor: Executor = async ({ nodeId, label, inputVars, runId }) => {
  const rnd = seededRandom(`${runId}:${nodeId}:${label}`);
  const tokensIn = 50 + Math.floor(rnd() * 50);
  const tokensOut = 80 + Math.floor(rnd() * 100);
  const costUSD = estimateCost(tokensIn + tokensOut, 0.005);
  const text = `OpenAI response (${label}) for ${Object.keys(inputVars).join(', ')}`;
  const result: ExecutorResult = { text, tokensIn, tokensOut, costUSD, outputVars: { text } };
  await new Promise((r) => setTimeout(r, 150 + Math.floor(rnd() * 300)));
  return result;
};
