from pathlib import Path
import json
import re

root = Path('.')
batch = root / 'newspapers/oregon-city-enterprise/1915-pages-121-160'
mp = batch / 'manifest.json'
manifest = json.loads(mp.read_text())
items = manifest['items']
assert len(items) == 40
assert items[0]['chronological_page'] == 121 and items[0]['date'] == '1915-04-16' and items[0]['sequence'] == 1
assert items[-1]['chronological_page'] == 160 and items[-1]['date'] == '1915-05-14' and items[-1]['sequence'] == 8

sr_path = root / 'evidence/source-register.md'
er_path = root / 'evidence/evidence-register.md'
sr = sr_path.read_text()
er = er_path.read_text()
if 'Morning Enterprise 1915 visual batch, chronological pages 121-160' in sr:
    raise SystemExit('Enterprise pages 121-160 already integrated')

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

readme = f'''# Morning Enterprise scans - 1915 chronological pages 121-160

Source **{source_id}** / evidence **{evidence_id}**. Forty unchanged single-page archive PDFs covering five complete Friday issues from **16 April through 14 May 1915**, eight pages per issue. All 40 scans were rendered and visually inspected on 27 August 2026.

Exact archive URLs and SHA-256 hashes are preserved in `manifest.json` and `sha256.txt`. Media **IMG-{first_media:04d}-IMG-{last_media:04d}** correspond one-to-one to the saved PDFs.

[Detailed visual-review checkpoint](../../../evidence/source-captures/1915-enterprise-pages-121-160.md).

Pause point: **chronological page 160 = 14 May 1915, page 8**. Next Enterprise page: **161 = 21 May 1915, page 1**. Enterprise progress is **160/428 images = 40/107 four-page scan sheets**; 268 images / 67 sheets remain. This batch does not certify 1915 as ONLINE COMPLETE.
'''
(batch / 'README.md').write_text(readme)

capture = f'''# 1915 Morning Enterprise - chronological pages 121-160

Review date: **27 August 2026**. Source **{source_id}**; evidence **{evidence_id}**.  
Status: **VISUALLY VERIFIED - all 40 page images inspected**.

## Scope and pause checkpoint

This batch covers five complete eight-page issues: **16 April, 23 April, 30 April, 7 May and 14 May 1915**. Repository originals are in `newspapers/oregon-city-enterprise/1915-pages-121-160/`; exact URLs and hashes are in the manifest. Media **IMG-{first_media:04d}-IMG-{last_media:04d}**.

**Pause:** page **160 = 14 May 1915 p8**.  
**Next:** page **161 = 21 May 1915 p1**.  
Enterprise progress: **160/428 images = 40/107 four-page scan sheets**; **268 images / 67 sheets remain**.

## Visually verified findings

### 23 April and later - Fashion Stable on Fifth between Main and Water

A professional notice for **W. S. Eddy, V.S., M.D.V.** places him at the **Fashion Stable, Fifth Street, between Main and Water Streets**. The same relative-location notice recurs in this batch, including 14 May p7. This is a useful Fifth Street block anchor, but no street number is printed; no 102/104/106/108/110 Fifth number is inferred.

The earlier pages-1-120 checkpoint transcribed a January notice as **A. J. Eddy**. Because the later scans clearly print **W. S. Eddy**, the initials are preserved as an unresolved transcription/identity discrepancy rather than silently merged. The January scan should be rechecked before any identity correction is made.

### 7 May p5 - Holman & Randall partnership formation

A report headed **“T. P. Randall Plans to Go Into Business”** says former postmaster T. P. Randall and R. L. Holman would become partners in the undertaking establishment then conducted by Holman **on Main Street near Fifth**, and that the firm would be known as **Holman & Randall**. This provides a dated formation milestone before the June advertisements already placing Holman & Randall at Fifth and Main.

The article does **not** print 501 Main or any numbered Fifth address. The premises remain intersection/relative-location evidence only.

### Main Street paving and streetscape sequence

- **16 April p7:** Councilman Cox explains his opposition in the continuing Main Street pavement-material dispute.
- **23 April p5:** the council accepts the property-owner direction toward Worswick asphalt pavement and instructs the city engineer to prepare plans/specifications.
- **30 April p5:** the council passes a resolution for the new Main Street improvement and continues the Worswick specification process.
- **7 May p1:** a Portland Gas & Coke Co. presentation discusses proposed **cluster lighting on Main Street**, a streetscape/public-realm proposal rather than a storefront event.
- **7 May p3:** removal of City Engineer Noble is reported as potentially delaying the Main Street improvement.

These items tighten the pre-construction chronology of the 1915 street project. None establishes demolition, relocation or alteration of a 501/503/505 storefront.

## Target-address and Fifth-number coverage

Across these 40 visually inspected pages, no defensible exact **503 Main** or **505 Main** occupant/building-status statement was identified. No exact **102, 104, 106, 108 or 110 Fifth Street** listing, and no other new numbered Fifth Street occupant, was established. These are bounded coverage statements only - not evidence of vacancy, demolition, non-use or nonexistence.

## Resume rule

Resume at **21 May 1915 p1 / chronological Enterprise page 161**. OCR/text may be used for discovery only; the remaining 268 images do not count until the actual page scans are visually inspected.
'''
cap_path = root / 'evidence/source-captures/1915-enterprise-pages-121-160.md'
assert not cap_path.exists()
cap_path.write_text(capture)

