from pathlib import Path
import json
import re

root = Path('.')
batch = root / 'newspapers/oregon-city-enterprise/1915-pages-201-225'
mp = batch / 'manifest.json'
manifest = json.loads(mp.read_text())
items = manifest['items']
assert len(items) == 25
assert items[0]['chronological_page'] == 201 and items[0]['date'] == '1915-06-25' and items[0]['sequence'] == 1
assert items[-1]['chronological_page'] == 225 and items[-1]['date'] == '1915-07-16' and items[-1]['sequence'] == 1

sr_path = root / 'evidence/source-register.md'
er_path = root / 'evidence/evidence-register.md'
sr = sr_path.read_text()
er = er_path.read_text()
if 'Morning Enterprise 1915 visual batch, chronological pages 201-225' in sr:
    raise SystemExit('Enterprise pages 201-225 already integrated')

s_nums = [int(x) for x in re.findall(r'## S-(\d{3})\b', sr)]
e_nums = [int(x) for x in re.findall(r'## E-(\d{3})\b', er)]
source_id = f'S-{max(s_nums) + 1:03d}'
evidence_id = f'E-{max(e_nums) + 1:03d}'

mr_path = root / 'media/photo-metadata-register.md'
mr = mr_path.read_text()
m_nums = [int(x) for x in re.findall(r'IMG-(\d{4})', mr)]
first_media = max(m_nums) + 1
for off, item in enumerate(items):
    item['review_status'] = 'VISUALLY VERIFIED'
    item['visual_review_date'] = '2026-08-27'
    item['media_id'] = f'IMG-{first_media + off:04d}'
    item['printed_page'] = item['sequence']
last_media = first_media + 24
manifest['review_status'] = 'VISUALLY VERIFIED - all 25 chronological page images inspected 2026-08-27'
manifest['source_id'] = source_id
manifest['evidence_id'] = evidence_id
manifest['media_range'] = f'IMG-{first_media:04d}-IMG-{last_media:04d}'
mp.write_text(json.dumps(manifest, indent=2) + '\n')

readme = f'''# Morning Enterprise scans - 1915 chronological pages 201-225

Source **{source_id}** / evidence **{evidence_id}**. Twenty-five unchanged single-page archive PDFs covering complete issues of **25 June, 2 July and 9 July 1915**, plus **16 July page 1**. All 25 scans were rendered and visually inspected on 27 August 2026.

Exact archive URLs and SHA-256 hashes are preserved in `manifest.json` and `sha256.txt`. Media **IMG-{first_media:04d}-IMG-{last_media:04d}** correspond one-to-one to the saved PDFs.

[Detailed visual-review checkpoint](../../../evidence/source-captures/1915-enterprise-pages-201-225.md).

Pause point: **chronological page 225 = 16 July 1915, page 1**. Next Enterprise page: **226 = 16 July 1915, page 2**. Enterprise progress is **225/428 images**; **203 images remain**. This batch does not certify 1915 as ONLINE COMPLETE.
'''
(batch / 'README.md').write_text(readme)

