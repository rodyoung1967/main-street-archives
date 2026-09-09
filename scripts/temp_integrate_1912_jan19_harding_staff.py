#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one anchor in {rel}, found {count}: {old!r}")
    write(rel, text.replace(old, new, 1))

S = "S-299"
E = "E-273"
P1 = "P-399"
P2 = "P-400"
CAP = "evidence/source-captures/1912-01-19-courier-harding-drugstore-staff-visual-review.md"
E_NAME = "Harding Drug Store staff item: Percy Cross and A. B. Wilmot, 1912"

append_once(
    "evidence/source-register.md",
    "## S-299 — Oregon City Courier, 19 January 1912 p.8 — Harding Drug Store staff item",
    f'''## S-299 — Oregon City Courier, 19 January 1912 p.8 — Harding Drug Store staff item
Type: Primary newspaper page scan; **VISUALLY VERIFIED** 8 September 2026.  
Canonical page: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/  
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8.pdf  
PDF SHA-256: `bc4bdb274d1d0530e087da7a01b3f0dfc832ef1174ccd6cfba53e4ec89795a62`.  
Related evidence/business/people: `{E}` / `BUS-007` / `{P1}`, `{P2}`.  
Repository source capture: `{CAP}`.  
Notes: Direct scan inspection of the upper-left Local News column reports that **Percy Cross accepted a position in Harding Drug Store during the absence of A. B. Wilmot**. The page prints no street number and no formal job title. Separate 5 January evidence places Geo. A. Harding at 511 Main; do not treat this 19 January page as an independent exact-address source.'''
)

append_once(
    "database/sources.yml",
    "  - id: S-299\n",
    f'''  - id: S-299
    name: Oregon City Courier, 19 January 1912 p.8 — Harding Drug Store staff item
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/
    notes: >-
      Visually verified 8 Sep 2026 from the original page scan. The local-news item directly reports Percy Cross accepting a position in Harding Drug Store during the absence of A. B. Wilmot. No street number, formal job title, ownership status, or employment duration is printed. PDF SHA-256 bc4bdb274d1d0530e087da7a01b3f0dfc832ef1174ccd6cfba53e4ec89795a62.
    related_evidence: [E-273]
    related_businesses: [BUS-007]
    related_people: [P-399, P-400]'''
)

append_once(
    "evidence/evidence-register.md",
    "## E-273 — Harding Drug Store staff item: Percy Cross and A. B. Wilmot, 1912",
    f'''## E-273 — {E_NAME}
Type: Primary newspaper scan / business-staff evidence; **VISUALLY VERIFIED**.  
Date: **19 January 1912**.  
Source: `{S}`.  
Related business/people: `BUS-007`; `{P1}`, `{P2}`.  
Record: `evidence/E-273-1912-harding-drugstore-staff-cross-wilmot.md`.  
Capture: `{CAP}`.  
Claims: The 19 January 1912 *Oregon City Courier* p.8 scan directly reports **Percy Cross** accepting a position in **Harding Drug Store** during the absence of **A. B. Wilmot**. This documents active business staffing/operation and directly associates both men with the store. The page gives no street number and no formal job title, license, ownership interest, employment duration, or reason/duration of Wilmot's absence. Separate 5 January evidence (`E-092`) places Geo. A. Harding at 511 Main, but this page is not an independent exact-address source.  
Confidence: **Very High / DOCUMENTED-DIRECT** for the published staffing statement; unresolved for exact roles, employment duration, ownership/tenancy, and address on this page.'''
)

append_once(
    "database/evidence.yml",
    "  - id: E-273\n",
    f'''  - id: E-273
    name: "{E_NAME}"
    type: Primary newspaper scan / business-staff evidence; visually verified
    claims:
      - The 19 January 1912 Oregon City Courier p.8 scan directly reports Percy Cross accepting a position in Harding Drug Store during the absence of A. B. Wilmot.
      - The item directly associates Cross and Wilmot with Harding Drug Store and documents active staffing/operation on that date.
      - The page prints no street number, formal job title, professional license, ownership status, employment duration, or reason/duration of Wilmot's absence.
      - Separate 5 January evidence E-092 places Geo. A. Harding at 511 Main; the 19 January item is not an independent exact-address source.
    confidence: Very High for the visually verified published statement; unresolved for role details, duration and exact address on this page.
    related_sources: [S-299]
    related_businesses: [BUS-007]
    related_people: [P-399, P-400]
    related_buildings: []
    repository_file: evidence/E-273-1912-harding-drugstore-staff-cross-wilmot.md'''
)

append_once(
    "people/people-index.md",
    "| P-399 | [Percy Cross](profiles/percy-cross.md)",
    '''## 19 January 1912 Harding Drug Store staff additions

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-399 | [Percy Cross](profiles/percy-cross.md) | Harding Drug Store staff / temporary-position notice | 19 Jan. 1912 Courier visually reports Cross accepted a position in Harding Drug Store during A. B. Wilmot's absence. Formal job title, credentials and duration unresolved. `E-273` / `S-299`. |
| P-400 | [A. B. Wilmot](profiles/a-b-wilmot.md) | Harding Drug Store staff association | Same notice directly associates Wilmot with the store and says he was absent. Formal job title, credentials, ownership and absence duration/reason unresolved. `E-273` / `S-299`. |'''
)

