from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')


def replace_exact(path, old, new, count=1):
    text = read(path)
    actual = text.count(old)
    if actual != count:
        raise RuntimeError(f'{path}: expected {count} matches, found {actual}: {old[:80]!r}')
    write(path, text.replace(old, new, count))


def replace_section(path, start, next_start, new_section):
    text = read(path)
    i = text.find(start)
    if i < 0:
        raise RuntimeError(f'{path}: missing start {start}')
    j = text.find(next_start, i + len(start))
    if j < 0:
        raise RuntimeError(f'{path}: missing next section {next_start}')
    write(path, text[:i] + new_section.rstrip() + '\n\n' + text[j:])

# Canonical evidence item for the Task 7 synthesis.
e108 = '''# E-108 — Block 4 Harding Address-to-Property Bridge

## Evidence type
Cross-source cadastral/property synthesis using visually verified primary evidence, current legal-description leads, and explicitly bounded inference.

## Core findings

1. The corrected odd-numbered 501/503/505/507 Main frontage is original Oregon City **Block 4**, not Block 26 (`E-094`).
2. The visually verified 23 October 1913 assessment lists **G. A. Harding at Block 4 Lots 3 and 4**.
3. Current county-derived legal-description leads place **503 in part Lot 4**, **505 in parts Lots 3 and 4**, and the modern consolidated **507 parcel in parts Lots 2, 3 and 4**. These modern boundaries are not backdated automatically.
4. Independent primary advertisements place the **Chicago Store at 505 Main** in 1911–1913. A 25 December 1913 *Oregon City Courier* primary OCR/text report says the Chicago clothing-store building was owned by **George Harding**. Because that page image has not yet been visually certified, the Harding-building wording remains **primary OCR/text-only**, while the combined Harding↔505 connection is a **strong multi-source inference**.
5. The visually verified 13 July 1922 sale report says Harding's Main/Fifth property group was divided between **C. Gates**, who received the Fifth Street Restaurant location, and **S. Wolf**, who received the remainder (`E-096`). The visually verified 20 July fire report names **S. Wolf of Portland** as owner of the ignition building (`E-103`). The close dates, same property cluster and same S. Wolf wording create a **strong property-chain inference**, not deed-level title proof.
6. The August 1922 Gates replacement had two ground-floor storerooms (`E-097`). That is compatible with more than one modern-address mapping, so the exact Gates/Wolf line remains unresolved.

## Address classifications

- **501 Main:** proven numbered premises by 1912/1913 and part of the corrected Block 4 frontage; exact original lot unresolved. Gates principally at 501 remains plausible, not proven.
- **503 Main:** current legal-description lead overlaps Block 4 Lot 4. It may be the start of Wolf's 1922 remainder or part of Gates's two-store replacement.
- **505 Main:** current legal-description lead overlaps Block 4 Lots 3 and 4. The Chicago Store exact-address evidence plus the 1913 Harding building-owner text create the strongest current pre-1922 Harding↔505 bridge, but not deed-level parcel proof.
- **507 Main:** current consolidated parcel overlaps Block 4 Lots 2–4; that modern shape must not be backdated to the pre-1967 storefronts.

## Competing 1922 storefront models

- **Model A:** Gates principally at 501; Wolf begins at 503. Compatible with the working 503-ignition / 505-pool-hall reconstruction.
- **Model B:** Gates's two Main-facing rooms became 501+503; Wolf begins near 505.

Neither model is established. **501 remains a live fire-origin alternative** until the Fifth Street Restaurant footprint is proved. The working 503-ignition / 505-adjoining-pool-hall reconstruction remains a hypothesis, not a finding.

## Highest-value unresolved bridges

1. OHS MSS 1503 Box 19 title abstract — Block 4 Lots 3 & 4 / Main & Fifth (`E-095`).
2. Recorded Harding → S. Wolf / C. Gates deed(s), legal descriptions and dimensions.
3. Gates/Junken 1922 permit, plans or assessment sketch.
4. Original 1906 numbering plat/plan.
5. Recorded/official target-parcel deed or assessor images for 503 and 505.

## Sources and related evidence

Primary/official source IDs used directly: `S-032`, `S-107`, `S-109`, `S-110`, `S-111`, `S-112`, `S-113`, `S-117`.

Related evidence: `E-094`, `E-095`, `E-096`, `E-097`, `E-103`, `E-104`.

Detailed synthesis: `evidence/source-captures/task7-address-to-property-bridge-2026-08-26.md`.

Primary OCR/text-only Harding-owner capture: `evidence/source-captures/1913-chicago-store-fire-george-harding-owner.md`.

## Confidence

- Block 4 orientation and 1913 Harding Lots 3–4: **Very High / visually verified primary evidence**.
- Modern lot-overlap descriptions: **High / strong current legal-description leads; official recorded images still desirable**.
- Harding↔505 by December 1913: **Strong multi-source inference**, with the owner wording **primary OCR/text-only pending visual certification**.
- Harding 1913 property context → July 1922 Harding sale group: **Strong inference; intervening deed chain unresolved**.
- July 1922 Wolf remainder → Wolf-owned ignition building: **High / strong cross-source inference; deed and exact storefront unresolved**.
- Exact Gates/Wolf dividing wall and exact 501/503/505 ignition address: **Unresolved**.
'''
write('evidence/E-108-block4-harding-address-property-bridge.md', e108)

