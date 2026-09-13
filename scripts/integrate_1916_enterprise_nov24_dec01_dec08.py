from pathlib import Path

issues = [
    ('1916-11-24','24 November 1916','november24','S-363','E-336',
     'Page 2 contains real-estate-transfer coverage; page 3 places Larsen & Company at Corner 10th and Main Sts.; page 5 places Morgan’s on Seventh Street; page 7 repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street.'),
    ('1916-12-01','1 December 1916','december01','S-364','E-337',
     'Page 3 places Larsen & Company at Corner 10th and Main Sts.; page 5 places Morgan’s on Seventh Street; page 7 repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street; page 8 contains real-estate-transfer coverage. Page 3 required a clean re-render after the first local PNG was unreadable.'),
    ('1916-12-08','8 December 1916','december08','S-365','E-338',
     'Page 5 places Larsen & Company at Corner 10th and Main Sts. and Morgan’s on Seventh Street; page 7 contains real-estate-transfer coverage and repeats W. S. Eddy at Fashion Stable, between Fourth and Fifth on Main Street.'),
]

for date,label,slug,sid,eid,details in issues:
    p=Path(f'evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md')
    if p.exists():
        raise SystemExit(f'capture already exists: {p}')
    p.write_text(f'''# Oregon City Enterprise — {label} — complete issue visual review\n\n**Status:** VISUALLY VERIFIED — **8/8 genuine weekly pages inspected** on 13 September 2026.  \n**Source:** *Oregon City Enterprise*, {label}, edition 1, University of Oregon Historic Oregon Newspapers, LCCN `sn00063700`.  \n**Canonical issue:** https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/  \n**Repository originals:** `newspapers/oregon-city-enterprise/1916/{date}/`.\n\n## Retrieval and review method\n\nThe repository fetch workflow preserved the eight valid original page PDFs plus a fetch manifest. Every preserved PDF was rendered to a faithful page image and each page was individually visually inspected at readable scale. OCR/text extraction was discovery/navigation only and did not substitute for scan review.\n\n## Findings\n\nNo inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.\n\n{details}\n\nThe printed real-estate-transfer material supplies no source-explicit target-block transfer. The recurring business/address references are non-target geographic controls only.\n\n## Cross-record propagation audit\n\nThis issue adds annual visual-coverage evidence only. It does **not** establish a new target occupant, business, ownership, tenancy, licensing, or building fact. No target timeline/building/business/person fact is manufactured from the no-hit.\n\n## Evidentiary limits\n\n- No source-explicit target-premises event was found in the complete eight-page issue.\n- Tenth/Main, Seventh Street, and Fourth–Fifth/Main references are exact non-target controls only.\n- No-hit language is bounded issue coverage and is not evidence of vacancy, non-use, demolition, closure, or non-ownership.\n''')

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
    s += f'''\n\n  - id: {sid}\n    name: "Oregon City Enterprise, {label}, complete issue visual review"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/"\n    type: "Primary newspaper page scans; visually verified 8/8 pages"\n    date: "{date}"\n    repository_file: "evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md"\n    related_evidence: [{eid}]\n    notes: "Complete issue visually reviewed; recurring non-target Main Street controls and transfer material checked; no source-explicit target-premises event."\n'''
srcy.write_text(s)

evy=Path('database/evidence.yml'); s=evy.read_text()
for _,_,_,_,eid,_ in issues:
    if f'  - id: {eid}' in s: raise SystemExit(f'{eid} already allocated YAML')
for date,label,slug,sid,eid,details in issues:
    s += f'''\n\n  - id: {eid}\n    name: "{label} Enterprise complete visual review"\n    type: "Primary newspaper visual evidence / annual issue-level coverage"\n    claims:\n      - "All 8/8 pages visually inspected."\n      - "Recurring non-target Main Street controls and printed transfer material checked."\n      - "No source-explicit target-premises event; no-hit is bounded coverage only."\n    confidence: "Very High"\n    related_sources: [{sid}]\n    related_businesses: []\n    related_buildings: []\n    repository_file: "evidence/source-captures/1916-enterprise-{slug}-visual-review-2026-09-13.md"\n'''
evy.write_text(s)

cp=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); s=cp.read_text()
repls={
 '377/426 certified visually reviewed pages through 17 November 1916':'401/426 certified visually reviewed pages through 8 December 1916',
 '835 certified visually reviewed; 49 uncertified':'859 certified visually reviewed; 25 uncertified',
 '- Enterprise: **377/426 certified weekly pages**':'- Enterprise: **401/426 certified weekly pages**',
 '- Combined: **835/884 certified**':'- Combined: **859/884 certified**',
 '- Enterprise pages remaining uncertified: **49**':'- Enterprise pages remaining uncertified: **25**',
 'The next ordinary unreviewed Enterprise issue is **24 November 1916**.':'The next ordinary unreviewed Enterprise issue is **15 December 1916**.',
}
for old,new in repls.items():
    if old in s: s=s.replace(old,new,1)
s += '''\n\n## 13 September continuation — 24 November, 1 December, and 8 December certified\n\n- **24 November 1916:** 8/8 original weekly pages visually inspected (`S-363`, `E-336`); no source-explicit target-premises event.\n- **1 December 1916:** 8/8 original weekly pages visually inspected (`S-364`, `E-337`); page 3 was cleanly re-rendered after the initial local PNG was unreadable; no source-explicit target-premises event.\n- **8 December 1916:** 8/8 original weekly pages visually inspected (`S-365`, `E-338`); no source-explicit target-premises event.\n- Larsen & Company at Tenth/Main, Morgan’s on Seventh Street, W. S. Eddy at Fashion Stable between Fourth and Fifth on Main, and printed real-estate-transfer material recur as non-target controls without a source-explicit 501/503/505/505½/507 Main event.\n- Enterprise certified coverage is now **401/426**; combined newspaper coverage is **859/884**; **25 Enterprise pages remain uncertified**.\n- The true **12 May weekly page 8** remains a `RETRIEVAL GAP`.\n- Next ordinary Enterprise issue for visual review: **15 December 1916**.\n'''
cp.write_text(s)

ys=Path('registers/year-status.md'); s=ys.read_text()
old='Enterprise **377/426 certified visually reviewed pages through 17 November 1916**'
new='Enterprise **401/426 certified visually reviewed pages through 8 December 1916**'
if old not in s: raise SystemExit('year-status coverage baseline missing')
s=s.replace(old,new,1)
s=s.replace('Combined certified newspaper coverage **835/884**; **49 Enterprise pages remain uncertified**.','Combined certified newspaper coverage **859/884**; **25 Enterprise pages remain uncertified**.',1)
s=s.replace('the next ordinary unreviewed issue is **24 November 1916**.','the next ordinary unreviewed issue is **15 December 1916**.',1)
marker='`evidence/source-captures/1916-enterprise-november17-visual-review-2026-09-13.md`'
addition=marker+'; `evidence/source-captures/1916-enterprise-november24-visual-review-2026-09-13.md`; `evidence/source-captures/1916-enterprise-december01-visual-review-2026-09-13.md`; `evidence/source-captures/1916-enterprise-december08-visual-review-2026-09-13.md`'
if addition not in s:
    if marker not in s: raise SystemExit('year-status November17 marker missing')
    s=s.replace(marker,addition,1)
ys.write_text(s)
