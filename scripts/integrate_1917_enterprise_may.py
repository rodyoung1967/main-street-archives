from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise May visual closeout — 2026-09-06"
CAPTURE = "evidence/source-captures/1917-enterprise-may-04-25-visual-review-2026-09-06.md"
MANIFEST = "newspapers/oregon-city-enterprise/1917-may/manifest.json"
BUILDING = "buildings/106-fifth.md"
FARR_BUS = "businesses/farr-brothers-store.md"
FARR_GUARD = "evidence/source-captures/1922-farr-brothers-identity-clarification-2026-09-03.md"


def r(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def w(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block, marker=MARKER):
    text = r(rel)
    if marker in text:
        return
    w(rel, text.rstrip() + "\n\n" + block.strip() + "\n")


def replace_once(rel, old, new):
    text = r(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected text missing in {rel}: {old[:120]!r}")
    w(rel, text.replace(old, new, 1))


def replace_regex(rel, pattern, repl, required=True):
    text = r(rel)
    new, n = re.subn(pattern, repl, text, count=1, flags=re.M)
    if not n:
        if required:
            raise SystemExit(f"Pattern missing in {rel}: {pattern}")
        return False
    w(rel, new)
    return True


def yaml_add(rel, entity_id, field, value):
    text = r(rel)
    m = re.search(rf"(?ms)(^  - id: {re.escape(entity_id)}\n.*?)(?=^  - id: |\Z)", text)
    if not m:
        raise SystemExit(f"{entity_id} missing from {rel}")
    block = m.group(1)
    if re.search(rf"(?m)^    - {re.escape(value)}$", block) or re.search(rf"(?m)^    {re.escape(field)}: \[.*\b{re.escape(value)}\b.*\]$", block):
        return
    fm = re.search(rf"(?ms)^    {re.escape(field)}:\n(?:    - .*\n)*", block)
    if fm:
        newblock = block[:fm.end()] + f"    - {value}\n" + block[fm.end():]
    else:
        pos = re.search(r"(?m)^    repository_file:", block)
        ins = f"    {field}:\n    - {value}\n"
        newblock = block[:pos.start()] + ins + block[pos.start():] if pos else block.rstrip() + "\n" + ins
    w(rel, text[:m.start()] + newblock + text[m.end():])


if not (ROOT / MANIFEST).exists():
    raise SystemExit("May manifest not preserved")
retrieval_commit = subprocess.check_output(["git", "log", "-1", "--format=%H", "--", MANIFEST], cwd=ROOT, text=True).strip()

# Dynamic IDs, allocated only after the workflow rebases onto live main.
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", r("evidence/source-register.md"))]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", r("evidence/evidence-register.md"))]
building_nums = [int(x) for x in re.findall(r"(?m)^  - id: B-(\d{3})\b", r("database/buildings.yml"))]
business_nums = [int(x) for x in re.findall(r"\| BUS-(\d{3}) \|", r("businesses/business-index.md"))]
timeline_nums = [int(x) for x in re.findall(r"(?m)^  - id: T-(\d{3})\b", r("database/timeline.yml"))]
if not all((source_nums, evidence_nums, building_nums, business_nums, timeline_nums)):
    raise SystemExit("Could not allocate May IDs")
SID = f"S-{max(source_nums)+1:03d}"
EID = f"E-{max(evidence_nums)+1:03d}"
BID = f"B-{max(building_nums)+1:03d}"
BUS = f"BUS-{max(business_nums)+1:03d}"
TID = f"T-{max(timeline_nums)+1:03d}"

# Recover IDs after an idempotent rerun.
if (ROOT / CAPTURE).exists():
    cap = r(CAPTURE)
    for name, pat in {
        "SID": r"source `(S-\d{3})`", "EID": r"evidence `(E-\d{3})`",
        "BID": r"building `(B-\d{3})`", "BUS": r"Farr business `(BUS-\d{3})`",
        "TID": r"timeline `(T-\d{3})`"
    }.items():
        m = re.search(pat, cap)
        if not m:
            raise SystemExit(f"Existing May capture lacks {name}")
        globals()[name] = m.group(1)

