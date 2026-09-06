from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise April visual review and page-8 gap — 2026-09-06"
CAPTURE_REL = "evidence/source-captures/1917-enterprise-april-06-27-visual-review-2026-09-06.md"
MANIFEST_REL = "newspapers/oregon-city-enterprise/1917-april/manifest.json"
RECOVERY_REL = "newspapers/oregon-city-enterprise/1917-april/recovery-april13-page8/recovery-manifest.json"
PERSON_REL = "people/profiles/w-s-eddy.md"
BUSINESS_REL = "businesses/fashion-stable.md"
WB_EDDY_REL = "businesses/w-b-eddys-store-1917.md"
BUILDING_427_REL = "buildings/427-main.md"


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


def insert_before_first(rel, pattern, block, marker=MARKER):
    text = read(rel)
    if marker in text:
        return False
    m = re.search(pattern, text, re.M)
    if not m:
        return append_once(rel, block, marker)
    prefix = text[:m.start()]
    suffix = text[m.start():]
    if not prefix.endswith("\n"):
        prefix += "\n"
    write(rel, prefix + "\n" + block.strip() + "\n\n" + suffix)
    return True


for rel in (MANIFEST_REL, RECOVERY_REL):
    if not (ROOT / rel).exists():
        raise SystemExit(f"Required preserved file missing: {rel}")

RETRIEVAL_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()
RECOVERY_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", RECOVERY_REL], cwd=ROOT, text=True
).strip()
if not RETRIEVAL_COMMIT or not RECOVERY_COMMIT:
    raise SystemExit("Could not determine April retrieval/recovery commit")

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
people_index = read("people/people-index.md")
business_index = read("businesses/business-index.md")
manual_text = read("MANUAL-FOLLOWUP.md")

source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
person_nums = [int(x) for x in re.findall(r"\| P-(\d{3}) \|", people_index)]
business_nums = [int(x) for x in re.findall(r"\| BUS-(\d{3}) \|", business_index)]
manual_nums = [int(x) for x in re.findall(r"\bMF-(\d{3})\b", manual_text)]
if not all((source_nums, evidence_nums, person_nums, business_nums, manual_nums)):
    raise SystemExit("Could not determine one or more current ID maxima")

SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"
PERSON_ID = f"P-{max(person_nums)+1:03d}"
BUSINESS_ID = f"BUS-{max(business_nums)+1:03d}"
MANUAL_ID = f"MF-{max(manual_nums)+1:03d}"

# Idempotent recovery if a previous run already created the capture/entities.
if (ROOT / CAPTURE_REL).exists():
    cap = read(CAPTURE_REL)
    for label, pat in [
        ("source", r"source `(S-\d{3})`"),
        ("evidence", r"evidence `(E-\d{3})`"),
        ("person", r"person `(P-\d{3})`"),
        ("business", r"business `(BUS-\d{3})`"),
        ("manual", r"manual callout `(MF-\d{3})`"),
    ]:
        m = re.search(pat, cap)
        if not m:
            raise SystemExit(f"Existing April capture lacks recoverable {label} ID")
        if label == "source": SOURCE_ID = m.group(1)
        elif label == "evidence": EVIDENCE_ID = m.group(1)
        elif label == "person": PERSON_ID = m.group(1)
        elif label == "business": BUSINESS_ID = m.group(1)
        elif label == "manual": MANUAL_ID = m.group(1)

if (ROOT / PERSON_REL).exists():
    m = re.search(r"Person ID: `(P-\d{3})`", read(PERSON_REL))
    if m: PERSON_ID = m.group(1)
if (ROOT / BUSINESS_REL).exists():
    m = re.search(r"Business ID: `(BUS-\d{3})`", read(BUSINESS_REL))
    if m: BUSINESS_ID = m.group(1)

