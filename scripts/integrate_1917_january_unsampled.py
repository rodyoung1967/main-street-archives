from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

SOURCE_ID = "S-247"
EVIDENCE_ID = "E-221"
TIMELINE_ID = "T-093"
EDDY_BUSINESS_ID = "BUS-100"
STREBIG_1917_BUSINESS_ID = "BUS-101"
MARKER = "1917 January unsampled Courier visual review — 2026-09-05"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block, marker=MARKER):
    text = read(rel)
    if marker in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")
    return True


def create_once(rel, content):
    p = ROOT / rel
    if p.exists():
        existing = p.read_text(encoding="utf-8")
        if MARKER not in existing:
            raise SystemExit(f"{rel} exists without expected marker")
        return False
    write(rel, content)
    return True


# Hard-stop on accidental ID reuse. Existing marker means the script is being rerun idempotently.
for rel, ident in [
    ("evidence/source-register.md", SOURCE_ID),
    ("evidence/evidence-register.md", EVIDENCE_ID),
    ("timeline.md", TIMELINE_ID),
    ("businesses/business-index.md", EDDY_BUSINESS_ID),
    ("businesses/business-index.md", STREBIG_1917_BUSINESS_ID),
]:
    text = read(rel)
    if ident in text and MARKER not in text:
        raise SystemExit(f"{ident} already appears in {rel}; stop rather than reuse/renumber")

capture_rel = "evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md"
capture = r'''# 1917 Oregon City Courier — January 11, 18 and 25 unsampled issue visual review

<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

Status: **VISUALLY VERIFIED — 3 complete issues / 24 of 24 page scans reviewed. 1917 remains IN PROGRESS.**

Archive IDs: source `S-247`; evidence `E-221`; timeline `T-093`; new business records `BUS-100` and `BUS-101`.

Preserved originals: `newspapers/oregon-city-courier/1917-january-unsampled/`  
Retrieval commit: `032e40d834369295984b4ab66bf9fa783adb9d73`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-january-unsampled/manifest.json`

## Scope and method

This pass continues the first-issue-of-each-month sample (`S-134` / `E-120`) by reviewing the three remaining January weekly issues: **11 January, 18 January and 25 January 1917**. The actual scanned newspaper page PDFs were retrieved from Historic Oregon Newspapers, preserved with SHA-256 hashes, rendered at readable resolution, and visually inspected page by page. OCR/text extraction was used only after visual inspection as a discovery/checking aid.

Issue inventory for this continuation:

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 11 Jan. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 18 Jan. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 25 Jan. 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Together with the earlier January 4 sample issue, January now has **4 complete Courier issues / 32 page images visually reviewed**. This does not certify the rest of 1917 or other relevant newspaper titles.

## Major new exact-address finding — 25 January p. 6

A large W. B. Eddy advertisement visibly states that the store's **new location** is:

- **427 Main Street**;
- **Corner 5th**;
- the **building formerly occupied by the Strebig Meat Market**.

The advertisement also says the business had been forced out of its other storeroom quickly. It does **not** print the former room's address, so no move is inferred from 526 Main or any other earlier Eddy address without an independent bridge.

This is direct evidence that **427 Main was a Fifth/Main corner address by 25 January 1917** and that W. B. Eddy's Store publicly represented itself there on that date. It also directly records a **Strebig Meat Market** as a former occupant of the building, but does not date that prior occupancy.

### Identity limits

- `BUS-100` **W. B. Eddy's Store (1917)** is kept separate from `BUS-032` **Eddy's Dependable Store**, directly advertised at 526 Main on 25 November 1915. Similar name/merchandise and chronology make a relationship worth testing, but the January 25 advertisement does not identify the old room as 526 Main and no source yet proves they are the same business/proprietor.
- `BUS-101` **Strebig Meat Market (former 427 occupant named in 1917)** is kept separate from `BUS-047`, the **Strebig fresh-meat market** advertised at Albright's Old Stand, Fifth/Main, in October 1907. The identical printed surname and meat-market context are significant, but a ten-year gap remains and identity/continuity is not assumed.
- Existing 1922 evidence places `BUS-087` Quality Restaurant at **427 Main** (`E-179` / `S-141`). The 1917 anchor is five years earlier; address continuity does **not** prove physical-building continuity through 1922.

## Repeated exact-address anchors in the three issues

These are dated observations, not proof of uninterrupted occupancy:

- **11 Jan., p. 2:** Portland Railway Light & Power Co. Electric Store — **Andresen Building, 619 Main**.
- **11 Jan., p. 4:** Scripture & May — **108 Fifth**.
- **18 Jan., p. 2:** Electric Store — **619 Main**.
- **18 Jan., p. 5:** Scripture & May — **108 Fifth**.
- **25 Jan., p. 2:** Electric Store — **619 Main**.
- **25 Jan., p. 5:** Scripture & May — **108 Fifth**.
- **25 Jan., p. 6:** W. B. Eddy's Store — **427 Main Street, Corner 5th**.
- Williams Bros. Transfer & Storage also visibly repeats **Office 612 Main Street** in this batch. One OCR rendering misread that number as 512; the scan controls and reads **612**.
- R. L. Holman's **Fifth and Main** undertaking advertising continues to recur, consistent with the already established 1917 intersection evidence.

## Other downtown transition context

- **18 Jan., p. 8:** a report says Frank J. Alldredge's barber shop moved into the storeroom formerly occupied by Charman & Co.'s drug store in the Electric Hotel building. No exact number is printed, so no numbered-address succession is assigned.
- **25 Jan., p. 8:** a planned men's resort is reported for a Main Street room of the Electric Hotel building. No exact number is printed.
- **25 Jan., p. 1:** the Commercial Club report says new business structures were contemplated along Main Street. This is broad development context only, not evidence of construction at 501/503/505.

## Exact target-address result

Across these **24 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was found. This is a bounded coverage result for the three January issues only. It is **not** evidence of vacancy, non-use, demolition, closure or absence at any address.

## Effect on 1917 status

1917 remains **IN PROGRESS**. The January continuation advances exhaustive Courier coverage but does not resolve:

1. the unreviewed Courier issues outside the completed sample/January batches;
2. complete relevant-title annual coverage;
3. the true **13 December 1917 Courier page 21** retrieval gap; or
4. the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap, including the 501/503/505/507/509/511 sequence.

The new 427 Main corner anchor should be used as a spatial and occupancy control, not as a substitute for the unresolved target-address evidence.
'''
create_once(capture_rel, capture)

