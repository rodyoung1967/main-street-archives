#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

SID_CEM = "S-249"
SID_OBIT = "S-250"
SID_OLCC = "S-251"
EID_CEM = "E-223"
EID_OBIT = "E-224"
EID_OLCC = "E-225"
CAPTURE = ROOT / "evidence/source-captures/503-505-grisham-wiitanen-online-pass-2026-09-05.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected anchor not found in {rel}: {old[:120]!r}")
    write(rel, text.replace(old, new, 1))


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.strip() + "\n")


# Stop instead of reusing IDs if parallel main assigned them.
for ident, rel in [
    (SID_CEM, "evidence/source-register.md"),
    (SID_OBIT, "evidence/source-register.md"),
    (SID_OLCC, "evidence/source-register.md"),
    (EID_CEM, "evidence/evidence-register.md"),
    (EID_OBIT, "evidence/evidence-register.md"),
    (EID_OLCC, "evidence/evidence-register.md"),
]:
    if re.search(rf"^## {re.escape(ident)}\b", read(rel), re.M):
        raise SystemExit(f"{ident} is already assigned in {rel}; stop rather than reuse/renumber.")

if CAPTURE.exists():
    raise SystemExit(f"Capture already exists: {CAPTURE.relative_to(ROOT)}")

CAPTURE.write_text(r'''# 503 / 505 Main — Grisham / Wiitanen targeted online pass

Date: **5 September 2026**  
Status: **IN PROGRESS targeted person/business/property pass; not an annual ONLINE COMPLETE closeout.**

Purpose: tighten the documentary relationship of **Raye Grisham / LaFarlette**, **Richard (Dick) Wiitanen**, and **Sheila Wiitanen** to **503 Main** and **505 Main** while keeping business ownership, operation, liquor licensing, and real-estate title separate.

## Controlling separation rule

- **The Wheel belongs only to 503 Main.**
- Raye's documented family/business connection is to the 503 Wheel chain. No recovered source in this pass gives Raye an ownership/operator role at 505.
- Dick and Sheila's 503 and 505 histories are separate chains: at 503 the family account is Wheel business purchase → later 503 real-estate purchase → later combined sale; at 505 the family account is Brass Rail operation before real-estate ownership → later 505 property purchase → later operator/transfer/repo cycle.

## New direct identity evidence for Raye

### Oregon City cemetery register — `S-249` / `E-223`

The City of Oregon City's **Mausoleum Burial List by Last Name**, dated 5 September 2019, was opened and **PDF page 49 / viewer index 48 was visually inspected**. The row directly records:

- last name **GRISHAM**;
- first name **RAYE**;
- middle **W.**;
- maiden name **WEAVER**;
- niche **97**;
- death **6/30/2012**;
- age **94**;
- burial date **11/2/2012**.

Official PDF: https://www.orcity.org/DocumentCenter/View/646/Mausoleum-Burial-List-by-Last-Name---September-2019-PDF

This supplies direct municipal support for the surname sequence **Raye Weaver → Raye LaFarlette → Raye Grisham**. It does not establish any business transaction.

### The Oregonian obituary — `S-250` / `E-224`

The Oregonian obituary published **11 July 2012** identifies **Raye W. Grisham**, gives birth **30 Dec. 1918** and death **30 June 2012**, names daughters **Carol Stover and Sheila Wiitanen**, and says Raye was preceded in death by husbands **Floyd La Farlette** and **Cliff Grisham**.

URL: https://obits.oregonlive.com/us/obituaries/oregon/name/raye-grisham-obituary?id=25350789

The obituary reports age **93**. That conflicts with the City cemetery register's age **94**. The birth/death dates printed in the obituary are arithmetically consistent with age 93, but the archive preserves both source statements rather than silently correcting the municipal row.

The obituary does **not** mention The Wheel, 503 Main, 505 Main, or a business sale. Its value here is family/identity corroboration, especially the direct Raye→Sheila relationship and husband-name sequence.

## New 503 business-succession endpoint

### OLCC historical license list — `S-251` / `E-225`

An official Oregon Liquor Control Commission historical **licenses-by-type** PDF is indexed with a row for:

- trade name **THE WHEEL BAR & GRILL**;
- licensee **MAURICE ENTERPRISES INC**;
- address **503 MAIN ST, OREGON CITY, OR 97045**;
- license number **104145**;
- license expiration **3/31/09**.

Official PDF URL: https://www.olcc.state.or.us/pdfs/licensesbytype.pdf

The text row was recovered through the official-PDF search index, but the PDF itself returned a retrieval error when opened for page-image review in this session. Classification is therefore **OCR/TEXT ONLY / OFFICIAL INDEXED PDF TEXT, with visual verification still a retrieval gap**.

This materially tightens the later 503 operating-license chain: Richard M. Wiitanen is directly documented as owner of The Wheel Cafe at 503 in August 1985 (`E-049`), while the OLCC record associates The Wheel Bar & Grill at 503 with **Maurice Enterprises Inc** in the license cycle ending 31 March 2009 (`E-225`). It does **not** supply the date or terms of the Wiitanen sale, prove the 503 deed transfer, or establish that the business and real estate changed hands on the same day.

## D & S Incorporated — lead only, not accepted proof

A tertiary address-history aggregator associates **D & S Incorporated** at 503 Main with **Sheila Wiitanen (President)** and **Richard M. Wiitanen (Secretary)** and also lists The Wheel Bar & Grill contacts at that address:

https://www.addresshistory.com/503-main-st-oregon-city-or-97045

The same page warns that its records combine multiple sources and may contain duplicates or contradictory information. Its asserted dates are not treated as formation/occupancy proof.

The official Oregon Secretary of State business-registry route was tested, but the historical search path encountered access/security blocking in this session. Therefore the original D & S filing, formation date, registry number, registered office, and entity history remain a **RETRIEVAL GAP / UNVERIFIED LEAD**. A registry number previously surfaced in conversational research (**005432-80**) was **not independently verified in an official record during this pass and is not accepted as evidence**.

Do not infer that D & S Incorporated was the legal vehicle that bought The Wheel from Raye until the state filing and transaction/license records establish that relationship.

## 505 Main — status after targeted pass

No new deed proving Dick/Sheila's acquisition of 505 was recovered online. Existing direct anchors remain:

- `E-030`: **6 April 1988** Oregon City Manager's Report identifies **The Dug Inn (formerly The Brass Rail), 505 Main**, with a change-of-ownership application from **Dick or Sheila Wiitanen** to the Cotterells.
- later municipal permit evidence identifies **Richard Martin Wiitanen** on the 505 owner line, independently supporting continuing 505 real-estate association long after the tavern-operator changes.

A third-party property/tax-data aggregation for tax year 2010 lists **Richard M. Wiitanen & Sheila J. Wiitanen** at 505 and separately lists Maurice/Shahtout-related ownership data at 503. Because the original assessor roll/deed image was not recovered, this remains a **lead**, not new deed evidence. Continue `MF-034` for the 505 parcel-first owner/deed-reference chain.

## What this changes

### 503 Main

The documentary bracket for the later Wheel business chain is now tighter:

1. Family history: Raye owned The Wheel business and sold it to Dick/Sheila; exact transfer date open.
2. **By Aug. 1985:** direct newspaper evidence names **Richard M. Wiitanen** as owner of The Wheel Cafe at 503 (`E-049`).
3. **OLCC license cycle ending 31 Mar. 2009:** official indexed state-license text names **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill, 503 Main** (`E-225`), pending visual page verification.
4. Exact **Wiitanen → later buyer/licensee** business-transfer date and exact 503 real-estate conveyance remain unresolved.

### 505 Main

The pass does not change the controlling sequence: Dick/Sheila's Brass Rail operation, later real-estate ownership, 1988 transfer role, later return/control and 505 Tavern rename remain separate from Raye's 503 history. The exact 505 vesting deed remains open under `MF-034`.

## Best next sources

1. **Oregon Secretary of State — D & S Incorporated original filing/history**: verify entity identity, registry number, formation date, officers, registered office, and any 503 address before using the entity in the Wheel transaction narrative. Do not pay for a special inactive-business search without project-steward authorization.
2. **503 Main parcel-first chronological ownership/deed-reference chain** using account **00572650 / tax lot 2-2E-31AB-08200**: recover the deed by which Dick/Sheila acquired 503 and the deed by which they later conveyed it.
3. **OLCC historical change-of-ownership/license file for The Wheel / 503 Main**, especially between the August 1985 Richard Wiitanen anchor and the Maurice Enterprises license record, to date the operating-business transfer independently of the deed.
4. Continue **MF-034** separately for 505; do not use a 503 corporation/license record to infer 505 ownership.

No email, records request, paid search, or purchase was made in this pass.
''', encoding="utf-8")

