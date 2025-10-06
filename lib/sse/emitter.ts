import { EventEmitter } from 'events';

export type RunEvent =
  | { type: 'RUN_STARTED'; runId: string; pipelineId: string; ts: number }
  | { type: 'STEP_STARTED'; runId: string; nodeId: string; label: string; ts: number }
  | { type: 'STEP_FINISHED'; runId: string; nodeId: string; tokenIn: number; tokenOut: number; costUSD: number; output?: any; ts: number }
  | { type: 'LOG'; runId: string; message: string; ts: number }
  | { type: 'RUN_FINISHED'; runId: string; tokenIn: number; tokenOut: number; costUSD: number; ts: number }
  | { type: 'RUN_FAILED'; runId: string; error: string; ts: number };

class RunEmitter {
  private emitter = new EventEmitter({ captureRejections: false });

  on(runId: string, listener: (event: RunEvent) => void) {
    this.emitter.on(runId, listener);
  }

  off(runId: string, listener: (event: RunEvent) => void) {
    this.emitter.off(runId, listener);
  }

  emit(event: RunEvent) {
    this.emitter.emit(event.runId, event);
  }
}

export const runEmitter = new RunEmitter();
