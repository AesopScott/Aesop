#!/usr/bin/env python3
"""
Daily Products Ladder update watcher.

The watcher scans every product in docs/theladder-products-catalog.md for
public release/update signals, compares those signals with the previous run,
and writes a review queue. It intentionally does not rewrite curriculum rows
from unreviewed web signals.
"""

from __future__ import annotations

import argparse
import email.utils
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
CATALOG_PATH = REPO_ROOT / "docs" / "theladder-products-catalog.md"
STATE_PATH = REPO_ROOT / "docs" / "product-update-state.json"
REPORT_JSON_PATH = REPO_ROOT / "docs" / "product-update-report.json"
REPORT_MD_PATH = REPO_ROOT / "docs" / "product-update-report.md"

USER_AGENT = "AesopProductWatcher/1.0 (+https://aesopacademy.org/theladder-products/)"
DEFAULT_DELAY_SECONDS = 0.35
DEFAULT_LIMIT = 500

UPDATE_TERMS = [
    "launch",
    "launched",
    "release",
    "released",
    "update",
    "updated",
    "upgrade",
    "new",
    "version",
    "copilot",
    "agent",
    "agents",
    "ai",
    "model",
    "feature",
    "integration",
    "acquisition",
    "pricing",
    "security",
    "governance",
    "compliance",
]

HIGH_VALUE_TERMS = {
    "launch",
    "launched",
    "release",
    "released",
    "version",
    "model",
    "agent",
    "agents",
    "pricing",
    "security",
    "compliance",
    "acquisition",
}


@dataclass
class Product:
    id: int
    name: str
    product_type: str
    reason: str
    depth: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_text(value: str, limit: int = 500) -> str:
    value = html.unescape(str(value or ""))
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    cut = value[:limit].rsplit(" ", 1)[0].rstrip(".,;:")
    return f"{cut}."


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "product"


def signal_id(url: str, title: str) -> str:
    raw = f"{url.strip()}|{title.strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def parse_catalog(path: Path = CATALOG_PATH) -> list[Product]:
    products: list[Product] = []
    row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = row_re.match(line)
        if not match:
            continue
        products.append(Product(
            id=int(match.group(1)),
            name=match.group(2).strip(),
            product_type=match.group(3).strip(),
            reason=match.group(4).strip(),
            depth=match.group(5).strip(),
        ))
    return products


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def fetch_url(url: str, timeout: int = 16) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urlopen(request, timeout=timeout) as response:
        return response.read(1_500_000)


def product_query(product: Product) -> str:
    scoped_name = f'"{product.name}"'
    if len(product.name) <= 4 or product.name.lower() in {"gem", "xero", "cove.tool"}:
        scoped_name = f'"{product.name}" AI product'
    return f'{scoped_name} (AI OR artificial intelligence) (launch OR release OR update OR version OR feature)'


def bing_news_rss_url(product: Product) -> str:
    params = {
        "q": product_query(product),
        "format": "rss",
        "setlang": "en-US",
        "cc": "US",
        "count": "10",
    }
    return f"https://www.bing.com/news/search?{urllib.parse.urlencode(params)}"


def parse_date(value: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).date().isoformat()
    except Exception:
        return value[:40]


def score_signal(product: Product, title: str, summary: str, source: str) -> int:
    text = f"{title} {summary}".lower()
    score = 0
    name_parts = [part for part in re.split(r"[^a-z0-9]+", product.name.lower()) if len(part) >= 3]
    if product.name.lower() in text:
        score += 40
    else:
        score += min(25, 7 * sum(1 for part in name_parts if part in text))
    for term in UPDATE_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text):
            score += 8 if term in HIGH_VALUE_TERMS else 4
    if any(domain in source.lower() for domain in ["blog", "news", "press", "release"]):
        score += 8
    if product.depth == "B/I/A":
        score += 4
    return min(score, 100)


def collect_signals(product: Product) -> tuple[list[dict], str | None]:
    url = bing_news_rss_url(product)
    try:
        payload = fetch_url(url)
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return [], f"{type(error).__name__}: {error}"

    try:
        root = ET.fromstring(payload)
    except ET.ParseError as error:
        return [], f"RSS parse failed: {error}"

    signals: list[dict] = []
    for item in root.findall("./channel/item")[:10]:
        title = clean_text(item.findtext("title"), 220)
        link = clean_text(item.findtext("link"), 500)
        summary = clean_text(item.findtext("description"), 320)
        source = clean_text(item.findtext("source"), 160)
        published = parse_date(item.findtext("pubDate"))
        if not title or not link:
            continue
        score = score_signal(product, title, summary, source)
        if score < 34:
            continue
        signals.append({
            "id": signal_id(link, title),
            "title": title,
            "url": link,
            "source": source or urllib.parse.urlparse(link).netloc,
            "published": published,
            "summary": summary,
            "score": score,
        })

    signals.sort(key=lambda item: item.get("score", 0), reverse=True)
    return signals[:5], None