# Human-readable evidence register + YAML mirror.
ereg = read('evidence/evidence-register.md')
if '## E-108 —' in ereg:
    raise RuntimeError('E-108 already exists in evidence register')
ereg += '''\n\n## E-108 — Block 4 Harding Address-to-Property Bridge
Type: Cross-source cadastral/property synthesis  
Dates: 1911–1925 evidence synthesized 26 August 2026  
Sources: `S-032`, `S-107`, `S-109`, `S-110`, `S-111`, `S-112`, `S-113`, `S-117`  
Related record: `evidence/E-108-block4-harding-address-property-bridge.md`  
Claims: Task 7 establishes a defensible bridge from corrected original **Block 4** through **G. A. Harding's Lots 3–4**, the Harding/505 Chicago Store building-owner lead, and the July 1922 Harding→Gates/Wolf property division. The evidence strongly links Wolf's newly reported remainder to the Wolf-owned fire-origin building but does **not** identify the exact 501/503/505 dividing wall. Current 503 overlaps Lot 4 and 505 overlaps Lots 3–4 as current legal-description leads; modern boundaries are not backdated. Two Gates/Wolf storefront models remain live, and 501 remains a fire-origin alternative.  
Confidence: Very High for Block 4 orientation and Harding Lots 3–4; High/strong inference for the Harding-property/Wolf chain; Strong multi-source inference for Harding↔505 with the December 1913 owner wording still primary OCR/text-only; exact 1922 storefront mapping unresolved.
'''
write('evidence/evidence-register.md', ereg)

yml = read('database/evidence.yml')
if '\n  - id: E-108\n' in yml:
    raise RuntimeError('E-108 already exists in YAML')
yml += '''\n\n  - id: E-108
    name: Block 4 Harding Address-to-Property Bridge
    type: Cross-source cadastral/property synthesis
    claims:
      - Corrected original Block 4 provides the cadastral frame for the odd-numbered 501/503/505/507 frontage, and the 1913 assessment lists G. A. Harding at Block 4 Lots 3 and 4.
      - Current legal-description leads place 503 in part Lot 4 and 505 in parts Lots 3 and 4; those modern boundaries are not automatically backdated to 1922.
      - Chicago Store exact-address evidence at 505 plus the December 1913 primary OCR/text report naming George Harding as building owner creates a strong Harding-to-505 bridge, pending visual certification of that owner wording.
      - The July 1922 Harding sale division and the fire report strongly connect S. Wolf's reported remainder to the Wolf-owned ignition building, but do not establish the exact 501/503/505 storefront boundary.
      - Gates-at-501 and Gates-at-501-plus-503 remain competing hypotheses; the 503-ignition/505-pool-hall reconstruction remains a working hypothesis and 501 remains live.
    confidence: Very High for Block 4 orientation and Harding Lots 3-4; High/strong inference for the Harding property/Wolf chain; Strong multi-source inference for Harding-to-505 with owner wording OCR/text-only pending visual certification; exact storefront mapping unresolved.
    related_sources:
      - S-032
      - S-107
      - S-109
      - S-110
      - S-111
      - S-112
      - S-113
      - S-117
    related_buildings:
      - B-001
      - B-002
      - B-003
      - B-005
    repository_file: evidence/E-108-block4-harding-address-property-bridge.md
'''
write('database/evidence.yml', yml)

