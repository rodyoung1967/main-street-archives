from pathlib import Path
import re

MARKER = "<!-- 505-shpo-30539-visual-review-2026-09-07 -->"
YMARKER = "# 505-shpo-30539-visual-review-2026-09-07"

SOURCE_NAME = "Oregon SHPO resource 30539 — 505 Main May 2000 Historic Resource Survey Form"
EVIDENCE_OCC_NAME = "May 2000 505 Main survey visually confirms Harr 1945 and Well's 1953 directory-synthesis wording"
EVIDENCE_OWNER_NAME = "May 2000 505 Main survey owner field names Richard and Sheila Wiitanen"

PDF = "records/historic-surveys/505-main-shpo-resource-30539-inventory-form.pdf"
PROV = "records/historic-surveys/505-main-shpo-resource-30539-inventory-form-provenance.md"
CAP = "evidence/source-captures/2000-downtown-survey-1945-harr-source-provenance-gap-2026-09-04.md"
REQUEST = "registers/research-requests/505-1983-historic-inventory-owner-field-request-2026-09-05.md"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return False
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")
    return True


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))
    return True


def next_yaml_id(path, prefix):
    text = read(path)
    nums = [int(x) for x in re.findall(rf"(?m)^\s*- id:\s*{re.escape(prefix)}-(\d{{3,4}})\s*$", text)]
    return max(nums, default=0) + 1


def fmt(prefix, num):
    return f"{prefix}-{num:03d}"


def add_yaml_relation(path, entity_id, key, value):
    text = read(path)
    pattern = re.compile(
        rf"(?ms)^  - id: {re.escape(entity_id)}\s*$.*?(?=^  - id: |\Z)"
    )
    m = pattern.search(text)
    if not m:
        raise SystemExit(f"Entity {entity_id} not found in {path}")
    block = m.group(0)

    if re.search(rf"(?m)^\s*-\s*{re.escape(value)}\s*$", block):
        return False
    inline_key = re.search(rf"(?m)^    {re.escape(key)}:\s*\[([^\]]*)\]\s*$", block)
    if inline_key and re.search(rf"(?<![A-Za-z0-9-]){re.escape(value)}(?![A-Za-z0-9-])", inline_key.group(1)):
        return False

    if inline_key:
        current = inline_key.group(1).strip()
        replacement = f"    {key}: [{current}, {value}]" if current else f"    {key}: [{value}]"
        new_block = block[:inline_key.start()] + replacement + block[inline_key.end():]
    else:
        multi = re.search(rf"(?m)^    {re.escape(key)}:\s*$", block)
        if multi:
            start = multi.end()
            tail = block[start:]
            next_key = re.search(r"(?m)^    [A-Za-z_][A-Za-z0-9_-]*:\s*", tail)
            insert_at = start + (next_key.start() if next_key else len(tail))
            before = block[:insert_at].rstrip("\n")
            after = block[insert_at:].lstrip("\n")
            new_block = before + f"\n      - {value}\n" + after
        else:
            new_block = block.rstrip() + f"\n    {key}:\n      - {value}\n"

    write(path, text[:m.start()] + new_block + text[m.end():])
    return True


def add_markdown_related_id(path, label, value):
    text = read(path)
    pat = re.compile(rf"(?m)^- {re.escape(label)}: (.+)$")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"{label} line not found in {path}")
    if value in m.group(1):
        return False
    new_line = m.group(0) + f", `{value}`"
    write(path, text[:m.start()] + new_line + text[m.end():])
    return True


if MARKER in read("evidence/source-register.md"):
    print("505 SHPO 30539 visual-review integration already present.")
    raise SystemExit(0)

s0 = next_yaml_id("database/sources.yml", "S")
e0 = next_yaml_id("database/evidence.yml", "E")
S_SCAN = fmt("S", s0)
E_OCC = fmt("E", e0)
E_OWNER = fmt("E", e0 + 1)

