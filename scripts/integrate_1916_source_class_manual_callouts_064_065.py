from pathlib import Path

manual=Path('MANUAL-FOLLOWUP.md')
s=manual.read_text()
if '### MF-064 — 1916 Morning Enterprise microfilm review' not in s:
    anchor='## 1917 ONLINE COMPLETE — remaining manual work\n'
    block='''### MF-064 — 1916 Morning Enterprise microfilm review\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Review the 1916 *Morning Enterprise* daily on microfilm. University of Oregon confirms the title continued 1911–1933 and was issued on microfilm, but Oregon City's digitization project exposes the public online run only through 23 December 1913. Oregon Historical Society's microfilm inventory holds *Morning Enterprise*, June 8, 1911–Nov. 2, 1933, Cabinet I, Drawer 5. Search target addresses, Fifth/Main, occupants/businesses, moves, construction/demolition, pool/billiard/cigar/soft-drink activity, property transactions, Harding and Hylton.\n\n### MF-065 — Clackamas County 1916 Tax List\n\n**Class: YEAR-CLOSEOUT / MANUAL CALLOUT.** Inspect the physical **Clackamas County Tax List, 1916 (1 volume)** identified by the Oregon State Archives county-records inventory at the Museum of the Oregon Territory, Halon Room. Target Original Oregon City Block 4 Lots 3–4, G. A. Harding and other owners/agents, valuations/improvements/transfers, and address/parcel linkage relevant to 501/503/503½/505/507 Main. No public online 1916 page images were identified.\n\n'''
    if anchor not in s: raise SystemExit('manual anchor missing')
    s=s.replace(anchor,block+anchor,1)
    old='Last amended: **13 September 2026** — converted three exhausted 1916 online-first gaps into year-closeout manual callouts `MF-061`–`MF-063`; no existing MF ID was renumbered or removed.'
    new='Last amended: **13 September 2026** — converted exhausted 1916 online gaps into year-closeout manual callouts `MF-061`–`MF-065`; no existing MF ID was renumbered or removed.'
    if old in s: s=s.replace(old,new,1)
    manual.write_text(s)

cp=Path('evidence/source-captures/1916-online-audit-checkpoint.md')
s=cp.read_text()
if 'MF-064' not in s:
    marker='The year remains **IN PROGRESS / NOT ONLINE COMPLETE**.'
    note='''The 1916 *Morning Enterprise* daily is now classified as manual-only for 1916 (`MF-064`): the title survives on microfilm through 1933, but the public digitized Oregon City run ends in 1913. The Clackamas County **1916 Tax List** is likewise classified as physical/manual (`MF-065`) based on the Oregon State Archives county inventory. The Sanborn/fire-insurance-map class is closed for 1916-specific online retrieval: the public Oregon City series brackets 1916 with 1911 and 1925 editions and exposes no 1916 Sanborn edition. See `1916-source-class-closure-morning-enterprise-tax-sanborn-2026-09-13.md`.\n\n'''
    if marker not in s: raise SystemExit('checkpoint marker missing')
    s=s.replace(marker,note+marker,1)
    cp.write_text(s)

print('integrated MF-064 and MF-065 source-class closures')
