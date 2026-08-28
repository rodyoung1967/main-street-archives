from pathlib import Path
import json
import re

root = Path('.')
batch = root / 'newspapers/oregon-city-enterprise/1915-pages-161-200'
mp = batch / 'manifest.json'
manifest = json.loads(mp.read_text())
items = manifest['items']
assert len(items) == 40
assert items[0]['chronological_page'] == 161 and items[0]['date'] == '1915-05-21' and items[0]['sequence'] == 1
assert items[-1]['chronological_page'] == 200 and items[-1]['date'] == '1915-06-18' and items[-1]['sequence'] == 8

sr_path = root / 'evidence/source-register.md'
er_path = root / 'evidence/evidence-register.md'
sr = sr_path.read_text()
er = er_path.read_text()
source_name = 'Morning Enterprise 1915 visual batch, chronological pages 161-200'
evidence_name = '1915 Enterprise pages 161-200 visual review'
if source_name in sr or evidence_name in er:
    raise SystemExit('Enterprise pages 161-200 already integrated')

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
last_media = first_media + 39
manifest['review_status'] = 'VISUALLY VERIFIED - all 40 chronological page images inspected 2026-08-27'
manifest['source_id'] = source_id
manifest['evidence_id'] = evidence_id
manifest['media_range'] = f'IMG-{first_media:04d}-IMG-{last_media:04d}'
mp.write_text(json.dumps(manifest, indent=2) + '\n')

readme = f'''# Morning Enterprise scans - 1915 chronological pages 161-200

Source **{source_id}** / evidence **{evidence_id}**. Forty unchanged single-page archive PDFs covering five complete Friday issues from **21 May through 18 June 1915**, eight pages per issue. All 40 scans were rendered and visually inspected on 27 August 2026.

Exact archive URLs and SHA-256 hashes are preserved in `manifest.json` and `sha256.txt`. Media **IMG-{first_media:04d}-IMG-{last_media:04d}** correspond one-to-one to the saved PDFs.

[Detailed visual-review checkpoint](../../../evidence/source-captures/1915-enterprise-pages-161-200.md).

Pause point: **chronological page 200 = 18 June 1915, page 8**. Next Enterprise page: **201 = 25 June 1915, page 1**. Enterprise progress is **200/428 images = 50/107 four-page scan sheets**; 228 images / 57 sheets remain. This batch does not certify 1915 as ONLINE COMPLETE.
'''
(batch / 'README.md').write_text(readme)

