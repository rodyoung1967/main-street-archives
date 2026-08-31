#!/usr/bin/env python3
"""Bounded OCR discovery pass for the Banner-Courier, July 1919-Dec 1920.

Discovery only. This script does not promote OCR text to evidence and does not
certify annual research completeness. It inventories available issue/page OCR,
then records high-value snippets for 501/503/505 Main construction, occupancy,
and Fifth-Sixth Main transition leads.
"""
from __future__ import annotations

from datetime import date, timedelta
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "evidence/source-captures/1919-1920-banner-courier-ocr-discovery.md"
OUT_JSON = ROOT / "evidence/source-captures/1919-1920-banner-courier-ocr-inventory.json"

LCCN = "sn00063699"
START = date(1919, 7, 9)
END = date(1920, 12, 31)
BASE = "https://oregonnews.uoregon.edu/lccn/{lccn}/{day}/ed-1/seq-{seq}/ocr/"
UA = "main-street-archives historical research bot/1.0 (bounded archival discovery)"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return unescape(" ".join(self.parts))


def fetch(url: str) -> tuple[int | None, str]:
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urlopen(req, timeout=25) as r:
            raw = r.read().decode("utf-8", errors="replace")
            return getattr(r, "status", 200), raw
    except HTTPError as e:
        return e.code, ""
    except (URLError, TimeoutError):
        return None, ""


def visible_text(html: str) -> str:
    p = TextExtractor()
    p.feed(html)
    text = p.text()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def looks_like_page(text: str) -> bool:
    low = text.lower()
    if len(text) < 500:
        return False
    bad = ("page not found", "404 not found", "we're sorry")
    return not any(x in low for x in bad)


PATTERNS: dict[str, re.Pattern[str]] = {
    "505_half": re.compile(r"\b505\s*(?:1\s*/\s*2|½|1-2)\b", re.I),
    "505": re.compile(r"\b505\b", re.I),
    "503": re.compile(r"\b503\b", re.I),
    "501": re.compile(r"\b501\b", re.I),
    "leland": re.compile(r"\bLeland\b", re.I),
    "dollar": re.compile(r"\b(?:Clem(?:ent)?\s+)?Dollar\b", re.I),
    "wolf_miller": re.compile(r"\bWolf\b|\bMiller\b|Wolf\s*&\s*Miller", re.I),
    "harding": re.compile(r"\bHarding\b", re.I),
    "fifth_main": re.compile(r"(?:Fifth|5th)\s*(?:and|&|at|near|/)?\s*Main|Main\s*(?:and|&|at|near|/)?\s*(?:Fifth|5th)", re.I),
    "fifth_sixth": re.compile(r"between\s+(?:Fifth|5th)\s+and\s+(?:Sixth|6th)|(?:Fifth|5th).{0,80}(?:Sixth|6th)", re.I),
    "pool": re.compile(r"pool\s*hall|poolhall|billiard", re.I),
    "construction": re.compile(r"new\s+building|build(?:ing|ings)?|construct(?:ion|ed|ing)?|erect(?:ed|ing|ion)?|remodel(?:ed|ing)?|alter(?:ed|ation|ing)?|demolish(?:ed|ing)?|tear(?:ing)?\s+down|torn\s+down|rebuild|repair(?:ed|ing|s)?", re.I),
    "occupancy": re.compile(r"lease(?:d|s)?|rent(?:ed|s|ing)?|vacant|store\s*room|storeroom|move(?:d|s|ing)?|relocat(?:e|ed|ion)|permit|permission|application|sign", re.I),
}


def snippet(text: str, start: int, end: int, radius: int = 280) -> str:
    a = max(0, start - radius)
    b = min(len(text), end + radius)
    s = text[a:b]
    return re.sub(r"\s+", " ", s).strip()


def analyze(text: str) -> tuple[int, list[str], list[str]]:
    matches: dict[str, list[re.Match[str]]] = {}
    for name, pat in PATTERNS.items():
        found = list(pat.finditer(text))
        if found:
            matches[name] = found

    score = 0
    if "505_half" in matches:
        score += 12
    if "505" in matches:
        score += 7
    if "503" in matches:
        score += 5
    if "501" in matches:
        score += 4
    for name in ("leland", "dollar"):
        if name in matches:
            score += 10
    if "wolf_miller" in matches:
        score += 5
    if "harding" in matches:
        score += 3
    if "fifth_main" in matches or "fifth_sixth" in matches:
        score += 4
    if "pool" in matches:
        score += 5
    if "construction" in matches:
        score += 3
    if "occupancy" in matches:
        score += 2

    # Require something more specific than an isolated common Main-Street term.
    strong = any(k in matches for k in ("505_half", "505", "503", "501", "leland", "dollar"))
    contextual = (
        any(k in matches for k in ("fifth_main", "fifth_sixth", "harding", "wolf_miller"))
        and any(k in matches for k in ("pool", "construction", "occupancy"))
    )
    if not (strong or contextual):
        return 0, [], []

    labels = sorted(matches)
    snippets: list[str] = []
    seen: set[str] = set()
    for name in labels:
        for m in matches[name][:2]:
            s = snippet(text, m.start(), m.end())
            key = s[:120]
            if key not in seen:
                seen.add(key)
                snippets.append(s)
            if len(snippets) >= 6:
                break
        if len(snippets) >= 6:
            break
    return score, labels, snippets


