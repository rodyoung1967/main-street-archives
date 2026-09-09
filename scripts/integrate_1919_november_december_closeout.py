#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DATE = "2026-09-08"
MARKER = "<!-- 1919 November-December annual online closeout — 2026-09-08 -->"
YAML_MARKER = "# 1919 November-December annual online closeout — 2026-09-08"
NOV_CAPTURE = "evidence/source-captures/1919-november-enterprise-visual-review-2026-09-08.md"
DEC_CAPTURE = "evidence/source-captures/1919-december-enterprise-visual-review-2026-09-08.md"
CLOSE_CAPTURE = "evidence/source-captures/1919-online-source-class-closeout-2026-09-08.md"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


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


def max_num(path, prefix):
    nums = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums:
        raise RuntimeError(f"No {prefix} IDs found in {path}")
    return max(nums)


def update_yaml_relation(path, entity_id, field, value):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)", text)
    if not m:
        return False
    block = m.group(0)
    inline = re.search(rf"(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$", block)
    if inline:
        vals = [v.strip() for v in inline.group(1).split(',') if v.strip()]
        if value in vals:
            return False
        vals.append(value)
        repl = f"    {field}: [" + ", ".join(vals) + "]"
        block = block[:inline.start()] + repl + block[inline.end():]
    else:
        if not block.endswith("\n"):
            block += "\n"
        block += f"    {field}: [{value}]\n"
    p.write_text(text[:m.start()] + block + text[m.end():], encoding="utf-8")
    return True


if Path(CLOSE_CAPTURE).exists() and MARKER in read(CLOSE_CAPTURE):
    print("1919 closeout already integrated; refusing duplicate integration.")
    sys.exit(0)

# Allocate at runtime after the workflow rebases onto the latest main so parallel work wins.
s0 = max_num("evidence/source-register.md", "S")
e0 = max_num("evidence/evidence-register.md", "E")
mf0 = max_num("MANUAL-FOLLOWUP.md", "MF")
S_NOV, S_DEC, S_CLOSE = [f"S-{n:03d}" for n in (s0 + 1, s0 + 2, s0 + 3)]
E_NOV, E_DEC, E_CLOSE = [f"E-{n:03d}" for n in (e0 + 1, e0 + 2, e0 + 3)]
MF_PERMIT = f"MF-{mf0 + 1:03d}"

nov = f'''# November 1919 Oregon City Enterprise scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 32/32 online-exposed November Enterprise pages inspected from original scans.**  
Annual status after final closeout: **1919 ONLINE COMPLETE**; inaccessible Banner-Courier remains manual work under `MF-030`.

Archive IDs: source `{S_NOV}`; evidence `{E_NOV}`.

## Scope

| Title | Issues | Pages | Result |
| --- | --- | ---: | --- |
| *Oregon City Enterprise* | 7, 14, 21, 28 Nov. 1919 | **32/32** | Every preserved page visually inspected |
| *The Banner-Courier* | 6, 13, 20, 27 Nov. 1919 | **0 online** | Manual microfilm gap, `MF-030` |

Preserved scans: `newspapers/oregon-city-enterprise/1919-november/`  
Manifest: `newspapers/oregon-city-enterprise/1919-november/manifest.json`  
Banner-Courier gap manifest: `newspapers/banner-courier/1919-november/manifest.json`

OCR/text was used only to locate candidates. Certification is based on visual inspection of the original scanned pages.

## 28 November — B. J. Staats Hardware selling-out advertisement

Page 8 visibly advertises **B. J. Staats Hardware Co.** under the heading **“Selling Out Hardware and Implements”** and directly prints **520–22 Main Street**. The ad says Staats is going out of the hardware business and intends to sell the stock quickly.

This is direct dated business/address and liquidation-intent evidence. It does **not** prove the final closure date, sale completion, property ownership, lease termination, or transfer of the stock/business.

The address creates an unresolved conflict with the separately visually verified December 1919 CCHS photograph (`S-147` / `E-132` / `IMG-0723`), whose institutional catalog metadata identifies the photographed B. J. Staats Hardware storefront as **516 Main Street** while the image visibly shows **Closing Out Sale** / **Big Sale** signage. The same business name and sale context make the records important to reconcile, but neither source is silently corrected to match the other. Possibilities such as a multi-bay storefront, address-range usage, later cataloging error, or a move remain hypotheses until a contemporary directory, deed, assessment, map, or other primary address control resolves the discrepancy.

## Other November context

- **7 Nov.:** all eight pages reviewed; the Enterprise's own “Making a Newspaper” / plant material is unrelated to 501/503/505 construction.
- **14 Nov.:** all eight pages reviewed; construction/real-estate material inspected but no source-explicit 501/503/505/505½ event recovered.
- **21 Nov.:** all eight pages reviewed; a major Oregon City fire destroyed the First Methodist Church / Price Bros. block in the Seventh Street area. It is downtown fire context, not a Fifth/Main target event.
- **28 Nov.:** all eight pages reviewed; aside from the Staats advertisement above, no source-explicit target-number construction/occupancy event was recovered.

## Target-frontage result and limit

Across all 32 November Enterprise pages, no source-explicit **501, 503, 505 or 505½ Main** occupant, construction, demolition, rebuild, remodel, lease, sale, fire, or ownership event was established. This is a bounded result for the reviewed Enterprise pages only. It is not evidence of vacancy or non-use and cannot be projected across the inaccessible Banner-Courier issues.
'''
write(NOV_CAPTURE, nov)

