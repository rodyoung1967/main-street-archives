from pathlib import Path
import hashlib
import json
import re
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "2008.008.005.002"
ACCOUNT = "4813"
ENTRY_ID = "82ebfcc0-9b1e-11eb-b3ef-53e7205a00b4"
SLUG = "oregon-city-1896-6th-and-main-street"
REVIEW = "2026-09-05"
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}"
HUB = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{SLUG}"

STEWARD = {
    "filename": "Oregon City 1896 - 6th and Main Street.jpg",
    "width": 2048,
    "height": 1616,
    "bytes": 1143797,
    "sha256": "bdaecd73ca379a34d444afc8764b6972c0bb39532a906a0f33b3dceb34bac3c8",
}
STEWARD_SPATIAL = (
    "Project steward identifies the two men near the Fifth/Main crossing as standing on the northeast corner of Fifth and Main. "
    "With that fixed corner, the right/west side of Main approaching Fifth contains predecessor buildings on the sites later numbered "
    "511, 509, 507, 505, 503 and 501; the old 501-505 group is visible farther down the right side and must not be described as the later/current buildings."
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
        return
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    fm = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if fm:
        field_start = m.start() + fm.end()
        after = text[field_start:end]
        nf = re.search(r"(?m)^    [A-Za-z0-9_]+:", after)
        insert_at = field_start + (nf.start() if nf else len(after))
        text = text[:insert_at].rstrip("\n") + f"\n      - {item}\n" + text[insert_at:].lstrip("\n")
    else:
        insert_at = end
        text = text[:insert_at].rstrip("\n") + f"\n    {field}:\n      - {item}\n\n" + text[insert_at:].lstrip("\n")
    wr(path, text)


# Exact-object idempotency. Do not let references to the title block a first integration.
if (
    f"Catalog ID: `{TARGET}`" in rd("evidence/source-register.md")
    or f"CCHS object: **{TARGET}**" in rd("media/photo-metadata-register.md")
):
    print(f"{TARGET} already integrated; no changes needed.")
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

TITLE = prop(entry, "hasName") or "Oregon City 1896 - 6th and Main Street"
DESCRIPTION = prop(entry, "hasDescription") or labeled_value(entry, "Description")
DATE_MADE = labeled_value(entry, "Date made") or "1896 (from institutional title; separate Date made field not recovered)"
MEDIUM = labeled_value(entry, "Medium")
NEGATIVE = labeled_value(entry, "Location of Negative")
OTHER = labeled_value(entry, "Other Number") or labeled_value(entry, "Other No.")

IMAGE = f"media/photos/early-main-street/{MID}_1896-6th-main-predecessor-501-505-cchs-2008-008-005-002.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-2008-008-005-002-1896-6th-main-predecessor-501-505-2026-09-05.md"
API = "evidence/source-captures/cchs-2008-008-005-002-1896-6th-main-api-2026-09-05.json"

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
    "steward_spatial_annotation": STEWARD_SPATIAL,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

SOURCE_NAME = f"CCHS {TARGET} — Oregon City 1896, Sixth and Main streetscape"
EVIDENCE_NAME = "1896 Sixth/Main photograph anchors predecessor frontage on the later 501-505 sites"

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`. Related buildings/sites: `B-005` (later-numbered 501), `B-001` (later-numbered 503), `B-002` (later-numbered 505). Related business context: `BUS-007` (Harding Drug Store).

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

## Project-steward supplied image

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Spatial annotation: **{STEWARD_SPATIAL}**

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact object `{TARGET}`
- Dimensions: **{width} × {height}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-file fingerprint is preserved even when the repository uses a different institutional derivative of the same catalog object.

## Direct visual review

The photograph looks south along Main Street through the Sixth-to-Fifth commercial block. The following sign text is readable or substantially readable in the supplied scan:

- **PORTLAND HOUSE** on the east/left side of Main;
- **TICKET O... / EAST S... / RAILWA...** on the west/right side, consistent with an East Side Railway ticket-office sign;
- **HARDING / CUT R... / DRUG ST...** immediately below/near the railway-ticket sign;
- an **OFFICE** sign on the east/left side;
- a probable **KRAUSSE BROS.** sign at the upper-left edge, retained as a probable transcription rather than a fully secure reading.

No `501`, `503`, `505`, `507`, `509`, or `511` street number is readable in the photograph.

## Fifth/Main spatial anchor and later-numbered sites

The project steward identifies the two men near the Fifth/Main crossing as standing on the **northeast corner of Fifth and Main**. Treated as attributed steward spatial testimony, that fixed corner makes the right side of the photograph the **west / later odd-numbered side of Main** as the view approaches Fifth.

The later address sequence on that side is **511 → 509 → 507 → 505 → 503 → 501** moving south toward Fifth. This sequence is independently documented for the later numbered era; it is used here only as a spatial reference system.

The structures visible in this 1896 photograph at the later-numbered **501, 503 and 505 sites are predecessor buildings**. They are **not** to be described as the later/current 501, 503 or 505 structures merely because they occupy the same general street positions. Individual bay boundaries in the distant 501-505 group are not sufficiently legible in this scan to assign a particular 1896 storefront/business to 501, 503 or 505.

## Harding / ticket-office address interpretation

The **HARDING / ... DRUG ST...** and adjacent railway-ticket wording provide a strong business-sign anchor on the west/right side north of Fifth. Existing archive evidence later places George A. Harding's drug business at **511 Main in 1911-1915** and strongly supports a later **507** association in March 1921. CCHS also retrospectively catalogs an 1880/1880s Harding storefront photograph as **505 Main**, while the image itself shows no number.

Therefore this 1896 photograph **does not by itself prove a numbered address for Harding**. Its physical position is compatible with the later odd-numbered storefront sequence and is valuable for reconstructing the pre-numbering block, but an 1896-to-later-number assignment must be established by Sanborn/fixed-landmark geometry or a contemporary address/building-name source rather than back-projecting the 1911 number.

## Evidence classification

- **DOCUMENTED / DIRECT:** exact CCHS object/title and catalog date context; visible Main Street streetscape.
- **VISUALLY VERIFIED:** Portland House; Harding/drug-store wording; railway ticket-office wording; broad storefront order and predecessor building fabric.
- **ATTRIBUTED PROJECT-STEWARD SPATIAL TESTIMONY:** the two men mark the northeast Fifth/Main corner.
- **STRONG SPATIAL INFERENCE:** with that corner fixed, the west/right-side approach corresponds to the sites later numbered 511 through 501 in descending order toward Fifth.
- **DOCUMENTED CAUTION:** the 1896 structures at later 501-505 positions are predecessor buildings; same later address position does not establish building continuity.
- **UNRESOLVED:** exact individual 1896 bay boundaries for later 501/503/505; exact numbered location of Harding in 1896; precise identity/address of Portland House, East Side Railway office and probable Krausse Bros. from this photo alone.

## Research value / next test

This photograph should be aligned against the **1890 and 1892 Sanborn sheets** and the nearby 1895/1896 fixed-location photographs. The highest-value test is to use Fifth Street, Sixth Street, party-wall spacing, roof heights and storefront widths to map the later 501/503/505/507/509/511 sites onto the photographed predecessor buildings without assuming continuity.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`.  
Date: **{DATE_MADE}**.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.  
Related sites/buildings: `B-005`, `B-001`, `B-002`; related business context: `BUS-007`.  
Notes: Steward fixes the northeast Fifth/Main corner by the two men. The visible later-501/503/505 positions contain predecessor buildings, not the later/current structures. Readable Harding/drug-store and railway-ticket signs are preserved without assigning an unsupported 1896 street number.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Type: Primary historic photograph / spatial and predecessor-building evidence  
Claims:
- CCHS `{TARGET}` is titled **{TITLE}** and is dated **{DATE_MADE}**.
- Direct visual review reads **PORTLAND HOUSE**, substantial **HARDING / ... DRUG ST...** wording and substantial **TICKET ... / EAST ... / RAILWA...** wording.
- Project steward identifies the two men near the crossing as standing on the northeast corner of Fifth and Main.
- Using that corner only as an attributed spatial anchor, the right/west-side approach corresponds to the sites later numbered 511, 509, 507, 505, 503 and 501 toward Fifth.
- The 1896 structures at the later 501/503/505 positions are predecessor buildings; the photograph does not establish continuity with the later/current buildings.
- No individual 1896 business is assigned to later 501, 503 or 505 from this image alone, and Harding is not assigned an 1896 number from later address evidence.
Classification: **DOCUMENTED / DIRECT** for object/date and visible sign/street fabric; **ATTRIBUTED PROJECT-STEWARD SPATIAL TESTIMONY** for the northeast-corner identification; **STRONG SPATIAL INFERENCE** for the later-numbered site sequence; **UNRESOLVED** for individual predecessor bay/address assignments and Harding's exact 1896 number.  
Confidence: **Very High** for object identity and visible signs; **High** for the steward-anchored side/order geometry; **Unresolved** for exact 501/503/505 predecessor boundaries.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS {TARGET} Oregon City 1896, Sixth and Main", f'''## {MID} — CCHS {TARGET} Oregon City 1896, Sixth and Main
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS object: **{TARGET}**
- CCHS title: **{TITLE}**
- Date made: **{DATE_MADE}**
- Repository file: `{IMAGE}`
- Repository dimensions: **{width} × {height}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward upload: `{STEWARD['filename']}`, **{STEWARD['width']} × {STEWARD['height']}**, {STEWARD['bytes']:,} bytes, SHA-256 `{STEWARD['sha256']}`
- Visual review: Portland House; Harding/drug-store wording; East Side Railway ticket-office wording; Sixth-to-Fifth Main streetscape.
- Spatial caution: steward identifies the two men as the northeast Fifth/Main corner. The later 501-505 sites are visible on the right/west side as **predecessor buildings**, not the later/current structures. Individual bay assignments remain unresolved.
- Public record: {HUB}''')

append_once("media/photos/early-main-street/README.md", f"## {MID} — CCHS {TARGET} Oregon City 1896, Sixth and Main", f'''## {MID} — CCHS {TARGET} Oregon City 1896, Sixth and Main

- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- Directly visible: Portland House, Harding/drug-store wording, railway ticket-office wording and the pre-numbering Main Street building fabric.
- Steward spatial anchor: the two men mark the northeast Fifth/Main corner.
- The later 501/503/505 positions contain **older predecessor buildings** in this image. Do not backdate the later building identities to 1896.''')

append_once("timeline.md", f"## 1896 — CCHS Sixth/Main predecessor-frontage photograph ({TID})", f'''## 1896 — CCHS Sixth/Main predecessor-frontage photograph (`{TID}`)

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) is titled **{TITLE}**. The photograph visibly shows Portland House, Harding/drug-store wording and East Side Railway ticket-office wording. The project steward identifies the two men near Fifth as standing on the **northeast corner of Fifth and Main**, allowing the right/west side to be read as the pre-numbering sites later numbered 511 through 501 toward Fifth. The buildings occupying the later **501/503/505 sites in 1896 are predecessor structures**; no continuity with the later/current buildings is inferred and no individual 1896 business is assigned to 501/503/505 from this image alone.''')

append_once("registers/research-log.md", f"### 2026-09-05 — integrated CCHS {TARGET} 1896 Sixth/Main predecessor-frontage view", f'''### 2026-09-05 — integrated CCHS {TARGET} 1896 Sixth/Main predecessor-frontage view
- Added `{SID}` / `{EID}` / `{MID}` / `{TID}` and the largest public CCHS derivative of the exact catalog object.
- Preserved the steward original-file fingerprint: {STEWARD['width']}×{STEWARD['height']}, {STEWARD['bytes']:,} bytes, SHA-256 `{STEWARD['sha256']}`.
- Recorded visible Portland House, Harding/drug-store and East Side Railway ticket-office wording.
- Preserved the steward's northeast Fifth/Main corner identification as attributed spatial testimony.
- Recorded the crucial structural distinction that the 1896 buildings on the later 501/503/505 sites are **predecessor buildings**, not the later/current structures.
- Did not back-project Harding's later 511/507 addresses into 1896 and did not assign individual 1896 businesses to later 501/503/505 without a geometric or contemporary-address bridge.''')

