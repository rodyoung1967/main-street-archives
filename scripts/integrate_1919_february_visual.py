#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 February Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 February Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md"

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
    if not nums: raise RuntimeError(f'No {prefix} ids')
    return f'{prefix}-{max(nums)+1:03d}'

def add_inline_list_value(path, entity_id, field, value):
    p=Path(path); t=p.read_text(encoding='utf-8')
    m=re.search(rf'(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)',t)
    if not m: return False
    block=m.group(0)
    fm=re.search(rf'(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$',block)
    if not fm: return False
    vals=[v.strip() for v in fm.group(1).split(',') if v.strip()]
    if value in vals: return False
    vals.append(value)
    newfield=f'    {field}: [' + ', '.join(vals) + ']'
    newblock=block[:fm.start()] + newfield + block[fm.end():]
    t=t[:m.start()] + newblock + t[m.end():]
    p.write_text(t,encoding='utf-8'); return True

if Path(CAPTURE).exists():
    print('February capture already exists; refusing duplicate integration.')
    sys.exit(0)

S=next_id('evidence/source-register.md','S')
E=next_id('evidence/evidence-register.md','E')

capture=f'''# February 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 56/56 recovered February pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. January + February cumulative local-newspaper visual coverage: **126 pages**.

Archive IDs: source `{S}`; evidence `{E}`.

## Scope

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Courier* | 6, 13, 20, 27 Feb. 1919 | **24/24** |
| *Oregon City Enterprise* | 7, 14, 21, 28 Feb. 1919 | **32/32** |
| **February total** | **8 issues** | **56/56** |

Preserved originals:
- `newspapers/oregon-city-courier/1919-february/`
- `newspapers/oregon-city-enterprise/1919-february/`

Retrieval commit: `875e78ba84cee92956aa6995c15417e508f16436`.

Every recovered page was visually checked for printed issue date and page number before OCR/text discovery. Courier issues contain pages 1–6; Enterprise issues pages 1–8. No substituted-page, duplicate-page, or printed-date defect was found in the February set.

## Major finding — F. D. Cox billiard-parlor sale

### 6 February Courier p1 — annual license

The council report directly says **F. D. Cox was granted a billiard hall license for the year**. No premises address is printed.

### 13 February Courier p1 — sale

A story headed **COX BILLIARD PARLORS ARE SOLD TO B. C. MAN** directly says the billiard parlors belonging to **F. D. Cox** had been purchased by **Mr. Rohrberg, of Ocean Falls, B.C.**, who had recently moved to Oregon City. It says Rohrberg had been employed by the Pacific Mills at Ocean Falls and that **Cox would take active charge of his soda works in Oregon City**.

The scan clearly reads **Rohrberg**. OCR variants such as `Rohiberg` are rejected.

### 14 February Enterprise p5 — independent sale/handover confirmation

Under **BUSINESS CHANGE**, the Enterprise independently reports that **Mr. Rohrberg of Ocean Falls, B.C., has purchased the billiard parlors of F. D. Cox and will assume charge Wednesday morning**. Because the issue is Friday 14 February, that wording dates the intended handover to **Wednesday, 12 February 1919**. The item again says Cox would devote his time to his soda works.

### Address limitation

These February records prove a 1919 Cox billiard operation, annual license, sale, buyer surname/origin, and intended handover date. **They do not print the billiard-parlor street address.**

The 1915 raid-period Cox hall is directly documented **on Main between Seventh and Eighth**, which excludes 503 for that 1915 episode. The February 1919 sale must **not** be projected backward or forward onto that same room without a premises bridge. It likewise must not be assigned to 501, 503, or 505 Main.

## Ohio Dentists continuation — 507½ Main over Harding's Drug Store

Visually verified Enterprise ads on **14 February p2** and **28 February p7** repeat:

- **Ohio Dentists**;
- **Dr. J. G. Nash, Manager**;
- **507½ Main Street**;
- **over Harding's Drug Store**;
- **Phone 62**.

This extends the January direct office-location run through **28 February 1919**. The ads still do **not** print `Harding Drug Store, 507 Main`; the exact lower-floor 507 assignment remains a **strong spatial/address inference**, not direct exact-number evidence.

A separate recurring Courier ad for **New System Painless Dentists** gives **Rooms 9-10-11-12, Andresen Building**. It is not merged with Ohio Dentists merely because both advertise painless dentistry.

## Theroux Music House — 210 Seventh Street

Enterprise advertisements on **7 February p3**, **14 February p3**, and **21 February p2** directly print **Theroux Music House, 210 Seventh Street** (7 Feb adds `near Elevator`). This is a direct 1919 business-address control. It does not establish the exact date Theroux left the earlier 519 Main premises; separate evidence already places another occupant at 519 by October 1918.

## Farr Brothers market-report continuation

The **21 February p3** and **28 February p7** Enterprise market reports visibly say they are given/furnished by **Brady Mercantile Company and Farr Brothers**. These are dated local-business appearances only. They print no address or individual Farr proprietor and are **not** evidence for Edwin/Alice Farr, Farr's Pool Hall at 505, or a Farr→Harr transition.

## Target frontage — 501 / 503 / 505 Main

Across all 56 visually reviewed pages and the post-visual text-discovery pass:

- no defensible source-explicit **501 Main** occupant was found;
- no defensible source-explicit **503 Main** occupant was found;
- no defensible source-explicit **505 Main** occupant was found;
- no February Wolf & Miller exact-address continuation was found;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move, or fire event was found.

Numeric collisions in legal notices, monetary figures, and non-target addresses were rejected as context rather than target addresses.

**This is bounded February coverage only. It is not evidence of vacancy, non-use, closure, demolition, or absence of an occupant.**

## Cross-Record Propagation Audit

Propagated: source/evidence registers and YAML, Cox pool-hall lead, Ohio Dentists/Nash, Theroux, Farr Brothers, master/business/address timelines, open questions/leads, crosswalk, year status, archive index, and research log.

No 501/503/505 building event is created because February supplies no direct target-premises event.

## Next chronological step

Continue with **March 1919 Enterprise + Courier** under the same scan-first standard. High-value follow-forward target: **Mr. Rohrberg / Cox billiard parlors** for an exact premises address or later license/business name.
'''
write(CAPTURE,capture)