dec = f'''# December 1919 Oregon City Enterprise scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 32/32 online-exposed December Enterprise pages inspected from original scans.**  
Annual status after final closeout: **1919 ONLINE COMPLETE**; inaccessible Banner-Courier remains manual work under `MF-030`.

Archive IDs: source `{S_DEC}`; evidence `{E_DEC}`.

## Scope

| Title | Issues | Pages | Result |
| --- | --- | ---: | --- |
| *Oregon City Enterprise* | 5, 12, 19, 26 Dec. 1919 | **32/32** | Every preserved page visually inspected |
| *The Banner-Courier* | 4, 11, 18, 25 Dec. 1919 | **0 online** | Manual microfilm gap, `MF-030` |

Preserved scans: `newspapers/oregon-city-enterprise/1919-december/`  
Manifest: `newspapers/oregon-city-enterprise/1919-december/manifest.json`  
Banner-Courier gap manifest: `newspapers/banner-courier/1919-december/manifest.json`  
Preservation commit: `6af4401bd27d42a456b90df5610a4b078b39bc67`.

OCR/text was used only as a discovery/navigation aid. Certification is based on visual inspection of the original scanned pages.

## 19 December — Portland House fire at Fifth and Main

Page 5, **“SMALL FIRE ON MAIN,”** directly reports a small fire at the **Portland House at Fifth and Main**, identifies **Mr. and Mrs. Beck** as owners of the Portland House, and describes the Portland House as a **frame structure**, with adjoining buildings also described as frame construction.

This is direct December 1919 Fifth/Main physical-condition and named-owner/business evidence. The article does **not** print a street number, legal description, side of Main, parcel, deed reference, construction date, or modern-building identity. It therefore is **not assigned to 501, 503 or 505 Main** and does not prove continuity with the Portland House visible in the 1896 CCHS photograph.

## Other December context

- **5 Dec.:** fire-damage/repair and rebuilding proceedings involving other downtown property were visually reviewed; no source-explicit 501/503/505/505½ target event was recovered.
- **12 Dec.:** all eight pages reviewed; no source-explicit target-number physical/property event recovered.
- **19 Dec.:** Portland House finding above; no exact target-number assignment.
- **26 Dec.:** all eight pages reviewed; no source-explicit target-number physical/property event recovered.

## Target-frontage result and limit

Across all 32 December Enterprise pages, no source-explicit **501, 503, 505 or 505½ Main** occupant, construction, demolition, rebuild, remodel, lease, sale, fire, or ownership event was established. The Fifth/Main Portland House fire is intersection context only. This is bounded Enterprise coverage and is not evidence of vacancy, non-use, demolition, or absence of an occupant.
'''
write(DEC_CAPTURE, dec)