eddy_rel = "businesses/w-b-eddys-store-1917.md"
eddy_page = r'''# W. B. Eddy's Store — 1917

<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

Business ID: `BUS-100`.

## Documented 25 January 1917 location

A visually verified *Oregon City Courier* advertisement on **25 January 1917, p. 6** (`S-247` / `E-221`) identifies **W. B. Eddy's Store** at its **new location, 427 Main Street, Corner 5th**. The advertisement says the building was formerly occupied by the Strebig Meat Market (`BUS-101`).

The ad says the business was forced from another storeroom in a hurry but does not give that former address. Therefore this record does **not** prove a move from the 1915 `BUS-032` Eddy's Dependable Store at 526 Main.

## Identity and continuity limits

`BUS-100` is intentionally separate from `BUS-032` until a source directly links the 1915 and 1917 businesses, proprietor, or move. It is also not merged with the 1910 Watson B. Eddy & Son record solely on initials/surname. The 1917 source proves the dated public business name/address only; it does not prove real-estate ownership, lease terms, prior address, or physical-building continuity to the 1922 Quality Restaurant at 427 Main.
'''
create_once(eddy_rel, eddy_page)

strebig_rel = "businesses/strebig-meat-market-427-former-occupant.md"
strebig_page = r'''# Strebig Meat Market — former 427 Main occupant named in 1917

<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

Business ID: `BUS-101`.

## What the 1917 source establishes

A visually verified W. B. Eddy advertisement in the *Oregon City Courier*, **25 January 1917, p. 6** (`S-247` / `E-221`), states that Eddy's new location at **427 Main Street, Corner 5th** was the **building formerly occupied by the Strebig Meat Market**.

This proves a prior Strebig Meat Market association with the 427 corner building relative to 25 January 1917, but the advertisement does not give the start date, end date, proprietor, lease, ownership, or exact transition day.

## Separate from the 1907 Strebig record until bridged

`BUS-047` is a separately documented **Strebig fresh-meat market** at **Albright's Old Stand, Fifth/Main** in October 1907. The matching surname/spelling, meat trade and Fifth/Main geography make identity a strong research target, but the archive does not merge `BUS-101` with `BUS-047` across the ten-year gap without an independent continuity/identity source.
'''
create_once(strebig_rel, strebig_page)

