# Workflow examples

Two starters that call Bravona's published Actors. Neither file contains a token or a price. Current pricing is on each Actor's Store page.

## LangChain: docs to Documents

[`langchain_docs_to_documents.py`](langchain_docs_to_documents.py) runs [`bravona/docs-to-markdown-rag`](https://apify.com/bravona/docs-to-markdown-rag) through `apify-client` and loads each Markdown chunk into a LangChain `Document`. You can then pass `documents` into a splitter, a vector store, or a retriever.

```bash
export APIFY_TOKEN=your_apify_token_here
pip install -r ../requirements.txt
python langchain_docs_to_documents.py
```

The script uses a short public W3C dummy PDF so a first run stays small. Change `SAMPLE_URL` to any public URL the Actor accepts.

## n8n: Academic Paper Search

[`n8n-academic-papers-search.json`](n8n-academic-papers-search.json) is an importable n8n workflow:

1. In n8n, open **Workflows → Import from File** and choose the JSON file. It imports inactive.
2. Create a **Header Auth** credential:
   - Name (credential label): `Apify API token`
   - Header name: `Authorization`
   - Header value: `Bearer YOUR_APIFY_TOKEN`
3. Attach that credential to the **Run Academic Paper Search** HTTP Request node. Replace the `PLACEHOLDER_CREDENTIAL_ID` credential, or re-select the credential in the node UI.
4. Run the workflow once with **Test workflow**.

The HTTP Request node calls:

`POST https://api.apify.com/v2/acts/bravona~academic-papers-search/run-sync-get-dataset-items?timeout=120`

That official Apify endpoint waits for the run to finish and returns the dataset items in the response body. The example input searches OpenAlex only, with `maxResults` set to 3.

You can use the official Apify n8n node the same way if you have it installed: point it at `bravona/academic-papers-search` and keep the token in n8n credentials, not in the workflow JSON.

Pricing: see https://apify.com/bravona/academic-papers-search
