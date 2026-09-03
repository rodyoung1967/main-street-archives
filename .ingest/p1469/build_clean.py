from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

SOURCE_ID = "S-203"
EVIDENCE_ID = "E-183"
MEDIA_ID = "IMG-0732"
OBJECT_ID = "P-1469"
TARGET = Path("media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg")
CAPTURE = Path("evidence/source-captures/1890-cchs-p1469-main-street-flood-photo-2026-09-03.md")
CATALOG_API = "https://api.catalogit.app/api/public/search?query=P-1469&size=50"
CATALOG_PAGE = "https://hub.catalogit.app/clackamas-county-historical-society/folder/entry/1890-flood-oregon-city-main-street-1"
EXPECTED_ENTRY_UUID = "de65a6a0-9b1e-11eb-b3ef-53e7205a00b4"
EXPECTED_SLUG = "1890-flood-oregon-city-main-street-1"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append(path, text):
    p = Path(path)
    current = p.read_text(encoding="utf-8").rstrip()
    p.write_text(current + "\n\n" + text.strip() + "\n", encoding="utf-8")


def assert_free(marker, paths):
    for path in paths:
        if marker in read(path):
            raise SystemExit(f"{marker} already appears in {path}; stop rather than reuse/overwrite")


assert_free(SOURCE_ID, ["evidence/source-register.md", "database/sources.yml"])
assert_free(EVIDENCE_ID, ["evidence/evidence-register.md", "database/evidence.yml"])
assert_free(MEDIA_ID, ["media/photo-metadata-register.md", "media/photos/inventory.md", "media/catalog.md"])
assert_free(OBJECT_ID, ["media/photo-metadata-register.md", "evidence/source-register.md"])

catalog = json.loads(Path("/tmp/p1469.json").read_text(encoding="utf-8"))
entries = [e for e in catalog.get("entries", []) if e.get("properties", {}).get("hasCatalogNumber", {}).get("value_text") == OBJECT_ID]
if len(entries) != 1:
    raise SystemExit(f"Expected exactly one {OBJECT_ID} CatalogIt entry, found {len(entries)}")
entry = entries[0]
if entry.get("id") != EXPECTED_ENTRY_UUID or entry.get("slug") != EXPECTED_SLUG:
    raise SystemExit("CatalogIt P-1469 entry identity changed; stop for review")

props = entry["properties"]
title = props["hasName"]["value_text"]
description = props["hasDescription"]["value_text"]
made = props["hasCreateOrManufactureInfo"]["value"]
year = made["hasMadeDate"]["value_fuzzydaterange"]["fuzzydate_from"]["fuzzydate_value"]
media = entry.get("media", [])
if not media:
    raise SystemExit("CatalogIt entry has no media")
selected = media[0]
derivs = selected.get("derivatives", {})
image_url = derivs.get("public_highres_2x", {}).get("path") or derivs.get("public_highres", {}).get("path")
if not image_url:
    raise SystemExit("CatalogIt entry has no public high-resolution derivative")
media_uuid = selected.get("uuid")

if not TARGET.exists():
    raise SystemExit(f"Expected downloaded image at {TARGET}")
raw = TARGET.read_bytes()
if not raw.startswith(b"\xff\xd8\xff"):
    raise SystemExit("Downloaded P-1469 file is not a JPEG")
sha = hashlib.sha256(raw).hexdigest()
size = len(raw)

try:
    from PIL import Image
    with Image.open(TARGET) as im:
        width, height = im.size
        fmt = im.format
except Exception as exc:
    raise SystemExit(f"Could not verify image with Pillow: {exc}")
if fmt != "JPEG":
    raise SystemExit(f"Unexpected image format {fmt}")

