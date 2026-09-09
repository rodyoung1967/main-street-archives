#!/usr/bin/env python3
"""Temporary 1912 Historic Oregon Newspapers inventory/visual-audit probe.

Fetches the title-specific 1912 calendars directly from Historic Oregon Newspapers,
builds an auditable issue/page inventory for the three Oregon City titles used by the
annual closeout, screens archive OCR only for discovery, and makes contact sheets of
the Oregon City Courier scans for page-by-page visual inspection.

This is instrumentation, not historical evidence. OCR hits remain discovery-only until
the corresponding scan is visually verified.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from PIL import Image, ImageOps, ImageDraw

BASE = "https://oregonnews.uoregon.edu"
OUT = Path("probe-results")
OUT.mkdir(exist_ok=True)
(OUT / "courier-contact-sheets").mkdir(exist_ok=True)
(OUT / "courier-hit-pages").mkdir(exist_ok=True)

TITLES = {
    "courier": ("sn00063698", "Oregon City courier"),
    "enterprise": ("sn00063700", "Oregon City enterprise"),
    "morning-enterprise": ("sn00063701", "Morning enterprise"),
}

# Broad discovery vocabulary. This intentionally over-returns; OCR is navigation only.
TERMS = [
    "501 main", "503 main", "505 main", "507 main", "509 main", "511 main",
    "fifth and main", "5th and main", "sixth and main", "6th and main",
    "between fifth and sixth", "between 5th and 6th", "postoffice", "post office",
    "palace saloon", "joe wilson", "joseph wilson", "smith", "george young",
    "g. h. young", "harding", "willamette building", "willamette bldg",
    "chicago store", "brightbill", "gambrinus", "trudell", "schrader",
    "wemmo", "haas", "pool hall", "pool room", "billiard", "saloon",
    "new building", "building", "demol", "tear down", "tearing down", "torn down",
    "fire", "burned", "burnt", "remodel", "repair", "move", "moved",
    "excavat", "brick", "concrete", "main street", "main st.",
]

UA = "MainStreetArchiveResearch/1.0 (historical-research audit; contact via project repository)"
S = requests.Session()
S.headers.update({"User-Agent": UA})


def get(url: str, *, binary: bool = False, attempts: int = 4):
    last = None
    for n in range(attempts):
        try:
            r = S.get(url, timeout=45)
            if r.status_code == 200:
                return r.content if binary else r.text
            last = RuntimeError(f"HTTP {r.status_code} {url}")
        except Exception as exc:  # noqa: BLE001
            last = exc
        time.sleep(1.0 + n)
    raise RuntimeError(str(last))


def issue_links(lccn: str) -> list[str]:
    url = f"{BASE}/lccn/{lccn}/issues/1912/"
    html = get(url)
    pat = re.compile(r'href=["\']([^"\']*/lccn/' + re.escape(lccn) + r'/1912-\d{2}-\d{2}/ed-\d+/)["\']')
    links = [urljoin(BASE, m) for m in pat.findall(html)]
    # Some deployments render relative links without the leading lccn path in the captured href.
    if not links:
        pat2 = re.compile(r'href=["\']([^"\']*1912-\d{2}-\d{2}/ed-\d+/)["\']')
        links = [urljoin(url, m) for m in pat2.findall(html)]
    return sorted(set(links))


def page_sequences(issue_url: str) -> list[int]:
    html = get(issue_url)
    seqs = {int(x) for x in re.findall(r'/seq-(\d+)/', html)}
    if not seqs:
        # The issue page may list image/page labels without ordinary page anchors. Use
        # the page selector option values as a fallback.
        seqs = {int(x) for x in re.findall(r'seq-(\d+)', html)}
    return sorted(seqs)


def page_json_url(issue_url: str, seq: int) -> str:
    return issue_url.rstrip("/") + f"/seq-{seq}.json"


def thumbnail_url(issue_url: str, seq: int, width: int) -> str | None:
    # Prefer the IIIF canvas JSON because it gives a stable image-service URL.
    try:
        data = json.loads(get(page_json_url(issue_url, seq)))
        thumb = data.get("thumbnail")
        if isinstance(thumb, dict):
            thumb = thumb.get("@id") or thumb.get("id")
        if isinstance(thumb, str) and "/full/" in thumb:
            return re.sub(r'/full/[^/]+/0/default\.jpg$', f'/full/{width},/0/default.jpg', thumb)
        images = data.get("images") or []
        if images:
            resource = images[0].get("resource", {})
            service = resource.get("service") or {}
            sid = service.get("@id") if isinstance(service, dict) else None
            if sid:
                return sid.rstrip("/") + f"/full/{width},/0/default.jpg"
            rid = resource.get("@id")
            if isinstance(rid, str):
                return rid.rstrip("/") + f"/full/{width},/0/default.jpg"
    except Exception:
        pass

    # Fallback to the page HTML's rendered IIIF thumbnail.
    try:
        html = get(issue_url.rstrip("/") + f"/seq-{seq}/")
        m = re.search(r'(https?://[^"\']+/images/iiif/[^"\']+/full/)(?:\d+|!\d+,\d+|\d+,)(/0/default\.jpg)', html)
        if m:
            return m.group(1) + f"{width}," + m.group(2)
    except Exception:
        pass
    return None


def normalize_ocr(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def discover_terms(text: str) -> list[str]:
    low = normalize_ocr(text)
    return sorted({t for t in TERMS if t in low})


def save_contact_sheet(items: list[tuple[str, Image.Image]], path: Path) -> None:
    # Two pages across x two rows, retaining enough pixels to inspect page layout while
    # keeping the artifact manageable. The source URL/date/seq label is drawn above each.
    if not items:
        return
    cell_w, cell_h = 1220, 1820
    cols = 2
    rows = (len(items) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    for idx, (label, im) in enumerate(items):
        x = (idx % cols) * cell_w
        y = (idx // cols) * cell_h
        draw.text((x + 10, y + 8), label, fill="black")
        fitted = ImageOps.contain(im.convert("RGB"), (cell_w - 20, cell_h - 45))
        canvas.paste(fitted, (x + (cell_w - fitted.width) // 2, y + 38))
    canvas.save(path, "JPEG", quality=82, optimize=True)


def main() -> int:
    inventory_rows = []
    ocr_hits = []
    errors = []
    title_summary = {}

    courier_sheet_items: list[tuple[str, Image.Image]] = []
    courier_sheet_no = 1

    for key, (lccn, title_name) in TITLES.items():
        try:
            issues = issue_links(lccn)
        except Exception as exc:  # noqa: BLE001
            errors.append({"title": key, "stage": "calendar", "error": str(exc)})
            continue
        title_pages = 0
        title_summary[key] = {"lccn": lccn, "title": title_name, "issues": len(issues), "pages": 0}

        for issue_url in issues:
            date_m = re.search(r'/(1912-\d{2}-\d{2})/', issue_url)
            date = date_m.group(1) if date_m else "UNKNOWN"
            try:
                seqs = page_sequences(issue_url)
            except Exception as exc:  # noqa: BLE001
                errors.append({"title": key, "date": date, "stage": "issue", "error": str(exc), "url": issue_url})
                continue

            title_pages += len(seqs)
            for seq in seqs:
                page_url = issue_url.rstrip("/") + f"/seq-{seq}/"
                terms = []
                ocr_state = "OK"
                try:
                    ocr = get(page_url + "ocr.txt")
                    terms = discover_terms(ocr)
                except Exception as exc:  # noqa: BLE001
                    ocr_state = "RETRIEVAL GAP"
                    errors.append({"title": key, "date": date, "seq": seq, "stage": "ocr", "error": str(exc), "url": page_url})

                inventory_rows.append({
                    "title_key": key,
                    "title": title_name,
                    "lccn": lccn,
                    "date": date,
                    "seq": seq,
                    "issue_page_count": len(seqs),
                    "page_url": page_url,
                    "ocr_state": ocr_state,
                    "discovery_terms": "; ".join(terms),
                })
                if terms:
                    ocr_hits.append({
                        "title_key": key, "date": date, "seq": seq,
                        "page_url": page_url, "terms": terms,
                    })

                # Generate all-page Courier visual sheets, plus high-res individual images
                # for OCR-discovery hits. Failure here is logged as a visual retrieval gap.
                if key == "courier":
                    try:
                        u = thumbnail_url(issue_url, seq, 1150)
                        if not u:
                            raise RuntimeError("No IIIF thumbnail URL recovered")
                        blob = get(u, binary=True)
                        im = Image.open(io.BytesIO(blob)).convert("RGB")
                        label = f"{date} seq-{seq}  {page_url}"
                        courier_sheet_items.append((label, im))
                        if len(courier_sheet_items) == 4:
                            p = OUT / "courier-contact-sheets" / f"sheet-{courier_sheet_no:03d}.jpg"
                            save_contact_sheet(courier_sheet_items, p)
                            courier_sheet_items = []
                            courier_sheet_no += 1

                        if terms:
                            hi = thumbnail_url(issue_url, seq, 2200)
                            if hi:
                                hib = get(hi, binary=True)
                                (OUT / "courier-hit-pages" / f"{date}-seq-{seq}.jpg").write_bytes(hib)
                    except Exception as exc:  # noqa: BLE001
                        errors.append({"title": key, "date": date, "seq": seq, "stage": "image", "error": str(exc), "url": page_url})

        title_summary[key]["pages"] = title_pages

    if courier_sheet_items:
        p = OUT / "courier-contact-sheets" / f"sheet-{courier_sheet_no:03d}.jpg"
        save_contact_sheet(courier_sheet_items, p)

    with (OUT / "inventory.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["title_key", "title", "lccn", "date", "seq", "issue_page_count", "page_url", "ocr_state", "discovery_terms"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(inventory_rows)

    (OUT / "inventory.json").write_text(json.dumps(inventory_rows, indent=2), encoding="utf-8")
    (OUT / "ocr-hits.json").write_text(json.dumps(ocr_hits, indent=2), encoding="utf-8")
    (OUT / "errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    (OUT / "summary.json").write_text(json.dumps(title_summary, indent=2), encoding="utf-8")

    print(json.dumps(title_summary, indent=2))
    print(f"inventory rows: {len(inventory_rows)}")
    print(f"OCR discovery hits: {len(ocr_hits)}")
    print(f"logged retrieval/errors: {len(errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