source_block = r'''## S-247 — Oregon City Courier, 11/18/25 January 1917 complete-page visual-review batch
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 24/24 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **11 January 1917 (8 pages); 18 January 1917 (8 pages); 25 January 1917 (8 pages)**.  
Preserved originals: `newspapers/oregon-city-courier/1917-january-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-january-unsampled/manifest.json`  
Retrieval commit: `032e40d834369295984b4ab66bf9fa783adb9d73`  
Related evidence/business/building: `E-221`; `BUS-100`, `BUS-101`; `B-016`.  
Capture: `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`.  
Notes: 25 Jan. p.6 directly prints W. B. Eddy's Store at **427 Main Street, Corner 5th** and says the building was formerly occupied by the **Strebig Meat Market**. The three issues also repeat 108 Fifth and 619 Main anchors. No exact 501/503/505/507/509/511 occupant was found in this bounded batch; silence is not vacancy evidence.'''
append_once("evidence/source-register.md", source_block)

evidence_block = r'''## E-221 — 25 January 1917 W. B. Eddy ad fixes 427 Main at corner Fifth and names former Strebig Meat Market occupancy
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->
Source: `S-247`  
Related building: `B-016`  
Related businesses: `BUS-100`, `BUS-101`; identity leads `BUS-032`, `BUS-047`; later 427 business `BUS-087`.  
Type: Primary newspaper advertisement; visually verified  
Claims:
- *Oregon City Courier*, **25 January 1917, p.6**, directly advertises **W. B. Eddy's Store** at its **new location, 427 Main Street, Corner 5th**.
- The same advertisement directly says that building was **formerly occupied by the Strebig Meat Market**.
- The advertisement says Eddy had been forced out of another storeroom quickly but does not print that former address; no 526-to-427 move is proved.
- `BUS-100` is therefore kept separate from the 1915 `BUS-032` Eddy's Dependable Store unless an independent identity/move bridge is found.
- `BUS-101` is kept separate from the 1907 `BUS-047` Strebig fresh-meat market at Albright's Old Stand/Fifth-Main unless an independent continuity/identity bridge is found.
- Existing 1922 `BUS-087` Quality Restaurant evidence at 427 is a later same-address anchor only; the 1917 advertisement does not prove physical-building survival or continuous occupancy through 1922.
- Across the complete 11/18/25 January batch (**24 visually reviewed pages**), no exact 501/503/505/507/509/511 Main occupant was established. This is coverage only and not negative evidence.
Classification: **DOCUMENTED / DIRECT** for the 25 January 1917 business/address/former-occupant wording; **UNRESOLVED** for Eddy 1915→1917 identity, Strebig 1907→pre-1917 identity, and 1917→1922 physical-building continuity.  
Confidence: **Very High** for the visible 25 January wording and 24-page visual-review count; unresolved for the cross-period identity/continuity questions.'''
append_once("evidence/evidence-register.md", evidence_block)

