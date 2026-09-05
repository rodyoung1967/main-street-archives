from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "2008.008.002.425"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1947 - Aerial.jpg",
    "width": 1583,
    "height": 2048,
    "bytes": 1069600,
    "sha256": "0646272020265b20b230ccbf8343cf2f797f70bc39543270443de23102ca92da",
}

CATALOG = {
    "title": "Oregon City 1947 - Aerial",
    "entry_object_id": TARGET,
    "tags": ["Willamette Falls Exhibit - Brain Storm"],
    "description": "Oregon City from the air.",
    "date_made": "1947",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_numbers": ["Gardner 425", "Tripp, Bill #3"],
}

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode(
    {"query": TARGET, "size": 50}
)


def rd(path):
    return Path(path).read_text(encoding="utf-8")


def wr(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path, marker, block):
    text = rd(path)
    if marker in text:
        return
    wr(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def next_id(path, prefix, width):
    vals = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    if not vals:
        raise SystemExit(f"No {prefix} IDs found in {path}")
    return f"{prefix}-{max(vals)+1:0{width}d}"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def catno(obj):
    try:
        return obj["properties"]["hasCatalogNumber"]["value_text"]
    except Exception:
        return None


def prop(obj, key):
    try:
        return obj["properties"][key].get("value_text")
    except Exception:
        return None


def find_match(obj):
    if isinstance(obj, dict):
        if catno(obj) == TARGET:
            return obj
        for value in obj.values():
            match = find_match(value)
            if match is not None:
                return match
    elif isinstance(obj, list):
        for value in obj:
            match = find_match(value)
            if match is not None:
                return match
    return None


def choose_derivative(entry):
    found = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path"):
                continue
            if "thumbnail" in key.lower():
                continue
            width = int(val.get("width") or 0)
            height = int(val.get("height") or 0)
            if width and height:
                found.append((width * height, width, height, key, val["path"]))
    if not found:
        raise SystemExit(f"No public image derivative found for {TARGET}")
    found.sort(reverse=True)
    _, width, height, key, url = found[0]
    return {"key": key, "width": width, "height": height, "url": url}


for path in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    if TARGET in rd(path):
        print(f"{TARGET} already integrated; no changes needed.")
        raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
MID = next_id("media/photo-metadata-register.md", "IMG", 4)

search = get_json(SEARCH_URL)
match = find_match(search)
if match is None:
    raise SystemExit(f"Exact CCHS catalog number {TARGET} not returned by {SEARCH_URL}")
entry_id = match.get("id")
if not entry_id:
    raise SystemExit("Matching CCHS search result has no id")
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{entry_id}"
entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit(f"Fetched entry mismatch: expected {TARGET}, got {catno(entry)}")

der = choose_derivative(entry)
data = get_bytes(der["url"])
if not data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected derivative is not JPEG")
with Image.open(BytesIO(data)) as image:
    width, height = image.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()

slug = entry.get("slug") or match.get("slug")
HUB = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug else ENTRY
)

TITLE = prop(entry, "hasName") or CATALOG["title"]
DESCRIPTION = prop(entry, "hasDescription") or CATALOG["description"]

IMAGE = f"media/photos/aerials/{MID}_1947-oregon-city-aerial-cchs-2008-008-002-425.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-2008-008-002-425-1947-oregon-city-aerial-2026-09-05.md"
API = "evidence/source-captures/cchs-2008-008-002-425-1947-oregon-city-aerial-api-2026-09-05.json"

