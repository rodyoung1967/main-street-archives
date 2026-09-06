from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "S-253"
EVIDENCE_ID = "E-227"
MARKER = "1917 March 15-29 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block):
    text = read(rel)
    if MARKER in text:
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


def entity_block(text, ident, next_prefix):
    pat = re.compile(rf"(?ms)^  - id: {re.escape(ident)}\n.*?(?=^  - id: {re.escape(next_prefix)}|\Z)")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"{ident} block not found")
    return m


def add_yaml_related(block, key, value):
    if re.search(rf"(?m)^    {re.escape(key)}: \[[^\n]*\b{re.escape(value)}\b[^\n]*\]$", block):
        return block
    inline = re.search(rf"(?m)^    {re.escape(key)}: \[(.*?)\]$", block)
    if inline:
        items = [x.strip() for x in inline.group(1).split(",") if x.strip()]
        if value not in items:
            items.append(value)
        return block[:inline.start()] + f"    {key}: [{', '.join(items)}]" + block[inline.end():]
    multi = re.search(rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:    - [^\n]+\n|      - [^\n]+\n)+)", block)
    if multi:
        items_text = multi.group("items")
        if re.search(rf"(?m)^\s+- {re.escape(value)}\s*$", items_text):
            return block
        indent = "      " if "      - " in items_text else "    "
        return block[:multi.end("items")] + f"{indent}- {value}\n" + block[multi.end("items"):]
    # Add a compact list before the next related_* key or block end.
    insert_at = len(block)
    m = re.search(r"(?m)^    related_", block)
    if m:
        insert_at = m.start()
    return block[:insert_at] + f"    {key}: [{value}]\n" + block[insert_at:]


# Hard stops on parallel ID consumption.
for rel, ident in [("evidence/source-register.md", SOURCE_ID), ("evidence/evidence-register.md", EVIDENCE_ID)]:
    text = read(rel)
    if ident in text and MARKER not in text:
        raise SystemExit(f"{ident} already appears in {rel}; stop rather than reuse/renumber")

