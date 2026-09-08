#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 March Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 March Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-march-enterprise-courier-visual-review-2026-09-07.md"

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,t): Path(p).write_text(t, encoding='utf-8')
def append_once(path, marker, block):
    p=Path(path); t=p.read_text(encoding='utf-8')
    if marker in t: return False
    if not t.endswith('\n'): t+='\n'
    t += '\n' + block.strip() + '\n'
    p.write_text(t,encoding='utf-8'); return True

def next_id(path,prefix):
    nums=[int(x) for x in re.findall(rf'\b{re.escape(prefix)}-(\d+)\b',read(path))]
    if not nums: raise RuntimeError(f'No {prefix} ids in {path}')
    return f'{prefix}-{max(nums)+1:03d}'

def update_yaml_relation(path, entity_id, field, value):
    p=Path(path); t=p.read_text(encoding='utf-8')
    m=re.search(rf'(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)',t)
    if not m: return False
    block=m.group(0)
    fm=re.search(rf'(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$',block)
    if fm:
        vals=[v.strip() for v in fm.group(1).split(',') if v.strip()]
        if value in vals: return False
        vals.append(value)
        new=f'    {field}: [' + ', '.join(vals) + ']'
        block=block[:fm.start()] + new + block[fm.end():]
    else:
        fm=re.search(rf'(?m)^    {re.escape(field)}:\s*$\n((?:      - .*\n)*)',block)
        if fm:
            vals=[x.strip() for x in re.findall(r'(?m)^      -\s*(.+?)\s*$',fm.group(1))]
            if value in vals: return False
            replacement=f'    {field}:\n' + fm.group(1) + f'      - {value}\n'
            block=block[:fm.start()] + replacement + block[fm.end():]
        else:
            if not block.endswith('\n'): block += '\n'
            block += f'    {field}: [{value}]\n'
    t=t[:m.start()] + block + t[m.end():]
    p.write_text(t,encoding='utf-8')
    return True

if Path(CAPTURE).exists():
    print('March capture already exists; refusing duplicate integration.')
    sys.exit(0)

S=next_id('evidence/source-register.md','S')
E=next_id('evidence/evidence-register.md','E')
T=next_id('database/timeline.yml','T')

