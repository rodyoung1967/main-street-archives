#!/usr/bin/env python3
from pathlib import Path
import re
import sys

MARKER = "<!-- 1919 January Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 January Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md"

def read(path):
    return Path(path).read_text(encoding="utf-8")

def write(path, text):
    Path(path).write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text, encoding="utf-8")
    return True

def next_id(path, prefix, pattern=None):
    text = read(path)
    pat = pattern or rf"\b{re.escape(prefix)}-(\d+)\b"
    nums = [int(x) for x in re.findall(pat, text)]
    if not nums:
        raise RuntimeError(f"No {prefix} IDs found in {path}")
    return f"{prefix}-{max(nums)+1:03d}"

def ensure_absent(id_):
    for path in [
        "evidence/source-register.md", "evidence/evidence-register.md",
        "businesses/business-index.md", "people/people-index.md",
        "database/sources.yml", "database/evidence.yml",
        "database/businesses.yml", "database/people.yml",
    ]:
        if Path(path).exists() and re.search(rf"\b{re.escape(id_)}\b", read(path)):
            raise RuntimeError(f"Allocated ID already present: {id_} in {path}")

if Path(CAPTURE).exists():
    print("January 1919 capture already exists; refusing duplicate integration.")
    sys.exit(0)

S = next_id("evidence/source-register.md", "S")
E = next_id("evidence/evidence-register.md", "E")
BUS = next_id("businesses/business-index.md", "BUS")
PERS = next_id("database/people.yml", "P", r"(?m)^\s*- id: P-(\d+)\s*$")

for id_ in (S, E, BUS, PERS):
    ensure_absent(id_)

