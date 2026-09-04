from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "2008.008.046.040"
MEDIA_ID = "IMG-0744"
SOURCE_ID = "S-215"
EVIDENCE_ID = "E-195"
TIMELINE_ID = "T-078"

REPO_IMAGE = "media/photos/early-main-street/IMG-0744_1895-oregon-city-welcome-arch-6th-main-cchs-2008-008-046-040.jpg"
API_CAPTURE = "evidence/source-captures/1895-cchs-2008-008-046-040-welcome-arch-6th-main-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1895-cchs-2008-008-046-040-welcome-arch-6th-main-target-frontage-2026-09-04.md"
SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET_CATALOG, "size": 50})
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "Welcome Arch, O.C. Main St., 1895.jpg",
    "width": 2048,
    "height": 1285,
    "bytes": 886058,
    "sha256": "90a533ef0c721ed65ed45d090d07ac0dcc372cba0f8d138543f96a2b7035924e",
}
CATALOG_METADATA = {
    "title": 'Oregon City "Welcome Arch"',
    "entry_object_id": TARGET_CATALOG,
    "description": 'Oregon City "Welcome Arch", 6th and Main.',
    "date_made": "1895",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_number": "Culp, Ed 40",
    "stevens_photo_number": "97",
}
STEWARD_TARGET_NOTE = (
    "Project steward identifies the predecessor Main Street frontage later numbered "
    "501, 503 and 505 as visible in the background on the right side of the street."
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
    else:
        raise SystemExit(f"Could not find line prefix {prefix!r} in {path}")
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


# Immutable-ID guards.
guards = [
    (SOURCE_ID, "evidence/source-register.md", rf"(?m)^## {SOURCE_ID}\b"),
    (EVIDENCE_ID, "evidence/evidence-register.md", rf"(?m)^## {EVIDENCE_ID}\b"),
    (MEDIA_ID, "media/photo-metadata-register.md", rf"(?m)^## {MEDIA_ID}\b"),
    (TIMELINE_ID, "database/timeline.yml", rf"(?m)^  - id: {TIMELINE_ID}$"),
]
present = {ident: bool(re.search(pattern, read(path))) for ident, path, pattern in guards}
if any(present.values()):
    if all(present.values()) and Path(REPO_IMAGE).exists():
        print("Welcome Arch photo already integrated; no changes needed.")
        raise SystemExit(0)
    raise SystemExit(f"Partial ID collision detected: {present}; stop rather than reuse/renumber IDs.")

# Exact object retrieval.
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

capture = f"""# CCHS {TARGET_CATALOG} — Oregon City "Welcome Arch", 6th and Main, 1895

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt record recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. RIGHT-BACKGROUND 501/503/505 PREDECESSOR-FRONTAGE IDENTIFICATION IS PROBABLE / WORKING HYPOTHESIS FOR INDIVIDUAL LATER ADDRESS BOUNDARIES.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`. Related later-address records: `B-005` (501), `B-001` (503), `B-002` (505). Related fixed-location comparison: `S-204` / `E-184` / `IMG-0733`. Related map context: `SM-005` / `S-018` / `E-020` (1892 Sanborn).

## Catalog record

- Institutional title: **Oregon City "Welcome Arch"**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **Oregon City "Welcome Arch", 6th and Main.**
- Date made: **1895**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of negative: **Society Collection**
- Other No.: **Culp, Ed 40**
- Stevens Photo #: **97**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Steward target annotation: **{STEWARD_TARGET_NOTE}**

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact catalog object; the steward upload remains separately tracked by filename, dimensions, bytes and hash.

## Direct visual observation

The photograph shows a large decorated **WELCOME** arch spanning Main Street, with American flags and bunting. Commercial buildings extend down Main on both sides. On the right foreground is a large brick commercial building with **WILLAMETTE LAND CO.** signage, while additional storefronts continue beyond the arch into the background. The target side of Main is therefore visible in a street-level perspective rather than only as a distant roofline.

No later `501`, `503`, or `505` street numbers are readable in the image.

## Target-frontage interpretation

The CCHS catalog directly fixes the scene at **6th and Main** in **1895**. The project steward identifies the predecessor frontage later associated with **501, 503 and 505 Main** in the **background on the right side of the street**, beyond the arch.

That target-side reading is consistent with the previously corrected Sixth-to-Fifth orientation for `S-214` / `E-194` / `IMG-0743`, where the later odd-numbered Fifth-to-Sixth frontage is on the east/right side when looking south. It is also compatible with the fixed-location P-1456 (`S-204` / `E-184`) and the developed frontage mapped on the 1892 Sanborn (`SM-005` / `S-018` / `E-020`).

This photograph is a stronger spatial anchor than an unlocated streetscape because CCHS itself supplies **6th and Main**. However, the photo does not visibly print the later address numbers, and individual storefront divisions in the right-background sequence have not yet been aligned building-by-building to later 501/503/505 boundaries.

Classification: **DOCUMENTED / DIRECT** for the CCHS object, 1895 date, Sixth/Main location, arch and visible Main Street streetscape; **PROBABLE / WORKING HYPOTHESIS** for assigning individual right-background predecessor storefronts to later 501, 503 and 505 boundaries.

## Historical limits

1. Oregon City's formal citywide numbering program is documented in 1906. Do not describe the pictured 1895 businesses as then using official `501`, `503`, or `505` numbers solely from this image.
2. The image supports the location of the predecessor frontage in the right-hand background, but it does not by itself prove the exact internal storefront boundaries corresponding to each later number.
3. The image does not prove occupancy or business ownership of the target predecessor storefronts unless a sign is separately resolved and corroborated.
4. The image does not prove continuity from any 1895 structure into the 1907–1918 numbered occupants, the 1922 fire/rebuild sequence, or the surviving 503/505 buildings.
5. The `501/503/505` identification is a later-address spatial mapping, not a claim that those numbers were visible or officially in use in 1895.

## Best next comparison

Align the right-background storefront sequence against `SM-005` (1892), `SM-006` (1900), fixed-location P-1456 (`S-204` / `E-184`), and `IMG-0743` (`S-214` / `E-194`). Use the Sixth/Main intersection, the arch position, party walls, rooflines, facade widths, setbacks, and sign-bearing walls to assign the predecessor storefront sequence before applying later street numbers.
"""
write(SOURCE_CAPTURE, capture)

# Human-readable source/evidence registers.
append_once(
    "evidence/source-register.md",
    f"## {SOURCE_ID} —",
    f"""## {SOURCE_ID} — Clackamas County Historical Society {TARGET_CATALOG}, Oregon City "Welcome Arch", 6th and Main, 1895
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026 and exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media/timeline: `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`. Related later-address records: `B-005`, `B-001`, `B-002`; comparison `S-204` / `E-184`, `S-214` / `E-194`; map context `SM-005` / `S-018` / `E-020`.  
Notes: CCHS catalogs the photograph as **Oregon City "Welcome Arch"**, **6th and Main**, date **1895**, with **Culp, Ed 40** and **Stevens Photo #97**. The project steward identifies the predecessor frontage later associated with 501/503/505 in the background on the **right side of the street**. The archive treats the target-side location as strong spatial context but keeps individual storefront-to-later-number divisions **PROBABLE / WORKING HYPOTHESIS**; no pre-1906 numbered-address or post-1922 structural-continuity inference. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`."""
)

append_once(
    "evidence/evidence-register.md",
    f"## {EVIDENCE_ID} —",
    f"""## {EVIDENCE_ID} — CCHS 1895 Welcome Arch photo fixes Sixth/Main and shows target predecessor frontage in right background
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / DIRECT** for the 1895 Sixth/Main scene and **PROBABLE / WORKING HYPOTHESIS** for individual later 501/503/505 storefront boundaries.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`; comparison `S-204` / `E-184`, `S-214` / `E-194`; map context `SM-005` / `S-018` / `E-020`.  
Claims: CCHS object `{TARGET_CATALOG}` is cataloged **Oregon City "Welcome Arch"**, described as **6th and Main**, and dated **1895**. The photograph directly shows the decorated arch, Main Street commercial buildings, and a continuing storefront sequence beyond the arch. The project steward identifies the predecessor frontage later associated with **501, 503 and 505 Main** in the **right-hand background**. The CCHS-supplied Sixth/Main location makes this a strong fixed spatial anchor, and the right-side target reading is consistent with the corrected `IMG-0743` orientation and 1892 Sanborn block geometry.  
Limits: `501`, `503`, and `505` are not readable and should not be backdated as official 1895 numbers. Exact individual storefront-to-later-address boundaries, occupants, ownership, and continuity to later numbered or post-1922 structures are not proved by this photograph alone.  
Confidence: **Very High** for CCHS object/date/location and visible streetscape; **PROBABLE / WORKING HYPOTHESIS** for assigning individual visible predecessor storefronts to later 501/503/505 boundaries."""
)

# Database source/evidence/timeline.
append_once(
    "database/sources.yml",
    f"  - id: {SOURCE_ID}",
    f"""  - id: {SOURCE_ID}
    name: 'Clackamas County Historical Society {TARGET_CATALOG}, Oregon City "Welcome Arch", 6th and Main, 1895'
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "CCHS catalogs the scene at 6th and Main in 1895. Steward identifies the predecessor frontage later associated with 501/503/505 in the right-hand background. Exact individual later-address boundaries remain PROBABLE / WORKING HYPOTHESIS; no pre-1906 numbering or structural-continuity inference. Related {EVIDENCE_ID}/{MEDIA_ID}/{TIMELINE_ID}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]"""
)

append_once(
    "database/evidence.yml",
    f"  - id: {EVIDENCE_ID}",
    f"""  - id: {EVIDENCE_ID}
    name: 'CCHS 1895 Welcome Arch photo fixes Sixth/Main and shows target predecessor frontage in right background'
    type: "Institutional photograph/catalog metadata plus direct visual review; documented/direct for 1895 Sixth/Main scene and probable/working-hypothesis for individual later-address mapping"
    claims:
      - 'CCHS {TARGET_CATALOG} catalogs Oregon City "Welcome Arch", 6th and Main, dated 1895.'
      - "The photograph directly shows the decorated arch and commercial Main Street storefronts extending beyond it."
      - "Project steward identifies the predecessor frontage later associated with 501/503/505 in the right-hand background; this is consistent with corrected Sixth-to-Fifth orientation and 1892 Sanborn geometry."
      - "The later address numbers are not visible; individual storefront-to-number boundaries and structural continuity remain unresolved."
    confidence: "Very High for CCHS object/date/location and visible streetscape; PROBABLE / WORKING HYPOTHESIS for individual later-address storefront mapping."
    related_sources: [{SOURCE_ID}, S-204, S-214, S-018]
    related_buildings: [B-005, B-001, B-002]"""
)

append_once(
    "database/timeline.yml",
    f"  - id: {TIMELINE_ID}",
    f"""  - id: {TIMELINE_ID}
    date: 1895
    summary: CCHS Welcome Arch photograph is cataloged at Sixth/Main; project steward identifies the predecessor frontage later associated with 501/503/505 in the right-hand background beyond the arch.
    confidence: Very High for CCHS date/location and visible streetscape; PROBABLE / WORKING HYPOTHESIS for individual later-address storefront boundaries. No pre-1906 numbering or structural-continuity inference.
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}, S-204, S-214, S-018]
    related_buildings: [B-005, B-001, B-002]"""
)

# Building linkage.
for building_id in ("B-005", "B-001", "B-002"):
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_evidence", EVIDENCE_ID)
    add_entity_yaml_list_item("database/buildings.yml", building_id, "related_sources", SOURCE_ID)

for building_file in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    append_inline_id(building_file, "- Related evidence:", EVIDENCE_ID)
    append_inline_id(building_file, "- Related sources:", SOURCE_ID)
    append_once(
        building_file,
        "## 1895 Welcome Arch photograph — fixed Sixth/Main target-side context",
        f"""## 1895 Welcome Arch photograph — fixed Sixth/Main target-side context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` preserves CCHS `{TARGET_CATALOG}`, cataloged **Oregon City "Welcome Arch"**, **6th and Main**, **1895**. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the **right-hand background beyond the arch**.

The institutional Sixth/Main location makes this photograph a strong spatial anchor and is consistent with the corrected right-side orientation in `S-214` / `E-194` and the 1892 Sanborn block geometry. Exact individual storefront-to-later-number boundaries remain **PROBABLE / WORKING HYPOTHESIS** because the later numbers are not visible and formal citywide numbering came later. No occupancy, title, or continuity to post-1922/surviving structures is inferred."""
    )

# Address timelines.
for timeline_file, address in (
    ("timelines/501-main.md", "501"),
    ("timelines/503-main.md", "503"),
    ("timelines/505-main.md", "505"),
):
    append_once(
        timeline_file,
        "## 1895 — Welcome Arch / Sixth-Main fixed-location photo context",
        f"""## 1895 — Welcome Arch / Sixth-Main fixed-location photo context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` is cataloged by CCHS at **6th and Main** in **1895**. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the right-hand background. For the later **{address} Main** timeline, treat the photo as strong fixed-location block context but **PROBABLE / WORKING HYPOTHESIS** for the exact individual predecessor storefront boundary. Do not backdate the later street number or infer structural continuity."""
    )

# Media metadata and inventories.
append_once(
    "media/photo-metadata-register.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Oregon City "Welcome Arch", 6th and Main, 1895
- Repository file: `{REPO_IMAGE}`
- CCHS object: `{TARGET_CATALOG}`
- Catalog title: **Oregon City "Welcome Arch"**
- Catalog description/location: **Oregon City "Welcome Arch", 6th and Main.**
- Catalog date: **1895**
- Medium / negative location: **Negative / Society Collection**
- Other identifiers: **Culp, Ed 40**; **Stevens Photo #97**
- CCHS/API: {catalog_link} ; {entry_url}
- Repository derivative: **{repo_width} × {repo_height}**, **{repo_bytes:,} bytes**, SHA-256 `{repo_sha}`
- Steward attachment: `{STEWARD['filename']}`; **{STEWARD['width']} × {STEWARD['height']}**, **{STEWARD['bytes']:,} bytes**, SHA-256 `{STEWARD['sha256']}`
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`
- Target relevance: project steward identifies the predecessor frontage later associated with **501/503/505** in the **right-hand background beyond the arch**. CCHS directly supplies Sixth/Main and 1895, but individual storefront-to-later-number boundaries remain **PROBABLE / WORKING HYPOTHESIS**; no pre-1906 numbering or post-1922 continuity inference.
- Review: `{SOURCE_CAPTURE}`"""
)

append_once(
    "media/photos/inventory.md",
    f"### {MEDIA_ID} —",
    f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG} Oregon City "Welcome Arch", 6th and Main, 1895
- File: `{REPO_IMAGE}`
- Dimensions: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Institutional metadata: CCHS **Oregon City "Welcome Arch"**, **6th and Main**, **1895**; Culp, Ed 40; Stevens Photo #97.
- Source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`.
- Target relevance: steward identifies later 501/503/505 predecessor frontage in the right-hand background; individual later-address boundaries remain **PROBABLE / WORKING HYPOTHESIS**."""
)

append_once(
    "media/photos/early-main-street/README.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Oregon City "Welcome Arch", 6th and Main, 1895

`{Path(REPO_IMAGE).name}` preserves the largest public derivative recovered from the exact CCHS object. CCHS directly catalogs the scene at **6th and Main** in **1895**. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the right-hand background beyond the arch. This is strong fixed-location target-block context, but exact individual later-address boundaries remain **PROBABLE / WORKING HYPOTHESIS** and no pre-1906 numbering or post-1922 continuity is inferred. See `{SOURCE_ID}` / `{EVIDENCE_ID}` and `{SOURCE_CAPTURE}`."""
)

# Crosswalk, global timeline, map comparison, research log.
append_once(
    "indexes/id-crosswalk.md",
    f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} —",
    f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} — CCHS 1895 Welcome Arch at Sixth/Main
