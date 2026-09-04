from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "2008.008.003.104"
MEDIA_ID = "IMG-0743"
SOURCE_ID = "S-214"
EVIDENCE_ID = "E-194"
TIMELINE_ID = "T-077"

SOURCE_NAME = "Clackamas County Historical Society 2008.008.003.104, Main Street, Oregon City"
EVIDENCE_NAME = "CCHS 1890-1899 Main Street view provides pre-numbering Fifth-Sixth block streetscape context"

REPO_IMAGE = "media/photos/early-main-street/IMG-0743_1890-1899-main-street-oregon-city-cchs-2008-008-003-104.jpg"
API_CAPTURE = "evidence/source-captures/1890-1899-cchs-2008-008-003-104-main-street-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1890-1899-cchs-2008-008-003-104-main-street-sixth-fifth-context-2026-09-04.md"
SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET_CATALOG, "size": 50})
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "Main Street, Oregon City looking south from 6th onto 5th st.jpg",
    "width": 2048,
    "height": 1420,
    "bytes": 527507,
    "sha256": "69de483d0541125560cbdd263435aa0a69847975c0aacff8a90f732e220605a0",
}
CATALOG_METADATA = {
    "title": "Main Street, Oregon City",
    "entry_object_id": TARGET_CATALOG,
    "description": "Main Street, Oregon City",
    "date_made": "1890 - 1899",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_number": "Stevens 104",
    "stevens_photo_number": "102",
    "other_photo_number": "Bill Howell #2000",
}
STEWARD_VIEWPOINT_NOTE = (
    "The project-steward supplied filename identifies the scene as looking south from Sixth Street "
    "toward Fifth Street on Main Street. This wording is preserved as steward metadata, not as CCHS catalog text."
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def append_inline_id(path: str, prefix: str, ident: str) -> None:
    text = read(path)
    lines = text.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            if f"`{ident}`" not in line:
                lines[i] = line.rstrip() + f", `{ident}`"
                changed = True
            break
    if changed:
        write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def add_entity_yaml_list_item(path: str, entity_id: str, field: str, item: str) -> None:
    text = read(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Could not find {entity_id} in {path}")
    next_m = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + next_m.start() if next_m else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    field_match = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if not field_match:
        raise SystemExit(f"Could not find {field} list for {entity_id} in {path}")
    field_abs_end = m.start() + field_match.end()
    after = text[field_abs_end:end]
    next_field = re.search(r"(?m)^    [a-zA-Z0-9_]+:", after)
    insert_at = field_abs_end + (next_field.start() if next_field else len(after))
    insertion = f"\n      - {item}"
    text = text[:insert_at].rstrip("\n") + insertion + "\n" + text[insert_at:].lstrip("\n")
    write(path, text)


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def catalog_number(d):
    try:
        return d["properties"]["hasCatalogNumber"]["value_text"]
    except (KeyError, TypeError):
        return None


def find_matching_dict(obj):
    if isinstance(obj, dict):
        if catalog_number(obj) == TARGET_CATALOG:
            return obj
        for value in obj.values():
            found = find_matching_dict(value)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_matching_dict(value)
            if found is not None:
                return found
    return None


def choose_derivative(entry):
    candidates = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path"):
                continue
            if "thumbnail" in key or key in {"complementary_color", "dominant_color"}:
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                candidates.append((w * h, w, h, key, val["path"]))
    if not candidates:
        raise SystemExit("No public image derivative found in the exact CCHS record.")
    candidates.sort(reverse=True)
    _, w, h, key, url = candidates[0]
    return {"key": key, "url": url, "width": w, "height": h}


# Immutable-ID and duplicate-object guards. Stop rather than reuse or renumber.
guards = [
    (SOURCE_ID, "evidence/source-register.md", rf"(?m)^## {SOURCE_ID}\b"),
    (EVIDENCE_ID, "evidence/evidence-register.md", rf"(?m)^## {EVIDENCE_ID}\b"),
    (MEDIA_ID, "media/photo-metadata-register.md", rf"(?m)^## {MEDIA_ID}\b"),
    (TIMELINE_ID, "database/timeline.yml", rf"(?m)^  - id: {TIMELINE_ID}$"),
]
present = {ident: bool(re.search(pattern, read(path))) for ident, path, pattern in guards}
if any(present.values()):
    if all(present.values()) and Path(REPO_IMAGE).exists():
        print("1890s Main Street photo already integrated; no changes needed.")
        raise SystemExit(0)
    raise SystemExit(f"Partial ID collision detected: {present}; stop rather than reuse/renumber IDs.")

for duplicate_path in ("evidence/source-register.md", "media/photo-metadata-register.md", "database/sources.yml"):
    if TARGET_CATALOG in read(duplicate_path):
        raise SystemExit(f"CCHS object {TARGET_CATALOG} already appears in {duplicate_path}; stop rather than duplicate it.")

search = get_json(SEARCH_URL)
match = find_matching_dict(search)
if match is None:
    raise SystemExit(f"Exact CCHS catalog number {TARGET_CATALOG} was not returned by {SEARCH_URL}")
entry_id = match.get("id")
if not entry_id:
    raise SystemExit("Matching CCHS search record had no entry UUID.")
entry_url = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT_ID}/entries/{entry_id}"
entry = get_json(entry_url)
if catalog_number(entry) != TARGET_CATALOG:
    raise SystemExit(f"Fetched CCHS entry did not retain exact catalog number {TARGET_CATALOG}.")

derivative = choose_derivative(entry)
image_data = get_bytes(derivative["url"])
if not image_data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected CCHS derivative is not a JPEG.")
img = Image.open(BytesIO(image_data))
repo_width, repo_height = img.size
repo_sha = sha256_bytes(image_data)
repo_bytes = len(image_data)

path = Path(REPO_IMAGE)
if path.exists():
    raise SystemExit(f"Target image path already exists without registered {MEDIA_ID}: {REPO_IMAGE}")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(image_data)

slug = entry.get("slug") or match.get("slug")
hub_url = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug else None
)
catalog_link = hub_url or entry_url

