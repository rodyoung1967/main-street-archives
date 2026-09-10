#!/usr/bin/env python3
from pathlib import Path
import re

DATE_MARKER = "<!-- 1912 Jan 19 Courier pages 5-8 visual review — 2026-09-09 -->"
YAML_MARKER = "# 1912 Jan 19 Courier pages 5-8 visual review — 2026-09-09"
CAPTURE = "evidence/source-captures/1912-courier-jan-19-pages-5-8-visual-review-2026-09-09.md"
BINARY_COMMIT = "7b9e00c697da21f6caea5bb696055b0d910c1ed6"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def append_once(path, marker, block):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text, encoding="utf-8")
    return True


def next_id(path, prefix):
    nums = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums:
        raise RuntimeError(f"No {prefix} IDs found in {path}")
    return f"{prefix}-{max(nums)+1:03d}"


def find_person_id(name):
    text = read("database/people.yml")
    # Find an exact name field within a person block.
    for m in re.finditer(r"(?ms)^  - id: (P-\d+)\n(.*?)(?=^  - id: |\Z)", text):
        block = m.group(2)
        nm = re.search(r"(?m)^    name:\s*[\"']?(.+?)[\"']?\s*$", block)
        if nm and nm.group(1).strip().strip('"\'') == name:
            return m.group(1)
    return None


def allocate_person_ids(names):
    result = {}
    used = [int(x) for x in re.findall(r"\bP-(\d+)\b", read("people/people-index.md"))]
    n = max(used) if used else 0
    for name in names:
        found = find_person_id(name)
        if found:
            result[name] = found
        else:
            n += 1
            result[name] = f"P-{n:03d}"
    return result


def update_yaml_relation(path, entity_id, field, value):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)", text)
    if not m:
        raise RuntimeError(f"Could not find {entity_id} in {path}")
    block = m.group(0)
    inline = re.search(rf"(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$", block)
    if inline:
        vals = [v.strip() for v in inline.group(1).split(",") if v.strip()]
        if value in vals:
            return False
        vals.append(value)
        replacement = f"    {field}: [" + ", ".join(vals) + "]"
        block = block[:inline.start()] + replacement + block[inline.end():]
    else:
        lines = block.splitlines(keepends=True)
        idx = None
        for i, line in enumerate(lines):
            if re.match(rf"^    {re.escape(field)}:\s*$", line.rstrip("\n")):
                idx = i
                break
        if idx is None:
            if not block.endswith("\n"):
                block += "\n"
            block += f"    {field}: [{value}]\n"
        else:
            j = idx + 1
            vals = []
            item_indent = None
            while j < len(lines):
                im = re.match(r"^(\s*)-\s*(.+?)\s*\n?$", lines[j])
                if not im or len(im.group(1)) < 4:
                    break
                item_indent = item_indent or im.group(1)
                vals.append(im.group(2).strip())
                j += 1
            if value in vals:
                return False
            indent = item_indent or "    "
            lines.insert(j, f"{indent}- {value}\n")
            block = "".join(lines)
    text = text[:m.start()] + block + text[m.end():]
    p.write_text(text, encoding="utf-8")
    return True


def replace_once(path, old, new, required=True):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if required:
            raise RuntimeError(f"Expected text not found in {path}: {old[:80]!r}")
        return False
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf-8")
    return True


if Path(CAPTURE).exists():
    print("Capture already exists; refusing duplicate integration.")
    raise SystemExit(0)

S = next_id("evidence/source-register.md", "S")
E = next_id("evidence/evidence-register.md", "E")
people = allocate_person_ids(["Percy Cross", "A. E. Wilmot", "Milton Price"])
P_CROSS = people["Percy Cross"]
P_WILMOT = people["A. E. Wilmot"]
P_PRICE = people["Milton Price"]

