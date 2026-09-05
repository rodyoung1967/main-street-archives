from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1043"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1930s - Streetcar on Main at 6th(1).jpg",
    "width": 2048,
    "height": 1214,
    "bytes": 617696,
    "sha256": "870d294ee08012121c057d63b6f90112ff5305600c36a2f1895fa57738b65e08",
    "orientation_note": "Project steward states the camera is looking south from 6th Street toward 5th Street.",
}

CATALOG = {
    "title": "Oregon City 1930s - Streetcar on Main at 6th",
    "entry_object_id": TARGET,
    "description": "Main Street Looking Southwest from 6th Street",
    "date_made": "1930 - 1939",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Halon",
    "other_number": "Society Photo #: 168",
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
with Image.open(BytesIO(data)) as im:
    w, h = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()

slug = entry.get("slug") or match.get("slug")
HUB = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug else ENTRY
)

IMAGE = f"media/photos/main-street/{MID}_1930-1939-main-6th-looking-south-business-roster-cchs-p1043.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-p1043-1930s-main-6th-looking-south-business-roster-2026-09-05.md"
API = "evidence/source-captures/cchs-p1043-1930s-main-6th-business-roster-api-2026-09-05.json"

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

capture = f'''# CCHS {TARGET} — 1930s Main Street from Sixth toward Fifth, business-sign roster

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made: **1930–1939**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of Negative: **Halon**
- Other Number: **Society Photo #: 168**
- Public record: {HUB}
- Public API: {ENTRY}

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`
- Steward orientation statement: **camera looks south from 6th Street toward 5th Street**.

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact `{TARGET}` catalog object
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-file fingerprint is retained. If the public derivative differs in encoding or dimensions, both are treated as representations of the same institutional photograph/object rather than as different scenes.

## Orientation and block geometry

The CCHS description says **Main Street Looking Southwest from 6th Street**. The project steward further clarifies the practical archive orientation as **looking south from Sixth toward Fifth**.

That makes the right side of the photograph the **west / odd-numbered side of Main**, descending toward the 5th/Main target corner, while the left side is the **east / even-numbered side**. The photograph therefore provides an unusually useful same-frame business-sign and facade sequence for reconstructing the Sixth-to-Fifth block.

The 503/505 frontage lies farther south in the photographed row, but no `503`, `505`, `FARR'S`, or other target-address wording is secure enough in this frame to make a new direct occupancy claim from this photograph alone.

## Directly readable business/sign text

### West / odd-numbered side of Main — right side of frame

The following text is directly readable or substantially readable:

- **OREGON CITY AUTO PARTS** — large vertical/arched sign.
- **FAIN'S MEN'S STORE** — projecting sign; smaller wording includes **SHOES** and **UNION MADE GOODS**; **CLEANERS** also appears below.
- **SANDWICH NOOK** — projecting sign.
- **REXALL** — vertical round-topped sign.
- **DRUGS** — large sign below/near the Rexall marker.
- **HARDWARE** — smaller projecting sign in the same general storefront sequence.
- **CAFE** — at least one smaller sign farther south.
- **HOTEL** — multiple hotel signs farther down Main.
- A large painted wall advertisement contains a clear **5-10-25** price sequence and **STORE**, but the business name is partly blocked and is not transcribed as a firm name.

Less-secure readings retained as **PROBABLE / PARTIAL**, not direct full transcriptions:

- a projecting cafe sign ending in **...MONDS CAFE**; the leading letters are obscured;
- a large vertical **... SHOE SHOP** sign at the near-right edge; the proprietor/name above `SHOE SHOP` is clipped;
- additional small furniture/jewelry/ice-cream wording is present but not sufficiently clear for reliable firm-name transcription.

### East / even-numbered side of Main — left side of frame

Directly readable or substantially readable:

- **TOURIST HOTEL** with **FREE GARAGE TO TOURISTS**.
- **ALEXANDER'S MKT.**
- **AMERICAN CLEANERS** is readable on a more distant sign in the east-side row.
- **ICE CREAM** is visible above/near that distant sign; the photograph alone does not establish whether the ice-cream wording belongs to American Cleaners or to a separate overlapping storefront/sign.
- additional market/Coca-Cola and storefront lettering is present but not promoted beyond what is legible.

## Relationship to established archive entities

### 505 Main / Farr's Pool Hall

`{TARGET}` is valuable **spatial context**, but it is not being used as another direct Farr-at-505 source. The stronger 1936 anchor remains CCHS `P-1128` (`S-236` / `E-210` / `IMG-0757` / `T-087`), where the 505 storefront is specifically mapped and the principal sign is probably `FARR'S`.

This photograph should instead be used to reconstruct the intervening storefront sequence from Sixth toward Fifth. Once exact addresses are assigned to the clearly named businesses above, that sequence can independently test where 511, 509, 507, 505 and 503 fall in this perspective.

### Harding Drug Store / Harding Building

The **REXALL / DRUGS** sign cluster lies in the west-side commercial sequence and is visually consistent with the known Harding Drug Store / Harding Building context (`BUS-007` / `B-003`). However, **HARDING** itself is not securely readable in this frame. The archive therefore preserves this as a **PROBABLE / CROSS-SOURCE ALIGNMENT LEAD**, not a direct named-photo identification.

### American Cleaners

The same business name **AMERICAN CLEANERS** is readable here and in the later circa-mid-1960s CCHS `P-4563` record (`BUS-097` / `S-231` / `E-205` / `IMG-0752`). **Name identity alone is not enough to merge the 1930s sign with the later business entity.** The possibility of continuity, relocation, or a distinct same-name operation remains open pending directories, advertisements, licenses, or other independent identifiers.

## Highest-value use of this photograph

This image can become a strong **address-sequence control** by matching its visible business roster against 1930–1939 directories, newspaper advertisements and licenses. The highest-value targets are:

1. exact addresses and operating spans for **Oregon City Auto Parts**, **Fain's Men's Store**, **Sandwich Nook**, **Tourist Hotel**, and **Alexander's Market**;
2. identity/address of the **...MONDS CAFE** sign;
3. identity/address of the near-right **... SHOE SHOP**;
4. exact business behind the painted **5-10-25 ... STORE** wall advertisement;
5. whether the visible **REXALL / DRUGS** grouping can be securely tied to Harding Drug Store in the exposure period;
6. whether the 1930s **AMERICAN CLEANERS** sign is the same business later photographed at Fifth/Main in `P-4563`;
7. use the resolved sign sequence to independently map the distant **503/505** storefronts and cross-check the `P-1128` Farr-at-505 mapping.

## Evidence classification

- **DOCUMENTED / DIRECT:** CCHS `{TARGET}`; catalog date range **1930–1939**; catalog view from Sixth looking southwest; streetcar and Main Street commercial corridor; readable signs listed above.
- **DOCUMENTED / DIRECT, attributed steward spatial statement:** practical orientation south from Sixth toward Fifth.
- **PROBABLE / PARTIAL:** `...MONDS CAFE`, near-right `... SHOE SHOP`, and incomplete painted `5-10-25 ... STORE` name.
- **PROBABLE / CROSS-SOURCE ALIGNMENT LEAD:** Rexall/Drugs grouping as Harding Drug Store context.
- **UNRESOLVED:** exact addresses for most visible businesses; exact exposure year inside 1930–1939; identity continuity for American Cleaners; direct identification of 503 or 505 in this frame.
- **NO NEGATIVE INFERENCE:** inability to read a Farr/503/505 sign in this distant perspective is not evidence that a business was absent.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — CCHS {TARGET}, 1930s Main Street from Sixth toward Fifth
Type: Primary historic streetscape photograph with CCHS institutional metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **1930–1939** per CCHS Date made metadata; exact exposure year unresolved.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Other number: **Society Photo #168**.
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related block context: `B-001` 503 Main; `B-002` 505 Main; `B-003` Harding Building / Harding Drug context.
Notes: Direct sign roster includes Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall/Drugs, Tourist Hotel, Alexander's Mkt., American Cleaners and other partial signs. Most exact street numbers remain unresolved; no new direct 503/505 occupancy claim is made from this frame.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — 1930s P-1043 provides Sixth-to-Fifth Main Street business-sign and facade sequence
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic streetscape evidence with institutional catalog metadata
Claims:
- CCHS `{TARGET}` is cataloged **Oregon City 1930s - Streetcar on Main at 6th**, Date made **1930–1939**, description **Main Street Looking Southwest from 6th Street**.
- Project steward clarifies the view as looking south from Sixth toward Fifth.
- Directly readable west-side signs include **OREGON CITY AUTO PARTS**, **FAIN'S MEN'S STORE**, **SANDWICH NOOK**, **REXALL**, **DRUGS**, **HARDWARE**, and smaller CAFE/HOTEL wording.
- Directly readable east-side signs include **TOURIST HOTEL / FREE GARAGE TO TOURISTS**, **ALEXANDER'S MKT.**, and **AMERICAN CLEANERS**.
- Partial/probable text includes **...MONDS CAFE**, a near-right **... SHOE SHOP**, and a painted **5-10-25 ... STORE** advertisement.
- The Rexall/Drugs cluster is consistent with established Harding Drug context but Harding's name is not directly readable here.
- The distant 503/505 frontage is not secure enough for a new direct occupancy claim; this source is an address-sequence/spatial control to be reconciled with directories and `P-1128`.
Classification: **DOCUMENTED / DIRECT** for object/date range/orientation wording and clearly readable sign text; **PROBABLE / PARTIAL** for incomplete signs; **PROBABLE / CROSS-SOURCE ALIGNMENT LEAD** for Harding; **UNRESOLVED** for most exact street numbers and 503/505-specific signage.
Confidence: **Very High** for the institutional object/date range and clear sign readings; lower where explicitly marked partial/probable.
Related buildings: `B-001`, `B-002`, `B-003`.
Related source control: `S-236` / `E-210` / `IMG-0757` (1936 P-1128 Farr-at-505 anchor).
''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS P-1043, 1930s Main at Sixth looking toward Fifth
- Type: Historic Main Street streetscape / streetcar / commercial-block photograph
- CCHS catalog: `{TARGET}`
- CCHS title: **{CATALOG["title"]}**
- CCHS Date made: **1930–1939**; exact exposure year unresolved
- CCHS description: **{CATALOG["description"]}**
- CCHS other number: **Society Photo #168**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Steward orientation: looking south from Sixth toward Fifth.
- Direct visual text includes Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall, Drugs, Hardware, Tourist Hotel, Alexander's Mkt., American Cleaners, and partial additional signs.
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Key value: same-frame storefront-sign sequence for reconstructing the Sixth-to-Fifth Main Street block and independently checking 503/505 spatial mapping.
- Limit: most exact street numbers and the distant 503/505 sign identities remain unresolved.''')