append_once("evidence/source-register.md", f"## {SID_CEM} —", f'''## {SID_CEM} — Oregon City Mausoleum Burial List, Raye W. Grisham / maiden Weaver
Type: Official municipal cemetery register PDF; **VISUALLY VERIFIED** 5 September 2026.  
Institution: City of Oregon City.  
Document: **Mausoleum Burial List by Last Name**, dated **5 September 2019**.  
Page: PDF page 49 / viewer index 48.  
URL: https://www.orcity.org/DocumentCenter/View/646/Mausoleum-Burial-List-by-Last-Name---September-2019-PDF  
Related evidence/person: `{EID_CEM}` / `P-006`.  
Capture: `evidence/source-captures/503-505-grisham-wiitanen-online-pass-2026-09-05.md`.  
Notes: Direct row records **GRISHAM, RAYE, W., maiden WEAVER**, death 6/30/2012, age 94, burial 11/2/2012, niche 97. Age conflicts with `S-250` obituary's 93; preserve both.''')

append_once("evidence/source-register.md", f"## {SID_OBIT} —", f'''## {SID_OBIT} — The Oregonian obituary for Raye W. Grisham, 11 July 2012
Type: Newspaper obituary webpage / family identity source; page text directly inspected 5 September 2026.  
Publication: **The Oregonian**.  
Publication date: **11 July 2012**.  
URL: https://obits.oregonlive.com/us/obituaries/oregon/name/raye-grisham-obituary?id=25350789  
Related evidence/people: `{EID_OBIT}` / `P-006`, `P-008`, `P-022`.  
Capture: `evidence/source-captures/503-505-grisham-wiitanen-online-pass-2026-09-05.md`.  
Notes: Obituary identifies Raye W. Grisham, age 93, birth 30 Dec. 1918, death 30 June 2012; daughters Carol Stover and Sheila Wiitanen; deceased husbands Floyd La Farlette and Cliff Grisham. It does not mention The Wheel or either Main Street address.''')

