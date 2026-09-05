from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "P-1317"
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "Oregon City - View from Bluff.jpg",
    "width": 2048,
    "height": 1503,
    "bytes": 1246287,
    "sha256": "f3218dbee1c625ffd253968052269e6027844f5e61eafe957605e813b7778698",
}
CATALOG_METADATA = {
    "title": "Oregon City - View from Bluff",
    "entry_object_id": TARGET_CATALOG,
    "description": "Oregon City from the Bluff at 5th Street. The original is on the back of B-016-005583.",
    "date_made": None,
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Halon",
    "other_photo_number": "Back of B-0160.005583",
}
STEWARD_TARGET_NOTE = (
    "Project steward identifies the predecessor frontage/building group later associated "
    "with 501, 503 and 505 Main as visible through the tree branches."
)

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode(
    {"query": TARGET_CATALOG, "size": 50}
)


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
        return
    next_m = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + next_m.start() if next_m else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    field_match = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if not field_match:
        return
    field_abs_end = m.start() + field_match.end()
    after = text[field_abs_end:end]
    next_field = re.search(r"(?m)^    [a-zA-Z0-9_]+:", after)
    insert_at = field_abs_end + (next_field.start() if next_field else len(after))
    insertion = f"\n      - {item}"
    text = text[:insert_at].rstrip("\n") + insertion + "\n" + text[insert_at:].lstrip("\n")
    write(path, text)