capture = f'''# 19 January 1912 Oregon City Courier — pages 5–8 visual review

{DATE_MARKER}

Date reviewed: **9 September 2026**  
Status: **VISUALLY VERIFIED — 4/4 supplied pages; 19 January issue now 8/8 visually verified.**  
Annual status: **1912 IN PROGRESS**.

Archive IDs: source `{S}`; evidence `{E}`; people `{P_CROSS}` Percy Cross, `{P_WILMOT}` A. E. Wilmot, `{P_PRICE}` Milton Price.

## Method and preservation

The project steward supplied printed pages **5, 6, 7, and 8** from the 19 January 1912 *Oregon City Courier*. Each actual PDF page image was rendered and visually inspected; OCR/extracted text was used only as a discovery aid. Visible mastheads/page numbers confirm all four pages belong to the same issue.

The exact supplied bytes match the canonical Oregon Historic Newspapers PDF derivatives and are physically preserved in the repository by commit `{BINARY_COMMIT}`:

| Uploaded filename | Printed page | SHA-256 | Repository file |
| --- | ---: | --- | --- |
| `Courier Jan 19, 1912 p5.pdf` | 5 | `d7419216d8a39ecfdd726302590ab365f2d7074beac327083c3b84a1c48ddce6` | `newspapers/oregon-city-courier/1912-01-19-page-5.pdf` |
| `Courier Jan 19, 1912 p6.pdf` | 6 | `53b2c8b4c8b03036fed8a8cc04f18a895dc6fc980ecbc8c052ab7913b2a61300` | `newspapers/oregon-city-courier/1912-01-19-page-6.pdf` |
| `Courier Jan 19, 1912 p7.pdf` | 7 | `fd88d8623b8203ba49ece2f2c31faf0a8f826569543b18b69d1ce02d1054f444` | `newspapers/oregon-city-courier/1912-01-19-page-7.pdf` |
| `Courier Jan 19, 1912 p8.pdf` | 8 | `bc4bdb274d1d0530e087da7a01b3f0dfc832ef1174ccd6cfba53e4ec89795a62` | `newspapers/oregon-city-courier/1912-01-19-page-8.pdf` |

Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/

Pages 1–4 were already visually verified and preserved as `S-307`. With this batch, the issue is now **8/8 VISUALLY VERIFIED**.

## Page-by-page screening

### Page 5

No source-explicit 501/503/505/507/509/511 Main occupant, ownership, business-transition, construction, demolition, move, sale, or fire claim was found.

Useful context retained without target-block inference:
- a local item says **Carlton Harding** spent Sunday in Oregon City with his parents, **Mr. and Mrs. George Harding**. The article does not print George's middle initial, occupation, or address, so this is **not merged automatically with `P-001` George A. Harding**;
- Clyde & Surfus advertises at **1003 Main St.**;
- Larsen & Company advertises at the **corner of Tenth and Main**;
- Burmeister & Andresen gives **Suspension Bridge Corner**;
- local news reports a bungalow under construction at First and Center and rain damage to the new St. Paul's church foundation trenches.

These are city/address/context controls only.

### Page 6

No defensible target-frontage claim was found. A professional advertisement directly places **Straight & Salisbury at 720 Main St.**; other professional and legal notices do not establish a 501–511 Main event.

### Page 7 — Milton Price and Farr Bros. context

The County Court jury list says taxpayers were drawn from the Clackamas County assessment roll and, under **“Oregon City, Oregon, No. 1,”** prints **“Milton Price, pool hall.”** This is direct, visually verified wording associating `{P_PRICE}` Milton Price with the descriptor/occupation **pool hall** in that jury-list context.

Limits: the page does **not** state that Price owned, operated, or worked at a particular pool hall; it prints no trade name or address. Do not merge him with H. N. / H. H. Smith, the 503 Main pool hall, Clem Dollar, A. Leland, or any later 505 pool-hall chain without independent bridging evidence.

The same page's **County Poor** expenditure list includes **“Farr Bros” — $10.00**. This establishes a dated same-name supplier/payee appearance only. It prints no address, proprietor, or business type and is **not merged with `BUS-104` Farr Brothers Store / Meat Market, Edwin/Alice Farr, or Farr's Pool Hall at 505 Main** without a continuity bridge.

### Page 8 — Harding drugstore staffing notice

The actual scan directly and legibly states:

> **“Percy Cross has accepted a position in the Harding drugstore during the absence of A. E. Wilmot.”**

This upgrades the former OCR/TEXT ONLY lead to **DOCUMENTED / DIRECT — VISUALLY VERIFIED** for the printed staffing relationship:
- `{P_CROSS}` Percy Cross accepted a position in the Harding drugstore;
- `{P_WILMOT}` A. E. Wilmot was absent during the period for which Cross accepted the position;
- the source itself does **not** state Wilmot's precise job title or employment status beyond that wording.

The page does **not** print a street number and does not name George A. Harding. Independently, `E-092` places **George A. Harding at 511 Main** on 5 January 1912. Reading the two contemporary sources together supports a **STRONG CROSS-SOURCE INFERENCE** that the 19 January “Harding drugstore” notice concerns the same Harding drug business then documented at 511 Main, but **511 Main is not source-explicit on page 8** and no property/building ownership is inferred.

## Target-frontage result

Across pages 5–8, the only material target-business finding is the page-8 Harding drugstore staffing notice. The four pages do **not** establish a new direct 501/503/505 occupant, do not resolve the H. N. / H. H. Smith initials conflict, and do not create a new 505 Main occupancy claim.

The p5–p7 no-hit result is bounded coverage only, never evidence of vacancy, closure, non-use, or absence of an event.

## Cross-record propagation audit

This batch is propagated to:
- source/evidence registers and YAML;
- `{P_CROSS}`, `{P_WILMOT}`, and `{P_PRICE}` person controls;
- `BUS-007` Harding Drug Store and its YAML relations;
- the 1912 Courier page-review/page-count checkpoints;
- the Jan. 19 pages 1–4 capture and thread-preservation audit as superseding updates;
- the 8 September 1912 final handoff so its former page-8 OCR-only instruction is explicitly superseded;
- ID crosswalk and research log.

No target building record, target-address timeline event, business ownership, property ownership, or 1912 annual-status change is warranted. `1912` remains **IN PROGRESS**.
'''
write(CAPTURE, capture)

