from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET = "P-5578"
ACCOUNT = "4813"
REVIEW = "2026-09-05"

STEWARD = {
    "filename": "Oregon City 1922 - Aerial View of West Linn and Oregon City.jpg",
    "width": 2048,
    "height": 1600,
    "bytes": 1197569,
    "sha256": "a3310bf8ad80041f7ef6b5a1998237aa10893373485668dc91b40e77d23c1b4c",
}
CATALOG = {
    "title": "Oregon City 1922 - Aerial View of West Linn and Oregon City",
    "entry_object_id": TARGET,
    "description": "Aerial View #2 of Willamette Falls, W. Linn and O.C. Companion Photos P-4776, P-5577, P-5578, P-5579, P-5580. 2014.002.027.002",
    "date_made": "1927",
    "medium": "Photographic Paper",
    "location_of_negative": "CCHS Halon Room",
    "other_number": "Gardner Photos 027_002",
}
SOURCE_NAME = "CCHS P-5578, Oregon City aerial view of West Linn and Oregon City, Date made 1927"
EVIDENCE_NAME = "P-5578 visually supports a probable two-story building mass at the steward-mapped historic 501 position in the cataloged 1927 state"

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
            if not isinstance(val, dict) or not val.get("path"):
                continue
            lk = key.lower()
            if "thumbnail" in lk or lk in {"complementary_color", "dominant_color"}:
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


def add_header_id(path, label, item):
    text = rd(path)
    lines = text.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if line.startswith(label):
            if f"`{item}`" not in line:
                lines[i] = line.rstrip() + f", `{item}`"
                changed = True
            break
    if changed:
        wr(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


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
HUB = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug else ENTRY
)

IMAGE = f"media/photos/aerials/{MID}_1927-west-linn-oregon-city-aerial-cchs-p5578.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = "evidence/source-captures/cchs-p5578-1927-west-linn-oregon-city-aerial-501-two-story-2026-09-05.md"
API = "evidence/source-captures/cchs-p5578-1927-west-linn-oregon-city-aerial-api-2026-09-05.json"

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
    "title_date_conflict": {
        "title_contains": "1922",
        "date_made_field": "1927",
        "archive_treatment": "Preserve both. Use Date made 1927 for chronology while retaining the exact institutional title and flagging the discrepancy."
    },
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS {TARGET} — aerial view of West Linn and Oregon City; catalog Date made 1927

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`. Related building: `B-005` (historic 501 Main).

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made: **1927**
- Medium: **Photographic Paper**
- Location of Negative: **CCHS Halon Room**
- Other No.: **Gardner Photos 027_002**
- Public record: {HUB}
- Public API: {ENTRY}

## Catalog title/date discrepancy

The institutional **title contains “1922”**, while the separate **Date made field is 1927**. Both are preserved exactly. For chronological placement, the archive uses the explicit Date made field **1927**, but flags the title/date discrepancy rather than silently normalizing it. This source should not be backdated to 1922 merely because of the title.

## Project-steward supplied image

- Original filename: `{STEWARD["filename"]}`
- Dimensions: **{STEWARD["width"]} × {STEWARD["height"]}**
- Bytes: **{STEWARD["bytes"]:,}**
- SHA-256: `{STEWARD["sha256"]}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from the exact `{TARGET}` object
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{"yes" if sha == STEWARD["sha256"] else "no"}**

The steward-upload fingerprint is retained even when the canonical repository derivative differs in encoding or dimensions.

## Direct visual review and 501 interpretation

The photograph is a broad aerial/elevated view across West Linn and Oregon City, with the Willamette River, bridge, downtown commercial blocks, bluff and residential grid visible.

At the project-steward mapped position of historic **501 Main**, the visible building mass **appears to be two stories tall**. The roof/wall height is more consistent with a two-story building than with a one-story storefront.

The photograph itself does **not** show a readable `501` number, so the exact address assignment depends on the established project spatial mapping rather than signage in this image. Classification for the statement “the historic 501 building is two stories in this photograph” is therefore **PROBABLE / WORKING HYPOTHESIS**, while the visual observation that the mapped corner mass appears two stories is **VISUALLY VERIFIED**.

## Relationship to the Gates 1922 rebuild

