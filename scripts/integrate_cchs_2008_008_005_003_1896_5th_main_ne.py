from pathlib import Path
import hashlib
import json
import re
import urllib.request
from io import BytesIO
from PIL import Image

ACCOUNT = "4813"
TARGET = "2008.008.005.003"
ENTRY_ID = "82f6f940-9b1e-11eb-b3ef-53e7205a00b4"
ENTRY = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{ENTRY_ID}"
HUB = "https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/oregon-city-1896-5th-and-main-street-looking-ne"
REVIEW = "2026-09-05"
STEWARD = {
    "filename": "Oregon City 1896 - 5th and Main Street Looking NE.jpg",
    "width": 2048,
    "height": 1616,
    "bytes": 1120199,
    "sha256": "37d0c6b6aa607bd8891d2440a095cea802f8e6f116f4dd927982331895668547",
    "orientation_note": "Project steward: on 5th looking north toward 6th.",
}
SOURCE_NAME = "CCHS 2008.008.005.003, Oregon City 1896 - 5th and Main Street Looking NE"
EVIDENCE_NAME = "1896 Fifth/Main photograph anchors Albright cold-storage signage at the Fifth/Main corner and Wilhelm Tell House toward Sixth/Main"


def rd(path):
    return Path(path).read_text(encoding="utf-8")


def wr(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path, marker, block):
    text = rd(path)
    if marker in text:
        return
    wr(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def next_id(path, prefix, width):
    vals = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    if not vals:
        raise SystemExit(f"No {prefix} ids found in {path}")
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


def choose_derivative(entry):
    found = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path"):
                continue
            lk = key.lower()
            if "thumbnail" in lk or lk in {"complementary_color", "dominant_color"}:
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                found.append((w*h, w, h, key, val["path"]))
    if not found:
        raise SystemExit("No public image derivative found")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}


# Duplicate guard across canonical human-readable registers.
for p in ("evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"):
    if TARGET in rd(p):
        print(f"{TARGET} already integrated; no changes needed.")
        raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
MID = next_id("media/photo-metadata-register.md", "IMG", 4)

entry = get_json(ENTRY)
if catno(entry) != TARGET:
    raise SystemExit(f"CCHS entry mismatch: expected {TARGET}, got {catno(entry)}")
der = choose_derivative(entry)
data = get_bytes(der["url"])
if not data.startswith(b"\xff\xd8"):
    raise SystemExit("Selected CCHS derivative is not JPEG")
with Image.open(BytesIO(data)) as im:
    w, h = im.size
nbytes = len(data)
sha = hashlib.sha256(data).hexdigest()

IMAGE = f"media/photos/early-main-street/{MID}_1896-5th-main-looking-ne-cchs-2008-008-005-003.jpg"
Path(IMAGE).parent.mkdir(parents=True, exist_ok=True)
Path(IMAGE).write_bytes(data)
CAP = "evidence/source-captures/cchs-2008-008-005-003-1896-5th-main-looking-ne-signs-addresses-2026-09-05.md"
API = "evidence/source-captures/cchs-2008-008-005-003-1896-5th-main-looking-ne-api-2026-09-05.json"

wr(API, json.dumps({
    "reviewed": REVIEW,
    "catalog": TARGET,
    "entry_url": ENTRY,
    "hub_url": HUB,
    "repository_file": IMAGE,
    "selected_derivative": der,
    "repository_image": {"width": w, "height": h, "bytes": nbytes, "sha256": sha},
    "steward_upload": STEWARD,
    "repository_byte_identical_to_steward_upload": sha == STEWARD["sha256"],
    "entry": entry,
}, indent=2, ensure_ascii=False) + "\n")

