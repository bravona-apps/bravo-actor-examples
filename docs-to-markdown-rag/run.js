#!/usr/bin/env node
/**
 * Run bravona/docs-to-markdown-rag and print a few dataset items.
 *
 * Requires the APIFY_TOKEN environment variable.
 * Pricing: see the Store page https://apify.com/bravona/docs-to-markdown-rag
 */

import { ApifyClient } from 'apify-client';

const ACTOR = 'bravona/docs-to-markdown-rag';
const STORE_PAGE = 'https://apify.com/bravona/docs-to-markdown-rag';

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable. See .env.example.');
  process.exit(1);
}

const client = new ApifyClient({ token });
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

console.log(`Starting ${ACTOR} ...`);
console.log(`Pricing: see ${STORE_PAGE}`);

const run = await client.actor(ACTOR).call(runInput, { log: null });
const datasetId = run.defaultDatasetId;
console.log(`Run ${run.id} finished with status ${run.status}.`);

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
