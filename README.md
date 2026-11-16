# Bravona Apify Actor examples

Short, runnable examples that call [Bravona](https://apify.com/bravona)'s public Apify Actors through the official `apify-client` libraries. This repository does **not** include Actor source code. Each example starts a run of a published Actor and prints a few dataset items.

Current pricing for every Actor is on its Store page. This repository does not list prices.

## Actors

All six Store pages below were checked and returned HTTP 200 with the slugs shown.

| Actor | Store page | Example folder |
| --- | --- | --- |
| Academic Paper Search: OpenAlex, PubMed, arXiv | https://apify.com/bravona/academic-papers-search | [`academic-papers-search/`](academic-papers-search/) |
| Steam Reviews and Store Data Scraper for Games | https://apify.com/bravona/steam-reviews-and-store-data | [`steam-reviews-and-store-data/`](steam-reviews-and-store-data/) |
| Greenhouse, Lever and Ashby Jobs Scraper | https://apify.com/bravona/ats-jobs-greenhouse-lever-ashby | [`ats-jobs-greenhouse-lever-ashby/`](ats-jobs-greenhouse-lever-ashby/) |
| Documents to Markdown/JSON for RAG (PDF, Office, OCR) | https://apify.com/bravona/docs-to-markdown-rag | [`docs-to-markdown-rag/`](docs-to-markdown-rag/) |
| Website Screenshot and URL/HTML to PDF Renderer | https://apify.com/bravona/screenshot-pdf-renderer | [`screenshot-pdf-renderer/`](screenshot-pdf-renderer/) |
| Remote Jobs Aggregator: Remote OK, WWR, Jobicy | https://apify.com/bravona/remote-jobs-multi-board-feed | [`remote-jobs-multi-board-feed/`](remote-jobs-multi-board-feed/) |

Each folder has:

- `run.py` — Python example using `apify-client`
- `run.js` — Node.js example using `apify-client`
- `sample-output.json` — a small, trimmed sample in the real dataset shape, using public or clearly fictional data (no personal emails)

The examples call each Actor by its `bravona/<slug>` name and use inputs that match the published input schema, with small limits so a first run stays inexpensive. See the Store page of the Actor you run for current pricing.

## Setup

1. Create an Apify API token in [Apify Console → Settings → Integrations](https://console.apify.com/settings/integrations).
2. Copy [`.env.example`](.env.example) to `.env` and set `APIFY_TOKEN`, or export it in your shell:

   ```bash
   export APIFY_TOKEN=your_apify_token_here
   ```

3. Install dependencies.

   Python:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   Node.js 18+:

   ```bash
   npm install
   ```

## Run an example

```bash
python academic-papers-search/run.py
node academic-papers-search/run.js
# or: npm run academic
```

The same pattern works in every Actor folder. The scripts start the Actor through `apify-client`, poll run status until it finishes, then print a few dataset items. Shared helpers live in `shared.py` and `shared.js`. `sample-output.json` is a static illustration of the dataset shape; running the script talks to the live Actor and returns fresh results.

## Workflows

[`workflows/`](workflows/) has two starter integrations:

- [`langchain_docs_to_documents.py`](workflows/langchain_docs_to_documents.py) — runs `bravona/docs-to-markdown-rag` and loads Markdown chunks into LangChain `Document` objects.
- [`n8n-academic-papers-search.json`](workflows/n8n-academic-papers-search.json) — an importable n8n workflow that calls `bravona/academic-papers-search` through an HTTP Request node. Credentials are placeholders only; put your token in n8n's credential store, never in the workflow JSON.

See [`workflows/README.md`](workflows/README.md) for import and setup notes.

## Unofficial sources

These Actors read public or official APIs and public web pages. They are unofficial tools and are not affiliated with, endorsed by, or sponsored by OpenAlex, NCBI/PubMed, arXiv, Valve/Steam, Greenhouse, Lever, Ashby, Remote OK, We Work Remotely, Jobicy, or the other sites they read.

## License

[MIT](LICENSE) © Bravona
