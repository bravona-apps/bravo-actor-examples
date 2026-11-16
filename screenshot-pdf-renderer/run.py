#!/usr/bin/env python3
"""Run bravona/screenshot-pdf-renderer and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/screenshot-pdf-renderer
"""

from __future__ import annotations

import os
import sys

from apify_client import ApifyClient

ACTOR = "bravona/screenshot-pdf-renderer"
STORE_PAGE = "https://apify.com/bravona/screenshot-pdf-renderer"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")

    client = ApifyClient(token)
    run_input = {
        "urls": ["https://example.com"],
        "format": "png",
        "fullPage": False,
        "devicePreset": "desktop",
        "maxCaptures": 1,
        "blockAdsAndTrackers": True,
        "respectRobotsTxt": True,
    }

    print(f"Starting {ACTOR} ...")
    print(f"Pricing: see {STORE_PAGE}")
    run = client.actor(ACTOR).call(run_input=run_input, logger=None)
    if not run:
        sys.exit("The Actor call returned no run object.")

    dataset_id = run.get("defaultDatasetId")
    status = run.get("status")
    print(f"Run {run.get('id')} finished with status {status}.")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).")
    for item in items[:5]:
        print(
                    f"- {item.get('status')} {item.get('format')} {item.get('title')} "
                    f"{item.get('widthPx')}x{item.get('heightPx')} {item.get('fileUrl')}"
                )
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more")


if __name__ == "__main__":
    main()
