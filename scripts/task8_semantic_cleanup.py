from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def p(path): return ROOT / path

def read(path): return p(path).read_text(encoding='utf-8')
def write(path, text): p(path).write_text(text, encoding='utf-8')

def rep(path, old, new, count=1):
    text = read(path)
    found = text.count(old)
    if found != count:
        raise RuntimeError(f'{path}: expected {count}, found {found} for {old[:90]!r}')
    write(path, text.replace(old, new, count))

# Remove duplicate legacy OQ-031 paragraph left after the first integration migration.
dup = '''\n\nWhere did the line fall between **C. Gates's Fifth Street Restaurant location** and **S. Wolf's remainder** in the visually verified 13 July sale report (`E-096`), and how did Gates's two-store hollow-tile replacement (`E-097`) map to modern 501/503/505? Two models remain live: Gates principally at 501 with Wolf beginning at 503, or Gates at 501+503 with Wolf beginning near 505. Recover the deed, permit/plans, dimensions, insurance records, and first exact-address tenants; do not decide from the 1925 use pattern alone.'''
rep('evidence/open-questions.md', dup, '')

# OHS title-abstract lead: remove obsolete later-Block-4 premise while preserving the index conflict/manual callout.
path = 'evidence/source-captures/ohs-mss1503-block4-lots3-4-title-abstract-lead.md'
rep(path,
'''3. Can the abstract tie modern Block 4 / Lots 3–4 to an earlier cadastral description or predecessor parcel?\n4. Does it show a 1922 fire-era transfer, mortgage, insurance, rebuilding, or value-related event?\n5. Can it separate the real-estate chains of **503** and **505**?''',
'''3. Can the abstract trace the **original Block 4 Lots 3–4** Harding chain into the 1922 Wolf/Gates division and later parcel splits?\n4. Does it show a 1922 fire-era transfer, mortgage, insurance, rebuilding, or value-related event?\n5. Can it distinguish historical lot/title boundaries from the later/current real-estate chains of **503** and **505**?''')

old_section = '''## Relationship to historic Block 26\n\nA separate primary 1906 source in `E-064` places the William Tell Hotel at Sixth & Main on **Lot 8, Block 26, Oregon City**.\n\nA visually verified 1913 assessment notice independently confirms that the original Oregon City system placed:\n\n- **Blocks 7, 6, 5, and 4** on one side of Fifth Street; and\n- **Block 26** immediately across Fifth, extending north toward Sixth Street.\n\nSource: `S-107` / `E-094`\n\nhttps://oregonnews.uoregon.edu/lccn/sn00063701/1913-10-23/ed-1/seq-8.pdf\n\nTherefore the modern/current `Block 4` description used for 503/505 is **not the same original block-numbering system** as the 1906/1913 Block 26 description. The OHS abstract may be especially useful in explaining when/how the later Block 4 description came into use.'''
new_section = '''## Relationship to historic Block 26 — Task 6 correction\n\nA separate primary 1906 source in `E-064` places the William Tell Hotel at Sixth & Main on **Lot 8, Block 26, Oregon City**. The visually verified 1913 assessment (`S-107` / `E-094`) simultaneously identifies **G. A. Harding at original Block 4 Lots 3–4** and separate owners in Block 26. Task 6 establishes that these are **different original physical blocks on opposite sides of Main**, not successive numbering systems.\n\nCurrent 503/505 legal-description leads remain in original **Block 4**; current 504 across Main remains in **Block 26 Lot 5**. The OHS abstract is therefore valuable as a potentially direct **Block 4 title-chain source**, especially for Harding → Wolf/Gates and later parcel splits. It is **not** being sought to explain any Block 26 → Block 4 conversion, because that conversion premise has been withdrawn.'''
rep(path, old_section, new_section)
rep(path,
'5. preserve any older legal descriptions, subdivision/replat references, assessment notations, and building/improvement references that precede current Block 4 wording.',
'5. preserve all legal descriptions, subdivision/replat references, assessment notations, lot splits, and building/improvement references that show how original Block 4 Lots 3–4 relate to later 503/505 parcel boundaries.')
rep(path,
'- S. Wolf, 1922 ownership, improvement ownership, and original Block 26-to-later Block 4 conversion: **unresolved**',
'- S. Wolf, 1922 ownership, improvement ownership, and the exact original-Block-4-to-later-parcel chain: **unresolved**')

# Task 2 retrieval audit: convert stale live cadastral conclusions and request language.
path = 'evidence/source-captures/1906-ordinance-357-retrieval-audit-2026-08-26.md'
rep(path,
'No new exact-address/lot conclusion is created by this note. The original Block 26 / later Block 4 distinction remains unresolved, and the working 501/503/505-to-Lot-5 alignment remains a strong inference rather than cadastral proof.',
'No new exact-address/lot conclusion was created by Task 2. **Task 6 later corrected the cadastral orientation:** original Block 4 is the odd-numbered 501/503/505/507 side, while Block 26 is opposite/even. Exact historic lot-to-address assignments still require the numbering plat/title/deed evidence.')
rep(path,
'- `RL-025`: recover the original ordinance and associated numbering plat/plan, with highest priority on Main Street between Fifth and Sixth / original Block 26.',
'- `RL-025`: recover the original ordinance and associated numbering plat/plan, with highest priority on the **original Block 4 odd-numbered frontage** between Fifth and Sixth; use Block 26 only as an opposite-side control.')
rep(path,
'> Please include any surviving plat, map, schedule, index, attachment, or other record showing the assigned street numbers for **Main Street between Fifth and Sixth Streets**, including the frontage historically described as **Block 26**, and especially numbers **501, 503, 505, and 507 Main**.',
'> Please include any surviving plat, map, schedule, index, attachment, or other record showing the assigned street numbers for **Main Street between Fifth and Sixth Streets**, especially the **original Block 4 odd-numbered frontage** containing **501, 503, 505, and 507 Main**. Please also include the opposite-side Block 26 frontage where useful for orientation.')
rep(path,
'- Exact mapping of 501/503/505/507 to original Block 26 lots/buildings under the official numbering system: **Unresolved**.\n- Original Block 26 / later-current Block 4 conversion: **Unresolved; do not merge the systems**.',
'- Exact mapping of 501/503/505/507 to original **Block 4** lots/buildings under the official numbering system: **Unresolved**.\n- Block 26 → Block 4 conversion for the target frontage: **Resolved as a false premise by Task 6**; they are separate original opposite-side blocks.')

