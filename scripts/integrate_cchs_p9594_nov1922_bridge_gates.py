from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-9594"
ACCOUNT = "4813"
REVIEW = "2026-09-05"
SOURCE_NAME = "CCHS P-9594, Oregon City arch bridge and temporary bridge, November 1922"
EVIDENCE_NAME = "November 1922 photograph provides a probable visual of the Fifth/Main Gates fire-replacement building"

STEWARD = {
    "filename": "Oregon City 1922 - Arch Bridge and Temporary Bridge 1922 Oregon City.jpg",
    "width": 1909,
    "height": 851,
    "bytes": 311884,
    "sha256": "fe746669c983a2584104c68a00b2a26b25be6d6ccf71265828be2e12849d308d",
}
CATALOG = {
    "title": "Oregon City 1922 - Arch Bridge and Temporary Bridge 1922 Oregon City",
    "entry_object_id": TARGET,
    "description": "Arch Bridge Under Construction and Temporary Bridge, Oregon City, Nov. 1922 West Linn Inn in background.",
    "date_made": "1922",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_name": "2008.008.002.046",
    "other_number": "Gardner 46",
    "other_photo_number": "Meyers #39",
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
        wr(path, "\n".join(lines) + "\n")

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

IMAGE = f"media/photos/main-street/{MID}_1922-11-arch-temporary-bridge-fifth-main-cchs-p9594.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)
CAP = "evidence/source-captures/cchs-p9594-nov-1922-arch-temporary-bridge-fifth-main-2026-09-05.md"
API = "evidence/source-captures/cchs-p9594-nov-1922-arch-temporary-bridge-api-2026-09-05.json"

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

capture = f'''# CCHS {TARGET} — November 1922 arch/temporary-bridge view and Fifth/Main fire-replacement candidate

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`.

## Institutional catalog metadata supplied by project steward

- Name/Title: **{CATALOG["title"]}**
- Entry/Object ID: **{TARGET}**
- Description: **{CATALOG["description"]}**
- Date made field: **1922**
- Description-level month: **November 1922**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of Negative: **Society Collection**
- Other Name: **2008.008.002.046**
- Other No.: **Gardner 46**
- Other Photo #: **Meyers #39**
- Public record: {HUB}
- Public API: {ENTRY}

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
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

The exact steward-upload fingerprint is retained even when the repository derivative differs in encoding or dimensions.

## Direct visual review

The photograph is a broad bluff/elevated view across lower Oregon City. The temporary bridge and the new arch bridge under construction provide the dominant dated context. The Main Street commercial blocks are also visible. A conspicuously light-toned building mass appears at/near the Fifth/Main corner zone north of the historically documented Electric Hotel block.

The image alone does **not** print a readable `501`, `503`, or `505` number on that building and does not identify its owner or tenant.

## Cross-source relationship to the July–August 1922 fire/rebuild sequence

Existing primary newspaper evidence (`E-097`, sources `S-112` and `S-113`) establishes that by **17–18 August 1922** C. E. Gates was erecting a **two-story hollow-tile** replacement at Fifth/Main for the building formerly occupied by the Fifth Street Restaurant and destroyed in the July fire. The first floor was planned for **two storerooms**, one already leased to a barber, and occupancy was expected around **1 October**.

Because CCHS describes this photograph specifically as **November 1922**, the light-toned Fifth/Main corner building is temporally and spatially consistent with that newly completed Gates replacement. This is the strongest photographic candidate presently in the archive for a near-immediate post-construction view of the Gates building.

Classification: **STRONG CROSS-SOURCE INFERENCE**, not direct address proof.

## Critical mapping limit

This photograph does **not** establish that the July 1922 fire destroyed a building already proved to be modern-numbered **501 Main**, and it does **not** prove that the light-toned replacement is **501 alone**.

The exact modern-address footprint remains the same unresolved problem recorded in `E-097` and the 28 August model test:

- Gates's replacement may have mapped principally to later **501**;
- Gates's two ground-floor rooms may instead have corresponded to later **501 + 503**;
- changed entrances, room divisions or footprints between July 1922 and the 1925 Sanborn remain possible.

The photograph therefore strengthens the **visual chronology of the Gates rebuild** but does not select Model A or Model B and does not identify the Wolf-owned ignition room.

## Relationship to the 1925 Sanborn

The 1925 Sanborn later shows **501 store**, **503 restaurant**, and **505 billiards/cigars** as separate numbered occupancies. P-9594 now gives a dated November 1922 photographic state only a few months after the fire and Gates construction. A fixed-landmark/footprint alignment between this photograph, the 1925 Sanborn and later securely mapped photographs is now a high-value discriminator for whether the Gates building occupied later 501 alone or 501+503.

## Evidence state

- **DOCUMENTED / DIRECT:** CCHS object identity; 1922 Date made field; description specifically stating **Nov. 1922**; arch bridge under construction and temporary bridge context.
- **VISUALLY VERIFIED:** lower Oregon City commercial blocks and a light-toned building at/near the Fifth/Main candidate zone.
- **STRONG CROSS-SOURCE INFERENCE:** that this light-toned corner building is the newly completed Gates Fifth/Main fire-replacement described in August 1922.
- **UNRESOLVED:** exact mapping to 501 alone versus 501+503 or another arrangement; exact Wolf/Gates dividing line; ignition-room number; July pool-hall number.

No absence in the photograph is treated as proof of vacancy, demolition or non-use.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`; alternate object name `2008.008.002.046`; Gardner 46; Meyers #39.  
Date: **1922** Date made; description specifically says **Nov. 1922**.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media: `{EID}` / `{MID}`.  
Notes: Broad bridge/downtown view. A light-toned Fifth/Main corner building is a strong cross-source candidate for the Gates fire-replacement documented under `E-097`, but exact 501/503/505 mapping remains unresolved.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Type: Primary historic photograph plus cross-source structural inference  
Claims:
- CCHS `{TARGET}` catalogs the scene as **Oregon City 1922 - Arch Bridge and Temporary Bridge 1922 Oregon City** and its description specifically dates the view to **Nov. 1922**.
- Direct visual review shows the downtown commercial blocks and a conspicuously light-toned building at/near the Fifth/Main candidate zone.
- `E-097` independently proves Gates was constructing a two-story hollow-tile Fifth/Main fire-replacement in August 1922, with occupancy projected around October 1.
- The November timing and mapped corner context make the light-toned building a **strong cross-source candidate** for the newly completed Gates replacement.
- The image does **not** prove that the replacement equals modern 501 alone, that 501 specifically was the July fire-destroyed building, or that Gates's two ground-floor rooms became the later 501+503 pair.
Classification: **DOCUMENTED / DIRECT** for object/date/scene; **STRONG CROSS-SOURCE INFERENCE** for Gates-replacement identification; **UNRESOLVED** for exact modern-number footprint.  
Confidence: **Very High** for CCHS object/date metadata and broad scene; **High** for the Gates-replacement visual candidate; unresolved for 501-vs-501+503 mapping.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS P-9594", f'''## {MID} — CCHS P-9594, November 1922 arch/temporary bridge and Fifth/Main candidate
- Type: Historic elevated streetscape / bridge-construction photograph
- CCHS catalog: `{TARGET}`
- Other identifiers: `2008.008.002.046`; Gardner 46; Meyers #39
- CCHS title: **{CATALOG["title"]}**
- CCHS Date made: **1922**; description specifies **Nov. 1922**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD["filename"]}`; {STEWARD["width"]}×{STEWARD["height"]}; {STEWARD["bytes"]:,} bytes; SHA-256 `{STEWARD["sha256"]}`
- Visual note: light-toned Fifth/Main corner-zone building is a strong cross-source candidate for the newly completed Gates fire-replacement (`E-097`), not direct proof of 501 alone or 501+503.
- Related source/evidence: `{SID}` / `{EID}`''')

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `{IMAGE}`; `{CAP}` | November 1922 bridge/downtown photograph; strong cross-source candidate for the Gates Fifth/Main fire-replacement. Exact 501 vs. 501+503 footprint remains unresolved. |''')

append_once("registers/research-log.md", "CCHS P-9594 November 1922 bridge/Gates candidate", f'''### 2026-09-05 — CCHS P-9594 November 1922 bridge/Gates candidate
- Integrated project-steward supplied CCHS `{TARGET}` as `{MID}` / `{SID}` / `{EID}`.
- Preserved steward original fingerprint: `{STEWARD["filename"]}`, {STEWARD["width"]}×{STEWARD["height"]}, {STEWARD["bytes"]:,} bytes, SHA-256 `{STEWARD["sha256"]}`.
- CCHS description specifically dates the scene to **Nov. 1922**. Direct visual review identifies a light-toned building at/near the Fifth/Main corner candidate zone.
- Cross-source comparison with the August Gates construction reports (`E-097`) makes that building a **strong candidate for the newly completed Gates fire-replacement**.
- Preserved the critical limit: the archive has **not** proved that the July fire-destroyed restaurant building was modern-numbered 501, nor that the replacement equals 501 alone rather than 501+503 or another arrangement.
- This adds a high-value visual bridge but does not alter the 1922 annual status.''')

append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{HUB}"
    type: Primary historic photograph with CCHS institutional catalog metadata
    date: "November 1922"
    repository_file: "{IMAGE}"
    notes: "CCHS P-9594 bridge/downtown view. Light-toned Fifth/Main corner-zone building is a strong cross-source candidate for the Gates fire-replacement documented in E-097; exact 501/503/505 mapping remains unresolved."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: Primary historic photograph plus cross-source structural inference
    date: "November 1922"
    claims:
      - "CCHS P-9594 has a 1922 Date made field and a description specifically stating Nov. 1922."
      - "Direct visual review shows a light-toned building at/near the Fifth/Main candidate zone."
      - "E-097 independently proves Gates was constructing a two-story hollow-tile Fifth/Main fire-replacement in August 1922 with occupancy projected around October 1."
      - "The November timing and corner context make the photographed building a strong candidate for the newly completed Gates replacement."
      - "The photograph does not prove modern 501 alone, 501+503, or the numbered identity of the July fire-destroyed building."
    confidence: "Very High for CCHS object/date metadata and broad scene; High for the Gates-replacement visual candidate; unresolved for exact modern-number footprint."
    related_sources: [{SID}]
    related_media: [{MID}]
    related_buildings: [B-001, B-002, B-005]
    repository_file: "{CAP}"''')

# Add a photographic cross-check to the existing Gates evidence rather than replacing it.
append_once("evidence/E-097-1922-gates-fifth-main-fire-rebuild.md", "## November 1922 photographic cross-check — CCHS P-9594", f'''## November 1922 photographic cross-check — CCHS P-9594

New `{SID}` / `{EID}` / `{MID}` adds a CCHS photograph whose description specifically dates the scene to **November 1922**. A light-toned building is visible at/near the Fifth/Main candidate zone. Because the August reports above document Gates's two-story hollow-tile fire-replacement under construction with occupancy projected around 1 October, the November photograph is a **strong cross-source candidate for the newly completed Gates building**.

This strengthens the visual chronology but does **not** remove the mapping limit in this evidence record. The photograph does not prove that Gates's replacement was modern **501 alone**, that it was **501+503**, or that the July fire-destroyed restaurant building had already been proved as numbered 501. Fixed-landmark and footprint alignment against the 1925 Sanborn remains required.''')

building_note = f'''### November 1922 CCHS P-9594 visual bridge

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) is described by the institution as a **November 1922** view. A light-toned building appears at/near the Fifth/Main corner candidate zone. Cross-checking the photograph against the August 1922 Gates construction reports makes it a **strong candidate for the newly completed Gates fire-replacement**.

This does **not** prove the replacement was this numbered address. In particular, the archive still cannot choose between a Gates footprint principally at later 501 and a two-bay 501+503 arrangement. The photograph is a new visual bridge, not an exact-address determination.'''
for path in ("buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"):
    append_once(path, "### November 1922 CCHS P-9594 visual bridge", building_note)
    add_header_id(path, "- Related evidence:", EID)
    add_header_id(path, "- Related sources:", SID)

append_once("evidence/research-leads.md", "### 5 September 2026 — P-9594 November 1922 visual bridge", f'''### 5 September 2026 — P-9594 November 1922 visual bridge (`RL-010` / `RL-019` / 1922 Gates model)

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) supplies a description-dated **November 1922** photograph only months after the July fire and August Gates construction reports. The light-toned Fifth/Main candidate building is now the strongest photographic candidate for the newly completed Gates replacement. Next test: align P-9594 against the **1925 Sanborn Sheet 6** and securely mapped later street/aerial views using the Electric Hotel block, Fifth/Main crossing, bridge approach and surviving block edges. The goal is to test **501 alone vs. 501+503**, not to assume either model. Do not rewrite the July fire as a proved '501 burned' event unless an independent numbered-premises bridge is recovered.''')

for bid in ("B-001", "B-002", "B-005"):
    yaml_add_list_item("database/buildings.yml", bid, "related_evidence", EID)
    yaml_add_list_item("database/buildings.yml", bid, "related_sources", SID)

print(f"Integrated {TARGET}: {SID} {EID} {MID}")
