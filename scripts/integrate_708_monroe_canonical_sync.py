from pathlib import Path
import re

MARKER = "<!-- 708-monroe-canonical-sync-2026-09-06 -->"
DATE = "2026-09-06"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return False
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")
    return True


def add_file_once(path, content):
    p = Path(path)
    if p.exists():
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def next_num(path, prefix):
    text = read(path)
    nums = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d{{3,4}})\b", text)]
    return max(nums, default=0) + 1


def fmt(prefix, num):
    return f"{prefix}-{num:03d}"


# Stop cleanly on rerun after the canonical source entry exists.
if MARKER in read("evidence/source-register.md"):
    print("708 Monroe canonical synchronization is already present.")
    raise SystemExit(0)

# Allocate IDs from the synchronized canonical registers at workflow runtime.
s0 = next_num("evidence/source-register.md", "S")
e0 = next_num("evidence/evidence-register.md", "E")
p0 = next_num("people/people-index.md", "P")
b0 = next_num("database/buildings.yml", "B")

S_RENT = fmt("S", s0)
S_CLARENCE = fmt("S", s0 + 1)
S_FARR_STORE = fmt("S", s0 + 2)
S_PERMIT = fmt("S", s0 + 3)
E_RENT = fmt("E", e0)
E_CLARENCE = fmt("E", e0 + 1)
E_SPATIAL = fmt("E", e0 + 2)
P_CLARENCE = fmt("P", p0)
B_708 = fmt("B", b0)

rent_capture = "evidence/source-captures/1945-c-p-farr-recreation-building-rent-ocr-lead-2026-09-03.md"
spatial_capture = "evidence/source-captures/1946-708-monroe-farr-store-spatial-separation-2026-09-06.md"

source_block = f'''{MARKER}
## {S_RENT} — Oregon City Commission, 6 March 1946 — February recreation-department rent at 708 Monroe
Type: Primary municipal Commission/claims record; **OCR/TEXT ONLY — ORIGINAL PAGE IMAGE NOT VISUALLY CERTIFIED**.  
Public record: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723048/File/document  
Meeting: **6 March 1946**; Recorder claims report covers **February 1946**.  
Relevant extracted sequence: **C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00**.  
Related evidence/person/building: `{E_RENT}`; `{P_CLARENCE}`; `{B_708}`.  
Capture: `{rent_capture}`.  
Notes: The readable municipal text is unusually explicit about the address, but repeated attempts to render the original claim-page image failed. Preserve this as OCR/TEXT ONLY until the scan is visually inspected. The entry is evidence for a City recreation-department rental at **708 Monroe**, not 505 Main, Farr's Pool Hall, or Harr's Recreation Center.

## {S_CLARENCE} — Oregon City Courier, 23 June 1911 — Clarence P. Farr executor notice
Type: Primary newspaper legal notice; **TEXT/TRANSCRIPTION CONTROL — PAGE IMAGE NOT NEWLY CERTIFIED IN THIS synchronization**.  
Archive page: https://oregonnews.uoregon.edu/lccn/sn00063698/1911-06-23/ed-1/seq-7/  
Relevant wording identifies **CLARENCE P. FARR** as executor of the estate of Isaac Farr.  
Related evidence/person: `{E_CLARENCE}`; `{P_CLARENCE}`.  
Capture: `{rent_capture}`.  
Notes: This supplies the direct middle-initial bridge for the Oregon City Clarence Farr family line. It is not by itself proof that every later `C. P. Farr` reference names this person.

## {S_FARR_STORE} — Oregon City historic-resource record, Farr Store / 919 7th Street
Type: Official City historic-resource synthesis and underlying survey route; secondary property/biographical evidence.  
City page: https://www.orcity.org/2142/919-7th-Street  
Survey PDF: https://www.orcity.org/DocumentCenter/View/7877/919_7th  
Related evidence/person: `{E_CLARENCE}`, `{E_SPATIAL}`; `{P_CLARENCE}`.  
Captures: `{rent_capture}`; `{spatial_capture}`.  
Notes: The City identifies Clarence Farr with Farr Brothers / Farr Store at the northwest corner of Seventh and Monroe and reports a mid-1940s sale to Dewey Krueger. This is official secondary evidence and does not identify the 708 Monroe recreation premises or connect Clarence to Edwin F. Farr's 505 Main pool hall.

## {S_PERMIT} — Oregon City 19 September 2017 permit log — 919 7th / 709 Monroe same-APN control
Type: Official municipal permit-log property/address control.  
PDF: https://www.orcity.org/DocumentCenter/View/638/September-11-2017-to-September-15-2017-PDF  
Relevant rows: permits BM-17-0295/BM-17-0296 list **919 7th St** and BM-17-0297 lists **709 Monroe St**, with the same owner and APN **2-2E-31AD-05000**.  
Related evidence/building: `{E_SPATIAL}`; `{B_708}` as comparison context only.  
Capture: `{spatial_capture}`.  
Notes: This directly establishes a modern 919 7th / 709 Monroe parcel-address relationship. It does not prove that 709 existed as an address in 1946, identify the historic 708 parcel, or establish ownership of the 708 recreation premises.'''
append_once("evidence/source-register.md", MARKER, source_block)

