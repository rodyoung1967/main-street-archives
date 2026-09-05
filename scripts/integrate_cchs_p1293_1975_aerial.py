from pathlib import Path
import hashlib, json, re, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image

TARGET = 'P-1293'
ACCOUNT = '4813'
REVIEW = '2026-09-05'
STEWARD = {
    'filename': 'Oregon City 1981 - Aerial View.jpg',
    'width': 2009,
    'height': 2048,
    'bytes': 779338,
    'sha256': '7fcbdd1dc89b26d93498b6aa87af075b35965b3cb72de71a163198604e7a9912',
    'supplied_title': 'Oregon City 1981 - Aerial View',
    'catalog_date_supplied': '1975',
    'catalog_description_supplied': (
        'Aerial Views of Oregon City, 1975. A) Main Street and McLoughlin Avenue/5th Street. '
        'B) Willamette Falls. C) Museum Site Before Museum of the Oregon Territory was Built. '
        'Companion Photos - P-1293, P-4391, P-4392'
    ),
    'notes_supplied': 'Medium: Photographic Paper; Location of Negative: Halon',
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

def find(obj):
    if isinstance(obj, dict):
        if catno(obj) == TARGET:
            return obj
        for v in obj.values():
            z = find(v)
            if z is not None:
                return z
    elif isinstance(obj, list):
        for v in obj:
            z = find(v)
            if z is not None:
                return z
    return None

def derivative(entry):
    a = []
    for m in entry.get('media', []):
        for k, v in m.get('derivatives', {}).items():
            if not isinstance(v, dict) or not v.get('path') or 'thumbnail' in k.lower():
                continue
            w, h = int(v.get('width') or 0), int(v.get('height') or 0)
            if w and h:
                a.append((w * h, w, h, k, v['path']))
    if not a:
        raise SystemExit('No public image derivative found for CCHS P-1293')
    a.sort(reverse=True)
    _, w, h, k, u = a[0]
    return {'key': k, 'width': w, 'height': h, 'url': u}

# Duplicate guard: exact catalog object should only be integrated once.
for p in ['evidence/source-register.md', 'media/photo-metadata-register.md', 'indexes/id-crosswalk.md']:
    if TARGET in rd(p):
        print(f'{TARGET} already integrated; no changes needed.')
        raise SystemExit(0)

SID = f"S-{maxid('evidence/source-register.md', 'S') + 1:03d}"
EID = f"E-{maxid('evidence/evidence-register.md', 'E') + 1:03d}"
MID = f"IMG-{maxid('media/photo-metadata-register.md', 'IMG') + 1:04d}"
TID = f"T-{maxid('timeline.md', 'T') + 1:03d}"

SEARCH = 'https://api.catalogit.app/api/public/search?' + urllib.parse.urlencode({'query': TARGET, 'size': 50})
match = find(get_json(SEARCH))
if match is None:
    raise SystemExit('Exact CCHS P-1293 not returned by catalog search')
entry_id = match.get('id')
ENTRY = f'https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{entry_id}'
entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit('Fetched catalog entry mismatch for P-1293')

der = derivative(entry)
data = get_bytes(der['url'])
if not data.startswith(b'\xff\xd8'):
    raise SystemExit('Selected P-1293 derivative is not JPEG')
im = Image.open(BytesIO(data))
w, h = im.size
sha = hashlib.sha256(data).hexdigest()
n = len(data)
slug = entry.get('slug') or match.get('slug')
HUB = (
    f'https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}'
    if slug else ENTRY
)

IMAGE = f'media/photos/aerials/{MID}_1975-oregon-city-aerial-503-505-main-cchs-p1293.jpg'
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)

CAP = 'evidence/source-captures/1975-cchs-p1293-oregon-city-aerial-503-505-501-2026-09-05.md'
API = 'evidence/source-captures/1975-cchs-p1293-oregon-city-aerial-api-2026-09-05.json'
api = {
    'reviewed': REVIEW,
    'catalog': TARGET,
    'search_url': SEARCH,
    'entry_url': ENTRY,
    'hub_url': HUB,
    'selected_derivative': der,
    'repository_file': IMAGE,
    'repository_image': {'width': w, 'height': h, 'bytes': n, 'sha256': sha},
    'steward_upload': STEWARD,
    'entry': entry,
}
wr(API, json.dumps(api, indent=2, ensure_ascii=False) + '\n')

