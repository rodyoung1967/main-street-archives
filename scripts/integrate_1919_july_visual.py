#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 July online Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 July online Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-july-online-enterprise-courier-visual-review-2026-09-07.md"
SOURCE_NAME = "July 1919 online-exposed Oregon City Enterprise + final Courier visual-review batch"
EVIDENCE_NAME = "July 1919 online visual review: bounded target coverage with Banner-Courier retrieval gap"


def read(path): return Path(path).read_text(encoding='utf-8')
def write(path,text): Path(path).write_text(text,encoding='utf-8')
def append_once(path, marker, block):
    p=Path(path); text=p.read_text(encoding='utf-8')
    if marker in text: return False
    if not text.endswith('\n'): text+='\n'
    text += '\n'+block.strip()+'\n'; p.write_text(text,encoding='utf-8'); return True

def next_id(path,prefix):
    nums=[int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b",read(path))]
    if not nums: raise RuntimeError(f'No {prefix} ids in {path}')
    return f'{prefix}-{max(nums)+1:03d}'

def update_yaml_relation(path,entity_id,field,value):
    p=Path(path); text=p.read_text(encoding='utf-8')
    m=re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)",text)
    if not m: return False
    block=m.group(0)
    inline=re.search(rf"(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$",block)
    if inline:
        vals=[v.strip() for v in inline.group(1).split(',') if v.strip()]
        if value in vals: return False
        vals.append(value); repl=f"    {field}: ["+', '.join(vals)+']'
        block=block[:inline.start()]+repl+block[inline.end():]
    else:
        lines=block.splitlines(keepends=True); idx=None
        for i,line in enumerate(lines):
            if re.match(rf"^    {re.escape(field)}:\s*$",line.rstrip('\n')): idx=i; break
        if idx is None:
            if not block.endswith('\n'): block+='\n'
            block += f"    {field}: [{value}]\n"
        else:
            j=idx+1; vals=[]; item_indent=None
            while j<len(lines):
                im=re.match(r"^(\s*)-\s*(.+?)\s*\n?$",lines[j])
                if not im or len(im.group(1))<4: break
                item_indent=item_indent or im.group(1); vals.append(im.group(2).strip()); j+=1
            if value in vals: return False
            lines.insert(j,f"{item_indent or '      '}- {value}\n"); block=''.join(lines)
    p.write_text(text[:m.start()]+block+text[m.end():],encoding='utf-8'); return True

if Path(CAPTURE).exists():
    print('July capture already exists; refusing duplicate integration.'); sys.exit(0)
S=next_id('evidence/source-register.md','S')
E=next_id('evidence/evidence-register.md','E')