capture=f'''# March 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 56/56 recovered March pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. January–March cumulative local-newspaper visual coverage: **182 pages**.

Archive IDs: source `{S}`; evidence `{E}`; timeline `{T}`.

## Scope

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Courier* | 6, 13, 20, 27 Mar. 1919 | **24/24** |
| *Oregon City Enterprise* | 7, 14, 21, 28 Mar. 1919 | **32/32** |
| **March total** | **8 issues** | **56/56** |

Preserved originals:
- `newspapers/oregon-city-courier/1919-march/`
- `newspapers/oregon-city-enterprise/1919-march/`

Retrieval commit: `a1cc936` (`Archive March 1919 Oregon City newspaper scans`).

Every recovered page was visually checked for printed issue date and page number before OCR/text discovery. Courier issues visibly contain pages 1–6 and Enterprise issues pages 1–8. No substituted-page, duplicate-page, or printed-date defect was found in the March set.

## Major finding — Cox billiard license transferred to F. D. Rohberger

### 6 March Courier p1 — direct license-transfer wording

The original scan directly states:

> **The billiard license of F. D. Cox was transferred to F. D. Rohberger, the new owner of the parlors.**

This is **DOCUMENTED / DIRECT** evidence that the municipal billiard license previously held by F. D. Cox was transferred to a person printed as **F. D. Rohberger**, whom the paper calls **the new owner of the parlors**. No premises address is printed.

This is the first direct municipal-action follow-through after February's sale reports.

### Contemporary buyer-name conflict: Rohrberg vs. Rohberger

The February sale reports visibly call the buyer **Mr. Rohrberg of Ocean Falls, B.C.** The 6 March Courier council report visibly prints **F. D. Rohberger**. The chronology and transaction context strongly suggest that these references may describe the same purchaser, but the spelling and initials are not identical.

Classification: **UNRESOLVED CONTEMPORARY NAME-FORM CONFLICT / STRONG TRANSACTION CONTINUITY INFERENCE**. Preserve both printed forms. Do not silently normalize one to the other and do not create a person identity record until an independent identifier reconciles the names.

### 7 March Enterprise p3 — damaged-edge corroboration only

The Enterprise council summary visibly begins **“The billiard parlor license of F. D.”** and ends **“…er by the council.”** The intervening right-edge text is lost/cropped in the surviving scan. It is consistent with a license-transfer report but does not preserve a complete name or sentence. The complete 6 March Courier wording controls the direct claim.

### Address limitation

Neither the 6 March Courier nor the surviving readable portion of the 7 March Enterprise prints the billiard-parlor address. The direct 1915 Cox hall location on Main between Seventh and Eighth cannot be projected into 1919. The March transfer must not be assigned to 501, 503, or 505 Main without an independent premises bridge.

## Ohio Dentists continuation — 507½ Main over Harding's Drug Store

Visually verified Enterprise advertisements on **14 March p3** and **21 March p3** directly repeat:

- **Ohio Dentists**;
- **Dr. J. G. Nash, Manager**;
- **507½ Main Street**;
- **over Harding's Drug Store**;
- **Phone 62**.

This extends the direct office-location run through **21 March 1919**. The ads still do not print `Harding Drug Store, 507 Main`; Harding's exact lower-floor 507 assignment remains a **STRONG SPATIAL/ADDRESS INFERENCE**, not direct exact-number evidence.

## Farr Brothers market-report continuation

The **7 March p7**, **21 March p2**, and **28 March p6** Enterprise market reports visibly credit **Brady Mercantile Company and Farr Brothers**. These are dated local-business appearances only. They print no exact address or individual Farr proprietor and do not bridge to Edwin/Alice Farr, Farr's Pool Hall at 505, Carl Harr, or Harr's Recreation Center.

## Theroux Music House — 210 Seventh Street continuation

The **28 March Enterprise p3** visibly prints a Theroux Music House advertisement with **210 Seventh Street**. This extends the direct 1919 Seventh Street business-address control. It does not establish the exact date Theroux left the earlier 519 Main premises.

## Target frontage — 501 / 503 / 505 Main

Across all 56 visually reviewed pages and the post-visual text-discovery pass:

- no defensible source-explicit **501 Main** occupant was found;
- no defensible source-explicit **503 Main** occupant was found;
- no defensible source-explicit **505 Main** occupant was found;
- no March Wolf & Miller exact-address continuation was found;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move, or fire event was found.

Numeric collisions, legal descriptions, monetary figures, and unrelated Main Street numbers were rejected as non-target context.

**This is bounded March coverage only. It is not evidence of vacancy, non-use, closure, demolition, or absence of an occupant.**

## Cross-Record Propagation Audit

Propagated: source/evidence registers and YAML; Cox pool-hall lead; Ohio Dentists/Nash; Harding/507½ spatial chronology; Theroux; Farr Brothers; master/business/address timelines; database timeline; open questions/research leads; crosswalk; year status; archive index; and research log.

No 501/503/505 building event is created because March supplies no direct target-premises event.

## Next chronological step

Continue with **April 1919 Enterprise + Courier** under the same scan-first standard. High-value follow-forward targets remain the **Rohberger / Rohrberg buyer identity and billiard-parlor premises**, plus any exact 501/503/505 occupant or construction/property transition.
'''
write(CAPTURE,capture)

append_once('evidence/source-register.md',MARKER,f'''## {S} — March 1919 Oregon City Enterprise + Courier complete monthly visual-review batch
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: Courier 6/13/20/27 Mar., 24 pages; Enterprise 7/14/21/28 Mar., 32 pages; **56/56 total**.  
Repository originals: `newspapers/oregon-city-courier/1919-march/` and `newspapers/oregon-city-enterprise/1919-march/`.  
Related evidence: `{E}`.  
Notes: 6 Mar Courier directly transfers F. D. Cox's billiard license to **F. D. Rohberger, the new owner of the parlors**; February sale reports instead print **Mr. Rohrberg**, so the name form remains unresolved. Ohio Dentists continues at 507½-over-Harding through 21 Mar.; Farr Brothers market-report credits and Theroux at 210 Seventh continue. No source-explicit 501/503/505 occupant or target construction event; bounded coverage only.''')

