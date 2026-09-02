#!/usr/bin/env python3
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(".")

NEW_PDFS = [
    {
        "source_id": "S-186",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1914-07-02/ed-1/seq-1.pdf",
        "repo_path": "newspapers/oregon-city-courier/1914-07-02-page-1-wolfe-miller-name-check.pdf",
        "upload_name": "Wolf & Miller (names maybe) Oregon City courier., July 02, 1914, Image 1.pdf",
        "sha256": "0644f663fc40f2e2cc4354bcba6f2b7e449cf4bb2bcbe3a5c214d5e074ce53ea",
        "size": 751977,
    },
    {
        "source_id": "S-187",
        "evidence_id": "E-166",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1918-09-20/ed-1/seq-3.pdf",
        "repo_path": "newspapers/oregon-city-enterprise/1918-09-20-page-3-wolf-miller-505-main-ad.pdf",
        "upload_name": "505 Main (Wolf & Miller Ad) Oregon City enterprise., September 20, 1918, Page Page 3, Image 3.pdf",
        "sha256": "e57be939f0cdb3bf1f9f943e19acdfbb6ea168c72d29b959fdaa160e977e7f00",
        "size": 717562,
    },
    {
        "source_id": "S-034",
        "evidence_id": "E-027",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4.pdf",
        "repo_path": "newspapers/oregon-city-courier/1918-10-10-page-4-wolf-miller-505-main.pdf",
        "upload_name": "505 Main (Wolf & Miller) Oregon City courier., October 10, 1918, Page 4, Image 4.pdf",
        "sha256": "bbed6092aa4743f7e86286c4c25f03544648bc1e523bf5d5da557d487af302c0",
        "size": 866276,
    },
    {
        "source_id": "S-188",
        "evidence_id": "E-167",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-31/ed-1/seq-4.pdf",
        "repo_path": "newspapers/oregon-city-courier/1918-10-31-page-4-wolf-miller-503-main-answer-key.pdf",
        "upload_name": "505 Main (Wolf & Miller-Clothes and shoe repair) Oregon City courier., October 31, 1918, Page 4, Image 4.pdf",
        "sha256": "f2ebfe6a187f50057ea63ee373df79c3b7b4f857218159f3e72aa751d3221900",
        "size": 801148,
    },
]

EXISTING_DUP = {
    "source_id": "S-113",
    "evidence_id": "E-097",
    "repo_path": "newspapers/oregon-city-enterprise/1922-08-18-page-5-gates-fire-replacement-building.pdf",
    "upload_name": "501 Main st (new Building) Oregon City enterprise., August 18, 1922, Page Page five, Image 5.pdf",
    "sha256": "eb951886bcf06817db94368d3634d08848bcdab99e886c0ce5e73b4c1d7d6348",
    "size": 843509,
}

CAPTURE = "evidence/source-captures/1914-1922-wolf-miller-steward-upload-supplement-2026-09-02.md"

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + "\n" + block.strip("\n") + "\n")

def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old[:160]!r}")
    write(path, text.replace(old, new, 1))

def sha256(data):
    return hashlib.sha256(data).hexdigest()

src = read("evidence/source-register.md")
ev = read("evidence/evidence-register.md")
if "## S-185" not in src or "## S-186" in src:
    raise RuntimeError("Unexpected source ID state; expected S-185 highest and S-186 free")
if "## E-165" not in ev or "## E-166" in ev:
    raise RuntimeError("Unexpected evidence ID state; expected E-165 highest and E-166 free")
dt = read("database/timeline.yml")
if "  - id: T-060" not in dt or "  - id: T-061" in dt:
    raise RuntimeError("Unexpected timeline ID state; expected T-060 highest and T-061 free")

existing_hashes = {}
for p in ROOT.rglob("*.pdf"):
    try:
        existing_hashes.setdefault(sha256(p.read_bytes()), str(p))
    except OSError:
        pass