capture_text = f'''# 1917 Oregon City Enterprise — May 4, 11, 18 and 25 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 32/32 genuine intended-date pages. May monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SID}`; evidence `{EID}`; building `{BID}`; Farr business `{BUS}`; timeline `{TID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-may/`  
Retrieval commit: `{retrieval_commit}`  
Manifest: `{MANIFEST}`

## Page-identity audit

All 32 actual page scans for **4, 11, 18 and 25 May 1917** were visually inspected. Each issue has eight genuine matching-date pages, and printed page identities 1–8 were checked because the March/April runs exposed source-association defects. **No May page substitution, duplicate-page defect or retrieval gap was found.** OCR/text was used only after the scan-first pass as a candidate locator.

Enterprise cumulative genuine intended-date coverage advances from **136 through April to 168 through May**. The two earlier Enterprise gaps remain (true 16 March p5 and true 13 April p8). **246 exposed June–December slots remain**, plus final title-calendar reconciliation.

## Direct findings

### 25 May p.8 — 106 Fifth Street

The article **“OPPORTUNITY IS OPEN FOR ABLE-BODIED MEN TO ESCAPE DRAFT LAW”** states that Oregon National Guard **“enlistments are being received at 106 Fifth street.”** This is **DOCUMENTED / DIRECT** exact-address use and establishes stable address record `{BID}` for a dated recruiting/enlistment location.

It does not establish property ownership, ordinary tenancy, room, parcel, footprint, construction date, building continuity, or duration. It does not connect 106 Fifth to 501/503/505 Main. The repository's 29 August entity audit correctly withheld a 106 Fifth record when no direct use was known; this new primary evidence supersedes that old reason for omission for **106 Fifth only**.

### W. S. Eddy / Fashion Stable through 25 May

Professional ads on **4, 11, 18 and 25 May p.7** repeat **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends `P-396` / `BUS-103` from the April control through **25 May 1917**. No number is printed. Do not assign Fashion Stable to 106 Fifth, 110 Fifth, 427 Main or another number, and do not merge W. S. Eddy with W. B. Eddy.

### 25 May p.6 — Farr Brothers Meat market

The market-price column says prices are supplied by the **Brady Mercantile Company and Farr Brothers Meat market**. That is direct 1917 business-type evidence, but the article gives **no Farr Brothers street address and no individual proprietor**.

Together with already preserved 1922 primary descriptions (**Grocers, Butchers**) and Oregon City's official Farr Store history associating the Farr Brothers Store at 919 7th with Louis and Clarence Farr, the business now merits stable record `{BUS}`. The 1917 page itself does **not** prove a 919 7th address or name Clarence/Louis individually. `{BUS}` remains strictly separate from Edwin F. Farr, Alice Farr, Farr's Pool Hall (`BUS-013`) at 505, and Harr's Recreation Center.

### Other context and target-frontage result

18 May p.6 includes Jones Drug Co. in county expenditures without an exact address; existing exact 617 Main controls remain stronger. Other Harding/Jones references are likewise unnumbered. Numeric financial/statistical strings that resemble target numbers were rejected.

Across all **32 genuine May pages**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact **427 Main** occupant was established. This is bounded coverage only—not vacancy, non-use, demolition or absence evidence.

## Cross-record propagation audit

Reviewed: 501/503/505 building and unified timeline records; Fifth Street building/address records; 427/W. B. Eddy controls; W. S. Eddy/Fashion Stable records; Edwin/Alice/Clarence/Farr Brothers identity controls; master/business timelines; year status; open questions; research leads; source/evidence registers; database YAML; crosswalk; archive index.

Propagation:
- create `{BID}` 106 Fifth because May supplies a direct exact-address use;
- extend `P-396` / `BUS-103` Fashion Stable through 25 May without assigning a number;
- create separate `{BUS}` Farr Brothers Store / Meat Market and retain all Farr no-merge limits;
- do **not** add a 1917 501/503/505 occupant or building event because May establishes none.

## Status

**May Enterprise monthly batch is closed: 32/32 visually verified.** 1917 remains **IN PROGRESS** with **168 genuine intended-date Enterprise pages through May**, two earlier Enterprise retrieval gaps and **246 June–December exposed slots** still to review. Courier/directory/other-source blockers remain separately active.
'''
if not (ROOT / CAPTURE).exists():
    w(CAPTURE, capture_text)

