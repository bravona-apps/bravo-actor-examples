#!/usr/bin/env node
/**
 * Run bravona/screenshot-pdf-renderer and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/screenshot-pdf-renderer
 */

import { ApifyClient } from 'apify-client';

const ACTOR = 'bravona/screenshot-pdf-renderer';
const STORE_PAGE = 'https://apify.com/bravona/screenshot-pdf-renderer';

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable. See .env.example.');
  process.exit(1);
}

const client = new ApifyClient({ token });
const runInput = {
  urls: ['https://example.com'],
  format: 'png',
  fullPage: false,
  devicePreset: 'desktop',
  maxCaptures: 1,
  blockAdsAndTrackers: true,
  respectRobotsTxt: true,
};

console.log(`Starting ${ACTOR} ...`);
console.log(`Pricing: see ${STORE_PAGE}`);

const run = await client.actor(ACTOR).call(runInput, { log: null });
const datasetId = run.defaultDatasetId;
console.log(`Run ${run.id} finished with status ${run.status}.`);

const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(`- ${item.status} ${item.format} ${item.title} ${item.widthPx}x${item.heightPx} ${item.fileUrl}`);
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