source_yaml = f'''{MARKER}
  - id: {S_RENT}
    name: "Oregon City Commission, 6 March 1946 — February recreation-department rent at 708 Monroe"
    url: "https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723048/File/document"
    type: "Primary municipal claims record; OCR/TEXT ONLY pending page-image certification"
    date: "1946-03-06"
    notes: "Extracted sequence: C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00. This is a 708 Monroe municipal-recreation record, not a 505 Main occupancy or Farr/Harr business-transfer record."
    related_evidence: [{E_RENT}]
    related_people: [{P_CLARENCE}]
    related_buildings: [{B_708}]
    repository_file: "{rent_capture}"

  - id: {S_CLARENCE}
    name: "Oregon City Courier, 23 June 1911 — Clarence P. Farr executor notice"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1911-06-23/ed-1/seq-7/"
    type: "Primary newspaper legal notice; text control"
    date: "1911-06-23"
    notes: "Explicitly names Clarence P. Farr as executor of Isaac Farr's estate; used as the direct middle-initial bridge in the later C. P. Farr identity analysis."
    related_evidence: [{E_CLARENCE}]
    related_people: [{P_CLARENCE}]
    repository_file: "{rent_capture}"

  - id: {S_FARR_STORE}
    name: "Oregon City historic-resource record — Farr Store, 919 7th Street"
    url: "https://www.orcity.org/2142/919-7th-Street"
    type: "Official municipal historic-resource synthesis / survey route"
    notes: "Identifies Clarence Farr with Farr Brothers/Farr Store at Seventh and Monroe and reports a mid-1940s sale to Dewey Krueger; does not identify 708 Monroe or 505 Main."
    related_evidence: [{E_CLARENCE}, {E_SPATIAL}]
    related_people: [{P_CLARENCE}]
    repository_file: "{spatial_capture}"

  - id: {S_PERMIT}
    name: "Oregon City 2017 permit log — 919 7th and 709 Monroe same-APN control"
    url: "https://www.orcity.org/DocumentCenter/View/638/September-11-2017-to-September-15-2017-PDF"
    type: "Official municipal permit-log address/parcel control"
    date: "2017-09-19"
    notes: "919 7th and 709 Monroe appear under the same APN 2-2E-31AD-05000. Modern parcel/address control only; does not identify historic 708 ownership."
    related_evidence: [{E_SPATIAL}]
    related_buildings: [{B_708}]
    repository_file: "{spatial_capture}"'''
append_once("database/sources.yml", MARKER, source_yaml)