capture = f'''# 1915 Morning Enterprise - chronological pages 201-225

Review date: **27 August 2026**. Source **{source_id}**; evidence **{evidence_id}**.  
Status: **VISUALLY VERIFIED - all 25 page images inspected**.

## Scope and pause checkpoint

This batch covers three complete eight-page issues - **25 June, 2 July and 9 July 1915** - plus **16 July page 1**. Repository originals are in `newspapers/oregon-city-enterprise/1915-pages-201-225/`; exact URLs and hashes are in the manifest. Media **IMG-{first_media:04d}-IMG-{last_media:04d}**.

**Pause:** page **225 = 16 July 1915 p1**.  
**Next:** page **226 = 16 July 1915 p2**.  
Enterprise progress: **225/428 images**; **203 images remain**.

## Visually verified findings

### 25 June p5 - Main Street paving contract awarded to Worswick

The page carries the headline **“PAVING OF MAIN STREET AWARDED TO WORSWICK.”** The article reports that the contract for improvement of Main Street with asphaltic-concrete pavement was awarded to the Worswick company. It describes Worswick as the only bidder, gives the bid as **$1.20 per yard**, states that a **10-year good-condition guarantee** was required, and says the improvement cost was not to exceed **$14,184**. The same report says the Portland Railway, Light & Power company would straighten/adjust its Main Street track before the new street surface was laid.

This independently corroborates the 24 June Courier contract report and strengthens the street-project chronology. It is public-works evidence only and does not establish demolition, relocation or alteration of 501/503/505 storefronts.

### 2 July p3 - paving bond/contract deadlock

A visually inspected report headed **“SCHUEBEL AND PAVING MEN STILL DEADLOCKED”** describes an unresolved dispute between City Attorney Schuebel and the paving representatives over the bond/guarantee terms. The article says the contract could not simply proceed without satisfying the required protection/guarantee conditions. This shows that the June 25 award did not mean every contract-security issue was already settled.

### 9 July p3 - security terms and physical Main Street work begin

The page prominently reports **“TWO BONDS AND DEPOSIT OF 15 PER CENT OF COST OF MAIN STREET PAVEMENT WILL PROTECT OREGON CITY.”** A separate article on the same page is headed **“MAIN STREET WORK BEGINS AT LAST”** and reports that the Portland Railway, Light & Power company had begun work on its Main Street track, including bringing in rails/material so defective track could be corrected before paving. The report expected paving-company work to follow after the rail work.

This is useful physical-project evidence: Main Street work had moved from planning/contracting into on-street preparation by 9 July. It still does **not** establish a target-storefront building event.

### 16 July p1 - partial-issue cutoff

Page 1 of the 16 July issue was visually reviewed. No target-block exact-address or numbered Fifth Street finding was established on this page. Pages 2-8 of the issue remain pending and begin the next batch.

## Target-address and Fifth-number coverage

Across these 25 visually inspected pages, no defensible exact **503 Main** or **505 Main** occupant/building-status statement was identified. No exact **102, 104, 106, 108 or 110 Fifth Street** listing, and no other new numbered Fifth Street occupant, was established. These are bounded coverage statements only - not evidence of vacancy, demolition, non-use or nonexistence.

## Resume rule

Resume at **16 July 1915 p2 / chronological Enterprise page 226**. OCR/text may be used for discovery only; the remaining 203 images do not count until the actual page scans are visually inspected.
'''
cap_path = root / 'evidence/source-captures/1915-enterprise-pages-201-225.md'
assert not cap_path.exists()
cap_path.write_text(capture)

source_name = 'Morning Enterprise 1915 visual batch, chronological pages 201-225'
evidence_name = '1915 Enterprise pages 201-225 visual review'

sr += f'''\n\n## {source_id} - {source_name}
Type: Primary newspaper scans / exhaustive visual review.  
Dates: 25 June-16 July 1915; 25 page images (three complete issues plus 16 July p1).  
Repository: `newspapers/oregon-city-enterprise/1915-pages-201-225/`; exact URLs and SHA-256 hashes in `manifest.json`.  
Media: `IMG-{first_media:04d}` through `IMG-{last_media:04d}`.  
Evidence: `{evidence_id}`; detailed review `evidence/source-captures/1915-enterprise-pages-201-225.md`.  
Notes: All 25 scans visually inspected. June 25 confirms the Worswick Main Street paving award; July 2 records the bond/guarantee deadlock; July 9 records security terms and actual Main Street rail/preparatory work beginning. No exact 503/505 or new numbered Fifth occupant; coverage only. Pause after 16 July p1; next p2.
'''
sr_path.write_text(sr)

sy_path = root / 'database/sources.yml'
sy = sy_path.read_text().rstrip()
sy += f'''\n\n  - id: {source_id}
    name: {source_name}
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1915-06-25/ed-1/
    notes: Twenty-five page PDFs from June 25 through July 16 p1, visually inspected and preserved under newspapers/oregon-city-enterprise/1915-pages-201-225/. Related evidence {evidence_id}; media IMG-{first_media:04d} through IMG-{last_media:04d}. Enterprise pause 225/428 images; next July 16 p2.
'''
sy_path.write_text(sy + '\n')

