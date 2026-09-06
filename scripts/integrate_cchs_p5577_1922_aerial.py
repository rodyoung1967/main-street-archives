from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-5577"
ACCOUNT = "4813"
REVIEW = "2026-09-05"
SOURCE_NAME = "CCHS P-5577, Oregon City aerial view of Willamette Falls and Oregon City, 1922"
EVIDENCE_NAME = "1922 P-5577 aerial preserves downtown and Fifth/Main spatial context without a month-specific fire/rebuild state"

CATALOG = {
    "title": "Oregon City 1922 - Aerial View of Willamette Falls and Oregon City",
    "entry_object_id": TARGET,
    "description": "Aerial View #1 of Willamette Falls, West Linn and Oregon City.  Companion Photos P-4776, P-5577, P-5578, P-5579, P-5580. 2014.002.027.001",
    "date_made": "1922",
    "medium": "Photographic Paper",
    "location_of_negative": "CCHS Halon Room",
    "other_number": "Gardner Photos 027_001",
}

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET, "size": 200})


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
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
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
TID = next_id("timeline.md", "T", 3)

search = get_json(SEARCH_URL)
match = find_match(search)
if match is None:
    raise SystemExit(f"Exact CCHS catalog number {TARGET} in account {ACCOUNT} not returned")
entry_id = match.get("id")
if not entry_id:
    raise SystemExit("Matching CCHS result has no id")
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

IMAGE = f"media/photos/aerials/{MID}_1922-willamette-falls-oregon-city-aerial-cchs-p5577.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)
CAP = "evidence/source-captures/cchs-p5577-1922-willamette-falls-oregon-city-aerial-2026-09-05.md"
API = "evidence/source-captures/cchs-p5577-1922-willamette-falls-oregon-city-aerial-api-2026-09-05.json"

