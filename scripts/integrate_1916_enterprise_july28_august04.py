from pathlib import Path
import re

captures = [
    Path('evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md'),
    Path('evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md'),
]
for p in captures:
    if not p.exists():
        raise SystemExit(f'missing required capture: {p}')

# Source register: refresh S-345 so Portland House context is not lost, then append S-346/S-347.
p = Path('evidence/source-register.md')
s = p.read_text()
s345 = '''## S-345 — Oregon City Enterprise, 21 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 21 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-21/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`  
Related evidence: `E-318`.  
Notes: Page 1 reports the $75,000 federal-building appropriation proposal and several tentative Oregon City sites but identifies none. Page 5 identifies Minnie L. Foster as owner of the recently rebuilt Portland House at Main/Fifth and Frank and Mark Beck as three-year leaseholders from 1 June 1916; no numbered target-address bridge is printed.
'''
if '## S-345 —' in s:
    s = re.sub(r'## S-345 —.*?(?=\n## S-|\Z)', s345.rstrip(), s, count=1, flags=re.S)
else:
    s += '\n\n' + s345
if '## S-346 —' not in s:
    s += '''\n\n## S-346 — Oregon City Enterprise, 28 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 28 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-28/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md`  
Related evidence: `E-319`.  
Notes: Exact Tenth/Main collision and Larsen & Co. controls; no source-explicit target-premises event.

## S-347 — Oregon City Enterprise, 4 August 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 4 August 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-04/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md`  
Related evidence: `E-320`.  
Notes: Page 8 projects Hawley construction along Main to the alley between Fourth and Fifth, explicitly south of the Fifth–Sixth target block; no source-explicit target-premises event.
'''
p.write_text(s)

# Evidence register: refresh E-318 and append E-319/E-320.
p = Path('evidence/evidence-register.md')
s = p.read_text()
e318 = '''## E-318 — 21 July 1916 Enterprise complete visual review, federal-building update, and Portland House relationships
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 says $75,000 had been included for site purchase and federal-building construction and that several tentative Oregon City locations had been evaluated, but identifies none. Page 5 identifies Minnie L. Foster as owner of the recently rebuilt Portland House at Main/Fifth and Frank and Mark Beck as three-year leaseholders from 1 June 1916; they sought $300 damages over alleged incomplete lease-required changes/improvements. Neither item supplies a numbered bridge to 501/503/505/505½/507 Main.  
Source: `S-345`.  
Confidence: Very High for visual coverage and printed chronology/relationships; no target-site or target-address inference.
'''
if '## E-318 —' in s:
    s = re.sub(r'## E-318 —.*?(?=\n## E-|\Z)', e318.rstrip(), s, count=1, flags=re.S)
else:
    s += '\n\n' + e318
if '## E-319 —' not in s:
    s += '''\n\n## E-319 — 28 July 1916 Enterprise complete visual review and non-target Main Street controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 reports an automobile collision at Tenth/Main and page 5 again places Larsen & Co. at Tenth/Main. Both are exact non-target controls. No inspected page directly supplies a target-premises event.  
Source: `S-346`.  
Confidence: Very High for visual coverage and printed non-target locations.

## E-320 — 4 August 1916 Enterprise complete visual review and Hawley south-block construction chronology
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 8 says erection of Hawley buildings along Main Street to the alley between Fourth and Fifth would probably begin early the next year. This is physical-development chronology south of Fifth Street, not a Fifth–Sixth target-block event. Page 5 again places Larsen & Co. at Tenth/Main. No inspected page directly supplies a target-premises event.  
Source: `S-347`.  
Confidence: Very High for visual coverage and printed block limits; no target-address inference.
'''
p.write_text(s)

# YAML source index: update S-345 note and append S-346/S-347.
p = Path('database/sources.yml')
s = p.read_text()
s = s.replace('notes: "$75,000 federal-building appropriation/site-selection chronology; several tentative locations mentioned but none identified."', 'notes: "$75,000 federal-building appropriation/site-selection chronology with no identified site; Portland House at Main/Fifth recently rebuilt, owned by Minnie L. Foster and leased to Frank and Mark Beck from 1 June 1916, without a numbered target-address bridge."')
if '  - id: S-346' not in s:
    s += '''\n\n  - id: S-346
    name: "Oregon City Enterprise, 28 July 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-28/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-07-28"
    repository_file: "evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md"
    related_evidence: [E-319]
    notes: "Exact Tenth/Main collision and Larsen & Co. controls; no source-explicit target-premises event."
  - id: S-347
    name: "Oregon City Enterprise, 4 August 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-04/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-08-04"
    repository_file: "evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md"
    related_evidence: [E-320]
    notes: "Hawley projected Main Street construction between Fourth and Fifth is explicitly south of the target block; no source-explicit target-premises event."
'''
p.write_text(s)

