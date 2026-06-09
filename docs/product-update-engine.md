# Products Ladder Update Engine

The Products Ladder update engine checks the product catalog once per day for public signals that a listed product has changed.

## Files

- `.github/scripts/check_product_updates.py`: scans the catalog and writes reports.
- `.github/workflows/product-catalog-daily-check.yml`: runs the scan daily at 10:15 UTC and on manual dispatch.
- `docs/product-update-report.json`: machine-readable review queue from the latest run.
- `docs/product-update-report.md`: human-readable review queue from the latest run.
- `docs/product-update-state.json`: persistent signal memory used to identify new signals.

## What It Checks

The engine parses every row in `docs/theladder-products-catalog.md`, currently 500 products. For each product it queries public news/update signals and looks for release, version, feature, pricing, security, compliance, acquisition, model, and agent-related terms.

## Review Statuses

- `review_now`: a new signal appears strong enough to review immediately.
- `monitor`: a new signal looks relevant but needs human confirmation.
- `new_low_confidence_signal`: a weak new signal was detected.
- `unchanged`: no new signal crossed the threshold since the previous run.

## Safety Rule

The engine does not automatically rewrite curriculum rows. It creates a review queue first, because product release headlines can be wrong, duplicated, sponsored, stale, or unrelated to the actual product course.

## Manual Run

```bash
python .github/scripts/check_product_updates.py --limit 500
```

Fast smoke test:

```bash
python .github/scripts/check_product_updates.py --limit 5 --dry-run --delay 0
```