capture = f"""# January 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 70/70 recovered January pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. This monthly batch does not certify the year.

Archive IDs: source `{S}`; evidence `{E}`; Ohio Painless Dentists / Ohio Dentists `{BUS}`; Dr. J. G. Nash `{PERS}`.

## Scope and source inventory

The January 1919 annual-standard pass covered both relevant local titles then publishing online:

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Enterprise* | 3, 10, 17, 24, 31 Jan. 1919 | **40/40** |
| *Oregon City Courier* | 2, 9, 16, 23, 30 Jan. 1919 | **30/30** |
| **January total** | **10 issues** | **70/70** |

Preserved originals:
- `newspapers/oregon-city-enterprise/1919-january/`
- `newspapers/oregon-city-courier/1919-january/`

Each repository directory contains the recovered page PDFs and a retrieval manifest. The original batch was preserved by commit `e67fd0189e034b5484afc8c19d36bfa07582b78d`.

## Scan identity audit

Every recovered page was visually checked for printed issue identity and printed page number before OCR-assisted discovery.

- Enterprise issues on 3/10/17/24/31 Jan. visibly carry the intended issue date and pages 1–8.
- Courier issues on 2/9/16/23 Jan. visibly carry the intended issue date and pages 1–6.
- **30 Jan. Courier source typo:** page 1 correctly prints **Thursday, January 30, 1919**. Interior pages 2–6 visibly print **January 30, 1918** in the running header even though they belong to the same 30 Jan. 1919 issue. Contemporary issue content and the page sequence support a printed running-header year error, **not a substituted-page inference**. The source error is preserved rather than silently corrected.

## Direct January findings

### Ohio Painless Dentists / Ohio Dentists — 507½ Main over Harding's Drug Store

The original scans directly show the upstairs dental office at **507½ Main Street** with the relational wording **over Harding's Drug Store**:

- **2 Jan. Courier p. 3:** `Ohio Painless Dentists`, `507½ Main Street`, Oregon City, and `Over Harding's Drug Store`. The visible panel does not name Nash.
- **10 Jan. Enterprise p. 2:** `OHIO DENTISTS`, **Dr. J. G. Nash, Manager**, Phone 62, `507½ Main Street over Hardings Drug Store`.
- **17 Jan. Enterprise p. 6:** repeats **Dr. J. G. Nash**, Phone 62, **507½ Main Street over Hardings Drug Store**.
- **31 Jan. Enterprise p. 6:** repeats **Dr. J. G. Nash**, Phone 62, **507½ Main Street over Harding's Drug Store**.

Classification:
- the dental office at **507½ Main** is **DOCUMENTED / DIRECT**;
- Nash as manager on 10/17/31 Jan. is **DOCUMENTED / DIRECT**;
- the ads directly establish that the 507½ office was described as being over Harding's Drug Store;
- because the ads do **not** print `507 Main` for Harding itself, Harding Drug Store at ground-floor **507** remains a **STRONG SPATIAL/ADDRESS INFERENCE**, not a source-explicit exact-number fact.

This moves the known 507½-over-Harding configuration back from the previously integrated March 1921 Freeze evidence to **2 January 1919**. It narrows the interval after Harding's direct 511 Main advertising in 1911–1916. It does **not** prove a construction date, ownership, tenancy terms, or physical continuity of any surviving building.

### Pantorium Cleaners — 500 Main

The **2 Jan. 1919 Courier p. 3** scan directly prints:

- **Pantorium Cleaners**
- **500 Main Street**
- clothes called for and delivered;
- made-to-order clothing.

The enlarged original confirms **500**, not 510. This extends the already visually verified Pantorium **500 Main** anchor of 24 Oct. 1918 through **2 Jan. 1919**. The January ad does not print the 1918 phone number and does not establish operator identity or property ownership.

The direct address sequence is therefore:
1. 12 Feb. 1914 — 416 Main;
2. 24 Oct. 1918 — 500 Main;
3. **2 Jan. 1919 — 500 Main**;
4. Jan./Jun. 1922 — business active, recovered sources do not print an address;
5. 20 Jul. 1922 — 519 Main.

The 500→519 move date remains unresolved.

## Target-frontage result: 501 / 503 / 505

Across the 70 visually reviewed January pages and the post-visual OCR/discovery pass:

- no defensible source-explicit **501 Main** occupant was found;
- no defensible source-explicit **503 Main** occupant was found;
- no defensible source-explicit **505 Main** occupant was found;
- no January Wolf & Miller advertisement or article was found that can extend the verified 1918 exact-address run;
- no target-specific demolition, rebuilding, remodeling, construction, lease, sale, move, or vacancy event was found.

OCR numeric collisions such as monetary/account figures containing `503` or `505` were rejected as non-address context.

**These are bounded January source-coverage results only. They are not evidence that 501, 503, or 505 was vacant, unused, closed, demolished, or without an occupant.**

## Other rejected / bounded candidates

- January public-health/influenza material temporarily closes categories including pool rooms/billiard rooms/card rooms citywide. No recovered wording ties the order to a target address or operator, so no 501/503/505 business event is created.
- `C. E. Miller` appears in county expenditure material. No independent identifier bridges that person to Gilbert Miller (`P-046`); no merge is made.
- Holman & Pace funeral-parlor wording appears in January, but recovered January pages do not print 501 or Fifth/Main. Existing business continuity is not converted into exact 501 occupancy.

## Construction-date interpretation

The City survey's `c.1919` estimate for surviving 503 remains a secondary historic-inventory estimate. January's 507½/Harding configuration is useful neighboring-frontage evidence, but it does **not** establish when 503 or 505 was built, rebuilt, altered, or replaced.

## Cross-Record Propagation Audit

Propagated:
- source/evidence registers and YAML;
- new Ohio Dentists business and J. G. Nash person records;
- Harding Drug Store / 507½ spatial chronology;
- Pantorium 500 Main chronology;
- business/address timelines, crosswalk, annual-status register, research leads, research log, archive index, and master timeline.

Not propagated as building events for 501/503/505:
- January target no-hits;
- general influenza closure;
- unbridged Miller references.

Reason: none establishes a new target occupant, vacancy, ownership, or physical-building event.

## Next chronological step

Continue the annual-standard scan-first pass with **February 1919 Oregon City Enterprise and Oregon City Courier**, preserving every retrievable original page, visually checking printed issue date/page identity before OCR discovery, then integrating verified findings.

1919 remains **IN PROGRESS**.
"""
write(CAPTURE, capture)

