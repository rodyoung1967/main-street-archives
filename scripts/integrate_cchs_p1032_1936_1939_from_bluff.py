from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1032"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1930s - From Bluff.jpg",
    "width": 2048,
    "height": 1372,
    "bytes": 813578,
    "sha256": "41b1fa63e264689c39a78f6bb3e522eb96520d10b91051c29299e8abd92d8b00",
}
CATALOG = {
    "title": "Oregon City 1930s - From Bluff",
    "entry_object_id": TARGET,
    "description": "Oregon City photo from Bluff looking down on railroad tracks and Tunnel entrance on Highway 99E.",
    "date_made": "1936 - 1939",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Halon",
}

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET, "size": 200})

def rd(path):
    return Path(path).read_text(encoding="utf-8")

def wr(path, text):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")

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

def find_match(obj):
    if isinstance(obj, dict):
        if catno(obj) == TARGET and str(obj.get("account_id")) == ACCOUNT:
            return obj
        for v in obj.values():
            m = find_match(v)
            if m is not None:
                return m
    elif isinstance(obj, list):
        for v in obj:
            m = find_match(v)
            if m is not None:
                return m
    return None

def choose_derivative(entry):
    found = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path") or "thumbnail" in key.lower():
                continue
            w = int(val.get("width") or 0); h = int(val.get("height") or 0)
            if w and h:
                found.append((w*h, w, h, key, val["path"]))
    if not found:
        raise SystemExit(f"No public image derivative found for {TARGET}")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}

for p in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    if TARGET in rd(p):
        print(f"{TARGET} already integrated; no changes needed.")
        raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
MID = next_id("media/photo-metadata-register.md", "IMG", 4)

search = get_json(SEARCH_URL)
match = find_match(search)
if match is None:
    raise SystemExit(f"Exact CCHS catalog number {TARGET} in account {ACCOUNT} not returned by {SEARCH_URL}")
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
with Image.open(BytesIO(data)) as im:
    w, h = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()
slug = entry.get("slug") or match.get("slug")
HUB = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}" if slug else ENTRY

IMAGE = f"media/photos/main-street/{MID}_1936-1939-oregon-city-from-bluff-highway99e-cchs-p1032.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)
CAP = "evidence/source-captures/cchs-p1032-1936-1939-oregon-city-from-bluff-highway99e-2026-09-05.md"
API = "evidence/source-captures/cchs-p1032-1936-1939-from-bluff-api-2026-09-05.json"