closeout = f'''# 1919 all-online-source-class closeout

{MARKER}

Closeout level: **ONLINE COMPLETE**  
Source/evidence: `{S_CLOSE}` / `{E_CLOSE}`

This closeout certifies the defined online research pass under `RESEARCH-STANDARD.md`. It does **not** claim that the 503/505 construction date is solved and does **not** claim manual work is complete.

## Newspaper certification

The 1919 Oregon City local-newspaper inventory resolves into three successive/overlapping titles relevant to this project:

| Title | Issue dates accounted for | Online pages visually reviewed | Remaining gap |
| --- | ---: | ---: | --- |
| *Oregon City Enterprise* (`sn00063700`) | **52 Friday issues** | **474/474** | none among the online-exposed Enterprise pages |
| *Oregon City Courier* (`sn00063698`) | **26 issues, 2 Jan.–3 Jul.** | **164/164** | none among the online-exposed Courier pages |
| *The Banner-Courier* (`sn00063699`) | **24 known issues, 17 Jul.–25 Dec.** | **0 online** | entire known run is not exposed in the digitized title; microfilm/manual `MF-030` |
| **Total** | **102 issue dates** | **638/638 online-retrievable pages visually reviewed** | **24 Banner-Courier issues manual** |

Monthly visual totals: Jan 70; Feb 56; Mar 56; Apr 56; May 72; Jun 56; Jul 38; Aug 40; Sep 32; Oct 40; Nov 32; Dec 32 = **638 pages**.

All 638 online-retrievable pages were visually inspected from scanned page images. OCR, text extraction and search were discovery aids only. The missing Banner-Courier run is a precisely documented manual microfilm gap beginning 17 July 1919; its absence from the online platform is never treated as historical absence.

Key 1919 newspaper findings already integrated include Ohio Dentists/J. G. Nash at **507½ Main over Harding's Drug Store** early in the year; Theroux Music House at **210 Seventh** through October; the eight-week cleaner/dyer classified that visibly prints **500 Fifth and Main streets, two doors south of new post office, Phone 260**; Fesznecker moving his tin/repair shop to the building just south of the post office; the Fifth Street Restaurant/W. W. Pollock fine; Gilbert Miller family context; the November Staats liquidation advertisement at **520–22 Main**; and the December Portland House fire at **Fifth and Main**. None supplies direct primary construction proof for the surviving 503/505 buildings.

## Other online source classes

| Class | Online work completed / result |
| --- | --- |
| Directories | Public/indexed routes for the **1919–1920 R. L. Polk Oregon/Washington Gazetteer and Business Directory** were traced to FamilySearch catalog `1439422`, but the target page images require authenticated/restricted access. Ordinary public-copy and catalog/ARK routes were exhausted without asserting directory contents. This is `MF-040` / `1919-D01`, now a restricted/manual closeout item rather than unfinished ordinary-public searching. |
| Maps | The corrected **1911 Sanborn Sheet 16** (`SM-010` / `S-298` / `E-272`) and **1925 Sheet 6** (`SM-008` / `S-021`) are visually reviewed and bracket a material frontage/footprint change. No 1919 Sanborn edition provides a contemporary construction date. The maps establish change by 1925, not the exact year of each rebuild. |
| Municipal | Public/indexed Oregon City historic-document, meeting/minute and related routes were checked in the controlling 1919–1920 access trail/closeout work. No source-explicit online 1919 target permit/improvement file or direct construction record was recovered. The known 2 June 1920 A. Leland/505½ council record remains `MF-041`; surviving 1919–21 permit/improvement files are `{MF_PERMIT}`. |
| Property / title | Current public county systems and online finding aids do not expose the required contemporary target-block assessment/title images. The 1920–25 Block 4 assessment work is `MF-019`; Harding→Wolf/Gates deed/legal-description work is `MF-006`; OHS MSS 1503 Box 19 title abstract is `MF-007`. These are underlying-record/manual tasks, not negative search results. |
| Historic resources | City/SHPO historic-resource material is integrated. The surviving 503 **c.1919** date remains an approximate secondary survey estimate; the surviving 505 is bracketed by primary/official map evidence to **1911–1925**, with **c.1920 tentative** and the older c.1908 survey date superseded. Neither survey estimate is primary construction proof. |
| Photographs | The December 1919 CCHS snow photograph (`S-147` / `E-132` / `IMG-0723`) is visually verified and catalogs B. J. Staats Hardware at **516 Main**, with sale signage visible. The 28 Nov. newspaper ad directly says **520–22 Main**, creating an unresolved address conflict. Existing online photo work has not produced a dated 1919 image proving construction of 503/505. |
| General public/indexed web | The controlling 1919–1920 construction/occupancy closeout and 8 September handoff document that the remaining ordinary public/indexed online routes were worked without resolving the exact 503/505 physical-change date. Remaining high-value routes require restricted/authenticated or manual records. |

## Unresolved conflicts and historical questions

1. **503 construction date:** c.1919 remains a secondary survey estimate, not primary proof.
2. **505 construction date:** primary/official evidence brackets the surviving building between 1911 and 1925; c.1920 remains tentative.
3. **Staats address conflict:** 28 Nov. 1919 Enterprise directly prints **520–22 Main**, while the CCHS December photograph is cataloged **516 Main**. Neither is silently normalized.
4. **Cleaner/dyer wording:** all eight verified advertisements print **500 Fifth and Main streets**, not a normalized “500 Main.”
5. **1919 exact 501/503/505 occupancy:** no direct annual newspaper finding establishes those exact storefront occupants; source silence is not vacancy evidence.
6. **Clem Dollar vs. A. Leland:** Clem Dollar is directly at a pool hall on Main between Fifth/Sixth in Feb. 1920; A. Leland is directly permitted at 505½ in June 1920. Same-hall/operator succession remains unproved.

## Numbered manual-work callouts

1. `MF-030` / `1919-BC01` — inspect **24 Banner-Courier issues, 17 Jul.–25 Dec. 1919**, on Oregon City Public Library microfilm for address, construction, remodel, lease, sign and occupancy evidence.
2. `MF-040` / `1919-D01` — authenticated/restricted **1919–1920 Polk Oregon/Washington Gazetteer** Oregon City address/classified pages; FamilySearch catalog `1439422`.
3. `{MF_PERMIT}` — inspect any surviving **1919–1921 Oregon City building permit, improvement, alteration, sign, sidewalk/street-front or related property files** for 501/503/505/505½ Main and the Fifth/Main target frontage.
4. `MF-019` / `1920-TAX01` — 1920–25 Block 4 assessment/tax records for land/improvement changes, without automatically equating valuation change to construction.
5. `MF-006` / `1922-DEED01` — Harding → S. Wolf / C. Gates deeds and legal descriptions.
6. `MF-007` / `1922-OHS01` — OHS MSS 1503 Series B Box 19 Block 4 Lots 3–4 title abstract.
7. `MF-041` / `1920-MIN01` — actual 2 June 1920 Council minutes and A. Leland application/bond/license/sign material for 505½.

These callouts prevent **ONLINE + MANUAL COMPLETE**, not **ONLINE COMPLETE**. No institutional request was sent and no paid research was authorized.

## Certification statement

**1919 is ONLINE COMPLETE.** Every online-retrievable page in the identified relevant local-newspaper inventory has been visually reviewed; the other applicable ordinary public/indexed online source classes have been audited and integrated; remaining restricted/physical/institutional work is explicitly called out above. Absence of evidence was not treated as evidence of absence. The exact 503/505 construction dates remain historically unresolved despite completion of the online research pass.
'''
write(CLOSE_CAPTURE, closeout)