append_once("media/photos/inventory.md", f"### {MID} —", f'''### {MID} — CCHS P-1043, 1930s Main Street business-sign roster
- File: `{IMAGE}`
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS: `P-1043`; Society Photo #168; Date made **1930–1939**
- Key value: view south from Sixth toward Fifth with a dense readable business-sign sequence on both sides of Main; useful for exact-address reconstruction and cross-checking 503/505.
- Limit: this frame does not securely yield a direct Farr/503/505 sign reading.''')

append_once("indexes/id-crosswalk.md", f"## {SID} / {EID} / {MID} / {TID} — CCHS P-1043", f'''## {SID} / {EID} / {MID} / {TID} — CCHS P-1043, 1930s Sixth-to-Fifth Main Street view

| Record | Links | Notes |
| --- | --- | --- |
| `{SID}` / `{EID}` / `{MID}` / `{TID}` | `B-001`, `B-002`, `B-003`; cross-check `S-236` / `E-210` / `IMG-0757` | 1930–1939 streetscape from Sixth toward Fifth; direct business-sign roster. 503/505 exact signage unresolved in this frame; use as spatial/address-sequence control. |''')

append_once("registers/research-log.md", "### 2026-09-05 — CCHS P-1043", f'''### 2026-09-05 — CCHS P-1043 1930s Main Street from Sixth
- Integrated `{TARGET}` as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Preserved CCHS Date made **1930–1939**, description **Main Street Looking Southwest from 6th Street**, Society Photo #168, and steward clarification that the view looks south from Sixth toward Fifth.
- Direct sign roster records Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall/Drugs, Tourist Hotel, Alexander's Mkt., American Cleaners, Hardware and additional partial signs.
- Did **not** assign most signs to exact street numbers from perspective alone.
- Did **not** merge the 1930s American Cleaners wording with later `BUS-097` solely by name.
- Did **not** treat Rexall/Drugs as a direct Harding-name transcription; it is retained only as a probable cross-source alignment lead.
- Did **not** make a new direct 503/505 occupancy claim from the distant frontage. `P-1128` remains the stronger 1936 Farr-at-505 anchor.''')

