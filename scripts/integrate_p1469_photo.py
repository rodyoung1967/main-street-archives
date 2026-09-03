from pathlib import Path
import hashlib

TARGET = Path('media/photos/early-main-street/IMG-0732_1890-flood-6th-main-looking-southwest-cchs-p1469.jpg')
sha = hashlib.sha256(TARGET.read_bytes()).hexdigest()
size = TARGET.stat().st_size


def read(path):
    return Path(path).read_text(encoding='utf-8')


def write(path, text):
    Path(path).write_text(text, encoding='utf-8')


# Immutable-ID guards.
corpus = '\n'.join(read(p) for p in [
    'evidence/source-register.md',
    'evidence/evidence-register.md',
    'database/sources.yml',
    'database/evidence.yml',
    'media/photo-metadata-register.md',
])
for token in ('S-203', 'E-183', 'IMG-0732', 'P-1469'):
    if token in corpus:
        raise SystemExit(f'{token} already present/assigned; stop rather than reuse')

capture_path = Path('evidence/source-captures/1890-cchs-p1469-main-6th-looking-southwest-2026-09-03.md')
capture_path.write_text(f'''# CCHS P-1469 — 1890 Flood - Oregon City Main Street

Status: **VISUALLY VERIFIED institutional historic photograph; exact CCHS catalog record recovered online**  
Integration date: **3 September 2026**

## Institutional record

- Holding institution: Clackamas County Historical Society.
- Catalog platform: CatalogIt public collection.
- Object ID: **P-1469**.
- Catalog title: **1890 Flood - Oregon City Main Street**.
- Catalog date: **1890**.
- Catalog description: **Oregon City Main Street, 6th and Main, looking southwest. Unidentified people. Flooding. Debris.**
- Catalog entry slug: `1890-flood-oregon-city-main-street-1`.
- Public API lookup used for verification: `https://api.catalogit.app/api/public/search?query=P-1469&size=50`.
- Public high-resolution derivative preserved from CCHS/CatalogIt's published media.

## Repository preservation

- Source ID: `S-203`.
- Evidence ID: `E-183`.
- Media ID: `IMG-0732`.
- File: `{TARGET.as_posix()}`.
- SHA-256: `{sha}`.
- Bytes: {size}.
- JPEG magic bytes verified before integration.

## Historical-use boundary

The institutional record directly establishes the cataloged subject, date, intersection, and view direction. It does **not** by itself prove that any visible structure is the same physical building later numbered 501, 503, or 505 Main. Any such facade/building-continuity identification requires separate spatial comparison with Sanborn geometry, fixed landmarks, and other photographs.
''', encoding='utf-8')

p = 'evidence/source-register.md'
write(p, read(p).rstrip() + f'''\n\n## S-203 — Clackamas County Historical Society P-1469, 1890 Flood - Oregon City Main Street
Type: Institutional historic-photograph catalog record plus published image; **VISUALLY VERIFIED**.  
Holding institution: Clackamas County Historical Society.  
Object ID: `P-1469`.  
Catalog title: **1890 Flood - Oregon City Main Street**.  
Catalog description: **Oregon City Main Street, 6th and Main, looking southwest. Unidentified people. Flooding. Debris.**  
Catalog date: **1890**.  
Catalog lookup: `https://api.catalogit.app/api/public/search?query=P-1469&size=50`  
Repository image: `{TARGET.as_posix()}`  
SHA-256: `{sha}`  
Related evidence: `E-183`; media: `IMG-0732`.  
Record: `{capture_path.as_posix()}`.  
Notes: Institutional metadata directly establishes the cataloged intersection/view direction and 1890 date. It does not establish physical continuity between visible buildings and later 501/503/505 structures.
''')

