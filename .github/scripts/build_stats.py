#!/usr/bin/env python3
"""
build_stats.py — Generate stats.json for the homepage live-stats banner.

Produces three numbers surfaced by the top banner on index.html:
  - learnersThisWeek : GA4 `activeUsers` over the last 7 days (0 if API unavailable)
  - coursesLive      : Count of entries in course-registry.json with status='live'
  - languages        : Count of supported UI languages (canonical list below)

Reads:
  ai-academy/modules/course-registry.json
Writes:
  stats.json  (at repo root — served as https://aesopacademy.org/stats.json)

Environment (for GA4 metric, all optional — script degrades gracefully if missing):
  GA4_PROPERTY_ID              : numeric GA4 property ID (e.g. "123456789")
  GA4_SERVICE_ACCOUNT_JSON     : full JSON credentials string for a service account
                                 with "Viewer" role on the GA4 property.

Usage:
    python .github/scripts/build_stats.py

Exits 0 even on partial failure so the cron workflow can commit whatever was
obtained. On total failure (e.g. registry missing), exits 1.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = REPO_ROOT / "ai-academy" / "modules" / "course-registry.json"
STATS_PATH = REPO_ROOT / "stats.json"

# Canonical list of UI languages actually supported by the router in index.html.
# Keep this in sync with the <button data-lang="..."> pills in the top banner.
LANGUAGES = ["en", "es", "hi", "ar"]


def count_live_courses() -> int:
    """Count courses in the registry whose status == 'live'."""
    if not REGISTRY_PATH.exists():
        print(f"[stats] WARNING: registry not found at {REGISTRY_PATH}", file=sys.stderr)
        return 0
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return 0
    return sum(
        1 for v in data.values()
        if isinstance(v, dict) and v.get("status") == "live"
    )


def fetch_active_users() -> int | None:
    """
    Query GA4 Data API for activeUsers over the last 7 days.
    Returns None if credentials aren't configured or the API fails — the caller
    should preserve the previous value or hide the stat in that case.
    """
    property_id = os.environ.get("GA4_PROPERTY_ID", "").strip()
    creds_json = os.environ.get("GA4_SERVICE_ACCOUNT_JSON", "").strip()

    if not property_id or not creds_json:
        print("[stats] GA4 credentials not configured — skipping learner count", file=sys.stderr)
        return None

    try:
        from google.oauth2 import service_account  # type: ignore
        from google.analytics.data_v1beta import BetaAnalyticsDataClient  # type: ignore
        from google.analytics.data_v1beta.types import (  # type: ignore
            DateRange, Metric, RunReportRequest,
        )
    except ImportError as e:
        print(f"[stats] GA4 libraries not installed ({e}) — skipping learner count", file=sys.stderr)
        return None

    try:
        creds_dict = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/analytics.readonly"],
        )
        client = BetaAnalyticsDataClient(credentials=credentials)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )
        response = client.run_report(request)
        if response.rows:
            value = response.rows[0].metric_values[0].value
            return int(value)
        return 0
    except Exception as e:
        print(f"[stats] GA4 query failed: {e}", file=sys.stderr)
        return None


def load_previous_stats() -> dict:
    """Read the existing stats.json, if any, so we can preserve prior values
    when a single metric fails."""
    if not STATS_PATH.exists():
        return {}
    try:
        with STATS_PATH.open(encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main() -> int:
    previous = load_previous_stats()

    courses_live = count_live_courses()
    if courses_live == 0:
        # Registry missing or empty is a hard fail — keep previous value if we had one.
        courses_live = previous.get("coursesLive", 0)

    learners = fetch_active_users()
    if learners is None:
        # Preserve last known good value; else null (banner hides the stat).
        learners = previous.get("learnersThisWeek")

    stats = {
        "learnersThisWeek": learners,
        "coursesLive": courses_live,
        "languages": len(LANGUAGES),
        "supportedLanguages": LANGUAGES,
        "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": {
            "learnersThisWeek": "GA4 activeUsers, last 7 days" if learners is not None else "unavailable",
            "coursesLive": "course-registry.json where status=='live'",
            "languages": "canonical list in build_stats.py",
        },
    }

    STATS_PATH.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(f"[stats] wrote {STATS_PATH}")
    print(f"  learnersThisWeek = {learners}")
    print(f"  coursesLive      = {courses_live}")
    print(f"  languages        = {len(LANGUAGES)}  ({', '.join(LANGUAGES)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
