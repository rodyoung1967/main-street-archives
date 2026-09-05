from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "P-6974"
SECONDARY_CATALOG = "2008.008.001.320"
ACCOUNT_ID = "4813"
REVIEW_DATE = "2026-09-04"

STEWARD = {
    "filename": "Oregon City 1908 - Friedrich's Hardware and Little's Confectionery at 510-512 7th Street.jpg",
    "width": 2048,
    "height": 1372,
    "bytes": 516379,
    "sha256": "b394eacbd2e3052599abd7829c3207a8d7b0ebdf709d0b90b5cd8e54fb10d41d",
}

CATALOG_METADATA = {
    "title": "Oregon City 1908 - Friedrich's Hardware and Little's Confectionery at 510-512 7th Street",
    "entry_object_id": TARGET_CATALOG,
    "description": "Friedrich's Hardware and Little's Confectionery  510 - 512 7th St., Oregon City (Richard Friedrichs on right; Walter Little on left)  2008.008.001.320 Negative and Sample Print",
    "date_made": "1908",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_numbers": ["Society 320", "Society Photo #: 320", "Ferguson Collection #18"],
}

SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode(
    {"query": TARGET_CATALOG, "size": 50}
)


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def max_numeric_id(path: str, prefix: str) -> int:
    nums = [int(v) for v in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums:
        raise SystemExit(f"No existing {prefix} IDs found in {path}")
    return max(nums)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def catalog_number(d):
    try:
        return d["properties"]["hasCatalogNumber"]["value_text"]
    except (KeyError, TypeError):
        return None


def find_matching_dict(obj):
    if isinstance(obj, dict):
        if catalog_number(obj) == TARGET_CATALOG:
            return obj
        for value in obj.values():
            found = find_matching_dict(value)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_matching_dict(value)
            if found is not None:
                return found
    return None


def choose_derivative(entry):
    candidates = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path"):
                continue
            if "thumbnail" in key or key in {"complementary_color", "dominant_color"}:
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                candidates.append((w * h, w, h, key, val["path"]))
    if not candidates:
        raise SystemExit("No public image derivative found in the exact CCHS record.")
    candidates.sort(reverse=True)
    _, w, h, key, url = candidates[0]
    return {"key": key, "url": url, "width": w, "height": h}


# Never create a second archive identity for the same institutional object.
for p in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    text = read(p)
    if TARGET_CATALOG in text or SECONDARY_CATALOG in text:
        print(f"{TARGET_CATALOG}/{SECONDARY_CATALOG} already integrated in {p}; no changes needed.")
        raise SystemExit(0)

SOURCE_ID = f"S-{max_numeric_id('evidence/source-register.md', 'S') + 1:03d}"
EVIDENCE_ID = f"E-{max_numeric_id('evidence/evidence-register.md', 'E') + 1:03d}"
MEDIA_ID = f"IMG-{max_numeric_id('media/photo-metadata-register.md', 'IMG') + 1:04d}"

person_base = max_numeric_id("people/people-index.md", "P")
RICHARD_ID = f"P-{person_base + 1:03d}"
WALTER1908_ID = f"P-{person_base + 2:03d}"

business_base = max_numeric_id("businesses/business-index.md", "BUS")
FRIEDRICH_BUS_ID = f"BUS-{business_base + 1:03d}"
LITTLE_BUS_ID = f"BUS-{business_base + 2:03d}"

REPO_IMAGE = (
    f"media/photos/early-main-street/{MEDIA_ID}_1908-friedrichs-hardware-littles-confectionery-"
    f"510-512-7th-cchs-p6974.jpg"
)
API_CAPTURE = "evidence/source-captures/1908-cchs-p6974-friedrich-little-510-512-7th-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1908-cchs-p6974-friedrich-little-510-512-7th-2026-09-04.md"

search = get_json(SEARCH_URL)
match = find_matching_dict(search)
if match is None:
    raise SystemExit(f"Exact CCHS catalog number {TARGET_CATALOG} was not returned by {SEARCH_URL}")
entry_id = match.get("id")
if not entry_id:
    raise SystemExit("Matching CCHS search record had no entry UUID.")
entry_url = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT_ID}/entries/{entry_id}"
entry = get_json(entry_url)
if catalog_number(entry) != TARGET_CATALOG:
    raise SystemExit(f"Fetched CCHS entry did not retain exact catalog number {TARGET_CATALOG}.")

