from pathlib import Path
import json
import re

root = Path('.')
batch = root / 'newspapers/oregon-city-enterprise/1915-pages-001-120'
mp = batch / 'manifest.json'
manifest = json.loads(mp.read_text())
items = manifest['items']
assert len(items) == 120
assert items[0]['date'] == '1915-01-01' and items[0]['sequence'] == 1
assert items[-1]['date'] == '1915-04-09' and items[-1]['sequence'] == 8

sr_path = root / 'evidence/source-register.md'
er_path = root / 'evidence/evidence-register.md'
sr = sr_path.read_text()
er = er_path.read_text()
if '1915 Enterprise pages 1–120 visual review' in er or '1915 Enterprise pages 1-120 visual review' in er:
    raise SystemExit('Enterprise pages 1-120 already integrated')

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
last_media = first_media + 119
manifest['review_status'] = 'VISUALLY VERIFIED — all 120 chronological page images inspected 2026-08-27'
manifest['source_id'] = source_id
manifest['evidence_id'] = evidence_id
manifest['media_range'] = f'IMG-{first_media:04d}–IMG-{last_media:04d}'
mp.write_text(json.dumps(manifest, indent=2) + '\n')

issue_dates = [
    '1915-01-01', '1915-01-08', '1915-01-15', '1915-01-22', '1915-01-29',
    '1915-02-05', '1915-02-12', '1915-02-19', '1915-02-26',
    '1915-03-05', '1915-03-12', '1915-03-19', '1915-03-26',
    '1915-04-02', '1915-04-09'
]

readme = f'''# Morning Enterprise scans — 1915 chronological pages 1–120

Source **{source_id}** / evidence **{evidence_id}**. These are 120 unchanged single-page archive PDFs covering 15 complete Friday issues from **1 January through 9 April 1915**, eight pages per issue. All 120 scans were rendered and visually inspected on 27 August 2026.

Exact archive URLs and SHA-256 hashes are preserved in `manifest.json` and `sha256.txt`. Media **IMG-{first_media:04d}–IMG-{last_media:04d}** correspond one-to-one to the saved PDFs.

[Detailed visual-review checkpoint](../../../evidence/source-captures/1915-enterprise-pages-001-120.md).

Pause point: **chronological page 120 = 9 April 1915, sequence/page 8**. Next Enterprise page: **121 = 16 April 1915, sequence/page 1**. Enterprise progress is **120/428 images = 30/107 four-page scan sheets**; 308 images / 77 sheets remain. This batch does not certify 1915 as ONLINE COMPLETE.
'''
(batch / 'README.md').write_text(readme)

issue_rows = '\n'.join(f'| {d} | 1–8 | VISUALLY VERIFIED |' for d in issue_dates)
capture = f'''# 1915 Morning Enterprise — chronological pages 1–120

Review date: **27 August 2026**. Source **{source_id}**; evidence **{evidence_id}**.  
Status: **VISUALLY VERIFIED — all 120 page images inspected**.

## Scope and pause checkpoint

The first **120 chronological page images** of the 1915 *Morning Enterprise* were recovered, preserved, rendered and visually inspected. The cutoff lands cleanly after 15 complete eight-page issues:

| Issue date | Pages | Status |
| --- | --- | --- |
{issue_rows}

Repository originals: `newspapers/oregon-city-enterprise/1915-pages-001-120/`; exact URLs and SHA-256 hashes are preserved in the manifest. Media **IMG-{first_media:04d}–IMG-{last_media:04d}**.

**Pause:** page **120 = 9 April 1915 p8**.  
**Next:** page **121 = 16 April 1915 p1**.  
Enterprise progress: **120/428 images = 30/107 four-page scan sheets**; **308 images / 77 sheets remain**.

## Visually verified findings

### 1 January 1915 p5 — Holman move to Fifth and Main

R. L. Holman's advertisement states that the leading funeral director **“has moved to more commodious parlors” at Fifth and Main Street**. This is strong intersection-level evidence that Holman's premises were at Fifth/Main by the first 1915 issue. It does **not** print a numbered address and is not converted to 501, 503, 505 or a numbered Fifth Street premise without an independent mapping source.

### 8 January 1915 p7 and recurring notices — Fashion Stable on Fifth

A. J. Eddy, V.S., M.D.V., advertises at the **Fashion Stable, Fifth Street, between Main and Water Streets**. The same relative-location notice recurs during this batch. This is a valuable Fifth Street block anchor between the commercial Main frontage and Water Street, but it is **unnumbered**. No 102/104/106/108/110 Fifth number is inferred from the wording.

### 26 March 1915 p1 — Main Street brick reuse proposal

A visually inspected article headed **“MAIN STREET BRICKS MAY BE PUT ON ROAD”** reports a proposal to improve the Singer Hill road using the best bricks removed from Main Street. The report says many bricks near the curb and in the southern portion of Main Street remained serviceable and could be taken up, cleaned and reused. This corroborates physical removal/reworking of the old Main Street paving in the 1915 improvement program. It does not establish demolition or alteration of a target storefront.

### 2 April 1915 p1 — Main Street improvement as a major 1915 public work

The front-page public-works report includes **improvement of Main Street** among the large Oregon City/Clackamas County projects expected to employ many workers during 1915, alongside the locks, West Linn water system, roads and bridges. This corroborates the scale and contemporary importance of the Main Street project, not a building event.

### 9 April 1915 p3 — paving-material debate

The visually inspected council report records continued debate over the material to be used on Main Street, including a resolution calling for **El Oso** and criticism/discussion of asphaltic concrete. This extends the documented pre-construction decision sequence for the 1915 repaving. It does not prove a target-address property action.

## Target-address and Fifth-number coverage

Across these 120 visually inspected pages, no defensible exact **503 Main** or **505 Main** occupant/building-status statement was identified. No exact **102, 104, 106, 108 or 110 Fifth Street** listing, and no new numbered Fifth Street occupant, was established in this batch. The Holman and Fashion Stable notices are retained exactly as intersection/relative-location evidence. These are bounded coverage statements only — not evidence of vacancy, demolition, non-use or nonexistence.

## Resume rule

Resume at **16 April 1915 p1 / chronological Enterprise page 121**. OCR/text may be used for discovery, but the remaining 308 images do not count until their actual page scans are visually inspected. Courier 123/123 remains complete at the visual-review level, while Courier callouts M01–M04 and the remaining 1915 online-source/manual-work requirements remain open.
'''
cap = root / 'evidence/source-captures/1915-enterprise-pages-001-120.md'
assert not cap.exists()
cap.write_text(capture)