# Task 3 visual-inspection checkpoint: remove old E-094 alignment and wrong target block references.
path = 'evidence/source-captures/ordinance-357-visual-inspection-task3-2026-08-26.md'
rep(path,
'- any direct mapping of **501, 503, 505, or 507 Main** to original Block 26 lots/buildings;\n- any connection between original Block 26 and later/current `(2) OREGON CITY, Block 4`.',
'- any direct mapping of **501, 503, 505, or 507 Main** to original Block 4 lots/buildings;\n- any cadastral lot-to-address assignment for the target frontage.')
old = '''The existing `E-094` working conclusion remains unchanged:\n\n- **501 / 503 / 505 ≈ original Block 26 Lot 5** — strong map/geometry inference;\n- **507 begins ≈ original Block 26 Lot 6** — strong map/geometry inference.\n\nThose relationships are not promoted to proven fact by Ordinance No. 357 because the ordinance's numbering schedule/plat has not been recovered.'''
new = '''Task 6 subsequently corrected the `E-094` cadastral orientation: the odd-numbered target frontage is original **Block 4**, not Block 26. Current legal-description leads place 503 in part Lot 4 and 505 in parts Lots 3–4, while historic 501's exact original lot remains unresolved.\n\nNothing in the surviving Ordinance 357 excerpt promotes any exact Block 4 lot-to-address relationship to proven fact because the ordinance's numbering schedule/plat has not been recovered.'''
rep(path, old, new)
rep(path,
'- Block 26 / Block 4 systems kept separate: **YES**.',
'- Correct target orientation (original Block 4 odd side; Block 26 opposite side) incorporated by Task 6: **YES**.')
rep(path,
'6. Any surviving Main Street sheet/schedule specifically showing Fifth-to-Sixth / original Block 26 and **501, 503, 505, 507 Main**.',
'6. Any surviving Main Street sheet/schedule specifically showing the Fifth-to-Sixth **original Block 4** odd-numbered frontage and **501, 503, 505, 507 Main**, with Block 26 used only as an opposite-side control.')

# Task 4 numbering-plat locator: remove stale 'unchanged' alignment and correct record request.
path = 'evidence/source-captures/1906-numbering-plat-locator-task4-2026-08-26.md'
rep(path,
'The existing working alignment remains unchanged: **501/503/505 ≈ original Block 26 Lot 5; 507 begins ≈ original Lot 6**. That is still a strong map/geometry inference, not cadastral or numbering-plat proof.',
'**Task 6 later corrected the cadastral orientation:** the odd-numbered 501/503/505/507 frontage is original **Block 4**, not Block 26. The plat remains essential because the exact original Block 4 lot/building assignments—especially historic 501 and the internal storefront boundaries—are still unresolved.')
rep(path,
'> Please search for the official Oregon City street/house-numbering plat or plan created in 1906 and filed with City Recorder W. A. Dimick. Contemporary Oregon City newspapers reported on 6 July 1906 that a plat designating the correct numbering had been filed with the Recorder, on 17 August 1906 that the completed numbering plat was in the Recorder’s office, and a City Recorder notice on 3 October 1913 stated that a plat and plan showing the proper street number for all Oregon City property remained on file. Please search Ordinance No. 357 supporting records, 1906 council proceedings, permanent maps/plans/drawings, engineering maps, street-name/house-numbering records, and any recorder-filed map or plat indexes. Please include the portion showing Main Street between Fifth and Sixth Streets, original Block 26, especially addresses 501, 503, 505 and 507 Main.',
'> Please search for the official Oregon City street/house-numbering plat or plan created in 1906 and filed with City Recorder W. A. Dimick. Contemporary Oregon City newspapers reported on 6 July 1906 that a plat designating the correct numbering had been filed with the Recorder, on 17 August 1906 that the completed numbering plat was in the Recorder’s office, and a City Recorder notice on 3 October 1913 stated that a plat and plan showing the proper street number for all Oregon City property remained on file. Please search Ordinance No. 357 supporting records, 1906 council proceedings, permanent maps/plans/drawings, engineering maps, street-name/house-numbering records, and any recorder-filed map or plat indexes. Please include the portion showing Main Street between Fifth and Sixth Streets, especially the **original Block 4 odd-numbered frontage at 501, 503, 505 and 507 Main**; include Block 26 across Main as an orientation control if shown.')

# Self-clean temporary files.
for temp in ['scripts/task8_semantic_cleanup.py', '.github/workflows/task8-semantic-cleanup.yml']:
    f = p(temp)
    if f.exists(): f.unlink()

print('Task 8 semantic cleanup applied')
