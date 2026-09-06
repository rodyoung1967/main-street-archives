from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1798"
ACCOUNT = "4813"
REVIEW = "2026-09-05"
STEWARD = {
    "filename": "Oregon City Labor Day Parade 1902 - 5th and Main.jpg",
    "width": 850,
    "height": 669,
    "bytes": 81519,
    "sha256": "c2ba7159afc46bac160511ab0c6d77f1603056a03b858229b503a5152d1bb514",
}
CATALOG = {
    "title": "Oregon City Labor Day Parade 1902 - 5th and Main",
    "description": "Oregon City Labor Day Parade, 1902.  5th & Main. 1st September 1902.",
    "date_made": "1902",
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
            if m is not None: return m
    elif isinstance(obj, list):
        for v in obj:
            m = find_match(v)
            if m is not None: return m
    return None


def choose_derivative(entry):
    found = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path") or "thumbnail" in key.lower():
                continue
            w = int(val.get("width") or 0); h = int(val.get("height") or 0)
            if w and h: found.append((w*h, w, h, key, val["path"]))
    if not found: raise SystemExit("No public image derivative found")
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
if match is None: raise SystemExit(f"Exact CCHS object {TARGET} not returned")
entry_id = match.get("id")
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{entry_id}"
entry = get_json(ENTRY)
if catno(entry) != TARGET: raise SystemExit("Catalog mismatch")
der = choose_derivative(entry)
data = get_bytes(der["url"])
if not data.startswith(b"\xff\xd8"): raise SystemExit("Selected derivative is not JPEG")
with Image.open(BytesIO(data)) as im:
    w, h = im.size
nbytes = len(data); sha = hashlib.sha256(data).hexdigest()
slug = entry.get("slug") or match.get("slug")
HUB = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}" if slug else ENTRY
IMAGE = f"media/photos/early-main-street/{MID}_1902-09-01-labor-day-parade-5th-main-cchs-p1798.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True); Path(IMAGE).write_bytes(data)
CAP = "evidence/source-captures/cchs-p1798-1902-09-01-labor-day-parade-5th-main-signs-2026-09-05.md"
API = "evidence/source-captures/cchs-p1798-1902-labor-day-parade-api-2026-09-05.json"
wr(API, json.dumps({"reviewed": REVIEW, "catalog": TARGET, "search_url": SEARCH_URL, "entry_url": ENTRY, "hub_url": HUB, "selected_derivative": der, "repository_file": IMAGE, "repository_image": {"width": w, "height": h, "bytes": nbytes, "sha256": sha}, "steward_upload": STEWARD, "catalog_metadata_supplied_by_steward": CATALOG, "entry": entry}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS P-1798 — Labor Day parade at Fifth & Main, 1 September 1902

Reviewed **5 September 2026** from the project-steward supplied photograph and exact CCHS object `P-1798`.

Archive IDs: `{SID}` / `{EID}` / `{MID}`.

## Catalog metadata
- Title: **Oregon City Labor Day Parade 1902 - 5th and Main**
- Entry/Object ID: **P-1798**
- Description: **Oregon City Labor Day Parade, 1902. 5th & Main. 1st September 1902.**
- Date made: **1902**; description supplies **1 September 1902**.
- Place: Oregon City, Clackamas County, Oregon
- Medium: **Photographic Paper**
- Location of Negative: **Halon**
- Public record: {HUB}

## Steward upload
- Filename: `{STEWARD['filename']}`
- Dimensions: **850 × 669**
- Bytes: **81,519**
- SHA-256: `{STEWARD['sha256']}`

## Repository image
- File: `{IMAGE}`
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

## Direct sign review
Enlarged visual review supports these readings:
- **RINGLING BROS.** — clear large wall advertising.
- **WORLD'S GREATEST SHOWS** — readable beneath the Ringling name; this is circus advertising, not the occupant name.
- **GENERAL ARTHUR CIGAR** — clear advertising panel on the adjoining/nearby wall; treat as product advertising, not a business identification.
- Upper-left background signage appears to include **DRUGS** and **CHARMAN & CO**; retain as contextual/probable background reading rather than target-store identification.
- A background sign includes a readable **STEAM LAUNDRY** phrase, but the full business name is not secure from this frame.
- At the right edge, **FURNITU...** is visible, consistent with a furniture sign, but the complete wording/business is not secure.

The very pale/faded lettering on the center target-area wall was tested at multiple enlargements/contrast treatments. It remains **UNRESOLVED**. No business name should be assigned from those strokes. In particular, the archive already knows from `E-146` that The Union Store advertised on Main between Fifth and Sixth in November 1902, but this photograph does **not** visually establish that the faded center lettering says Union Store or that the pictured premises was that business.

## Structural observation
The target-area commercial mass in this 1902 view presents as a **low one-story / tall-false-front type commercial form**: no secure second-floor window row is visible and the roof/storefront relationship reads substantially lower than the clearly multi-story buildings behind it. Classification: **PROBABLE / WORKING HYPOTHESIS** for one-story construction, because a tall false front and the oblique view limit exact story-count proof.

This matters because `E-097` independently documents Gates erecting a **new two-story hollow-tile** Fifth/Main fire-replacement in August 1922, and `E-216` later shows an apparently two-story mass at the steward-mapped historic 501 position in the cataloged 1927 state. Together, the photographs support a meaningful **pre-1922 low-profile versus post-1922 two-story contrast**.

They do **not** prove that the particular low 1902 building survived unchanged until the July 1922 fire. Twenty years of possible construction/alteration remain unbridged, and exact later 501/503/505 boundaries cannot be back-projected from this photograph alone.

## Evidence state
- **DOCUMENTED / DIRECT:** CCHS object/date/location metadata; visible parade and Fifth/Main streetscape; Ringling Bros. and General Arthur advertising.
- **VISUALLY VERIFIED:** low-profile target-area building form and advertising panels.
- **PROBABLE / WORKING HYPOTHESIS:** target-area commercial building is one story or a one-story structure with tall false front.
- **UNRESOLVED:** pale center-wall text; exact 1902 occupant; exact mapping to later 501/503/505; continuity of the 1902 structure to the July 1922 fire.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — CCHS P-1798", f'''## {SID} — CCHS P-1798, Labor Day parade at Fifth & Main, 1 September 1902
Type: Primary historic photograph with CCHS catalog metadata; **VISUALLY VERIFIED** 5 September 2026.  
Catalog ID: `P-1798`.  
Date: **1 September 1902** from CCHS description.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media: `{EID}` / `{MID}`.  
Notes: Ringling Bros. / World's Greatest Shows and General Arthur cigar advertising are readable. Pale center-wall lettering remains unresolved. Target-area structure presents as a probable low one-story/tall-false-front form; exact later 501/503/505 mapping and continuity to 1922 remain unproved.''')

append_once("evidence/evidence-register.md", f"## {EID} — 1902 Fifth/Main", f'''## {EID} — 1902 Fifth/Main photograph shows a low-profile predecessor-era commercial form and readable advertising, but no secure occupant name
Source: `{SID}`  
Media: `{MID}`  
Type: Primary photographic evidence  
Claims:
- CCHS `P-1798` describes the photograph as the Oregon City Labor Day Parade at Fifth & Main on **1 September 1902**.
- `RINGLING BROS.` and `WORLD'S GREATEST SHOWS` are readable as wall advertising; `GENERAL ARTHUR CIGAR` is also readable advertising.
- The center target-area building presents visually as a low one-story / tall-false-front commercial form; story count is **PROBABLE / WORKING HYPOTHESIS**, not architectural proof.
- The pale center-wall lettering is not secure enough to transcribe and is not assigned to The Union Store or any other occupant.
- Compared with `E-097`'s documented two-story Gates replacement and `E-216`'s probable two-story 1927 501-area mass, this image supplies a useful earlier structural contrast, but does not prove continuity from 1902 to the July 1922 fire.
Classification: **DOCUMENTED / DIRECT** for photograph identity/date and readable advertising; **PROBABLE / WORKING HYPOTHESIS** for one-story form; **UNRESOLVED** for occupant, faded lettering, exact later address mapping, and 1902-to-1922 building continuity.  
Confidence: Very High for catalog/date and clear advertising; Moderate for one-story interpretation; unresolved for occupant/address continuity.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS P-1798", f'''## {MID} — CCHS P-1798 Labor Day parade, Fifth & Main, 1 September 1902
- Type: Historic street/parade photograph
- CCHS object: **P-1798**
- CCHS title: **Oregon City Labor Day Parade 1902 - 5th and Main**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD['filename']}`; 850×669; 81,519 bytes; SHA-256 `{STEWARD['sha256']}`
- Visual note: Ringling Bros./World's Greatest Shows and General Arthur cigar advertising readable; faded center-wall business lettering unresolved; target-area structure appears low/likely one-story or tall-false-front.
- Related source/evidence: `{SID}` / `{EID}`''')

append_once("media/photos/inventory.md", f"### {MID} — CCHS P-1798", f'''### {MID} — CCHS P-1798 Labor Day parade at Fifth & Main, 1902
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- CCHS object: `P-1798`
- Date: **1 September 1902** from catalog description
- Status: committed; readable advertising recorded; pale target-wall lettering, exact occupant, exact later address mapping and building continuity remain unresolved.''')

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `P-1798`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `P-1798` | `{IMAGE}`; `{CAP}` | 1 Sep. 1902 Fifth/Main Labor Day parade. Readable Ringling Bros./General Arthur advertising; low-profile target-area form is a probable one-story/tall-false-front predecessor state. Faded occupant lettering and later 501/503/505 mapping unresolved. |''')

append_once("evidence/open-questions.md", "### 5 September 2026 — P-1798 visual update to OQ-033", f'''### 5 September 2026 — P-1798 visual update to OQ-033
CCHS `P-1798` (`{SID}` / `{EID}` / `{MID}`) adds a precisely described **1 September 1902 Fifth/Main** photograph. It gives a low-profile probable one-story/tall-false-front structural state in the target zone, but its pale business lettering remains unreadable and no exact later 501/503/505 mapping follows. Existing `E-146` Union Store block-level evidence remains a separate candidate and is not visually assigned to the photograph.''')

append_once("registers/research-log.md", "CCHS P-1798 Labor Day parade", f'''### 2026-09-05 — CCHS P-1798 Labor Day parade / Fifth-Main sign review
- Integrated steward-supplied CCHS `P-1798` as `{MID}` / `{SID}` / `{EID}`.
- Preserved steward fingerprint: `{STEWARD['filename']}`, 850×669, 81,519 bytes, SHA-256 `{STEWARD['sha256']}`.
- Readable advertising: **Ringling Bros. / World's Greatest Shows** and **General Arthur Cigar**. Background Charman/drug and steam-laundry wording is contextual only.
- Multiple enlargement/contrast passes did not produce a defensible transcription of the pale center-wall lettering; it is not assigned to The Union Store or another occupant.
- Recorded the target-area building as a **probable** low one-story/tall-false-front form. This supplies a pre-1922 structural contrast with `E-097`/`E-216`, not proof that the same building survived to the July 1922 fire.
- No year-level research status changed.''')

append_once("database/sources.yml", f"  - id: {SID}", f'''  - id: {SID}
    name: "CCHS P-1798 — Labor Day parade at Fifth and Main, 1 September 1902"
    url: "{HUB}"
    type: Primary historic photograph with CCHS institutional catalog metadata
    date: "1902-09-01"
    repository_file: "{IMAGE}"
    notes: "Readable Ringling Bros. and General Arthur advertising; faded occupant lettering and exact later address mapping unresolved."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}", f'''  - id: {EID}
    name: "1902 Fifth/Main photograph shows low-profile predecessor-era commercial form and readable advertising"
    type: Primary photographic evidence
    date: "1902-09-01"
    claims:
      - "CCHS P-1798 describes the scene as the Oregon City Labor Day Parade at Fifth and Main on 1 September 1902."
      - "Ringling Bros. / World's Greatest Shows and General Arthur cigar advertising are readable."
      - "The target-area structure presents as a probable low one-story or tall-false-front commercial form."
      - "Pale center-wall lettering, exact occupant, later 501/503/505 mapping, and continuity to the July 1922 fire remain unresolved."
    confidence: "Very High for date/object/readable advertising; Moderate for one-story interpretation; unresolved for occupant/address/building continuity."
    related_sources: [{SID}]
    related_media: [{MID}]
    related_buildings: [B-005, B-001, B-002]
    repository_file: "{IMAGE}"''')

print(f"Integrated {TARGET} as {MID} / {SID} / {EID}")
