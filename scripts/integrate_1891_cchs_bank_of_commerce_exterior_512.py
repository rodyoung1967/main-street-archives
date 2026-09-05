from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET = "2008.008.049.057"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City Bank of Commerce 1891 - Oregon City.jpg",
    "width": 2048,
    "height": 1472,
    "bytes": 776187,
    "sha256": "070287adf65b6f19187c4a2fbb1b65610b641ea57ce03af2e0e32965e352c359",
}

CATALOG = {
    "title": "Oregon City Bank of Commerce 1891 - Oregon City",
    "entry_object_id": TARGET,
    "tags": ["vol 2", "Presentation"],
    "description": (
        "Exterior of the Commercial Bank, Oregon City Bank of Commerce (1st National) was 512 Main Street. "
        "The bank has since been demolished and the structure to the right renumbered. Remnants of the stone "
        "remain at the northwest corner. JAH 11/2022  The house rooming house behind the bank, once sat where "
        "the bank was located. One of Maj. Thomas Charmans earlier homes, it was pulled back off Main Street "
        "for the bank (JAH 03/2023)"
    ),
    "date_made": "1891",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_number": "Lynch-Criteser 057",
    "other_photo_number": "Latourette Family #1",
}

SOURCE_NAME = "CCHS 2008.008.049.057, Oregon City Bank of Commerce exterior, 1891"
EVIDENCE_NAME = "CCHS 1891 exterior documents Commercial Bank facade cataloged at 512 Main"

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
            if "thumbnail" in key.lower() or key in {"complementary_color", "dominant_color"}:
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                found.append((w*h, w, h, key, val["path"]))
    if not found:
        raise SystemExit("No public image derivative found for exact CCHS object")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}


# Idempotency by exact catalog object.
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

IMAGE = f"media/photos/early-main-street/{MID}_1891-oregon-city-bank-of-commerce-exterior-512-main-cchs-2008-008-049-057.jpg"
path = Path(IMAGE)
if path.exists():
    raise SystemExit(f"Target image already exists without registered object: {IMAGE}")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(data)

CAP = "evidence/source-captures/1891-cchs-2008-008-049-057-bank-of-commerce-exterior-512-main-2026-09-05.md"
API = "evidence/source-captures/1891-cchs-2008-008-049-057-bank-of-commerce-exterior-512-main-api-2026-09-05.json"
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