append_once("evidence/research-leads.md", f"### 1896 CCHS {TARGET} supplement", f'''### 1896 CCHS {TARGET} supplement
`{SID}` / `{EID}` / `{MID}` adds a fixed-view test for the existing Harding Block / Willamette Building and pre-numbering storefront-mapping problem. Align the steward-identified northeast Fifth/Main corner and the visible Harding/railway-ticket signs against the 1890/1892 Sanborns and neighboring historic photographs. Goal: map later 501/503/505/507/509/511 **sites** onto the 1896 predecessor bays without assuming that any pictured building survives into the later numbered era.''')

for path, title in [
    ("buildings/501-main.md", "## 1896 CCHS predecessor-site photograph"),
    ("buildings/503-main.md", "## 1896 CCHS predecessor-site photograph"),
    ("buildings/505-main.md", "## 1896 CCHS predecessor-site photograph"),
]:
    append_once(path, title, f'''{title}
`{SID}` / `{EID}` / `{MID}` preserves CCHS `{TARGET}`, **{TITLE}**. The project steward fixes the northeast Fifth/Main corner using the two men visible near the crossing. The later-numbered 501/503/505 positions can therefore be placed generally on the right/west side approaching Fifth, but the structures visible there in 1896 are **predecessor buildings**, not the later/current numbered building. Individual 1896 bay boundaries and occupants remain unresolved; address position is not treated as building continuity.''')