def classify_product(product: Product, signals: list[dict], previous_ids: set[str]) -> dict:
    new_signals = [signal for signal in signals if signal["id"] not in previous_ids]
    top_score = max([signal["score"] for signal in signals], default=0)
    new_top_score = max([signal["score"] for signal in new_signals], default=0)
    if new_top_score >= 78:
        status = "review_now"
    elif new_signals and new_top_score >= 55:
        status = "monitor"
    elif new_signals:
        status = "new_low_confidence_signal"
    else:
        status = "unchanged"
    return {
        "id": product.id,
        "name": product.name,
        "type": product.product_type,
        "depth": product.depth,
        "status": status,
        "topScore": top_score,
        "newSignalCount": len(new_signals),
        "signals": signals,
        "newSignals": new_signals,
    }


def update_state(previous_state: dict, product_results: list[dict], run_id: str) -> dict:
    existing = previous_state.get("products") or {}
    products: dict[str, dict] = {}
    for result in product_results:
        key = str(result["id"])
        old = existing.get(key) or {}
        signal_ids = [signal["id"] for signal in result["signals"]]
        products[key] = {
            "name": result["name"],
            "lastCheckedAt": run_id,
            "lastStatus": result["status"],
            "signalIds": signal_ids,
            "lastSignals": result["signals"],
        }
        if result["status"] != "unchanged":
            products[key]["lastChangedAt"] = run_id
        elif old.get("lastChangedAt"):
            products[key]["lastChangedAt"] = old["lastChangedAt"]
    return {
        "version": 1,
        "updatedAt": run_id,
        "products": products,
    }


def write_reports(run_id: str, products: list[Product], results: list[dict], errors: list[dict]) -> None:
    review_now = [item for item in results if item["status"] == "review_now"]
    monitor = [item for item in results if item["status"] == "monitor"]
    low = [item for item in results if item["status"] == "new_low_confidence_signal"]
    changed = review_now + monitor + low

    report = {
        "version": 1,
        "generatedAt": run_id,
        "catalogPath": str(CATALOG_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "productCount": len(products),
        "checkedCount": len(results),
        "errorCount": len(errors),
        "summary": {
            "reviewNow": len(review_now),
            "monitor": len(monitor),
            "newLowConfidenceSignal": len(low),
            "unchanged": len([item for item in results if item["status"] == "unchanged"]),
        },
        "reviewQueue": changed,
        "errors": errors,
    }
    REPORT_JSON_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Products Ladder Daily Update Report",
        "",
        f"Generated: {run_id}",
        "",
        "## Summary",
        "",
        f"- Products checked: {len(results)} / {len(products)}",
        f"- Review now: {len(review_now)}",
        f"- Monitor: {len(monitor)}",
        f"- Low-confidence new signals: {len(low)}",
        f"- Fetch or parse errors: {len(errors)}",
        "",
        "## Review Queue",
        "",
    ]
    if not changed:
        lines.append("No new product update signals crossed the review threshold.")
    else:
        for item in changed[:80]:
            lines.extend([
                f"### #{item['id']} {item['name']} ({item['status']})",
                "",
                f"- Type: {item['type']}",
                f"- Top score: {item['topScore']}",
                f"- New signals: {item['newSignalCount']}",
            ])
            for signal in item["newSignals"][:3]:
                lines.append(f"- [{signal['title']}]({signal['url']})")
                if signal.get("source") or signal.get("published"):
                    lines.append(f"  - Source/date: {signal.get('source', 'unknown')} / {signal.get('published', 'unknown')}")
            lines.append("")
    if errors:
        lines.extend(["## Errors", ""])
        for error in errors[:100]:
            lines.append(f"- #{error['id']} {error['name']}: {error['error']}")
    REPORT_MD_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run(limit: int, delay_seconds: float, dry_run: bool) -> int:
    run_id = now_iso()
    products = parse_catalog()
    if limit > 0:
        products_to_check = products[:limit]
    else:
        products_to_check = products
    previous_state = load_json(STATE_PATH, {"products": {}})
    previous_products = previous_state.get("products") or {}
    results: list[dict] = []
    errors: list[dict] = []

    for index, product in enumerate(products_to_check, start=1):
        previous_ids = set((previous_products.get(str(product.id)) or {}).get("signalIds") or [])
        signals, error = collect_signals(product)
        if error:
            errors.append({"id": product.id, "name": product.name, "error": error})
        results.append(classify_product(product, signals, previous_ids))
        if delay_seconds > 0 and index < len(products_to_check):
            time.sleep(delay_seconds)

    write_reports(run_id, products, results, errors)
    if not dry_run:
        new_state = update_state(previous_state, results, run_id)
        STATE_PATH.write_text(json.dumps(new_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "generatedAt": run_id,
        "productCount": len(products),
        "checkedCount": len(results),
        "reviewQueueCount": len([item for item in results if item["status"] != "unchanged"]),
        "errorCount": len(errors),
        "dryRun": dry_run,
    }, indent=2))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check Products Ladder products for public update signals.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Number of products to check. Use 0 for all.")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS, help="Delay between product RSS requests.")
    parser.add_argument("--dry-run", action="store_true", help="Write reports but do not update persistent state.")
    args = parser.parse_args(argv)
    return run(limit=args.limit, delay_seconds=args.delay, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
