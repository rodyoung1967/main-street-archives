from pathlib import Path

issues = [
    ('1916-12-15','15 December 1916','december15','S-366','E-339',
     'Page 5 places Larsen & Company at Corner 10th and Main Sts. and Morgan’s on Seventh Street; page 7 repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street; page 8 contains real-estate-transfer coverage.'),
    ('1916-12-22','22 December 1916','december22','S-367','E-340',
     'Page 5 places Larsen & Company at Corner 10th and Main Sts. and Morgan’s on Seventh Street; page 7 repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street; page 8 continues court/legal listings. Page 1 required a clean re-render after the first local PNG was corrupted.'),
    ('1916-12-29','29 December 1916','december29','S-368','E-341',
     'Page 1 reports Julius Wilbur as proprietor of the Friars’ Club at Milwaukie, explicitly a non-target locality; page 2 places Larsen & Company at Corner 10th and Main Sts.; page 5 places Morgan’s on Seventh Street; page 7 repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street.'),
]

for date,label,slug,sid,eid,details in issues:
    p=Path(f'evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md')
    if p.exists(): raise SystemExit(f'capture already exists: {p}')
    p.write_text(f'''# Oregon City Enterprise — {label} — complete issue visual review\n\n**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 13 September 2026.  \n**Source:** *Oregon City Enterprise*, {label}, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  \n**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/  \n**Repository originals:** `newspapers/oregon-city-enterprise/1916/{date}/`.\n\n## Retrieval and review method\n\nThe repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was discovery/navigation only and did not substitute for scan review.\n\n## Findings\n\nNo inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.\n\n{details}\n\nRecurring printed business/address, transfer, court, and legal material supplies no source-explicit target-block event. These references remain non-target geographic or contextual controls only.\n\n## Cross-record propagation audit\n\nThis issue adds annual visual-coverage evidence only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target timeline/building/business/person fact is manufactured from the no-hit.\n\n## Evidentiary limits\n\n- No source-explicit target-premises event was found in the complete eight-page issue.\n- Tenth/Main, Seventh Street, Fourth–Fifth/Main, and Milwaukie references are non-target controls only.\n- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.\n''')

src=Path('evidence/source-register.md'); s=src.read_text()
for _,_,_,sid,_,_ in issues:
    if f'## {sid} —' in s: raise SystemExit(f'{sid} already allocated')
for date,label,slug,sid,eid,details in issues:
    s += f'''\n\n## {sid} — Oregon City Enterprise, {label}, complete issue visual review\nType: Primary newspaper page scans; visually verified **8/8 pages**  \nDate: {label}  \nURL: https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/  \nRepository capture: `evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md`  \nRelated evidence: `{eid}`.  \nNotes: {details} No source-explicit target-premises event.\n'''
src.write_text(s)

ev=Path('evidence/evidence-register.md'); s=ev.read_text()
for _,_,_,_,eid,_ in issues:
    if f'## {eid} —' in s: raise SystemExit(f'{eid} already allocated')
for date,label,slug,sid,eid,details in issues:
    s += f'''\n\n## {eid} — {label} Enterprise complete visual review\nType: Primary newspaper visual evidence / annual issue-level coverage  \nClaims: All **8/8** page scans were visually inspected. {details} No inspected page directly supplies a target-premises event.  \nSource: `{sid}`.  \nConfidence: Very High for visual coverage and printed geographic controls; no-hit is bounded issue coverage only.\n'''
ev.write_text(s)

srcy=Path('database/sources.yml'); s=srcy.read_text()
for _,_,_,sid,_,_ in issues:
    if f'  - id: {sid}' in s: raise SystemExit(f'{sid} already allocated YAML')
for date,label,slug,sid,eid,details in issues:
    s += f'''\n\n  - id: {sid}\n    name: "Oregon City Enterprise, {label}, complete issue visual review"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/"\n    type: "Primary newspaper page scans; visually verified 8/8 pages"\n    date: "{date}"\n    repository_file: "evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md"\n    related_evidence: [{eid}]\n    notes: "Complete issue visually reviewed; recurring non-target Main Street controls and contextual legal/transfer material checked; no source-explicit target-premises event."\n'''
srcy.write_text(s)