er += f'''\n\n## {evidence_id} - {evidence_name}
Type: Primary newspaper visual review; source `{source_id}`.  
Record: `evidence/source-captures/1915-enterprise-pages-201-225.md`.  
Claims: All 25 page images from 25 June through 16 July p1 were visually inspected. June 25 p5 independently confirms the Worswick Main Street paving contract award, $1.20-per-yard bid, 10-year guarantee condition and $14,184 maximum cost. July 2 p3 records a bond/guarantee deadlock. July 9 p3 records two-bond/15-percent security terms and that physical Main Street rail/preparatory work had begun. No exact 503/505 or new numbered Fifth occupant is established; coverage only.  
Confidence: Very High for the visually readable public-works wording; target occupancy and building effects unresolved.
'''
er_path.write_text(er)

ey_path = root / 'database/evidence.yml'
ey = ey_path.read_text().rstrip()
ey += f'''\n\n  - id: {evidence_id}
    name: {evidence_name}
    type: Primary newspaper visual review of 25 page images
    claims:
      - All 25 page images from June 25 through July 16 page 1 were visually inspected.
      - June 25 page 5 independently confirms the Worswick Main Street paving contract award, a $1.20-per-yard bid, a 10-year guarantee condition, and a maximum improvement cost of $14,184.
      - July 2 page 3 records an unresolved paving bond/guarantee deadlock.
      - July 9 page 3 records two-bond and 15-percent security terms and says actual Main Street rail/preparatory work had begun before paving.
      - No defensible exact 503/505 occupant or new numbered Fifth Street occupant was identified; this is bounded coverage only, not vacancy or non-use evidence.
    confidence: Very High for visually verified public-works wording; target occupancy and building effects unresolved.
    related_sources: [{source_id}]
    related_evidence: [E-114]
    related_buildings: [B-001, B-002, B-005]
    repository_file: evidence/source-captures/1915-enterprise-pages-201-225.md
'''
ey_path.write_text(ey + '\n')

mr = mr.rstrip() + f'''\n\n## Morning Enterprise 1915 pages 201-225 - {source_id} / {evidence_id}

All 25 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-201-225/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
'''
for item in items:
    mr += f"| {item['media_id']} | `newspapers/oregon-city-enterprise/1915-pages-201-225/{item['file']}` | {item['date']} / seq{item['sequence']} / printed{item['printed_page']} |\n"
mr_path.write_text(mr + '\n')

ys_path = root / 'registers/year-status.md'
ys = ys_path.read_text()
match = re.search(r'^\| 1915 \|.*$', ys, re.M)
assert match
newrow = '| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-enterprise-pages-121-160.md`; `evidence/source-captures/1915-enterprise-pages-161-200.md`; `evidence/source-captures/1915-enterprise-pages-201-225.md`; `evidence/source-captures/1915-page-review-checklist.md` | Courier **123/123** through year end. Enterprise **225/428 images**, visually reviewed through **16 Jul p1**; next 16 Jul p2, **203 images remain**. Water-ledger/other-source work pending; Courier M01-M04 remain open. |'
ys = ys[:match.start()] + newrow + ys[match.end():]
ys_path.write_text(ys)

pc_path = root / 'evidence/source-captures/1915-page-review-checklist.md'
pc = pc_path.read_text()
pc = re.sub(r'^Status:.*$', 'Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 225/428 images; other-source work pending**', pc, count=1, flags=re.M)
anchors = [
    '\n## Latest Enterprise pause checkpoint - chronological page 200 / 18 June 1915\n',
    '\n## Latest Enterprise pause checkpoint — chronological page 200 / 18 June 1915\n'
]
anchor = next((a for a in anchors if a in pc), None)
assert anchor
checkpoint = f'''\n## Latest Enterprise pause checkpoint - chronological page 225 / 16 July 1915 p1

- **225/428 Enterprise page images visually inspected.** New review covers June 25, July 2 and July 9 in full plus July 16 p1. Source `{source_id}`, evidence `{evidence_id}`, media `IMG-{first_media:04d}`-`IMG-{last_media:04d}`.
- Saved originals: `newspapers/oregon-city-enterprise/1915-pages-201-225/`; [detailed visual log](1915-enterprise-pages-201-225.md).
- **Exact pause:** page 225 = July 16 p1. **Next:** page 226 = July 16 p2. Remaining Enterprise: **203 images**.
- Verified additions: June 25 Worswick contract award; July 2 bond/guarantee deadlock; July 9 security terms and physical Main Street rail/preparatory work beginning.
- No exact 503/505 or new numbered Fifth occupant identified. Coverage only; no vacancy/non-use inference.
- Courier remains 123/123; M01-M04, water-ledger/other-source review and year closeout remain open. **1915 is not ONLINE COMPLETE.**
'''
pc = pc.replace(anchor, checkpoint + anchor, 1)
pc_path.write_text(pc)