append_once('evidence/source-register.md',MARKER,f'''## {S} — February 1919 Oregon City Enterprise + Courier complete monthly visual-review batch
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: Courier 6/13/20/27 Feb., 24 pages; Enterprise 7/14/21/28 Feb., 32 pages; **56/56 total**.  
Repository originals: `newspapers/oregon-city-courier/1919-february/` and `newspapers/oregon-city-enterprise/1919-february/`.  
Related evidence: `{E}`.  
Notes: F. D. Cox annual billiard-hall license and Feb. 12 sale/handover to Mr. Rohrberg; Ohio Dentists 507½-over-Harding continuation; Theroux Music House 210 Seventh; Farr Brothers market-report credits. No source-explicit 501/503/505 occupant or target construction event; bounded coverage only.''')

append_once('evidence/evidence-register.md',MARKER,f'''## {E} — February 1919 visual review: Cox billiard sale and neighboring business controls
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **56/56** recovered February pages were visually inspected after printed date/page identity review;
- 6 Feb Courier p1 says **F. D. Cox was granted a billiard hall license for the year**;
- 13 Feb Courier p1 says Cox's billiard parlors were purchased by **Mr. Rohrberg of Ocean Falls, B.C.**;
- 14 Feb Enterprise p5 independently says Rohrberg purchased the parlors and would **assume charge Wednesday morning**, dating the intended handover to **12 Feb. 1919**; no premises address is printed;
- 14 and 28 Feb Enterprise ads repeat **Ohio Dentists / Dr. J. G. Nash at 507½ Main over Harding's Drug Store**;
- 7/14/21 Feb Enterprise ads directly place **Theroux Music House at 210 Seventh Street**;
- 21/28 Feb market reports credit **Brady Mercantile Company and Farr Brothers** without address or proprietor;
- no source-explicit 501/503/505 occupant or target physical-building event was found; no-hit is coverage only.
Confidence: **Very High** for scan-visible wording and monthly page coverage; none for a Cox/ Rohrberg premises number not printed by the sources.''')

