#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re

IMAGE = Path('media/photos/early-main-street/IMG-0727_1890-flood-main-street-after-waters-resided-p1474.jpg')
EXPECTED_SHA256 = 'c6fc21c3acb6c2ea182510870c407b16c05cd303f31b6471ad2948dad31b58df'
EXPECTED_SIZE = 653119
ORIGINAL_NAME = '1890 Flood, after the water resided, looking north from 5th & Main Street, Oregon City, Oregon (503 & 505 1st on the laft & blacksmith visible on the right)(1).jpg'
CATALOG_URL = 'https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/1890-flood-main-street-after-waters-resided-oregon-city-oregon.'
SOURCE_NAME = 'Clackamas County Historical Society P-1474 — 1890 Flood Main Street After Waters Resided'
EVIDENCE_NAME = '1890 flood photograph of Main Street after waters resided, P-1474'


def read(path):
    return Path(path).read_text(encoding='utf-8')


def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + '\n\n' + block.rstrip() + '\n')


def replace_once(path, old, new):
    text = read(path)
    if old not in text:
        raise SystemExit(f'Expected text not found in {path}: {old!r}')
    write(path, text.replace(old, new, 1))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


# Hard guards: never reuse/renumber immutable IDs.
guards = [
    ('IMG-0727', 'media/photo-metadata-register.md', r'(?m)^## IMG-0727\b'),
    ('S-200', 'evidence/source-register.md', r'(?m)^## S-200\b'),
    ('E-179', 'evidence/evidence-register.md', r'(?m)^## E-179\b'),
    ('T-072', 'database/timeline.yml', r'(?m)^  - id: T-072$'),
    ('RL-048', 'evidence/research-leads.md', r'(?m)^## RL-048\b'),
]
for ident, path, pat in guards:
    if re.search(pat, read(path)):
        raise SystemExit(f'{ident} already assigned in {path}; stop rather than reuse/renumber.')

if not IMAGE.exists():
    raise SystemExit(f'Missing downloaded image {IMAGE}')
actual_sha = sha256(IMAGE)
actual_size = IMAGE.stat().st_size
if actual_sha != EXPECTED_SHA256 or actual_size != EXPECTED_SIZE:
    raise SystemExit(f'Image mismatch: sha={actual_sha}, size={actual_size}; expected sha={EXPECTED_SHA256}, size={EXPECTED_SIZE}')

# Dedicated visual-review record: institutional metadata and steward interpretation stay separate.
write('evidence/source-captures/1890-flood-main-street-p1474-visual-review-2026-09-02.md', f'''# 1890 flood — Main Street after waters resided — P-1474 visual review

Review date: **2 September 2026**  
Status: **VISUALLY VERIFIED HISTORIC PHOTOGRAPH; EXACT 501–505 FRONTAGE IDENTIFICATION REMAINS A PROJECT-STEWARD WORKING HYPOTHESIS PENDING SPATIAL CORROBORATION**

## Preserved source

- Media ID: `IMG-0727`
- Source ID: `S-200`
- Evidence ID: `E-179`
- Repository file: `{IMAGE.as_posix()}`
- Original supplied filename: `{ORIGINAL_NAME}`
- SHA-256: `{EXPECTED_SHA256}`
- Bytes: `{EXPECTED_SIZE}`
- Institutional catalog: {CATALOG_URL}
- Clackamas County Historical Society object: **P-1474**

## Institutional metadata — DOCUMENTED / DIRECT

The Clackamas County Historical Society catalog supplies:

- title: **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon.**
- object ID: **P-1474**
- description: **1890 Flood, after the water resided, Main Street, Oregon City, Oregon.**
- date made: **1890**
- place: **Oregon City, Clackamas County, Oregon, United States of America, North America**
- medium: **Photographic Paper**
- original size shown in the public catalog: **5 × 8 inches**
- original format shown in the public catalog: **Print-Photographic**

The supplied access image visibly carries a **Clackamas County Historical Society** watermark and depicts an early Main Street streetscape after flooding.

## Project-steward spatial interpretation — WORKING HYPOTHESIS

The project steward identifies the camera position/direction as **looking north from Fifth & Main** and identifies the first frontage on the **left** as the buildings associated with the later **501–505 Main** address range. The supplied filename also records the steward's observation that a blacksmith is visible on the right.

That address/camera interpretation is **not stated in the museum metadata supplied above** and no 501/503/505 number is visibly legible in the photograph. It must therefore remain separate from the institutional catalog record until tested against fixed landmarks, the 1890 Sanborn, street geometry, neighboring businesses/buildings, and other flood/streetscape views.

## Historical use and limits

This photograph is a high-value **pre-1911 structural/street-scene anchor** for the Main/Fifth frontage. If the steward's spatial identification is corroborated, it can help test how the future 501/503/505 frontage changed between the 1890 image, the corrected 1911 Sanborn Sheet 16, the 1922 fire/rebuild sequence, and the 1925 Sanborn.

It does **not** by itself prove:

- that any individual facade is exactly 501, 503, or 505;
- that the later numbered addresses were already in official use in 1890;
- ownership or business occupancy of the pictured structures;
- continuity between the photographed 1890 structures and the surviving modern 503/505 buildings.

See `RL-048` for the spatial-verification task.
''')

