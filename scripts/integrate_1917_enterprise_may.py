from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise May visual closeout — 2026-09-06"
CAPTURE_REL = "evidence/source-captures/1917-enterprise-may-04-25-visual-review-2026-09-06.md"
MANIFEST_REL = "newspapers/oregon-city-enterprise/1917-may/manifest.json"
BUILDING_REL = "buildings/106-fifth.md"
FARR_BUS_REL = "businesses/farr-brothers-store.md"
FARR_CLARIFICATION_REL = "evidence/source-captures/1922-farr-brothers-identity-clarification-2026-09-03.md"
WS_EDDY_REL = "people/profiles/w-s-eddy.md"
FASHION_REL = "businesses/fashion-stable.md"
CLARENCE_REL = "people/profiles/clarence-p-farr.md"


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


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"Expected text not found in {rel}: {old[:100]!r}")
    write(rel, text.replace(old, new, 1))
    return True


def regex_replace_once(rel, pattern, repl):
    text = read(rel)
    new, n = re.subn(pattern, repl, text, count=1, flags=re.M)
    if n == 0:
        raise SystemExit(f"Pattern not found in {rel}: {pattern}")
    write(rel, new)
    return True


def add_yaml_list_item_to_entity(rel, entity_id, field, value):
    text = read(rel)
    pat = re.compile(rf"(?ms)(^  - id: {re.escape(entity_id)}\n.*?)(?=^  - id: |\Z)")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Entity {entity_id} not found in {rel}")
    block = m.group(1)
    if re.search(rf"(?m)^    - {re.escape(value)}$", block) or re.search(rf"(?m)^    {re.escape(field)}: \[.*\b{re.escape(value)}\b.*\]$", block):
        return False
    field_pat = re.compile(rf"(?ms)(^    {re.escape(field)}:\n)((?:    - .*\n)*)")
    fm = field_pat.search(block)
    if fm:
        new_block = block[:fm.end()] + f"    - {value}\n" + block[fm.end():]
    else:
        # Insert before repository_file when available, otherwise at end of entity block.
        pos = re.search(r"(?m)^    repository_file:", block)
        ins = f"    {field}:\n    - {value}\n"
        if pos:
            new_block = block[:pos.start()] + ins + block[pos.start():]
        else:
            new_block = block.rstrip("\n") + "\n" + ins
    write(rel, text[:m.start()] + new_block + text[m.end():])
    return True


def add_yaml_related_scalar_list(rel, entity_id, field, value):
    # Alias retained for readability.
    return add_yaml_list_item_to_entity(rel, entity_id, field, value)


if not (ROOT / MANIFEST_REL).exists():
    raise SystemExit(f"Required May manifest missing: {MANIFEST_REL}")

RETRIEVAL_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()
if not RETRIEVAL_COMMIT:
    raise SystemExit("Could not determine May retrieval commit")

# Allocate IDs from the live synchronized checkout.
source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
buildings_yml = read("database/buildings.yml")
business_index = read("businesses/business-index.md")
timeline_yml = read("database/timeline.yml")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
building_nums = [int(x) for x in re.findall(r"(?m)^  - id: B-(\d{3})\b", buildings_yml)]
business_nums = [int(x) for x in re.findall(r"\| BUS-(\d{3}) \|", business_index)]
timeline_nums = [int(x) for x in re.findall(r"(?m)^  - id: T-(\d{3})\b", timeline_yml)]
if not all((source_nums, evidence_nums, building_nums, business_nums, timeline_nums)):
    raise SystemExit("Could not determine current ID maxima")
SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"
BUILDING_ID = f"B-{max(building_nums)+1:03d}"
FARR_BUS_ID = f"BUS-{max(business_nums)+1:03d}"
TIMELINE_ID = f"T-{max(timeline_nums)+1:03d}"

# Idempotent recovery if a prior run got as far as writing the May capture.
if (ROOT / CAPTURE_REL).exists():
    cap = read(CAPTURE_REL)
    pats = {
        "source": r"source `(S-\d{3})`",
        "evidence": r"evidence `(E-\d{3})`",
        "building": r"building `(B-\d{3})`",
        "Farr business": r"Farr business `(BUS-\d{3})`",
        "timeline": r"timeline `(T-\d{3})`",
    }
    vals = {}
    for label, pat in pats.items():
        m = re.search(pat, cap)
        if not m:
            raise SystemExit(f"Existing May capture lacks recoverable {label} ID")
        vals[label] = m.group(1)
    SOURCE_ID = vals["source"]
    EVIDENCE_ID = vals["evidence"]
    BUILDING_ID = vals["building"]
    FARR_BUS_ID = vals["Farr business"]
    TIMELINE_ID = vals["timeline"]

