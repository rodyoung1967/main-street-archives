#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

S252 = "S-252"
S253 = "S-253"
S254 = "S-254"
E226 = "E-226"
E227 = "E-227"
E228 = "E-228"
P107 = "P-107"
MF048 = "MF-048"
CAPTURE = ROOT / "evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md"
DRAFT = ROOT / "registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md"
PROFILE = ROOT / "people/profiles/maurice-shahtout.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected anchor not found in {rel}: {old[:160]!r}")
    write(rel, text.replace(old, new, 1))


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.rstrip() + "\n")


# Fail rather than reuse IDs if parallel main has advanced into them.
checks = [
    (S252, "evidence/source-register.md", rf"^## {S252}\\b"),
    (S253, "evidence/source-register.md", rf"^## {S253}\\b"),
    (S254, "evidence/source-register.md", rf"^## {S254}\\b"),
    (E226, "evidence/evidence-register.md", rf"^## {E226}\\b"),
    (E227, "evidence/evidence-register.md", rf"^## {E227}\\b"),
    (E228, "evidence/evidence-register.md", rf"^## {E228}\\b"),
    (P107, "people/people-index.md", rf"^\\| {P107} \\|"),
]
for ident, rel, pat in checks:
    if re.search(pat, read(rel), re.M):
        raise SystemExit(f"{ident} is already assigned in {rel}; stop rather than reuse/renumber.")
for path in (CAPTURE, DRAFT, PROFILE):
    if path.exists():
        raise SystemExit(f"Target already exists: {path.relative_to(ROOT)}")

CAPTURE.write_text(r'''# 503 Main — 2002 transaction / 2010 Maurice ownership follow-up

Date: **5 September 2026**  
Status: **TARGETED OWNERSHIP PASS — transaction parties still unresolved**.

Purpose: test whether a public-record-derived **2 December 2002 / $200,000** 503 Main transaction can be identified as the later Wiitanen conveyance, and determine how **Maurice Shahtout / Maurice Enterprises Inc** fit the later 503 chain without mixing that chain with Wiitanen ownership of 505 Main.

## 1. 2 December 2002 transaction — `S-252` / `E-226`

Homes.com publishes a purchase-history table for **503 Main St, Oregon City** and states that it collects the history from publicly available records. The table reports:

- **2 Dec. 2002** — sale price **$200,000** — title company **Oregon Title Insurance Co**;
- **6 Jul. 2007** — $361,000;
- **9 Feb. 2009** — $318,480;
- later entries in 2012, 2016 and 2017.

The site hides the buyer and seller names behind sign-in. Therefore the 2 December 2002 entry is a **transaction lead only**. It is not presently proof that Dick and Sheila Wiitanen were the grantors or that Maurice Shahtout was the buyer. The later 2007/2009 entries must also be reconciled with the separate 2010 assessment-derived record below before interpreting this as a clean deed chain.

URL: https://www.homes.com/property/503-main-st-oregon-city-or/lt9ek3mwclkqr/

## 2. 2010 assessment-derived cross-address snapshot — `S-253` / `E-227`

City-Data republishes Clackamas County property-tax assessment data for **tax year 2010**. The page shows two separate entries at each target address:

### 503 Main

- **MAURICE SHAHTOUT** — land value $29,675; building value $74,240; total market value $103,915; **most recent sale price $200,000**.
- **MAURICE ENTERPRISES INC** — total market value $21,664.

### 505 Main

- **RICHARD M WIITANEN & SHEILA J WIITANEN** — land value $27,519; building value $70,980; total market value $98,499; most recent sale price $92,500.
- **505 TAVERN** — total market value $25,397.

URL: https://www.city-data.com/clackamas-county/M/Main-Street-1.html

This is **secondary repackaging of public-record data**, not the original assessor roll. Its most important historical value is the cross-address separation: by the 2010 tax-year snapshot, the page names **Maurice Shahtout** on the 503 land/building entry while **Richard and Sheila Wiitanen** remain on the 505 land/building entry. The separate Maurice Enterprises Inc and 505 Tavern entries are consistent with business/personal-property-type records being carried separately, but the republished page itself does not label those second entries clearly enough to assign a formal tax-account type from this source alone.

The matching **$200,000** amount between the 2010 Maurice Shahtout entry and the 2 Dec. 2002 Homes.com entry is important but **not sufficient to identify the 2002 buyer**. Homes.com also reports later 2007 and 2009 purchase events, while the 2010 assessment-derived page still calls $200,000 the most recent sale price. Preserve that discrepancy until the county deed/index chain is inspected.

## 3. Official County business-personal-property evidence — `S-254` / `E-228`

Clackamas County's **2026 Cancellation of Delinquent Business Personal Property Tax Accounts** spreadsheet directly names account **P2252284 — MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL)** in multiple historical tax-year sections, including 2013-14, 2014-15 and 2015-16.

URL: https://docs.clackamas.us/documents/drupal/9e3c9ae6-b8c8-4920-b7f5-b6012417cf67

This is direct official County evidence connecting **Maurice Enterprises Inc** to the **The Wheel Bar & Grill** trade name. The row does not print 503 Main, so address linkage continues to come independently from the OLCC record `S-251` / `E-225`, which names Maurice Enterprises Inc as licensee for The Wheel Bar & Grill at **503 Main** in the license cycle expiring 31 March 2009.

## 4. Maurice Shahtout identity handling

`P-107` is created for **Maurice Shahtout** because the 2010 assessment-derived page materially names him on the 503 real-estate entry. A tertiary address-history aggregator also associates Maurice Shahtout with The Wheel / Maurice Enterprises, but its dates and contact-role synthesis are not used as proof here.

Do **not** yet state that:

- Maurice Shahtout was the 2 Dec. 2002 buyer;
- Maurice Shahtout and Maurice Enterprises Inc were legally identical interests;
- the Wiitanens conveyed 503 directly to Maurice Shahtout on 2 Dec. 2002;
- the 2002 transaction transferred both business and real estate on the same recorded instrument.

Those conclusions require the deed/index and preferably OLCC change-of-ownership file.

## 5. What is now stronger

The downstream 503/505 separation is substantially clearer:

1. **By Aug. 1985** — Richard M. Wiitanen is directly documented as owner of The Wheel Cafe business at 503 (`E-049`).
2. **2 Dec. 2002** — a public-record-derived transaction history reports a $200,000 503 transaction, parties hidden (`E-226`).
3. **OLCC cycle ending 31 Mar. 2009** — Maurice Enterprises Inc is listed as The Wheel Bar & Grill licensee at 503 (`E-225`).
4. **Tax year 2010** — public-record-derived assessment data names Maurice Shahtout on the 503 land/building entry, while Richard and Sheila Wiitanen are named together on the 505 land/building entry (`E-227`).
5. **2013-16 historical BPP tax years** — Clackamas County directly connects Maurice Enterprises Inc with The Wheel Bar & Grill (`E-228`).

This establishes a strong later **Maurice-side endpoint** at 503 and an independent **Richard + Sheila ownership snapshot at 505**, but the exact Wiitanen→Maurice conveyance mechanics remain unresolved.

## 6. Next decisive record

The decisive source is now the **503 parcel-first chronological ownership/deed-reference chain** for:

- account / parcel **00572650**;
- tax lot **2-2E-31AB-08200**;
- legal description lead **2 OREGON CITY PT LT 4 BLK 4**.

Retrieve the deed by which Dick/Sheila acquired 503 and the deed by which they conveyed it out, with special attention to the **2 December 2002 / $200,000** transaction. `MF-048` tracks this as a separate 503 request. Do not merge it with `MF-034`, which is the separate 505 Wiitanen vesting-deed chain.

No email, paid search, or records request was sent in this pass.
''', encoding="utf-8")