append_once('evidence/evidence-register.md',MARKER,f'''## {E} — March 1919 visual review: Cox→Rohberger license transfer and neighboring business controls
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **56/56** recovered March pages were visually inspected after printed date/page identity review;
- 6 Mar Courier p1 directly says **F. D. Cox's billiard license was transferred to F. D. Rohberger, the new owner of the parlors**; no premises address is printed;
- February's buyer form **Mr. Rohrberg** and March's **F. D. Rohberger** are preserved as an unresolved contemporary name-form conflict; transaction continuity is strongly suggested but identity is not silently normalized;
- 14/21 Mar Enterprise ads repeat **Ohio Dentists / Dr. J. G. Nash at 507½ Main over Harding's Drug Store**;
- 7/21/28 Mar market reports credit **Brady Mercantile Company and Farr Brothers** without address or proprietor;
- 28 Mar Enterprise p3 directly prints **Theroux Music House, 210 Seventh Street**;
- no source-explicit 501/503/505 occupant or target physical-building event was found; no-hit is coverage only.
Confidence: **Very High** for scan-visible wording and monthly page coverage; **Unresolved conflict** for buyer surname/initial form; none for an unprinted billiard premises number.''')

append_once('database/sources.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {S}\n    name: "March 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary scan batch, visually verified 56/56 pages: 24 Courier and 32 Enterprise.\n      Direct findings include transfer of F. D. Cox's billiard license to F. D. Rohberger,\n      called the new owner of the parlors; February printed the buyer as Mr. Rohrberg, so\n      the name form remains unresolved. Ohio Dentists continued at 507½ Main over Harding's\n      Drug Store; Farr Brothers market-report credits and Theroux at 210 Seventh continued.\n      No source-explicit 501/503/505 occupant was found.\n''')
append_once('database/evidence.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {E}\n    name: "March 1919 visual review: Cox to Rohberger license transfer and neighboring controls"\n    type: Primary newspaper scan batch\n    claims:\n      - 56/56 recovered March 1919 pages visually verified.\n      - F. D. Cox's billiard license was transferred to F. D. Rohberger, called the new owner of the parlors; address not printed.\n      - February Mr. Rohrberg versus March F. D. Rohberger is an unresolved contemporary name-form conflict.\n      - Ohio Dentists continued at 507½ Main over Harding's Drug Store through 21 March; Theroux Music House was directly at 210 Seventh Street on 28 March.\n      - Farr Brothers appeared in 7, 21 and 28 March market-report credits without address or individual proprietor.\n    confidence: Very High for scan-visible wording and page coverage; unresolved for buyer name normalization; none for unprinted billiard premises number\n    related_sources: [{S}]\n    related_evidence: []\n    related_businesses: [BUS-106, BUS-029, BUS-104]\n    related_people: [P-397]\n    related_buildings: [B-003]\n    sources: [{S}]\n    notes: >-\n      March monthly scan-first review. Cox/Rohberger premises must not be assigned to 501,\n      503 or 505 Main; the 1915 Cox location cannot be projected into 1919. The damaged right\n      edge of the 7 March Enterprise council report supplies only incomplete corroboration.\n''')