# Correct stale standalone E-095 interpretation.
e095 = read('evidence/E-095-ohs-mss1503-main-fifth-title-abstract-index.md')
old = '''## Historical significance and limits\n\nThe index row strongly overlaps the later/current Block 4 parcel-description problem around 503/505 and possibly part of 507 Main. It is therefore a high-priority route for testing:\n\n- the Lot 5 Barlow/David ownership chain from the 1913 assessment toward 1922;\n- whether **S. Wolf** appears in land or building/improvement ownership;\n- the reported later Wolf-family ownership of 503;\n- the mechanism connecting original Block 26 to later/current Block 4 descriptions.\n\nThe actual title abstract has not been found online, retrieved, or visually inspected. Accordingly, `E-095` proves **none** of those property-history propositions. It is a verified archival index finding plus an open **MANUAL CALLOUT**.'''
new = '''## Historical significance and limits\n\nTask 6 corrected the cadastral orientation: **Block 4 is the original target-side block**, not a later replacement for Block 26. The 1913 assessment independently lists **G. A. Harding at Block 4 Lots 3 and 4**, while current 503/505 legal-description leads overlap those same lots. The index row is therefore a potentially direct correct-side title-chain lead for testing:\n\n- the Harding ownership chain for Block 4 Lots 3–4;\n- the July 1922 Harding → **S. Wolf / C. Gates** division;\n- whether **S. Wolf** appears in land or building/improvement ownership;\n- the reported later Wolf-family ownership of 503;\n- the historical relationship between original lot lines and later 503/505 parcel divisions.\n\nThe actual title abstract has not been found online, retrieved, or visually inspected. Accordingly, `E-095` proves **none** of those property-history propositions. It is a verified archival index finding plus an open **MANUAL CALLOUT**. See `E-108` for the current address-to-property synthesis.'''
if old not in e095:
    raise RuntimeError('E-095 stale interpretation block did not match')
e095 = e095.replace(old, new, 1).replace('S. Wolf, 1922 ownership, improvement ownership, and cadastral conversion: **Unresolved pending retrieval**', 'S. Wolf, 1922 ownership, improvement ownership, and exact parcel/title chain: **Unresolved pending retrieval**')
write('evidence/E-095-ohs-mss1503-main-fifth-title-abstract-index.md', e095)

# Correct open questions and connect Task 7.
replace_exact(
    'evidence/open-questions.md',
    '## OQ-004 — 503 / 505 Boundary\nStatus: **Original-lot context narrowed; modern legal/physical boundary remains open.** `E-094` strongly aligns the original Block 26 Lot 5/Lot 6 division with the **505/507 wall**, placing 501/503/505 approximately within Lot 5. That does not resolve the internal 503/505 parcel/wall/depth relationship. What records prove the modern widths, depths, common wall and any rear additions?',
    '## OQ-004 — 503 / 505 Boundary\nStatus: **Cadastral orientation corrected; modern legal/physical boundary remains open.** `E-094` establishes that the odd-numbered frontage is original **Block 4**, not Block 26. Current legal-description leads place **503 in part Lot 4** and **505 in parts Lots 3 and 4**, but those modern parcel lines must not be backdated automatically. `E-108` connects this Block 4 context to Harding and the 1922 property group while leaving the exact 503/505 historical wall unresolved. What recorded deeds, assessor maps, surveys, wall/structural evidence and rear-addition records prove the modern and historical widths, depths and common boundary?'
)
replace_section(
    'evidence/open-questions.md',
    '## OQ-031 — July 1922 Gates / Wolf Frontage Division',
    '',
    '''## OQ-031 — July 1922 Gates / Wolf Frontage Division
Status: **NARROWED BY `E-108`; exact dividing line remains unresolved.** Task 7 establishes a strong property-group bridge from original Block 4 and Harding Lots 3–4 into the July 1922 Harding → Gates/Wolf division and then to the Wolf-owned ignition building. It still does not locate the dividing wall.

Two models remain live: **(A)** Gates principally at 501, with Wolf beginning at 503; or **(B)** Gates's two Main-facing storerooms became 501+503, with Wolf beginning near 505. The working 503-ignition / 505-adjoining-pool-hall model remains compatible with Model A but is not proved, and **501 remains a live alternative**.

Highest-value resolution records: the OHS MSS 1503 Block 4 Lots 3–4 abstract, Harding→Wolf/Gates deed(s), Gates/Junken permit or plans, original numbering plat, and first post-fire exact-address tenants. Do not decide from the 1925 use pattern alone.'''
)

