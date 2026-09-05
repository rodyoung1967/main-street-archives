from pathlib import Path
import hashlib, json, re, urllib.request
from io import BytesIO
from PIL import Image

TARGET = 'P-4564'
ACCOUNT = '4813'
ENTRY_ID = '660be880-9b1f-11eb-b3ef-53e7205a00b4'
REVIEW = '2026-09-05'
STEWARD = {
    'filename': "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin Blvd.jpg",
    'width': 2048,
    'height': 1639,
    'bytes': 599969,
    'sha256': '45ac666a169bd62c7a689dee7bb01d1fdbae2862609bedb96be815e6b0b24880',
    'orientation': 'Camera at/near The Wheel on the northwest corner of 5th and Main, looking southeast across the intersection.',
}


def rd(p):
    return Path(p).read_text(encoding='utf-8')


def wr(p, s):
    q = Path(p)
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(s, encoding='utf-8')


def append_once(p, marker, block):
    s = rd(p)
    if marker in s:
        return
    wr(p, s.rstrip() + '\n\n' + block.rstrip() + '\n')


def maxid(p, prefix):
    vals = [int(x) for x in re.findall(rf'\b{re.escape(prefix)}-(\d+)\b', rd(p))]
    return max(vals)


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def get_bytes(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def catno(d):
    try:
        return d['properties']['hasCatalogNumber']['value_text']
    except Exception:
        return None


def prop(d, key):
    try:
        return d['properties'][key].get('value_text')
    except Exception:
        return None


def derivative(entry):
    found = []
    for m in entry.get('media', []):
        for k, v in m.get('derivatives', {}).items():
            if not isinstance(v, dict) or not v.get('path') or 'thumbnail' in k.lower():
                continue
            w = int(v.get('width') or 0)
            h = int(v.get('height') or 0)
            if w and h:
                found.append((w * h, w, h, k, v['path']))
    if not found:
        raise SystemExit(f'No public image derivative found for {TARGET}')
    found.sort(reverse=True)
    _, w, h, k, u = found[0]
    return {'key': k, 'width': w, 'height': h, 'url': u}


# Do not integrate the same institutional object twice.
for p in ['evidence/source-register.md', 'media/photo-metadata-register.md', 'indexes/id-crosswalk.md']:
    if TARGET in rd(p):
        print(f'{TARGET} already integrated; no changes needed.')
        raise SystemExit(0)

SID = f"S-{maxid('evidence/source-register.md', 'S') + 1:03d}"
EID = f"E-{maxid('evidence/evidence-register.md', 'E') + 1:03d}"
MID = f"IMG-{maxid('media/photo-metadata-register.md', 'IMG') + 1:04d}"
TID = f"T-{maxid('timeline.md', 'T') + 1:03d}"
bmax = maxid('businesses/business-index.md', 'BUS')
MOBIL = f'BUS-{bmax + 1:03d}'
HAGEN = f'BUS-{bmax + 2:03d}'

ENTRY = f'https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}'
entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit(f'Fetched catalog entry mismatch: expected {TARGET}, got {catno(entry)}')

der = derivative(entry)
data = get_bytes(der['url'])
if not data.startswith(b'\xff\xd8'):
    raise SystemExit('Selected P-4564 derivative is not JPEG')
im = Image.open(BytesIO(data))
w, h = im.size
sha = hashlib.sha256(data).hexdigest()
n = len(data)
slug = entry.get('slug') or 'oregon-city-1960s-street-scene-corner-of-main-and-mcloughlin-blvd'
HUB = f'https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}'

IMAGE = f'media/photos/main-street/{MID}_circa-mid-1960s-mobil-hagen-southeast-5th-main-cchs-p4564.jpg'
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = 'evidence/source-captures/cchs-p4564-mid-1960s-mobil-hagen-southeast-5th-main-2026-09-05.md'
API = 'evidence/source-captures/cchs-p4564-mid-1960s-mobil-hagen-southeast-5th-main-api-2026-09-05.json'
api = {
    'reviewed': REVIEW,
    'catalog': TARGET,
    'entry_url': ENTRY,
    'hub_url': HUB,
    'selected_derivative': der,
    'repository_file': IMAGE,
    'repository_image': {'width': w, 'height': h, 'bytes': n, 'sha256': sha},
    'steward_upload': STEWARD,
    'entry': entry,
}
wr(API, json.dumps(api, indent=2, ensure_ascii=False) + '\n')

TITLE = prop(entry, 'hasName') or "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin Blvd"
DESCRIPTION = prop(entry, 'hasDescription') or ''
SOURCE_NAME = 'CCHS P-4564 — circa-mid-1960s Mobil station and L. H. Hagen Agency at 5th/Main'
EVIDENCE_NAME = 'Circa-mid-1960s photograph documents southeast 5th/Main Mobil station and Hagen insurance agency'
TIMELINE_NAME = 'Circa mid-1960s — opposite-corner Mobil and Hagen scene from The Wheel corner'

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public catalog object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`; businesses `{MOBIL}` / `{HAGEN}`.

## Institutional catalog record

- Name/Title: **{TITLE}**
- Entry/Object ID: **{TARGET}**
- Description, preserved verbatim:

> {DESCRIPTION.replace(chr(10), chr(10) + '> ')}

- Exposure date: **circa mid-1960s** from the catalog description; no exact date is supplied.
- Public record: {HUB}
- Public API: {ENTRY}

The catalog writes **“Mobile Service Station.”** The photographed brand sign itself reads **Mobil**. The archive preserves the catalog wording verbatim while using **Mobil** for the visible petroleum brand; it does not silently normalize the institutional transcription.

## Project-steward supplied image

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact catalog object `{TARGET}`
- Dimensions: **{w} × {h}**
- Bytes: **{n:,}**
- SHA-256: `{sha}`

The source-backed CCHS derivative is retained as the canonical repository binary. The project-steward upload's exact filename, dimensions, byte count, and hash are preserved above so the supplied copy remains auditable even if the CCHS derivative differs in resolution or compression.

## Direct visual review

The photograph directly shows:

- a **Mobil** branded service station and forecourt occupying the prominent corner across the intersection;
- multiple fuel pumps beneath the station canopy and a tall Mobil pole sign;
- a freestanding price board reading **FREE** and **31 9**; the product/detail text between those elements is too small to promote as a historical claim here;
- an adjacent low commercial building with readable **The L. H. HAGEN Agency** and vertical **INSURANCE** signage;
- the rock bluff, traffic signal, roadway/track geometry, parked automobiles, and industrial structures behind the corner businesses.

The image does **not** show the 503 or 505 Main storefront facades. They are outside the frame behind or beside the camera position described below.

## Camera orientation supplied by project steward

The project steward identifies the camera as being at the **corner where The Wheel was located**, at/near **503 Main on the northwest corner of 5th and Main**, looking **southeast** across the intersection. On that orientation, the photographed Mobil station is on the **southeast corner of 5th and Main**, and The Wheel/503 is behind the camera.

This is retained as attributed project-steward spatial testimony. It is consistent with the separately established archive location of The Wheel at **503 Main** (`BUS-004` / `B-001`) and with the photographed opposite-corner geometry, but the photograph itself does not display a readable 503 street number or The Wheel sign. Therefore the orientation is not misrepresented as a CCHS catalog statement.

## Business identifications

- `{MOBIL}` — **Mobil Service Station (5th/Main context)**. The Mobil brand is visually direct. CCHS identifies a “Mobile Service Station.” Exact operator/legal entity and numbered street address remain unresolved.
- `{HAGEN}` — **The L. H. Hagen Agency**. The agency name and **INSURANCE** are visually readable and CCHS identifies “The L. H. Hagen Agency Insurance.” Exact numbered street address and proprietor identity are not established by this photo alone.
- CCHS also includes **Publishers** in the description. Industrial structures appear in the background, but this integration does not assign a specific background structure or legal entity from the photograph alone.

## Evidence classification

- **DOCUMENTED / DIRECT (photographic):** visible Mobil branding, service-station use, L. H. Hagen Agency/Insurance signage, and the photographed physical streetscape.
- **DOCUMENTED / DIRECT (institutional catalog):** CCHS object `{TARGET}` is described as circa mid-1960s and names a “Mobile Service Station,” “The L. H. Hagen Agency Insurance,” and “Publishers.”
- **DOCUMENTED / DIRECT (attributed steward testimony):** the project steward states that the camera was at the Wheel/503 corner looking southeast.
- **STRONG CROSS-SOURCE INFERENCE:** combining the steward orientation with the independently documented Wheel/503 corner location places the photographed Mobil station on the southeast corner opposite the target storefront row.
- **UNRESOLVED:** exact exposure date; exact numbered addresses; service-station operator/legal entity; Hagen proprietor identity; exact meaning of “Publishers” in the CCHS description.

## Research value

This photograph is primarily **intersection-orientation and opposite-corner context** for the 503/505 project. It should not be cited as a direct facade view of 503 or 505. Its strongest value is anchoring what stood across 5th/Main during the same broad mid-1960s period as CCHS `P-4565` (`IMG-0749`), which looks along the target Main Street business row.
'''
wr(CAP, capture)

append_once('evidence/source-register.md', f'## {SID} —', f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata and attributed project-steward camera-orientation testimony; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **circa mid-1960s** per CCHS description; exact exposure date unresolved.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related businesses: `{MOBIL}`, `{HAGEN}`, plus `BUS-004` only as camera-position context.
Notes: Image directly shows Mobil service-station branding and The L. H. Hagen Agency / Insurance signage. Project steward identifies the camera at/near The Wheel/503 northwest corner looking southeast; the target 503/505 facades are not visible.''')

append_once('evidence/evidence-register.md', f'## {EID} —', f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence with institutional catalog metadata and attributed project-steward spatial testimony
Claims:
- Visual review directly shows **Mobil** branding and a service-station forecourt, together with **The L. H. HAGEN Agency** and **INSURANCE** signage.
- CCHS `{TARGET}` describes the scene as circa mid-1960s and names a “Mobile Service Station,” “The L. H. Hagen Agency Insurance,” and “Publishers.”
- The project steward identifies the camera at/near The Wheel/503 northwest corner of 5th/Main looking southeast. Combined with independently established `BUS-004` / `B-001` location evidence, this strongly supports the Mobil station as the southeast-corner opposite-side context.
- The photograph does not depict the 503 or 505 storefront facades and does not establish exact numbered addresses for the station or Hagen agency.
Classification: **DOCUMENTED / DIRECT** for visible signs, photographed use, catalog wording, and the fact of the attributed steward statement; **STRONG CROSS-SOURCE INFERENCE** for the precise camera/opposite-corner spatial placement; exact exposure date and street numbers unresolved.
Confidence: **Very High** for P-4564 identity and visible Mobil/Hagen signage; **High** for the southeast-corner orientation when combined with steward testimony and established Wheel/503 location.
Related businesses: `{MOBIL}`, `{HAGEN}`, `BUS-004` (camera-position context only).
Related buildings: `B-001` (camera-position context only).''')

append_once('media/photo-metadata-register.md', f'## {MID} —', f'''## {MID} — CCHS P-4564, circa-mid-1960s Mobil/Hagen southeast-corner scene
- Type: Historic street-level intersection/commercial photograph
- Date: **circa mid-1960s** per CCHS catalog description; exact exposure date unresolved
- CCHS catalog: `{TARGET}`
- CCHS title: **{TITLE}**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {n:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD['filename']}`; {STEWARD['width']}×{STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Related businesses: `{MOBIL}` Mobil Service Station; `{HAGEN}` The L. H. Hagen Agency; `BUS-004` The Wheel only as camera-position context
- Orientation: project steward identifies camera at/near The Wheel/503 northwest corner of 5th/Main looking southeast; photographed Mobil station is opposite on southeast corner. The 503/505 facades are not visible.
- Visual findings: Mobil pole/canopy branding, fuel pumps, L. H. Hagen Agency and Insurance signage, bluff, traffic signal, roadway/track geometry and background industrial structures.''')

append_once('media/photos/inventory.md', f'### {MID} —', f'''### {MID} — Circa-mid-1960s Mobil/Hagen southeast-corner scene
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- CCHS: `{TARGET}`
- Key value: opposite-corner spatial context for 5th/Main; directly shows Mobil service station and L. H. Hagen Agency. Project steward places camera at/near The Wheel/503 looking southeast; 503/505 facades are not shown.''')

# Business records introduced by the photo.
append_once('businesses/business-index.md', f'| {MOBIL} |', f'''| {MOBIL} | [Mobil Service Station — 5th/Main context](mobil-service-station-5th-main.md) | Southeast corner of 5th/Main by steward orientation; exact number unresolved | CCHS `{TARGET}` says “Mobile Service Station”; photograph directly shows **Mobil** branding. Operator/legal entity unresolved. `{EID}`. |
| {HAGEN} | [The L. H. Hagen Agency](l-h-hagen-agency.md) | Adjacent to photographed Mobil station; exact number unresolved | CCHS `{TARGET}` names the agency; photograph directly reads **The L. H. HAGEN Agency** and **INSURANCE**. Proprietor identity unresolved. `{EID}`. |''')

wr('businesses/mobil-service-station-5th-main.md', f'''# Mobil Service Station — 5th/Main context

Business ID: `{MOBIL}`.

Address/status: **southeast corner of 5th/Main by project-steward camera orientation; exact historical street number unresolved**.

CCHS `{TARGET}` catalogs the circa-mid-1960s scene with the wording **“Mobile Service Station.”** The photograph itself directly shows the **Mobil** brand on the pole sign and station canopy, together with pumps and a service-station forecourt.

The project steward identifies the camera at/near The Wheel/503 northwest corner looking southeast, placing this station on the opposite southeast corner. That spatial placement is retained as attributed testimony plus cross-source inference, not as an exact numbered-address statement from CCHS.

Exact local operator, ownership, legal entity, numbered address, opening/closing dates, and relationship to earlier/later gas-station occupants remain unresolved.

Source/evidence/media: `{SID}` / `{EID}` / `{MID}`.
''')

wr('businesses/l-h-hagen-agency.md', f'''# The L. H. Hagen Agency

Business ID: `{HAGEN}`.

Address/status: **adjacent to the photographed Mobil station in the southeast 5th/Main corner context; exact historical street number unresolved**.

CCHS `{TARGET}` identifies **“The L. H. Hagen Agency Insurance.”** Visual review directly reads **The L. H. HAGEN Agency** and vertical **INSURANCE** signage on the low building to the right/east of the service station.

The photograph establishes the agency's presence in the CCHS-described circa-mid-1960s scene, but not its proprietor's full identity, exact street number, property ownership, or complete operating span.

Source/evidence/media: `{SID}` / `{EID}` / `{MID}`.
''')

append_once('timeline.md', f'## {TID} —', f'''## {TID} — {TIMELINE_NAME}

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows a **Mobil** service station and **The L. H. Hagen Agency / Insurance** in a scene cataloged **circa mid-1960s**. Project-steward orientation places the camera at/near The Wheel/503 northwest corner of 5th/Main looking southeast, making the station the opposite southeast-corner context. The target 503/505 facades are not visible, and exact opposite-side street numbers remain unresolved.''')

append_once('indexes/id-crosswalk.md', f'| `{MID}` CCHS `{TARGET}` |', f'''| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`, `{MOBIL}`, `{HAGEN}`, `BUS-004`, `B-001` | Circa-mid-1960s Mobil/Hagen opposite-corner scene. Mobil and Hagen signage direct; project steward places camera at/near The Wheel/503 looking southeast. `BUS-004` / `B-001` are camera-position context only; 503/505 facades are not depicted. |''')

append_once('registers/research-log.md', f'### 2026-09-05 — CCHS {TARGET}', f'''### 2026-09-05 — CCHS {TARGET} Mobil/Hagen southeast-corner photograph
- Integrated project-steward supplied image as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Exact CCHS object `{TARGET}` recovered and matched to the supplied title; catalog describes a circa-mid-1960s “Mobile Service Station,” “The L. H. Hagen Agency Insurance,” and “Publishers.”
- Direct visual review reads **Mobil**, **The L. H. HAGEN Agency**, and **INSURANCE**.
- Preserved steward orientation: camera at/near The Wheel/503 northwest corner of 5th/Main looking southeast. This is attributed testimony; the photograph itself does not show the 503/505 facades or an exact 503 street number.
- Added business records `{MOBIL}` and `{HAGEN}` with exact street numbers/operators left unresolved.''')

# Human-readable 503 building context, without claiming the facade is depicted.
append_once('buildings/503-main.md', f'## CCHS {TARGET} opposite-corner camera context', f'''## CCHS {TARGET} opposite-corner camera context

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), cataloged **circa mid-1960s**, does **not** show the 503 facade. The project steward identifies the camera as at/near The Wheel/503 northwest corner of 5th/Main looking southeast. On that attributed orientation, the photograph records the Mobil station and L. H. Hagen Agency across the intersection on the southeast side. Use this image as camera/orientation and opposite-corner context, not as direct architectural evidence for 503.''')

# YAML mirrors.
append_once('database/sources.yml', f'  - id: {SID}\n', f'''  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{CAP}"
    notes: "CCHS {TARGET}, circa mid-1960s; image directly shows Mobil service-station branding and L. H. Hagen Agency/Insurance. Steward camera orientation places the view from at/near The Wheel/503 looking southeast; 503/505 facades are not depicted."
    related_media: [{MID}]
    related_evidence: [{EID}]''')

append_once('database/evidence.yml', f'  - id: {EID}\n', f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: Primary photographic evidence with institutional catalog metadata and attributed project-steward spatial testimony
    classification: DOCUMENTED / DIRECT
    claims:
      - "Photograph directly shows Mobil branding, service-station use, The L. H. HAGEN Agency, and INSURANCE signage."
      - "CCHS {TARGET} describes the scene as circa mid-1960s and names a Mobile Service Station, The L. H. Hagen Agency Insurance, and Publishers."
      - "Project steward identifies the camera at/near The Wheel/503 northwest corner of 5th/Main looking southeast; combined with established Wheel/503 location evidence, this strongly supports the station as southeast-corner opposite-side context."
      - "The photograph does not depict the 503 or 505 storefront facades and does not establish exact opposite-side street numbers."
    confidence: "Very High for P-4564 identity and visible Mobil/Hagen signage; High for southeast-corner orientation with attributed steward testimony and established Wheel/503 location."
    related_sources: [{SID}]
    related_businesses: [{MOBIL}, {HAGEN}, BUS-004]
    related_buildings: [B-001]
    related_media: [{MID}]
    repository_file: {CAP}''')

append_once('database/timeline.yml', f'  - id: {TID}\n', f'''  - id: {TID}
    date: "circa mid-1960s"
    title: "{TIMELINE_NAME}"
    summary: "CCHS {TARGET} directly shows Mobil service-station and L. H. Hagen Agency signage. Project steward places the camera at/near The Wheel/503 northwest corner looking southeast; target 503/505 facades are not visible."
    confidence: "Very High for visible scene; High for attributed camera orientation; exact exposure date and street numbers unresolved."
    related_sources: [{SID}]
    related_evidence: [{EID}]
    related_businesses: [{MOBIL}, {HAGEN}, BUS-004]
    related_buildings: [B-001]''')

append_once('database/businesses.yml', f'  - id: {MOBIL}\n', f'''  - id: {MOBIL}
    name: "Mobil Service Station — 5th/Main context"
    repository_file: businesses/mobil-service-station-5th-main.md
    address: "Southeast corner of 5th/Main by steward orientation; exact number unresolved"
    status: "Documented in CCHS {TARGET} circa-mid-1960s photograph; exact operator/legal entity and operating span unresolved"
    related_evidence: [{EID}]
    related_sources: [{SID}]
    related_media: [{MID}]

  - id: {HAGEN}
    name: "The L. H. Hagen Agency"
    repository_file: businesses/l-h-hagen-agency.md
    address: "Adjacent to photographed Mobil station; exact number unresolved"
    status: "Documented in CCHS {TARGET} circa-mid-1960s photograph; proprietor identity and operating span unresolved"
    related_evidence: [{EID}]
    related_sources: [{SID}]
    related_media: [{MID}]''')

print(f'Integrated {TARGET}: {SID} / {EID} / {MID} / {TID} / {MOBIL} / {HAGEN}')
print(f'Repository image: {IMAGE} ({w}x{h}, {n} bytes, sha256 {sha})')
