from pathlib import Path

capture_oct06 = Path('evidence/source-captures/1916-enterprise-october06-visual-review-2026-09-12.md')
capture_oct13 = Path('evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md')
for p in (capture_oct06, capture_oct13):
    if p.exists():
        raise SystemExit(f'capture already exists: {p}; refusing duplicate integration')

oct06 = '''# Oregon City Enterprise — 6 October 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 6 October 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-06/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-10-06/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was used only for discovery/navigation and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 4 — real-estate-transfer coverage

Page 4 contains a county real-estate-transfer column. The visually inspected transfer list contains multiple transactions but no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

### Page 5 — recurring Tenth/Main and Morgan's controls

The lower-left advertisement visually identifies **Larsen & Company** at **Corner 10th and Main Sts., Oregon City, Or.** The same page carries a large **Morgan's** grocery advertisement. Neither advertisement assigns a business to the target Fifth–Sixth block.

### Page 7 — Fashion Stable geographic control

The professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This remains a non-target geographic control south of the target Fifth–Sixth block.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeated non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target building/business/person/timeline/open-question fact is manufactured from the no-hit.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
'''

oct13 = '''# Oregon City Enterprise — 13 October 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 13 October 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-13/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-10-13/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. One initially unreadable local rendering of page 5 was re-rendered as a clean JPEG and then visually inspected; OCR/text extraction did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 5 — recurring Tenth/Main and Morgan's controls

The lower-left advertisement visually identifies **Larsen & Company** at **Corner 10th and Main Sts., Oregon City, Or.** The same page carries another large **Morgan's** grocery advertisement. Neither advertisement supplies a target-block assignment.

### Page 7 — Fashion Stable geographic control

The professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the repeated visually verified non-target locator into mid-October.

### Page 8 — real-estate-transfer coverage

Page 8 contains a county real-estate-transfer column. Visual review produced no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeated non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target building/business/person/timeline/open-question fact is manufactured from the no-hit.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
'''

capture_oct06.write_text(oct06)
capture_oct13.write_text(oct13)

src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-356 —' in s or '## S-357 —' in s:
    raise SystemExit('S-356/S-357 already allocated; rebase and reassess IDs before integration')
s += '''\n\n## S-356 — Oregon City Enterprise, 6 October 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 6 October 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-06/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-october06-visual-review-2026-09-12.md`  
Related evidence: `E-329`.  
Notes: Page 4 transfer coverage was visually reviewed; page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.

## S-357 — Oregon City Enterprise, 13 October 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 13 October 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-13/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md`  
Related evidence: `E-330`.  
Notes: Page 5 repeats Larsen & Company at Tenth/Main and Morgan's advertising; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main; page 8 transfer coverage was visually reviewed. No source-explicit target-premises event.
'''
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-329 —' in s or '## E-330 —' in s:
    raise SystemExit('E-329/E-330 already allocated; rebase and reassess IDs before integration')
s += '''\n\n## E-329 — 6 October 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 4 real-estate-transfer coverage supplies no source-explicit target-block transfer. Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. No inspected page directly supplies a target-premises event.  
Source: `S-356`.  
Confidence: Very High for visual coverage and printed geographic controls; no-hit is bounded issue coverage only.

## E-330 — 13 October 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-357`.  
Confidence: Very High for visual coverage and printed geographic controls; no target-address inference.
'''
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-356' in s or '  - id: S-357' in s:
    raise SystemExit('S-356/S-357 already allocated in database')
s += '''\n\n  - id: S-356
    name: "Oregon City Enterprise, 6 October 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-06/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-10-06"
    repository_file: "evidence/source-captures/1916-enterprise-october06-visual-review-2026-09-12.md"
    related_evidence: [E-329]
    notes: "Page 4 transfer coverage; Larsen at Tenth/Main; Morgan's ad; Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
  - id: S-357
    name: "Oregon City Enterprise, 13 October 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-13/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-10-13"
    repository_file: "evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md"
    related_evidence: [E-330]
    notes: "Larsen at Tenth/Main; Morgan's ad; Fashion Stable between Fourth/Fifth on Main; page 8 transfer coverage; no source-explicit target-premises event."
'''
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-329' in s or '  - id: E-330' in s:
    raise SystemExit('E-329/E-330 already allocated in database')
s += '''\n\n  - id: E-329
    name: "6 October 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 4 real-estate-transfer coverage supplies no source-explicit target-block transfer."
      - "Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-356]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-october06-visual-review-2026-09-12.md"
  - id: E-330
    name: "13 October 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-357]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md"
'''
evy.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '321/426 certified visually reviewed pages through 29 September 1916':'337/426 certified visually reviewed pages through 13 October 1916',
    '779 certified visually reviewed; 105 uncertified':'795 certified visually reviewed; 89 uncertified',
    '- Enterprise: **321/426 certified weekly pages**':'- Enterprise: **337/426 certified weekly pages**',
    '- Combined: **779/884 certified**':'- Combined: **795/884 certified**',
    '- Enterprise pages remaining uncertified: **105**':'- Enterprise pages remaining uncertified: **89**',
    'The next ordinary unreviewed Enterprise issue is **6 October 1916**.':'The next ordinary unreviewed Enterprise issue is **20 October 1916**.',
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'checkpoint expected text missing: {old}')
    s = s.replace(old,new,1)
s += '''\n\n## 12 September continuation — 6 and 13 October certified

- **6 October 1916:** 8/8 original weekly pages visually inspected (`S-356`, `E-329`). Page 4 transfer coverage was reviewed; Larsen & Company remains at Tenth/Main; Morgan's advertising recurs; W. S. Eddy remains at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.
- **13 October 1916:** 8/8 original weekly pages visually inspected (`S-357`, `E-330`). Larsen & Company and Morgan's advertising recur on page 5; W. S. Eddy remains at Fashion Stable between Fourth and Fifth on Main; page 8 transfer coverage was reviewed. No target-premises event.
- Enterprise certified coverage is now **337/426**; combined newspaper coverage is **795/884**; **89 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **20 October 1916**.
'''
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
if 'Enterprise **321/426 certified visually reviewed pages through 29 September 1916**' not in s:
    raise SystemExit('year-status baseline text missing')
s = s.replace('Enterprise **321/426 certified visually reviewed pages through 29 September 1916**',
              'Enterprise **337/426 certified visually reviewed pages through 13 October 1916**',1)
s = s.replace('Combined certified newspaper coverage **779/884**; **105 Enterprise pages remain uncertified**.',
              'Combined certified newspaper coverage **795/884**; **89 Enterprise pages remain uncertified**.',1)
s = s.replace('the next ordinary unreviewed issue is **6 October 1916**.',
              'the next ordinary unreviewed issue is **20 October 1916**.',1)
marker='`evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-october06-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s:
        raise SystemExit('year-status September29 marker missing')
    s=s.replace(marker, addition, 1)
ys.write_text(s)
