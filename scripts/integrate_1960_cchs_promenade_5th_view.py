from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "2008.008.003.257"
MEDIA_ID = "IMG-0745"
SOURCE_ID = "S-216"
EVIDENCE_ID = "E-196"
TIMELINE_ID = "T-079"

REPO_IMAGE = "media/photos/early-main-street/IMG-0745_1960-oregon-city-promenade-5th-street-cchs-2008-008-003-257.jpg"
API_CAPTURE = "evidence/source-captures/1960-cchs-2008-008-003-257-promenade-5th-view-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1960-cchs-2008-008-003-257-promenade-5th-view-2026-09-04.md"
SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET_CATALOG, "size": 50})
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "O.C. looking downriver from Promenade at 5th St., 1960.jpg",
    "width": 2048,
    "height": 1372,
    "bytes": 926304,
    "sha256": "104df463198daefcf7047d750b79141853a5e8f1f1477c3245d0f1457531767d",
}
CATALOG_METADATA = {
    "title": "Oregon City (view from the Promenade at 5th St.)",
    "entry_object_id": TARGET_CATALOG,
    "description": "Oregon City (view from the Promenade at 5th St.)",
    "date_made": "1960",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_number": "Stevens 257",
    "stevens_photo_number": "257",
}


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
    (SOURCE_ID, "evidence/source-register.md", rf"(?m)^## {SOURCE_ID}\\b"),
    (EVIDENCE_ID, "evidence/evidence-register.md", rf"(?m)^## {EVIDENCE_ID}\\b"),
    (MEDIA_ID, "media/photo-metadata-register.md", rf"(?m)^## {MEDIA_ID}\\b"),
    (TIMELINE_ID, "database/timeline.yml", rf"(?m)^  - id: {TIMELINE_ID}$"),
]
present = {ident: bool(re.search(pattern, read(path))) for ident, path, pattern in guards}
if any(present.values()):
    if all(present.values()) and Path(REPO_IMAGE).exists():
        print("1960 Promenade photo already integrated; no changes needed.")
        raise SystemExit(0)
    raise SystemExit(f"Partial ID collision detected: {present}; stop rather than reuse/renumber IDs.")

# Retrieve exact institutional object and largest public derivative.
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
    "entry": entry,
}
write(API_CAPTURE, json.dumps(api_record, indent=2, ensure_ascii=False) + "\n")

capture = f"""# CCHS {TARGET_CATALOG} — Oregon City view from the Promenade at 5th Street, 1960

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt record recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. DOCUMENTED / DIRECT FOR THE 1960 ELEVATED DOWNTOWN VIEW; TARGET 501/503/505 BUILDING-LEVEL IDENTIFICATION IS NOT ASSIGNED IN THIS INTEGRATION.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`.

## Catalog record

- Institutional title: **Oregon City (view from the Promenade at 5th St.)**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **Oregon City (view from the Promenade at 5th St.)**
- Date made: **1960**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of negative: **Society Collection**
- Other No.: **Stevens 257**
- Stevens Photo #: **257**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact catalog object; the steward upload remains separately tracked by filename, dimensions, bytes and hash.

## Direct visual observation

The photograph is an elevated view over downtown Oregon City toward the Willamette River and bridge. It directly records the 1960 downtown roofscape, street grid, commercial blocks, automobiles, utility infrastructure, and river/bridge context. Readable large-scale signage includes **GEO. W. DUNMIRE, INC. / Oldsmobile** in the foreground. The image is especially useful as a dated broad comparison frame for downtown building massing and rear/roof conditions.

## Target-property relevance and limits

The catalog fixes the camera context as the **Promenade at 5th Street** and dates the image to **1960**. Because the view encompasses the lower downtown blocks around Fifth/Main, it may be useful for later photo-to-map alignment of the 501/503/505 block. However, this integration does **not** assign individual visible roofs or walls to `501`, `503`, or `505` without a separate building-by-building alignment.

Classification: **DOCUMENTED / DIRECT** for the CCHS object, 1960 date, Promenade-at-5th viewpoint description, and visible downtown scene; **UNRESOLVED** for exact target-building boundaries and any rear-addition or structural-continuity claim.

## Historical limits

1. The photograph does not by itself identify the individual 501, 503, or 505 structures.
2. No business occupancy, property ownership, remodel, addition, demolition, or construction date is inferred solely from this broad view.
3. Future use for 503/505 rear-footprint analysis should align recognizable block corners, street geometry, rooflines, party walls, and the 1950 Sanborn before assigning target structures.
4. The catalog date is used as institutional metadata; no attempt is made here to narrow the exposure date beyond 1960.

## Best next comparison

Compare this frame with the 1950 Sanborn (`SM-009` where applicable), later aerials/photographs, and known Fifth/Main landmarks to isolate the east-side Fifth-to-Sixth block and test 503/505 rear-footprint conditions in 1960.
"""
write(SOURCE_CAPTURE, capture)

