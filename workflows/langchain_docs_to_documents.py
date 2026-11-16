#!/usr/bin/env python3
"""Load output from bravona/docs-to-markdown-rag into LangChain Documents.

Runs the published Actor through apify-client, then turns each Markdown chunk
into a langchain_core.documents.Document. Swap the URL for any public PDF,
HTML page, or Office file the Actor accepts.

Requires APIFY_TOKEN in the environment, plus:

    pip install -r requirements.txt

Pricing: see the Store page https://apify.com/bravona/docs-to-markdown-rag
"""

from __future__ import annotations

import sys
from pathlib import Path

from apify_client import ApifyClient
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared import require_token, start_and_wait

ACTOR = "bravona/docs-to-markdown-rag"
STORE_PAGE = "https://apify.com/bravona/docs-to-markdown-rag"
SAMPLE_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"


def load_documents(token: str) -> list[Document]:
    client = ApifyClient(token)
    run_input = {
        "urls": [{"url": SAMPLE_URL}],
        "ocrMode": "off",
        "includeMarkdown": True,
        "includePages": False,
        "includeChunks": True,
        "maxDocuments": 1,
        "maxPagesPerDocument": 5,
    }

    run = start_and_wait(client, ACTOR, run_input, STORE_PAGE)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    documents: list[Document] = []

    for item in items:
        if item.get("status") != "ok":
            print(f"Skipping {item.get('source')}: {item.get('errorCode')} {item.get('errorMessage')}", flush=True)
            continue

        source = item.get("finalUrl") or item.get("fileName") or "unknown"
        metadata_base = {
            "source": source,
            "title": item.get("title"),
            "format": item.get("format"),
            "actor": ACTOR,
        }

        chunks = item.get("chunks") or []
        if chunks:
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=chunk.get("text") or "",
                        metadata={
                            **metadata_base,
                            "chunkIndex": chunk.get("chunkIndex"),
                            "pageStart": chunk.get("pageStart"),
                            "pageEnd": chunk.get("pageEnd"),
                            "headingPath": chunk.get("headingPath") or [],
                        },
                    )
                )
        elif item.get("markdown"):
            documents.append(
                Document(page_content=item["markdown"], metadata=metadata_base)
            )

    return documents


def main() -> None:
    documents = load_documents(require_token())
    print(f"Loaded {len(documents)} LangChain document(s).", flush=True)
    for doc in documents:
        print("---", flush=True)
        print(doc.metadata, flush=True)
        preview = doc.page_content[:500]
        print(preview if preview else "(empty)", flush=True)


if __name__ == "__main__":
    main()
