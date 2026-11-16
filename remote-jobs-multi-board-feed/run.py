#!/usr/bin/env python3
"""Run bravona/remote-jobs-multi-board-feed and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/remote-jobs-multi-board-feed
"""

from __future__ import annotations

import sys
from pathlib import Path

from apify_client import ApifyClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared import require_token, start_and_wait

ACTOR = "bravona/remote-jobs-multi-board-feed"
STORE_PAGE = "https://apify.com/bravona/remote-jobs-multi-board-feed"


def main() -> None:
    client = ApifyClient(require_token())
    run_input = {
        "keywords": ["python"],
        "searchInDescription": False,
        "includeWorldwide": True,
        "sources": ["jobicy", "remoteok", "weworkremotely"],
        "maxResults": 5,
        "sortBy": "newest",
        "includeDescription": False,
        "includeDescriptionHtml": False,
        "includeOnsiteArbeitnow": False,
        "onlyNewSinceLastRun": False,
    }

    run = start_and_wait(client, ACTOR, run_input, STORE_PAGE)
    print(f"Run {run.get('id')} finished with status {run.get('status')}.", flush=True)
    dataset_id = run.get("defaultDatasetId")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).", flush=True)
    for item in items[:5]:
        print(
            f"- {item.get('sourceName')}: {item.get('title')} at {item.get('company')} "
            f"({item.get('remoteRegion') or item.get('location')})\n  {item.get('sourceUrl')}",
            flush=True,
        )
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more", flush=True)


if __name__ == "__main__":
    main()