append_once('media/photo-metadata-register.md', '## IMG-0727 — 1890 Flood — Main Street After Waters Resided', f'''## IMG-0727 — 1890 Flood — Main Street After Waters Resided
File: `{IMAGE.as_posix()}`  
Original supplied filename: `{ORIGINAL_NAME}`  
Type: Historic photograph / flood aftermath streetscape  
Status: `committed`  
Source: Clackamas County Historical Society public catalog, object **P-1474** (`S-200`)  
Catalog URL: {CATALOG_URL}  
Catalog title: **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon.**  
Catalog description: **1890 Flood, after the water resided, Main Street, Oregon City, Oregon.**  
Catalog date: **1890**  
Catalog place: Oregon City, Clackamas County, Oregon, United States of America, North America  
Catalog medium: Photographic Paper  
Catalog original size/format: 5 × 8 inches; Print-Photographic  
SHA-256: `{EXPECTED_SHA256}`  
File size: {EXPECTED_SIZE} bytes  
Related evidence: `E-179`  
Related address records: `B-005` (501), `B-001` (503), `B-002` (505) — **candidate spatial relationship only**  
Visual note: supplied image visibly bears the Clackamas County Historical Society watermark and shows an early Main Street streetscape after flooding.  
Project-steward interpretation: camera is looking north from Fifth & Main; the first frontage at left is identified by the steward as the later 501–505 frontage, with a blacksmith visible on the right. This is retained as a **WORKING HYPOTHESIS**, not museum catalog metadata or direct address proof.  
Rights note: rights/reproduction terms were not supplied in the steward metadata; preserve the access copy and attribution without inferring a license.''')

# Update definitive photo inventory counts and add the new item.
inv = read('media/photos/inventory.md')
inv = inv.replace('- **69 committed raster files** in the repository.', '- **70 committed raster files** in the repository.', 1)
inv = inv.replace('- **42 photographs/aerials**, all stored together under `media/photos/`.', '- **43 photographs/aerials**, all stored together under `media/photos/`.', 1)
inv = inv.replace('### Street-level and early photographs — 4 files', '### Street-level and early photographs — 5 files', 1)
row = f'| `IMG-0727` | 1890 flood aftermath, Main Street, CCHS object P-1474 | [`early-main-street/IMG-0727_1890-flood-main-street-after-waters-resided-p1474.jpg`](early-main-street/IMG-0727_1890-flood-main-street-after-waters-resided-p1474.jpg) | Committed exact supplied-file match; museum establishes 1890/Main Street/P-1474. Steward identifies north-from-Fifth/Main and first-left 501–505 frontage; that spatial mapping remains a working hypothesis. |\n'
anchor = '| `IMG-0725` | George Young\'s Second Hand Store, 505 Main, 1910 | [`early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg`](early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg) | Committed exact supplied-file match; storefront and 505 doorway are visible. |\n'
if row not in inv:
    if anchor not in inv:
        raise SystemExit('Inventory IMG-0725 anchor not found')
    inv = inv.replace(anchor, anchor + row, 1)
