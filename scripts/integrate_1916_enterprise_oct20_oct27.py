from pathlib import Path

c20 = Path('evidence/source-captures/1916-enterprise-october20-visual-review-2026-09-13.md')
c27 = Path('evidence/source-captures/1916-enterprise-october27-visual-review-2026-09-13.md')
for p in (c20, c27):
    if p.exists():
        raise SystemExit(f'capture already exists: {p}; refusing duplicate integration')

c20.write_text('''# Oregon City Enterprise — 20 October 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 13 September 2026.  
**Source:** *Oregon City Enterprise*, 20 October 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-20/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-10-20/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. Page 6 was re-rendered cleanly after the first local PNG was unreadable. OCR/text extraction was discovery/navigation only and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 5 — recurring non-target business controls

The lower-left advertisement visually identifies **Larsen & Company** at **Corner 10th and Main Sts., Oregon City, Or.** The same page carries a large **Morgan's** grocery advertisement. Neither supplies a target Fifth–Sixth-block assignment.

### Page 7 — Fashion Stable geographic control

The professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This remains an exact non-target geographic control south of the target block.

### Page 8 — real-estate-transfer coverage

Page 8 contains a county **Real Estate Transfers** column. Visual review found multiple transactions but no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
''')

c27.write_text('''# Oregon City Enterprise — 27 October 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 13 September 2026.  
**Source:** *Oregon City Enterprise*, 27 October 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-27/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-10-27/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. Page 8 was re-rendered cleanly after the first local PNG was unreadable. OCR/text extraction was discovery/navigation only and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 5 — recurring non-target business controls

The lower-left advertisement visually identifies **Larsen & Company** at **Corner 10th and Main Sts., Oregon City, Or.** The same page carries a large **Morgan's** grocery advertisement. Neither supplies a target Fifth–Sixth-block assignment.

### Page 7 — Fashion Stable geographic control

The professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This remains an exact non-target geographic control.

### Page 8 — real-estate-transfer coverage

Page 8 contains a **Real Estate Transfers** column. Visual review found multiple transactions but no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
''')

src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-358 —' in s or '## S-359 —' in s:
    raise SystemExit('S-358/S-359 already allocated')
s += '''\n\n## S-358 — Oregon City Enterprise, 20 October 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 20 October 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-20/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-october20-visual-review-2026-09-13.md`  
Related evidence: `E-331`.  
Notes: Page 5 repeats Larsen & Company at Tenth/Main and Morgan's advertising; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main; page 8 real-estate-transfer coverage was visually reviewed. No source-explicit target-premises event.

## S-359 — Oregon City Enterprise, 27 October 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 27 October 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-27/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-october27-visual-review-2026-09-13.md`  
Related evidence: `E-332`.  
Notes: Page 5 repeats Larsen & Company at Tenth/Main and Morgan's advertising; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main; page 8 real-estate-transfer coverage was visually reviewed. No source-explicit target-premises event.
'''
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-331 —' in s or '## E-332 —' in s:
    raise SystemExit('E-331/E-332 already allocated')
s += '''\n\n## E-331 — 20 October 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-358`.  
Confidence: Very High for visual coverage and printed geographic controls; no-hit is bounded issue coverage only.

## E-332 — 27 October 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-359`.  
Confidence: Very High for visual coverage and printed geographic controls; no target-address inference.
'''
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-358' in s or '  - id: S-359' in s:
    raise SystemExit('S-358/S-359 already allocated in YAML')
s += '''\n\n  - id: S-358
    name: "Oregon City Enterprise, 20 October 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-20/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-10-20"
    repository_file: "evidence/source-captures/1916-enterprise-october20-visual-review-2026-09-13.md"
    related_evidence: [E-331]
    notes: "Larsen at Tenth/Main; Morgan's ad; Fashion Stable between Fourth/Fifth on Main; page 8 transfer coverage; no source-explicit target-premises event."
  - id: S-359
    name: "Oregon City Enterprise, 27 October 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-10-27/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-10-27"
    repository_file: "evidence/source-captures/1916-enterprise-october27-visual-review-2026-09-13.md"
    related_evidence: [E-332]
    notes: "Larsen at Tenth/Main; Morgan's ad; Fashion Stable between Fourth/Fifth on Main; page 8 transfer coverage; no source-explicit target-premises event."
'''
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-331' in s or '  - id: E-332' in s:
    raise SystemExit('E-331/E-332 already allocated in YAML')
s += '''\n\n  - id: E-331
    name: "20 October 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-358]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-october20-visual-review-2026-09-13.md"
  - id: E-332
    name: "27 October 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main and carries Morgan's advertising."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "Page 8 real-estate-transfer coverage supplies no source-explicit target-block transfer."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-359]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-october27-visual-review-2026-09-13.md"
'''
evy.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '337/426 certified visually reviewed pages through 13 October 1916':'353/426 certified visually reviewed pages through 27 October 1916',
    '795 certified visually reviewed; 89 uncertified':'811 certified visually reviewed; 73 uncertified',
    '- Enterprise: **337/426 certified weekly pages**':'- Enterprise: **353/426 certified weekly pages**',
    '- Combined: **795/884 certified**':'- Combined: **811/884 certified**',
    '- Enterprise pages remaining uncertified: **89**':'- Enterprise pages remaining uncertified: **73**',
    'The next ordinary unreviewed Enterprise issue is **20 October 1916**.':'The next ordinary unreviewed Enterprise issue is **3 November 1916**.',
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'checkpoint expected text missing: {old}')
    s=s.replace(old,new,1)
s += '''\n\n## 13 September continuation — 20 and 27 October certified

- **20 October 1916:** 8/8 original weekly pages visually inspected (`S-358`, `E-331`). Larsen & Company remains at Tenth/Main; Morgan's advertising recurs; W. S. Eddy remains at Fashion Stable between Fourth and Fifth on Main; page 8 real-estate-transfer coverage was reviewed. No source-explicit target-premises event.
- **27 October 1916:** 8/8 original weekly pages visually inspected (`S-359`, `E-332`). The same Larsen, Morgan's, and Fashion Stable controls recur; page 8 real-estate-transfer coverage was reviewed. No target-premises event.
- Enterprise certified coverage is now **353/426**; combined newspaper coverage is **811/884**; **73 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **3 November 1916**.
'''
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
if 'Enterprise **337/426 certified visually reviewed pages through 13 October 1916**' not in s:
    raise SystemExit('year-status baseline text missing')
s=s.replace('Enterprise **337/426 certified visually reviewed pages through 13 October 1916**','Enterprise **353/426 certified visually reviewed pages through 27 October 1916**',1)
s=s.replace('Combined certified newspaper coverage **795/884**; **89 Enterprise pages remain uncertified**.','Combined certified newspaper coverage **811/884**; **73 Enterprise pages remain uncertified**.',1)
s=s.replace('the next ordinary unreviewed issue is **20 October 1916**.','the next ordinary unreviewed issue is **3 November 1916**.',1)
marker='`evidence/source-captures/1916-enterprise-october13-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-october20-visual-review-2026-09-13.md`; `evidence/source-captures/1916-enterprise-october27-visual-review-2026-09-13.md`'
if addition not in s:
    if marker not in s:
        raise SystemExit('year-status October13 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
