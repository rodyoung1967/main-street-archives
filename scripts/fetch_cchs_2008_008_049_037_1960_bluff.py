from pathlib import Path
import hashlib
import json
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image

TARGET = "2008.008.049.037"
ACCOUNT = "4813"
IMAGE_PATH = "media/photos/main-street/IMG-0771_1960-5th-main-from-bluff-cchs-2008-008-049-037.jpg"
CAPTURE_PATH = "evidence/source-captures/cchs-2008-008-049-037-1960-fifth-main-bluff-photo.md"
META_PATH = "media/photo-metadata-register.md"
INVENTORY_PATH = "media/photos/inventory.md"

STEWARD_SHA256 = "7262acf57c7d2a4cf657053c39472809639e160054055b344106791ada341651"
STEWARD_WIDTH = 2048
STEWARD_HEIGHT = 1387
STEWARD_BYTES = 717179


def get_json(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def get_bytes(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 Main-Street-Archive/1.0"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def catalog_number(obj):
    try:
        return obj["properties"]["hasCatalogNumber"]["value_text"]
    except Exception:
        return None


def find_exact(obj):
    if isinstance(obj, dict):
        if catalog_number(obj) == TARGET:
            return obj
        for value in obj.values():
            hit = find_exact(value)
            if hit is not None:
                return hit
    elif isinstance(obj, list):
        for value in obj:
            hit = find_exact(value)
            if hit is not None:
                return hit
    return None


def choose_derivative(entry):
    candidates = []
    for media in entry.get("media", []):
        for key, value in media.get("derivatives", {}).items():
            if not isinstance(value, dict) or not value.get("path"):
                continue
            if "thumbnail" in key.lower():
                continue
            width = int(value.get("width") or 0)
            height = int(value.get("height") or 0)
            if width and height:
                candidates.append((width * height, width, height, key, value["path"]))
    if not candidates:
        raise SystemExit("No non-thumbnail public image derivative found")
    candidates.sort(reverse=True)
    _, width, height, key, url = candidates[0]
    return {"key": key, "width": width, "height": height, "url": url}


search_url = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode(
    {"query": TARGET, "size": 50}
)
search = get_json(search_url)
match = find_exact(search)
if match is None or not match.get("id"):
    raise SystemExit(f"Exact CCHS object {TARGET} not found")

entry_url = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{match['id']}"
entry = get_json(entry_url)
if catalog_number(entry) != TARGET:
    raise SystemExit(
        f"Catalog mismatch: expected {TARGET}, got {catalog_number(entry)}"
    )

derivative = choose_derivative(entry)
data = get_bytes(derivative["url"])
if not data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected CCHS derivative is not a JPEG")

image = Image.open(BytesIO(data))
width, height = image.size
byte_count = len(data)
sha256 = hashlib.sha256(data).hexdigest()

Path(IMAGE_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE_PATH).write_bytes(data)

slug = entry.get("slug") or match.get("slug")
hub_url = (
    "https://hub.catalogit.app/clackamas-county-historical-society/"
    f"folder/photographs/entry/{slug}"
    if slug
    else entry_url
)

capture = Path(CAPTURE_PATH).read_text(encoding="utf-8")
old_status = (
    "Binary status: **pending-upload** for repository retention because the current "
    "ChatGPT/GitHub connector path cannot transfer the conversation-sandbox JPEG bytes "
    "into the repository."
)
new_status = (
    "Binary status: **committed** as the largest public CCHS derivative recovered from "
    f"the exact catalog object at `{IMAGE_PATH}`. The project-steward upload fingerprint "
    "is preserved separately below because derivative bytes may differ."
)
if old_status in capture:
    capture = capture.replace(old_status, new_status)
elif "Binary status: **committed**" not in capture:
    raise SystemExit("Unexpected source-capture binary-status text")

expected_line = (
    "- Expected repository path once the binary-transfer path is available: "
    f"`{IMAGE_PATH}`"
)
replacement = (
    f"- Repository image: `{IMAGE_PATH}`\n"
    f"- Repository derivative dimensions: **{width} × {height}**\n"
    f"- Repository derivative bytes: **{byte_count:,}**\n"
    f"- Repository derivative SHA-256: `{sha256}`\n"
    f"- Public CCHS record: {hub_url}\n"
    f"- Public CCHS API: {entry_url}"
)
if expected_line in capture:
    capture = capture.replace(expected_line, replacement)
elif "- Repository image:" not in capture:
    raise SystemExit("Unexpected source-capture repository-path text")

Path(CAPTURE_PATH).write_text(capture, encoding="utf-8")

meta = Path(META_PATH).read_text(encoding="utf-8")
old_meta = (
    f"- Expected repository file: `{IMAGE_PATH}`\n"
    "- Status: **`pending-upload`** — the steward supplied the original in the ChatGPT "
    "conversation, but the current ChatGPT/GitHub connector cannot transfer the sandbox "
    "JPEG bytes into the repository. Preserve the fingerprint above and upload the binary "
    "when a supported transfer path is available."
)
new_meta = (
    f"- Repository file: `{IMAGE_PATH}`\n"
    f"- Repository derivative: **{width} × {height}**; **{byte_count:,} bytes**; "
    f"SHA-256 `{sha256}`\n"
    "- Status: **`committed`** — repository binary is the largest public CCHS derivative "
    "recovered from the exact catalog object. The steward-upload fingerprint above remains "
    "the control for the conversation-supplied copy.\n"
    f"- Public CCHS record: {hub_url}"
)
if old_meta in meta:
    meta = meta.replace(old_meta, new_meta)
elif "- Status: **`committed`**" not in meta[meta.find("## IMG-0771"):]:
    raise SystemExit("Unexpected IMG-0771 metadata status text")

Path(META_PATH).write_text(meta, encoding="utf-8")

inventory = Path(INVENTORY_PATH).read_text(encoding="utf-8")
if "### IMG-0771 —" not in inventory:
    block = f"""
### IMG-0771 — CCHS 2008.008.049.037, 1960 Fifth/Main bluff view
- File: `{IMAGE_PATH}`
- CCHS: `2008.008.049.037`; **Lynch-Criteser 037**
- Date: **1960**
- Review: `{CAPTURE_PATH}`
- Key value: exact-dated pre-1967-fire structural and streetscape control for Fifth/Main and the 503/505 frontage.
- Sign-reading limit: storefront lettering in this 2048-pixel steward copy is too soft for a new trade-name claim by itself; compare the stronger companion controls already registered for The Wheel / 505 Tavern signage.
"""
    inventory = inventory.rstrip() + "\n\n" + block.strip() + "\n"
    Path(INVENTORY_PATH).write_text(inventory, encoding="utf-8")

record = {
    "catalog": TARGET,
    "entry_url": entry_url,
    "hub_url": hub_url,
    "selected_derivative": derivative,
    "repository_file": IMAGE_PATH,
    "repository_image": {
        "width": width,
        "height": height,
        "bytes": byte_count,
        "sha256": sha256,
    },
    "steward_upload_control": {
        "width": STEWARD_WIDTH,
        "height": STEWARD_HEIGHT,
        "bytes": STEWARD_BYTES,
        "sha256": STEWARD_SHA256,
    },
}
Path("evidence/source-captures/cchs-2008-008-049-037-1960-fifth-main-bluff-api.json").write_text(
    json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

print(
    f"Preserved {TARGET} as {IMAGE_PATH}: {width}x{height}, "
    f"{byte_count} bytes, sha256 {sha256}"
)