DRAFT.write_text(r'''# MF-048 — 503 Main Wiitanen acquisition and conveyance deed request

Status: **DRAFT READY — NOT SENT**  
Prepared: 5 September 2026

## Assessment & Taxation / parcel-history request

**Recipient:** Clackamas County Assessment & Taxation public-records / property-records staff  
**Subject:** Historical ownership/deed-reference request — 503 Main Street, Oregon City (00572650 / 2-2E-31AB-08200)

Hello,

I am researching the ownership history of **503 Main Street, Oregon City, Oregon 97045**, currently associated with county account/parcel **00572650** and tax lot **2-2E-31AB-08200** (legal-description lead: **2 OREGON CITY PT LT 4 BLK 4**).

Could you please provide, or tell me how to obtain, the **chronological owner history and deed/instrument references** for this parcel from approximately **1970 through 2010**? I am especially trying to identify:

1. the deed/instrument by which **Richard M. (Dick) Wiitanen and/or Sheila J. Wiitanen** acquired the 503 Main real estate;
2. the deed/instrument by which they later conveyed the property out; and
3. the parties and recording reference associated with a public-record-derived transaction reported on **2 December 2002 for $200,000**.

For each ownership change, I would appreciate any available grantor/grantee names, recording date, instrument/document number, deed type, consideration/sale price, and legal description or tax-lot reference.

This request concerns **503 Main only**; I am researching 505 Main under a separate ownership chain.

Thank you for any assistance or direction to the appropriate historical ownership books, tax-lot cards, deed-reference records, or archived assessor files.

Sincerely,
Rodney Young

## Recording / deed-copy follow-up

**Recipient:** Clackamas County Recording  
**Subject:** Recorded deed copies — 503 Main Street, Oregon City / Wiitanen ownership chain

Hello,

I am researching the recorded ownership chain for **503 Main Street, Oregon City**, county account/parcel **00572650**, tax lot **2-2E-31AB-08200**.

I would like copies of the recorded instruments that:

1. vested the 503 Main property in **Richard M. (Dick) Wiitanen and/or Sheila J. Wiitanen**; and
2. later conveyed the property from the Wiitanens to the next owner.

A public-record-derived transaction history reports a **2 December 2002 sale for $200,000**, but the online source suppresses the buyer and seller names. If your index shows a conveyance affecting this parcel on or near that date, please include the instrument number, recording date, grantor, grantee, deed type, consideration if indexed, and a copy of the deed.

Please use the parcel/legal description rather than assuming the 2002 transaction was a Wiitanen conveyance; that is the question I am trying to verify.

Thank you,
Rodney Young
''', encoding="utf-8")