append_once("evidence/source-register.md", f"## {SID_OLCC} —", f'''## {SID_OLCC} — OLCC licenses-by-type historical PDF, The Wheel Bar & Grill / Maurice Enterprises Inc
Type: Official state liquor-license list; **OCR/TEXT ONLY / OFFICIAL INDEXED PDF TEXT — page-image retrieval gap**.  
Agency: Oregon Liquor Control Commission.  
URL: https://www.olcc.state.or.us/pdfs/licensesbytype.pdf  
Indexed row: **THE WHEEL BAR & GRILL — MAURICE ENTERPRISES INC — 503 MAIN ST, OREGON CITY, OR 97045 — license 104145 — expires 3/31/09**.  
Related evidence/building/business: `{EID_OLCC}` / `B-001` / `BUS-004`.  
Capture: `evidence/source-captures/503-505-grisham-wiitanen-online-pass-2026-09-05.md`.  
Notes: The direct PDF open/page-image route failed in this session, so retain OCR/TEXT ONLY status. The row establishes a later state-license association but not the Wiitanen sale date or real-estate title.''')

append_once("evidence/evidence-register.md", f"## {EID_CEM} —", f'''## {EID_CEM} — Oregon City cemetery register identifies Raye W. Grisham's maiden name as Weaver
Source: `{SID_CEM}`  
Related person: `P-006`  
Type: Official municipal cemetery register; visually verified  
Claims:
- City of Oregon City mausoleum register directly records **GRISHAM, RAYE, W.**, maiden name **WEAVER**.
- It records death **30 June 2012**, burial **2 November 2012**, niche 97, and age **94**.
- This directly supports **Weaver** as Raye's maiden surname; combined with independently established married surnames, the archive may describe her surname sequence as Weaver → LaFarlette → Grisham.
- The age-94 field conflicts with `S-250` / `{EID_OBIT}`, which reports age 93 and prints birth 30 Dec. 1918 / death 30 Jun. 2012. Preserve the conflict.
- The cemetery record does not establish a 503/505 business or property transaction.
Classification: **DOCUMENTED / DIRECT** for the municipal row and maiden-name field; **UNRESOLVED CONFLICT** for reported age.  
Confidence: **Very High** for the visually verified row; age conflict retained.''')

append_once("evidence/evidence-register.md", f"## {EID_OBIT} —", f'''## {EID_OBIT} — Raye W. Grisham obituary directly confirms Sheila Wiitanen as daughter and husband sequence
Source: `{SID_OBIT}`  
Related people: `P-006`, `P-008`, `P-022`  
Type: Contemporary newspaper obituary / family identity evidence  
Claims:
- The Oregonian obituary published **11 July 2012** identifies **Raye W. Grisham**, birth **30 Dec. 1918**, death **30 Jun. 2012**, age **93**.
- It names daughters **Carol Stover and Sheila Wiitanen**.
- It says Raye was preceded in death by husbands **Floyd La Farlette** and **Cliff Grisham**.
- It independently corroborates the Raye→Sheila family relationship relevant to the later Grisham→Wiitanen Wheel business history.
- It does **not** mention The Wheel, 503 Main, 505 Main, or a business/property transfer.
- Its age 93 conflicts with the municipal cemetery row's age 94 (`{EID_CEM}`), although the obituary's printed birth/death dates are consistent with age 93.
Classification: **DOCUMENTED / DIRECT** for the obituary wording and relationships; no address/business-transfer inference.  
Confidence: **High** for family/identity facts as published obituary evidence; age conflict preserved.''')

