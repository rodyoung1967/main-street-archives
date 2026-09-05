from pathlib import Path
import hashlib
import json
import re
import urllib.request
from io import BytesIO
from PIL import Image

TARGET = "P-1043"
ACCOUNT = "4813"
ENTRY_ID = "f9806ec0-9b1e-11eb-b3ef-53e7205a00b4"
ENTRY_URL = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}"
HUB_URL = "https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/oregon-city-1930s-streetcar-on-main-at-6th"
IMAGE = "media/photos/main-street/IMG-0758_1930-1939-main-6th-looking-south-business-roster-cchs-p1043.jpg"
API = "evidence/source-captures/cchs-p1043-1930s-main-6th-business-roster-api-2026-09-05.json"
CAP = "evidence/source-captures/cchs-p1043-1930s-main-6th-looking-south-business-roster-2026-09-05.md"
BAD_ACCOUNT = "11808"
BAD_ENTRY = "28a8afe0-76a1-11ee-bc74-3dd853f6747b"
BAD_HUB = "https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/child-in-front-of-building-1"
BAD_API = "https://api.catalogit.app/api/public/accounts/4813/entries/28a8afe0-76a1-11ee-bc74-3dd853f6747b"
BAD_DIMS = "550 × 850"
BAD_BYTES = "58,901"
BAD_SHA = "a96a00bfc65c364b95078ee38ef186f53faf66c3f2b78ce8fa6eb3864999a92d"

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

def rd(path):
    return Path(path).read_text(encoding="utf-8")

def wr(path, text):
    Path(path).write_text(text, encoding="utf-8")

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()

def catno(entry):
    return entry.get("properties", {}).get("hasCatalogNumber", {}).get("value_text")

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
        raise SystemExit("No public CCHS derivative found")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}