p = 'evidence/evidence-register.md'
write(p, read(p).rstrip() + '''\n\n## E-183 — CCHS P-1469 1890 flood view from 6th and Main looking southwest
Type: Institutional historic-photograph metadata plus visually verified image; source `S-203`; media `IMG-0732`.  
Claims:
- Clackamas County Historical Society catalogs object `P-1469` as **1890 Flood - Oregon City Main Street**.
- The institutional description places the camera at **6th and Main, looking southwest** and describes unidentified people, flooding, and debris.
- The structured catalog date is **1890**.
- The photograph provides direct visual context for the Main/Fifth-Sixth commercial streetscape during the 1890 flood.
- It does not independently prove that a depicted structure is the same physical building later numbered 501, 503, or 505 Main.
Confidence: Very High for institutional object identity, cataloged date, intersection, view direction, and visible flood scene; unresolved for exact target-building continuity.  
Related sources: `S-203`.  
Related media: `IMG-0732`.  
Record: `evidence/source-captures/1890-cchs-p1469-main-6th-looking-southwest-2026-09-03.md`.
''')

p = 'media/photo-metadata-register.md'
write(p, read(p).rstrip() + f'''\n\n## IMG-0732 — CCHS P-1469, 1890 flood at 6th and Main looking southwest
File: `{TARGET.as_posix()}`  
Type: Historic photograph  
Status: `committed` / `VISUALLY VERIFIED`  
Source: `S-203`; evidence: `E-183`  
Institution: Clackamas County Historical Society  
Object ID: `P-1469`  
Catalog title: **1890 Flood - Oregon City Main Street**  
Catalog date: **1890**  
Catalog description: **Oregon City Main Street, 6th and Main, looking southwest. Unidentified people. Flooding. Debris.**  
Catalog lookup: `https://api.catalogit.app/api/public/search?query=P-1469&size=50`  
Published derivative source: `https://d8e7jbdw4fu0e.cloudfront.net/4813/3c630c60-b5ce-11f0-b5a3-a3a9be51ef91-vdUeg2T.lg@2x.jpg`  
SHA-256: `{sha}`  
File size: {size} bytes  
Interpretive limit: institutional metadata establishes the view and date; exact 501/503/505 facade/building continuity remains a separate spatial-analysis question.
''')

p = 'database/sources.yml'
write(p, read(p).rstrip() + f'''\n\n  - id: S-203
    name: Clackamas County Historical Society P-1469, 1890 Flood - Oregon City Main Street
    url: https://api.catalogit.app/api/public/search?query=P-1469&size=50
    notes: Institutional CatalogIt record. Object P-1469; cataloged 1890; description places view at 6th and Main looking southwest with unidentified people, flooding, and debris. Visually verified image preserved at {TARGET.as_posix()}. Does not independently prove continuity to later 501/503/505 buildings.
    repository_file: {TARGET.as_posix()}
    sha256: {sha}
    related_evidence:
    - E-183
    related_media:
    - IMG-0732
''')

p = 'database/evidence.yml'
write(p, read(p).rstrip() + '''\n\n  - id: E-183
    name: CCHS P-1469 1890 flood view from 6th and Main looking southwest
    type: Institutional historic-photograph metadata plus visually verified image
    claims:
      - CCHS catalogs P-1469 as 1890 Flood - Oregon City Main Street.
      - Institutional description places the view at 6th and Main looking southwest.
      - The photograph shows unidentified people, flooding, and debris.
      - The institutional record dates the photograph to 1890.
      - Exact continuity to later 501, 503, or 505 Main buildings is not established by this photograph alone.
    confidence: Very High for object identity, date, intersection, view direction, and visible scene; unresolved for exact target-building continuity.
    related_sources:
      - S-203
    related_media:
      - IMG-0732
''')

p = 'media/photos/inventory.md'
s = read(p)
for old, new in [
    ('**69 committed raster files**', '**70 committed raster files**'),
    ('**42 photographs/aerials**', '**43 photographs/aerials**'),
    ('**All 69 raster files', '**All 70 raster files'),
    ('### Street-level and early photographs — 4 files', '### Street-level and early photographs — 5 files'),
]:
    if old not in s:
        raise SystemExit(f'inventory anchor missing: {old}')
    s = s.replace(old, new, 1)
