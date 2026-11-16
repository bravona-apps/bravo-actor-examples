#!/usr/bin/env node
/**
 * Run bravona/steam-reviews-and-store-data and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/steam-reviews-and-store-data
 */

import { ApifyClient } from 'apify-client';

const ACTOR = 'bravona/steam-reviews-and-store-data';
const STORE_PAGE = 'https://apify.com/bravona/steam-reviews-and-store-data';

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable. See .env.example.');
  process.exit(1);
}

const client = new ApifyClient({ token });
const runInput = {
  appIds: [570],
  mode: 'both',
  reviewFilter: 'recent',
  language: 'english',
  maxReviewsPerApp: 3,
  country: 'us',
};

console.log(`Starting ${ACTOR} ...`);
console.log(`Pricing: see ${STORE_PAGE}`);

const run = await client.actor(ACTOR).call(runInput, { log: null });
const datasetId = run.defaultDatasetId;
console.log(`Run ${run.id} finished with status ${run.status}.`);

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