append_once('evidence/source-captures/1915-1916-cox-pool-hall-lead.md',MARKER,f'''## March 1919 continuation — license transfer to F. D. Rohberger
{MARKER}

`{E}` / `{S}` provides the direct municipal-action follow-through to the February sale. The **6 Mar. 1919 Courier p1** visibly states: **“The billiard license of F. D. Cox was transferred to F. D. Rohberger, the new owner of the parlors.”** No premises address is printed.

This creates a contemporary name-form problem that must remain visible. The February sale stories visibly print **Mr. Rohrberg of Ocean Falls, B.C.**; the March council report visibly prints **F. D. Rohberger**. The sale→license-transfer chronology strongly suggests transaction continuity, but spelling/initial identity is not independently reconciled. Do not silently normalize the names or create an exact premises assignment.

The **7 Mar. Enterprise p3** council summary has a damaged/cropped right edge; it visibly begins `The billiard parlor license of F. D.` and ends `...er by the council`, but the missing edge prevents a complete name/sentence transcription. Use the complete Courier report for the direct transfer claim.

No March source places the parlors at 501/503/505 or proves that the 1919 room was the same as Cox's 1915 Main-between-Seventh/Eighth hall.''')

append_once('businesses/ohio-painless-dentists.md',MARKER,f'''## March 1919 continuation
{MARKER}

Visually verified **14 Mar. p3** and **21 Mar. p3 Enterprise** advertisements (`{E}` / `{S}`) repeat **Ohio Dentists**, **Dr. J. G. Nash, Manager**, **507½ Main Street**, **over Harding's Drug Store**, Phone 62. This extends the direct office-location run through **21 March 1919**. Harding's exact lower-floor number remains unprinted and therefore inferential.''')
append_once('people/profiles/j-g-nash.md',MARKER,f'''## March 1919 continuation
{MARKER}

`{E}` / `{S}` visually verifies Dr. J. G. Nash again as manager of Ohio Dentists at **507½ Main over Harding's Drug Store** on **14 and 21 March 1919**, extending his direct advertised role through 21 March.''')
append_once('buildings/507-harding-building.md',MARKER,f'''## March 1919 507½-over-Harding continuation
{MARKER}

`{E}` / `{S}` directly repeats Ohio Dentists at **507½ Main over Harding's Drug Store** on 14 and 21 March 1919. This extends the documented upstairs spatial relationship through **21 March** but still does not print Harding's lower-floor exact number, ownership, lease terms, construction date, or physical-building continuity.''')
append_once('businesses/ff-theroux.md',MARKER,f'''## March 1919 — 210 Seventh Street continuation
{MARKER}

The **28 Mar. 1919 Enterprise p3** scan (`{E}` / `{S}`) directly prints **Theroux Music House — 210 Seventh Street**. This extends the 1919 Seventh Street address control without establishing the exact departure date from 519 Main.''')
append_once('people/profiles/ff-theroux.md',MARKER,f'''## March 1919 address continuation
{MARKER}

`{E}` / `{S}` directly places Theroux Music House at **210 Seventh Street** again on **28 March 1919**. This is a dated business-address control, not a property-ownership or exact move-date claim.''')
append_once('businesses/farr-brothers-store.md',MARKER,f'''## March 1919 continuation
{MARKER}

The visually verified **7 Mar. p7**, **21 Mar. p2**, and **28 Mar. p6 Enterprise** market reports (`{E}` / `{S}`) credit **Brady Mercantile Company and Farr Brothers**. These are dated business appearances only: no address or individual proprietor is printed. Do not merge this grocery/meat concern with Edwin/Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr, or Harr's Recreation Center.''')

append_once('timeline.md',MARKER,f'''## March 1919 — Cox billiard license transfer; complete monthly visual batch
{MARKER}

A scan-first review of **56/56 March pages** (`{S}` / `{E}`) directly records the **6 March transfer of F. D. Cox's billiard license to F. D. Rohberger, “the new owner of the parlors.”** February's sale reports instead print the buyer as **Mr. Rohrberg of Ocean Falls, B.C.**; preserve this as an unresolved contemporary name-form conflict rather than silently normalizing it. No address is printed for the parlors. Ohio Dentists / Dr. J. G. Nash continue at **507½ Main over Harding's Drug Store through 21 March**; Farr Brothers market-report credits appear on 7/21/28 March; Theroux Music House is directly at **210 Seventh Street** on 28 March. No exact 501/503/505 occupant or target construction/property event was recovered; that is bounded coverage only.''')