append_once('database/sources.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {S}\n    name: "February 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary scan batch, visually verified 56/56 pages: 24 Courier and 32 Enterprise.\n      Direct findings include the F. D. Cox billiard-hall license and sale to Mr. Rohrberg,\n      Ohio Dentists at 507½ Main over Harding's Drug Store, Theroux at 210 Seventh, and\n      Farr Brothers market-report credits. No source-explicit 501/503/505 occupant was found.\n''')
append_once('database/evidence.yml',YAML_MARKER,YAML_MARKER+f'''\n  - id: {E}\n    name: "February 1919 visual review: Cox billiard sale and neighboring business controls"\n    type: Primary newspaper scan batch\n    claims:\n      - 56/56 recovered February 1919 pages visually verified.\n      - F. D. Cox received a 1919 billiard-hall license and sold his billiard parlors to Mr. Rohrberg, with intended handover 12 February; address not printed.\n      - Ohio Dentists continued at 507½ Main over Harding's Drug Store; Theroux Music House was directly at 210 Seventh Street.\n    confidence: Very High for scan-visible wording and page coverage; none for an unprinted Cox/Rohrberg premises number\n    related_sources: [{S}]\n    sources: [{S}]\n    notes: >-\n      February monthly scan-first review. Cox/Rohrberg premises must not be assigned to 501,\n      503 or 505 Main; the 1915 Cox location between Seventh and Eighth cannot be projected\n      into 1919 without an independent bridge. No target construction event was recovered.\n''')

append_once('evidence/source-captures/1915-1916-cox-pool-hall-lead.md',MARKER,f'''## February 1919 continuation — Cox licenses, then sells billiard parlors
{MARKER}

`{E}` / `{S}` adds a major later Cox control. The **6 Feb. 1919 Courier p1** council report directly says **F. D. Cox was granted a billiard hall license for the year**. The **13 Feb. Courier p1** then reports that Cox's billiard parlors had been purchased by **Mr. Rohrberg of Ocean Falls, B.C.** and that Cox would take active charge of his soda works. The **14 Feb. Enterprise p5** independently reports the purchase and says Rohrberg would **assume charge Wednesday morning**, establishing an intended handover on **12 Feb. 1919**.

None of these sources prints the parlors' address. Do **not** project the directly documented 1915 Main-between-Seventh/Eighth location into 1919, and do not assign the sold parlors to 501/503/505. Search forward under the visually verified surname **Rohrberg** for a premises number, license, advertisement, or business name.''')

append_once('businesses/ohio-painless-dentists.md',MARKER,f'''## February 1919 continuation
{MARKER}

Visually verified **14 Feb. p2** and **28 Feb. p7 Enterprise** advertisements (`{E}` / `{S}`) repeat **Ohio Dentists**, **Dr. J. G. Nash, Manager**, **507½ Main Street**, **over Harding's Drug Store**, Phone 62. This extends the direct office-location run through **28 February 1919**. Harding's exact lower-floor number remains unprinted and therefore inferential.''')
append_once('people/profiles/j-g-nash.md',MARKER,f'''## February 1919 continuation
{MARKER}

`{E}` / `{S}` visually verifies Dr. J. G. Nash again as manager of Ohio Dentists at **507½ Main over Harding's Drug Store** on **14 and 28 February 1919**, extending his direct advertised role through month end.''')
append_once('businesses/ff-theroux.md',MARKER,f'''## February 1919 — 210 Seventh Street
{MARKER}

`{E}` / `{S}` visually verifies **Theroux Music House at 210 Seventh Street** in Enterprise advertisements on **7, 14 and 21 February 1919**; the 7 Feb. ad adds **near Elevator**. This is direct 1919 address evidence. It does not by itself date Theroux's departure from 519 Main; separate evidence already places a different occupant at 519 by October 1918.''')
append_once('people/profiles/ff-theroux.md',MARKER,f'''## February 1919 address continuation
{MARKER}

`{E}` / `{S}` directly places Theroux Music House at **210 Seventh Street** on 7/14/21 Feb. 1919. This updates the later business-address chronology without proving the exact move date from 519 Main.''')
append_once('businesses/farr-brothers-store.md',MARKER,f'''## February 1919 continuation
{MARKER}

The visually verified **21 Feb. p3** and **28 Feb. p7 Enterprise** market reports (`{E}` / `{S}`) credit **Brady Mercantile Company and Farr Brothers**. These are dated business appearances only: no address or individual proprietor is printed. Do not merge this grocery/meat concern with Edwin/Alice Farr or Farr's Pool Hall at 505 Main.''')

