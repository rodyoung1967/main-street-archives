from pathlib import Path
import hashlib
import json
import re
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1241"
ACCOUNT = "4813"
ENTRY_ID = "00455f90-9b1f-11eb-b3ef-53e7205a00b4"
SLUG = "oregon-city-1900-ca-viewed-from-the-bluff-main-between-5th-and-7th-streets"
REVIEW = "2026-09-05"
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}"
HUB = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{SLUG}"

STEWARD = {
    "filename": "Oregon City 1900 ca - Viewed from the Bluff - Main between 5th and 7th Street.jpg",
    "width": 2048,
    "height": 1914,
    "bytes": 1045002,
    "sha256": "af12fed120f6c9e3a3c92de1302868df2cbe02d916ad7d68b640a8fa80b20d9e",
}
STEWARD_NOTE = (
    "Project steward identifies the far-left Main Street frontage in this view as the "
    "historic area later numbered 501-505 Main."
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


def labeled_value(obj, wanted):
    """Recursively recover a CatalogIt field by its displayed label."""
    if isinstance(obj, dict):
        if str(obj.get("label", "")).strip().lower() == wanted.lower():
            for key in ("value_text", "value_date", "value_datetime", "value_number", "value_boolean"):
                val = obj.get(key)
                if val not in (None, ""):
                    return str(val)
            ref = obj.get("value_reference")
            if isinstance(ref, dict) and ref.get("reference_value"):
                return str(ref["reference_value"])
        for v in obj.values():
            got = labeled_value(v, wanted)
            if got:
                return got
    elif isinstance(obj, list):
        for v in obj:
            got = labeled_value(v, wanted)
            if got:
                return got
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
                found.append((w * h, w, h, key, val["path"]))
    if not found:
        raise SystemExit(f"No public image derivative found for {TARGET}")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}


