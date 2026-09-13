from pathlib import Path

manual=Path('MANUAL-FOLLOWUP.md')
s=manual.read_text()
if '### MF-061 — 12 May 1916 Enterprise genuine weekly page 8' not in s:
    anchor='## 1917 ONLINE COMPLETE — remaining manual work\n'
    block='''## 1916 ONLINE-CLOSEOUT manual work created 13 September 2026\n\nThese three items have completed reasonable public-online recovery and are no longer ONLINE-FIRST tasks. They remain manual work for eventual **ONLINE + MANUAL COMPLETE**. Canonical closure checkpoint: `evidence/source-captures/1916-online-gap-closure-manual-callouts-2026-09-13.md`.\n\n### MF-061 — 12 May 1916 Enterprise genuine weekly page 8\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Retrieve the genuine weekly *Oregon City Enterprise*, 12 May 1916, page 8 through University of Oregon source-film/derivative review or another institutional microfilm holding. Archive sequence 8 is visibly *Morning Enterprise*; sequences 1–7 are the weekly issue. Bounded online recovery did not recover a weekly replacement. Preserve as `RETRIEVAL GAP` until the actual weekly page is visually inspected.\n\n### MF-062 — Sohns & Woodbeck 1916–1917 Oregon City directory pages\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Retrieve the Oregon City section of *Clackamas County & Oregon City Directory*, vol. 1 (Sohns & Woodbeck, 1916–1917), via FamilySearch catalog `1844954` at a FamilySearch Center/affiliate or the Oregon Historical Society copy. Visually inspect **501, 503, 503½, 505, 507, 509, 511 Main**, relevant named occupants/businesses, and any reverse/street-directory 500-block listing. Public online recovery is exhausted; the Oak Lodge PDF is explicitly only Oak Grove/Jennings Lodge.\n\n### MF-063 — Polk 1915–1916 Oregon City gazetteer/business-directory section\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Retrieve and visually inspect the Oregon City section of R. L. Polk & Co., *Oregon and Washington State Gazetteer and Business Directory, 1915–1916*. FamilySearch catalog `1439422` and all four image ARKs are known, but no unrestricted public mirror exposing the Oregon City pages was recovered. Use FamilySearch Center/affiliate access first; Spokane Public Library Inland Northwest Special Collections (`NW 917.9 OREGON`, barcode `37413310824562`) is a physical fallback. Check target names/business classes and address-bearing listings relevant to 501/503/503½/505/507/509/511 Main.\n\n'''
    if anchor not in s: raise SystemExit('manual dashboard anchor missing')
    s=s.replace(anchor,block+anchor,1)
    s=s.replace('Last amended: **10 September 2026** — synchronized the previously created 505 Main `MF-058` Ray Hansen / 1959–1965 proprietor-licensee package into this dashboard; later `MF-059` and `MF-060` remain unchanged and no existing MF ID was renumbered or removed.', 'Last amended: **13 September 2026** — converted three exhausted 1916 online-first gaps into year-closeout manual callouts `MF-061`–`MF-063`; no existing MF ID was renumbered or removed.',1)
    manual.write_text(s)

cp=Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s=cp.read_text()
marker='The year remains **IN PROGRESS / NOT ONLINE COMPLETE**.'
replacement='''Three formerly open online-first tasks are now closed as online recovery work and converted to numbered year-closeout manual callouts: `MF-061` (12 May weekly Enterprise page 8), `MF-062` (Sohns & Woodbeck 1916–1917 Oregon City directory), and `MF-063` (Polk 1915–1916 Oregon City gazetteer/business-directory section). See `1916-online-gap-closure-manual-callouts-2026-09-13.md`. These conversions satisfy the online-recovery portion for those sources without claiming the sources were obtained.\n\nThe year remains **IN PROGRESS / NOT ONLINE COMPLETE**.'''
if 'MF-061' not in s:
    if marker not in s: raise SystemExit('checkpoint marker missing')
    s=s.replace(marker,replacement,1)
    cp.write_text(s)

lead=Path('evidence/source-captures/1916-1917-directory-lead.md')
s=lead.read_text()
if 'MF-062' not in s:
    s += '''\n\n## 13 September 2026 online-closeout disposition\n\nA fresh public-web recovery pass again found bibliographic citations, FamilySearch catalog access, and the Oak Lodge excerpt, but no unrestricted public copy of the Oregon City section. Reasonable public-online recovery is therefore treated as exhausted for annual-closeout purposes. Remaining inspection is now `MF-062` (**YEAR-CLOSEOUT / MANUAL CALLOUT**), using FamilySearch Center/affiliate access or Oregon Historical Society. This changes the access state only; it does not supply or negate any 503/505 occupant.\n'''
    lead.write_text(s)

print('integrated 1916 online-gap manual callouts')
