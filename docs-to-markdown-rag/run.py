#!/usr/bin/env python3
"""Run bravona/docs-to-markdown-rag and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/docs-to-markdown-rag
"""

from __future__ import annotations

import sys
from pathlib import Path

from apify_client import ApifyClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared import require_token, start_and_wait

ACTOR = "bravona/docs-to-markdown-rag"
STORE_PAGE = "https://apify.com/bravona/docs-to-markdown-rag"


def main() -> None:
    client = ApifyClient(require_token())
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

    run = start_and_wait(client, ACTOR, run_input, STORE_PAGE)
    print(f"Run {run.get('id')} finished with status {run.get('status')}.", flush=True)
    dataset_id = run.get("defaultDatasetId")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).", flush=True)
    for item in items[:5]:
        print(
            f"- {item.get('status')} {item.get('format')} "
            f"{item.get('fileName') or item.get('finalUrl')} "
            f"chars={item.get('chars')} chunks={item.get('chunkCount')}",
            flush=True,
        )
        markdown = item.get("markdown") or ""
        if markdown:
            print(f"  markdown: {markdown[:200]!r}", flush=True)
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more", flush=True)


if __name__ == "__main__":
    main()