append_once("evidence/evidence-register.md", f"## {EID_OLCC} —", f'''## {EID_OLCC} — OLCC indexed license text places Maurice Enterprises Inc with The Wheel Bar & Grill at 503 Main
Source: `{SID_OLCC}`  
Related building/business: `B-001` / `BUS-004`  
Type: Official state liquor-license list text; original PDF page not visually recovered in this session  
Claims:
- Official OLCC indexed PDF text lists **THE WHEEL BAR & GRILL** with licensee **MAURICE ENTERPRISES INC** at **503 MAIN ST, OREGON CITY, OR 97045**.
- The row gives license number **104145** and expiration **31 March 2009**.
- This provides an independent later operating-license endpoint after `E-049`'s August 1985 Richard M. Wiitanen ownership anchor.
- It does not state when the Wiitanens sold The Wheel business, who purchased the 503 real estate, whether business and property transfers were simultaneous, or whether Maurice Enterprises held title.
- Direct PDF/page-image retrieval failed in this session, so the evidence remains **OCR/TEXT ONLY** pending visual verification.
Classification: **OCR/TEXT ONLY** from an official state PDF index; **RETRIEVAL GAP** for page-image certification.  
Confidence: **High** for the indexed state-license row; exact transfer mechanics/date unresolved.''')

append_once("database/sources.yml", f"  - id: {SID_CEM}\n", f'''  - id: {SID_CEM}
    name: "Oregon City Mausoleum Burial List — Raye W. Grisham / maiden Weaver"
    url: "https://www.orcity.org/DocumentCenter/View/646/Mausoleum-Burial-List-by-Last-Name---September-2019-PDF"
    type: "Official municipal cemetery register PDF; visually verified"
    notes: "PDF page 49 / viewer index 48 directly records GRISHAM RAYE W., maiden WEAVER, death 6/30/2012, age 94, burial 11/2/2012; age conflicts with S-250 obituary's 93."
    related_people: [P-006]
''')
append_once("database/sources.yml", f"  - id: {SID_OBIT}\n", f'''  - id: {SID_OBIT}
    name: "The Oregonian obituary — Raye W. Grisham, 11 July 2012"
    url: "https://obits.oregonlive.com/us/obituaries/oregon/name/raye-grisham-obituary?id=25350789"
    type: "Newspaper obituary webpage / family identity source"
    notes: "Names daughter Sheila Wiitanen and deceased husbands Floyd La Farlette and Cliff Grisham; gives birth 12/30/1918, death 6/30/2012, age 93. Does not mention The Wheel or 503/505."
    related_people: [P-006, P-008, P-022]
''')
append_once("database/sources.yml", f"  - id: {SID_OLCC}\n", f'''  - id: {SID_OLCC}
    name: "OLCC licenses-by-type historical PDF — The Wheel Bar & Grill / Maurice Enterprises Inc"
    url: "https://www.olcc.state.or.us/pdfs/licensesbytype.pdf"
    type: "Official state liquor-license list; OCR/TEXT ONLY pending page-image verification"
    notes: "Indexed row: THE WHEEL BAR & GRILL; MAURICE ENTERPRISES INC; 503 MAIN ST, OREGON CITY; license 104145; expires 3/31/09. Direct PDF page retrieval failed in this session."
    related_businesses: [BUS-004]
    related_buildings: [B-001]
''')

