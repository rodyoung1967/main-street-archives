from pathlib import Path

for p in [
    Path('evidence/source-captures/1916-enterprise-august11-visual-review-2026-09-12.md'),
    Path('evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md'),
]:
    if not p.exists():
        raise SystemExit(f'missing required capture: {p}')

# Append canonical source/evidence records if absent.
src = Path('evidence/source-register.md')
s = src.read_text()
if '## S-348 —' not in s:
    s += '''\n\n## S-348 — Oregon City Enterprise, 11 August 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 11 August 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-11/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-august11-visual-review-2026-09-12.md`  
Related evidence: `E-321`.  
Notes: Larsen & Co. is explicitly at Tenth/Main; no source-explicit event for 501/503/505/505½/507 Main.

## S-349 — Oregon City Enterprise, 18 August 1916, complete issue visual review
Type: Primary newspaper page scans; visually verified **8/8 pages**  
Date: 18 August 1916  
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-18/ed-1/  
Repository capture: `evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md`  
Related evidence: `E-322`.  
Notes: Larsen & Company is explicitly at Tenth/Main; page 7 prints 501 Division Street, an exact non-target control for bare-number 501 search hits. No target-premises event.
'''
src.write_text(s)

ev = Path('evidence/evidence-register.md')
s = ev.read_text()
if '## E-321 —' not in s:
    s += '''\n\n## E-321 — 11 August 1916 Enterprise complete visual review and Tenth/Main business control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Co. at Corner Tenth and Main Streets. No inspected page directly supplies a target-premises event.  
Source: `S-348`.  
Confidence: Very High for visual coverage and exact non-target location.

## E-322 — 18 August 1916 Enterprise complete visual review and non-target address controls
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 places Larsen & Company at Tenth/Main. Page 7 prints 501 Division Street, showing that a bare OCR/search hit for 501 is not a target Main Street address. No inspected page directly supplies a target-premises event.  
Source: `S-349`.  
Confidence: Very High for visual coverage and exact non-target location/address controls.
'''
ev.write_text(s)

srcy = Path('database/sources.yml')
s = srcy.read_text()
if '  - id: S-348' not in s:
    s += '''\n\n  - id: S-348
    name: "Oregon City Enterprise, 11 August 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-11/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-08-11"
    repository_file: "evidence/source-captures/1916-enterprise-august11-visual-review-2026-09-12.md"
    related_evidence: [E-321]
    notes: "Exact Tenth/Main Larsen & Co. control; no source-explicit target-premises event."
  - id: S-349
    name: "Oregon City Enterprise, 18 August 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-08-18/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-08-18"
    repository_file: "evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md"
    related_evidence: [E-322]
    notes: "Exact Tenth/Main business control and 501 Division Street non-target address-number control; no target-premises event."
'''
srcy.write_text(s)

evy = Path('database/evidence.yml')
s = evy.read_text()
if '  - id: E-321' not in s:
    s += '''\n\n  - id: E-321
    name: "11 August 1916 Enterprise complete visual review and Tenth/Main business control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Co. at Corner Tenth and Main Streets."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-348]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-august11-visual-review-2026-09-12.md"
  - id: E-322
    name: "18 August 1916 Enterprise complete visual review and non-target address controls"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places Larsen & Company at Tenth/Main."
      - "Page 7 prints 501 Division Street, an exact non-target control for bare-number 501 search hits."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-349]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md"
'''
evy.write_text(s)

# Normalize every live summary occurrence, including a stale duplicate Resume-point block left by the prior integration.
cp = Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s = cp.read_text()
repls = {
    '257/426 certified visually reviewed pages through 4 August 1916':'273/426 certified visually reviewed pages through 18 August 1916',
    '715 certified visually reviewed; 169 uncertified':'731 certified visually reviewed; 153 uncertified',
    '- Enterprise: **257/426 certified weekly pages**':'- Enterprise: **273/426 certified weekly pages**',
    '- Combined: **699/884 certified**':'- Combined: **731/884 certified**',
    '- Combined: **715/884 certified**':'- Combined: **731/884 certified**',
    '- Enterprise pages remaining uncertified: **185**':'- Enterprise pages remaining uncertified: **153**',
    '- Enterprise pages remaining uncertified: **169**':'- Enterprise pages remaining uncertified: **153**',
    'The next ordinary unreviewed Enterprise issue is **28 July 1916**.':'The next ordinary unreviewed Enterprise issue is **25 August 1916**.',
    'The next ordinary unreviewed Enterprise issue is **11 August 1916**.':'The next ordinary unreviewed Enterprise issue is **25 August 1916**.',
}
for old,new in repls.items():
    s=s.replace(old,new)
if '## 12 September continuation — 11 and 18 August certified' not in s:
    s += '''\n\n## 12 September continuation — 11 and 18 August certified

- **11 August 1916:** 8/8 original weekly pages visually inspected (`S-348`, `E-321`). Larsen & Co. is explicitly at Tenth/Main; no source-explicit target-premises event.
- **18 August 1916:** 8/8 original weekly pages visually inspected (`S-349`, `E-322`). Larsen & Company is at Tenth/Main; page 7 prints 501 Division Street, an exact non-target address-number control.
- Enterprise certified coverage is now **273/426**; combined newspaper coverage is **731/884**; **153 Enterprise pages remain uncertified**.
- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.
- Next ordinary Enterprise issue for visual review: **25 August 1916**.
'''
cp.write_text(s)

ys=Path('registers/year-status.md')
s=ys.read_text()
s=s.replace('Enterprise **257/426 certified visually reviewed pages through 4 August 1916**','Enterprise **273/426 certified visually reviewed pages through 18 August 1916**')
s=s.replace('Combined certified newspaper coverage **715/884**; **169 Enterprise pages remain uncertified**.','Combined certified newspaper coverage **731/884**; **153 Enterprise pages remain uncertified**.')
s=s.replace('the next ordinary unreviewed issue is **11 August 1916**.','the next ordinary unreviewed issue is **25 August 1916**.')
marker='`evidence/source-captures/1916-enterprise-august04-visual-review-2026-09-12.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-august11-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-august18-visual-review-2026-09-12.md`'
if addition not in s:
    if marker not in s: raise SystemExit('year-status August04 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