derivative = choose_derivative(entry)
image_data = get_bytes(derivative["url"])
if not image_data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected CCHS derivative is not a JPEG.")
img = Image.open(BytesIO(image_data))
repo_width, repo_height = img.size
repo_sha = sha256_bytes(image_data)
repo_bytes = len(image_data)

path = Path(REPO_IMAGE)
if path.exists():
    raise SystemExit(f"Target image path already exists without registered {MEDIA_ID}: {REPO_IMAGE}")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(image_data)

slug = entry.get("slug") or match.get("slug")
hub_url = (
    f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
    if slug
    else None
)
catalog_link = hub_url or entry_url

api_record = {
    "reviewed": REVIEW_DATE,
    "institution": "Clackamas County Historical Society",
    "search_url": SEARCH_URL,
    "entry_url": entry_url,
    "hub_url": hub_url,
    "selected_public_derivative": derivative,
    "repository_file": REPO_IMAGE,
    "repository_derivative": {
        "width": repo_width,
        "height": repo_height,
        "bytes": repo_bytes,
        "sha256": repo_sha,
    },
    "steward_attachment": STEWARD,
    "catalog_metadata_supplied_by_steward": CATALOG_METADATA,
    "entry": entry,
}
write(API_CAPTURE, json.dumps(api_record, indent=2, ensure_ascii=False) + "\n")

capture = f"""# CCHS {TARGET_CATALOG} — Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, 1908

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt object recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW. BUSINESS/PEOPLE IDENTIFICATIONS ARE CCHS CATALOG IDENTIFICATIONS; THE IMAGE ITSELF DOES NOT LEGIBLY PRINT THOSE NAMES. SAME-PERSON EQUATION WITH THE LATER WALTER L. LITTLE (`P-090`) IS UNRESOLVED.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`. New catalog-derived entities: `{FRIEDRICH_BUS_ID}` Friedrich's Hardware; `{LITTLE_BUS_ID}` Little's Confectionery; `{RICHARD_ID}` Richard Friedrichs; `{WALTER1908_ID}` Walter Little (1908 confectionery identification). Existing later same-name person: `P-090` Walter L. Little, not merged.

## Catalog record

- Institutional title: **{CATALOG_METADATA['title']}**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description: **{CATALOG_METADATA['description']}**
- Date made: **1908**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of negative: **Society Collection**
- Related catalog/object number in description: `{SECONDARY_CATALOG}`
- Other No.: **Society 320**
- Society Photo #: **320**
- Other Photo #: **Ferguson Collection #18**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is the largest public CCHS derivative recovered from the same exact institutional photograph; the steward upload remains separately tracked by filename, dimensions, bytes and hash.

## Direct visual observation

The photograph shows two adjacent street-level commercial storefronts with two men standing outside. A stairway rises between the storefronts. The left storefront is one story; the right storefront is two stories. Merchandise is visible in both display windows.

The project review does **not** independently identify the men by facial recognition and does **not** claim that the business names are legible in this scan. The names and left/right assignments come from the CCHS catalog description.

## What the catalog directly establishes

CCHS identifies the scene as **Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, Oregon City, 1908** and states **Richard Friedrichs on right; Walter Little on left**. This is direct institutional catalog evidence for the photographed business/address group and the catalog's identification of the two men.

The catalog wording gives the address as a combined **510–512 7th St.** group. It does not, in the supplied wording, explicitly assign 510 to one business and 512 to the other. The archive therefore does **not** split the individual numbers between Friedrich's Hardware and Little's Confectionery without further evidence.

## Walter Little identity limit

The archive already contains `P-090`, **Walter L. Little**, from 1921–1922 Oregon City records connected to the Leland & Little billiards lead. The 1908 CCHS catalog uses the name **Walter Little** for the man on the left at Little's Confectionery. The 14-year chronological gap, common name form, and lack of an independent same-person identifier mean these records must **not** be merged by name alone.

Accordingly, `{WALTER1908_ID}` is a separate provisional person record for the **1908 confectionery identification**. The possible equation `{WALTER1908_ID} = P-090` is an **UNVERIFIED LEAD / identity question**, not a historical conclusion.

## Richard Friedrichs identity limit

CCHS identifies **Richard Friedrichs** on the right at Friedrich's Hardware. Later Oregon City material in the repository includes references to **C. W. Friedrich and Son**. This photograph alone does not establish Richard's relationship to that later firm or any business succession; that remains a separate research question.

## Classification

- **DOCUMENTED / DIRECT (institutional catalog):** 1908 date; Oregon City; Friedrich's Hardware and Little's Confectionery; combined 510–512 7th Street location; Richard Friedrichs on right; Walter Little on left; `{TARGET_CATALOG}` / `{SECONDARY_CATALOG}` and related catalog numbers.
- **DIRECT VISUAL:** two adjacent storefronts, two men, stairway between buildings/storefronts, merchandise/display-window context.
- **UNRESOLVED:** which individual business occupied 510 versus 512; whether the catalog's 1908 Walter Little is later `P-090`; Richard Friedrichs's relationship to C. W. Friedrich and Son.

## Research value

This image is outside the core 501/503/505 Main frontage, but it is directly relevant to the project’s **Walter Little identity problem**. If the 1908 confectioner can be independently connected to the 1921–1922 W. L./Walter L. Little records, it would materially extend that person's Oregon City business chronology. Until then, the two identities remain separate.
"""
write(SOURCE_CAPTURE, capture)