api_record = {
    "reviewed": "2026-09-04",
    "institution": "Clackamas County Historical Society",
    "search_url": SEARCH_URL,
    "entry_url": entry_url,
    "hub_url": hub_url,
    "selected_public_derivative": derivative,
    "repository_file": REPO_IMAGE,
    "repository_derivative": {
        "width": repo_width,
        "height": repo_height,
        "bytes": repo_bytes,
        "sha256": repo_sha,
    },
    "steward_attachment": STEWARD,
    "catalog_metadata_supplied_by_steward": CATALOG_METADATA,
    "steward_viewpoint_annotation": STEWARD_VIEWPOINT_NOTE,
    "entry": entry,
}
write(API_CAPTURE, json.dumps(api_record, indent=2, ensure_ascii=False) + "\n")

capture = f"""# CCHS {TARGET_CATALOG} — Main Street, Oregon City, cataloged 1890–1899

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt record recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. EXACT SIXTH-TO-FIFTH CAMERA POSITION AND LATER 501/503/505 SUBDIVISIONS REMAIN PROBABLE / WORKING HYPOTHESIS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`. Related fixed-location comparison: `S-204` / `E-184` / `IMG-0733` (CCHS P-1456, 1890 Sixth/Main looking south after flood). Related map context: `SM-005` / `S-018` / `E-020` (1892 Sanborn) and `SM-006` / `S-019` / `E-020` (1900 Sanborn).

## Catalog record

- Institutional title: **Main Street, Oregon City**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **Main Street, Oregon City**
- Date made: **1890 - 1899**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of negative: **Society Collection**
- Other No.: **Stevens 104**
- Stevens Photo #: **102**
- Other Photo #: **Bill Howell #2000**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Steward viewpoint note: **{STEWARD_VIEWPOINT_NOTE}**

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from the exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact catalog record; the steward upload remains separately tracked by filename/dimensions/bytes/hash.

## Direct visual observation

The photograph visibly shows a broad street-level view down Oregon City's Main Street with commercial buildings on both sides, a rough/unpaved roadway, utility poles and overhead wires, horse-drawn vehicles, pedestrians, awnings and multiple business signs. A large wood hotel/restaurant-type building is prominent at left foreground and substantial commercial buildings occupy the right foreground and middle distance. Several signs are partially readable, but no business-name transcription is promoted here unless independently verified from a better crop or another source.

No later `501`, `503`, `505`, or other modern street numbers are readable in the image.

## Spatial interpretation

The project-steward supplied filename says the view looks **south from Sixth toward Fifth Street**. That wording is not present in the CCHS catalog metadata for `{TARGET_CATALOG}` and is therefore preserved as **project-steward metadata** rather than institutional description.

The proposed orientation is compatible with the existing CCHS P-1456 record (`S-204` / `E-184` / `IMG-0733`), which CCHS directly describes as Main Street at **Sixth and Main looking south** in 1890. The two records should be aligned structure-by-structure before treating this new photograph's camera position as independently proved.

If the steward filename orientation is correct, the **east-side Main Street block between Fifth and Sixth**—the block later containing 501/503/505 and higher odd numbers—appears along the left side of the view. This makes the photograph valuable pre-numbering structural/streetfront evidence, but exact later address boundaries have not yet been assigned to individual visible storefronts.

Classification: **DOCUMENTED / DIRECT** for the CCHS object, 1890–1899 date range, Main Street scene and visible streetscape; **PROBABLE / WORKING HYPOTHESIS** for the exact Sixth-to-Fifth camera position and for mapping individual pictured storefronts to later 501/503/505 boundaries.

## Historical limits

1. The catalog date is a **range, 1890–1899**, not a single exposure year. Do not silently convert the image to 1890, 1895, or another specific year.
2. Oregon City's formal citywide numbering program is documented in **1906**. Do not back-project later `501`, `503` and `505` numbers as official 1890s addresses.
3. The steward filename's Sixth-to-Fifth wording is useful provenance/context but is not CCHS catalog text for this object.
4. The image does not prove which individual 1890s storefront later became 501, 503, 505, 507, etc.; a Sanborn/photo alignment is still required.
5. The image does not prove continuity from any photographed 1890s structure to the 1907–1918 numbered occupants, the 1922 fire/rebuild sequence, or the surviving 503/505 buildings.
6. Business signs visible at distance should be transcribed only after dedicated enlarged visual review and independent cross-check where possible.

## Best next comparison

Align this image against the 1892 and 1900 Sanborn sheets and the fixed-location P-1456 1890 Sixth/Main-looking-south photograph. Use street intersections, building widths/heights, party walls, roof forms, projecting bays/awnings and sign-bearing walls to assign the photographed east-side storefront sequence before applying later street numbers.
"""
write(SOURCE_CAPTURE, capture)

