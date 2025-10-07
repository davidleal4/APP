export type NodeType =
  | 'LLM'
  | 'Embedding'
  | 'HTTP'
  | 'Tool'
  | 'Code'
  | 'Map'
  | 'Filter'
  | 'Reduce'
  | 'Branch'
  | 'Loop'
  | 'Merge'
  | 'Memory'
  | 'Evaluate'
  | 'Human'
  | 'Delay'
  | 'RateLimit'
  | 'Webhook'
  | 'Stop';

export interface ExecutorResult {
  text?: string;
  tokensIn: number;
  tokensOut: number;
  costUSD: number;
  outputVars?: Record<string, unknown>;
}

export interface ExecutorContext {
  nodeId: string;
  type: NodeType;
  label: string;
  config: any;
  inputVars: Record<string, unknown>;
  runId: string;
}

export type Executor = (ctx: ExecutorContext) => Promise<ExecutorResult>;
