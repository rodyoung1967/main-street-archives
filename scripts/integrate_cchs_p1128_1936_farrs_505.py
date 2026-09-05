from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1128"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1936 - 5th and Main from the Bluff.jpg",
    "width": 2048,
    "height": 1281,
    "bytes": 847507,
    "sha256": "518fbb3621ce273ae057dd1c759f3efd5c6ee3c8dad1131430c8b3253e6636fb",
    "visual_note": "Project steward identifies the target storefront as 505 Main and asked for enlarged sign review.",
}

CATALOG = {
    "title": "Oregon City 1936 - 5th and Main from the Bluff",
    "entry_object_id": TARGET,
    "tags": ["Arcadia"],
    "description": "Pacific Highway Through Oregon City. Photo by Ralph Eddy.  Also Negative and Sample Print - 2008.008.001.104  Original Maxine Bohoskie #2",
    "date_made": "1936",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Photographic Paper",
    "location_of_negative": "Halon",
    "accession_number": "2002.071.010",
}

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET, "size": 50})


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
            if "thumbnail" in key.lower() or key in {"dominant_color", "complementary_color"}:
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


# Idempotency guard.
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
    raise SystemExit("Matching CCHS result has no id")
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{entry_id}"
entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit(f"Fetched entry mismatch: expected {TARGET}, got {catno(entry)}")

slug = entry.get("slug") or match.get("slug")
HUB = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}" if slug else ENTRY

der = choose_derivative(entry)
data = get_bytes(der["url"])
if not data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected P-1128 derivative is not JPEG")
with Image.open(BytesIO(data)) as im:
    width, height = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()

IMAGE = f"media/photos/main-street/{MID}_1936-5th-main-bluff-farrs-505-cchs-p1128.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-p1128-1936-5th-main-bluff-farrs-505-signage-2026-09-05.md"
API = "evidence/source-captures/cchs-p1128-1936-5th-main-bluff-api-2026-09-05.json"

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

capture = f'''# CCHS P-1128 — Oregon City 1936, 5th and Main from the Bluff; 505 Farr signage review

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`. Related building/business: `B-002` / `BUS-013`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **Oregon City 1936 - 5th and Main from the Bluff**
- Entry/Object ID: **P-1128**
- Tag: **Arcadia**
- Description: **Pacific Highway Through Oregon City. Photo by Ralph Eddy.  Also Negative and Sample Print - 2008.008.001.104  Original Maxine Bohoskie #2**
- Date made: **1936**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Location of Negative: **Halon**
- Accession Number: **2002.071.010**
- Public record: {HUB}
- Public API: {ENTRY}

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact `P-1128` catalog object
- Dimensions: **{width} × {height}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-file fingerprint is retained because the repository connector cannot directly transfer the local attachment binary. The committed image is a derivative of the **exact same CCHS P-1128 catalog object**, not a substitute scene.

## Direct visual review of the 505 storefront

The photograph is a high, oblique view of the Fifth/Main commercial block. The project steward identifies the target storefront in the Main Street row as **505 Main**.

Focused enlarged review of the signage immediately above/on that storefront yields:

- the principal word is **PROBABLE `FARR'S`**;
- accompanying/lower wording is **LIKELY `POOL` or `POOL HALL`**, but the surviving resolution is not strong enough for a letter-perfect transcription;
- smaller secondary signs on the storefront are not read confidently and are left unresolved.

The archive therefore does **not** label the entire sign as a fully direct transcription.

## Cross-source interpretation

Independent existing City historic-resource evidence (`S-036` / `E-033`) identifies **Edwin F. Farr and Alice Farr as proprietors of Farr's Pool Hall at 505 Main**. The CCHS image is independently dated **1936**.

Combining:

1. the exact 1936 CCHS photograph;
2. the steward's 505 storefront identification;
3. the probable visual reading **FARR'S** with likely pool-related wording; and
4. the independent official-secondary identification of **Farr's Pool Hall at 505 Main**,

supports a **STRONG CROSS-SOURCE INFERENCE that P-1128 photographs Farr's Pool Hall operating at 505 Main in 1936**.

This is stronger than using the City inventory alone to associate Farr's with 505, but it remains carefully separated from a direct letter-perfect sign transcription.

## Chronological consequence

The photograph supplies a **1936 operating-state anchor** for the Farr business at 505. It does **not** establish that Farr's opened in 1934, 1936, or any specific earlier year. The **1934** date in the historic-resource material remains the Farrs' residence-acquisition context, not a business opening date.

The later Harr's Recreation Center record remains a separate business. The exact **Farr → Harr** transition date is still unresolved.

## Evidence classification

- **DOCUMENTED / DIRECT:** CCHS `P-1128`; institutional date **1936**; scene is the Fifth/Main corridor as cataloged.
- **PROBABLE / WORKING HYPOTHESIS (visual transcription):** principal 505 sign reads **FARR'S**; pool-related lower wording is likely but not fully legible.
- **STRONG CROSS-SOURCE INFERENCE:** the photographed 505 storefront is **Farr's Pool Hall in 1936**, based on the probable signage plus independent `S-036` / `E-033` business/address identification.
- **UNRESOLVED:** exact opening year; exact full sign wording; proprietor physically present at exposure; Farr-to-Harr transfer date; any property-ownership conclusion.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f'''## {SID} — CCHS P-1128 — Oregon City 1936, 5th and Main from the Bluff
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `P-1128`.
Date: **1936** per CCHS Date made metadata.
Photographer: **Ralph Eddy**, per CCHS description.
Accession: **2002.071.010**; description also references negative/sample print `2008.008.001.104` and Original Maxine Bohoskie #2.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related building/business: `B-002` / `BUS-013`.
Notes: Steward maps the target storefront to 505 Main. Enlarged review gives probable `FARR'S` and likely pool-related wording; cross-source comparison with `S-036` / `E-033` strongly supports Farr's Pool Hall at 505 in the 1936 photographed state. Full sign transcription remains unresolved.''')