for item in NEW_PDFS:
    with urllib.request.urlopen(item["url"], timeout=90) as r:
        data = r.read()
    got = sha256(data)
    if got != item["sha256"] or len(data) != item["size"]:
        raise RuntimeError(
            f"Canonical PDF mismatch {item['url']}: got {got}/{len(data)}, expected {item['sha256']}/{item['size']}"
        )
    dup = existing_hashes.get(got)
    if dup:
        item["actual_repo_path"] = dup
        item["deduplicated"] = True
    else:
        p = ROOT / item["repo_path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        item["actual_repo_path"] = item["repo_path"]
        item["deduplicated"] = False
        existing_hashes[got] = item["repo_path"]

dup_path = ROOT / EXISTING_DUP["repo_path"]
if not dup_path.exists():
    raise RuntimeError(f"Expected existing S-113 PDF missing: {dup_path}")
dup_data = dup_path.read_bytes()
if sha256(dup_data) != EXISTING_DUP["sha256"] or len(dup_data) != EXISTING_DUP["size"]:
    raise RuntimeError("Existing S-113 PDF does not match steward upload hash/size")

if not (ROOT / CAPTURE).exists():
    write(CAPTURE, f"""# Wolf & Miller steward-upload supplement, 1914–1922

Review date: **2 September 2026**.

Status: **FIVE PROJECT-STEWARD UPLOADS ACCOUNTED FOR; FOUR PREVIOUSLY UNPRESERVED PAGE PDFS HASH-VERIFIED AND PRESERVED; ONE 1922 PAGE DEDUPLICATED TO EXISTING S-113.**

## 2 July 1914 Courier p. 1 — S-186, rejected identity lead

The page was supplied because of possible Wolf/Miller names. Visual review does **not** identify the later Wolf & Miller partnership, Gilbert Miller, 503/505 Main, shoes, or shoe repair. It contains unrelated references including **C. A. Miller** and **G. R. Wolfe**. Preserve as a searched/rejected identity lead only.

Repository PDF: `{NEW_PDFS[0]['actual_repo_path']}`  
Original upload: `{NEW_PDFS[0]['upload_name']}`  
SHA-256: `{NEW_PDFS[0]['sha256']}` ({NEW_PDFS[0]['size']} bytes).

## 20 September 1918 Enterprise p. 3 — S-187 / E-166

A display advertisement directly prints **Men's Clothing / Shoes and Shoe Repairing / WOLF & MILLER / 505 Main St., Oregon City**.

Supported: Wolf & Miller directly advertised at **505 Main** by this date; advertised lines were men's clothing, shoes, and shoe repair. Partner names/shares, property ownership, and surviving-building continuity are not established.

Repository PDF: `{NEW_PDFS[1]['actual_repo_path']}`  
Original upload: `{NEW_PDFS[1]['upload_name']}`  
SHA-256: `{NEW_PDFS[1]['sha256']}` ({NEW_PDFS[1]['size']} bytes).

## 10 October 1918 Courier p. 4 — existing S-034 / E-027

The source/evidence IDs already existed, but the exact page PDF was not preserved. The page identifies **Wolf & Miller, 505 Main**, shoes, men's clothing/furnishings, and shoe repair; it also states the partnership was dissolving, with one partner going to Idaho and the other continuing the business.

Repository PDF: `{NEW_PDFS[2]['actual_repo_path']}`  
Original upload: `{NEW_PDFS[2]['upload_name']}`  
SHA-256: `{NEW_PDFS[2]['sha256']}` ({NEW_PDFS[2]['size']} bytes).

## 31 October 1918 Courier p. 4 — S-188 / E-167, address conflict

The answer page prints **Wolf & Miller at 503 Main St.**, selling men's clothing/furnishings and doing shoe repair. This conflicts with primary records at **505 Main** on 20 September, 10 October, and 24 October 1918.

Preserve the printed 503 wording. Do **not** silently correct it and do **not** infer a move from this answer key alone. A rapid post-dissolution move, typesetting/answer-key error, or another explanation remains open pending corroboration.

Repository PDF: `{NEW_PDFS[3]['actual_repo_path']}`  
Original upload: `{NEW_PDFS[3]['upload_name']}`  
SHA-256: `{NEW_PDFS[3]['sha256']}` ({NEW_PDFS[3]['size']} bytes).

## 18 August 1922 Enterprise p. 5 — existing S-113 / E-097

The steward upload `{EXISTING_DUP['upload_name']}` is byte-for-byte identical to the existing repository PDF `{EXISTING_DUP['repo_path']}`. SHA-256 `{EXISTING_DUP['sha256']}` ({EXISTING_DUP['size']} bytes). No duplicate binary or source ID was created.

The article documents the C. E. Gates Fifth/Main fire-replacement building; it does **not** print 501 Main, so exact 501/503 mapping remains unresolved.
""")

write("evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md", """# E-166 — Wolf & Miller at 505 Main, 20 September 1918

Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.

Source: `S-187` — *Oregon City Enterprise*, 20 September 1918, p. 3.

The advertisement directly prints **Wolf & Miller**, **505 Main St., Oregon City**, and the lines **Men's Clothing**, **Shoes and Shoe Repairing**.

This establishes the named business, exact address, and advertised trade on the publication date. It does not establish partner full names, legal shares, real-estate ownership, or continuity of the present physical building.
""")

write("evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md", """# E-167 — Wolf & Miller 503/505 address conflict, 31 October 1918

Type: Primary newspaper answer-key text; **VISUALLY VERIFIED**.

Source: `S-188` — *Oregon City Courier*, 31 October 1918, p. 4.

The answer page prints **Wolf & Miller at 503 Main St.**, with men's clothing/furnishings and shoe repair. This conflicts with direct 505 Main evidence on 20 September (`E-166` / `S-187`), 10 October (`E-027` / `S-034`), and 24 October (`E-124` / `S-138`).

Preserve the conflict. The 31 October answer page is not, by itself, proof that Wolf & Miller moved from 505 to 503. A rapid post-dissolution move, a typesetting/answer-key error, or another explanation remains possible.
""")

replace_once(
    "evidence/source-register.md",
    """## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
Related evidence: `E-027`
Notes: 505 Main shoe business / repair. Related evidence E-027.
""",
    f"""## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
Repository PDF: `{NEW_PDFS[2]['actual_repo_path']}`
Original uploaded filename: `{NEW_PDFS[2]['upload_name']}`
Related evidence: `E-027`; cross-reference `E-166`, `E-167`
Notes: 505 Main shoe/clothing business and shoe-repair department; partnership dissolution wording. Exact steward-upload PDF preserved, SHA-256 `{NEW_PDFS[2]['sha256']}`. The 31 October answer key later prints 503 Main; preserve that conflict rather than inferring a move.
"""
)

replace_once(
    "evidence/source-register.md",
    """## S-113 — Oregon City Enterprise, 18 August 1922, Gates fire-replacement building
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-5.pdf
Repository PDF: `newspapers/oregon-city-enterprise/1922-08-18-page-5-gates-fire-replacement-building.pdf`
Type: Primary newspaper post-fire construction and property evidence; **visually verified full-page scan**.
Related evidence: `E-097`, `E-108`; cross-reference `E-096`, `E-103`
Repository source capture: `evidence/source-captures/1922-harding-wolf-gates-sale-and-rebuild.md`
""",
    f"""## S-113 — Oregon City Enterprise, 18 August 1922, Gates fire-replacement building
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-5.pdf
Repository PDF: `newspapers/oregon-city-enterprise/1922-08-18-page-5-gates-fire-replacement-building.pdf`
Type: Primary newspaper post-fire construction and property evidence; **visually verified full-page scan**.
Related evidence: `E-097`, `E-108`; cross-reference `E-096`, `E-103`
Repository source capture: `evidence/source-captures/1922-harding-wolf-gates-sale-and-rebuild.md`
Steward-upload duplicate: `{EXISTING_DUP['upload_name']}` is byte-for-byte identical to the repository PDF; SHA-256 `{EXISTING_DUP['sha256']}` ({EXISTING_DUP['size']} bytes). No duplicate binary or ID created.
"""
)

append_once("evidence/source-register.md", "## S-186 —", f"""
## S-186 — Oregon City Courier, 2 July 1914, p. 1, Wolfe/Miller name-check page
Type: Primary newspaper scan; **VISUALLY VERIFIED NON-TARGET / REJECTED IDENTITY LEAD**; exact steward-upload PDF bytes preserved.  
Canonical PDF: {NEW_PDFS[0]['url']}  
Repository PDF: `{NEW_PDFS[0]['actual_repo_path']}`  
Original uploaded filename: `{NEW_PDFS[0]['upload_name']}`  
Related evidence: none; identity-triage source only.  
Notes: Page contains unrelated C. A. Miller and G. R. Wolfe references, but no Wolf & Miller firm, Gilbert Miller, 503/505 Main, or shoe-repair business. SHA-256 `{NEW_PDFS[0]['sha256']}`.

## S-187 — Oregon City Enterprise, 20 September 1918, p. 3, Wolf & Miller advertisement
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical PDF: {NEW_PDFS[1]['url']}  
Repository PDF: `{NEW_PDFS[1]['actual_repo_path']}`  
Original uploaded filename: `{NEW_PDFS[1]['upload_name']}`  
Related evidence: `E-166`; business `BUS-012`; building `B-002`.  
Notes: Directly prints Wolf & Miller, 505 Main St., Oregon City; men's clothing, shoes and shoe repairing. SHA-256 `{NEW_PDFS[1]['sha256']}`.

## S-188 — Oregon City Courier, 31 October 1918, p. 4, Wolf & Miller 503 Main answer-key conflict
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical PDF: {NEW_PDFS[3]['url']}  
Repository PDF: `{NEW_PDFS[3]['actual_repo_path']}`  
Original uploaded filename: `{NEW_PDFS[3]['upload_name']}`  
Related evidence: `E-167`; business `BUS-012`; buildings `B-001`, `B-002`.  
Notes: Answer page directly prints Wolf & Miller at 503 Main St.; conflicts with 20 Sep and 10/24 Oct 1918 evidence at 505 Main. Do not infer relocation without corroboration. SHA-256 `{NEW_PDFS[3]['sha256']}`.
""")

append_once("evidence/evidence-register.md", "## E-166 —", """
## E-166 — Wolf & Miller advertisement at 505 Main, 20 September 1918
Type: Primary newspaper visual evidence.  
Date: 20 September 1918.  
Source: `S-187` — *Oregon City Enterprise*, p. 3.  
Status: **VISUALLY VERIFIED**.  
Claims: Advertisement directly prints **Wolf & Miller**, **505 Main St., Oregon City**, men's clothing, shoes and shoe repairing.  
Limits: No partner given names, legal ownership, real-estate title, or surviving-structure continuity established.  
Confidence: Very High for printed business, exact address, and advertised trade; partner identity, title, and structure continuity unresolved.  
Related business: `BUS-012`; building `B-002`.  
Repository evidence file: `evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md`.

## E-167 — Wolf & Miller 503/505 address conflict, 31 October 1918
Type: Primary newspaper visual evidence / conflict record.  
Date: 31 October 1918.  
Source: `S-188` — *Oregon City Courier*, p. 4.  
Status: **VISUALLY VERIFIED**.  
Claims: The answer page directly prints **Wolf & Miller at 503 Main St.** and describes men's clothing/furnishings and shoe repairing.  
Conflict: `E-166` (20 Sep), `E-027` (10 Oct), and `E-124` (24 Oct) place Wolf & Miller at **505 Main**.  
Limits: Do not convert the 31 October wording into a proved move. Typesetting/answer-key error, rapid relocation, or another address discrepancy remain possible.  
Confidence: Very High for the printed 503 wording; cause of the discrepancy unresolved.  
Related business: `BUS-012`; buildings `B-001`, `B-002`.  
Repository evidence file: `evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md`.
""")

append_once("businesses/wolf-miller.md", "## September–October 1918 steward-page supplement", """
## September–October 1918 steward-page supplement

New visually verified steward uploads add two important anchors:

- **20 September 1918 (`S-187` / `E-166`)** — a direct Enterprise advertisement prints **Wolf & Miller, 505 Main St.**, men's clothing, shoes and shoe repairing.
- **31 October 1918 (`S-188` / `E-167`)** — the Courier answer page prints **Wolf & Miller at 503 Main St.**, conflicting with the 20 September and 10/24 October **505 Main** records.

The 31 October item is retained as an unresolved address conflict. It is **not** treated as proof that the firm moved from 505 to 503 after dissolution. Independent advertising, directories, leases/licenses, or other records are needed to decide whether this was a real move or a printed error.
""")

replace_once(
    "timelines/505-main.md",
    "| 10, 24 Oct. 1918 | **Wolf & Miller at 505 Main**, shoe/repair trade. | **Exact, visually verified**; Wolf identity and Miller discrepancy open. | `BUS-012`; `E-027`, `E-124`; `S-034`, `S-138` |",
    "| 20 Sep.; 10, 24 Oct. 1918; conflict 31 Oct. | **Wolf & Miller at 505 Main** on 20 Sep. and 10/24 Oct.; 31 Oct. Courier answer key prints **503 Main**. | **Exact, visually verified conflict.** Do not infer a move from 505 to 503 without corroboration; answer-key/typesetting error or rapid relocation remain possible. | `BUS-012`; `E-166`, `E-027`, `E-124`, `E-167`; `S-187`, `S-034`, `S-138`, `S-188` |"
)

append_once("timelines/503-main.md", "## 31 October 1918 Wolf & Miller address conflict", """
## 31 October 1918 Wolf & Miller address conflict

A visually verified *Oregon City Courier* answer page (`S-188` / `E-167`) prints **Wolf & Miller at 503 Main St.** This conflicts with direct 505 Main evidence on 20 September and 10/24 October 1918. The 503 wording is retained as a conflict only; it is not yet accepted as a proved 503 occupancy or relocation.
""")

append_once("buildings/505-main.md", "## Late-October 1918 Wolf & Miller address conflict", """
## Late-October 1918 Wolf & Miller address conflict

`S-187` / `E-166` directly places Wolf & Miller at **505 Main** on 20 September 1918, strengthening the earlier exact-address anchor. `S-188` / `E-167`, however, prints **503 Main** in the 31 October Courier answer key. Because 10 and 24 October evidence also says 505, the archive preserves this as an unresolved address conflict and does not infer a move or building change.
""")

append_once("buildings/503-main.md", "## 31 October 1918 Wolf & Miller conflict", """
## 31 October 1918 Wolf & Miller conflict

The 31 October 1918 *Courier* answer page (`S-188` / `E-167`) prints **Wolf & Miller at 503 Main St.** Direct records on 20 September and 10/24 October place the same named firm at **505 Main**. This is not sufficient to establish Wolf & Miller as a settled 503 occupant; retain it as a conflict pending corroboration.
""")

append_once("timeline.md", "## September–October 1918 — Wolf & Miller 505/503 address conflict", """
## September–October 1918 — Wolf & Miller 505/503 address conflict

A visually verified **20 September 1918 Enterprise** advertisement (`S-187` / `E-166`) directly prints **Wolf & Miller, 505 Main St., Oregon City**, with men's clothing, shoes and shoe repairing. The existing 10 and 24 October records also place the firm at 505.

A visually verified **31 October 1918 Courier** answer page (`S-188` / `E-167`) instead prints **Wolf & Miller at 503 Main St.** The discrepancy remains unresolved. The archive does not silently correct the 503 wording and does not infer a move from it alone.
""")

append_once("registers/business-timeline.md", "20 Sep. 1918 | Wolf & Miller | `BUS-012`", """
| 20 Sep. 1918 | Wolf & Miller | `BUS-012` | `E-166`; `S-187` | Very High primary | Direct advertisement: 505 Main; men's clothing, shoes and shoe repair. |
| 31 Oct. 1918 | Wolf & Miller address conflict | `BUS-012` | `E-167`; `S-188` | Very High for printed wording; interpretation unresolved | Courier answer page prints 503 Main despite 20 Sep and 10/24 Oct evidence at 505; no move inferred. |
""")

append_once("evidence/open-questions.md", "### 1918-OQ-WM-ADDRESS — Wolf & Miller 503/505 address conflict", """
### 1918-OQ-WM-ADDRESS — Wolf & Miller 503/505 address conflict
Why does the 31 October 1918 *Courier* answer page print **503 Main** for Wolf & Miller after primary records on 20 September, 10 October, and 24 October print **505 Main**? Test rapid relocation after partnership dissolution, answer-key/typesetting error, and other address explanations. Do not select a theory without independent evidence.
""")

append_once("evidence/research-leads.md", "### Wolf & Miller late-October 1918 address conflict", """
### Wolf & Miller late-October 1918 address conflict
Search late October–December 1918 advertisements, municipal licenses, directories, leases, tax/property records, and personal notices for Wolf & Miller, Gilbert Miller, 503 Main and 505 Main. The objective is to explain the new `S-188` / `E-167` 503 wording against the 20 Sep and 10/24 Oct 505 evidence.
""")

append_once("indexes/id-crosswalk.md", "| `S-187` / `E-166` | `BUS-012`; `B-002` |", """
| `S-186` | identity-triage only | 2 Jul. 1914 Courier page; unrelated Miller/Wolfe names, no target partnership evidence. |
| `S-187` / `E-166` | `BUS-012`; `B-002` | 20 Sep. 1918 direct Wolf & Miller advertisement at 505 Main. |
| `S-188` / `E-167` | `BUS-012`; `B-001`, `B-002` | 31 Oct. 1918 answer page prints 503 Main, conflicting with 505 evidence; no move inferred. |
""")

append_once("registers/research-log.md", "| 2026-09-02 | Five Wolf & Miller / Gates steward uploads reconciled |", """
| 2026-09-02 | Five Wolf & Miller / Gates steward uploads reconciled | Four previously unpreserved exact page PDFs hash-verified and preserved; 18 Aug. 1922 Gates page deduplicated to existing S-113. Added 20 Sep. 1918 direct 505 Wolf & Miller evidence and recorded the 31 Oct. 1918 503/505 address conflict without inferring relocation. |
""")

append_once("ARCHIVE_INDEX.md", "## 2 September 2026 — Wolf & Miller steward-upload supplement", """
## 2 September 2026 — Wolf & Miller steward-upload supplement

Five supplied newspaper PDFs were reconciled. Four previously unpreserved pages are now stored under `newspapers/`; the 18 Aug. 1922 Gates fire-replacement page was byte-for-byte identical to existing `S-113` and was not duplicated. New `S-187` / `E-166` directly places **Wolf & Miller at 505 Main on 20 Sep. 1918**. New `S-188` / `E-167` preserves a **31 Oct. 1918 Courier answer-page conflict printing 503 Main**. No move is inferred. `S-186` records the 2 Jul. 1914 page as a rejected identity lead; existing `S-034` now has its exact 10 Oct. 1918 PDF preserved.
""")

replace_once(
    "database/sources.yml",
    """  - id: S-034
    name: Oregon City Courier, 10 October 1918, Wolf and Miller
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
    notes: 505 Main shoe business / repair. Related evidence E-027.
""",
    f"""  - id: S-034
    name: Oregon City Courier, 10 October 1918, Wolf and Miller
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
    notes: 505 Main shoe/clothing business and shoe-repair department; partnership dissolution wording. Exact PDF preserved at {NEW_PDFS[2]['actual_repo_path']}, SHA-256 {NEW_PDFS[2]['sha256']}. Related evidence E-027; 31 October S-188/E-167 later prints conflicting 503 Main.
"""
)

append_once("database/sources.yml", "  - id: S-186", f"""
  - id: S-186
    name: Oregon City Courier, 2 July 1914, p. 1, Wolfe/Miller name-check page
    url: {NEW_PDFS[0]['url']}
    notes: Visually verified rejected identity lead. Exact PDF at {NEW_PDFS[0]['actual_repo_path']}; unrelated C. A. Miller and G. R. Wolfe references only, not Wolf & Miller partnership evidence. SHA-256 {NEW_PDFS[0]['sha256']}.

  - id: S-187
    name: Oregon City Enterprise, 20 September 1918, p. 3, Wolf & Miller advertisement
    url: {NEW_PDFS[1]['url']}
    notes: Visually verified direct advertisement for Wolf & Miller, 505 Main St., men's clothing, shoes and shoe repairing. Exact PDF at {NEW_PDFS[1]['actual_repo_path']}; E-166/BUS-012. SHA-256 {NEW_PDFS[1]['sha256']}.

  - id: S-188
    name: Oregon City Courier, 31 October 1918, p. 4, Wolf & Miller 503 Main answer-key conflict
    url: {NEW_PDFS[3]['url']}
    notes: Visually verified answer page prints Wolf & Miller at 503 Main, conflicting with 20 Sep and 10/24 Oct 505 Main records. Exact PDF at {NEW_PDFS[3]['actual_repo_path']}; E-167/BUS-012. Do not infer relocation. SHA-256 {NEW_PDFS[3]['sha256']}.
""")

append_once("database/evidence.yml", "  - id: E-166", """
  - id: E-166
    name: Wolf & Miller advertisement at 505 Main, 20 September 1918
    type: Primary newspaper visual evidence
    date: 20 September 1918
    claims:
      - Wolf & Miller directly advertises at 505 Main St., Oregon City.
      - Advertisement identifies men's clothing, shoes and shoe repairing.
      - Partner given names, legal ownership and surviving-building continuity are not established.
    confidence: Very High for printed business, address and advertised trade.
    related_sources: [S-187]
    related_businesses: [BUS-012]
    related_buildings: [B-002]
    repository_file: evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md

  - id: E-167
    name: Wolf & Miller 503/505 address conflict, 31 October 1918
    type: Primary newspaper visual evidence / conflict record
    date: 31 October 1918
    claims:
      - Courier answer page directly prints Wolf & Miller at 503 Main St. and describes clothing/furnishings and shoe repairing.
      - This conflicts with E-166, E-027 and E-124 placing the firm at 505 Main.
      - The archive does not infer relocation; printed error, rapid move or another address discrepancy remains possible.
    confidence: Very High for the printed 503 wording; unresolved for historical interpretation.
    related_sources: [S-188, S-187, S-034, S-138]
    related_evidence: [E-166, E-027, E-124]
    related_businesses: [BUS-012]
    related_buildings: [B-001, B-002]
    repository_file: evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md
""")

replace_once(
    "database/businesses.yml",
    """  - id: BUS-012
    name: Wolf & Miller
    address: 505 Main
    notes: October 10 1918 Oregon City Courier shoe business / shoe-repair department. Earlier Springfield association directly names Gilbert Miller on February 3, 1916; this is not 1916 occupancy at 505. Wolf given name and legal shares unresolved; preserve 1918 C. E. Miller discrepancy.
    related_buildings:
      - B-002
    related_people:
      - P-046
    related_evidence:
      - E-027
      - E-113
      - E-124
    related_sources:
      - S-034
      - S-125
      - S-138
    repository_file: businesses/wolf-miller.md
""",
    """  - id: BUS-012
    name: Wolf & Miller
    address: 505 Main on 20 Sep. and 10/24 Oct. 1918; 31 Oct. Courier answer key prints conflicting 503 Main
    notes: Direct 1918 records place the shoe/clothing/repair firm at 505 Main on 20 September and 10/24 October. A 31 October Courier answer page instead prints 503 Main; preserve the conflict and do not infer relocation without corroboration. Earlier Springfield association directly names Gilbert Miller on 3 February 1916 but is not Oregon City occupancy. Wolf given name/legal shares and C. E. Miller/Gilbert Miller discrepancy remain unresolved.
    related_buildings:
      - B-001
      - B-002
    related_people:
      - P-046
    related_evidence:
      - E-027
      - E-113
      - E-124
      - E-166
      - E-167
    related_sources:
      - S-034
      - S-125
      - S-138
      - S-187
      - S-188
    repository_file: businesses/wolf-miller.md
"""
)

append_once("database/timeline.yml", "  - id: T-061", """
  - id: T-061
    date: 20 September 1918
    summary: Oregon City Enterprise advertisement directly prints Wolf & Miller at 505 Main St., Oregon City, offering men's clothing, shoes and shoe repairing.
    confidence: Very High for printed business/address/trade; partner identity, title and structure continuity unresolved.
    related_evidence: [E-166]
    related_sources: [S-187]
    related_businesses: [BUS-012]
    related_buildings: [B-002]

  - id: T-062
    date: 31 October 1918
    summary: Oregon City Courier answer page prints Wolf & Miller at 503 Main St., conflicting with 20 September and 10/24 October records at 505 Main; relocation is not established.
    confidence: Very High for printed 503 wording; unresolved interpretation.
    related_evidence: [E-167]
    related_sources: [S-188]
    related_businesses: [BUS-012]
    related_buildings: [B-001, B-002]
""")

print("Wolf & Miller steward-upload integration prepared successfully.")
for item in NEW_PDFS:
    print(item["source_id"], item["actual_repo_path"], "deduplicated" if item["deduplicated"] else "added")
print("S-113 duplicate confirmed:", EXISTING_DUP["repo_path"])