append_once('registers/business-timeline.md',MARKER,f'''## March 1919 verified business controls
{MARKER}

| Date | Business / person | Location / transaction | Evidence / limit |
| --- | --- | --- | --- |
| 6 Mar. 1919 | F. D. Cox → **F. D. Rohberger** | Billiard license transferred; Rohberger called new owner of parlors | `{E}` / `{S}`; **no premises address**. February buyer printed `Mr. Rohrberg`; name form unresolved. |
| 14 & 21 Mar. 1919 | Ohio Dentists / Dr. J. G. Nash | **507½ Main over Harding's Drug Store** | Direct; Harding lower-floor exact number remains inferential. |
| 7, 21 & 28 Mar. 1919 | Farr Brothers + Brady Mercantile | Market-report provider credit | Direct business appearance only; no address/proprietor; no 505 merge. |
| 28 Mar. 1919 | Theroux Music House | **210 Seventh Street** | Direct address continuation; exact move date from 519 unresolved. |''')

append_once('registers/address-register.md',MARKER,f'''## March 1919 address controls
{MARKER}

| Address | Date | Directly documented use | Evidence / limit |
| --- | --- | --- | --- |
| **507½ Main** | 14 & 21 Mar. 1919 | Ohio Dentists; Dr. J. G. Nash manager | `{E}` / `{S}`; direct `over Harding's Drug Store` wording; Harding lower exact number not printed. |
| **210 Seventh Street** | 28 Mar. 1919 | Theroux Music House | `{E}` / `{S}`; direct business-address continuation. |''')

append_once('evidence/open-questions.md',MARKER,f'''## March 1919 Cox buyer-name / premises refinement
{MARKER}

`{E}` / `{S}` directly establishes the 6 March **F. D. Cox → F. D. Rohberger billiard-license transfer**, with Rohberger called the new owner of the parlors. February's sale reports instead print **Mr. Rohrberg of Ocean Falls, B.C.** Treat the identity/name form as unresolved until an independent directory, license application/bond, census, business advertisement, or other identifier reconciles the forms.

The parlors' 1919 address remains unresolved. Do not project Cox's 1915 Main-between-Seventh/Eighth location forward, and do not assign the transfer to 501/503/505 without direct premises evidence. March's complete 56-page target no-hit does not answer the occupancy/construction question.''')

append_once('evidence/research-leads.md',MARKER,f'''## 7 September 2026 — March 1919 Rohberger / Rohrberg follow-forward
{MARKER}

`{E}` / `{S}` advances the February Cox-sale lead: the **6 Mar. Courier p1** directly prints **F. D. Rohberger** as transferee of Cox's billiard license and **new owner of the parlors**. Search forward under both **Rohberger** and **Rohrberg**, including initials F. D. and any later first-name/initial variants, for an exact premises address, annual license/application/bond, advertisement, directory entry, residence, or sale. Preserve the February `Mr. Rohrberg of Ocean Falls, B.C.` spelling as a competing contemporary form until independently reconciled.

Continue exact-address searches for 501/503/505 and target construction/property language. March no-hit remains bounded coverage only.''')

append_once('indexes/id-crosswalk.md',MARKER,f'''## {S} / {E} / {T} — March 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` / `{T}` → Cox billiard research: **F. D. Cox license transferred to F. D. Rohberger**, called new owner of the parlors; premises number unresolved; February `Mr. Rohrberg` form remains a name conflict.
- `{S}` / `{E}` → `BUS-106` / `P-397` / `B-003`: Ohio Dentists / J. G. Nash continue at **507½ Main over Harding's Drug Store** through 21 Mar.; Harding lower exact number remains inference.
- `{S}` / `{E}` → `BUS-104`: Farr Brothers market-report credits on 7/21/28 Mar., no address/proprietor and no Farr-pool-hall merge.
- `{S}` / `{E}` → `BUS-029` / `P-044`: Theroux Music House directly at **210 Seventh Street** on 28 Mar.
- No 501/503/505 building event is created from the March no-hit.''')