def next_numeric_id(path: str, prefix: str, width: int) -> str:
    nums = [int(v) for v in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums:
        raise SystemExit(f"No existing {prefix} IDs found in {path}")
    return f"{prefix}-{max(nums)+1:0{width}d}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


# Idempotency: never create a second archive identity for the same CCHS object.
for p in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    if TARGET_CATALOG in read(p):
        print(f"{TARGET_CATALOG} is already integrated in {p}; no changes needed.")
        raise SystemExit(0)

# Allocate the next IDs from the newest checked-out main, so concurrent work cannot steal fixed IDs.
SOURCE_ID = next_numeric_id("evidence/source-register.md", "S", 3)
EVIDENCE_ID = next_numeric_id("evidence/evidence-register.md", "E", 3)
MEDIA_ID = next_numeric_id("media/photo-metadata-register.md", "IMG", 4)
TIMELINE_ID = next_numeric_id("database/timeline.yml", "T", 3)

REPO_IMAGE = (
    f"media/photos/early-main-street/{MEDIA_ID}_undated-oregon-city-view-from-bluff-"
    f"5th-street-cchs-p1317.jpg"
)
API_CAPTURE = (
    "evidence/source-captures/undated-cchs-p1317-oregon-city-view-from-bluff-"
    "5th-street-api-2026-09-04.json"
)
SOURCE_CAPTURE = (
    "evidence/source-captures/undated-cchs-p1317-oregon-city-view-from-bluff-"
    "5th-street-target-frontage-2026-09-04.md"
)

# Retrieve the exact institutional object and the largest public derivative.
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
    if slug
    else None
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

capture = f"""# CCHS {TARGET_CATALOG} — Oregon City - View from Bluff, Fifth Street

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt object recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. EXPOSURE DATE UNRESOLVED. STEWARD IDENTIFICATION OF THE 501/503/505 PREDECESSOR FRONTAGE THROUGH THE TREE BRANCHES IS PROBABLE / WORKING HYPOTHESIS FOR INDIVIDUAL LATER-ADDRESS MAPPING.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`. Related later-address records: `B-005` (501), `B-001` (503), `B-002` (505). Related map/photo controls: `SM-005` / `S-018` (1892 Sanborn), `SM-006` / `S-019` (1900 Sanborn), `S-213` / `E-193` / `IMG-0742` (1895 bluff view), and `S-215` / `E-195` / `IMG-0744` (1895 Welcome Arch).

## Catalog record supplied by project steward

- Institutional title: **Oregon City - View from Bluff**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **Oregon City from the Bluff at 5th Street. The original is on the back of B-016-005583.**
- Date made: **not supplied**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of negative: **Halon**
- Other Photo #: **Back of B-0160.005583**
- Note on identifier wording: the description and Other Photo # use slightly different `B-016...` strings; both are preserved exactly as supplied rather than normalized.
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
- Public derivative recovered from the exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact catalog object; the steward upload remains separately tracked by filename, dimensions, bytes and hash as a substantive duplicate of the same institutional photograph.

## Direct visual observation

The photograph is an elevated bluff view over lower Oregon City. A seated man appears in the left foreground. Trees and branches frame and partly obscure the downtown scene. The view directly records a dense commercial roofscape, streets, the Willamette-side industrial complex, smoke/steam, and a prominent **HOTEL** roof sign. The target-side downtown buildings are partly visible through the branches rather than presented as an unobstructed facade view.

No later `501`, `503`, or `505` street number is readable in the photograph.

## Target-frontage interpretation

CCHS's description directly fixes the viewpoint as **the Bluff at 5th Street**. The project steward identifies the predecessor frontage/building group later associated with **501, 503 and 505 Main** as visible **through the tree branches**.

That identification is spatially plausible and valuable because the Fifth Street bluff viewpoint constrains the target block more strongly than an unlocated city overview. However, branches obscure substantial portions of the scene, the catalog supplies no exposure date, and the later address numbers are not visible. This image therefore does **not** establish which visible wall/roof belongs to later 501 versus 503 versus 505, nor that one physical building spanned all three later numbers.

Classification: **DOCUMENTED / DIRECT** for the CCHS object, Bluff-at-Fifth location description and visible downtown scene; **PROBABLE / WORKING HYPOTHESIS** for exact identification of the partially obscured predecessor 501/503/505 frontage and its individual later-address boundaries; **UNRESOLVED** for exposure date and structural continuity.

## Historical limits

1. The catalog metadata supplied here gives **no exposure date**. Do not date the photograph from clothing, vegetation, industrial appearance, accession numbering, or architectural resemblance alone.
2. The steward's 501/503/505 identification is a later-address spatial interpretation; no such number is visible in the image.
3. Do not treat the visible frontage as proof that one building occupied all three later addresses.
4. The photograph does not by itself prove business occupancy, title, construction date, demolition date, or continuity into the 1907–1918 numbered premises, the 1922 fire/rebuild sequence, or the surviving 503/505 structures.
5. The two related-object strings `B-016-005583` and `B-0160.005583` are retained as catalog wording variants pending inspection of the referenced original/backing item.

## Best next comparison

Align the partially obscured target frontage against the 1892 and 1900 Sanborn sheets, the fixed-location 1895 Welcome Arch view (`IMG-0744`), the other 1895 bluff photograph (`IMG-0742`), and the 1890 Sixth/Main views (`IMG-0732` / `IMG-0733`). Use Fifth/Main street geometry, roof heights, party walls, setbacks and neighboring landmarks to test the steward identification and, if possible, bracket the exposure date without assuming building continuity.
"""
write(SOURCE_CAPTURE, capture)

append_once(
    "evidence/source-register.md",
    f"## {SOURCE_ID} —",
    f"""## {SOURCE_ID} — Clackamas County Historical Society {TARGET_CATALOG}, Oregon City - View from Bluff at Fifth Street
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026; exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media/timeline: `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`.  
Notes: CCHS describes the image as **Oregon City from the Bluff at 5th Street** and supplies no exposure date in the steward metadata. Project steward identifies the predecessor frontage/building group later associated with 501/503/505 Main as visible through tree branches. Treat exact individual later-address mapping as **PROBABLE / WORKING HYPOTHESIS**. Preserve the description's `B-016-005583` and Other Photo # `Back of B-0160.005583` as separate supplied strings. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`.""",
)

append_once(
    "evidence/evidence-register.md",
    f"## {EVIDENCE_ID} —",
    f"""## {EVIDENCE_ID} — CCHS P-1317 Fifth Street bluff view shows probable 501/503/505 predecessor frontage through branches
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / DIRECT** for the Bluff-at-Fifth scene; **PROBABLE / WORKING HYPOTHESIS** for exact later-address frontage mapping.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`.  
Claims: CCHS object `{TARGET_CATALOG}` is titled **Oregon City - View from Bluff** and described as **Oregon City from the Bluff at 5th Street**. The image directly shows an elevated downtown Oregon City scene partly obscured by trees. Project steward identifies the predecessor frontage/building group later associated with **501/503/505 Main** as visible through the branches.  
Limits: The catalog supplies no exposure date; no 501/503/505 number is readable; individual storefront/roof boundaries are not assigned; no one-building-across-three-addresses or structural-continuity inference is made.  
Confidence: **Very High** for CCHS object/view description and visible scene; **PROBABLE / WORKING HYPOTHESIS** for the target-frontage identification; exposure date **UNRESOLVED**.""",
)

append_once(
    "database/sources.yml",
    f"  - id: {SOURCE_ID}\n",
    f"""  - id: {SOURCE_ID}
    name: "Clackamas County Historical Society {TARGET_CATALOG}, Oregon City - View from Bluff at Fifth Street"
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "CCHS P-1317; Oregon City from the Bluff at 5th Street; exposure date not supplied. Steward identifies probable predecessor 501/503/505 frontage through tree branches; exact later-address boundaries unresolved. Related {EVIDENCE_ID}/{MEDIA_ID}/{TIMELINE_ID}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]
    related_buildings: [B-005, B-001, B-002]""",
)

append_once(
    "database/evidence.yml",
    f"  - id: {EVIDENCE_ID}\n",
    f"""  - id: {EVIDENCE_ID}
    name: "CCHS P-1317 Fifth Street bluff view shows probable 501/503/505 predecessor frontage through branches"
    type: "Institutional photograph/catalog metadata plus direct visual review"
    claims:
      - "CCHS P-1317 is titled Oregon City - View from Bluff and described as Oregon City from the Bluff at 5th Street."
      - "The photograph directly depicts an elevated downtown Oregon City scene partly obscured by trees; the project steward identifies the predecessor frontage later associated with 501/503/505 Main through the branches."
      - "No later target number is visible and individual 501/503/505 boundaries remain unresolved."
      - "The exposure date is not supplied in the steward catalog metadata."
    confidence: "Very High for catalog identity/view description and visible scene; probable/working hypothesis for exact target-frontage mapping; exposure date unresolved."
    related_sources: [{SOURCE_ID}]
    related_buildings: [B-005, B-001, B-002]""",
)

append_once(
    "database/timeline.yml",
    f"  - id: {TIMELINE_ID}\n",
    f"""  - id: {TIMELINE_ID}
    date: Undated
    summary: CCHS P-1317 shows Oregon City from the Bluff at 5th Street; the project steward identifies the partially branch-obscured predecessor frontage later associated with 501/503/505 Main, but individual later-address boundaries and exposure date remain unresolved.
    confidence: Very High for CCHS viewpoint description and visible scene; probable/working hypothesis for exact target-frontage mapping; exposure date unresolved.
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
    related_buildings: [B-005, B-001, B-002]""",
)

append_once(
    "media/photo-metadata-register.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS P-1317 Oregon City - View from Bluff at Fifth Street
- Repository file: `{REPO_IMAGE}`
- CCHS object: `{TARGET_CATALOG}`
- Catalog title: **Oregon City - View from Bluff**
- Catalog description: **Oregon City from the Bluff at 5th Street. The original is on the back of B-016-005583.**
- Catalog date: **not supplied / unresolved**
- Place: **Oregon City, Clackamas County, Oregon**
- Medium / negative location: **Photographic Paper / Halon**
- Other Photo #: **Back of B-0160.005583**
- Identifier note: description and Other Photo # use different supplied `B-016...` strings; both retained verbatim.
- Repository derivative: **{repo_width} × {repo_height}**, {repo_bytes:,} bytes, SHA-256 `{repo_sha}`
- Steward upload: `{STEWARD['filename']}`, **{STEWARD['width']} × {STEWARD['height']}**, {STEWARD['bytes']:,} bytes, SHA-256 `{STEWARD['sha256']}`
- Review: **VISUALLY VERIFIED 4 September 2026**. Elevated downtown scene framed/obscured by trees; project steward identifies probable predecessor 501/503/505 frontage through branches.
- Boundary: exact individual later-address assignment, exposure date and structural continuity remain unresolved.
- Related source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`.""",
)

append_once(
    "media/photos/inventory.md",
    f"### {MEDIA_ID} —",
    f"""### {MEDIA_ID} — CCHS P-1317 Oregon City view from Bluff at Fifth Street
- File: `{REPO_IMAGE}`
- Dimensions: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Source/evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`; exposure date **not supplied**.
- View: elevated Oregon City from the Fifth Street bluff, partially obscured by trees.
- Steward target note: predecessor frontage later associated with 501/503/505 is visible through branches.
- Limit: individual later-address boundaries, date and structural continuity remain unresolved.""",
)

append_once(
    "media/photos/early-main-street/README.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS P-1317 Oregon City - View from Bluff at Fifth Street

`{Path(REPO_IMAGE).name}` preserves the largest public derivative recovered from the exact CCHS P-1317 object. CCHS describes the view as **Oregon City from the Bluff at 5th Street**; no exposure date is supplied. The project steward identifies the predecessor frontage later associated with **501/503/505 Main** through the tree branches. Exact individual later-address boundaries and structural continuity remain **PROBABLE / WORKING HYPOTHESIS / UNRESOLVED**. See `{SOURCE_CAPTURE}`.""",
)

append_once(
    "indexes/id-crosswalk.md",
    f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} —",
    f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} — CCHS P-1317 Fifth Street bluff view