# Source register
append_once("evidence/source-register.md", MARKER + " source-register", f'''## {S_NOV} — November 1919 Oregon City Enterprise complete online visual-review batch
{MARKER} source-register
Type: Primary newspaper scans plus Banner-Courier retrieval-gap manifest; **32/32 Enterprise pages VISUALLY VERIFIED** 8 September 2026.  
Coverage: Enterprise 7/14/21/28 Nov., 32 pages; Banner-Courier 6/13/20/27 Nov. manual `MF-030`.  
Repository originals: `newspapers/oregon-city-enterprise/1919-november/`; capture `{NOV_CAPTURE}`.  
Related evidence: `{E_NOV}`.  
Notes: 28 Nov. p8 directly advertises B. J. Staats Hardware Co., “Selling Out Hardware and Implements,” **520–22 Main Street**. This conflicts with the separately cataloged December 1919 CCHS **516 Main** Staats photograph; neither address is normalized. No source-explicit 501/503/505/505½ construction/occupancy event was established in the 32 pages.

## {S_DEC} — December 1919 Oregon City Enterprise complete online visual-review batch
Type: Primary newspaper scans plus Banner-Courier retrieval-gap manifest; **32/32 Enterprise pages VISUALLY VERIFIED** 8 September 2026.  
Coverage: Enterprise 5/12/19/26 Dec., 32 pages; Banner-Courier 4/11/18/25 Dec. manual `MF-030`.  
Repository originals: `newspapers/oregon-city-enterprise/1919-december/`; capture `{DEC_CAPTURE}`.  
Related evidence: `{E_DEC}`.  
Notes: 19 Dec. p5 directly reports the Portland House at Fifth and Main, identifies Mr. and Mrs. Beck as owners, and describes it/adjoining buildings as frame construction. No street number or target-building identity is printed; no 501/503/505 assignment is made.

## {S_CLOSE} — 1919 all-online-source-class closeout synthesis
Type: Repository synthesis of visually verified primary scans, official/secondary online source-class work and explicit restricted/manual gaps; **ONLINE COMPLETE certification record**.  
Capture: `{CLOSE_CAPTURE}`.  
Related evidence: `{E_CLOSE}`.  
Notes: 102 local-newspaper issue dates accounted for; 638/638 online-retrievable pages visually reviewed; 24 Banner-Courier issues remain `MF-030`. Other ordinary public/indexed online source classes are closed; restricted/manual records remain explicitly listed.''')