append_once("database/evidence.yml", f"  - id: {EID_CEM}\n", f'''  - id: {EID_CEM}
    name: "Oregon City cemetery register identifies Raye W. Grisham maiden name as Weaver"
    type: "Official municipal cemetery register; visually verified"
    claims:
      - "Raye W. Grisham is directly recorded with maiden name WEAVER."
      - "Death 6/30/2012; burial 11/2/2012; age field 94."
      - "Age conflicts with E-224 obituary age 93; preserve both source statements."
      - "This is identity evidence, not a 503/505 business or property transaction."
    confidence: "Very High for the visually verified municipal row; age conflict unresolved"
    related_sources: [S-249]
    related_people: [P-006]
''')
append_once("database/evidence.yml", f"  - id: {EID_OBIT}\n", f'''  - id: {EID_OBIT}
    name: "Raye W. Grisham obituary confirms Sheila Wiitanen as daughter and husband sequence"
    type: "Newspaper obituary / family identity evidence"
    claims:
      - "The Oregonian obituary gives Raye W. Grisham birth 12/30/1918, death 6/30/2012, age 93."
      - "Names daughters Carol Stover and Sheila Wiitanen."
      - "Names deceased husbands Floyd La Farlette and Cliff Grisham."
      - "Does not mention The Wheel, 503 Main, 505 Main, or a transfer."
    confidence: "High for published family/identity wording; age conflict with E-223 retained"
    related_sources: [S-250]
    related_people: [P-006, P-008, P-022]
''')
append_once("database/evidence.yml", f"  - id: {EID_OLCC}\n", f'''  - id: {EID_OLCC}
    name: "OLCC indexed license text places Maurice Enterprises Inc with The Wheel Bar & Grill at 503 Main"
    type: "Official state liquor-license list text; OCR/TEXT ONLY"
    claims:
      - "OLCC indexed text lists THE WHEEL BAR & GRILL, MAURICE ENTERPRISES INC, 503 MAIN ST OREGON CITY, license 104145, expires 3/31/09."
      - "Provides a later operating-license endpoint after Richard M. Wiitanen's August 1985 owner anchor."
      - "Does not prove the Wiitanen business-sale date, real-estate conveyance, or simultaneous transfer."
      - "Direct PDF page-image retrieval failed; visual certification remains a retrieval gap."
    confidence: "High for official indexed license text; pending visual page verification"
    related_sources: [S-251]
    related_buildings: [B-001]
    related_businesses: [BUS-004]
''')

replace_once("people/profiles/raye-grisham.md",
             "- Related evidence: `E-007`, `E-009`, `E-019`, `E-022`",
             f"- Related evidence: `E-007`, `E-009`, `E-019`, `E-022`, `{EID_CEM}`, `{EID_OBIT}`")
replace_once("people/profiles/raye-grisham.md",
             "- **Raye LaFarlette and Raye Grisham are the same woman**, Rodney Young's grandmother.\n- First marriage: **LaFarlette** (with Floyd LaFarlette, `P-022`).",
             f"- **Raye LaFarlette and Raye Grisham are the same woman**, Rodney Young's grandmother.\n- The City of Oregon City mausoleum register directly records her maiden name as **Weaver** (`{EID_CEM}`), so the supported surname sequence is **Raye Weaver → Raye LaFarlette → Raye Grisham**.\n- First marriage: **LaFarlette** (with Floyd LaFarlette, `P-022`).")
replace_once("people/profiles/raye-grisham.md",
             "Family history places Raye in the continuing Wheel operation at 503. Victor (`P-010`) independently managed the restaurant portion during Raye Grisham's years and the early Dick/Sheila period (`E-007`).",
             f"Family history places Raye in the continuing Wheel operation at 503. Victor (`P-010`) independently managed the restaurant portion during Raye Grisham's years and the early Dick/Sheila period (`E-007`).\n\nThe **11 July 2012 Oregonian obituary** independently names **Sheila Wiitanen as Raye's daughter** and names deceased husbands **Floyd La Farlette** and **Cliff Grisham** (`{EID_OBIT}`). The obituary does not mention The Wheel or either Main Street property, so it corroborates family identity rather than a business transaction. Its age 93 conflicts with the City cemetery row's age 94; the conflict is retained.")

replace_once("people/profiles/sheila-wiitanen.md",
             "Sheila was the daughter of Floyd and Raye LaFarlette.",
             f"Sheila was the daughter of Floyd and Raye LaFarlette. The 11 July 2012 Oregonian obituary for Raye independently names **Sheila Wiitanen as Raye's daughter** (`{EID_OBIT}`).")

replace_once("people/profiles/richard-dick-wiitanen.md",
             "An August 1985 *Oregonian* report independently names **Richard M. Wiitanen** as owner of The Wheel Cafe business at 503 (`E-049`).",
             f"An August 1985 *Oregonian* report independently names **Richard M. Wiitanen** as owner of The Wheel Cafe business at 503 (`E-049`). Official OLCC indexed license text later associates **Maurice Enterprises Inc** with **The Wheel Bar & Grill, 503 Main**, license 104145 expiring 31 March 2009 (`{EID_OLCC}`; OCR/TEXT ONLY pending page-image verification). This narrows the later business-successor bracket but does not date Richard/Sheila's sale or the 503 deed transfer.")

replace_once("businesses/the-wheel.md",
             "- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`",
             f"- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`, `{EID_OLCC}`")