append_once("evidence/research-leads.md", "### P-1043 1930s Sixth-to-Fifth storefront-sequence lead", f'''### P-1043 1930s Sixth-to-Fifth storefront-sequence lead

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) provides a dense, dated-range **1930–1939** sign sequence looking south from Sixth toward Fifth. Cross-check 1930–1939 directories, ads and licenses for **Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Tourist Hotel, Alexander's Market, the partial ...MONDS CAFE, the clipped ... SHOE SHOP, the painted 5-10-25 ... STORE sign, and the Rexall/Drugs grouping**.

Primary goals: assign exact numbered addresses; narrow the photograph's exposure year by overlapping business operating spans; test whether the Rexall/Drugs position is Harding Drug Store; determine whether the 1930s American Cleaners sign is related to later `BUS-097`; then use the resolved west-side address sequence as an independent geometry check on `P-1128` / Farr's Pool Hall at 505. Do not merge same-name businesses or infer exact addresses from sign order alone.''')

append_once("timeline.md", f"## {TID} — 1930–1939 — P-1043 Main Street business-sign roster", f'''## {TID} — 1930–1939 — P-1043 Main Street business-sign roster

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}`) looks southwest/south from Sixth toward Fifth and preserves a dense commercial-sign sequence. Clear text includes **Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall/Drugs, Tourist Hotel, Alexander's Mkt., American Cleaners**, and other partial signs. This is a high-value block-mapping control, but most exact numbers remain unresolved and the distant 503/505 frontage is not secure enough for a new direct occupancy claim.

Cross-check: the independently integrated **1936 P-1128** view (`S-236` / `E-210` / `IMG-0757`) remains the stronger photographic anchor for Farr's Pool Hall at 505.''')