SOURCE_NAME = 'CCHS P-1293 — Oregon City aerial, cataloged 1975'
EVIDENCE_NAME = '1975 aerial confirms deeper 505 footprint than 503 and continued absence of 501'
TIMELINE_NAME = '1975 — aerial shows deeper 505 rear footprint and no 501 structure'

capture = f'''# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public catalog object recovered as `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`.

## Catalog metadata supplied by project steward

- Name/Title: **Oregon City 1981 - Aerial View**
- Entry/Object ID: **{TARGET}**
- Description: **{STEWARD['catalog_description_supplied']}**
- Made/Created — Date made: **1975**
- Place: Oregon City, Clackamas County, Oregon, United States
- Notes: **{STEWARD['notes_supplied']}**

### Date/title conflict preserved

The uploaded filename/title says **1981**, while the CCHS metadata supplied with the object says **Date made 1975** and the description begins **“Aerial Views of Oregon City, 1975.”** The archive therefore treats **1975 as the institutional catalog date** and preserves **1981 only as supplied title/filename wording**. No attempt is made to silently harmonize the two.

## Steward upload

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
- Public record: {HUB}
- Public API: {ENTRY}

The repository preserves the source-backed CCHS derivative as the canonical binary and records the project-steward upload's exact filename, dimensions, byte count, and hash above. They represent the same supplied/cataloged photograph; the steward file is therefore not separately duplicated in the repository.

## Direct visual review — target block

Using the already-established 5th/Main address mapping from the Sanborn and aerial series (`E-020`, `E-021`), the photograph provides a clear later-state roof/footprint comparison:

- **505 Main extends materially farther rearward/westward than 503 Main** in this aerial. This upgrades the former owner/field observation in `E-011` from an uncorroborated working note to an independently photographed later-state condition.
- The separate **501 Main corner structure is absent**. This is independent photographic corroboration of the prior aerial finding that 501 had already disappeared by **1944** (`E-021`); it does **not** move the established 1936–1944 removal bracket.
- The image does **not** establish when 505 acquired the greater rear depth. It therefore supports the existence of the asymmetry **by 1975**, but does not prove the `E-101` hypothesis that a rear addition/remodel occurred specifically around 1940.
- The image does not establish legal parcel boundaries, exact dimensions, construction ownership, or the cause/date of 501 removal.

## Effect on the 505 rear-expansion question

This photograph materially improves `RL-005` / `E-101` / `E-102` because it supplies a high-quality independent endpoint: **the deeper 505 footprint definitely existed by the CCHS-cataloged 1975 date**.

The next useful comparison is no longer “does 505 ever become deeper than 503?” but **when does that asymmetry first become visible?** Compare the existing photocompare frames in order — especially **1936, 1940, 1944, 1955, 1961, and 1974** — and then test the first visible change against assessor cards, permits, and physical material breaks.

## Evidence classification

- **DOCUMENTED / DIRECT (photographic):** in the mapped target block, the 505 footprint extends farther rearward than 503; the former 501 corner footprint is absent.
- **DOCUMENTED / DIRECT (institutional catalog):** CCHS object `{TARGET}` is cataloged with a 1975 date and 1975 aerial description.
- **STRONG CROSS-SOURCE CORROBORATION:** 501 remains absent long after the separately established 1936–1944 removal interval.
- **UNRESOLVED:** exact date and nature of the 505 rear-depth change; whether it explains the 1940 historic-resource date; precise legal/building-line dimensions; reason for 501 removal.

## Research consequence

Do **not** treat the 1975 image as proof of a 1940 addition. Use it as the later-state terminus for a frame-by-frame rear-edge chronology and as independent confirmation that the modern 505-vs-503 depth difference is historical rather than only a present-day observation.
'''
wr(CAP, capture)