rp_path = root / 'evidence/source-captures/1915-main-street-repaving.md'
rp = rp_path.read_text()
if '25 June-9 July 1915 - Enterprise contract and work-start sequence' not in rp:
    section = f'''\n## 25 June-9 July 1915 - Enterprise contract and work-start sequence

**Morning Enterprise; visually verified under {source_id} / {evidence_id}.**

- **25 June p5:** Worswick is reported as the only bidder and is awarded the Main Street asphaltic-concrete paving contract at $1.20 per yard, with a 10-year guarantee condition and maximum stated improvement cost of $14,184. Portland Railway, Light & Power track adjustment is to precede the new street surface.
- **2 July p3:** City Attorney Schuebel and paving representatives remain deadlocked over bond/guarantee terms, showing that the award did not immediately settle contract security.
- **9 July p3:** the paper reports two bonds plus a 15-percent deposit as protection for the city and separately says **Main Street work begins at last**, with Portland Railway, Light & Power starting track/rail preparation before paving work follows.

This independently strengthens the transition from contract award to actual on-street preparation. It is evidence about street and rail work, not storefront demolition or target-building alteration.
'''
    marker = '\n## 8 July 1915 - bond settled; work expected shortly\n'
    if marker not in rp:
        marker = '\n## 8 July 1915 — bond settled; work expected shortly\n'
    assert marker in rp
    rp = rp.replace(marker, section + marker, 1)
    rp_path.write_text(rp)

ms_path = root / 'evidence/source-captures/1915-main-street-research.md'
ms = ms_path.read_text()
if 'Enterprise checkpoint through 16 July p1' not in ms:
    ms += f'''\n\n## Enterprise checkpoint through 16 July p1 - {source_id} / {evidence_id}

Enterprise pages 201-225 were visually reviewed. The batch independently confirms the June 25 Worswick Main Street paving award, the July 2 guarantee/bond dispute, and the July 9 transition into physical Main Street rail/preparatory work. No exact 503/505 occupant or new numbered Fifth Street address was established. Review pauses at July 16 p1; resume at p2.\n'''
    ms_path.write_text(ms)

rl_path = root / 'registers/research-log.md'
rl = rl_path.read_text().rstrip()
rl += f'''\n\n## 2026-08-27 - 1915 Enterprise pages 201-225
- Visually inspected 25 page scans, 25 June through 16 July p1 (`{source_id}` / `{evidence_id}`).
- Preserved all original PDFs and hashes in `newspapers/oregon-city-enterprise/1915-pages-201-225/`.
- Confirmed June 25 Worswick contract award, July 2 bond/guarantee deadlock, and July 9 beginning of physical Main Street rail/preparatory work.
- No exact 503/505 or new numbered Fifth occupant identified; no negative occupancy inference made.
- Enterprise pause: 225/428 images; next page 226 = 16 July p2.\n'''
rl_path.write_text(rl + '\n')

ai_path = root / 'ARCHIVE_INDEX.md'
ai = ai_path.read_text().rstrip()
if '1915-enterprise-pages-201-225.md' not in ai:
    ai += f'''\n- `evidence/source-captures/1915-enterprise-pages-201-225.md` - {source_id}/{evidence_id}, 25 visually reviewed Morning Enterprise pages through 16 July p1; preserved originals under `newspapers/oregon-city-enterprise/1915-pages-201-225/`.\n'''
    ai_path.write_text(ai + '\n')

print(f'Allocated {source_id}, {evidence_id}, IMG-{first_media:04d}..IMG-{last_media:04d}')