capture = f'''# 1915 Morning Enterprise - chronological pages 161-200

Review date: **27 August 2026**. Source **{source_id}**; evidence **{evidence_id}**.  
Status: **VISUALLY VERIFIED - all 40 page images inspected**.

## Scope and pause checkpoint

This batch covers five complete eight-page issues: **21 May, 28 May, 4 June, 11 June and 18 June 1915**. Repository originals are in `newspapers/oregon-city-enterprise/1915-pages-161-200/`; exact URLs and hashes are in the manifest. Media **IMG-{first_media:04d}-IMG-{last_media:04d}**.

**Pause:** page **200 = 18 June 1915 p8**.  
**Next:** page **201 = 25 June 1915 p1**.  
Enterprise progress: **200/428 images = 50/107 four-page scan sheets**; **228 images / 57 sheets remain**.

## Visually verified findings

### 4 June p1 - Cox pool hall directly located between Seventh and Eighth

The front-page report headed **“ROOMS OF MOOSE LODGE IS FIRST PLACE INSPECTED”** identifies **Cox's poolhall, Main street between Seventh and Eighth**, and later repeats that officers went to **Cox's poolhall on Main street between Seventh and Eighth streets**.

This is direct relative-location evidence for the Cox hall involved in the late-May/early-June 1915 raid sequence. It materially supersedes the project's earlier directional inference that the officers' movement “down Main street” made the Fifth-Sixth / 503 area plausible for that raid-period hall. A premises between Seventh and Eighth cannot be 503 Main. The exact numbered address remains unresolved.

The identification with **Frank D. Cox** rests on the same raid/court sequence and independent February 1915 directory and June Courier evidence naming Frank D. Cox; it is not a surname-only merger.

### 11 June p3 and 18 June follow-up - Cox hall continuity

A 11 June report says a Ford automobile ran onto the sidewalk at **Cox's poolhall on Main street** and damaged two glass showcases. The 18 June front page continues the Myers/Cox case sequence. Neither item supplies a numbered street address.

### 4 June p3 - Main Street improvement ordinance and cluster lights

The city-council report states that the ordinance calling for **improvement of Main street** was read a second time and passed unanimously, and the recorder was instructed to advertise for bids. The same report says **T. L. Charman, representing Main street property owners**, presented a proposition for **cluster lights on Main street**. This strengthens the public-works/streetscape chronology but does not establish alteration or removal of a 501/503/505 storefront.

### Fashion Stable - Fifth between Main and Water

Recurring notices continue to place **W. S. Eddy, V.S., M.D.V.** at the **Fashion Stable, Fifth Street between Main and Water Streets**, through at least 11 June in this batch. No street number is printed. The earlier January transcription as A. J. Eddy remains an initials/transcription discrepancy pending direct recheck; the identities are not silently merged.

### Holman & Randall continuity

A 21 May notice refers to the **undertaking establishment of Holman & Randall**, and an 11 June notice refers to the **Holman & Randall undertaking parlors**. These extend business-name continuity between the 7 May partnership-formation report and the 17 June Courier advertisement at Fifth and Main. The Enterprise notices here do not print a numbered address.

### 18 June council headline - Main Street property owners

The 18 June council page visibly headlines that **offers made by Main Street property owners were turned down** and separately notes street-oiling discussion. The exact terms of those offers were not promoted beyond the readable headline-level context in this review.

## Target-address and Fifth-number coverage

Across these 40 visually inspected pages, no defensible exact **503 Main** or **505 Main** occupant/building-status statement was identified. No exact **102, 104, 106, 108 or 110 Fifth Street** listing, and no other new numbered Fifth Street occupant, was established. These are bounded coverage statements only - not evidence of vacancy, demolition, non-use or nonexistence.

The June 4 Cox location is a positive geographic finding: the raid-period Cox pool hall was **between Seventh and Eighth on Main**, so it was not 503 Main during that episode.

## Resume rule

Resume at **25 June 1915 p1 / chronological Enterprise page 201**. OCR/text may be used for discovery only; the remaining 228 images do not count until the actual page scans are visually inspected.
'''
cap_path = root / 'evidence/source-captures/1915-enterprise-pages-161-200.md'
assert not cap_path.exists()
cap_path.write_text(capture)

sr += f'''\n\n## {source_id} - {source_name}
Type: Primary newspaper scans / exhaustive visual review.  
Dates: 21 May-18 June 1915; five complete issues, 40 page images.  
Repository: `newspapers/oregon-city-enterprise/1915-pages-161-200/`; exact URLs and SHA-256 hashes in `manifest.json`.  
Media: `IMG-{first_media:04d}` through `IMG-{last_media:04d}`.  
Evidence: `{evidence_id}`; detailed review `evidence/source-captures/1915-enterprise-pages-161-200.md`.  
Notes: All 40 scans visually inspected. June 4 p1 directly places Cox's poolhall on Main between Seventh and Eighth, excluding 503 for that raid-period hall; June 4 p3 advances the Main Street improvement/cluster-light chronology; W. S. Eddy/Fashion Stable and Holman & Randall continuity are retained without invented numbers. No exact 503/505 or new numbered Fifth occupant; coverage only.
'''
sr_path.write_text(sr)

sy_path = root / 'database/sources.yml'
sy = sy_path.read_text().rstrip()
sy += f'''\n\n  - id: {source_id}
    name: {source_name}
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1915-05-21/ed-1/
    notes: Forty page PDFs from five complete issues, May 21 through June 18, visually inspected and preserved under newspapers/oregon-city-enterprise/1915-pages-161-200/. Related evidence {evidence_id}; media IMG-{first_media:04d} through IMG-{last_media:04d}. Enterprise pause 200/428 images; next June 25 p1.
'''
sy_path.write_text(sy + '\n')

er += f'''\n\n## {evidence_id} - {evidence_name}
Type: Primary newspaper visual review; source `{source_id}`.  
Record: `evidence/source-captures/1915-enterprise-pages-161-200.md`.  
Claims: All 40 page images from 21 May through 18 June were visually inspected. June 4 p1 directly places Cox's poolhall on Main Street between Seventh and Eighth, superseding the earlier directional theory that 503 was plausible for the raid-period hall; the exact number remains unresolved. June 11 corroborates Cox's Main Street poolhall. June 4 p3 records second reading/unanimous passage of the Main Street improvement ordinance, bid advertising and a cluster-light proposal from T. L. Charman representing Main Street property owners. W. S. Eddy/Fashion Stable continues on Fifth between Main and Water; Holman & Randall business-name continuity appears May 21 and June 11. No exact 503/505 or new numbered Fifth occupant is established; coverage only.  
Confidence: Very High for visually readable location and public-works wording; exact Cox number and target occupancy unresolved.
'''
er_path.write_text(er)