append_once("evidence/evidence-register.md", f"## {EID} —", f'''## {EID} — 1936 P-1128 photograph strongly supports Farr's Pool Hall at 505 Main
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence with institutional catalog metadata plus cross-source business/address identification
Claims:
- CCHS `P-1128` is cataloged **Oregon City 1936 - 5th and Main from the Bluff**, Date made **1936**, photograph by Ralph Eddy per the institutional description.
- Project-steward spatial identification maps the target storefront in the photographed Main Street row to **505 Main**.
- Enlarged visual review yields **PROBABLE `FARR'S`** as the principal sign and likely **POOL / POOL HALL** wording, but not a secure letter-perfect full-sign transcription.
- Independent `S-036` / `E-033` identifies Edwin F. and Alice Farr as proprietors of **Farr's Pool Hall at 505 Main**.
- Together these facts support a **STRONG CROSS-SOURCE INFERENCE** that the 1936 photograph shows Farr's Pool Hall operating at 505 Main.
- The photograph does not establish an opening date, property ownership, the physical presence of either proprietor, or the Farr-to-Harr transition date.
Classification: **DOCUMENTED / DIRECT** for object/date; **PROBABLE / WORKING HYPOTHESIS** for exact sign transcription; **STRONG CROSS-SOURCE INFERENCE** for Farr's Pool Hall at 505 in the 1936 photographed state.
Confidence: **High** for the 1936 Farr's-at-505 operating-state conclusion; lower for exact lower-line sign wording.
Related sources: `{SID}`, `S-036`.
Related evidence: `E-033`.
Related business: `BUS-013`.
Related building: `B-002`.''')

append_once("media/photo-metadata-register.md", f"## {MID} —", f'''## {MID} — CCHS P-1128, Oregon City 1936 — 5th and Main from the Bluff
- Type: Historic elevated streetscape / commercial-block photograph
- CCHS catalog: `P-1128`
- CCHS title: **Oregon City 1936 - 5th and Main from the Bluff**
- Date made: **1936**
- Photographer: **Ralph Eddy**, per CCHS description
- Accession: **2002.071.010**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{width} × {height}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Related building/business: `B-002` / `BUS-013`
- Sign review: 505 principal sign **probably reads `FARR'S`**; lower wording is likely `POOL` or `POOL HALL` but not securely transcribed.
- Cross-source value: with `S-036` / `E-033`, strongly supports **Farr's Pool Hall at 505 Main in 1936**; does not establish opening date.''')

append_once("media/photos/inventory.md", f"### {MID} —", f'''### {MID} — CCHS P-1128 — 1936 Fifth/Main bluff view
- File: `{IMAGE}`
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS: `P-1128`; accession **2002.071.010**; photograph by Ralph Eddy per catalog description.
- Key value: project-steward mapping identifies the 505 storefront; enlarged review gives probable **FARR'S** and likely pool-related wording. Cross-source comparison with `E-033` strongly supports **Farr's Pool Hall at 505 Main in 1936**.
- Limit: full sign text, business opening date, property ownership, and Farr-to-Harr transition remain unresolved.''')

append_once("indexes/id-crosswalk.md", f"## {SID} / {EID} / {MID} / {TID} — CCHS P-1128", f'''## {SID} / {EID} / {MID} / {TID} — CCHS P-1128, 1936 Fifth/Main bluff view

| Record | Links | Notes |
| --- | --- | --- |
| `{SID}` / `{EID}` / `{MID}` / `{TID}` | `B-002`; `BUS-013`; `S-036` / `E-033` | Exact 1936 CCHS photograph. Steward maps target storefront to 505; probable **FARR'S** sign and likely pool wording combine with independent City business/address evidence to strongly support Farr's Pool Hall at 505 in 1936. Exact full sign text/opening date remain unresolved. |''')