rec = f'| `{ORIGINAL_NAME}` | `{EXPECTED_SHA256}` | `IMG-0727` — `{IMAGE.as_posix()}` | Exact byte match; CCHS P-1474 metadata integrated; steward 501–505 mapping retained as working hypothesis |\n'
recent_anchor = 'The original filenames remain preserved in the canonical media records.'
if rec not in inv:
    if recent_anchor not in inv:
        raise SystemExit('Inventory recent-reconciliation anchor not found')
    inv = inv.replace(recent_anchor, rec + '\n' + recent_anchor, 1)
write('media/photos/inventory.md', inv)

# Update early-photo README status and add a dedicated section.
readme = read('media/photos/early-main-street/README.md')
readme = readme.replace('Status: **four street-level files are committed (`IMG-0722`–`IMG-0725`); four additional public-source full scenes are planned but have not been imported**', 'Status: **five standalone street-level files are committed (`IMG-0722`–`IMG-0725`, `IMG-0727`); four additional public-source full scenes are planned but have not been imported**', 1)
readme = readme.replace('The committed set comprises three exact byte matches to recent steward-supplied JPEGs (`IMG-0723`–`IMG-0725`) and one provenance-unresolved crop (`IMG-0722`).', 'The committed set comprises four exact byte matches to steward-supplied JPEGs (`IMG-0723`–`IMG-0725`, `IMG-0727`) and one provenance-unresolved crop (`IMG-0722`).', 1)
section = '''## Committed 1890 flood streetscape — CCHS P-1474

- `IMG-0727` — `IMG-0727_1890-flood-main-street-after-waters-resided-p1474.jpg`
- Clackamas County Historical Society object **P-1474**, cataloged **1890**, title **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon.**
- Institutional metadata identifies Main Street/Oregon City but does not assign 501/503/505 or a camera direction.
- Project steward identifies the view as looking north from Fifth & Main and the first left frontage as the later 501–505 frontage. Preserve that as a **working hypothesis** pending Sanborn/landmark comparison (`S-200`, `E-179`, `RL-048`).
- Do not use the photograph alone as proof of current-building continuity, ownership, or business occupancy.
'''
if '## Committed 1890 flood streetscape — CCHS P-1474' not in readme:
    readme = readme.replace('## Committed exact-address photograph\n', section + '\n## Committed exact-address photograph\n', 1)
write('media/photos/early-main-street/README.md', readme)

# Source and evidence registers + YAML mirrors.
append_once('evidence/source-register.md', '## S-200 — ' + SOURCE_NAME, f'''## S-200 — {SOURCE_NAME}
Source/location: {CATALOG_URL}  
Repository file: `{IMAGE.as_posix()}`  
Original supplied filename: `{ORIGINAL_NAME}`  
Type: Primary historic photograph / institutional catalog metadata; **VISUALLY VERIFIED**  
Related evidence: `E-179`; media `IMG-0727`.  
Notes: Clackamas County Historical Society catalog object **P-1474** titles/describes an 1890 Main Street flood-aftermath photograph in Oregon City and lists Photographic Paper, 5 × 8 inches, Print-Photographic. The supplied image is preserved byte-for-byte (SHA-256 `{EXPECTED_SHA256}`) and visibly bears the CCHS watermark. The steward's Fifth/Main camera position and 501–505-frontage identification are recorded separately as a working hypothesis, not institutional metadata.''')