ey_path = root / 'database/evidence.yml'
ey = ey_path.read_text().rstrip()
ey += f'''\n\n  - id: {evidence_id}
    name: {evidence_name}
    type: Primary newspaper visual review of 40 page images
    claims:
      - All 40 page images from May 21 through June 18 were visually inspected.
      - June 4 p1 directly places Cox's poolhall on Main Street between Seventh and Eighth, excluding 503 Main for that raid-period hall while leaving the exact number unresolved.
      - June 11 reports a Ford automobile damaging showcases at Cox's poolhall on Main Street, corroborating continued operation.
      - June 4 p3 records second reading and unanimous passage of the Main Street improvement ordinance, instructions to advertise for bids, and a cluster-light proposal by T. L. Charman representing Main Street property owners.
      - W. S. Eddy remains at Fashion Stable on Fifth between Main and Water, and Holman & Randall business-name continuity appears May 21 and June 11; none of these items prints a target street number.
      - No defensible exact 503/505 occupant or new numbered Fifth Street occupant was identified; this is bounded coverage only, not vacancy or non-use evidence.
    confidence: Very High for visually verified printed location and public-works wording; exact Cox number and target occupancy unresolved.
    related_sources: [{source_id}]
    related_evidence: [E-054]
    related_buildings: [B-001, B-002, B-005]
    repository_file: evidence/source-captures/1915-enterprise-pages-161-200.md
'''
ey_path.write_text(ey + '\n')

mr = mr.rstrip() + f'''\n\n## Morning Enterprise 1915 pages 161-200 - {source_id} / {evidence_id}

All 40 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-161-200/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
'''
for item in items:
    mr += f"| {item['media_id']} | `newspapers/oregon-city-enterprise/1915-pages-161-200/{item['file']}` | {item['date']} / seq{item['sequence']} / printed{item['printed_page']} |\n"
mr_path.write_text(mr + '\n')

# Canonical annual status.
ys_path = root / 'registers/year-status.md'
ys = ys_path.read_text()
match = re.search(r'^\| 1915 \|.*$', ys, re.M)
assert match
newrow = '| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-enterprise-pages-121-160.md`; `evidence/source-captures/1915-enterprise-pages-161-200.md`; `evidence/source-captures/1915-page-review-checklist.md` | Courier **123/123** through year end. Enterprise **200/428 images = 50/107 sheets**, visually reviewed through **18 Jun p8**; next 25 Jun p1, 228 images / 57 sheets remain. Water-ledger/other-source work pending; Courier M01-M04 remain open. |'
ys = ys[:match.start()] + newrow + ys[match.end():]
ys_path.write_text(ys)

# Detailed checklist: add newest checkpoint before older Enterprise checkpoint.
pc_path = root / 'evidence/source-captures/1915-page-review-checklist.md'
pc = pc_path.read_text()
pc = re.sub(r'^Status:.*$', 'Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 200/428 images; other-source work pending**', pc, count=1, flags=re.M)
anchor_match = re.search(r'\n## Latest Enterprise pause checkpoint[^\n]*\n', pc)
assert anchor_match
checkpoint = f'''\n## Latest Enterprise pause checkpoint - chronological page 200 / 18 June 1915

- **200/428 Enterprise page images visually inspected = 50/107 four-page scan sheets.** Five new complete issues, May 21 through June 18. Source `{source_id}`, evidence `{evidence_id}`, media `IMG-{first_media:04d}`-`IMG-{last_media:04d}`.
- Saved originals: `newspapers/oregon-city-enterprise/1915-pages-161-200/`; [detailed visual log](1915-enterprise-pages-161-200.md).
- **Exact pause:** page 200 = June 18 p8. **Next:** page 201 = June 25 p1. Remaining Enterprise: **228 images / 57 sheets**.
- Major correction: June 4 p1 directly locates Cox's raid-period poolhall **between Seventh and Eighth on Main**, excluding 503 for that episode and superseding the prior directional 500-block theory; exact number remains unresolved.
- June 4 p3 advances the Main Street improvement/cluster-light chronology. W. S. Eddy/Fashion Stable continues between Main and Water on Fifth; Holman & Randall continuity appears May 21 and June 11.
- No exact 503/505 or new numbered Fifth occupant identified. Coverage only; no vacancy/non-use inference.
- Courier remains 123/123; M01-M04, water-ledger/other-source review and year closeout remain open. **1915 is not ONLINE COMPLETE.**
'''
pc = pc[:anchor_match.start()] + checkpoint + pc[anchor_match.start():]
pc_path.write_text(pc)

