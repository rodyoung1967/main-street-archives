from pathlib import Path

def append_once(path, marker, block):
    p=Path(path); t=p.read_text()
    if marker not in t: p.write_text(t.rstrip()+"\n\n"+block.strip('\n')+"\n")

def repl(path, old, new):
    p=Path(path); t=p.read_text()
    if old not in t: raise SystemExit(f'missing expected text in {path}: {old}')
    p.write_text(t.replace(old,new))

append_once('evidence/source-register.md','## S-332 — Oregon City Enterprise, 21 April 1916','''
## S-332 — Oregon City Enterprise, 21 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **21 April 1916**, edition 1.  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-21/`.  
Source capture: `evidence/source-captures/1916-enterprise-april21-visual-review-2026-09-11.md`.  
Related evidence: `E-305`.  
Notes: Page 2's “POSTOFFICE SITE IS ISSUE” item is explicitly an Estacada story, not Oregon City. No source-explicit target-premises event.

## S-333 — Oregon City Enterprise, 28 April 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 11 September 2026.  
Publication/date: *Oregon City Enterprise*, **28 April 1916**, edition 1.  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-04-28/`.  
Source capture: `evidence/source-captures/1916-enterprise-april28-visual-review-2026-09-11.md`.  
Related evidence: `E-306`.  
Notes: Page 1's Parkplace site/lease story concerns Oregon Portland Railway, Light & Power Company, not the target frontage. No source-explicit target-premises event.
''')
append_once('evidence/evidence-register.md','## E-305 — 21 April 1916 Enterprise complete visual review','''
## E-305 — 21 April 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-332`.  
Claims: all **8/8 pages** visually inspected; the page-2 post-office-site story is explicitly Estacada, not Oregon City; no page establishes a 501/503/505/505½/507 Main target-premises event; no-hit is bounded coverage only.  
Classification: **DOCUMENTED / DIRECT** for page coverage and Estacada control; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for target frontage.  
Confidence: **Very High**.

## E-306 — 28 April 1916 Enterprise complete visual review and cumulative checkpoint
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-333`.  
Claims: all **8/8 pages** visually inspected; the page-1 Parkplace site/lease story concerns Oregon Portland Railway, Light & Power Company and is non-target; no page establishes a 501/503/505/505½/507 Main target-premises event; Enterprise coverage advances to **146/426**, combined **604/884**, with **280** Enterprise pages uncertified; no-hit is bounded coverage only.  
Classification: **DOCUMENTED / DIRECT** for page coverage and Parkplace control; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for target frontage.  
Confidence: **Very High**.
''')
append_once('database/sources.yml','  - id: S-332','''
  - id: S-332
    name: "Oregon City Enterprise, 21 April 1916, complete issue visual review"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-21"
    repository_file: "evidence/source-captures/1916-enterprise-april21-visual-review-2026-09-11.md"
    related_evidence: [E-305]
    notes: "Page 2 post-office-site item is explicitly Estacada, not Oregon City; no source-explicit target-premises event."
  - id: S-333
    name: "Oregon City Enterprise, 28 April 1916, complete issue visual review"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-04-28"
    repository_file: "evidence/source-captures/1916-enterprise-april28-visual-review-2026-09-11.md"
    related_evidence: [E-306]
    notes: "Page 1 Parkplace site/lease item concerns Oregon Portland Railway, Light & Power Company, not target frontage; no source-explicit target-premises event."
''')
append_once('database/evidence.yml','  - id: E-305','''
  - id: E-305
    name: "21 April 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected from original scans."
      - "Page 2 post-office-site story is explicitly Estacada, not Oregon City."
      - "No page establishes a 501/503/505/505½/507 Main target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-332]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-april21-visual-review-2026-09-11.md"
  - id: E-306
    name: "28 April 1916 Enterprise complete visual review and cumulative checkpoint"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected from original scans."
      - "Page 1 Parkplace site/lease story concerns Oregon Portland Railway, Light & Power Company and is non-target."
      - "No page establishes a 501/503/505/505½/507 Main target-premises event; Enterprise coverage is 146/426 and combined coverage 604/884 with 280 Enterprise pages uncertified."
    confidence: "Very High"
    related_sources: [S-333]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-april28-visual-review-2026-09-11.md"
''')

p='registers/year-status.md'; t=Path(p).read_text()
old='Enterprise **130/426 visually reviewed through 14 April 1916**. Combined certified newspaper coverage **588/884**; **296 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **21 April 1916**.'
new='Enterprise **146/426 visually reviewed through 28 April 1916**. Combined certified newspaper coverage **604/884**; **280 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **5 May 1916**.'
if old not in t: raise SystemExit('year status changed; refusing overwrite')
t=t.replace(old,new)
anchor='`evidence/source-captures/1916-enterprise-april14-visual-review-2026-09-11.md`'
t=t.replace(anchor,anchor+'; `evidence/source-captures/1916-enterprise-april21-visual-review-2026-09-11.md`; `evidence/source-captures/1916-enterprise-april28-visual-review-2026-09-11.md`',1)
Path(p).write_text(t)

p='evidence/source-captures/1916-online-audit-checkpoint.md'; t=Path(p).read_text()
for old,new in [
('**130/426 visually reviewed through 14 April 1916**','**146/426 visually reviewed through 28 April 1916**'),
('**588 visually reviewed; 296 pending**','**604 visually reviewed; 280 pending**'),
('- Enterprise: **130/426**','- Enterprise: **146/426**'),
('- Combined: **588/884**','- Combined: **604/884**'),
('- Enterprise pages remaining: **296**','- Enterprise pages remaining: **280**'),
('The next ordinary unreviewed *Oregon City Enterprise* issue is **21 April 1916**.','The next ordinary unreviewed *Oregon City Enterprise* issue is **5 May 1916**.')]:
    if old not in t: raise SystemExit(f'checkpoint changed: {old}')
    t=t.replace(old,new)
anchor='- `1916-enterprise-april14-visual-review-2026-09-11.md`\n'
if '- `1916-enterprise-april28-visual-review-2026-09-11.md`' not in t:
    if anchor not in t: raise SystemExit('checkpoint link anchor missing')
    t=t.replace(anchor,anchor+'- `1916-enterprise-april21-visual-review-2026-09-11.md`\n- `1916-enterprise-april28-visual-review-2026-09-11.md`\n')
Path(p).write_text(t)