capture=f'''# July 1919 online-exposed Oregon City newspaper scan-first visual review

{MARKER}

Status: **ONLINE-EXPOSED PAGES VISUALLY VERIFIED — 38/38 recovered July pages inspected from original scans; Banner-Courier manual retrieval gap remains.**  
Annual status: **1919 IN PROGRESS**. January–July online-exposed local-newspaper visual coverage: **404 pages**.

Archive IDs: source `{S}`; evidence `{E}`.

## Title-transition inventory

Institutional holdings and the archive probe require July to be treated differently from January–June:

- *Oregon City Courier* holdings end with **3 July 1919**;
- the Courier and *Clackamas County Banner* merged on **8 July 1919**;
- *The Banner-Courier* holdings begin **17 July 1919**;
- the 1919 *Banner-Courier* issues are not exposed in the Historic Oregon Newspapers digitized run and remain a manual microfilm route under `MF-030`.

The first retrieval workflow incorrectly assumed a 10 July Courier issue and stopped when none was exposed. That was a calendar-model error, not negative evidence. The corrected inventory follows the institutional title transition and does **not** treat 10 July as a missing Courier issue.

## Scope actually visually reviewed

| Title | Issues reviewed | Pages | Status |
| --- | --- | ---: | --- |
| *Oregon City Courier* | 3 Jul. 1919 | **6/6** | Final issue in institutional holdings; visually reviewed |
| *Oregon City Enterprise* | 4, 11, 18, 25 Jul. 1919 | **32/32** | All four online-exposed July issues visually reviewed |
| *The Banner-Courier* | 17, 24, 31 Jul. 1919 | **0** | **RETRIEVAL GAP — manual microfilm (`MF-030`)** |
| **Online visual total** | **5 issues** | **38/38** | Banner-Courier gap excluded from visual count |

Preserved originals / manifests:
- `newspapers/oregon-city-courier/1919-july/`
- `newspapers/oregon-city-enterprise/1919-july/`
- `newspapers/banner-courier/1919-july/manifest.json`

Retrieval commit: `08b330b` (`Archive July 1919 Oregon City newspaper scans and gap manifests`).

Every one of the **38 recovered online pages** was visually checked from the scan image for printed title/date/page identity before text-assisted discovery. No substituted-page, duplicate-page, or printed-date defect was found in the recovered online set.

## Target frontage — 501 / 503 / 505 Main

Across the 38 visually reviewed online pages and the post-visual text-discovery backstop:

- no source-explicit **501 Main** occupant was recovered;
- no source-explicit **503 Main** occupant was recovered;
- no source-explicit **505 Main / 505½ Main** occupant was recovered;
- no source-explicit **507 / 507½ / 509 / 511 Main** target-neighbor occurrence was recovered;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move or fire event was recovered.

This conclusion applies **only to the 38 online-exposed pages**. It cannot be extended across the inaccessible 17/24/31 July *Banner-Courier* issues. It is bounded coverage, not vacancy/closure/non-use evidence.

## Re-encountered evidence — do not duplicate

### 18 and 25 July — unnamed cleaner/dyer, already `S-152` / `E-136`
The original **18 Jul. p7** and **25 Jul. p7** Enterprise scans were reopened during this monthly pass and visibly repeat:

- `Clothes cleaned, pressed and dyed.`
- **`500 Fifth and Main streets`**
- **`two doors south of new post office`**
- **Phone 260**

These exact July pages were already visually integrated in the cleaner-repeat set (`S-152`) strengthening `E-136`. The monthly review therefore references rather than re-registers the historical claim. Direct scan inspection again confirms the 25 July number is **500**, not the OCR misreading `600`. The wording is still not normalized to 500 Main or 500 Fifth, and the advertiser remains unidentified.

### 11 July — Gilbert Miller household item, already `S-160` / `E-144`
The **11 Jul. Enterprise p5** page was re-encountered during full-month inspection. Its Gilbert Miller household/relocation item was already visually integrated as `S-160` / `E-144`. It remains identity/residence context only: the item does not print Wolf & Miller, 505 Main, a legal partner, property ownership or construction.

## New monthly continuation controls

### Theroux Music House — 210 Seventh Street through 25 July
The **25 Jul. Enterprise p7** scan directly prints a classified for **Theroux Music House, 210 Seventh St.** (`{S}` / `{E}`). This extends the monthly business-address control through **25 July 1919** without establishing the exact move date from the earlier 519 Main premises.

### Farr Brothers — market-report appearances without address
Enterprise market reports on **11 Jul. p6, 18 Jul. p3 and 25 Jul. p6** credit **Brady Mercantile Company and Farr Brothers**. These are dated business appearances only. They print no exact address and no individual Farr proprietor; they do not bridge to Edwin/Alice Farr or Farr's Pool Hall at 505.

## Other target-like candidates resolved

- Personal items mentioning **Clem Dollar** on 4, 11 and 18 July provide no business premises and remain unrelated to the later exact 505½ pool-hall sequence.
- The **3 Jul. Courier p6** report that C. J. Hood would build a lumber-storage platform concerns the Hood Lumber Company tract behind the Oregon City Ice plant, not the target frontage.
- Other generic `new store`, lease, building, remodel and sale language found by text discovery was visually/contextually unrelated to 501/503/505.

## Banner-Courier retrieval gap

Direct July probing reconfirms that the **17, 24 and 31 July 1919 Banner-Courier issues are not exposed at the tested Historic Oregon Newspapers PDF route**. This is consistent with the already documented institutional availability record in `1919-1920-banner-courier-ocr-discovery.md` and remains `MF-030`.

The gap is especially important because it covers the exact interval after the Courier/Banner merger. No negative occupancy or construction conclusion may be drawn for those missing issues.

## Cross-record propagation audit

Updated: source/evidence registers and YAML; Theroux and Farr business/person controls; Banner-Courier access checkpoint; 1919–1920 construction checkpoint; business timeline; ID crosswalk; year-status; archive index; and research log.

Reviewed but deliberately **not** changed: 501/503/505 building records, ownership timeline, master historical timeline, Wolf/S. Wolf relations, Gilbert Miller/Wolf & Miller evidence, and cleaner evidence `E-136`. Those latter July claims were already integrated under their exact page-source IDs; duplicating them under the monthly batch would add no historical content.

No new manual-followup item is created. `MF-030` already exactly covers the inaccessible Banner-Courier interval.

## Next chronological step

Continue with **August 1919 Enterprise** online scans while preserving all August Banner-Courier dates as `MF-030` manual gaps. Do not count inaccessible Banner-Courier issues as reviewed and do not infer anything from their absence online.
'''
write(CAPTURE,capture)