capture = f'''# CCHS P-1469 — 1890 Flood - Oregon City Main Street

Integration date: **3 September 2026**  
Evidence state: **DOCUMENTED / DIRECT for the institutional catalog metadata and preserved image association**  
Visual-use boundary: **do not use this image alone to assign an exact 501/503/505 facade, building identity, ownership, or continuity**

## Institutional record

- Holding institution: **Clackamas County Historical Society**
- Entry/Object ID: **{OBJECT_ID}**
- CatalogIt entry UUID: `{EXPECTED_ENTRY_UUID}`
- Catalog slug: `{EXPECTED_SLUG}`
- Catalog title: **{title}**
- Catalog description: **{description}**
- Date made: **{year}**
- Classification: **Photograph**
- Public catalog page: {CATALOG_PAGE}
- Public API lookup: {CATALOG_API}

## Preserved repository image

- Media ID: `{MEDIA_ID}`
- Repository file: `{TARGET.as_posix()}`
- CatalogIt media UUID: `{media_uuid}`
- Public derivative used for recovery: {image_url}
- Dimensions: **{width} × {height}**
- Format: JPEG
- SHA-256: `{sha}`
- Bytes: {size}

## Recovery and provenance note

The project steward had already supplied a photograph identified as the CCHS 1890 Main Street flood view at 6th and Main looking southwest, but the temporary GitHub staging branch retained only incomplete base64 fragments and could not reconstruct a valid JPEG. Rather than commit corrupt bytes, this integration recovered the image from the exact CCHS CatalogIt entry **P-1469** and preserved its current public high-resolution derivative.

The repository does **not** claim this recovered derivative is byte-identical to the earlier steward upload. The institutional object identity, catalog title, date, description, and image association are direct from CCHS; byte identity to the earlier local upload remains unproved.

## Historical-use boundary

CCHS directly catalogs the scene as Oregon City Main Street at **6th and Main, looking southwest**, with flooding, debris, and unidentified people. This is strong location/context evidence for the 1890 flood streetscape. It is not, by itself, an exact-address identification of 501, 503, or 505 Main and does not prove that any pictured structure is the same physical building as a later structure at those addresses.
'''
write(CAPTURE, capture)

source_md = f'''## {SOURCE_ID} — Clackamas County Historical Society photograph P-1469, 1890 Main Street flood
Type: Institutional historic-photograph catalog record and preserved public image derivative; **CATALOG METADATA VERIFIED**.  
Holding institution: Clackamas County Historical Society.  
Entry/Object ID: `{OBJECT_ID}`.  
Catalog title: **{title}**.  
Catalog description: **{description}**  
Date made: **{year}**.  
CatalogIt entry UUID: `{EXPECTED_ENTRY_UUID}`; slug `{EXPECTED_SLUG}`.  
Catalog page: {CATALOG_PAGE}  
API lookup: {CATALOG_API}  
Repository image: `{TARGET.as_posix()}` (`{MEDIA_ID}`), SHA-256 `{sha}`, {width}×{height} JPEG, {size} bytes.  
Source capture: `{CAPTURE.as_posix()}`.  
Related evidence: `{EVIDENCE_ID}`.  
Notes: CCHS directly identifies the scene as 6th and Main looking southwest during the 1890 flood. Do not use this source alone to assign an exact 501/503/505 facade or physical-building continuity. The earlier steward-supplied file was not recoverable byte-for-byte from the temporary staging fragments; the committed file is the exact current CCHS public high-resolution derivative.'''
append("evidence/source-register.md", source_md)

evidence_md = f'''## {EVIDENCE_ID} — CCHS P-1469 1890 Main Street flood scene at 6th and Main
Type: Institutional historic-photograph catalog metadata plus preserved image; source `{SOURCE_ID}`; media `{MEDIA_ID}`.  
Evidence state: **DOCUMENTED / DIRECT** for the institutional title, date, location description, and image association.  
Claims:
- Clackamas County Historical Society catalogs object **{OBJECT_ID}** as **{title}** and dates it to **{year}**.
- The catalog description places the photograph at **6th and Main, looking southwest** and identifies flooding, debris, and unidentified people.
- The preserved repository image is the public high-resolution derivative attached to that exact institutional record.
- The source does **not** independently establish an exact 501/503/505 address for a particular pictured facade and does not establish building continuity to later structures.
Confidence: **Very High** for the CCHS catalog metadata and image association; exact target-frontage/facade interpretation remains separate.  
Source capture: `{CAPTURE.as_posix()}`.'''
append("evidence/evidence-register.md", evidence_md)