source_block = f'''{MARKER}
## {S_SCAN} — {SOURCE_NAME}
Type: Official Oregon SHPO-held historic-resource survey form; **ORIGINAL OFFICIAL SCAN, 3/3 PAGES VISUALLY VERIFIED**.  
Resource: **Oregon Historic Sites Database RESOURCE_ID 30539 — 505 Main St / 505 Tavern**.  
Survey/form: Oregon Inventory of Historic Properties — Historic Resource Survey Form; researcher **Michelle L. Dennis**; recorded **May 2000**.  
Official endpoint: https://heritagedata.prd.state.or.us/historic/index.cfm?do=main.loadFile&load=30539.pdf  
Repository PDF: `{PDF}`  
SHA-256: `5c07dbb4582d80a57b477506ae84ac728ae5b909fb1c41f12d1b1d89b1646bd5`  
Visual review: all **3 pages** rendered from the preserved official PDF and inspected 7 September 2026.  
Related evidence/building/businesses/people: `{E_OCC}`, `{E_OWNER}`; `B-002`; `BUS-014`, `BUS-015`; `P-007`, `P-008`.  
Provenance: `{PROV}`.  
Notes:
- Page 1 directly states that **"The 1945 city directory lists Harr's Recreation Center at 505 Main"** and that the building is listed in the **1953 city directory as "Well's Recreation."**
- The same page says the building was apparently used "for this purpose for a number of years"; this is survey-author synthesis and is **not** proof of uninterrupted Harr operation or a direct Harr→Well transfer.
- Page 3 directly lists source classes and bibliography entries including the **1941 Directory of Oregon City**, **1948 Directory of Clackamas County** (the form itself prints "Director of Clackamas County"), Sanborn maps, newspapers, local history files, and the City's **1983 Historic Survey of Downtown Oregon City (individual property files)**. It does **not** identify the exact 1945 or 1953 directory title/page behind those occupancy statements.
- Page 3 owner field directly records **Richard and Sheila Wiitanen**. Treat this as a dated official-survey ownership field, not a recorded deed/conveyance.
'''

source_yaml = f'''{YMARKER}
  - id: {S_SCAN}
    name: "{SOURCE_NAME}"
    url: "https://heritagedata.prd.state.or.us/historic/index.cfm?do=main.loadFile&load=30539.pdf"
    type: "Official Oregon SHPO historic-resource survey form; original scan 3/3 pages visually verified"
    date: "2000-05"
    repository_file: "{PDF}"
    notes: "RESOURCE_ID 30539. Page 1 explicitly reports a 1945 city-directory listing for Harr's Recreation Center at 505 Main and a 1953 city-directory listing for Well's Recreation; page 3 names Richard and Sheila Wiitanen in the owner field and lists source classes/bibliography. Underlying 1945/1953 directory title/page remains unresolved."
    related_evidence: [{E_OCC}, {E_OWNER}]
    related_buildings: [B-002]
    related_businesses: [BUS-014, BUS-015]
    related_people: [P-007, P-008]'''