PROFILE.write_text(r'''# Maurice Shahtout

Person ID: `P-107`  
Related building: `B-001` (503 Main Street)  
Related business context: `BUS-004` (The Wheel)  
Related evidence: `E-227`

A secondary public-record-derived 2010 Clackamas County assessment page names **Maurice Shahtout** on the **503 Main Street** land/building entry and reports a most recent sale price of **$200,000** (`S-253` / `E-227`). This is a material downstream real-estate ownership lead after the Wiitanen era.

An independent OLCC list names **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill, 503 Main** in the license cycle expiring 31 March 2009 (`E-225`), and a later official County business-personal-property cancellation list directly links **Maurice Enterprises Inc** with the trade name **The Wheel Bar & Grill** (`E-228`). Neither official entity record names Maurice Shahtout personally.

Do not equate Maurice Shahtout with Maurice Enterprises Inc solely by shared first name/business context. The exact corporate relationship, the 503 deed, and whether he was the buyer in the reported 2 December 2002 / $200,000 transaction remain unresolved pending primary county and corporate records.
''', encoding="utf-8")

append_once("evidence/source-register.md", f"## {S252} —", r'''## S-252 — Homes.com public-record-derived 503 Main purchase history
Type: Secondary property-data aggregator reporting publicly available records; **TRANSACTION LEAD ONLY**.  
URL: https://www.homes.com/property/503-main-st-oregon-city-or/lt9ek3mwclkqr/  
Related evidence/building: `E-226` / `B-001`.  
Capture: `evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md`.  
Notes: Reports a **2 Dec. 2002** 503 Main purchase at **$200,000**, title company Oregon Title Insurance Co, but hides buyer/seller names. Also reports later 2007/2009 events that conflict with the separate 2010 assessment-derived page's “most recent sale price” wording. Do not identify the 2002 parties without the deed/index.''')

append_once("evidence/source-register.md", f"## {S253} —", r'''## S-253 — City-Data repackaged 2010 Clackamas County assessment data for 503 and 505 Main
Type: Secondary republication of public-record property-tax assessment data; **PUBLIC-RECORD-DERIVED / ORIGINAL ROLL NOT INSPECTED**.  
Tax year represented: **2010**.  
URL: https://www.city-data.com/clackamas-county/M/Main-Street-1.html  
Related evidence/buildings/person: `E-227` / `B-001`, `B-002` / `P-107`.  
Capture: `evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md`.  
Notes: At 503, names Maurice Shahtout on a land/building entry with most recent sale price $200,000 and separately lists Maurice Enterprises Inc. At 505, names Richard M Wiitanen & Sheila J Wiitanen on a land/building entry and separately lists 505 Tavern. Strong cross-address ownership snapshot, but verify against original County assessment/deed records.''')

append_once("evidence/source-register.md", f"## {S254} —", r'''## S-254 — Clackamas County 2026 cancellation list, Maurice Enterprises Inc (The Wheel Bar & Grill)
Type: Official Clackamas County business-personal-property tax spreadsheet; **DIRECT OFFICIAL TEXT**.  
URL: https://docs.clackamas.us/documents/drupal/9e3c9ae6-b8c8-4920-b7f5-b6012417cf67  
Related evidence/business: `E-228` / `BUS-004`.  
Capture: `evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md`.  
Notes: Account `P2252284` directly names **MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL)** in multiple historical tax-year sections including 2013-14, 2014-15 and 2015-16. The row does not print 503 Main; address linkage is independently supplied by `S-251` / `E-225`.''')

append_once("evidence/evidence-register.md", f"## {E226} —", r'''## E-226 — 503 Main purchase history reports a $200,000 transaction on 2 December 2002
Source: `S-252`  
Related building: `B-001`  
Type: Secondary public-record-derived transaction-history lead  
Claims:
- Homes.com reports a **2 December 2002** transaction at **503 Main Street** for **$200,000**, with Oregon Title Insurance Co named as title company.
- Buyer and seller names are hidden; the record therefore does **not** establish that the Wiitanens were grantors or Maurice Shahtout was purchaser.
- The same source reports later 2007 and 2009 purchase events; those must be reconciled with other assessment/deed evidence rather than silently treated as a clean chain.
Classification: **DOCUMENTED SECONDARY TRANSACTION LEAD / PARTIES UNRESOLVED**.  
Confidence: **High** for the aggregator's displayed date/price; **Unresolved** for parties, deed type and historical interpretation.''')