evidence_block = f'''{MARKER}
## {E_RENT} — February 1946 City recreation-department rent is explicitly addressed to 708 Monroe
Source: `{S_RENT}`  
Related person/building: `{P_CLARENCE}` / `{B_708}`  
Type: Primary municipal claims text; page image not visually certified  
Claims:
- The 6 March 1946 Oregon City Commission claims material for February aligns **C. P. Farr**, **Rent at 708 Monroe - Rec. Dept.**, and **$150.00**.
- The repeated 1944–1946 C. P. Farr / $150 recreation-rent pattern strongly suggests the same rental relationship across adjacent months, but **708 Monroe is directly printed only in the recovered February 1946 text**.
- This record should not be used as evidence for **505 Main**, **Farr's Pool Hall**, **Harr's Recreation Center**, or a Farr→Harr transfer.
Classification: **OCR/TEXT ONLY** for the municipal row; **DOCUMENTED ADDRESS IN EXTRACTED PRIMARY TEXT**, pending scan certification.  
Confidence: High for the extracted wording; original-page visual verification still required.

## {E_CLARENCE} — Municipal C. P. Farr is strongly identified as Clarence P. Farr, not Edwin F. Farr
Sources: `{S_CLARENCE}`, `{S_FARR_STORE}`; municipal context in `{S_RENT}`  
Related person: `{P_CLARENCE}`  
Type: Cross-source identity control  
Claims:
- The 23 June 1911 legal notice directly names **Clarence P. Farr** in the Oregon City Farr family line.
- Oregon City's official Farr Store history independently identifies **Clarence Farr** with the local Farr Brothers/Farr Store family and property context.
- Early-1940s Oregon City municipal records use **C. P. Farr** for a commissioner; the 1944–1946 recreation-rent claims use the same initials.
- Together these facts strongly support identifying the municipal/rent **C. P. Farr** as **Clarence P. Farr**.
- No recovered 1940s record in this chain spells out `Clarence P. Farr` in the same rent row, so the identity remains **STRONG CROSS-SOURCE INFERENCE**, not a direct same-record expansion.
- Clarence P. Farr is kept separate from **Edwin F. Farr (`P-028`)**, Alice Farr, and Farr's Pool Hall at 505 Main.
Classification: **STRONG CROSS-SOURCE INFERENCE / IDENTITY GUARD**.  
Confidence: High; direct 1940s spelled-out bridge still desirable.

## {E_SPATIAL} — 708 Monroe is strongly separated from the Farr Store's documented 709 Monroe address
Sources: `{S_RENT}`, `{S_FARR_STORE}`, `{S_PERMIT}`  
Related building/person: `{B_708}` / `{P_CLARENCE}`  
Type: Address/parcel comparison; historic 708 title unresolved  
Claims:
- The 1946 municipal rent text identifies the recreation premises as **708 Monroe**.
- A 2017 official City permit log directly associates **919 7th Street** and **709 Monroe Street** with the same APN **2-2E-31AD-05000**, consistent with the Farr Store corner property having a Monroe-side 709 address.
- This strongly favors **708 Monroe and the Farr Store/709 Monroe property being separate premises**, rather than 708 being a simple alternate address for 919 7th.
- The comparison does not establish the 1946 owner/legal description of 708, uninterrupted address usage, or building survival.
Classification: **STRONG CROSS-SOURCE SPATIAL INFERENCE**; historic 708 parcel ownership remains unresolved.  
Confidence: High for separation; unresolved for 1946 title/boundary.'''
append_once("evidence/evidence-register.md", MARKER, evidence_block)

