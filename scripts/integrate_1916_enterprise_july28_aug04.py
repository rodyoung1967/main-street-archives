from pathlib import Path

captures = [
    Path('evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md'),
    Path('evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md'),
]
for p in captures:
    if not p.exists():
        raise SystemExit(f'missing capture: {p}')

src_md = Path('evidence/source-register.md')
s = src_md.read_text()
if '## S-346 —' not in s:
    s += '''\n\n## S-346 — Oregon City Enterprise, 28 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 28 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-28/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md`  
Related evidence: `E-319`.  
Notes: Exact Tenth/Main controls appear on pages 1 and 5; no source-explicit event for 501/503/505/505½/507 Main.

## S-347 — Oregon City Enterprise, 4 August 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 4 August 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-04/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md`  
Related evidence: `E-320`.  
Notes: Page 8 reports projected Hawley construction along Main to the alley between Fourth and Fifth, explicitly south of the target Fifth-Sixth block; no target-premises event.
'''
src_md.write_text(s)

ev_md = Path('evidence/evidence-register.md')
s = ev_md.read_text()
if '## E-319 —' not in s:
    s += '''\n\n## E-319 — 28 July 1916 Enterprise complete visual review and Tenth/Main controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 locates an automobile collision at Tenth and Main; page 5 again locates Larsen & Co. at Tenth/Main. No inspected page directly supplies a target-premises event.  
Source: `S-346`.  
Confidence: Very High for visual coverage and exact non-target location controls.

## E-320 — 4 August 1916 Enterprise complete visual review and Hawley Fourth-Fifth construction chronology
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 8 says Hawley's second addition is postponed and projected buildings along Main Street to the alley between Fourth and Fifth would probably begin early the next year. This is a different block from the target Fifth-Sixth frontage and is not assigned to 501/503/505/505½/507 Main.  
Source: `S-347`.  
Confidence: Very High for visual coverage and printed geography; no target-block inference.
'''
ev_md.write_text(s)

src_y = Path('database/sources.yml')
s = src_y.read_text()
if '  - id: S-346' not in s:
    s += '''\n\n  - id: S-346
    name: "Oregon City Enterprise, 28 July 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-28/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-07-28"
    repository_file: "evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md"
    related_evidence: [E-319]
    notes: "Exact Tenth/Main controls; no source-explicit target-premises event."
  - id: S-347
    name: "Oregon City Enterprise, 4 August 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-04/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-08-04"
    repository_file: "evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md"
    related_evidence: [E-320]
    notes: "Hawley projected Main Street construction between Fourth and Fifth; geographically separate from target Fifth-Sixth block."
'''
src_y.write_text(s)

ev_y = Path('database/evidence.yml')
s = ev_y.read_text()
if '  - id: E-319' not in s:
    s += '''\n\n  - id: E-319
    name: "28 July 1916 Enterprise complete visual review and Tenth/Main controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 locates an automobile collision at Tenth/Main and page 5 locates Larsen & Co. at Tenth/Main."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-346]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md"
  - id: E-320
    name: "4 August 1916 Enterprise complete visual review and Hawley Fourth-Fifth construction chronology"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 8 projects Hawley buildings along Main Street to the alley between Fourth and Fifth, probably beginning early the next year."
      - "The printed geography is south of the target Fifth-Sixth block and is not assigned to 501/503/505/505½/507 Main."
    confidence: "Very High"
    related_sources: [S-347]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md"
'''
ev_y.write_text(s)

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = [
    ('241/426 certified visually reviewed pages through 21 July 1916', '257/426 certified visually reviewed pages through 4 August 1916'),
    ('699 certified visually reviewed; 185 uncertified', '715 certified visually reviewed; 169 uncertified'),
    ('- Enterprise: **241/426 certified weekly pages**', '- Enterprise: **257/426 certified weekly pages**'),
    ('- Combined: **699/884 certified**', '- Combined: **715/884 certified**'),
    ('- Enterprise pages remaining uncertified: **185**', '- Enterprise pages remaining uncertified: **169**'),
    ('The next ordinary unreviewed Enterprise issue is **28 July 1916**.', 'The next ordinary unreviewed Enterprise issue is **11 August 1916**.'),
]
for old,new in repls:
    if old not in s: raise SystemExit(f'checkpoint expected text missing: {old}')
    s=s.replace(old,new,1)
if '## 12 September continuation — 28 July and 4 August certified' not in s:
    s += '''\n\n## 12 September continuation — 28 July and 4 August certified

- **28 July 1916:** 8/8 original weekly pages visually inspected (`S-346`, `E-319`). Exact Tenth/Main controls; no source-explicit target-premises event.
- **4 August 1916:** 8/8 original weekly pages visually inspected (`S-347`, `E-320`). Page 8 places projected Hawley Main Street construction between Fourth and Fifth, explicitly outside the target Fifth-Sixth block.
- Enterprise certified coverage is now **257/426**; combined newspaper coverage is **715/884**; **169 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **11 August 1916**.
'''
cp.write_text(s)

ys=Path('registers/year-status.md')
s=ys.read_text()
repls=[
    ('Enterprise **241/426 certified visually reviewed pages through 21 July 1916**', 'Enterprise **257/426 certified visually reviewed pages through 4 August 1916**'),
    ('Combined certified newspaper coverage **699/884**; **185 Enterprise pages remain uncertified**.', 'Combined certified newspaper coverage **715/884**; **169 Enterprise pages remain uncertified**.'),
    ('the next ordinary unreviewed issue is **28 July 1916**.', 'the next ordinary unreviewed issue is **11 August 1916**.'),
]
for old,new in repls:
    if old not in s: raise SystemExit(f'year-status expected text missing: {old}')
    s=s.replace(old,new,1)
marker='`evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s: raise SystemExit('year-status July21 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
