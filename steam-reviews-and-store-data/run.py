#!/usr/bin/env python3
"""Run bravona/steam-reviews-and-store-data and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/steam-reviews-and-store-data
"""

from __future__ import annotations

import json
import os
import sys

from apify_client import ApifyClient

ACTOR = "bravona/steam-reviews-and-store-data"
STORE_PAGE = "https://apify.com/bravona/steam-reviews-and-store-data"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")

    client = ApifyClient(token)
    run_input = {
        "appIds": [570],
        "mode": "both",
        "reviewFilter": "recent",
        "language": "english",
        "maxReviewsPerApp": 3,
        "country": "us",
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
        kind = item.get("itemType")
        if kind == "game-details":
            print(
                f"- [game-details] {item.get('appName')} (app {item.get('appId')}) "
                f"{item.get('reviewScoreDesc')} {item.get('storeUrl')}"
            )
        else:
            text = json.dumps((item.get("text") or "")[:120])
            print(f"- [review] {item.get('appName')}: votedUp={item.get('votedUp')} {text}")
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more")


if __name__ == "__main__":
    main()