source_name = 'Morning Enterprise 1915 visual batch, chronological pages 121-160'
evidence_name = '1915 Enterprise pages 121-160 visual review'

sr += f'''\n\n## {source_id} - {source_name}
Type: Primary newspaper scans / exhaustive visual review.  
Dates: 16 April-14 May 1915; five complete issues, 40 page images.  
Repository: `newspapers/oregon-city-enterprise/1915-pages-121-160/`; exact URLs and SHA-256 hashes in `manifest.json`.  
Media: `IMG-{first_media:04d}` through `IMG-{last_media:04d}`.  
Evidence: `{evidence_id}`; detailed review `evidence/source-captures/1915-enterprise-pages-121-160.md`.  
Notes: All 40 scans visually inspected. W. S. Eddy/Fashion Stable is placed on Fifth between Main and Water; 7 May reports formation of Holman & Randall at Holman's Main-near-Fifth undertaking establishment; April-May reports extend the Main Street paving/cluster-light chronology. No exact 503/505 or new numbered Fifth occupant; coverage only.
'''
sr_path.write_text(sr)

sy_path = root / 'database/sources.yml'
sy = sy_path.read_text().rstrip()
sy += f'''\n\n  - id: {source_id}
    name: {source_name}
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1915-04-16/ed-1/
    notes: Forty page PDFs from five complete issues, Apr 16 through May 14, visually inspected and preserved under newspapers/oregon-city-enterprise/1915-pages-121-160/. Related evidence {evidence_id}; media IMG-{first_media:04d} through IMG-{last_media:04d}. Enterprise pause 160/428 images; next May 21 p1.
'''
sy_path.write_text(sy + '\n')

er += f'''\n\n## {evidence_id} - {evidence_name}
Type: Primary newspaper visual review; source `{source_id}`.  
Record: `evidence/source-captures/1915-enterprise-pages-121-160.md`.  
Claims: All 40 page images from 16 April through 14 May were visually inspected. W. S. Eddy is repeatedly placed at Fashion Stable on Fifth between Main and Water, without a number. On 7 May p5 T. P. Randall and R. L. Holman are reported forming Holman & Randall at Holman's undertaking establishment on Main near Fifth. April-May reports document successive planning/resolution steps for Main Street paving, a cluster-light proposal and a potential delay after removal of the city engineer. No exact 503/505 or new numbered Fifth occupant is established; coverage only.  
Confidence: Very High for visually readable business-location and public-works wording; exact numbered mapping and target occupancy unresolved.
'''
er_path.write_text(er)

ey_path = root / 'database/evidence.yml'
ey = ey_path.read_text().rstrip()
ey += f'''\n\n  - id: {evidence_id}
    name: {evidence_name}
    type: Primary newspaper visual review of 40 page images
    claims:
      - All 40 page images from April 16 through May 14 were visually inspected.
      - W. S. Eddy is repeatedly listed at Fashion Stable on Fifth Street between Main and Water Streets; no street number is printed.
      - May 7 p5 reports T. P. Randall and R. L. Holman forming Holman & Randall at Holman's undertaking establishment on Main Street near Fifth; no numbered address is printed.
      - April 16, April 23, April 30 and May 7 reports extend the Main Street paving decision chronology; May 7 also records a cluster-light proposal and possible paving delay after removal of the city engineer.
      - No defensible exact 503/505 occupant or new numbered Fifth Street occupant was identified; this is bounded coverage only, not vacancy or non-use evidence.
    confidence: Very High for visually verified printed location and public-works wording; exact numbered mapping and target occupancy unresolved.
    related_sources: [{source_id}]
    related_evidence: [E-054, E-111]
    related_buildings: [B-001, B-002, B-005]
    repository_file: evidence/source-captures/1915-enterprise-pages-121-160.md
'''
ey_path.write_text(ey + '\n')