append_once('evidence/source-register.md',MARKER,f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans plus retrieval-gap manifest; **38/38 online-exposed pages VISUALLY VERIFIED** 7 September 2026.  
Coverage: final Courier issue 3 Jul., 6 pages; Enterprise 4/11/18/25 Jul., 32 pages; Banner-Courier 17/24/31 Jul. **manual retrieval gaps** under `MF-030`.  
Repository originals: `newspapers/oregon-city-courier/1919-july/`, `newspapers/oregon-city-enterprise/1919-july/`; gap manifest `newspapers/banner-courier/1919-july/manifest.json`.  
Related evidence: `{E}`.  
Notes: No exact 501/503/505/505½ occupant or target physical-building event in the 38 online pages. Previously integrated July cleaner (`S-152`/`E-136`) and Gilbert Miller (`S-160`/`E-144`) pages were re-encountered but not duplicated. Theroux continues at 210 Seventh through 25 Jul.; Farr Brothers appears in market reports without address/proprietor.''')

append_once('evidence/evidence-register.md',MARKER,f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper online scan batch with explicit manual title gap.  
Sources: `{S}`; existing exact-page controls `S-152`, `S-160`.  
Claims:
- all **38/38 online-exposed July pages** were visually inspected after printed title/date/page identity review;
- *Oregon City Courier* ends in the institutional July sequence at 3 Jul.; 17/24/31 Jul. Banner-Courier remain manual gaps under `MF-030`;
- no source-explicit 501/503/505/505½ occupant or target construction/property event was established in the online pages;
- 18/25 Jul. cleaner pages visibly reconfirm existing `E-136` but are not duplicated;
- 11 Jul. Gilbert Miller page visibly reconfirms existing `E-144` but is not duplicated;
- 25 Jul. directly continues Theroux Music House at 210 Seventh Street;
- 11/18/25 Jul. market reports credit Farr Brothers without address or individual proprietor.
Confidence: **Very High** for scan-visible wording and online-page coverage; **RETRIEVAL GAP** for Banner-Courier 17/24/31 Jul.; none for an unprinted target occupant/event.''')