# Synchronized source/evidence YAML records.
sources = read("database/sources.yml")
if SOURCE_ID not in sources:
    sources = sources.rstrip() + r'''

  - id: S-247
    name: "Oregon City Courier 11/18/25 January 1917 complete-page visual-review batch"
    type: "Primary newspaper page scans; visually verified 24/24 pages"
    date: "1917-01-11 through 1917-01-25"
    repository_file: "evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md"
    notes: "Preserved originals and manifest are under newspapers/oregon-city-courier/1917-january-unsampled/. Jan 25 p6 directly prints W. B. Eddy's Store at 427 Main Street, Corner 5th, in building formerly occupied by Strebig Meat Market."
    related_evidence: [E-221]
    related_businesses: [BUS-100, BUS-101]
    related_buildings: [B-016]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if EVIDENCE_ID not in evidence:
    evidence = evidence.rstrip() + r'''

  - id: E-221
    name: "25 January 1917 W. B. Eddy ad fixes 427 Main at corner Fifth and names former Strebig Meat Market occupancy"
    type: "Primary newspaper advertisement; visually verified"
    date: "1917-01-25"
    claims:
      - "W. B. Eddy's Store directly advertises its new location as 427 Main Street, Corner 5th."
      - "The advertisement says the building was formerly occupied by the Strebig Meat Market."
      - "The prior Eddy storeroom is not numbered; no move from 526 Main is proved."
      - "BUS-100 remains separate from BUS-032 pending an identity/move bridge."
      - "BUS-101 remains separate from BUS-047 pending a 1907-to-pre-1917 identity/continuity bridge."
      - "The later 1922 Quality Restaurant at 427 is a same-address control, not proof of physical-building continuity."
      - "The 24-page January 11/18/25 batch established no exact 501/503/505/507/509/511 occupant; this is bounded coverage, not vacancy evidence."
    confidence: "Very High for the visually verified 1917 wording and page-review count; unresolved for cross-period identity and building continuity."
    related_sources: [S-247]
    related_businesses: [BUS-100, BUS-101, BUS-032, BUS-047, BUS-087]
    related_buildings: [B-016]
''' + "\n"
    write("database/evidence.yml", evidence)

# New business-index rows after current highest BUS-099 row.
bidx = read("businesses/business-index.md")
if EDDY_BUSINESS_ID not in bidx:
    lines = bidx.splitlines()
    pos = next((i for i, line in enumerate(lines) if line.startswith("| BUS-099 |")), None)
    if pos is None:
        raise SystemExit("BUS-099 row not found; cannot insert BUS-100/BUS-101 safely")
    rows = [
        "| BUS-100 | [W. B. Eddy's Store — 1917](w-b-eddys-store-1917.md) | 427 Main Street, corner Fifth (25 Jan. 1917) | Direct new-location advertisement `E-221` / `S-247`. Kept separate from 1915 BUS-032 and 1910 Watson B. Eddy record pending identity/move proof. |",
        "| BUS-101 | [Strebig Meat Market — former 427 occupant](strebig-meat-market-427-former-occupant.md) | Former occupant of 427 Main corner building by 25 Jan. 1917; exact occupancy dates unknown | Named directly as former occupant in `E-221` / `S-247`. Kept separate from 1907 BUS-047 pending identity/continuity proof. |",
    ]
    lines[pos + 1:pos + 1] = rows
    write("businesses/business-index.md", "\n".join(lines) + "\n")

businesses = read("database/businesses.yml")
if EDDY_BUSINESS_ID not in businesses:
    businesses = businesses.rstrip() + r'''

  - id: BUS-100
    name: "W. B. Eddy's Store — 1917"
    repository_file: "businesses/w-b-eddys-store-1917.md"
    address: "427 Main Street, corner Fifth (25 January 1917)"
    notes: "Direct advertisement calls 427 the new location and says the business was forced from another storeroom, whose address is not stated. Kept separate from BUS-032 and the 1910 Watson B. Eddy record pending an identity/move bridge."
    related_buildings: [B-016]
    related_evidence: [E-221]
    related_sources: [S-247]

  - id: BUS-101
    name: "Strebig Meat Market — former 427 Main occupant named in 1917"
    repository_file: "businesses/strebig-meat-market-427-former-occupant.md"
    address: "427 Main Street corner building; former occupant as of 25 January 1917; exact dates unknown"
    notes: "The W. B. Eddy advertisement says the 427 building was formerly occupied by the Strebig Meat Market. Kept separate from BUS-047 (1907 Strebig at Albright's Old Stand/Fifth-Main) pending independent identity/continuity proof."
    related_buildings: [B-016]
    related_evidence: [E-221]
    related_sources: [S-247]