replace_once("businesses/the-wheel.md",
             "Oregon City Commission minutes of **7 June 1967** place \"the Wheel\" at **503 Main Street** (`E-025`). Newspapers document **Wheel Cafe**, **Wheel Restaurant**, and **The Wheel Cafe** at this location; August 1985 reporting identifies **Richard M. Wiitanen** as owner of The Wheel Cafe (`E-049`).",
             f"Oregon City Commission minutes of **7 June 1967** place \"the Wheel\" at **503 Main Street** (`E-025`). Newspapers document **Wheel Cafe**, **Wheel Restaurant**, and **The Wheel Cafe** at this location; August 1985 reporting identifies **Richard M. Wiitanen** as owner of The Wheel Cafe (`E-049`). Official OLCC indexed license text later lists **The Wheel Bar & Grill — Maurice Enterprises Inc — 503 Main — license 104145 — expires 31 March 2009** (`{EID_OLCC}`). That state-list row remains OCR/TEXT ONLY until the original PDF page can be visually opened, and it does not prove the exact Wiitanen sale or deed date.")
replace_once("businesses/the-wheel.md",
             "- Richard M. Wiitanen is independently documented as owner of **The Wheel Cafe business at 503 Main** in August 1985 (`E-049`).",
             f"- Richard M. Wiitanen is independently documented as owner of **The Wheel Cafe business at 503 Main** in August 1985 (`E-049`).\n- OLCC indexed license text later identifies **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill at 503 Main**, license 104145 expiring **31 March 2009** (`{EID_OLCC}`; OCR/TEXT ONLY pending visual page verification).")

replace_once("buildings/503-main.md",
             "`E-193`, `E-194`, `E-195`, `E-197`, `E-213`",
             f"`E-193`, `E-194`, `E-195`, `E-197`, `E-213`, `{EID_OLCC}`")
replace_once("buildings/503-main.md",
             "`S-213`, `S-214`, `S-215`, `S-217`, `S-239`",
             f"`S-213`, `S-214`, `S-215`, `S-217`, `S-239`, `{SID_OLCC}`")
replace_once("buildings/503-main.md",
             "- Oregonian 1985 (`E-048`, `E-049`): **The Wheel Cafe, 503 Main St.**; **Richard M. Wiitanen** named as owner in August 1985.",
             f"- Oregonian 1985 (`E-048`, `E-049`): **The Wheel Cafe, 503 Main St.**; **Richard M. Wiitanen** named as owner in August 1985.\n- OLCC indexed license text (`{EID_OLCC}` / `{SID_OLCC}`): **The Wheel Bar & Grill — Maurice Enterprises Inc — 503 Main**, license 104145, expires 31 March 2009. **OCR/TEXT ONLY** pending visual PDF-page recovery; this is a business-license endpoint, not deed proof.")
replace_once("buildings/503-main.md",
             "- Locate the **later transaction in which Dick and Sheila sold both The Wheel business and the 503 building**, including purchaser, date, deed, liquor-license transfer, and business-sale documents.",
             f"- Locate the **later transaction in which Dick and Sheila sold both The Wheel business and the 503 building**, including purchaser, date, deed, liquor-license transfer, and business-sale documents. Use `{EID_OLCC}`'s later Maurice Enterprises license association to bracket the business side without assuming the real-estate transfer occurred simultaneously.")

replace_once("timelines/503-main.md",
             "| Apr.–Aug. 1985 | **The Wheel Cafe, 503 Main**; Richard Wiitanen named business owner. | **Exact primary**; does not date property purchase. | `E-048`, `E-049`; `S-055`–`S-057` |",
             f"| Apr.–Aug. 1985 | **The Wheel Cafe, 503 Main**; Richard Wiitanen named business owner. | **Exact primary**; does not date property purchase. | `E-048`, `E-049`; `S-055`–`S-057` |\n| OLCC license cycle ending 31 Mar. 2009 | **The Wheel Bar & Grill, 503 Main**; licensee **Maurice Enterprises Inc**, license 104145. | **OCR/TEXT ONLY from official state PDF index**; page-image retrieval gap; does not date business sale or deed transfer. | `{EID_OLCC}`; `{SID_OLCC}` |")

replace_once("registers/business-timeline.md",
             "| Apr.–Aug. 1985 | The Wheel Cafe | `BUS-004` | `E-048`, `E-049` | Very High | Lottery outlet at 503 Main St.; Richard M. Wiitanen named owner. Working family interpretation is that the Grisham → Wiitanen transition was a sale of the 503 business; exact transaction date/terms pending. |",
             f"| Apr.–Aug. 1985 | The Wheel Cafe | `BUS-004` | `E-048`, `E-049` | Very High | Lottery outlet at 503 Main St.; Richard M. Wiitanen named owner. Working family interpretation is that the Grisham → Wiitanen transition was a sale of the 503 business; exact transaction date/terms pending. |\n| OLCC license cycle ending 31 Mar. 2009 | The Wheel Bar & Grill | `BUS-004` | `{EID_OLCC}` | High official indexed text; visual page pending | OLCC indexed license row names Maurice Enterprises Inc at 503 Main, license 104145. This is a later operating-license endpoint, not proof of the Wiitanen sale date or 503 title transfer. |")

