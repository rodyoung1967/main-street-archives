from pathlib import Path

cap10 = '''# Oregon City Enterprise — 10 March 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **10 March 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

The original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-03-10/` by commit `fd01de61c17a04c6810f8927527b80658a169a42` (`Preserve Enterprise Mar 10 and Mar 17 1916 scans`). The fetch manifest records successful retrieval of archive sequences 1–10; sequences 11–12 returned 404. The issue is therefore **10 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-10/ed-1/

## Visual review

All **10/10 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The review screened 501/503/505/505 1/2/507 Main; Smith, Young, Brightbill, Harding, Chicago Store, Palace Saloon, Schrader, Post Office, Tolpolar, First National Bank, Raasch/Lamb; pool/billiards, saloon/soft drinks, liquor licensing; and construction, demolition, fire, remodeling, moves, leases, sales, transfers, property ownership and exact Main Street address controls.

## Result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or other physical-building transition. The issue contains general prohibition/liquor-enforcement, legal, business and local reporting, but no inspected item supplies a defensible bridge to the target frontage.

This is **bounded page-review coverage only** and is not evidence of vacancy, non-use, closure, demolition or absence.

## Cross-record propagation audit

Because this issue establishes no new target entity fact, no target timeline, building, business, person, open-question, research-lead, crosswalk or historical YAML entity update is warranted. Required propagation is limited to issue/source/evidence coverage records and annual status.

## Resume point

After this issue, the next ordinary unreviewed *Oregon City Enterprise* issue is **17 March 1916**.
'''

cap17 = '''# Oregon City Enterprise — 17 March 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **17 March 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

The original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-03-17/` by commit `fd01de61c17a04c6810f8927527b80658a169a42` (`Preserve Enterprise Mar 10 and Mar 17 1916 scans`). The fetch manifest records successful retrieval of archive sequences 1–8; sequences 9–12 returned 404. The issue is therefore **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-17/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The same annual target screen used for the preceding issues was applied page by page.

## Result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** target-premises event. Page 8 includes county-expense listings containing an **I. Tolpolar** payment and ordinary real-estate-transfer/county-court material; these items do not print a target Main Street address or establish a target occupancy, ownership, tenancy, licensing, sale, construction, demolition, closure or vacancy event. A First National Bank advertisement and broader prohibition/legal reporting likewise provide context only.

This is **bounded page-review coverage only** and is not evidence of vacancy, non-use, closure, demolition or absence.

## Updated 1916 newspaper coverage

With 10 March (10 pages) and 17 March (8 pages) certified:

- *Oregon City Courier*: **458/458 visually reviewed**
- *Oregon City Enterprise*: **98/426 visually reviewed through 17 March 1916**
- Combined 1916 newspaper coverage: **556/884 visually reviewed**
- Enterprise pages still uncertified: **328**
- 1916 status: **IN PROGRESS / NOT ONLINE COMPLETE**

## Cross-record propagation audit

No new target entity fact is established. The Tolpolar occurrence is county-expense context only and does not change the existing address/business chronology. No target timeline, building, business, person, open-question, research-lead or crosswalk update is warranted beyond the issue/source/evidence and annual-coverage records.

## Resume point

The next ordinary unreviewed *Oregon City Enterprise* issue is **24 March 1916**, unless newer parallel work advances the ledger first.
'''

Path('evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md').write_text(cap10)
Path('evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md').write_text(cap17)

def append_once(path, marker, block):
    p = Path(path)
    t = p.read_text()
    if marker not in t:
        p.write_text(t.rstrip() + '\n\n' + block.strip() + '\n')

append_once('evidence/source-register.md', '## S-326 — Oregon City Enterprise, 10 March 1916', '''
## S-326 — Oregon City Enterprise, 10 March 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 10/10 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **10 March 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-10/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-03-10/`; fetch manifest in the same directory.  
Preservation commit: `fd01de61c17a04c6810f8927527b80658a169a42`.  
Source capture: `evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`.  
Related evidence: `E-299`.  
Notes: All ten original pages visually inspected; no source-explicit 501/503/505/505 1/2/507 Main target-premises event. Bounded coverage only, not absence evidence.

## S-327 — Oregon City Enterprise, 17 March 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **17 March 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-17/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-03-17/`; fetch manifest in the same directory.  
Preservation commit: `fd01de61c17a04c6810f8927527b80658a169a42`.  
Source capture: `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md`.  
Related evidence: `E-300`.  
Notes: All eight original pages visually inspected. Page 8 includes an I. Tolpolar county-expense listing and ordinary county/real-estate material, but no defensible target-premises bridge. Bounded coverage only, not absence evidence.
''')