- Source: `{SOURCE_ID}` — CCHS `P-1317`, **Oregon City - View from Bluff**, description fixes Bluff at Fifth Street.
- Evidence: `{EVIDENCE_ID}` — project-steward probable identification of the branch-obscured predecessor 501/503/505 frontage; individual later-address mapping and exposure date unresolved.
- Media: `{MEDIA_ID}` — `{REPO_IMAGE}`.
- Timeline: `{TIMELINE_ID}` — undated bluff-view context.
- Review: `{SOURCE_CAPTURE}`.""",
)

append_once(
    "timeline.md",
    "## Undated — CCHS P-1317 Fifth Street bluff view / probable 501-503-505 predecessor frontage",
    f"""## Undated — CCHS P-1317 Fifth Street bluff view / probable 501-503-505 predecessor frontage

CCHS `P-1317` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`) is titled **Oregon City - View from Bluff** and described as **Oregon City from the Bluff at 5th Street**. The photograph directly shows an elevated downtown scene partly obscured by trees. The project steward identifies the predecessor frontage/building group later associated with **501/503/505 Main** as visible through the branches.

The catalog metadata supplied with the image gives **no exposure date**, and no later target street number is readable. Treat exact target-frontage identification as **PROBABLE / WORKING HYPOTHESIS** and individual 501-versus-503-versus-505 roof/storefront assignment, one-building-versus-multiple-buildings interpretation, and structural continuity as unresolved.""",
)

target_building_block = f"""## Undated CCHS P-1317 Fifth Street bluff photograph

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` preserves CCHS `P-1317`, **Oregon City - View from Bluff**, described as **Oregon City from the Bluff at 5th Street**. The project steward identifies the predecessor frontage/building group later associated with **501/503/505 Main** as visible through the tree branches.