append_once(
    "evidence/source-register.md",
    f"## {SOURCE_ID} —",
    f"""## {SOURCE_ID} — Clackamas County Historical Society {TARGET_CATALOG}, Oregon City view from the Promenade at 5th Street, 1960
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026 and exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media/timeline: `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`.  
Notes: CCHS catalogs the image as **Oregon City (view from the Promenade at 5th St.)**, date **1960**, with **Stevens 257 / Stevens Photo #257** and negative location **Society Collection**. The photograph directly records a broad elevated downtown view toward the river and bridge. Exact 501/503/505 building identification is not assigned in this integration; use as dated structural context pending separate block alignment. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`.""",
)

append_once(
    "evidence/evidence-register.md",
    f"## {EVIDENCE_ID} —",
    f"""## {EVIDENCE_ID} — CCHS 1960 Promenade-at-Fifth elevated downtown view
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / DIRECT** for the dated downtown scene; target-building assignment unresolved.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`; timeline `{TIMELINE_ID}`.  
Claims: CCHS object `{TARGET_CATALOG}` is cataloged **Oregon City (view from the Promenade at 5th St.)**, date **1960**. The photograph directly depicts an elevated downtown Oregon City scene toward the Willamette River and bridge, including commercial rooflines, streets, vehicles and utility infrastructure. It provides a dated comparison frame for downtown building massing and roof/rear conditions.  
Limits: Individual visible structures are not assigned here to 501, 503 or 505 Main; no rear addition, demolition, remodeling, ownership, occupancy or structural-continuity claim is inferred without separate map/photo alignment.  
Confidence: **Very High** for CCHS catalog identity/date/view description and visible downtown content; **UNRESOLVED** for exact target-building mapping.""",
)

append_once(
    "database/sources.yml",
    f"  - id: {SOURCE_ID}\n",
    f"""  - id: {SOURCE_ID}
    name: "Clackamas County Historical Society {TARGET_CATALOG}, Oregon City view from the Promenade at 5th Street, 1960"
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "CCHS object {TARGET_CATALOG}; 1960 elevated downtown view from the Promenade at 5th St. Steward image visually verified; exact 501/503/505 building assignment remains unresolved. Related {EVIDENCE_ID}/{MEDIA_ID}/{TIMELINE_ID}. Steward SHA-256 {STEWARD['sha256']}; repository derivative SHA-256 {repo_sha}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]""",
)

append_once(
    "database/evidence.yml",
    f"  - id: {EVIDENCE_ID}\n",
    f"""  - id: {EVIDENCE_ID}
    name: "CCHS 1960 Promenade-at-Fifth elevated downtown view"
    type: "Institutional photograph/catalog metadata plus direct visual review"
    claims:
      - "CCHS {TARGET_CATALOG} catalogs Oregon City (view from the Promenade at 5th St.) and dates it 1960."
      - "The photograph directly depicts an elevated downtown view toward the Willamette River and bridge, documenting commercial rooflines, streets, automobiles and utility infrastructure."
      - "The frame is useful as dated structural context, but individual 501/503/505 buildings are not assigned without separate photo/map alignment."
    confidence: "Very High for catalog identity/date/view description and visible downtown content; unresolved for exact target-building mapping."
    related_sources: [{SOURCE_ID}]""",
)

append_once(
    "database/timeline.yml",
    f"  - id: {TIMELINE_ID}\n",
    f"""  - id: {TIMELINE_ID}
    date: 1960
    summary: CCHS photograph from the Promenade at 5th Street documents an elevated downtown Oregon City view toward the Willamette River and bridge; exact 501/503/505 building mapping remains unresolved pending photo/map alignment.
    confidence: Very High for CCHS date/view description and visible scene; exact target-building mapping unresolved.
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]""",
)