sr += f'''\n\n## {source_id} — Morning Enterprise 1915 visual batch, chronological pages 1–120
Type: Primary newspaper scans / exhaustive visual review.  
Dates: 1 January–9 April 1915; 15 complete issues, 120 page images.  
Canonical URL pattern: https://oregonnews.uoregon.edu/lccn/sn00063700/YYYY-MM-DD/ed-1/seq-N.pdf  
Repository: `newspapers/oregon-city-enterprise/1915-pages-001-120/`; exact URLs and SHA-256 hashes in `manifest.json`.  
Media: `IMG-{first_media:04d}` through `IMG-{last_media:04d}`.  
Evidence: `{evidence_id}`; detailed review `evidence/source-captures/1915-enterprise-pages-001-120.md`.  
Notes: All 120 scans visually inspected. Holman move to Fifth/Main verified 1 Jan p5; A. J. Eddy/Fashion Stable verified on Fifth between Main and Water; Mar 26, Apr 2 and Apr 9 pages extend the Main Street paving chronology. No exact 503/505 or new numbered Fifth occupant identified; coverage only. Pause after 9 Apr p8; next 16 Apr p1.
'''
sr_path.write_text(sr)

sy_path = root / 'database/sources.yml'
sy = sy_path.read_text().rstrip()
sy += f'''\n\n  - id: {source_id}
    name: Morning Enterprise 1915 visual batch, chronological pages 1-120
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1915-01-01/ed-1/
    notes: 120 page PDFs from fifteen complete issues, Jan 1 through Apr 9, visually inspected and preserved under newspapers/oregon-city-enterprise/1915-pages-001-120/. Related evidence {evidence_id}; media IMG-{first_media:04d} through IMG-{last_media:04d}. Enterprise pause 120/428 images; next Apr 16 p1.
'''
sy_path.write_text(sy + '\n')

er += f'''\n\n## {evidence_id} — 1915 Enterprise pages 1–120 visual review
Type: Primary newspaper visual review; source `{source_id}`.  
Record: `evidence/source-captures/1915-enterprise-pages-001-120.md`.  
Claims: All 120 page images from 1 January through 9 April were visually inspected. Jan 1 p5 says R. L. Holman moved to Fifth/Main. Jan 8 p7 and recurring notices place A. J. Eddy at Fashion Stable on Fifth between Main and Water. Mar 26 p1 reports proposed reuse of bricks removed from Main Street; Apr 2 p1 identifies Main Street improvement as a major 1915 public work; Apr 9 p3 records the paving-material debate. No exact 503/505 or new numbered Fifth occupant is established; coverage only.  
Confidence: Very High for the visually readable location and public-works wording; exact numbered mapping and target occupancy unresolved.
'''
er_path.write_text(er)