# Update YAML sidecars for existing entities affected by the new evidence.
replace_once("database/people.yml",
             "notes: Woman. Raye LaFarlette and Raye Grisham are the same person; the surname change followed divorce/remarriage and is not evidence of a Wheel business transfer. Bought The Wheel at 503 Main. The Wheel was never at 505. Previously recorded as possibly male Ray Grisham at 505; superseded August 2026. Not the same person as Ray Hansen.",
             "notes: Woman. Raye LaFarlette and Raye Grisham are the same person; City cemetery evidence now records maiden name Weaver, supporting the surname sequence Weaver → LaFarlette → Grisham. The surname change followed marriage/divorce/remarriage and is not evidence of a Wheel business transfer. The 2012 Oregonian obituary independently names Sheila Wiitanen as her daughter and Floyd La Farlette / Cliff Grisham as deceased husbands. Bought The Wheel at 503 Main. The Wheel was never at 505. Previously recorded as possibly male Ray Grisham at 505; superseded August 2026. Not the same person as Ray Hansen.")
replace_once("database/people.yml",
             "notes: Oregonian August 1985 names Richard M. Wiitanen as owner of The Wheel Cafe business at 503 Main. Family history says Dick and Sheila ran Brass Rail at 505 before owning that building, then later purchased the 505 real estate from Mrs. Nesmeth/Nemeth. Before selling the business to their son Mitch in March 1991, they renamed it 505 Tavern. A 2017 permit confirms continuing 505 property interest. Died November 2024; the 505 building then passed through his estate to Rodney and Mitch.",
             "notes: Oregonian August 1985 names Richard M. Wiitanen as owner of The Wheel Cafe business at 503 Main. Later OLCC indexed text names Maurice Enterprises Inc as licensee for The Wheel Bar & Grill at 503, license 104145 expiring 3/31/09; this brackets the later business succession but does not date the Wiitanen sale or 503 deed. Family history says Dick and Sheila ran Brass Rail at 505 before owning that building, then later purchased the 505 real estate from Mrs. Nesmeth/Nemeth. Before selling the business to their son Mitch in March 1991, they renamed it 505 Tavern. A 2017 permit confirms continuing 505 property interest. Died November 2024; the 505 building then passed through his estate to Rodney and Mitch.")

replace_once("database/businesses.yml",
             "notes: The Wheel was only at 503 Main and was never a 505 Main business. Raye LaFarlette / Raye Grisham is the same person and bought The Wheel at 503; the surname change is not a business transfer. Documented as Wheel Cafe at 5th and Main by 1960, Wheel Restaurant in the 1967 fire article, and The Wheel Cafe at 503 Main in 1985 with Richard M. Wiitanen as owner. June 7 1967 Commission minutes place the Wheel at 503 Main Street. A 2017 article's phrase \"The Wheel Tavern\" is source wording only; family correction says it was never an official business name. The former Mrs. Nemeth/Nesmeth property-purchase claim does not belong to 503; that purchase was 505 Main.",
             "notes: The Wheel was only at 503 Main and was never a 505 Main business. Raye LaFarlette / Raye Grisham is the same person and bought The Wheel at 503; the surname change is not a business transfer. Documented as Wheel Cafe at 5th and Main by 1960, Wheel Restaurant in the 1967 fire article, and The Wheel Cafe at 503 Main in 1985 with Richard M. Wiitanen as owner. OLCC indexed license text later names Maurice Enterprises Inc as licensee for The Wheel Bar & Grill at 503, license 104145 expiring 3/31/09; this is a later operating-license endpoint, not a deed/sale date. June 7 1967 Commission minutes place the Wheel at 503 Main Street. A 2017 article's phrase \"The Wheel Tavern\" is source wording only; family correction says it was never an official business name. The former Mrs. Nemeth/Nesmeth property-purchase claim does not belong to 503; that purchase was 505 Main.")
replace_once("database/businesses.yml",
             "      - E-206\n  - id: BUS-005",
             f"      - E-206\n      - {EID_OLCC}\n  - id: BUS-005")

# Insert B-001 sidecar links without touching B-002.
replace_once("database/buildings.yml",
             "      - E-217\n\n      - E-219\n    related_sources:",
             f"      - E-217\n      - {EID_OLCC}\n\n      - E-219\n    related_sources:")