wr(API, json.dumps({
    "reviewed": REVIEW,
    "catalog": TARGET,
    "search_url": SEARCH_URL,
    "entry_url": ENTRY,
    "hub_url": HUB,
    "selected_derivative": der,
    "repository_file": IMAGE,
    "repository_image": {"width": w, "height": h, "bytes": nbytes, "sha256": sha},
    "steward_upload": STEWARD,
    "catalog_metadata_supplied_by_steward": CATALOG,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS {TARGET} — Oregon City from bluff, 1936–1939

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made: **1936–1939**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of Negative: **Halon**
- Public record: {HUB}
- Public API: {ENTRY}

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact `{TARGET}` catalog object
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-upload fingerprint is retained even when the repository derivative differs in encoding or dimensions.

## Direct visual review

The bluff view directly shows the lower Oregon City urban/transportation landscape, including the railroad tracks, Highway 99E/tunnel-approach corridor, Oregon City–West Linn bridge, commercial/industrial blocks, and multiple period signs.

For the **503/505 Main research question**, enlarged review of the supplied image does **not** yield a reliable direct reading of a `503`, `505`, or business-name sign that can be securely assigned to either target storefront. Several signs elsewhere in the scene are readable or partly readable, but the target-address signage is too small/oblique for a defensible transcription from this frame alone.

The photograph therefore remains valuable as **dated spatial/context evidence** for 1936–1939, but it is not promoted as new direct business-occupancy evidence for 503 or 505.

## Evidence classification and limits

- **DOCUMENTED / DIRECT:** CCHS object `{TARGET}`, title/description, catalog Date made **1936–1939**, and the visible lower-Oregon-City transportation/commercial scene.
- **VISUALLY VERIFIED:** railroad tracks, Highway 99E/tunnel-approach context, bridge, commercial blocks, and broad streetscape geometry.
- **UNRESOLVED:** exact target-storefront sign transcription for 503/505 from this view; no target business name is assigned from this photograph alone.
- Failure to read a 503/505 sign is **not** evidence that a sign or business was absent.

## Research use

Use this photograph as a contemporaneous bluff-view control alongside the canonical 1936 city aerial (`IMG-0007`) and other 1930s street-level photographs. If a higher-resolution original negative/scan becomes available, re-test the 503/505 facade zone for sign text before making any occupancy claim.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — CCHS {TARGET}, Oregon City from bluff, 1936–1939
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`.  
Date: **1936–1939** per catalog Date made field.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media: `{EID}` / `{MID}`.  
Notes: Bluff view of lower Oregon City, railroad tracks and Highway 99E/tunnel approach. Enlarged review does not support a reliable direct 503/505 sign transcription; absence of readable wording is not negative occupancy evidence.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — 1936–1939 bluff photograph provides dated lower-Oregon-City context but no secure 503/505 sign reading
Source: `{SID}`  
Media: `{MID}`  
Type: Primary photographic evidence with institutional catalog metadata  
Claims:
- CCHS `{TARGET}` catalogs the photograph as **Oregon City 1930s - From Bluff**, Date made **1936–1939**.
- The photograph directly depicts lower Oregon City, railroad tracks, Highway 99E/tunnel-approach context, the bridge, and commercial/industrial blocks.
- Enlarged review does **not** support a secure transcription of a `503`, `505`, or target-business sign from this frame alone.
- The unreadable target signage is a visual-resolution limit and is not evidence of absence.
Classification: **DOCUMENTED / DIRECT** for object identity/date and broad scene; **UNRESOLVED** for 503/505 sign transcription.  
Confidence: **Very High** for institutional metadata and broad visual context; unresolved for target-sign text.''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS P-1032, Oregon City from bluff, 1936–1939
- Type: Historic elevated/bluff streetscape photograph
- CCHS catalog: `{TARGET}`
- CCHS title: **{CATALOG["title"]}**
- CCHS Date made: **1936–1939**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Visual note: lower Oregon City/railroad/Highway 99E context; no secure 503/505 sign transcription from the supplied frame.
- Related source/evidence: `{SID}` / `{EID}`''')

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `{IMAGE}`; `{CAP}` | CCHS 1936–1939 bluff view. Direct broad transportation/commercial context; 503/505 sign text remains unresolved at current image scale and is not treated as negative occupancy evidence. |''')

append_once("registers/research-log.md", "CCHS P-1032 1936–1939 bluff view", f'''### 2026-09-05 — CCHS P-1032 1936–1939 bluff view
- Integrated project-steward supplied CCHS photograph `{TARGET}` as `{MID}` / `{SID}` / `{EID}`.
- Preserved the steward-upload fingerprint: `{STEWARD["filename"]}`, {STEWARD["width"]}×{STEWARD["height"]}, {STEWARD["bytes"]:,} bytes, SHA-256 `{STEWARD["sha256"]}`.
- Direct enlarged review found the lower Oregon City / railroad / Highway 99E / bridge context clearly useful, but no `503`, `505`, or target-business sign is secure enough for a new direct occupancy claim.
- The target-sign reading remains unresolved; unreadability is not evidence of absence.
- This integration does not change annual research-status certifications.''')

append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "CCHS {TARGET} — Oregon City from bluff, 1936–1939"
    url: "{HUB}"
    type: Primary historic photograph with CCHS institutional catalog metadata
    date: "1936-1939"
    repository_file: "{IMAGE}"
    notes: "Bluff view of lower Oregon City, railroad tracks and Highway 99E/tunnel approach; no secure 503/505 sign transcription from current image."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "1936-1939 bluff photograph provides dated lower-Oregon-City context but no secure 503/505 sign reading"
    type: Primary photographic evidence with institutional catalog metadata
    date: "1936-1939"
    claims:
      - "CCHS P-1032 catalogs the photograph as Oregon City 1930s - From Bluff, Date made 1936-1939."
      - "The photograph directly depicts lower Oregon City, railroad tracks, Highway 99E/tunnel-approach context, bridge, and commercial/industrial blocks."
      - "Enlarged review does not support a secure 503, 505, or target-business sign transcription from this frame alone."
      - "Unreadable target signage is a visual-resolution limit and is not evidence of absence."
    confidence: "Very High for object identity/date and broad visual context; unresolved for target-sign text."
    related_sources: [{SID}]
    related_media: [{MID}]
    repository_file: "{CAP}"''')

print(f"Integrated {TARGET}: {SID} {EID} {MID}")
