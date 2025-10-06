import crypto from 'crypto';

export function seededRandom(seed: string): () => number {
  let h = crypto.createHash('sha256').update(seed).digest();
  let i = 0;
  return () => {
    const value = h[i % h.length] / 255;
    i += 1;
    return value;
  };
}

export function estimateCost(tokens: number, pricePer1K = 0.003): number {
  return Math.round((tokens / 1000) * pricePer1K * 10000) / 10000;
}