photo_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Main Street, Oregon City, cataloged 1890–1899

- Type: Institutional historic photograph / Main Street streetscape
- CCHS external object: `{TARGET_CATALOG}`
- Catalog title: **Main Street, Oregon City**
- Catalog date: **1890 - 1899**
- Repository file: `{REPO_IMAGE}`
- Status: `committed`
- Repository derivative: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Steward attachment: `{STEWARD['filename']}`; {STEWARD['width']} × {STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`
- Other identifiers: **Stevens 104**; **Stevens Photo #102**; **Bill Howell #2000**
- Catalog note: medium **Negative**; negative location **Society Collection**.
- Viewpoint note: steward filename says looking south from Sixth toward Fifth; this is preserved as project metadata, not institutional catalog wording. It is compatible with fixed-location CCHS P-1456 (`S-204` / `E-184`) but remains a **PROBABLE / WORKING HYPOTHESIS** until photo-to-photo/map alignment.
- Target relevance: if that orientation is correct, the east-side Fifth-to-Sixth block later containing 501/503/505 appears on the left side of the view; exact later address divisions and structural continuity remain unresolved.
- Review: `{SOURCE_CAPTURE}`
"""
append_once("media/photo-metadata-register.md", f"## {MEDIA_ID}", photo_block)

inventory_block = f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG} Main Street, Oregon City, 1890–1899
- File: `{REPO_IMAGE}`
- Institutional metadata: Main Street, Oregon City; date range 1890–1899; Stevens 104 / Stevens Photo #102 / Bill Howell #2000.
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`.
- Spatial use: steward filename identifies a Sixth-to-Fifth southward view; treat as probable pending alignment with P-1456 and 1892/1900 Sanborns. No later-address or building-continuity inference.
"""
append_once("media/photos/inventory.md", f"### {MEDIA_ID}", inventory_block)

readme_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Main Street, Oregon City, cataloged 1890–1899

`{Path(REPO_IMAGE).name}` preserves the largest public derivative recovered from the exact CCHS object. CCHS catalogs the photograph simply as **Main Street, Oregon City**, date **1890–1899**. The steward filename says the view looks south from Sixth toward Fifth; that is retained as project metadata and is compatible with the separate fixed-location P-1456 1890 record, not treated as catalog fact for this object. If confirmed, the later 501/503/505 block lies along the east/left side of the view. Exact storefront-to-number mapping and continuity remain unresolved. See `{SOURCE_ID}` / `{EVIDENCE_ID}` and `{SOURCE_CAPTURE}`.
"""
append_once("media/photos/early-main-street/README.md", f"## {MEDIA_ID}", readme_block)

source_block = f"""## {SOURCE_ID} — {SOURCE_NAME}
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026 and exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media/timeline: `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`. Related location comparison: `S-204` / `E-184`; map context `SM-005` / `S-018`, `SM-006` / `S-019`, and `E-020`.  
Notes: CCHS catalogs the image as **Main Street, Oregon City**, date range **1890 - 1899**, with Stevens 104, Stevens Photo #102 and Bill Howell #2000. The steward filename identifies a southward Sixth-to-Fifth view; preserve that as project metadata, not CCHS wording. If confirmed, the later odd-numbered Fifth-to-Sixth target frontage is visible along the east/left side, but exact later-address boundaries and structural continuity are unresolved. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`.
"""
append_once("evidence/source-register.md", f"## {SOURCE_ID}", source_block)

evidence_block = f"""## {EVIDENCE_ID} — {EVIDENCE_NAME}
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / DIRECT** for the CCHS 1890–1899 Main Street scene and **PROBABLE / WORKING HYPOTHESIS** for exact Sixth-to-Fifth viewpoint and later-address mapping.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`; comparison `S-204` / `E-184`; map context `SM-005` / `S-018`, `SM-006` / `S-019`, `E-020`.  
Claims: CCHS object `{TARGET_CATALOG}` is cataloged **Main Street, Oregon City** with date range **1890 - 1899**. The photograph directly depicts a broad Main Street commercial streetscape with buildings on both sides, roadway, utility infrastructure, horse-drawn vehicles and pedestrians. The project-steward filename identifies the view as looking south from Sixth toward Fifth; this is compatible with the separate fixed-location P-1456 1890 Sixth/Main-looking-south record. If that orientation is confirmed, the east-side Fifth-to-Sixth block later containing 501/503/505 lies along the left side of the view.  
Limits: the catalog itself does not state Sixth/Fifth; the later 501/503/505 numbers are not visible and should not be backdated before the 1906 numbering program. Individual storefront-to-address mapping, exact exposure year, occupancy, ownership and continuity to later/pre- or post-1922 structures are not proved.  
Confidence: **Very High** for CCHS object/date-range/Main Street identity and visible streetscape; **PROBABLE / WORKING HYPOTHESIS** for camera position and exact target storefront mapping.
"""
append_once("evidence/evidence-register.md", f"## {EVIDENCE_ID}", evidence_block)

# Synchronized YAML mirrors: keep names exactly identical to Markdown headings.
sources_yml = read("database/sources.yml").rstrip()
sources_yml += f"""

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "CCHS {TARGET_CATALOG}; Main Street, Oregon City; date range 1890-1899. Steward filename says south from Sixth toward Fifth; project metadata only, probable pending P-1456/Sanborn alignment. No pre-1906 numbered-address or structural-continuity inference. Related {EVIDENCE_ID}/{MEDIA_ID}/{TIMELINE_ID}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]
"""
write("database/sources.yml", sources_yml + "\n")

evidence_yml = read("database/evidence.yml").rstrip()
evidence_yml += f"""

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Institutional photograph/catalog metadata plus direct visual review; documented/direct for 1890-1899 Main Street scene and probable/working-hypothesis for exact viewpoint/later-address mapping"
    claims:
      - "CCHS {TARGET_CATALOG} catalogs Main Street, Oregon City with date range 1890-1899."
      - "The photograph directly shows a broad commercial Main Street streetscape with buildings on both sides, roadway, utility infrastructure, horse-drawn vehicles and pedestrians."
      - "Steward filename identifies a southward Sixth-to-Fifth view; this is compatible with fixed-location CCHS P-1456 but is not catalog wording for this object."
      - "If the viewpoint is confirmed, the east-side Fifth-to-Sixth block later containing 501/503/505 lies along the left side of the view; exact storefront boundaries and continuity are unresolved."
    confidence: "Very High for CCHS object/date-range/Main Street identity and visible streetscape; PROBABLE / WORKING HYPOTHESIS for exact camera position and target storefront mapping."
    related_sources: [{SOURCE_ID}, S-204, S-018, S-019]
    related_buildings: [B-005, B-001, B-002]
"""
write("database/evidence.yml", evidence_yml + "\n")

timeline_yml = read("database/timeline.yml").rstrip()
timeline_yml += f"""

  - id: {TIMELINE_ID}
    date: 1890-1899
    summary: CCHS Main Street photograph documents a late-19th-century commercial streetscape. Steward filename identifies a southward Sixth-to-Fifth view compatible with P-1456; if confirmed, the later 501/503/505 block is on the east/left side.
    confidence: Very High for CCHS date range and Main Street scene; PROBABLE / WORKING HYPOTHESIS for exact camera position and later-address storefront mapping. No pre-1906 number or continuity inference.
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}, S-204, S-018, S-019]
    related_buildings: [B-005, B-001, B-002]
"""
write("database/timeline.yml", timeline_yml + "\n")

# Building Markdown pages + synchronized building YAML associations.
building_section = f"""## 1890–1899 Main Street photograph — pre-numbering block context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` preserves CCHS `{TARGET_CATALOG}`, cataloged **Main Street, Oregon City**, date **1890–1899**. The project-steward filename identifies the view as looking south from Sixth toward Fifth. That proposed orientation is compatible with fixed-location P-1456 (`S-204` / `E-184`) but is not catalog wording for this object.

If the orientation is confirmed, the east-side Fifth-to-Sixth frontage later containing **501/503/505 Main** appears along the left side of the photograph. Classification for exact storefront-to-later-address mapping remains **PROBABLE / WORKING HYPOTHESIS**. The later numbers are not visible, the exposure year is not narrowed within 1890–1899, and continuity to numbered or post-1922 structures is not established.
"""
for building_path in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    append_inline_id(building_path, "- Related evidence:", EVIDENCE_ID)
    append_inline_id(building_path, "- Related sources:", SOURCE_ID)
    append_once(building_path, "## 1890–1899 Main Street photograph — pre-numbering block context", building_section)

for building_id in ("B-001", "B-002", "B-005"):
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_evidence", EVIDENCE_ID)
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_sources", SOURCE_ID)

timeline_note = f"""## 1890–1899 — Main Street street-level photograph / Sixth-to-Fifth viewpoint candidate

CCHS `{TARGET_CATALOG}` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`) catalogs a **Main Street, Oregon City** photograph to **1890–1899**. The steward filename identifies a southward view from Sixth toward Fifth; existing P-1456 (`S-204` / `E-184`) independently establishes a CCHS 1890 Sixth/Main-looking-south viewpoint and makes that interpretation plausible.

If confirmed, the later 501/503/505 block is visible on the east/left side of Main. Exact storefront boundaries, specific exposure year, pre-1906 numbered addresses, occupancy and continuity remain unresolved.
"""
append_once("timeline.md", "## 1890–1899 — Main Street street-level photograph / Sixth-to-Fifth viewpoint candidate", timeline_note)

for tpath, label in (
    ("timelines/501-main.md", "501"),
    ("timelines/503-main.md", "503"),
    ("timelines/505-main.md", "505"),
):
    specific = f"""## 1890–1899 — Pre-numbering Main Street photo context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` is a CCHS Main Street photograph dated **1890–1899**. The steward filename says it looks south from Sixth toward Fifth; if that probable orientation is confirmed, the east-side block later containing **{label} Main** is visible along the left side. The `{label}` number is not visible and should not be backdated; exact storefront identity and physical continuity remain unresolved.
"""
    append_once(tpath, "## 1890–1899 — Pre-numbering Main Street photo context", specific)

map_note = f"""## 1890–1899 CCHS Main Street street-level photo cross-check

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` adds CCHS `{TARGET_CATALOG}`, cataloged **Main Street, Oregon City**, date **1890–1899**. The project-steward filename says the view looks south from Sixth toward Fifth. That proposed viewpoint is compatible with CCHS P-1456 (`S-204` / `E-184`), which CCHS directly locates at Sixth/Main looking south in 1890.

This photograph should be aligned against `SM-005` (1892) and `SM-006` (1900), plus P-1456, using intersection geometry, building widths/heights, roof forms, party walls and sign-bearing walls. If the viewpoint is confirmed, the later 501/503/505 east-side block is visible along the left side. Until alignment is completed, exact later-address storefront assignments remain **PROBABLE / WORKING HYPOTHESIS** and no structural continuity is inferred.
"""
append_once("maps/sanborn-comparison-503-505-507.md", "## 1890–1899 CCHS Main Street street-level photo cross-check", map_note)

crosswalk = f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} — CCHS 1890–1899 Main Street photograph

