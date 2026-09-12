from pathlib import Path

cap07 = '''# Oregon City Enterprise — 7 April 1916 complete visual review

Date verified: 11 September 2026
Workstream: ANNUAL-1916
Publication: *Oregon City Enterprise*
LCCN: `sn00063700`
Issue date: **7 April 1916**
Evidence state: **VISUALLY VERIFIED FROM ORIGINAL PAGE PDFs**

## Source preservation

Original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-04-07/` by commit `bcd045cde650eeb682dabd49a8e882c15adc75b2` (`Preserve Enterprise Apr 7 and Apr 14 1916 scans`). The fetch manifest records archive sequences 1–8 as successful PDFs and sequences 9–14 as 404, so this issue is **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. Screening included 501/503/505/505 1/2/507 Main, established people/business names, pool/billiards/saloon/liquor terms, construction/demolition/fire/remodeling, moves/leases/sales/transfers/property ownership, Post Office material, and Main Street address controls.

## New contextual finding — post-office receipts

Page 7 directly reports under **“POSTOFFICE SHOWS GAIN IN BUSINESS”** that Postmaster **J. J. Cooke** reported Oregon City post-office receipts of **$5,095.95** for January–March 1916 versus **$4,715.95** for the same three months in 1915, an increase of **$380.00**.

Classification: **DOCUMENTED / DIRECT** for the printed receipts and Postmaster attribution. The article prints **no street address or site** and therefore does not identify the post office with 501/503/505/507 Main, does not establish a move, and does not alter the separate March 24 federal-building proposal or the later 1918 lease / April 1919 move chronology.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or physical-building transition.

Page 8 contains general real-estate transfer notices, including Harding-name material, but visual review does not provide a defensible legal-description/address bridge to the target frontage. It is therefore not used to infer target ownership or occupancy.

This is **bounded page-review coverage only**, not evidence of vacancy, non-use, closure, demolition, or absence.

## Cross-record propagation audit

The post-office receipt report is propagated narrowly to the Post Office chronology because it documents continued Oregon City postal operations in first-quarter 1916 but supplies no premises address. No target timeline/building/business/person/ownership entry is warranted. Required annual coverage is propagated through the source/evidence registers and annual checkpoint.

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

Original University of Oregon Historic Oregon Newspapers page PDFs are preserved under `newspapers/oregon-city-enterprise/1916/1916-04-14/` by commit `bcd045cde650eeb682dabd49a8e882c15adc75b2` (`Preserve Enterprise Apr 7 and Apr 14 1916 scans`). The fetch manifest records archive sequences 1–8 as successful PDFs and sequences 9–14 as 404, so the issue is **8 pages**.

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/

## Visual review

All **8/8 original page PDFs** were rendered and visually inspected. OCR/text was used only as a discovery aid. The same annual target screen used for preceding issues was applied page by page.

## Target-premises result

No page supplies a source-explicit exact **501, 503, 505, 505 1/2, or 507 Main** target-premises event establishing an occupant, proprietor, business owner, property owner, tenant, licensee, trade-name change, sale, transfer, construction, demolition, closure, vacancy, or physical-building transition. Page 4 contains general saloon/prohibition commentary, and other pages contain general Main Street/legal/business material, but none supplies a target-address or parcel bridge.

This is **bounded page-review coverage only**, not evidence of vacancy, non-use, closure, demolition, or absence.

## Updated 1916 newspaper coverage

With 7 April and 14 April fully visually certified:

- *Oregon City Courier*: **458/458 visually reviewed**
- *Oregon City Enterprise*: **130/426 visually reviewed through 14 April 1916**
- Combined 1916 newspaper coverage: **588/884 visually reviewed**
- Enterprise pages still uncertified: **296**
- 1916 status: **IN PROGRESS / NOT ONLINE COMPLETE**

## Cross-record propagation audit

Because this issue establishes no new target entity fact, no target timeline, building, business, person, open-question, research-lead, crosswalk, or historical-entity update is warranted. Required propagation is limited to issue/source/evidence coverage and annual status.

## Resume point

Next ordinary unreviewed *Oregon City Enterprise* issue: **21 April 1916**, unless newer parallel work advances the ledger first.
'''

