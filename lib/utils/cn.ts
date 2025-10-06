import { twMerge } from 'tailwind-merge';

type ClassValue = string | undefined | null | false | ClassValue[] | { [k: string]: boolean };

export function cn(...inputs: ClassValue[]): string {
  const flat: string[] = [];
  for (const input of inputs) {
    if (!input) continue;
    if (typeof input === 'string') flat.push(input);
    else if (Array.isArray(input)) flat.push(cn(...input));
    else if (typeof input === 'object') {
      for (const key of Object.keys(input)) if ((input as any)[key]) flat.push(key);
    }
  }
  return twMerge(flat.join(' '));
}