append_once(
    "media/photo-metadata-register.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Oregon City view from Promenade at 5th St., 1960
- Repository file: `{REPO_IMAGE}`
- CCHS object: `{TARGET_CATALOG}`
- Catalog title: **Oregon City (view from the Promenade at 5th St.)**
- Catalog date: **1960**
- Catalog description: **Oregon City (view from the Promenade at 5th St.)**
- Medium / negative location: **Negative / Society Collection**
- Other numbers: **Stevens 257; Stevens Photo #257**
- Repository derivative: **{repo_width} × {repo_height}**, {repo_bytes:,} bytes, SHA-256 `{repo_sha}`
- Steward upload: `{STEWARD['filename']}`, **{STEWARD['width']} × {STEWARD['height']}**, {STEWARD['bytes']:,} bytes, SHA-256 `{STEWARD['sha256']}`
- Review: **VISUALLY VERIFIED 4 September 2026**. Broad elevated downtown context; exact 501/503/505 building assignment unresolved.
- Related source/evidence/timeline: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}`.""",
)

append_once(
    "media/photos/inventory.md",
    f"### {MEDIA_ID} —",
    f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG} Oregon City view from Promenade at 5th St., 1960
- File: `{REPO_IMAGE}`
- Dimensions: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Source: `{SOURCE_ID}` / `{EVIDENCE_ID}`; CCHS date **1960**.
- View: elevated downtown Oregon City toward the river/bridge from the Promenade at Fifth Street.
- Target status: exact 501/503/505 building assignment unresolved; retained as dated structural comparison context.""",
)

append_once(
    "media/photos/early-main-street/README.md",
    f"## {MEDIA_ID} —",
    f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Promenade at 5th Street view, 1960

`{Path(REPO_IMAGE).name}` preserves the largest public derivative recovered from the exact CCHS object. CCHS catalogs the elevated downtown view from the **Promenade at 5th St.** and dates it **1960**. It is retained as a dated downtown structural/roofline comparison frame. Individual 501/503/505 buildings are not assigned from this broad view without separate map/photo alignment. See `{SOURCE_CAPTURE}`.""",
)

append_once(
    "indexes/id-crosswalk.md",
    f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} —",
    f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} / {TIMELINE_ID} — CCHS 1960 Promenade at Fifth Street downtown view
- Source: `{SOURCE_ID}` — CCHS `{TARGET_CATALOG}`, **Oregon City (view from the Promenade at 5th St.)**, 1960.
- Evidence: `{EVIDENCE_ID}` — dated elevated downtown context; exact 501/503/505 building assignment unresolved.
- Media: `{MEDIA_ID}` — `{REPO_IMAGE}`.
- Timeline: `{TIMELINE_ID}` — 1960 downtown view.
- Review: `{SOURCE_CAPTURE}`.""",
)

append_once(
    "timeline.md",
    "## 1960 — CCHS Promenade at Fifth Street elevated downtown view",
    f"""## 1960 — CCHS Promenade at Fifth Street elevated downtown view

CCHS `{TARGET_CATALOG}` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` / `{TIMELINE_ID}`) is cataloged **Oregon City (view from the Promenade at 5th St.)**, **1960**. The photograph directly records the downtown roofscape, streets, automobiles, utility infrastructure, Willamette River and bridge from an elevated Promenade viewpoint. It is useful as a dated structural comparison frame, but this integration does **not** assign individual visible structures to 501, 503 or 505 Main without separate map/photo alignment.""",
)

append_once(
    "registers/research-log.md",
    "## 4 September 2026 — CCHS 1960 Promenade at Fifth Street photo integration",
    f"""## 4 September 2026 — CCHS 1960 Promenade at Fifth Street photo integration

- Preserved `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{TIMELINE_ID}` for CCHS `{TARGET_CATALOG}`, **Oregon City (view from the Promenade at 5th St.)**, **1960**.
- Exact CCHS object and largest public derivative retrieved by catalog number; project-steward upload visually reviewed and separately hashed.
- Treated the image as **DOCUMENTED / DIRECT** dated downtown structural context. Did not assign individual roofs/walls to 501/503/505 or infer additions, remodeling, ownership or occupancy without separate alignment.
- Best next use: compare against the 1950 Sanborn and later aerials/photos to isolate the east-side Fifth-to-Sixth block and test 503/505 rear-footprint conditions.""",
)

print(f"Integrated {TARGET_CATALOG} as {MEDIA_ID} / {SOURCE_ID} / {EVIDENCE_ID} / {TIMELINE_ID}")
print(f"Repository image: {REPO_IMAGE} ({repo_width}x{repo_height}, {repo_bytes} bytes, sha256 {repo_sha})")