evidence_block = f'''{MARKER}
## {E_OCC} — {EVIDENCE_OCC_NAME}
Source: `{S_SCAN}`  
Related building/businesses: `B-002`; `BUS-014`, `BUS-015`  
Type: Official historic-resource survey synthesis; original survey scan visually verified  
Claims:
- Page 1 of the May 2000 individual 505 Main form directly states: **"The 1945 city directory lists Harr's Recreation Center at 505 Main."**
- It further states that the building was apparently used for this purpose for a number of years and was listed in the **1953 city directory as "Well's Recreation."**
- Page 3 visually confirms the survey's source classes and bibliography, including the 1941 Oregon City and 1948 Clackamas County Pacific Directory Service volumes and the 1983 Oregon City individual property files.
- The form does **not** supply a title/page for a 1945 directory or a 1953 directory, and its selected bibliography does not identify either volume by those years. Therefore the project has now verified the **survey's exact wording**, not the underlying directory pages.
- No direct Farr→Harr or Harr→Well business-sale, ownership-transfer, or uninterrupted-operation relationship is inferred.
Classification: **DOCUMENTED / DIRECT and VISUALLY VERIFIED for what the May 2000 survey form says; OFFICIAL SECONDARY for the 1945/1953 occupancy chronology; underlying directory pages remain RETRIEVAL GAP / unresolved provenance.**  
Confidence: Very High for the survey wording; Moderate pending original directory pages for the historical occupancy dates.

## {E_OWNER} — {EVIDENCE_OWNER_NAME}
Source: `{S_SCAN}`  
Related building/people: `B-002`; `P-007`, `P-008`  
Type: Official historic-resource survey owner field; original survey scan visually verified  
Claims:
- Page 3 of the May 2000 individual 505 Main survey form directly records **Richard and Sheila Wiitanen** in the owner field.
- This establishes that the official May 2000 survey record treated Richard and Sheila as the 505 property owners by that survey date.
- It does **not** identify the acquisition date, seller, deed number, legal description, purchase terms, or prove the remembered Nesmeth/Nemeth seller spelling.
Classification: **DOCUMENTED / DIRECT for the survey-form owner field; OFFICIAL-SURVEY OWNERSHIP SNAPSHOT, not deed proof of conveyance.**  
Confidence: High for the May 2000 ownership snapshot; exact acquisition mechanics/date remain unresolved.
'''

evidence_yaml = f'''{YMARKER}
  - id: {E_OCC}
    name: "{EVIDENCE_OCC_NAME}"
    type: "Official historic-resource survey synthesis; original scan visually verified"
    claims:
      - "May 2000 individual 505 Main form explicitly says the 1945 city directory lists Harr's Recreation Center at 505 Main."
      - "The same form says the building is listed in the 1953 city directory as Well's Recreation."
      - "Page 3 confirms source classes/bibliography but does not identify the exact 1945 or 1953 directory title/page."
      - "No direct Farr-to-Harr or Harr-to-Well transfer or uninterrupted operation is inferred."
    confidence: "Very High for survey wording; underlying directory pages remain unresolved"
    related_sources: [{S_SCAN}]
    related_buildings: [B-002]
    related_businesses: [BUS-014, BUS-015]
    repository_file: "{PROV}"

  - id: {E_OWNER}
    name: "{EVIDENCE_OWNER_NAME}"
    type: "Official historic-resource survey owner field; original scan visually verified"
    claims:
      - "Page 3 of the May 2000 505 Main survey form records Richard and Sheila Wiitanen in the owner field."
      - "This is an official-survey ownership snapshot by May 2000, not a recorded deed or proof of acquisition date."
    confidence: "High for the May 2000 ownership snapshot; deed and acquisition date remain unresolved"
    related_sources: [{S_SCAN}]
    related_buildings: [B-002]
    related_people: [P-007, P-008]
    repository_file: "{PROV}"'''

append_once("evidence/source-register.md", MARKER, source_block)
append_once("database/sources.yml", YMARKER, source_yaml)
append_once("evidence/evidence-register.md", MARKER, evidence_block)
append_once("database/evidence.yml", YMARKER, evidence_yaml)