append_once("evidence/evidence-register.md", f"## {E227} —", r'''## E-227 — 2010 assessment snapshot separates Maurice Shahtout at 503 from Richard and Sheila Wiitanen at 505
Source: `S-253`  
Related buildings: `B-001`, `B-002`  
Related people: `P-107`, `P-007`, `P-008`  
Type: Secondary republication of Clackamas County tax-assessment data  
Claims:
- For tax year **2010**, the republished 503 land/building entry names **MAURICE SHAHTOUT**, with land value $29,675, building value $74,240, total market value $103,915, and most recent sale price **$200,000**.
- A separate 503 entry names **MAURICE ENTERPRISES INC** with total market value $21,664.
- The republished 505 land/building entry names **RICHARD M WIITANEN & SHEILA J WIITANEN**, with land value $27,519, building value $70,980 and total market value $98,499.
- A separate 505 entry names **505 TAVERN** with total market value $25,397.
- This materially supports a 2010 cross-address separation: Maurice Shahtout is the named 503 real-estate owner in the republished assessment data while Richard and Sheila Wiitanen remain jointly named at 505.
- The source is not the original County roll and does not itself prove deed dates, entity relationships, or the 2002 buyer.
Classification: **STRONG SECONDARY PUBLIC-RECORD-DERIVED OWNERSHIP SNAPSHOT**; deed-level title remains pending.  
Confidence: **High** for the displayed 2010 assessment names/values; primary county verification still required.''')

append_once("evidence/evidence-register.md", f"## {E228} —", r'''## E-228 — County business-personal-property record links Maurice Enterprises Inc to The Wheel Bar & Grill
Source: `S-254`  
Related building/business: `B-001` / `BUS-004`  
Type: Official Clackamas County business-personal-property tax record  
Claims:
- Clackamas County's 2026 cancellation list directly names account **P2252284 — MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL)**.
- The account appears in multiple historical tax-year sections including 2013-14, 2014-15 and 2015-16.
- The County row does not print a street address, so it is not used alone to locate the business; `E-225` independently places Maurice Enterprises Inc / The Wheel Bar & Grill at **503 Main** in the OLCC record.
- The source does not name Maurice Shahtout personally and does not prove real-estate ownership.
Classification: **DOCUMENTED / DIRECT** for entity-to-trade-name linkage; **NO REAL-ESTATE TITLE CLAIM**.  
Confidence: **Very High** for the official County account/trade-name wording.''')