append_once("registers/research-log.md", "### 2026-09-05 — CCHS P-1128 1936 Farr signage at 505", f'''### 2026-09-05 — CCHS P-1128 1936 Farr signage at 505
- Integrated CCHS `P-1128` as `{MID}` / `{SID}` / `{EID}` / `{TID}` with the steward-supplied metadata and exact steward-file fingerprint preserved.
- CCHS dates the photograph **1936** and credits **Ralph Eddy** in the description.
- Project steward identifies the target storefront as **505 Main**. Enlarged review reads the principal sign as **probable `FARR'S`**; lower wording is likely pool-related but is not strong enough for a letter-perfect transcription.
- Cross-source comparison with the existing official-secondary `S-036` / `E-033` identification of **Farr's Pool Hall at 505 Main** supports a **STRONG CROSS-SOURCE INFERENCE** that Farr's was operating there in the 1936 photographed state.
- This creates a 1936 occupancy anchor but does **not** turn the Farrs' 1934 residence purchase into a pool-hall opening date and does not resolve the Farr-to-Harr transition.''')

append_once("businesses/farrs-pool-hall.md", "## 1936 photographic anchor — CCHS P-1128", f'''## 1936 photographic anchor — CCHS P-1128

CCHS `P-1128` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) is an independently cataloged **1936** bluff view of Fifth/Main. The project steward identifies the target storefront as **505 Main**. Enlarged review makes the principal storefront sign **probable `FARR'S`**, with lower wording likely **POOL / POOL HALL** but not securely legible enough for a full direct transcription.

Because the independent City historic-resource evidence (`S-036` / `E-033`) already identifies **Farr's Pool Hall at 505 Main**, the combined evidence is classified **STRONG CROSS-SOURCE INFERENCE** that the photograph shows Farr's Pool Hall operating at 505 in **1936**. This is an operating-state anchor, not an opening date. The Farr-to-Harr transition remains unresolved.''')

append_once("buildings/505-main.md", "## 1936 CCHS P-1128 Farr signage anchor", f'''## 1936 CCHS P-1128 Farr signage anchor

CCHS `P-1128` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) is dated **1936** and shows the Fifth/Main block from the bluff. The project steward identifies the relevant storefront as **505 Main**. Enlarged review yields a **probable `FARR'S`** principal sign and likely pool-related lower wording. Combined with the independent City inventory (`S-036` / `E-033`) naming **Farr's Pool Hall at 505 Main**, this strongly supports Farr's operating at 505 in the 1936 photographed state.

Do not treat this as proof that Farr's opened in 1934 or 1936, as a property-ownership record, or as proof of uninterrupted continuity from the 1925 unnamed billiards/cigars use. The exact Farr-to-Harr transition remains open.''')

# Revise the existing Farr row in the 505-specific timeline rather than leaving the new anchor detached.
t505 = rd("timelines/505-main.md")
old = "| Date unresolved; 1934 residence context | Edwin and Alice Farr identified as proprietors of **Farr's Pool Hall at 505**; their residence was acquired in 1934. | High official secondary for business/address association; 1934 is **not** a business opening date. | `BUS-013`; `P-028`, `P-029`; `E-033`; `S-036` |"
new = f"| By 1936 photographic state; 1934 residence context | Edwin and Alice Farr are identified by the City as proprietors of **Farr's Pool Hall at 505**. CCHS `P-1128` is dated **1936**; steward storefront mapping plus probable **FARR'S** / likely pool-related signage strongly supports Farr's operating at 505 in the photographed state. | **STRONG CROSS-SOURCE INFERENCE** for Farr's at 505 in 1936; exact full sign text remains probable/partly unresolved. The 1934 residence acquisition is **not** a business opening date. | `BUS-013`; `P-028`, `P-029`; `E-033`, `{EID}`; `S-036`, `{SID}`; `{MID}`; `{TID}` |"
if old in t505:
    wr("timelines/505-main.md", t505.replace(old, new, 1))
elif TARGET not in t505:
    append_once("timelines/505-main.md", "## 1936 P-1128 Farr photographic anchor", f'''## 1936 P-1128 Farr photographic anchor

CCHS `P-1128` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) provides a 1936 photographic state. Steward mapping plus probable `FARR'S` / likely pool-related signage, combined with `S-036` / `E-033`, strongly supports Farr's Pool Hall at 505 Main in 1936. Exact opening date and Farr-to-Harr transition remain unresolved.''')

