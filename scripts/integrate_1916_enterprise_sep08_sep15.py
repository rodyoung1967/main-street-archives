from pathlib import Path

capture_sep08 = Path('evidence/source-captures/1916-enterprise-september08-visual-review-2026-09-12.md')
capture_sep15 = Path('evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md')
for p in (capture_sep08, capture_sep15):
    if p.exists():
        raise SystemExit(f'capture already exists: {p}; refusing duplicate integration')

sep08 = '''# Oregon City Enterprise — 8 September 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 8 September 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-08/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-09-08/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was used only for discovery/navigation and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 4 — real-estate-transfer coverage

Page 4 includes a county real-estate-transfer column. The visually inspected column contains multiple transfers but no source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer.

### Page 5 — recurring explicit non-target business control

The lower-left advertisement visually identifies **Larsen & Company** as leading grocers/general merchants at **Corner 10th and Main Sts., Oregon City, Or.** This is an exact non-target Main Street control and does not connect the business to the target Fifth–Sixth block.

### Page 7 — Fashion Stable geographic control

The professional directory visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** as established at **Fashion Stable, between Fourth and Fifth on Main Street**. This independently repeats the same printed locator visually verified in the 1 September issue. The location is south of the target Fifth–Sixth block and is retained only as an exact geographic control.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeat non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. Accordingly no target building/business/person/timeline/open-question fact is manufactured from the no-hit. Canonical source/evidence registers, YAML, year status, and the 1916 checkpoint are the records requiring synchronization.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Tenth/Main and Fourth–Fifth/Main references are retained only as exact non-target controls.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
'''

sep15 = '''# Oregon City Enterprise — 15 September 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 15 September 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-15/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-09-15/`.

## Retrieval and review method

The repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was used only for discovery/navigation and did not substitute for scan review.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 1 — Twelfth Street riverfront control

A front-page article locates a Frank Busch riverfront improvement at **Twelfth Street**. This is an explicit non-target geographic control and does not bear on the Fifth–Sixth target block.

### Page 5 — recurring explicit non-target business control

The lower-left advertisement visually identifies **Larsen & Company** as leading grocers/general merchants at **Corner 10th and Main Sts., Oregon City, Or.** This repeats the exact non-target Main Street control seen in the preceding issues.

### Page 7 — real-estate transfers and Fashion Stable geographic control

Page 7 includes a real-estate-transfer column; the visually inspected transfers do not supply a source-explicit 501/503/505/505½/507 Main transaction or otherwise identifiable target-block transfer. The same page's professional directory again visually prints veterinarian **W. S. Eddy, V.S., M.D.V.** as established at **Fashion Stable, between Fourth and Fifth on Main Street**. The identical locator is now visually confirmed in the 1, 8, and 15 September issues and remains an exact non-target geographic control only.

## Cross-record propagation audit

This issue adds annual visual-coverage evidence and repeat non-target controls only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. Accordingly no target building/business/person/timeline/open-question fact is manufactured from the no-hit. Canonical source/evidence registers, YAML, year status, and the 1916 checkpoint are the records requiring synchronization.

## Evidentiary limits

- No source-explicit target-premises event was found in the complete eight-page issue.
- Twelfth Street, Tenth/Main, and Fourth–Fifth/Main references are retained only as exact non-target controls.
- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.
'''

capture_sep08.write_text(sep08)
capture_sep15.write_text(sep15)

# Guard against parallel ID allocation or duplicate integration.
src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-352 —' in s or '## S-353 —' in s:
    raise SystemExit('S-352/S-353 already allocated; rebase and reassess IDs before integration')
if 'september08-visual-review-2026-09-12.md' in s or 'september15-visual-review-2026-09-12.md' in s:
    raise SystemExit('capture already appears in source register; refusing duplicate integration')
s += '''\n\n## S-352 — Oregon City Enterprise, 8 September 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 8 September 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-08/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-september08-visual-review-2026-09-12.md`  
Related evidence: `E-325`.  
Notes: Page 4 transfer coverage was visually reviewed; page 5 places Larsen & Company at Tenth/Main; page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.

## S-353 — Oregon City Enterprise, 15 September 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 15 September 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-15/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md`  
Related evidence: `E-326`.  
Notes: Page 1 places a riverfront improvement at Twelfth; page 5 repeats Larsen & Company at Tenth/Main; page 7 transfer coverage was visually reviewed and repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.
'''
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-325 —' in s or '## E-326 —' in s:
    raise SystemExit('E-325/E-326 already allocated; rebase and reassess IDs before integration')
