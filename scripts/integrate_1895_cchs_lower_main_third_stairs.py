from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "2008.008.003.125"
MEDIA_ID = "IMG-0742"
SOURCE_ID = "S-213"
EVIDENCE_ID = "E-193"
TIMELINE_ID = "T-076"

SOURCE_NAME = "Clackamas County Historical Society 2008.008.003.125, Lower Main Street Oregon City from Top of 3rd Street Stairs 1895"
EVIDENCE_NAME = "CCHS 1895 bluff photo shows pre-1922 Main/Fifth target-frontage roofline candidate"

REPO_IMAGE = "media/photos/early-main-street/IMG-0742_1895-lower-main-from-3rd-street-stairs-cchs-2008-008-003-125.jpg"
API_CAPTURE = "evidence/source-captures/1895-cchs-2008-008-003-125-lower-main-third-stairs-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1895-cchs-2008-008-003-125-lower-main-third-stairs-target-frontage-2026-09-04.md"
SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET_CATALOG, "size": 50})
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "Lower Main Street Oregon City from Top of 3rd Street Stairs 1895.jpg",
    "width": 2048,
    "height": 1397,
    "bytes": 581027,
    "sha256": "97f006c0f74ac9fabc2cd4e1be0f71d7e781afbbc795c272cec7d3b9bb125cff",
}
CATALOG_METADATA = {
    "title": "Lower Main Street Oregon City from Top of 3rd Street Stairs 1895",
    "entry_object_id": TARGET_CATALOG,
    "description": "Oregon City from the Bluff, looking down river from top of 3rd Street Stairs.",
    "date_made": "1895",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Society Collection",
    "other_number": "Stevens 125",
    "other_photo_number": "125",
}
STEWARD_TARGET_NOTE = (
    "Project steward identifies the top/roof of the predecessor frontage later associated "
    "with 501, 503 and 505 Main as visible in this photograph."
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
    start_pat = re.compile(rf"(?m)^  - id: {re.escape(entity_id)}\s*$")
    m = start_pat.search(text)
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


# Immutable-ID guards. Stop rather than reuse or renumber.
guards = [
    (SOURCE_ID, "evidence/source-register.md", rf"(?m)^## {SOURCE_ID}\b"),
    (EVIDENCE_ID, "evidence/evidence-register.md", rf"(?m)^## {EVIDENCE_ID}\b"),
    (MEDIA_ID, "media/photo-metadata-register.md", rf"(?m)^## {MEDIA_ID}\b"),
    (TIMELINE_ID, "database/timeline.yml", rf"(?m)^  - id: {TIMELINE_ID}$"),
]
present = {ident: bool(re.search(pattern, read(path))) for ident, path, pattern in guards}
if any(present.values()):
    if all(present.values()) and Path(REPO_IMAGE).exists():
        print("1895 bluff photo already integrated; no changes needed.")
        raise SystemExit(0)
    raise SystemExit(f"Partial ID collision detected: {present}; stop rather than reuse/renumber IDs.")

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
    "steward_target_frontage_annotation": STEWARD_TARGET_NOTE,
    "entry": entry,
}
write(API_CAPTURE, json.dumps(api_record, indent=2, ensure_ascii=False) + "\n")

capture = f"""# CCHS {TARGET_CATALOG} — Lower Main Street from top of 3rd Street Stairs, 1895

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt record recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. TARGET 501/503/505 ROOFLINE IDENTIFICATION IS PROBABLE / WORKING HYPOTHESIS, NOT AN 1895 NUMBERED-ADDRESS CLAIM.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`. Related later-address records: `B-005` (501), `B-001` (503), `B-002` (505). Related map context: `SM-005` / `S-018` / `E-020` (1892 Sanborn).

## Catalog record

- Institutional title: **Lower Main Street Oregon City from Top of 3rd Street Stairs 1895**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **Oregon City from the Bluff, looking down river from top of 3rd Street Stairs.**
- Date made: **1895**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of negative: **Society Collection**
- Other No.: **Stevens 125**
- Stevens Photo #: **125**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Steward spatial note: **{STEWARD_TARGET_NOTE}**

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from the exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact catalog record; the steward upload remains separately tracked by filename/dimensions/bytes/hash.

## Direct visual observation

The full photograph is an elevated overview of lower Oregon City looking downriver. It visibly includes a long stretch of Main Street commercial fabric, intersecting streets, roofs and rear/side elevations, the railroad corridor at right, the river/bridge zone in the distance, and a **Clackamas County Historical Society** watermark.

The project steward identifies the **top/roof of the predecessor frontage later associated with 501, 503 and 505 Main** as visible in the Main/Fifth area. Visual inspection confirms that roof/top portions of the relevant commercial row are visible in the correct general streetscape, although the individual later address divisions are not readable in the photograph.

## Cross-source interpretation

The 1892 Sanborn (`SM-005` / `S-018` / `E-020`) independently maps a developed commercial frontage in this Main/Fifth area. That is compatible with the 1895 bluff photograph showing an established predecessor commercial row.

Classification for the specific target assignment: **PROBABLE / WORKING HYPOTHESIS**. The photograph + known viewpoint + existing map context support the steward's identification, but a dedicated photogrammetric/landmark alignment has not yet assigned each visible roof segment to the later 501, 503 and 505 address boundaries.

## Historical limits

1. Oregon City's formal citywide numbering program is documented in **1906**. Do **not** back-project the later `501`, `503` and `505` numbers as official 1895 addresses merely because the later-address frontage can be spatially discussed.
2. The photo does **not** establish that one single physical building spanned all three later address spaces. "501/503/505 predecessor frontage" is safer than "the 501/503/505 building" until the 1892/1900 footprint and later address subdivision are explicitly aligned.
3. The photo does not prove continuity from 1895 to the 1907–1918 numbered occupants or to the post-1922 / surviving 503–505 structures.
4. Exact storefront walls, internal subdivisions and later numbered boundaries are obscured by distance, viewpoint and intervening roofs.
5. This evidence strengthens the **structural/streetfront chronology**, not business occupancy or ownership.
"""
write(SOURCE_CAPTURE, capture)