append_once('evidence/evidence-register.md', '## E-179 — ' + EVIDENCE_NAME, f'''## E-179 — {EVIDENCE_NAME}
Type: Primary historic photograph / institutional catalog metadata / project-steward spatial interpretation  
Sources: `S-200`  
Claims: CCHS catalog object **P-1474** directly identifies an **1890** photograph of **Main Street, Oregon City** after flood waters had resided/receded. The supplied image visibly depicts the flooded/aftermath Main Street streetscape and bears the CCHS watermark. The project steward identifies the camera as looking north from Fifth & Main and the first left frontage as the later 501–505 frontage; because the museum metadata does not state that camera/address mapping and no target number is visibly legible, that mapping remains a **WORKING HYPOTHESIS** pending spatial corroboration. The photograph does not establish ownership, occupancy, official 1890 address numbering, or continuity with the surviving 503/505 buildings.  
Confidence: **Very High** for institutional date/place/object metadata and visible streetscape; **Working hypothesis** for exact Fifth/Main camera position and 501–505 frontage mapping.  
Related record: `evidence/E-179-1890-flood-main-street-p1474.md`''')

append_once('database/sources.yml', '  - id: S-200\n', f'''  - id: S-200
    name: {SOURCE_NAME}
    url: {CATALOG_URL}
    notes: >-
      Visually verified steward-supplied historic photograph, exact bytes preserved as {IMAGE.as_posix()} (SHA-256 {EXPECTED_SHA256}). CCHS object P-1474 catalogs an 1890 Main Street flood-aftermath scene in Oregon City. Steward Fifth/Main camera and 501–505-frontage identification remains a working hypothesis, not museum metadata. Related evidence E-179 and media IMG-0727.''')

append_once('database/evidence.yml', '  - id: E-179\n', f'''  - id: E-179
    name: {EVIDENCE_NAME}
    type: Primary historic photograph / institutional catalog metadata / project-steward spatial interpretation
    claims:
      - Clackamas County Historical Society object P-1474 directly catalogs an 1890 Main Street flood-aftermath photograph in Oregon City.
      - The supplied image visibly depicts the early Main Street streetscape and bears the CCHS watermark.
      - The project steward identifies the view as north from Fifth/Main with the first left frontage corresponding to the later 501–505 range; museum metadata does not state that mapping, so it remains a working hypothesis.
      - The photograph does not prove official 1890 address numbering, ownership, occupancy, or continuity with the surviving 503/505 buildings.
    confidence: Very High for institutional date/place/object metadata and visible streetscape; Working hypothesis for exact Fifth/Main camera position and 501–505 frontage mapping.
    related_sources: [S-200]
    related_buildings: [B-005, B-001, B-002]
    repository_file: evidence/E-179-1890-flood-main-street-p1474.md''')

write('evidence/E-179-1890-flood-main-street-p1474.md', f'''# E-179 — {EVIDENCE_NAME}

Type: Primary historic photograph / institutional catalog metadata / project-steward spatial interpretation.  
Source: `S-200`; media: `IMG-0727`; related address records: `B-005`, `B-001`, `B-002`.

## Documented / direct

The Clackamas County Historical Society public catalog identifies object **P-1474** as **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon.**, dated **1890**, with the description **1890 Flood, after the water resided, Main Street, Oregon City, Oregon.** The catalog gives Oregon City / Clackamas County / Oregon and medium **Photographic Paper**. The supplied access image visibly carries the CCHS watermark and shows the early Main Street streetscape after flooding.

## Working hypothesis — exact spatial mapping

The project steward identifies the image as looking **north from Fifth & Main** and identifies the first frontage on the **left** as the buildings associated with the later **501–505 Main** address range. This is important project knowledge, but the supplied institutional metadata does not state the camera location/direction or the numbered-address mapping, and no 501/503/505 number is visibly legible in the photograph.

Therefore the exact spatial identification is classified **WORKING HYPOTHESIS** pending comparison against the 1890 Sanborn, fixed landmarks, neighboring structures/businesses, street geometry, and the other 1890 flood images.

## Historical significance and limits

If spatially corroborated, `IMG-0727` becomes an unusually early visual anchor for testing the physical evolution of the future 501/503/505 frontage before the corrected 1911 Sanborn Sheet 16 and the 1922–1925 physical-change sequence. It does not by itself establish official address numbering in 1890, business or property ownership, individual storefront identities, or continuity with the surviving modern 503/505 structures.
''')