capture = r'''# 1917 Oregon City Courier — March 15, 22 and 29 complete-issue visual review

<!-- 1917 March 15-29 Courier visual review — 2026-09-05 -->

Status: **VISUALLY VERIFIED — 3 complete issues / 28 of 28 page scans reviewed. March Courier is now complete within the retrieved weekly issue inventory; 1917 remains IN PROGRESS.**

Archive IDs: source `S-253`; evidence `E-227`.

Preserved originals: `newspapers/oregon-city-courier/1917-march-unsampled/`  
Retrieval commit: `413f0499335e7d4c21093b928038b33175bc7b6f`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-march-unsampled/manifest.json`

## Scope and method

This pass completes the remaining March weekly *Oregon City Courier* issues after the already reviewed 1 March monthly sample (`S-134` / `E-120`) and 8 March checkpoint (`S-252` / `E-226`). Every actual page scan was rendered and visually inspected page by page. Text extraction was used only after visual inspection as a checking aid.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 15 Mar. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 22 Mar. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 29 Mar. 1917 | 12 | **VISUALLY VERIFIED 12/12** |

Together with 1 March (8 pages) and 8 March (10 pages), March now has **5 complete Courier issues / 46 page images visually verified**.

Across the non-overlapping structured monthly sample plus the January, February and March continuations, the project now has **22 complete tracked 1917 Courier issues / 186 page images visually verified**. This remains a progress measure, not exhaustive annual certification.

## Major chronology refinement — Jones Drug Company at 617 Main by 15 March

Two exact-address advertisements materially improve the Jones Drug chronology:

- **15 March 1917, p.2:** **JONES DRUG CO. — 617 Main Street — JACK & ALBRIGHT**.
- **22 March 1917, p.6:** the same exact **617 Main Street** Jones Drug advertisement recurs.

This moves the earliest currently integrated exact-number Jones Drug observation from **1 November 1917** back to **15 March 1917**. It does not establish the exact move day, legal succession, lease, building ownership, or uninterrupted occupancy between March and November. The June 1916 report (`E-119`) remains future-tense/prospective evidence of an Andresen-area rearrangement rather than proof that the move had already occurred on that reporting date.

On **29 March p.9**, a large Jones Drug Company Easter advertisement prints only **MAIN STREET**, with no street number. That unnumbered ad is not used to infer 617 from same-month repetition; the exact 617 claims rest on the March 15 and March 22 scans themselves.

## Other dated address controls

These are dated observations only, not proof of uninterrupted occupancy:

- **15 Mar. p.3:** Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **15 Mar. p.5:** optometrist — **612 Main Street**.
- **15 Mar. p.7:** Electric Store — **Andresen Bldg., 619 Main St.**
- **22 Mar. p.3:** Williams Bros. Transfer & Storage — **Office 612 Main Street**; R. L. Holman — **Fifth and Main**.
- **22 Mar. p.5:** optometrist — **612 Main Street**.
- **22 Mar. p.7:** Electric Store — **Andresen Bldg., 619 Main St.**
- **29 Mar. p.4:** R. L. Holman — **Fifth and Main St.**
- **29 Mar. p.5:** Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **29 Mar. p.7:** optometrist — **612 Main Street**.
- **29 Mar. p.10:** R. L. Holman — **Fifth and Main St.**
- **29 Mar. p.11:** Electric Store — **Andresen Bldg., 619 Main St.**; R. L. Holman — **Fifth and Main St.**

## Exact target-address result

Across these **28 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this continuation.

A post-review text-layer check was run only as a backstop. It surfaced the same real 612/617/619/Fifth-Main controls and no defensible hidden target-address hit. Numeric strings in legal, tax, financial or other non-address contexts were not treated as storefront evidence.

This is bounded coverage for the three issues only. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

March *Courier* coverage is now complete within the five-issue March inventory: **5 issues / 46 pages visually verified**. 1917 remains **IN PROGRESS** because later unsampled issues and other relevant title/source-class work remain, including the known true **13 December 1917 Courier page 21** retrieval gap and the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap.
'''
create_once(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Courier, 15/22/29 March 1917 complete-page visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 28/28 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **15 March 1917 (8 pages); 22 March 1917 (8 pages); 29 March 1917 (12 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-03-15/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-march-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-march-unsampled/manifest.json`  
Retrieval commit: `413f0499335e7d4c21093b928038b33175bc7b6f`  
Related evidence/business/building: `{EVIDENCE_ID}`; `BUS-040`; `B-013`.  
Capture: `{CAPTURE_REL}`.  
Notes: 15 Mar. p2 and 22 Mar. p6 directly print Jones Drug Co. at **617 Main Street**, moving its earliest integrated exact-number observation earlier than the prior 1 Nov. sample. Selected 612 Main, 619 Main and Fifth/Main anchors recur. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; silence is not vacancy evidence.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — March 1917 continuation moves Jones Drug's exact 617 Main anchor back to 15 March and clears 28 pages
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Related building/business: `B-013` / `BUS-040`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **28 page scans** for the 15, 22 and 29 March 1917 *Oregon City Courier* issues were visually reviewed.
- With the previously reviewed 1 and 8 March issues, March now has **5 complete issues / 46 visually verified pages**.
- Across the non-overlapping monthly-sample, January, February and March-continuation batches, the project now documents **22 complete tracked issues / 186 visually verified pages**; this is not exhaustive annual coverage.
- **15 March p.2** directly advertises **Jones Drug Co., 617 Main Street, Jack & Albright**; **22 March p.6** repeats the same exact-number address.
- These scans move the earliest integrated exact-number Jones Drug observation from 1 November back to **15 March 1917**, but do not prove the exact move day, legal succession, lease, title, or uninterrupted occupancy.
- **29 March p.9** advertises Jones Drug Company at **Main Street** without a number; that unnumbered wording is preserved separately and is not used to infer 617.
- Selected direct controls repeat **612 Main**, **619 Main**, and **Fifth/Main** during the batch.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in these 28 pages. This is bounded coverage only and not vacancy, demolition or absence evidence.
Classification: **DOCUMENTED / DIRECT** for the page-review count, March 15/22 Jones Drug 617 wording, and other visible dated anchors; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected scans and printed address wording; unresolved for exact move day and physical/tenancy continuity.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if SOURCE_ID not in sources:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Courier 15/22/29 March 1917 complete-page visual-review batch"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-03-15/ed-1/"
    type: "Primary newspaper page scans; visually verified 28/28 pages"
    date: "1917-03-15 through 1917-03-29"
    repository_file: "{CAPTURE_REL}"
    notes: "March 15 p2 and March 22 p6 directly print Jones Drug Co. at 617 Main Street. March 29 p9 prints Main Street without a number. Other repeated controls include 612 Main, 619 Main and Fifth/Main. No target 501/503/505/507/509/511 or new 427 Main occupant was established."
    related_evidence: [{EVIDENCE_ID}]
    related_businesses: [BUS-040]
    related_buildings: [B-013]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if EVIDENCE_ID not in evidence:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "March 1917 continuation moves Jones Drug exact 617 Main anchor back to 15 March and clears 28 pages"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-03-15 through 1917-03-29"
    claims:
      - "All 28 page scans for the 15, 22 and 29 March 1917 Courier issues were visually reviewed."
      - "With the 1 and 8 March issues, March now has 5 complete issues / 46 visually verified pages."
      - "The non-overlapping monthly-sample, January, February and March batches now total 22 complete tracked issues / 186 visually verified pages; this is not exhaustive annual coverage."
      - "15 March p2 directly prints Jones Drug Co. at 617 Main Street, Jack & Albright; 22 March p6 repeats the exact 617 Main address."
      - "The exact-number observation moves the integrated Jones Drug 617 anchor back from 1 November to 15 March 1917 without proving the move day, tenancy, title or continuous occupancy."
      - "29 March p9 prints Jones Drug Company at Main Street without a number and is not used to infer 617."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the 28-page batch; this is bounded coverage, not vacancy or absence evidence."
    confidence: "Very High for the inspected-page count and visible dated address wording; unresolved for exact move day and continuity."
    related_sources: [{SOURCE_ID}]
    related_businesses: [BUS-040]
    related_buildings: [B-013]
''' + "\n"
    write("database/evidence.yml", evidence)

# Update Jones Drug narrative.
jones = read("businesses/jones-drug-company.md")
if MARKER not in jones:
    old = "A June 1916 report described a prospective Jones Drug Company move into a former Portland Railway Light & Power / Schilling room during Andresen Building rearrangements (`E-119`). A visually verified 1 November 1917 advertisement directly places **Jones Drug Company at 617 Main Street** (`E-120`)."
    new = "A June 1916 report described a prospective Jones Drug Company move into a former Portland Railway Light & Power / Schilling room during Andresen Building rearrangements (`E-119`). Visually verified advertisements now directly place **Jones Drug Company at 617 Main Street by 15 March 1917**, repeat the exact address on **22 March 1917** (`E-227` / `S-253`), and repeat 617 again on **1 November 1917** (`E-120`)."
    if old not in jones:
        raise SystemExit("Expected Jones Drug chronology paragraph not found")
    jones = jones.replace(old, new, 1)
    jones = jones.replace("Sources: `S-133`, `S-134`.", "Sources: `S-133`, `S-253`, `S-134`.\n\n<!-- " + MARKER + " -->", 1)
    write("businesses/jones-drug-company.md", jones)

# Update 617 address narrative.
b617 = read("buildings/617-main-beaver-building.md")
if MARKER not in b617:
    b617 = b617.replace("- Related evidence: `E-109`, `E-116`, `E-119`, `E-120`", "- Related evidence: `E-109`, `E-116`, `E-119`, `E-120`, `E-227`", 1)
    b617 = b617.replace("- Related sources: `S-121`, `S-130`, `S-133`, `S-134`", "- Related sources: `S-121`, `S-130`, `S-133`, `S-134`, `S-253`", 1)
    b617 = b617.replace("By 1 November 1917, Jones Drug Company directly advertised at 617 Main.", "By **15 March 1917**, Jones Drug Company directly advertised at **617 Main**; the exact-number advertisement recurs on **22 March**, with another exact 617 advertisement on 1 November. The 29 March Jones Drug advertisement says only Main Street and is not used to infer the number.", 1)
    b617 += "\n<!-- " + MARKER + " -->\n"
    write("buildings/617-main-beaver-building.md", b617)

# Business index BUS-040 row.
bidx = read("businesses/business-index.md")
if EVIDENCE_ID not in bidx:
    lines = bidx.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| BUS-040 |"):
            lines[i] = "| BUS-040 | [Jones Drug Company](jones-drug-company.md) | 617 Main by 15 Mar. 1917; Andresen-area move prospect in June 1916 | March 15 and 22 exact-address ads (`E-227`/`S-253`) move the integrated 617 anchor earlier than the Nov. 1 sample (`E-120`); exact move day, tenancy and one-room succession unresolved. |"
            break
    else:
        raise SystemExit("BUS-040 business-index row not found")
    write("businesses/business-index.md", "\n".join(lines) + "\n")

# database/businesses BUS-040 block.
businesses = read("database/businesses.yml")
m = re.search(r"(?ms)^  - id: BUS-040\n.*?(?=^  - id: BUS-|\Z)", businesses)
if not m:
    raise SystemExit("BUS-040 database block not found")
block = m.group(0)
if EVIDENCE_ID not in block:
    block = re.sub(r"(?m)^    address:.*$", "    address: 617 Main by 15 March 1917; Andresen Building move prospect in 1916", block, count=1)
    block = re.sub(r"(?m)^    notes:.*$", "    notes: March 15 and 22 1917 exact-address ads directly place Jones Drug Company at 617 Main; Nov 1 repeats it. June 1916 remains prospective move evidence. Exact move day, lease, succession and continuity unresolved.", block, count=1)
    block = add_yaml_related(block, "related_evidence", EVIDENCE_ID)
    block = add_yaml_related(block, "related_sources", SOURCE_ID)
    businesses = businesses[:m.start()] + block + businesses[m.end():]
    write("database/businesses.yml", businesses)

# database/buildings B-013 block.
buildings = read("database/buildings.yml")
m = re.search(r"(?ms)^  - id: B-013\n.*?(?=^  - id: B-|\Z)", buildings)
if not m:
    raise SystemExit("B-013 database block not found")
block = m.group(0)
if EVIDENCE_ID not in block:
    block = re.sub(r"(?m)^    notes:.*$", "    notes: Electric Store and Schilling optometry are dated 1915–1916 occupants; Jones Drug Company is directly at 617 Main by 15 March 1917 and again 22 March / 1 November. The 29 March Jones ad is Main Street only. Shared-room arrangement, ownership, building continuity and exact transition dates unresolved.", block, count=1)
    block = add_yaml_related(block, "related_evidence", EVIDENCE_ID)
    block = add_yaml_related(block, "related_sources", SOURCE_ID)
    buildings = buildings[:m.start()] + block + buildings[m.end():]
    write("database/buildings.yml", buildings)

# Address register exact row.
addr = read("registers/address-register.md")
if EVIDENCE_ID not in addr:
    lines = addr.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| 617 Main Street, Oregon City, Oregon (Beaver Building address) |"):
            lines[i] = "| 617 Main Street, Oregon City, Oregon (Beaver Building address) | `B-013` | `buildings/617-main-beaver-building.md` | `BUS-031`, `BUS-037`, `BUS-040` | `E-109`, `E-119`, `E-120`, `E-227` | Jones Drug is now directly at **617 Main by 15 March 1917** and again 22 March / 1 November. Earlier 1915–16 occupants remain separately dated; do not infer one-room succession, exact move day, building ownership or continuous occupancy. |"
            break
    else:
        raise SystemExit("617 Main address-register row not found")
    write("registers/address-register.md", "\n".join(lines) + "\n")

# Timeline narrative: append a bounded refinement under the existing 1917 section by marker.
timeline = read("timeline.md")
if MARKER not in timeline:
    heading = "## 1917 — selected 108 Fifth, 519, 617 and 619 Main anchors\n"
    if heading not in timeline:
        raise SystemExit("1917 selected-anchor timeline heading not found")
    insert = f'''\n### March continuation refinement\n<!-- {MARKER} -->\n\n`{EVIDENCE_ID}` / `{SOURCE_ID}` moves the earliest integrated exact-number **Jones Drug Company (`BUS-040`) at 617 Main** observation back from the 1 November sample to **15 March 1917**, repeated on **22 March**. The 29 March Jones Drug ad prints only Main Street. These are dated observations; they do not prove the exact move day, lease, uninterrupted occupancy or a single physical room/building succession. March is now **5 complete Courier issues / 46 visually verified pages**; the non-overlapping tracked 1917 count is **22 issues / 186 pages**, still IN PROGRESS.\n'''
    timeline = timeline.replace(heading, heading + insert, 1)
    write("timeline.md", timeline)

# Synchronize T-032 in database/timeline.yml.
dbt = read("database/timeline.yml")
m = re.search(r"(?ms)^  - id: T-032\n.*?(?=^  - id: T-|\Z)", dbt)
if not m:
    raise SystemExit("T-032 block not found")
block = m.group(0)
if EVIDENCE_ID not in block:
    block = re.sub(r"(?m)^    summary:.*$", "    summary: Sample and March continuation directly repeat Scripture & May at 108 Fifth, Electric Store at 619 Main, Theroux at 519 Main and Jones Drug at 617 Main; Jones is exact at 617 by 15 March 1917 and again 22 March / 1 November. These are dated observations, not uninterrupted occupancy.", block, count=1)
    block = add_yaml_related(block, "related_evidence", EVIDENCE_ID)
    block = add_yaml_related(block, "related_sources", SOURCE_ID)
    dbt = dbt[:m.start()] + block + dbt[m.end():]
    write("database/timeline.yml", dbt)

# Business timeline audit note.
btl = f'''## March 1917 Jones Drug exact-address refinement\n<!-- {MARKER} -->\n\n| Date | Address | Business | ID | Evidence | Limit |\n| --- | --- | --- | --- | --- | --- |\n| 15 Mar. 1917 | 617 Main | Jones Drug Co. | `BUS-040` | `{EVIDENCE_ID}` / `{SOURCE_ID}` | Direct ad; moves earliest integrated exact-number observation earlier than 1 Nov. Exact move day/tenancy/continuity unresolved. |\n| 22 Mar. 1917 | 617 Main | Jones Drug Co. | `BUS-040` | `{EVIDENCE_ID}` / `{SOURCE_ID}` | Direct repeated ad; dated observation only. |'''
append_once("registers/business-timeline.md", btl)

review_block = f'''## March 15–29 continuation — 5 September 2026\n<!-- {MARKER} -->\n\n`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **28/28 pages** of the remaining 15, 22 and 29 March *Courier* issues. Together with the already reviewed March 1 and March 8 issues, **March Courier coverage is now 5 complete issues / 46 pages visually verified**.\n\nThe major chronology refinement is **Jones Drug Co. at 617 Main on 15 March p.2 and 22 March p.6**, moving the earliest integrated exact-number Jones observation earlier than the prior 1 November sample. The 29 March p.9 Jones ad says Main Street only and is not used to infer a number. Repeated 612 Main, 619 Main and Fifth/Main controls remain dated observations only.\n\nNo exact 501/503/505/507/509/511 or new 427 Main occupant was established. Across the non-overlapping monthly sample plus January–March continuations, the documented progress count is now **22 complete tracked issues / 186 visually verified pages**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## March completion added 5 September 2026\n<!-- {MARKER} -->\n\n`{SOURCE_ID}` / `{EVIDENCE_ID}` completes visual review of the remaining March 15/22/29 *Courier* issues (**28/28 pages**). With March 1 and 8, March is now **5 complete issues / 46 pages visually verified**. The non-overlapping monthly-sample + January + February + March batches total **22 complete tracked issues / 186 visually verified pages**. Jones Drug is directly at 617 Main by 15 March and again 22 March; this refines a neighboring address chronology but does not resolve 501/503/505. This remains partial annual coverage, not closeout certification. The 13 December true-page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

# Update year status.
year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md` | Structured monthly sample plus January–March continuations now give **22 complete tracked issues / 186 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February **4 / 36**; March **5 / 46**. Jones Drug is directly at 617 Main by 15 March and again 22 March; Jan. 25 supplies 427 Main/corner Fifth. No batch so far establishes an exact 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk = f'''## {SOURCE_ID} / {EVIDENCE_ID} — remaining March 1917 visual review and Jones Drug 617 refinement\n<!-- {MARKER} -->\n\n| Record | Links | Notes |\n| --- | --- | --- |\n| `{SOURCE_ID}` / `{EVIDENCE_ID}` | `BUS-040`; `B-013`; `T-032`; 1917 annual audit | 15/22/29 March batch, **28/28 pages visually reviewed**. Jones Drug directly at **617 Main** on 15 and 22 March; 29 March says Main Street only. No exact 501/503/505/507/509/511 or new 427 occupant; no continuity/vacancy inference. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

log = f'''### 2026-09-05 — completed remaining March 1917 Courier visual review\n<!-- {MARKER} -->\n- Synced against current `main` after parallel ownership work; `{SOURCE_ID}` / `{EVIDENCE_ID}` were free at integration start and the script hard-stops on collision.\n- Visually inspected **28/28 actual page scans** for 15, 22 and 29 March 1917; source batch retrieval commit `413f0499335e7d4c21093b928038b33175bc7b6f`.\n- March is now **5 complete issues / 46 visually verified pages** including the March 1 sample and March 8 checkpoint.\n- Major direct refinement: Jones Drug Co. **617 Main Street** on 15 Mar. p2 and 22 Mar. p6. This moves the earliest integrated exact-number Jones anchor earlier than Nov. 1; exact move day, tenancy and physical succession remain unresolved.\n- 29 Mar. p9 says only Main Street; no number was backfilled from other dates.\n- Repeated controls include **612 Main**, **619 Main**, and **Fifth/Main**.\n- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in these 28 pages. This is bounded coverage only, not vacancy/non-use evidence.\n- Non-overlapping tracked 1917 progress is now **22 complete issues / 186 visually verified page images**. 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log)

print("Integrated S-253 / E-227 remaining March 1917 review")