evidence_yaml = f'''{MARKER}
  - id: {E_RENT}
    name: "February 1946 City recreation-department rent is explicitly addressed to 708 Monroe"
    type: "Primary municipal claims text; OCR/TEXT ONLY pending scan certification"
    claims:
      - "6 March 1946 claims material aligns C. P. Farr, Rent at 708 Monroe - Rec. Dept., and $150.00."
      - "The record is a 708 Monroe municipal-recreation-premises record and is not evidence for 505 Main, Farr's Pool Hall, Harr's Recreation Center, or a Farr-to-Harr transfer."
    confidence: "High for extracted wording; original-page visual certification pending"
    related_sources: [{S_RENT}]
    related_people: [{P_CLARENCE}]
    related_buildings: [{B_708}]
    repository_file: "{rent_capture}"

  - id: {E_CLARENCE}
    name: "Municipal C. P. Farr is strongly identified as Clarence P. Farr"
    type: "Cross-source identity control"
    claims:
      - "A 1911 Oregon City legal notice explicitly names Clarence P. Farr."
      - "Official City Farr Store history independently identifies Clarence Farr in the local Farr Brothers family/property context."
      - "The later municipal C. P. Farr identity is a strong cross-source inference, not a same-record full-name expansion."
      - "Clarence P. Farr is not merged with Edwin F. Farr or Farr's Pool Hall at 505 Main."
    confidence: "High; direct 1940s spelled-out identity bridge still desirable"
    related_sources: [{S_CLARENCE}, {S_FARR_STORE}, {S_RENT}]
    related_people: [{P_CLARENCE}, P-028]
    repository_file: "{rent_capture}"

  - id: {E_SPATIAL}
    name: "708 Monroe is strongly separated from the Farr Store's documented 709 Monroe address"
    type: "Cross-source address/parcel comparison"
    claims:
      - "1946 municipal text names 708 Monroe for the recreation premises."
      - "2017 City permit records place 919 7th and 709 Monroe on the same APN 2-2E-31AD-05000."
      - "The evidence strongly favors separate 708 and 709/Farr Store premises; historic 708 title remains unresolved."
    confidence: "High for spatial separation; historic 708 ownership and legal description unresolved"
    related_sources: [{S_RENT}, {S_FARR_STORE}, {S_PERMIT}]
    related_people: [{P_CLARENCE}]
    related_buildings: [{B_708}]
    repository_file: "{spatial_capture}"'''
append_once("database/evidence.yml", MARKER, evidence_yaml)

person_profile = f'''# Clarence P. Farr

Person ID: `{P_CLARENCE}`.

{MARKER}

## Identity

A 23 June 1911 *Oregon City Courier* legal notice explicitly names **Clarence P. Farr** as executor of Isaac Farr's estate (`{S_CLARENCE}` / `{E_CLARENCE}`). Oregon City's official Farr Store history independently identifies Clarence Farr with the local Farr Brothers / 919 7th Street family and property context (`{S_FARR_STORE}`).

Later Oregon City municipal records use **C. P. Farr**. The archive therefore treats **C. P. Farr → Clarence P. Farr** as a **STRONG CROSS-SOURCE INFERENCE**, not as a direct full-name transcription from the 1946 rent row. A spelled-out 1940s municipal/property record remains desirable.

## 1946 recreation-rent context

The 6 March 1946 Commission claims text aligns C. P. Farr with **Rent at 708 Monroe - Rec. Dept. — $150.00** (`{S_RENT}` / `{E_RENT}`). The original claim-page image has not been visually certified, so the row remains **OCR/TEXT ONLY**.

Clarence P. Farr is **not** merged with Edwin F. Farr (`P-028`), Alice Farr, Farr's Pool Hall (`BUS-013`), Carl R. Harr (`P-094`), or Harr's Recreation Center (`BUS-014`). The 708 Monroe municipal recreation premises is a separate research thread from 505 Main.'''
add_file_once("people/profiles/clarence-p-farr.md", person_profile)

people_block = f'''{MARKER}
## 6 September 2026 identity addition

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| {P_CLARENCE} | [Clarence P. Farr](profiles/clarence-p-farr.md) | Oregon City Farr Brothers family / municipal C. P. Farr identity control | 1911 source directly gives **Clarence P. Farr**; later municipal `C. P. Farr` identity is a **STRONG CROSS-SOURCE INFERENCE**. February 1946 recreation rent is addressed to 708 Monroe. Keep separate from Edwin F. Farr / 505 Main. |'''
append_once("people/people-index.md", MARKER, people_block)