# New research lead for the exact spatial claim.
append_once('evidence/research-leads.md', '## RL-048 — Verify P-1474 1890 flood photograph camera position and 501–505 frontage mapping', '''## RL-048 — Verify P-1474 1890 flood photograph camera position and 501–505 frontage mapping
Use `IMG-0727` / `S-200` / `E-179` to test the project-steward identification that CCHS object P-1474 is looking north from Fifth & Main and that the first left frontage corresponds to the later 501–505 address range. Compare the 1890 Sanborn (`SM-004` / `S-017`), street width/alignment, corner geometry, blacksmith and post-office/other fixed landmarks, utility poles, rooflines and adjacent structures against the other 1890 flood views and later streetscapes. Keep the address assignment as a **WORKING HYPOTHESIS** until the geometry is independently corroborated.''')

# Add a timeline record and shared 501/503/505 timeline rows.
append_once('database/timeline.yml', '  - id: T-072\n', '''  - id: T-072
    date: "1890"
    summary: Clackamas County Historical Society photograph P-1474 depicts Main Street after the 1890 flood waters had resided/receded. Project steward identifies the view as north from Fifth/Main with the first left frontage as the later 501–505 range; exact spatial mapping remains a working hypothesis.
    confidence: Very High for catalog date/place/object metadata and visible streetscape; Working hypothesis for Fifth/Main camera and 501–505 mapping.
    related_evidence: [E-179]
    related_sources: [S-200]
    related_buildings: [B-005, B-001, B-002]''')

append_once('timeline.md', '## 1890 — CCHS P-1474 flood-afterward Main Street photograph', '''## 1890 — CCHS P-1474 flood-afterward Main Street photograph
Clackamas County Historical Society object **P-1474** is cataloged as an **1890** photograph of Main Street, Oregon City, after flood waters had resided/receded (`S-200` / `E-179` / `IMG-0727`, `T-072`). The project steward identifies the camera as looking north from Fifth & Main and the first left frontage as the later **501–505 Main** range. Because the institutional metadata does not make that address/camera identification and no target number is visibly legible, the exact mapping remains a **WORKING HYPOTHESIS** (`RL-048`). The image is an early structural comparison source, not proof that the pictured buildings are the surviving 503/505 structures.''')

shared_row = '| 1890 | CCHS P-1474 flood-afterward Main Street photograph; project steward identifies view as north from Fifth/Main with first left frontage as the later 501–505 range. | **Direct** for cataloged 1890 Main Street scene; **Working hypothesis** for exact camera/address mapping; no present-building continuity implied. | `S-200`; `E-179`; `IMG-0727`; `T-072`; `RL-048` |\n'
for path in ['timelines/501-main.md', 'timelines/503-main.md', 'timelines/505-main.md']:
    text = read(path)
    if shared_row not in text:
        anchor = '| 1844–1900 |'
        pos = text.find(anchor)
        if pos < 0:
            raise SystemExit(f'Could not find early timeline anchor in {path}')
        end = text.find('\n', pos) + 1
        text = text[:end] + shared_row + text[end:]
        write(path, text)