append_once("businesses/harding-drug-store.md", "## 1896 Sixth/Main street-view anchor", f'''## 1896 Sixth/Main street-view anchor
CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), titled **{TITLE}**, directly shows substantial **HARDING / ... DRUG ST...** wording next to substantial East Side Railway ticket-office wording on the west/right side of Main north of Fifth. The project steward's Fifth/Main corner identification makes this valuable pre-numbering spatial evidence. It does **not** by itself prove Harding's exact 1896 numbered address. Keep the 1880/1880s retrospective 505 catalog label, the 1911-1915 direct 511 evidence and the 1921 strong 507 inference separate until geometric/contemporary evidence resolves the earlier move sequence.''')

append_once("indexes/id-crosswalk.md", f"| `{TARGET}` CCHS 1896 Sixth/Main", f'''| `{TARGET}` CCHS 1896 Sixth/Main | `{SID}` | `{MID}` / `{IMAGE}` | `{EID}`, `{TID}` | `B-005`, `B-001`, `B-002`, `BUS-007` |''')

# Synchronized YAML records.
sy = rd("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SID)}\s*$", sy) is None:
    sy = sy.rstrip() + f'''\n\n  - id: {SID}\n    name: "{SOURCE_NAME}"\n    url: "{CAP}"\n    notes: "CCHS {TARGET}; 1896 Sixth/Main streetscape. Steward fixes northeast Fifth/Main corner; later 501-505 positions contain predecessor buildings. Harding/drug-store and railway-ticket wording visible; no unsupported 1896 number assigned."\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n''' + "\n"
    wr("database/sources.yml", sy)