capture = f'''# CCHS {TARGET} — Oregon City 1896, Fifth/Main looking northeast/north toward Sixth

Reviewed **5 September 2026** from the project-steward supplied photograph and exact Clackamas County Historical Society CatalogIt object `{TARGET}`.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`.

## Identification and provenance

- CCHS catalog ID: **{TARGET}**
- CCHS title: **Oregon City 1896 - 5th and Main Street Looking NE**
- Public record: {HUB}
- Public API object: {ENTRY}
- Project-steward spatial annotation: **on 5th looking north toward 6th**. This is preserved as steward-supplied orientation context, not silently converted into institutional metadata.

### Project-steward supplied image

- Original filename: `{STEWARD['filename']}`
- Dimensions: **2048 × 1616**
- Bytes: **1,120,199**
- SHA-256: `{STEWARD['sha256']}`

### Canonical repository image

- File: `{IMAGE}`
- Source: largest public derivative from the exact CCHS object, used because repository writes cannot directly ingest the conversation-local binary; the exact steward-upload fingerprint above is retained for provenance.
- Dimensions: **{w} × {h}**
- Bytes: **{nbytes:,}**
- SHA-256: `{sha}`
- Byte-identical to steward upload: **{'yes' if sha == STEWARD['sha256'] else 'no'}**

## Direct sign review

High-resolution visual inspection supports the following readings:

1. **WILHELM TELL HOUSE** — directly readable on the right/east-side block toward the north end of the view.
2. **C. ALBRIGHT'S** and **COLD STORAGE** — directly readable on the prominent arched sign on the right/east side near the foreground. The small middle wording is not relied upon.
3. **Schlitz** — directly readable on the projecting sign on the left/west side.
4. A large left-foreground sale/store sign and several smaller fascia signs contain partial lettering, but their full business names are not secure enough to transcribe from this photograph. They remain unresolved rather than guessed.

## Address / business correlation

### C. Albright's cold-storage sign — strong Fifth/Main anchor

Existing visually verified repository evidence `E-173` / `S-194` states that on **1 March 1907** R. A. Sawyer had purchased **the Meat Business of Charles Albright**, would continue at **the old stand**, and gave the location **5th and Main Sts.** A separate October 1907 record already preserved under `E-123` describes Strebig fresh meats at **Albright's Old Stand, Cor. 5th and Main Sts.**

The 1896 photograph now supplies an independent earlier visual of a **C. ALBRIGHT'S / COLD STORAGE** sign at the steward-mapped Fifth/Main foreground. Together these sources provide a **STRONG CROSS-SOURCE INFERENCE** that the photographed premises is the Charles Albright meat-market/cold-storage stand later remembered in the 1907 Fifth/Main succession records.

This does **not** prove a later numbered address. In particular, the archive must not automatically call the 1896 Albright building **501 Main** merely because later numbering places 501 at Main/Fifth. Other 1907 evidence also places A. J. Surber at 501 Main/Fifth, and room/building boundaries or corner usage may have changed.

### Wilhelm Tell House — Sixth/Main north-end anchor

The photograph directly reads **WILHELM TELL HOUSE** toward the north end of the block. A later primary *Oregon City Enterprise* advertisement dated **25 July 1902** gives the Wilhelm Tell House location as **Sixth and Main Streets** and names A. H. Griessen as proprietor. That later advertisement is a useful independent location anchor for the sign and supports the steward's north-toward-Sixth orientation. It does not establish that Griessen was proprietor in 1896 or assign the building a later numbered address.

Primary newspaper locator: https://oregonnews.uoregon.edu/lccn/sn00063700/1902-07-25/ed-1/seq-5/

### Schlitz sign — probable Bon Ton relationship, not yet an address assignment

A **Schlitz** projecting sign is directly visible on the west/left side near Fifth. A primary *Oregon City Enterprise* advertisement dated **28 September 1894** places **The Bon Ton** on **Main Street, near Fifth** and advertises **Jos. Schlitz Brewing Co.'s Milwaukee beer on draught**. The business/location/product combination makes The Bon Ton a **PROBABLE / WORKING HYPOTHESIS** for the photographed Schlitz-sign premises.

The photograph itself does not read `BON TON`, and the 1894 advertisement does not give a numbered address or side of Main, so no exact storefront number is assigned.

Primary newspaper locator: https://oregonnews.uoregon.edu/lccn/sn00063700/1894-09-28/ed-1/seq-8/

## Implication for 501/503/505 research

This photograph is a valuable **pre-numbering spatial control** for the Fifth-to-Sixth block. The Albright sign strongly anchors a Fifth/Main meat-market premises in the foreground and the Wilhelm Tell House supplies a later-correlated Sixth/Main anchor toward the other end. Those anchors can be used to test the intervening storefront sequence against the 1892 Sanborn and later numbered-address ladder.

The photograph does **not** by itself prove which 1896 walls later became 501, 503, or 505, nor that any photographed 1896 structure survived to the 1922 fire or into the surviving 503/505 buildings. Address continuity and building continuity remain separate questions.

## Evidence classification

- **DOCUMENTED / DIRECT:** exact CCHS object/title; visible `WILHELM TELL HOUSE`, `C. ALBRIGHT'S`, `COLD STORAGE`, and `Schlitz` signage.
- **STRONG CROSS-SOURCE INFERENCE:** photographed Albright cold-storage premises corresponds to the Charles Albright meat-business stand later documented at Fifth/Main in `E-173` and `E-123`.
- **STRONG LOCATION COMPATIBILITY:** Wilhelm Tell House sign is consistent with the 1902 primary advertisement at Sixth/Main and helps anchor the north end of the view.
- **PROBABLE / WORKING HYPOTHESIS:** photographed Schlitz-sign premises is The Bon Ton, based on the 1894 Main-near-Fifth Schlitz advertisement.
- **UNRESOLVED:** exact later 501/503/505 boundaries, exact numbered addresses of these 1896 businesses, full reading of the partial left-foreground signs, and building continuity after 1896.
'''
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} — {SOURCE_NAME}", f'''## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with CCHS catalog identity; **VISUALLY VERIFIED** 5 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{TARGET}`.  
Title/date wording: **Oregon City 1896 - 5th and Main Street Looking NE**.  
Repository image: `{IMAGE}`.  
Capture: `{CAP}`.  
Public record: {HUB}  
Related evidence/media: `{EID}` / `{MID}`; cross-checks `E-173`, `E-123`.  
Related study area: historic 501/503/505 predecessor frontage; exact later numbered boundaries unresolved.  
Notes: `WILHELM TELL HOUSE`, `C. ALBRIGHT'S` / `COLD STORAGE`, and `Schlitz` are directly readable. Steward orientation is on Fifth looking north toward Sixth.''')

append_once("evidence/evidence-register.md", f"## {EID} — {EVIDENCE_NAME}", f'''## {EID} — {EVIDENCE_NAME}
Source: `{SID}`  
Media: `{MID}`  
Type: Primary photographic evidence with cross-source spatial/business correlation  
Claims:
- CCHS `{TARGET}` is titled **Oregon City 1896 - 5th and Main Street Looking NE**; the project steward further identifies the camera as on Fifth looking north toward Sixth.
- `C. ALBRIGHT'S` and `COLD STORAGE` are directly readable on the right/east-side foreground sign; `E-173` and `E-123` independently place Charles Albright's old meat-business stand at Fifth/Main by 1907, creating a strong cross-source site correlation.
- `WILHELM TELL HOUSE` is directly readable toward the north end; a 25 July 1902 primary advertisement independently locates that business at Sixth/Main, supporting the view orientation without proving 1896 proprietorship or a numbered address.
- `Schlitz` is directly readable on the west/left side; an 1894 primary advertisement places The Bon Ton on Main near Fifth and advertises Schlitz beer, making that business a probable photographed-premises candidate rather than a proved identification.
- The photograph does not establish exact later 501/503/505 boundaries or building continuity into 1922 or the surviving structures.
Classification: **DOCUMENTED / DIRECT** for visible signs and CCHS identity; **STRONG CROSS-SOURCE INFERENCE** for Albright's Fifth/Main site; **PROBABLE / WORKING HYPOTHESIS** for the Bon Ton/Schlitz identification; exact numbered-address mapping unresolved.  
Confidence: Very High for readable signs and object identity; High for Albright Fifth/Main correlation; Moderate for Bon Ton identification; unresolved for exact later numbers/building continuity.''')

append_once("media/photo-metadata-register.md", f"## {MID} — CCHS {TARGET}", f'''## {MID} — CCHS {TARGET}, Oregon City 1896 - 5th and Main Street Looking NE
- Type: Historic streetscape photograph
- CCHS object: **{TARGET}**
- CCHS title: **Oregon City 1896 - 5th and Main Street Looking NE**
- Repository file: `{IMAGE}`
- Status: `committed`
- Repository dimensions: **{w} × {h}**; {nbytes:,} bytes; SHA-256 `{sha}`
- Steward original: `{STEWARD['filename']}`; 2048×1616; 1,120,199 bytes; SHA-256 `{STEWARD['sha256']}`
- Steward orientation: **on 5th looking north toward 6th**
- Visual note: Wilhelm Tell House; C. Albright's / Cold Storage; Schlitz signs readable. Exact later 501/503/505 storefront boundaries remain unresolved.
- Related source/evidence: `{SID}` / `{EID}`''')

append_once("media/photos/inventory.md", f"### {MID} — CCHS {TARGET}", f'''### {MID} — CCHS {TARGET}, 1896 Fifth/Main looking NE
- File: `{IMAGE}`
- Source/evidence: `{SID}` / `{EID}`
- Date/title: **1896** in institutional title
- Status: committed; readable Albright cold-storage, Wilhelm Tell House and Schlitz signage; exact later numbered-address mapping unresolved.''')

append_once("media/photos/early-main-street/README.md", f"`{MID}` — 1896 Fifth/Main looking NE", f'''- `{MID}` — 1896 Fifth/Main looking NE, CCHS `{TARGET}`: `{IMAGE}`. Directly readable `C. ALBRIGHT'S` / `COLD STORAGE`, `WILHELM TELL HOUSE`, and `Schlitz` signs. Albright has a strong cross-source Fifth/Main site bridge through `E-173`/`E-123`; exact later 501/503/505 boundaries remain unresolved.''')

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f'''| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `{IMAGE}`; `{CAP}` | 1896 Fifth/Main view; visible Albright cold-storage, Wilhelm Tell House and Schlitz signs. Albright strongly correlates to later Fifth/Main old-stand evidence; exact later 501/503/505 numbers unresolved. |''')

append_once("evidence/open-questions.md", "### 5 September 2026 — 1896 Albright/Wilhelm sign-map question", f'''### 5 September 2026 — 1896 Albright/Wilhelm sign-map question
CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) provides a new pre-numbering Fifth/Main spatial control. `C. ALBRIGHT'S` / `COLD STORAGE` is visibly on the steward-mapped Fifth/Main foreground and strongly correlates with `E-173`/`E-123` Albright-old-stand evidence; Wilhelm Tell House provides a north-end Sixth/Main compatibility anchor. **Open:** align the photograph to the 1892 Sanborn and later exact-number ladder before assigning any photographed 1896 bay to modern 501, 503 or 505.''')

append_once("evidence/research-leads.md", "### 1896 Fifth/Main sign-to-address alignment", f'''### 1896 Fifth/Main sign-to-address alignment
CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) now gives two strong block anchors: Albright's cold-storage/meat premises at the Fifth/Main foreground and Wilhelm Tell House toward the Sixth/Main end. Next compare the visible party walls/storefront widths with the 1892 Sanborn, then test the later 1907–1912 address ladder. Do not back-project 501/503/505 numbers solely from the photograph.''')