- Source: `{SOURCE_ID}` — CCHS `{TARGET_CATALOG}`, **Oregon City "Welcome Arch"**, 6th and Main, 1895.
- Evidence: `{EVIDENCE_ID}` — fixed Sixth/Main streetscape with steward-identified later 501/503/505 predecessor frontage in right-hand background.
- Media: `{MEDIA_ID}` — `{REPO_IMAGE}`.
- Timeline: `{TIMELINE_ID}` — 1895 fixed-location target-block photo context.
- Related buildings: `B-005` / `B-001` / `B-002`; comparisons `S-204` / `E-184`, `S-214` / `E-194`; map `SM-005` / `S-018` / `E-020`.
- Limit: later street numbers are not visible or backdated; exact individual storefront boundaries and structural continuity remain unresolved.
- Review: `{SOURCE_CAPTURE}`."""
)

append_once(
    "timeline.md",
    "## 1895 — Welcome Arch at Sixth/Main shows later 501/503/505 predecessor frontage in right background",
    f"""## 1895 — Welcome Arch at Sixth/Main shows later 501/503/505 predecessor frontage in right background

CCHS `{TARGET_CATALOG}` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`) is cataloged **Oregon City "Welcome Arch"**, **6th and Main**, **1895**. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the **right-hand background beyond the arch**. Because the institution directly fixes the Sixth/Main location, this is strong block-level spatial evidence and is consistent with the corrected right-side orientation of `IMG-0743` and the 1892 Sanborn. Exact individual later-address storefront boundaries remain **PROBABLE / WORKING HYPOTHESIS**; the later numbers are not visible and structural continuity is not inferred."""
)

append_once(
    "maps/sanborn-comparison-503-505-507.md",
    "## 1895 CCHS Welcome Arch / Sixth-Main photo cross-check",
    f"""## 1895 CCHS Welcome Arch / Sixth-Main photo cross-check

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` adds CCHS `{TARGET_CATALOG}`, directly cataloged at **6th and Main** in **1895**. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the right-hand background beyond the arch.