wr(API, json.dumps({
    "reviewed": REVIEW,
    "catalog": TARGET,
    "search_url": SEARCH_URL,
    "entry_url": ENTRY,
    "hub_url": HUB,
    "selected_derivative": der,
    "repository_file": IMAGE,
    "repository_image": {"width": width, "height": height, "bytes": nbytes, "sha256": sha},
    "steward_upload": STEWARD,
    "catalog_metadata_supplied_by_steward": CATALOG,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

SOURCE_NAME = f"CCHS {TARGET} — Oregon City 1947 aerial"
EVIDENCE_NAME = "1947 CCHS high-oblique aerial provides an independent downtown/riverfront control"

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Tag: **Willamette Falls Exhibit - Brain Storm**
- Description: **{CATALOG["description"]}**
- Date made: **1947**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of Negative: **Society Collection**
- Other Number: **Gardner 425**
- Other Photo #: **Tripp, Bill #3**
- Public record: {HUB}
- Public API: {ENTRY}

Live CatalogIt title recovered during integration: **{TITLE}**. Live description recovered during integration: **{DESCRIPTION}**.

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact catalog object `{TARGET}`
- Dimensions: **{width} × {height}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to the steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

When the repository derivative differs in encoding or dimensions from the steward attachment, the archive treats both as the same institutional photograph/object and preserves the exact steward-file fingerprint above; byte identity is not inferred.

## Direct visual review

The photograph is a high oblique aerial over Oregon City and the Willamette River. It visibly documents:

- lower/downtown Oregon City and its dense commercial/industrial building fabric;
- the Willamette River and the Oregon City–West Linn bridge;
- the riverfront highway/corridor geometry;
- Willamette Falls and the large industrial/mill complex around the falls;
- extensive log booms in the river;
- the west-bank industrial and hillside context.

The **503/505 Main project area lies within the lower-downtown field of view**, but this integration does **not** promote an individual 501, 503, or 505 roof/footprint identification from this oblique photograph. The steep camera angle, dense roofs, and perspective differ materially from the city photocompare plan-view frames.

## Relationship to the canonical aerial sequence

This independent CCHS photograph is cataloged **1947**, placing it chronologically between the city photocompare frames **1944 (`IMG-0009`)** and **1955 (`IMG-0010`)**. The canonical photocompare re-review already establishes that:

- 501 Main was removed between 1936 and 1940; and
- 1940 is the earliest reviewed photocompare frame in which the later deeper rearward 505 footprint can be distinguished relative to 503.

This 1947 oblique is therefore a potentially valuable **independent cross-check**, but it does not change either conclusion until the target block is securely aligned using fixed landmarks.

## Evidence classification and limits

- **DOCUMENTED / DIRECT (institutional catalog):** CCHS `{TARGET}` identifies the photograph as **Oregon City 1947 - Aerial**, Date made **1947**.
- **DOCUMENTED / DIRECT (visual):** broad Oregon City downtown/riverfront, bridge, falls, industrial complex, highway/corridor, and log-boom context.
- **STRONG CHRONOLOGICAL CONTEXT:** the dated 1947 view falls between existing 1944 and 1955 target-area photocompare controls.
- **UNRESOLVED:** exact 501/503/505 roof mapping within this oblique image; whether the 505-vs-503 rear-depth asymmetry can be independently read from this particular view; any new demolition/construction date inferred from it.

Failure to isolate an individual target roof in this oblique photograph is **not** evidence that the building or footprint was absent.

## Highest-value follow-up

Align this 1947 view to `IMG-0009` (1944) and `IMG-0010` (1955) using fixed landmarks such as the bridge approach, river/highway curvature, street grid, large institutional buildings, and surviving block edges. Only after that alignment should this photograph be used to independently test the former 501 corner and the relative rear depths of 503 and 505.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic aerial photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **1947** per CCHS Date made metadata.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Other numbers: **Gardner 425**; **Tripp, Bill #3**.
Related evidence/media: `{EID}` / `{MID}`.
Use limit: dated independent high-oblique downtown/riverfront control. Exact 501/503/505 roof mapping is not yet verified, so no new target-footprint or construction-date claim is made from this source alone.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary historic aerial photographic evidence with institutional catalog metadata
Claims:
- CCHS `{TARGET}` catalogs the photograph as **Oregon City 1947 - Aerial**, Date made **1947**.
- Direct visual review shows lower/downtown Oregon City, the Willamette River, Oregon City–West Linn bridge, riverfront/highway corridor, Willamette Falls industrial complex, and log booms.
- The 1947 date makes the photograph an independent chronological control between city photocompare `IMG-0009` (1944) and `IMG-0010` (1955).
- Exact individual 501/503/505 roof mapping has not yet been verified in this steep oblique view; existing `E-021` / 1940 re-review conclusions remain unchanged.
Classification: **DOCUMENTED / DIRECT** for object identity, 1947 date and broad visual content; **UNRESOLVED** for target-building roof/footprint mapping.
Confidence: **Very High** for CCHS object/date and broad scene; unresolved for 501/503/505-specific geometry.''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS {TARGET}, Oregon City 1947 aerial
- Type: Historic high-oblique aerial photograph
- CCHS catalog: `{TARGET}`
- CCHS title: **{CATALOG["title"]}**
- Date made: **1947**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{width} × {height}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Other numbers: **Gardner 425**; **Tripp, Bill #3**
- Source/Evidence: `{SID}` / `{EID}`
- Visual value: dated 1947 downtown/riverfront high-oblique control between the canonical 1944 and 1955 aerial frames.
- Limit: exact 501/503/505 roof mapping remains unresolved pending fixed-landmark alignment.''')

append_once("media/photos/inventory.md", f"### {MID} —", f'''### {MID} — CCHS 1947 Oregon City aerial
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- CCHS: `{TARGET}`; **Gardner 425**; **Tripp, Bill #3**
- Key value: independent dated **1947** high-oblique downtown/riverfront control between `IMG-0009` (1944) and `IMG-0010` (1955). Exact 501/503/505 roof mapping remains pending.''')

append_once("media/photos/aerials/README.md", f"## Independent CCHS {TARGET} 1947 aerial", f'''## Independent CCHS {TARGET} 1947 aerial

`{MID}` preserves CCHS `{TARGET}`, cataloged **1947**, an independent high-oblique view of Oregon City, the Willamette River, bridge, falls/industrial complex, riverfront corridor and log booms. It falls chronologically between city photocompare `IMG-0009` (1944) and `IMG-0010` (1955). The target 501/503/505 block is within the downtown field, but individual roof mapping has not yet been verified in this oblique geometry; see `{SID}` / `{EID}` and `{CAP}`.''')

append_once("evidence/aerial-5th-main-photocompare-series.md", f"## Independent 1947 CCHS {TARGET} high-oblique control", f'''## Independent 1947 CCHS {TARGET} high-oblique control

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) is an independent **1947** high-oblique aerial rather than a city photocompare screenshot. It provides a valuable dated control between `IMG-0009` (1944) and `IMG-0010` (1955), but the camera angle and dense roof field differ enough that this integration does **not** yet promote an individual 501/503/505 roof assignment. Existing conclusions remain unchanged: 501 removal is bracketed **1936–1940**, and 1940 is the earliest reviewed photocompare frame where the deeper 505 rear footprint can be distinguished relative to 503. Fixed-landmark alignment of the 1947 photograph is the next step before using it as independent target-footprint confirmation.''')

append_once("evidence/research-leads.md", "### 1947 CCHS high-oblique control for RL-005", f'''### 1947 CCHS high-oblique control for RL-005

New CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) supplies a dated **1947** oblique aerial between the canonical 1944 and 1955 plan-view frames. Re-align it using the bridge approach, river/highway curvature, street grid, institutional buildings and block edges, then test whether the former 501 corner and the 505-vs-503 rear-depth asymmetry can be independently read. Do **not** treat current difficulty isolating an individual roof as evidence of absence.''')

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `{IMAGE}`; `{CAP}` | CCHS catalogs the high-oblique Oregon City aerial as **1947**; independent chronological control between `IMG-0009` and `IMG-0010`. Exact 501/503/505 roof mapping remains unresolved pending fixed-landmark alignment. |''')