# Evidence register
append_once("evidence/evidence-register.md", MARKER + " evidence-register", f'''## {E_NOV} — November 1919 Enterprise review and B. J. Staats 520–22 Main liquidation address
{MARKER} evidence-register
Type: Primary newspaper visual evidence / monthly complete online batch.  
Source: `{S_NOV}`.  
Claims:
- **32/32 November Enterprise pages** were visually inspected;
- 28 Nov. p8 directly prints **B. J. Staats Hardware Co., 520–22 Main Street** and a selling-out / going-out-of-hardware-business message;
- the address conflicts with CCHS December 1919 catalog metadata placing the visually matching Staats sale storefront at **516 Main** (`E-132`); neither source is corrected by assumption;
- no source-explicit 501/503/505/505½ target construction/occupancy event was established in the reviewed pages;
- four November Banner-Courier issues remain `MF-030` manual microfilm work.
Classification: **DOCUMENTED / DIRECT** for scan-visible wording; **UNRESOLVED CONFLICT** for 516 vs. 520–22; **COVERAGE RESULT ONLY** for no target finding.  
Confidence: **Very High** for page coverage and printed advertisement.

## {E_DEC} — December 1919 Enterprise review and Portland House Fifth/Main fire
Type: Primary newspaper visual evidence / monthly complete online batch.  
Source: `{S_DEC}`.  
Claims:
- **32/32 December Enterprise pages** were visually inspected;
- 19 Dec. p5 directly places the **Portland House at Fifth and Main**, identifies **Mr. and Mrs. Beck** as owners, and describes the Portland House and adjoining buildings as frame construction;
- the article supplies no number, parcel, side-of-street statement, legal description or present-building identity, so it is not assigned to 501/503/505;
- no source-explicit 501/503/505/505½ target construction/occupancy event was established in the reviewed pages;
- four December Banner-Courier issues remain `MF-030` manual microfilm work.
Classification: **DOCUMENTED / DIRECT** for scan-visible Fifth/Main wording and construction material; **INTERSECTION CONTEXT ONLY** for the target frontage.  
Confidence: **Very High** for page coverage and printed report.

## {E_CLOSE} — 1919 ONLINE COMPLETE certification
Type: Annual research-completeness synthesis under `RESEARCH-STANDARD.md`.  
Source: `{S_CLOSE}`.  
Claims:
- the 1919 local-newspaper inventory accounts for **52 Enterprise + 26 Courier + 24 Banner-Courier = 102 issue dates**;
- all **638/638 online-retrievable pages** (474 Enterprise + 164 Courier) were visually reviewed;
- the 24 Banner-Courier issues from 17 Jul.–25 Dec. are precisely documented manual microfilm gaps under `MF-030`;
- applicable ordinary public/indexed online directory, map, municipal, property/title, historic-resource, photograph and general-web routes have been audited/integrated, with remaining restricted/manual routes explicitly called out;
- 1919 therefore meets the repository definition of **ONLINE COMPLETE**, but not ONLINE + MANUAL COMPLETE;
- exact construction dates of the surviving 503 and 505 buildings remain unresolved.
Classification: **RESEARCH-COVERAGE CERTIFICATION**, not historical proof of source silence.  
Confidence: **Very High** for completion state as documented; unresolved for construction dates.''')

# YAML mirrors
append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S_NOV}\n    name: "November 1919 Oregon City Enterprise complete online visual-review batch"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      32/32 November Enterprise pages visually verified. 28 Nov p8 directly prints B. J. Staats Hardware Co. at 520-22 Main Street with selling-out wording; conflicts with CCHS December catalog metadata at 516 Main. Banner-Courier remains MF-030.\n  - id: {S_DEC}\n    name: "December 1919 Oregon City Enterprise complete online visual-review batch"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      32/32 December Enterprise pages visually verified. 19 Dec p5 directly places Portland House at Fifth and Main, names Mr. and Mrs. Beck as owners, and describes frame construction; no numbered target assignment. Banner-Courier remains MF-030.\n  - id: {S_CLOSE}\n    name: "1919 all-online-source-class closeout synthesis"\n    url: https://github.com/rodyoung1967/main-street-archives\n    notes: >-\n      ONLINE COMPLETE certification: 102 local issue dates accounted for; 638/638 online-retrievable pages visually reviewed; 24 Banner-Courier issues and other restricted/manual records remain explicit callouts.\n''')
append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E_NOV}\n    name: "November 1919 Enterprise review and B. J. Staats 520-22 Main liquidation address"\n    type: Primary newspaper visual evidence / complete monthly online batch\n    claims:\n      - 32/32 November 1919 Enterprise pages visually verified.\n      - 28 November page 8 directly prints B. J. Staats Hardware Co. at 520-22 Main Street with selling-out wording.\n      - The 520-22 address conflicts with the separately cataloged December 1919 CCHS Staats photograph at 516 Main; neither source is normalized.\n      - No exact 501, 503, 505 or 505-half target construction or occupancy event was established.\n    confidence: Very High for visible wording; unresolved for address reconciliation\n    related_sources: [{S_NOV}]\n    related_businesses: [BUS-079]\n    related_buildings: [B-015]\n  - id: {E_DEC}\n    name: "December 1919 Enterprise review and Portland House Fifth-Main fire"\n    type: Primary newspaper visual evidence / complete monthly online batch\n    claims:\n      - 32/32 December 1919 Enterprise pages visually verified.\n      - 19 December page 5 directly places Portland House at Fifth and Main, names Mr. and Mrs. Beck as owners, and describes the Portland House and adjoining buildings as frame construction.\n      - No numbered target assignment is made because the article supplies no street number, parcel or present-building identity.\n    confidence: Very High for visible wording; intersection context only for target frontage\n    related_sources: [{S_DEC}]\n    related_businesses: []\n    related_buildings: []\n  - id: {E_CLOSE}\n    name: "1919 ONLINE COMPLETE certification"\n    type: Annual research-coverage certification under RESEARCH-STANDARD.md\n    claims:\n      - 102 relevant local-newspaper issue dates are accounted for.\n      - 638/638 online-retrievable 1919 local-newspaper pages were visually reviewed.\n      - 24 Banner-Courier issues remain MF-030 manual microfilm work.\n      - Other ordinary public/indexed online source classes are audited and remaining restricted/manual routes are explicit callouts.\n      - 1919 is ONLINE COMPLETE but not ONLINE + MANUAL COMPLETE.\n      - Exact 503 and 505 construction dates remain unresolved.\n    confidence: Very High for research-completeness state\n    related_sources: [{S_CLOSE}]\n    related_businesses: []\n    related_buildings: [B-001, B-002]\n''')

# Entity propagation for Staats; preserve existing primary catalog address while adding conflict.
append_once("businesses/b-j-staats-hardware.md", MARKER, f'''## 28 November 1919 newspaper address conflict
{MARKER}