For this address record, use the photo as **PROBABLE / WORKING HYPOTHESIS** spatial/structural context only. The catalog supplies no exposure date, the later street numbers are not visible, branches obscure the target area, and the image does not establish individual 501/503/505 boundaries or continuity into later numbered/surviving structures."""

for bpath in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    append_inline_id(bpath, "- Related evidence:", EVIDENCE_ID)
    append_inline_id(bpath, "- Related sources:", SOURCE_ID)
    append_once(bpath, "## Undated CCHS P-1317 Fifth Street bluff photograph", target_building_block)

for bid in ("B-005", "B-001", "B-002"):
    add_entity_yaml_list_item("database/buildings.yml", bid, "related_evidence", EVIDENCE_ID)
    add_entity_yaml_list_item("database/buildings.yml", bid, "related_sources", SOURCE_ID)

timeline_block = f"""## Undated — CCHS P-1317 Fifth Street bluff photo context

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` is CCHS `P-1317`, described as **Oregon City from the Bluff at 5th Street**. The project steward identifies the partially branch-obscured predecessor frontage later associated with **501/503/505 Main**. Use this as **PROBABLE / WORKING HYPOTHESIS** spatial context only: the exposure date is not supplied, later address numbers are not visible, and individual storefront/roof boundaries and structural continuity remain unresolved."""

for tpath in ("timelines/501-main.md", "timelines/503-main.md", "timelines/505-main.md"):
    append_once(tpath, "## Undated — CCHS P-1317 Fifth Street bluff photo context", timeline_block)

append_once(
    "maps/sanborn-comparison-503-505-507.md",
    "## Undated CCHS P-1317 Fifth Street bluff-photo comparison target",
    f"""## Undated CCHS P-1317 Fifth Street bluff-photo comparison target

CCHS `P-1317` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}`) is described as **Oregon City from the Bluff at 5th Street**. The project steward identifies the predecessor frontage later associated with 501/503/505 Main through tree branches. The image has no supplied exposure date and does not visibly print the later numbers.

