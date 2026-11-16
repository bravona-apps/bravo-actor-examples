#!/usr/bin/env node
/**
 * Run bravona/remote-jobs-multi-board-feed and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/remote-jobs-multi-board-feed
 */

import { ApifyClient } from 'apify-client';
import { requireToken, startAndWait } from '../shared.js';

const ACTOR = 'bravona/remote-jobs-multi-board-feed';
const STORE_PAGE = 'https://apify.com/bravona/remote-jobs-multi-board-feed';

const client = new ApifyClient({ token: requireToken() });
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

const run = await startAndWait(client, ACTOR, runInput, STORE_PAGE);
console.log(`Run ${run.id} finished with status ${run.status}.`);

const datasetId = run.defaultDatasetId;
const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(
    `- ${item.sourceName}: ${item.title} at ${item.company} (${item.remoteRegion || item.location})\n  ${item.sourceUrl}`,
  );
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