row = f'| `IMG-0732` | CCHS P-1469, 1890 flood, 6th and Main looking southwest | [`early-main-street/{TARGET.name}`](early-main-street/{TARGET.name}) | Committed published CCHS/CatalogIt derivative; visually verified. Institutional metadata establishes date/intersection/view direction; exact 501/503/505 building continuity remains unresolved. |\n'
anchor = '\n## Recent supplied-file reconciliation\n'
if anchor not in s:
    raise SystemExit('inventory insertion anchor missing')
s = s.replace(anchor, row + anchor, 1)
write(p, s)

p = 'media/photos/early-main-street/README.md'
s = read(p)
old = 'Status: **four street-level files are committed (`IMG-0722`–`IMG-0725`); four additional public-source full scenes are planned but have not been imported**'
new = 'Status: **five street-level files are committed (`IMG-0722`–`IMG-0725`, `IMG-0732`); three additional public-source full scenes remain planned**'
if old not in s:
    raise SystemExit('README status anchor missing')
s = s.replace(old, new, 1)
section = f'''\n## IMG-0732 — CCHS P-1469, 1890 flood at 6th and Main looking southwest

- File: `{TARGET.name}`
- Clackamas County Historical Society object `P-1469`.
- Catalog title: **1890 Flood - Oregon City Main Street**.
- Catalog description places the view at **6th and Main, looking southwest**; unidentified people, flooding, and debris.
- Catalog date: **1890**.
- Published CCHS/CatalogIt high-resolution derivative preserved and visually verified.
- Do not use this photograph alone to claim exact physical continuity to later 501/503/505 Main structures.

'''
marker = '\n## Committed exact-address photograph\n'
if marker not in s:
    raise SystemExit('README insertion anchor missing')
s = s.replace(marker, section + '## Committed exact-address photograph\n', 1)
write(p, s)

p = 'media/catalog.md'
s = read(p)
anchor = "| `IMG-0725` | `media/photo-metadata-register.md` | Committed 1910 George Young's Second Hand Store photograph with visible 505 doorway (`S-149` / `E-134`) |\n"
if anchor not in s:
    raise SystemExit('media catalog anchor missing')
s = s.replace(anchor, anchor + '| `IMG-0732` | `media/photo-metadata-register.md` | Committed CCHS P-1469 1890 flood photograph, 6th and Main looking southwest (`S-203` / `E-183`) |\n', 1)
write(p, s)

p = 'indexes/id-crosswalk.md'
write(p, read(p).rstrip() + f'''\n\n### CCHS P-1469 1890 flood photograph

| Source/evidence/media | Repository record | Boundary |
| --- | --- | --- |
| `S-203` / `E-183` / `IMG-0732` / CCHS `P-1469` | `{TARGET.as_posix()}`; `{capture_path.as_posix()}` | Institutional record directly establishes 1890, 6th and Main, looking southwest, flooding/debris. Exact continuity to later 501/503/505 buildings remains unresolved. |
''')

p = 'registers/research-log.md'
write(p, read(p).rstrip() + f'''\n\n## 2026-09-03 — Integrate CCHS P-1469 1890 flood photograph

- Recovered the authoritative Clackamas County Historical Society CatalogIt record for object **P-1469**, titled **1890 Flood - Oregon City Main Street**.
- The institutional description places the camera at **6th and Main, looking southwest**, with unidentified people, flooding, and debris; structured date **1890**.
- Preserved the published CCHS/CatalogIt high-resolution JPEG as `IMG-0732` at `{TARGET.as_posix()}`; SHA-256 `{sha}` ({size} bytes).
- Added `S-203` and `E-183`, synchronized Markdown/YAML records, photograph inventory, media navigation, crosswalk, and source capture.
- Preserved the building-continuity boundary: this photograph does not independently prove that a visible structure is the same building later numbered 501, 503, or 505 Main.
''')

print(f'Integrated P-1469 as IMG-0732; sha256={sha}; bytes={size}')