prov = read(PROV)
prov = prov.replace(
    "Status: **ORIGINAL OFFICIAL PDF RETRIEVED; VISUAL REVIEW REQUIRED BEFORE PROMOTING SCAN CONTENT.**",
    "Status: **ORIGINAL OFFICIAL PDF RETRIEVED; 3/3 PAGES VISUALLY VERIFIED 7 SEPTEMBER 2026.**",
)
write(PROV, prov)
append_once(PROV, MARKER, f'''{MARKER}
## Visual review completed — 7 September 2026

All **3 pages** of the original preserved Oregon SHPO PDF were rendered directly from `{PDF}` and visually inspected.

### Page 1
The individual form directly identifies **505 Main Street**, gives **c.1920** as the survey construction estimate, historic use/function **Billiards & Cigars Shop**, current name/use **505 Tavern**, and records Michelle L. Dennis / May 2000.

The Statement of Significance visibly states:
- the 1983 survey indicated c.1908, but the survey author places construction between 1911 and 1925, perhaps about 1920;
- the 1916 city directory does not show a business at 505;
- the 1925 Sanborn shows a billiard parlor/cigar shop;
- the 1941 directory does not list a business at 505 but lists Dr. Roy Briggs at 505 1/2;
- **the 1945 city directory lists Harr's Recreation Center at 505 Main**;
- the building was apparently used for this purpose for a number of years and is listed in the **1953 city directory as Well's Recreation**.

These are now **VISUALLY VERIFIED statements of the 2000 survey form**. They remain **official-secondary historical claims** until the cited directory pages are recovered.

### Page 2
The form includes a historic-resource documentation photograph and locator map. The photograph visibly shows the 505 frontage with **THE WHEEL** signage on the neighboring 503 storefront at left. No exact exposure date beyond the survey context is inferred from the image.

### Page 3
The owner field visibly records **Richard and Sheila Wiitanen**. This is an official-survey ownership snapshot by May 2000, not deed proof or an acquisition date.

Checked research-source categories include Sanborn maps, city directories, biographical encyclopedias, newspapers, SHPO files, local histories, and historic photographs. Visible bibliography entries include the 1917 Sohns & Woodbeck directory, the Pacific Directory Service **1941 Directory of Oregon City**, the Pacific Directory Service **1948 Clackamas County** volume (the form visibly prints "Director of Clackamas County"), Sanborn maps, newspapers, **Historic Oregon City (1957)**, and the City's **1983 Historic Survey of Downtown Oregon City (individual property files)**.

The form does **not** identify the exact title/page of a 1945 directory or 1953 directory. Those original pages and the older 1983 property/research file remain the provenance targets.

Canonical source/evidence: `{S_SCAN}` / `{E_OCC}` / `{E_OWNER}`.
''')

append_once(CAP, MARKER, f'''{MARKER}
## 7 September 2026 — individual 505 form recovered and visually verified

The previously targeted **individual May 2000 505 Main Historic Resource Survey Form** has now been recovered from Oregon SHPO **RESOURCE_ID 30539**, preserved at `{PDF}`, and all **3/3 pages were visually inspected** (`{S_SCAN}` / `{E_OCC}` / `{E_OWNER}`).

This materially narrows the provenance gap:
- the form itself explicitly says **"The 1945 city directory lists Harr's Recreation Center at 505 Main"**;
- it explicitly says the property is listed in the **1953 city directory as "Well's Recreation"**;
- page 3 lists the 1941 Oregon City and 1948 Clackamas County directory volumes and the City's 1983 individual property files, but **does not identify the exact 1945 or 1953 directory title/page**.

Therefore the 2000 form is no longer a retrieval target. The remaining high-value provenance targets are:
1. the actual underlying **1945 and 1953 directory pages/title/effective-year controls**;
2. the **1983 505 individual property file**, worksheets/source notes, and any retained directory transcriptions;
3. the 1947–48 Clackamas County Directory and missing 1944–48 municipal/OLCC licensing material for independent transition evidence.

The exact Farr→Harr transition remains unresolved, and no Harr→Well ownership/business-transfer claim is created.
''')

append_once("businesses/harrs-recreation-center.md", MARKER, f'''{MARKER}
## May 2000 individual survey-form provenance now visually verified

The original three-page Oregon SHPO scan for resource **30539 / 505 Main** has now been visually reviewed (`{S_SCAN}` / `{E_OCC}`). Page 1 explicitly states that **"The 1945 city directory lists Harr's Recreation Center at 505 Main."** This upgrades the project's knowledge of the **survey's exact wording**, but not the underlying directory evidence: the form does not identify the exact 1945 directory title/page, and that original page remains unrecovered.

The form then says the building was apparently used for this purpose for a number of years before reporting **Well's Recreation** in the 1953 city directory. Treat that as survey synthesis only; do not infer uninterrupted Harr operation or a direct Harr→Well transfer.
''')

