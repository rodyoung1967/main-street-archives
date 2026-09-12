from pathlib import Path


def write_new(path: str, text: str) -> None:
    p = Path(path)
    if p.exists():
        raise SystemExit(f"refusing to overwrite existing {path}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


june30 = """# Oregon City Enterprise — 30 June 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 30 June 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-30/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-06-30/`.

## Retrieval and review method

Sequences 1–14 were tested by the repository fetch workflow. Sequences **1–8** returned valid original page PDFs and later tested sequences did not add issue pages; the fetch manifest is preserved beside the scans. The archive issue navigator independently reports **8 pages**. Every one of the eight delivered PDFs was rendered and the resulting faithful page image was individually visually inspected. OCR/text extraction was used only after visual inspection as a discovery/navigation aid.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 2 — Water/Fifth business-location control

A DeNike & Martin advertisement identifies the firm as successors to O. G. Thomas and prints its **new location as the corner of Water and Fifth Streets, Oregon City**. This is useful Fifth Street spatial/business context, but it is on Water Street and is **not** evidence for the target Main Street frontage.

### Page 8 — H. P. Brightbill Main Street business control

A short court item identifies **H. P. Brightbill as a Main Street grocer** and reports his suit against J. E. and Alice Morley to collect an alleged $2.65 bill. The item prints **no street number**. It therefore supports only a Main Street business association for Brightbill on this date and must not be assigned to 501/503/505/505½/507 without an independent address bridge.

Page 8 also carries Jones Drug Co. advertising and real-estate-transfer material, but nothing visually inspected provides a defensible target-address bridge.

## Propagation decision

This batch adds issue-level coverage plus two bounded spatial/business controls. Neither control establishes a target-premises occupant, owner, tenant, license, transfer, structural event, or vacancy. No target timeline/business/building/person entry is warranted from this issue alone.

## Evidence limits

- **VISUALLY VERIFIED:** all 8 delivered pages.
- **No target-premises event found:** bounded issue coverage only; not evidence of vacancy, closure, non-use, or non-ownership.
- Brightbill is printed only as a **Main Street grocer**; no modern target number is supplied.
- The separate **12 May 1916 true weekly page-8 RETRIEVAL GAP** remains unchanged.
"""

july07 = """# Oregon City Enterprise — 7 July 1916 — complete issue visual review

**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 12 September 2026.  
**Source:** *Oregon City Enterprise*, 7 July 1916, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  
**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-07/ed-1/  
**Repository originals:** `newspapers/oregon-city-enterprise/1916/1916-07-07/`.

## Retrieval and review method

Sequences 1–14 were tested by the repository fetch workflow. Sequences **1–8** returned valid original page PDFs and later tested sequences did not add issue pages; the fetch manifest is preserved beside the scans. The archive issue navigator independently reports **8 pages**. Every one of the eight delivered PDFs was rendered and the resulting faithful page image was individually visually inspected. OCR/text extraction was used only after visual inspection as a discovery/navigation aid.

## Findings

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

### Page 2 — repeated Water/Fifth control

The DeNike & Martin advertisement again prints **new location: corner Water and Fifth Streets, Oregon City**. This repeats the 30 June spatial/business control and remains outside the target Main Street frontage.

### Page 3 — Hotel Belle / Willamette Hotel transition

A visually inspected item reports that **Fritz Boysen sold his interest in the Hotel Belle to Miles Copley**, who renamed it the **Hotel Willamette** and was remodeling it and establishing a lunch counter in connection with the hotel and soft-drink emporium. The article separately says the building belonged to **Isaac Gratton**, was leased to the **Henry Weinhard estate**, subleased to Boysen, and then to the new proprietor. This is useful relationship-separation evidence elsewhere in Oregon City: business interest/proprietorship, building ownership, master lease and sublease are distinct. The item does not place this chain at a target Main Street number.

### Pages 5 and 8 — explicit non-target Main Street controls

Page 5 prints **Larsen & Co., Corner 10th and Main Streets**. Page 8 is a full-page Miller & Obst clearance advertisement that prints **Suspension Bridge Corner, 7th at Main, Oregon City**. Both are exact contemporary Main Street controls, but both are explicitly outside the Fifth/Sixth target frontage.

## Propagation decision

This batch adds issue-level coverage and several useful non-target spatial/relationship controls. It does not establish a new target occupant, business, license, property transfer, structural event, or vacancy. No target timeline/business/building/person fact should be manufactured from the issue-level no-hit.

## Evidence limits

- **VISUALLY VERIFIED:** all 8 delivered pages.
- **No target-premises event found:** bounded issue coverage only; not evidence of vacancy, closure, non-use, or non-ownership.
- The Hotel Belle/Willamette item is retained as a relationship-separation control, not a target-premises event.
- The separate **12 May 1916 true weekly page-8 RETRIEVAL GAP** remains unchanged.
"""

write_new("evidence/source-captures/1916-enterprise-june30-visual-review-2026-09-12.md", june30)
write_new("evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md", july07)

src_md = Path("evidence/source-register.md")
s = src_md.read_text()
if "S-342" in s or "S-343" in s:
    raise SystemExit("source IDs already claimed")
s += """

## S-342 — Oregon City Enterprise, 30 June 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 30 June 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-30/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-june30-visual-review-2026-09-12.md`  
Related evidence: `E-315`.  
Notes: Page 2 prints DeNike & Martin at Water/Fifth; page 8 calls H. P. Brightbill a Main Street grocer without a street number. No source-explicit target-premises event.

## S-343 — Oregon City Enterprise, 7 July 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 7 July 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-07/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md`  
Related evidence: `E-316`.  
Notes: Exact non-target controls include Water/Fifth, Tenth/Main and Seventh/Main; Hotel Belle/Willamette relationship chain is not assigned to a target address. No source-explicit target-premises event.
"""
src_md.write_text(s)

ev_md = Path("evidence/evidence-register.md")
s = ev_md.read_text()
if "E-315" in s or "E-316" in s:
    raise SystemExit("evidence IDs already claimed")
s += """

## E-315 — 30 June 1916 Enterprise complete visual review and bounded Main/Fifth controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 2 places DeNike & Martin at the corner of Water and Fifth; page 8 identifies H. P. Brightbill as a Main Street grocer but supplies no street number. Neither item permits assignment to 501/503/505/505½/507 Main. No inspected page directly supplies a target-premises event.  
Source: `S-342`.  
Confidence: Very High for visual coverage and printed wording; no target-address inference.

## E-316 — 7 July 1916 Enterprise complete visual review and explicit non-target controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. DeNike & Martin is again at Water/Fifth; Larsen & Co. is explicitly at Tenth/Main; Miller & Obst is explicitly at Seventh/Main. Page 3 distinguishes the Hotel Belle/Willamette business-interest transition from Isaac Gratton building ownership and the Weinhard lease/sublease chain, but gives no target-address bridge. No inspected page directly supplies a target-premises event.  
Source: `S-343`.  
Confidence: Very High for visual coverage and printed non-target controls; no target-address inference.
"""
ev_md.write_text(s)

src_y = Path("database/sources.yml")
s = src_y.read_text()
if "  - id: S-342" in s or "  - id: S-343" in s:
    raise SystemExit("YAML source IDs claimed")
s += """

  - id: S-342
    name: "Oregon City Enterprise, 30 June 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-30/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-06-30"
    repository_file: "evidence/source-captures/1916-enterprise-june30-visual-review-2026-09-12.md"
    related_evidence: [E-315]
    notes: "Water/Fifth business control and unnumbered H. P. Brightbill Main Street grocer control; no source-explicit target-premises event."
  - id: S-343
    name: "Oregon City Enterprise, 7 July 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-07-07/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-07-07"
    repository_file: "evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md"
    related_evidence: [E-316]
    notes: "Explicit non-target Water/Fifth, Tenth/Main and Seventh/Main controls plus Hotel Belle/Willamette relationship-separation evidence; no source-explicit target-premises event."
"""
src_y.write_text(s)

ev_y = Path("database/evidence.yml")
s = ev_y.read_text()
if "  - id: E-315" in s or "  - id: E-316" in s:
    raise SystemExit("YAML evidence IDs claimed")
s += """

  - id: E-315
    name: "30 June 1916 Enterprise complete visual review and bounded Main/Fifth controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 2 places DeNike & Martin at Water/Fifth; page 8 identifies H. P. Brightbill as a Main Street grocer without a street number."
      - "Neither control permits assignment to 501/503/505/505½/507 Main."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-342]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-june30-visual-review-2026-09-12.md"
  - id: E-316
    name: "7 July 1916 Enterprise complete visual review and explicit non-target controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Exact non-target controls place DeNike & Martin at Water/Fifth, Larsen & Co. at Tenth/Main, and Miller & Obst at Seventh/Main."
      - "Page 3 distinguishes Hotel Belle/Willamette business interest, building ownership, lease and sublease relationships without a target-address bridge."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-343]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md"
"""
ev_y.write_text(s)

cp = Path("evidence/source-captures/1916-online-audit-checkpoint.md")
s = cp.read_text()
pairs = [
    ("209/426 certified visually reviewed pages through 23 June 1916", "225/426 certified visually reviewed pages through 7 July 1916"),
    ("667 certified visually reviewed; 217 uncertified", "683 certified visually reviewed; 201 uncertified"),
    ("Enterprise: **209/426 certified weekly pages**", "Enterprise: **225/426 certified weekly pages**"),
    ("Combined certified newspaper coverage: **667/884**", "Combined certified newspaper coverage: **683/884**"),
    ("**217 Enterprise pages remain uncertified**", "**201 Enterprise pages remain uncertified**"),
    ("next ordinary unreviewed issue is **30 June 1916**", "next ordinary unreviewed issue is **14 July 1916**"),
]
for old, new in pairs:
    if old not in s:
        raise SystemExit(f"checkpoint expected text missing: {old}")
    s = s.replace(old, new)
s += """

## 12 September continuation — 30 June and 7 July certified

- **30 June 1916:** 8/8 original weekly pages visually inspected (`S-342`, `E-315`). DeNike & Martin is explicitly at Water/Fifth; H. P. Brightbill is called a Main Street grocer but no number is printed. No target-premises event.
- **7 July 1916:** 8/8 original weekly pages visually inspected (`S-343`, `E-316`). Explicit non-target controls include Water/Fifth, Tenth/Main and Seventh/Main; the Hotel Belle/Willamette item usefully separates business interest, building ownership, lease and sublease relationships but supplies no target-address bridge.
- Enterprise certified coverage is now **225/426**; combined newspaper coverage is **683/884**; **201 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **14 July 1916**.
"""
cp.write_text(s)

ys = Path("registers/year-status.md")
s = ys.read_text()
old = "Enterprise **209/426 certified visually reviewed pages through 23 June 1916**"
new = "Enterprise **225/426 certified visually reviewed pages through 7 July 1916**"
if old not in s:
    raise SystemExit("year-status old Enterprise count missing")
s = s.replace(old, new, 1)
old = "Combined certified newspaper coverage **667/884**; **217 Enterprise pages remain uncertified**."
new = "Combined certified newspaper coverage **683/884**; **201 Enterprise pages remain uncertified**."
if old not in s:
    raise SystemExit("year-status old combined count missing")
s = s.replace(old, new, 1)
old = "the next ordinary unreviewed issue is **30 June 1916**."
new = "the next ordinary unreviewed issue is **14 July 1916**."
if old not in s:
    raise SystemExit("year-status next-issue text missing")
s = s.replace(old, new, 1)
marker = "`evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md`"
add = marker + "; `evidence/source-captures/1916-enterprise-june30-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-july07-visual-review-2026-09-12.md`"
if marker not in s:
    raise SystemExit("year-status primary record marker missing")
s = s.replace(marker, add, 1)
ys.write_text(s)