append_once(
    'evidence/source-register.md',
    f'## {SID} —',
    f'''## {SID} — {SOURCE_NAME}
Type: Primary historic aerial photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society.
Catalog ID: `{TARGET}`.
Date: **1975** per supplied CCHS Date made field and description; uploaded title/filename says “1981” and is preserved as conflicting title wording.
Repository image: `{IMAGE}`.
Capture: `{CAP}`.
Public record: {HUB}
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Notes: Target-block review directly shows 505 extending farther rearward than 503 and confirms continued absence of the former 501 corner structure. It does not date the 505 rear-depth change or prove the 1940 addition hypothesis.'''
)

append_once(
    'evidence/evidence-register.md',
    f'## {EID} —',
    f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary aerial photographic evidence with institutional catalog metadata
Claims:
- In the established 5th/Main address mapping, the **505 Main footprint extends materially farther rearward/westward than 503 Main** in the CCHS-cataloged 1975 aerial.
- The former **501 Main** corner structure is absent, independently corroborating—but not narrowing—the existing `E-021` removal bracket of 1936–1944.
- The photograph establishes the 505/503 rear-depth asymmetry **by 1975** but does **not** establish when it first appeared and does not prove `E-101`'s proposed circa-1940 rear addition/remodel.
- The uploaded title/filename says 1981 while the supplied institutional metadata says 1975; 1975 is retained as the catalog date and the conflict is explicit.
Classification: **DOCUMENTED / DIRECT** for photographed later-state geometry and catalog date statement; **STRONG CROSS-SOURCE CORROBORATION** for continued 501 absence; change date remains unresolved.
Confidence: **High to Very High** for relative 505-vs-503 rear depth and 501 absence in the mapped block; no exact measurement or construction date inferred.
Related prior evidence: `E-011`, `E-021`, `E-101`, `E-102`.
Related buildings: `B-001`, `B-002`, `B-005`.'''
)

append_once(
    'media/photo-metadata-register.md',
    f'## {MID} —',
    f'''## {MID} — CCHS P-1293, Oregon City aerial cataloged 1975
- Type: Historic aerial photograph
- Institutional date: **1975** per supplied CCHS Date made field and description
- Supplied title/filename: **Oregon City 1981 - Aerial View** — title/date conflict preserved
- CCHS catalog: `{TARGET}`
- Related buildings: `B-001` (503), `B-002` (505), `B-005` (501 historic/removed)
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Repository file: `{IMAGE}`
- Repository dimensions: **{w} × {h}**; {n:,} bytes; SHA-256 `{sha}`
- Steward upload: `{STEWARD['filename']}`; {STEWARD['width']}×{STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Visual finding: in the established target-block mapping, **505 extends farther rearward than 503**, while the separate former **501** corner structure is absent.
- Interpretation limit: confirms the later-state geometry by 1975; does not date a 505 addition, prove a 1940 construction event, establish legal boundaries, or alter the already-established 1936–1944 501 removal bracket.
- Review: `{CAP}`'''
)

append_once(
    'media/photos/inventory.md',
    f'### {MID} —',
    f'''### {MID} — CCHS P-1293 Oregon City aerial, cataloged 1975
- File: `{IMAGE}`
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS: `{TARGET}`
- Key value: independent high-quality aerial confirmation that 505 is deeper rearward than 503 by 1975 and that 501 remains absent; supplied “1981” title conflicts with CCHS 1975 date metadata and is preserved as such.'''
)

append_once(
    'media/photos/aerials/README.md',
    '## Independent CCHS P-1293 aerial',
    f'''## Independent CCHS P-1293 aerial

`{MID}` is an **independent CCHS aerial cataloged 1975**, not a frame from the Oregon City photocompare screenshot series. It directly confirms a deeper rearward 505 footprint relative to 503 and continued absence of 501. See `{SID}` / `{EID}` and `{CAP}`. The supplied filename/title says 1981; CCHS metadata says 1975.'''
)

append_once(
    'evidence/aerial-5th-main-photocompare-series.md',
    '## Independent 1975 CCHS P-1293 cross-check',
    f'''## Independent 1975 CCHS P-1293 cross-check

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) is independent of the city photocompare screenshots and supplies a useful later-state control. In the established 5th/Main mapping, **505 extends farther rearward than 503** and the former **501** corner structure remains absent. The 501 observation only corroborates the existing 1936–1944 removal bracket. The 505 observation sharpens the rear-expansion research question: determine the earliest photocompare frame in which the 505-vs-503 depth asymmetry becomes visible. The photograph itself does not date the change or prove a circa-1940 addition.'''
)

append_once(
    'evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md',
    '## 5 September 2026 follow-up — CCHS P-1293',
    f'''## 5 September 2026 follow-up — CCHS P-1293

New independent aerial `{MID}` / `{SID}` / `{EID}`, cataloged by CCHS as **1975**, directly shows **505 extending farther rearward than 503**. This confirms the later-state asymmetry previously carried as owner observation (`E-011`) but **does not date its origin** and does not by itself validate the circa-1940 rear-addition hypothesis (`E-101`). It changes the best next test to a frame-by-frame search for the **first appearance** of the asymmetry in 1936/1940/1944/1955/1961/1974 aerials, followed by permit/assessor correlation.'''
)

append_once(
    'evidence/research-leads.md',
    'P-1293 1975 rear-depth terminus for RL-005',
    f'''### P-1293 1975 rear-depth terminus for RL-005

CCHS `{TARGET}` (`{MID}` / `{SID}` / `{EID}`) now directly confirms that **505 Main extended farther rearward than 503 Main by 1975**. Treat this as a later-state terminus, not a construction date. Re-review `IMG-0007` (1936), `IMG-0008` (1940), `IMG-0009` (1944), `IMG-0010` (1955), `IMG-0011` (1961), and `IMG-0012` (1974) specifically for the first frame showing the same rear-edge asymmetry; then target assessor cards/permits around that earliest transition. This is a focused follow-up to `RL-005` / `E-101` / `E-102`.'''
)

for path, title, text in [
    (
        'buildings/503-main.md',
        '1975 P-1293 aerial footprint comparison',
        f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), cataloged **1975**, shows the mapped 503 footprint ending materially sooner rearward/westward than adjacent 505. This is relative-footprint evidence only; it does not establish the legal boundary or when 505 became deeper.'
    ),
    (
        'buildings/505-main.md',
        '1975 P-1293 aerial footprint comparison',
        f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), cataloged **1975**, directly confirms the later-state condition that **505 extends farther rearward/westward than 503**. This materially corroborates `E-011` and supplies a by-1975 endpoint for `RL-005`, but does not prove the change occurred in 1940 or identify an addition permit.'
    ),
    (
        'buildings/501-main.md',
        '1975 P-1293 continued absence',
        f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), cataloged **1975**, shows no separate 501 structure at the mapped former corner site. This is independent later corroboration only; `E-021` already establishes that 501 disappeared between 1936 and 1944, so the 1975 image does not narrow the removal date.'
    ),
]:
    append_once(path, f'## {title}', f'## {title}\n\n{text}')

append_once(
    'timelines/503-main.md',
    f'| 1975 | CCHS {TARGET}',
    f'| 1975 | CCHS `{TARGET}` aerial shows 503 ending materially sooner rearward than adjacent 505. | Direct relative-footprint evidence; no legal boundary or change date inferred. | `{EID}`; `{SID}`; `{MID}` |'
)
append_once(
    'timelines/505-main.md',
    f'| 1975 | CCHS {TARGET}',
    f'| 1975 | CCHS `{TARGET}` aerial directly shows **505 extending farther rearward than 503**. | Confirms later-state asymmetry by 1975; does not date the change or prove a circa-1940 addition. | `{EID}`; `{SID}`; `{MID}` |'
)
append_once(
    'timelines/501-main.md',
    f'| 1975 | CCHS {TARGET}',
    f'| 1975 | CCHS `{TARGET}` aerial shows the former 501 corner footprint still absent. | Corroboration only; 1936–1944 removal bracket already established by `E-021`. | `{EID}`; `{SID}`; `{MID}` |'
)
append_once(
    'timeline.md',
    f'## {TID} —',
    f'''## {TID} — {TIMELINE_NAME}

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), institutionally cataloged **1975**, provides an independent aerial control for the 5th/Main block. In the established address mapping, **505 Main extends materially farther rearward/westward than 503 Main**, while the separate former **501 Main** corner structure is absent. The 505 observation confirms the later-state depth asymmetry by 1975 but does not date the change or prove the `E-101` circa-1940 rear-addition hypothesis. The 501 observation corroborates but does not narrow the existing **1936–1944** removal bracket. The uploaded title/filename says “1981”; the CCHS 1975 date wording is controlling as catalog metadata and the discrepancy is preserved.'''
)

append_once(
    'indexes/id-crosswalk.md',
    f'`{MID}` CCHS `{TARGET}`',
    f'| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`, `B-001`, `B-002`, `B-005`, `E-011`, `E-021`, `E-101`, `E-102` | CCHS-cataloged 1975 aerial; 505 visibly deeper rearward than 503; 501 absent; supplied title says 1981, catalog metadata says 1975. |'
)

append_once(
    'registers/research-log.md',
    f'## 5 September 2026 — CCHS {TARGET}',
    f'''## 5 September 2026 — CCHS {TARGET} 1975 aerial footprint control