wr(API, json.dumps({
    "reviewed": REVIEW,
    "catalog": TARGET,
    "search_url": SEARCH_URL,
    "entry_url": ENTRY,
    "hub_url": HUB,
    "selected_derivative": der,
    "repository_file": IMAGE,
    "repository_image": {"width": w, "height": h, "bytes": nbytes, "sha256": sha},
    "catalog_metadata_supplied_by_steward": CATALOG,
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS {TARGET} — 1922 aerial view of Willamette Falls, West Linn and Oregon City

Reviewed **5 September 2026** from the project-steward supplied image and exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made: **1922**
- Medium: **Photographic Paper**
- Location of Negative: **CCHS Halon Room**
- Other No.: **Gardner Photos 027_001**
- Public record: {HUB}
- Public API: {ENTRY}

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact `{TARGET}` object
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`

## Direct visual review

The photograph is a broad elevated/aerial view centered on **Willamette Falls**, with **West Linn** on the west side of the river and **Oregon City** on the east side. The lower Oregon City street grid, commercial district, riverfront/rail corridor, industrial works and bridge area are all visible in one frame.

The **Fifth/Main target district lies within the downtown portion of the image**, making this useful for block-scale geometry and footprint comparison. At the available scale, however, individual `501`, `503` and `505` street numbers and business signs are not readable. No business occupancy is assigned from this image alone.

## Why the 1922 date matters — and its limit

The institutional record supplies **1922**, but no month or day. That means P-5577 cannot by itself be classified as a pre-fire or post-fire photograph relative to the **18 July 1922 Fifth/Main fire**, and it cannot by itself prove whether the Gates replacement described in August was already standing.

This limitation is especially important because CCHS `P-9594` (`S-239` / `E-213` / `IMG-0760`) is specifically described as **November 1922** and therefore remains the stronger dated photographic control for the post-fire Gates-rebuild question.

P-5577 should instead be used as **same-year aerial spatial evidence** and tested against:

- the 1911 and 1925 Sanborn geometry;
- `P-9594`'s November 1922 Fifth/Main bridge/downtown view;
- the August 1922 Gates construction reports (`E-097`);
- later aerials and securely mapped street-level photographs.

## Companion-series importance

The CCHS description explicitly names companion photographs **P-4776, P-5578, P-5579 and P-5580**. Those should be retrieved and reviewed as a set. Adjacent exposures may show the Fifth/Main block at a better angle or scale and may allow a relative flight sequence to be reconstructed.

The `2014.002.027.001` designation and **Gardner Photos 027_001** number also suggest this image belongs to a numbered Gardner photographic sequence. Preserve those identifiers when locating the companions.

## Evidence state

- **DOCUMENTED / DIRECT:** CCHS object identity, title, 1922 Date made, description, companion-photo numbers and Gardner identifier.
- **VISUALLY VERIFIED:** broad aerial coverage of Willamette Falls, West Linn, Oregon City and the downtown grid.
- **DOCUMENTED SPATIAL CONTEXT:** the Fifth/Main district is within the photographed downtown area.
- **UNRESOLVED:** precise exposure date within 1922; pre- versus post-18-July-fire state; exact 501/503/505 footprint transcription from this image; any business occupancy.

No visual absence is treated as proof of vacancy, demolition or non-use.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic aerial photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`; Gardner Photos `027_001`; accession/series wording `2014.002.027.001`.  
Date: **1922**; no month supplied.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.  
Notes: Broad aerial of Willamette Falls, West Linn and Oregon City. Fifth/Main lies within the downtown frame, but individual target numbers/business signs are unreadable at this scale. Because no month is supplied, do not classify the view as pre- or post-July-1922 fire from this source alone. Companion photos: P-4776, P-5578, P-5579, P-5580.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Type: Primary historic aerial photograph / spatial-context evidence  
Claims:
- CCHS `{TARGET}` catalogs an **Aerial View #1 of Willamette Falls, West Linn and Oregon City**, Date made **1922**.
- Direct visual review confirms broad coverage of the Oregon City downtown grid and the Fifth/Main district.
- Individual 501/503/505 numbers and business signs are not readable at the available scale, so the image is not used for direct occupancy assignments.
- Because the catalog provides **no month**, the image cannot by itself be placed before or after the 18 July 1922 Fifth/Main fire or used to prove the Gates replacement was standing.
- CCHS names companion photographs **P-4776, P-5578, P-5579 and P-5580**; reviewing that sequence may improve target-block geometry and dating.
Classification: **DOCUMENTED / DIRECT** for object/date/year and broad scene; **DOCUMENTED SPATIAL CONTEXT** for the target district being in frame; **UNRESOLVED** for fire/rebuild state and exact target footprints.  
Confidence: **Very High** for catalog identity/year and broad visual geography; unresolved for precise within-year chronology and target-building detail.''')

append_once("media/photo-metadata-register.md", f"### {MID} — CCHS {TARGET} 1922 aerial view of Willamette Falls and Oregon City", f'''### {MID} — CCHS {TARGET} 1922 aerial view of Willamette Falls and Oregon City
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS object: **{TARGET}**
- CCHS title: **{CATALOG["title"]}**
- Date made: **1922**
- Description: **{CATALOG["description"]}**
- Medium: **Photographic Paper**; negative location **CCHS Halon Room**
- Other number: **Gardner Photos 027_001**
- Repository file: `{IMAGE}`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Status: `committed`
- Visual review: broad Willamette Falls / West Linn / Oregon City aerial. Fifth/Main is within the downtown frame, but exact 501/503/505 lettering and business signs are not readable. No month is supplied, so pre-/post-July-1922-fire state remains unresolved.
- Companion-photo lead: `P-4776`, `P-5578`, `P-5579`, `P-5580`.
''')

append_once("timeline.md", f"## 1922 — {TID}: P-5577 aerial documents same-year downtown geometry", f'''## 1922 — {TID}: P-5577 aerial documents same-year downtown geometry

CCHS `P-5577` (`{SID}` / `{EID}` / `{MID}`) is a **1922** aerial of Willamette Falls, West Linn and Oregon City. The downtown grid and Fifth/Main district are in frame, providing same-year spatial context for the target block. The catalog gives **no month**, so this photograph is **not** used to decide whether the exposure predates or postdates the 18 July Fifth/Main fire or whether the Gates replacement was already complete. Exact 501/503/505 signs are unreadable at this scale. Companion exposures `P-4776`, `P-5578`, `P-5579`, and `P-5580` remain a high-value sequence to retrieve.
''')

# Timeline YAML synchronized entry.
timeline_yml = Path("database/timeline.yml")
ty = timeline_yml.read_text(encoding="utf-8")
if TID not in ty:
    ty = ty.rstrip() + f'''\n\n  - id: {TID}\n    date: "1922"\n    title: "1922 — P-5577 aerial documents same-year downtown geometry"\n    summary: "CCHS P-5577 is a 1922 aerial of Willamette Falls, West Linn and Oregon City. Fifth/Main is within the downtown frame, but exact 501/503/505 signs are unreadable and no month is supplied, so pre/post-July-fire state remains unresolved."\n    confidence: "Very High for catalog year and broad geography; unresolved for within-year chronology and target-building detail."\n    related_sources: [{SID}]\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n''' + "\n"
    timeline_yml.write_text(ty, encoding="utf-8")

# Source/evidence YAML synchronized entries.
sources_yml = Path("database/sources.yml")
sy = sources_yml.read_text(encoding="utf-8")
if SID not in sy:
    sy = sy.rstrip() + f'''\n\n  - id: {SID}\n    name: "{SOURCE_NAME}"\n    url: "{HUB}"\n    type: "Primary historic aerial photograph with CCHS institutional catalog metadata"\n    date: "1922"\n    repository_file: "{IMAGE}"\n    notes: "Broad Willamette Falls/West Linn/Oregon City aerial; Fifth/Main lies in frame. No month, readable target numbers, or direct business occupancy. Companion photos P-4776/P-5578/P-5579/P-5580."\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n''' + "\n"
    sources_yml.write_text(sy, encoding="utf-8")

evidence_yml = Path("database/evidence.yml")
ey = evidence_yml.read_text(encoding="utf-8")
if EID not in ey:
    ey = ey.rstrip() + f'''\n\n  - id: {EID}\n    name: "{EVIDENCE_NAME}"\n    type: "Primary historic aerial photograph / spatial-context evidence"\n    date: "1922"\n    claims:\n      - "CCHS P-5577 catalogs Aerial View #1 of Willamette Falls, West Linn and Oregon City, Date made 1922."\n      - "The downtown grid and Fifth/Main district are visually in frame."\n      - "Individual 501/503/505 numbers and business signs are not readable at the available scale."\n      - "No month is supplied, so the image cannot by itself be placed before or after the 18 July 1922 Fifth/Main fire or used to prove the Gates replacement was standing."\n      - "Companion photos P-4776, P-5578, P-5579 and P-5580 should be reviewed as a sequence."\n    confidence: "Very High for catalog identity/year and broad geography; unresolved for precise within-year chronology and target-building detail."\n    related_sources: [{SID}]\n    related_media: [{MID}]\n    repository_file: "{CAP}"\n''' + "\n"
    evidence_yml.write_text(ey, encoding="utf-8")

append_once("indexes/id-crosswalk.md", f"`{MID}` CCHS `{TARGET}`", f'''| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`; `B-001`, `B-002`, `B-005` context | 1922 aerial of Willamette Falls/West Linn/Oregon City. Fifth/Main target district is in frame, but exact 501/503/505 detail and pre/post-July-fire state are unresolved because the catalog gives no month. Companion sequence: P-4776/P-5578/P-5579/P-5580. |''')

append_once("evidence/research-leads.md", "P-5577 companion aerial sequence", f'''### P-5577 companion aerial sequence

CCHS `P-5577` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) explicitly names companion photographs **P-4776, P-5578, P-5579 and P-5580**. Retrieve all four and compare their camera positions, overlap and target-block visibility. The goal is to determine whether any exposure gives a stronger footprint view of 501/503/505 or can be relatively sequenced against the July 1922 fire and November `P-9594` control. Do not infer pre/post-fire status from P-5577's year-only date.''')

append_once("registers/research-log.md", "CCHS P-5577 1922 aerial", f'''### 2026-09-05 — CCHS P-5577 1922 aerial
- Integrated project-steward supplied CCHS `{TARGET}` as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Preserved title, description, Date made **1922**, medium, negative location, Gardner Photos `027_001`, and companion list `P-4776`, `P-5578`, `P-5579`, `P-5580`.
- Direct visual review confirms broad Willamette Falls / West Linn / Oregon City coverage with the Fifth/Main district inside the downtown frame.
- Exact 501/503/505 lettering/business signage is unreadable at this scale.
- Because no month is supplied, P-5577 is **not** classified as pre- or post-18-July-1922-fire evidence. `P-9594` remains the stronger November 1922 post-fire visual control.
- No annual research-status certification changed.''')

# Add source/evidence/media references to target building headers and YAML only as spatial context.
for rel in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    text = rd(rel)
    marker = f"### 1922 P-5577 aerial spatial context"
    if marker not in text:
        text = text.rstrip() + f'''\n\n### 1922 P-5577 aerial spatial context\n\nCCHS `P-5577` (`{SID}` / `{EID}` / `{MID}`) places the Fifth/Main district within a broad **1922** aerial of Oregon City. The image is useful for block-scale geometry and companion-flight comparison, but exact target numbers are unreadable and the catalog supplies no month. Do **not** use it alone to classify this address as pre- or post-July-fire or to prove a specific Gates-rebuild footprint.\n'''
        wr(rel, text)

print(f"Integrated {TARGET} as {SID} / {EID} / {MID} / {TID}")