This is a stronger later-state structural control than year-only `P-5577` for one reason: CCHS's Date made field places `P-5578` in **1927**, after the July 1922 fire, the August 1922 Gates construction reports and the 1925 Sanborn.

`E-097` independently documents C. E. Gates erecting a **two-story hollow-tile** Fifth/Main fire-replacement building in August 1922. The two-story mass visible at the steward-mapped historic 501 position in this 1927 aerial is therefore **compatible with** the Gates replacement and strengthens the possibility that the later 501-area structure represents all or part of that rebuild.

It still does **not** prove that:
- the visible 1927 mass is exactly the Gates building;
- Gates's two ground-floor storerooms mapped to 501 alone or 501+503;
- the photographed two-story mass's party walls match later numbered boundaries; or
- the 1927 Date made field resolves the exact construction history of 503 or 505.

Those remain cross-source mapping questions.

## Companion-series relationship

The description identifies `P-5578` as **Aerial View #2** and names companions `P-4776`, `P-5577`, `P-5579`, and `P-5580`. `P-5577` is already archived as `S-241` / `E-215` / `IMG-0761` and carries a Date made field of **1922**.

Because `P-5578` carries a Date made field of **1927**, do **not** assume the companion-series photographs were all taken on the same flight or same date. The remaining companions should be checked individually for their own Date made fields and visual states.

## Evidence state

- **DOCUMENTED / DIRECT:** exact CCHS object identity, title wording, description, Date made **1927**, Gardner number, and companion list.
- **VISUALLY VERIFIED:** broad aerial geography and an apparently two-story building mass at the steward-mapped historic 501 position.
- **PROBABLE / WORKING HYPOTHESIS:** exact identification of that visible two-story mass as historic numbered 501 Main.
- **STRONG CROSS-SOURCE COMPATIBILITY:** the 1927 two-story mass is structurally compatible with the two-story Gates replacement reported in August 1922.
- **UNRESOLVED:** exact Gates-to-501/503 footprint; whether the title's “1922” is legacy wording or an error; exact structural relationship among 501, 503 and 505.