Use this frame as a photo/Sanborn alignment target, not a dated footprint map. Compare its partially obscured roof/wall sequence against `SM-005` (1892), `SM-006` (1900), `IMG-0742`, `IMG-0744`, and the fixed 1890 Sixth/Main views. A successful alignment may strengthen the target-frontage identification and help bracket the exposure date; it must not be used to assume building continuity across the 1922 fire/rebuild sequence.""",
)

append_once(
    "registers/research-log.md",
    "## 4 September 2026 — CCHS P-1317 Fifth Street bluff photo integration",
    f"""## 4 September 2026 — CCHS P-1317 Fifth Street bluff photo integration

- Preserved `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}` for CCHS `P-1317`, **Oregon City - View from Bluff**, described as Oregon City from the Bluff at 5th Street.
- Exact CCHS object and largest public derivative retrieved by catalog number; steward upload visually reviewed and separately hashed.
- Catalog metadata supplied with the image gives **no exposure date**. The description's `B-016-005583` and Other Photo # `Back of B-0160.005583` variants were both retained rather than normalized.
- Project steward identifies the predecessor frontage/building group later associated with 501/503/505 Main through the tree branches. Recorded as **PROBABLE / WORKING HYPOTHESIS** for exact later-address mapping; no individual address boundary, single-building claim or structural continuity inferred.
- Best next step: align with 1892/1900 Sanborn, 1890 Sixth/Main photographs, and the 1895 bluff/Welcome-Arch views to test the target mapping and possibly bracket the exposure date.""",
)

print(
    f"Integrated {TARGET_CATALOG} as {MEDIA_ID} / {SOURCE_ID} / "
    f"{EVIDENCE_ID} / {TIMELINE_ID}"
)
print(
    f"Repository image: {REPO_IMAGE} ({repo_width}x{repo_height}, "
    f"{repo_bytes} bytes, sha256 {repo_sha})"
)
