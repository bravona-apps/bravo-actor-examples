/**
 * Shared helpers for the Bravona Actor examples.
 */

import { ApifyClient } from 'apify-client';

const TERMINAL_STATUSES = new Set(['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT', 'TIMED_OUT']);
const WAIT_TIMEOUT_SECS = 180;

export function requireToken() {
  const token = process.env.APIFY_TOKEN;
  if (!token) {
    console.error('Set the APIFY_TOKEN environment variable. See .env.example.');
    process.exit(1);
  }
  return token;
}

export function getClient() {
  return new ApifyClient({ token: requireToken() });
}

/**
 * Start a published Actor and poll its status until it finishes.
 *
 * Polls `client.run(id).get()` instead of the client's long-poll `call()` /
 * `waitForFinish()` helpers, which can hang on some networks after the run
 * has already succeeded.
 */
export async function startAndWait(client, actor, runInput, storePage, timeoutSecs = WAIT_TIMEOUT_SECS) {
  const started = await client.actor(actor).start(runInput);
  const runId = started.id;
  console.log(`Started ${actor} run ${runId}.`);
  console.log(`Pricing: see ${storePage}`);

  const deadline = Date.now() + timeoutSecs * 1000;
  while (true) {
    const run = await client.run(runId).get();
    if (!run) {
      console.error(`Could not load run ${runId}.`);
      process.exit(1);
    }
    if (TERMINAL_STATUSES.has(run.status)) {
      return run;
    }
    if (Date.now() >= deadline) {
      console.error(`Timed out waiting for run ${runId} (last status: ${run.status}).`);
      process.exit(1);
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}