append_once('registers/research-log.md',MARKER,f'''| 2026-09-07 | Completed March 1919 Enterprise + Courier scan-first visual audit | **56/56 pages**: Courier 24/24 (6/13/20/27 Mar.) + Enterprise 32/32 (7/14/21/28 Mar.), bringing Jan–Mar cumulative local-newspaper visual coverage to **182 pages**. Directly verified F. D. Cox's billiard-license transfer to **F. D. Rohberger, new owner of the parlors**; preserved February `Mr. Rohrberg` vs March `F. D. Rohberger` as an unresolved contemporary name-form conflict. Ohio Dentists/Nash continue at 507½-over-Harding through 21 Mar.; Farr Brothers and Theroux controls extended. No exact 501/503/505 occupant or target construction event; bounded coverage only. Created `{S}` / `{E}` / `{T}`. 1919 remains IN PROGRESS; next chronological batch April. |
{MARKER}''')

append_once('ARCHIVE_INDEX.md',MARKER,f'''## 1919 March complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- March local-newspaper coverage: **56/56 visually verified pages** (`{S}` / `{E}`); Jan–Mar cumulative **182 pages**.
- Cox billiard license transferred on 6 Mar. to **F. D. Rohberger**, called new owner of the parlors; no address printed. February `Mr. Rohrberg` versus March `F. D. Rohberger` remains an unresolved contemporary name-form conflict.
- Ohio Dentists at 507½-over-Harding through 21 Mar.; Farr Brothers market-report continuation; Theroux at 210 Seventh on 28 Mar.
- No source-explicit 501/503/505 occupant or target construction/property event; bounded coverage only.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological batch: **April 1919 Enterprise + Courier**.''')

timeline_yml = read('database/timeline.yml')
if not re.search(rf'(?m)^  - id: {re.escape(T)}\s*$', timeline_yml):
    timeline_yml = timeline_yml.rstrip() + f'''\n\n  - id: {T}\n    date: 6 March 1919\n    summary: Oregon City Courier reports that F. D. Cox's billiard license was transferred to F. D. Rohberger, called the new owner of the parlors; February sale reports printed the buyer as Mr. Rohrberg of Ocean Falls, B.C.\n    confidence: Very High for the visible license-transfer wording; unresolved for buyer name normalization and premises address\n    related_evidence:\n      - {E}\n    related_sources:\n      - {S}\n''' + '\n'
    write('database/timeline.yml', timeline_yml)

for entity in ['BUS-106','BUS-029','BUS-104']:
    update_yaml_relation('database/businesses.yml', entity, 'related_evidence', E)
    update_yaml_relation('database/businesses.yml', entity, 'related_sources', S)
for entity in ['P-397','P-044']:
    update_yaml_relation('database/people.yml', entity, 'related_evidence', E)
    update_yaml_relation('database/people.yml', entity, 'related_sources', S)
update_yaml_relation('database/buildings.yml', 'B-003', 'related_evidence', E)
update_yaml_relation('database/buildings.yml', 'B-003', 'related_sources', S)

ys=read('registers/year-status.md'); lines=ys.splitlines(); found=False
for i,line in enumerate(lines):
    if line.startswith('| 1919 |'):
        lines[i]=(f'| 1919 | **IN PROGRESS** | `{CAPTURE}`; `evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md`; '
                  '`evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; '
                  '`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | '
                  f'January–March scan-first local-newspaper coverage **182 visually verified pages**: January 70 + February 56 + March 56 (`{S}`/`{E}` for March). '
                  'March directly records the F. D. Cox billiard-license transfer to F. D. Rohberger, called new owner of the parlors, while preserving February `Mr. Rohrberg` as an unresolved name-form conflict; no premises number. '
                  'Ohio Dentists at 507½-over-Harding extends through 21 Mar.; Farr Brothers and Theroux controls continue; no exact 501/503/505 occupant or target construction event. '
                  'April–December annual visual work and other online source classes remain; Banner-Courier from July 1919 has a documented manual microfilm gap. |')
        found=True; break
if not found: raise RuntimeError('1919 year-status row not found')
write('registers/year-status.md','\n'.join(lines)+'\n')

print(f'Integrated March 1919 as {S} / {E} / {T}')