append_once('timeline.md',MARKER,f'''## February 1919 — complete local-newspaper monthly visual batch
{MARKER}

A scan-first review of **56/56 February pages** (`{S}` / `{E}`) adds a major pool-business transition: F. D. Cox received a yearly billiard-hall license on 6 Feb.; his billiard parlors were reported sold to **Mr. Rohrberg of Ocean Falls, B.C.**, with the Enterprise saying Rohrberg would assume charge **12 Feb. 1919**. The address is not printed and is not assigned to 501/503/505 or projected from Cox's 1915 Seventh–Eighth location. Ohio Dentists/Dr. Nash continue at **507½ Main over Harding's Drug Store** through 28 Feb.; Theroux Music House is directly at **210 Seventh** on 7/14/21 Feb.; Farr Brothers receives 21/28 Feb market-report credits. No exact 501/503/505 occupant or target construction event was recovered; this is bounded coverage only.''')

append_once('registers/business-timeline.md',MARKER,f'''## February 1919 verified business controls
{MARKER}

| Date | Address | Business / event | Evidence | Limit |
| --- | --- | --- | --- | --- |
| 6–14 Feb. 1919 | **Not printed** | F. D. Cox billiard hall licensed for year; parlors sold to Mr. Rohrberg; intended handover 12 Feb. | `{E}` / `{S}` | Direct sale/operation chronology; no premises number and no 501/503/505 assignment. |
| 14 & 28 Feb. 1919 | **507½ Main** | Ohio Dentists / Dr. J. G. Nash | `{E}` / `{S}` | Direct; `over Harding's Drug Store`; Harding lower exact number unprinted. |
| 7/14/21 Feb. 1919 | **210 Seventh Street** | Theroux Music House (`BUS-029`) | `{E}` / `{S}` | Direct; exact prior move date from 519 Main unresolved. |
| 21 & 28 Feb. 1919 | Not printed | Farr Brothers + Brady Mercantile market-report credit | `{E}` / `{S}` | Dated business appearance only; no Farr's Pool Hall merge. |''')

append_once('registers/address-register.md',MARKER,f'''## February 1919 address controls
{MARKER}

| Address | Date | Use | Evidence / limit |
| --- | --- | --- | --- |
| **507½ Main** | 14 & 28 Feb. 1919 | Ohio Dentists; Dr. J. G. Nash manager | `{E}` / `{S}`; direct `over Harding's Drug Store`, but Harding's ground-floor exact number is not printed. |
| **210 Seventh Street** | 7/14/21 Feb. 1919 | Theroux Music House | `{E}` / `{S}`; direct business address, unrelated to target frontage. |''')