evy=Path('database/evidence.yml'); s=evy.read_text()
for _,_,_,_,eid,_ in issues:
    if f'  - id: {eid}' in s: raise SystemExit(f'{eid} already allocated YAML')
for date,label,slug,sid,eid,details in issues:
    s += f'''\n\n  - id: {eid}\n    name: "{label} Enterprise complete visual review"\n    type: "Primary newspaper visual evidence / annual issue-level coverage"\n    claims:\n      - "All 8/8 pages visually inspected."\n      - "Recurring non-target Main Street controls and contextual legal/transfer material checked."\n      - "No source-explicit target-premises event; no-hit is bounded coverage only."\n    confidence: "Very High"\n    related_sources: [{sid}]\n    related_businesses: []\n    related_buildings: []\n    repository_file: "evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md"\n'''
evy.write_text(s)

cp=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); s=cp.read_text()
repls={
 '401/426 certified visually reviewed pages through 8 December 1916':'425/426 certified visually reviewed pages through 29 December 1916',
 '859 certified visually reviewed; 25 uncertified':'883 certified visually reviewed; 1 uncertified',
 '- Enterprise: **401/426 certified weekly pages**':'- Enterprise: **425/426 certified weekly pages**',
 '- Combined: **859/884 certified**':'- Combined: **883/884 certified**',
 '- Enterprise pages remaining uncertified: **25**':'- Enterprise pages remaining uncertified: **1**',
 'The next ordinary unreviewed Enterprise issue is **15 December 1916**.':'All ordinary 1916 Enterprise issue dates are now visually reviewed through **29 December 1916**; the only uncertified Enterprise page is the true **12 May weekly page 8** retrieval gap.',
}
for old,new in repls.items():
    if old not in s: raise SystemExit(f'checkpoint expected text missing: {old}')
    s=s.replace(old,new,1)
s += '''\n\n## 13 September year-end continuation — 15, 22, and 29 December certified\n\n- **15 December 1916:** 8/8 original weekly pages visually inspected (`S-366`, `E-339`); no source-explicit target-premises event.\n- **22 December 1916:** 8/8 original weekly pages visually inspected (`S-367`, `E-340`); page 1 was cleanly re-rendered after the initial local PNG was corrupted; no source-explicit target-premises event.\n- **29 December 1916:** 8/8 original weekly pages visually inspected (`S-368`, `E-341`); no source-explicit target-premises event. The Friars’ Club story on page 1 is explicitly Milwaukie and is non-target.\n- Enterprise certified coverage is now **425/426**; combined newspaper coverage is **883/884**.\n- Every ordinary 1916 Enterprise issue date through year-end has now been visually reviewed.\n- The sole uncertified Enterprise page is the true **12 May weekly page 8**, which remains a documented `RETRIEVAL GAP`.\n- 1916 remains **IN PROGRESS**, not ONLINE COMPLETE, because final other-online-source-class review and manual-callout reconciliation still remain, and the 12 May gap must be carried into the closeout/manual route rather than treated as negative evidence.\n'''
cp.write_text(s)

ys=Path('registers/year-status.md'); s=ys.read_text()
old='Enterprise **401/426 certified visually reviewed pages through 8 December 1916**'
new='Enterprise **425/426 certified visually reviewed pages through 29 December 1916**'
if old not in s: raise SystemExit('year-status coverage baseline missing')
s=s.replace(old,new,1)
s=s.replace('Combined certified newspaper coverage **859/884**; **25 Enterprise pages remain uncertified**.','Combined certified newspaper coverage **883/884**; **1 Enterprise page remains uncertified**.',1)
s=s.replace('the next ordinary unreviewed issue is **15 December 1916**.','all ordinary Enterprise issue dates through 29 December are visually reviewed; the only uncertified Enterprise page is the true 12 May weekly page 8 retrieval gap.',1)
marker='`evidence/source-captures/1916-enterprise-december08-visual-review-2026-09-13.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-december15-visual-review-2026-09-13.md`; `evidence/source-captures/1916-enterprise-december22-visual-review-2026-09-13.md`; `evidence/source-captures/1916-enterprise-december29-visual-review-2026-09-13.md`'
if addition not in s:
    if marker not in s: raise SystemExit('year-status December08 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