append_once("registers/address-register.md", f"1896 photograph — C. Albright's cold-storage sign", f'''| Fifth/Main foreground; no number (1896 photograph) | C. Albright's cold-storage/meat premises | `{EID}` with later `E-173` / `E-123` | **Strong cross-source intersection/site correlation**: photographed sign reads `C. ALBRIGHT'S` / `COLD STORAGE`; later records call Charles Albright's meat-business location/old stand Fifth/Main. Exact later number and building continuity unresolved. |''')

append_once("evidence/E-173-1907-sawyer-albright-meat-fifth-main.md", "## 1896 photographic predecessor cross-check", f'''## 1896 photographic predecessor cross-check

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows **C. ALBRIGHT'S** and **COLD STORAGE** signage in the project-steward mapped Fifth/Main foreground of an institutional-title **1896** streetscape. This is independent earlier photographic support for the Albright business/site that this 1907 advertisement calls Sawyer's purchased predecessor and **old stand** at Fifth/Main. Exact later street number and 1896-to-1907 building continuity remain unresolved.''')

append_once("registers/research-log.md", f"CCHS {TARGET} 1896 Fifth/Main sign-address photo", f'''### 2026-09-05 — CCHS {TARGET} 1896 Fifth/Main sign-to-address photograph
- Integrated the steward-supplied scene as `{MID}` / `{SID}` / `{EID}`.
- Preserved steward original fingerprint: `{STEWARD['filename']}`, 2048×1616, 1,120,199 bytes, SHA-256 `{STEWARD['sha256']}`.
- Direct visual reads: `C. ALBRIGHT'S` / `COLD STORAGE`, `WILHELM TELL HOUSE`, and `Schlitz`.
- Cross-checked Albright against existing `E-173`/`E-123` Fifth/Main old-stand evidence; classified the exact numbered address as unresolved.
- Preserved Wilhelm Tell House at Sixth/Main (1902 primary-ad compatibility) and The Bon Ton/Schlitz (1894 Main-near-Fifth ad) as location/identity correlations with explicit uncertainty.
- No annual research-status certification changed.''')