append_once("evidence/source-register.md", f'''## {SID} — Oregon City Enterprise, May 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **32/32 genuine intended-date pages visually verified**.  
Issue dates: 4, 11, 18 and 25 May 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-05-25/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-may/`; manifest `{MANIFEST}`; retrieval commit `{retrieval_commit}`.  
Evidence: `{EID}`; capture: `{CAPTURE}`.  
Notes: Direct 106 Fifth National Guard enlistment use; W. S. Eddy/Fashion Stable continuation; Farr Brothers Meat market wording. No exact target Main occupant.''')

append_once("evidence/evidence-register.md", f'''## {EID} — May 1917 Enterprise closes 32-page batch and establishes 106 Fifth enlistment use
<!-- {MARKER} -->
Source: `{SID}`  
Claims:
- all **32/32 May scans** are visually verified genuine intended-date pages;
- Enterprise cumulative coverage is **168 genuine pages through May**, with 246 exposed June–December slots remaining;
- 25 May p8 directly states National Guard enlistments are received at **106 Fifth street** (`{BID}`);
- 4/11/18/25 May p7 ads extend W. S. Eddy/Fashion Stable at Main between Fourth/Fifth through 25 May;
- 25 May p6 directly calls Farr Brothers a **Meat market**, without an address or named individual proprietor;
- no exact 501/503/505/507/509/511 Main or new 427 Main occupant was established.
Classification: **DOCUMENTED / DIRECT** for page identity, 106 Fifth, Fashion Stable and Farr Brothers business type; **COVERAGE RESULT ONLY** for no target-address hit.  
Confidence: **Very High**, with identity/building-continuity limits preserved.''')

