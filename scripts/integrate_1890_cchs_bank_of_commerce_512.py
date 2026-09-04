from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET_CATALOG = "2008.008.049.056"
MEDIA_ID = "IMG-0741"
SOURCE_ID = "S-212"
EVIDENCE_ID = "E-192"
REPO_IMAGE = "media/photos/early-main-street/IMG-0741_1890-oregon-city-bank-of-commerce-interior-512-main-cchs-2008-008-049-056.jpg"
API_CAPTURE = "evidence/source-captures/1890-cchs-2008-008-049-056-bank-of-commerce-interior-512-main-api-2026-09-04.json"
SOURCE_CAPTURE = "evidence/source-captures/1890-cchs-2008-008-049-056-bank-of-commerce-interior-512-main-2026-09-04.md"
SEARCH_URL = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": TARGET_CATALOG, "size": 50})
ACCOUNT_ID = "4813"

STEWARD = {
    "filename": "Interior of the Oregon City Bank of Commerce, 512 Main St 1890(1).jpg",
    "width": 2048,
    "height": 1384,
    "bytes": 1614953,
    "sha256": "892ac908cbed6ab49381e890ecedce0410bb936f709a8f326ef969874f0c11a0",
}
CATALOG_METADATA = {
    "title": "Interior of the Oregon City Bank of Commerce",
    "entry_object_id": TARGET_CATALOG,
    "description": "Interior of the Oregon City Bank of Commerce (1st National), 512 Main. Latourette and Myers ?",
    "date_made": "1890",
    "city": "Oregon City",
    "county": "Clackamas",
    "state": "Oregon",
    "country": "United States of America",
    "continent": "North America",
    "medium": "Negative",
    "location_of_negative": "Society Collection",
    "other_number": "Lynch-Criteser 056",
    "other_photo_number": "Freytag Collection #1",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


checks = {
    SOURCE_ID: ("evidence/source-register.md", f"## {SOURCE_ID}"),
    EVIDENCE_ID: ("evidence/evidence-register.md", f"## {EVIDENCE_ID}"),
    MEDIA_ID: ("media/photo-metadata-register.md", f"## {MEDIA_ID}"),
}
present = {ident: marker in read(path) for ident, (path, marker) in checks.items()}
if any(present.values()):
    if all(present.values()) and Path(REPO_IMAGE).exists():
        print("Bank photo already integrated; no changes needed.")
        raise SystemExit(0)
    raise SystemExit(f"Partial ID collision detected: {present}; stop rather than reuse/renumber IDs.")

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
    if slug else None
)