append_once('database/sources.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary July scan batch: 38/38 online-exposed pages visually verified. Final Courier 3 July\n      plus four Enterprise issues; Banner-Courier 17, 24 and 31 July remain MF-030 manual retrieval gaps.\n''')
append_once('database/evidence.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper online scan batch with explicit manual retrieval gap\n    claims:\n      - 38/38 online-exposed July 1919 pages visually verified.\n      - No source-explicit 501, 503, 505 or 505-half Main occupant or target physical-building event was established in those online pages.\n      - Banner-Courier issues of 17, 24 and 31 July remain manual microfilm retrieval gaps under MF-030.\n      - Existing cleaner/dyer E-136 and Gilbert Miller E-144 were reconfirmed but not duplicated.\n      - Theroux Music House continued at 210 Seventh Street through 25 July.\n      - Farr Brothers appeared in July market reports without address or individual proprietor.\n    confidence: Very High for visible online pages; retrieval gap for inaccessible Banner-Courier issues\n    related_sources: [{S}]\n    related_evidence: [E-136, E-144]\n    related_businesses: [BUS-104, BUS-029]\n    related_people: [P-044]\n    related_buildings: []\n    sources: [{S}]\n    notes: >-\n      July is not a complete local-newspaper month because the successor Banner-Courier is unavailable online.\n      No negative inference is made across the inaccessible issues.\n''')

append_once('businesses/farr-brothers-store.md',MARKER,f'''## July 1919 market-report continuation
{MARKER}

Visually reviewed Enterprise market reports on **11, 18 and 25 July 1919** (`{S}` / `{E}`) credit **Brady Mercantile Company and Farr Brothers**. They print no exact address or individual Farr proprietor and do not bridge this concern to Edwin/Alice Farr or Farr's Pool Hall at 505 Main.
''')
append_once('businesses/ff-theroux.md',MARKER,f'''## July 1919 — 210 Seventh Street continuation
{MARKER}

The visually verified **25 July Enterprise p7** classified (`{S}` / `{E}`) directly prints **Theroux Music House, 210 Seventh St.**, extending the direct business-address chronology through **25 July 1919** without proving the exact move date from 519 Main.
''')
append_once('people/profiles/ff-theroux.md',MARKER,f'''## July 1919 address continuation
{MARKER}

`{S}` / `{E}` directly continues Theroux Music House at **210 Seventh Street** through **25 July 1919**. This is a business-location control, not property ownership.
''')

append_once('evidence/source-captures/1919-1920-banner-courier-ocr-discovery.md',MARKER,f'''## July 1919 monthly visual-pass reconfirmation
{MARKER}

The July monthly scan workflow (`{S}` / `{E}`) corrected the issue calendar against institutional holdings: the final *Oregon City Courier* issue in the sequence is **3 July 1919**; the Courier/Banner merger occurred **8 July**; successor *Banner-Courier* holdings begin **17 July**. Direct PDF-route probes for **17, 24 and 31 July 1919** again returned no exposed online issue pages. Those dates remain **RETRIEVAL GAPS / `MF-030`**, not negative evidence. The 3 July Courier and all four July Enterprise issues were preserved and visually reviewed separately.
''')
append_once('evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md',MARKER,f'''## July 1919 online-exposed visual addition
{MARKER}

The July online scan pass (`{S}` / `{E}`) visually reviewed **38/38 exposed pages** — final Courier 3 Jul. plus Enterprise 4/11/18/25 Jul. — and found no source-explicit construction, demolition, rebuilding, remodeling, lease, sale, move or fire event assignable to **501, 503, 505 or 505½ Main**. This does **not** cover the inaccessible 17/24/31 Jul. Banner-Courier issues, which remain `MF-030`; no physical-work absence may be inferred across that gap.
''')