No absence in the photograph is treated as proof of vacancy, demolition or non-use.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic aerial photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`; Gardner Photos `027_002`; series wording `2014.002.027.002`.  
Institutional title: **{CATALOG["title"]}**.  
Date made field: **1927**; title/date discrepancy retained.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media/timeline/building: `{EID}` / `{MID}` / `{TID}` / `B-005`.  
Notes: At the steward-mapped historic 501 position, the visible building mass appears two stories tall. Exact 501 numbering is not visible and remains a spatial mapping inference. The 1927 state is compatible with the two-story Gates replacement documented in 1922 but does not prove building identity.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Related building: `B-005`  
Type: Primary historic aerial photograph / structural and spatial evidence  
Claims:
- CCHS `{TARGET}` is titled **{CATALOG["title"]}**, while its separate Date made field is **1927**; both are preserved and the discrepancy remains explicit.
- Direct visual review shows an apparently **two-story** building mass at the project-steward mapped historic 501 position.
- No readable `501` number appears in the image, so the exact address assignment is **PROBABLE / WORKING HYPOTHESIS**, not direct numbered-address evidence.
- The 1927 two-story mass is structurally compatible with the two-story Gates Fifth/Main fire-replacement independently documented in August 1922 (`E-097`).
- This photograph does not resolve whether the Gates building mapped to later 501 alone, 501+503, or another room/footprint arrangement.
Classification: **DOCUMENTED / DIRECT** for CCHS metadata; **VISUALLY VERIFIED** for apparent two-story mass; **PROBABLE / WORKING HYPOTHESIS** for exact 501 assignment; **STRONG CROSS-SOURCE COMPATIBILITY** with the Gates two-story rebuild description.  
Confidence: **High** for visual story-height interpretation at the mapped position; exact numbered-address/building identity remains unresolved.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS {TARGET} 1927 aerial view of West Linn and Oregon City", f'''## {MID} — CCHS {TARGET} 1927 aerial view of West Linn and Oregon City
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- Related building: `B-005`
- CCHS object: **{TARGET}**
- CCHS title: **{CATALOG["title"]}**
- Date made: **1927**
- Title/date note: title contains `1922`; separate Date made field is `1927`. Preserve both; chronology uses Date made 1927 pending further catalog clarification.
- Description: **{CATALOG["description"]}**
- Medium: **Photographic Paper**; negative location **CCHS Halon Room**
- Other number: **Gardner Photos 027_002**
- Project-steward upload: `{STEWARD["filename"]}`; {STEWARD["width"]} × {STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Repository file: `{IMAGE}`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Status: `committed`
- Visual review: at the steward-mapped historic 501 position, the building mass appears **two stories tall**. No `501` number is readable, so exact address mapping remains probable rather than direct.
- Structural comparison: compatible with the two-story Gates Fifth/Main replacement reported in August 1922 (`E-097`); identity not proved.
''')

append_once("timeline.md", f"## 1927 — {TID}: P-5578 shows probable two-story mass at mapped historic 501 position", f'''## 1927 — {TID}: P-5578 shows probable two-story mass at mapped historic 501 position

CCHS `P-5578` (`{SID}` / `{EID}` / `{MID}`) has an institutional title containing **1922** but a separate **Date made field of 1927**. Both are preserved; this timeline uses the Date made field while flagging the discrepancy. In the steward-mapped historic 501 position, direct visual review shows a building mass that appears **two stories tall**. Because no `501` number is visible, exact address identity remains **PROBABLE / WORKING HYPOTHESIS**. The two-story 1927 state is compatible with the two-story Gates Fifth/Main replacement reported in August 1922 (`E-097`) but does not resolve whether that rebuild mapped to later 501 alone or 501+503.
''')

p = Path("database/timeline.yml")
s = p.read_text(encoding="utf-8")
if TID not in s:
    s = s.rstrip() + f'''

  - id: {TID}
    date: "1927"
    title: "1927 — P-5578 shows probable two-story mass at mapped historic 501 position"
    summary: "CCHS P-5578 has a title containing 1922 but Date made 1927. At the steward-mapped historic 501 position, the visible mass appears two stories tall; exact numbered identity is not directly readable."
    confidence: "High for visual story-height interpretation; probable for exact 501 mapping; Gates identity unresolved."
    related_sources: [{SID}]
    related_evidence: [{EID}]
    related_media: [{MID}]
    related_buildings: [B-005]
''' + "\n"
    p.write_text(s, encoding="utf-8")

p = Path("database/sources.yml")
s = p.read_text(encoding="utf-8")
if SID not in s:
    s = s.rstrip() + f'''

  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{HUB}"
    type: "Primary historic aerial photograph with CCHS institutional catalog metadata"
    date: "1927"
    repository_file: "{IMAGE}"
    notes: "Institutional title contains 1922 but Date made is 1927. At steward-mapped historic 501 position, visible mass appears two stories; exact 501 number is not readable."
    related_evidence: [{EID}]
    related_media: [{MID}]
    related_buildings: [B-005]
''' + "\n"
    p.write_text(s, encoding="utf-8")

p = Path("database/evidence.yml")
s = p.read_text(encoding="utf-8")
if EID not in s:
    s = s.rstrip() + f'''

  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: "Primary historic aerial photograph / structural and spatial evidence"
    date: "1927"
    claims:
      - "CCHS P-5578 title contains 1922 while the separate Date made field is 1927; both are preserved."
      - "At the project-steward mapped historic 501 position, the visible building mass appears two stories tall."
      - "No readable 501 number is present, so exact address identity remains probable rather than direct."
      - "The 1927 two-story mass is compatible with the two-story Gates Fifth/Main replacement documented in August 1922, but identity and exact 501/503 footprint remain unresolved."
    confidence: "High for visual two-story interpretation; probable for exact 501 mapping; unresolved for Gates identity and footprint."
    related_sources: [{SID}]
    related_media: [{MID}]
    related_buildings: [B-005]
    repository_file: "{CAP}"
''' + "\n"
    p.write_text(s, encoding="utf-8")

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / `{TID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / `{TID}` / CCHS `{TARGET}` | `B-005`; cross-check `S-241` / `E-215` / `IMG-0761` and `E-097` | CCHS title says 1922 but Date made says 1927. At the steward-mapped historic 501 position, the visible mass appears two stories tall; exact 501 number and Gates identity remain unresolved. |''')

append_once("registers/research-log.md", "CCHS P-5578 1927 aerial / probable two-story 501 mass", f'''### 2026-09-05 — CCHS P-5578 1927 aerial / probable two-story 501 mass
- Integrated project-steward supplied CCHS `{TARGET}` as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Preserved the institutional title **{CATALOG["title"]}** and the separate Date made field **1927** as an explicit catalog discrepancy rather than silently reconciling them.
- Preserved steward-upload fingerprint: `{STEWARD["filename"]}`, {STEWARD["width"]}×{STEWARD["height"]}, {STEWARD["bytes"]:,} bytes, SHA-256 `{STEWARD["sha256"]}`.
- At the steward-mapped historic 501 position, direct visual review shows an apparently **two-story** building mass. Exact `501` numbering is not readable, so address assignment remains **PROBABLE / WORKING HYPOTHESIS**.
- The 1927 two-story state is compatible with the two-story Gates Fifth/Main replacement independently reported in August 1922 (`E-097`) but does not prove identity or resolve the 501-versus-501+503 footprint model.
- `P-5578` is companion-series exposure #2; remaining `P-4776`, `P-5579`, and `P-5580` should be checked individually for their own Date made fields. Do not assume all companion images share a 1922 date.
- No annual closeout status changed.''')

append_once("evidence/research-leads.md", "P-5578 companion-series date/footprint follow-up", f'''### P-5578 companion-series date/footprint follow-up

CCHS `P-5578` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) is now reviewed. Its title contains **1922**, but its separate Date made field is **1927**, while already archived `P-5577` has Date made **1922**. Therefore the companion list must not be assumed to be one same-date flight. Retrieve `P-4776`, `P-5579`, and `P-5580` individually, record each Date made field, and compare the steward-mapped 501/503/505 footprint and story heights. Highest-value test: determine whether the apparent two-story 501-position mass persists consistently and whether any angle clarifies the Gates 501-alone versus 501+503 model.''')

add_header_id("buildings/501-main.md", "- Related evidence:", EID)
add_header_id("buildings/501-main.md", "- Related sources:", SID)

append_once("buildings/501-main.md", "### 1927 P-5578 aerial — probable two-story mass at mapped 501 position", f'''### 1927 P-5578 aerial — probable two-story mass at mapped 501 position

