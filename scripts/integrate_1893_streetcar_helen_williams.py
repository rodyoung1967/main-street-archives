from pathlib import Path
import base64, hashlib, json, re, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image

REVIEW_DATE = "2026-09-04"
STEWARD_FILENAME = "Oregon City 1893 - Streetcar Helen - Oregon City's First Streetcar.jpg"
STEWARD_WIDTH = 2048
STEWARD_HEIGHT = 1332
STEWARD_BYTES = 1159631
STEWARD_SHA256 = "db0f1a09d0394c33adc313628091ed418832eaefdb46ab326c6485c384cf6f03"
ACCOUNT_ID = "4813"


def read(p): return Path(p).read_text(encoding="utf-8")
def write(p, s):
    q=Path(p); q.parent.mkdir(parents=True, exist_ok=True); q.write_text(s, encoding="utf-8")
def append_once(p, marker, block):
    s=read(p)
    if marker in s: return
    write(p, s.rstrip()+"\n\n"+block.rstrip()+"\n")
def next_id(path, prefix, width):
    nums=[int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    return f"{prefix}-{max(nums)+1:0{width}d}"
def get_json(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r: return json.load(r)
def get_bytes(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 Main-Street-Archive/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r: return r.read()
def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values(): yield from walk(v)
    elif isinstance(obj, list):
        for v in obj: yield from walk(v)
def textish(d):
    vals=[]
    for k,v in d.items():
        if isinstance(v,str): vals.append(v)
        elif isinstance(v,dict):
            for kk in ("value_text","display_value","name","title","description"):
                if isinstance(v.get(kk),str): vals.append(v[kk])
    return " ".join(vals)
def catalog_number(d):
    try: return d["properties"]["hasCatalogNumber"]["value_text"]
    except Exception: return None
def choose_derivative(entry):
    c=[]
    for m in entry.get("media",[]):
        for key,val in (m.get("derivatives") or {}).items():
            if not isinstance(val,dict) or not val.get("path") or "thumbnail" in key: continue
            w=int(val.get("width") or 0); h=int(val.get("height") or 0)
            if w and h: c.append((w*h,w,h,key,val["path"]))
    if not c: return None
    c.sort(reverse=True); _,w,h,key,url=c[0]
    return {"width":w,"height":h,"key":key,"url":url}

# Do not duplicate an already completed integration.
for p in ["media/photo-metadata-register.md","evidence/source-register.md","evidence/evidence-register.md"]:
    if "Streetcar Helen" in read(p) or STEWARD_SHA256 in read(p):
        print("Helen photograph already integrated; nothing to do.")
        raise SystemExit(0)

SOURCE_ID=next_id("evidence/source-register.md","S",3)
EVIDENCE_ID=next_id("evidence/evidence-register.md","E",3)
MEDIA_ID=next_id("media/photo-metadata-register.md","IMG",4)

# Prefer exact institutional CatalogIt object and its largest public derivative.
entry=None; entry_url=None; hub_url=None; derivative=None; image_data=None
queries=["Helen", "First Street Car", "streetcar Oregon City 1893"]
for q in queries:
    try:
        search_url="https://api.catalogit.app/api/public/search?"+urllib.parse.urlencode({"query":q,"size":100})
        data=get_json(search_url)
        candidates=[]
        for d in walk(data):
            t=textish(d).lower()
            if "helen" in t and ("street car" in t or "streetcar" in t or "1893" in t):
                if d.get("id"): candidates.append(d)
        if not candidates: continue
        match=candidates[0]
        eid=match.get("id")
        entry_url=f"https://api.catalogit.app/api/public/accounts/{ACCOUNT_ID}/entries/{eid}"
        entry=get_json(entry_url)
        derivative=choose_derivative(entry)
        if derivative:
            image_data=get_bytes(derivative["url"])
            if image_data.startswith(b"\xff\xd8"):
                slug=entry.get("slug") or match.get("slug")
                if slug: hub_url=f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}"
                break
    except Exception as exc:
        print("CatalogIt query failed:",q,exc)
        entry=None; derivative=None; image_data=None

# Technical fallback: reconstruct the staged reduced derivative if CatalogIt cannot be reached.
if not image_data:
    parts=["scripts/.helen_payload/part00.b64","scripts/.helen_payload/part01_02.b64","scripts/.helen_payload/part03_04.b64","scripts/.helen_payload/part05_06.b64","scripts/.helen_payload/part07_08.b64","scripts/.helen_payload/part09_10.b64"]
    if not all(Path(p).exists() for p in parts):
        raise SystemExit("Neither an institutional derivative nor the staged fallback payload is available.")
    image_data=base64.b64decode("".join(read(p).strip() for p in parts))
    derivative={"url":None,"key":"staged steward derivative","width":None,"height":None}

img=Image.open(BytesIO(image_data)); repo_w,repo_h=img.size
repo_sha=hashlib.sha256(image_data).hexdigest(); repo_bytes=len(image_data)
repo_path=f"media/photos/early-main-street/{MEDIA_ID}_1893-streetcar-helen-sixth-main-ee-williams.jpg"
Path(repo_path).parent.mkdir(parents=True,exist_ok=True); Path(repo_path).write_bytes(image_data)

catalog_id=catalog_number(entry) if entry else None
catalog_title=None
if entry:
    catalog_title=textish(entry)[:500]
source_capture="evidence/source-captures/1893-streetcar-helen-sixth-main-ee-williams-2026-09-04.md"

capture=f'''# 1893 Streetcar Helen at Sixth/Main — E. E. Williams storefront evidence

Reviewed **4 September 2026** from the project-steward supplied photograph and, when available, the matching Clackamas County Historical Society public catalog object/derivative.

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; image `{MEDIA_ID}`.

## Steward photograph

- Original filename: `{STEWARD_FILENAME}`
- Steward dimensions: **{STEWARD_WIDTH} × {STEWARD_HEIGHT}**
- Steward bytes: **{STEWARD_BYTES:,}**
- Steward SHA-256: `{STEWARD_SHA256}`
- Scene identification: **First street car “Helen” into Oregon City at Sixth and Main Street, 1893**. This wording is corroborated by Oregon City's municipal-elevator historical display, which credits the photograph to the Clackamas County Historical Society.

## Repository image

- File: `{repo_path}`
- Dimensions: **{repo_w} × {repo_h}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Institutional catalog number recovered: **{catalog_id or 'not recovered in automated pass'}**
- Catalog API: {entry_url or 'not recovered'}
- Catalog public page: {hub_url or 'not recovered'}
- Image-source relation: {'largest public CCHS derivative recovered from the matching catalog entry' if entry else 'technical reduced derivative reconstructed from the steward-supplied image payload; the exact steward original remains preserved by filename/dimensions/bytes/SHA-256 metadata'}.

## Direct visual observations

The photograph looks south along Main Street from the Sixth Street area. The electric streetcar **Helen** occupies the foreground tracks. Commercial storefronts line both sides of Main.

On the **right/east side of Main**, the storefront lettering **E. E. WILLIAMS** is directly legible. Farther south on the same side a large **DRUGS** sign is also directly legible, but this photograph alone does not safely resolve the druggist/business name.

The E. E. Williams reading is particularly important because the separately reviewed **1895 Welcome Arch** photograph (`S-215` / `E-195` / `IMG-0744`) independently shows **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** on the right-hand predecessor frontage later associated spatially with 501/503/505 Main. The 1893 photograph therefore supplies an earlier visual continuity point for the named Williams business on this Main Street side/frontage.

## Evidence classification and limits

- **DOCUMENTED / DIRECT:** `E. E. WILLIAMS` is visibly readable in the 1893 photograph.
- **DOCUMENTED / DIRECT:** a large `DRUGS` sign is visibly readable farther south on the same side.
- **STRONG SPATIAL CONTEXT:** the photograph is identified as Sixth/Main and looks south toward Fifth; the later odd-numbered Fifth-to-Sixth frontage is therefore on the right/east side.
- **PROBABLE / WORKING HYPOTHESIS:** correlating the Williams storefront to the predecessor frontage later numbered 501/503/505.
- **UNRESOLVED:** which individual later number (501, 503, or 505) corresponds to the Williams storefront. No later street number is readable in the 1893 photograph, and Oregon City's formal numbering program postdates the image.
- Do **not** infer surviving-building continuity from 1893 to the 1922 rebuild or present buildings without independent structural evidence.

## Best next comparison

Align the Williams storefront and adjacent party walls against the 1892 and 1900 Sanborn sheets and the 1895 Welcome Arch view. The repeated **E. E. Williams** identification across the 1893 and 1895 photographs should materially improve storefront-to-lot alignment.
'''
write(source_capture,capture)

append_once("evidence/source-register.md",f"## {SOURCE_ID} —",f'''## {SOURCE_ID} — 1893 Streetcar Helen at Sixth/Main photograph
Type: Historic photograph / institutional-photo evidence
Date: 1893
Location: Sixth and Main, Oregon City, Oregon
Repository image: `{repo_path}`
Capture: `{source_capture}`
Steward original: `{STEWARD_FILENAME}`; {STEWARD_WIDTH}×{STEWARD_HEIGHT}; SHA-256 `{STEWARD_SHA256}`.
Finding: direct visual review reads **E. E. WILLIAMS** on the right/east Main Street storefront and **DRUGS** farther south. The Williams sign provides an earlier visual comparison to the independently transcribed 1895 E. E. Williams grocery sign (`S-215`/`E-195`). Exact later 501/503/505 assignment remains unresolved.''')

append_once("evidence/evidence-register.md",f"## {EVIDENCE_ID} —",f'''## {EVIDENCE_ID} — 1893 E. E. Williams storefront visible in Streetcar Helen photograph
Source: `{SOURCE_ID}`
Media: `{MEDIA_ID}`
Classification: **DOCUMENTED / DIRECT** for visible `E. E. WILLIAMS`; **PROBABLE / WORKING HYPOTHESIS** for assignment to a specific later 501/503/505 storefront.
Claim: The 1893 Sixth/Main streetcar photograph visibly names **E. E. WILLIAMS** on the east/right side of Main and visibly shows a separate **DRUGS** sign farther south. Together with the 1895 Welcome Arch transcription (`E-195`), this establishes a two-date photographic anchor for E. E. Williams on the same target-side Main Street frontage, while leaving the exact later numbered bay unresolved.
Capture: `{source_capture}`.''')

append_once("media/photo-metadata-register.md",f"## {MEDIA_ID} —",f'''## {MEDIA_ID} — 1893 Streetcar Helen at Sixth/Main; E. E. Williams visible
- Type: Historic street-level photograph
- Date: **1893**
- Location: **Sixth and Main, Oregon City; looking south along Main toward Fifth**
- Source/Evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`
- Repository file: `{repo_path}`
- Repository dimensions: **{repo_w} × {repo_h}**
- Repository bytes: **{repo_bytes:,}**
- Repository SHA-256: `{repo_sha}`
- Steward original filename: `{STEWARD_FILENAME}`
- Steward original dimensions/bytes/SHA-256: **{STEWARD_WIDTH} × {STEWARD_HEIGHT}**, **{STEWARD_BYTES:,} bytes**, `{STEWARD_SHA256}`
- Direct signage: **E. E. WILLIAMS**; separate **DRUGS** sign farther south.
- Interpretation limit: do not assign Williams to later 501 vs 503 vs 505 until Sanborn/photo alignment resolves the individual storefront boundary.
- Review: `{source_capture}`.''')

append_once("media/photos/inventory.md",f"### {MEDIA_ID} —",f'''### {MEDIA_ID} — 1893 Streetcar Helen at Sixth/Main
- File: `{repo_path}`
- Source/evidence: `{SOURCE_ID}` / `{EVIDENCE_ID}`
- Steward original: `{STEWARD_FILENAME}`; 2048×1332; SHA-256 `{STEWARD_SHA256}`.
- Direct visual finding: **E. E. WILLIAMS** is legible on the right/east Main Street storefront; **DRUGS** is legible farther south.
- Comparison value: earlier anchor for the E. E. Williams grocery sign independently visible in the 1895 Welcome Arch photograph; exact later 501/503/505 bay remains unresolved.''')

append_once("registers/research-log.md","## 4 September 2026 — 1893 Streetcar Helen signage re-review",f'''## 4 September 2026 — 1893 Streetcar Helen signage re-review

- Recovered/integrated the steward-supplied **1893 Streetcar Helen** photograph at Sixth/Main as `{MEDIA_ID}` / `{SOURCE_ID}` / `{EVIDENCE_ID}`.
- Enlarged visual review directly reads **E. E. WILLIAMS** on the right/east Main Street storefront and a separate **DRUGS** sign farther south.
- This adds a 1893 visual anchor for the same **E. E. Williams** business independently read in the 1895 Welcome Arch photograph (`IMG-0744` / `E-195`).
- Exact assignment of the Williams storefront to later **501, 503, or 505** remains unresolved pending 1892/1900 Sanborn and photo alignment.''')

append_once("maps/sanborn-comparison-503-505-507.md","1893 Streetcar Helen / E. E. Williams comparison",f'''## 1893 Streetcar Helen / E. E. Williams comparison

`{SOURCE_ID}` / `{EVIDENCE_ID}` / `{MEDIA_ID}` adds a fixed **1893 Sixth/Main looking-south** street-level comparison. The right/east storefront directly reads **E. E. WILLIAMS**, while the 1895 Welcome Arch image (`S-215` / `E-195` / `IMG-0744`) independently reads **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** on the target-side predecessor frontage. Use the repeated Williams sign, party walls, roof forms, facade widths and the 1892/1900 Sanborn geometry to resolve the individual later 501/503/505 bay. Do not backdate the later street numbers or infer physical continuity solely from the matching business name.''')

# Remove temporary staged reduced-payload fragments after the canonical photo is created.
for p in Path("scripts/.helen_payload").glob("*.b64") if Path("scripts/.helen_payload").exists() else []:
    p.unlink()
try: Path("scripts/.helen_payload").rmdir()
except OSError: pass

print(f"Integrated {MEDIA_ID} / {SOURCE_ID} / {EVIDENCE_ID}: {repo_path}")