mr = mr.rstrip() + f'''\n\n## Morning Enterprise 1915 pages 121-160 - {source_id} / {evidence_id}

All 40 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-121-160/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
'''
for item in items:
    mr += f"| {item['media_id']} | `newspapers/oregon-city-enterprise/1915-pages-121-160/{item['file']}` | {item['date']} / seq{item['sequence']} / printed{item['printed_page']} |\n"
mr_path.write_text(mr + '\n')

ys_path = root / 'registers/year-status.md'
ys = ys_path.read_text()
match = re.search(r'^\| 1915 \|.*$', ys, re.M)
assert match
newrow = '| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-enterprise-pages-121-160.md`; `evidence/source-captures/1915-page-review-checklist.md` | Courier **123/123** through year end. Enterprise **160/428 images = 40/107 sheets**, visually reviewed through **14 May p8**; next 21 May p1, 268 images / 67 sheets remain. Water-ledger/other-source work pending; Courier M01-M04 remain open. |'
ys = ys[:match.start()] + newrow + ys[match.end():]
ys_path.write_text(ys)

pc_path = root / 'evidence/source-captures/1915-page-review-checklist.md'
pc = pc_path.read_text()
pc = re.sub(r'^Status:.*$', 'Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 160/428 images; other-source work pending**', pc, count=1, flags=re.M)
anchor = '\n## Latest Enterprise pause checkpoint - chronological page 120 / 9 April 1915\n'
if anchor not in pc:
    anchor = '\n## Latest Enterprise pause checkpoint — chronological page 120 / 9 April 1915\n'
assert anchor in pc
checkpoint = f'''\n## Latest Enterprise pause checkpoint - chronological page 160 / 14 May 1915

- **160/428 Enterprise page images visually inspected = 40/107 four-page scan sheets.** Five new complete issues, Apr. 16 through May 14. Source `{source_id}`, evidence `{evidence_id}`, media `IMG-{first_media:04d}`-`IMG-{last_media:04d}`.
- Saved originals: `newspapers/oregon-city-enterprise/1915-pages-121-160/`; [detailed visual log](1915-enterprise-pages-121-160.md).
- **Exact pause:** page 160 = May 14 p8. **Next:** page 161 = May 21 p1. Remaining Enterprise: **268 images / 67 sheets**.
- Verified additions: W. S. Eddy/Fashion Stable on Fifth between Main and Water; May 7 formation of Holman & Randall at Main near Fifth; additional Main Street paving decision/cluster-light/engineer-delay chronology.
- No exact 503/505 or new numbered Fifth occupant identified. Coverage only; no vacancy/non-use inference.
- Courier remains 123/123; M01-M04, water-ledger/other-source review and year closeout remain open. **1915 is not ONLINE COMPLETE.**
'''
pc = pc.replace(anchor, checkpoint + anchor, 1)
pc_path.write_text(pc)

# Extend the dedicated repaving chronology with the newly certified Enterprise sequence.
rp_path = root / 'evidence/source-captures/1915-main-street-repaving.md'
rp = rp_path.read_text()
insert_before = '\n## 24 June 1915 - contract awarded\n'
if insert_before not in rp:
    insert_before = '\n## 24 June 1915 — contract awarded\n'
assert insert_before in rp
new_sections = f'''\n## 16 April-7 May 1915 - Enterprise decision and streetscape sequence

**Morning Enterprise; visually verified under {source_id} / {evidence_id}.**

- **16 April p7:** Councilman Cox explains his opposition during the pavement-material dispute.
- **23 April p5:** council action follows a well-signed Main Street property-owner petition favoring Worswick pavement and directs preparation of plans/specifications.
- **30 April p5:** the council passes the Main Street improvement resolution and continues the Worswick specification process.
- **7 May p1:** Portland Gas & Coke representatives discuss possible cluster lighting for Main Street; no definite installation is established by this item.
- **7 May p3:** removal of City Engineer Noble is reported as potentially delaying the Main Street improvement.

This sequence strengthens the administrative/public-realm chronology. It does **not** establish demolition, relocation or alteration of a 501/503/505 storefront.
'''
rp = rp.replace(insert_before, new_sections + insert_before, 1)
rp_path.write_text(rp)

