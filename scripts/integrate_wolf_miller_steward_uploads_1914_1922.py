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

EXISTING_1922 = {
    "source_id": "S-113",
    "evidence_id": "E-097",
    "repo_path": "newspapers/oregon-city-enterprise/1922-08-18-page-5-gates-fire-replacement-building.pdf",
    "upload_name": "501 Main st (new Building) Oregon City enterprise., August 18, 1922, Page Page five, Image 5.pdf",
    "sha256": "eb951886bcf06817db94368d3634d08848bcdab99e886c0ce5e73b4c1d7d6348",
    "size": 843509,
}


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
        raise RuntimeError(f"Expected text not found in {path}: {old[:180]!r}")
    write(path, text.replace(old, new, 1))


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


# Guard ID sequence and exact baseline assumptions. Never backfill or renumber IDs.
source_register = read("evidence/source-register.md")
evidence_register = read("evidence/evidence-register.md")
timeline_yml = read("database/timeline.yml")
for required in ["## S-185", "## E-165", "  - id: T-060"]:
    haystack = source_register if required.startswith("## S-") else evidence_register if required.startswith("## E-") else timeline_yml
    if required not in haystack:
        raise RuntimeError(f"Expected current baseline marker missing: {required}")
for forbidden in ["## S-186", "## S-187", "## S-188"]:
    if forbidden in source_register:
        raise RuntimeError(f"Source ID already assigned: {forbidden}")
for forbidden in ["## E-166", "## E-167"]:
    if forbidden in evidence_register:
        raise RuntimeError(f"Evidence ID already assigned: {forbidden}")
for forbidden in ["  - id: T-061", "  - id: T-062"]:
    if forbidden in timeline_yml:
        raise RuntimeError(f"Timeline ID already assigned: {forbidden.strip()}")

# Build hash index before fetching so exact duplicates are deduplicated rather than copied.
existing_hashes = {}
for p in ROOT.rglob("*.pdf"):
    try:
        existing_hashes.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), str(p))
    except OSError:
        pass