api_record = {
    "reviewed": "2026-09-04",
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

catalog_link = hub_url or entry_url
capture = f"""# CCHS {TARGET_CATALOG} — Interior of the Oregon City Bank of Commerce, cataloged 512 Main / 1890

Reviewed **4 September 2026** from the project-steward supplied JPEG and the exact Clackamas County Historical Society public CatalogIt record recovered by catalog number.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW; ADDRESS, DATE, INSTITUTION-NAME AND PERSON-IDENTIFICATION CAUTIONS APPLY.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`.

## Catalog record

- Institutional title: **Interior of the Oregon City Bank of Commerce**
- Entry/Object ID: `{TARGET_CATALOG}`
- Description supplied by the steward/catalog: **Interior of the Oregon City Bank of Commerce (1st National), 512 Main. Latourette and Myers ?**
- Date made: **1890**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Negative**
- Location of negative: **Society Collection**
- Other No.: **Lynch-Criteser 056**
- Other Photo #: **Freytag Collection #1**
- Public record: {catalog_link}
- Public API entry: {entry_url}

## Steward attachment

- Original filename: `{STEWARD['filename']}`
- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**
- Bytes: **{STEWARD['bytes']:,}**
- SHA-256: `{STEWARD['sha256']}`

## Repository image

- File: `{REPO_IMAGE}`
- Public derivative recovered from the exact CCHS record: {derivative['url']}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Relation to upload: repository binary is a public CCHS derivative from the same exact catalog record; it is not assumed byte-identical to the steward JPEG.

## Direct visual observation

The supplied image visibly depicts a historic bank/office interior with a long wooden service counter and teller-style partitioning, interior doorways, framed wall material and a **Clackamas County Historical Society** watermark. No readable **512 Main** street number, **1890** date, bank name, or person name is visible in the image itself at the supplied resolution.

## Historical limits

1. **512 Main** and **1890** are catalog metadata, not image-visible facts. They are preserved as institutional attribution rather than silently converted into building-continuity proof.
2. The wording **“Oregon City Bank of Commerce (1st National)”** may reflect later institutional/catalog interpretation. The photograph alone does not establish the exact corporate-name chronology or prove that every later Bank of Commerce / First National reference concerns the same institution, room or building.
3. **“Latourette and Myers ?”** is explicitly uncertain in the supplied description. It is retained verbatim as a lead and is not promoted to a positive identification of the people shown.
4. This is a valuable **even-side Main Street / 512 Main address anchor**, but it does not by itself map 512 to a particular modern surviving structure or establish structural continuity from 1890.
5. No inference about 503 or 505 Main occupancy, ownership, or building continuity is made from this photograph.
"""
write(SOURCE_CAPTURE, capture)

photo_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Interior of Oregon City Bank of Commerce, 512 Main, cataloged 1890

- Type: Institutional historic photograph / interior view
- CCHS external object: `{TARGET_CATALOG}`
- Catalog title: **Interior of the Oregon City Bank of Commerce**
- Catalog date: **1890**
- Catalog location: **512 Main, Oregon City** (institutional metadata; not image-visible)
- Repository file: `{REPO_IMAGE}`
- Status: `committed`
- Repository derivative: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Steward attachment: `{STEWARD['filename']}`; {STEWARD['width']} × {STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`
- Source/evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`
- Other identifiers: **Lynch-Criteser 056**; **Freytag Collection #1**
- Catalog note: medium **Negative**; negative location **Society Collection**.
- Interpretation limit: the catalog's **“(1st National)”** and **“Latourette and Myers ?”** wording is preserved as institutional/uncertain metadata; the image does not visibly prove the address, date, institution name, or person identities. No structural continuity to a modern building is inferred.
- Review: `{SOURCE_CAPTURE}`
"""
append_once("media/photo-metadata-register.md", f"## {MEDIA_ID}", photo_block)

inventory_block = f"""### {MEDIA_ID} — CCHS {TARGET_CATALOG} Bank of Commerce interior, 512 Main, cataloged 1890
- File: `{REPO_IMAGE}`
- Institutional metadata: Interior of the Oregon City Bank of Commerce; 512 Main; 1890; Lynch-Criteser 056 / Freytag Collection #1.
- Source/evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`.
- Limit: address/date/name are catalog metadata; “Latourette and Myers ?” remains uncertain and no building continuity is inferred.
"""
append_once("media/photos/inventory.md", f"### {MEDIA_ID}", inventory_block)

readme_block = f"""## {MEDIA_ID} — CCHS {TARGET_CATALOG} Bank of Commerce interior, 512 Main, cataloged 1890

`{Path(REPO_IMAGE).name}` preserves the largest public image derivative recovered from the exact CCHS catalog-number record. The steward-supplied image was visually reviewed and is tracked by its original dimensions, byte count and SHA-256 in `media/photo-metadata-register.md`. CCHS catalogs the scene as the **Interior of the Oregon City Bank of Commerce**, **512 Main**, **1890**; those are institutional metadata rather than text visible in the image. The description's **“Latourette and Myers ?”** remains explicitly uncertain. See `{SOURCE_ID}` / `{EVIDENCE_ID}` and `{SOURCE_CAPTURE}`.
"""
append_once("media/photos/early-main-street/README.md", f"## {MEDIA_ID}", readme_block)

source_block = f"""## {SOURCE_ID} — Clackamas County Historical Society {TARGET_CATALOG}, Interior of the Oregon City Bank of Commerce
Type: Institutional historic photograph and museum-catalog record; steward JPEG **VISUALLY VERIFIED** 4 September 2026 and exact CatalogIt object retrieved by catalog number.  
Catalog/API: {catalog_link} ; {entry_url}  
Repository image: `{REPO_IMAGE}`  
Source capture: `{SOURCE_CAPTURE}`  
Related evidence/media: `{EVIDENCE_ID}` / `{MEDIA_ID}`.  
Notes: CCHS metadata supplied with the photo gives **1890**, **512 Main**, medium **Negative**, negative location **Society Collection**, **Lynch-Criteser 056**, and **Freytag Collection #1**. Description wording **“(1st National)”** and **“Latourette and Myers ?”** is retained exactly as uncertain/institutional metadata; the image itself does not visibly print the address, date, bank name, or person names. No 503/505 or present-building continuity is inferred. Steward SHA-256 `{STEWARD['sha256']}`; committed derivative SHA-256 `{repo_sha}`.
"""
append_once("evidence/source-register.md", f"## {SOURCE_ID}", source_block)

evidence_block = f"""## {EVIDENCE_ID} — CCHS catalogs 1890 Bank of Commerce interior at 512 Main
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / VISUALLY VERIFIED**, with address/date/institution-name/person-identification cautions.  
Source: `{SOURCE_ID}`; image `{MEDIA_ID}`.  
Claims: CCHS object `{TARGET_CATALOG}` is cataloged **Interior of the Oregon City Bank of Commerce**, date **1890**, with description **“Interior of the Oregon City Bank of Commerce (1st National), 512 Main. Latourette and Myers ?”**. The supplied image visibly shows a historic bank/office interior with a long service counter and teller-style partitioning. Catalog metadata also gives **Negative**, **Society Collection**, **Lynch-Criteser 056**, and **Freytag Collection #1**.  
Limits: 512 Main, 1890, the Bank of Commerce/First National relationship, and any Latourette/Myers identification are not readable from the image itself. The question mark after Myers is retained as uncertainty. This source does not prove corporate-name continuity, occupancy continuity, ownership, a particular surviving building, or any 503/505 condition.  
Confidence: **Very High** for the exact CCHS catalog wording and visible interior content; **UNRESOLVED** for catalog-date precision, retrospective address mapping, institutional-name chronology, person identities, and structural continuity.
"""
append_once("evidence/evidence-register.md", f"## {EVIDENCE_ID}", evidence_block)

sources_yml = f"""  - id: {SOURCE_ID}
    name: "Clackamas County Historical Society {TARGET_CATALOG}, Interior of the Oregon City Bank of Commerce, 512 Main, cataloged 1890"
    url: "{catalog_link}"
    repository_file: "{REPO_IMAGE}"
    notes: "Exact CCHS catalog-number record and visually reviewed steward image. Catalog supplies 1890 / 512 Main / Negative / Society Collection / Lynch-Criteser 056 / Freytag Collection #1. '(1st National)' and 'Latourette and Myers ?' remain institutional/uncertain metadata; no building continuity or 503/505 claim. Related {EVIDENCE_ID}/{MEDIA_ID}. Steward SHA-256 {STEWARD['sha256']}; repository derivative SHA-256 {repo_sha}."
    related_evidence: [{EVIDENCE_ID}]
    related_media: [{MEDIA_ID}]
"""
append_once("database/sources.yml", f"  - id: {SOURCE_ID}\n", sources_yml)

evidence_yml = f"""  - id: {EVIDENCE_ID}
    name: "CCHS catalogs 1890 Bank of Commerce interior at 512 Main"
    type: "Institutional photograph/catalog metadata plus direct visual review; documented/visually verified with address/date/institution-name/person-identification cautions"
    claims:
      - "CCHS {TARGET_CATALOG} catalogs Interior of the Oregon City Bank of Commerce, date 1890, and describes it as (1st National), 512 Main, with Latourette and Myers followed by a question mark."
      - "The supplied photograph visibly shows a historic bank/office interior with a long service counter and teller-style partitioning; it does not visibly print 512 Main, 1890, the bank name, or person names."
      - "Catalog metadata supplies Negative; Society Collection; Lynch-Criteser 056; Freytag Collection #1."
    confidence: "Very High for exact catalog wording and visible interior content; unresolved for date/address precision, institutional-name chronology, person identities and structural continuity."
    related_sources: [{SOURCE_ID}]
"""
append_once("database/evidence.yml", f"  - id: {EVIDENCE_ID}\n", evidence_yml)

crosswalk_block = f"""## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID} — CCHS {TARGET_CATALOG} Bank of Commerce interior

- Source: `{SOURCE_ID}` — exact CCHS catalog-number record for **Interior of the Oregon City Bank of Commerce**.
- Evidence: `{EVIDENCE_ID}` — cataloged **1890 / 512 Main** and direct interior-image content, with attribution limits.
- Media: `{MEDIA_ID}` — `{REPO_IMAGE}`.
- Other institutional identifiers: **Lynch-Criteser 056**; **Freytag Collection #1**.
- Limits: **“(1st National)”** and **“Latourette and Myers ?”** remain catalog/uncertain wording; no modern-building, ownership, person-identity, or 503/505 continuity is asserted.
- Review: `{SOURCE_CAPTURE}`.
"""
append_once("indexes/id-crosswalk.md", f"## {SOURCE_ID} / {EVIDENCE_ID} / {MEDIA_ID}", crosswalk_block)

log_block = f"""## 4 September 2026 — CCHS 1890 Bank of Commerce interior, cataloged 512 Main

- Checked current `main` before integration; exact object `{TARGET_CATALOG}` was not already registered.
- Preserved the largest public derivative recovered from the exact CCHS record as `{MEDIA_ID}` and recorded the steward upload hash/dimensions separately for provenance.
- Added `{SOURCE_ID}` / `{EVIDENCE_ID}` plus API/source captures and synchronized media/source/evidence/crosswalk records.
- Preserved **“(1st National)”** and **“Latourette and Myers ?”** as catalog wording rather than positive identification. The image does not visibly prove 512 Main, 1890, the bank name or the people; no present-building or 503/505 continuity was inferred.
- Validator must pass before the integration commit is pushed.
"""
append_once("registers/research-log.md", "## 4 September 2026 — CCHS 1890 Bank of Commerce interior", log_block)

print(f"Integrated {MEDIA_ID}/{SOURCE_ID}/{EVIDENCE_ID}: {REPO_IMAGE}")
print(f"Repository derivative: {repo_width}x{repo_height}, {repo_bytes} bytes, sha256 {repo_sha}")