# Structured source/evidence records. Names exactly match the Markdown headings.
append_once("database/sources.yml", f"  - id: {SID}\n", f'''  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "{HUB}"
    repository_file: "{IMAGE}"
    notes: "Primary CCHS photograph, visually verified; steward orientation on Fifth looking north toward Sixth. Visible Albright cold-storage, Wilhelm Tell House and Schlitz signage; exact later numbered-address mapping unresolved."
    related_evidence: [{EID}]
    related_media: [{MID}]''')

append_once("database/evidence.yml", f"  - id: {EID}\n", f'''  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: "Primary photographic evidence with cross-source spatial/business correlation"
    claims:
      - "C. ALBRIGHT'S and COLD STORAGE are directly readable; existing E-173/E-123 independently place Charles Albright's old meat-business stand at Fifth/Main."
      - "WILHELM TELL HOUSE is directly readable toward the north end and is compatible with a 1902 primary advertisement locating that business at Sixth/Main."
      - "Schlitz is directly readable; an 1894 Main-near-Fifth Bon Ton advertisement for Schlitz beer makes The Bon Ton a probable, not proved, photographed-premises identification."
      - "Exact later 501/503/505 boundaries and building continuity remain unresolved."
    confidence: "Very High for visible signs/object identity; High for Albright Fifth/Main correlation; Moderate for Bon Ton identification; exact numbered addresses unresolved."
    related_sources: [{SID}]
    related_evidence: [E-173, E-123]
    repository_file: "{CAP}"''')

print(f"Integrated {TARGET} as {MID} / {SID} / {EID}")
