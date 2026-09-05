from pathlib import Path
import hashlib, json, re, urllib.request
from io import BytesIO
from PIL import Image

TARGET = 'P-4563'
ACCOUNT = '4813'
ENTRY_ID = 'd6ad7c50-ba05-11ed-a262-e7d6d6f41c49'
REVIEW = '2026-09-05'
STEWARD = {
    'filename': "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin - Mid 1960's(1).jpg",
    'width': 2048,
    'height': 1627,
    'bytes': 495209,
    'sha256': '55786b2024ad8186289859095b3d132ad27b742155d1c7ddf98ee03c68d78fa6',
    'location_note': 'The photographed storefront group is the northeast corner of 5th and Main.',
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


for p in ['evidence/source-register.md', 'media/photo-metadata-register.md', 'indexes/id-crosswalk.md']:
    if TARGET in rd(p):
        print(f'{TARGET} already integrated; no changes needed.')
        raise SystemExit(0)

SID = f"S-{maxid('evidence/source-register.md', 'S') + 1:03d}"
EID = f"E-{maxid('evidence/evidence-register.md', 'E') + 1:03d}"
MID = f"IMG-{maxid('media/photo-metadata-register.md', 'IMG') + 1:04d}"
TID = f"T-{maxid('timeline.md', 'T') + 1:03d}"
bmax = maxid('businesses/business-index.md', 'BUS')
CLEANERS = f'BUS-{bmax + 1:03d}'
OUTDOOR = f'BUS-{bmax + 2:03d}'

ENTRY = f'https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}'
entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit(f'Fetched catalog entry mismatch: expected {TARGET}, got {catno(entry)}')

der = derivative(entry)
data = get_bytes(der['url'])
if not data.startswith(b'\xff\xd8'):
    raise SystemExit('Selected P-4563 derivative is not JPEG')
im = Image.open(BytesIO(data))
w, h = im.size
sha = hashlib.sha256(data).hexdigest()
n = len(data)
slug = entry.get('slug') or 'oregon-city-1960s-street-scene-corner-of-main-and-mcloughlin-mid-1960s-1'
HUB = f'https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}'

IMAGE = f'media/photos/main-street/{MID}_circa-mid-1960s-northeast-5th-main-american-cleaners-outdoor-store-cchs-p4563.jpg'
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = 'evidence/source-captures/cchs-p4563-mid-1960s-northeast-5th-main-american-cleaners-outdoor-store-2026-09-05.md'
API = 'evidence/source-captures/cchs-p4563-mid-1960s-northeast-5th-main-american-cleaners-outdoor-store-api-2026-09-05.json'
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

TITLE = prop(entry, 'hasName') or "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin - Mid 1960's"
DESCRIPTION = prop(entry, 'hasDescription') or ''
SOURCE_NAME = 'CCHS P-4563 — circa-mid-1960s northeast 5th/Main American Cleaners and Outdoor Store scene'
EVIDENCE_NAME = 'Circa-mid-1960s photograph documents the northeast 5th/Main commercial corner'
TIMELINE_NAME = 'Circa mid-1960s — northeast 5th/Main American Cleaners and Outdoor Store corner'

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public catalog object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`; businesses `{CLEANERS}` / `{OUTDOOR}`.

## Institutional catalog record

- Name/Title: **{TITLE}**
- Entry/Object ID: **{TARGET}**
- Description, preserved verbatim:

> {DESCRIPTION.replace(chr(10), chr(10) + '> ')}

- Exposure date: **circa mid-1960s** from the catalog description; no exact date is supplied.
- Public record: {HUB}
- Public API: {ENTRY}

## Project-steward supplied image

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`
- Steward spatial note: **{STEWARD['location_note']}**

The supplied image and the CCHS derivative are the same institutional photograph/object. The source-backed CCHS derivative is retained as the canonical repository binary; the exact supplied-file metadata above preserves the steward copy for audit.

## Repository image

- File: `{IMAGE}`
- Source: largest public CCHS derivative recovered from exact catalog object `{TARGET}`
- Dimensions: **{w} × {h}**
- Bytes: **{n:,}**
- SHA-256: `{sha}`

## Direct visual review

The photograph directly shows the commercial storefront group at the intersection, including:

- **AMERICAN CLEANERS** on the corner storefront;
- a large **OUTDOOR STORE** sign, with smaller lettering that appears to read **A & K** above it;
- an adjacent **SPORTING GOODS** sign with smaller category words including **CAMPING**, **HUNTING**, and **FISHING**;
- the **MAIN** and **5th ST** street blades at the intersection;
- mid-century automobiles, traffic signals, curb/fire-hydrant details, roadway/track geometry, and the bluff rising behind the buildings.

The exact relationship between the **SPORTING GOODS** frontage and the catalog-identified **Outdoor Store** is not promoted beyond the visual adjacency without an independent directory or advertisement.

## Northeast-corner identification

The project steward identifies the photographed storefront group as the **northeast corner of 5th and Main**. CCHS independently describes the image as the corner of Main and McLoughlin and explicitly adds **“(5th and Main Street)”** in the catalog description. The northeast-quadrant assignment is retained as attributed project-steward spatial testimony; the photograph itself visibly confirms the 5th/Main intersection but does not print “northeast.”

This photograph does **not** show the 503 or 505 Main storefront facades. Its project value is neighboring-corner and intersection-control context.

## Business identifications

- `{CLEANERS}` — **American Cleaners**. Business name is directly readable and CCHS names American Cleaners. Exact numbered street address and operator/legal entity remain unresolved.
- `{OUTDOOR}` — **A & K Outdoor Store / Outdoor Store**. **OUTDOOR STORE** is directly readable; CCHS names “Outdoor Store.” The smaller **A & K** lettering is visually apparent but should be checked against a directory or advertisement before treating the punctuation/legal trade name as final. Exact numbered street address and proprietor remain unresolved.

## Evidence classification

- **DOCUMENTED / DIRECT (photographic):** American Cleaners, Outdoor Store, Sporting Goods signage, 5th/Main street blades, and the physical streetscape.
- **DOCUMENTED / DIRECT (institutional catalog):** CCHS `{TARGET}` is circa mid-1960s and identifies **American Cleaners** and **Outdoor Store**, with the parenthetical **(5th and Main Street)**.
- **DOCUMENTED / DIRECT (attributed steward testimony):** the project steward identifies the photographed commercial corner as the **northeast corner of 5th and Main**.
- **UNRESOLVED:** exact exposure date; exact numbered street addresses; operators/legal entities; whether the adjacent Sporting Goods frontage was part of the same Outdoor Store business.

## Research value

Together with CCHS `P-4564` (`IMG-0751`) and `P-4565` (`IMG-0749`), this image materially improves mid-1960s intersection orientation around the 503/505 study area while remaining separate from direct evidence of the target storefront facades.
'''
wr(CAP, capture)

append_once('evidence/source-register.md', f'## {SID} —', f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS institutional catalog metadata and attributed project-steward quadrant identification; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **circa mid-1960s** per CCHS description; exact exposure date unresolved.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related businesses: `{CLEANERS}`, `{OUTDOOR}`.
Notes: CCHS names American Cleaners and Outdoor Store and specifies “(5th and Main Street).” Project steward identifies the photographed storefront group as the northeast corner of 5th/Main. Target 503/505 facades are not shown.''')