source_block = f"""
## {S} — January 1919 Oregon City Enterprise + Courier complete monthly visual-review batch
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: *Oregon City Enterprise* 3/10/17/24/31 Jan. 1919, 40 pages; *Oregon City Courier* 2/9/16/23/30 Jan. 1919, 30 pages; **70/70 January pages**.  
Repository originals: `newspapers/oregon-city-enterprise/1919-january/` and `newspapers/oregon-city-courier/1919-january/`.  
Related evidence: `{E}`.  
Notes: Direct findings include Ohio Dentists at **507½ Main over Harding's Drug Store** and Pantorium Cleaners at **500 Main**. No source-explicit January 501/503/505 occupant or target construction event was found; this is bounded coverage only. Courier 30 Jan. pp.2–6 contain a printed `1918` running-header year error within the genuine 1919 issue.
"""
append_once("evidence/source-register.md", MARKER, source_block)

evidence_block = f"""
## {E} — January 1919 Enterprise/Courier visual review: 507½ Harding relation and Pantorium 500
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **70/70** recovered January 1919 pages across the five Enterprise and five Courier issues were visually inspected after printed date/page identity review;
- 2 Jan. Courier p3 directly places **Ohio Painless Dentists at 507½ Main Street, over Harding's Drug Store**;
- 10/17/31 Jan. Enterprise ads repeat **Ohio Dentists**, **Dr. J. G. Nash, Manager**, Phone 62, at **507½ Main Street over Harding's Drug Store**;
- the relation supports Harding-at-ground-floor-507 only as a **STRONG SPATIAL/ADDRESS INFERENCE** because no January ad prints `507 Main` for Harding itself;
- 2 Jan. Courier p3 directly places **Pantorium Cleaners at 500 Main Street**, extending its 24 Oct. 1918 exact-address anchor;
- no defensible source-explicit January occupant for **501/503/505 Main** and no target construction/demolition/remodel event was found; no-hit is bounded coverage, not absence/vacancy evidence;
- 30 Jan. Courier interior pp.2–6 visibly carry a mistaken `January 30, 1918` running header inside the genuine 1919 issue; this is preserved as a printed-source error, not page substitution.
Related business/person: `{BUS}`, `{PERS}`, `BUS-007`, `BUS-073`.  
Confidence: **Very High** for scan-visible wording and January page coverage; **Strong inference only** for Harding's exact ground-floor number.
"""
append_once("evidence/evidence-register.md", MARKER, evidence_block)

business_page = f"""# Ohio Painless Dentists / Ohio Dentists — 507½ Main, January 1919

Business ID: `{BUS}`. Related person: Dr. J. G. Nash (`{PERS}`). Related evidence/source: `{E}` / `{S}`.

## Direct January 1919 evidence

The January 1919 scan-first review directly verifies this dental office at **507½ Main Street, Oregon City**:

- **2 Jan. Courier p3:** `Ohio Painless Dentists`, `507½ Main Street`, `Over Harding's Drug Store`; Nash is not named in the visible panel.
- **10 Jan. Enterprise p2:** `OHIO DENTISTS`, **Dr. J. G. Nash, Manager**, Phone 62, `507½ Main Street over Hardings Drug Store`.
- **17 Jan. Enterprise p6:** same manager, phone and 507½-over-Harding wording.
- **31 Jan. Enterprise p6:** same manager, phone and 507½-over-Harding wording.

## Interpretation limits

The office's exact **507½** address and the published relational wording over Harding's Drug Store are direct facts. The lower-floor exact number for Harding is **not** printed in these ads. Do not turn this into direct `Harding Drug Store = 507 Main` evidence, a lease, building ownership, or construction-date claim.

The January sequence moves the known 507½-over-Harding arrangement back to **2 January 1919**, earlier than the previously integrated March 1921 Freeze sequence.

Full monthly review: [{CAPTURE}](../{CAPTURE}).
"""
write("businesses/ohio-painless-dentists.md", business_page)