append_once("evidence/source-register.md", DATE_MARKER, f'''## {S} — Oregon City Courier, 19 January 1912, pages 5–8 visual-review batch
{DATE_MARKER}
Type: Primary newspaper page scans; **VISUALLY VERIFIED 4/4 PAGES**; completes the issue at **8/8 visually verified** with `S-307`.  
Publication/date: *Oregon City Courier*, **19 January 1912**, printed pages **5–8**.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/  
Repository originals: `newspapers/oregon-city-courier/1912-01-19-page-5.pdf` through `1912-01-19-page-8.pdf`.  
SHA-256: p5 `d7419216d8a39ecfdd726302590ab365f2d7074beac327083c3b84a1c48ddce6`; p6 `53b2c8b4c8b03036fed8a8cc04f18a895dc6fc980ecbc8c052ab7913b2a61300`; p7 `fd88d8623b8203ba49ece2f2c31faf0a8f826569543b18b69d1ce02d1054f444`; p8 `bc4bdb274d1d0530e087da7a01b3f0dfc832ef1174ccd6cfba53e4ec89795a62`.  
Binary preservation commit: `{BINARY_COMMIT}`.  
Related evidence: `{E}`; cross-reference `E-092`.  
Source capture: `{CAPTURE}`.  
Notes: Page 8 directly verifies Percy Cross accepting a position in the Harding drugstore during A. E. Wilmot's absence; no street number is printed. Page 7 prints “Milton Price, pool hall” in the Oregon City No. 1 jury-list section and Farr Bros. as a $10 County Poor payee, both without address/role continuity sufficient for target-business merger. Pages 5–6 add only non-target city/address context. No new direct 501/503/505 occupancy claim; 1912 remains IN PROGRESS.''')