# RL-025 was still pointed at the wrong side of Main.
replace_exact(
    'evidence/research-leads.md',
    'Highest priority is the Main Street frontage of **Block 26 between Fifth and Sixth**, because the plat may directly establish the original 1906 numbers for the storefronts later known as 501, 503, 505, and 507.',
    'Highest priority is the odd-numbered Main Street frontage of original **Block 4 between Fifth and Sixth**, because Task 6 established that this—not Block 26—is the 501/503/505/507 side. Block 26 remains an opposite-side geographic control.'
)

# Replace stale 1913 ownership caution with the corrected method note.
write('evidence/source-captures/1913-building-vs-land-ownership-caution-for-1922-wolf-search.md', '''# 1913 building-owner vs. assessed-lot-owner caution — corrected Block 4 framework

Status: **CADASTRAL ORIENTATION CORRECTED; PRIMARY OWNER WORDING OCR/TEXT-ONLY; 1922 SALE/FIRE SEQUENCE VISUALLY VERIFIED**

This note preserves the useful methodological caution from the earlier research while withdrawing its obsolete Block 26 target-side model.

## Corrected cadastral frame

Task 6 (`E-094`) established that the odd-numbered 501/503/505/507 frontage is original **Block 4**. The 23 October 1913 assessment, visually verified as `S-107`, lists **G. A. Harding at Block 4 Lots 3 and 4**. Block 26 Lots 5–8 are on the opposite/even side of Main and must not be used as the target 503/505 land chain.

## Harding building-owner evidence at the 505 address context

Independent primary advertisements place the **Chicago Store at 505 Main** in 1911–1913 (`S-032` / `E-026`). The 25 December 1913 *Oregon City Courier* primary OCR/text report says the Chicago clothing-store building was owned by **George Harding**. The page image has not yet been visually certified, so that owner wording remains **primary OCR/text-only**.

Combined with Harding's visually verified Block 4 Lots 3–4 assessment entry and current 503/505 lot-overlap leads, the evidence supports a **strong multi-source Harding↔505 property/building inference**, not a deed-level statement that the exact modern 505 parcel existed in the same form.

## 1922 implication

The visually verified 13 July 1922 sale report (`E-096` / `S-111`) divides Harding's Main/Fifth property group between **C. Gates** (Fifth Street Restaurant location) and **S. Wolf** (remainder). The visually verified 20 July fire report (`E-103` / `S-117`) names S. Wolf of Portland as owner of the ignition building. This creates a strong immediate property-chain inference while leaving deed mechanics and the exact 501/503/505 wall unresolved.

## Method rule retained

Property ownership, assessed land ownership, building/improvement ownership, business operation and newspaper owner wording are separate evidentiary categories. A land assessment that omits a reported building owner does not by itself disprove the building-owner report; conversely, a newspaper owner label does not prove fee title.

Search both:
- deeds, grantor/grantee indexes, title abstracts, tax/assessment land records; and
- improvement assessments, fire insurance, leases, mortgages, permits and building-sale notices.

## Current resolution targets

1. OHS MSS 1503 Box 19 — Block 4 Lots 3 & 4 / Main & Fifth (`E-095`).
2. Harding → S. Wolf / C. Gates recorded deed(s).
3. Gates/Junken 1922 plans/permit/assessment sketch.
4. Official recorded/assessor parcel images for 503 and 505.
5. Visual certification of the 25 December 1913 Harding-owner article.

See `E-108` and `evidence/source-captures/task7-address-to-property-bridge-2026-08-26.md` for the integrated address-to-property classification.
''')

# Link E-108 into address and ownership registers.
for addr in ['501 Main Street', '503 Main Street', '505 Main Street', '507 Main Street']:
    pass
text = read('registers/address-register.md')
text = text.replace('`E-096`, `E-097`, `E-104` | Task 6 places', '`E-096`, `E-097`, `E-104`, `E-108` | Task 6 places', 1)
text = text.replace('`E-097`, `E-098`, `E-099` | Kwality', '`E-097`, `E-098`, `E-099`, `E-108` | Kwality', 1)
text = text.replace('`E-100`, `E-101`, `E-102` | Current legal-description', '`E-100`, `E-101`, `E-102`, `E-108` | Current legal-description', 1)
text = text.replace('`E-045`, `E-094`, `E-095` | Original Block 4 frontage', '`E-045`, `E-094`, `E-095`, `E-108` | Original Block 4 frontage', 1)
write('registers/address-register.md', text)

