#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image

ACCOUNT = "4813"
REVIEW = "2026-09-09"
MARKER = "<!-- 2026-09-09-cchs-1918-p267-target-transition -->"

OBJECTS = [
    {
        "catalog": "2008.008.009.016",
        "label": "1918 bluff-at-4th Street Steps",
        "title": "Oregon City from the Bluff at 4th Street Steps",
        "description": "Oregon City from the Bluff at 4th Street Steps. Huntley Drug Store Post Card negative.",
        "date": "1918",
        "medium": "Negative",
        "location_negative": "Society Collection",
        "other_number": "Brewer-Green 16",
        "steward_filename": "Oregon City from the Bluff at 4th Street Steps.jpg",
        "steward_width": 2048,
        "steward_height": 1181,
        "steward_bytes": 884802,
        "steward_sha256": "f41164c211f4934d1b80d769ede9ff898742861f0615b87d1e6f9d987db5025e",
        "slug_name": "1918-bluff-4th-street-steps-target-frontage",
        "visual_note": "Project steward identifies the later-numbered 501/503/505 predecessor frontage and notes that the upper false-front/parapet over the later 505 position is already partly lowered/removed compared with the earlier more uniform roofline across the group.",
    },
    {
        "catalog": "P-267",
        "label": "1924-1928 Arch Bridge bluff view",
        "title": "Oregon City and the Arch Bridge as Seen from Bluff",
        "description": "Oregon City and the Arch Bridge as seen from the Bluff.",
        "date": "1924-1928",
        "medium": "Photographic Paper",
        "location_negative": "[not supplied]",
        "other_number": "[not supplied]",
        "steward_filename": "Oregon City and the Arch Bridge as Seen from Bluff.jpg",
        "steward_width": 2048,
        "steward_height": 1623,
        "steward_bytes": 904513,
        "steward_sha256": "f5c6d00ca21370a82dd125a583fb5634d95c6ac64b1556f24e3b643631e904b2",
        "slug_name": "1924-1928-arch-bridge-bluff-target-frontage",
        "visual_note": "Project steward identifies a later changed state in which the replacement/new 501 structure is present and the neighboring 503/505-area buildings no longer match the 1918 predecessor frontage.",
    },
]


def rd(path):
    return Path(path).read_text(encoding="utf-8")


def wr(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path, marker, block):
    text = rd(path)
    if marker in text:
        return False
    wr(path, text.rstrip() + "\n\n" + block.strip() + "\n")
    return True


