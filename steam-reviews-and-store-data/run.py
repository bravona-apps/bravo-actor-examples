#!/usr/bin/env python3
"""Run bravona/steam-reviews-and-store-data and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/steam-reviews-and-store-data
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from apify_client import ApifyClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared import require_token, start_and_wait

ACTOR = "bravona/steam-reviews-and-store-data"
STORE_PAGE = "https://apify.com/bravona/steam-reviews-and-store-data"


def main() -> None:
    client = ApifyClient(require_token())
    run_input = {
        "appIds": [570],
        "mode": "both",
        "reviewFilter": "recent",
        "language": "english",
        "maxReviewsPerApp": 3,
        "country": "us",
    }

    run = start_and_wait(client, ACTOR, run_input, STORE_PAGE)
    print(f"Run {run.get('id')} finished with status {run.get('status')}.", flush=True)
    dataset_id = run.get("defaultDatasetId")
    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Dataset {dataset_id} has {len(items)} item(s).", flush=True)
    for item in items[:5]:
        kind = item.get("itemType")
        if kind == "game-details":
            print(
                f"- [game-details] {item.get('appName')} (app {item.get('appId')}) "
                f"{item.get('reviewScoreDesc')} {item.get('storeUrl')}",
                flush=True,
            )
        else:
            text = json.dumps((item.get("text") or "")[:120])
            print(
                f"- [review] {item.get('appName')}: votedUp={item.get('votedUp')} {text}",
                flush=True,
            )
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more", flush=True)


if __name__ == "__main__":
    main()