# YAML evidence index: replace E-318 block fields conservatively and append E-319/E-320.
p = Path('database/evidence.yml')
s = p.read_text()
s = s.replace('name: "21 July 1916 Enterprise complete visual review and federal-building status update"', 'name: "21 July 1916 Enterprise complete visual review, federal-building update, and Portland House relationships"')
needle = '      - "No evidentiary bridge to 501/503/505/505½/507 Main is supplied."'
addition = '      - "Page 5 identifies Minnie L. Foster as owner of the recently rebuilt Portland House at Main/Fifth and Frank and Mark Beck as three-year leaseholders from 1 June 1916; they sought $300 damages over alleged incomplete lease-required changes/improvements."\n      - "Neither the federal-building article nor the Portland House report supplies a numbered bridge to 501/503/505/505½/507 Main."'
if needle in s:
    s = s.replace(needle, addition, 1)
if '  - id: E-319' not in s:
    s += '''\n\n  - id: E-319
    name: "28 July 1916 Enterprise complete visual review and non-target Main Street controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 reports an automobile collision at Tenth/Main and page 5 again places Larsen & Co. at Tenth/Main."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-346]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md"
  - id: E-320
    name: "4 August 1916 Enterprise complete visual review and Hawley south-block construction chronology"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 8 says erection of Hawley buildings along Main Street to the alley between Fourth and Fifth would probably begin early the next year."
      - "The described construction is south of Fifth Street and is not a Fifth–Sixth target-block event."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-347]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md"
'''
p.write_text(s)

# Coverage checkpoint: only advance from the verified July-21 state.
p = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = p.read_text()
for old, new in [
    ('241/426 certified visually reviewed pages through 21 July 1916', '257/426 certified visually reviewed pages through 4 August 1916'),
    ('699 certified visually reviewed; 185 uncertified', '715 certified visually reviewed; 169 uncertified'),
    ('Enterprise: **241/426 certified weekly pages**', 'Enterprise: **257/426 certified weekly pages**'),
    ('Combined certified newspaper coverage: **699/884**', 'Combined certified newspaper coverage: **715/884**'),
    ('**185 Enterprise pages remain uncertified**', '**169 Enterprise pages remain uncertified**'),
    ('next ordinary unreviewed issue is **28 July 1916**', 'next ordinary unreviewed issue is **11 August 1916**'),
]:
    if old in s:
        s = s.replace(old, new)
if '## 12 September continuation — 28 July and 4 August certified' not in s:
    s += '''\n\n## 12 September continuation — 28 July and 4 August certified

- **28 July 1916:** 8/8 original weekly pages visually inspected (`S-346`, `E-319`). Tenth/Main collision and Larsen & Co. references are exact non-target controls; no target-premises event.
- **4 August 1916:** 8/8 original weekly pages visually inspected (`S-347`, `E-320`). Page 8 projects Hawley construction along Main Street to the alley between Fourth and Fifth, explicitly south of the Fifth–Sixth target block; no target-premises event.
- Enterprise certified coverage is now **257/426**; combined newspaper coverage is **715/884**; **169 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **11 August 1916**.
'''
p.write_text(s)

# Year status: advance the 1916 row from the same certified July-21 state.
p = Path('registers/year-status.md')
s = p.read_text()
for old, new in [
    ('Enterprise **241/426 certified visually reviewed pages through 21 July 1916**', 'Enterprise **257/426 certified visually reviewed pages through 4 August 1916**'),
    ('Combined certified newspaper coverage **699/884**; **185 Enterprise pages remain uncertified**.', 'Combined certified newspaper coverage **715/884**; **169 Enterprise pages remain uncertified**.'),
    ('the next ordinary unreviewed issue is **28 July 1916**.', 'the next ordinary unreviewed issue is **11 August 1916**.'),
]:
    if old in s:
        s = s.replace(old, new, 1)
marker = '`evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`'
addition = marker + '; `evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md`'
if addition not in s and marker in s:
    s = s.replace(marker, addition, 1)
p.write_text(s)
