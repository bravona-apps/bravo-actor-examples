#!/usr/bin/env node
/**
 * Run bravona/steam-reviews-and-store-data and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/steam-reviews-and-store-data
 */

import { ApifyClient } from 'apify-client';
import { requireToken, startAndWait } from '../shared.js';

const ACTOR = 'bravona/steam-reviews-and-store-data';
const STORE_PAGE = 'https://apify.com/bravona/steam-reviews-and-store-data';

const client = new ApifyClient({ token: requireToken() });
const runInput = {
  appIds: [570],
  mode: 'both',
  reviewFilter: 'recent',
  language: 'english',
  maxReviewsPerApp: 3,
  country: 'us',
};

const run = await startAndWait(client, ACTOR, runInput, STORE_PAGE);
console.log(`Run ${run.id} finished with status ${run.status}.`);

const datasetId = run.defaultDatasetId;
const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  if (item.itemType === 'game-details') {
    console.log(
      `- [game-details] ${item.appName} (app ${item.appId}) ${item.reviewScoreDesc} ${item.storeUrl}`,
    );
  } else {
    const text = (item.text || '').slice(0, 120);
    console.log(`- [review] ${item.appName}: votedUp=${item.votedUp} ${JSON.stringify(text)}`);
  }
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