append_once("businesses/wells-recreation.md", MARKER, f'''{MARKER}
## May 2000 individual survey-form provenance now visually verified

The original Oregon SHPO resource **30539** scan has now been visually reviewed (`{S_SCAN}` / `{E_OCC}`). Page 1 explicitly states that the property is listed in the **1953 city directory as "Well's Recreation."** The project's preservation of the apostrophe spelling is therefore now scan-certified as **the 2000 survey form's wording**.

The exact underlying 1953 directory title/page, proprietor, opening/closing dates, and relationship to Harr's Recreation Center remain unresolved. No Harr→Well business transfer is inferred.
''')

replace_once(
    "businesses/business-index.md",
    "| BUS-014 | [Harr's Recreation Center](harrs-recreation-center.md) | 505 Main | 1945 secondary and late-1948 direct Carl R. Harr evidence; distinct from Farr's; exact transition unresolved. |",
    f"| BUS-014 | [Harr's Recreation Center](harrs-recreation-center.md) | 505 Main | May 2000 individual survey scan now visually verifies the survey's explicit 1945-directory wording (`{E_OCC}` / `{S_SCAN}`); late-1948 direct Carl R. Harr evidence remains independent; Farr→Harr transition unresolved. |",
)
replace_once(
    "businesses/business-index.md",
    "| BUS-015 | [“Well's Recreation”](wells-recreation.md) | 505 Main | 1953 City directory synthesis; spelling preserved, original page needed. |",
    f"| BUS-015 | [“Well's Recreation”](wells-recreation.md) | 505 Main | May 2000 individual survey scan visually verifies the survey's explicit 1953-directory wording/spelling (`{E_OCC}` / `{S_SCAN}`); original directory page/proprietor still needed. |",
)

for bid in ("BUS-014", "BUS-015"):
    add_yaml_relation("database/businesses.yml", bid, "related_evidence", E_OCC)
    add_yaml_relation("database/businesses.yml", bid, "related_sources", S_SCAN)

add_markdown_related_id("buildings/505-main.md", "Related evidence", E_OCC)
add_markdown_related_id("buildings/505-main.md", "Related evidence", E_OWNER)
add_markdown_related_id("buildings/505-main.md", "Related sources", S_SCAN)
append_once("buildings/505-main.md", MARKER, f'''{MARKER}
## May 2000 SHPO individual form — visual review

The complete three-page individual 505 Main survey form for Oregon SHPO **RESOURCE_ID 30539** is now preserved and visually verified (`{S_SCAN}`).

For occupancy chronology, page 1 explicitly reports **Harr's Recreation Center** from a "1945 city directory" and **Well's Recreation** from a "1953 city directory" (`{E_OCC}`). This confirms the exact wording of the official secondary synthesis but still does not supply the underlying directory pages or a direct Farr→Harr / Harr→Well transfer.

For property ownership, page 3 records **Richard and Sheila Wiitanen** in the owner field (`{E_OWNER}`). This gives a dated official-survey ownership snapshot by **May 2000**, narrowing the Wiitanen property chronology, but it does not establish the purchase date, seller, deed, or terms.
''')

add_yaml_relation("database/buildings.yml", "B-002", "related_evidence", E_OCC)
add_yaml_relation("database/buildings.yml", "B-002", "related_evidence", E_OWNER)
add_yaml_relation("database/buildings.yml", "B-002", "related_sources", S_SCAN)

for pid, profile in (
    ("P-007", "people/profiles/richard-dick-wiitanen.md"),
    ("P-008", "people/profiles/sheila-wiitanen.md"),
):
    add_yaml_relation("database/people.yml", pid, "related_evidence", E_OWNER)
    add_yaml_relation("database/people.yml", pid, "related_sources", S_SCAN)
    if Path(profile).exists():
        append_once(profile, MARKER, f'''{MARKER}
## May 2000 505 property-owner survey field

The visually reviewed individual Oregon SHPO form for **505 Main / resource 30539** records **Richard and Sheila Wiitanen** in the owner field in May 2000 (`{S_SCAN}` / `{E_OWNER}`). This is an official-survey ownership snapshot, not a deed and not proof of the acquisition date or seller.
''')

