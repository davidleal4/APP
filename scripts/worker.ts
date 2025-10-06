import { runPipeline } from '@/lib/orchestrator/runner';

// Simple in-process worker runner stub
(async () => {
  console.log('Worker ready (stub). Waiting for jobs...');
  // In a real worker, we would subscribe to a queue.
  if (process.env.DEMO_RUN) {
    await runPipeline(process.env.DEMO_RUN, {});
  }
})();