This source should be aligned against `SM-005` (1892), `SM-006` (1900), fixed-location P-1456 (`S-204` / `E-184`) and `IMG-0743` (`S-214` / `E-194`). The cataloged Sixth/Main position makes it a particularly useful geometry anchor. Use party walls, facade widths, roof forms and the Fifth intersection to assign individual predecessor storefronts; until that alignment is complete, exact 501/503/505 boundaries remain **PROBABLE / WORKING HYPOTHESIS**."""
)

append_once(
    "registers/research-log.md",
    "## 4 September 2026 — CCHS Welcome Arch 1895 photo integration",
    f"""## 4 September 2026 — CCHS Welcome Arch 1895 photo integration

- Preserved `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}` for CCHS `{TARGET_CATALOG}`, **Oregon City "Welcome Arch"**, **6th and Main**, **1895**.
- Exact CCHS object and largest public derivative retrieved by catalog number; steward upload separately tracked by original filename, dimensions, bytes and SHA-256.
- Project steward identifies the predecessor frontage later associated with **501/503/505 Main** in the **right-hand background beyond the arch**.
- Classified the Sixth/Main date/location and visible streetscape as **DOCUMENTED / DIRECT**; exact individual later-address storefront boundaries remain **PROBABLE / WORKING HYPOTHESIS**.
- No pre-1906 numbered-address, occupancy, ownership, or structural-continuity claim was introduced."""
)

print(f"Integrated {TARGET_CATALOG} as {MEDIA_ID} / {SOURCE_ID} / {EVIDENCE_ID} / {TIMELINE_ID}")
print(f"Repository image: {REPO_IMAGE} ({repo_width}x{repo_height}, {repo_bytes} bytes, sha256 {repo_sha})")