people_yaml = f'''{MARKER}
  - id: {P_CLARENCE}
    name: Clarence P. Farr
    role: "Oregon City Farr Brothers family / municipal C. P. Farr identity control"
    notes: "1911 legal notice directly names Clarence P. Farr. Later municipal C. P. Farr is a strong cross-source identity inference; February 1946 recreation rent is addressed to 708 Monroe. Keep separate from Edwin F. Farr and the 505 Main pool-hall chain."
    related_sources: [{S_CLARENCE}, {S_FARR_STORE}, {S_RENT}]
    related_evidence: [{E_CLARENCE}, {E_RENT}, {E_SPATIAL}]
    related_buildings: [{B_708}]
    repository_file: people/profiles/clarence-p-farr.md'''
append_once("database/people.yml", MARKER, people_yaml)

building_page = f'''# 708 Monroe Street — recreation-premises research control

Building/address ID: `{B_708}`.

{MARKER}

## Scope

This is an **address/premises research-control record**, created because a February 1946 Oregon City municipal claim explicitly identifies **708 Monroe** as the City's recreation-department rental. It is outside the 501/503/505 Main frontage and must not be used to merge the C. P. Farr municipal-rent thread with Farr's Pool Hall or Harr's Recreation Center at 505 Main.

## Evidence

- `{S_RENT}` / `{E_RENT}` — 6 March 1946 Commission claims text for February: **C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00**. **OCR/TEXT ONLY** pending scan certification.
- `{S_PERMIT}` / `{E_SPATIAL}` — 2017 City permit control places **919 7th** and **709 Monroe** on the same APN, strongly favoring 708 as a separate premises from the Farr Store parcel.
- `{S_FARR_STORE}` — official City Farr Store history is context for Clarence Farr only; it does not identify 708.

## Unresolved

The 1944–1946 ownership/legal description of 708 Monroe, exact building footprint, construction history, lease instrument, and continuity into the later YMCA/Clackamas Y use remain unresolved. No building-continuity claim is made.'''
add_file_once("buildings/708-monroe.md", building_page)

building_yaml = f'''{MARKER}
  - id: {B_708}
    name: 708 Monroe Street recreation-premises control
    address: 708 Monroe Street, Oregon City, Oregon
    repository_file: buildings/708-monroe.md
    notes: "February 1946 municipal claims text identifies City recreation-department rent at 708 Monroe. This address record is deliberately separate from 505 Main and from the Farr Store/919 7th/709 Monroe property. Historic ownership, legal description, footprint and building continuity are unresolved."
    related_people: [{P_CLARENCE}]
    related_evidence: [{E_RENT}, {E_SPATIAL}]
    related_sources: [{S_RENT}, {S_PERMIT}, {S_FARR_STORE}]'''
append_once("database/buildings.yml", MARKER, building_yaml)

crosswalk_block = f'''{MARKER}
## 6 September 2026 — 708 Monroe / Clarence P. Farr separation control

| Record | Links | Handling rule |
| --- | --- | --- |
| `{S_RENT}` / `{E_RENT}` | `{B_708}`, `{P_CLARENCE}` | February 1946 municipal recreation rent: **708 Monroe**, not 505 Main; OCR/TEXT ONLY pending scan certification. |
| `{S_CLARENCE}` / `{S_FARR_STORE}` / `{E_CLARENCE}` | `{P_CLARENCE}` | `C. P. Farr → Clarence P. Farr` is **STRONG CROSS-SOURCE INFERENCE**; do not merge with `P-028` Edwin F. Farr. |
| `{S_PERMIT}` / `{E_SPATIAL}` | `{B_708}` | Modern 919 7th / 709 Monroe same-APN control strongly separates the 708 premises; historic 708 title remains unresolved. |'''
append_once("indexes/id-crosswalk.md", MARKER, crosswalk_block)