append_once("buildings/503-main.md", "## 1930s P-1043 Sixth-to-Fifth spatial control", f'''## 1930s P-1043 Sixth-to-Fifth spatial control

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}` / `{TID}`), dated **1930–1939**, looks south from Sixth toward Fifth and shows the west-side odd-numbered commercial row continuing toward the 503/505 corner. The image supplies a dense business-sign/facade sequence that can help map the target frontage once the intervening businesses are assigned exact numbers. **No 503 sign or business name is securely readable at the target distance in this frame**, so it is context rather than a new 503 occupancy record.''')

append_once("buildings/505-main.md", "## 1930s P-1043 Sixth-to-Fifth spatial control", f'''## 1930s P-1043 Sixth-to-Fifth spatial control

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}` / `{TID}`), dated **1930–1939**, looks south from Sixth toward Fifth and provides a same-frame sign sequence along the west-side odd-numbered Main Street row. It should be used to assign intermediate storefront numbers and independently test the 505 position.

**No `505` or secure `FARR'S` wording is directly readable in this more distant view.** The stronger operating-state anchor remains CCHS `P-1128` (`S-236` / `E-210` / `IMG-0757`), where steward storefront mapping plus probable `FARR'S` signage supports Farr's Pool Hall at 505 in 1936.''')

append_once("buildings/507-harding-building.md", "## 1930s P-1043 Rexall/Drugs alignment lead", f'''## 1930s P-1043 Rexall/Drugs alignment lead

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}`), dated **1930–1939**, directly shows a **REXALL / DRUGS** sign cluster in the west-side Main Street storefront sequence. Its position is consistent with the established Harding Drug / Harding Building context, but **HARDING is not securely readable in this image**. Treat the photograph as a **probable cross-source alignment lead**, not a direct named Harding identification, until the exact directory/address sequence is matched.''')

if Path("businesses/american-cleaners.md").exists():
    append_once("businesses/american-cleaners.md", "## 1930s same-name P-1043 lead", f'''## 1930s same-name P-1043 lead

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}`) visibly contains **AMERICAN CLEANERS** wording in the east-side Main Street row during a broad **1930–1939** catalog period. This is **not yet merged into `BUS-097` as the same operating entity**. The later `P-4563` American Cleaners is circa mid-1960s at the northeast 5th/Main corner; continuity, relocation, legal identity and exact 1930s address require independent evidence.''')