source_yml = f'''  - id: {SOURCE_ID}
    name: Clackamas County Historical Society photograph P-1469, 1890 Main Street flood
    url: {CATALOG_PAGE}
    notes: >-
      CCHS catalogs P-1469 as "{title}" ({year}) and describes the scene as 6th and Main looking southwest, with unidentified people, flooding, and debris. The repository preserves the current CCHS public high-resolution derivative as {MEDIA_ID}. Exact 501/503/505 facade identity and building continuity are not asserted. The prior steward upload could not be reconstructed byte-for-byte from incomplete staging fragments.
    repository_file: {TARGET.as_posix()}
    sha256: {sha}
    related_evidence:
    - {EVIDENCE_ID}
    related_media:
    - {MEDIA_ID}'''
append("database/sources.yml", source_yml)

evidence_yml = f'''  - id: {EVIDENCE_ID}
    name: CCHS P-1469 1890 Main Street flood scene at 6th and Main
    type: Institutional historic-photograph catalog metadata plus preserved image
    claims:
    - CCHS catalogs P-1469 as "{title}" and dates it to {year}.
    - The CCHS description places the scene at 6th and Main looking southwest and identifies flooding, debris, and unidentified people.
    - The repository image is the public high-resolution derivative attached to that exact CCHS record.
    - The photograph alone does not establish an exact 501/503/505 facade or continuity to later buildings.
    confidence: Very High for institutional catalog metadata and image association; exact target-frontage interpretation remains separate.
    related_sources:
    - {SOURCE_ID}
    related_media:
    - {MEDIA_ID}
    repository_file: {CAPTURE.as_posix()}'''
append("database/evidence.yml", evidence_yml)

media_md = f'''## {MEDIA_ID} — CCHS P-1469, 1890 Main Street flood at 6th and Main
File: `{TARGET.as_posix()}`  
Type: Historic photograph / institutional public derivative  
Status: `committed`  
Source: `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`  
Holding institution / object: Clackamas County Historical Society, **{OBJECT_ID}**  
Catalog title: **{title}**  
Catalog description: **{description}**  
Date made: **{year}**  
Catalog entry UUID: `{EXPECTED_ENTRY_UUID}`  
CatalogIt media UUID: `{media_uuid}`  
Public catalog page: {CATALOG_PAGE}  
Recovered derivative: {image_url}  
Dimensions: {width} × {height}  
SHA-256: `{sha}`  
File size: {size} bytes  
Provenance note: the temporary steward-upload staging chunks were incomplete and could not reconstruct a valid JPEG. This committed file is the exact current CCHS public high-resolution derivative for P-1469; byte identity to the earlier steward upload is not claimed.  
Historical-use limit: the institutional record directly supplies the 6th/Main southwest location context, but this image alone does not assign an exact 501/503/505 facade or prove physical-building continuity.'''
append("media/photo-metadata-register.md", media_md)

inv_path = "media/photos/inventory.md"
inv = read(inv_path)
patterns = [
    (r'- \*\*(\d+) committed raster files\*\* in the repository\.', lambda m: f'- **{int(m.group(1))+1} committed raster files** in the repository.'),
    (r'- \*\*(\d+) photographs/aerials\*\*, all stored together under `media/photos/`\.', lambda m: f'- **{int(m.group(1))+1} photographs/aerials**, all stored together under `media/photos/`.'),
    (r'### Street-level and early photographs — (\d+) files', lambda m: f'### Street-level and early photographs — {int(m.group(1))+1} files'),
]
for pat, repl in patterns:
    inv, n = re.subn(pat, repl, inv, count=1)
    if n != 1:
        raise SystemExit(f"Inventory count pattern failed: {pat}")
row = f'| `{MEDIA_ID}` | CCHS {OBJECT_ID}; {title}; {year}; 6th/Main looking southwest | [`early-main-street/{TARGET.name}`](early-main-street/{TARGET.name}) | Committed CCHS public high-resolution derivative; exact institutional object identity and scene description established. Byte identity to the earlier steward upload is not claimed; exact 501/503/505 facade mapping remains separate. |\n'
anchor = "\n## Recent supplied-file reconciliation\n"
if anchor not in inv:
    raise SystemExit("Inventory reconciliation anchor missing")
inv = inv.replace(anchor, row + anchor, 1)
recovery_row = f'| `Oregon City Main Street, 6th & Main, looking southwest down main. (Clackamas County Historical Society).jpg` (steward-supplied identification; exact original bytes not recoverable from staging) | not available | `{MEDIA_ID}` — `{TARGET.as_posix()}` | Recovered from exact CCHS {OBJECT_ID} record as current public high-resolution derivative; **not claimed as an exact byte match** to the earlier upload. |\n'
marker = "\nThe original filenames remain preserved in the canonical media records."
if marker not in inv:
    raise SystemExit("Inventory supplied-file table anchor missing")
