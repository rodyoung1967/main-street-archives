from pathlib import Path
import hashlib, json, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image

TARGET = "C.0250.005060"
ACCOUNT = "4813"
IMAGE_PATH = "media/photos/main-street/IMG-0773_c1929-1935-oregon-city-main-street-bluff-cchs-c0250-005060.jpg"
CAPTURE_PATH = "evidence/source-captures/2026-09-15-c0250-005060-binary-ingest-and-conversation-handoff.md"
META_PATH = "media/photo-metadata-register.md"
INVENTORY_PATH = "media/photos/inventory.md"
STEWARD_SHA256 = "97b269e43fe38e85b9b8169e1a819870528e7f3ac676279e3a1594d6b3d302aa"
STEWARD_WIDTH = 1381
STEWARD_HEIGHT = 870
STEWARD_BYTES = 219852

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req,timeout=90) as r: return json.load(r)
def get_bytes(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req,timeout=90) as r: return r.read()
def catalog_number(obj):
    try: return obj["properties"]["hasCatalogNumber"]["value_text"]
    except Exception: return None
def find_exact(obj):
    if isinstance(obj,dict):
        if catalog_number(obj)==TARGET: return obj
        for v in obj.values():
            h=find_exact(v)
            if h is not None: return h
    elif isinstance(obj,list):
        for v in obj:
            h=find_exact(v)
            if h is not None: return h
    return None
def choose_derivative(entry):
    c=[]
    for media in entry.get("media",[]):
        for key,val in media.get("derivatives",{}).items():
            if not isinstance(val,dict) or not val.get("path") or "thumbnail" in key.lower(): continue
            w,h=int(val.get("width") or 0),int(val.get("height") or 0)
            if w and h: c.append((w*h,w,h,key,val["path"]))
    if not c: raise SystemExit("No non-thumbnail public image derivative found")
    c.sort(reverse=True); _,w,h,key,url=c[0]
    return {"key":key,"width":w,"height":h,"url":url}

search=get_json("https://api.catalogit.app/api/public/search?"+urllib.parse.urlencode({"query":TARGET,"size":50}))
match=find_exact(search)
if match is None or not match.get("id"): raise SystemExit(f"Exact CCHS object {TARGET} not found")
entry_url=f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{match['id']}"
entry=get_json(entry_url)
if catalog_number(entry)!=TARGET: raise SystemExit(f"Catalog mismatch: expected {TARGET}, got {catalog_number(entry)}")
derivative=choose_derivative(entry); data=get_bytes(derivative["url"])
if not data.startswith(b"\xff\xd8"): raise SystemExit("Selected derivative is not JPEG")
im=Image.open(BytesIO(data)); width,height=im.size; byte_count=len(data); sha256=hashlib.sha256(data).hexdigest()
Path(IMAGE_PATH).parent.mkdir(parents=True,exist_ok=True); Path(IMAGE_PATH).write_bytes(data)
slug=entry.get("slug") or match.get("slug")
hub_url=(f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}" if slug else entry_url)

meta=Path(META_PATH).read_text(encoding="utf-8")
if "## IMG-0773 — CCHS C.0250.005060" not in meta:
    meta += f'''\n\n## IMG-0773 — CCHS C.0250.005060 — Oregon City Main Street from the Bluff\n\n- Type: Historic photograph / CCHS public derivative\n- Institutional title: `Oregon City Main Street`\n- CCHS Entry/Object ID: `C.0250.005060`\n- Institutional description: `Business Section of Oregon City from the Bluff.`\n- Institutional date: none stated in steward-supplied metadata.\n- Project working date: **circa 1929–1935**; research estimate, not CCHS metadata.\n- Repository file: `{IMAGE_PATH}`\n- Repository derivative: **{width} × {height}**; **{byte_count:,} bytes**; SHA-256 `{sha256}`\n- Steward-upload control: **{STEWARD_WIDTH} × {STEWARD_HEIGHT}**; **{STEWARD_BYTES:,} bytes**; SHA-256 `{STEWARD_SHA256}`\n- Status: **`committed`** — largest public derivative recovered from the exact CCHS catalog object.\n- Public CCHS record: {hub_url}\n- Dating evidence: completed 1922 arch bridge; bridge-adjacent building strongly consistent with the 1923 replacement Elks Lodge; Railroad Avenue visually consistent with the documented 1929 improvement; old courthouse still standing, before its 1936–37 replacement.\n- Photographer: Ralph Eddy **probable**, based on visible `Eddy` mark; not promoted to institutional attribution without catalog confirmation.\n'''
    Path(META_PATH).write_text(meta,encoding="utf-8")

inv=Path(INVENTORY_PATH).read_text(encoding="utf-8")
if "### IMG-0773 — CCHS C.0250.005060" not in inv:
    inv += f'''\n\n### IMG-0773 — CCHS C.0250.005060, Oregon City Main Street from the Bluff\n- File: `{IMAGE_PATH}`\n- CCHS: `C.0250.005060`\n- Institutional title: `Oregon City Main Street`\n- Project working date: **circa 1929–1935** (not institutional metadata)\n- Key value: broad downtown/bridge/Railroad Avenue/courthouse visual control; supports the 1929–1935 dating analysis.\n- Review: `evidence/source-captures/2026-09-15-eddy-bluff-photo-1929-1935-metadata-challenge-and-ohs-followup.md`\n'''
    Path(INVENTORY_PATH).write_text(inv,encoding="utf-8")

cap=Path(CAPTURE_PATH).read_text(encoding="utf-8")
marker="\n## Binary ingest completion\n"
if marker not in cap:
    cap += f'''\n## Binary ingest completion\n\nThe exact CCHS catalog object `{TARGET}` was recovered through the public CatalogIt API and its largest non-thumbnail public JPEG derivative was committed as `{IMAGE_PATH}`.\n\n- Repository derivative: {width} × {height}; {byte_count:,} bytes\n- Repository SHA-256: `{sha256}`\n- Steward-upload SHA-256 control: `{STEWARD_SHA256}`\n- Public CCHS record: {hub_url}\n- Evidence-state note: the circa 1929–1935 date remains a project research estimate, not institutional metadata.\n'''
    Path(CAPTURE_PATH).write_text(cap,encoding="utf-8")

record={"catalog":TARGET,"entry_url":entry_url,"hub_url":hub_url,"selected_derivative":derivative,"repository_file":IMAGE_PATH,"repository_image":{"width":width,"height":height,"bytes":byte_count,"sha256":sha256},"steward_upload_control":{"width":STEWARD_WIDTH,"height":STEWARD_HEIGHT,"bytes":STEWARD_BYTES,"sha256":STEWARD_SHA256}}
Path("evidence/source-captures/cchs-c0250-005060-bluff-api.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print(f"Preserved {TARGET} as {IMAGE_PATH}: {width}x{height}, {byte_count} bytes, sha256 {sha256}")