capture = f'''# 1917 Oregon City Enterprise — May 4, 11, 18 and 25 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 32/32 genuine intended-date pages across all four May issues. May monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; building `{BUILDING_ID}`; Farr business `{FARR_BUS_ID}`; timeline `{TIMELINE_ID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-may/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Manifest: `{MANIFEST_REL}`

## Scope and page-identity audit

The archive exposes four May Friday issue buckets, eight page PDFs each: **4, 11, 18 and 25 May 1917**. All **32/32 actual page scans** were rendered and visually inspected. Printed dates and printed page numbers were separately checked because March and April exposed source-association defects.

| Issue date | Exposed pages | Genuine intended-date pages | Status |
| --- | ---: | ---: | --- |
| 4 May 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 11 May 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 18 May 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 25 May 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |

No May misassociated page, duplicate printed page, or page-level retrieval gap was found. OCR/text extraction was used only after the scan-first pass to locate small-print candidates for enlarged reinspection.

Enterprise cumulative genuine intended-date coverage therefore advances from **136 through April to 168 through May**. Two earlier Enterprise page-level retrieval gaps remain (true 16 March p5 and true 13 April p8). **246 exposed June-December slots remain** in the Friday-pattern inventory, with final title-calendar reconciliation still required.

## Direct May findings

### 25 May p.8 — exact 106 Fifth Street enlistment use

The article **“OPPORTUNITY IS OPEN FOR ABLE-BODIED MEN TO ESCAPE DRAFT LAW”** discusses Oregon National Guard units being brought to war strength and directly states that **“enlistments are being received at 106 Fifth street.”**

This is the first currently integrated direct exact-address use observation sufficient to establish a stable **106 Fifth Street** address/building record (`{BUILDING_ID}`). It proves a dated **National Guard enlistment/recruiting location** on 25 May 1917. It does **not** identify the property owner, ordinary tenant, exact room, parcel, footprint, construction date, building fabric, or duration of the recruiting use.

The prior repository entity audit deliberately declined to invent a 106 Fifth record because no direct exact-address use had then been recovered. That historical audit decision remains preserved, but this new primary evidence supersedes its factual premise for **106 Fifth only**. It does not establish 102 or 104 Fifth.

### W. S. Eddy / Fashion Stable through 25 May

Professional-directory advertisements on **4, 11, 18 and 25 May p.7** directly repeat **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the already integrated April observation (`E-252` / `S-279`) through **25 May 1917**.

The exact move date from the 1915 Fifth-between-Main-and-Water wording remains unresolved. Do not assign Fashion Stable to 427 Main, 110 Fifth, 106 Fifth, or any other number. Do not merge W. S. Eddy (`P-396`) with W. B. Eddy / W. B. Eddy's Store (`BUS-100`).

### 25 May p.6 — Farr Brothers Meat market

The market-price column directly states that its prices are supplied by the **Brady Mercantile Company and Farr Brothers Meat market**. This is direct 1917 business-type evidence for **Farr Brothers as a meat-market business**, but the item prints **no street address and no individual proprietor names**.

Combined with the already preserved 1922 primary descriptions of Farr Brothers as **Grocers, Butchers** and Oregon City's official historic-resource identification of the **Farr Brothers Store** at 919 7th associated with Louis and Clarence Farr, the business now has enough multi-date and identity-conflict significance to receive stable business record `{FARR_BUS_ID}`. The 1917 page itself does **not** prove that the May 1917 meat market was already at 919 7th or that Clarence/Louis personally authored or operated the quoted market report.

This business remains strictly separate from **Edwin F. Farr / Alice Farr / Farr's Pool Hall (`BUS-013`) at 505 Main**. The surname and later official family context are not a bridge to 505.

### Other contextual references

- 18 May p.6 includes **Jones Drug Co.** in county expenditures, but prints no exact 617 Main address; existing exact March/November controls remain stronger for its address chronology.
- 25 May material references Harding Drug Company and other downtown actors without a new exact target address.
- Numeric strings resembling 501/503/505/507/509/511 in financial/statistical contexts were rejected as address evidence.

## Target-frontage result

Across the **32 genuine May pages**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established, and no new exact **427 Main** occupant was established.

This is a bounded coverage result only. It is not evidence of vacancy, non-use, demolition, absence of a storefront, or absence of an unadvertised occupant.

## Cross-record propagation audit

Reviewed against this batch: the 501/503/505 building and unified timeline records, 427 Main and W. B. Eddy controls, Fifth Street building/address register, W. S. Eddy/Fashion Stable person/business records, Farr/Farr's Pool Hall/Clarence Farr identity controls, master and business timelines, open questions, research leads, year status, source/evidence registers, YAML sidecars, crosswalk and archive index.

**Propagation decisions:**
- create exact-address record `{BUILDING_ID}` for **106 Fifth** because the new scan directly establishes a dated use there;
- extend `P-396` / `BUS-103` Fashion Stable chronology through 25 May 1917 without assigning a number;
- create separate business `{FARR_BUS_ID}` for **Farr Brothers Store / Meat Market** because the business now has direct multi-date primary business-type evidence plus official identity/location context;
- preserve Clarence P. Farr as an official cross-source identity context, while not claiming that the 25 May article names him individually;
- do **not** create or alter a 1917 501/503/505 occupancy event because May establishes none;
- keep all Farr and Eddy no-merge guards intact.

## Effect on 1917 status

1917 remains **IN PROGRESS**. May itself is closed as a complete monthly Enterprise scan batch (**32/32**). Enterprise now has **168 genuine intended-date pages visually verified through May**, the two previously documented March/April retrieval gaps, and **246 exposed June-December slots** still requiring visual review. Courier, Sohns & Woodbeck directory, title-calendar reconciliation, other online source classes and manual closeout work remain separate blockers.
'''
if not (ROOT / CAPTURE_REL).exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Enterprise, May 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **32/32 genuine intended-date pages visually verified**.  
Publication: *Oregon City Enterprise*  
Issue dates: **4, 11, 18 and 25 May 1917**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-05-25/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-may/`  
Manifest: `{MANIFEST_REL}`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: May is complete 32/32 with no page-association gap. 25 May p8 directly places National Guard enlistments at 106 Fifth; p6 directly calls Farr Brothers a Meat market; repeated p7 ads extend W. S. Eddy/Fashion Stable on Main between Fourth/Fifth through 25 May. No exact 501/503/505/507/509/511 or new 427 Main occupant was established.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — May 1917 Enterprise completes 32-page batch, establishes 106 Fifth enlistment use, and strengthens Farr Brothers identity
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper visual review  
Claims:
- All **32 May page scans** for 4/11/18/25 May were visually inspected and match their intended issue dates/page identities; May has no new retrieval gap.
- Enterprise cumulative genuine intended-date visual coverage advances to **168 pages through May**, with **246 exposed June-December slots** remaining; the earlier 16 March p5 and 13 April p8 gaps remain.
- **25 May p.8** directly states that Oregon National Guard **enlistments are being received at 106 Fifth street**, establishing a dated exact-address recruiting/use observation at `{BUILDING_ID}`.
- Repeated **4/11/18/25 May p.7** ads continue **W. S. Eddy / Fashion Stable, between Fourth and Fifth on Main Street**, extending the verified 1917 span through 25 May without a number.
- **25 May p.6** directly calls **Farr Brothers** a **Meat market**. It prints no address or individual proprietor; later 1922 and official City evidence remain necessary for the broader Farr Brothers identity/location chronology.
- No defensible exact **501/503/505/507/509/511 Main** or new 427 Main occupant was established in May.
Classification: **DOCUMENTED / DIRECT** for May page identity, 106 Fifth wording, Fashion Stable wording and Farr Brothers business type; **COVERAGE RESULT ONLY** for the target-frontage no-hit.  
Confidence: **Very High** for visibly verified wording and counts; no vacancy, physical-building continuity, 505/Farr merge, or numbered Fashion Stable inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

# Source/evidence YAML.
sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Enterprise, May 1917 complete scan-first visual-review batch"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-05-25/ed-1/"
    type: "Primary newspaper page scans; 32/32 genuine intended-date pages visually verified"
    date: "1917-05-04 through 1917-05-25"
    repository_file: "{CAPTURE_REL}"
    notes: "May complete 32/32. Direct 106 Fifth enlistment use, W. S. Eddy/Fashion Stable continuation, and Farr Brothers Meat market wording; no exact target Main occupant."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "May 1917 Enterprise completes 32-page batch, establishes 106 Fifth enlistment use, and strengthens Farr Brothers identity"
    type: "Primary newspaper visual review"
    date: "1917-05-04 through 1917-05-25"
    claims:
      - "All 32 May page scans were visually verified with matching issue/page identities."
      - "Enterprise cumulative genuine intended-date coverage is 168 pages through May; 246 exposed June-December slots remain."
      - "25 May p8 directly states National Guard enlistments are being received at 106 Fifth street."
      - "May p7 ads extend W. S. Eddy/Fashion Stable at Main between Fourth/Fifth through 25 May."
      - "25 May p6 directly describes Farr Brothers as a Meat market, with no address or individual proprietor printed."
      - "No exact 501/503/505/507/509/511 Main or new 427 Main occupant was established in May."
    confidence: "Very High for visible wording and counts; identity/location limits retained."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

# Create the newly justified 106 Fifth address record.
if not (ROOT / BUILDING_REL).exists():
    write(BUILDING_REL, f'''# 106 Fifth Street

Building/address ID: `{BUILDING_ID}`.

## What is established

On **25 May 1917**, a visually verified *Oregon City Enterprise* article about Oregon National Guard recruiting states that **“enlistments are being received at 106 Fifth street”** (`{EVIDENCE_ID}` / `{SOURCE_ID}`).

This establishes **106 Fifth Street as a published exact-address recruiting/enlistment location on that date**.

## Limits

The source does not identify the owner, ordinary commercial tenant, exact room, parcel, building footprint, construction date, physical fabric, or duration of the recruiting use. The address observation does not prove continuity with any later or earlier structure.

Do not merge 106 Fifth with 107, 108, 109 or 110 Fifth; do not assign Fashion Stable to 106 Fifth; and do not use this civic recruiting use to infer anything about occupancy at 501/503/505 Main.

## Repository-history note

The 29 August entity audit intentionally declined to create a 106 Fifth record because the then-reviewed evidence contained no direct exact-address occupant/use observation. `{EVIDENCE_ID}` supplies that missing direct observation and supersedes that earlier **reason for omission** without deleting the historical audit record.
''')

buildings = read("database/buildings.yml")
if re.search(rf"(?m)^  - id: {re.escape(BUILDING_ID)}$", buildings) is None:
    buildings = buildings.rstrip() + f'''

  - id: {BUILDING_ID}
    name: 106 Fifth Street (historic National Guard enlistment address)
    address: 106 Fifth Street, Oregon City, Oregon
    repository_file: {BUILDING_REL}
    notes: "25 May 1917 Enterprise directly states that Oregon National Guard enlistments were being received at 106 Fifth street. Dated civic/recruiting use only; owner, ordinary tenant, parcel, footprint and physical continuity unresolved."
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/buildings.yml", buildings)

# Create the now-mature Farr Brothers business entity.
if not (ROOT / FARR_BUS_REL).exists():
    write(FARR_BUS_REL, f'''# Farr Brothers Store / Meat Market

Business ID: `{FARR_BUS_ID}`. Official identity context includes Clarence P. Farr (`P-395`); the 25 May 1917 article itself names no individual proprietor.

## Direct primary chronology

- **25 May 1917:** visually verified *Oregon City Enterprise* market-price column says prices were supplied by the **Brady Mercantile Company and Farr Brothers Meat market** (`{EVIDENCE_ID}` / `{SOURCE_ID}`). No address is printed.
- **1922:** already preserved primary merchant/labor evidence lists **Farr Brothers** separately from local pool-hall/billiards businesses and describes Farr Brothers as **Grocers, Butchers** (see `evidence/source-captures/1922-farr-brothers-identity-clarification-2026-09-03.md`).

## Official location/identity context

Oregon City's official historic-resource history for the Farr Store identifies the **Farr Brothers Store at 919 7th Street** and associates the business with **Louis and Clarence Farr**, continuing there into the mid-1940s. That official secondary source supplies the later/overall store identity and location context; the **1917 newspaper does not itself print 919 7th**.

## Critical no-merge rule

This is **not Farr's Pool Hall (`BUS-013`) at 505 Main**. Do not merge Louis/Clarence Farr's Farr Brothers grocery/meat business with Edwin F. Farr, Alice Farr, Farr's Pool Hall, Carl R. Harr, or Harr's Recreation Center merely because of the surname or the word recreation in later municipal records.

The May 1917 source does not establish the exact 1917 street address, land ownership, building ownership, or individual operators.
''')

business_index_block = f'''## May 1917 Enterprise business promotion
<!-- {MARKER} -->

| ID | Business | Address / location | Notes |
| --- | --- | --- | --- |
| {FARR_BUS_ID} | [Farr Brothers Store / Meat Market](farr-brothers-store.md) | 25 May 1917 article gives no address; official later/historic context is 919 7th | Direct May 1917 wording: **Farr Brothers Meat market**. 1922 primary sources say Grocers/Butchers; official City history associates Farr Brothers Store with Louis/Clarence Farr at 919 7th. Strictly separate from Edwin/Alice Farr and 505 Main pool hall. `{EVIDENCE_ID}` / `{SOURCE_ID}`. |'''
append_once("businesses/business-index.md", business_index_block)

businesses = read("database/businesses.yml")
if re.search(rf"(?m)^  - id: {re.escape(FARR_BUS_ID)}$", businesses) is None:
    businesses = businesses.rstrip() + f'''

  - id: {FARR_BUS_ID}
    name: Farr Brothers Store / Meat Market
    repository_file: {FARR_BUS_REL}
    address: "1917 exact address unresolved; official Farr Store history places the business at 919 7th Street"
    notes: "25 May 1917 Enterprise directly calls Farr Brothers a Meat market; 1922 primary evidence describes Grocers/Butchers; official City history associates Farr Brothers Store with Louis and Clarence Farr at 919 7th. Do not merge with Edwin/Alice Farr or Farr's Pool Hall at 505."
    related_people: [P-395]
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/businesses.yml", businesses)

# Extend existing W. S. Eddy/Fashion Stable records through May.
replace_once(
    FASHION_REL,
    "- **April 1917:** repeated ads place Fashion Stable **between Fourth and Fifth on Main Street** (`E-252` / `S-279`).",
    f"- **6 April–25 May 1917:** repeated ads place Fashion Stable **between Fourth and Fifth on Main Street** (`E-252` / `S-279`; continued `{EVIDENCE_ID}` / `{SOURCE_ID}`)."
)
append_once(FASHION_REL, f'''## May 1917 continuation
<!-- {MARKER} -->

Visually verified professional ads on 4, 11, 18 and 25 May p.7 repeat W. S. Eddy / Fashion Stable **between Fourth and Fifth on Main Street** (`{EVIDENCE_ID}` / `{SOURCE_ID}`). This extends the dated 1917 observation through **25 May** but still supplies no number.''')

replace_once(
    WS_EDDY_REL,
    "- **6–27 April 1917:** repeated visually reviewed professional ads place **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street** (`E-252` / `S-279`). No street number is printed.",
    f"- **6 April–25 May 1917:** repeated visually reviewed professional ads place **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street** (`E-252` / `S-279`; continued `{EVIDENCE_ID}` / `{SOURCE_ID}`). No street number is printed."
)
append_once(WS_EDDY_REL, f'''## May 1917 continuation
<!-- {MARKER} -->

The 4/11/18/25 May p.7 ads repeat the same name, credentials, business and relative location. The latest visually verified date in this batch is **25 May 1917** (`{EVIDENCE_ID}` / `{SOURCE_ID}`).''')

# Extend Clarence Farr context without falsely saying the 1917 page names him.
append_once(CLARENCE_REL, f'''## 1917 Farr Brothers business-type control
<!-- {MARKER} -->

`{EVIDENCE_ID}` / `{SOURCE_ID}` directly calls **Farr Brothers** a **Meat market** on 25 May 1917. The page does **not** name Clarence individually. Clarence's connection to the Farr Brothers Store comes from the independent official City identity source already cited above. Stable business `{FARR_BUS_ID}` therefore links here as cross-source identity context, not as a direct 25 May proprietor statement.''')

# Update YAML relationships for existing entities.
add_yaml_related_scalar_list("database/people.yml", "P-396", "related_evidence", EVIDENCE_ID)
add_yaml_related_scalar_list("database/people.yml", "P-396", "related_sources", SOURCE_ID)
add_yaml_related_scalar_list("database/people.yml", "P-395", "related_businesses", FARR_BUS_ID)
add_yaml_related_scalar_list("database/people.yml", "P-395", "related_evidence", EVIDENCE_ID)
add_yaml_related_scalar_list("database/people.yml", "P-395", "related_sources", SOURCE_ID)
add_yaml_related_scalar_list("database/businesses.yml", "BUS-103", "related_evidence", EVIDENCE_ID)
add_yaml_related_scalar_list("database/businesses.yml", "BUS-103", "related_sources", SOURCE_ID)

# Human-readable people index: preserve same IDs, update the current-state summaries.
people = read("people/people-index.md")
old_p396 = re.search(r"(?m)^\| P-396 \|.*$", people)
if old_p396 and EVIDENCE_ID not in old_p396.group(0):
    newline = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 notices place him/Fashion Stable on Fifth between Main/Water; April–May 1917 ads place Fashion Stable on Main between Fourth/Fifth through 25 May. Exact move date/number unresolved; not merged with W. B. Eddy. `E-252` / `S-279`; `{EVIDENCE_ID}` / `{SOURCE_ID}`. |"
    people = people[:old_p396.start()] + newline + people[old_p396.end():]
old_p395 = re.search(r"(?m)^\| P-395 \|.*$", people)
if old_p395 and FARR_BUS_ID not in old_p395.group(0):
    newline = f"| P-395 | [Clarence P. Farr](profiles/clarence-p-farr.md) | Oregon City Farr Brothers family / municipal C. P. Farr identity control | 1911 directly gives Clarence P. Farr; official City history associates Clarence with Farr Brothers Store (`{FARR_BUS_ID}`), while 25 May 1917 only names Farr Brothers Meat market and does not name him individually. Keep separate from Edwin F. Farr / 505 Main. |"
    people = people[:old_p395.start()] + newline + people[old_p395.end():]
write("people/people-index.md", people)

# Update business-index Fashion Stable row if present.
bi = read("businesses/business-index.md")
m = re.search(r"(?m)^\| BUS-103 \|.*$", bi)
if m and EVIDENCE_ID not in m.group(0):
    newline = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–25 May 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); repeated May ads extend the direct Main-block observation through 25 May. No exact number; not W. B. Eddy/427 by assumption. `E-252` / `S-279`; `{EVIDENCE_ID}` / `{SOURCE_ID}`. |"
    bi = bi[:m.start()] + newline + bi[m.end():]
    write("businesses/business-index.md", bi)

# Add exact 106 Fifth timeline record in YAML.
ty = read("database/timeline.yml")
if re.search(rf"(?m)^  - id: {re.escape(TIMELINE_ID)}$", ty) is None:
    ty = ty.rstrip() + f'''

  - id: {TIMELINE_ID}
    date: "25 May 1917"
    summary: "Oregon City Enterprise directly states that Oregon National Guard enlistments are being received at 106 Fifth Street; this is a dated recruiting/use observation, not proof of owner, ordinary tenant, parcel or building continuity."
    confidence: "Very High for exact-address published wording; physical/property relationships unresolved"
    related_evidence:
      - {EVIDENCE_ID}
    related_buildings:
      - {BUILDING_ID}
''' + "\n"
    write("database/timeline.yml", ty)

# Master timeline and business timeline.
append_once("timeline.md", f'''## 25 May 1917 — {TIMELINE_ID}: National Guard enlistments at 106 Fifth
<!-- {MARKER} -->

A visually verified *Oregon City Enterprise* article directly states that Oregon National Guard **enlistments are being received at 106 Fifth street** (`{SOURCE_ID}` / `{EVIDENCE_ID}`; `{BUILDING_ID}`). This establishes a dated exact-address civic/recruiting use. It does not identify the owner or ordinary tenant, define the footprint, or connect 106 Fifth to 501/503/505 Main.

The same May batch extends **W. S. Eddy / Fashion Stable (`P-396` / `BUS-103`) at Main between Fourth and Fifth through 25 May 1917**, and directly calls **Farr Brothers (`{FARR_BUS_ID}`) a Meat market** without an address. Farr Brothers remains separate from Edwin/Alice Farr and 505 Main.''')

# Replace the April-only row where possible, then add Farr Brothers chronology row.
bt = read("registers/business-timeline.md")n
