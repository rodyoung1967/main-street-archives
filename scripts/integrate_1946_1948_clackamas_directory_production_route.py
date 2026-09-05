from pathlib import Path
import re

REVIEW = "2026-09-04"
CAP = "evidence/source-captures/1946-1948-clackamas-county-directory-production-retrieval-route-2026-09-04.md"


def rd(path):
    return Path(path).read_text(encoding="utf-8")


def wr(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def maxid(path, prefix):
    vals = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    return max(vals) if vals else 0


def append_once(path, marker, block):
    text = rd(path)
    if marker in text:
        return False
    wr(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")
    return True


def insert_before(path, marker, unique, block):
    text = rd(path)
    if unique in text:
        return False
    if marker not in text:
        raise SystemExit(f"marker not found in {path}: {marker}")
    wr(path, text.replace(marker, block.rstrip() + "\n\n" + marker, 1))
    return True


def replace_once(path, old, new):
    text = rd(path)
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"text not found in {path}: {old}")
    wr(path, text.replace(old, new, 1))
    return True


if Path(CAP).exists():
    print("Directory production/retrieval route already integrated; no changes needed.")
    raise SystemExit(0)

s0 = maxid("evidence/source-register.md", "S")
e0 = maxid("evidence/evidence-register.md", "E")
S_AUG = f"S-{s0+1:03d}"
S_SEP = f"S-{s0+2:03d}"
S_CITY = f"S-{s0+3:03d}"
S_LIB = f"S-{s0+4:03d}"
S_CCHS = f"S-{s0+5:03d}"
S_OC = f"S-{s0+6:03d}"
S_LO = f"S-{s0+7:03d}"
S_FS = f"S-{s0+8:03d}"
E_PROD = f"E-{e0+1:03d}"
E_ROUTE = f"E-{e0+2:03d}"

URL_AUG = "https://oregonnews.uoregon.edu/lccn/2024240281/1946-08-01/ed-1/seq-3/ocr/"
URL_SEP = "https://oregonnews.uoregon.edu/lccn/2024240281/1946-09-05/ed-1/seq-4/ocr/"
URL_CITY = "https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723051/File/document"
URL_LIB = "https://oregonnews.uoregon.edu/lccn/2024240281/1948-07-08/ed-1/seq-5.pdf"
URL_CCHS = "https://clackamascountyhistoricalsociety.wordpress.com/2012/02/27/facts-you-should-know-about-oregon-city/"
URL_OC = "https://www.orcity.org/DocumentCenter/View/4025/Downtown-Final-Report---2000-PDF"
URL_LO = "https://www.ci.oswego.or.us/sites/default/files/fileattachments/boc_hrab/webpage/18280/103_107_burnham_road_ils.pdf"
URL_FS = "https://www.familysearch.org/en/search/catalog/95422"

capture = f'''# 1946–1948 Clackamas County Directory production and retrieval route

Reviewed **4 September 2026** while continuing the Farr's Pool Hall → Harr's Recreation Center / 505 Main transition search.

Archive IDs: production evidence `{E_PROD}` from `{S_AUG}` / `{S_SEP}`; publication/retrieval evidence `{E_ROUTE}` from `{S_CITY}` / `{S_LIB}` / `{S_CCHS}` / `{S_OC}` / `{S_LO}` / `{S_FS}`.

## Why this source matters

The still-unrecovered **1947–48 Clackamas County Directory** is one of the best surviving candidates for placing Farr or Harr at **505 Main** between the secondary 1945 Harr claim and the direct 1948 municipal evidence. New contemporary newspaper evidence changes how any eventual directory listing must be interpreted: Pacific Directory Service was gathering the underlying county-wide directory data in **August–September 1946**.

A listing in a volume labeled 1947–48 therefore must not automatically be treated as a condition observed in 1948. The exact listing date depends on the directory's canvass/publication practices and the target entry itself.

## 1 August 1946 — county-wide directory campaign

Source: *Sandy Post*, 1 August 1946, p.3 (`{S_AUG}`).

URL: {URL_AUG}

The newspaper carries a Pacific Directory Service advertisement headed **“A new Clackamas County Directory, now being compiled”**. The OCR/text layer states that the directory was intended to include:

- Sandy and the other incorporated cities in Clackamas County;
- corporations, business and professional firms;
- individuals' occupations and business connections;
- home and business addresses;
- wives' and children's names;
- telephone information;
- real-estate ownership designation;
- rural-route listings;
- a county-wide classified business directory and buyers' guide.

The advertisement says incorporated-city listings would be gathered by **house-to-house canvass**. It also says more than **15,000** questionnaires had recently been sent to rural-route, star-route and post-office-box holders.

This source is preserved as **PRIMARY NEWSPAPER OCR/TEXT ONLY**. The archive page text is readable, but the scan itself was not successfully rendered for visual certification in this pass.

## 5 September 1946 — canvass still underway

Source: *Sandy Post*, 5 September 1946, p.4 (`{S_SEP}`).

URL: {URL_SEP}

A follow-up Pacific Directory Service notice again describes the Clackamas County directory then being compiled. It says incorporated-city listings would come from a house-to-house canvass and again refers to more than 15,000 mailed rural questionnaires. It asks for full name, spouse name, occupation/business, employer, home/business addresses, real-estate ownership, postal location and telephone information.

The OCR identifies **Pacific Directory Service, Publishers**, Room 8, Beaver Building, Oregon City. The manager's name is not promoted because the OCR is imperfect and the scan was not visually certified.

This is also **PRIMARY NEWSPAPER OCR/TEXT ONLY**.

## What the 1946 notices establish — and do not establish

**DOCUMENTED / DIRECT from the OCR/text layers:** Pacific Directory Service was conducting a county-wide directory compilation campaign in August and September 1946, using house-to-house canvassing in incorporated cities and mailed questionnaires in rural areas.

**STRONG CROSS-SOURCE INFERENCE, not direct proof:** this 1946 campaign is likely the production campaign for the volume later cited as **Directory of Clackamas County, 1947–48 / 1948**. The title page or an explicit contemporary publication notice is still needed to prove that production lineage.

Research consequence: if the target volume lists Harr at 505, that listing could reflect a canvass response collected in late 1946. Conversely, a Farr listing could survive into a later-labeled volume because of publication lag. Do not assign the printed directory year as an exact occupancy date without the volume's explanatory/front-matter evidence.

## February–March 1948 — Oregon City bought a Pacific Directory Service “Directory”

Source: Oregon City Commission minutes / March 3, 1948 February-claims report (`{S_CITY}`).

URL: {URL_CITY}

Municipal page **474** begins the 11 February 1948 special meeting naming **Messrs. Harr and McDougald** as pool-hall operators. The same official PDF proceeds to the **3 March 1948 regular meeting**, where the Commission approved the report of claims against the City for **February**. In the extracted multi-column claims table on municipal page **477**, **Pacific Directory Service** appears in the vendor sequence and **Directory** appears in the corresponding item-description sequence.

The flattened OCR/text extraction does **not** preserve the table geometry well enough to assign the dollar amount safely. A previous repository note gave **$9.75**; that amount is withdrawn as overprecise until the page image is visually inspected.

This is **PRIMARY MUNICIPAL OCR/TEXT ONLY** for the Pacific Directory Service / Directory purchase relationship. It establishes that Oregon City was processing a Pacific Directory Service directory expense in the February 1948 claims cycle; it does not print the directory title or expose a Farr/Harr/505 listing.

## 8 July 1948 — directory available at Sandy branch library

Source: *Sandy Post*, 8 July 1948, p.5 (`{S_LIB}`).

URL: {URL_LIB}

The newspaper reports that librarian **Lois Shearman** said a copy of the **new Clackamas County Directory** was available for use in the Sandy branch of the Clackamas County library.

This directly proves county-library availability of a newly issued Clackamas County directory by 8 July 1948, but the short notice does not name the publisher or formal edition. The page-image endpoint could not be visually certified in this pass, so the finding remains **PRIMARY NEWSPAPER OCR/TEXT ONLY**.

## Later bibliographic and institutional controls

### CCHS used a “Pacific Directory, 1947-48”

Clackamas County Historical Society published a 2012 Oregon City fact sheet explicitly credited to **“Pacific Directory, 1947-48”** (`{S_CCHS}`).

URL: {URL_CCHS}

This is a strong retrieval lead because it shows CCHS had access to the volume or a close derivative in modern research work. It is not itself evidence of the Farr/Harr listing.

### Official title/date variants

Oregon City's 2000 Downtown Final Report bibliography (`{S_OC}`) cites:

- Pacific Directory Service, **Directory of Clackamas County**, Portland, **1948**.

URL: {URL_OC}

A 2014 City of Lake Oswego historic-resource survey (`{S_LO}`) cites:

- Pacific Directory Service, **1947–1948 Directory of Clackamas County**, Portland, Oregon.

URL: {URL_LO}

These are likely bibliographic variants for the same volume, but that identity remains a **STRONG CROSS-SOURCE INFERENCE** until the actual title page is inspected.

### Historic Ticor provenance trail

Multiple Oregon historic-resource inventory forms from the 1980s–1990s cite **Clackamas County Directory, 1947-48** together with **Ticor Title Company, Oregon City, OR**. This suggests that historic-resource researchers accessed the directory through a Ticor Title research collection or provenance chain. It is a historical holdings lead only; no current Ticor custody is assumed.

### FamilySearch catalog control — not the target 1947–48 edition

FamilySearch catalog record **95422** (`{S_FS}`) has the similar title **Oregon City (Clackamas County, Oregon) city directory ...**, but its author is **R. L. Polk & Co.**, publication begins **1960**, and its listed contained volumes begin in 1960. It is therefore **not** evidence that FamilySearch holds the 1947–48 Pacific Directory Service volume under that catalog record.

URL: {URL_FS}

This exclusion prevents a misleading retrieval route from being repeated.

## Best current retrieval route

The strongest current manual/institutional route is the **Wilmer Gardner Research Library / Clackamas County Family History Society** in the same Oregon City building as CCHS, because:

1. CCHS itself publicly used the Pacific Directory 1947–48 in 2012;
2. the research library holds books, maps, reference collections, local-history files and other Clackamas County material;
3. librarians accept research inquiries;
4. historical records show a Clackamas County library branch had a copy by July 1948.

Request the actual volume or scans, not a later transcription.

## Exact pages/entries to inspect when the volume is found

Inspect all available sections rather than a single surname hit:

1. **Harr** — Carl R. Harr and all Harr entries.
2. **Farr** — Edwin F. / Edwin Franklin / E. F. Farr and Alice Farr.
3. Business names: **Harr's Recreation Center**, **Farr's Pool Hall**.
4. Exact premises: **505 Main**, **505½ Main**, and neighboring **501–511 Main**.
5. Classified headings: pool, billiards, recreation, taverns, beer, cigars/tobacco.
6. Street/address index or reverse directory if present.
7. Front matter explaining canvass date, compilation date, publication date and how carry-forward listings were handled.

## Farr → Harr status after this pass

The transition date remains **unresolved**.

What changed is the interpretation and retrieval strategy:

- the target county directory is now tied to a documented **1946 data-gathering campaign**;
- Oregon City was processing a Pacific Directory Service **Directory** expense in the **February 1948 claims cycle**;
- the Sandy branch had a **new Clackamas County Directory** by **8 July 1948**;
- CCHS later explicitly used a **Pacific Directory, 1947-48**;
- official bibliographies identify the publisher as **Pacific Directory Service** and the volume as either 1947–48 or 1948.

No source recovered here states whether Farr or Harr occupied 505 in the 1946 canvass. That remains the next decisive check.
'''
wr(CAP, capture)

# Source register
sources = [
    (S_AUG, "Sandy Post, 1 August 1946, Clackamas County Directory compilation advertisement", "Primary newspaper OCR/text only", "1 August 1946", URL_AUG, E_PROD, "Pacific Directory Service county-wide directory campaign; house-to-house canvass and rural questionnaire methodology. Scan not visually certified in this pass."),
    (S_SEP, "Sandy Post, 5 September 1946, Clackamas County Directory compilation notice", "Primary newspaper OCR/text only", "5 September 1946", URL_SEP, E_PROD, "Follow-up Pacific Directory Service county-wide compilation notice; canvass/questionnaire fields. Scan not visually certified in this pass."),
    (S_CITY, "Oregon City Commission, March 3 1948 February claims, Pacific Directory Service Directory", "Primary municipal OCR/text only", "3 March 1948 meeting; report covers February 1948 claims", URL_CITY, E_ROUTE, "Municipal p.477 extracted table places Pacific Directory Service in vendor sequence and Directory in item sequence. Exact dollar amount withheld pending visual table inspection."),
    (S_LIB, "Sandy Post, 8 July 1948, new Clackamas County Directory at Sandy library branch", "Primary newspaper OCR/text only", "8 July 1948", URL_LIB, E_ROUTE, "Contemporary notice that a new Clackamas County Directory was available at Sandy branch of the county library. Publisher/edition not printed in notice."),
    (S_CCHS, "CCHS 2012 Facts You Should Know About Oregon City citing Pacific Directory 1947-48", "Institutional secondary web source", "27 February 2012", URL_CCHS, E_ROUTE, "CCHS explicitly credits Pacific Directory, 1947-48; strong modern retrieval/provenance lead, not target occupancy evidence."),
    (S_OC, "Oregon City 2000 Downtown Final Report bibliography, Pacific Directory Service Directory of Clackamas County 1948", "Official secondary bibliography", "2000", URL_OC, E_ROUTE, "Official bibliography identifies Pacific Directory Service, Directory of Clackamas County, Portland, 1948."),
    (S_LO, "Lake Oswego 2014 historic survey bibliography, Pacific Directory Service 1947-1948 Directory of Clackamas County", "Official secondary bibliography", "2014", URL_LO, E_ROUTE, "Official bibliography uses the 1947-1948 date form for Pacific Directory Service Directory of Clackamas County."),
    (S_FS, "FamilySearch catalog 95422 Oregon City directory, 1960-forward R. L. Polk control", "Current institutional catalog HTML", "catalog reviewed 4 September 2026", URL_FS, E_ROUTE, "Control/exclusion: catalog 95422 is R. L. Polk, publication 1960-forward, and does not establish the 1947-48 Pacific Directory Service volume."),
]
for sid, name, typ, date, url, eid, notes in sources:
    append_once("evidence/source-register.md", f"## {sid} —", f'''## {sid} — {name}
Type: {typ}.
Date: {date}.
URL: {url}
Related evidence: `{eid}`.
Capture: `{CAP}`.
Notes: {notes}''')

# Evidence register
append_once("evidence/evidence-register.md", f"## {E_PROD} —", f'''## {E_PROD} — Pacific Directory Service county-directory data collection underway August–September 1946
Type: Primary newspaper OCR/text-only production evidence; sources `{S_AUG}` and `{S_SEP}`.
Evidence state: **DOCUMENTED / DIRECT** for the 1946 compilation campaign and collection method; **STRONG CROSS-SOURCE INFERENCE** that this campaign produced the later-labeled 1947–48/1948 Clackamas County volume.
Claims:
- Pacific Directory Service was compiling a new county-wide Clackamas County directory in August and September 1946.
- Incorporated-city data was to be gathered by house-to-house canvass; rural data used more than 15,000 mailed questionnaires.
- Requested/listed fields included business/occupation and home/business address data, making the volume directly relevant to 505 Main occupancy research.
- The eventual printed year must not automatically be treated as the observation date because the documented canvass began in 1946.
Confidence: Very High for the OCR-described compilation method; High but not direct for linkage to the later 1947–48/1948 edition.
Related sources: `{S_AUG}`, `{S_SEP}`.
Related businesses: `BUS-013`, `BUS-014`.
Related building: `B-002`.
Record: `{CAP}`.''')

append_once("evidence/evidence-register.md", f"## {E_ROUTE} —", f'''## {E_ROUTE} — 1947–48 Clackamas County Directory publication/availability and retrieval route
Type: Cross-source publication/holdings reconstruction; sources `{S_CITY}`, `{S_LIB}`, `{S_CCHS}`, `{S_OC}`, `{S_LO}`, `{S_FS}`.
Evidence state: **DOCUMENTED / DIRECT** for each source's own statement; **STRONG CROSS-SOURCE INFERENCE** that the bibliographic 1947–48 and 1948 labels describe the same Pacific Directory Service county volume and that the 1946 campaign produced it.
Claims:
- Oregon City's March 3, 1948 report of February claims includes Pacific Directory Service and an item described as Directory; the flattened OCR does not safely preserve the amount.
- By 8 July 1948 the Sandy branch of the Clackamas County library had a newly issued Clackamas County Directory available for use.
- CCHS later explicitly used a source it called Pacific Directory, 1947-48.
- Oregon City's 2000 bibliography cites Pacific Directory Service, Directory of Clackamas County, 1948; Lake Oswego's 2014 survey cites Pacific Directory Service, 1947–1948 Directory of Clackamas County.
- FamilySearch catalog 95422 is a 1960-forward R. L. Polk series and is not the target 1947–48 Pacific Directory Service edition.
Confidence: Very High for the individual source statements; High for the edition-identity/provenance reconstruction; no confidence upgrade to Farr/Harr occupancy until the actual target pages are inspected.
Related sources: `{S_CITY}`, `{S_LIB}`, `{S_CCHS}`, `{S_OC}`, `{S_LO}`, `{S_FS}`.
Related businesses: `BUS-013`, `BUS-014`.
Related building: `B-002`.
Record: `{CAP}`.''')

# Structured sources
sy = rd("database/sources.yml").rstrip()
for sid, name, typ, date, url, eid, notes in sources:
    if f"  - id: {sid}\n" in sy:
        continue
    safe_name = name.replace('"', "'")
    safe_type = typ.replace('"', "'")
    safe_date = date.replace('"', "'")
    safe_notes = notes.replace('"', "'")
    sy += f'''\n\n  - id: {sid}
    name: "{safe_name}"
    type: "{safe_type}"
    date: "{safe_date}"
    url: "{url}"
    notes: "{safe_notes}"
    related_evidence: [{eid}]'''
wr("database/sources.yml", sy + "\n")

# Structured evidence
ey = rd("database/evidence.yml").rstrip()
if f"  - id: {E_PROD}\n" not in ey:
    ey += f'''\n\n  - id: {E_PROD}
    name: "Pacific Directory Service county-directory data collection underway August-September 1946"
    type: "Primary newspaper OCR/text-only production evidence"
    claims:
      - "Pacific Directory Service was compiling a county-wide Clackamas County directory in August-September 1946 using house-to-house canvassing in incorporated cities and more than 15,000 rural questionnaires."
      - "The eventual printed directory year must not automatically be used as an exact occupancy observation date."
      - "Linkage of the 1946 campaign to the later 1947-48/1948 county volume is a strong cross-source inference, not direct proof."
    confidence: "Very High for compilation method; High but not direct for edition linkage."
    related_sources: [{S_AUG}, {S_SEP}]
    related_businesses: [BUS-013, BUS-014]
    related_buildings: [B-002]
    repository_file: {CAP}'''
if f"  - id: {E_ROUTE}\n" not in ey:
    ey += f'''\n\n  - id: {E_ROUTE}
    name: "1947-48 Clackamas County Directory publication availability and retrieval route"
    type: "Cross-source publication and holdings reconstruction"
    claims:
      - "Oregon City's March 3 1948 report of February claims includes Pacific Directory Service and a Directory item; exact dollar amount is withheld because OCR flattened the table geometry."
      - "A new Clackamas County Directory was available at the Sandy branch of the county library by July 8 1948."
      - "CCHS later explicitly used Pacific Directory, 1947-48; official Oregon City and Lake Oswego bibliographies identify Pacific Directory Service and use 1948 versus 1947-1948 date forms."
      - "FamilySearch catalog 95422 is a 1960-forward R. L. Polk series, not the target Pacific Directory Service volume."
    confidence: "Very High for individual source statements; High for edition/provenance reconstruction; target Farr/Harr listing still uninspected."
    related_sources: [{S_CITY}, {S_LIB}, {S_CCHS}, {S_OC}, {S_LO}, {S_FS}]
    related_businesses: [BUS-013, BUS-014]
    related_buildings: [B-002]
    repository_file: {CAP}'''
wr("database/evidence.yml", ey + "\n")

# Correct overprecision and link the dedicated route in the existing reconstruction capture.
recon = "evidence/source-captures/1945-1948-liquor-license-list-reconstruction-pass-2026-09-04.md"
replace_once(
    recon,
    "On municipal page **477**, the claims text pairs **Pacific Directory Service** with the description **Directory** and an amount of **$9.75** in the OCR-aligned expense list.",
    "On municipal page **477**, the extracted claims text places **Pacific Directory Service** in the vendor sequence and **Directory** in the corresponding item-description sequence. Because the OCR/text extraction flattens the multi-column table, the dollar amount cannot be safely assigned without visual page inspection; the previous **$9.75** reading is withdrawn as overprecise."
)
insert_before(
    recon,
    "## Current Farr → Harr conclusion",
    "### Dedicated 1946–1948 production / retrieval reconstruction",
    f'''### Dedicated 1946–1948 production / retrieval reconstruction

See `{CAP}` (`{E_PROD}` / `{E_ROUTE}`). New 1 August and 5 September 1946 *Sandy Post* notices establish that Pacific Directory Service was then gathering county-directory data through house-to-house canvassing and rural questionnaires. This means an eventual Farr/Harr hit in the volume later labeled 1947–48/1948 cannot be dated solely from the printed edition year; the front matter and listing context must be checked for canvass/publication lag.

The same reconstruction also preserves the February 1948 Oregon City directory expense, July 1948 Sandy-library availability, CCHS's later explicit use of a Pacific Directory 1947-48, official bibliographic variants, and the FamilySearch 95422 exclusion.'''
)

# Business-page research cautions.
for path, marker, text in [
    ("businesses/farrs-pool-hall.md", "## 1946–1948 county-directory timing caution", f'''## 1946–1948 county-directory timing caution

The target Pacific Directory Service county volume later cited as **1947–48 / 1948** is now tied to a documented county-wide data-gathering campaign underway in **August–September 1946** (`{E_PROD}` / `{CAP}`). If Farr appears in the eventual directory pages, do not treat the printed edition year as an exact 1947 or 1948 occupancy date without the volume's front matter and listing context.'''),
    ("businesses/harrs-recreation-center.md", "## 1946–1948 county-directory timing caution", f'''## 1946–1948 county-directory timing caution

The target Pacific Directory Service county volume later cited as **1947–48 / 1948** is now tied to a documented county-wide data-gathering campaign underway in **August–September 1946** (`{E_PROD}` / `{CAP}`). If Harr / Harr's Recreation Center appears at 505 in the eventual directory pages, the listing may reflect a late-1946 canvass rather than a condition first observed in 1948; the actual page and front matter remain required.'''),
]:
    append_once(path, marker, text)

# Research lead / log.
append_once("evidence/research-leads.md", "### Recover Pacific Directory Service 1947–48 Clackamas County volume", f'''### Recover Pacific Directory Service 1947–48 Clackamas County volume

Highest-value Farr→Harr source target. The production/retrieval reconstruction in `{CAP}` (`{E_PROD}` / `{E_ROUTE}`) shows county-wide data gathering underway in Aug.–Sep. **1946**, a Pacific Directory Service **Directory** expense in Oregon City's February 1948 claims cycle, county-library availability by 8 July 1948, and CCHS's later explicit use of a **Pacific Directory, 1947-48**.

Primary route: **Wilmer Gardner Research Library / Clackamas County Family History Society and CCHS**. Request the actual volume/title page and scans of all Harr, Farr, 505/505½ Main, 501–511 Main, and pool/billiards/recreation classified/address sections. Also capture front matter describing canvass and publication dates. Historic Ticor Title Company citations are a secondary provenance lead. FamilySearch catalog 95422 is excluded because it begins with the 1960 R. L. Polk series.''')

append_once("registers/research-log.md", "### 2026-09-04 — 1946–48 Clackamas County Directory production and retrieval route", f'''### 2026-09-04 — 1946–48 Clackamas County Directory production and retrieval route
- Added `{CAP}` with new evidence `{E_PROD}` / `{E_ROUTE}` and sources `{S_AUG}`–`{S_FS}`.
- 1 Aug. and 5 Sep. 1946 *Sandy Post* notices show Pacific Directory Service actively compiling a county-wide directory using house-to-house canvassing plus more than 15,000 rural questionnaires. Newspaper scan images were not visually certified, so these remain OCR/TEXT ONLY.
- Corrected the existing March 1948 municipal directory clue: the text extraction supports Pacific Directory Service + Directory in the February-claims table, but **not a safely assigned dollar amount**; the earlier `$9.75` statement is withdrawn pending visual table inspection.
- Preserved 8 Jul. 1948 Sandy-library availability, CCHS's later use of **Pacific Directory, 1947-48**, official 1947-48/1948 bibliographic variants, historic Ticor provenance, and FamilySearch catalog 95422 as a non-target 1960-forward Polk series.
- Key interpretive change: any eventual Farr/Harr hit in the 1947–48 directory may reflect **late-1946 canvass data** and must not be dated mechanically from the edition label.
- Farr's Pool Hall → Harr's Recreation Center transition date remains unresolved.''')

print(f"Integrated {CAP}; sources {S_AUG}-{S_FS}; evidence {E_PROD},{E_ROUTE}; transition date unchanged.")
