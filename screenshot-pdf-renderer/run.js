#!/usr/bin/env node
/**
 * Run bravona/screenshot-pdf-renderer and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/screenshot-pdf-renderer
 */

import { ApifyClient } from 'apify-client';
import { requireToken, startAndWait } from '../shared.js';

const ACTOR = 'bravona/screenshot-pdf-renderer';
const STORE_PAGE = 'https://apify.com/bravona/screenshot-pdf-renderer';

const client = new ApifyClient({ token: requireToken() });
const runInput = {
  urls: ['https://example.com'],
  format: 'png',
  fullPage: false,
  devicePreset: 'desktop',
  maxCaptures: 1,
  blockAdsAndTrackers: true,
  respectRobotsTxt: true,
};

const run = await startAndWait(client, ACTOR, runInput, STORE_PAGE);
console.log(`Run ${run.id} finished with status ${run.status}.`);

const datasetId = run.defaultDatasetId;
const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(
    `- ${item.status} ${item.format} ${item.title} ${item.widthPx}x${item.heightPx} ${item.fileUrl}`,
  );
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