capture = f'''# CCHS {TARGET} — Oregon City Bank of Commerce exterior, 1891

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public CatalogIt object `{TARGET}`.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. 512 MAIN, DEMOLITION/RENUMBERING, STONE-REMNANT, AND MOVED-ROOMING-HOUSE STATEMENTS ARE CATALOG ANNOTATIONS; THE COMMERCIAL BANK FACADE WORDING IS IMAGE-VISIBLE.**

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`. Related earlier CCHS interior record: `S-212` / `E-192` / `IMG-0741`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Tags: **vol 2; Presentation**
- Description: **{CATALOG["description"]}**
- Date made: **1891**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of Negative: **Society Collection**
- Other No.: **Lynch-Criteser 057**
- Other Photo #: **Latourette Family #1**
- Public record: {HUB}
- Public API: {ENTRY}

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact catalog object `{TARGET}`
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`

## Direct visual review

The photograph directly shows a substantial stone-front commercial building. **COMMERCIAL BANK** is visibly carved/lettered high on the front facade. The bank has a large arched front window, an arched entrance bay, heavy rusticated stone piers, and a long side wall extending back toward the bluff.

The immediately adjacent storefront to the right carries a clearly visible **SHARPLES** sign. Enlarged review also supports reading the window lettering as **WILSON & COOKE / HARDWARE**; because the neighboring storefront is only partly shown and the catalog says the structure to the right was later renumbered, this image does not assign a modern street number to that hardware storefront.

At left/rear, a separate **ROOMS / & BOARD** sign is visible. Houses/buildings appear higher on the bluff behind the bank.

No **512** street number is visible on the bank facade in this photograph.

## Catalog interpretation preserved as annotation

The CCHS description states that the Oregon City Bank of Commerce / First National was at **512 Main Street**, that the bank was later demolished, that the structure to the right was renumbered, and that remnants of the stone remain at the northwest corner. Those statements are preserved as **institutional catalog annotation (JAH 11/2022)** rather than treated as facts independently proved by the 1891 image.

The same description states that a rooming house behind the bank once occupied the bank site, was one of Maj. Thomas Charman's earlier homes, and was pulled back from Main Street for construction of the bank. That is preserved as **institutional catalog annotation (JAH 03/2023)**. The 1891 image alone does not establish the move date, ownership chain, or exact earlier footprint.

## Relationship to the 1890 interior photograph

CCHS object `2008.008.049.056` (`S-212` / `E-192` / `IMG-0741`) is cataloged as a **1890 interior of the Oregon City Bank of Commerce at 512 Main**. This 1891 exterior is a closely related institutional record and, unlike the interior, directly displays **COMMERCIAL BANK** on the building facade.

Together the two CCHS objects strengthen the institutional identification of the bank context, but the archive does not use the pair to infer uninterrupted corporate succession, exact legal ownership, or survival of the 1891 building into later periods without independent records.

## Relevance to the 503/505 project

This is an **even-side Main Street spatial/address control**, not direct evidence of 503 or 505 occupancy. Its value is in reconstructing the opposite-side Main Street streetscape, the historical 512 Main bank location, later renumbering, and neighboring-building geometry. Do not use the catalog's later-address statements to backdate modern parcel boundaries.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **1891** per catalog.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media: `{EID}` / `{MID}`.
Related earlier bank interior: `S-212` / `E-192` / `IMG-0741`.
Notes: **COMMERCIAL BANK** is directly visible on the facade. Catalog metadata places the bank at 512 Main and supplies later demolition/renumbering, stone-remnant, and moved-rooming-house annotations; those later historical statements are retained as institutional annotation rather than treated as image-visible facts.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence with institutional catalog metadata
Claims:
- CCHS object `{TARGET}` is dated **1891** and titled **{CATALOG["title"]}**.
- **COMMERCIAL BANK** is directly visible on the stone facade.
- CCHS catalogs the Oregon City Bank of Commerce / First National at **512 Main Street**.
- CCHS later annotation says the bank was demolished, the structure to the right was renumbered, stone remnants remain at the northwest corner, and a former Thomas Charman house/rooming house was moved back from Main Street for the bank.
- The right-hand neighboring storefront visibly carries **SHARPLES** signage; enlarged review supports **WILSON & COOKE / HARDWARE** window lettering, but no modern number is assigned from this image.
- The photograph is a contextual even-side Main Street control and does not establish 503/505 occupancy or building continuity.
Classification: **DOCUMENTED / DIRECT** for the CCHS object/date and image-visible facade/signage; **institutional catalog annotation** for 512 Main, demolition/renumbering, stone-remnant, and moved-rooming-house history.
Confidence: **Very High** for object identity, catalog date, and visible COMMERCIAL BANK wording; **High as attributed catalog metadata** for the later JAH annotations, pending independent primary-record corroboration.''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS {TARGET}, Oregon City Bank of Commerce exterior, 1891
- Type: Historic commercial-building exterior photograph
- CCHS catalog: `{TARGET}`
- CCHS title: **{CATALOG["title"]}**
- CCHS date: **1891**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Source/evidence: `{SID}` / `{EID}`
- Other identifiers: **Lynch-Criteser 057**; **Latourette Family #1**
- Direct visual text: **COMMERCIAL BANK**; neighboring **SHARPLES**; enlarged neighboring window supports **WILSON & COOKE / HARDWARE**; left/rear **ROOMS & BOARD**.
- Limits: no 512 number is image-visible. The 512 Main location and later demolition/renumbering, stone-remnant, and moved-rooming-house statements are CCHS/JAH catalog annotations. Do not infer a modern neighboring address from the partial right-hand storefront.
- Related image: `IMG-0741` / `S-212` / `E-192`, CCHS 1890 Bank of Commerce interior.''')

append_once("media/photos/inventory.md", f"### {MID} —", f'''### {MID} — CCHS {TARGET} Bank of Commerce exterior, 1891
- File: `{IMAGE}`
- Direct visual: **COMMERCIAL BANK** facade; partial neighboring hardware storefront; bluff-side context.
- Institutional metadata: Oregon City Bank of Commerce / First National, **512 Main**, 1891; Lynch-Criteser 057 / Latourette Family #1.
- Source/evidence: `{SID}` / `{EID}`.
- Limit: 512 Main and later demolition/renumbering / moved-house history are catalog annotations; no 512 number is visible.''')