def main() -> None:
    issues: list[dict] = []
    hits: list[dict] = []
    errors: list[dict] = []
    day = START

    while day <= END:
        day_s = day.isoformat()
        url1 = BASE.format(lccn=LCCN, day=day_s, seq=1)
        status, html = fetch(url1)
        if status == 200:
            text1 = visible_text(html)
            if looks_like_page(text1):
                pages = 0
                consecutive_missing = 0
                seq = 1
                while seq <= 24 and consecutive_missing < 2:
                    url = BASE.format(lccn=LCCN, day=day_s, seq=seq)
                    if seq == 1:
                        st, body, text = status, html, text1
                    else:
                        st, body = fetch(url)
                        text = visible_text(body) if st == 200 else ""
                    if st == 200 and looks_like_page(text):
                        pages += 1
                        consecutive_missing = 0
                        score, labels, snippets = analyze(text)
                        if score:
                            hits.append({
                                "date": day_s,
                                "seq": seq,
                                "url": url,
                                "score": score,
                                "labels": labels,
                                "snippets": snippets,
                            })
                    else:
                        consecutive_missing += 1
                    seq += 1
                    time.sleep(0.035)
                issues.append({"date": day_s, "pages": pages})
        elif status not in (404, 410):
            errors.append({"date": day_s, "seq": 1, "status": status})
        day += timedelta(days=1)
        time.sleep(0.02)

    hits.sort(key=lambda x: (-x["score"], x["date"], x["seq"]))
    inventory = {
        "title": "Banner-Courier",
        "lccn": LCCN,
        "date_range": [START.isoformat(), END.isoformat()],
        "method": "OCR discovery only; direct scan verification required before evidence promotion",
        "issue_count": len(issues),
        "page_count": sum(i["pages"] for i in issues),
        "issues": issues,
        "hits": hits,
        "errors": errors,
    }
    OUT_JSON.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Banner-Courier 1919–1920 OCR discovery pass",
        "",
        "Status: **OCR DISCOVERY ONLY — NOT VISUALLY VERIFIED AND NOT ANNUAL COMPLETION**",
        "",
        "## Scope",
        "",
        f"- Title: *Banner-Courier* (LCCN `{LCCN}`).",
        f"- Calendar probe: **{START.isoformat()} through {END.isoformat()}**.",
        f"- Issues discovered: **{len(issues)}**.",
        f"- OCR pages inventoried: **{sum(i['pages'] for i in issues)}**.",
        "- Method: probe each calendar date for sequence 1, then enumerate available page OCR for discovered issues.",
        "- Purpose: close the successor-title gap after the *Oregon City Courier* ended/merged in July 1919 and identify pages requiring visual inspection for 501/503/505 Main construction, occupancy, pool-hall, and relocation questions.",
        "- **No OCR wording below is evidence until the actual page scan is visually inspected.**",
        "",
        "## Issue inventory",
        "",
    ]
    for i in issues:
        lines.append(f"- {i['date']}: {i['pages']} OCR pages")

    lines.extend(["", "## Ranked discovery hits", ""])
    if not hits:
        lines.append("No high-value hits matched the bounded rules. This is search status only, not evidence of absence.")
    else:
        for h in hits[:120]:
            lines.extend([
                f"### {h['date']} — seq {h['seq']} — score {h['score']}",
                f"URL: {h['url']}",
                f"Matched groups: {', '.join(h['labels'])}",
                "",
            ])
            for s in h["snippets"]:
                lines.append(f"- OCR snippet: {s}")
            lines.append("")

    lines.extend([
        "## Limits / next step",
        "",
        "- OCR is used only for discovery under `RESEARCH-STANDARD.md`.",
        "- Visually inspect the strongest page scans before creating or changing any S/E/BUS/P evidence records.",
        "- Search silence does not prove vacancy, no construction, no move, or no business operation.",
        "- This pass does not mark 1919 or 1920 ONLINE COMPLETE.",
        "- Full machine-readable inventory and snippets are preserved in `evidence/source-captures/1919-1920-banner-courier-ocr-inventory.json`.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Banner-Courier discovery complete: {len(issues)} issues / {sum(i['pages'] for i in issues)} pages / {len(hits)} hits")


if __name__ == "__main__":
    main()