photo_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Lower Main Street from 3rd Street Stairs, 1895

- Type: Institutional historic photograph / elevated cityscape
- CCHS external object: `{TARGET_CATALOG}`
- Catalog title: **Lower Main Street Oregon City from Top of 3rd Street Stairs 1895**
- Catalog date: **1895**
- Repository file: `{REPO_IMAGE}`
- Status: `committed`
- Repository derivative: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Steward attachment: `{STEWARD['filename']}`; {STEWARD['width']} × {STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`
- Other identifiers: **Stevens 125**; **Stevens Photo #125**
- Catalog note: medium **Photographic Paper**; negative location **Society Collection**.
- Target-frontage note: project steward identifies the roof/top of the predecessor frontage later associated with 501/503/505 Main as visible. Preserve as **PROBABLE / WORKING HYPOTHESIS** for exact target assignment; the photo does not display the later address numbers or resolve internal storefront boundaries.
- Related map context: `SM-005` / `S-018` / `E-020` (1892 Sanborn).
- Review: `{SOURCE_CAPTURE}`
"""
append_once("media/photo-metadata-register.md", f"## {MEDIA_ID}", photo_block)

inventory_block = f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG} Lower Main / 3rd Street Stairs, 1895
- File: `{REPO_IMAGE}`
- Institutional metadata: Oregon City from bluff/top of 3rd Street Stairs, looking downriver; 1895; Stevens 125.
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`.
- Target relevance: the later 501/503/505 predecessor-frontage roof/top is a steward-identified, map-compatible **PROBABLE / WORKING HYPOTHESIS**; no 1895 numbered-address or building-continuity claim.
"""
append_once("media/photos/inventory.md", f"### {MEDIA_ID}", inventory_block)

readme_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Lower Main Street from 3rd Street Stairs, 1895

`{Path(REPO_IMAGE).name}` preserves the largest public derivative recovered from the exact CCHS object. CCHS catalogs the view as **Lower Main Street Oregon City from Top of 3rd Street Stairs 1895**. The project steward identifies the roof/top of the predecessor frontage later associated with 501/503/505 Main as visible; the archive records that specific spatial assignment as **PROBABLE / WORKING HYPOTHESIS**, consistent with the developed frontage mapped on the 1892 Sanborn, not as an 1895 numbered-address or continuity claim. See `{SOURCE_ID}` / `{EVIDENCE_ID}` and `{SOURCE_CAPTURE}`.
"""
append_once("media/photos/early-main-street/README.md", f"## {MEDIA_ID}", readme_block)

source_block = f"""## {SOURCE_ID} — {SOURCE_NAME}
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026 and exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media/timeline: `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`. Related later-address records: `B-005`, `B-001`, `B-002`; map context `SM-005` / `S-018` / `E-020`.  
Notes: CCHS catalogs the bluff/downriver view as 1895 and supplies Stevens 125 / Photo #125. Project-steward annotation identifies the top/roof of the predecessor frontage later associated with 501/503/505 Main as visible. The archive treats exact target assignment as **PROBABLE / WORKING HYPOTHESIS** and does not backdate the post-1906 street numbers, infer one building spanning all three later addresses, or claim continuity into the post-1922 structures. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`.
"""
append_once("evidence/source-register.md", f"## {SOURCE_ID}", source_block)

evidence_block = f"""## {EVIDENCE_ID} — {EVIDENCE_NAME}
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / DIRECT** for the 1895 bluff streetscape and **PROBABLE / WORKING HYPOTHESIS** for the exact later 501/503/505 frontage assignment.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`; map context `SM-005` / `S-018` / `E-020`.  
Claims: CCHS object `{TARGET_CATALOG}` is cataloged **Lower Main Street Oregon City from Top of 3rd Street Stairs 1895**, described as Oregon City from the bluff looking downriver from the top of the 3rd Street Stairs. The image directly depicts the lower-Main commercial streetscape. The project steward identifies the roof/top of the predecessor frontage later associated with 501, 503 and 505 Main as visible; that identification is compatible with the developed commercial frontage independently mapped in 1892.  
Limits: the later 501/503/505 numbers are not visible and should not be backdated before the 1906 numbering program. Exact later-address boundaries within the visible roofline have not been photogrammetrically aligned. The image does not prove a single building across all three spaces, occupancy, ownership, or continuity to the post-1922/surviving structures.  
Confidence: **Very High** for catalog metadata and visible 1895 streetscape; **PROBABLE / WORKING HYPOTHESIS** for exact target-frontage roofline assignment.
"""
append_once("evidence/evidence-register.md", f"## {EVIDENCE_ID}", evidence_block)

# Synchronized YAML mirrors: keep names exactly identical to Markdown headings.
sources_yml = read("database/sources.yml").rstrip()
sources_yml += f"""

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "CCHS {TARGET_CATALOG}; cataloged 1895 bluff/downriver view from top of 3rd Street Stairs. Steward target-roofline identification is PROBABLE / WORKING HYPOTHESIS only; do not backdate later street numbers or infer structural continuity. Related {EVIDENCE_ID}/{MEDIA_ID}/{TIMELINE_ID}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]
"""
write("database/sources.yml", sources_yml + "\n")

evidence_yml = read("database/evidence.yml").rstrip()
evidence_yml += f"""

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Institutional photograph/catalog metadata plus direct visual review; documented/direct for 1895 streetscape and probable/working-hypothesis for exact later-address frontage assignment"
    claims:
      - "CCHS {TARGET_CATALOG} catalogs Lower Main Street Oregon City from Top of 3rd Street Stairs 1895 and describes a bluff view looking downriver."
      - "The photograph directly depicts the lower-Main commercial streetscape."
      - "Project steward identifies the roof/top of the predecessor frontage later associated with 501/503/505 Main as visible; this is compatible with the developed frontage mapped on the 1892 Sanborn."
      - "Later 501/503/505 address boundaries are not visible; no pre-1906 numbered-address, single-building, occupancy, ownership or continuity claim is made."
    confidence: "Very High for catalog metadata and visible streetscape; PROBABLE / WORKING HYPOTHESIS for exact target-frontage roofline assignment."
    related_sources: [{SOURCE_ID}, S-018]
    related_buildings: [B-005, B-001, B-002]
"""
write("database/evidence.yml", evidence_yml + "\n")

timeline_yml = read("database/timeline.yml").rstrip()
timeline_yml += f"""

  - id: {TIMELINE_ID}
    date: 1895
    summary: CCHS bluff photograph shows lower Main Street; steward identification plus map-compatible spatial context places a visible roof/top candidate on the predecessor frontage later associated with 501/503/505 Main.
    confidence: Very High for cataloged 1895 view; PROBABLE / WORKING HYPOTHESIS for exact later-address frontage assignment. No pre-1906 numbered-address or structural-continuity inference.
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}, S-018]
    related_buildings: [B-005, B-001, B-002]
"""
write("database/timeline.yml", timeline_yml + "\n")

# Building Markdown pages + synchronized building YAML associations.
building_section = f"""## 1895 bluff photograph — predecessor target-frontage roofline candidate

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` preserves the CCHS bluff view cataloged **1895**. The project steward identifies the roof/top of the predecessor frontage later associated with **501/503/505 Main** as visible. Existing 1892 Sanborn context (`SM-005` / `S-018` / `E-020`) independently shows developed commercial frontage in the area.

Classification: **PROBABLE / WORKING HYPOTHESIS for exact target-frontage assignment.** The later street numbers are not image-visible and should not be backdated before Oregon City's 1906 numbering program. The photograph does not prove one building spanned all three later addresses or establish continuity to post-1922 structures.
"""
for building_path in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    append_inline_id(building_path, "- Related evidence:", EVIDENCE_ID)
    append_inline_id(building_path, "- Related sources:", SOURCE_ID)
    append_once(building_path, "## 1895 bluff photograph — predecessor target-frontage roofline candidate", building_section)

for building_id in ("B-001", "B-002", "B-005"):
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_evidence", EVIDENCE_ID)
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_sources", SOURCE_ID)

timeline_note = f"""## 1895 — Bluff photograph of lower Main; target-frontage roofline candidate

CCHS `{TARGET_CATALOG}` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`) catalogs a photograph made from the top of the 3rd Street Stairs looking downriver in **1895**. The project steward identifies the visible roof/top of the predecessor frontage later associated with 501/503/505 Main. The 1892 Sanborn independently establishes developed commercial frontage in the area.

The specific later-address roofline mapping remains **PROBABLE / WORKING HYPOTHESIS**: the photo does not display 501/503/505 numbers, does not prove one physical building covered all three later spaces, and does not bridge continuity to the post-1922 structures.
"""
append_once("timeline.md", "## 1895 — Bluff photograph of lower Main; target-frontage roofline candidate", timeline_note)

for tpath, label in (
    ("timelines/501-main.md", "501"),
    ("timelines/503-main.md", "503"),
    ("timelines/505-main.md", "505"),
):
    specific = f"""## 1895 — Pre-numbering predecessor-frontage photo context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` is an 1895 CCHS bluff photograph in which the project steward identifies the roof/top of the predecessor Main/Fifth frontage later associated with **501/503/505 Main** as visible. For this {label} timeline, use the image only as **PROBABLE / WORKING HYPOTHESIS** spatial/structural context. The `{label}` number is not visible and should not be backdated to 1895; physical continuity into later numbered or surviving structures remains unproved.
"""
    append_once(tpath, "## 1895 — Pre-numbering predecessor-frontage photo context", specific)

map_note = f"""## 1895 CCHS bluff-photo cross-check

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` adds a CCHS photograph cataloged **1895**, made from the top of the 3rd Street Stairs looking downriver. The project steward identifies the roof/top of the predecessor frontage later associated with 501/503/505 Main as visible. This is compatible with the developed commercial frontage shown by `SM-005` (1892).

Use this as **PROBABLE / WORKING HYPOTHESIS** for precise target-roof assignment until landmark/roof geometry is explicitly aligned across the 1892/1900 Sanborns and the photograph. Do not infer that the later address numbers existed in 1895, that one structure spanned all three later spaces, or that the visible roof continued into the post-1922 buildings.
"""
append_once("maps/sanborn-comparison-503-505-507.md", "## 1895 CCHS bluff-photo cross-check", map_note)

crosswalk = f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} — CCHS 1895 lower-Main bluff photograph