- Source: `{SOURCE_ID}` — CCHS `{TARGET_CATALOG}`.
- Evidence: `{EVIDENCE_ID}` — direct Main Street/date-range streetscape; probable Sixth-to-Fifth viewpoint and later-address mapping.
- Media: `{MEDIA_ID}` — full public CCHS derivative.
- Timeline: `{TIMELINE_ID}` — 1890–1899 photograph context.
- Related buildings: `B-005` 501, `B-001` 503, `B-002` 505 (later-address spatial context only).
- Related fixed-location photo: `S-204` / `E-184` / `IMG-0733`.
- Related map context: `SM-005` / `S-018`; `SM-006` / `S-019`; `E-020`.
- Limit: no pre-1906 numbered-address, exact exposure-year, storefront-boundary, occupancy, ownership or continuity inference.
- Review: `{SOURCE_CAPTURE}`.
"""
append_once("indexes/id-crosswalk.md", f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID}", crosswalk)

log = f"""## 4 September 2026 — CCHS 1890–1899 Main Street photograph 2008.008.003.104

- Checked current `main`; exact object `{TARGET_CATALOG}` was not already registered.
- Preserved the largest public derivative from the exact CCHS object as `{MEDIA_ID}` and tracked the steward upload separately by filename, dimensions, bytes and SHA-256.
- Added `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}` and synchronized source/evidence/building/timeline/photo/crosswalk/map-comparison records.
- CCHS metadata is limited to **Main Street, Oregon City** and **1890–1899**. The steward filename's **looking south from Sixth toward Fifth** wording is preserved as project metadata, not institutional catalog wording.
- The proposed viewpoint is compatible with fixed-location P-1456 (`S-204` / `E-184`), but exact camera position and storefront-to-later-501/503/505 mapping remain **PROBABLE / WORKING HYPOTHESIS** pending photo/Sanborn alignment.
- Explicitly did not backdate 501/503/505 street numbers, select a single exposure year, or infer continuity into later numbered or post-1922 structures.
"""
append_once("registers/research-log.md", "## 4 September 2026 — CCHS 1890–1899 Main Street photograph 2008.008.003.104", log)

print(f"Integrated {MEDIA_ID}/{SOURCE_ID}/{EVIDENCE_ID}/{TIMELINE_ID}: {REPO_IMAGE}")
print(f"Repository derivative: {repo_width}x{repo_height}, {repo_bytes} bytes, sha256 {repo_sha}")