append_once(
    "evidence/source-register.md",
    f"## {SOURCE_ID} —",
    f"""## {SOURCE_ID} — CCHS {TARGET_CATALOG}, Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, 1908
Type: Institutional historic photograph and museum-catalog record; photograph visually reviewed.
Institution: Clackamas County Historical Society.
Catalog IDs: `{TARGET_CATALOG}`; description also names `{SECONDARY_CATALOG}`; Society 320; Society Photo #320; Ferguson Collection #18.
Date: **1908**.
Location: **510–512 7th Street, Oregon City** as a combined cataloged address group.
Repository file: `{REPO_IMAGE}`.
Source capture: `{SOURCE_CAPTURE}`.
Public record: {catalog_link}
Public API: {entry_url}
Related evidence/media: `{EVIDENCE_ID}` / `{MEDIA_ID}`.
Notes: CCHS identifies **Richard Friedrichs on right** and **Walter Little on left** with Friedrich's Hardware and Little's Confectionery. The image itself does not independently prove the names, and the catalog wording does not assign 510 versus 512 to a specific business. The 1908 Walter Little is **not merged** with later `P-090` Walter L. Little solely by name.""",
)

append_once(
    "evidence/evidence-register.md",
    f"## {EVIDENCE_ID} —",
    f"""## {EVIDENCE_ID} — 1908 Friedrich's Hardware / Little's Confectionery at 510–512 7th Street
Source: `{SOURCE_ID}`
Media: `{MEDIA_ID}`
Type: Primary photographic evidence with institutional catalog metadata
Claims:
- CCHS catalogs the photograph to **1908** and identifies the business group as **Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, Oregon City**.
- CCHS identifies **Richard Friedrichs on right** and **Walter Little on left**.
- The catalog wording provides 510–512 as a combined address group and does not establish which individual business held 510 versus 512.
- The photograph visually shows two adjacent commercial storefronts, two men, and a stairway between the storefronts, but the business/person names are catalog identifications rather than independently legible image text.
- The 1908 Walter Little record is **not sufficient by itself** to merge with `P-090` Walter L. Little of the 1921–1922 billiards research.
Classification: **DOCUMENTED / DIRECT** for CCHS catalog metadata and visible streetscape; **UNRESOLVED IDENTITY** for `{WALTER1908_ID}` versus `P-090` and for Richard Friedrichs versus later Friedrich firm references.
Confidence: **Very High** for the CCHS object, 1908 date, combined 510–512 7th Street business-group identification and cataloged left/right person identifications; individual 510/512 assignment and later-person/business continuity unresolved.""",
)

append_once(
    "media/photo-metadata-register.md",
    f"### {MEDIA_ID} —",
    f"""### {MEDIA_ID} — 1908 Friedrich's Hardware and Little's Confectionery, 510–512 7th Street
- Type: Historic street-level photograph
- Date: **1908**
- Institutional catalog: CCHS `{TARGET_CATALOG}`; description also cites `{SECONDARY_CATALOG}`
- Location: **510–512 7th Street, Oregon City** as a combined cataloged address group
- CCHS description: **Friedrich's Hardware and Little's Confectionery ... (Richard Friedrichs on right; Walter Little on left)**
- Source/Evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`
- Repository file: `{REPO_IMAGE}`
- Repository derivative: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Steward original: `{STEWARD['filename']}`; {STEWARD['width']} × {STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Provenance: largest public derivative recovered from the exact CCHS object; steward upload tracked separately by exact signature.
- Interpretation limit: CCHS, not facial recognition or legible storefront text, supplies the business/person names. Do not split 510 versus 512 between the two businesses without further evidence. Do not merge the cataloged 1908 Walter Little with `P-090` solely by name.
- Review: `{SOURCE_CAPTURE}`""",
)

