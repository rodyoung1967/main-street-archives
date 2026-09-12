from pathlib import Path


def append_once(path, marker, text):
    p = Path(path)
    s = p.read_text()
    if marker not in s:
        p.write_text(s.rstrip() + "\n\n" + text.strip("\n") + "\n")


def replace_required(path, old, new):
    p = Path(path)
    s = p.read_text()
    if old not in s:
        raise SystemExit(f"missing expected text in {path}: {old}")
    p.write_text(s.replace(old, new, 1))


append_once('evidence/source-register.md', '## S-338 — Oregon City Enterprise, 2 June 1916', r'''
## S-338 — Oregon City Enterprise, 2 June 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **2 June 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-02/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-06-02/`.  
Source capture: `evidence/source-captures/1916-enterprise-june02-visual-review-2026-09-12.md`.  
Related evidence: `E-311`.  
Notes: All eight original page scans were visually inspected. Page 1 says seven firms will move so Burmeister & Andresen, jewelers, can expand, but prints no target street number for that relocation chain. No page establishes a source-explicit 501/503/505/505½/507 Main premises event. No-hit is bounded coverage, not vacancy evidence.

## S-339 — Oregon City Enterprise, 9 June 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **9 June 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-09/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-06-09/`.  
Source capture: `evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md`.  
Related evidence: `E-312`.  
Notes: All eight original page scans were visually inspected. Legal, real-estate-transfer, Main Street and Harding material supplies no exact target-premises bridge, and no page maps the late-May/2 June Jones Drug/Burmeister & Andresen relocation chain to 501/503/505/505½/507 Main. No-hit is bounded coverage, not vacancy evidence.
''')

append_once('evidence/evidence-register.md', '## E-311 — 2 June 1916 Enterprise complete visual review', r'''
## E-311 — 2 June 1916 Enterprise complete visual review and Burmeister & Andresen relocation control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 directly reports that seven firms will move so Burmeister & Andresen, jewelers, can have room to expand; the page does not print a target street number for that expansion/relocation chain, so it is retained as non-target commercial context only. No page directly assigns an occupant, owner, tenant, licensee, business name, sale/transfer, construction, demolition, closure or vacancy to 501/503/505/505½/507 Main. The no-hit is coverage evidence only, not evidence of absence.  
Source: `S-338`.  
Confidence: Very High for issue-level visual coverage and the printed relocation statement; no target-address inference.

## E-312 — 9 June 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. The issue includes legal, real-estate-transfer, construction, Main Street and George A. Harding material, but none supplies a source-explicit target-premises assignment. No inspected page provides a defensible address bridge connecting the late-May/2 June Jones Drug/Burmeister & Andresen relocation sequence to 501/503/505/505½/507 Main. This is coverage evidence only, not evidence of absence.  
Source: `S-339`.  
Confidence: Very High for issue-level visual coverage; no target-premises inference from the bounded no-hit.
''')

append_once('database/sources.yml', '  - id: S-338', r'''
  - id: S-338
    name: "Oregon City Enterprise, 2 June 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-02/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-06-02"
    repository_file: "evidence/source-captures/1916-enterprise-june02-visual-review-2026-09-12.md"
    related_evidence: [E-311]
    notes: "Page 1 reports seven firms will move so Burmeister & Andresen can expand, but gives no target street number; no source-explicit target-premises event."
  - id: S-339
    name: "Oregon City Enterprise, 9 June 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-09/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-06-09"
    repository_file: "evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md"
    related_evidence: [E-312]
    notes: "No source-explicit target-premises event; no address bridge for the Jones Drug/Burmeister & Andresen relocation chain; no-hit is bounded coverage only."
''')

append_once('database/evidence.yml', '  - id: E-311', r'''
  - id: E-311
    name: "2 June 1916 Enterprise complete visual review and Burmeister & Andresen relocation control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 reports seven firms will move so Burmeister & Andresen, jewelers, can expand, but prints no target street number for that relocation chain."
      - "No source-explicit target-premises event for 501/503/505/505½/507 Main."
      - "No-hit is bounded coverage only, not vacancy evidence."
    confidence: "Very High for printed wording and visual coverage; no target-address inference"
    related_sources: [S-338]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-june02-visual-review-2026-09-12.md"
  - id: E-312
    name: "9 June 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Legal, real-estate-transfer, construction, Main Street and Harding material supplies no source-explicit target-premises assignment."
      - "No defensible target-address bridge is printed for the late-May/2 June Jones Drug/Burmeister & Andresen relocation sequence."
      - "No-hit is bounded coverage only, not vacancy evidence."
    confidence: "Very High"
    related_sources: [S-339]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md"
''')

replace_required(
    'registers/year-status.md',
    'Enterprise **177/426 certified visually reviewed pages through 26 May 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP** after bounded alternate-edition/title recovery attempts. Combined certified newspaper coverage **635/884**; **249 Enterprise pages remain uncertified**. The 12 May true weekly page 8 remains an explicit retrieval gap carried forward; the next ordinary unreviewed issue is **2 June 1916**.',
    'Enterprise **193/426 certified visually reviewed pages through 9 June 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP** after bounded alternate-edition/title recovery attempts. Combined certified newspaper coverage **651/884**; **233 Enterprise pages remain uncertified**. The 12 May true weekly page 8 remains an explicit retrieval gap carried forward; the next ordinary unreviewed issue is **16 June 1916**.'
)

p = Path('registers/year-status.md')
s = p.read_text()
old = '`evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md` | 104 issues / 884 pages.'
new = '`evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-june02-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md` | 104 issues / 884 pages.'
if old not in s:
    raise SystemExit('year-status capture anchor changed')
p.write_text(s.replace(old, new, 1))

p = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = p.read_text()
repls = [
    ('**177/426 certified visually reviewed pages through 26 May 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**', '**193/426 certified visually reviewed pages through 9 June 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**'),
    ('**635 certified visually reviewed; 249 uncertified**', '**651 certified visually reviewed; 233 uncertified**'),
    ('Enterprise: **177/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**', 'Enterprise: **193/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**'),
    ('Combined: **635/884 certified**', 'Combined: **651/884 certified**'),
    ('Enterprise pages remaining uncertified: **249**', 'Enterprise pages remaining uncertified: **233**'),
    ('The next ordinary unreviewed Enterprise issue is **2 June 1916**.', 'The complete **2 June** and **9 June** issues are now **8/8 visually verified**. The next ordinary unreviewed Enterprise issue is **16 June 1916**.'),
]
for old, new in repls:
    if old not in s:
        raise SystemExit(f'checkpoint changed; missing: {old}')
    s = s.replace(old, new, 1)
anchor = '- `1916-enterprise-may26-visual-review-2026-09-12.md`\n'
if '- `1916-enterprise-june09-visual-review-2026-09-12.md`' not in s:
    if anchor not in s:
        raise SystemExit('checkpoint capture anchor missing')
    s = s.replace(anchor, anchor + '- `1916-enterprise-june02-visual-review-2026-09-12.md`\n- `1916-enterprise-june09-visual-review-2026-09-12.md`\n', 1)
p.write_text(s)