Path('evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md').write_text(cap07)
Path('evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md').write_text(cap14)

def append_once(path, marker, block):
    p = Path(path)
    t = p.read_text()
    if marker not in t:
        p.write_text(t.rstrip() + "\n\n" + block.strip('\n') + "\n")

def replace_required(path, old, new):
    p = Path(path)
    t = p.read_text()
    if old not in t:
        raise SystemExit(f"required text not found in {path}: {old[:120]!r}")
    p.write_text(t.replace(old, new))

append_once('evidence/source-register.md', '## S-330 — Oregon City Enterprise, 7 April 1916', '''
## S-330 — Oregon City Enterprise, 7 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **7 April 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-07/`.  
Source capture: `evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md`.  
Related evidence: `E-303`.  
Notes: All eight original pages visually inspected. Page 7 directly reports J. J. Cooke's first-quarter 1916 Oregon City post-office receipts of $5,095.95 versus $4,715.95 in the same 1915 period, but gives no post-office address/site. No source-explicit target-premises event; page-8 real-estate/Harding-name material lacks a defensible target bridge.

## S-331 — Oregon City Enterprise, 14 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **14 April 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-14/`.  
Source capture: `evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md`.  
Related evidence: `E-304`.  
Notes: All eight original pages visually inspected; no source-explicit target-premises event. General saloon/prohibition, Main Street, legal and business material lacks a target-address or parcel bridge.
''')

append_once('evidence/evidence-register.md', '## E-303 — 7 April 1916 Enterprise complete visual review', '''
## E-303 — 7 April 1916 Enterprise complete visual review and post-office receipts
Type: Primary newspaper visual evidence / annual issue-level coverage / postal-operation context.  
Source: `S-330`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- page 7 directly reports Postmaster **J. J. Cooke** and Oregon City post-office receipts of **$5,095.95** for January–March 1916 versus **$4,715.95** for the same months in 1915, a **$380.00** increase;
- the receipt report prints no post-office street address or site and does not establish a move or target-premises relationship;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- general page-8 real-estate/Harding-name material does not provide a defensible target bridge;
- the target no-hit is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage and printed postal receipts; **NO ADDRESS/SITE INFERENCE** for the post office; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.

## E-304 — 14 April 1916 Enterprise complete visual review and cumulative checkpoint
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-331`.  
Claims:
- all **8/8 pages** were visually inspected from original scans;
- no page establishes a 501/503/505/505 1/2/507 Main target-premises event;
- general saloon/prohibition, Main Street, legal and business material does not supply a target-address or parcel bridge;
- Enterprise coverage advances to **130/426 through 14 April 1916**; combined coverage is **588/884**, with **296 Enterprise pages** uncertified;
- the no-hit result is bounded coverage only and not absence evidence.  
Classification: **DOCUMENTED / DIRECT** for page coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High**.
''')

append_once('database/sources.yml', '  - id: S-330', '''
  - id: S-330
    name: "Oregon City Enterprise, 7 April 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-07/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-07"
    repository_file: "evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md"
    related_evidence: [E-303]
    notes: "All eight original pages visually inspected. Page 7 directly reports J. J. Cooke's first-quarter 1916 Oregon City post-office receipts of $5,095.95 versus $4,715.95 for the same 1915 months, but gives no address/site. No source-explicit target-premises event."

  - id: S-331
    name: "Oregon City Enterprise, 14 April 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-04-14/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-14"
    repository_file: "evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md"
    related_evidence: [E-304]
    notes: "All eight original pages visually inspected; no source-explicit target-premises event. General saloon/prohibition, Main Street, legal and business material lacks a target-address or parcel bridge."
''')

