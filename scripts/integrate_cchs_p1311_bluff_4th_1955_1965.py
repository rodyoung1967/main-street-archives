from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1311"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1955 - from the Bluff at 4th Street Looking Northwest.jpg",
    "width": 2048,
    "height": 1616,
    "bytes": 909725,
    "sha256": "e04639c56001073eed1c010708298ca50460e0380b8e004509732328696bde98",
    "visual_note": "Project steward identifies THE WHEEL wording on the 503 Main frontage and 505 TAVERN wording/signage on the 505 Main frontage.",
}

CATALOG = {
    "title": "Oregon City 1955 - from the Bluff at 4th Street Looking Northwest",
    "entry_object_id": TARGET,
    "description": "Oregon City from the Bluff at 4th Street Looking Northwest. West Linn Inn in background.",
    "date_made": "1955 - 1965",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Halon",
}

EVIDENCE_NAME = "1955-1965 bluff photograph documents The Wheel at 503 and 505 Tavern signage at 505"
TIMELINE_SUMMARY = (
    "CCHS P-1311, cataloged 1955-1965, shows the 5th/Main target frontage from the bluff at 4th Street. "
    "Project-steward visual identification, supported by direct enlarged review, reads The Wheel on the 503 frontage "
    "and 505 Tavern signage on the adjacent 505 frontage. The broad catalog date range does not establish a single exposure year."
)

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


def find_match(obj):
    if isinstance(obj, dict):
        if catno(obj) == TARGET:
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
            if not isinstance(val, dict) or not val.get("path"):
                continue
            if "thumbnail" in key.lower():
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                found.append((w*h, w, h, key, val["path"]))
    if not found:
        raise SystemExit("No public image derivative found for P-1311")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}


def yaml_add_list_item(path, entity_id, field, item):
    text = rd(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        return
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    fm = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if not fm:
        return
    field_start = m.start() + fm.end()
    after = text[field_start:end]
    nf = re.search(r"(?m)^    [A-Za-z0-9_]+:", after)
    insert_at = field_start + (nf.start() if nf else len(after))
    insertion = f"\n      - {item}"
    text = text[:insert_at].rstrip("\n") + insertion + "\n" + text[insert_at:].lstrip("\n")
    wr(path, text)


for p in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    if TARGET in rd(p):
        print(f"{TARGET} already integrated; no changes needed.")
        raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
MID = next_id("media/photo-metadata-register.md", "IMG", 4)
TID = next_id("database/timeline.yml", "T", 3)

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
im = Image.open(BytesIO(data))
w, h = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()

slug = entry.get("slug") or match.get("slug")
HUB = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug else ENTRY
)