text = read('registers/ownership-timeline.md')
text = text.replace('`E-094` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 505', '`E-094`, `E-108` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 505', 1)
text = text.replace('`E-094` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 503', '`E-094`, `E-108` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 503', 1)
text = text.replace('`E-096` / `S-111` | Very High for published wording; deed pending', '`E-096`, `E-108` / `S-111` | Very High for published wording; deed pending', 1)
text = text.replace('Visually verified 20 Jul. fire report; cross-reference `E-096` | Very High', 'Visually verified 20 Jul. fire report; cross-reference `E-096`, `E-108` | Very High', 1)
write('registers/ownership-timeline.md', text)

# Building pages: link evidence and append a concise current bridge note.
for path in ['buildings/501-main.md','buildings/503-main.md','buildings/505-main.md','buildings/507-harding-building.md']:
    text = read(path)
    if '`E-108`' not in text.split('\n', 12)[0:12]:
        # add E-108 to the first Related evidence line without assuming its exact list
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith('- Related evidence:') and '`E-108`' not in line:
                lines[idx] = line + ', `E-108`'
                break
        text = '\n'.join(lines) + ('\n' if read(path).endswith('\n') else '')
    if '## Task 7 Address-to-Property Bridge' not in text:
        text += '''\n\n## Task 7 Address-to-Property Bridge\n\n`E-108` integrates the corrected original Block 4 framework with Harding's 1913 Lots 3–4 ownership, current lot-overlap leads, the July 1922 Harding→Gates/Wolf division, and the Wolf-owned ignition-building report. It strengthens the property-group chronology but **does not establish the exact Gates/Wolf storefront wall or fire-origin number**. Modern parcel boundaries are not backdated automatically.\n'''
    write(path, text)

# Map comparison: make E-108 part of the working reconstruction.
text = read('maps/sanborn-comparison-503-505-507.md')
if '- `E-108` — integrated Block 4 Harding address-to-property bridge' not in text:
    marker = '- `S-112`, `S-113` — visually verified 17–18 August 1922 Gates corner-rebuild reports\n'
    if marker not in text:
        raise RuntimeError('map source-set marker missing')
    text = text.replace(marker, marker + '- `E-108` — integrated Block 4 Harding address-to-property bridge and storefront-classification synthesis\n', 1)
    text += '''\n\n## Task 7 Integrated Address-to-Property Bridge\n\n`E-108` now provides the controlling synthesis for using this map with cadastral/property evidence. The proven framework is original **Block 4** with Harding at Lots 3–4 in 1913; current 503 overlaps Lot 4 and current 505 overlaps Lots 3–4 as current legal-description leads. The July 1922 property division still permits both Gates-principally-at-501 and Gates-at-501+503 models. The 1925 Sanborn use pattern may test compatibility but must not be backdated as proof of the 1922 wall.\n'''
write('maps/sanborn-comparison-503-505-507.md', text)

# Crosswalk: add E-108 to the four relevant buildings.
text = read('indexes/id-crosswalk.md')
text = text.replace('`E-094`–`E-099`, `E-103`;', '`E-094`–`E-099`, `E-103`, `E-108`;', 1)
text = text.replace('`E-094`–`E-103`;', '`E-094`–`E-103`, `E-108`;', 1)
text = text.replace('Original-building evidence `E-016`, `E-017`, `E-020`, `E-021`, `E-045`, `E-094`;', 'Original-building evidence `E-016`, `E-017`, `E-020`, `E-021`, `E-045`, `E-094`, `E-108`;', 1)
text = text.replace('`E-103`, `E-104`;', '`E-103`, `E-104`, `E-108`;', 1)
write('indexes/id-crosswalk.md', text)

