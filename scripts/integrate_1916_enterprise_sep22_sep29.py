from pathlib import Path

sep22_path = Path('evidence/source-captures/1916-enterprise-september22-visual-review-2026-09-12.md')
sep29_path = Path('evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md')
for p in (sep22_path, sep29_path):
    if p.exists():
        raise SystemExit(f'capture already exists: {p}; refusing duplicate integration')

sep22 = """# Oregon City Enterprise — 22 September 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 22 September 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-22/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-09-22/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was used only for discovery/navigation and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 3 — recurring Tenth/Main control

The lower-left advertisement visually identifies **Larsen & Company** as leading grocers/general merchants at **Corner 10th and Main Sts., Oregon City, Or.** This is an exact non-target Main Street control.

### Page 5 — Seventh Street control

The large **Morgan's** grocery advertisement explicitly locates the business on **Seventh Street — Near Elevator**. This is a non-target location and is retained only as a geographic control.

### Page 7 — Fashion Stable and transfer coverage

The professional directory visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** as established at **Fashion Stable, between Fourth and Fifth on Main Street**. The page also contains real-estate-transfer material; visual review produced no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeat non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target building/business/person/timeline/open-question fact is manufactured from the no-hit.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main, Seventh Street, and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
"""

sep29 = """# Oregon City Enterprise — 29 September 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 29 September 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-29/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-09-29/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was used only for discovery/navigation and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 5 — recurring Tenth/Main control

The lower-left advertisement visually identifies **Larsen & Company** at **Corner 10th and Main Sts., Oregon City, Or.** The same page carries **Morgan's** grocery advertising without a target-block assignment.

### Page 7 — Fashion Stable geographic control

The professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the visually confirmed repetition of the same non-target locator through 1, 8, 15, 22, and 29 September 1916.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeat non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target building/business/person/timeline/open-question fact is manufactured from the no-hit.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are exact non-target controls only.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
"""

sep22_path.write_text(sep22)
sep29_path.write_text(sep29)

src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-354 —' in s or '## S-355 —' in s:
    raise SystemExit('S-354/S-355 already allocated; rebase and reassess IDs before integration')
s += """

## S-354 — Oregon City Enterprise, 22 September 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 22 September 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-22/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-september22-visual-review-2026-09-12.md`  
Related evidence: `E-327`.  
Notes: Page 3 places Larsen & Company at Tenth/Main; page 5 places Morgan's on Seventh Street near the elevator; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main and includes visually reviewed transfer coverage. No source-explicit target-premises event.

## S-355 — Oregon City Enterprise, 29 September 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 29 September 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-29/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md`  
Related evidence: `E-328`.  
Notes: Page 5 repeats Larsen & Company at Tenth/Main; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.
"""
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-327 —' in s or '## E-328 —' in s:
    raise SystemExit('E-327/E-328 already allocated; rebase and reassess IDs before integration')
s += """

## E-327 — 22 September 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 3 places Larsen & Company at Tenth/Main. Page 5 places Morgan's on Seventh Street near the elevator. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street and its transfer material supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-354`.  
Confidence: Very High for visual coverage and printed geographic controls; no-hit is bounded issue coverage only.

## E-328 — 29 September 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. No inspected page directly supplies a target-premises event.  
Source: `S-355`.  
Confidence: Very High for visual coverage and printed geographic controls; no target-address inference.
"""
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-354' in s or '  - id: S-355' in s:
    raise SystemExit('S-354/S-355 already allocated in database')
s += """

  - id: S-354
    name: "Oregon City Enterprise, 22 September 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-22/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-09-22"
    repository_file: "evidence/source-captures/1916-enterprise-september22-visual-review-2026-09-12.md"
    related_evidence: [E-327]
    notes: "Larsen at Tenth/Main; Morgan's on Seventh Street near elevator; Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
  - id: S-355
    name: "Oregon City Enterprise, 29 September 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-29/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-09-29"
    repository_file: "evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md"
    related_evidence: [E-328]
    notes: "Larsen at Tenth/Main and Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
"""
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-327' in s or '  - id: E-328' in s:
    raise SystemExit('E-327/E-328 already allocated in database')
s += """

  - id: E-327
    name: "22 September 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 3 places Larsen & Company at Tenth/Main."
      - "Page 5 places Morgan's on Seventh Street near the elevator."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street and its transfer material supplies no source-explicit target-block transfer."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-354]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-september22-visual-review-2026-09-12.md"
  - id: E-328
    name: "29 September 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-355]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md"
"""
evy.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '305/426 certified visually reviewed pages through 15 September 1916':'321/426 certified visually reviewed pages through 29 September 1916',
    '763 certified visually reviewed; 121 uncertified':'779 certified visually reviewed; 105 uncertified',
    '- Enterprise: **305/426 certified weekly pages**':'- Enterprise: **321/426 certified weekly pages**',
    '- Combined: **763/884 certified**':'- Combined: **779/884 certified**',
    '- Enterprise pages remaining uncertified: **121**':'- Enterprise pages remaining uncertified: **105**',
    'The next ordinary unreviewed Enterprise issue is **22 September 1916**.':'The next ordinary unreviewed Enterprise issue is **6 October 1916**.',
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'checkpoint expected text missing: {old}')
    s = s.replace(old,new,1)
s += """

## 12 September continuation — 22 and 29 September certified

- **22 September 1916:** 8/8 original weekly pages visually inspected (`S-354`, `E-327`). Larsen & Company is at Tenth/Main; Morgan's is on Seventh Street near the elevator; W. S. Eddy is at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.
- **29 September 1916:** 8/8 original weekly pages visually inspected (`S-355`, `E-328`). Larsen & Company remains at Tenth/Main and W. S. Eddy remains at Fashion Stable between Fourth and Fifth on Main. No target-premises event.
- The Fashion Stable locator is now visually confirmed in the **1, 8, 15, 22, and 29 September 1916** Enterprise issues and remains a non-target geographic control only.
- Enterprise certified coverage is now **321/426**; combined newspaper coverage is **779/884**; **105 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **6 October 1916**.
"""
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
if 'Enterprise **305/426 certified visually reviewed pages through 15 September 1916**' not in s:
    raise SystemExit('year-status baseline text missing')
s = s.replace('Enterprise **305/426 certified visually reviewed pages through 15 September 1916**',
              'Enterprise **321/426 certified visually reviewed pages through 29 September 1916**',1)
s = s.replace('Combined certified newspaper coverage **763/884**; **121 Enterprise pages remain uncertified**.',
              'Combined certified newspaper coverage **779/884**; **105 Enterprise pages remain uncertified**.',1)
s = s.replace('the next ordinary unreviewed issue is **22 September 1916**.',
              'the next ordinary unreviewed issue is **6 October 1916**.',1)
marker='`evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-september22-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-september29-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s:
        raise SystemExit('year-status September15 marker missing')
    s=s.replace(marker, addition, 1)
ys.write_text(s)
