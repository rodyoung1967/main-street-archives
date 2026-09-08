#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 September Enterprise visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 September Enterprise visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-september-enterprise-visual-review-2026-09-07.md"
SOURCE_NAME = "September 1919 Oregon City Enterprise complete online visual-review batch with Banner-Courier gap"
EVIDENCE_NAME = "September 1919 visual review: Fesznecker shop move just south of post office and bounded target coverage"


def read(path): return Path(path).read_text(encoding="utf-8")
def write(path,text): Path(path).write_text(text,encoding="utf-8")
def append_once(path, marker, block):
    p=Path(path); text=p.read_text(encoding="utf-8")
    if marker in text: return False
    if not text.endswith("\n"): text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text,encoding="utf-8"); return True

def next_id(path,prefix):
    nums=[int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums: raise RuntimeError(f"No {prefix} ids in {path}")
    return f"{prefix}-{max(nums)+1:03d}"

if Path(CAPTURE).exists():
    print("September capture already exists; refusing duplicate integration.")
    sys.exit(0)

S=next_id("evidence/source-register.md","S")
E=next_id("evidence/evidence-register.md","E")
P=next_id("people/people-index.md","P")
BUS=next_id("businesses/business-index.md","BUS")

capture=f'''# September 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **ONLINE-EXPOSED PAGES VISUALLY VERIFIED — 32/32 recovered September Enterprise pages inspected from original scans; Banner-Courier manual retrieval gap remains.**  
Annual status: **1919 IN PROGRESS**. January–September online-exposed local-newspaper visual coverage: **476 pages**.

Archive IDs: source `{S}`; evidence `{E}`; person `{P}`; business `{BUS}`.

## Scope

| Title | Issues reviewed | Pages | Status |
| --- | --- | ---: | --- |
| *Oregon City Enterprise* | 5, 12, 19, 26 Sep. 1919 | **32/32** | All four online-exposed September issues visually reviewed |
| *The Banner-Courier* | 4, 11, 18, 25 Sep. 1919 | **0** | **RETRIEVAL GAP — manual microfilm (`MF-030`)** |
| **Online visual total** | **4 issues** | **32/32** | Banner-Courier gap excluded from visual count |

Preserved originals / manifests:
- `newspapers/oregon-city-enterprise/1919-september/`
- `newspapers/banner-courier/1919-september/manifest.json`

Retrieval commit: `d630baf` (`Archive September 1919 Oregon City newspaper scans and gap manifest`).

All 32 recovered Enterprise pages were visually checked for printed publication/date/page identity before text-assisted discovery. No substituted-page, duplicate-page, or printed-date defect was found in the recovered Enterprise set.

## New direct spatial/business finding — 12 September p.2

The original **12 Sep. 1919 Enterprise p.2** scan visibly states:

> **S. Fesznecker has moved his tin and repair shop from Broadway to the building just south of the post office.**

This is **DOCUMENTED / DIRECT** evidence for a business move and relative location. The source does **not** print a formal trade name, exact street, street number, parcel, building owner, lease terms, or legal lot. `S. Fesznecker tin and repair shop` is therefore an archive descriptive label only.

The post-office landmark is independently established by April 1919 evidence (`S-292` / `E-266`) as the new Oregon City Post Office quarters at Fifth and Main, in two combined store rooms. The September wording therefore creates a useful relative-location anchor near that post office, but it is not normalized to any numbered Main or Fifth address.

### Relationship to the cleaner/dyer spatial control

Existing `S-152` / `E-136` directly prints the unnamed cleaner/dyer in July–early September at **`500 Fifth and Main streets`**, **`two doors south of new post office`**, Phone 260. The Fesznecker item one week later says **`the building just south of the post office`**.

Together these are a **spatial comparison lead**, not proof that the two businesses occupied adjacent numbered storefronts, not proof of a one-door/two-door sequence, and not proof that either occupied 501/503/505. `just south` is less exact than `two doors south`, and the cleaner's unusual `500 Fifth and Main streets` wording remains unresolved.

## Theroux Music House — 210 Seventh Street through 26 September

The **12 Sep. p7** and **26 Sep. p7** scans visibly print **Theroux Music House, 210 Seventh St.** The OCR derivative misreads the leading `2` as `1` (`110 Seventh`), but the original scan clearly reads **210**. This directly extends the dated Theroux address control through **26 September 1919** without proving the exact date of the earlier move from 519 Main.

## Farr Brothers — continuing business appearances without a 505 bridge

September Enterprise material continues Farr Brothers appearances, including market-report provider wording. These items do not print an exact premises or identify Edwin/Alice Farr as proprietors. No connection is created to Farr's Pool Hall at 505 Main solely from the shared surname/business wording.

## Target frontage — 501 / 503 / 505 Main

Across all **32 visually reviewed Enterprise pages** plus the post-visual discovery pass:
- no source-explicit **501 Main** occupant was recovered;
- no source-explicit **503 Main** occupant was recovered;
- no source-explicit **505 Main / 505½ Main** occupant was recovered;
- no source-explicit **507 / 507½ / 509 / 511 Main** target-neighbor occurrence was recovered;
- no target-specific construction, demolition, rebuilding, remodeling, fire, sale, lease or ownership event was recovered.

This is **bounded September Enterprise coverage only**. It does not establish vacancy, closure, non-use, demolition, or absence of an occupant, and it cannot be projected across the inaccessible September Banner-Courier issues.

## Banner-Courier retrieval gap

Direct probing reconfirmed that **4, 11, 18 and 25 September 1919 Banner-Courier issues are not exposed at the tested Historic Oregon Newspapers PDF route**. Institutional holdings confirm the title in this period on microfilm. The gap remains under existing `MF-030`; no new manual ID is created.

## Cross-record propagation audit

Updated: source/evidence registers and YAML; new Fesznecker person/business records; post-office spatial-anchor captures; cleaner/post-office comparison lead; Theroux chronology; business timeline; master timeline; address register; research leads; ID crosswalk; 1919 construction checkpoint; Banner-Courier access checkpoint; year-status; archive index; historical-society supplement; and research log.

Reviewed but deliberately **not** changed: 501/503/505 building histories, ownership timeline, Wheel/Kwality/Farr-pool-hall relations, and cleaner evidence `E-136`. September does not establish a numbered target occupant or target structural/ownership event.

## Next chronological step

Continue with **October 1919 Enterprise** online scans while preserving October Banner-Courier dates under `MF-030`.
'''
write(CAPTURE,capture)

append_once("evidence/source-register.md",MARKER,f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans plus retrieval-gap manifest; **32/32 online-exposed pages VISUALLY VERIFIED** 7 September 2026.  
Coverage: Enterprise 5/12/19/26 Sep., 32 pages; Banner-Courier 4/11/18/25 Sep. **manual retrieval gaps** under `MF-030`.  
Repository originals: `newspapers/oregon-city-enterprise/1919-september/`; gap manifest `newspapers/banner-courier/1919-september/manifest.json`.  
Related evidence: `{E}`.  
Notes: 12 Sep. p2 directly reports S. Fesznecker moving his tin and repair shop from Broadway to the building just south of the post office. No exact 501/503/505/505½ occupant or target structural event was established.''')

append_once("evidence/evidence-register.md",MARKER,f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper online scan batch with explicit successor-title retrieval gap.  
Sources: `{S}`; related post-office evidence `E-266`; related cleaner evidence `E-136`.  
Claims:
- all **32/32 online-exposed September Enterprise pages** were visually inspected after printed title/date/page identity review;
- **12 Sep. p2** directly states that **S. Fesznecker moved his tin and repair shop from Broadway to the building just south of the post office**;
- this is a relative-location/business-move fact only; no exact street number, parcel, formal trade name or building ownership is printed;
- the finding can be compared with the already verified cleaner/dyer wording `two doors south of new post office`, but does not prove exact storefront adjacency or a target-number identity;
- Theroux Music House is visibly **210 Seventh Street** through 26 Sep.; OCR `110` is a misreading;
- no source-explicit 501/503/505/505½ occupant or target construction/property event was established in the online pages;
- September Banner-Courier issues remain manual retrieval gaps under `MF-030`.
Confidence: **Very High** for scan-visible wording and page coverage; **RETRIEVAL GAP** for inaccessible Banner-Courier issues; none for an unprinted numbered target address.''')

append_once("database/sources.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary September scan batch: 32/32 Enterprise pages visually verified. Banner-Courier 4, 11, 18 and 25 September remain MF-030 manual retrieval gaps. The 12 September p2 scan directly reports S. Fesznecker moving his tin and repair shop from Broadway to the building just south of the post office.\n''')
append_once("database/evidence.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper online scan batch with explicit manual retrieval gap\n    claims:\n      - 32/32 online-exposed September 1919 Enterprise pages visually verified.\n      - S. Fesznecker moved his tin and repair shop from Broadway to the building just south of the post office by 12 September 1919.\n      - No exact street number, parcel, formal trade name or building ownership was printed for the Fesznecker shop.\n      - Theroux Music House continued at 210 Seventh Street through 26 September; OCR 110 is incorrect.\n      - No source-explicit 501, 503, 505 or 505-half Main occupant or target physical-building event was established.\n      - Banner-Courier 4, 11, 18 and 25 September remain manual microfilm retrieval gaps under MF-030.\n    confidence: Very High for visible online pages; retrieval gap for inaccessible Banner-Courier issues\n    related_sources: [{S}]\n    related_evidence: [E-136, E-266]\n    related_businesses: [{BUS}, BUS-029]\n    related_people: [{P}, P-044]\n    related_buildings: []\n    sources: [{S}]\n''')

append_once("people/people-index.md",MARKER,f'''| {P} | [S. Fesznecker](profiles/s-fesznecker.md) | Tin and repair shop operator | 12 Sep. 1919 Enterprise directly reports a move from Broadway to the building just south of the post office. Given name, exact address, ownership/tenancy and later chronology unresolved. `{E}`. |\n{MARKER}''')
append_once("businesses/business-index.md",MARKER,f'''| {BUS} | [S. Fesznecker tin and repair shop](s-fesznecker-tin-repair.md) | Broadway earlier; building just south of post office by 12 Sep. 1919; exact number unresolved | Descriptive archive label, not a proved formal trade name. Direct move wording `{E}`; no 501/503/505 assignment. |\n{MARKER}''')

write("people/profiles/s-fesznecker.md",f'''# S. Fesznecker

ID: `{P}`  
Role: tin and repair shop operator  
Related business: `{BUS}`  
Related evidence: `{E}` / source `{S}`

## 12 September 1919 direct record

The visually verified *Oregon City Enterprise*, 12 Sep. 1919, p.2 directly reports that **S. Fesznecker moved his tin and repair shop from Broadway to the building just south of the post office**.

The source supplies only the initial `S.`. Do not expand the given name without independent evidence. It does not print a street number, property owner, lease, formal business name or relationship to 501/503/505.
''')
write("businesses/s-fesznecker-tin-repair.md",f'''# S. Fesznecker tin and repair shop

ID: `{BUS}`  
Operator: `{P}`  
Archive label: descriptive only; formal trade name unknown  
Related evidence: `{E}` / source `{S}`

## Location chronology

- Before 12 Sep. 1919: **Broadway**, exact address unresolved.
- By 12 Sep. 1919: **the building just south of the post office**, exact street/number/parcel unresolved.

This relative-location wording is direct. It may be compared with the cleaner/dyer's separately verified `two doors south of new post office` wording (`E-136`) but does not prove numbered-storefront adjacency or a 501/503/505 identity.
''')

append_once("database/people.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {P}\n    name: S. Fesznecker\n    role: Tin and repair shop operator\n    notes: >-\n      12 September 1919 Enterprise directly reports a move from Broadway to the building just south of the post office. Given name, exact street number, tenancy and later chronology unresolved.\n    related_businesses: [{BUS}]\n    related_evidence: [{E}]\n    related_sources: [{S}]\n    repository_file: people/profiles/s-fesznecker.md\n''')
append_once("database/businesses.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {BUS}\n    name: S. Fesznecker tin and repair shop\n    address: Broadway earlier; building just south of post office by 12 Sep. 1919; exact number unresolved\n    notes: >-\n      Descriptive archive label only; formal trade name unknown. The 12 September Enterprise directly reports the move but does not print a numbered address, parcel or building owner. No 501/503/505 assignment.\n    related_people: [{P}]\n    related_evidence: [{E}]\n    related_sources: [{S}]\n    repository_file: businesses/s-fesznecker-tin-repair.md\n''')

append_once("businesses/ff-theroux.md",MARKER,f'''## September 1919 — 210 Seventh Street continuation and OCR correction
{MARKER}

The visually verified **12 and 26 September 1919 Enterprise p7** advertisements (`{S}` / `{E}`) print **Theroux Music House, 210 Seventh St.** OCR reads `110`, but the original scans clearly show **210**. This extends the dated address control through 26 September without proving the exact prior move date from 519 Main.
''')
append_once("people/profiles/ff-theroux.md",MARKER,f'''## September 1919 address continuation
{MARKER}

`{S}` / `{E}` directly continues Theroux Music House at **210 Seventh Street through 26 September 1919**. OCR `110` is rejected after scan inspection.
''')
append_once("evidence/source-captures/1918-1922-post-office-east-main-fifth-sixth-anchor.md",MARKER,f'''## September 1919 — Fesznecker relative-location anchor
{MARKER}

The visually verified **12 Sep. 1919 Enterprise p2** (`{S}` / `{E}`) reports that **S. Fesznecker moved his tin and repair shop from Broadway to the building just south of the post office**. The article prints no exact street number. Compare cautiously with cleaner/dyer `E-136`, which says `two doors south of new post office`; the two expressions create a useful spatial lead but do not prove exact numbered storefront adjacency.
''')
append_once("evidence/source-captures/1918-post-office-east-side-main-fifth-sixth-latourette.md",MARKER,f'''## September 1919 relative-location corroboration
{MARKER}

`{S}` / `{E}` adds a direct post-move neighborhood anchor: S. Fesznecker's tin and repair shop moved from Broadway to **the building just south of the post office** by 12 Sep. 1919. No number/parcel is printed and the item does not resolve the 1918/1919 post-office ownership-description conflict.
''')
append_once("evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md",MARKER,f'''## September 1919 comparison lead — Fesznecker
{MARKER}

A separate visually verified 12 Sep. 1919 item (`{S}` / `{E}`) says S. Fesznecker moved his tin and repair shop to **the building just south of the post office**. This can be compared with the cleaner's `two doors south of new post office` wording, but does not identify the cleaner, normalize `500 Fifth and Main streets`, or prove a one-door/two-door numbered storefront sequence.
''')
append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md",MARKER,f'''## September 1919 monthly visual addition
{MARKER}

The complete online-exposed September Enterprise pass (`{S}` / `{E}`) visually reviewed **32/32 pages**. It found no source-explicit target-frontage construction, demolition, rebuilding or remodeling event and no exact 501/503/505 occupant. The new Fesznecker move is a relative post-office neighborhood anchor only, not a target-building assignment. Banner-Courier remains unavailable online under `MF-030`.
''')
append_once("evidence/source-captures/1919-1920-banner-courier-ocr-discovery.md",MARKER,f'''## September 1919 monthly reconfirmation
{MARKER}

The September workflow recovered and visually reviewed all **32 Enterprise pages** but again found no online Banner-Courier pages for **4/11/18/25 Sep. 1919**. The existing institutional microfilm route and `MF-030` remain controlling. Retrieval gap, not negative evidence.
''')
append_once("evidence/research-leads.md",MARKER,f'''## September 1919 — identify S. Fesznecker and the post-office-south storefront
{MARKER}

Direct source `{S}` / `{E}` places **S. Fesznecker's tin and repair shop** in the **building just south of the post office** by 12 Sep. 1919 after a move from Broadway. Next online/manual targets: identify Fesznecker's full name; locate directory/telephone/classified listings; test whether a numbered address is recoverable; and compare the location carefully with cleaner/dyer `E-136` (`two doors south`). Do not assign 501/503/505 or infer exact adjacency without an independent address/parcel bridge.
''')
append_once("registers/business-timeline.md",MARKER,f'''| 12 Sep. 1919 | Building just south of Oregon City Post Office; exact number unresolved | S. Fesznecker tin and repair shop | `{BUS}` | `{E}` | Direct move from Broadway; descriptive business label only. |\n| 26 Sep. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | Scan visibly reads 210; OCR 110 rejected. |\n{MARKER}''')
append_once("registers/address-register.md",MARKER,f'''## September 1919 relative-location anchor south of Post Office
{MARKER}

`{E}` directly places `{BUS}` in **the building just south of the post office** on 12 Sep. 1919 after a move from Broadway. Exact street number/parcel is unresolved; no 501/503/505 normalization. Compare cautiously with cleaner/dyer `E-136` (`two doors south of new post office`).
''')
append_once("timeline.md",MARKER,f'''## 12 September 1919 — tin/repair shop moves just south of Post Office
{MARKER}

The *Oregon City Enterprise* p.2 (`{S}` / `{E}`) directly reports that **S. Fesznecker (`{P}`) moved his tin and repair shop (`{BUS}`) from Broadway to the building just south of the post office**. Exact street number, parcel and formal trade name remain unresolved. This is a neighborhood spatial/business-move event, not a 501/503/505 assignment.
''')
append_once("indexes/id-crosswalk.md",MARKER,f'''| {S} | {E} | {P} | {BUS} | — | 12 Sep. 1919 Enterprise p2: Fesznecker tin/repair shop move from Broadway to building just south of Post Office |\n{MARKER}''')
append_once("records/historical-society/503-505-main-historical-society-research-supplement-2026-08-24.md",MARKER,f'''## September 1919 Post Office neighborhood refinement
{MARKER}

A visually verified 12 Sep. 1919 Enterprise item (`{S}` / `{E}`) says **S. Fesznecker moved his tin and repair shop from Broadway to the building just south of the post office**. This adds a second relative-location control near the April 1919 Fifth/Main post office and the cleaner/dyer's `two doors south` wording, but it does not establish an exact numbered storefront or connect the shop to 501/503/505.
''')
append_once("ARCHIVE_INDEX.md",MARKER,f'''## 1919 September monthly visual checkpoint
{MARKER}

- **1919 remains IN PROGRESS.**
- September Enterprise: **32/32 online-exposed pages visually verified**; January–September cumulative online local-newspaper visual count **476 pages**.
- Banner-Courier 4/11/18/25 Sep. remains `MF-030` manual microfilm gap.
- New direct spatial lead: 12 Sep. p2 places S. Fesznecker's tin/repair shop in the building just south of the Post Office after moving from Broadway; exact number unresolved.
- No source-explicit 501/503/505/505½ occupant or target physical-building event established in September Enterprise.
- Full review: `{CAPTURE}`.
- Next chronological batch: **October 1919 Enterprise**.
''')
append_once("registers/research-log.md",MARKER,f'''## 7 September 2026 — September 1919 monthly scan-first review
{MARKER}

- Preserved retrieval commit `d630baf`; visually inspected **32/32** Enterprise pages for 5/12/19/26 Sep. 1919.
- Printed title/date/page sequences coherent; no source-association defect found.
- Direct new finding: 12 Sep. p2 — S. Fesznecker moved tin/repair shop from Broadway to building just south of Post Office (`{S}` / `{E}`, `{P}`, `{BUS}`).
- Theroux p7 ads visibly read **210 Seventh**, correcting OCR `110`.
- No exact 501/503/505/505½ occupant or target structural/ownership event recovered; bounded coverage only.
- Banner-Courier 4/11/18/25 Sep. remains `MF-030` retrieval/manual gap.
''')

# Conservatively update canonical 1919 year row while preserving existing blockers.
ys=read("registers/year-status.md"); lines=ys.splitlines(); found=False
for i,line in enumerate(lines):
    if line.startswith("| 1919 |"):
        parts=line.split("|")
        while len(parts)<6: parts.append("")
        sources=parts[3].strip()
        if CAPTURE not in sources:
            sources=f"`{CAPTURE}`; " + sources
        blockers=parts[4].strip()
        note=("September Enterprise 32/32 visually verified; Jan-Sep cumulative online local-newspaper visual count 476 pages. "
              "Banner-Courier 17 Jul. onward remains MF-030 manual microfilm gap; Oct-Dec Enterprise still pending. "
              "12 Sep. adds Fesznecker shop just south of Post Office; no exact target-number assignment.")
        if note not in blockers:
            blockers=(blockers + " " + note).strip()
        lines[i]=f"| 1919 | **IN PROGRESS** | {sources} | {blockers} |"
        found=True; break
if not found: raise RuntimeError("1919 year-status row not found")
write("registers/year-status.md","\n".join(lines)+"\n")

print(f"Integrated September 1919 online batch as {S} / {E}; new {P} / {BUS}")
