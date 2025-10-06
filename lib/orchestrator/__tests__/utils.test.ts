import { describe, it, expect } from 'vitest';
import { estimateCost, seededRandom } from '../utils';

describe('utils', () => {
  it('estimateCost rounds to 4 decimals', () => {
    expect(estimateCost(1234, 0.01)).toBe(0.0123);
  });

  it('seededRandom produces deterministic values', () => {
    const r1 = seededRandom('abc');
    const r2 = seededRandom('abc');
    expect([r1(), r1(), r1()]).toEqual([r2(), r2(), r2()]);
  });
});
