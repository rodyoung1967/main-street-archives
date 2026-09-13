from pathlib import Path

captures = [
    Path('evidence/source-captures/1916-enterprise-august25-visual-review-2026-09-12.md'),
    Path('evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md'),
]
for p in captures:
    if not p.exists():
        raise SystemExit(f'missing required capture: {p}')

# Guard against parallel ID allocation or duplicate integration.
src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-350 —' in s or '## S-351 —' in s:
    raise SystemExit('S-350/S-351 already allocated; rebase and reassess IDs before integration')
if 'august25-visual-review-2026-09-12.md' in s or 'september01-visual-review-2026-09-12.md' in s:
    raise SystemExit('capture already appears in source register; refusing duplicate integration')
s += '''\n\n## S-350 — Oregon City Enterprise, 25 August 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 25 August 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-25/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-august25-visual-review-2026-09-12.md`  
Related evidence: `E-323`.  
Notes: Page 5 places Larsen & Company at Tenth/Main; page 8 real-estate-transfer coverage was visually reviewed. No source-explicit target-premises event.

## S-351 — Oregon City Enterprise, 1 September 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 1 September 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-01/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md`  
Related evidence: `E-324`.  
Notes: Page 5 places Larsen & Company at Tenth/Main; page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main, explicitly south of the target block; page 8 transfer coverage was visually reviewed. No target-premises event.
'''
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-323 —' in s or '## E-324 —' in s:
    raise SystemExit('E-323/E-324 already allocated; rebase and reassess IDs before integration')
s += '''\n\n## E-323 — 25 August 1916 Enterprise complete visual review and Tenth/Main control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Corner Tenth and Main Streets. Page 8 real-estate-transfer coverage was visually inspected and supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-350`.  
Confidence: Very High for visual coverage and exact non-target location; no-hit is bounded issue coverage only.

## E-324 — 1 September 1916 Enterprise complete visual review and non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main. Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street, explicitly south of the target Fifth–Sixth block. Page 8 transfer coverage supplies no source-explicit target-block transfer. No inspected page directly supplies a target-premises event.  
Source: `S-351`.  
Confidence: Very High for visual coverage and printed geographic controls; no target-address inference.
'''
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-350' in s or '  - id: S-351' in s:
    raise SystemExit('S-350/S-351 already allocated in database; refusing duplicate integration')
s += '''\n\n  - id: S-350
    name: "Oregon City Enterprise, 25 August 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-25/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-08-25"
    repository_file: "evidence/source-captures/1916-enterprise-august25-visual-review-2026-09-12.md"
    related_evidence: [E-323]
    notes: "Exact Tenth/Main Larsen & Company control; page 8 transfer coverage visually reviewed; no source-explicit target-premises event."
  - id: S-351
    name: "Oregon City Enterprise, 1 September 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-01/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-09-01"
    repository_file: "evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md"
    related_evidence: [E-324]
    notes: "Tenth/Main Larsen control and Fashion Stable between Fourth/Fifth on Main; no source-explicit target-premises event."
'''
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-323' in s or '  - id: E-324' in s:
    raise SystemExit('E-323/E-324 already allocated in database; refusing duplicate integration')
s += '''\n\n  - id: E-323
    name: "25 August 1916 Enterprise complete visual review and Tenth/Main control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Corner Tenth and Main Streets."
      - "Page 8 real-estate-transfer coverage was visually inspected."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-350]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-august25-visual-review-2026-09-12.md"
  - id: E-324
    name: "1 September 1916 Enterprise complete visual review and non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main."
      - "Page 7 places W. S. Eddy at Fashion Stable between Fourth and Fifth on Main Street, south of the target block."
      - "Page 8 transfer coverage was visually inspected."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-351]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md"
'''
evy.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '273/426 certified visually reviewed pages through 18 August 1916':'289/426 certified visually reviewed pages through 1 September 1916',
    '731 certified visually reviewed; 153 uncertified':'747 certified visually reviewed; 137 uncertified',
    '- Enterprise: **273/426 certified weekly pages**':'- Enterprise: **289/426 certified weekly pages**',
    '- Combined: **731/884 certified**':'- Combined: **747/884 certified**',
    '- Enterprise pages remaining uncertified: **153**':'- Enterprise pages remaining uncertified: **137**',
    'The next ordinary unreviewed Enterprise issue is **25 August 1916**.':'The next ordinary unreviewed Enterprise issue is **8 September 1916**.',
}
for old,new in repls.items(): s=s.replace(old,new)
if '## 12 September continuation — 25 August and 1 September certified' not in s:
    s += '''\n\n## 12 September continuation — 25 August and 1 September certified

- **25 August 1916:** 8/8 original weekly pages visually inspected (`S-350`, `E-323`). Larsen & Company is explicitly at Tenth/Main; page 8 transfer coverage was visually reviewed; no source-explicit target-premises event.
- **1 September 1916:** 8/8 original weekly pages visually inspected (`S-351`, `E-324`). Larsen & Company is at Tenth/Main; W. S. Eddy is at Fashion Stable between Fourth and Fifth on Main, explicitly south of the target block; no target-premises event.
- Enterprise certified coverage is now **289/426**; combined newspaper coverage is **747/884**; **137 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **8 September 1916**.
'''
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
s=s.replace('Enterprise **273/426 certified visually reviewed pages through 18 August 1916**','Enterprise **289/426 certified visually reviewed pages through 1 September 1916**')
s=s.replace('Combined certified newspaper coverage **731/884**; **153 Enterprise pages remain uncertified**.','Combined certified newspaper coverage **747/884**; **137 Enterprise pages remain uncertified**.')
s=s.replace('the next ordinary unreviewed issue is **25 August 1916**.','the next ordinary unreviewed issue is **8 September 1916**.')
marker='`evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-august25-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-september01-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s: raise SystemExit('year-status August18 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
