from pathlib import Path


def append_once(path, marker, text):
    p=Path(path); s=p.read_text()
    if marker not in s:
        cleaned=text.strip("\n")
        p.write_text(s.rstrip()+"\n\n"+cleaned+"\n")

append_once('evidence/source-register.md','## S-336 — Oregon City Enterprise, 19 May 1916',r'''
## S-336 — Oregon City Enterprise, 19 May 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **19 May 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-19/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-05-19/`.  
Source capture: `evidence/source-captures/1916-enterprise-may19-visual-review-2026-09-12.md`.  
Related evidence: `E-309`.  
Notes: All eight original page scans were visually inspected. No page prints a source-explicit target-premises occupant, owner, tenant, licensee, business-name, sale, transfer, construction, demolition, closure or vacancy event for 501/503/505/505½/507 Main. General Main Street and unrelated Harding/Young material is non-target context only. No-hit is bounded coverage, not vacancy evidence.

## S-337 — Oregon City Enterprise, 26 May 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **26 May 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-26/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-05-26/`.  
Source capture: `evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md`.  
Related evidence: `E-310`.  
Notes: All eight original page scans were visually inspected. Page 8 is a Jones Drug Company forced-out-of-location sale ad stating an imminent move because the landlord wanted more room for his own business; it identifies the old location only as next to Burmeister & Andresen's and prints no street number, so it is not mapped to the target frontage. No source-explicit target-premises event appears. No-hit is bounded coverage, not vacancy evidence.
''')

append_once('evidence/evidence-register.md','## E-309 — 19 May 1916 Enterprise complete visual review',r'''
## E-309 — 19 May 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. No page directly assigns an occupant, owner, tenant, licensee, business name, sale/transfer, construction, demolition, closure or vacancy to 501/503/505/505½/507 Main. General Main Street and unrelated Harding/Young material does not establish a target bridge. This is coverage evidence only, not evidence of absence.  
Source: `S-336`.  
Confidence: Very High for issue-level visual coverage; no target-premises inference from the bounded no-hit.

## E-310 — 26 May 1916 Enterprise complete visual review and Jones Drug relocation control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 8 directly states Jones Drug Company is going to move very soon because the landlord wants more room for his own business and labels the current premises only as “Old location—Next to Burmeister & Andresen’s.” No street number is printed, so the move is retained as non-target city/business context and is not mapped to 501/503/505/505½/507 Main. No page establishes a source-explicit target-premises event. The no-hit is coverage only, not vacancy evidence.  
Source: `S-337`.  
Confidence: Very High for the printed wording and issue-level visual coverage; no target-address inference.
''')

append_once('database/sources.yml','  - id: S-336',r'''
  - id: S-336
    name: "Oregon City Enterprise, 19 May 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-19/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-05-19"
    repository_file: "evidence/source-captures/1916-enterprise-may19-visual-review-2026-09-12.md"
    related_evidence: [E-309]
    notes: "No source-explicit target-premises event; no-hit is bounded coverage only."
  - id: S-337
    name: "Oregon City Enterprise, 26 May 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-26/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-05-26"
    repository_file: "evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md"
    related_evidence: [E-310]
    notes: "Page 8 documents a Jones Drug imminent move but prints no street number; no target-premises bridge."
''')

append_once('database/evidence.yml','  - id: E-309',r'''
  - id: E-309
    name: "19 May 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "No source-explicit target-premises event for 501/503/505/505½/507 Main."
      - "No-hit is bounded coverage only, not vacancy evidence."
    confidence: "Very High"
    related_sources: [S-336]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-may19-visual-review-2026-09-12.md"
  - id: E-310
    name: "26 May 1916 Enterprise complete visual review and Jones Drug relocation control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Jones Drug says it will move very soon because its landlord wants more room for his own business; old location described only as next to Burmeister & Andresen's."
      - "No street number is printed, so the Jones Drug move is not mapped to the target frontage."
      - "No source-explicit target-premises event for 501/503/505/505½/507 Main."
    confidence: "Very High for printed wording; no target-address inference"
    related_sources: [S-337]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md"
''')

p=Path('registers/year-status.md'); s=p.read_text()
s=s.replace('Enterprise **161/426 certified visually reviewed pages through 12 May 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP**. Combined certified newspaper coverage **619/884**; **265 Enterprise pages remain uncertified**. The immediate chronological unresolved item is **12 May 1916 genuine weekly page 8**; after that gap is resolved or formally carried forward, the next ordinary issue is **19 May 1916**.', 'Enterprise **177/426 certified visually reviewed pages through 26 May 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP** after bounded alternate-edition/title recovery attempts. Combined certified newspaper coverage **635/884**; **249 Enterprise pages remain uncertified**. The 12 May true weekly page 8 remains an explicit retrieval gap carried forward; the next ordinary unreviewed issue is **2 June 1916**.')
s=s.replace('`evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md` | 104 issues / 884 pages.', '`evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-may19-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-may26-visual-review-2026-09-12.md` | 104 issues / 884 pages.')
p.write_text(s)

p=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); s=p.read_text()
s=s.replace('**161/426 certified visually reviewed pages through 12 May 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**','**177/426 certified visually reviewed pages through 26 May 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**')
s=s.replace('**619 certified visually reviewed; 265 uncertified**','**635 certified visually reviewed; 249 uncertified**')
s=s.replace('Enterprise: **161/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**','Enterprise: **177/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**')
s=s.replace('Combined: **619/884 certified**','Combined: **635/884 certified**')
s=s.replace('Enterprise pages remaining uncertified: **265**','Enterprise pages remaining uncertified: **249**')
s=s.replace('After that gap is resolved or formally carried forward under the research standard, continue with the next ordinary issue, **19 May 1916**.','Bounded recovery attempts for the 12 May page-8 anomaly did not recover a replacement weekly page, so the gap is explicitly carried forward. The complete **19 May** and **26 May** issues are now **8/8 visually verified**. The next ordinary unreviewed Enterprise issue is **2 June 1916**.')
if '1916-enterprise-may19-visual-review-2026-09-12.md' not in s:
    s=s.replace('- `1916-enterprise-may12-visual-review-2026-09-12.md`','- `1916-enterprise-may12-visual-review-2026-09-12.md`\n- `1916-enterprise-may19-visual-review-2026-09-12.md`\n- `1916-enterprise-may26-visual-review-2026-09-12.md`')
p.write_text(s)
