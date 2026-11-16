#!/usr/bin/env python3
"""Run bravona/screenshot-pdf-renderer and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/screenshot-pdf-renderer
"""

from __future__ import annotations

import sys
from pathlib import Path

from apify_client import ApifyClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared import require_token, start_and_wait

ACTOR = "bravona/screenshot-pdf-renderer"
STORE_PAGE = "https://apify.com/bravona/screenshot-pdf-renderer"


def main() -> None:
    client = ApifyClient(require_token())
    run_input = {
        "urls": ["https://example.com"],
        "format": "png",
        "fullPage": False,
        "devicePreset": "desktop",
        "maxCaptures": 1,
        "blockAdsAndTrackers": True,
        "respectRobotsTxt": True,
    }

    run = start_and_wait(client, ACTOR, run_input, STORE_PAGE)
    print(f"Run {run.get('id')} finished with status {run.get('status')}.", flush=True)
    dataset_id = run.get("defaultDatasetId")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).", flush=True)
    for item in items[:5]:
        print(
            f"- {item.get('status')} {item.get('format')} {item.get('title')} "
            f"{item.get('widthPx')}x{item.get('heightPx')} {item.get('fileUrl')}",
            flush=True,
        )
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more", flush=True)


if __name__ == "__main__":
    main()