append_once('evidence/open-questions.md',MARKER,f'''## February 1919 Cox/Rohrberg premises question
{MARKER}

`{E}` / `{S}` proves F. D. Cox still held an Oregon City billiard-hall license in early Feb. 1919 and then sold his billiard parlors to **Mr. Rohrberg**, with intended handover **12 Feb.** The exact premises remains unresolved. The direct 1915 Cox hall between Seventh and Eighth must not be projected into 1919. Resolve Rohrberg's given name and locate his 1919 license/application, advertisement, directory listing, or premises number before connecting this sale to any Main Street address.''')
append_once('evidence/research-leads.md',MARKER,f'''## 7 September 2026 — Cox → Rohrberg February 1919 follow-forward
{MARKER}

`{E}` / `{S}` establishes an intended **12 Feb. 1919** handover of F. D. Cox's billiard parlors to **Mr. Rohrberg of Ocean Falls, B.C.**, but no address. Search March–June 1919 newspapers, council/license records and directories for **Rohrberg + billiard/pool/cigar**, and separately test whether a premises number appears. Do not project the 1915 Cox Seventh–Eighth location or infer 501/503/505 from business type alone.''')
append_once('indexes/id-crosswalk.md',MARKER,f'''## {S} / {E} — February 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` → Cox pool-hall research: yearly license, sale to Mr. Rohrberg, intended 12 Feb. handover; address unresolved.
- `{S}` / `{E}` → `BUS-106` / `P-397`: Ohio Dentists / J. G. Nash continue at **507½ Main over Harding's Drug Store** through 28 Feb.
- `{S}` / `{E}` → `BUS-029` / `P-044`: Theroux Music House directly at **210 Seventh** on 7/14/21 Feb.
- `{S}` / `{E}` → `BUS-104`: Farr Brothers market-report credits 21/28 Feb.; no Farr's Pool Hall merge.
- No 501/503/505 building event created from the February no-hit.''')
append_once('registers/research-log.md',MARKER,f'''| 2026-09-07 | Completed February 1919 Enterprise + Courier scan-first visual audit | **56/56 pages**: Courier 24/24 (6/13/20/27 Feb.) + Enterprise 32/32 (7/14/21/28 Feb.); cumulative Jan–Feb **126 visually verified pages**. F. D. Cox annual billiard license and Cox→Rohrberg sale/handover (12 Feb intended) verified without premises address; Ohio Dentists 507½-over-Harding through 28 Feb.; Theroux 210 Seventh; Farr Brothers market-report credits. No exact 501/503/505 occupant or target construction event; bounded coverage only. `{S}` / `{E}`. |\n{MARKER}''')
append_once('ARCHIVE_INDEX.md',MARKER,f'''## 1919 February complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- February local-newspaper coverage: **56/56 visually verified pages** (`{S}` / `{E}`); Jan–Feb cumulative **126 pages**.
- Cox billiard hall: yearly license followed by sale to Mr. Rohrberg, intended handover 12 Feb.; premises number unresolved.
- Ohio Dentists at 507½-over-Harding through 28 Feb.; Theroux at 210 Seventh; Farr Brothers market-report continuation.
- No source-explicit 501/503/505 occupant or target construction event; no-hit is bounded coverage only.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological batch: **March 1919 Enterprise + Courier**.''')

# Update 1919 year-status row in place.
ys=read('registers/year-status.md')
lines=ys.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| 1919 |'):
        lines[i]=(f'| 1919 | **IN PROGRESS** | `{CAPTURE}`; `evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; '
                  '`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | '
                  f'January + February scan-first local-newspaper coverage **126 visually verified pages**: January 70 + February 56 (`{S}`/`{E}` for February). '
                  'February adds the F. D. Cox billiard license and Cox→Rohrberg sale/handover without a premises number, extends Ohio Dentists at 507½-over-Harding through 28 Feb., and directly places Theroux at 210 Seventh; no exact 501/503/505 occupant or target construction event. '
                  'March–December annual visual work and other online source classes remain; Banner-Courier from July 1919 has a documented manual microfilm gap. |')
        break
else: raise RuntimeError('1919 year-status row not found')
write('registers/year-status.md','\n'.join(lines)+'\n')

# Link new source/evidence to January-created Ohio/Nash YAML records where their inline lists exist.
for path,eid in [('database/businesses.yml','BUS-106'),('database/people.yml','P-397')]:
    add_inline_list_value(path,eid,'related_evidence',E)
    add_inline_list_value(path,eid,'related_sources',S)

print(f'Integrated February 1919 as {S} / {E}')
