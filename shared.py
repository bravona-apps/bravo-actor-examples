"""Shared helpers for the Bravona Actor examples."""

from __future__ import annotations

import os
import sys
import time
from typing import Any

from apify_client import ApifyClient

TERMINAL_STATUSES = frozenset({"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "TIMED_OUT"})
WAIT_TIMEOUT_SECS = 180


def require_token() -> str:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable. See .env.example.")
    return token


def start_and_wait(
    client: ApifyClient,
    actor: str,
    run_input: dict[str, Any],
    store_page: str,
    timeout_secs: int = WAIT_TIMEOUT_SECS,
) -> dict[str, Any]:
    """Start a published Actor and poll its status until it finishes.

    Polls ``client.run(id).get()`` instead of the client's long-poll
    ``call()`` / ``wait_for_finish()`` helpers, which can hang on some networks
    after the run has already succeeded.
    """
    started = client.actor(actor).start(run_input=run_input)
    run_id = started["id"]
    print(f"Started {actor} run {run_id}.", flush=True)
    print(f"Pricing: see {store_page}", flush=True)

    deadline = time.time() + timeout_secs
    while True:
        run = client.run(run_id).get()
        if not run:
            sys.exit(f"Could not load run {run_id}.")
        status = run.get("status")
        if status in TERMINAL_STATUSES:
            return run
        if time.time() >= deadline:
            sys.exit(f"Timed out waiting for run {run_id} (last status: {status}).")
        time.sleep(1)
