#!/usr/bin/env python3
"""Discover 1923–1924 regional-newspaper leads for 503/505 Main.

OCR is used only for discovery.  Candidate claims must be checked against the
actual page scan before they are promoted into the archive's evidence records.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import random
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "evidence/source-captures/1923-1924-regional-business-ocr-discovery.json"
OUT_MD = ROOT / "evidence/source-captures/1923-1924-regional-business-ocr-discovery.md"
BASE = "https://oregonnews.uoregon.edu"
YEARS = (1923, 1924)
UA = "main-street-archives archival discovery/1.0"
WORKERS = 12
BATCH_SIZE = 150

TITLES = {
    "sn96088133": "Eastern Clackamas News",
    "sn97071044": "Gresham Outlook",
    "sn84006724": "Hillsboro Argus",
    "sn00063558": "Mt. Scott Herald",
    "sn98062568": "The Advocate",
    "sn90066132": "Capital Journal",
    "sn85042470": "Oregon Statesman",
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", unescape(" ".join(self.parts))).strip()


@dataclass(frozen=True)
class Page:
    lccn: str
    title: str
    day: str
    edition: int
    seq: int

    @property
    def ocr_url(self) -> str:
        return f"{BASE}/lccn/{self.lccn}/{self.day}/ed-{self.edition}/seq-{self.seq}/ocr.txt"

    @property
    def pdf_url(self) -> str:
        return f"{BASE}/lccn/{self.lccn}/{self.day}/ed-{self.edition}/seq-{self.seq}.pdf"


def chunks(values: list, size: int = BATCH_SIZE):
    for start in range(0, len(values), size):
        yield values[start:start + size]


def curl_fetch_many(items: list[tuple[str, str]]) -> tuple[dict[str, str], list[dict]]:
    """Fetch URL batches through curl's connection-pooling multi interface."""
    bodies: dict[str, str] = {}
    errors: list[dict] = []
    for batch in chunks(items):
        with tempfile.TemporaryDirectory(prefix="msa-ocr-") as temp_name:
            temp = Path(temp_name)
            config = temp / "curl.conf"
            lines = []
            paths: dict[str, Path] = {}
            for number, (key, url) in enumerate(batch):
                output = temp / f"{number:05d}.txt"
                paths[key] = output
                # curl associates -o/--output with the URL that follows it.
                lines.extend([f'output = "{output}"', f'url = "{url}"'])
            config.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = subprocess.run(
                [
                    "curl", "--location", "--silent", "--show-error",
                    "--connect-timeout", "12", "--max-time", "45",
                    "--retry", "1", "--retry-delay", "1",
                    "--parallel", "--parallel-immediate", "--parallel-max", str(WORKERS),
                    "--user-agent", UA, "--config", str(config),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            for key, url in batch:
                output = paths[key]
                if output.exists():
                    bodies[key] = output.read_text(encoding="utf-8", errors="replace")
                else:
                    errors.append({"key": key, "url": url, "status": "curl-output-missing"})
            if result.returncode and result.stderr.strip():
                errors.append({"stage": "curl-batch", "status": result.returncode, "detail": result.stderr.strip()[:2000]})
    return bodies, errors


def html_text(body: str) -> str:
    parser = TextExtractor()
    parser.feed(body)
    return parser.text()


ISSUE_RE = re.compile(r'/lccn/([^/]+)/(192[34]-\d{2}-\d{2})/ed-(\d+)/')
SEQ_RE = re.compile(r"seq-(\d+)")


def inventory_issues() -> tuple[list[tuple[str, str, int, str]], list[dict]]:
    issues: set[tuple[str, str, int, str]] = set()
    requests = []
    for lccn, title in TITLES.items():
        for year in YEARS:
            url = f"{BASE}/lccn/{lccn}/issues/{year}/"
            requests.append((f"{lccn}:{year}", url))
    bodies, errors = curl_fetch_many(requests)
    for lccn, title in TITLES.items():
        for year in YEARS:
            body = bodies.get(f"{lccn}:{year}", "")
            for match in ISSUE_RE.finditer(body):
                if match.group(1) == lccn and int(match.group(2)[:4]) == year:
                    issues.add((lccn, match.group(2), int(match.group(3)), title))
    return sorted(issues, key=lambda x: (x[0], x[1], x[2])), errors


def inventory_pages(issues: list[tuple[str, str, int, str]]) -> tuple[list[Page], list[dict]]:
    requests: list[tuple[str, str]] = []
    lookup: dict[str, tuple[str, str, int, str]] = {}
    for number, issue in enumerate(issues):
        lccn, day, edition, title = issue
        key = str(number)
        lookup[key] = issue
        requests.append((key, f"{BASE}/lccn/{lccn}/{day}/ed-{edition}/"))
    random.Random(19231924).shuffle(requests)
    bodies, errors = curl_fetch_many(requests)
    # A large parallel archive read can occasionally return a protection or
    # transient page without the issue sequence. Retry only unresolved issues.
    for _attempt in range(2):
        retry = [(key, url) for key, url in requests if not SEQ_RE.search(bodies.get(key, ""))]
        if not retry:
            break
        random.Random(503505 + _attempt).shuffle(retry)
        recovered, retry_errors = curl_fetch_many(retry)
        bodies.update({key: value for key, value in recovered.items() if SEQ_RE.search(value)})
        errors.extend(retry_errors)
    pages: list[Page] = []
    for key, issue in lookup.items():
        lccn, day, edition, title = issue
        seqs = sorted({int(value) for value in SEQ_RE.findall(bodies.get(key, ""))})
        if not seqs:
            errors.append({"stage": "issue-pages", "lccn": lccn, "day": day, "edition": edition, "status": "no-sequences"})
        pages.extend(Page(lccn, title, day, edition, seq) for seq in seqs)
    return pages, errors


PATTERNS = {
    "oregon_city": re.compile(r"\bOregon\s+City\b", re.I),
    "farr": re.compile(r"\bFarr(?:'s|s)?\b", re.I),
    "edwin_farr": re.compile(r"\b(?:Edwin|Ed|E\.?\s*F\.?)\s+Farr\b", re.I),
    "alice_farr": re.compile(r"\bAlice\s+Farr\b", re.I),
    "kwality": re.compile(r"\bK(?:w|u)ality\b", re.I),
    "quality_restaurant": re.compile(r"\bQuality\s+(?:Restaurant|Cafe)\b", re.I),
    "jager": re.compile(r"\bJ\.?\s*Jager\b|\bJager\b", re.I),
    "leland_little": re.compile(r"\bLeland\s*(?:&|and)\s*Little\b", re.I),
    "timms": re.compile(r"\bTimms?(?:'s|s)?\b", re.I),
    "mcanulty_barry": re.compile(r"\bMcAnulty\b|\bBarry\b", re.I),
    "freeze": re.compile(r"\b(?:Dr\.?\s+)?Freeze\b", re.I),
    "wheeler": re.compile(r"\bWheeler\b", re.I),
    "clem_dollar": re.compile(r"\bClem(?:ent)?\s+Dollar\b", re.I),
    "address_503": re.compile(r"\b503(?:\s+Main|\s+Main\s+Street)?\b", re.I),
    "address_505": re.compile(r"\b505(?:\s*(?:1\s*/\s*2|½)|\s+Main|\s+Main\s+Street)?\b", re.I),
    "pool_billiards": re.compile(r"\bpool\s*(?:hall|room)|\bbilliards?\b", re.I),
    "cigars": re.compile(r"\bcigars?|\btobacco\b", re.I),
    "restaurant": re.compile(r"\brestaurants?|\bcafes?\b|\blunch\s*room\b", re.I),
    "fifth_main": re.compile(r"(?:Fifth|5th)\s*(?:and|&|at|near|/)\s*Main|Main\s*(?:and|&|at|near|/)\s*(?:Fifth|5th)", re.I),
    "fifth_address": re.compile(r"\b\d{1,3}\s+(?:Fifth|5th)(?:\s+Street)?\b", re.I),
    "transition": re.compile(r"\b(?:sold|sells|sale|bought|buys|purchased|transfer(?:red)?|lease[ds]?|rent(?:ed|s)?|move[ds]?|moving|open(?:ed|ing)?|new\s+quarters|takes?\s+over|successor)\b", re.I),
}


def positions(text: str, key: str) -> list[re.Match[str]]:
    return list(PATTERNS[key].finditer(text))


def near(left: list[re.Match[str]], right: list[re.Match[str]], distance: int) -> bool:
    return any(abs(a.start() - b.start()) <= distance for a in left for b in right)


def snippets(text: str, matches: list[re.Match[str]], radius: int = 320, limit: int = 2) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for match in sorted(matches, key=lambda m: m.start()):
        value = re.sub(r"\s+", " ", text[max(0, match.start() - radius):min(len(text), match.end() + radius)]).strip()
        marker = value[:160]
        if marker not in seen:
            seen.add(marker)
            output.append(value)
        if len(output) >= limit:
            break
    return output


def analyze(page: Page, text: str) -> dict | None:
    found = {key: positions(text, key) for key in PATTERNS}
    found = {key: value for key, value in found.items() if value}
    if not found:
        return None

    city = found.get("oregon_city", [])
    trades = sum((found.get(key, []) for key in ("pool_billiards", "cigars", "restaurant")), [])
    exact_names = sum((found.get(key, []) for key in ("edwin_farr", "alice_farr", "kwality", "quality_restaurant", "jager", "leland_little", "clem_dollar")), [])
    ambiguous_names = sum((found.get(key, []) for key in ("farr", "timms", "mcanulty_barry", "freeze", "wheeler")), [])
    addresses = found.get("address_503", []) + found.get("address_505", [])
    fifth = found.get("fifth_main", []) + found.get("fifth_address", [])
    transition = found.get("transition", [])

    reasons: list[str] = []
    score = 0
    if exact_names and (near(exact_names, city, 1800) or near(exact_names, trades, 1000) or near(exact_names, addresses, 1000)):
        reasons.append("exact-name-context")
        score += 12
    if ambiguous_names and city and (near(ambiguous_names, city, 1200) or near(ambiguous_names, trades, 800) or near(ambiguous_names, addresses, 800)):
        reasons.append("name-oregon-city-context")
        score += 8
    if addresses and trades and near(addresses, trades, 700):
        reasons.append("address-trade-context")
        score += 10
    if fifth and city and (near(fifth, city, 1600) or near(fifth, trades, 800)):
        reasons.append("fifth-street-context")
        score += 6
    if transition and (exact_names or ambiguous_names or addresses) and near(transition, exact_names + ambiguous_names + addresses, 900):
        reasons.append("business-transition-context")
        score += 5

    if not reasons:
        return None
    all_matches = exact_names + ambiguous_names + addresses + fifth + trades + transition + city
    return {
        "lccn": page.lccn,
        "title": page.title,
        "date": page.day,
        "edition": page.edition,
        "seq": page.seq,
        "ocr_url": page.ocr_url,
        "pdf_url": page.pdf_url,
        "score": score,
        "reasons": reasons,
        "groups": sorted(found),
        "snippets": snippets(text, all_matches),
    }


def main() -> None:
    issues, errors = inventory_issues()
    print(f"Calendars inventoried: {len(issues)} issues", flush=True)
    pages, page_errors = inventory_pages(issues)
    errors.extend(page_errors)
    pages.sort(key=lambda p: (p.lccn, p.day, p.edition, p.seq))
    print(f"Issue pages inventoried: {len(pages)} pages", flush=True)

    hits: list[dict] = []
    completed = 0
    for page_batch in chunks(pages):
        requests = [(str(number), page.ocr_url) for number, page in enumerate(page_batch)]
        bodies, batch_errors = curl_fetch_many(requests)
        errors.extend(batch_errors)
        for number, page in enumerate(page_batch):
            body = bodies.get(str(number), "")
            if len(body) < 100 or "page not found" in body.lower():
                errors.append({"stage": "ocr", "lccn": page.lccn, "day": page.day, "edition": page.edition, "seq": page.seq, "status": "missing-or-invalid", "url": page.ocr_url})
                hit = None
            else:
                hit = analyze(page, re.sub(r"\s+", " ", body).strip())
            if hit:
                hits.append(hit)
            completed += 1
            if completed % 1000 == 0:
                print(f"OCR progress: {completed}/{len(pages)} pages; {len(hits)} candidates", flush=True)
    hits.sort(key=lambda value: (-value["score"], value["date"], value["lccn"], value["seq"]))

    title_summary: dict[str, dict] = {}
    for lccn, title in TITLES.items():
        issue_rows = [issue for issue in issues if issue[0] == lccn]
        page_rows = [page for page in pages if page.lccn == lccn]
        title_summary[lccn] = {
            "title": title,
            "issues": len(issue_rows),
            "pages": len(page_rows),
            "years": {str(year): len([issue for issue in issue_rows if issue[1].startswith(str(year))]) for year in YEARS},
        }

    shortlist_groups = {
        "edwin_farr", "alice_farr", "farr", "kwality", "quality_restaurant",
        "jager", "leland_little", "clem_dollar", "fifth_main", "fifth_address",
    }
    shortlist = [
        hit for hit in hits
        if hit["score"] >= 10 or shortlist_groups.intersection(hit["groups"])
    ]
    machine_shortlist = [
        {key: value for key, value in hit.items() if key != "snippets"}
        for hit in shortlist
    ]

    data = {
        "status": "OCR DISCOVERY ONLY — direct scan verification required",
        "date_range": ["1923-01-01", "1924-12-31"],
        "method": "Issue calendars and issue page lists inventoried; every exposed page OCR checked using bounded co-occurrence rules.",
        "titles": title_summary,
        "issue_count": len(issues),
        "page_count": len(pages),
        "raw_candidate_count": len(hits),
        "candidate_count": len(shortlist),
        "candidate_selection": "Score at least 10, or Farr, exact-name, or Fifth Street match group.",
        "candidates": machine_shortlist,
        "errors": errors,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# 1923–1924 regional newspaper business OCR discovery",
        "",
        "Status: **OCR DISCOVERY ONLY — NOT VISUALLY VERIFIED AND NOT ANNUAL COMPLETION**",
        "",
        "## Coverage",
        "",
        f"- Issues inventoried: **{len(issues)}**.",
        f"- OCR pages checked: **{len(pages)}**.",
        f"- Candidate pages: **{len(hits)}**.",
        "- The Oregon City Banner-Courier and Oregon City Enterprise public calendars expose no 1923–1924 issues; this pass therefore checks regional titles that do have scans.",
        "- OCR is discovery only. Search silence is not evidence that a business, person, address, or event did not exist.",
        "",
        "| LCCN | Title | 1923 issues | 1924 issues | Pages |",
        "|---|---|---:|---:|---:|",
    ]
    for lccn, row in title_summary.items():
        lines.append(f"| `{lccn}` | {row['title']} | {row['years']['1923']} | {row['years']['1924']} | {row['pages']} |")
    lines.extend([
        "",
        "## Ranked shortlist",
        "",
        f"The readable report lists **{len(shortlist)}** of the **{len(hits)}** machine candidates: pages scoring at least 10, plus every Farr, exact-name, and Fifth Street candidate. The JSON preserves the same shortlist and source links.",
        "",
        "| Date | Title | Page | Score | Reasons | Matched groups | Scan |",
        "|---|---|---:|---:|---|---|---|",
    ])
    if not shortlist:
        lines.append("No candidates met the bounded co-occurrence rules.")
    for hit in shortlist:
        lines.append(
            f"| {hit['date']} | {hit['title']} | {hit['seq']} | {hit['score']} | "
            f"{', '.join(hit['reasons'])} | {', '.join(hit['groups'])} | [PDF]({hit['pdf_url']}) |"
        )
    lines.extend([
        "## Limits / next step",
        "",
        "- Visually inspect every plausible candidate page before promoting a claim.",
        "- Record unrelated-name false positives so they are not repeatedly re-opened.",
        "- Any local 1923–1924 newspaper work remains a manual microfilm callout because those local scans are not exposed online.",
        f"- Machine-readable coverage and candidate shortlist: `{OUT_JSON.relative_to(ROOT)}`.",
    ])
    if errors:
        lines.extend(["", "## Retrieval errors", "", f"The machine-readable file records **{len(errors)}** calendar, issue-page, or OCR retrieval errors for later retry."])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"1923-1924 regional discovery: {len(issues)} issues / {len(pages)} pages / {len(hits)} candidates / {len(errors)} errors")


if __name__ == "__main__":
    main()