def next_id(path, prefix, width):
    vals = [int(v) for v in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    if not vals:
        raise RuntimeError(f"No {prefix} IDs found in {path}")
    return f"{prefix}-{max(vals)+1:0{width}d}"


def next_ids(path, prefix, width, count):
    vals = [int(v) for v in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    if not vals:
        raise RuntimeError(f"No {prefix} IDs found in {path}")
    n = max(vals)
    return [f"{prefix}-{n+i:0{width}d}" for i in range(1, count+1)]


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


def find_match(obj, target):
    if isinstance(obj, dict):
        if catno(obj) == target:
            return obj
        for v in obj.values():
            m = find_match(v, target)
            if m is not None:
                return m
    elif isinstance(obj, list):
        for v in obj:
            m = find_match(v, target)
            if m is not None:
                return m
    return None


def choose_derivative(entry):
    found = []
    for media in entry.get("media", []):
        for key, val in media.get("derivatives", {}).items():
            if not isinstance(val, dict) or not val.get("path"):
                continue
            if "thumbnail" in key.lower():
                continue
            w = int(val.get("width") or 0)
            h = int(val.get("height") or 0)
            if w and h:
                found.append((w*h, w, h, key, val["path"]))
    if not found:
        raise RuntimeError("No public image derivative found")
    found.sort(reverse=True)
    _, w, h, key, url = found[0]
    return {"key": key, "width": w, "height": h, "url": url}


def yaml_add_list_item(path, entity_id, field, item):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise RuntimeError(f"{entity_id} not found in {path}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    # Existing list field.
    fm = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if fm:
        field_abs = m.start() + fm.end()
        after = text[field_abs:end]
        nf = re.search(r"(?m)^    [A-Za-z0-9_]+:\s*", after)
        field_end = field_abs + (nf.start() if nf else len(after))
        field_text = text[field_abs:field_end]
        if re.search(rf"(?m)^\s+-\s+{re.escape(item)}\s*$", field_text):
            return False
        insert = field_end
        text = text[:insert].rstrip("\n") + f"\n      - {item}\n" + text[insert:].lstrip("\n")
    else:
        # Add before end of entity block.
        insert = end
        text = text[:insert].rstrip("\n") + f"\n    {field}:\n      - {item}\n\n" + text[insert:].lstrip("\n")
    p.write_text(text, encoding="utf-8")
    return True


def safe_slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# Avoid duplicate integration if either exact catalog object already exists as a source/media record.
for o in OBJECTS:
    for path in ("evidence/source-register.md", "media/photo-metadata-register.md"):
        if o["catalog"] in rd(path):
            raise SystemExit(f"Catalog object {o['catalog']} already appears in {path}; stop for manual reconciliation.")

SIDS = next_ids("evidence/source-register.md", "S", 3, 2)
EIDS = next_ids("evidence/evidence-register.md", "E", 3, 3)
MIDS = next_ids("media/photo-metadata-register.md", "IMG", 4, 2)
TIDS = next_ids("database/timeline.yml", "T", 3, 2)

records = []
for idx, o in enumerate(OBJECTS):
    target = o["catalog"]
    search_url = "https://api.catalogit.app/api/public/search?" + urllib.parse.urlencode({"query": target, "size": 50})
    search = get_json(search_url)
    match = find_match(search, target)
    if match is None or not match.get("id"):
        raise RuntimeError(f"Exact CCHS catalog object {target} not found")
    entry_url = f"https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{match['id']}"
    entry = get_json(entry_url)
    if catno(entry) != target:
        raise RuntimeError(f"Catalog mismatch for {target}: {catno(entry)}")
    derivative = choose_derivative(entry)
    raw = get_bytes(derivative["url"])
    im = Image.open(BytesIO(raw))
    im.load()
    fmt = (im.format or "").upper()
    if fmt not in {"JPEG", "PNG"}:
        raise RuntimeError(f"Unexpected derivative format {fmt} for {target}")
    ext = ".jpg" if fmt == "JPEG" else ".png"
    mid = MIDS[idx]
    image_path = f"media/photos/early-main-street/{mid}_{o['slug_name']}-cchs-{safe_slug(target)}{ext}"
    Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    Path(image_path).write_bytes(raw)
    slug = entry.get("slug") or match.get("slug")
    hub = f"https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}" if slug else entry_url
    rec = dict(o)
    rec.update({
        "sid": SIDS[idx], "eid": EIDS[idx], "mid": mid, "tid": TIDS[idx],
        "search_url": search_url, "entry_url": entry_url, "hub": hub,
        "derivative": derivative, "repository_file": image_path,
        "repo_width": im.width, "repo_height": im.height, "repo_bytes": len(raw),
        "repo_sha256": hashlib.sha256(raw).hexdigest(), "repo_format": fmt,
    })
    records.append(rec)

r18, rlate = records
EBR = EIDS[2]

# Detailed captures.
for r in records:
    cap = f"evidence/source-captures/{safe_slug(r['catalog'])}-{r['slug_name']}-2026-09-09.md"
    r["capture"] = cap
    if r["catalog"] == "2008.008.009.016":
        visual = f'''## Direct visual review and steward spatial annotation

The supplied photograph and the matching CCHS object were visually reviewed. The image directly shows the 1918 downtown Oregon City streetscape from the bluff/4th Street steps. The later street numbers **501, 503, and 505 are not readable in the photograph itself**.

The project steward identifies the target predecessor frontage using the established Fifth/Main geometry and notes that, in this 1918 state, the **upper false-front/parapet over the later 505 position is already partly missing/lowered compared with the earlier more uniform roofline of the predecessor group**. The image visibly supports an uneven upper facade/roofline in the steward-identified row, but the individual 505 bay assignment is therefore recorded as **attributed steward spatial testimony plus cross-source mapping**, not as a number read from the photograph.

This image is important as a pre-replacement structural control: it shows predecessor-era fabric still present at the steward-identified later 501/503/505 sites in 1918. It does not prove when any surviving present-day building was constructed, who owned the buildings, or what caused the later changes.'''
    else:
        visual = f'''## Direct visual review and steward spatial annotation

The supplied photograph and matching CCHS object were visually reviewed. The photograph directly shows the completed Arch Bridge and the downtown streetscape from the bluff within the CCHS **1924–1928** date range. The later street numbers **501, 503, and 505 are not readable in the photograph itself**.

The project steward identifies the target row and observes that the **new/replacement 501 state is present** and that the neighboring **503/505-area structures no longer match the 1918 predecessor group**. Direct visual comparison supports a materially changed building/roofline state in the target area, but exact individual bay identity is recorded through steward spatial identification plus the project's established map geometry rather than through readable address numbers.

Because the CCHS date is a range, this photograph does not supply an exact construction or replacement year. It corroborates a changed post-1918 target-frontage state; the 1925 Sanborn remains the tighter independent by-1925 map control.'''
    capture = f'''# CCHS {r['catalog']} — {r['title']}

{MARKER}

Reviewed **9 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public CatalogIt object.

Archive IDs: source `{r['sid']}`; evidence `{r['eid']}`; media `{r['mid']}`; timeline `{r['tid']}`. Related buildings/sites: `B-005` (501 Main), `B-001` (503 Main), `B-002` (505 Main).

## Institutional metadata supplied by project steward

- Name/Title: **{r['title']}**
- Entry/Object ID: **{r['catalog']}**
- Description: **{r['description']}**
- Date made: **{r['date']}**
- Medium: **{r['medium']}**
- Location of Negative: **{r['location_negative']}**
- Other Number: **{r['other_number']}**
- Public CCHS record: {r['hub']}
- Public API record: {r['entry_url']}

## Project-steward supplied image provenance

- Original filename: `{r['steward_filename']}`
- Dimensions: **{r['steward_width']} × {r['steward_height']}**
- Bytes: **{r['steward_bytes']:,}**
- SHA-256: `{r['steward_sha256']}`
- Steward observation: **{r['visual_note']}**

## Repository image

- File: `{r['repository_file']}`
- Source: largest public CCHS derivative recovered from exact catalog object `{r['catalog']}`
- Format/dimensions: **{r['repo_format']} — {r['repo_width']} × {r['repo_height']}**
- Bytes: **{r['repo_bytes']:,}**
- SHA-256: `{r['repo_sha256']}`
- Steward-upload byte identity: **{'yes' if r['repo_sha256'] == r['steward_sha256'] else 'no'}**

When the repository derivative differs byte-for-byte from the steward upload, it is retained as the canonical institutional copy of the **same substantive photograph**; the steward upload's exact fingerprint is preserved above to make the duplicate/variant decision auditable.

{visual}

## Evidence classification and limits

- **DOCUMENTED / DIRECT:** the CCHS catalog object, supplied catalog metadata, and the visible overall Oregon City streetscape.
- **VISUALLY VERIFIED:** the photograph itself was inspected.
- **ATTRIBUTED PROJECT-STEWARD SPATIAL TESTIMONY:** the 501/503/505 bay identification and the steward's comparative structural reading.
- **STRONG CROSS-SOURCE INFERENCE:** alignment of those later-numbered sites with the established Sanborn/address geometry.
- **UNRESOLVED:** exact construction/replacement dates for individual 501/503/505 structures, exact ownership, builder, and causation of the changes.

This photograph must not be used alone to infer property ownership, a business transfer, a 1922-fire causal relationship, or uninterrupted building continuity.
'''
    wr(cap, capture)

comparison_path = "evidence/source-captures/1918-to-1925-target-frontage-photographic-structural-bracket-2026-09-09.md"
comparison = f'''# 1918 → 1925 target-frontage photographic / map structural bracket

{MARKER}

Status: **STRUCTURAL TRANSITION BRACKET TIGHTENED; exact individual construction dates remain unresolved.**

Related new sources: `{r18['sid']}` / `{r18['eid']}` / `{r18['mid']}` and `{rlate['sid']}` / `{rlate['eid']}` / `{rlate['mid']}`. Existing map control: `E-020` / `S-021` (1925 Sanborn) and the 1911→1925 geometry reconciliation associated with `E-272`.

## What the new photographs add

The exact CCHS **1918** bluff-at-4th photograph provides a strong pre-change control. The project steward identifies the predecessor frontage at the later 501/503/505 sites and notes a partial lowering/loss of the upper false-front/parapet over the later 505 position. Address numbers are not visible, so the individual bay mapping remains steward-attributed plus cross-source.

CCHS **P-267**, dated **1924–1928**, shows a materially later downtown state. The steward identifies the new/replacement 501 state and replacement/changed structures at the neighboring 503/505 area. The exact exposure year is not supplied.

Independently, the visually reviewed **1925 Sanborn** maps 501, 503, and 505 as separate spaces and differs materially from the controlling 1911 target sheet. Therefore the strongest defensible combined conclusion is:

> **The target frontage underwent material physical replacement/reconfiguration after the photographed 1918 state and by the 1925 Sanborn state.**

This is a tighter structural bracket than the earlier broad 1911→1925 map-only interval. It does **not** prove that all three present-day buildings were erected in a single campaign, nor that the entire current 503 or 505 structure dates to one event.

## Relationship to later c.1919 / c.1920 survey estimates

The City/inventory estimates of approximately **1919 for 503** and **1920 for 505** fall plausibly inside this new photographic/map bracket. The new photographs make those estimates more chronologically plausible, but **do not independently prove those exact years**. Permit, assessor, deed, construction reporting, or other primary event evidence is still required.

## 1922 fire caution

The bracket also overlaps the July 1922 Fifth/Main fire/rebuild sequence, but the photographs do **not** identify the Wolf-owned ignition room, the Gates/Wolf storefront boundary, or prove that the visible 503/505 changes were caused by that fire. Existing 1922 competing models remain unresolved.

## Cross-record propagation decision

This batch warrants structural updates to 501/503/505 building/timeline records and `RL-024`, but no ownership, occupancy, business-sale, or fire-origin claim. No annual year-status change is made.
'''
wr(comparison_path, comparison)

# Source register + YAML.
for r in records:
    append_once("evidence/source-register.md", f"## {r['sid']} —", f'''## {r['sid']} — CCHS {r['catalog']}, {r['title']}
{MARKER}
Type: Primary institutional historic photograph; **VISUALLY VERIFIED** 9 September 2026.  
Institution: Clackamas County Historical Society.  
Catalog ID: `{r['catalog']}`.  
Date: **{r['date']}** per supplied CCHS metadata.  
Repository image: `{r['repository_file']}`.  
Capture: `{r['capture']}`.  
Public record: {r['hub']}  
Related evidence/media/timeline: `{r['eid']}` / `{r['mid']}` / `{r['tid']}`.  
Related buildings: `B-005`, `B-001`, `B-002`.  
Notes: Later street numbers are not readable in the photograph; exact 501/503/505 bay mapping is preserved as project-steward spatial identification plus established cross-source geometry. Exact construction/ownership conclusions are not inferred.''')
    append_once("database/sources.yml", f"  - id: {r['sid']}\n", f'''  - id: {r['sid']}
    name: "CCHS {r['catalog']}, {r['title']}"
    url: "{r['hub']}"
    type: "Primary institutional historic photograph; visually verified 9 September 2026"
    date: "{r['date']}"
    repository_file: "{r['repository_file']}"
    related_evidence: [{r['eid']}]
    related_media: [{r['mid']}]
    related_buildings: [B-005, B-001, B-002]
    notes: "Address numbers are not readable; target-bay identification is steward-attributed plus cross-source geometry. Detailed limits in {r['capture']}."''')

# Evidence register + YAML: direct photo records.
for r in records:
    if r["catalog"] == "2008.008.009.016":
        claim1 = "The 1918 photograph directly documents the downtown bluff-at-4th streetscape; the project steward identifies predecessor frontage at the later 501/503/505 sites."
        claim2 = "The steward identifies the later 505 position as already having a partly lowered/removed upper false-front/parapet relative to the earlier more uniform predecessor roofline; the photo visibly supports an uneven upper-facade state, while exact bay mapping remains cross-source."
    else:
        claim1 = "The 1924-1928 photograph directly documents the later Arch Bridge-era downtown streetscape; the project steward identifies the target 501/503/505 area."
        claim2 = "The steward identifies the new/replacement 501 state and materially changed/replacement neighboring 503/505-area structures compared with 1918; the date range prevents an exact construction year from being inferred."
    append_once("evidence/evidence-register.md", f"## {r['eid']} —", f'''## {r['eid']} — CCHS {r['catalog']} target-frontage photographic state
{MARKER}
Source: `{r['sid']}`; media `{r['mid']}`; capture `{r['capture']}`.  
Type: Primary institutional photographic evidence with project-steward spatial annotation.  
Claims:
- {claim1}
- {claim2}
- No 501/503/505 address number is readable in the image itself; individual target-bay identification is not treated as source-explicit numbering.
Classification: **DOCUMENTED / DIRECT** for photographed streetscape; **ATTRIBUTED STEWARD SPATIAL TESTIMONY + STRONG CROSS-SOURCE INFERENCE** for later-numbered bay mapping and comparative facade interpretation.  
Confidence: **Very High** for object/image/date metadata; High for broad target-row comparative structural state; exact individual construction dates unresolved.  
Related buildings: `B-005`, `B-001`, `B-002`.''')
    append_once("database/evidence.yml", f"  - id: {r['eid']}\n", f'''  - id: {r['eid']}
    name: "CCHS {r['catalog']} target-frontage photographic state"
    type: "Primary institutional photographic evidence with project-steward spatial annotation"
    claims:
      - "{claim1.replace('"', "'")}"
      - "{claim2.replace('"', "'")}"
      - "No 501/503/505 address number is readable in the image itself; individual target-bay identification is not source-explicit numbering."
    confidence: "Very High for object/image/date metadata; High for broad comparative structural state; exact construction dates unresolved"
    related_sources: [{r['sid']}]
    related_media: [{r['mid']}]
    related_buildings: [B-005, B-001, B-002]
    repository_file: "{r['capture']}"''')

# Cross-source structural bracket evidence.
append_once("evidence/evidence-register.md", f"## {EBR} —", f'''## {EBR} — 1918→1925 target-frontage physical-change bracket
{MARKER}
Sources: `{r18['sid']}`, `{rlate['sid']}`; cross-reference existing `E-020` / `S-021` and `E-272`.  
Related record: `{comparison_path}`.  
Claims:
- The 1918 photograph provides a predecessor-era target-frontage state; the later P-267 photograph provides a changed 1924–1928 state.
- The independent 1925 Sanborn supplies the tighter later control and confirms changed storefront/footprint geometry relative to 1911.
- Combined, the evidence supports material target-frontage replacement/reconfiguration **after the photographed 1918 state and by 1925**.
- The City c.1919 (503) and tentative c.1920 (505) estimates are chronologically compatible with this bracket but are not independently proved by the photographs.
- The bracket does not establish a single rebuilding campaign, exact individual construction dates, ownership, builder identity, or a causal link to the July 1922 fire.
Classification: **STRONG CROSS-SOURCE INFERENCE** for the after-1918/by-1925 structural transition bracket.  
Confidence: **High** for the broad transition interval; exact building-by-building event dates unresolved.  
Related buildings: `B-005`, `B-001`, `B-002`.''')
append_once("database/evidence.yml", f"  - id: {EBR}\n", f'''  - id: {EBR}
    name: "1918 to 1925 target-frontage physical-change bracket"
    type: "Cross-source photographic and Sanborn structural inference"
    claims:
      - "1918 provides a predecessor target-frontage state and CCHS P-267 provides a changed 1924-1928 state."
      - "The independent 1925 Sanborn supplies the tighter later control; combined evidence supports material replacement/reconfiguration after the photographed 1918 state and by 1925."
      - "The c.1919 503 and tentative c.1920 505 survey estimates are compatible with the bracket but are not independently proved by it."
      - "No single rebuilding campaign, exact construction date, ownership, builder, or 1922-fire causation is established."
    confidence: "High for broad after-1918/by-1925 transition; individual building dates unresolved"
    related_sources: [{r18['sid']}, {rlate['sid']}, S-021]
    related_evidence: [{r18['eid']}, {rlate['eid']}, E-020, E-272]
    related_media: [{r18['mid']}, {rlate['mid']}]
    related_buildings: [B-005, B-001, B-002]
    repository_file: "{comparison_path}"''')

# Media registers.
for r in records:
    append_once("media/photo-metadata-register.md", f"## {r['mid']} —", f'''## {r['mid']} — CCHS {r['catalog']}, {r['title']}
{MARKER}
- Type: Historic elevated Oregon City streetscape photograph
- CCHS catalog: `{r['catalog']}`
- CCHS title: **{r['title']}**
- CCHS date: **{r['date']}**
- Repository file: `{r['repository_file']}`
- Status: `committed`
- Repository dimensions: **{r['repo_width']} × {r['repo_height']}**; {r['repo_bytes']:,} bytes; SHA-256 `{r['repo_sha256']}`
- Steward original: `{r['steward_filename']}`; {r['steward_width']}×{r['steward_height']}; {r['steward_bytes']:,} bytes; SHA-256 `{r['steward_sha256']}`
- Duplicate/variant handling: repository preserves the institutional CCHS derivative of the same substantive photograph; steward fingerprint retained even if bytes differ.
- Related source/evidence/timeline: `{r['sid']}` / `{r['eid']}` / `{r['tid']}`
- Related buildings: `B-005`, `B-001`, `B-002`
- Interpretation limit: later street numbers are not readable; target-bay mapping and comparative facade reading are steward-attributed plus cross-source geometry.
- Review: `{r['capture']}`''')
    append_once("media/photos/inventory.md", f"### {r['mid']} —", f'''### {r['mid']} — CCHS {r['catalog']}, {r['title']}
- File: `{r['repository_file']}`
- Source/evidence: `{r['sid']}` / `{r['eid']}`
- CCHS: `{r['catalog']}`
- Date: **{r['date']}**
- Key value: structural-state control for the steward-identified 501/503/505 target frontage; see detailed capture for address-mapping limits.''')

# Building Markdown sections and YAML relations.
for bpath, bid, name in [
    ("buildings/501-main.md", "B-005", "501 Main"),
    ("buildings/503-main.md", "B-001", "503 Main"),
    ("buildings/505-main.md", "B-002", "505 Main"),
]:
    append_once(bpath, MARKER, f'''## 1918→1925 photographic structural bracket
{MARKER}

The newly integrated CCHS 1918 bluff photograph (`{r18['sid']}` / `{r18['eid']}` / `{r18['mid']}`) and CCHS P-267 (`{rlate['sid']}` / `{rlate['eid']}` / `{rlate['mid']}`), read with the existing 1925 Sanborn (`E-020`), materially tighten the target-frontage physical-change interval. The project steward maps the visible target row to later 501/503/505 positions; no address numbers are readable in either photograph.

The strongest combined conclusion (`{EBR}`) is that the frontage underwent **material physical replacement/reconfiguration after the photographed 1918 state and by 1925**. For {name}, this narrows the structural-history search but does not prove an exact construction year, single building campaign, ownership, builder, or 1922-fire causation. The c.1919/c.1920 historic-survey estimates remain estimates, not primary event dates.

At the later 505 position specifically, the steward identifies the 1918 upper false-front/parapet as already partly lowered/removed relative to the earlier predecessor roofline; that individual-bay reading remains steward-attributed plus cross-source rather than a directly readable street-number assignment.''')
    for eid in (r18['eid'], rlate['eid'], EBR):
        yaml_add_list_item("database/buildings.yml", bid, "related_evidence", eid)
    for sid in (r18['sid'], rlate['sid']):
        yaml_add_list_item("database/buildings.yml", bid, "related_sources", sid)

# Timeline Markdown/YAML.
append_once("timeline.md", MARKER, f'''## 1918 — CCHS bluff photograph preserves predecessor target-frontage state
{MARKER}

CCHS `{r18['catalog']}` (`{r18['sid']}` / `{r18['eid']}` / `{r18['mid']}`) is cataloged **1918** and shows downtown Oregon City from the bluff at 4th Street steps. The project steward identifies the later 501/503/505 target row and notes partial lowering/loss of the upper false-front/parapet over the later 505 position. Street numbers are not readable, so the bay mapping is steward-attributed plus cross-source. This provides a strong pre-change photographic control, not a precise construction date.

## 1924–1928 — P-267 shows changed target-frontage state

CCHS `P-267` (`{rlate['sid']}` / `{rlate['eid']}` / `{rlate['mid']}`) shows the Arch Bridge-era downtown within a **1924–1928** catalog range. The project steward identifies the new/replacement 501 state and materially changed neighboring 503/505-area structures. Read with the independent 1925 Sanborn, the combined evidence (`{EBR}`) supports a target-frontage physical transition **after the photographed 1918 state and by 1925**. Exact building-by-building construction dates and 1922-fire causation remain unresolved.''')

for r, title, summary in [
    (r18, "1918 — bluff photograph preserves predecessor target-frontage state", "CCHS 2008.008.009.016 is cataloged 1918. The steward identifies the later 501/503/505 target row and a partly lowered/removed upper false-front at the later 505 position; numbers are not readable, so bay mapping is steward-attributed plus cross-source."),
    (rlate, "1924-1928 — P-267 shows changed target-frontage state", "CCHS P-267 shows the Arch Bridge-era downtown. The steward identifies a new/replacement 501 state and changed neighboring 503/505-area structures; exact exposure year and individual construction dates remain unresolved."),
]:
    append_once("database/timeline.yml", f"  - id: {r['tid']}\n", f'''  - id: {r['tid']}
    date: "{r['date']}"
    title: "{title}"
    summary: "{summary}"
    confidence: "Very High for catalog/image state; target-bay mapping steward-attributed plus cross-source"
    related_evidence: [{r['eid']}, {EBR}]
    related_sources: [{r['sid']}]
    related_media: [{r['mid']}]
    related_buildings: [B-005, B-001, B-002]''')

for tpath in ("timelines/501-main.md", "timelines/503-main.md", "timelines/505-main.md"):
    append_once(tpath, MARKER, f'''## 1918→1925 photographic transition bracket
{MARKER}

| Date/state | Evidence | Interpretation |
| --- | --- | --- |
| 1918 | CCHS `{r18['catalog']}` (`{r18['eid']}` / `{r18['mid']}`) | Steward-identified predecessor 501/503/505 target row; later 505 upper false-front/parapet already partly lowered; no readable street numbers. |
| 1924–1928 | CCHS `P-267` (`{rlate['eid']}` / `{rlate['mid']}`) | Steward identifies new/replacement 501 state and changed neighboring 503/505-area structures; exact exposure year unresolved. |
| By 1925 | existing Sanborn `E-020` | Independent changed storefront/footprint geometry. |

Combined `{EBR}`: **material target-frontage replacement/reconfiguration occurred after the photographed 1918 state and by 1925**. This does not establish exact individual construction dates, a single rebuild campaign, ownership, or 1922-fire causation.''')

# Crosswalk, leads, open questions, construction checkpoint, research log.
append_once("indexes/id-crosswalk.md", MARKER, f'''## 1918→1925 target-frontage photographic bracket — 9 September 2026
{MARKER}

| Media/source | Evidence/timeline | Buildings | Meaning |
| --- | --- | --- | --- |
| `{r18['mid']}` / `{r18['sid']}` / CCHS `{r18['catalog']}` | `{r18['eid']}` / `{r18['tid']}` | `B-005`, `B-001`, `B-002` | 1918 predecessor target-row state; 505 false-front change is steward-attributed plus cross-source. |
| `{rlate['mid']}` / `{rlate['sid']}` / CCHS `P-267` | `{rlate['eid']}` / `{rlate['tid']}` | `B-005`, `B-001`, `B-002` | 1924–1928 changed target-row state. |
| Cross-source | `{EBR}` + existing `E-020` / `E-272` | `B-005`, `B-001`, `B-002` | Strong inference: material target-frontage replacement/reconfiguration after 1918 and by 1925; exact individual event dates unresolved. |''')

append_once("evidence/research-leads.md", MARKER, f'''### RL-024 update — 1918→1925 photograph/map bracket
{MARKER}

New CCHS photograph controls `{r18['eid']}` and `{rlate['eid']}`, combined in `{EBR}`, tighten the target physical-change search to **after the photographed 1918 state and by the 1925 Sanborn state**. Continue `RL-024` for the exact building-by-building event dates, permits, assessor/improvement changes, construction reporting, and any 1922-fire relationship. Do not upgrade c.1919 (503) or c.1920 (505) from survey estimates solely because they fall inside the bracket.''')

append_once("evidence/open-questions.md", MARKER, f'''## Structural-date update — 1918→1925 photograph/map bracket
{MARKER}

New CCHS photographic evidence (`{r18['eid']}`, `{rlate['eid']}`) plus the 1925 Sanborn tightens the broad 501/503/505 frontage transition to **after the photographed 1918 state and by 1925** (`{EBR}`). The exact questions remain open: when was each later structure or major component built/rebuilt, was the work one campaign or multiple, and what relationship—if any—did it have to the July 1922 fire? The c.1919 and c.1920 inventory dates remain unproved estimates.''')

append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", MARKER, f'''## 9 September 2026 photographic bracket update
{MARKER}

Two newly supplied CCHS bluff photographs materially improve the structural chronology. The 1918 object `{r18['catalog']}` (`{r18['sid']}` / `{r18['eid']}` / `{r18['mid']}`) preserves the steward-identified predecessor target row, with a partly lowered/removed upper false-front at the later 505 position. CCHS `P-267` (`{rlate['sid']}` / `{rlate['eid']}` / `{rlate['mid']}`), dated 1924–1928, preserves the steward-identified changed/replacement target-row state. With the independent 1925 Sanborn, `{EBR}` tightens the broad physical-change interval to **after the photographed 1918 state and by 1925**.

This does not convert the City's c.1919 503 or tentative c.1920 505 estimates into primary construction dates. It also does not assign the July 1922 fire origin or Gates/Wolf property division to a specific modern-numbered storefront. Continue the underlying permit/assessor/deed/newspaper research.''')

append_once("registers/research-log.md", MARKER, f'''### 2026-09-09 — 1918 and P-267 bluff photographs tighten 501/503/505 structural bracket
{MARKER}

- Integrated CCHS `{r18['catalog']}` as `{r18['sid']}` / `{r18['eid']}` / `{r18['mid']}` / `{r18['tid']}` and CCHS `P-267` as `{rlate['sid']}` / `{rlate['eid']}` / `{rlate['mid']}` / `{rlate['tid']}`.
- Preserved each exact steward-upload filename, dimensions, byte size and SHA-256, and committed the largest public institutional CCHS derivative of the same substantive photograph.
- Recorded steward spatial testimony that the 1918 target row shows a partly lowered/removed upper false-front at the later 505 position and that P-267 shows a new/replacement 501 state plus changed neighboring 503/505-area structures.
- Combined with the independent 1925 Sanborn, registered `{EBR}`: material target-frontage replacement/reconfiguration occurred **after the photographed 1918 state and by 1925**.
- Preserved limits: no readable target address numbers in either photo; no exact construction year, single-campaign conclusion, ownership, builder, or 1922-fire causation inferred. c.1919/c.1920 remain survey estimates.
- Cross-record propagation audited across source/evidence/media registers, building records/YAML, master and address timelines, open questions, RL-024, ID crosswalk, and the 1919–1920 construction checkpoint.''')

print(json.dumps({
    "sources": SIDS, "evidence": EIDS, "media": MIDS, "timeline": TIDS,
    "images": [r["repository_file"] for r in records],
    "comparison": comparison_path,
}, indent=2))