replace_once(
    "timelines/505-main.md",
    "| 1945 | **Harr's Recreation Center** reported at 505. | Official secondary; original directory page needed. | `BUS-014`; `E-032` |",
    f"| 1945 | **Harr's Recreation Center** reported at 505. | May 2000 individual SHPO survey scan is now **VISUALLY VERIFIED** and explicitly says a \"1945 city directory\" lists Harr's here; the underlying directory title/page remains unrecovered, so the occupancy date remains official secondary. | `BUS-014`; `E-032`; `{E_OCC}`; `{S_SCAN}` |",
)
replace_once(
    "timelines/505-main.md",
    "| 1953 | **“Well's Recreation”** reported at 505. | Official secondary; spelling/page verification open. | `BUS-015`; `E-032` |",
    f"| 1953 | **“Well's Recreation”** reported at 505. | May 2000 individual SHPO survey scan is now **VISUALLY VERIFIED** and explicitly attributes this wording to a \"1953 city directory\"; the underlying directory page/proprietor remains unresolved. | `BUS-015`; `E-032`; `{E_OCC}`; `{S_SCAN}` |",
)
needle = "| 2009 | Mike Berman states he bought 505 Tavern. |"
timeline = read("timelines/505-main.md")
if f"`{E_OWNER}`" not in timeline:
    idx = timeline.find(needle)
    if idx < 0:
        raise SystemExit("Could not locate 2009 row in timelines/505-main.md")
    row = f"| May 2000 | Individual Oregon SHPO 505 survey records **Richard and Sheila Wiitanen** in the owner field. | **Official-survey ownership snapshot**; not deed proof and does not date the acquisition from Mrs. Nesmeth/Nemeth. | `P-007`, `P-008`; `{E_OWNER}`; `{S_SCAN}` |\n"
    write("timelines/505-main.md", timeline[:idx] + row + timeline[idx:])

bt = read("registers/business-timeline.md")
old_h = "| 1945 (City synthesis) | Harr's Recreation Center | `BUS-014` | `E-032` | Official secondary | Original directory page/citation still needed. |"
new_h = f"| 1945 (City synthesis; May 2000 individual form visually verified) | Harr's Recreation Center | `BUS-014` | `E-032`, `{E_OCC}` | Official secondary chronology; survey wording visually verified | SHPO resource 30539 page 1 explicitly says a \"1945 city directory\" lists Harr's at 505; underlying directory title/page still needed. |"
old_w = "| 1953 (City synthesis) | “Well's Recreation” | `BUS-015` | `E-032` | Official secondary | Original directory page/spelling/proprietor still needed. |"
new_w = f"| 1953 (City synthesis; May 2000 individual form visually verified) | “Well's Recreation” | `BUS-015` | `E-032`, `{E_OCC}` | Official secondary chronology; survey wording visually verified | SHPO resource 30539 page 1 explicitly attributes \"Well's Recreation\" to a 1953 city directory; underlying page/proprietor still needed. |"
if old_h in bt:
    bt = bt.replace(old_h, new_h, 1)
elif new_h not in bt:
    raise SystemExit("Expected Harr business-timeline row not found")
if old_w in bt:
    bt = bt.replace(old_w, new_w, 1)
elif new_w not in bt:
    raise SystemExit("Expected Well business-timeline row not found")
write("registers/business-timeline.md", bt)

append_once("evidence/open-questions.md", MARKER, f'''{MARKER}
### 7 September 2026 — 505 SHPO individual form narrows Farr→Harr→Well provenance, does not close it

The three-page May 2000 individual 505 Main form from Oregon SHPO resource **30539** is now visually verified (`{S_SCAN}` / `{E_OCC}`). It explicitly says a **1945 city directory** lists Harr's Recreation Center at 505 and a **1953 city directory** lists **Well's Recreation**. The actual directory title/page for either year is still unrecovered, so the exact Farr→Harr changeover and Harr→Well transition remain open.

The same form's owner field names **Richard and Sheila Wiitanen** (`{E_OWNER}`), establishing an official-survey ownership snapshot by May 2000. The exact 505 acquisition date, remembered Nesmeth/Nemeth seller identity/spelling, deed, and terms remain open.
''')