def yaml_add_list_item(path, entity_id, field, item):
    text = rd(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Could not find {entity_id} in {path}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    fm = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if not fm:
        raise SystemExit(f"Could not find field {field} under {entity_id} in {path}")
    field_start = m.start() + fm.end()
    after = text[field_start:end]
    nf = re.search(r"(?m)^    [A-Za-z0-9_]+:", after)
    insert_at = field_start + (nf.start() if nf else len(after))
    text = text[:insert_at].rstrip("\n") + f"\n      - {item}\n" + text[insert_at:].lstrip("\n")
    wr(path, text)


# Exact-object idempotency only; companion references to P-1241 must not block integration.
if (
    f"Catalog ID: `{TARGET}`" in rd("evidence/source-register.md")
    or f"CCHS object: **{TARGET}**" in rd("media/photo-metadata-register.md")
):
    print(f"{TARGET} already integrated as its own archival object; no changes needed.")
    raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
MID = next_id("media/photo-metadata-register.md", "IMG", 4)
TID = next_id("database/timeline.yml", "T", 3)

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

TITLE = prop(entry, "hasName") or "Oregon City 1900 ca - Viewed from the Bluff - Main between 5th and 7th Streets"
DESCRIPTION = prop(entry, "hasDescription") or labeled_value(entry, "Description")
DATE_MADE = labeled_value(entry, "Date made") or "ca. 1900 (from institutional title; separate Date made field not recovered)"
MEDIUM = labeled_value(entry, "Medium")
NEGATIVE = labeled_value(entry, "Location of Negative")
OTHER = labeled_value(entry, "Other Number") or labeled_value(entry, "Other No.")

IMAGE = f"media/photos/early-main-street/{MID}_ca1900-bluff-main-5th-7th-cchs-p1241.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-p1241-ca1900-bluff-main-5th-7th-target-frontage-2026-09-05.md"
API = "evidence/source-captures/cchs-p1241-ca1900-bluff-main-5th-7th-api-2026-09-05.json"

wr(API, json.dumps({
    "reviewed": REVIEW,
    "institution": "Clackamas County Historical Society",
    "catalog": TARGET,
    "entry_url": ENTRY,
    "hub_url": HUB,
    "live_title": TITLE,
    "live_description": DESCRIPTION,
    "live_date_made": DATE_MADE,
    "live_medium": MEDIUM,
    "live_location_of_negative": NEGATIVE,
    "live_other_number": OTHER,
    "selected_derivative": der,
    "repository_file": IMAGE,
    "repository_image": {"width": width, "height": height, "bytes": nbytes, "sha256": sha},
    "steward_upload": STEWARD,
    "steward_target_annotation": STEWARD_NOTE,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

SOURCE_NAME = f"CCHS {TARGET} — circa-1900 bluff view, Main between Fifth and Seventh"
EVIDENCE_NAME = "Circa-1900 bluff view preserves the Main/Fifth-to-Seventh streetscape and probable 501-505 predecessor frontage"

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`. Related buildings: `B-005` (501), `B-001` (503), `B-002` (505).

## Institutional record

- Name/Title: **{TITLE}**
- Entry/Object ID: **{TARGET}**
- Description: **{DESCRIPTION or '[no description text recovered]'}**
- Date made: **{DATE_MADE}**
- Medium: **{MEDIUM or '[not recovered]'}**
- Location of Negative: **{NEGATIVE or '[not recovered]'}**
- Other Number: **{OTHER or '[not recovered]'}**
- Public record: {HUB}
- Public API: {ENTRY}

The institutional title itself explicitly locates the view on **Main between 5th and 7th Streets** and labels it **1900 ca**. If the separate Date made field differs, both values are retained in the raw API capture rather than silently normalized.

## Project-steward supplied image

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Steward annotation: **{STEWARD_NOTE}**

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact object `{TARGET}`
- Dimensions: **{width} × {height}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-file fingerprint is preserved even when the repository uses a larger institutional derivative of the same photograph.

## Direct visual review

The photograph is an elevated bluff view across lower Oregon City toward the Willamette River and the historic bridge. It records a dense lower-Main commercial roofscape, the river/bridge setting, bluff-side development and multiple building fronts and rear elevations between Fifth and Seventh Streets.

At the **far left edge**, a row of Main Street commercial frontage is visible. No later `501`, `503`, or `505` street number is readable in the photograph itself.

## 501-505 interpretation

The project steward identifies the far-left frontage as the historic area later numbered **501-505 Main**. That identification is especially plausible because the institutional title independently fixes the photographed Main Street span as **between Fifth and Seventh Streets**. The photograph therefore provides valuable early spatial evidence for the predecessor frontage near the Fifth/Main corner.

However, the image does not itself label individual address numbers, and circa-1900 address numbering/building continuity cannot be assumed to match the later 501/503/505 parcels or surviving buildings. Accordingly:

- **DOCUMENTED / DIRECT:** CCHS object identity and institutional title locating Main between Fifth and Seventh; visible early Main Street streetscape.
- **VISUALLY VERIFIED:** far-left commercial frontage is present in the photograph.
- **PROBABLE / WORKING HYPOTHESIS:** the far-left frontage corresponds to the historic area later numbered 501-505 Main.
- **UNRESOLVED:** exact individual 501/503/505 boundaries within the visible frontage; exposure date precision; continuity from these circa-1900 buildings to later numbered structures.

## Research value

This is a high-value pre-1911 structural comparison source. Align the far-left frontage against the **1892 and 1900 Sanborn sheets**, the 1895 fixed-location photographs, and later 1907-1916 Main Street images. Focus on roof heights, party walls, setbacks, Fifth Street width/alignment, and neighboring facade rhythm. Do not infer one-to-one building continuity from address position alone.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`.  
Date: **{DATE_MADE}**; institutional title says **1900 ca**.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.  
Related buildings: `B-005`, `B-001`, `B-002`.  
Notes: Institutional title locates Main between Fifth and Seventh. Steward identifies the far-left frontage as the later 501-505 area; exact numbered boundaries and building continuity remain unresolved.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Type: Primary historic photograph / early streetscape and building-geometry evidence  
Claims:
- CCHS `{TARGET}` is titled **{TITLE}**, explicitly locating the photographed Main Street span between **5th and 7th Streets**.
- Direct visual review confirms an early commercial frontage at the far-left side of the image.
- Project steward identifies that far-left frontage as the historic area later numbered **501-505 Main**.
- Because no later street number is readable and address/building continuity cannot be assumed across circa 1900, the exact 501/503/505 boundaries remain unresolved.
Classification: **DOCUMENTED / DIRECT** for object/title and broad streetscape; **VISUALLY VERIFIED** for the far-left frontage; **PROBABLE / WORKING HYPOTHESIS** for later 501-505 mapping; **UNRESOLVED** for individual boundaries and building continuity.  
Confidence: **Very High** for object identity/title geography; **Moderate-to-High** for the steward-mapped 501-505 area; unresolved for individual-address footprints.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS {TARGET} circa-1900 bluff view, Main between Fifth and Seventh", f'''## {MID} — CCHS {TARGET} circa-1900 bluff view, Main between Fifth and Seventh
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS object: **{TARGET}**
- CCHS title: **{TITLE}**
- Date made: **{DATE_MADE}**
- Repository file: `{IMAGE}`
- Repository dimensions: **{width} × {height}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD['filename']}`; {STEWARD['width']}×{STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Status: `committed`
- Visual note: early Main Street frontage is visible at far left. Steward maps it to the later 501-505 area; no address numbers are readable and individual building continuity remains unresolved.
''')

append_once("media/photos/inventory.md", f"### {MID} — CCHS {TARGET}", f'''### {MID} — CCHS {TARGET} circa-1900 Main-between-Fifth-and-Seventh bluff view
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`.
- Institutional title places the view on Main between Fifth and Seventh; steward identifies the far-left frontage as the later 501-505 area.
- Limit: exact numbered boundaries and continuity to later buildings are not proved by the photograph alone.
''')

append_once("timeline.md", f"## {DATE_MADE} — {TID}: P-1241 bluff view preserves early Fifth-to-Seventh Main frontage", f'''## {DATE_MADE} — {TID}: P-1241 bluff view preserves early Fifth-to-Seventh Main frontage

CCHS `P-1241` (`{SID}` / `{EID}` / `{MID}`) is titled **{TITLE}**. The institutional title fixes the photographed commercial span as Main between Fifth and Seventh. At far left, the project steward identifies the visible frontage with the area later numbered **501-505 Main**. The early frontage is visually present, but no later address number is readable; exact 501/503/505 boundaries and building continuity remain a **PROBABLE / WORKING HYPOTHESIS**, not direct proof.
''')

# Synchronized YAML records.
sy = rd("database/sources.yml")
if SID not in sy:
    sy = sy.rstrip() + f'''\n\n  - id: {SID}\n    name: "{SOURCE_NAME}"\n    url: "{HUB}"\n    type: "Primary historic photograph with CCHS institutional catalog metadata"\n    date: "{DATE_MADE}"\n    repository_file: "{IMAGE}"\n    notes: "Institutional title locates Main between Fifth and Seventh; steward maps far-left frontage to later 501-505 area. Exact numbered boundaries/building continuity unresolved."\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n''' + "\n"
    wr("database/sources.yml", sy)

ey = rd("database/evidence.yml")
if EID not in ey:
    ey = ey.rstrip() + f'''\n\n  - id: {EID}\n    name: "{EVIDENCE_NAME}"\n    type: "Primary historic photograph / early streetscape and building-geometry evidence"\n    date: "{DATE_MADE}"\n    claims:\n      - "CCHS P-1241 title locates Main between Fifth and Seventh Streets."\n      - "Far-left early commercial frontage is visually present."\n      - "Project steward identifies that frontage as the historic area later numbered 501-505 Main."\n      - "No later address numbers are readable; individual boundaries and building continuity remain unresolved."\n    confidence: "Very High for object/title geography; Moderate-to-High for later-area mapping; unresolved for individual address footprints."\n    related_sources: [{SID}]\n    related_media: [{MID}]\n    related_buildings: [B-005, B-001, B-002]\n    repository_file: "{CAP}"\n''' + "\n"
    wr("database/evidence.yml", ey)

ty = rd("database/timeline.yml")
if TID not in ty:
    ty = ty.rstrip() + f'''\n\n  - id: {TID}\n    date: "{DATE_MADE}"\n    title: "P-1241 bluff view preserves early Fifth-to-Seventh Main frontage"\n    summary: "CCHS P-1241 locates Main between Fifth and Seventh; far-left frontage is steward-mapped to the later 501-505 area, with exact address boundaries and building continuity unresolved."\n    confidence: "Very High for catalog geography; probable for later 501-505 area mapping."\n    related_sources: [{SID}]\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n    related_buildings: [B-005, B-001, B-002]\n''' + "\n"
    wr("database/timeline.yml", ty)

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `B-005`, `B-001`, `B-002`; `{TID}` | Circa-1900 bluff view titled Main between Fifth and Seventh; steward maps far-left frontage to later 501-505 area. Exact numbered boundaries/building continuity unresolved. |''')

append_once("evidence/research-leads.md", "P-1241 circa-1900 far-left frontage alignment", f'''### P-1241 circa-1900 far-left frontage alignment

CCHS `P-1241` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) explicitly locates the photographed Main Street span between Fifth and Seventh. The steward maps the far-left frontage to the later 501-505 area. Align that frontage against the 1892/1900 Sanborn sheets and 1895/1907-1916 photographs using party walls, roof heights, setbacks, Fifth Street alignment and adjacent building rhythm. Goal: determine whether any visible circa-1900 mass can be securely mapped to later 501, 503 or 505 without assuming address continuity equals building continuity.''')

append_once("registers/research-log.md", "CCHS P-1241 circa-1900 bluff view", f'''### 2026-09-05 — CCHS P-1241 circa-1900 bluff view
- Integrated project-steward supplied CCHS `{TARGET}` as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Institutional title: **{TITLE}**; it independently locates Main between Fifth and Seventh.
- Steward original preserved by filename, dimensions, bytes and SHA-256 `{STEWARD['sha256']}`; canonical repository binary is the largest exact-object CCHS derivative.
- Direct visual review confirms the far-left early commercial frontage. Steward identifies it as the later 501-505 area; exact individual-number boundaries and building continuity remain probable/unresolved rather than direct.
- No annual research-status certification changed.''')

for rel, bid in (("buildings/501-main.md", "B-005"), ("buildings/503-main.md", "B-001"), ("buildings/505-main.md", "B-002")):
    append_once(rel, "### Circa-1900 P-1241 bluff-view frontage context", f'''### Circa-1900 P-1241 bluff-view frontage context

CCHS `P-1241` (`{SID}` / `{EID}` / `{MID}`) is titled **{TITLE}**, independently fixing the photographed Main Street span between Fifth and Seventh. The project steward identifies the far-left visible frontage as the area later numbered 501-505 Main. The frontage itself is visible, but this photograph does **not** show a readable `{rel.split('/')[-1].split('-')[0]}` number or prove individual later-address boundaries/building continuity. Use as **PROBABLE spatial context** pending Sanborn/photo alignment.
''')
    yaml_add_list_item("database/buildings.yml", bid, "related_evidence", EID)
    yaml_add_list_item("database/buildings.yml", bid, "related_sources", SID)

print(f"Integrated {TARGET} as {SID} / {EID} / {MID} / {TID}")