append_once("evidence/evidence-register.md", DATE_MARKER, f'''## {E} — 19 January 1912 Courier pages 5–8: Harding staffing and pool-hall context
{DATE_MARKER}
Type: Primary newspaper scan evidence; **VISUALLY VERIFIED**.  
Source: `{S}`. Cross-reference: `E-092`.  
Claims:
- page 8 directly states that **Percy Cross (`{P_CROSS}`) accepted a position in the Harding drugstore during the absence of A. E. Wilmot (`{P_WILMOT}`)**;
- page 8 prints no street number and does not name George A. Harding; `E-092` independently places George A. Harding at 511 Main on 5 January, so same-store/511 continuity is a **STRONG CROSS-SOURCE INFERENCE**, not a page-8 direct address;
- page 7 directly prints **“Milton Price, pool hall”** under Oregon City, Oregon, No. 1 in a jury list drawn from the assessment roll; it does not state proprietor, employee, trade name, or address and is not merged to the 503/505 pool-hall chains;
- page 7 lists **Farr Bros. — $10.00** under County Poor expenditures; same-name/payee evidence only, with no merger to later `BUS-104`, Edwin/Alice Farr, or 505 Main;
- pages 5–8 produce no new direct 501/503/505 occupant, ownership, structural, or transition claim.
Classification: **DOCUMENTED / DIRECT** for scan-visible wording; **STRONG CROSS-SOURCE INFERENCE** only for interpreting the unnumbered Harding drugstore notice with `E-092`; **UNRESOLVED** for Milton Price's exact pool-hall role/location and Farr Bros. identity continuity.  
Confidence: **Very High** for the printed wording and 4/4 page review.''')

append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S}\n    name: "Oregon City Courier, 19 January 1912, pages 5–8 visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/"\n    type: "Primary newspaper page scans; visually verified 4/4; completes 19 January issue at 8/8 with S-307"\n    date: "1912-01-19"\n    repository_file: "{CAPTURE}"\n    notes: >-\n      Exact page PDFs are preserved under newspapers/oregon-city-courier/ by commit {BINARY_COMMIT}.\n      Page 8 directly verifies Percy Cross accepting a position in the Harding drugstore during A. E. Wilmot's absence,\n      but prints no street number. Page 7 prints Milton Price, pool hall, and a Farr Bros County Poor payment without\n      enough address/identity detail for target-business merger. 1912 remains IN PROGRESS.\n''')