- Integrated `{MID}` / `{SID}` / `{EID}` / `{TID}` from exact CCHS catalog object `{TARGET}` and project-steward supplied photograph metadata.
- Visual review confirms **505 extends farther rearward than 503** and **501 is absent** in the mapped target block.
- Recorded this as a by-1975 later-state endpoint for the unresolved 505 rear-depth chronology; did **not** convert it into proof of a 1940 addition.
- Preserved the metadata conflict: supplied title/filename says **1981**, while the CCHS Date made field/description says **1975**.
- 501 absence is corroborative only because `E-021` already brackets removal to 1936–1944.'''
)

# Structured source/evidence/timeline append.
sy = rd('database/sources.yml').rstrip()
sy += f'''

  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{CAP}"
    notes: "CCHS P-1293 aerial cataloged 1975; uploaded title says 1981. Direct mapped-block view confirms 505 is deeper rearward than 503 and 501 remains absent."
    related_media: [{MID}]
    related_evidence: [{EID}]'''
wr('database/sources.yml', sy + '\n')

ey = rd('database/evidence.yml').rstrip()
ey += f'''

  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: Primary aerial photographic evidence with institutional catalog metadata
    classification: DOCUMENTED / DIRECT
    claims:
      - "In the established 5th/Main mapping, 505 Main extends materially farther rearward/westward than 503 Main in the CCHS-cataloged 1975 aerial."
      - "The former 501 Main corner structure is absent; this corroborates but does not narrow the existing 1936-1944 removal bracket."
      - "The image confirms the 505/503 rear-depth asymmetry by 1975 but does not date its origin or prove a circa-1940 addition."
      - "The supplied title/filename says 1981 while the institutional metadata says 1975; the conflict is preserved."
    confidence: "High to Very High for relative footprint and 501 absence in the mapped block; no exact dimensions or construction date inferred."
    related_sources: [{SID}]
    related_buildings: [B-001, B-002, B-005]
    related_media: [{MID}]
    repository_file: {CAP}'''
wr('database/evidence.yml', ey + '\n')

ty = rd('database/timeline.yml').rstrip()
ty += f'''

  - id: {TID}
    date: "1975"
    title: "{TIMELINE_NAME}"
    summary: "CCHS P-1293 confirms that 505 extends farther rearward than 503 by 1975 and that the former 501 structure remains absent; no change date inferred."
    confidence: "High for mapped relative footprint; exact construction/change date unresolved."
    related_sources: [{SID}]
    related_evidence: [{EID}]
    related_buildings: [B-001, B-002, B-005]'''
wr('database/timeline.yml', ty + '\n')

print(f'Integrated {MID}/{SID}/{EID}/{TID}; image {IMAGE}')