`{S_NOV}` / `{E_NOV}` visually verifies an Enterprise page-eight advertisement reading **B. J. Staats Hardware Co.**, **520–22 Main Street**, under **Selling Out Hardware and Implements**, with wording that Staats was going out of the hardware business. This directly supports liquidation intent by 28 November.

The newspaper address conflicts with the CCHS December 1919 photograph cataloged at **516 Main** (`S-147` / `E-132` / `IMG-0723`), which visibly shows the Staats fascia and sale signs. Preserve both addresses. The current evidence does not establish whether this reflects a multi-bay address range, a move, alternate numbering/use, or later catalog metadata error, and it does not establish the final closure date.
''')
append_once("buildings/516-main.md", MARKER, f'''## November 1919 newspaper-address conflict
{MARKER}

The institutional **516 Main** catalog address for the December Staats photograph now has a direct contemporary conflict: the visually verified **28 November 1919 Enterprise p8** advertisement (`{S_NOV}` / `{E_NOV}`) prints **B. J. Staats Hardware Co., 520–22 Main Street** with selling-out wording. Do not silently replace 516 with 520–22 or vice versa. The photograph itself does not visibly print a street number, so reconciliation requires another contemporary address/property control.
''')

# Structured relations where the entities exist.
for path, eid in [("database/businesses.yml", "BUS-079"), ("database/buildings.yml", "B-015")]:
    update_yaml_relation(path, eid, "related_evidence", E_NOV)
    update_yaml_relation(path, eid, "related_sources", S_NOV)

# Human-readable indexes/timelines.
append_once("registers/address-register.md", MARKER, f'''| 520–22 Main Street | 28 Nov. 1919 | B. J. Staats Hardware Co.; selling-out advertisement | `{E_NOV}` / `{S_NOV}`; direct newspaper address. Conflicts with CCHS December photo metadata at 516 Main; no normalization. |
| Fifth and Main | 19 Dec. 1919 | Portland House; Mr. and Mrs. Beck named owners; frame structure / adjoining frame buildings | `{E_DEC}` / `{S_DEC}`; no street number, parcel, side or present-building identity; intersection context only. |
{MARKER}''')
append_once("registers/business-timeline.md", MARKER, f'''| 28 Nov. 1919 | 520–22 Main | B. J. Staats Hardware Co. | `BUS-079` | `{E_NOV}` | Selling-out ad; conflicts with December CCHS catalog address 516 Main. Does not prove final closure. |
| 19 Dec. 1919 | Fifth and Main, number not printed | Portland House | — | `{E_DEC}` | Mr. and Mrs. Beck named owners; frame structure and adjoining frame buildings; not assigned to 501/503/505. |
{MARKER}''')
append_once("timeline.md", MARKER, f'''## November–December 1919 — Staats address conflict; Portland House fire; online year closeout
{MARKER}

The complete November Enterprise pass (`{S_NOV}` / `{E_NOV}`) visually reviewed **32/32 pages**. On **28 November p8**, B. J. Staats Hardware Co. directly advertises **520–22 Main Street** while selling out its hardware/implement stock. That contemporary address conflicts with the separately visually verified December CCHS photograph cataloged at **516 Main**, where Staats and sale signage are visible. Both sources stand; no address is normalized by assumption.

The complete December Enterprise pass (`{S_DEC}` / `{E_DEC}`) visually reviewed **32/32 pages**. On **19 December p5**, a small-fire report places the **Portland House at Fifth and Main**, names **Mr. and Mrs. Beck** as owners and describes the Portland House and adjoining buildings as frame construction. The report prints no number or parcel and is not assigned to 501/503/505.