# Extend Holman evidence without converting relative location to 501.
h_path = root / 'evidence/E-054-holman-fifth-main-1915-1917.md'
h = h_path.read_text()
h = h.replace('Sources: `S-064`, `S-065`, `S-066`; supplemental batch `S-120` / `E-107`', f'Sources: `S-064`, `S-065`, `S-066`; supplemental batches `S-120` / `E-107` and `{source_id}` / `{evidence_id}`')
section = f'''\n## 7 May 1915 partnership formation

The visually verified *Morning Enterprise* report on 7 May p5 says **T. P. Randall and R. L. Holman would become partners** in the undertaking establishment then conducted by Holman **on Main Street near Fifth**, and that the firm would be known as **Holman & Randall** (`{source_id}` / `{evidence_id}`). This supplies a formation milestone before the 17 June Fifth-and-Main advertisement. It does not print 501 Main or a numbered Fifth address.
'''
h += section
h_path.write_text(h)

hc_path = root / 'evidence/source-captures/501-main-holman-1915-1921.md'
hc = hc_path.read_text()
marker = '\n## 17 June 1915 — Oregon City Courier, page 3\n'
assert marker in hc
may = f'''\n## 7 May 1915 - Morning Enterprise, page 5

Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1915-05-07/ed-1/seq-5.pdf

Visually verified under `{source_id}` / `{evidence_id}`. The report says T. P. Randall and R. L. Holman would form **Holman & Randall** in the undertaking establishment then conducted by Holman **on Main Street near Fifth**. This is a dated partnership/relative-location milestone, not proof of `501 Main`.
'''
hc = hc.replace(marker, may + marker, 1)
hc_path.write_text(hc)

# Add relative Fifth anchor and preserve the Eddy-initials discrepancy.
ar_path = root / 'registers/address-register.md'
ar = ar_path.read_text()
goal = '### Fifth Street address-reconstruction goal'
assert goal in ar
note = f'''\n**1915 relative-location anchor:** `{source_id}` / `{evidence_id}` visually verifies **W. S. Eddy at the Fashion Stable, Fifth Street between Main and Water Streets**, with no number printed. Do not assign 102/104/106/108/110 from this wording. The earlier pages-1-120 record transcribes a January notice as A. J. Eddy; preserve that initials discrepancy pending direct recheck rather than merging the identities.\n\n'''
ar = ar.replace(goal, note + goal, 1)
ar_path.write_text(ar)

# Research log.
rl_path = root / 'registers/research-log.md'
rl = rl_path.read_text()
row_anchor = '| --- | --- | --- | --- |\n'
assert row_anchor in rl
row = f'| 2026-08-27 | Visually reviewed 1915 Enterprise chronological pages 121-160 / five complete issues | {source_id}/{evidence_id}: W. S. Eddy/Fashion Stable on Fifth between Main and Water; May 7 Holman & Randall formation at Main near Fifth; additional paving/cluster-light/engineer-delay chronology. No exact 503/505 or numbered Fifth hit; coverage only. | Paused after page160 = May14 p8. Next page161 = May21 p1. Enterprise160/428;268 images /67 sheets remain. |\n'
rl = rl.replace(row_anchor, row_anchor + row, 1)
rl_path.write_text(rl)

# Timeline narrative: add a concise 1915 spring milestone if not already present.
tl_path = root / 'timeline.md'
tl = tl_path.read_text()
if '## Spring 1915 - Holman & Randall formation and Main Street planning' not in tl:
    anchor = '\n## 1915'
    idx = tl.find(anchor)
    block = f'''\n\n## Spring 1915 - Holman & Randall formation and Main Street planning
Visually reviewed *Morning Enterprise* pages now show Holman at Fifth/Main by January and report on **7 May** that T. P. Randall and R. L. Holman would form **Holman & Randall** in Holman's undertaking establishment **on Main Street near Fifth**. Separate April-May reports document the Worswick paving decision sequence, a Main Street cluster-light proposal and possible delay after removal of the city engineer (`{evidence_id}`). These are relative-location/public-realm facts only; they do not establish 501/503/505 building alteration or exact Holman numbering.
'''
    if idx >= 0:
        tl = tl[:idx] + block + tl[idx:]
    else:
        tl += block
    tl_path.write_text(tl)

print(f'Allocated {source_id}, {evidence_id}, IMG-{first_media:04d}..IMG-{last_media:04d}')