capture = f'''# 1917 Oregon City Enterprise — April 6, 13, 20 and 27 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 31 genuine intended-date pages; 6/20/27 April are complete 8/8, 13 April is 7/8 with true printed page 8 a RETRIEVAL GAP. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; person `{PERSON_ID}`; business `{BUSINESS_ID}`; manual callout `{MANUAL_ID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-april/`  
Original retrieval commit: `{RETRIEVAL_COMMIT}`  
Manifest: `{MANIFEST_REL}`  
Recovery audit: `{RECOVERY_REL}`  
Recovery commit: `{RECOVERY_COMMIT}`

## Scope and page-identity audit

All **32 archive-supplied April slots** were rendered and visually inspected. Because the March pass exposed a source-association defect, the April pass separately checked printed mastheads and page numbers instead of trusting archive sequence metadata.

| Archive issue bucket | Exposed slots | Genuine matching issue pages | Status |
| --- | ---: | ---: | --- |
| 6 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 13 April 1917 | 8 | 7 | **PARTIAL 7/8 — true printed Page 8 RETRIEVAL GAP** |
| 20 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 27 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |

The archive object exposed as **13 April sequence 8 / Page 8** is not a printed Page 8. Enlarged visual inspection shows **PAGE 6** at upper left. Its masthead prints **THURSDAY, APRIL [obscured], 1917**, with the date numeral physically obscured/marked and a handwritten `13` above the date area. The normal sequence 6 is already a separate Friday 13 April printed Page 6. Sequence 8 is therefore preserved as a **second Page-6/source variant**, not silently counted as Page 8.

The dedicated recovery audit tested Oregon PDF/JP2/OCR/XML/RDF/HTML derivatives, ed-1 sequences 9–12, editions 2–4, neighboring-issue source objects, Chronicling America/LOC routes, and LOC JSON discovery. No hidden replacement sequence or alternate edition exposed the true printed Page 8. All Oregon derivatives of seq-8 resolve to the same printed Page-6 variant. The true **13 April 1917 printed Page 8** is retained as **RETRIEVAL GAP / manual callout `{MANUAL_ID}`**, not as negative evidence.

With 105 genuine intended-date Enterprise pages through March, April adds **31**, making **136 genuine intended-date pages visually verified through April**. The archive has supplied **138 January-April slots**, two of which are source-association substitutions/gaps (16 Mar p5 and 13 Apr p8). **278 later May-December exposed slots remain unreviewed.**

## Direct April findings

### W. S. Eddy / Fashion Stable relative-location change

Repeated professional advertisements in the visually reviewed April issues identify **W. S. Eddy, V.S., M.D.V.** and say he is established at the **Fashion Stable, between Fourth and Fifth on Main Street**. The wording is directly visible on 6 April p.7 and recurs in the later April p.7 advertisements.

This materially changes the existing Fashion Stable chronology. The archive's visually verified 1915 Enterprise evidence (`E-112` / `S-124`, continued under `E-114` / `S-128`) places **W. S. Eddy at the Fashion Stable on Fifth Street between Main and Water Streets**. The exact initials, veterinary credentials and Fashion Stable name make the 1915 and 1917 observations a strong same-person/same-business bridge, while the different relative location means the archive must allow a **move, changed stable premises, or changed advertisement-location wording sometime after the 1915 observation and by April 1917**. No exact move date or street number is inferred.

This is **not** a bridge to **W. B. Eddy's Store (`BUS-100`) at 427 Main**. W. B. and W. S. remain separate printed identities. The April relative wording also does not prove that Fashion Stable was 427 Main, 110 Fifth, or any other numbered premises.

Because W. S. Eddy / Fashion Stable now has a multi-date chronology and a location-change problem requiring explanation, this integration promotes stable person `{PERSON_ID}` and business `{BUSINESS_ID}` records.

### Fifth/Main parade and Strebig context

**13 April p.1** directly reports that the preparedness parade started from **Fifth and Main streets at 7:30 p.m.** and that **Henry Strebig headed the line of march carrying a large American flag**. This is useful civic/person/intersection context only. It does not place Strebig's meat market at the target numbered storefronts on that date and does not alter the separate 427 Main former-Strebig-business evidence.

### Annie L. Farr and Farr Brothers identity controls

**20 April p.3** directly prints a real-estate transfer: **Annie L. Farr to W. P. Morris and Viola Morris, lot 6, block 92, Oregon City; $1.** This is a dated Oregon City Farr identity/property context. It does not identify Annie with Alice Farr, Edwin F. Farr, or the later 505 Main pool hall. The February source separately printed **Annis L. Farr**; spelling similarity is retained as an identity question, not normalized into one person.

**20 April p.8** directly includes **Farr Bros.** in county-poor expenditures. That reinforces the already separated Farr Brothers supplier/business context but supplies no 505 Main address and no bridge to Edwin/Alice Farr. Numeric strings such as dollar amounts that resemble target street numbers are rejected as address evidence.

## Exact target-address result

Across the **31 genuine intended-date April pages recovered and visually reviewed**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact **427 Main** occupant was established.

The unrecovered true 13 April Page 8 is excluded from that bounded no-hit statement. Nothing in the April silence or page gap proves vacancy, demolition, non-use, or absence of a target storefront.

## Cross-record propagation audit

Reviewed against this batch: `buildings/503-main.md`, `buildings/505-main.md`, `timelines/503-main.md`, `timelines/505-main.md`, `buildings/427-main.md`, `businesses/w-b-eddys-store-1917.md`, the Farr person/business records, `people/people-index.md`, `businesses/business-index.md`, `database/people.yml`, `database/businesses.yml`, `timeline.md`, `registers/address-register.md`, `registers/business-timeline.md`, `evidence/open-questions.md`, `evidence/research-leads.md`, and `indexes/id-crosswalk.md`.

**Propagation decision:**
- Promote W. S. Eddy / Fashion Stable to stable person/business records because the evidence is now multi-date and location-conflict-heavy.
- Update the master/address/business chronology and the 427/W. B. Eddy no-merge guard.
- Update open questions/leads with the new Fashion Stable location-change problem and April Page-8 retrieval gap.
- Do **not** add a 1917 503/505 occupant/building event: the batch establishes none.
- Do **not** create a numbered Fashion Stable building: both 1915 and 1917 evidence are relative-location statements.
- Do **not** merge Annie/Annis L. Farr, Farr Brothers, Edwin F. Farr, Alice Farr, W. S. Eddy, W. B. Eddy, or the earlier A. J. Eddy wording without independent bridges.

## Effect on 1917 status

1917 remains **IN PROGRESS**. Enterprise now has **136 genuine intended-date pages visually verified through April**, two known Enterprise page-level retrieval gaps (16 March p5 and 13 April p8), and **278 May-December exposed slots** still requiring page-by-page visual review. Existing Courier and directory/source-class blockers remain separately active.
'''
if not (ROOT / CAPTURE_REL).exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Enterprise, April 1917 scan-first visual-review batch with Page-8 source conflict
<!-- {MARKER} -->
Type: Primary newspaper page scans plus derivative-recovery audit; **32/32 exposed slots visually inspected, 31 genuine intended-date pages recovered**.  
Publication: *Oregon City Enterprise*  
Issue dates: 6, 13, 20 and 27 April 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-04-13/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-april/`  
Manifest: `{MANIFEST_REL}`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Recovery manifest: `{RECOVERY_REL}`  
Recovery commit: `{RECOVERY_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`. Manual callout: `{MANUAL_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: 13 April seq-8 visibly prints PAGE 6 and a Thursday masthead with altered/obscured date, while normal seq-6 is already Friday Page 6. True printed Page 8 remains unrecovered. April directly advances W. S. Eddy/Fashion Stable to Main between Fourth and Fifth, differing from the 1915 Fifth-between-Main-and-Water location. No exact target-number occupant was established.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — April 1917 Enterprise audit finds Page-8 gap and advances W. S. Eddy / Fashion Stable chronology
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper visual review plus source-recovery audit  
Claims:
- All **32 exposed April archive slots** were visually inspected; **31 are genuine intended-date pages**.
- 13 April seq-8 visibly prints **PAGE 6** and a **Thursday** masthead with the date physically obscured/marked; normal seq-6 is separately the Friday Page 6. True 13 April printed Page 8 remains a **RETRIEVAL GAP** under `{MANUAL_ID}` after derivative, hidden-sequence, alternate-edition and LOC recovery attempts.
- Enterprise cumulative genuine intended-date coverage through April is **136 pages**; **278 May-December exposed slots remain**.
- Repeated April p.7 ads directly place **W. S. Eddy, V.S., M.D.V., at Fashion Stable between Fourth and Fifth on Main Street**. This differs from visually verified 1915 evidence placing W. S. Eddy/Fashion Stable on Fifth between Main and Water; exact move date and number remain unresolved.
- 13 April p.1 directly places a preparedness parade start at Fifth/Main and names Henry Strebig as line leader; civic context only, not storefront occupancy.
- 20 April p.3 directly records **Annie L. Farr -> W. P. Morris and Viola Morris, lot 6, block 92, Oregon City, $1**; no bridge to Alice/Edwin Farr or 505 Main.
- 20 April p.8 directly includes **Farr Bros.** in county-poor expenditures; no 505 address or Edwin/Alice bridge.
- No defensible exact **501/503/505/507/509/511 Main** occupant and no new exact 427 Main occupant was established on the 31 genuine intended-date pages.
Classification: **DOCUMENTED / DIRECT** for visible page identity, relative-location wording, transfer, parade and expenditure wording; **STRONG CROSS-SOURCE IDENTITY** for W. S. Eddy/Fashion Stable across 1915 and 1917; **RETRIEVAL GAP** for true 13 April Page 8; **NO-MERGE / COVERAGE RESULT ONLY** for the guarded identities and target no-hit.  
Confidence: **Very High** for the direct scan readings and page conflict; no exact move date, numbered Fashion Stable premises, vacancy or target occupancy is inferred.'''
append_once("evidence/evidence-register.md", evidence_block)

# Stable person/business pages now warranted by multi-date chronology and location conflict.
if not (ROOT / PERSON_REL).exists():
    write(PERSON_REL, f'''# W. S. Eddy

Person ID: `{PERSON_ID}`. Related business: `{BUSINESS_ID}` (Fashion Stable).

## Documented chronology

- **23 April 1915 and later 1915 notices:** visually verified Enterprise evidence places **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, Fifth Street between Main and Water Streets** (`E-112` / `S-124`; continued `E-114` / `S-128`). No street number is printed.
- **6–27 April 1917:** repeated visually reviewed professional ads place **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street** (`{EVIDENCE_ID}` / `{SOURCE_ID}`). No street number is printed.

The identical initials, professional credentials and Fashion Stable name strongly bridge these as the same W. S. Eddy/business chronology. The changed relative location supports a move, changed stable premises, or changed location wording by April 1917, but does not establish the exact move date.

## Identity limits

Do **not** merge W. S. Eddy with **W. B. Eddy / W. B. Eddy's Store (`BUS-100`) at 427 Main** merely by surname and initial. The printed initials differ and no source currently bridges them. Earlier 1915 **A. J. Eddy** wording likewise remains separate unless independently reconciled.

Do not assign W. S. Eddy/Fashion Stable to 427 Main, 110 Fifth, or another numbered building from the relative-location wording alone.
''')

if not (ROOT / BUSINESS_REL).exists():
    write(BUSINESS_REL, f'''# Fashion Stable

Business ID: `{BUSINESS_ID}`. Related person: W. S. Eddy (`{PERSON_ID}`). Exact numbered premises unresolved.

## Relative-location chronology

- **1915:** W. S. Eddy professional notices place Fashion Stable on **Fifth Street between Main and Water Streets** (`E-112` / `S-124`; continued `E-114` / `S-128`).
- **April 1917:** repeated ads place Fashion Stable **between Fourth and Fifth on Main Street** (`{EVIDENCE_ID}` / `{SOURCE_ID}`).

This is direct evidence for two dated relative locations and a strong same-business bridge through W. S. Eddy's repeated name/credentials. It is not proof of a specific move date, lease, ownership, or physical-building continuity.

## Guardrails

- Do not equate Fashion Stable with the 1914–1915 water-ledger **110 Fifth / Stable** record without an exact-number bridge.
- Do not assign the April 1917 stable to **427 Main** merely because 427 lies within the Fourth/Fifth Main block.
- Do not merge W. S. Eddy with **W. B. Eddy's Store (`BUS-100`)** at 427 Main.
- No connection to 501/503/505 is established by these relative-location ads.
''')

# Markdown index entries.
if f"| {PERSON_ID} |" not in read("people/people-index.md"):
    append_once("people/people-index.md", f'''## April 1917 Enterprise entity promotion
<!-- {MARKER} -->

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| {PERSON_ID} | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 notices place him/Fashion Stable on Fifth between Main/Water; April 1917 ads place Fashion Stable on Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. `{EVIDENCE_ID}` / `{SOURCE_ID}`. |''')

if f"| {BUSINESS_ID} |" not in read("businesses/business-index.md"):
    append_once("businesses/business-index.md", f'''## April 1917 Enterprise entity promotion
<!-- {MARKER} -->

| ID | Business | Address / location | Notes |
| --- | --- | --- | --- |
| {BUSINESS_ID} | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; April 1917 Main between Fourth/Fifth; no number | Multi-date relative-location chronology through W. S. Eddy; possible move/location-wording change. No 110 Fifth, 427 Main, or target-frontage assignment. `{EVIDENCE_ID}` / `{SOURCE_ID}`. |''')

# YAML source/evidence.
sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Enterprise, April 1917 scan-first visual-review batch with Page-8 source conflict"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-04-13/ed-1/"
    type: "Primary newspaper page scans plus recovery audit; 32 exposed slots inspected, 31 genuine intended-date pages"
    date: "1917-04-06 through 1917-04-27"
    repository_file: "{CAPTURE_REL}"
    notes: "True 13 April printed Page 8 remains unrecovered; April advances W. S. Eddy/Fashion Stable relative location to Main between Fourth and Fifth."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "April 1917 Enterprise audit finds Page-8 gap and advances W. S. Eddy / Fashion Stable chronology"
    type: "Primary newspaper visual review plus source-recovery audit"
    date: "1917-04-06 through 1917-04-27"
    claims:
      - "All 32 exposed April slots were inspected; 31 are genuine intended-date pages."
      - "13 April seq-8 is visibly printed Page 6; true printed Page 8 remains a retrieval gap."
      - "Enterprise cumulative genuine intended-date coverage through April is 136 pages; 278 later exposed slots remain."
      - "Repeated April ads place W. S. Eddy / Fashion Stable between Fourth and Fifth on Main, differing from the 1915 Fifth-between-Main-and-Water location."
      - "20 April p3 records Annie L. Farr conveying lot 6 block 92 Oregon City for $1; identity with Alice/Annis/Edwin Farr is not established."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established on the 31 genuine intended-date pages."
    confidence: "Very High for direct scan readings; location-change and identity limits preserved."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

people = read("database/people.yml")
if re.search(rf"(?m)^  - id: {re.escape(PERSON_ID)}$", people) is None:
    people = people.rstrip() + f'''

  - id: {PERSON_ID}
    name: W. S. Eddy
    repository_file: {PERSON_REL}
    role: Veterinarian / Fashion Stable professional
    notes: >-
      Visually verified 1915 notices place W. S. Eddy / Fashion Stable on Fifth Street between Main and Water; repeated April 1917 ads place the stable on Main between Fourth and Fifth. Exact move date and number unresolved. Do not merge with W. B. Eddy or earlier A. J. Eddy wording without a bridge.
    related_businesses: [{BUSINESS_ID}]
    related_evidence: [E-112, E-114, {EVIDENCE_ID}]
    related_sources: [S-124, S-128, {SOURCE_ID}]
''' + "\n"
    write("database/people.yml", people)

businesses = read("database/businesses.yml")
if re.search(rf"(?m)^  - id: {re.escape(BUSINESS_ID)}$", businesses) is None:
    businesses = businesses.rstrip() + f'''

  - id: {BUSINESS_ID}
    name: Fashion Stable
    repository_file: {BUSINESS_REL}
    address: "1915 Fifth Street between Main and Water; April 1917 Main Street between Fourth and Fifth; exact number unresolved"
    notes: >-
      Multi-date relative-location chronology through W. S. Eddy. The changed wording supports a move, changed premises, or changed location description but does not establish exact move date, title, lease, or numbered building. Not assigned to 110 Fifth, 427 Main, or 501/503/505.
    related_people: [{PERSON_ID}]
    related_evidence: [E-112, E-114, {EVIDENCE_ID}]
    related_sources: [S-124, S-128, {SOURCE_ID}]
''' + "\n"
    write("database/businesses.yml", businesses)

# Manual retrieval gap.
manual_block = f'''---

## 6 September 2026 — April 1917 Enterprise source-page retrieval gap
<!-- {MARKER} -->

| ID | Audited disposition | Still needed? | Audit decision |
| --- | --- | --- | --- |
| **{MANUAL_ID}** | **YEAR-CLOSEOUT / MANUAL CALLOUT** | **Yes for 1917 manual completion** | Obtain the **true printed Page 8 of the 13 April 1917 Oregon City Enterprise** from Oregon City Public Library microfilm, Oregon Digital Newspaper Program source microfilm/original, or another institutional copy. The online archive's seq-8 object visibly prints **PAGE 6** and a Thursday masthead with an obscured/marked date, while seq-6 is already the normal Friday Page 6. PDF/JP2/OCR/RDF, ed-1 seq9-12, editions 2-4, neighboring-object, Chronicling America/LOC and LOC-index recovery did not expose the true Page 8. Inspect any institutional replacement visually for target addresses/businesses and integrate it. Retrieval gap, not negative evidence. See `{CAPTURE_REL}` and `{RECOVERY_REL}`. |'''
append_once("MANUAL-FOLLOWUP.md", manual_block)

# Closeout/status/open-lead propagation.
append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise April audit added 6 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually inspects all **32 April archive slots**, credits **31 genuine intended-date pages**, and identifies true 13 April printed Page 8 as retrieval gap `{MANUAL_ID}` because seq-8 is visibly a second printed Page 6 variant. Enterprise cumulative genuine coverage is **136 pages through April**; **278 May-December slots remain**. April also promotes W. S. Eddy (`{PERSON_ID}`) / Fashion Stable (`{BUSINESS_ID}`): 1917 ads place the stable on Main between Fourth/Fifth, differing from the 1915 Fifth-between-Main-and-Water location. No exact 501/503/505/507/509/511 or new 427 occupant was established.''')

append_once("evidence/open-questions.md", f'''### 6 September 2026 — April 1917 Enterprise page gap and Fashion Stable location change
<!-- {MARKER} -->

`{EVIDENCE_ID}` / `{SOURCE_ID}` leaves the true **13 April printed Page 8** unrecovered under `{MANUAL_ID}`; the archive's seq-8 is visibly a second Page 6 variant. The 31 genuine intended-date April pages establish no target 501/503/505/507/509/511 occupant.

A separate direct finding now gives W. S. Eddy / Fashion Stable a location-change problem: 1915 evidence places the stable on **Fifth between Main and Water**, while repeated April 1917 ads place it **on Main between Fourth and Fifth**. Resolve whether the stable physically moved, the advertised office/stable relationship changed, or one relative-location wording described a different entrance/premises. Do not assign an exact number and do not merge W. S. Eddy with W. B. Eddy at 427 Main.''')

append_once("evidence/research-leads.md", f'''## 6 September 2026 — W. S. Eddy / Fashion Stable 1915–1917 location-change lead
<!-- {MARKER} -->

New `{SOURCE_ID}` / `{EVIDENCE_ID}` evidence promotes W. S. Eddy (`{PERSON_ID}`) and Fashion Stable (`{BUSINESS_ID}`) to stable entities. Compare 1915 notices (**Fifth Street between Main and Water**) with April 1917 notices (**Main Street between Fourth and Fifth**) and search 1915–1917 move notices, directories, city licenses, stable/livery ads, fire insurance maps, and property records for the transition. Keep **W. S. Eddy**, January 1917 **W. B. Eddy's Store at 427 Main**, and earlier **A. J. Eddy** wording separate unless a contemporary source bridges them. The result may sharpen 427/Fifth geography but is not currently a 427 assignment.

The same April batch leaves true 13 April printed Page 8 as retrieval gap `{MANUAL_ID}` and establishes no exact target-frontage occupant on the 31 genuine pages.''')

# 427/building and W.B. Eddy business guardrail updates.
append_once(BUILDING_427_REL, f'''## April 1917 W. S. Eddy / Fashion Stable nearby relative-location control
<!-- {MARKER} -->

`{EVIDENCE_ID}` / `{SOURCE_ID}` repeatedly places **W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street** in April 1917. This is a relative-location control within the same Main block as 427, but **does not print 427**. Do not assign Fashion Stable to this building or merge W. S. Eddy with the separately printed **W. B. Eddy's Store (`BUS-100`)** at 427 Main without an independent bridge.''')

append_once(WB_EDDY_REL, f'''## W. S. Eddy / Fashion Stable no-merge guard — April 1917
<!-- {MARKER} -->

April Enterprise ads (`{EVIDENCE_ID}` / `{SOURCE_ID}`) name **W. S. Eddy, V.S., M.D.V.** at Fashion Stable **between Fourth and Fifth on Main Street**. The initials differ from this business's **W. B. Eddy** wording. The relative block location is not enough to identify the men or businesses as the same, and Fashion Stable is not assigned to 427 Main.''')

# Address/business timeline and master chronology.
append_once("registers/address-register.md", f'''## 1915–1917 Fashion Stable relative-location change
<!-- {MARKER} -->

- `E-112` / `S-124` (continued `E-114` / `S-128`) places **W. S. Eddy / Fashion Stable on Fifth Street between Main and Water** in 1915.
- `{EVIDENCE_ID}` / `{SOURCE_ID}` places **W. S. Eddy / Fashion Stable on Main Street between Fourth and Fifth** repeatedly in April 1917.

Both are relative-location evidence. No numbered building record is created. Test a move or changed premises/entrance before mapping Fashion Stable to 110 Fifth, 427 Main, or another address.''')

append_once("registers/business-timeline.md", f'''## W. S. Eddy / Fashion Stable relative-location chronology
<!-- {MARKER} -->

| Period | Address / relative location | Business / person | IDs | Evidence | Limits |
| --- | --- | --- | --- | --- | --- |
| Apr.–Jun. 1915 verified span | Fifth Street between Main and Water | Fashion Stable / W. S. Eddy | `{BUSINESS_ID}` / `{PERSON_ID}` | `E-112`, `E-114`; `S-124`, `S-128` | Relative location only; no number. |
| 6–27 Apr. 1917 | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `{BUSINESS_ID}` / `{PERSON_ID}` | `{EVIDENCE_ID}` / `{SOURCE_ID}` | Repeated direct ads; exact move day/number unresolved. Not W. B. Eddy/427 by assumption. |''')

master_block = f'''## April 1917 — Fashion Stable shifts relative-location evidence
<!-- {MARKER} -->

Repeated *Oregon City Enterprise* professional ads place **W. S. Eddy (`{PERSON_ID}`) at Fashion Stable (`{BUSINESS_ID}`), between Fourth and Fifth on Main Street** (`{EVIDENCE_ID}` / `{SOURCE_ID}`). The archive's 1915 direct evidence had placed W. S. Eddy/Fashion Stable on **Fifth Street between Main and Water** (`E-112`, `E-114`). Treat this as a dated relative-location change supporting a possible move or changed premises/location wording, not as an exact move date or numbered-building assignment. It does not identify W. S. Eddy with W. B. Eddy's Store at 427 Main.

The same April batch reports a preparedness parade beginning at **Fifth and Main** with Henry Strebig leading the line; civic/intersection context only. True 13 April printed Page 8 remains a retrieval gap under `{MANUAL_ID}`.'''
insert_before_first("timeline.md", r"(?m)^## 1918\b", master_block)

# Crosswalk and entity-audit trail.
append_once("indexes/id-crosswalk.md", f'''## {PERSON_ID} / {BUSINESS_ID} — W. S. Eddy / Fashion Stable
<!-- {MARKER} -->

| Person | Business | Evidence / source | Building relationship |
| --- | --- | --- | --- |
| `{PERSON_ID}` W. S. Eddy | `{BUSINESS_ID}` Fashion Stable | 1915 `E-112`/`S-124`, `E-114`/`S-128`; April 1917 `{EVIDENCE_ID}`/`{SOURCE_ID}` | No numbered building assigned. 1915 relative location Fifth between Main/Water; April 1917 Main between Fourth/Fifth. No 110 Fifth or 427 Main bridge. |''')

append_once("registers/entity-page-audit-2026-08-29.md", f'''## 6 September 2026 follow-up — W. S. Eddy / Fashion Stable promotion
<!-- {MARKER} -->

April 1917 Enterprise review converts W. S. Eddy / Fashion Stable from peripheral relative-location mentions into a **multi-date, location-conflict-heavy chronology**, meeting this audit's promotion rule. Added person `{PERSON_ID}` and business `{BUSINESS_ID}` with standalone pages and YAML/index synchronization. No building ID is created because neither the 1915 nor 1917 notice prints an exact number.''')

# Year status and archive index.
year = read("registers/year-status.md")
lines = year.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = f"| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE_REL}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 unresolved. *Oregon City Enterprise*: **136 genuine intended-date pages through April**; 138 Jan-Apr archive slots inspected, with true 16 Mar p5 and true 13 Apr p8 retrieval gaps; **278 May-Dec exposed slots remain**. April promotes W. S. Eddy/Fashion Stable relative-location chronology but establishes no target-frontage occupant. Title-calendar reconciliation, Sohns & Woodbeck Oregon City directory section, and other source-class closeout remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

idx = read("ARCHIVE_INDEX.md")
m = re.search(r"(?m)^- \*\*1917 — IN PROGRESS:\*\*.*$", idx)
if m:
    repl = f"- **1917 — IN PROGRESS:** *Courier* reaches all 52 issue dates with **435 genuine pages visually verified** and true 13 Dec p21 unresolved. *Oregon City Enterprise*: **136 genuine intended-date pages through April**; true 16 Mar p5 and 13 Apr p8 remain retrieval gaps; **278 May-Dec exposed slots remain**. April adds W. S. Eddy/Fashion Stable relative-location chronology but no target-address occupant. Sohns & Woodbeck 1916–17 Oregon City directory section remains unresolved."
    idx = idx[:m.start()] + repl + idx[m.end():]
    write("ARCHIVE_INDEX.md", idx)

append_once("registers/research-log.md", f'''| 2026-09-06 | Completed gap-aware April 1917 Oregon City Enterprise audit | Inspected **32/32 exposed April slots**; **31 genuine intended-date pages**. Archive seq-8 for 13 Apr is visibly printed Page 6; true Page 8 remains `{MANUAL_ID}` after alternate recovery. Cumulative Enterprise genuine coverage **136 pages through April**; 278 later slots remain. Promoted W. S. Eddy `{PERSON_ID}` / Fashion Stable `{BUSINESS_ID}` because April ads move the relative location from 1915 Fifth-between-Main/Water to 1917 Main-between-Fourth/Fifth. Annie L. Farr transfer and Farr Bros expenditure contexts retained without 505/Edwin/Alice merge. No target-number occupant established. | Continue May Enterprise with printed-date/page-number audit before text backstop. |''')

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} / {PERSON_ID} / {BUSINESS_ID} / {MANUAL_ID}")