append_once(
    "database/people.yml",
    "  - id: P-399\n",
    '''  - id: P-399
    name: Percy Cross
    role: Harding Drug Store staff / temporary-position notice
    notes: Visually verified 19 Jan 1912 Courier reports Cross accepted a position in Harding Drug Store during the absence of A. B. Wilmot. Formal job title, credentials, duration and ownership status are not stated.
    related_businesses: [BUS-007]
    related_evidence: [E-273]
    related_sources: [S-299]
    repository_file: people/profiles/percy-cross.md

  - id: P-400
    name: A. B. Wilmot
    role: Harding Drug Store staff association
    notes: Visually verified 19 Jan 1912 Courier directly associates Wilmot with Harding Drug Store and says he was absent when Percy Cross accepted a position. Formal job title, credentials, ownership status and absence duration/reason are not stated; initials are preserved exactly as the scan reads them.
    related_businesses: [BUS-007]
    related_evidence: [E-273]
    related_sources: [S-299]
    repository_file: people/profiles/a-b-wilmot.md'''
)

append_once(
    "businesses/harding-drug-store.md",
    "## 19 January 1912 staff control — Percy Cross and A. B. Wilmot",
    '''## 19 January 1912 staff control — Percy Cross and A. B. Wilmot
A visually verified 19 January 1912 *Oregon City Courier* local-news item (`E-273` / `S-299`) reports that **Percy Cross (`P-399`) accepted a position in Harding Drug Store during the absence of A. B. Wilmot (`P-400`)**. This directly documents active staffing/operation and associates both men with the business.

The item does not state a street number or either man's formal job title. It therefore does not replace the separately verified 5 January 1912 **Geo. A. Harding — 511 Main** address control (`E-092`), nor does it by itself prove Cross or Wilmot worked at the numbered 511 premises. Do not infer pharmacist/druggist credentials, ownership, or employment duration without another source.'''
)

replace_once(
    "database/businesses.yml",
    "    related_people:\n    - P-001\n",
    "    related_people:\n    - P-001\n    - P-399\n    - P-400\n"
)
replace_once(
    "database/businesses.yml",
    "    - E-267\n\n    - E-219\n",
    "    - E-267\n    - E-273\n\n    - E-219\n"
)
replace_once(
    "database/businesses.yml",
    "    - S-293\n\n    - S-245\n",
    "    - S-293\n    - S-299\n\n    - S-245\n"
)

append_once(
    "indexes/id-crosswalk.md",
    "## S-299 / E-273 — 19 January 1912 Harding Drug Store staff control",
    '''## S-299 / E-273 — 19 January 1912 Harding Drug Store staff control
- `S-299` → `E-273` → `BUS-007`: visually verified 19 Jan. 1912 *Courier* p.8 staffing/operation statement for Harding Drug Store.
- `S-299` / `E-273` → `P-399`: Percy Cross accepted a position in the store.
- `S-299` / `E-273` → `P-400`: A. B. Wilmot was the absent store-associated person named in the notice.
- No building ID or exact-address edge is created from this page because the notice prints no street number; `E-092` remains the separate 5 Jan. 1912 511 Main address control.'''
)

replace_once(
    "evidence/source-captures/1912-main-street-research.md",
    "- **501 Main:** no exact 1912 occupant recovered in the current pass.",
    "- **501 Main:** positive exact occupant — Joe Wilson's Palace Saloon is directly at **501 Main** on 19 March (`E-104` / `S-118`)."
)
append_once(
    "evidence/source-captures/1912-main-street-research.md",
    "## 19 January Harding Drug Store staff visual-review integration",
    '''## 19 January Harding Drug Store staff visual-review integration
Page 8 of the 19 January 1912 *Oregon City Courier* is now directly scan-certified as `S-299` / `E-273`. The Local News column reports **Percy Cross accepting a position in Harding Drug Store during the absence of A. B. Wilmot**. This is direct business-staff evidence and strengthens the January operating chronology. The notice prints no street number or job title, so it is not used as an independent 511 Main source or as proof that either man was a pharmacist/druggist.'''
)

append_once(
    "registers/research-log.md",
    "### 2026-09-08 — 19 January 1912 Harding Drug Store staff item scan-certified",
    '''### 2026-09-08 — 19 January 1912 Harding Drug Store staff item scan-certified
- Retrieved the original 19 Jan. 1912 *Oregon City Courier* p.8 PDF and visually inspected the scan after OCR discovery.
- Direct reading: Percy Cross accepted a position in Harding Drug Store during the absence of A. B. Wilmot (`S-299` / `E-273`; `P-399`, `P-400`).
- Preserved PDF SHA-256 `bc4bdb274d1d0530e087da7a01b3f0dfc832ef1174ccd6cfba53e4ec89795a62` in the source capture.
- Kept the page address-neutral because it prints no street number; 5 Jan. 1912 `E-092` remains the separate direct 511 Main control.
- Corrected the stale 1912 annual-capture target-status bullet so 501 Main now reflects the already integrated 19 Mar. Joe Wilson / Palace Saloon exact-address evidence (`E-104` / `S-118`).'''
)

print("Integrated S-299 / E-273 / P-399 / P-400 and corrected stale 1912 501 status")
# workflow-trigger touch 2