append_once("evidence/research-leads.md", MARKER, f'''{MARKER}
### 7 September 2026 — SHPO 30539 recovered; provenance search moves behind the 2000 form

The individual May 2000 505 Main SHPO form is **no longer a retrieval target**: all three pages are preserved and visually verified as `{S_SCAN}` / `{E_OCC}` / `{E_OWNER}`.

For the recreation-business chain, search and retrieval should now target the **sources behind the form**:
1. the actual 1945 and 1953 directory title/page/effective-year controls;
2. the City's **1983 Historic Survey of Downtown Oregon City individual 505 property file**, which the form explicitly lists among its sources;
3. MF-001 / the **1947–48 Clackamas County Directory** (canvassed in 1946) for the Farr→Harr bracket;
4. MF-002 / missing **1944–48 municipal or OLCC license proceedings** for direct transition evidence.

Include spelling variants **Well's / Wells / Well / Welle / Welsh**, but preserve "Well's Recreation" as the exact 2000 survey-form wording unless an original directory page establishes otherwise. Do not infer direct Harr→Well succession from the survey narrative.
''')

append_once(REQUEST, MARKER, f'''{MARKER}
## 7 September 2026 scope update — 2000 individual form obtained

The **May 2000 individual 505 Main survey form has now been obtained directly from Oregon SHPO resource 30539 and visually reviewed in full** (`{S_SCAN}` / `{E_OCC}` / `{E_OWNER}`). Do not request that form again.

The remaining request scope should focus on:
- the older **1982–1983 / 1983-era individual 505 property file**;
- research worksheets, source annotations, correspondence, directory transcriptions/extracts, and prior-record identifiers;
- material identifying the exact source/page behind **Harr's Recreation Center (1945)** and **Well's Recreation (1953)**;
- any underlying owner/assessor source for the 2000 owner field naming Richard and Sheila Wiitanen.

The recovered 2000 form narrows but does not eliminate the cumulative-file request.
''')

append_once("indexes/id-crosswalk.md", MARKER, f'''{MARKER}
## {S_SCAN} / {E_OCC} / {E_OWNER} — Oregon SHPO 30539, 505 Main May 2000 individual survey
- `{S_SCAN}` → visually verified 3-page official SHPO survey scan for `B-002`.
- `{E_OCC}` → `B-002` / `BUS-014` Harr's Recreation Center / `BUS-015` Well's Recreation; exact survey wording verified, underlying 1945/1953 directory pages unresolved.
- `{E_OWNER}` → `B-002` / `P-007` Richard / Dick Wiitanen / `P-008` Sheila Wiitanen; official May 2000 owner-field snapshot, not deed proof.
''')

append_once("registers/research-log.md", MARKER, f'''{MARKER}
### 2026-09-07 — visually verified complete 505 SHPO resource 30539 individual form
- Re-synchronized to current `main` before integration and followed `AGENTS.md` / `RESEARCH-STANDARD.md`.
- Preserved official PDF was rendered and **3/3 pages visually inspected** after successful workflow run.
- Registered `{S_SCAN}` and claim-level `{E_OCC}` / `{E_OWNER}`.
- Page 1 explicitly attributes **Harr's Recreation Center at 505** to a "1945 city directory" and **Well's Recreation** to a "1953 city directory"; original directory pages remain unresolved.
- Page 3 names **Richard and Sheila Wiitanen** in the owner field, providing a May 2000 official-survey ownership snapshot but not a deed/acquisition date.
- Propagation audit completed across 505 building/business/person records, unified/business timelines, open questions, research leads, research-request scope, crosswalk, and YAML mirrors. Root master timeline was reviewed but not changed because the historical chronology dates themselves did not change; the source/evidence state change is carried in the unified 505 and business timelines.
''')

print(f"Integrated {S_SCAN}, {E_OCC}, {E_OWNER}.")