if Path("businesses/harding-drug-store.md").exists():
    append_once("businesses/harding-drug-store.md", "## 1930s P-1043 Rexall/Drugs lead", f'''## 1930s P-1043 Rexall/Drugs lead

CCHS `P-1043` (`{SID}` / `{EID}` / `{MID}`), cataloged **1930–1939**, shows **REXALL** and **DRUGS** signage in the expected west-side Main Street sequence. The spatial relationship is consistent with Harding Drug Store, but the name **HARDING** is not directly legible, so this remains a **probable alignment lead** rather than direct business-name proof.''')

for path, addr in (("timelines/503-main.md", "503"), ("timelines/505-main.md", "505")):
    if Path(path).exists():
        append_once(path, f"| 1930–1939 | P-1043 block-sequence context", f'''| 1930–1939 | P-1043 block-sequence context | CCHS `P-1043` looks south from Sixth toward Fifth and preserves a dense west-side odd-number storefront-sign sequence. Exact `{addr}` sign/occupant is not securely readable in this frame; use it as spatial/address-sequence context and cross-check with `P-1128`. | `{EID}`; `{SID}`; `{MID}` |''')

append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "CCHS P-1043 — Oregon City 1930s, streetcar on Main at 6th"
    url: "{HUB}"
    type: Primary historic streetscape photograph with CCHS institutional catalog metadata
    date: "1930-1939"
    repository_file: "{IMAGE}"
    notes: "View southwest/south from Sixth toward Fifth. Direct sign roster includes Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall/Drugs, Tourist Hotel, Alexander's Mkt., American Cleaners and partial additional signs. Most exact numbers and direct 503/505 signage remain unresolved."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "1930s P-1043 provides Sixth-to-Fifth Main Street business-sign and facade sequence"
    type: Primary photographic streetscape evidence with institutional catalog metadata
    date: "1930-1939"
    claims:
      - "CCHS P-1043 is cataloged Oregon City 1930s - Streetcar on Main at 6th, Date made 1930-1939, description Main Street Looking Southwest from 6th Street."
      - "Project steward clarifies the practical orientation as looking south from Sixth toward Fifth."
      - "Direct sign text includes Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall, Drugs, Hardware, Tourist Hotel, Alexander's Mkt., and American Cleaners."
      - "Partial signs include ...MONDS CAFE, a clipped ... SHOE SHOP, and a painted 5-10-25 ... STORE advertisement."
      - "Rexall/Drugs is a probable Harding alignment lead, not direct HARDING transcription."
      - "The distant 503/505 frontage is not secure enough for a new direct occupancy claim; use as spatial/address-sequence control."
    confidence: "Very High for object/date range/clear sign readings; probable where marked; exact addresses and target storefront identities unresolved."
    related_sources: [{SID}]
    related_buildings: [B-001, B-002, B-003]''')

append_once("database/timeline.yml", f"  - id: {TID}", f'''  - id: {TID}
    date: "1930-1939"
    title: "1930-1939 — P-1043 Main Street business-sign roster from Sixth toward Fifth"
    summary: "CCHS P-1043 preserves a dense business-sign sequence looking south from Sixth toward Fifth. Clear text includes Oregon City Auto Parts, Fain's Men's Store, Sandwich Nook, Rexall/Drugs, Tourist Hotel, Alexander's Mkt. and American Cleaners. Exact addresses and direct 503/505 signage remain unresolved; use as block-mapping control."
    confidence: "Very High for catalog/sign text; unresolved for most exact addresses and target storefront identities."
    related_sources: [{SID}]
    related_evidence: [{EID}]
    related_buildings: [B-001, B-002, B-003]''')

for bid in ("B-001", "B-002", "B-003"):
    yaml_add_list_item("database/buildings.yml", bid, "related_evidence", EID)
    yaml_add_list_item("database/buildings.yml", bid, "related_sources", SID)

print(f"Integrated {TARGET}: {SID} / {EID} / {MID} / {TID}")
print(f"Repository image: {IMAGE}")