# Link the photo carefully in all three building records without assigning a specific facade.
building_note = '''## 1890 CCHS P-1474 flood photograph — candidate shared frontage context
CCHS object **P-1474** is cataloged as an **1890 Main Street, Oregon City** flood-afterward photograph and is preserved as `IMG-0727` (`S-200` / `E-179`). The project steward identifies the camera as looking north from Fifth & Main and the first left frontage as the later **501–505 Main** range. Because the institutional metadata does not state that numbered-address mapping and no target number is visibly legible, the exact assignment remains a **WORKING HYPOTHESIS** (`RL-048`). Use the photo as a pre-1911 structural/streetscape comparison source; do not infer ownership, occupancy, or continuity with the surviving current building from the image alone.'''
for path in ['buildings/501-main.md', 'buildings/503-main.md', 'buildings/505-main.md']:
    append_once(path, '## 1890 CCHS P-1474 flood photograph — candidate shared frontage context', building_note)

# Add the new early anchor to the physical-change checkpoint.
append_once('evidence/source-captures/1911-1925-physical-change-research-checkpoint-2026-09-02.md', '## 2 September 2026 supplement — 1890 P-1474 photographic anchor', '''## 2 September 2026 supplement — 1890 P-1474 photographic anchor
`IMG-0727` / `S-200` / `E-179` now preserves a CCHS photograph cataloged **1890** and described as Main Street after the flood waters had resided/receded. The project steward identifies the view as north from Fifth/Main and the first left frontage as the later 501–505 range. That exact spatial mapping is not institutional metadata and remains a working hypothesis (`RL-048`), but the image creates a valuable pre-1911 comparison target for the corrected 1911 Sheet 16 and the 1922–1925 physical-change analysis.''')

append_once('indexes/id-crosswalk.md', '| `IMG-0727` | `S-200` / `E-179`; `B-005`, `B-001`, `B-002`; `T-072`; `RL-048` |', f'''| `IMG-0727` | `S-200` / `E-179`; `B-005`, `B-001`, `B-002`; `T-072`; `RL-048` | CCHS P-1474, 1890 flood-afterward Main Street photograph. Museum metadata establishes 1890/Main Street; steward north-from-Fifth/Main and 501–505 mapping remains a working hypothesis. Repository file `{IMAGE.as_posix()}`. |''')

append_once('ARCHIVE_INDEX.md', '## 1890 CCHS flood photograph — P-1474 / IMG-0727', '''## 1890 CCHS flood photograph — P-1474 / IMG-0727
[Visual review](evidence/source-captures/1890-flood-main-street-p1474-visual-review-2026-09-02.md) and [`IMG-0727`](media/photos/early-main-street/IMG-0727_1890-flood-main-street-after-waters-resided-p1474.jpg) preserve Clackamas County Historical Society object **P-1474**, cataloged as an **1890 Main Street** flood-afterward photograph (`S-200` / `E-179`). Project-steward identification of the camera as north from Fifth/Main and the first-left frontage as later 501–505 is retained as a **working hypothesis** pending spatial corroboration (`RL-048`).''')

append_once('registers/research-log.md', '## 2 September 2026 — CCHS P-1474 1890 flood photograph preserved', f'''## 2 September 2026 — CCHS P-1474 1890 flood photograph preserved
- Verified the steward-supplied JPEG was not already present in the repository and assigned `IMG-0727`; exact file SHA-256 `{EXPECTED_SHA256}`.
- Preserved CCHS object **P-1474** at `{IMAGE.as_posix()}` and registered `S-200` / `E-179`.
- Institutional metadata records 1890 / Main Street / Oregon City / Photographic Paper; it does not state 501/503/505 or camera direction.
- Preserved the project-steward identification (north from Fifth/Main; first left frontage = later 501–505) separately as a **working hypothesis**, with `RL-048` for Sanborn/landmark verification.
- Linked the photograph as shared pre-1911 structural context to 501 (`B-005`), 503 (`B-001`) and 505 (`B-002`) without asserting current-building continuity or occupancy.
- No annual closeout status changed.''')

print('P-1474 integration records written successfully.')
