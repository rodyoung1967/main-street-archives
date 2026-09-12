from pathlib import Path

cap07 = '''# Oregon City Enterprise — 7 April 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **7 April 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

Original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-04-07/`. The fetch manifest records sequences 1–8 as PDFs and 9–14 as 404, so this issue is **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. Screening included 501/503/505/505 1/2/507 Main, established people/business names, pool/billiards/saloon/liquor terms, construction/demolition/fire/remodeling, moves/leases/sales/transfers/property ownership, and Main Street address controls.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or physical-building transition.

Page 8 contains general real-estate transfer notices, including OCR-discoverable Harding-name material, but visual review does not provide a defensible bridge to the target frontage. It is therefore not used to infer target ownership or occupancy.

This is **bounded page-review coverage only**, not evidence of vacancy, non-use, closure, demolition, or absence.

## Resume point

Next ordinary unreviewed *Oregon City Enterprise* issue: **14 April 1916**.
'''

cap14 = '''# Oregon City Enterprise — 14 April 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **14 April 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

Original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-04-14/`. The issue bundle contains **8 pages** and all eight were visually reviewed.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The same annual target screen used for preceding issues was applied page by page.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** target-premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or physical-building transition. General prohibition/saloon/pool-room discussion and general Main Street references do not provide a target-address bridge.

This is **bounded page-review coverage only**, not evidence of vacancy, non-use, closure, demolition, or absence.

## Updated 1916 newspaper coverage

With 7 April and 14 April fully visually certified:

- *Oregon City Courier*: **458/458 visually reviewed**
- *Oregon City Enterprise*: **130/426 visually reviewed through 14 April 1916**
- Combined 1916 newspaper coverage: **588/884 visually reviewed**
- Enterprise pages still uncertified: **296**
- 1916 status: **IN PROGRESS / NOT ONLINE COMPLETE**

## Resume point

Next ordinary unreviewed *Oregon City Enterprise* issue: **21 April 1916**, unless newer parallel work advances the ledger first.
'''

Path('evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md').write_text(cap07)
Path('evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md').write_text(cap14)

def append_once(path, marker, block):
    p=Path(path); t=p.read_text()
    if marker not in t:
        p.write_text(t.rstrip()+"\n\n"+block.strip()+"\n")

append_once('evidence/source-register.md','## S-330 — Oregon City Enterprise, 7 April 1916','''
## S-330 — Oregon City Enterprise, 7 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **7 April 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-07/`.  
Source capture: `evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md`.  
Related evidence: `E-303`.  
Notes: All eight original pages visually inspected; no source-explicit target-premises event. General real-estate/Harding-name material does not supply a defensible target bridge.

## S-331 — Oregon City Enterprise, 14 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **14 April 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-14/`.  
Source capture: `evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md`.  
Related evidence: `E-304`.  
Notes: All eight original pages visually inspected; no source-explicit target-premises event. General prohibition/saloon/pool-room and Main Street material lacks a target-address bridge.
''')

append_once('evidence/evidence-register.md','## E-303 — 7 April 1916 Enterprise complete visual review','''
## E-303 — 7 April 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-330`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- general real-estate/Harding-name material does not provide a defensible target bridge;
- the target no-hit is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.

## E-304 — 14 April 1916 Enterprise complete visual review and cumulative checkpoint
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-331`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- Enterprise coverage advances to **130/426 through 14 April 1916**; combined coverage is **588/884**, with **296 Enterprise pages** uncertified;
- the no-hit result is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.
''')

append_once('database/sources.yml','  - id: S-330','''
  - id: S-330
    name: "Oregon City Enterprise, 7 April 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-07"
    repository_file: "evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md"
    related_evidence: [E-303]
    notes: "All eight original pages visually inspected; no source-explicit target-premises event. General real-estate/Harding-name material lacks a defensible target bridge."

  - id: S-331
    name: "Oregon City Enterprise, 14 April 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-14"
    repository_file: "evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md"
    related_evidence: [E-304]
    notes: "All eight original pages visually inspected; no source-explicit target-premises event. General prohibition/saloon/pool-room and Main Street material lacks a target-address bridge."
''')

append_once('database/evidence.yml','  - id: E-303','''
  - id: E-303
    name: "7 April 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
      - "General real-estate/Harding-name material does not provide a defensible target bridge."
      - "The no-hit result is bounded coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-330]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md"

  - id: E-304
    name: "14 April 1916 Enterprise complete visual review and cumulative checkpoint"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
      - "Enterprise coverage advances to 130/426 through 14 April 1916; combined coverage is 588/884, with 296 Enterprise pages uncertified."
      - "The no-hit result is bounded coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-331]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md"
''')

for path in ['registers/year-status.md','evidence/source-captures/1916-online-audit-checkpoint.md']:
    p=Path(path); t=p.read_text()
    t=t.replace('114/426 visually reviewed through 31 March 1916','130/426 visually reviewed through 14 April 1916')
    t=t.replace('572/884','588/884').replace('312 Enterprise pages','296 Enterprise pages').replace('Enterprise pages remaining: **312**','Enterprise pages remaining: **296**')
    t=t.replace('Enterprise: **114/426**','Enterprise: **130/426**').replace('**572 visually reviewed; 312 pending**','**588 visually reviewed; 296 pending**')
    t=t.replace('next ordinary unreviewed Enterprise issue is **7 April 1916**','next ordinary unreviewed Enterprise issue is **21 April 1916**')
    t=t.replace('next ordinary unreviewed *Oregon City Enterprise* issue is **7 April 1916**','next ordinary unreviewed *Oregon City Enterprise* issue is **21 April 1916**')
    p.write_text(t)
