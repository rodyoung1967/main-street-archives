from pathlib import Path
import runpy

runpy.run_path('scripts/maintenance/integrate_1916_enterprise_may19_may26.py', run_name='__main__')

p = Path('evidence/evidence-register.md')
s = p.read_text()
old = '''## E-309 — 19 May 1916 Enterprise complete visual review
**State:** DOCUMENTED / DIRECT for issue-level visual coverage; bounded no-hit only for target premises.  
**Source:** `S-336`.  
All **8/8** page scans were visually inspected. No page directly assigns an occupant, owner, tenant, licensee, business name, sale/transfer, construction, demolition, closure or vacancy to 501/503/505/505½/507 Main. General Main Street and unrelated Harding/Young material does not establish a target bridge. This is coverage evidence only, not evidence of absence.

## E-310 — 26 May 1916 Enterprise complete visual review and Jones Drug relocation control
**State:** DOCUMENTED / DIRECT for issue-level visual coverage and the printed Jones Drug move wording; no target-address bridge.  
**Source:** `S-337`.  
All **8/8** page scans were visually inspected. Page 8 directly states Jones Drug Company is going to move very soon because the landlord wants more room for his own business and labels the current premises only as “Old location—Next to Burmeister & Andresen’s.” No street number is printed, so the move is retained as non-target city/business context and is not mapped to 501/503/505/505½/507 Main. No page establishes a source-explicit target-premises event. The no-hit is coverage only, not vacancy evidence.'''
new = '''## E-309 — 19 May 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-336`.  
Claims: all **8/8 pages** were visually inspected; no page directly assigns an occupant, owner, tenant, licensee, business name, sale/transfer, construction, demolition, closure or vacancy to 501/503/505/505½/507 Main; general Main Street and unrelated Harding/Young material does not establish a target bridge; this is coverage evidence only, not evidence of absence.  
Classification: **DOCUMENTED / DIRECT** for issue-level visual coverage; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for the target frontage.  
Confidence: **Very High** for page coverage and the bounded no-hit scope.

## E-310 — 26 May 1916 Enterprise complete visual review and Jones Drug relocation control
Type: Primary newspaper visual evidence / annual issue-level coverage / non-target relocation control.  
Source: `S-337`.  
Claims: all **8/8 pages** were visually inspected; page 8 directly states Jones Drug Company is going to move very soon because the landlord wants more room for his own business and labels the current premises only as “Old location—Next to Burmeister & Andresen’s”; no street number is printed, so the move is retained as non-target city/business context and is not mapped to 501/503/505/505½/507 Main; no page establishes a source-explicit target-premises event; the no-hit is coverage only, not vacancy evidence.  
Classification: **DOCUMENTED / DIRECT** for issue-level visual coverage and the printed Jones Drug move wording; **NO TARGET-ADDRESS BRIDGE** for the studied frontage.  
Confidence: **Very High** for the printed wording and page coverage; no confidence assigned to an unmade target-address inference.'''
if old not in s:
    raise SystemExit('expected E-309/E-310 provisional block not found')
p.write_text(s.replace(old, new, 1))