s += '''\n\n## E-325 — 8 September 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 4 real-estate-transfer coverage supplies no source-explicit target-block transfer. Page 5 places Larsen & Company at Tenth/Main. Page 7 repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. No inspected page directly supplies a target-premises event.  
Source: `S-352`.  
Confidence: Very High for visual coverage and printed geographic controls; no-hit is bounded issue coverage only.

## E-326 — 15 September 1916 Enterprise complete visual review and repeated non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 places a riverfront improvement at Twelfth Street. Page 5 places Larsen & Company at Tenth/Main. Page 7 transfer coverage supplies no source-explicit target-block transfer and repeats W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street. No inspected page directly supplies a target-premises event.  
Source: `S-353`.  
Confidence: Very High for visual coverage and printed geographic controls; no target-address inference.
'''
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-352' in s or '  - id: S-353' in s:
    raise SystemExit('S-352/S-353 already allocated in database; refusing duplicate integration')
s += '''\n\n  - id: S-352
    name: "Oregon City Enterprise, 8 September 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-08/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-09-08"
    repository_file: "evidence/source-captures/1916-enterprise-september08-visual-review-2026-09-12.md"
    related_evidence: [E-325]
    notes: "Page 4 transfer coverage reviewed; Tenth/Main Larsen control and Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
  - id: S-353
    name: "Oregon City Enterprise, 15 September 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-15/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-09-15"
    repository_file: "evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md"
    related_evidence: [E-326]
    notes: "Twelfth Street control; Tenth/Main Larsen control; page 7 transfer coverage and Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
'''
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-325' in s or '  - id: E-326' in s:
    raise SystemExit('E-325/E-326 already allocated in database; refusing duplicate integration')
s += '''\n\n  - id: E-325
    name: "8 September 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 4 real-estate-transfer coverage was visually inspected and supplies no source-explicit target-block transfer."
      - "Page 5 places Larsen & Company at Tenth/Main."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-352]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-september08-visual-review-2026-09-12.md"
  - id: E-326
    name: "15 September 1916 Enterprise complete visual review and repeated non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 places a Frank Busch riverfront improvement at Twelfth Street."
      - "Page 5 places Larsen & Company at Tenth/Main."
      - "Page 7 real-estate-transfer coverage was visually inspected and places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-353]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md"
'''
evy.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '289/426 certified visually reviewed pages through 1 September 1916':'305/426 certified visually reviewed pages through 15 September 1916',
    '747 certified visually reviewed; 137 uncertified':'763 certified visually reviewed; 121 uncertified',
    '- Enterprise: **289/426 certified weekly pages**':'- Enterprise: **305/426 certified weekly pages**',
    '- Combined: **747/884 certified**':'- Combined: **763/884 certified**',
    '- Enterprise pages remaining uncertified: **137**':'- Enterprise pages remaining uncertified: **121**',
    'The next ordinary unreviewed Enterprise issue is **8 September 1916**.':'The next ordinary unreviewed Enterprise issue is **22 September 1916**.',
}
for old, new in repls.items():
    if old not in s:
        raise SystemExit(f'checkpoint expected text missing: {old}')
    s = s.replace(old, new, 1)
if '## 12 September continuation — 8 and 15 September certified' not in s:
    s += '''\n\n## 12 September continuation — 8 and 15 September certified

- **8 September 1916:** 8/8 original weekly pages visually inspected (`S-352`, `E-325`). Page 4 transfer coverage was reviewed; Larsen & Company is explicitly at Tenth/Main; W. S. Eddy is explicitly at Fashion Stable between Fourth and Fifth on Main. No source-explicit target-premises event.
- **15 September 1916:** 8/8 original weekly pages visually inspected (`S-353`, `E-326`). A page-1 item places a Frank Busch riverfront improvement at Twelfth; Larsen & Company remains at Tenth/Main; page 7 transfer coverage was reviewed and again places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main. No target-premises event.
- The Fashion Stable locator is now independently visually confirmed in the **1, 8, and 15 September 1916** Enterprise issues; it remains south of the target Fifth–Sixth block and is not a target-address assignment.
- Enterprise certified coverage is now **305/426**; combined newspaper coverage is **763/884**; **121 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **22 September 1916**.
'''
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
repls = {
    'Enterprise **289/426 certified visually reviewed pages through 1 September 1916**':'Enterprise **305/426 certified visually reviewed pages through 15 September 1916**',
    'Combined certified newspaper coverage **747/884**; **137 Enterprise pages remain uncertified**.':'Combined certified newspaper coverage **763/884**; **121 Enterprise pages remain uncertified**.',
    'the next ordinary unreviewed issue is **8 September 1916**.':'the next ordinary unreviewed issue is **22 September 1916**.',
}
for old, new in repls.items():
    if old not in s:
        raise SystemExit(f'year-status expected text missing: {old}')
    s = s.replace(old, new, 1)
marker='`evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-september08-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-september15-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s:
        raise SystemExit('year-status September01 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