for item in NEW_PDFS:
    with urllib.request.urlopen(item["url"], timeout=60) as r:
        data = r.read()
    got_sha = sha256_bytes(data)
    if got_sha != item["sha256"] or len(data) != item["size"]:
        raise RuntimeError(
            f"Canonical PDF differs from steward upload for {item['source_id']}: "
            f"got {got_sha}/{len(data)}, expected {item['sha256']}/{item['size']}"
        )
    duplicate = existing_hashes.get(got_sha)
    if duplicate:
        item["actual_repo_path"] = duplicate
        item["already_preserved"] = True
    else:
        p = ROOT / item["repo_path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        item["actual_repo_path"] = item["repo_path"]
        item["already_preserved"] = False
        existing_hashes[got_sha] = item["repo_path"]

# The August 1922 upload must be the exact page already preserved as S-113.
p = ROOT / EXISTING_1922["repo_path"]
data = p.read_bytes()
if sha256_bytes(data) != EXISTING_1922["sha256"] or len(data) != EXISTING_1922["size"]:
    raise RuntimeError("Existing S-113 repository PDF does not match the steward upload exactly")

by_id = {x["source_id"]: x for x in NEW_PDFS}

capture_path = "evidence/source-captures/1914-1922-wolf-miller-steward-upload-supplement-2026-09-02.md"
capture = f"""# Wolf & Miller steward-upload supplement, 1914–1922

Review date: **2 September 2026**.

Status: **FIVE PROJECT-STEWARD UPLOADS ACCOUNTED FOR; FOUR PREVIOUSLY UNPRESERVED PAGE PDFs ADDED OR DEDUPLICATED BY EXACT HASH; ONE 1922 PAGE CONFIRMED AS AN EXACT DUPLICATE OF EXISTING S-113.**

## S-186 — Oregon City Courier, 2 July 1914, p. 1 — rejected Wolf & Miller identity lead

This page was supplied because of possible Wolf/Miller names. Visual review does **not** identify the later Wolf & Miller firm, Gilbert Miller, 503/505 Main, shoes, men's furnishings, or shoe repair. It includes unrelated people such as **C. A. Miller** and **G. R. Wolfe** (with an `e`).

Handling: preserve the page as a searched/rejected identity lead only. Do not use it as evidence for `BUS-012` occupancy, partnership, or identity.

Repository file: `{by_id['S-186']['actual_repo_path']}`  
Canonical PDF: {by_id['S-186']['url']}  
Original upload: `{by_id['S-186']['upload_name']}`  
SHA-256: `{by_id['S-186']['sha256']}` ({by_id['S-186']['size']} bytes).

## S-187 / E-166 — Oregon City Enterprise, 20 September 1918, p. 3

A display advertisement visibly prints:

**Men's Clothing / Shoes and Shoe Repairing / WOLF & MILLER / 505 Main St., Oregon City.**

Supported:
- Wolf & Miller was directly advertising at **505 Main Street** by 20 September 1918;
- the advertised lines were men's clothing, shoes, and shoe repairing.

Limits:
- the ad does not identify the partners by full name, establish legal shares, property ownership, or prove that the surviving present-day 505 structure was already present;
- it strengthens but does not by itself prove the Gilbert Miller identity bridge.

Repository file: `{by_id['S-187']['actual_repo_path']}`  
Canonical PDF: {by_id['S-187']['url']}  
Original upload: `{by_id['S-187']['upload_name']}`  
SHA-256: `{by_id['S-187']['sha256']}` ({by_id['S-187']['size']} bytes).

## Existing S-034 / E-027 — Oregon City Courier, 10 October 1918, p. 4

This exact page was already the registered source `S-034` / evidence `E-027`, but the page PDF itself had not been preserved in the newspaper directory. The steward upload now supplies durable exact-page preservation.

The page's local-business feature directly identifies **Wolf & Miller — 505 Main**, shoes, men's clothing/furnishings, and an up-to-date shoe-repair department with Landis electric machinery. It also says the partnership was dissolving: one member would go to Idaho and the other would restock and continue the business.

Repository file: `{by_id['S-034']['actual_repo_path']}`  
Canonical PDF: {by_id['S-034']['url']}  
Original upload: `{by_id['S-034']['upload_name']}`  
SHA-256: `{by_id['S-034']['sha256']}` ({by_id['S-034']['size']} bytes).

## S-188 / E-167 — Oregon City Courier, 31 October 1918, p. 4 — 503/505 address conflict

The page publishes the answer key to the earlier “Who's Who in Oregon City” feature. Answer **22** visibly says:

**Wolf & Miller at 503 Main St.**, not only sell men's clothing and furnishing goods, but also do shoe repairing.

This conflicts with:
- the **20 September 1918 Enterprise** advertisement at **505 Main** (`S-187` / `E-166`);
- the **10 October 1918 Courier** feature at **505 Main** (`S-034` / `E-027`);
- the archive's separately verified **24 October 1918** Wolf & Miller 505 evidence (`S-138` / `E-124`).

Safe handling:
- preserve the printed **503 Main** wording as a real primary-source conflict;
- do **not** silently correct it to 505;
- do **not** infer a 505→503 move from this answer key alone, especially because the 10 October feature had announced a partnership dissolution and because an answer-key or typesetting error is also possible;
- leave rapid relocation, address error, and other explanations open pending independent late-October/November evidence.

Repository file: `{by_id['S-188']['actual_repo_path']}`  
Canonical PDF: {by_id['S-188']['url']}  
Original upload: `{by_id['S-188']['upload_name']}`  
SHA-256: `{by_id['S-188']['sha256']}` ({by_id['S-188']['size']} bytes).

## Existing S-113 / E-097 — Oregon City Enterprise, 18 August 1922, p. 5

The steward upload `{EXISTING_1922['upload_name']}` is byte-for-byte identical to the already-preserved repository page:

`{EXISTING_1922['repo_path']}`

SHA-256: `{EXISTING_1922['sha256']}` ({EXISTING_1922['size']} bytes).

No duplicate source ID or duplicate PDF was created. The existing source remains `S-113` / `E-097` and documents the C. E. Gates Fifth/Main fire-replacement building. Its article does **not** print 501 Main; the project's 501/503 mapping remains a hypothesis requiring an independent bridge.
"""
if not (ROOT / capture_path).exists():
    write(capture_path, capture)

# New evidence records.
write("evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md", f"""# E-166 — Wolf & Miller at 505 Main, 20 September 1918

Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.

Source: `S-187` — *Oregon City Enterprise*, 20 September 1918, p. 3.

The advertisement directly prints **Wolf & Miller**, **505 Main St., Oregon City**, and the lines **Men's Clothing**, **Shoes and Shoe Repairing**.

This is direct dated evidence for the business name, exact address, and advertised trade. It does not identify the partners by full name, prove legal shares or real-estate ownership, or establish continuity of the present physical building.

Repository PDF: `{by_id['S-187']['actual_repo_path']}`  
SHA-256: `{by_id['S-187']['sha256']}`.
""")

write("evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md", f"""# E-167 — Wolf & Miller 503 Main answer-key conflict, 31 October 1918

Type: Primary newspaper answer-key text; **VISUALLY VERIFIED**.

Source: `S-188` — *Oregon City Courier*, 31 October 1918, p. 4.

Answer 22 says **Wolf & Miller at 503 Main St.** sold men's clothing and furnishing goods and did shoe repairing.

This printed address conflicts with direct 505 Main evidence on 20 September (`E-166` / `S-187`), 10 October (`E-027` / `S-034`), and 24 October (`E-124` / `S-138`). Preserve the conflict. Do not silently normalize 503 to 505 and do not treat the answer key alone as proof of a move. A rapid relocation after the announced dissolution, an answer-key/typesetting error, or another explanation remains possible.

Repository PDF: `{by_id['S-188']['actual_repo_path']}`  
SHA-256: `{by_id['S-188']['sha256']}`.
""")

# Enrich existing S-034 and S-113 with durable PDF/provenance data.
replace_once(
    "evidence/source-register.md",
    "## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller\nSource/location: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/\nRelated evidence: `E-027`\nNotes: 505 Main shoe business / repair. Related evidence E-027.",
    f"""## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/  
Repository PDF: `{by_id['S-034']['actual_repo_path']}`  
Original uploaded filename: `{by_id['S-034']['upload_name']}`  
Related evidence: `E-027`  
Notes: **VISUALLY VERIFIED** 505 Main shoe / men's furnishings / shoe-repair feature; partnership dissolution says one member would go to Idaho and the other would restock and continue. Exact steward-upload bytes preserved. SHA-256 `{by_id['S-034']['sha256']}`."""
)

replace_once(
    "evidence/source-register.md",
    "## S-113 — Oregon City Enterprise, 18 August 1922, Gates fire-replacement building\nCanonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-5.pdf\nRepository PDF: `newspapers/oregon-city-enterprise/1922-08-18-page-5-gates-fire-replacement-building.pdf`\nType: Primary newspaper post-fire construction and property evidence; **visually verified full-page scan**.\nRelated evidence: `E-097`, `E-108`; cross-reference `E-096`, `E-103`\nRepository source capture: `evidence/source-captures/1922-harding-wolf-gates-sale-and-rebuild.md`",
    f"""## S-113 — Oregon City Enterprise, 18 August 1922, Gates fire-replacement building
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-5.pdf  
Repository PDF: `{EXISTING_1922['repo_path']}`  
Type: Primary newspaper post-fire construction and property evidence; **visually verified full-page scan**.  
Related evidence: `E-097`, `E-108`; cross-reference `E-096`, `E-103`  
Repository source capture: `evidence/source-captures/1922-harding-wolf-gates-sale-and-rebuild.md`  
Duplicate steward-upload alias: `{EXISTING_1922['upload_name']}` is byte-for-byte identical to the canonical repository PDF; no duplicate source ID/file created. SHA-256 `{EXISTING_1922['sha256']}`."""
)

append_once("evidence/source-register.md", "## S-186 —", f"""
## S-186 — Oregon City Courier, 2 July 1914, p. 1, Wolf/Miller name check
Type: Primary newspaper scan; **VISUALLY VERIFIED AS A REJECTED/NON-TARGET IDENTITY LEAD**.  
Canonical PDF: {by_id['S-186']['url']}  
Repository PDF: `{by_id['S-186']['actual_repo_path']}`  
Original uploaded filename: `{by_id['S-186']['upload_name']}`  
Notes: Page contains unrelated C. A. Miller and G. R. Wolfe references but does not identify Wolf & Miller, Gilbert Miller, 503/505 Main, or the later shoe business. No new evidence record created. SHA-256 `{by_id['S-186']['sha256']}`.

## S-187 — Oregon City Enterprise, 20 September 1918, p. 3, Wolf & Miller 505 Main advertisement
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical PDF: {by_id['S-187']['url']}  
Repository PDF: `{by_id['S-187']['actual_repo_path']}`  
Original uploaded filename: `{by_id['S-187']['upload_name']}`  
Related evidence: `E-166`; business `BUS-012`; building `B-002`.  
Notes: Ad directly prints Wolf & Miller, 505 Main St., Oregon City, men's clothing, shoes and shoe repairing. SHA-256 `{by_id['S-187']['sha256']}`.

## S-188 — Oregon City Courier, 31 October 1918, p. 4, Wolf & Miller 503 Main answer-key conflict
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical PDF: {by_id['S-188']['url']}  
Repository PDF: `{by_id['S-188']['actual_repo_path']}`  
Original uploaded filename: `{by_id['S-188']['upload_name']}`  
Related evidence: `E-167`; business `BUS-012`; buildings `B-001`, `B-002`.  
Notes: Answer key prints Wolf & Miller at 503 Main; conflicts with 20 Sep, 10 Oct and 24 Oct 505 Main evidence. Preserve conflict; no move inferred. SHA-256 `{by_id['S-188']['sha256']}`.
""")

append_once("evidence/evidence-register.md", "## E-166 —", f"""
## E-166 — 20 September 1918 Wolf & Miller advertisement at 505 Main
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.  
Source: `S-187` — *Oregon City Enterprise*, 20 September 1918, p. 3.  
Claims: Direct advertisement prints Wolf & Miller at **505 Main St., Oregon City**, with men's clothing, shoes and shoe repairing.  
Confidence: Very High for name, exact address, and advertised trade; partner identities, legal shares, title, and surviving-building continuity unresolved.  
Related business: `BUS-012`; building `B-002`.  
Repository record: `evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md`.

## E-167 — 31 October 1918 Wolf & Miller 503 Main answer-key conflict
Type: Primary newspaper answer-key text; **VISUALLY VERIFIED**.  
Source: `S-188` — *Oregon City Courier*, 31 October 1918, p. 4.  
Claims: Answer 22 directly prints **Wolf & Miller at 503 Main St.**, selling men's clothing/furnishings and doing shoe repair.  
Conflict: Direct sources on 20 Sep (`E-166`), 10 Oct (`E-027`) and 24 Oct (`E-124`) print **505 Main**. Preserve the conflict; the 31 Oct line is not by itself proof of relocation and is not silently corrected.  
Confidence: Very High for the printed 503 wording; Low/undetermined for what caused the discrepancy.  
Related business: `BUS-012`; buildings `B-001`, `B-002`.  
Repository record: `evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md`.
""")

# Source YAML, including enrichment of existing S-034.
replace_once(
    "database/sources.yml",
    "  - id: S-034\n    name: Oregon City Courier, 10 October 1918, Wolf and Miller\n    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/\n    notes: 505 Main shoe business / repair. Related evidence E-027.",
    f"""  - id: S-034
    name: Oregon City Courier, 10 October 1918, Wolf and Miller
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
    notes: "Visually verified 505 Main shoe, men's-furnishings and shoe-repair feature; partnership dissolution wording. Exact steward-upload page preserved at {by_id['S-034']['actual_repo_path']}; SHA-256 {by_id['S-034']['sha256']}. Related evidence E-027."""
)

append_once("database/sources.yml", "  - id: S-186", f"""
  - id: S-186
    name: Oregon City Courier, 2 July 1914, p. 1, Wolf/Miller name check
    url: {by_id['S-186']['url']}
    notes: "Visually reviewed rejected/non-target identity lead. Contains unrelated C. A. Miller and G. R. Wolfe but no Wolf & Miller firm, Gilbert Miller, 503/505 Main or shoe business. Repository PDF {by_id['S-186']['actual_repo_path']}; SHA-256 {by_id['S-186']['sha256']}."
  - id: S-187
    name: Oregon City Enterprise, 20 September 1918, p. 3, Wolf & Miller 505 Main advertisement
    url: {by_id['S-187']['url']}
    notes: "Visually verified exact 505 Main advertisement for Wolf & Miller, men's clothing, shoes and shoe repairing. E-166/BUS-012/B-002. Repository PDF {by_id['S-187']['actual_repo_path']}; SHA-256 {by_id['S-187']['sha256']}."
  - id: S-188
    name: Oregon City Courier, 31 October 1918, p. 4, Wolf & Miller 503 Main answer-key conflict
    url: {by_id['S-188']['url']}
    notes: "Visually verified answer key prints Wolf & Miller at 503 Main, conflicting with 20 Sep, 10 Oct and 24 Oct 505 evidence. Preserve conflict; no move inferred. E-167/BUS-012/B-001/B-002. Repository PDF {by_id['S-188']['actual_repo_path']}; SHA-256 {by_id['S-188']['sha256']}."
""")

append_once("database/evidence.yml", "  - id: E-166", """
  - id: E-166
    name: 20 September 1918 Wolf & Miller advertisement at 505 Main
    type: Primary newspaper advertisement; visually verified
    claims:
      - Wolf & Miller is directly advertised at 505 Main St., Oregon City.
      - Advertised lines are men's clothing, shoes and shoe repairing.
      - Partner identities, legal shares, real-estate title and surviving-building continuity are not established.
    confidence: Very High for printed business, exact address and trade; identity/title/structure continuity unresolved.
    related_sources: [S-187]
    related_businesses: [BUS-012]
    related_buildings: [B-002]
    repository_file: evidence/E-166-1918-09-20-wolf-miller-505-main-ad.md
  - id: E-167
    name: 31 October 1918 Wolf & Miller 503 Main answer-key conflict
    type: Primary newspaper answer-key text; visually verified
    claims:
      - The Courier answer key directly prints Wolf & Miller at 503 Main St., with men's clothing/furnishings and shoe repair.
      - This conflicts with 20 September, 10 October and 24 October 1918 primary evidence at 505 Main.
      - The discrepancy is preserved; the answer key alone does not prove a move and is not silently corrected.
    confidence: Very High for printed 503 wording; cause of discrepancy unresolved.
    related_sources: [S-188, S-187, S-034, S-138]
    related_evidence: [E-166, E-027, E-124]
    related_businesses: [BUS-012]
    related_buildings: [B-001, B-002]
    repository_file: evidence/E-167-1918-10-31-wolf-miller-503-main-conflict.md
""")

# Update Wolf & Miller business record and structured business mirror.
replace_once(
    "businesses/wolf-miller.md",
    "A visually verified 3 February 1916 Springfield notice identifies Gilbert Miller with Wolf & Miller there; it is an antecedent, not Oregon City occupancy (`E-113` / `S-125`). The 10 and 24 October 1918 Oregon City records directly place **Wolf & Miller at 505 Main** in the shoe/repair trade (`E-027`, `E-124`; `S-034`, `S-138`). The Wolf partner and legal shares remain unresolved; preserve the C. E. Miller/Gilbert Miller discrepancy. Do not merge this Wolf with S. Wolf or later 503 ownership without a direct bridge.",
    "A visually verified 3 February 1916 Springfield notice identifies Gilbert Miller with Wolf & Miller there; it is an antecedent, not Oregon City occupancy (`E-113` / `S-125`). The **20 September**, **10 October**, and **24 October 1918** Oregon City records directly place **Wolf & Miller at 505 Main** in the men's-clothing/shoe/repair trade (`E-166`, `E-027`, `E-124`; `S-187`, `S-034`, `S-138`). A **31 October Courier answer key instead prints 503 Main** (`E-167` / `S-188`). Preserve that 503/505 conflict: it may reflect a rapid post-dissolution move, an answer-key/typesetting error, or another explanation; the answer key alone does not establish relocation. The Wolf partner and legal shares remain unresolved; preserve the C. E. Miller/Gilbert Miller discrepancy. Do not merge this Wolf with S. Wolf or later 503 ownership without a direct bridge."
)

old_bus = """  - id: BUS-012
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
    repository_file: businesses/wolf-miller.md"""
new_bus = """  - id: BUS-012
    name: Wolf & Miller
    address: 505 Main on 20 Sep, 10 Oct and 24 Oct 1918; 31 Oct Courier answer key prints conflicting 503 Main
    notes: Direct September/October 1918 primary records place Wolf & Miller at 505 Main in men's clothing, shoes and shoe repair. A 31 October answer key instead prints 503 Main; preserve this unresolved conflict and do not infer a move from that line alone. Earlier Springfield association directly names Gilbert Miller on February 3, 1916; this is not 1916 Oregon City occupancy. Wolf given name/legal shares and C. E. Miller/Gilbert Miller discrepancy remain unresolved.
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
    repository_file: businesses/wolf-miller.md"""
replace_once("database/businesses.yml", old_bus, new_bus)

# Update address/building records without converting the conflict into a move.
append_once("buildings/505-main.md", "## 1918 Wolf & Miller address conflict update — 2 September 2026", """
## 1918 Wolf & Miller address conflict update — 2 September 2026

A newly preserved **20 September 1918 Enterprise** ad (`E-166` / `S-187`) pushes direct Wolf & Miller occupancy at **505 Main** back before the existing 10 and 24 October anchors. A **31 October Courier answer key** (`E-167` / `S-188`) then prints **503 Main** for the same firm/trade. The archive preserves the discrepancy and does not treat the 31 October line as proof of a move. Rapid relocation after the announced partnership dissolution, answer-key/typesetting error, and other explanations remain open.
""")
append_once("buildings/503-main.md", "## 31 October 1918 Wolf & Miller address conflict", """
## 31 October 1918 Wolf & Miller address conflict

The **31 October 1918 Courier** answer key (`E-167` / `S-188`) prints **Wolf & Miller at 503 Main**, selling men's clothing/furnishings and doing shoe repair. Direct sources on 20 September, 10 October, and 24 October print the firm at **505 Main**. This is retained as an unresolved primary-source address conflict, not accepted as proof that Wolf & Miller actually relocated into the 503 premises.
""")

replace_once(
    "timelines/505-main.md",
    "| 10, 24 Oct. 1918 | **Wolf & Miller at 505 Main**, shoe/repair trade. | **Exact, visually verified**; Wolf identity and Miller discrepancy open. | `BUS-012`; `E-027`, `E-124`; `S-034`, `S-138` |",
    "| 20 Sep.; 10, 24 Oct. 1918; conflicting 31 Oct. answer key | **Wolf & Miller at 505 Main** in three direct September/October records; 31 Oct. *Courier* answer key instead prints **503 Main**. | **Exact, visually verified printed wording**. Preserve 503/505 conflict; do not infer a move from answer key alone. Wolf identity, Miller discrepancy, and reason for address conflict open. | `BUS-012`; `E-166`, `E-027`, `E-124`, `E-167`; `S-187`, `S-034`, `S-138`, `S-188` |"
)
append_once("timelines/503-main.md", "| 31 Oct. 1918 | Wolf & Miller answer key prints **503 Main**", """
| 31 Oct. 1918 | Wolf & Miller answer key prints **503 Main** while 20 Sep., 10 Oct. and 24 Oct. primary sources print **505 Main**. | **Primary-source conflict**; not proof of a move, occupancy continuity, or property ownership. | `BUS-012`; `E-167`; `S-188` |
""")

append_once("timeline.md", "## September–October 1918 — Wolf & Miller 505 Main anchors and 503 answer-key conflict", """
## September–October 1918 — Wolf & Miller 505 Main anchors and 503 answer-key conflict

A visually verified **20 September 1918 Oregon City Enterprise** advertisement directly prints **Wolf & Miller, 505 Main St., Oregon City**, with men's clothing, shoes and shoe repairing (`S-187` / `E-166`). The already registered **10 October Courier** feature (`S-034` / `E-027`), now preserved as an exact page PDF, again prints **505 Main** and says the partnership was dissolving, one member going to Idaho while the other would restock and continue. Existing **24 October** evidence (`S-138` / `E-124`) also places the firm at 505.

A newly preserved **31 October Courier** answer key, however, prints **Wolf & Miller at 503 Main** (`S-188` / `E-167`). The archive preserves this address conflict. It is not silently corrected to 505 and is not treated alone as proof of a 505→503 move; rapid relocation after dissolution, an answer-key/typesetting error, or another explanation remains open.
""")

append_once("registers/business-timeline.md", "| 20 Sep. 1918 | Wolf & Miller | `BUS-012` | `E-166`; `S-187`", """
| 20 Sep. 1918 | Wolf & Miller | `BUS-012` | `E-166`; `S-187` | Very High primary | Direct ad: 505 Main; men's clothing, shoes and shoe repairing. |
| 31 Oct. 1918 | Wolf & Miller | `BUS-012` | `E-167`; `S-188` | Very High for printed wording; interpretation unresolved | Courier answer key prints 503 Main, conflicting with 20 Sep., 10 Oct. and 24 Oct. 505 evidence; no move inferred. |
""")

append_once("evidence/open-questions.md", "### 1918-OQ-WM-ADDRESS — Wolf & Miller 503/505 conflict", """
### 1918-OQ-WM-ADDRESS — Wolf & Miller 503/505 conflict
The 20 September, 10 October and 24 October 1918 sources place Wolf & Miller at **505 Main**, while the 31 October *Courier* answer key prints **503 Main** (`E-166`, `E-027`, `E-124`, `E-167`). Determine whether the last line reflects a rapid move after partnership dissolution, a typesetting/answer-key error, or another address change. Do not select a theory without independent evidence.
""")
append_once("evidence/research-leads.md", "### Wolf & Miller 31 October 1918 503/505 discrepancy", """
### Wolf & Miller 31 October 1918 503/505 discrepancy
Search late October–December 1918 advertisements, municipal licenses, directories, leases and property records for Wolf & Miller, Gilbert Miller, 503 Main and 505 Main. The immediate goal is to explain why three primary records through 24 October print 505 while the 31 October *Courier* answer key prints 503. Preserve all address variants until resolved.
""")

append_once("indexes/id-crosswalk.md", "| `S-187` / `E-166` | `BUS-012`; `B-002`", """
| `S-187` / `E-166` | `BUS-012`; `B-002` | 20 Sep. 1918 direct Wolf & Miller advertisement at 505 Main. |
| `S-188` / `E-167` | `BUS-012`; `B-001`, `B-002` | 31 Oct. 1918 answer key prints 503 Main, conflicting with 505 evidence; no move inferred. |
| `S-186` | none assigned | 2 Jul. 1914 page preserved as rejected/non-target Wolf/Miller identity lead. |
""")

append_once("registers/research-log.md", "| 2026-09-02 | Integrated five Wolf & Miller / Gates steward uploads", """
| 2026-09-02 | Integrated five Wolf & Miller / Gates steward uploads | Four previously unpreserved newspaper PDFs were hash-verified and preserved; the 18 Aug. 1922 Gates page was confirmed byte-for-byte identical to existing S-113 and deduplicated. Added 20 Sep. 1918 Wolf & Miller 505 evidence and preserved the 31 Oct. 1918 answer-key 503/505 conflict without inferring a move. |
""")

append_once("ARCHIVE_INDEX.md", "## 2 September 2026 — Wolf & Miller steward-upload supplement", """
## 2 September 2026 — Wolf & Miller steward-upload supplement

Five newly supplied project-steward PDFs were reconciled against the repository. Four previously unpreserved pages are now stored under `newspapers/`; the 18 Aug. 1922 Gates building page was an exact duplicate of existing `S-113` and was not copied. New direct evidence places Wolf & Miller at **505 Main on 20 Sep. 1918** (`S-187` / `E-166`), while the **31 Oct. 1918 Courier answer key prints 503 Main** (`S-188` / `E-167`). The archive retains this as an unresolved primary-source conflict rather than asserting a move. `S-186` preserves the 2 Jul. 1914 page as a rejected identity lead; the existing `S-034` 10 Oct. 1918 source now has its exact page PDF preserved.
""")

# Timeline YAML IDs follow current T-060.
append_once("database/timeline.yml", "  - id: T-061", """
  - id: T-061
    date: 20 September 1918
    summary: Oregon City Enterprise advertisement directly places Wolf & Miller at 505 Main St., Oregon City, advertising men's clothing, shoes and shoe repairing.
    confidence: Very High for printed business, address and trade; partner identity, title and surviving-building continuity unresolved.
    related_evidence: [E-166]
    related_sources: [S-187]
    related_businesses: [BUS-012]
    related_buildings: [B-002]
  - id: T-062
    date: 31 October 1918
    summary: Oregon City Courier answer key prints Wolf & Miller at 503 Main, conflicting with primary 20 Sep., 10 Oct. and 24 Oct. records at 505 Main. The conflict is preserved and no relocation is inferred from the answer key alone.
    confidence: Very High for printed 503 wording; cause of address discrepancy unresolved.
    related_evidence: [E-167]
    related_sources: [S-188, S-187, S-034, S-138]
    related_businesses: [BUS-012]
    related_buildings: [B-001, B-002]
""")

print("Wolf & Miller steward-upload integration prepared successfully.")
for item in NEW_PDFS:
    print(item["source_id"], item["actual_repo_path"], "existing" if item["already_preserved"] else "added")
print("S-113 duplicate confirmed:", EXISTING_1922["repo_path"])
