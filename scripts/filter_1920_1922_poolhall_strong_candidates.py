#!/usr/bin/env python3
"""Filter the broad 1920–1922 pool-hall OCR inventory to strong local candidates.

This is discovery triage only. It never promotes OCR to evidence. The broad
inventory intentionally favored recall; this script requires target terms to
co-occur inside the same saved OCR snippet so page-wide keyword collisions do
not drive visual-review work.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence/source-captures/1920-1922-505-poolhall-transition-ocr-discovery.json"
OUT = ROOT / "evidence/source-captures/1920-1922-505-poolhall-strong-candidates.md"
JSON_OUT = ROOT / "evidence/source-captures/1920-1922-505-poolhall-strong-candidates.json"

RX = {
    "505_main": re.compile(r"\b505(?:\s*(?:½|1\s*/\s*2|1[-/]?2))?\b.{0,90}\bmain\b|\bmain\b.{0,90}\b505(?:\s*(?:½|1\s*/\s*2|1[-/]?2))?\b", re.I),
    "505": re.compile(r"\b505(?:\s*(?:½|1\s*/\s*2|1[-/]?2))?\b", re.I),
    "leland": re.compile(r"\b(?:a\.?\s+)?leland\b", re.I),
    "clem_dollar": re.compile(r"\bclem\s+dollar\b", re.I),
    "timms": re.compile(r"\btimms\b|\btimm['’]s\b", re.I),
    "freeze_name": re.compile(r"\bdr\.?\s+freeze\b|\bfreeze\b.{0,60}\b(?:optom|optical|office|main|505)\b", re.I),
    "wolf_miller": re.compile(r"\bwolf\s*(?:&|and)\s*miller\b", re.I),
    "pool": re.compile(r"\bpool\s*(?:hall|room)\b|\bbilliard", re.I),
    "cigar": re.compile(r"\bcigar|\btobacco\b", re.I),
    "transition": re.compile(r"\b(?:open(?:ed|ing)?|move[ds]?|remov(?:e|ed|ing)|sold|sell|sale|lease[ds]?|rent(?:ed|ing)?|permit(?:ted)?|license[ds]?|sign|remodel(?:ed|ing)?|repair(?:ed|ing)?|build(?:ing|s)?|construct(?:ed|ion|ing)?|demolish(?:ed|ing)?|tear(?:ing)?\s+down)\b", re.I),
    "main_block": re.compile(r"\bmain\b.{0,120}\b(?:fifth|5th|sixth|6th)\b|\b(?:fifth|5th|sixth|6th)\b.{0,120}\bmain\b", re.I),
}


def tests(text: str):
    present = {k for k, rx in RX.items() if rx.search(text)}
    reasons = []
    if "505_main" in present:
        reasons.append("exact 505/Main proximity")
    if "505" in present and "pool" in present:
        reasons.append("505 + pool/billiards in same snippet")
    if "505" in present and "cigar" in present:
        reasons.append("505 + cigar/tobacco in same snippet")
    if "leland" in present and ({"505", "pool", "cigar"} & present):
        reasons.append("Leland + target use/address in same snippet")
    if "clem_dollar" in present and ({"505", "pool"} & present):
        reasons.append("Clem Dollar + target pool/address in same snippet")
    if "timms" in present and ({"505", "pool", "cigar"} & present):
        reasons.append("Timms + target use/address in same snippet")
    if "freeze_name" in present and ({"505", "transition"} & present):
        reasons.append("Dr. Freeze + target address/transition in same snippet")
    if "wolf_miller" in present and ({"505", "transition"} & present):
        reasons.append("Wolf & Miller + target address/transition in same snippet")
    if "505" in present and "transition" in present:
        reasons.append("505 + transition language in same snippet")
    if "pool" in present and "main_block" in present and "transition" in present:
        reasons.append("Main Fifth–Sixth pool + transition language")
    return present, reasons


def compact(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    strong = []
    review = []
    for hit in data.get("hits", []):
        selected = []
        reason_set = []
        for raw in hit.get("snippets", []):
            text = compact(raw)
            present, reasons = tests(text)
            if reasons:
                selected.append({"text": text, "terms": sorted(present), "reasons": reasons})
                reason_set.extend(reasons)
        if selected:
            strong.append({
                "date": hit["date"], "seq": hit["seq"], "url": hit["url"],
                "groups": hit.get("groups", []), "reasons": sorted(set(reason_set)),
                "snippets": selected,
            })
            continue

        # Secondary queue: exact person/business names on a page with target-use
        # groups, even where the saved snippets do not overlap. This is deliberately
        # separated from the strong list and should be reviewed only after strong hits.
        groups = set(hit.get("groups", []))
        names = groups & {"leland", "clem_dollar", "timms", "freeze", "wolf_miller"}
        uses = groups & {"505", "pool_hall", "cigar_tobacco"}
        if names and uses:
            review.append({
                "date": hit["date"], "seq": hit["seq"], "url": hit["url"],
                "groups": sorted(groups),
                "reason": "page-wide target-name + target-use collision; no same-snippet proximity",
            })

    result = {
        "source": str(SRC.relative_to(ROOT)),
        "broad_candidate_count": len(data.get("hits", [])),
        "strong_count": len(strong),
        "secondary_count": len(review),
        "strong": strong,
        "secondary": review,
        "status": "OCR discovery triage only; visual scan review required before promotion",
    }
    JSON_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# 1920–1922 Enterprise 505/505½ pool-hall strong candidate index",
        "",
        "Status: **OCR DISCOVERY TRIAGE ONLY — direct scan review required before any historical claim**",
        "",
        f"Broad inventory candidates: **{result['broad_candidate_count']}**.",
        f"Same-snippet high-signal candidates: **{result['strong_count']}**.",
        f"Secondary page-wide collision queue: **{result['secondary_count']}**.",
        "",
        "The broad pass favored recall. This filter requires exact target names/addresses and target-use or transition language to occur in the **same saved OCR context window**. It prevents unrelated articles on the same newspaper page from being treated as a historical lead.",
        "",
        "## High-signal candidates",
        "",
    ]
    if not strong:
        lines.append("No same-snippet high-signal candidates survived the filter. This is a search result only, not evidence of historical absence.")
    for i, h in enumerate(strong, 1):
        lines += [
            f"### {i}. {h['date']} — page {h['seq']}",
            f"OCR URL: {h['url']}",
            f"Reasons: {'; '.join(h['reasons'])}",
            f"Broad groups: {', '.join(h['groups'])}",
            "",
        ]
        for s in h["snippets"][:4]:
            lines.append(f"- OCR context ({'; '.join(s['reasons'])}): {s['text']}")
        lines.append("")

    lines += ["## Secondary collision queue", ""]
    if not review:
        lines.append("No secondary candidates.")
    else:
        lines += ["| Date | Page | Groups | Why secondary |", "|---|---:|---|---|"]
        for h in review:
            lines.append(f"| {h['date']} | {h['seq']} | {', '.join(h['groups'])} | {h['reason']} |")

    lines += [
        "",
        "## Handling rule",
        "",
        "1. Visually inspect the original newspaper page for high-signal candidates first.",
        "2. Do not promote OCR wording, identity, address, succession, construction, or relocation without scan verification.",
        "3. Review the secondary queue only if high-signal pages do not resolve the transition.",
        "4. Search silence or filtered-out pages are not evidence of vacancy, non-operation, or absence of construction.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"filtered {result['broad_candidate_count']} broad hits -> {result['strong_count']} strong + {result['secondary_count']} secondary")


if __name__ == "__main__":
    main()
