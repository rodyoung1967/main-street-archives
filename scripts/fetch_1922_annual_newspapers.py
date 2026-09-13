#!/usr/bin/env python3
"""Fetch the complete online 1922 Oregon City local-newspaper corpus.

The script inventories each expected weekly issue from the ODNP issue page,
then preserves every exposed page PDF plus OCR text and a hash manifest.  OCR
is retained only as a discovery aid; the manifest deliberately remains
RETRIEVAL ONLY until the scans are visually reviewed and separately certified.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://oregonnews.uoregon.edu/lccn"
UA = "main-street-archives annual-audit/1.0"
TITLES = {
    "oregon-city-enterprise": {
        "name": "Oregon City Enterprise",
        "lccn": "sn00063700",
        "first": dt.date(1922, 1, 6),
    },
    "banner-courier": {
        "name": "The Banner-Courier",
        "lccn": "sn00063699",
        "first": dt.date(1922, 1, 5),
    },
}


def weekly_dates(first: dt.date) -> list[dt.date]:
    dates: list[dt.date] = []
    day = first
    while day.year == 1922:
        dates.append(day)
        day += dt.timedelta(days=7)
    return dates


def published_dates(meta: dict[str, object]) -> list[dt.date]:
    """Read the archive's title calendar instead of assuming every weekday.

    This matters for exceptions such as the Oregon City Enterprise issue dated
    Wednesday, 15 June 1922 instead of its ordinary Friday publication date.
    """
    calendar_url = f"{BASE}/{meta['lccn']}/issues/1922/"
    html = fetch(calendar_url).decode("utf-8", errors="replace")
    pattern = rf"/lccn/{meta['lccn']}/(1922-\d{{2}}-\d{{2}})/ed-\d+/"
    dates = sorted({dt.date.fromisoformat(value) for value in re.findall(pattern, html)})
    if not dates:
        raise RuntimeError(f"No 1922 issue dates exposed for {calendar_url}")
    return dates


def fetch(url: str, attempts: int = 5) -> bytes:
    for attempt in range(1, attempts + 1):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=90) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            if attempt == attempts:
                raise
            time.sleep(attempt * 1.5)
    raise RuntimeError(f"unreachable fetch failure: {url}")


def issue_inventory(meta: dict[str, object], day: dt.date) -> tuple[str, list[int]]:
    date = day.isoformat()
    issue_url = f"{BASE}/{meta['lccn']}/{date}/ed-1/"
    html = fetch(issue_url).decode("utf-8", errors="replace")
    sequences = sorted({int(value) for value in re.findall(r"seq-(\d+)", html)})
    if not sequences:
        raise RuntimeError(f"No page sequences exposed for {issue_url}")
    expected = list(range(1, max(sequences) + 1))
    if sequences != expected:
        raise RuntimeError(f"Non-contiguous sequence inventory for {issue_url}: {sequences}")
    return issue_url, sequences


def fetch_page(
    out: Path, lccn: str, date: str, sequence: int
) -> dict[str, object]:
    stem = f"{date}-seq-{sequence:02d}"
    page = f"{BASE}/{lccn}/{date}/ed-1/seq-{sequence}"
    pdf_url = f"{page}.pdf"
    ocr_url = f"{page}/ocr.txt"
    pdf = fetch(pdf_url)
    if not pdf.startswith(b"%PDF"):
        raise RuntimeError(f"Non-PDF response for {pdf_url}: {pdf[:40]!r}")
    ocr = fetch(ocr_url)
    pdf_path = out / f"{stem}.pdf"
    ocr_path = out / "ocr" / f"{stem}.txt"
    pdf_path.write_bytes(pdf)
    ocr_path.write_bytes(ocr)
    return {
        "sequence": sequence,
        "file": pdf_path.name,
        "url": pdf_url,
        "bytes": len(pdf),
        "sha256": hashlib.sha256(pdf).hexdigest(),
        "ocr_file": str(Path("ocr") / ocr_path.name),
        "ocr_url": ocr_url,
        "ocr_bytes": len(ocr),
        "ocr_sha256": hashlib.sha256(ocr).hexdigest(),
    }


def fetch_title_month(slug: str, meta: dict[str, object], month: int, workers: int) -> None:
    all_published = published_dates(meta)
    days = [day for day in all_published if day.month == month]
    expected = set(weekly_dates(meta["first"]))
    published = set(all_published)
    out = ROOT / "newspapers" / slug / f"1922-{month:02d}"
    (out / "ocr").mkdir(parents=True, exist_ok=True)
    issues: list[dict[str, object]] = []
    for day in days:
        issue_url, sequences = issue_inventory(meta, day)
        date = day.isoformat()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            pages = list(
                pool.map(
                    lambda seq: fetch_page(out, str(meta["lccn"]), date, seq),
                    sequences,
                )
            )
        issues.append(
            {
                "date": date,
                "issue_url": issue_url,
                "page_count": len(pages),
                "pages": pages,
            }
        )
        print(f"{meta['name']} {date}: {len(pages)} pages", flush=True)
    manifest = {
        "title": meta["name"],
        "lccn": meta["lccn"],
        "year": 1922,
        "month": month,
        "status": "RETRIEVAL ONLY — original page scans require visual inspection before certification",
        "inventory_source": f"{BASE}/{meta['lccn']}/issues/1922/",
        "expected_weekly_dates_absent_from_archive_calendar": sorted(
            day.isoformat() for day in expected - published if day.month == month
        ),
        "archive_calendar_dates_outside_expected_weekday": sorted(
            day.isoformat() for day in published - expected if day.month == month
        ),
        "issues": issues,
        "total_pages": sum(int(issue["page_count"]) for issue in issues),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", type=int, action="append", choices=range(1, 13))
    parser.add_argument("--title", action="append", choices=sorted(TITLES))
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    months = sorted(set(args.month or range(1, 13)))
    titles = args.title or list(TITLES)
    for month in months:
        for slug in titles:
            fetch_title_month(slug, TITLES[slug], month, args.workers)


if __name__ == "__main__":
    main()