ey_path = root / 'database/evidence.yml'
ey = ey_path.read_text().rstrip()
ey += f'''\n\n  - id: {evidence_id}
    name: 1915 Enterprise pages 1-120 visual review
    type: Primary newspaper visual review of 120 page images
    claims:
      - All 120 page images from January 1 through April 9 were visually inspected.
      - January 1 p5 states R. L. Holman moved to more commodious parlors at Fifth and Main; no number is printed.
      - January 8 p7 and recurring professional notices place A. J. Eddy at Fashion Stable on Fifth Street between Main and Water Streets; no number is printed.
      - March 26 p1 reports a proposal to reuse serviceable bricks removed from Main Street on Singer Hill, corroborating physical paving removal/reworking.
      - April 2 p1 identifies improvement of Main Street among major 1915 public works; April 9 p3 records continued debate over paving material including El Oso and asphaltic concrete.
      - No defensible exact 503/505 occupant or new numbered Fifth Street occupant was identified; this is bounded coverage only, not vacancy or non-use evidence.
    confidence: Very High for visually verified printed location and public-works wording; exact numbered mapping and target occupancy unresolved.
    related_sources: [{source_id}]
    related_evidence: [E-054]
    related_buildings: [B-001, B-002, B-005]
    repository_file: evidence/source-captures/1915-enterprise-pages-001-120.md
'''
ey_path.write_text(ey + '\n')

mr = mr.rstrip() + f'''\n\n## Morning Enterprise 1915 pages 1–120 — {source_id} / {evidence_id}

All 120 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-001-120/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
'''
for item in items:
    mr += f"| {item['media_id']} | `newspapers/oregon-city-enterprise/1915-pages-001-120/{item['file']}` | {item['date']} / seq{item['sequence']} / printed{item['printed_page']} |\n"
mr_path.write_text(mr + '\n')

ys_path = root / 'registers/year-status.md'
ys = ys_path.read_text()
match = re.search(r'^\| 1915 \|.*$', ys, re.M)
assert match
newrow = '| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-page-review-checklist.md` | Courier **123/123** through year end. Enterprise **120/428 images = 30/107 sheets**, visually reviewed through **9 Apr p8**; next 16 Apr p1, 308 images / 77 sheets remain. Water-ledger/other-source work pending; Courier M01–M04 remain open. |'
ys = ys[:match.start()] + newrow + ys[match.end():]
ys_path.write_text(ys)

pc_path = root / 'evidence/source-captures/1915-page-review-checklist.md'
pc = pc_path.read_text()
pc = re.sub(r'^Status:.*$', 'Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 120/428 images; other-source work pending**', pc, count=1, flags=re.M)
marker = '\n## Latest Courier completion checkpoint - through 30 December 1915\n'
assert marker in pc
checkpoint = f'''\n## Latest Enterprise pause checkpoint — chronological page 120 / 9 April 1915

- **120/428 Enterprise page images visually inspected = 30/107 four-page scan sheets.** Fifteen complete issues, Jan. 1 through Apr. 9, eight pages each. Source `{source_id}`, evidence `{evidence_id}`, media `IMG-{first_media:04d}`–`IMG-{last_media:04d}`.
- Saved originals: `newspapers/oregon-city-enterprise/1915-pages-001-120/`; [detailed visual log](1915-enterprise-pages-001-120.md).
- **Exact pause:** page 120 = Apr. 9 p8. **Next:** page 121 = Apr. 16 p1. Remaining Enterprise: **308 images / 77 sheets**.
- Verified additions: Holman moved to Fifth/Main by Jan. 1; A. J. Eddy/Fashion Stable on Fifth between Main and Water; Main Street brick-removal/reuse proposal Mar. 26; major-work context Apr. 2; paving-material debate Apr. 9.
- No exact 503/505 or new numbered Fifth occupant identified in this batch. Coverage only; no vacancy/non-use inference.
- Courier remains 123/123; M01–M04, water-ledger/other-source review and year closeout remain open. **1915 is not ONLINE COMPLETE.**
'''
pc = pc.replace(marker, checkpoint + marker, 1)
pc_path.write_text(pc)