The annual closeout (`{S_CLOSE}` / `{E_CLOSE}`) certifies **1919 ONLINE COMPLETE**: **638/638 online-retrievable local-newspaper pages** were visually reviewed across 52 Enterprise and 26 Courier issues; 24 Banner-Courier issue dates remain `MF-030` manual microfilm work. Other ordinary public/indexed online source classes are closed, with restricted/manual records explicitly retained. The exact surviving 503/505 construction dates remain unresolved.
''')
append_once("indexes/id-crosswalk.md", MARKER, f'''## 1919 November–December and annual closeout
{MARKER}

| Source / evidence | Entity / topic | Scope and limit |
| --- | --- | --- |
| `{S_NOV}` / `{E_NOV}` | `BUS-079`; `B-015` conflict context | 32/32 Nov. Enterprise pages; Staats selling-out ad directly **520–22 Main**; CCHS Dec. catalog says **516 Main**. Preserve conflict. |
| `{S_DEC}` / `{E_DEC}` | Fifth/Main Portland House context | 32/32 Dec. Enterprise pages; Mr./Mrs. Beck owners, frame structure; no numbered target assignment. |
| `{S_CLOSE}` / `{E_CLOSE}` | 1919 annual status | **ONLINE COMPLETE**; 638/638 online pages visually reviewed; 24 Banner-Courier issues plus restricted/manual records remain callouts. |
''')

# Construction/occupancy controls and handoff supersession.
append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", MARKER, f'''## November–December 1919 completion and annual certification
{MARKER}

November (`{S_NOV}` / `{E_NOV}`) and December (`{S_DEC}` / `{E_DEC}`) Enterprise are now **32/32 + 32/32 visually verified**. Neither month supplies source-explicit 501/503/505/505½ construction or occupancy proof. November adds the B. J. Staats **520–22 Main** selling-out ad, which conflicts with the December CCHS photograph cataloged at **516 Main**; December adds Portland House at **Fifth and Main**, owned by Mr. and Mrs. Beck and described as frame construction, but with no numbered target assignment.

The formal annual source-class audit is `{CLOSE_CAPTURE}` (`{S_CLOSE}` / `{E_CLOSE}`): **1919 is ONLINE COMPLETE**. This changes research-work status only. The surviving 503 c.1919 estimate remains secondary/approximate, the surviving 505 remains bracketed to 1911–1925 with c.1920 tentative, and the exact physical-change date remains unresolved pending manual/restricted records.
''')
append_once("evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md", MARKER, f'''## 8 September annual-status supersession
{MARKER}

The narrow construction/occupancy public/indexed online pass recorded here has now been followed by complete November and December Enterprise visual review and the full 1919 annual source-class closeout. See `{CLOSE_CAPTURE}` (`{S_CLOSE}` / `{E_CLOSE}`). **1919 is now ONLINE COMPLETE**, not because the construction date was solved, but because the defined online work is complete and every remaining restricted/manual task is explicitly called out. The construction-date conclusion itself is unchanged.
''')
append_once("evidence/source-captures/2026-09-08-1919-1920-construction-occupancy-handoff.md", MARKER, f'''## Superseding 1919 end-state
{MARKER}

The handoff's November and December resume points are complete. November Enterprise **32/32** and December Enterprise **32/32** were visually reviewed and integrated as `{S_NOV}` / `{E_NOV}` and `{S_DEC}` / `{E_DEC}`. The annual source-class audit is `{S_CLOSE}` / `{E_CLOSE}` at `{CLOSE_CAPTURE}`.

**1919 is now ONLINE COMPLETE.** Banner-Courier and the authenticated/manual construction-date sources remain open, so 1919 is not ONLINE + MANUAL COMPLETE. Future chronological research should not repeat the completed 1919 online newspaper/public-indexed work; use the numbered manual callouts or proceed into the 1920 annual audit as appropriate.
''')

# Manual dashboard: add the missing permit/improvement-file item and clarify restricted Polk handling for closeout.
append_once("MANUAL-FOLLOWUP.md", MARKER, f'''## 1919 ONLINE COMPLETE manual-callout reconciliation
{MARKER}

For the 1919 annual closeout, `MF-040` / `1919-D01` is treated as a **RESTRICTED/AUTHENTICATED MANUAL CALLOUT**: public catalog/ARK and alternate public-copy routes were exhausted, while the actual 1919–1920 Polk target images require authenticated FamilySearch access. This does not authorize institutional outreach or paid research.

### {MF_PERMIT} — 1919–1921 Oregon City target-frontage permit / improvement files