# Timeline: remove remaining live wrong-side guidance and add the integrated bridge.
text = read('timeline.md')
text = text.replace('Its recorded narrative gives lots in that portion—including target Block 26—as **at least 66 feet front by 100 feet back**, with 10-foot alleys (`E-094` / `S-108`). This direct plat evidence supersedes the former 50-foot general-context model for Block 26.', 'Its recorded narrative gives Applegate-surveyed lots in that portion **at least 66 feet front by 100 feet back**, with 10-foot alleys (`E-094` / `S-108`). Task 6 corrected the target odd-numbered frontage to original **Block 4**; Block 26 is retained as the opposite-side control.', 1)
text = text.replace('## 1906 — formal street numbering and Block 26 reconstruction anchors', '## 1906 — formal street numbering and opposite-side Block 26 control', 1)
text = text.replace('This fixed north-end lot anchor, combined with the missing 1906 numbering plat and Sanborn maps, may allow the remaining Block 26 lots to be mapped toward Fifth Street (`RL-026`). No direct 1906 source has yet been found showing demolition or replacement of the predecessor buildings corresponding to later 501/503/505.', 'This fixes an important **opposite-side** Block 26 control at Sixth/Main. It must not be used to walk southward into the odd-numbered 501/503/505/507 frontage; that reconstruction now begins with original **Block 4** (`RL-026`, `E-108`). No direct 1906 source has yet been found showing demolition or replacement of the predecessor buildings corresponding to later 501/503/505.', 1)
if '## 1922 — integrated Harding / Gates / Wolf property bridge' not in text:
    anchor = '## 1924'
    idx = text.find(anchor)
    if idx < 0:
        raise RuntimeError('timeline 1924 anchor missing')
    insert = '''## 1922 — integrated Harding / Gates / Wolf property bridge\n`E-108` synthesizes the corrected original Block 4 framework with the 1913 Harding Lots 3–4 assessment, the strong Harding↔505 Chicago Store building-owner lead, the July 1922 Harding property division, and the Wolf-owned ignition-building report. The property-group chain is strong, but the exact Gates/Wolf wall is unresolved: Gates principally at 501 and Gates at 501+503 remain competing models. Do not promote the working 503-ignition / 505-pool-hall model to fact, and keep 501 live until the restaurant footprint is proved.\n\n'''
    text = text[:idx] + insert + text[idx:]
write('timeline.md', text)

# Source register reverse-link updates for the primary sources most central to E-108.
text = read('evidence/source-register.md')
for old, new in [
    ('Related evidence: `E-026`  \nNotes: Primary advertisements place The Chicago Store at 505 Main.', 'Related evidence: `E-026`, `E-108`  \nNotes: Primary advertisements place The Chicago Store at 505 Main.'),
    ('Related evidence: `E-094`; cross-reference `E-064`', 'Related evidence: `E-094`, `E-108`; cross-reference `E-064`'),
    ('Related evidence: `E-095`\nRepository source capture:', 'Related evidence: `E-095`, `E-108`\nRepository source capture:'),
    ('Related evidence: `E-096`', 'Related evidence: `E-096`, `E-108`'),
    ('Related evidence: `E-097`', 'Related evidence: `E-097`, `E-108`'),
    ('Related evidence: `E-103`', 'Related evidence: `E-103`, `E-108`'),
]:
    text = text.replace(old, new)
write('evidence/source-register.md', text)

# Database sources reverse links where the same source entries already have related_evidence lists.
text = read('database/sources.yml')
# conservative list insertion: only add under known source blocks if E-108 absent
for sid in ['S-032','S-107','S-109','S-110','S-111','S-112','S-113','S-117']:
    start = text.find(f'  - id: {sid}\n')
    if start < 0:
        raise RuntimeError(f'missing {sid} in sources YAML')
    end = text.find('\n  - id: S-', start + 1)
    if end < 0:
        end = len(text)
    block = text[start:end]
    if 'E-108' in block:
        continue
    if '    related_evidence:\n' in block:
        block = block.replace('    related_evidence:\n', '    related_evidence:\n      - E-108\n', 1)
        text = text[:start] + block + text[end:]
    # If the source has no reverse relationship field, leave it rather than inventing schema.
write('database/sources.yml', text)

# ARCHIVE_INDEX navigation: include the new canonical evidence note if evidence section exists.
text = read('ARCHIVE_INDEX.md')
if 'E-108-block4-harding-address-property-bridge.md' not in text:
    marker = 'evidence/E-094-original-plat-block26-lot5-boundary.md'
    if marker in text:
        line_end = text.find('\n', text.find(marker))
        text = text[:line_end+1] + '- `evidence/E-108-block4-harding-address-property-bridge.md` — integrated Block 4 / Harding / 1922 address-to-property bridge.\n' + text[line_end+1:]
    else:
        text += '\n- `evidence/E-108-block4-harding-address-property-bridge.md` — integrated Block 4 / Harding / 1922 address-to-property bridge.\n'
write('ARCHIVE_INDEX.md', text)

# Self-clean temporary migration files in the resulting commit.
for temp in ['scripts/task8_integrate_address_bridge.py', '.github/workflows/task8-integrate.yml']:
    p = ROOT / temp
    if p.exists():
        p.unlink()

print('Task 8 integration applied')