inv = inv.replace(marker, recovery_row + marker, 1)
write(inv_path, inv)

readme_path = "media/photos/early-main-street/README.md"
readme = read(readme_path)
readme, n = re.subn(
    r'Status: \*\*four street-level files are committed \(`IMG-0722`–`IMG-0725`\); four additional public-source full scenes are planned but have not been imported\*\*',
    f'Status: **five standalone street-level files are committed (`IMG-0722`–`IMG-0725`, `{MEDIA_ID}`); three additional public-source full scenes remain planned**',
    readme,
    count=1,
)
if n != 1:
    raise SystemExit("Early-photo README status line changed; stop for review")
section = f'''\n## Committed CCHS {OBJECT_ID} 1890 flood photograph\n\n- `{MEDIA_ID}` — `{TARGET.name}`\n- Clackamas County Historical Society object **{OBJECT_ID}**, catalog title **{title}**.\n- CCHS dates the image **{year}** and describes it as **6th and Main, looking southwest**, with unidentified people, flooding, and debris.\n- The committed JPEG is the current CCHS public high-resolution derivative ({width}×{height}); SHA-256 `{sha}`.\n- The earlier steward-supplied image was incompletely staged, so byte identity to that upload is not claimed.\n- Do not use this photograph alone to assign a specific 501/503/505 facade or physical-building continuity.\n\n'''
marker = "\n## Committed exact-address photograph\n"
if marker not in readme:
    raise SystemExit("Early-photo README insertion anchor missing")
readme = readme.replace(marker, section + "## Committed exact-address photograph\n", 1)
write(readme_path, readme)

catalog_path = "media/catalog.md"
cat = read(catalog_path)
row = f'| `{MEDIA_ID}` | `media/photo-metadata-register.md` | Committed CCHS {OBJECT_ID} 1890 Main Street flood photograph, 6th/Main looking southwest (`{SOURCE_ID}` / `{EVIDENCE_ID}`) |\n'
marker = "\n## Deprecated Older Paths\n"
if marker not in cat:
    raise SystemExit("Media catalog insertion anchor missing")
cat = cat.replace(marker, row + marker, 1)
write(catalog_path, cat)

cross = f'''### CCHS {OBJECT_ID} 1890 flood photograph\n\n| Media/source/evidence | Repository record | Boundary |\n| --- | --- | --- |\n| `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}` / CCHS `{OBJECT_ID}` | `{TARGET.as_posix()}`; `{CAPTURE.as_posix()}` | CCHS directly supplies 1890 and 6th/Main southwest scene metadata; do not infer an exact 501/503/505 facade or building continuity from the image alone. |'''
append("indexes/id-crosswalk.md", cross)

log = f'''## 2026-09-03 — Commit CCHS {OBJECT_ID} 1890 Main Street flood photograph\n\n- Recovered the exact Clackamas County Historical Society CatalogIt record **{OBJECT_ID}**, title **{title}**, dated **{year}**, described as **6th and Main, looking southwest** with flooding, debris, and unidentified people.\n- The abandoned temporary staging chunks were incomplete and could not reconstruct a valid JPEG; corrupt bytes were not committed.\n- Preserved the current CCHS public high-resolution derivative as `{MEDIA_ID}` at `{TARGET.as_posix()}` ({width}×{height}, SHA-256 `{sha}`, {size} bytes).\n- Assigned `{SOURCE_ID}` and `{EVIDENCE_ID}` without renumbering existing records and synchronized Markdown/YAML source/evidence registers, media metadata, photograph inventory, media catalog, early-photo README, crosswalk, and source capture.\n- Preserved the uncertainty boundary: byte identity to the earlier steward upload is not claimed, and the photograph alone does not prove an exact 501/503/505 facade or building continuity.'''
append("registers/research-log.md", log)

print(json.dumps({
    "source": SOURCE_ID,
    "evidence": EVIDENCE_ID,
    "media": MEDIA_ID,
    "object": OBJECT_ID,
    "target": TARGET.as_posix(),
    "sha256": sha,
    "bytes": size,
    "dimensions": [width, height],
    "image_url": image_url,
}, indent=2))
