#!/usr/bin/env node
/**
 * Run bravona/academic-papers-search and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/academic-papers-search
 */

import { ApifyClient } from 'apify-client';
import { requireToken, startAndWait } from '../shared.js';

const ACTOR = 'bravona/academic-papers-search';
const STORE_PAGE = 'https://apify.com/bravona/academic-papers-search';

const client = new ApifyClient({ token: requireToken() });
const runInput = {
  query: 'CRISPR',
  sources: ['openalex'],
  maxResults: 3,
  dedupe: true,
};

const run = await startAndWait(client, ACTOR, runInput, STORE_PAGE);
console.log(`Run ${run.id} finished with status ${run.status}.`);

const datasetId = run.defaultDatasetId;
const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(
    `- ${item.title} (${item.year}) doi=${item.doi} sources=${JSON.stringify(item.foundIn)}\n  ${item.sourceUrl}`,
  );
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