archive_block = f'''{MARKER}
### 708 Monroe Street — off-Main research control

Primary file: `buildings/708-monroe.md` (`{B_708}`).

A February 1946 Oregon City Commission claims record identifies the City's recreation-department rent as **C. P. Farr — 708 Monroe — $150** (`{S_RENT}` / `{E_RENT}`; **OCR/TEXT ONLY** pending scan certification). This address is retained because it closes a misleading Farr/Harr research path: it is **not evidence for 505 Main**. A separate City permit-address control strongly distinguishes 708 from the Farr Store parcel's documented **709 Monroe / 919 7th** address (`{E_SPATIAL}`).'''
append_once("ARCHIVE_INDEX.md", MARKER, archive_block)

openq_block = f'''{MARKER}
## 6 September 2026 — Farr→Harr false-path closure: C. P. Farr recreation rent is 708 Monroe

`{S_RENT}` / `{E_RENT}` records the February 1946 City recreation-department rent at **708 Monroe**, not 505 Main. `{E_CLARENCE}` strongly identifies the municipal `C. P. Farr` as **Clarence P. Farr** and explicitly keeps him separate from Edwin F. Farr (`P-028`). `{E_SPATIAL}` further favors 708 as separate from the Farr Store's documented 709 Monroe / 919 7th parcel.

**Effect on open questions:** the exact **Farr's Pool Hall → Harr's Recreation Center** transition at 505 remains open, but the C. P. Farr municipal recreation-rent series is removed as evidence for that transition. Continue with the 1947–48 directory, missing 1944–48 liquor-license proceedings, and cumulative 505 historic-resource source notes. Historic ownership/legal description of 708 itself remains unresolved.'''
append_once("evidence/open-questions.md", MARKER, openq_block)

lead_block = f'''{MARKER}
## 6 September 2026 — 708 Monroe separation control for the Farr/Harr search

The municipal C. P. Farr recreation-rent thread now has an exact premises control: **708 Monroe** (`{S_RENT}` / `{E_RENT}`), with C. P. Farr strongly identified as **Clarence P. Farr** (`{E_CLARENCE}`). Do **not** spend further Farr→Harr research effort treating this rent series as a possible 505 Main clue unless a new direct source explicitly bridges the premises. `{E_SPATIAL}` strongly separates 708 from the Farr Store/709 Monroe parcel as well.

For the mid-1940s 505 transition, retain the existing priority order: **MF-001 1947–48 Clackamas County Directory → MF-002 missing 1944–48 Oregon City liquor-license proceedings → MF-047 cumulative 505 historic-resource file/source notes**.'''
append_once("evidence/research-leads.md", MARKER, lead_block)

farr_note = f'''{MARKER}
## 708 Monroe identity guard

The separately registered municipal recreation-rent record `{S_RENT}` / `{E_RENT}` identifies **708 Monroe**, not 505 Main. Its payee `C. P. Farr` is strongly identified as **Clarence P. Farr (`{P_CLARENCE}`)** under `{E_CLARENCE}`. This is not Edwin F. Farr and is not evidence for Farr's Pool Hall opening, operation, ownership, or transfer at 505.'''
append_once("businesses/farrs-pool-hall.md", MARKER, farr_note)

harr_note = f'''{MARKER}
## 708 Monroe false-path closure

The 1944–1946 municipal `C. P. Farr` recreation-rent series is now controlled by the February 1946 exact-address text **708 Monroe** (`{S_RENT}` / `{E_RENT}`), with `C. P. Farr` strongly identified as Clarence P. Farr (`{P_CLARENCE}`). It is therefore not evidence for Harr's Recreation Center at 505 or for the Farr→Harr transition. The 1945 Harr source-provenance gap remains unchanged.'''
append_once("businesses/harrs-recreation-center.md", MARKER, harr_note)