# Research log: insert at top of table.
rl_path = root / 'registers/research-log.md'
rl = rl_path.read_text()
sep = '| --- | --- | --- | --- |\n'
assert sep in rl
row = f'| 2026-08-27 | Visually reviewed Morning Enterprise chronological pages 161-200 (May 21-June 18), preserved all 40 scans | {evidence_id}/{source_id}: June 4 directly places Cox poolhall on Main between Seventh and Eighth, superseding the earlier 503-directional hypothesis for the raid-period hall; June 4 council coverage advances Main Street improvement/cluster-light chronology; Fashion Stable and Holman & Randall continuity retained without invented numbers. | Pause at page 200 / June 18 p8. Resume page 201 / June 25 p1. Enterprise 200/428; 228 images remain; 1915 stays IN PROGRESS. |\n'
rl = rl.replace(sep, sep + row, 1)
rl_path.write_text(rl)

# Repaving chronology: insert June 4 visual step before June 24 contract award.
rp_path = root / 'evidence/source-captures/1915-main-street-repaving.md'
rp = rp_path.read_text()
if f'{source_id} / {evidence_id}' not in rp:
    marker = '\n## 24 June 1915'
    idx = rp.find(marker)
    assert idx >= 0
    sec = f'''\n## 4 June 1915 - Enterprise improvement ordinance and cluster-light proposal

**Morning Enterprise, 4 June 1915, p. 3; visually verified under `{source_id}` / `{evidence_id}`.**

The council report says the ordinance calling for improvement of Main Street was read the second time and passed unanimously, and the recorder was instructed to advertise for bids. The same report says **T. L. Charman, representing Main Street property owners**, presented a proposition for **cluster lights on Main Street**.

This is direct administrative/public-realm evidence. It strengthens the paving and streetscape chronology but does **not** establish demolition, relocation, ownership transfer, or alteration of a 501/503/505 storefront.

'''
    rp = rp[:idx] + sec + rp[idx:]
rp_path.write_text(rp)

# Cox lead: place a prominent supersession note near the top; retain older inference as historical research trail.
cox_path = root / 'evidence/source-captures/1915-1916-cox-pool-hall-lead.md'
cox = cox_path.read_text()
if 'June 4 Enterprise location correction' not in cox:
    intro_marker = '\n## Earlier exact-address lead'
    idx = cox.find(intro_marker)
    assert idx >= 0
    correction = f'''\n## June 4 Enterprise location correction - raid-period hall is NOT 503

**Morning Enterprise, 4 June 1915, p. 1; visually verified under `{source_id}` / `{evidence_id}`.** The raid report directly identifies **Cox's poolhall on Main Street between Seventh and Eighth streets**.

This positive geographic evidence **supersedes the earlier directional inference below** that movement “down Main street” from the Moose rooms made the Fifth-Sixth / 500 block, including 503, plausible for the raid-period Cox hall. Whatever the exact number, a premises between Seventh and Eighth was **not 503 Main**. The exact numbered address remains unresolved.

The same raid/court sequence is independently tied to **Frank D. Cox** by the February 1915 merchant-directory listing and June Courier reporting. This correction therefore does not depend on a surname-only identity merge.

A 11 June *Enterprise* report independently says a Ford struck **Cox's poolhall on Main street**, corroborating continued operation one week later without supplying a number. The 18 June issue continues the Myers/Cox case.

**Handling rule:** retain the older directional discussion below as a superseded research trail only; do not use it prospectively to argue that Cox occupied 503 in June 1915.
'''
    cox = cox[:idx] + correction + cox[idx:]
cox_path.write_text(cox)