rl_path = root / 'registers/research-log.md'
rl = rl_path.read_text()
sep = '| --- | --- | --- | --- |\n'
assert sep in rl
row = f'| 2026-08-27 | Restarted 1915 Morning Enterprise visual pass; processed chronological pages 1–120 | Preserved and visually inspected 120 page scans / 15 complete issues, Jan. 1–Apr. 9. Verified Holman at Fifth/Main, A. J. Eddy/Fashion Stable on Fifth between Main and Water, and Mar.–Apr. Main Street paving chronology. No exact 503/505 or new numbered Fifth occupant; coverage only. | Pause at Apr. 9 p8. Resume page 121 / Apr. 16 p1; 308 Enterprise images / 77 sheets remain. Courier 123/123; other-source work and M01–M04 remain. |\n'
rl = rl.replace(sep, sep + row, 1)
rl_path.write_text(rl)

ar_path = root / 'registers/address-register.md'
ar = ar_path.read_text()
anchor = '### Fifth Street address-reconstruction goal\n'
assert anchor in ar
add = f'''### Enterprise visual update through 9 April 1915

**{evidence_id}/{source_id}** adds an unnumbered but useful Fifth Street anchor: A. J. Eddy advertised at **Fashion Stable, Fifth Street between Main and Water Streets**, beginning with the visually verified 8 January p7 notice and recurring in the reviewed period. R. L. Holman's 1 January p5 advertisement separately says he had moved to **Fifth and Main**. Neither relative-location statement is assigned to 501/503/505 or to 102/104/106/108/110 Fifth without an independent numbered source. No new numbered Fifth address was established in Enterprise pages 1–120.

'''
ar = ar.replace(anchor, add + anchor, 1)
ar_path.write_text(ar)

rep_path = root / 'evidence/source-captures/1915-main-street-repaving.md'
rep = rep_path.read_text().rstrip()
if 'Enterprise visual addendum — 26 March through 9 April 1915' not in rep:
    rep += f'''\n\n## Enterprise visual addendum — 26 March through 9 April 1915

Source `{source_id}` / evidence `{evidence_id}` adds three visually verified stages to the paving chronology. **26 March p1** reports a proposal to reuse serviceable bricks removed from Main Street on Singer Hill. **2 April p1** identifies Main Street improvement among the area's major 1915 public works. **9 April p3** records continued council debate over paving material, including El Oso and asphaltic concrete. These items establish street-surface planning/removal context only; they do not establish demolition, rebuilding, or alteration of 501/503/505.
'''
rep_path.write_text(rep + '\n')

tl_path = root / 'timeline.md'
tl = tl_path.read_text()
if 'Enterprise visual checkpoint through 9 April 1915' not in tl:
    m = re.search(r'(^## 1915[^\n]*\n)', tl, re.M)
    if m:
        para = f'''\n**Enterprise visual checkpoint through 9 April 1915 (`{evidence_id}` / `{source_id}`).** The first 120 *Morning Enterprise* page images were visually reviewed. A 1 January ad says R. L. Holman had moved to Fifth/Main; recurring professional-directory notices place A. J. Eddy at Fashion Stable on Fifth between Main and Water. On 26 March the paper reported a proposal to reuse bricks removed from Main Street on Singer Hill; 2 April described Main Street improvement among the area's major 1915 public works; and 9 April recorded continued paving-material debate. None of these pages supplies an exact 503/505 occupant or a new numbered Fifth address.
'''
        tl = tl[:m.end()] + para + tl[m.end():]
    else:
        tl += f'''\n\n## January–April 1915 — Enterprise visual checkpoint through 9 April 1915
The first 120 *Morning Enterprise* pages are visually verified under `{evidence_id}` / `{source_id}`. Holman is at Fifth/Main; A. J. Eddy/Fashion Stable is on Fifth between Main and Water; March–April reports extend the Main Street paving chronology. No exact 503/505 or new numbered Fifth address is established.
'''
tl_path.write_text(tl)

dty_path = root / 'database/timeline.yml'
dty = dty_path.read_text().rstrip()
t_nums = [int(x) for x in re.findall(r'^  - id: T-(\d{3})\b', dty, re.M)]
tid = f'T-{max(t_nums) + 1:03d}'
dty += f'''\n\n  - id: {tid}
    date: January 1-April 9, 1915
    summary: First 120 Morning Enterprise pages visually reviewed. Holman states he moved to Fifth/Main; A. J. Eddy advertises at Fashion Stable on Fifth between Main and Water; March-April reports document Main Street brick removal/reuse planning, major-improvement context, and paving-material debate. No exact 503/505 or new numbered Fifth address is established.
    confidence: Very High for visually verified printed wording; exact numbered target mapping unresolved
    related_evidence:
      - {evidence_id}
    related_buildings:
      - B-001
      - B-002
      - B-005
'''
dty_path.write_text(dty + '\n')

print(f'Allocated {source_id}, {evidence_id}, IMG-{first_media:04d}..IMG-{last_media:04d}, {tid}')