append_once('evidence/evidence-register.md', '## E-299 — 10 March 1916 Enterprise complete visual review', '''
## E-299 — 10 March 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-326`.  
Claims:
- all **10/10 pages** were visually inspected from original scans;
- no page prints a source-explicit 501/503/505/505 1/2/507 Main occupant, proprietor, owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy or other target-premises transition;
- the no-hit result is issue-level coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.

## E-300 — 17 March 1916 Enterprise complete visual review and cumulative checkpoint
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-327`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- page 8 includes county-expense material naming I. Tolpolar plus real-estate-transfer/county-court material, but no exact target-address bridge;
- no page establishes a 501/503/505/505 1/2/507 Main occupant, proprietor, owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy or other target-premises event;
- Enterprise coverage advances to **98/426 through 17 March 1916**; combined coverage is **556/884**, with **328 Enterprise pages** uncertified;
- the no-hit result is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.
''')

append_once('database/sources.yml', '  - id: S-326', '''
  - id: S-326
    name: "Oregon City Enterprise, 10 March 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-10/ed-1/"
    type: "Primary newspaper page scans; visually verified 10/10 pages"
    date: "1916-03-10"
    repository_file: "evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md"
    related_evidence: [E-299]
    notes: "All ten original pages visually inspected; no source-explicit 501/503/505/505 1/2/507 Main target-premises event. Bounded coverage only, not absence evidence."

  - id: S-327
    name: "Oregon City Enterprise, 17 March 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-03-17/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-03-17"
    repository_file: "evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md"
    related_evidence: [E-300]
    notes: "All eight original pages visually inspected. Page 8 includes an I. Tolpolar county-expense listing and ordinary county/real-estate material, but no defensible target-premises bridge. Bounded coverage only, not absence evidence."
''')

append_once('database/evidence.yml', '  - id: E-299', '''
  - id: E-299
    name: "10 March 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 10/10 pages were visually inspected from original scans."
      - "No page prints a source-explicit 501/503/505/505 1/2/507 Main target-premises event."
      - "The no-hit result is issue-level coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-326]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md"

  - id: E-300
    name: "17 March 1916 Enterprise complete visual review and cumulative checkpoint"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "Page 8 includes county-expense material naming I. Tolpolar plus real-estate-transfer/county-court material, but no exact target-address bridge."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
      - "Enterprise coverage advances to 98/426 through 17 March 1916; combined coverage is 556/884, with 328 Enterprise pages uncertified."
      - "The no-hit result is bounded coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-327]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md"
''')

p = Path('registers/year-status.md')
t = p.read_text()
old = '| 1916 | **IN PROGRESS** | `evidence/source-captures/1916-online-audit-checkpoint.md`; `evidence/source-captures/1916-enterprise-retrieval-gaps-resolved-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-february25-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march03-visual-review-2026-09-11.md` | 104 issues / 884 pages. Courier **458/458 visually reviewed — complete**. Enterprise **80/426 visually reviewed through 3 March 1916**. Combined certified newspaper coverage **538/884**; **346 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **10 March 1916**. Other online source classes and final manual-callout reconciliation remain pending; no source silence is vacancy evidence. |'
new = '| 1916 | **IN PROGRESS** | `evidence/source-captures/1916-online-audit-checkpoint.md`; `evidence/source-captures/1916-enterprise-retrieval-gaps-resolved-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-february25-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march03-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md` | 104 issues / 884 pages. Courier **458/458 visually reviewed — complete**. Enterprise **98/426 visually reviewed through 17 March 1916**. Combined certified newspaper coverage **556/884**; **328 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **24 March 1916**. Other online source classes and final manual-callout reconciliation remain pending; no source silence is vacancy evidence. |'
if old in t:
    t = t.replace(old, new)
p.write_text(t)

p = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
t = p.read_text()
t = t.replace('**80/426 visually reviewed through 3 March 1916**', '**98/426 visually reviewed through 17 March 1916**')
t = t.replace('**538 visually reviewed; 346 pending**', '**556 visually reviewed; 328 pending**')
t = t.replace('Enterprise: **80/426**', 'Enterprise: **98/426**')
t = t.replace('Combined: **538/884**', 'Combined: **556/884**')
t = t.replace('Enterprise pages remaining: **346**', 'Enterprise pages remaining: **328**')
t = t.replace('The next ordinary unreviewed *Oregon City Enterprise* issue is **10 March 1916**.', 'The next ordinary unreviewed *Oregon City Enterprise* issue is **24 March 1916**.')
if '1916-enterprise-march17-visual-review-2026-09-11.md' not in t:
    anchor = '- `1916-enterprise-march03-visual-review-2026-09-11.md`'
    t = t.replace(anchor, anchor + '\n- `1916-enterprise-march10-visual-review-2026-09-11.md`\n- `1916-enterprise-march17-visual-review-2026-09-11.md`')
p.write_text(t)