# Update the February Cox directory capture with the new segment-level evidence.
fdc_path = root / 'evidence/source-captures/1915-frank-cox-main-street-billiard-directory-visual.md'
fdc = fdc_path.read_text()
if 'June 4 Enterprise segment-level location' not in fdc:
    marker = '\n## Research target\n'
    assert marker in fdc
    sec = f'''\n## June 4 Enterprise segment-level location

The exhaustive *Morning Enterprise* review now adds a stronger location constraint. The **4 June 1915 p1** raid report, visually verified under `{source_id}` / `{evidence_id}`, places **Cox's poolhall on Main Street between Seventh and Eighth streets**. A **11 June** report again places Cox's poolhall on Main Street.

Read with the independent February directory listing naming **Frank D. Cox — Main St** and the June Courier raid/court sequence, this establishes that the raid-period Cox hall was in the Seventh-Eighth segment of Main. It **rules out 503 Main for that episode** while leaving the exact numbered premises unresolved.
'''
    fdc = fdc.replace(marker, sec + marker, 1)
    fdc = fdc.replace('Locate another edition of this merchant directory, a local city directory, advertisement, license/bond record, or council entry that expands **Frank D. Cox — Main St** to a numbered premises.', 'Locate a directory, advertisement, license/bond record, council entry, Sanborn/address key, or other source that converts the now-established **Main Street between Seventh and Eighth** segment into Cox\'s exact numbered premises. Do not reopen 503 for the June 1915 raid-period hall without contrary direct evidence.')
fdc_path.write_text(fdc)

# Holman/Randall continuity.
hol_path = root / 'evidence/E-054-holman-fifth-main-1915-1917.md'
hol = hol_path.read_text()
if 'May-June 1915 Enterprise continuity' not in hol:
    hol += f'''\n\n## May-June 1915 Enterprise continuity

`{source_id}` / `{evidence_id}` visually verifies a **21 May 1915** notice referring to the undertaking establishment of **Holman & Randall** and an **11 June 1915** notice referring to the **Holman & Randall undertaking parlors**. These extend the business-name chronology between the 7 May partnership-formation report and the 17 June Courier Fifth/Main advertisement. The Enterprise notices here do not print `501 Main` or any numbered Fifth Street address; the existing mapping caution remains unchanged.
'''
hol_path.write_text(hol)

# Address register: add Cox segment anchor and extend Fashion Stable chronology.
ar_path = root / 'registers/address-register.md'
ar = ar_path.read_text()
if 'Main Street between Seventh and Eighth (1915 Cox poolhall context)' not in ar:
    table_anchor = '| Main near Seventh (context; unnumbered premises)'
    pos = ar.find(table_anchor)
    assert pos >= 0
    line_end = ar.find('\n', pos)
    new_line = f'| Main Street between Seventh and Eighth (1915 Cox poolhall context) | Unassigned; exact number unresolved | `evidence/source-captures/1915-1916-cox-pool-hall-lead.md` | Cox poolhall / Frank D. Cox context | {evidence_id} | June 4, 1915 Morning Enterprise directly places Cox\'s raid-period poolhall on Main between Seventh and Eighth. This positive location excludes 503 Main for that episode; exact number remains unresolved. |\n'
    ar = ar[:line_end+1] + new_line + ar[line_end+1:]
if f'`{source_id}` / `{evidence_id}` extends W. S. Eddy' not in ar:
    marker = '\n### Fifth Street address-reconstruction goal\n'
    assert marker in ar
    para = f'''\n`{source_id}` / `{evidence_id}` extends W. S. Eddy / Fashion Stable's unnumbered **Fifth Street between Main and Water** location through at least **11 June 1915**. No numbered Fifth address is inferred, and the earlier A. J. / W. S. initials discrepancy remains open pending recheck.\n'''
    ar = ar.replace(marker, para + marker, 1)
ar_path.write_text(ar)

# Reconcile the old partial Enterprise audit with the exhaustive pass now reaching June 18.
epr_path = root / 'evidence/source-captures/1915-enterprise-page-review.md'
epr = epr_path.read_text()
if 'Exhaustive-pass supersession checkpoint - 18 June 1915' not in epr:
    status_line = 'Status: **active / incomplete**\n'
    assert status_line in epr
    note = f'''\n## Exhaustive-pass supersession checkpoint - 18 June 1915

The later exhaustive visual audit now reaches **chronological page 200 / 18 June 1915 p8** (`{source_id}` / `{evidence_id}`), with every retrievable page from 1 January through that point visually inspected and preserved. The selected-page notes below remain useful as historical research trail, but they no longer define coverage for dates through 18 June. The next exhaustive page is **25 June p1 / chronological page 201**.
'''
    epr = epr.replace(status_line, status_line + note, 1)
epr_path.write_text(epr)

print(f'Allocated {source_id}, {evidence_id}, IMG-{first_media:04d}..IMG-{last_media:04d}')
