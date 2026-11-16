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

import os
import sys

from apify_client import ApifyClient
from langchain_core.documents import Document

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

    print(f"Starting {ACTOR} ...")
    print(f"Pricing: see {STORE_PAGE}")
    run = client.actor(ACTOR).call(run_input=run_input)
    if not run:
        sys.exit("The Actor call returned no run object.")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    documents: list[Document] = []

    for item in items:
        if item.get("status") != "ok":
            print(f"Skipping {item.get('source')}: {item.get('errorCode')} {item.get('errorMessage')}")
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
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")

    documents = load_documents(token)
    print(f"Loaded {len(documents)} LangChain document(s).")
    for doc in documents:
        print("---")
        print(doc.metadata)
        preview = doc.page_content[:500]
        print(preview if preview else "(empty)")


if __name__ == "__main__":
    main()