append_once(
    "media/photos/inventory.md",
    f"### {MEDIA_ID} —",
    f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG}, Friedrich's Hardware and Little's Confectionery, 1908
- File: `{REPO_IMAGE}`
- Source/evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`
- CCHS catalog: `{TARGET_CATALOG}`; 1908; combined 510–512 7th Street group.
- Steward original: `{STEWARD['filename']}`; {STEWARD['width']} × {STEWARD['height']}; SHA-256 `{STEWARD['sha256']}`.
- CCHS identification: Richard Friedrichs on right; Walter Little on left.
- Limit: individual 510/512 business assignment unresolved; 1908 Walter Little not merged with `P-090`.""",
)

# Business entity pages and indexes. The combined address is preserved without guessing which business had which number.
write(
    "businesses/friedrichs-hardware-7th-street.md",
    f"""# Friedrich's Hardware — 510–512 7th Street group, 1908

Business ID: `{FRIEDRICH_BUS_ID}`.

CCHS `{TARGET_CATALOG}` catalogs **Friedrich's Hardware and Little's Confectionery** together at **510–512 7th Street, Oregon City** in **1908**, and identifies **Richard Friedrichs on right** (`{EVIDENCE_ID}`). The supplied catalog wording does not say whether Friedrich's Hardware specifically occupied 510 or 512, so the individual number remains unresolved.

This record does not establish continuity or family/business identity with later references to **C. W. Friedrich and Son**. That relationship requires independent evidence.
""",
)
write(
    "businesses/littles-confectionery-7th-street.md",
    f"""# Little's Confectionery — 510–512 7th Street group, 1908

Business ID: `{LITTLE_BUS_ID}`.

CCHS `{TARGET_CATALOG}` catalogs **Friedrich's Hardware and Little's Confectionery** together at **510–512 7th Street, Oregon City** in **1908**, and identifies **Walter Little on left** (`{EVIDENCE_ID}`). The supplied catalog wording does not say whether Little's Confectionery specifically occupied 510 or 512, so the individual number remains unresolved.

The cataloged 1908 **Walter Little** is represented separately as `{WALTER1908_ID}` and is **not merged by name alone** with `P-090` Walter L. Little from the 1921–1922 billiards research.
""",
)
append_once(
    "businesses/business-index.md",
    f"| {FRIEDRICH_BUS_ID} |",
    f"""| {FRIEDRICH_BUS_ID} | [Friedrich's Hardware](friedrichs-hardware-7th-street.md) | 510–512 7th Street group; individual number unresolved | CCHS `{TARGET_CATALOG}`, 1908; Richard Friedrichs cataloged on right. `{EVIDENCE_ID}`. |
| {LITTLE_BUS_ID} | [Little's Confectionery](littles-confectionery-7th-street.md) | 510–512 7th Street group; individual number unresolved | CCHS `{TARGET_CATALOG}`, 1908; Walter Little cataloged on left; not merged with `P-090`. `{EVIDENCE_ID}`. |""",
)
append_once(
    "database/businesses.yml",
    f"  - id: {FRIEDRICH_BUS_ID}",
    f"""  - id: {FRIEDRICH_BUS_ID}
    name: Friedrich's Hardware
    address: 510–512 7th Street group, Oregon City; individual number unresolved
    notes: CCHS {TARGET_CATALOG} catalogs Friedrich's Hardware with Little's Confectionery at the combined 510–512 7th Street group in 1908 and identifies Richard Friedrichs on right. No continuity to later C. W. Friedrich and Son is claimed.
    related_people: [{RICHARD_ID}]
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
    repository_file: businesses/friedrichs-hardware-7th-street.md

  - id: {LITTLE_BUS_ID}
    name: Little's Confectionery
    address: 510–512 7th Street group, Oregon City; individual number unresolved
    notes: CCHS {TARGET_CATALOG} catalogs Little's Confectionery with Friedrich's Hardware at the combined 510–512 7th Street group in 1908 and identifies Walter Little on left. The 1908 Walter Little identity is kept separate from P-090 pending corroboration.
    related_people: [{WALTER1908_ID}]
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
    repository_file: businesses/littles-confectionery-7th-street.md""",
)

# Separate person records preserve the anti-conflation rule.
write(
    "people/profiles/richard-friedrichs-1908.md",
    f"""# Richard Friedrichs — 1908 CCHS hardware-store identification

Person ID: `{RICHARD_ID}`. Related business: `{FRIEDRICH_BUS_ID}` Friedrich's Hardware.

CCHS `{TARGET_CATALOG}` identifies **Richard Friedrichs on right** in the 1908 photograph of Friedrich's Hardware and Little's Confectionery at the combined **510–512 7th Street** address group (`{EVIDENCE_ID}`). This is an institutional catalog identification; the project is not independently identifying him from facial features.

Later repository material contains references to **C. W. Friedrich and Son**. Richard's relationship to that later firm is unresolved and must not be inferred from surname/business type alone.
""",
)
write(
    "people/profiles/walter-little-1908-confectionery.md",
    f"""# Walter Little — 1908 CCHS confectionery identification

Person ID: `{WALTER1908_ID}`. Related business: `{LITTLE_BUS_ID}` Little's Confectionery.

CCHS `{TARGET_CATALOG}` identifies **Walter Little on left** in the 1908 photograph of Friedrich's Hardware and Little's Confectionery at the combined **510–512 7th Street** address group (`{EVIDENCE_ID}`). This is an institutional catalog identification; the project is not independently identifying him from facial features.

This record is deliberately **not merged** with `P-090` **Walter L. Little**, who appears in 1921–1922 Oregon City records tied to the Leland & Little billiards lead. The same-person equation remains an **UNVERIFIED LEAD** pending an independent identifier such as middle initial, residence, spouse/family, directory continuity, occupation transition, or another record explicitly connecting the two contexts.
""",
)
append_once(
    "people/people-index.md",
    f"| {RICHARD_ID} |",
    f"""| {RICHARD_ID} | [Richard Friedrichs — 1908 CCHS identification](profiles/richard-friedrichs-1908.md) | Hardware-store catalog subject | CCHS `{TARGET_CATALOG}` identifies him on right; relation to later Friedrich firm unresolved. |
| {WALTER1908_ID} | [Walter Little — 1908 confectionery identification](profiles/walter-little-1908-confectionery.md) | Confectionery catalog subject | CCHS `{TARGET_CATALOG}` identifies him on left; deliberately not merged with `P-090`. |""",
)
append_once(
    "database/people.yml",
    f"  - id: {RICHARD_ID}",
    f"""  - id: {RICHARD_ID}
    name: Richard Friedrichs
    role: Friedrich's Hardware cataloged subject, 1908
    notes: CCHS {TARGET_CATALOG} identifies Richard Friedrichs on right in the 1908 510–512 7th Street photograph. Relation to later C. W. Friedrich and Son references is unresolved.
    related_businesses: [{FRIEDRICH_BUS_ID}]
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
    repository_file: people/profiles/richard-friedrichs-1908.md

  - id: {WALTER1908_ID}
    name: Walter Little — 1908 confectionery identification
    role: Little's Confectionery cataloged subject, 1908
    notes: CCHS {TARGET_CATALOG} identifies Walter Little on left in the 1908 510–512 7th Street photograph. Kept separate from P-090 Walter L. Little pending independent same-person evidence.
    related_businesses: [{LITTLE_BUS_ID}]
    related_evidence: [{EVIDENCE_ID}]
    related_sources: [{SOURCE_ID}]
    repository_file: people/profiles/walter-little-1908-confectionery.md""",
)

append_once(
    "database/sources.yml",
    f"  - id: {SOURCE_ID}",
    f"""  - id: {SOURCE_ID}
    name: CCHS {TARGET_CATALOG} — Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, 1908
    url: {catalog_link}
    notes: Institutional photograph/catalog record. CCHS identifies Richard Friedrichs on right and Walter Little on left. Combined 510–512 address does not assign individual numbers; 1908 Walter Little is not merged with P-090 by name alone.
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]
    related_businesses: [{FRIEDRICH_BUS_ID}, {LITTLE_BUS_ID}]
    related_people: [{RICHARD_ID}, {WALTER1908_ID}]""",
)
append_once(
    "database/evidence.yml",
    f"  - id: {EVIDENCE_ID}",
    f"""  - id: {EVIDENCE_ID}
    name: 1908 Friedrich's Hardware / Little's Confectionery at 510–512 7th Street
    type: Primary photographic evidence with institutional catalog metadata
    claims:
      - CCHS catalogs the photograph to 1908 and identifies Friedrich's Hardware and Little's Confectionery at the combined 510–512 7th Street address group in Oregon City.
      - CCHS identifies Richard Friedrichs on right and Walter Little on left.
      - The supplied catalog wording does not establish which individual business occupied 510 versus 512.
      - The cataloged 1908 Walter Little is not sufficient by itself to merge with P-090 Walter L. Little from the 1921–1922 billiards research.
    confidence: Very High for the CCHS object/date/combined-address/business and cataloged person identifications; individual 510/512 assignment and later identity continuity unresolved.
    related_sources: [{SOURCE_ID}]
    related_businesses: [{FRIEDRICH_BUS_ID}, {LITTLE_BUS_ID}]
    related_people: [{RICHARD_ID}, {WALTER1908_ID}]
    repository_file: {SOURCE_CAPTURE}""",
)

append_once(
    "evidence/research-leads.md",
    f"## 1908 Walter Little confectionery identity lead — {TARGET_CATALOG}",
    f"""## 1908 Walter Little confectionery identity lead — {TARGET_CATALOG}

CCHS `{TARGET_CATALOG}` (`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}`) identifies **Walter Little on left** at **Little's Confectionery** in the combined **510–512 7th Street** business group in **1908**. The archive already has `P-090` Walter L. Little in 1921–1922 billiards-related records.

**State: UNVERIFIED LEAD / identity question.** Do not merge `{WALTER1908_ID}` with `P-090` by name alone. Seek an independent bridge: 1908–1922 city/business directories, residence/spouse/family identifiers, middle initial, voter/census records, confectionery-to-cigar/billiards transition advertising, or a record explicitly naming the same Walter/W. L. Little across both contexts.

A secondary lead is whether cataloged **Richard Friedrichs** (`{RICHARD_ID}`) is related to the later **C. W. Friedrich and Son** hardware references; surname and business type alone are insufficient.""",
)

append_once(
    "indexes/id-crosswalk.md",
    f"## CCHS {TARGET_CATALOG} —",
    f"""## CCHS {TARGET_CATALOG} — 1908 510–512 7th Street photograph

- Source/evidence/media: `{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}`.
- Businesses: `{FRIEDRICH_BUS_ID}` Friedrich's Hardware; `{LITTLE_BUS_ID}` Little's Confectionery.
- Cataloged people: `{RICHARD_ID}` Richard Friedrichs; `{WALTER1908_ID}` Walter Little (1908 confectionery identification).
- Identity guardrail: `{WALTER1908_ID}` is **not merged** with `P-090` Walter L. Little; same-person question remains unresolved.
- Catalog identifiers: `{TARGET_CATALOG}`; `{SECONDARY_CATALOG}`; Society 320; Society Photo #320; Ferguson Collection #18.
- Review: `{SOURCE_CAPTURE}`.""",
)

append_once(
    "registers/research-log.md",
    f"## 4 September 2026 — CCHS {TARGET_CATALOG}",
    f"""## 4 September 2026 — CCHS {TARGET_CATALOG} 1908 Friedrich/Little 7th Street photograph

- Integrated the steward-supplied 1908 photograph as `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}` using the exact CCHS catalog object and largest public derivative.
- Preserved CCHS's combined **510–512 7th Street** wording without guessing which business occupied which individual number.
- Added `{FRIEDRICH_BUS_ID}` Friedrich's Hardware and `{LITTLE_BUS_ID}` Little's Confectionery.
- Added separate catalog-derived person records `{RICHARD_ID}` Richard Friedrichs and `{WALTER1908_ID}` Walter Little (1908 confectionery identification).
- Did **not** merge the 1908 Walter Little with `P-090` Walter L. Little from the 1921–1922 billiards research; opened an identity lead instead.
- Steward original signature: {STEWARD['width']} × {STEWARD['height']}, {STEWARD['bytes']:,} bytes, SHA-256 `{STEWARD['sha256']}`.""",
)

print(
    f"Integrated {MEDIA_ID} / {SOURCE_ID} / {EVIDENCE_ID}; businesses {FRIEDRICH_BUS_ID}, {LITTLE_BUS_ID}; "
    f"people {RICHARD_ID}, {WALTER1908_ID}; image {REPO_IMAGE}"
)