''' + "\n"
    write("database/businesses.yml", businesses)

# Add the direct 1917 anchor to the B-016 narrative page.
building_block = r'''## 25 January 1917 exact corner-address control
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

`E-221` / `S-247` adds the earliest currently integrated exact-number evidence on this address page: a visually verified *Courier* advertisement identifies **W. B. Eddy's Store (`BUS-100`) at 427 Main Street, Corner 5th** and says the building was formerly occupied by the **Strebig Meat Market (`BUS-101`)**.

This directly fixes **427 Main as a Fifth/Main corner address by 25 January 1917**, but it does not establish the legal parcel, ownership, a specific construction date, or physical survival of the 1917 building into the 1922 Quality Restaurant (`BUS-087`) or 1925 mapped state. `BUS-100` is not merged with 1915 `BUS-032`, and `BUS-101` is not merged with 1907 `BUS-047`, without an independent bridge.'''
append_once("buildings/427-main.md", building_block)

# Synchronize B-016's YAML lists and concise note without reserializing the file.
buildings = read("database/buildings.yml")
m = re.search(r"(?ms)^  - id: B-016\n.*?(?=^  - id:|\Z)", buildings)
if not m:
    raise SystemExit("B-016 block not found in database/buildings.yml")
block = m.group(0)
if EVIDENCE_ID not in block:
    def add_inline(block_text, key, values):
        pat = re.compile(rf"(?m)^    {re.escape(key)}: \[(.*?)\]$")
        mm = pat.search(block_text)
        if not mm:
            raise SystemExit(f"B-016 {key} inline list not found")
        items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
        for value in values:
            if value not in items:
                items.append(value)
        return block_text[:mm.start()] + f"    {key}: [{', '.join(items)}]" + block_text[mm.end():]
    block = add_inline(block, "related_businesses", [EDDY_BUSINESS_ID, STREBIG_1917_BUSINESS_ID])
    block = add_inline(block, "related_evidence", [EVIDENCE_ID])
    block = add_inline(block, "related_sources", [SOURCE_ID])
    block = re.sub(
        r"(?m)^    notes: (.*)$",
        lambda mm: "    notes: " + mm.group(1) + " Jan 25 1917 Courier directly fixes 427 Main as corner Fifth for W. B. Eddy's Store and names Strebig Meat Market as former building occupant; cross-period business identity and physical-building continuity remain unresolved.",
        block,
        count=1,
    )
    buildings = buildings[:m.start()] + block + buildings[m.end():]
    write("database/buildings.yml", buildings)

# Update the canonical address-register row by address rather than positional assumptions.
addr = read("registers/address-register.md")
if EVIDENCE_ID not in addr:
    lines = addr.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if line.startswith("| 427 Main Street (historic address) |"):
            lines[i] = "| 427 Main Street (historic address) | `B-016` | `buildings/427-main.md` | `BUS-100`, `BUS-101`, `BUS-087` | `E-221`, `E-179`, `E-182` | Jan. 25, 1917 ad directly fixes 427 Main at corner Fifth for W. B. Eddy's Store and names Strebig Meat Market as former building occupant; June 8, 1922 Quality Restaurant ad prints 427 and phone 517. Business identity and physical-building continuity across dates are not assumed. |"
            changed = True
            break
    if not changed:
        raise SystemExit("427 Main address-register row not found")
    write("registers/address-register.md", "\n".join(lines) + "\n")

# Timeline narrative + YAML.
timeline_block = r'''## 25 January 1917 — T-093: W. B. Eddy's Store at 427 Main, corner Fifth; Strebig Meat Market named as former occupant
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