append_once("database/sources.yml", f"  - id: {S252}\n", r'''  - id: S-252
    name: "Homes.com public-record-derived 503 Main purchase history"
    url: "https://www.homes.com/property/503-main-st-oregon-city-or/lt9ek3mwclkqr/"
    type: "Secondary public-record-derived property transaction aggregator"
    notes: "Reports 2 Dec 2002 transaction at 503 Main for $200,000 with parties hidden; later 2007/2009 events require reconciliation. Transaction lead only."
    related_evidence: [E-226]
    related_buildings: [B-001]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("database/sources.yml", f"  - id: {S253}\n", r'''  - id: S-253
    name: "City-Data repackaged 2010 Clackamas County assessment data for 503 and 505 Main"
    url: "https://www.city-data.com/clackamas-county/M/Main-Street-1.html"
    type: "Secondary republication of public-record tax assessment data"
    notes: "Tax-year 2010 page names Maurice Shahtout on 503 land/building entry and Richard M Wiitanen & Sheila J Wiitanen on 505 land/building entry; original County roll/deeds remain uninspected."
    related_evidence: [E-227]
    related_buildings: [B-001, B-002]
    related_people: [P-107, P-007, P-008]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("database/sources.yml", f"  - id: {S254}\n", r'''  - id: S-254
    name: "Clackamas County 2026 cancellation list, Maurice Enterprises Inc (The Wheel Bar & Grill)"
    url: "https://docs.clackamas.us/documents/drupal/9e3c9ae6-b8c8-4920-b7f5-b6012417cf67"
    type: "Official county business-personal-property tax record"
    notes: "Account P2252284 names MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL) in multiple historical tax-year sections; row supplies no street address."
    related_evidence: [E-228]
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("database/evidence.yml", f"  - id: {E226}\n", r'''  - id: E-226
    name: "503 Main purchase history reports a $200,000 transaction on 2 December 2002"
    type: "Secondary public-record-derived transaction-history lead"
    claims:
      - "Homes.com reports a 2 December 2002 transaction at 503 Main for $200,000."
      - "Buyer and seller names are hidden; Wiitanen grantor and Maurice buyer identities are not established."
      - "Later 2007 and 2009 aggregator events require reconciliation with primary deed/index records."
    confidence: "High for displayed date/price; parties and deed interpretation unresolved"
    related_sources: [S-252]
    related_buildings: [B-001]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("database/evidence.yml", f"  - id: {E227}\n", r'''  - id: E-227
    name: "2010 assessment snapshot separates Maurice Shahtout at 503 from Richard and Sheila Wiitanen at 505"
    type: "Secondary republication of public-record tax assessment data"
    claims:
      - "Tax-year 2010 republished 503 land/building entry names Maurice Shahtout and reports most recent sale price $200,000."
      - "A separate 503 entry names Maurice Enterprises Inc."
      - "Tax-year 2010 republished 505 land/building entry names Richard M Wiitanen & Sheila J Wiitanen."
      - "A separate 505 entry names 505 Tavern."
      - "This is a strong cross-address ownership snapshot but not deed-level proof."
    confidence: "High for displayed assessment-derived names and values; primary County verification pending"
    related_sources: [S-253]
    related_buildings: [B-001, B-002]
    related_people: [P-107, P-007, P-008]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("database/evidence.yml", f"  - id: {E228}\n", r'''  - id: E-228
    name: "County business-personal-property record links Maurice Enterprises Inc to The Wheel Bar & Grill"
    type: "Official county business-personal-property tax record"
    claims:
      - "Clackamas County account P2252284 directly names MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL)."
      - "The account appears in multiple historical tax-year sections including 2013-14, 2014-15 and 2015-16."
      - "The County row does not print an address and does not name Maurice Shahtout personally."
    confidence: "Very High for entity/trade-name wording; no real-estate-title claim"
    related_sources: [S-254]
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    repository_file: evidence/source-captures/503-main-2002-2010-maurice-ownership-follow-up-2026-09-05.md''')

append_once("people/people-index.md", f"| {P107} |", r'''| P-107 | [Maurice Shahtout](profiles/maurice-shahtout.md) | 503 Main downstream real-estate owner lead | Public-record-derived 2010 assessment page names him on 503 land/building entry; exact acquisition deed and relationship to Maurice Enterprises Inc remain unresolved. |''')

append_once("database/people.yml", f"  - id: {P107}\n", r'''  - id: P-107
    name: Maurice Shahtout
    role: 503 Main downstream real-estate owner lead
    notes: "Secondary public-record-derived 2010 assessment page names Maurice Shahtout on the 503 land/building entry and reports most recent sale price $200,000. Exact acquisition deed and legal relationship to Maurice Enterprises Inc remain unresolved."
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_evidence: [E-227]
    related_sources: [S-253]
    repository_file: people/profiles/maurice-shahtout.md''')

# Core 503 building/business link lists.
replace_once("buildings/503-main.md",
    "- Related people: `P-003`, `P-004`, `P-006`, `P-007`, `P-008`, `P-014`, `P-015`, `P-016`, `P-017`, `P-021`, `P-022`, `P-023`, `P-024`, `P-025`, `P-034`, `P-035`, `P-036`",
    "- Related people: `P-003`, `P-004`, `P-006`, `P-007`, `P-008`, `P-014`, `P-015`, `P-016`, `P-017`, `P-021`, `P-022`, `P-023`, `P-024`, `P-025`, `P-034`, `P-035`, `P-036`, `P-107`")
replace_once("buildings/503-main.md",
    "`E-213`, `E-225`",
    "`E-213`, `E-225`, `E-226`, `E-227`, `E-228`")
replace_once("buildings/503-main.md",
    "`S-239`, `S-251`",
    "`S-239`, `S-251`, `S-252`, `S-253`, `S-254`")

append_once("buildings/503-main.md", "## 2002–2010 downstream ownership bracket", r'''## 2002–2010 downstream ownership bracket

`E-226` adds a **2 December 2002 / $200,000** 503 transaction lead, but the aggregator hides the buyer and seller. `E-227` then supplies a public-record-derived **2010** assessment snapshot naming **Maurice Shahtout** on the 503 land/building entry while the neighboring 505 land/building entry still names **Richard M. and Sheila J. Wiitanen**. `E-228` independently links **Maurice Enterprises Inc** to **The Wheel Bar & Grill** in an official Clackamas County business-personal-property record, while `E-225` independently places that entity/trade name at 503 through OLCC.

This strongly narrows the downstream 503 chain but does **not** yet prove that the 2 December 2002 transaction was the Wiitanen conveyance, that Maurice Shahtout was its buyer, or that Maurice Shahtout and Maurice Enterprises Inc were legally the same interest. Retrieve the County deed/index chain under `MF-048`.''')

replace_once("businesses/the-wheel.md",
    "- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`, `E-225`",
    "- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`, `E-225`, `E-226`, `E-227`, `E-228`")
replace_once("businesses/the-wheel.md",
    "- Related people: `P-006`, `P-010`, `P-022`, `P-007`, `P-008`",
    "- Related people: `P-006`, `P-010`, `P-022`, `P-007`, `P-008`, `P-107`")
replace_once("businesses/the-wheel.md",
    "- OLCC indexed license text later identifies **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill at 503 Main**, license 104145 expiring **31 March 2009** (`E-225`; OCR/TEXT ONLY pending visual page verification).",
    "- OLCC indexed license text later identifies **Maurice Enterprises Inc** as licensee for **The Wheel Bar & Grill at 503 Main**, license 104145 expiring **31 March 2009** (`E-225`; OCR/TEXT ONLY pending visual page verification).\n- A public-record-derived **2010** assessment page names **Maurice Shahtout** on the 503 land/building entry and separately names Maurice Enterprises Inc at 503 (`E-227`).\n- Clackamas County later directly links **Maurice Enterprises Inc** to the trade name **The Wheel Bar & Grill** in business-personal-property account `P2252284` (`E-228`).\n- A **2 December 2002 / $200,000** 503 transaction is now identified as a high-value deed lead, but its buyer/seller remain hidden and it is not yet accepted as the Wiitanen sale (`E-226`).")

# Address timelines / ownership chronology.
replace_once("timelines/503-main.md",
    "| Apr.–Aug. 1985 | **The Wheel Cafe, 503 Main**; Richard Wiitanen named business owner. | **Exact primary**; does not date property purchase. | `E-048`, `E-049`; `S-055`–`S-057` |",
    "| Apr.–Aug. 1985 | **The Wheel Cafe, 503 Main**; Richard Wiitanen named business owner. | **Exact primary**; does not date property purchase. | `E-048`, `E-049`; `S-055`–`S-057` |\n| 2 Dec. 2002 | Public-record-derived purchase history reports a **$200,000** 503 transaction. | **Secondary transaction lead only**; buyer/seller hidden, so not yet the proved Wiitanen conveyance. | `E-226`; `S-252` |\n| Tax year 2010 | Public-record-derived assessment page names **Maurice Shahtout** on 503 land/building entry and separately **Maurice Enterprises Inc** at 503. | Strong secondary ownership snapshot; original roll/deed pending. The page's $200,000 “most recent sale” wording conflicts with aggregator-reported 2007/2009 events. | `P-107`; `E-227`; `S-253` |")

replace_once("timelines/505-main.md",
    "| 2017 | Thirsty Duck reopening / permits / Wiitanen owner line. |",
    "| Tax year 2010 | Public-record-derived assessment page names **Richard M. Wiitanen & Sheila J. Wiitanen** on the 505 land/building entry and separately **505 Tavern** at 505. | **Strong secondary ownership snapshot**; original County roll/deed still pending. | `P-007`, `P-008`; `E-227`; `S-253` |\n| 2017 | Thirsty Duck reopening / permits / Wiitanen owner line. |")

replace_once("registers/ownership-timeline.md",
    "| Later; exact date open | 503 Main | Dick and Sheila Wiitanen → later buyer | **Sold The Wheel business and 503 building together** | `E-022` | High family | Buyer, date, deed, business-sale agreement, and liquor-license transfer pending. |",
    "| Later; exact date open | 503 Main | Dick and Sheila Wiitanen → later buyer | **Sold The Wheel business and 503 building together** | `E-022` | High family | Buyer, date, deed, business-sale agreement, and liquor-license transfer pending. |\n| 2 Dec. 2002 transaction lead | 503 Main | Parties hidden | Reported $200,000 property transaction | `E-226` / `S-252` | High for displayed date/price; parties unresolved | Candidate interval for the downstream conveyance only; do not label Wiitanen→Shahtout without deed/index proof. |\n| Tax year 2010 | 503 Main | Maurice Shahtout | Named on land/building assessment entry | `E-227` / `S-253` | Strong secondary public-record-derived | Original assessor roll/deed pending. Separate 503 entry names Maurice Enterprises Inc. |")
replace_once("registers/ownership-timeline.md",
    "| After 505 property purchase through Nov. 2024 | 505 Main | Wiitanen family / Richard M. Wiitanen | Real-estate owners / landlords | `E-022`, `E-035`, `E-038` | High family; very high by 2017 permit for Richard interest | Sheila died in 2014; ownership continued through Dick's death. |",
    "| After 505 property purchase through Nov. 2024 | 505 Main | Wiitanen family / Richard M. Wiitanen | Real-estate owners / landlords | `E-022`, `E-035`, `E-038`, `E-227` | High family; strong secondary 2010 joint-owner snapshot; very high by 2017 permit for Richard interest | Tax-year 2010 assessment-derived data names **Richard M. Wiitanen & Sheila J. Wiitanen** together on the 505 land/building entry; Sheila died in 2014; ownership continued through Dick's death. |")

# Research-lead update.
old_rl = "**5 September 2026 update:** `E-223` / `S-249` now records Raye's maiden name **Weaver**; `E-224` / `S-250` independently confirms **Sheila Wiitanen as Raye's daughter**. For 503, `E-049` directly names Richard M. Wiitanen as Wheel Cafe owner in August 1985, while `E-225` / `S-251` later names **Maurice Enterprises Inc** as The Wheel Bar & Grill licensee at 503 in the OLCC cycle expiring 31 March 2009 (**OCR/TEXT ONLY pending page-image verification**). Highest-value 503 work is now the parcel-first deed chain for account **00572650 / 2-2E-31AB-08200**, plus OLCC change-of-ownership records between the 1985 and 2009 endpoints. A tertiary D & S Incorporated association is retained only as a lead; the official Oregon corporate filing and any previously mentioned registry number remain unverified. Keep this completely separate from `MF-034`'s 505 deed chain."
new_rl = "**5 September 2026 update:** `E-223` / `S-249` now records Raye's maiden name **Weaver**; `E-224` / `S-250` independently confirms **Sheila Wiitanen as Raye's daughter**. For 503, `E-049` directly names Richard M. Wiitanen as Wheel Cafe owner in August 1985, while `E-225` / `S-251` later names **Maurice Enterprises Inc** as The Wheel Bar & Grill licensee at 503 in the OLCC cycle expiring 31 March 2009 (**OCR/TEXT ONLY pending page-image verification**). The follow-up now adds a **2 Dec. 2002 / $200,000** 503 transaction lead with hidden parties (`E-226`), a public-record-derived **2010** assessment snapshot naming **Maurice Shahtout** on the 503 land/building entry while **Richard M. & Sheila J. Wiitanen** remain jointly named on the 505 land/building entry (`E-227`), and an official County business-personal-property record directly linking **Maurice Enterprises Inc** to **The Wheel Bar & Grill** (`E-228`). The matching $200,000 amount is suggestive but not buyer proof because the transaction aggregator also reports later 2007/2009 events. Highest-value 503 work is now `MF-048`: the parcel-first deed chain for account **00572650 / 2-2E-31AB-08200**, plus OLCC change-of-ownership records. A tertiary D & S Incorporated association remains only a lead; the official Oregon corporate filing and any previously mentioned registry number remain unverified. Keep this completely separate from `MF-034`'s 505 deed chain."
replace_once("evidence/research-leads.md", old_rl, new_rl)

append_once("registers/research-log.md", "## 503 downstream ownership / Maurice follow-up — 5 September 2026", r'''## 503 downstream ownership / Maurice follow-up — 5 September 2026

- Recovered a public-record-derived **2 Dec. 2002 / $200,000** 503 transaction lead (`S-252` / `E-226`); buyer/seller names remain hidden and no Wiitanen→Maurice conveyance is asserted.
- Recovered a 2010 Clackamas assessment-data republication that separately names **Maurice Shahtout** on the 503 land/building entry and **Richard M. Wiitanen & Sheila J. Wiitanen** on the 505 land/building entry (`S-253` / `E-227`). This materially strengthens the downstream separation of the two properties.
- Registered **Maurice Shahtout** as `P-107` based on the 2010 ownership entry, while keeping him separate from Maurice Enterprises Inc pending corporate/deed proof.
- Recovered official Clackamas County BPP text naming account **P2252284 — MAURICE ENTERPRISES INC (THE WHEEL BAR & GRILL)** (`S-254` / `E-228`), independently strengthening the entity/trade-name link already addressed by OLCC `E-225`.
- Preserved the conflict that Homes.com reports later 2007/2009 purchase events while the 2010 assessment-derived page gives Maurice Shahtout a “most recent sale price” of $200,000. No clean deed-chain interpretation is made from the aggregators.
- Added `MF-048` and a two-stage Assessment & Taxation / Recording draft for the 503 Wiitanen acquisition and conveyance deeds. No outreach was sent.''')

append_once("indexes/id-crosswalk.md", "## S-252 / E-226 — 503 downstream ownership follow-up", r'''## S-252 / E-226 — 503 downstream ownership follow-up

| Record | Links | Notes |
| --- | --- | --- |
| `S-252` / `E-226` | `B-001` | Public-record-derived 2 Dec. 2002 / $200,000 503 transaction; parties hidden. |
| `S-253` / `E-227` | `B-001`, `B-002`, `P-107`, `P-007`, `P-008` | 2010 assessment-derived page names Maurice Shahtout at 503 and Richard M. & Sheila J. Wiitanen at 505; original County roll/deeds pending. |
| `S-254` / `E-228` | `B-001`, `BUS-004` | Official County BPP account P2252284 names Maurice Enterprises Inc (The Wheel Bar & Grill); row has no address. |
| `P-107` Maurice Shahtout | `B-001`, `BUS-004`, `E-227`, `S-253` | Named on the 2010 503 land/building assessment-derived entry; exact deed and Maurice Enterprises relationship unresolved. |''')

# Open question / business timeline concise updates.
append_once("evidence/open-questions.md", "### 503 Wiitanen exit / Maurice acquisition — 5 September 2026", r'''### 503 Wiitanen exit / Maurice acquisition — 5 September 2026

The downstream bracket is now materially tighter but the deed is still missing. `E-226` reports a **2 Dec. 2002 / $200,000** 503 transaction with hidden parties; `E-227` names **Maurice Shahtout** on the 503 land/building assessment-derived entry in tax year 2010; `E-225` and `E-228` independently tie **Maurice Enterprises Inc / The Wheel Bar & Grill** to the later 503 business chain. The same 2010 page still names **Richard M. and Sheila J. Wiitanen** on the 505 land/building entry. Retrieve the 503 deed/index chain under `MF-048` before identifying the 2002 parties or equating Maurice Shahtout with Maurice Enterprises Inc.''')

replace_once("registers/business-timeline.md",
    "| Apr.–Aug. 1985 | The Wheel Cafe | `BUS-004` | `E-048`, `E-049` | Very High | Lottery outlet at 503 Main St.; Richard M. Wiitanen named owner. Working family interpretation is that the Grisham → Wiitanen transition was a sale of the 503 business; exact transaction date/terms pending. |",
    "| Apr.–Aug. 1985 | The Wheel Cafe | `BUS-004` | `E-048`, `E-049` | Very High | Lottery outlet at 503 Main St.; Richard M. Wiitanen named owner. Working family interpretation is that the Grisham → Wiitanen transition was a sale of the 503 business; exact transaction date/terms pending. |\n| 2002 transaction lead; 2009–2016 later Maurice chain | The Wheel / Wheel Bar & Grill | `BUS-004` | `E-225`–`E-228` | Mixed: official entity/trade-name records + strong secondary ownership snapshot | 2 Dec. 2002 / $200,000 property transaction has hidden parties. OLCC names Maurice Enterprises Inc at 503 by the cycle ending 31 Mar. 2009; 2010 assessment-derived data names Maurice Shahtout on 503 land/building entry; County later directly links Maurice Enterprises Inc to The Wheel Bar & Grill. Exact Wiitanen conveyance and entity/person relationship remain unresolved. |")

# Database relation mirrors: add IDs where their entity blocks can be safely edited by exact anchors.
replace_once("database/people.yml",
    "    related_sources: [S-253]\n    repository_file: people/profiles/maurice-shahtout.md",
    "    related_sources: [S-253]\n    repository_file: people/profiles/maurice-shahtout.md")

# MANUAL-FOLLOWUP: add active row after current order 17, plus audited disposition and dispatch draft pointer.
manual = read("MANUAL-FOLLOWUP.md")
if MF048 not in manual:
    row17 = "| 17 | **MF-014** | Retrieve the original **1906 numbering plat / Ordinance 357 implementation records** | Foundational address-mapping source for pre-/post-1906 Main/Fifth numbering | **ACTIVE MANUAL — DRAFT READY**. [City Recorder email draft](registers/research-requests/active-manual-outreach-drafts-2026-09-05.md) |"
    row18 = "| 18 | **MF-048** | Retrieve the **503 Main parcel-first ownership/deed-reference chain**, including the Wiitanen acquisition deed and conveyance out, with special attention to the reported **2 Dec. 2002 / $200,000** transaction | New 2010 assessment-derived evidence names Maurice Shahtout at 503 while the Wiitanens remain at 505, but the 2002 parties are hidden; deed proof is now the decisive bridge | **ACTIVE MANUAL — TWO-STAGE DRAFT READY**. [503 deed-chain draft](registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md) |"
    if row17 not in manual:
        raise SystemExit("MF section-1 row-17 anchor missing; stop rather than guess.")
    manual = manual.replace(row17, row17 + "\n" + row18, 1)
    marker = "| MF-047 | **ACTIVE MANUAL** | **Yes** |"
    idx = manual.find(marker)
    if idx == -1:
        # Append audit disposition if exact MF-047 row isn't exposed in current form.
        manual = manual.rstrip() + "\n\n## MF-048 — 503 Wiitanen acquisition / conveyance deed chain\n\n**ACTIVE MANUAL.** Retrieve the 503 Main parcel-first owner/deed-reference history and the actual deeds into and out of Dick/Sheila Wiitanen; test the reported 2 Dec. 2002 / $200,000 transaction without assuming its parties. Draft: `registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md`. Keep separate from MF-034 (505).\n"
    else:
        # Insert a concise new audited-disposition row immediately after the MF-047 table row.
        line_end = manual.find("\n", idx)
        mfrow = "\n| MF-048 | **ACTIVE MANUAL** | **Yes** | New 503-specific deed-chain task: identify Wiitanen acquisition and conveyance, testing the 2 Dec. 2002 / $200,000 lead. Keep separate from MF-034 (505). Draft linked in section 1. |"
        manual = manual[:line_end] + mfrow + manual[line_end:]
    write("MANUAL-FOLLOWUP.md", manual)

print("Integrated 503/505 2002-2010 ownership follow-up with S-252..S-254, E-226..E-228, P-107 and MF-048.")
