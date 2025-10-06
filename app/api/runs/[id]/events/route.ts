import { NextRequest } from 'next/server';
import { runEmitter, RunEvent } from '@/lib/sse/emitter';

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  const runId = params.id;
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      const send = (event: RunEvent) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
      };
      runEmitter.on(runId, send);
      // heartbeat
      const interval = setInterval(() => controller.enqueue(encoder.encode(': ping\n\n')), 15000);
      (controller as any)._cleanup = () => {
        clearInterval(interval);
        runEmitter.off(runId, send);
      };
    },
    cancel() {
      const anyController = this as any;
      anyController._cleanup?.();
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive'
    }
  });
}