edwin_note = f'''{MARKER}
## Clarence P. Farr no-merge control

`{P_CLARENCE}` **Clarence P. Farr** is now separately registered. The municipal `C. P. Farr` recreation-rent thread points to **708 Monroe** (`{E_RENT}`) and is not merged with Edwin F. Farr, Alice Farr, or Farr's Pool Hall at 505.'''
append_once("people/profiles/edwin-f-farr.md", MARKER, edwin_note)

b505_note = f'''{MARKER}
## 6 September 2026 — C. P. Farr recreation-rent false path closed

The separate municipal recreation-rent thread now has an exact February 1946 premises address: **708 Monroe** (`{S_RENT}` / `{E_RENT}`), not 505 Main. The payee `C. P. Farr` is strongly identified as Clarence P. Farr (`{P_CLARENCE}`), distinct from Edwin F. Farr. This does **not** change the 505 chronology; it removes the municipal recreation-rent series as evidence for Farr's Pool Hall, Harr's Recreation Center, or their transition.'''
append_once("buildings/505-main.md", MARKER, b505_note)

TL_NOTE = f'''{MARKER}
## Research-control note — 708 Monroe is not part of the 505 Farr→Harr chain

A February 1946 City claim prints **C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00** (`{S_RENT}` / `{E_RENT}`; OCR/TEXT ONLY pending scan certification). This is an off-site municipal recreation-premises thread and is not inserted as a 505 occupancy event. The exact Farr→Harr transition at 505 remains unresolved.'''
append_once("timelines/505-main.md", MARKER, TL_NOTE)

checkpoint_note = f'''{MARKER}
## 6 September 2026 addendum — C. P. Farr recreation-rent lead separated from 505

Subsequent work after this checkpoint recovered a February 1946 municipal claims line identifying **C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00** (`{S_RENT}` / `{E_RENT}`). The row remains **OCR/TEXT ONLY** pending scan certification. Cross-source identity work separately supports `C. P. Farr → Clarence P. Farr` (`{P_CLARENCE}` / `{E_CLARENCE}`), not Edwin F. Farr.

This does **not** change the checkpoint's Farr→Harr bracket. It closes the C. P. Farr municipal recreation-rent series as a 505 transition lead. The high-value resume routes remain MF-001, MF-002 and MF-047.'''
append_once("evidence/source-captures/2026-09-05-farr-harr-closeout-checkpoint.md", MARKER, checkpoint_note)

log_block = f'''{MARKER}
### 2026-09-06 — canonicalized the 708 Monroe / C. P. Farr separation finding before further Farr→Harr research
- Registered `{S_RENT}` / `{E_RENT}` for the 6 March 1946 Commission claims text: **C. P. Farr — Rent at 708 Monroe - Rec. Dept. — $150.00**; retained **OCR/TEXT ONLY** because the claim-page image has not rendered for visual certification.
- Registered `{P_CLARENCE}` Clarence P. Farr with `{S_CLARENCE}` / `{S_FARR_STORE}` / `{E_CLARENCE}` as a **STRONG CROSS-SOURCE INFERENCE**, explicitly separate from Edwin F. Farr (`P-028`).
- Registered `{B_708}` and `{S_PERMIT}` / `{E_SPATIAL}` as an off-Main address control; current City records strongly distinguish 708 from the Farr Store's documented 709 Monroe / 919 7th parcel.
- Synchronized source/evidence YAML, person/building records, crosswalk, index, open questions, research leads, 505/Farr/Harr handling notes, and the Farr→Harr checkpoint.
- Historical result: the C. P. Farr municipal recreation-rent series is **not evidence for 505 Main or the Farr→Harr transfer**; the exact transition remains unresolved.'''
append_once("registers/research-log.md", MARKER, log_block)

print(
    "Integrated 708 Monroe canonical sync with IDs: "
    f"{S_RENT}, {S_CLARENCE}, {S_FARR_STORE}, {S_PERMIT}; "
    f"{E_RENT}, {E_CLARENCE}, {E_SPATIAL}; {P_CLARENCE}; {B_708}."
)