Status: **ACTIVE MANUAL / RECORDS-ACCESS CALLOUT**.  
Source sought: any surviving **1919–1921 building permit, alteration/improvement, sign, sidewalk/street-front, inspection or related property files** for **501, 503, 505, 505½ Main** and the Fifth/Main target frontage.  
Likely route: Oregon City historic records/records management and any transferred archival holdings; use direct records inspection or a future steward-authorized request.  
Why manual: ordinary public/indexed online routes have not exposed the underlying files; catalog/index silence is not evidence that the files never existed.  
Question: determine whether a contemporary record directly dates demolition, construction, reconstruction, remodeling or sign work affecting the surviving 503/505 frontage.  
No request has been sent and no paid research has been authorized.
''')

# Year status: canonical certification register.
p = Path("registers/year-status.md")
y = p.read_text(encoding="utf-8")
y = y.replace("**Current certification result: 1917 is `ONLINE COMPLETE`; no year is `ONLINE + MANUAL COMPLETE`.**", "**Current certification result: 1917 and 1919 are `ONLINE COMPLETE`; no year is `ONLINE + MANUAL COMPLETE`.**")
lines = y.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1919 |"):
        lines[i] = f"| 1919 | **ONLINE COMPLETE** | `{CLOSE_CAPTURE}`; `{NOV_CAPTURE}`; `{DEC_CAPTURE}`; `evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | **102 local issue dates accounted for; 638/638 online-retrievable pages visually reviewed** (Enterprise 52 issues / 474 pages; Courier 26 issues / 164 pages). Banner-Courier 24 issues, 17 Jul.–25 Dec., remain `MF-030` manual microfilm. Other ordinary public/indexed online source classes are audited; restricted/manual directory, permits, assessment, deed/title and 1920 council records are explicit callouts. Exact 503/505 construction dates remain unresolved; no source silence is vacancy evidence. |"
        break
else:
    raise RuntimeError("1919 year-status row not found")
p.write_text("\n".join(lines) + "\n", encoding="utf-8")

# Archive navigation and log.
append_once("ARCHIVE_INDEX.md", MARKER, f'''### 1919 ONLINE COMPLETE closeout
{MARKER}
- [November 1919 Enterprise visual review]({NOV_CAPTURE}): `{S_NOV}` / `{E_NOV}` — 32/32 pages; Staats liquidation ad directly **520–22 Main**, preserved in conflict with CCHS December catalog **516 Main**.
- [December 1919 Enterprise visual review]({DEC_CAPTURE}): `{S_DEC}` / `{E_DEC}` — 32/32 pages; Portland House at Fifth/Main, Mr./Mrs. Beck owners, frame construction; no target-number assignment.
- [1919 all-online-source-class closeout]({CLOSE_CAPTURE}): `{S_CLOSE}` / `{E_CLOSE}` — **ONLINE COMPLETE**, 638/638 online-retrievable newspaper pages visually reviewed. 24 Banner-Courier issues and restricted/manual records remain explicit callouts; exact 503/505 construction dates unresolved.
''')
append_once("registers/research-log.md", MARKER, f'''## 8 September 2026 — November/December 1919 completion and ONLINE COMPLETE certification
{MARKER}
- Resynchronized against current `main` after parallel work and preserved the already-committed November/December originals/manifests.
- Visually reviewed **32/32 November Enterprise pages** and **32/32 December Enterprise pages** from scanned page images; OCR/text used only for discovery.
- Registered `{S_NOV}` / `{E_NOV}`: 28 Nov. B. J. Staats Hardware selling-out ad directly prints **520–22 Main**. Preserved unresolved conflict with CCHS December photograph cataloged **516 Main** (`S-147` / `E-132` / `IMG-0723`).
- Registered `{S_DEC}` / `{E_DEC}`: 19 Dec. Portland House fire directly places it at **Fifth and Main**, names **Mr. and Mrs. Beck** as owners and describes frame construction; no numbered target assignment.
- Completed the 1919 annual source-class audit `{S_CLOSE}` / `{E_CLOSE}`: **102 local issue dates accounted for and 638/638 online-retrievable pages visually verified**. The 24 Banner-Courier issues from 17 Jul.–25 Dec. remain `MF-030` manual microfilm work.
- Reconciled directory, map, municipal, property/title, historic-resource and photograph online-source classes. `MF-040` is retained as restricted/authenticated Polk work; added `{MF_PERMIT}` for surviving 1919–21 permit/improvement records; `MF-019`, `MF-006`, `MF-007` and `MF-041` remain underlying-record/manual routes.
- Certified **1919 ONLINE COMPLETE**, not ONLINE + MANUAL COMPLETE. No institutional request or paid research was authorized. The exact 503/505 construction date remains unresolved and source silence was not treated as vacancy or non-use.
''')

print(f"Integrated 1919 closeout: {S_NOV}/{E_NOV}, {S_DEC}/{E_DEC}, {S_CLOSE}/{E_CLOSE}; new manual callout {MF_PERMIT}")