append_once("registers/research-log.md", f"CCHS {TARGET} 1947 Oregon City aerial", f'''### 2026-09-05 — CCHS {TARGET} 1947 Oregon City aerial
- Preserved as `{MID}` / `{SID}` / `{EID}` from the exact CCHS catalog object, with project-steward upload fingerprint retained.
- Supplied metadata: **Oregon City 1947 - Aerial**, Date made **1947**, description **Oregon City from the air**, other numbers **Gardner 425** and **Tripp, Bill #3**.
- Direct visual review documents broad downtown/riverfront, bridge, Willamette Falls industrial complex, riverfront/highway geometry and log booms.
- Treated as an independent dated control between `IMG-0009` (1944) and `IMG-0010` (1955).
- Exact 501/503/505 roof mapping was **not** promoted from the oblique image; the existing 1936–1940 501-removal bracket and 1940 first-readable 505-depth asymmetry remain unchanged pending fixed-landmark alignment.
- This integration does not alter annual research-status certifications.''')

append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{HUB}"
    type: Primary historic aerial photograph with CCHS institutional catalog metadata
    date: "1947"
    repository_file: "{IMAGE}"
    notes: "Independent dated high-oblique Oregon City aerial; exact 501/503/505 roof mapping remains unresolved pending fixed-landmark alignment. Other numbers Gardner 425 and Tripp, Bill #3."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: Primary historic aerial photographic evidence with institutional catalog metadata
    date: "1947"
    claims:
      - "CCHS {TARGET} catalogs the photograph as Oregon City 1947 - Aerial, Date made 1947."
      - "Direct visual review shows lower/downtown Oregon City, the Willamette River, bridge, riverfront/highway corridor, Willamette Falls industrial complex, and log booms."
      - "The photograph is an independent chronological control between city photocompare IMG-0009 (1944) and IMG-0010 (1955)."
      - "Exact individual 501/503/505 roof mapping is unresolved in this steep oblique view; existing E-021 and 1940 re-review conclusions remain unchanged."
    confidence: "Very High for object identity, 1947 date and broad visual content; unresolved for target-building geometry."
    related_sources: [{SID}]
    related_media: [{MID}]
    repository_file: "{CAP}"''')

print(f"Integrated {TARGET}: {SID} {EID} {MID}")