IMAGE = f"media/photos/main-street/{MID}_1955-1965-bluff-4th-looking-northwest-wheel-503-505-tavern-cchs-p1311.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-p1311-1955-1965-bluff-4th-looking-northwest-wheel-503-505-tavern-2026-09-05.md"
API = "evidence/source-captures/cchs-p1311-1955-1965-bluff-4th-looking-northwest-api-2026-09-05.json"
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
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS {TARGET} — bluff at 4th Street looking northwest, 1955–1965

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`. Related buildings/businesses: `B-001` / `BUS-004` (503 Main / The Wheel) and `B-002` / `BUS-005` (505 Main / 505 Tavern).

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made: **{CATALOG["date_made"]}**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of Negative: **Halon**
- Public record: {HUB}
- Public API: {ENTRY}

The title begins with **“Oregon City 1955”**, while the catalog's Date made field is **1955–1965**. The archive preserves both and does not silently convert the title's “1955” into an exact exposure date.

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`
- Steward visual note: **{STEWARD["visual_note"]}**

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact catalog object `{TARGET}`
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`

## Direct visual review

The elevated bluff photograph looks northwest across lower Oregon City. It directly shows the 5th/Main intersection and the target Main Street frontage. Enlarged review of the supplied image supports the steward's identification of:

- **THE WHEEL** wording/signage on the 503 Main frontage;
- **505 TAVERN** / **TAVERN 505** signage on the immediately adjacent 505 Main frontage;
- the neighboring storefront row extending north along Main;
- the Mobil service-station corner and intersection/roadway geometry;
- the West Linn Inn in the background, consistent with the CCHS description.

The photograph is especially valuable because it places **The Wheel and 505 Tavern in the same frame** and clearly preserves their status as separate neighboring businesses at 503 and 505.

## Evidence classification and limits

- **DOCUMENTED / DIRECT (institutional catalog):** CCHS object `{TARGET}`, title, description, and **1955–1965** Date made range.
- **DOCUMENTED / DIRECT (photographic + steward identification):** The Wheel signage at 503 and 505 Tavern signage at 505 are visible in the target frontage when the image is enlarged.
- **DOCUMENTED / DIRECT (spatial):** the photograph depicts the 5th/Main target frontage from the bluff-at-4th viewpoint described by CCHS.
- **UNRESOLVED:** exact exposure year within 1955–1965; proprietor/operator identities at the instant of exposure; any business-transfer date inferred solely from this photograph.

This photograph does **not** prove that The Wheel or 505 Tavern operated continuously throughout the entire 1955–1965 catalog range. It establishes only that both signs/business identities are present in the photographed state at some unresolved date within that range.

## Chronological significance

For **503 Main**, the image independently complements the 30 November 1960 **Wheel Cafe** newspaper anchor (`E-044`) and the later exact 7 June 1967 municipal 503 Main record (`E-025`).

For **505 Main**, the image complements the exact November 1965 municipal **505 Tavern** renewal (`E-029`). Because the image's date range begins in 1955 but extends through 1965, it must **not** be used to backdate the 505 Tavern trade name to 1955 without a narrower exposure date or an independent earlier documentary source.

It also complements CCHS `P-4565` (`IMG-0749`), another mid-1960s view that shows the adjacent 503/505 businesses from street level.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — CCHS {TARGET}, bluff at 4th Street looking northwest
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **1955–1965** per catalog Date made field; exact exposure year unresolved.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related buildings/businesses: `B-001` / `BUS-004`; `B-002` / `BUS-005`.
Notes: Enlarged visual review supports the project-steward identification of The Wheel signage on 503 and 505 Tavern signage on adjacent 505. The broad catalog range cannot be collapsed to 1955.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence with institutional catalog metadata
Claims:
- CCHS `{TARGET}` is titled **{CATALOG["title"]}** and has Date made **1955–1965**.
- Enlarged review supports the project-steward identification of **The Wheel** wording/signage on the 503 Main frontage.
- Enlarged review supports **505 Tavern / Tavern 505** signage on the adjacent 505 Main frontage.
- The single photograph therefore directly documents the two businesses as separate neighboring 503/505 occupancies in the photographed state.
- The exact exposure year is unresolved; the photograph cannot by itself backdate 505 Tavern to 1955 or prove uninterrupted operation throughout 1955–1965.
Classification: **DOCUMENTED / DIRECT** for the CCHS object/date range and visible business signage; exact exposure year unresolved.
Confidence: **Very High** for object identity, broad catalog date range and 503/505 sign identifications.
Related buildings: `B-001`, `B-002`.
Related businesses: `BUS-004`, `BUS-005`.''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS P-1311, bluff at 4th looking northwest, 1955–1965
- Type: Historic elevated streetscape / commercial-block photograph
- CCHS catalog: `{TARGET}`
- CCHS title: **{CATALOG["title"]}**
- CCHS Date made: **1955–1965**; exact exposure year unresolved
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Related buildings/businesses: `B-001` / `BUS-004` (503 / The Wheel); `B-002` / `BUS-005` (505 / 505 Tavern)
- Visual findings: enlarged review supports The Wheel wording/signage on 503 and 505 Tavern / Tavern 505 signage on adjacent 505 in the same frame.''')

append_once("media/photos/inventory.md", f"### {MID} —", f'''### {MID} — 1955–1965 bluff-at-4th view of 503/505
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- CCHS: `{TARGET}`
- Key value: same-frame elevated view of The Wheel at 503 and 505 Tavern signage at 505; exact exposure year within 1955–1965 unresolved.''')

append_once("timeline.md", f"## {TID} —", f'''## {TID} — 1955–1965 — CCHS P-1311 bluff view shows The Wheel and 505 Tavern

{TIMELINE_SUMMARY}

Related source/evidence/media: `{SID}` / `{EID}` / `{MID}`. Related businesses/buildings: `BUS-004` / `B-001`; `BUS-005` / `B-002`.
''')

append_once("database/evidence.yml", f"  - id: {EID}\n", f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: "Primary photographic evidence with institutional catalog metadata"
    claims:
      - "CCHS P-1311 is cataloged with a 1955-1965 Date made range; exact exposure year is unresolved."
      - "Enlarged review supports The Wheel wording/signage on the 503 Main frontage."
      - "Enlarged review supports 505 Tavern / Tavern 505 signage on the adjacent 505 Main frontage."
      - "The photograph documents the two businesses as separate neighboring occupancies in the photographed state, but does not prove continuous operation throughout 1955-1965."
    confidence: "Very High for object identity, catalog date range and sign identifications; exact exposure year unresolved."
    related_sources:
      - {SID}
    related_buildings:
      - B-001
      - B-002
    related_businesses:
      - BUS-004
      - BUS-005
''')

append_once("database/timeline.yml", f"  - id: {TID}\n", f'''  - id: {TID}
    date: "1955-1965"
    summary: "{TIMELINE_SUMMARY}"
    confidence: "Very High for P-1311 identity, broad date range and sign identifications; exact exposure year unresolved."
    related_sources:
      - {SID}
    related_evidence:
      - {EID}
    related_businesses:
      - BUS-004
      - BUS-005
    related_buildings:
      - B-001
      - B-002
''')

append_once("buildings/503-main.md", "## 1955–1965 CCHS P-1311 bluff view", f'''## 1955–1965 CCHS P-1311 bluff view

CCHS `P-1311` (`{SID}` / `{EID}` / `{MID}`) is an elevated bluff-at-4th photograph with a catalog Date made range of **1955–1965**. Enlarged review supports **The Wheel** wording/signage on the 503 frontage, while the adjacent 505 frontage carries **505 Tavern / Tavern 505** signage. The image is direct same-frame evidence that the two businesses occupied separate neighboring storefronts in the photographed state. The exact exposure year remains unresolved and is not assigned as 1955 merely because the title begins “Oregon City 1955.”
''')

append_once("buildings/505-main.md", "## 1955–1965 CCHS P-1311 bluff view", f'''## 1955–1965 CCHS P-1311 bluff view

CCHS `P-1311` (`{SID}` / `{EID}` / `{MID}`) is an elevated bluff-at-4th photograph with a catalog Date made range of **1955–1965**. Enlarged review supports **505 Tavern / Tavern 505** signage on the 505 frontage and **The Wheel** signage on adjacent 503. This directly documents the separate neighboring business identities in the photographed state. Because the exposure year is unresolved within 1955–1965, the photograph does **not** by itself move the documented start of the 505 Tavern trade name back to 1955.
''')

append_once("businesses/the-wheel.md", "## 1955–1965 P-1311 bluff photograph", f'''## 1955–1965 P-1311 bluff photograph

CCHS `P-1311` (`{SID}` / `{EID}` / `{MID}`), cataloged **1955–1965**, provides an elevated same-frame view of 503 and 505 Main. Enlarged review supports **The Wheel** wording/signage on the 503 frontage and **505 Tavern / Tavern 505** on the adjacent 505 frontage. This strengthens the physical separation of the two businesses but does not supply an exact exposure year.
''')

append_once("businesses/the-505.md", "## 1955–1965 P-1311 bluff photograph", f'''## 1955–1965 P-1311 bluff photograph

CCHS `P-1311` (`{SID}` / `{EID}` / `{MID}`), cataloged **1955–1965**, provides an elevated same-frame view of 503 and 505 Main. Enlarged review supports **505 Tavern / Tavern 505** signage on 505 and **The Wheel** on adjacent 503. This is direct photographic evidence for the trade-name signage in the photographed state, but the broad date range prevents using the image alone to backdate 505 Tavern to 1955.
''')

append_once("timelines/503-main.md", f"`{EID}` / `{SID}` / `{MID}` P-1311", f'''| 1955–1965, exact year unresolved | CCHS `P-1311` bluff-at-4th photograph shows **The Wheel** signage on the 503 frontage and **505 Tavern / Tavern 505** on adjacent 505. | **Direct photographic** same-frame business separation; catalog range only, not a 1955 opening/date claim. | `{EID}`; `{SID}`; `{MID}` |''')

append_once("timelines/505-main.md", f"`{EID}` / `{SID}` / `{MID}` P-1311", f'''| 1955–1965, exact year unresolved | CCHS `P-1311` bluff-at-4th photograph shows **505 Tavern / Tavern 505** signage at 505 and **The Wheel** on adjacent 503. | **Direct photographic** same-frame business separation; broad date range cannot backdate the 505 Tavern name to 1955. | `{EID}`; `{SID}`; `{MID}` |''')

append_once("indexes/id-crosswalk.md", f"`{MID}` CCHS `{TARGET}`", f'''| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`, `BUS-004`, `B-001`, `BUS-005`, `B-002` | 1955–1965 bluff-at-4th view; enlarged review supports The Wheel on 503 and 505 Tavern signage on adjacent 505; exact exposure year unresolved. |''')

append_once("registers/research-log.md", "### 2026-09-05 — CCHS P-1311 bluff-at-4th photograph", f'''### 2026-09-05 — CCHS P-1311 bluff-at-4th photograph
- Integrated project-steward supplied photograph as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Preserved supplied CCHS metadata: title **{CATALOG["title"]}**, object `{TARGET}`, description naming the West Linn Inn, and Date made **1955–1965**.
- Enlarged visual review supports project-steward readings of **The Wheel** on the 503 frontage and **505 Tavern / Tavern 505** signage at adjacent 505.
- Preserved the date limit: the title's “1955” is not promoted to an exact exposure date and the image alone does not backdate 505 Tavern to 1955.
''')

for entity in ("B-001", "B-002"):
    yaml_add_list_item("database/buildings.yml", entity, "related_evidence", EID)
for entity in ("BUS-004", "BUS-005"):
    yaml_add_list_item("database/businesses.yml", entity, "related_evidence", EID)

print(f"Integrated {TARGET}: {SID} / {EID} / {MID} / {TID}")
print(f"Repository image: {IMAGE} ({w}x{h}, {nbytes} bytes, sha256 {sha})")