append_once("timeline.md", f"## {TID} — 1936 — CCHS P-1128 strongly supports Farr's Pool Hall at 505", f'''## {TID} — 1936 — CCHS P-1128 strongly supports Farr's Pool Hall at 505

CCHS `P-1128` (`{SID}` / `{EID}` / `{MID}`) is cataloged **1936**. The project steward identifies the target storefront in the Fifth/Main row as **505 Main**. Enlarged review gives probable **FARR'S** signage and likely pool-related wording. Combined with independent `S-036` / `E-033`, which identifies Edwin and Alice Farr as proprietors of **Farr's Pool Hall at 505 Main**, this is a **STRONG CROSS-SOURCE INFERENCE** that Farr's was operating at 505 in the 1936 photographed state. It does not establish an opening date or resolve the later Farr-to-Harr transition.''')

append_once("evidence/open-questions.md", "### 5 September 2026 — P-1128 narrows Farr occupancy to a 1936 photographic state", f'''### 5 September 2026 — P-1128 narrows Farr occupancy to a 1936 photographic state

CCHS `P-1128` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) is dated **1936**. Steward mapping of 505 plus a probable `FARR'S` sign and likely pool-related wording, combined with `S-036` / `E-033`, strongly supports Farr's Pool Hall at 505 in 1936. The **opening date remains unresolved**, and the later transition from Farr to Harr remains open.''')

append_once("evidence/research-leads.md", "### 1936 P-1128 Farr anchor", f'''### 1936 P-1128 Farr anchor

`{SID}` / `{EID}` / `{MID}` / `{TID}` now provides a **1936** photographed-state anchor strongly supporting Farr's Pool Hall at 505 Main. This narrows the useful transition search: determine how far **before 1936** Farr can be documented at 505 and locate the first documentary appearance of **Harr's Recreation Center** before the existing 1945/1948 anchors. The exact opening and Farr→Harr transfer dates remain unresolved.''')

# Human-readable source/evidence records are canonical; synchronize YAML databases.
append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "CCHS P-1128 — Oregon City 1936, 5th and Main from the Bluff"
    url: "{HUB}"
    type: Primary historic photograph with CCHS institutional catalog metadata
    date: "1936"
    repository_file: "{IMAGE}"
    notes: "Project steward maps target storefront to 505 Main. Enlarged review gives probable FARR'S and likely pool-related wording; with S-036/E-033 this strongly supports Farr's Pool Hall at 505 in the 1936 photographed state. Exact sign text/opening date remain unresolved."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "1936 P-1128 photograph strongly supports Farr's Pool Hall at 505 Main"
    type: Primary photographic evidence with cross-source business/address identification
    date: "1936"
    claims:
      - "CCHS P-1128 is cataloged Oregon City 1936 - 5th and Main from the Bluff, Date made 1936."
      - "Project-steward mapping identifies the target storefront as 505 Main."
      - "Enlarged review gives PROBABLE FARR'S and likely POOL / POOL HALL wording, but not a secure full-sign transcription."
      - "With independent S-036 / E-033 identifying Farr's Pool Hall at 505 Main, the photograph strongly supports Farr's operating at 505 in the 1936 photographed state."
      - "Opening date, property ownership, proprietor physical presence, and Farr-to-Harr transition remain unresolved."
    confidence: "STRONG CROSS-SOURCE INFERENCE for Farr's at 505 in 1936; PROBABLE for exact sign transcription"
    related_sources:
      - {SID}
      - S-036
    related_businesses:
      - BUS-013
    related_buildings:
      - B-002''')

append_once("database/timeline.yml", f"  - id: {TID}", f'''  - id: {TID}
    date: "1936"
    title: "1936 — CCHS P-1128 strongly supports Farr's Pool Hall at 505"
    summary: "CCHS P-1128 is dated 1936. Steward storefront mapping plus probable FARR'S / likely pool-related signage, combined with S-036/E-033, strongly supports Farr's Pool Hall operating at 505 Main in the photographed state. Exact opening date/full sign text/Farr-to-Harr transition remain unresolved."
    confidence: "Strong cross-source inference"
    evidence:
      - {EID}
      - E-033
    sources:
      - {SID}
      - S-036
    related_businesses:
      - BUS-013
    related_buildings:
      - B-002''')

yaml_add_list_item("database/buildings.yml", "B-002", "related_evidence", EID)
yaml_add_list_item("database/buildings.yml", "B-002", "related_sources", SID)
yaml_add_list_item("database/businesses.yml", "BUS-013", "related_evidence", EID)
yaml_add_list_item("database/businesses.yml", "BUS-013", "related_sources", SID)

print(f"Integrated {TARGET}: {SID} / {EID} / {MID} / {TID}")
print(f"Repository image: {IMAGE} ({width}x{height}, {nbytes} bytes, sha256 {sha})")