append_once('database/evidence.yml', '  - id: E-303', '''
  - id: E-303
    name: "7 April 1916 Enterprise complete visual review and post-office receipts"
    type: "Primary newspaper visual evidence / annual issue-level coverage / postal-operation context"
    claims:
      - "All 8/8 pages were visually inspected from original scans."
      - "Page 7 directly reports Postmaster J. J. Cooke and Oregon City post-office receipts of $5,095.95 for January-March 1916 versus $4,715.95 for the same months in 1915, a $380.00 increase."
      - "The report prints no post-office street address or site and does not establish a move or target-premises relationship."
      - "No page establishes a 501/503/505/505 1/2/507 Main target-premises event."
      - "General page-8 real-estate/Harding-name material does not provide a defensible target bridge."
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
      - "General saloon/prohibition, Main Street, legal and business material does not supply a target-address or parcel bridge."
      - "Enterprise coverage advances to 130/426 through 14 April 1916; combined coverage is 588/884, with 296 Enterprise pages uncertified."
      - "The no-hit result is bounded coverage only and not absence evidence."
    confidence: "Very High"
    related_sources: [S-331]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md"
''')

append_once('evidence/1912-main-street-postoffice-cluster.md', '## 7 April 1916 postal-receipts operating checkpoint', '''
## 7 April 1916 postal-receipts operating checkpoint

A visually verified **7 April 1916 Oregon City Enterprise, page 7** report (`S-330` / `E-303`) states that Postmaster **J. J. Cooke** reported Oregon City post-office receipts of **$5,095.95** for January–March 1916, compared with **$4,715.95** for the same three months in 1915, a **$380.00 increase**.

This is a narrow operating-volume checkpoint only. The article gives **no post-office street address, parcel, building owner, lease, site acquisition, construction, or move statement**. It therefore does not identify the postal premises with 501/503/505/507 Main and does not alter the separate **24 March 1916 federal-building proposal**, **1918 lease/change-of-location**, or **15 April 1919 actual move** evidence.
''')

year = Path('registers/year-status.md')
t = year.read_text()
old = "| 1916 | **IN PROGRESS** | `evidence/source-captures/1916-online-audit-checkpoint.md`; `evidence/source-captures/1916-enterprise-retrieval-gaps-resolved-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-february25-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march03-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md` | 104 issues / 884 pages. Courier **458/458 visually reviewed — complete**. Enterprise **114/426 visually reviewed through 31 March 1916**. Combined certified newspaper coverage **572/884**; **312 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **7 April 1916**. Other online source classes and final manual-callout reconciliation remain pending; no source silence is vacancy evidence. |"
new = "| 1916 | **IN PROGRESS** | `evidence/source-captures/1916-online-audit-checkpoint.md`; `evidence/source-captures/1916-enterprise-retrieval-gaps-resolved-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-february25-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march03-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march10-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march17-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march24-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-march31-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-april07-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md` | 104 issues / 884 pages. Courier **458/458 visually reviewed — complete**. Enterprise **130/426 visually reviewed through 14 April 1916**. Combined certified newspaper coverage **588/884**; **296 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **21 April 1916**. Other online source classes and final manual-callout reconciliation remain pending; no source silence is vacancy evidence. |"
if old not in t:
    raise SystemExit('1916 year-status row changed; refusing blind overwrite')
year.write_text(t.replace(old, new))

cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
t = cp.read_text()
repls = [
    ('**114/426 visually reviewed through 31 March 1916**', '**130/426 visually reviewed through 14 April 1916**'),
    ('**572 visually reviewed; 312 pending**', '**588 visually reviewed; 296 pending**'),
    ('Enterprise: **114/426**', 'Enterprise: **130/426**'),
    ('Combined: **572/884**', 'Combined: **588/884**'),
    ('Enterprise pages remaining: **312**', 'Enterprise pages remaining: **296**'),
    ('issue is **7 April 1916**', 'issue is **21 April 1916**'),
]
for old, new in repls:
    if old not in t:
        raise SystemExit(f'checkpoint text changed; missing {old!r}')
    t = t.replace(old, new)
if '1916-enterprise-april07-visual-review-2026-09-11.md' not in t:
    anchor = '- `1916-enterprise-march31-visual-review-2026-09-11.md`\n'
    if anchor not in t:
        raise SystemExit('checkpoint related-record anchor missing')
    t = t.replace(anchor, anchor + '- `1916-enterprise-april07-visual-review-2026-09-11.md`\n- `1916-enterprise-april14-visual-review-2026-09-11.md`\n')
cp.write_text(t)