A visually verified *Oregon City Courier* advertisement (`S-247` / `E-221`) gives **W. B. Eddy's Store (`BUS-100`)** at its **new location, 427 Main Street, Corner 5th** and says the building was formerly occupied by the **Strebig Meat Market (`BUS-101`)**. The ad does not identify Eddy's prior room, so no move from the 1915 526 Main `BUS-032` record is asserted. The former Strebig reference is likewise not merged with 1907 `BUS-047` without an independent identity/continuity bridge. The later 1922 Quality Restaurant at 427 is a same-address anchor, not proof that the same physical building survived.'''
append_once("timeline.md", timeline_block)

db_timeline = read("database/timeline.yml")
if TIMELINE_ID not in db_timeline:
    db_timeline = db_timeline.rstrip() + r'''

  - id: T-093
    date: 25 January 1917
    summary: "W. B. Eddy's Store advertises its new location at 427 Main Street, Corner 5th; the ad says the building was formerly occupied by the Strebig Meat Market."
    confidence: "Direct/very high for dated business-address and former-occupant wording; unresolved for Eddy 1915 identity, Strebig 1907 identity, and physical-building continuity to 1922."
    related_sources: [S-247]
    related_evidence: [E-221]
    related_businesses: [BUS-100, BUS-101, BUS-032, BUS-047, BUS-087]
    related_buildings: [B-016]
''' + "\n"
    write("database/timeline.yml", db_timeline)

# Continue the 1917 audit record without overwriting earlier checkpoint text.
review_block = r'''## January 11–25 exhaustive continuation — 5 September 2026
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

`S-247` / `E-221` visually clears all **24/24 pages** of the remaining January 11, 18 and 25 *Courier* issues. With the already reviewed January 4 issue, **January Courier coverage is now 4 complete issues / 32 page images visually verified**.

The major new address control is **25 January p.6: W. B. Eddy's Store, 427 Main Street, Corner 5th**, in a building the ad says was **formerly occupied by the Strebig Meat Market**. The archive keeps the 1917 Eddy and Strebig references separate from `BUS-032` and `BUS-047` until independent identity/continuity evidence is found. Repeated 108 Fifth and 619 Main ads corroborate `E-120` as additional dated observations.

No exact 501/503/505/507/509/511 occupant was established in these 24 pages; that bounded result is not vacancy evidence. 1917 remains **IN PROGRESS** because the remainder of the annual relevant-title/page audit, the true 13 Dec p21 retrieval gap, and the Sohns & Woodbeck Oregon City directory section remain open. See `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

# Update the canonical year-status row conservatively: only claim the tracked complete-issue batches.
year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md` | Structured monthly sample plus Jan. 11/18/25 continuation now gives **15 complete tracked issues / 120 page images visually verified** in those non-overlapping batches; January itself is **4 complete issues / 32 pages**. Jan. 25 adds direct 427 Main/corner Fifth and former Strebig Meat Market evidence. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

# Add targeted identity/address research follow-up under the existing RL-043 heading.
leads = read("evidence/research-leads.md")
lead_marker = "### 5 September 2026 — 1917 Eddy/Strebig/427 continuation"
if lead_marker not in leads:
    heading = "## RL-043 — Resolve unnumbered 1915 business changes and neighboring-address transitions\n"
    if heading not in leads:
        raise SystemExit("RL-043 heading not found")
    insert = r'''

### 5 September 2026 — 1917 Eddy/Strebig/427 continuation

`E-221` / `S-247` directly places **W. B. Eddy's Store (`BUS-100`) at 427 Main, corner Fifth** on 25 January 1917 and says the building was formerly occupied by **Strebig Meat Market (`BUS-101`)**. Test two separate bridges rather than merging by name: (1) whether 1915 `BUS-032` Eddy's Dependable Store at 526 and 1917 `BUS-100` are the same business/proprietor and, if so, when/where the move occurred; (2) whether `BUS-101` is the same Strebig operation as 1907 `BUS-047` at Albright's Old Stand/Fifth-Main. Directories, intervening advertisements and exact-address move notices are preferred. The 1917/1922 shared 427 address also requires a structural/parcel continuity test before treating it as one physical building.
'''
    leads = leads.replace(heading, heading + insert, 1)
    write("evidence/research-leads.md", leads)

