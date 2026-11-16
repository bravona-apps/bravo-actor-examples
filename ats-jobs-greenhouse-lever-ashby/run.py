#!/usr/bin/env python3
"""Run bravona/ats-jobs-greenhouse-lever-ashby and print a few dataset items.

Requires the APIFY_TOKEN environment variable.
Pricing: see the Store page https://apify.com/bravona/ats-jobs-greenhouse-lever-ashby
"""

from __future__ import annotations

import os
import sys

from apify_client import ApifyClient

ACTOR = "bravona/ats-jobs-greenhouse-lever-ashby"
STORE_PAGE = "https://apify.com/bravona/ats-jobs-greenhouse-lever-ashby"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")

    client = ApifyClient(token)
    run_input = {
        "companies": ["ramp"],
        "ats": "auto",
        "includeDescription": "none",
        "maxJobsPerCompany": 3,
        "remoteOnly": False,
        "onlyNewSinceLastRun": False,
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
        print(f"- {item.get('company')} / {item.get('ats')}: {item.get('title')} ({item.get('location')})\n  {item.get('jobUrl') or item.get('applyUrl')}")
    if len(items) > 5:
        print(f"... plus {len(items) - 5} more")


if __name__ == "__main__":
    main()