# YAML source/evidence.
text = r("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(SID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {SID}\n    name: "Oregon City Enterprise, May 1917 complete scan-first visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-05-25/ed-1/"\n    type: "Primary newspaper page scans; 32/32 genuine pages visually verified"\n    date: "1917-05-04 through 1917-05-25"\n    repository_file: "{CAPTURE}"\n    notes: "May complete; direct 106 Fifth enlistment use, Fashion Stable continuation and Farr Brothers Meat market wording."\n    related_evidence: [{EID}]\n'''
    w("database/sources.yml", text)
text = r("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(EID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {EID}\n    name: "May 1917 Enterprise closes 32-page batch and establishes 106 Fifth enlistment use"\n    type: "Primary newspaper visual review"\n    date: "1917-05-04 through 1917-05-25"\n    claims:\n      - "All 32 May pages visually verified."\n      - "Enterprise cumulative genuine coverage: 168 pages through May; 246 June-December slots remain."\n      - "25 May p8 directly states National Guard enlistments are received at 106 Fifth street."\n      - "May p7 ads extend W. S. Eddy/Fashion Stable through 25 May."\n      - "25 May p6 directly calls Farr Brothers a Meat market, without address or named proprietor."\n      - "No exact target Main occupant established in May."\n    confidence: "Very High for visible wording and counts; inference limits retained."\n    related_sources: [{SID}]\n'''
    w("database/evidence.yml", text)

# New 106 Fifth address/building record.
if not (ROOT / BUILDING).exists():
    w(BUILDING, f'''# 106 Fifth Street\n\nBuilding/address ID: `{BID}`.\n\n## Direct evidence\n\nA visually verified **25 May 1917 Oregon City Enterprise** article states that Oregon National Guard **“enlistments are being received at 106 Fifth street”** (`{EID}` / `{SID}`). This establishes a dated exact-address recruiting/enlistment use.\n\n## Limits\n\nOwner, ordinary tenant, exact room, parcel, footprint, construction date, physical fabric, continuity and duration are unresolved. Do not merge 106 Fifth with 107/108/109/110 Fifth, Fashion Stable, or any Main Street target solely from this evidence.\n\n## Audit history\n\nThe 29 August entity audit did not create 106 Fifth because no direct exact-address use had then been recovered. `{EID}` supplies that missing direct observation; the old audit wording is retained as historical process documentation.\n''')
text = r("database/buildings.yml")
if not re.search(rf"(?m)^  - id: {re.escape(BID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {BID}\n    name: 106 Fifth Street (historic National Guard enlistment address)\n    address: 106 Fifth Street, Oregon City, Oregon\n    repository_file: {BUILDING}\n    notes: "25 May 1917 Enterprise directly states National Guard enlistments were received at 106 Fifth. Dated recruiting use only; owner, ordinary tenant, parcel, footprint and physical continuity unresolved."\n    related_evidence: [{EID}]\n    related_sources: [{SID}]\n'''
    w("database/buildings.yml", text)

# New Farr Brothers business record.
if not (ROOT / FARR_BUS).exists():
    w(FARR_BUS, f'''# Farr Brothers Store / Meat Market\n\nBusiness ID: `{BUS}`. Official identity context includes Clarence P. Farr (`P-395`); the May 1917 article itself names no individual proprietor.\n\n## Chronology\n\n- **25 May 1917:** *Oregon City Enterprise* directly calls **Farr Brothers** a **Meat market** (`{EID}` / `{SID}`); no address printed.\n- **1922:** preserved primary sources list Farr Brothers separately from pool-hall businesses and describe **Grocers, Butchers**.\n- **Official City context:** Oregon City's Farr Store history identifies the Farr Brothers Store at **919 7th Street** with Louis and Clarence Farr and a later operating span into the mid-1940s. The City source supplies the identity/location context; the 1917 page does not itself print 919 7th.\n\n## No-merge rule\n\nDo not merge this grocery/meat business with Edwin F. Farr, Alice Farr, **Farr's Pool Hall (`BUS-013`) at 505 Main**, Carl Harr or Harr's Recreation Center. The 1917 evidence does not establish exact address, title or named operators.\n''')
append_once("businesses/business-index.md", f'''## May 1917 Enterprise business promotion
<!-- {MARKER} -->

| ID | Business | Address / location | Notes |
| --- | --- | --- | --- |
| {BUS} | [Farr Brothers Store / Meat Market](farr-brothers-store.md) | 1917 exact address unresolved; official Farr Store context is 919 7th | 25 May 1917 directly says **Farr Brothers Meat market**; 1922 primary sources say Grocers/Butchers. Official City history links the store to Louis/Clarence Farr. Strictly separate from Edwin/Alice Farr and 505 Main pool hall. `{EID}` / `{SID}`. |''')
text = r("database/businesses.yml")
if not re.search(rf"(?m)^  - id: {re.escape(BUS)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {BUS}\n    name: Farr Brothers Store / Meat Market\n    repository_file: {FARR_BUS}\n    address: "1917 exact address unresolved; official Farr Store history places the business at 919 7th Street"\n    notes: "25 May 1917 Enterprise directly calls Farr Brothers a Meat market; 1922 primary evidence says Grocers/Butchers; official City history associates Farr Brothers Store with Louis and Clarence Farr. No merge with Edwin/Alice Farr or 505 Main."\n    related_people: [P-395]\n    related_evidence: [{EID}]\n    related_sources: [{SID}]\n'''
    w("database/businesses.yml", text)

# Existing entity extensions.
replace_once("businesses/fashion-stable.md",
             "- **April 1917:** repeated ads place Fashion Stable **between Fourth and Fifth on Main Street** (`E-252` / `S-279`).",
             f"- **6 April–25 May 1917:** repeated ads place Fashion Stable **between Fourth and Fifth on Main Street** (`E-252` / `S-279`; continued `{EID}` / `{SID}`).")
append_once("businesses/fashion-stable.md", f'''## May continuation\n<!-- {MARKER} -->\n\nAds on 4, 11, 18 and 25 May p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street, extending the verified 1917 span through **25 May** (`{EID}` / `{SID}`). No exact number is printed.''')
replace_once("people/profiles/w-s-eddy.md",
             "- **6–27 April 1917:** repeated visually reviewed professional ads place **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street** (`E-252` / `S-279`). No street number is printed.",
             f"- **6 April–25 May 1917:** repeated visually reviewed professional ads place **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street** (`E-252` / `S-279`; continued `{EID}` / `{SID}`). No street number is printed.")
append_once("people/profiles/w-s-eddy.md", f'''## May continuation\n<!-- {MARKER} -->\n\nThe 4/11/18/25 May p7 ads repeat the same name, credentials, business and relative location; latest verified date is **25 May 1917** (`{EID}` / `{SID}`).''')
append_once("people/profiles/clarence-p-farr.md", f'''## 1917 Farr Brothers business-type control\n<!-- {MARKER} -->\n\n`{EID}` / `{SID}` directly calls **Farr Brothers** a **Meat market** on 25 May 1917. The page does **not** name Clarence individually. Clarence's relation to Farr Brothers Store comes from the independent official City source. Business `{BUS}` therefore links here as cross-source identity context, not a direct 25 May proprietor statement.''')
append_once(FARR_GUARD, f'''## 25 May 1917 direct business-type control\n<!-- {MARKER} -->\n\n`{EID}` / `{SID}` adds an earlier primary control: the *Oregon City Enterprise* market column directly calls **Farr Brothers** a **Meat market**. It prints no address or individual proprietor. This strengthens the grocery/meat identity and supports stable business `{BUS}` while reinforcing—not weakening—the no-merge rule with Edwin/Alice Farr and Farr's Pool Hall at 505.''')

for entity, field, val in [
    ("P-396", "related_evidence", EID), ("P-396", "related_sources", SID),
    ("P-395", "related_businesses", BUS), ("P-395", "related_evidence", EID), ("P-395", "related_sources", SID)]:
    yaml_add("database/people.yml", entity, field, val)
for field, val in [("related_evidence", EID), ("related_sources", SID)]:
    yaml_add("database/businesses.yml", "BUS-103", field, val)

# Refresh existing index rows without changing IDs.
people = r("people/people-index.md")
m = re.search(r"(?m)^\| P-396 \|.*$", people)
if m and EID not in m.group(0):
    row = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 Fifth-between-Main/Water; 6 Apr–25 May 1917 Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. `E-252` / `S-279`; `{EID}` / `{SID}`. |"
    people = people[:m.start()] + row + people[m.end():]
m = re.search(r"(?m)^\| P-395 \|.*$", people)
if m and BUS not in m.group(0):
    row = f"| P-395 | [Clarence P. Farr](profiles/clarence-p-farr.md) | Oregon City Farr Brothers family / municipal C. P. Farr identity control | Official City history associates Clarence with Farr Brothers Store (`{BUS}`); 25 May 1917 only names Farr Brothers Meat market, not Clarence individually. Keep separate from Edwin F. Farr / 505 Main. |"
    people = people[:m.start()] + row + people[m.end():]
w("people/people-index.md", people)
bi = r("businesses/business-index.md")
m = re.search(r"(?m)^\| BUS-103 \|.*$", bi)
if m and EID not in m.group(0):
    row = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–25 May 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); no exact number. May ads extend direct observation through 25 May. `E-252` / `S-279`; `{EID}` / `{SID}`. |"
    bi = bi[:m.start()] + row + bi[m.end():]
w("businesses/business-index.md", bi)

# 106 Fifth timeline YAML and narrative.
ty = r("database/timeline.yml")
if not re.search(rf"(?m)^  - id: {re.escape(TID)}$", ty):
    ty = ty.rstrip() + f'''\n\n  - id: {TID}\n    date: "25 May 1917"\n    summary: "Oregon City Enterprise directly states that Oregon National Guard enlistments are being received at 106 Fifth Street; dated recruiting use only, not owner/ordinary tenant or physical continuity."\n    confidence: "Very High for exact-address published wording; property/building relationships unresolved"\n    related_evidence:\n      - {EID}\n    related_buildings:\n      - {BID}\n'''
    w("database/timeline.yml", ty)
append_once("timeline.md", f'''## 25 May 1917 — {TID}: National Guard enlistments at 106 Fifth\n<!-- {MARKER} -->\n\nA visually verified *Oregon City Enterprise* article directly states that Oregon National Guard **enlistments are being received at 106 Fifth street** (`{SID}` / `{EID}`; `{BID}`). This establishes a dated recruiting use, not property ownership, ordinary tenancy or physical continuity.\n\nThe May batch also extends **W. S. Eddy / Fashion Stable (`P-396` / `BUS-103`) at Main between Fourth and Fifth through 25 May** and directly calls **Farr Brothers (`{BUS}`) a Meat market** without an address. Neither result establishes a 501/503/505 occupant.''')

# Business timeline: extend April Fashion Stable row and add separate Farr identity line.
bt = r("registers/business-timeline.md")
old = "| 6–27 Apr. 1917 | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252` / `S-279` | Repeated direct ads; exact move day/number unresolved. Not W. B. Eddy/427 by assumption. |"
new = f"| 6 Apr.–25 May 1917 | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252` / `S-279`; `{EID}` / `{SID}` | Repeated direct ads; exact move day/number unresolved. Not W. B. Eddy/427 by assumption. |"
if old in bt:
    bt = bt.replace(old, new, 1)
w("registers/business-timeline.md", bt)
append_once("registers/business-timeline.md", f'''## Farr Brothers separate business identity\n<!-- {MARKER} -->\n\n| Date | Address | Business | ID | Evidence | Limits |\n| --- | --- | --- | --- | --- | --- |\n| 25 May 1917 | Not printed | Farr Brothers Meat market | `{BUS}` | `{EID}` / `{SID}` | Direct business-type wording only; official later context is 919 7th. No Edwin/Alice Farr or 505 merge. |''')

# Address/navigation/crosswalk.
append_once("registers/address-register.md", f'''## 25 May 1917 — 106 Fifth exact-address anchor\n<!-- {MARKER} -->\n\n| Address | Building ID | Primary page | Related evidence | Established use / limits |\n| --- | --- | --- | --- | --- |\n| **106 Fifth Street** | `{BID}` | `{BUILDING}` | `{EID}` / `{SID}` | Oregon National Guard enlistments received here on 25 May 1917. Owner, ordinary tenant, parcel, footprint and physical continuity unresolved. |''')
append_once("indexes/id-crosswalk.md", f'''## {SID} / {EID} — May 1917 Enterprise closeout\n<!-- {MARKER} -->\n\n- `{BID}` — 106 Fifth exact-address National Guard enlistment use, 25 May 1917.\n- `P-396` / `BUS-103` — W. S. Eddy / Fashion Stable Main-between-Fourth/Fifth observation extended through 25 May.\n- `{BUS}` — Farr Brothers Store / Meat Market; 25 May 1917 direct meat-market wording, later official 919 7th / Clarence Farr context; separate from `BUS-013` 505 Main.\n- `{TID}` — dated 106 Fifth timeline event.\n''')
append_once("ARCHIVE_INDEX.md", f'''## May 1917 Enterprise additions\n<!-- {MARKER} -->\n\n- [`{BID}` — 106 Fifth Street](buildings/106-fifth.md): 25 May 1917 direct National Guard enlistment/recruiting use; property/building continuity unresolved.\n- [`{BUS}` — Farr Brothers Store / Meat Market](businesses/farr-brothers-store.md): 25 May 1917 direct meat-market wording; later official 919 7th / Louis-Clarence Farr context; **not** Farr's Pool Hall at 505.\n- `P-396` / `BUS-103` W. S. Eddy / Fashion Stable: Main-between-Fourth/Fifth observation now extends through 25 May 1917.\n''')

# Preserve entity-audit history while recording why 106 Fifth is now promoted.
append_once("registers/entity-page-audit-2026-08-29.md", f'''## 6 September 2026 follow-up — 106 Fifth and Farr Brothers promotion\n<!-- {MARKER} -->\n\nThe earlier audit correctly withheld **106 Fifth** because no direct exact-address use had then been recovered. May 1917 `S/E` evidence (`{SID}` / `{EID}`) now directly states National Guard enlistments were received at 106 Fifth, so address record `{BID}` is added. The earlier wording remains in place as audit history.\n\nThe same May source directly calls **Farr Brothers** a **Meat market**. Combined with 1922 primary Grocers/Butchers evidence and official City Farr Store identity/location context, the business now meets the archive threshold for stable business `{BUS}`. No 505/Edwin/Alice Farr merger is made.''')

# Year-closeout / questions / leads / log.
append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise May audit added 6 September 2026\n<!-- {MARKER} -->\n\n`{SID}` / `{EID}` closes May at **32/32 genuine visually verified pages** with no May page-identity gap. Enterprise cumulative coverage is **168 genuine intended-date pages through May**; the prior March/April gaps remain and **246 exposed June–December slots** are still pending. May directly establishes 106 Fifth as a National Guard enlistment location (`{BID}`), extends W. S. Eddy/Fashion Stable through 25 May, and calls Farr Brothers a Meat market (`{BUS}`). No exact target Main occupant was established; silence is not vacancy evidence.''')
append_once("evidence/open-questions.md", f'''## 6 September 2026 — May Enterprise narrowing\n<!-- {MARKER} -->\n\nMay 1917 is now 32/32 visually verified under `{SID}` / `{EID}`. The exact 1917 **503/505 occupant question remains unresolved**; May establishes no target Main occupant. The Fifth Street control is improved by direct **106 Fifth** enlistment use (`{BID}`). Enterprise still has 246 June–December exposed slots plus the two earlier page gaps and final title-calendar reconciliation.''')
append_once("evidence/research-leads.md", f'''## 6 September 2026 — Enterprise continuation after May\n<!-- {MARKER} -->\n\nMay is complete 32/32 (`{SID}` / `{EID}`), cumulative **168 genuine Enterprise pages through May**. Continue with **June 1/8/15/22/29 (40 exposed slots)** using printed-date/page-number audit before content promotion. Preserve the open exact 503/505 occupant question. Separately, `{BID}` establishes a 106 Fifth recruiting-use anchor and `{BUS}` strengthens the non-505 Farr Brothers grocery/meat identity.''')
append_once("registers/research-log.md", f'''### 2026-09-06 — closed May 1917 Oregon City Enterprise\n<!-- {MARKER} -->\n- Visually verified **32/32 genuine May pages**; no May source-association gap.\n- Enterprise cumulative genuine coverage: **168 pages through May**; **246 June–December slots remain**.\n- Added `{BID}` for direct 25 May **106 Fifth Street** National Guard enlistment use.\n- Extended `P-396` / `BUS-103` Fashion Stable through 25 May.\n- Added `{BUS}` Farr Brothers Store / Meat Market from direct 1917 meat-market wording plus existing 1922/official identity context; no Edwin/Alice/505 merge.\n- No exact 501/503/505/507/509/511 Main occupant established in May; no vacancy inference.''')

# Canonical annual status row.
yr = r("registers/year-status.md")n
