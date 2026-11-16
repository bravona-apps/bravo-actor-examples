#!/usr/bin/env node
/**
 * Run bravona/remote-jobs-multi-board-feed and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/remote-jobs-multi-board-feed
 */

import { ApifyClient } from 'apify-client';

const ACTOR = 'bravona/remote-jobs-multi-board-feed';
const STORE_PAGE = 'https://apify.com/bravona/remote-jobs-multi-board-feed';

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable. See .env.example.');
  process.exit(1);
}

const client = new ApifyClient({ token });
const runInput = {
  keywords: ['python'],
  searchInDescription: false,
  includeWorldwide: true,
  sources: ['jobicy', 'remoteok', 'weworkremotely'],
  maxResults: 5,
  sortBy: 'newest',
  includeDescription: false,
  includeDescriptionHtml: false,
  includeOnsiteArbeitnow: false,
  onlyNewSinceLastRun: false,
};

console.log(`Starting ${ACTOR} ...`);
console.log(`Pricing: see ${STORE_PAGE}`);

const run = await client.actor(ACTOR).call(runInput);
const datasetId = run.defaultDatasetId;
console.log(`Run ${run.id} finished with status ${run.status}.`);

const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(`- ${item.sourceName}: ${item.title} at ${item.company} (${item.remoteRegion || item.location})\n  ${item.sourceUrl}`);
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