person_page = f"""# Dr. J. G. Nash

Person ID: `{PERS}`. Related business: Ohio Painless Dentists / Ohio Dentists (`{BUS}`). Related source/evidence: `{S}` / `{E}`.

## Direct 1919 role

Visually verified *Oregon City Enterprise* advertisements on **10, 17, and 31 January 1919** name **Dr. J. G. Nash** as **Manager** of Ohio Dentists, Phone 62, at **507½ Main Street over Harding's Drug Store**.

The 2 January *Courier* advertisement directly establishes the same dental business/location but does not visibly name Nash.

This supports a documented business-management role and advertised office location. It does not establish property ownership, tenancy terms, professional partnership structure, or any relationship to the owners of the building or Harding Drug Store beyond the printed relative-location wording.

Full review: [{CAPTURE}](../../{CAPTURE}).
"""
write("people/profiles/j-g-nash.md", person_page)

business_index_block = f"""
## January 1919 entity promotion
{MARKER}

| ID | Business | Address / location | Notes |
| --- | --- | --- | --- |
| {BUS} | [Ohio Painless Dentists / Ohio Dentists](ohio-painless-dentists.md) | **507½ Main** | Direct 2/10/17/31 Jan. 1919 advertisements; `{PERS}` J. G. Nash named manager on 10/17/31; wording says over Harding's Drug Store. Harding's lower exact number is not printed. `{E}` / `{S}`. |
"""
append_once("businesses/business-index.md", MARKER, business_index_block)

people_index_block = f"""
## January 1919 entity promotion
{MARKER}

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| {PERS} | [Dr. J. G. Nash](profiles/j-g-nash.md) | Manager, Ohio Dentists | Directly named in 10/17/31 Jan. 1919 ads at 507½ Main over Harding's Drug Store; no property-ownership inference. `{E}` / `{S}`. |
"""
append_once("people/people-index.md", MARKER, people_index_block)

sources_yaml = f"""
  - id: {S}
    name: "January 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"
    url: https://oregonnews.uoregon.edu/
    notes: >-
      Primary newspaper scan batch, visually verified 7 September 2026: 40/40 Enterprise pages
      (3/10/17/24/31 Jan.) plus 30/30 Courier pages (2/9/16/23/30 Jan.), 70/70 total.
      Originals are preserved under newspapers/oregon-city-enterprise/1919-january/ and
      newspapers/oregon-city-courier/1919-january/. Direct findings include Ohio Dentists
      at 507½ Main over Harding's Drug Store and Pantorium Cleaners at 500 Main.
      No source-explicit January 501/503/505 occupant was found; bounded coverage only.
"""
append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + "\n" + sources_yaml)

evidence_yaml = f"""
  - id: {E}
    name: "January 1919 Enterprise/Courier visual review: 507½ Harding relation and Pantorium 500"
    type: Primary newspaper scan batch
    confidence: Very High for scan-visible wording; strong inference only for Harding exact ground-floor number
    claims:
      - 70/70 recovered January 1919 newspaper pages visually verified.
      - Ohio Dentists directly at 507½ Main over Harding Drug Store; Pantorium Cleaners directly at 500 Main.
    related_sources: [{S}]
    sources: [{S}]
    notes: >-
      70/70 recovered January pages visually inspected. Ohio Painless Dentists / Ohio Dentists
      is directly at 507½ Main over Harding's Drug Store on 2/10/17/31 January; Dr. J. G. Nash
      is directly named manager on 10/17/31. Harding's exact lower-floor 507 number remains a
      strong spatial inference because the ads do not print it. Pantorium Cleaners is directly
      at 500 Main on 2 January. No source-explicit 501/503/505 occupant or target construction
      event was found; no-hit is coverage only. Courier 30 Jan pp2-6 contain a printed 1918
      running-header typo within the genuine 1919 issue.
"""
append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + "\n" + evidence_yaml)

