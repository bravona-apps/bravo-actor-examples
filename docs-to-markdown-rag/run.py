#!/usr/bin/env python3
"""Run bravona/docs-to-markdown-rag and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/docs-to-markdown-rag
"""

from __future__ import annotations

import os
import sys

from apify_client import ApifyClient

ACTOR = "bravona/docs-to-markdown-rag"
STORE_PAGE = "https://apify.com/bravona/docs-to-markdown-rag"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")

    client = ApifyClient(token)
    run_input = {
        "urls": [
            {"url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
        ],
        "ocrMode": "off",
        "includeMarkdown": True,
        "includePages": True,
        "includeChunks": True,
        "maxDocuments": 1,
        "maxPagesPerDocument": 5,
    }

    print(f"Starting {ACTOR} ...")
    print(f"Pricing: see {STORE_PAGE}")
    run = client.actor(ACTOR).call(run_input=run_input)
    if not run:
        sys.exit("The Actor call returned no run object.")

    dataset_id = run.get("defaultDatasetId")
    status = run.get("status")
    print(f"Run {run.get('id')} finished with status {status}.")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).")
    for item in items[:5]:
        print(
            f"- {item.get('status')} {item.get('format')} "
            f"{item.get('fileName') or item.get('finalUrl')} "
            f"chars={item.get('chars')} chunks={item.get('chunkCount')}"
        )
        markdown = item.get("markdown") or ""
        if markdown:
            print(f"  markdown: {markdown[:200]!r}")
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more")


if __name__ == "__main__":
    main()