append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E}\n    name: "19 January 1912 Courier pages 5–8: Harding staffing and pool-hall context"\n    type: Primary newspaper scan evidence\n    claims:\n      - Page 8 directly states that Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot.\n      - Page 8 prints no street number or George A. Harding name; reading it with E-092 supports same-store/511 continuity only as a strong cross-source inference.\n      - Page 7 prints Milton Price, pool hall, in Oregon City Precinct No. 1, without proprietor/employee/address detail.\n      - Page 7 lists Farr Bros as a $10 County Poor payee without address, proprietor, or business-type detail.\n      - No new direct 501, 503, or 505 Main occupant or target structural event is established.\n    confidence: Very High for scan-visible wording; unresolved for exact Milton Price role/location and Farr Bros identity continuity\n    related_sources: [{S}]\n    related_evidence: [E-092]\n    related_businesses: [BUS-007]\n    related_people: [{P_CROSS}, {P_WILMOT}, {P_PRICE}]\n    related_buildings: []\n''')

# Add person controls only if exact-name entries do not already exist.
people_spec = [
    ("Percy Cross", P_CROSS, "Harding drugstore staffer", f"19 Jan. 1912 Courier p8 directly says he accepted a position in the Harding drugstore during A. E. Wilmot's absence. No job title, street number, ownership, or identity beyond the printed name is established. `{E}` / `{S}`."),
    ("A. E. Wilmot", P_WILMOT, "Harding drugstore staffing-context person", f"19 Jan. 1912 Courier p8 says Percy Cross accepted a Harding drugstore position during Wilmot's absence. The source does not state Wilmot's job title or ownership. `{E}` / `{S}`."),
    ("Milton Price", P_PRICE, "1912 jury-list taxpayer; 'pool hall' descriptor", f"19 Jan. 1912 Courier p7 prints 'Milton Price, pool hall' under Oregon City, Oregon, No. 1 in a taxpayer jury list. No pool-hall address, trade name, proprietor/employee role, or link to Smith/Leland/Dollar/505 is established. `{E}` / `{S}`."),
]
existing_names = read("database/people.yml")
for name, pid, role, notes in people_spec:
    if re.search(rf"(?m)^    name:\s*[\"']?{re.escape(name)}[\"']?\s*$", existing_names):
        continue
    append_once("people/people-index.md", f"| {pid} | {name} |", f"| {pid} | {name} | {role} | {notes} |")
    append_once("database/people.yml", f"  - id: {pid}\n", f'''  - id: {pid}\n    name: {name}\n    role: {role}\n    notes: >-\n      {notes.replace('`','')}\n    related_businesses: [BUS-007]''' if name != "Milton Price" else f'''  - id: {pid}\n    name: {name}\n    role: {role}\n    notes: >-\n      {notes.replace('`','')}\n    related_businesses: []''')

# Small person profiles preserve identity limits without overclaiming biography.
profiles = {
    "people/profiles/percy-cross.md": f'''# Percy Cross\n\nPerson ID: `{P_CROSS}`.\n\nThe visually verified 19 January 1912 *Oregon City Courier* page 8 directly states that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot** (`{E}` / `{S}`). The source prints no job title, street number, ownership role, or further identifier.\n\nDo not merge this person with other Cross family members by surname alone. `E-092` separately places George A. Harding at 511 Main two weeks earlier; using that to associate this notice with the 511 business is cross-source inference, not wording printed in Cross's notice.\n''',
    "people/profiles/a-e-wilmot.md": f'''# A. E. Wilmot\n\nPerson ID: `{P_WILMOT}`.\n\nThe visually verified 19 January 1912 *Oregon City Courier* page 8 says **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot** (`{E}` / `{S}`). This establishes Wilmot only as the person whose absence is mentioned in the store-staffing notice. The page does not state a job title, ownership role, street number, or expanded given names.\n''',
    "people/profiles/milton-price.md": f'''# Milton Price\n\nPerson ID: `{P_PRICE}`.\n\nThe visually verified 19 January 1912 *Oregon City Courier* page 7 says the annual jury was drawn from the Clackamas County assessment roll and, under **Oregon City, Oregon, No. 1**, prints **“Milton Price, pool hall.”** (`{E}` / `{S}`).\n\nTreat **pool hall** as the source's occupation/descriptor only. The page does not identify a trade name, street address, proprietor/employee status, or connection to H. N./H. H. Smith at 503 Main, Clem Dollar, A. Leland at 505½, or later 505 pool-hall operators.\n'''
}
for path, text in profiles.items():
    if not Path(path).exists():
        Path(path).write_text(text, encoding="utf-8")

# Relate the two staffing people and the new source/evidence to BUS-007.
for pid in (P_CROSS, P_WILMOT):
    update_yaml_relation("database/businesses.yml", "BUS-007", "related_people", pid)
update_yaml_relation("database/businesses.yml", "BUS-007", "related_evidence", E)
update_yaml_relation("database/businesses.yml", "BUS-007", "related_sources", S)

append_once("businesses/harding-drug-store.md", DATE_MARKER, f'''## 19 January 1912 staffing notice
{DATE_MARKER}

The actual *Oregon City Courier* p8 scan is now **VISUALLY VERIFIED** (`{E}` / `{S}`) and directly states that **Percy Cross (`{P_CROSS}`) accepted a position in the Harding drugstore during the absence of A. E. Wilmot (`{P_WILMOT}`)**. This supersedes the prior OCR/TEXT ONLY state for that notice.

The notice itself prints **no street number** and does not name George A. Harding. `E-092` independently places George A. Harding at **511 Main** on 5 January 1912. Taken together, the sources strongly support same-store continuity at 511 in January, but the 19 January notice is not direct exact-address evidence and does not prove property/building ownership or Wilmot's precise job role.
''')