def replace_section(path, header_regex, replacements):
    text = rd(path)
    m = re.search(header_regex, text, re.M)
    if not m:
        raise SystemExit(f"Section not found in {path}: {header_regex}")
    n = re.search(r"(?m)^## ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    sec = text[m.start():end]
    for old, new in replacements:
        sec = sec.replace(old, new)
    wr(path, text[:m.start()] + sec + text[end:])

def replace_yaml_item(path, entity_id, replacements):
    text = rd(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"YAML item {entity_id} not found in {path}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    sec = text[m.start():end]
    for old, new in replacements:
        sec = sec.replace(old, new)
    wr(path, text[:m.start()] + sec + text[end:])

entry = get_json(ENTRY_URL)
if str(entry.get("account_id")) != ACCOUNT:
    raise SystemExit(f"Wrong account: {entry.get('account_id')}")
if entry.get("account_slug") != "clackamas-county-historical-society":
    raise SystemExit(f"Wrong account slug: {entry.get('account_slug')}")
if catno(entry) != TARGET:
    raise SystemExit(f"Wrong catalog number: {catno(entry)}")
if entry.get("slug") != "oregon-city-1930s-streetcar-on-main-at-6th":
    raise SystemExit(f"Unexpected CCHS slug: {entry.get('slug')}")

props = entry.get("properties", {})
if props.get("hasName", {}).get("value_text") != CATALOG["title"]:
    raise SystemExit("CCHS title mismatch")
if props.get("hasDescription", {}).get("value_text") != CATALOG["description"]:
    raise SystemExit("CCHS description mismatch")

der = choose_derivative(entry)
data = get_bytes(der["url"])
if not data.startswith(b"\xff\xd8"):
    raise SystemExit("Correct CCHS derivative is not JPEG")
with Image.open(BytesIO(data)) as im:
    width, height = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()
if (width, height) != (2398, 1422):
    raise SystemExit(f"Unexpected correct derivative dimensions: {width}x{height}")
if sha != "c86af7360e1ab64eb0855ed967cc0d1c22f8b8a06254070d2743ffbce6226daa":
    raise SystemExit(f"Unexpected correct derivative SHA: {sha}")

# Replace the accidentally selected unrelated Fort Lauderdale image with the exact CCHS P-1043 derivative.
Path(IMAGE).write_bytes(data)

corrected_api = {
    "reviewed": "2026-09-05",
    "catalog": TARGET,
    "entry_url": ENTRY_URL,
    "hub_url": HUB_URL,
    "selected_derivative": der,
    "repository_file": IMAGE,
    "repository_image": {"width": width, "height": height, "bytes": nbytes, "sha256": sha},
    "steward_upload": STEWARD,
    "catalog_metadata_supplied_by_steward": CATALOG,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "correction_2026_09_05": {
        "reason": "The initial global CatalogIt search returned an unrelated History Fort Lauderdale object that reused catalog number P-1043 before the CCHS object. The archive was corrected to the account-scoped Clackamas County Historical Society object before finalization.",
        "rejected_account_id": BAD_ACCOUNT,
        "rejected_entry_id": BAD_ENTRY,
        "correct_account_id": ACCOUNT,
        "correct_entry_id": ENTRY_ID,
    },
    "entry": entry,
}
wr(API, json.dumps(corrected_api, indent=2, ensure_ascii=False) + "\n")

cap = rd(CAP)
cap = cap.replace(BAD_HUB, HUB_URL).replace(BAD_API, ENTRY_URL)
cap = cap.replace(f"- Dimensions: **{BAD_DIMS}**\n- Bytes: **{BAD_BYTES}**\n- SHA-256: `{BAD_SHA}`",
                  f"- Dimensions: **{width} × {height}**\n- Bytes: **{nbytes:,}**\n- SHA-256: `{sha}`")
correction = f'''\n## CatalogIt account-scope correction\n\nDuring initial automation, a **global CatalogIt search** encountered an unrelated **History Fort Lauderdale** object that also uses catalog number `P-1043`. That global duplicate was mistakenly selected as the first exact-number match. The error was detected by the mismatched account/slug and portrait image geometry and corrected **5 September 2026** before finalization.\n\nThe repository image and API capture now come from the exact account-scoped Clackamas County Historical Society object:\n\n- CCHS account ID: `{ACCOUNT}`\n- CCHS entry ID: `{ENTRY_ID}`\n- CCHS slug: `oregon-city-1930s-streetcar-on-main-at-6th`\n- Correct repository derivative: **{width} × {height}**, SHA-256 `{sha}`\n\nThe rejected Fort Lauderdale object is retained only in this audit explanation and is **not evidence for Oregon City**.\n'''
if "## CatalogIt account-scope correction" not in cap:
    marker = "## Project-steward supplied image"
    cap = cap.replace(marker, correction + "\n" + marker)
wr(CAP, cap)

replace_section("media/photo-metadata-register.md", r"^## IMG-0758\b.*$", [
    (f"Repository dimensions: **{BAD_DIMS}**; {BAD_BYTES} bytes; SHA-256 `{BAD_SHA}`",
     f"Repository dimensions: **{width} × {height}**; {nbytes:,} bytes; SHA-256 `{sha}`"),
    (BAD_HUB, HUB_URL),
])

replace_section("evidence/source-register.md", r"^## S-237\b.*$", [(BAD_HUB, HUB_URL), (BAD_API, ENTRY_URL)])
replace_yaml_item("database/sources.yml", "S-237", [(BAD_HUB, HUB_URL), (BAD_API, ENTRY_URL)])

# Make the reusable integration script account-safe so another same-number CatalogIt object cannot be selected.
script = Path("scripts/integrate_cchs_p1043_1930s_main_6th_business_roster.py")
text = script.read_text(encoding="utf-8")
text = text.replace('{"query": TARGET, "size": 50}', '{"query": TARGET, "size": 200}')
text = text.replace('if catno(obj) == TARGET:\n            return obj', 'if catno(obj) == TARGET and str(obj.get("account_id")) == ACCOUNT:\n            return obj')
script.write_text(text, encoding="utf-8")

log = Path("registers/research-log.md")
lt = log.read_text(encoding="utf-8")
block = f'''\n### 2026-09-05 — P-1043 CatalogIt account-scope correction\n- Detected that the first integration pass used a global CatalogIt exact-number match from unrelated **History Fort Lauderdale account 11808**, which also has an object numbered `P-1043`.\n- Correct CCHS match is **account 4813**, entry `{ENTRY_ID}`, slug `oregon-city-1930s-streetcar-on-main-at-6th`.\n- Replaced the incorrect portrait derivative with the correct CCHS landscape derivative at **{width}×{height}**, {nbytes:,} bytes, SHA-256 `{sha}`.\n- Rewrote the raw API capture to the CCHS object and corrected source/media URLs and fingerprints.\n- Hardened the reusable integration script to require `account_id == 4813` and expanded the search result set before choosing an exact catalog-number match.\n- The historical sign analysis was based on the steward-supplied Oregon City photograph and therefore did not depend on the rejected Fort Lauderdale image; this correction repairs source provenance and repository binary identity.\n'''
if "### 2026-09-05 — P-1043 CatalogIt account-scope correction" not in lt:
    log.write_text(lt.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")

print("Corrected P-1043 to exact CCHS account-scoped object")
print(width, height, nbytes, sha)