business_yaml = f"""
  - id: {BUS}
    name: Ohio Painless Dentists / Ohio Dentists
    repository_file: businesses/ohio-painless-dentists.md
    address: 507 1/2 Main
    notes: >-
      Visually verified advertisements on 2/10/17/31 Jan 1919 place the dental office at
      507½ Main over Harding's Drug Store. Dr. J. G. Nash is named manager on 10/17/31.
      The lower-floor exact number for Harding is not printed; do not convert the relation
      into direct Harding-at-507 proof, property ownership, or construction evidence.
    related_people: [{PERS}]
    related_evidence: [{E}]
    related_sources: [{S}]
"""
append_once("database/businesses.yml", YAML_MARKER, YAML_MARKER + "\n" + business_yaml)

person_yaml = f"""
  - id: {PERS}
    name: Dr. J. G. Nash
    repository_file: people/profiles/j-g-nash.md
    role: Manager, Ohio Dentists
    notes: >-
      Visually verified 10/17/31 Jan 1919 advertisements name Dr. J. G. Nash as manager,
      Phone 62, at 507½ Main over Harding's Drug Store. The 2 Jan ad establishes the same
      office/location but does not visibly name Nash.
    related_businesses: [{BUS}]
    related_evidence: [{E}]
    related_sources: [{S}]
"""
append_once("database/people.yml", YAML_MARKER, YAML_MARKER + "\n" + person_yaml)

harding_update = f"""
## January 1919 507½-over-Harding bridge
{MARKER}

`{E}` / `{S}` materially moves the known 507½-over-Harding configuration earlier than the March 1921 Freeze sequence. Direct scans on **2, 10, 17 and 31 January 1919** place Ohio Painless Dentists / Ohio Dentists (`{BUS}`) at **507½ Main Street** and explicitly describe the office as **over Harding's Drug Store**; 10/17/31 name Dr. J. G. Nash (`{PERS}`) as manager.

This is direct evidence for the upstairs **507½** address and its published relationship to Harding's store. It is **not** a direct advertisement saying `Harding Drug Store, 507 Main`. Harding-at-ground-floor-507 therefore remains a **STRONG SPATIAL/ADDRESS INFERENCE**. The direct 511 Main controls from 1911–1916 remain intact, and the exact move date to the later 507-area arrangement remains unresolved.
"""
append_once("businesses/harding-drug-store.md", MARKER, harding_update)

pantorium_update = f"""
## 2 January 1919 — Pantorium still at 500 Main
{MARKER}

`{E}` / `{S}` visually verifies a **2 Jan. 1919 Courier p3** advertisement reading **Pantorium Cleaners — 500 Main Street**. An enlarged scan confirms **500**, not 510. This extends the direct 500 Main run from the previously verified 24 Oct. 1918 classified through 2 Jan. 1919.

The ad does not print the 1918 phone number and does not resolve operator ownership. The direct address chronology is now **416 Main (1914) → 500 Main (24 Oct. 1918 and 2 Jan. 1919) → 519 Main by 20 Jul. 1922**, with the move date still unresolved.
"""
append_once("evidence/source-captures/pantorium-cleaners-address-chronology-1914-1922.md", MARKER, pantorium_update)