append_once("indexes/id-crosswalk.md", DATE_MARKER, f'''{DATE_MARKER}

| Source / evidence | Entity / topic | Scope and limit |
| --- | --- | --- |
| `{S}` / `{E}` | `BUS-007`; `{P_CROSS}` Percy Cross; `{P_WILMOT}` A. E. Wilmot | 19 Jan. 1912 p8 directly verifies Harding-drugstore staffing wording; no street number on page. `E-092` supplies separate 5 Jan. 511 Main control, so 511 continuity is cross-source inference only. |
| `{S}` / `{E}` | `{P_PRICE}` Milton Price | 19 Jan. p7 jury-list wording “Milton Price, pool hall”; no address or proprietor/employee status; no merge to 503/505 pool-hall chains. |
| `{S}` / `{E}` | Farr Bros. same-name lead | 19 Jan. p7 County Poor expenditure of $10; no address/proprietor/business type and no merge to later `BUS-104` or 505 Main. |
''')

append_once("registers/research-log.md", DATE_MARKER, f'''### 2026-09-09 — 19 January 1912 Courier pages 5–8 steward batch
{DATE_MARKER}
- Visually inspected the actual scans for printed pages **5–8**; combined with `S-307`, the 19 January issue is now **8/8 VISUALLY VERIFIED**.
- Preserved exact page PDFs at `newspapers/oregon-city-courier/1912-01-19-page-5.pdf` through `page-8.pdf`; hash-gated binary commit `{BINARY_COMMIT}`.
- Registered `{S}` / `{E}`. Page 8 directly verifies **Percy Cross accepting a position in the Harding drugstore during A. E. Wilmot's absence**, superseding the prior OCR-only state; no number is printed, and `E-092` remains the separate 5 Jan. 511 Main control.
- Page 7 prints **“Milton Price, pool hall”** in the Oregon City No. 1 jury list and **Farr Bros. $10** under County Poor expenditures; both are preserved with strict identity/address limits and are not merged to later pool-hall/Farr chains.
- Pages 5–6 add only non-target city/address context. No new direct 501/503/505 occupant or target structural event. **1912 remains IN PROGRESS**.
''')

# Supersede stale page-8 OCR-only statements without erasing their historical state.
replace_once(
    "evidence/source-captures/1912-courier-page-review-note.md",
    "A project-steward supplied batch reviewed on **9 September 2026** adds actual scan-review credit for **19 January 1912 printed pages 1–4**. All four scans are **VISUALLY VERIFIED**. They produced no safe new exact-address or target-block claim; the useful page-1 Willamette high-water and river-channel-improvement material is retained as non-target Oregon City context in `1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md`.\n\nThat batch does **not** certify 19 January pages/images 5–8. In particular, the separate page/image-8 Percy Cross / Harding Drug Store staffing lead remains **OCR/TEXT ONLY** until the actual scan is visually inspected.",
    f"Two project-steward supplied batches reviewed on **9 September 2026** now provide actual scan-review credit for **all eight printed pages of the 19 January 1912 issue**. Pages 1–4 are `S-307`; pages 5–8 are `{S}`. The issue is therefore **8/8 VISUALLY VERIFIED**. Pages 1–4 produced no safe new exact-address or target-block claim; page 1's Willamette high-water and river-channel material remains non-target city context. Page 8 now directly verifies Percy Cross accepting a position in the Harding drugstore during A. E. Wilmot's absence (`{E}` / `{S}`), superseding the earlier OCR/TEXT ONLY state. The page itself prints no street number."
)

