from pathlib import Path

cap24 = '''# Oregon City Enterprise — 24 March 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **24 March 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

The original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-03-24/` by commit `7ab8c306d68a7715c18858ed6129c15f48765b6d` (`Preserve Enterprise Mar 24 and Mar 31 1916 scans`). The fetch manifest records successful retrieval of archive sequences 1–8; sequences 9–12 returned 404. The issue is therefore **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-24/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The page-by-page screen included 501/503/505/505 1/2/507 Main, the established people/business names, pool/billiards/saloon/liquor terms, construction/demolition/fire/remodeling, moves/leases/sales/transfers/property ownership, and exact Main Street address controls.

## New contextual finding — proposed Oregon City post office

Page 1 directly reports under the heading **“OREGON CITY'S NEW POST OFFICE, $55,000”** that Treasury Secretary McAdoo considered a **one-story building covering 4,800 square feet** sufficient, at **$55,000**, with **$10,000 additional for the site**; the report says this reduced the amount from **$100,000** carried by the Hawley bill.

Classification: **DOCUMENTED / DIRECT** for the printed federal-planning proposal and amounts. The article prints **no site or street address**, does not identify a parcel or building owner, and does **not** establish that the proposed building was constructed, that a site was acquired, or that the post office moved in 1916. It therefore remains separate from the independently documented 1918 lease/change-of-location evidence and the April 1919 actual move.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or other physical-building transition.

This is **bounded page-review coverage only** for the target frontage and is not evidence of vacancy, non-use, closure, demolition, or absence.

## Cross-record propagation audit

The post-office proposal materially refines the broader Post Office chronology, so it is propagated to `evidence/1912-main-street-postoffice-cluster.md`. It does not justify a target timeline/building/business/person/ownership entry because no site or target-premises bridge is printed. Annual coverage is updated through the issue/source/evidence records.

## Resume point

After this issue, the next ordinary unreviewed *Oregon City Enterprise* issue is **31 March 1916**.
'''

cap31 = '''# Oregon City Enterprise — 31 March 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **31 March 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

The original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-03-31/` by commit `7ab8c306d68a7715c18858ed6129c15f48765b6d` (`Preserve Enterprise Mar 24 and Mar 31 1916 scans`). The fetch manifest records successful retrieval of archive sequences 1–8; sequences 9–12 returned 404. The issue is therefore **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-31/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The same annual target screen used for the preceding issues was applied page by page.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** target-premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or other physical-building transition. General local, legal, business, real-estate and market material does not supply a defensible target bridge.

This is **bounded page-review coverage only** and is not evidence of vacancy, non-use, closure, demolition or absence.

## Updated 1916 newspaper coverage

With 24 March and 31 March now fully visually certified:

- *Oregon City Courier*: **458/458 visually reviewed**
- *Oregon City Enterprise*: **114/426 visually reviewed through 31 March 1916**
- Combined 1916 newspaper coverage: **572/884 visually reviewed**
- Enterprise pages still uncertified: **312**
- 1916 status: **IN PROGRESS / NOT ONLINE COMPLETE**

## Cross-record propagation audit

Because this issue establishes no new target entity fact, no target timeline, building, business, person, open-question, research-lead, crosswalk or historical entity update is warranted. Required propagation is limited to issue/source/evidence coverage and annual status.

## Resume point

The next ordinary unreviewed *Oregon City Enterprise* issue is **7 April 1916**, unless newer parallel work advances the ledger first.
'''

Path('evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md').write_text(cap24)
Path('evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md').write_text(cap31)

def append_once(path, marker, block):
    p=Path(path); t=p.read_text()
    if marker not in t:
        p.write_text(t.rstrip()+"\n\n"+block.strip('\n')+"\n")

append_once('evidence/source-register.md','## S-328 — Oregon City Enterprise, 24 March 1916','''
## S-328 — Oregon City Enterprise, 24 March 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **24 March 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-24/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-03-24/`; fetch manifest in the same directory.  
Preservation commit: `7ab8c306d68a7715c18858ed6129c15f48765b6d`.  
Source capture: `evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md`.  
Related evidence: `E-301`.  
Notes: All eight original pages visually inspected. Page 1 directly reports the federal $55,000 one-story/4,800-square-foot Oregon City post-office proposal plus $10,000 for a site, without printing a site/address or proving construction or relocation. No target-premises event.

## S-329 — Oregon City Enterprise, 31 March 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **31 March 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-31/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-03-31/`; fetch manifest in the same directory.  
Preservation commit: `7ab8c306d68a7715c18858ed6129c15f48765b6d`.  
Source capture: `evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md`.  
Related evidence: `E-302`.  
Notes: All eight original pages visually inspected; no source-explicit 501/503/505/505 1/2/507 Main target-premises event. Bounded coverage only, not absence evidence.
''')

append_once('evidence/evidence-register.md','## E-301 — 24 March 1916 Enterprise complete visual review','''
## E-301 — 24 March 1916 Enterprise complete visual review and post-office proposal
Type: Primary newspaper visual evidence / annual issue-level coverage / federal-planning context.  
Source: `S-328`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- page 1 directly reports a proposed Oregon City post-office building: one story, 4,800 square feet, $55,000 construction estimate plus $10,000 for a site, reduced from the $100,000 Hawley bill amount;
- the article gives no site or street address and does not prove site acquisition, construction, occupancy or relocation;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- the target no-hit is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for the proposal wording and issue coverage; **NO SITE/MOVE/CONSTRUCTION INFERENCE**; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High** for the scan-visible proposal and page coverage.

## E-302 — 31 March 1916 Enterprise complete visual review and cumulative checkpoint
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-329`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- Enterprise coverage advances to **114/426 through 31 March 1916**; combined coverage is **572/884**, with **312 Enterprise pages** uncertified;
- the no-hit result is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.
''')