harding_building_update = f"""
## January 1919 upstairs-office / Harding relation
{MARKER}

`{E}` / `{S}` directly places Ohio Dentists (`{BUS}`) at **507½ Main** on 2/10/17/31 Jan. 1919 with the repeated wording **over Harding's Drug Store**. This is an important pre-1921 spatial anchor for the historic 507-area business row. It does not directly print Harding's ground-floor number and does not prove the physical identity, construction date, ownership or later survival of the building. Treat Harding-at-507 as a **strong spatial inference**, not direct exact-address evidence.
"""
append_once("buildings/507-harding-building.md", MARKER, harding_building_update)

timeline_block = f"""
## January 1919 — complete local-newspaper monthly visual batch
{MARKER}

A scan-first review of **70/70 January pages** across the *Oregon City Enterprise* and *Oregon City Courier* (`{S}` / `{E}`) directly places **Ohio Painless Dentists / Ohio Dentists at 507½ Main over Harding's Drug Store** on 2/10/17/31 Jan.; Dr. J. G. Nash (`{PERS}`) is named manager on 10/17/31. This pushes the known 507½-over-Harding arrangement back to **2 Jan. 1919**, while Harding's exact lower-floor number remains an inference rather than direct wording. The same 2 Jan. Courier page directly keeps **Pantorium Cleaners at 500 Main**. No defensible source-explicit January occupant for **501, 503 or 505 Main** and no target construction event was found; no-hit is bounded coverage only. The 30 Jan. Courier pp2–6 running header mistakenly prints 1918 inside the genuine 1919 issue.
"""
append_once("timeline.md", MARKER, timeline_block)

bt_block = f"""
## January 1919 verified business/address controls
{MARKER}

| Date span | Address | Business / person | Evidence | Confidence / limit |
| --- | --- | --- | --- | --- |
| 2/10/17/31 Jan. 1919 | **507½ Main** | Ohio Painless Dentists / Ohio Dentists (`{BUS}`); Dr. J. G. Nash (`{PERS}`) manager on 10/17/31 | `{E}` / `{S}` | Direct for dental office/manager and `over Harding's Drug Store`; Harding ground-floor 507 remains strong inference, not direct. |
| 2 Jan. 1919 | **500 Main** | Pantorium Cleaners (`BUS-073`) | `{E}` / `{S}` | Direct; extends 24 Oct. 1918 exact-address anchor; move to 519 remains unresolved. |
"""
append_once("registers/business-timeline.md", MARKER, bt_block)

address_block = f"""
## January 1919 address controls
{MARKER}

| Address | Date | Directly documented use | Evidence / limit |
| --- | --- | --- | --- |
| **500 Main** | 2 Jan. 1919 | Pantorium Cleaners | `{E}` / `{S}`; visually verified `500`, not 510. |
| **507½ Main** | 2/10/17/31 Jan. 1919 | Ohio Painless Dentists / Ohio Dentists; J. G. Nash manager on 10/17/31 | `{E}` / `{S}`; direct upstairs address and `over Harding's Drug Store`; Harding's lower exact number is not printed. |
"""
append_once("registers/address-register.md", MARKER, address_block)

openq_block = f"""
## January 1919 Harding / target-frontage refinement
{MARKER}

`{E}` / `{S}` moves the direct **507½ Main over Harding's Drug Store** relationship back to **2 Jan. 1919**, but still does not print Harding's lower-floor exact number. The open Harding-address question is narrowed: determine when the directly documented **511 Main** drug-store address of 1911–1916 changed to the later 507-area configuration and locate an independent source that explicitly prints Harding at 507.

The same complete January batch found no source-explicit occupant at 501/503/505 and no target construction event. This does **not** answer the occupancy or c.1919/c.1920 construction questions; it records January coverage only.
"""
append_once("evidence/open-questions.md", MARKER, openq_block)

