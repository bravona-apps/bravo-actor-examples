#!/usr/bin/env node
/**
 * Run bravona/docs-to-markdown-rag and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/docs-to-markdown-rag
 */

import { ApifyClient } from 'apify-client';
import { requireToken, startAndWait } from '../shared.js';

const ACTOR = 'bravona/docs-to-markdown-rag';
const STORE_PAGE = 'https://apify.com/bravona/docs-to-markdown-rag';

const client = new ApifyClient({ token: requireToken() });
const runInput = {
  urls: [
    { url: 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf' },
  ],
  ocrMode: 'off',
  includeMarkdown: true,
  includePages: true,
  includeChunks: true,
  maxDocuments: 1,
  maxPagesPerDocument: 5,
};

const run = await startAndWait(client, ACTOR, runInput, STORE_PAGE);
console.log(`Run ${run.id} finished with status ${run.status}.`);

const datasetId = run.defaultDatasetId;
const { items } = await client.dataset(datasetId).listItems();
console.log(`Dataset ${datasetId} has ${items.length} item(s).`);

for (const item of items.slice(0, 5)) {
  console.log(
    `- ${item.status} ${item.format} ${item.fileName || item.finalUrl} chars=${item.chars} chunks=${item.chunkCount}`,
  );
  if (item.markdown) {
    console.log(`  markdown: ${JSON.stringify(item.markdown.slice(0, 200))}`);
  }
}
if (items.length > 5) {
  console.log(`... plus ${items.length - 5} more`);
}