replace_once("database/buildings.yml",
             "      - S-243\n\n      - S-245\n    related_maps:",
             f"      - S-243\n      - {SID_OLCC}\n\n      - S-245\n    related_maps:")

# Sharpen the existing cross-address research lead without adding a redundant RL ID.
replace_once("evidence/research-leads.md",
             "## RL-008 — Separate 503 Business / 505 Property Ownership Chains",
             f"## RL-008 — Separate 503 Business / 505 Property Ownership Chains\n\n**5 September 2026 update:** `E-223` / `S-249` now records Raye's maiden name **Weaver**; `E-224` / `S-250` independently confirms **Sheila Wiitanen as Raye's daughter**. For 503, `E-049` directly names Richard M. Wiitanen as Wheel Cafe owner in August 1985, while `{EID_OLCC}` / `{SID_OLCC}` later names **Maurice Enterprises Inc** as The Wheel Bar & Grill licensee at 503 in the OLCC cycle expiring 31 March 2009 (**OCR/TEXT ONLY pending page-image verification**). Highest-value 503 work is now the parcel-first deed chain for account **00572650 / 2-2E-31AB-08200**, plus OLCC change-of-ownership records between the 1985 and 2009 endpoints. A tertiary D & S Incorporated association is retained only as a lead; the official Oregon corporate filing and any previously mentioned registry number remain unverified. Keep this completely separate from `MF-034`'s 505 deed chain.\n")

# Update open-question wording with the new endpoint.
replace_once("evidence/open-questions.md",
             "- Richard M. Wiitanen is independently documented as owner of The Wheel Cafe business at 503 in August 1985 (`E-049`).",
             f"- Richard M. Wiitanen is independently documented as owner of The Wheel Cafe business at 503 in August 1985 (`E-049`).\n- Official OLCC indexed license text later names **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill, 503 Main**, license 104145 expiring 31 March 2009 (`{EID_OLCC}` / `{SID_OLCC}`; OCR/TEXT ONLY pending visual PDF-page recovery). This narrows the later business-successor bracket but does not date the Wiitanen sale or 503 real-estate conveyance.")

append_once("indexes/id-crosswalk.md", f"## {SID_CEM} / {EID_CEM}", f'''## {SID_CEM} / {EID_CEM} — Raye Weaver identity anchor

| Record | Links | Notes |
| --- | --- | --- |
| `{SID_CEM}` / `{EID_CEM}` | `P-006` | Visually verified City cemetery row records Raye W. Grisham's maiden name as Weaver; age 94 conflicts with obituary age 93. |
| `{SID_OBIT}` / `{EID_OBIT}` | `P-006`, `P-008`, `P-022` | Oregonian obituary directly names Sheila Wiitanen as Raye's daughter and Floyd La Farlette / Cliff Grisham as deceased husbands; no 503/505 business claim. |
| `{SID_OLCC}` / `{EID_OLCC}` | `B-001`, `BUS-004`, compare `E-049` | Official OLCC indexed text names Maurice Enterprises Inc at The Wheel Bar & Grill, 503 Main, license 104145 expiring 3/31/09; OCR/TEXT ONLY pending visual page verification. |
''')

append_once("registers/research-log.md", "Grisham/Wiitanen targeted 503/505 pass — 5 September 2026", f'''## Grisham/Wiitanen targeted 503/505 pass — 5 September 2026

- Visually verified the Oregon City cemetery row recording **Raye W. Grisham — maiden Weaver** (`{SID_CEM}` / `{EID_CEM}`), preserving its age-94 conflict with the obituary.
- Recovered the 11 July 2012 Oregonian obituary naming **Sheila Wiitanen as Raye's daughter** and Floyd La Farlette / Cliff Grisham as deceased husbands (`{SID_OBIT}` / `{EID_OBIT}`).
- Recovered official OLCC indexed license text naming **Maurice Enterprises Inc** for **The Wheel Bar & Grill, 503 Main**, license 104145 expiring 31 March 2009 (`{SID_OLCC}` / `{EID_OLCC}`); original PDF page remains a visual-retrieval gap.
- Tested the **D & S Incorporated** lead. Only tertiary address-history aggregation was recovered; official Oregon corporate filing remained inaccessible through the available registry route. Previously surfaced registry number wording remains unverified and is not accepted into evidence.
- No new 505 vesting deed was recovered; `MF-034` remains the controlling manual deed-chain route. No outreach or paid search was initiated.
''')

print("Integrated targeted Grisham/Wiitanen pass with S-249..S-251 and E-223..E-225.")