ey = rd("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EID)}\s*$", ey) is None:
    ey = ey.rstrip() + f'''\n\n  - id: {EID}\n    name: "{EVIDENCE_NAME}"\n    type: "Primary historic photograph / spatial and predecessor-building evidence"\n    claims:\n      - "CCHS {TARGET} documents the 1896 Sixth/Main streetscape and visible Harding/drug-store, railway-ticket and Portland House signage."\n      - "Project steward identifies the two men near Fifth as standing on the northeast Fifth/Main corner; with that anchor, the right/west-side approach corresponds to sites later numbered 511 through 501 toward Fifth."\n      - "The 1896 structures at later 501/503/505 positions are predecessor buildings; no later-building continuity or exact 1896 numbered business assignment is inferred."\n    confidence: "Very High for object/sign visibility; High for steward-anchored side/order geometry; unresolved for exact individual predecessor bay/address assignments."\n    related_sources: [{SID}]\n    related_media: [{MID}]\n    related_buildings: [B-005, B-001, B-002]\n    related_businesses: [BUS-007]\n''' + "\n"
    wr("database/evidence.yml", ey)

ty = rd("database/timeline.yml")
if re.search(rf"(?m)^  - id: {re.escape(TID)}\s*$", ty) is None:
    ty = ty.rstrip() + f'''\n\n  - id: {TID}\n    date: "1896"\n    summary: "CCHS {TARGET} shows the Sixth-to-Fifth Main streetscape. Steward identifies the northeast Fifth/Main corner; later 501/503/505 sites contain predecessor buildings, with Harding/drug-store and East Side Railway ticket-office wording visible farther north on the west side."\n    confidence: "High for dated photo/signs and steward-anchored block geometry; individual later-numbered predecessor bay assignments unresolved."\n    related_sources: [{SID}]\n    related_evidence: [{EID}]\n    related_media: [{MID}]\n    related_buildings: [B-005, B-001, B-002]\n    related_businesses: [BUS-007]\n''' + "\n"
    wr("database/timeline.yml", ty)

for bid in ("B-001", "B-002", "B-005"):
    yaml_add_list_item("database/buildings.yml", bid, "related_evidence", EID)
    yaml_add_list_item("database/buildings.yml", bid, "related_sources", SID)

yaml_add_list_item("database/businesses.yml", "BUS-007", "related_evidence", EID)
yaml_add_list_item("database/businesses.yml", "BUS-007", "related_sources", SID)

print(f"Integrated {TARGET} as {SID} / {EID} / {MID} / {TID}")
print(f"Image: {IMAGE} ({width}x{height}, {nbytes} bytes, sha256 {sha})")