append_once('evidence/evidence-register.md', f'## {EID} —', f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence with institutional catalog metadata and attributed project-steward spatial testimony
Claims:
- Direct visual review reads **AMERICAN CLEANERS**, **OUTDOOR STORE**, **SPORTING GOODS**, **MAIN**, and **5th ST**.
- CCHS `{TARGET}` describes the scene as circa mid-1960s and names **American Cleaners** and **Outdoor Store**, with “(5th and Main Street)” in the description.
- Project steward identifies the photographed commercial group as the **northeast corner of 5th and Main**.
- The photograph is neighboring/intersection context and does not depict the 503/505 storefront facades.
Classification: **DOCUMENTED / DIRECT** for visible lettering, catalog wording, and the attributed steward statement; exact street numbers and business operators unresolved.
Confidence: **Very High** for P-4563 identity and visible/captured business names; **High** for northeast-quadrant placement based on steward testimony plus the visible/CCHS 5th/Main intersection identification.
Related businesses: `{CLEANERS}`, `{OUTDOOR}`.''')

append_once('media/photo-metadata-register.md', f'## {MID} —', f'''## {MID} — CCHS P-4563, circa-mid-1960s northeast 5th/Main commercial corner
- Type: Historic street-level intersection/commercial photograph
- Date: **circa mid-1960s** per CCHS catalog description; exact exposure date unresolved
- CCHS catalog: `{TARGET}`
- CCHS title: **{TITLE}**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {n:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD['filename']}`; {STEWARD['width']}×{STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Related businesses: `{CLEANERS}` American Cleaners; `{OUTDOOR}` A & K Outdoor Store / Outdoor Store
- Location: visible/CCHS 5th and Main intersection; project steward identifies pictured storefront group as the **northeast corner**.
- Visual findings: American Cleaners, Outdoor Store, Sporting Goods signage, Main/5th street blades, traffic signals, autos, roadway/track geometry and bluff.''')

append_once('media/photos/inventory.md', f'### {MID} —', f'''### {MID} — Circa-mid-1960s northeast 5th/Main American Cleaners / Outdoor Store
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- CCHS: `{TARGET}`
- Key value: documents the northeast 5th/Main neighboring corner, with American Cleaners and Outdoor Store directly/catalographically identified; target 503/505 facades are not shown.''')

append_once('businesses/business-index.md', f'| {CLEANERS} |', f'''| {CLEANERS} | [American Cleaners](american-cleaners.md) | Northeast corner of 5th/Main per project-steward spatial identification; exact number unresolved | CCHS `{TARGET}`, circa mid-1960s; name directly visible and cataloged. `{EID}`. |
| {OUTDOOR} | [A & K Outdoor Store / Outdoor Store](a-and-k-outdoor-store.md) | Northeast 5th/Main commercial group per project-steward identification; exact number unresolved | CCHS `{TARGET}`, circa mid-1960s; OUTDOOR STORE directly visible and catalog names Outdoor Store; smaller A & K lettering visually apparent but exact trade-name styling remains to corroborate. `{EID}`. |''')

wr('businesses/american-cleaners.md', f'''# American Cleaners

Business ID: `{CLEANERS}`.

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) catalogs **American Cleaners** in a circa-mid-1960s 5th/Main street scene, and the storefront sign **AMERICAN CLEANERS** is directly readable.

The project steward identifies the photographed storefront group as the **northeast corner of 5th and Main**. Exact numbered address, proprietor/legal entity, opening/closing dates, and building continuity remain unresolved.

Evidence state: **DOCUMENTED / DIRECT** for the photographed/cataloged business name; attributed steward testimony for northeast-corner placement.
''')

wr('businesses/a-and-k-outdoor-store.md', f'''# A & K Outdoor Store / Outdoor Store

Business ID: `{OUTDOOR}`.

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) catalogs an **Outdoor Store** in a circa-mid-1960s 5th/Main street scene. The photograph directly shows a large **OUTDOOR STORE** sign and smaller lettering that appears to read **A & K**. An adjacent **SPORTING GOODS** sign lists camping, hunting, and fishing.

The project steward identifies the photographed storefront group as the **northeast corner of 5th and Main**. Exact numbered address, proprietor/legal entity, the final punctuation/styling of the A & K name, and whether the adjacent Sporting Goods frontage was the same business remain unresolved.

Evidence state: **DOCUMENTED / DIRECT** for Outdoor Store and the visible signage; **UNRESOLVED** for exact legal/trade-name styling and storefront relationship.
''')

append_once('database/sources.yml', f'  - id: {SID}\n', f'''  - id: {SID}
    name: "CCHS P-4563 — circa-mid-1960s northeast 5th/Main American Cleaners and Outdoor Store scene"
    url: "{HUB}"
    repository_file: {CAP}
    notes: "Primary CCHS photograph; circa mid-1960s. CCHS names American Cleaners and Outdoor Store and specifies (5th and Main Street). Project steward identifies the pictured storefront group as the northeast corner."
''')

append_once('database/evidence.yml', f'  - id: {EID}\n', f'''  - id: {EID}
    name: "Circa-mid-1960s photograph documents northeast 5th/Main commercial corner"
    type: "Primary photographic evidence with institutional catalog metadata and attributed project-steward spatial testimony"
    claims:
      - "American Cleaners, Outdoor Store, Sporting Goods, Main and 5th St lettering are visible."
      - "CCHS P-4563 names American Cleaners and Outdoor Store and specifies (5th and Main Street)."
      - "Project steward identifies the photographed storefront group as the northeast corner of 5th and Main."
      - "The photograph does not show the 503/505 storefront facades."
    confidence: "Very High for catalog identity and visible signage; High for northeast-corner placement based on attributed steward testimony plus 5th/Main controls."
    related_sources: [{SID}]
    related_businesses: [{CLEANERS}, {OUTDOOR}]
    related_media: [{MID}]
    repository_file: {CAP}
''')

append_once('database/businesses.yml', f'  - id: {CLEANERS}\n', f'''  - id: {CLEANERS}
    name: American Cleaners
    repository_file: businesses/american-cleaners.md
    address: "Northeast corner of 5th/Main per steward identification; exact number unresolved"
    notes: "CCHS P-4563, circa mid-1960s; AMERICAN CLEANERS directly visible and cataloged."
    related_evidence: [{EID}]
    related_sources: [{SID}]
    related_media: [{MID}]

  - id: {OUTDOOR}
    name: "A & K Outdoor Store / Outdoor Store"
    repository_file: businesses/a-and-k-outdoor-store.md
    address: "Northeast 5th/Main commercial group per steward identification; exact number unresolved"
    notes: "OUTDOOR STORE directly visible and cataloged; smaller A & K lettering visually apparent; exact trade-name styling and Sporting Goods storefront relationship unresolved."
    related_evidence: [{EID}]
    related_sources: [{SID}]
    related_media: [{MID}]
''')

append_once('timeline.md', f'## {TID} —', f'''## {TID} — {TIMELINE_NAME}

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) documents **American Cleaners** and an **Outdoor Store** in a scene cataloged **circa mid-1960s** and explicitly described as **(5th and Main Street)**. The project steward identifies the pictured storefront group as the **northeast corner of 5th and Main**. The photograph supplies neighboring-corner/intersection context; it does not show the 503/505 facades.

Related businesses: `{CLEANERS}`, `{OUTDOOR}`.
''')

append_once('database/timeline.yml', f'  - id: {TID}\n', f'''  - id: {TID}
    date: "Circa mid-1960s"
    summary: "CCHS P-4563 documents American Cleaners and an Outdoor Store at the 5th/Main intersection; project steward identifies the pictured commercial group as the northeast corner. Target 503/505 facades are not shown."
    confidence: "Very High for P-4563/catalog and visible signs; High for northeast-quadrant placement from attributed steward testimony."
    related_sources: [{SID}]
    related_evidence: [{EID}]
    related_businesses: [{CLEANERS}, {OUTDOOR}]
''')

append_once('indexes/id-crosswalk.md', f'| `{MID}` CCHS `{TARGET}` |', f'''| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`, `{CLEANERS}`, `{OUTDOOR}` | Circa-mid-1960s northeast 5th/Main neighboring-corner scene; American Cleaners and Outdoor Store documented; target 503/505 facades not shown. |''')

append_once('registers/research-log.md', '### 2026-09-05 — CCHS P-4563 northeast 5th/Main photograph', f'''### 2026-09-05 — CCHS P-4563 northeast 5th/Main photograph
- Integrated project-steward supplied photograph as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Preserved exact CCHS metadata: title **{TITLE}**, object `{TARGET}`, and the catalog description naming **American Cleaners** and **Outdoor Store** with **(5th and Main Street)**.
- Direct visual review reads **AMERICAN CLEANERS**, **OUTDOOR STORE**, **SPORTING GOODS**, **MAIN**, and **5th ST**.
- Preserved steward spatial correction/identification: the photographed storefront group is the **northeast corner of 5th and Main**.
- Added business records `{CLEANERS}` American Cleaners and `{OUTDOOR}` A & K Outdoor Store / Outdoor Store without assigning unsupported street numbers or proprietors.
- The source-backed CCHS derivative is retained as the canonical binary; the exact supplied-file filename, dimensions, byte count and SHA-256 are preserved in the source capture/API record.
''')

print(f'Integrated {TARGET}: {SID} / {EID} / {MID} / {TID} / {CLEANERS} / {OUTDOOR}')
print(f'Repository image: {IMAGE} ({w}x{h}, {n} bytes, sha256 {sha})')