pagecount_old = '''The issue is controlled as an **eight-image issue**. Parallel work on 9 September visually inspected and preserved printed pages **1–4** (`S-307`). Those pages produced no safe new exact-address or target-block claim.\n\nThe archive again exposes page/image 8 text stating, with OCR noise, that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot**:\n\n- https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/\n\nThe actual page-8 scan/PDF still did not render through the available route during this continuation. Therefore the Percy Cross / Harding Drug Store item remains:\n\n**OCR/TEXT ONLY — PENDING SCAN CERTIFICATION.**\n\nDo not create a verified person/business relationship from this text until the actual page is visually inspected. Pages 5–8 remain uncredited visually in the current exhaustive ledger unless another current-main source capture separately certifies them.'''
pagecount_new = f'''The issue is controlled as an **eight-image issue**. Earlier on 9 September, pages **1–4** were visually inspected and preserved as `S-307`. Later the project steward supplied pages **5–8**; all four actual scans were visually inspected and preserved as `{S}`. The 19 January issue is now **8/8 VISUALLY VERIFIED**.\n\nPage 8 directly states that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot** (`{E}` / `{S}`):\n\n- https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/\n\nThis **supersedes the earlier OCR/TEXT ONLY / pending-scan state** recorded in the first version of this checkpoint. The page prints no street number. `E-092` independently places George A. Harding at 511 Main on 5 January, so interpreting this as the same 511 store is a strong cross-source inference, not wording printed on page 8.'''
replace_once("evidence/source-captures/1912-courier-pagecount-resume-2026-09-09.md", pagecount_old, pagecount_new)
replace_once(
    "evidence/source-captures/1912-courier-pagecount-resume-2026-09-09.md",
    "1. Continue recovery attempts for **19 January pages 5–8**, prioritizing page 8 for Percy Cross / Harding Drug Store.\n2. Resolve the remaining Courier count/sequence gaps:",
    "1. **19 January pages 1–8 are complete and visually verified; no further recovery is needed for that issue.**\n2. Resolve the remaining Courier count/sequence gaps:"
)

append_once("evidence/source-captures/1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md", DATE_MARKER, f'''## Superseding same-day update — pages 5–8 recovered and reviewed
{DATE_MARKER}

The earlier statement in this pages-1–4 checkpoint that page 8 remained OCR/TEXT ONLY accurately described the state at that moment. It is now **superseded**: pages 5–8 were subsequently supplied, visually inspected, and preserved as `{S}` / `{E}`. Page 8 directly verifies the Percy Cross / Harding drugstore / A. E. Wilmot staffing notice. The complete 19 January issue is now **8/8 VISUALLY VERIFIED**. See `{CAPTURE}`.
''')

append_once("evidence/source-captures/2026-09-09-1912-jan-19-thread-knowledge-preservation-audit.md", DATE_MARKER, f'''## Superseding same-day update — complete issue now preserved
{DATE_MARKER}

After this audit was first written, the project steward supplied 19 January printed pages **5–8**. All four actual scans were visually inspected and exact PDFs preserved in commit `{BINARY_COMMIT}`. They are registered as `{S}` / `{E}` and documented in `{CAPTURE}`. The issue is now **8/8 VISUALLY VERIFIED**.

Most importantly, page 8 directly verifies that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot**. The former OCR/TEXT ONLY state in the earlier portion of this audit is therefore superseded. The page prints no street number; `E-092` remains the separate 5 January 511 Main address control.
''')

append_once("evidence/source-captures/2026-09-08-1912-final-handoff-checkpoint.md", DATE_MARKER, f'''## 9 September 2026 supersession — 19 January page 8 visually verified
{DATE_MARKER}

The earlier handoff section requiring the Percy Cross / Harding drugstore item to remain **OCR/TEXT ONLY** is now superseded. The project steward supplied printed pages 5–8; the actual page-8 scan was visually inspected and directly states that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot**. See `{S}` / `{E}` and `{CAPTURE}`. Page 8 prints no street number, so `E-092` remains the independent 5 January 511 Main address control rather than being silently imported into the 19 January wording.
''')

# Make S-307's historical note self-correcting rather than globally stale.
replace_once(
    "evidence/source-register.md",
    "The separate 19 January page/image 8 Percy Cross / Harding Drug Store lead remains **OCR/TEXT ONLY** because page 8 is not in this four-page batch.",
    f"At the time of the pages 1–4 review, the separate page-8 Percy Cross / Harding Drug Store lead remained **OCR/TEXT ONLY** because page 8 was not in that batch. That state is now superseded by `{S}` / `{E}`, which visually verifies page 8."
)
replace_once(
    "database/sources.yml",
    "Page-8 Percy Cross / Harding Drug Store lead is still OCR/TEXT ONLY.",
    f"Page 8 was still OCR/TEXT ONLY at S-307 creation; that state is superseded by {S}/{E}, which visually verifies pages 5–8."
)

print(f"Integrated source {S}, evidence {E}, people {P_CROSS}, {P_WILMOT}, {P_PRICE}")