append_once('database/sources.yml','  - id: S-328','''
  - id: S-328
    name: "Oregon City Enterprise, 24 March 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-24/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-03-24"
    repository_file: "evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md"
    related_evidence: [E-301]
    notes: "All eight original pages visually inspected. Page 1 directly reports a proposed one-story 4,800-square-foot Oregon City post office at $55,000 plus $10,000 for a site; no site/address or proof of construction/move. No target-premises event."

  - id: S-329
    name: "Oregon City Enterprise, 31 March 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-31/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-03-31"
    repository_file: "evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md"
    related_evidence: [E-302]
    notes: "All eight original pages visually inspected; no source-explicit 501/503/505/505 1/2/507 Main target-premises event. Bounded coverage only, not absence evidence."
''')

append_once('database/evidence.yml','  - id: E-301','''
  - id: E-301
    name: "24 March 1916 Enterprise complete visual review and post-office proposal"
    type: "Primary newspaper visual evidence / annual issue-level coverage / federal-planning context"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "Page 1 directly reports a proposed Oregon City post-office building: one story, 4,800 square feet, $55,000 plus $10,000 for a site, reduced from the $100,000 Hawley bill amount."
      - "The article gives no site or street address and does not prove site acquisition, construction, occupancy or relocation."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
    confidence: "Very High for scan-visible wording and page coverage"
    related_sources: [S-328]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md"

  - id: E-302
    name: "31 March 1916 Enterprise complete visual review and cumulative checkpoint"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
      - "Enterprise coverage advances to 114/426 through 31 March 1916; combined coverage is 572/884, with 312 Enterprise pages uncertified."
      - "The no-hit result is bounded coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-329]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md"
''')

p=Path('registers/year-status.md'); t=p.read_text()
old='Enterprise **98/426 visually reviewed through 17 March 1916**. Combined certified newspaper coverage **556/884**; **328 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **24 March 1916**.'
new='Enterprise **114/426 visually reviewed through 31 March 1916**. Combined certified newspaper coverage **572/884**; **312 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **7 April 1916**.'
if old not in t: raise SystemExit('year-status anchor not found')
t=t.replace(old,new)
rowold='`evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md` |'
rownew='`evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md` |'
if rowold in t: t=t.replace(rowold,rownew)
p.write_text(t)

p=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); t=p.read_text()
t=t.replace('**98/426 visually reviewed through 17 March 1916**','**114/426 visually reviewed through 31 March 1916**')
t=t.replace('**556 visually reviewed; 328 pending**','**572 visually reviewed; 312 pending**')
t=t.replace('Enterprise: **98/426**','Enterprise: **114/426**')
t=t.replace('Combined: **556/884**','Combined: **572/884**')
t=t.replace('Enterprise pages remaining: **328**','Enterprise pages remaining: **312**')
t=t.replace('The next ordinary unreviewed *Oregon City Enterprise* issue is **24 March 1916**.','The next ordinary unreviewed *Oregon City Enterprise* issue is **7 April 1916**.')
anchor='- `1916-enterprise-march17-visual-review-2026-09-11.md`'
if '1916-enterprise-march31-visual-review-2026-09-11.md' not in t and anchor in t:
    t=t.replace(anchor,anchor+'\n- `1916-enterprise-march24-visual-review-2026-09-11.md`\n- `1916-enterprise-march31-visual-review-2026-09-11.md`')
p.write_text(t)

p=Path('evidence/1912-main-street-postoffice-cluster.md'); t=p.read_text()
marker='## 24 March 1916 federal post-office planning proposal'
if marker not in t:
    insert='''\n## 24 March 1916 federal post-office planning proposal\n\nA visually verified **24 March 1916 Oregon City Enterprise, page 1** report (`S-328` / `E-301`) adds an intermediate federal-planning checkpoint between the earlier circa-1912 Post Office location evidence and the later 1918–1919 location change. Under the heading **“OREGON CITY'S NEW POST OFFICE, $55,000,”** the article reports that Treasury Secretary McAdoo considered a **one-story, 4,800-square-foot** building sufficient at **$55,000**, with **$10,000 additional for the site**, reducing the amount from **$100,000** carried in the Hawley bill.\n\nThis is **planning/appropriation context only**. The article prints no site, street address, legal description, owner, acquisition, construction-start, completion, occupancy or move date. It therefore does **not** identify either the circa-1912 Post Office bay or the later post-1918 quarters, and it does not prove that the proposed federal building was ever constructed as described. Keep it separate from the **1918 ten-year lease/change-of-location evidence** and the **15 April 1919 actual move** already documented below.\n'''
    anchor2='## Chronology correction — the 1922 Post Office was a later location'
    if anchor2 not in t: raise SystemExit('post office cluster anchor not found')
    t=t.replace(anchor2,insert+'\n'+anchor2)
p.write_text(t)