append_once('registers/business-timeline.md',MARKER,f'''| 11/18/25 Jul. 1919 | address not printed | Farr Brothers market-report provider | `BUS-104` | `{E}` | Brady Mercantile + Farr Brothers credit; no individual proprietor/address bridge to 505. |
| 25 Jul. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | Direct classified continues the Seventh Street address. |
{MARKER}''')
append_once('indexes/id-crosswalk.md',MARKER,f'''## {S} / {E} — July 1919 online-exposed monthly visual batch
{MARKER}

- `{S}` / `{E}` → **38/38 online-exposed July pages** visually verified; Banner-Courier 17/24/31 Jul. remain `MF-030` retrieval gaps.
- `{S}` / `{E}` → `BUS-029` / `P-044` Theroux Music House at 210 Seventh through 25 Jul.
- `{S}` / `{E}` → `BUS-104` Farr Brothers July market-report continuation without address/proprietor.
- `S-152` / `E-136` → 18/25 Jul. cleaner/dyer repeat re-encountered, not duplicated.
- `S-160` / `E-144` → 11 Jul. Gilbert Miller item re-encountered, not duplicated.
- No target building, ownership or Wolf relation created from bounded July online coverage.
''')
append_once('registers/research-log.md',MARKER,f'''| 2026-09-07 | Completed July 1919 **online-exposed** Enterprise + final Courier scan-first visual audit | **38/38 online pages**: final Courier 3 Jul. 6/6 + Enterprise 4/11/18/25 Jul. 32/32. Corrected the title calendar: no 10 Jul. Courier issue is expected in institutional holdings; Banner-Courier begins 17 Jul. and 17/24/31 Jul. remain `MF-030` manual gaps. Cumulative Jan–Jul online visual coverage **404 pages**. No exact 501/503/505/505½ occupant or target construction/property event in the online pages. Existing cleaner `S-152`/`E-136` and Gilbert Miller `S-160`/`E-144` pages re-encountered without duplicate promotion. Theroux at 210 Seventh through 25 Jul.; Farr Brothers market credits without address/proprietor. Created `{S}` / `{E}`. |
{MARKER}''')
append_once('ARCHIVE_INDEX.md',MARKER,f'''## 1919 July online-exposed visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- July online coverage: **38/38 exposed pages visually verified** (`{S}` / `{E}`); Jan–Jul online cumulative **404 pages**.
- Final Courier issue in holdings: 3 Jul.; successor Banner-Courier begins 17 Jul. after the 8 Jul. merger.
- Banner-Courier 17/24/31 Jul. remain **manual retrieval gaps (`MF-030`)** and are not included in visual totals.
- No source-explicit 501/503/505/505½ occupant or target construction/property event in the online pages; bounded coverage only.
- Existing cleaner `E-136` and Gilbert Miller `E-144` July pages were re-encountered, not duplicated.
- Theroux remains at 210 Seventh through 25 Jul.; Farr Brothers appears in market reports without address/proprietor.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next online chronological batch: **August 1919 Enterprise**; Banner-Courier remains `MF-030`.
''')

ys=read('registers/year-status.md'); lines=ys.splitlines(); found=False
for i,line in enumerate(lines):
    if line.startswith('| 1919 |'):
        lines[i]=(f"| 1919 | **IN PROGRESS** | `{CAPTURE}`; `evidence/source-captures/1919-june-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-may-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-april-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-march-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; `evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | January–July **404 online-exposed pages visually verified**: Jan 70 + Feb 56 + Mar 56 + Apr 56 + May 72 + Jun 56 + Jul 38 (`{S}`/`{E}` for July). July comprises final Courier 3 Jul. plus Enterprise 4/11/18/25 Jul.; Banner-Courier 17/24/31 Jul. is unavailable online and remains `MF-030`, so July is not a fully source-complete month. No exact 501/503/505/505½ occupant or target construction event in July online pages. Existing cleaner `E-136` and Gilbert Miller `E-144` pages were re-encountered without duplicate promotion; Theroux and Farr business controls continue. August–December Enterprise visual work and other online source classes remain; Banner-Courier 17 Jul. 1919–31 Dec. 1920 is a documented manual microfilm gap. |")
        found=True; break
if not found: raise RuntimeError('1919 year-status row not found')
write('registers/year-status.md','\n'.join(lines)+'\n')

for entity in ['BUS-104','BUS-029']:
    update_yaml_relation('database/businesses.yml',entity,'related_evidence',E); update_yaml_relation('database/businesses.yml',entity,'related_sources',S)
update_yaml_relation('database/people.yml','P-044','related_evidence',E); update_yaml_relation('database/people.yml','P-044','related_sources',S)

print(f'Integrated July 1919 online batch as {S} / {E}')