# Add the 1917 address control to OQ-034 without changing its Newton conclusion.
questions = read("evidence/open-questions.md")
oq_marker = "### 5 September 2026 — 1917 427 Main corner control"
if oq_marker not in questions:
    heading = "## OQ-034 — Was George Newton's saved Quality restaurant the 427 Main business?\n"
    if heading not in questions:
        raise SystemExit("OQ-034 heading not found")
    insert = r'''

### 5 September 2026 — 1917 427 Main corner control

New `E-221` / `S-247` evidence independently fixes **427 Main Street at corner Fifth** on 25 January 1917, when W. B. Eddy's Store advertised there and named Strebig Meat Market as the building's former occupant. This strengthens the address's Fifth/Main geographic control but does **not** answer whether George Newton operated the 1922 Quality Restaurant at 427, and it does not establish physical-building continuity from 1917 to 1922. Keep Newton → 427 at its existing evidence state until a proprietor/address source joins the 1922 records directly.
'''
    questions = questions.replace(heading, heading + insert, 1)
    write("evidence/open-questions.md", questions)

# Crosswalk and research log.
crosswalk = r'''## S-247 / E-221 / T-093 — January 1917 427 Main corner control
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->

| Record | Links | Notes |
| --- | --- | --- |
| `S-247` / `E-221` / `T-093` | `B-016`; `BUS-100`, `BUS-101`; identity leads `BUS-032`, `BUS-047`; later `BUS-087` | 25 Jan. 1917 p6 directly gives W. B. Eddy's Store at **427 Main Street, Corner 5th** and names Strebig Meat Market as former building occupant. No cross-period business merger or physical-building continuity is assumed. |
| `BUS-100` | `S-247`, `E-221`, `B-016`, `T-093` | W. B. Eddy's Store at 427 on 25 Jan. 1917; prior room not numbered. |
| `BUS-101` | `S-247`, `E-221`, `B-016`, `T-093` | Strebig Meat Market named only as former 427 building occupant; exact occupancy dates/proprietor unresolved. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

research_log = r'''### 2026-09-05 — resumed exhaustive 1917 Courier review with remaining January issues
<!-- 1917 January unsampled Courier visual review — 2026-09-05 -->
- Preserved and visually inspected **24/24 actual page scans** for 11, 18 and 25 January 1917 (`S-247`). Retrieval commit: `032e40d834369295984b4ab66bf9fa783adb9d73`.
- With the earlier 4 January sample, January Courier coverage is now **4 complete issues / 32 page images visually verified**.
- Major new direct finding (`E-221`): **W. B. Eddy's Store — 427 Main Street, Corner 5th** on 25 Jan. p6; same ad says the building was formerly occupied by **Strebig Meat Market**.
- Created separate `BUS-100` and `BUS-101` records rather than silently merging with 1915 `BUS-032` or 1907 `BUS-047`; identity and move/continuity bridges remain open.
- Repeated 108 Fifth and 619 Main advertisements corroborate the existing 1917 sample anchors as additional dated observations.
- No exact 501/503/505/507/509/511 occupant was established in these 24 pages. This is bounded coverage only, not vacancy/non-use evidence.
- 1917 remains **IN PROGRESS**; unreviewed annual pages/titles, true 13 Dec p21 and the Sohns & Woodbeck Oregon City directory remain open.'''
append_once("registers/research-log.md", research_log)

print("Integrated S-247 / E-221 / T-093 / BUS-100 / BUS-101")
