from pathlib import Path

for p in [
    Path('evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md'),
    Path('evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md'),
]:
    if not p.exists():
        raise SystemExit(f'missing required capture: {p}')

src_md = Path('evidence/source-register.md')
s = src_md.read_text()
if '## S-344 —' not in s:
    s += '''\n\n## S-344 — Oregon City Enterprise, 14 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 14 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-14/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md`  
Related evidence: `E-317`.  
Notes: Page 4 gives same-block Main-between-Fifth-and-Sixth store-building improvement context without an exact number; Larsen & Co. is explicitly at Tenth/Main. No source-explicit target-premises event.

## S-345 — Oregon City Enterprise, 21 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 21 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-21/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`  
Related evidence: `E-318`.  
Notes: Page 1 reports the $75,000 federal-building appropriation proposal and multiple tentative Oregon City sites, but identifies no site or target-address bridge.
'''
src_md.write_text(s)

ev_md = Path('evidence/evidence-register.md')
s = ev_md.read_text()
if '## E-317 —' not in s:
    s += '''\n\n## E-317 — 14 July 1916 Enterprise complete visual review and same-block construction control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 4 lists Mary E. Barlow and J. W. David on Main Street between Fifth and Sixth with improvements to a store building costing $500, but no street number is printed. Larsen & Co. is explicitly at Tenth/Main and A. H. Buckles at Eleventh/Main. No inspected page directly supplies a target-premises event.  
Source: `S-344`.  
Confidence: Very High for visual coverage and printed wording; block-level construction context is not assigned to a target number.

## E-318 — 21 July 1916 Enterprise complete visual review and federal-building status update
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 says prospects for an Oregon City federal building had brightened after inclusion of $75,000 for site purchase and construction and says Postmaster J. J. Cooke had reported on several tentative locations. The article identifies no selected or tentative site by address, intersection, owner, legal description, or building, so it supplies no bridge to 501/503/505/505½/507 Main.  
Source: `S-345`.  
Confidence: Very High for visual coverage and printed federal-building chronology; no target-site inference.
'''
ev_md.write_text(s)

src_y = Path('database/sources.yml')
s = src_y.read_text()
if '  - id: S-344' not in s:
    s += '''\n\n  - id: S-344
    name: "Oregon City Enterprise, 14 July 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-14/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-07-14"
    repository_file: "evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md"
    related_evidence: [E-317]
    notes: "Same-block Main-between-Fifth-and-Sixth store-building improvement control without exact number; no source-explicit target-premises event."
  - id: S-345
    name: "Oregon City Enterprise, 21 July 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-21/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-07-21"
    repository_file: "evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md"
    related_evidence: [E-318]
    notes: "$75,000 federal-building appropriation/site-selection chronology; several tentative locations mentioned but none identified."
'''
src_y.write_text(s)

ev_y = Path('database/evidence.yml')
s = ev_y.read_text()
if '  - id: E-317' not in s:
    s += '''\n\n  - id: E-317
    name: "14 July 1916 Enterprise complete visual review and same-block construction control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 4 lists Mary E. Barlow and J. W. David on Main Street between Fifth and Sixth with improvements to a store building costing $500, without a street number."
      - "Explicit non-target controls place Larsen & Co. at Tenth/Main and A. H. Buckles at Eleventh/Main."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-344]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md"
  - id: E-318
    name: "21 July 1916 Enterprise complete visual review and federal-building status update"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 reports $75,000 for site purchase and federal-building construction and says several tentative Oregon City locations had been evaluated."
      - "No selected or tentative site is identified by address, intersection, owner, legal description, or building."
      - "No evidentiary bridge to 501/503/505/505½/507 Main is supplied."
    confidence: "Very High"
    related_sources: [S-345]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md"
'''
ev_y.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = [
    ('225/426 certified visually reviewed pages through 7 July 1916', '241/426 certified visually reviewed pages through 21 July 1916'),
    ('683 certified visually reviewed; 201 uncertified', '699 certified visually reviewed; 185 uncertified'),
    ('Enterprise: **225/426 certified weekly pages**', 'Enterprise: **241/426 certified weekly pages**'),
    ('Combined certified newspaper coverage: **683/884**', 'Combined certified newspaper coverage: **699/884**'),
    ('**201 Enterprise pages remain uncertified**', '**185 Enterprise pages remain uncertified**'),
    ('next ordinary unreviewed issue is **14 July 1916**', 'next ordinary unreviewed issue is **28 July 1916**'),
]
for old, new in repls:
    if old not in s:
        raise SystemExit(f'checkpoint expected text missing: {old}')
    s = s.replace(old, new)
if '## 12 September continuation — 14 and 21 July certified' not in s:
    s += '''\n\n## 12 September continuation — 14 and 21 July certified

- **14 July 1916:** 8/8 original weekly pages visually inspected (`S-344`, `E-317`). Page 4 supplies same-block store-building improvement context on Main between Fifth and Sixth but no exact number, so it is not assigned to a target premise. Larsen & Co. is explicitly at Tenth/Main; A. H. Buckles at Eleventh/Main.
- **21 July 1916:** 8/8 original weekly pages visually inspected (`S-345`, `E-318`). Page 1 materially advances the federal-building chronology: $75,000 was included for site purchase/construction and several tentative locations had been evaluated, but none is identified. No target-address bridge.
- Enterprise certified coverage is now **241/426**; combined newspaper coverage is **699/884**; **185 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **28 July 1916**.
'''
cp.write_text(s)

ys = Path('registers/year-status.md')
s = ys.read_text()
repls = [
    ('Enterprise **225/426 certified visually reviewed pages through 7 July 1916**', 'Enterprise **241/426 certified visually reviewed pages through 21 July 1916**'),
    ('Combined certified newspaper coverage **683/884**; **201 Enterprise pages remain uncertified**.', 'Combined certified newspaper coverage **699/884**; **185 Enterprise pages remain uncertified**.'),
    ('the next ordinary unreviewed issue is **14 July 1916**.', 'the next ordinary unreviewed issue is **28 July 1916**.'),
]
for old, new in repls:
    if old not in s:
        raise SystemExit(f'year-status expected text missing: {old}')
    s = s.replace(old, new, 1)
marker = '`evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md`'
addition = marker + '; `evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s:
        raise SystemExit('year-status July 7 primary record marker missing')
    s = s.replace(marker, addition, 1)
ys.write_text(s)