append_once("media/photos/early-main-street/README.md", f"## {MID} —", f'''## {MID} — CCHS {TARGET} Bank of Commerce exterior, 1891

`{Path(IMAGE).name}` preserves the largest public CCHS derivative recovered from the exact catalog object. **COMMERCIAL BANK** is directly visible on the stone facade. CCHS catalogs the bank as Oregon City Bank of Commerce / First National at **512 Main** and provides later JAH annotations concerning demolition, renumbering of the neighboring structure, surviving stone remnants, and a Thomas Charman house/rooming house moved back for the bank. Those later statements remain attributed catalog metadata. See `{SID}` / `{EID}` and `{CAP}`. Related interior photograph: `IMG-0741` (`S-212` / `E-192`).''')

append_once("indexes/id-crosswalk.md", f"## {SID} / {EID} / {MID} —", f'''## {SID} / {EID} / {MID} — CCHS {TARGET} Bank of Commerce exterior

| Record | Links | Notes |
| --- | --- | --- |
| `{SID}` / `{EID}` / `{MID}` | `S-212` / `E-192` / `IMG-0741` related interior | 1891 exterior: **COMMERCIAL BANK** directly visible; CCHS catalogs 512 Main. Later demolition/renumbering, stone-remnant, and moved-rooming-house history retained as attributed catalog annotation. |''')

append_once("registers/research-log.md", f"### 2026-09-05 — CCHS {TARGET}", f'''### 2026-09-05 — CCHS {TARGET} Bank of Commerce exterior integrated
- Checked current `main`; exact object `{TARGET}` was not already registered.
- Preserved the largest public derivative from the exact CCHS record as `{MID}` and tracked the steward upload separately by filename, dimensions, bytes, and SHA-256.
- Added `{SID}` / `{EID}` and synchronized source/evidence/media/crosswalk/inventory records.
- Direct visual review reads **COMMERCIAL BANK** on the facade; the partial neighboring storefront carries **SHARPLES** signage and enlarged review supports **WILSON & COOKE / HARDWARE** window lettering.
- Preserved CCHS/JAH later annotations for 512 Main, demolition/renumbering, northwest-corner stone remnants, and the moved Thomas Charman house/rooming house without upgrading them to image-visible or independently verified facts.
- Linked the closely related 1890 interior record `S-212` / `E-192` / `IMG-0741`.
- No 503/505 occupancy, title, or building-continuity claim was inferred from this even-side Main Street control photograph.''')

# Keep Markdown/YAML mirrors synchronized.
append_once("database/sources.yml", f"  - id: {SID}\n", f'''  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{HUB}"
    repository_file: "{IMAGE}"
    notes: "Primary CCHS photograph dated 1891. COMMERCIAL BANK is directly visible; CCHS catalogs the bank at 512 Main and supplies later JAH demolition/renumbering, stone-remnant, and moved-rooming-house annotations. Related interior: S-212/E-192/IMG-0741."''')

append_once("database/evidence.yml", f"  - id: {EID}\n", f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: "Primary photographic evidence with institutional catalog metadata"
    claims:
      - "CCHS object {TARGET} is dated 1891."
      - "COMMERCIAL BANK is directly visible on the stone facade."
      - "CCHS catalogs the Oregon City Bank of Commerce / First National at 512 Main Street."
      - "Later CCHS/JAH annotation reports demolition, neighboring-structure renumbering, surviving northwest-corner stone remnants, and a former Thomas Charman house/rooming house moved back for the bank."
      - "The image is an even-side Main Street context control and does not establish 503/505 occupancy or building continuity."
    confidence: "Very High for object identity/date and visible COMMERCIAL BANK wording; High as attributed institutional annotation for later historical statements, pending independent primary-record corroboration."
    related_sources:
      - {SID}''')

print(f"Integrated {TARGET}: {SID} / {EID} / {MID}")
print(f"Repository image: {IMAGE} ({w}x{h}, {nbytes} bytes, sha256 {sha})")