- Source: `{SOURCE_ID}` — CCHS `{TARGET_CATALOG}`.
- Evidence: `{EVIDENCE_ID}` — direct 1895 streetscape; probable/working-hypothesis target-frontage roofline assignment.
- Media: `{MEDIA_ID}` — full public CCHS derivative.
- Timeline: `{TIMELINE_ID}` — 1895 photograph context.
- Related buildings: `B-005` 501, `B-001` 503, `B-002` 505 (later-address mapping only).
- Related map context: `SM-005` / `S-018` / `E-020`.
- Limit: no pre-1906 numbered-address, one-building, occupancy, ownership or continuity inference.
- Review: `{SOURCE_CAPTURE}`.
"""
append_once("indexes/id-crosswalk.md", f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID}", crosswalk)

log = f"""## 4 September 2026 — CCHS 1895 Lower Main / 3rd Street Stairs photograph

- Checked current `main`; exact object `{TARGET_CATALOG}` was not already registered.
- Preserved the largest public derivative from the exact CCHS object as `{MEDIA_ID}` and tracked the steward upload separately by filename, dimensions, bytes and SHA-256.
- Added `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}` and synchronized source/evidence/building/timeline/photo/crosswalk records.
- Project steward identifies the roof/top of the predecessor frontage later associated with 501/503/505 Main as visible. Archive classification for that exact spatial assignment is **PROBABLE / WORKING HYPOTHESIS**, compatible with 1892 Sanborn developed-frontage context.
- Explicitly did not backdate 501/503/505 street numbers to 1895, did not claim a single building spanned all three later address spaces, and did not infer continuity into the post-1922 structures.
"""
append_once("registers/research-log.md", "## 4 September 2026 — CCHS 1895 Lower Main / 3rd Street Stairs photograph", log)

print(f"Integrated {MEDIA_ID}/{SOURCE_ID}/{EVIDENCE_ID}/{TIMELINE_ID}: {REPO_IMAGE}")
print(f"Repository derivative: {repo_width}x{repo_height}, {repo_bytes} bytes, sha256 {repo_sha}")
