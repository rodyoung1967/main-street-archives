from pathlib import Path

closeout='evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md'
if not Path(closeout).exists():
    raise SystemExit('closeout capture missing')

# Allocate closeout source/evidence IDs only if still free.
src=Path('evidence/source-register.md'); s=src.read_text()
if '## S-369 —' in s:
    raise SystemExit('S-369 already allocated')
s += '''\n\n## S-369 — 1916 online source-class closeout\nType: Research-standard annual closeout / online source-class audit  \nDate: 13 September 2026  \nURL: https://github.com/rodyoung1967/main-street-archives/blob/main/evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md  \nRepository capture: `evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md`  \nRelated evidence: `E-342`.  \nNotes: Certifies 1916 as ONLINE COMPLETE under RESEARCH-STANDARD.md after newspaper, directory, map, municipal, property, historic-resource, photograph, and official-database reconciliation. Remaining physical/restricted/non-rendering work is preserved as MF-061 through MF-067.\n'''
src.write_text(s)

ev=Path('evidence/evidence-register.md'); s=ev.read_text()
if '## E-342 —' in s:
    raise SystemExit('E-342 already allocated')
s += '''\n\n## E-342 — 1916 ONLINE COMPLETE source-class reconciliation\nType: Annual research-completeness evidence  \nClaims: 1916 satisfies the ONLINE COMPLETE definition; Courier is 458/458 visually reviewed; Enterprise is 425/426 certified with the true 12 May weekly page 8 preserved as a retrieval gap; all remaining non-online work is enumerated as MF-061 through MF-067. Other online source classes were reviewed or their public-online access limits established without treating source silence as historical absence.  \nSource: `S-369`.  \nConfidence: Very High for research-status classification; unresolved historical occupancy questions remain explicitly unresolved.\n'''
ev.write_text(s)

sy=Path('database/sources.yml'); s=sy.read_text()
if '  - id: S-369' in s: raise SystemExit('S-369 YAML already allocated')
s += '''\n\n  - id: S-369\n    name: "1916 online source-class closeout"\n    url: "https://github.com/rodyoung1967/main-street-archives/blob/main/evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md"\n    type: "Research-standard annual closeout / online source-class audit"\n    date: "2026-09-13"\n    repository_file: "evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md"\n    related_evidence: [E-342]\n    notes: "Certifies 1916 ONLINE COMPLETE; remaining physical/restricted/non-rendering work is MF-061 through MF-067."\n'''
sy.write_text(s)

ey=Path('database/evidence.yml'); s=ey.read_text()
if '  - id: E-342' in s: raise SystemExit('E-342 YAML already allocated')
s += '''\n\n  - id: E-342\n    name: "1916 ONLINE COMPLETE source-class reconciliation"\n    type: "Annual research-completeness evidence"\n    claims:\n      - "1916 satisfies the ONLINE COMPLETE definition in RESEARCH-STANDARD.md."\n      - "Courier 458/458 visually reviewed; Enterprise 425/426 certified with one precisely documented retrieval gap."\n      - "Remaining physical, restricted, institutional, user-assisted, or non-rendering work is MF-061 through MF-067."\n      - "Source silence was not treated as evidence of vacancy, closure, demolition, non-use, or non-ownership."\n    confidence: "Very High"\n    related_sources: [S-369]\n    related_businesses: []\n    related_buildings: []\n    repository_file: "evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md"\n'''
ey.write_text(s)

# Manual dashboard: append MF-066/MF-067 and a 1916 closeout header if not already present.
md=Path('MANUAL-FOLLOWUP.md'); s=md.read_text()
if '### MF-066 — 1916 City Commission minutes / ordinances / license records' not in s:
    block='''\n\n## 1916 ONLINE COMPLETE — remaining manual work\n\nFormal closeout: `evidence/source-captures/1916-online-source-class-closeout-2026-09-13.md`. The remaining 1916 manual tasks are **MF-061, MF-062, MF-063, MF-064, MF-065, MF-066, and MF-067**. No institutional request has been sent for this closeout.\n\n### MF-066 — 1916 City Commission minutes / ordinances / license records\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Inspect the 1916 City Commission minute/ordinance/license records through the Oregon City Recorder / ORMS WebDrawer route. The City's Meeting Document Archive exposes a 1910–1919 City Commission decade query, but the offsite WebDrawer query did not render through the research environment after direct recovery attempts. Prioritize pool-hall and cigar licensing, Raasch & Lamb, Harding, Hylton, 500-block Main, property/street actions, and the June 1916 temporary-permit / ordinance dispute reported in the Courier. Do not substitute the newspaper report for the underlying municipal record.\n\n### MF-067 — Oregon City historic photographs PDF / 1916 Fifth-Main check\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Visually inspect the City's 72-page `Photographs.pdf` (Historic Documents and Research → Historic Photos and Art) through a direct browser or institutional copy for securely dated 1916 or tightly bracketed Fifth/Main / 501–507 Main images. The source is publicly indexed, but page-image rendering and direct file recovery failed in the research environment. A no-hit may be recorded only after the images themselves are visually inspected.\n'''
    marker='## 1917 ONLINE COMPLETE — remaining manual work'
    if marker in s:
        s=s.replace(marker, block+'\n\n'+marker,1)
    else:
        s += block
md.write_text(s)

# Update checkpoint status and closeout reference.
cp=Path('evidence/source-captures/1916-online-audit-checkpoint.md'); s=cp.read_text()
s=s.replace('Status: **IN PROGRESS**','Status: **ONLINE COMPLETE**',1)
old='The year remains **IN PROGRESS / NOT ONLINE COMPLETE**.'
if old in s:
    s=s.replace(old,'The newspaper chronology is complete except for the precisely documented 12 May weekly page-8 retrieval gap. The formal 13 September source-class reconciliation now certifies the year **ONLINE COMPLETE**; remaining non-online work is MF-061 through MF-067.',1)
if '## 13 September 2026 — ONLINE COMPLETE closeout' not in s:
    s += '''\n\n## 13 September 2026 — ONLINE COMPLETE closeout\n\nFormal closeout: `1916-online-source-class-closeout-2026-09-13.md` (`S-369` / `E-342`). Newspaper coverage is Courier **458/458** and Enterprise **425/426**, with the genuine 12 May weekly page 8 preserved as `MF-061`. Directory, map, municipal, property, historic-resource, photograph, and official-database classes were reconciled. Remaining physical/restricted/non-rendering work is **MF-061 through MF-067**. Absence of evidence was not treated as evidence of absence.\n'''
cp.write_text(s)

# Promote year status.
ys=Path('registers/year-status.md'); s=ys.read_text()
old='| 1916 | **IN PROGRESS** |'
if old not in s:
    raise SystemExit('1916 year-status row baseline missing')
s=s.replace(old,'| 1916 | **ONLINE COMPLETE** |',1)
marker='`evidence/source-captures/1916-online-audit-checkpoint.md`;'
if marker in s and closeout not in s:
    s=s.replace(marker, marker+' `'+closeout+'`;',1)
s=s.replace('Other online source classes and final manual-callout reconciliation remain pending; no source silence is vacancy evidence.','Other online source classes are reconciled; remaining physical/restricted/non-rendering work is MF-061 through MF-067. No source silence is vacancy evidence.',1)
ys.write_text(s)