lead_block = f"""
## 7 September 2026 — January 1919 Harding address-transition lead
{MARKER}

`{E}` / `{S}` directly places Ohio Dentists at **507½ Main over Harding's Drug Store** on 2/10/17/31 Jan. 1919, moving that spatial relationship more than two years earlier than the prior March 1921 Freeze bridge. Search **after the last direct 511 Main Harding controls in 1916 and through 2 Jan. 1919** for a directory, Harding advertisement, lease, building notice or street-number listing that explicitly identifies the drug store's lower-floor number. Keep `507` as a strong inference until such a source is found.

Continue 1919 chronologically. The January 70-page no-hit for exact 501/503/505 is bounded coverage, not evidence of vacancy or non-use.
"""
append_once("evidence/research-leads.md", MARKER, lead_block)

crosswalk_block = f"""
## {S} / {E} — January 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` → `{BUS}` / `{PERS}`: Ohio Painless Dentists / Ohio Dentists, 507½ Main; J. G. Nash manager on 10/17/31 Jan.; direct `over Harding's Drug Store` wording.
- `{S}` / `{E}` → `BUS-007` / `B-003`: pushes the 507½-over-Harding spatial configuration back to 2 Jan. 1919; lower `507 Main` for Harding remains **STRONG INFERENCE**, not direct.
- `{S}` / `{E}` → `BUS-073`: Pantorium Cleaners directly at **500 Main** on 2 Jan. 1919.
- No 501/503/505 building event is created from the January no-hit.
"""
append_once("indexes/id-crosswalk.md", MARKER, crosswalk_block)

log_block = f"""
| 2026-09-07 | Completed January 1919 Enterprise + Courier scan-first visual audit | **70/70 pages**: Enterprise 40/40 (3/10/17/24/31 Jan.) + Courier 30/30 (2/9/16/23/30 Jan.). Directly verified Ohio Dentists at 507½ Main over Harding's Drug Store and Pantorium Cleaners at 500 Main; created `{S}` / `{E}` / `{BUS}` / `{PERS}`. No exact 501/503/505 occupant or target construction event; bounded coverage only. 30 Jan Courier pp2–6 preserve a printed 1918 running-header typo in the genuine 1919 issue. 1919 remains IN PROGRESS; next chronological batch February. |
{MARKER}
"""
append_once("registers/research-log.md", MARKER, log_block)

archive_block = f"""
## 1919 January complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- January local-newspaper coverage is **70/70 visually verified pages**: Enterprise 40/40 and Courier 30/30 (`{S}` / `{E}`).
- Direct January controls: Ohio Dentists (`{BUS}`) at **507½ Main over Harding's Drug Store**, Dr. J. G. Nash (`{PERS}`) manager on 10/17/31 Jan.; Pantorium Cleaners at **500 Main** on 2 Jan.
- No source-explicit 501/503/505 occupant or target construction event; no-hit is bounded coverage only.
- 30 Jan Courier interior running headers print 1918 inside the genuine 1919 issue; source typo documented.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological online batch: **February 1919 Enterprise + Courier**.
"""
append_once("ARCHIVE_INDEX.md", MARKER, archive_block)

ys = read("registers/year-status.md")
if "| 1919 |" not in ys:
    lines = ys.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("| 1918 |"):
            insert_at = i + 1
            break
    if insert_at is None:
        raise RuntimeError("Could not locate 1918 year-status row")
    row = (
        f"| 1919 | **IN PROGRESS** | `{CAPTURE}`; "
        "`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | "
        f"January monthly scan-first batch **70/70 visually verified pages**: Enterprise 40/40 + Courier 30/30 (`{S}`/`{E}`). "
        "Direct 507½-over-Harding and Pantorium 500 controls; no exact 501/503/505 occupant or target construction event. "
        "February–December annual visual work and other online source classes remain; Banner-Courier from July 1919 has a documented manual microfilm gap. |"
    )
    lines.insert(insert_at, row)
    write("registers/year-status.md", "\n".join(lines) + "\n")

if Path("businesses/pantorium-cleaners.md").exists():
    append_once("businesses/pantorium-cleaners.md", MARKER, pantorium_update)

print(f"Integrated January 1919 as {S} / {E}; new business {BUS}; new person {PERS}")