CCHS `P-5578` (`{SID}` / `{EID}` / `{MID}` / `{TID}`) is cataloged with a **Date made field of 1927**, despite an institutional title containing `1922`. At the project-steward mapped historic 501 position, the visible building mass appears **two stories tall**. The photograph does not show a readable `501`, so exact numbered identification is **PROBABLE / WORKING HYPOTHESIS**, not direct address evidence.

This is structurally compatible with the **two-story hollow-tile** Gates Fifth/Main replacement documented in August 1922 (`E-097`) and provides a useful post-1925 visual control. It does not prove that the visible 1927 mass is the Gates building or resolve whether Gates's two ground-floor storerooms became later 501 alone, 501+503, or another arrangement.''')

yaml_add_list_item("database/buildings.yml", "B-005", "related_evidence", EID)
yaml_add_list_item("database/buildings.yml", "B-005", "related_sources", SID)

p = Path("evidence/source-captures/cchs-p5577-1922-willamette-falls-oregon-city-aerial-2026-09-05.md")
s = p.read_text(encoding="utf-8")
marker = "## Companion P-5578 reviewed"
if marker not in s:
    s = s.rstrip() + f'''

## Companion P-5578 reviewed

Companion `P-5578` is now archived as `{SID}` / `{EID}` / `{MID}` / `{TID}`. Its institutional title also contains `1922`, but its separate Date made field is **1927**. This means the companion-series label alone cannot be used to assume all exposures were made in 1922 or on one flight. P-5578 also provides a clearer later-state observation that the building mass at the steward-mapped historic 501 position appears **two stories tall**.
''' + "\n"
    p.write_text(s, encoding="utf-8")

print(f"Integrated {TARGET} as {SID} / {EID} / {MID} / {TID}")
