from pathlib import Path


def append_once(path, marker, text):
    p = Path(path); s = p.read_text()
    if marker not in s:
        p.write_text(s.rstrip() + "\n\n" + text.strip("\n") + "\n")


def replace_required(path, old, new):
    p = Path(path); s = p.read_text()
    if old not in s:
        raise SystemExit(f"missing expected text in {path}: {old}")
    p.write_text(s.replace(old, new, 1))

append_once('evidence/source-register.md', '## S-340 — Oregon City Enterprise, 16 June 1916', r'''
## S-340 — Oregon City Enterprise, 16 June 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **16 June 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-16/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-06-16/`.  
Source capture: `evidence/source-captures/1916-enterprise-june16-visual-review-2026-09-12.md`.  
Related evidence: `E-313`.  
Notes: All eight original page scans were visually inspected. Page 5 directly describes a $30,500 Main Street realty deal on the east side between Seventh and Eighth and says one small corner belonged to George A. Harding; this is non-target Harding property context only. No page establishes a source-explicit 501/503/505/505½/507 Main premises event. No-hit is bounded coverage, not vacancy evidence.

## S-341 — Oregon City Enterprise, 23 June 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **23 June 1916**, edition 1.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-23/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-06-23/`.  
Source capture: `evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md`.  
Related evidence: `E-314`.  
Notes: All eight original page scans were visually inspected. Page 1 describes Hawley paper-mill expansion and an option on the southern half of the block bounded by Main, the Southern Pacific tracks, Fourth and Fifth, owned by James Tracy; this is nearby non-target parcel context only. No page establishes a source-explicit target-premises event.
''')

append_once('evidence/evidence-register.md', '## E-313 — 16 June 1916 Enterprise complete visual review', r'''
## E-313 — 16 June 1916 Enterprise complete visual review and Harding non-target Main Street property control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 5 directly reports a $30,500 Main Street real-estate transaction for property on the east side of Main between Seventh and Eighth and says one small corner belonged to George A. Harding. That Harding interest is outside the target Fifth/Sixth frontage and must not be projected onto 501/503/505/505½/507 Main. No page directly assigns a target occupant, owner, tenant, licensee, business name, sale/transfer, construction, demolition, closure or vacancy. No-hit is coverage evidence only.  
Source: `S-340`.  
Confidence: Very High for visual coverage and printed non-target property wording; no target-address inference.

## E-314 — 23 June 1916 Enterprise complete visual review and nearby Fourth/Fifth block development control
Type: Primary newspaper visual evidence / annual issue-level coverage  
Claims: All **8/8** page scans were visually inspected. Page 1 directly reports proposed Hawley paper-mill expansion and an option on the southern half of the block bounded by Main, the Southern Pacific tracks, Fourth and Fifth Streets, owned by James Tracy of Gladstone, with existing improvements to be removed if the additional mill were built. This is nearby non-target spatial/property context only. No page directly assigns a target-premises event to 501/503/505/505½/507 Main.  
Source: `S-341`.  
Confidence: Very High for visual coverage and printed nearby-block wording; no target-address inference.
''')

append_once('database/sources.yml', '  - id: S-340', r'''
  - id: S-340
    name: "Oregon City Enterprise, 16 June 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-16/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-06-16"
    repository_file: "evidence/source-captures/1916-enterprise-june16-visual-review-2026-09-12.md"
    related_evidence: [E-313]
    notes: "Page 5 gives non-target Harding property context on Main between Seventh and Eighth; no source-explicit target-premises event."
  - id: S-341
    name: "Oregon City Enterprise, 23 June 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-06-23/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-06-23"
    repository_file: "evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md"
    related_evidence: [E-314]
    notes: "Page 1 gives nearby Fourth/Fifth block Hawley expansion and James Tracy ownership context; no source-explicit target-premises event."
''')

append_once('database/evidence.yml', '  - id: E-313', r'''
  - id: E-313
    name: "16 June 1916 Enterprise complete visual review and Harding non-target property control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 5 places a $30,500 Main Street transaction between Seventh and Eighth and says one small corner belonged to George A. Harding."
      - "The Harding interest is non-target and must not be projected to 501/503/505/505½/507 Main."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-340]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-june16-visual-review-2026-09-12.md"
  - id: E-314
    name: "23 June 1916 Enterprise complete visual review and nearby Fourth/Fifth block control"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected."
      - "Page 1 describes proposed Hawley expansion and James Tracy ownership in the block bounded by Main, Southern Pacific tracks, Fourth and Fifth Streets."
      - "That parcel is nearby non-target context and does not establish a target-premises event."
      - "No source-explicit target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-341]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md"
''')

replace_required('registers/year-status.md',
'Enterprise **193/426 certified visually reviewed pages through 9 June 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP** after bounded alternate-edition/title recovery attempts. Combined certified newspaper coverage **651/884**; **233 Enterprise pages remain uncertified**. The 12 May true weekly page 8 remains an explicit retrieval gap carried forward; the next ordinary unreviewed issue is **16 June 1916**.',
'Enterprise **209/426 certified visually reviewed pages through 23 June 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP** after bounded alternate-edition/title recovery attempts. Combined certified newspaper coverage **667/884**; **217 Enterprise pages remain uncertified**. The 12 May true weekly page 8 remains an explicit retrieval gap carried forward; the next ordinary unreviewed issue is **30 June 1916**.')

p=Path('registers/year-status.md'); s=p.read_text(); old='`evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md` | 104 issues / 884 pages.'; new='`evidence/source-captures/1916-enterprise-june09-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-june16-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md` | 104 issues / 884 pages.'
if old not in s: raise SystemExit('year-status capture anchor changed')
p.write_text(s.replace(old,new,1))

p=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); s=p.read_text()
for old,new in [
('**193/426 certified visually reviewed pages through 9 June 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**','**209/426 certified visually reviewed pages through 23 June 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**'),
('**651 certified visually reviewed; 233 uncertified**','**667 certified visually reviewed; 217 uncertified**'),
('Enterprise: **193/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**','Enterprise: **209/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**'),
('Combined: **651/884 certified**','Combined: **667/884 certified**'),
('Enterprise pages remaining uncertified: **233**','Enterprise pages remaining uncertified: **217**'),
('The complete **2 June** and **9 June** issues are now **8/8 visually verified**. The next ordinary unreviewed Enterprise issue is **16 June 1916**.','The complete **16 June** and **23 June** issues are now **8/8 visually verified**. The next ordinary unreviewed Enterprise issue is **30 June 1916**.')]:
    if old not in s: raise SystemExit(f'checkpoint changed; missing: {old}')
    s=s.replace(old,new,1)
anchor='- `1916-enterprise-june09-visual-review-2026-09-12.md`\n'
if '- `1916-enterprise-june23-visual-review-2026-09-12.md`' not in s:
    if anchor not in s: raise SystemExit('checkpoint capture anchor missing')
    s=s.replace(anchor,anchor+'- `1916-enterprise-june16-visual-review-2026-09-12.md`\n- `1916-enterprise-june23-visual-review-2026-09-12.md`\n',1)
p.write_text(s)
