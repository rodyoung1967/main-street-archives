#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "Wheel Cafe May 1958 earliest recovered anchor — 2026-09-07"
PDF_REL = "newspapers/clackamas-county-news/1958-05-16-p2-wheel-cafe-lounge-503-main.pdf"
PDF_URL = "https://oregonnews.uoregon.edu/lccn/sn96088135/1958-05-16/ed-1/seq-2.pdf"
MAY9_URL = "https://oregonnews.uoregon.edu/lccn/sn96088135/1958-05-09/ed-1/seq-7.pdf"
CAPTURE = "evidence/source-captures/1958-wheel-cafe-earliest-advertisement-backward-pass-2026-09-07.md"
OLD_CAPTURE = "evidence/source-captures/morton-wheel-to-oregon-city-wheel-ownership-bridge-pass-2026-09-05.md"
REQUEST = "registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md"


def p(path):
    return ROOT / path


def read(path):
    return p(path).read_text(encoding="utf-8")


def write(path, text):
    p(path).parent.mkdir(parents=True, exist_ok=True)
    p(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def append_once(path, section):
    text = read(path) if p(path).exists() else ""
    if MARKER in text:
        return
    write(path, text.rstrip() + ("\n\n" if text.strip() else "") + section.strip())


def next_id(prefix, paths):
    nums = []
    pat = re.compile(rf"\b{re.escape(prefix)}-(\d+)\b")
    for path in paths:
        if p(path).exists():
            nums.extend(int(m.group(1)) for m in pat.finditer(read(path)))
    return f"{prefix}-{max(nums, default=0)+1:03d}"


def yaml_add_list_item(path, entity_id, key, value):
    text = read(path)
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n(?P<body>.*?)(?=^  - id: |\Z)", text)
    if not m:
        raise RuntimeError(f"Entity {entity_id} not found in {path}")
    block = m.group(0)
    km = re.search(rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:      - .*\n)*)", block)
    if km:
        if re.search(rf"(?m)^      - {re.escape(value)}$", km.group("items")):
            return
        newblock = block[:km.end("items")] + f"      - {value}\n" + block[km.end("items"):]
    else:
        newblock = block.rstrip() + f"\n    {key}:\n      - {value}\n"
    write(path, text[:m.start()] + newblock + text[m.end():])


def yaml_replace_in_entity(path, entity_id, old, new):
    text = read(path)
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n(?P<body>.*?)(?=^  - id: |\Z)", text)
    if not m:
        raise RuntimeError(f"Entity {entity_id} not found in {path}")
    block = m.group(0)
    if new in block:
        return
    if old not in block:
        print(f"WARN: expected entity text not found for {entity_id} in {path}")
        return
    newblock = block.replace(old, new, 1)
    write(path, text[:m.start()] + newblock + text[m.end():])


def insert_before_line(path, needle_start, new_line):
    text = read(path)
    if new_line in text:
        return
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(needle_start):
            lines.insert(i, new_line)
            write(path, "\n".join(lines))
            return
    print(f"WARN: timeline insertion target not found in {path}: {needle_start}")


def replace_text_if_present(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        print(f"WARN: expected text not found in {path}: {old[:100]}")
        return
    write(path, text.replace(old, new, 1))


def main():
    if not p(PDF_REL).exists() or p(PDF_REL).stat().st_size < 10000:
        raise RuntimeError(f"Missing or implausibly small source PDF: {PDF_REL}")

    if p(CAPTURE).exists() and MARKER in read(CAPTURE):
        print("May 1958 Wheel anchor already integrated; no duplicate write.")
        return

    sid = next_id("S", ["evidence/source-register.md", "database/sources.yml"])
    eid = next_id("E", ["evidence/evidence-register.md", "database/evidence.yml"])
    tid = next_id("T", ["database/timeline.yml"])

    write(CAPTURE, f'''# Wheel Cafe & Lounge — backward advertisement pass to May 1958

Date of research pass: **7 September 2026**

Status: **NEW VISUALLY VERIFIED EARLIER EXACT-ADDRESS ENDPOINT; PROPRIETOR / LICENSEE / TRANSITION MECHANISM UNRESOLVED**

<!-- {MARKER} -->

## Purpose

Avoid duplicating the parallel Flor/Remus directory/EDR/provenance work and instead test the newspaper transition boundary directly: how early can **Wheel Cafe & Lounge** be documented at **503 Main Street** before the previously registered 22 August 1958 advertisement?

## 16 May 1958 — exact-address Wheel advertisement

The actual scanned page image of *The Clackamas County News*, **16 May 1958, p. 2**, was visually inspected. In the page's **“WHERE TO FIND AND BUY IT IN OREGON CITY”** business guide, an advertisement directly reads:

- **WHEEL CAFE**
- **& LOUNGE**
- **STEAKS**
- **503 Main St.**
- **Ph: 9106**

Primary page: {PDF_URL}

Repository copy: `{PDF_REL}`

Classification: **DOCUMENTED / DIRECT — VISUALLY VERIFIED PRIMARY NEWSPAPER ADVERTISEMENT** for the Wheel Cafe & Lounge trade name, exact 503 Main address, and telephone 9106 on 16 May 1958.

The advertisement gives **no proprietor, owner, licensee, seller, buyer, predecessor, “new management,” or “formerly Kwality” wording**. It therefore does not establish who controlled the business or how the Kwality/Flor operation became the Wheel.

## Repeat-advertisement controls found during the backward pass

The same exact-address / phone advertisement was visually observed again on multiple later 1958 issues during this pass, including **30 May, 27 June, 11 July, 25 July, 1 August, 8 August, and 15 August**, before the already registered **22 August** page (`S-282` / `E-255`). These repeats corroborate continuing public use of the Wheel Cafe & Lounge name and phone 9106; they are not separate ownership events.

A source-association caution was also encountered: the online page object labeled **4 July 1958 p. 2** visually reproduced a page printing **27 June 1958**. It is not used here as independent 4 July evidence.

## Why 9 May does not create a negative opening boundary

The **9 May 1958 p. 7** scan was visually inspected. Its analogous business-guide panel is explicitly **“WHERE TO FIND AND BUY IT IN GRESHAM”**, not the Oregon City guide that carries the Wheel advertisement on 16 May. Primary page: {MAY9_URL}

Accordingly, failure to find the Wheel in that Gresham guide **cannot** prove the Wheel did not exist on 9 May. Special-layout and alternate-city guide pages in the surrounding issues likewise cannot support a negative existence inference.

The correct statement is therefore: **16 May 1958 is the earliest recovered and visually certified exact-address Wheel advertisement in this backward pass**, not a proved opening date.

## Revised documentary bracket

The current evidence endpoints are now:

- **1957** — City official-secondary synthesis: Mr. and Mrs. Albert D. Flor with the restaurant/cocktail-bar operation at 503 Main (`E-032` / `S-026`; underlying publication provenance remains under separate research); and
- **16 May 1958** — visually verified primary advertisement: Wheel Cafe & Lounge, 503 Main, phone 9106 (`{eid}` / `{sid}`).

Classification when paired: **DOCUMENTED ENDPOINTS / UNRESOLVED TRANSITION**.

Do **not** infer that Flor owned the Wheel, renamed Kwality Cafe, sold the business, or sold it to Raye LaFarlette/Grisham. The transition could predate 16 May, and the newspaper guide does not identify the operator.

## Research consequence

The highest-value Oregon-side licensing search should now explicitly cover **1951–1959**, with special attention to late 1957 through **May 1958**, rather than treating August 1958 as the first known Wheel state. The 1951 Flor/Remus application, 1953 `Al & Marge Kwality Cafe`, 1957 Flor-at-503 secondary control, and May 1958 Wheel advertisement remain separate evidence points until a license, directory, assumed-name, transfer, or sale source bridges them.

## Cross-record propagation audit

This batch changes a dated business/address endpoint, so the Wheel/Kwality/503 timelines, relevant business/building/person pages, source/evidence registers, crosswalk, database/YAML records, open question, research log, and MF-052/request wording are updated. No new proprietor, licensee, owner, property event, or Flor-to-Wheel transfer is manufactured from the advertisement.''')

    append_once("evidence/source-register.md", f'''## {sid} — Clackamas County News, 16 May 1958 p.2 — Wheel Cafe & Lounge at 503 Main
<!-- {MARKER} -->
Type: Primary newspaper page scan  
Publication: *The Clackamas County News* (archive catalog: *Estacada's Clackamas County news.*)  
Date/page: **16 May 1958, p. 2**  
Repository file: `{PDF_REL}`  
Primary URL: {PDF_URL}  
Evidence: `{eid}`  
Capture: `{CAPTURE}`  
Classification: **DOCUMENTED / DIRECT — VISUALLY VERIFIED.** The page's Oregon City business guide directly advertises **WHEEL CAFE & LOUNGE**, **STEAKS**, **503 Main St.**, **Ph: 9106**. It names no proprietor/licensee and is an earlier exact-address endpoint, not an opening or transfer date.''')

    append_once("evidence/evidence-register.md", f'''## {eid} — Wheel Cafe & Lounge is directly documented at 503 Main by 16 May 1958
<!-- {MARKER} -->
Source: `{sid}`  
Related building/business: `B-001` / `BUS-004`  
Type: Primary newspaper advertisement  
Claims:
- On **16 May 1958**, the visually inspected page directly advertises **WHEEL CAFE & LOUNGE** in an Oregon City business guide.
- The advertisement directly prints **503 Main St.** and **Ph: 9106**.
- This supersedes 22 August 1958 (`E-255` / `S-282`) only as the archive's **earliest currently recovered exact-number Wheel advertisement**; the August source remains valid later corroboration.
- Paired with `E-032`, the unresolved Flor/Kwality → Wheel transition is now bracketed from the 1957 Flor same-address control to no later than **16 May 1958**.
Limits:
- The advertisement does not name a proprietor, owner, licensee, seller, buyer, predecessor, or change-of-management event.
- A visually inspected 9 May issue page carries a **Gresham**, not Oregon City, business guide; its silence cannot be used as a negative opening boundary.
Classification: **DOCUMENTED / DIRECT** for 16 May 1958 name/address/phone; **UNRESOLVED TRANSITION** when paired with the 1957 Flor endpoint.''')

    append_once("database/sources.yml", f'''  - id: {sid}
    name: "Clackamas County News, 16 May 1958 p.2 — Wheel Cafe & Lounge at 503 Main"
    url: "{PDF_URL}"
    type: "Primary newspaper page scan"
    date: "1958-05-16"
    repository_file: "{PDF_REL}"
    notes: "Visually reviewed Oregon City business-guide ad: WHEEL CAFE & LOUNGE, STEAKS, 503 Main St., Ph: 9106. Earliest currently recovered exact-address Wheel advertisement; no proprietor/licensee or opening/transfer wording."
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_evidence: [{eid}]
    # {MARKER}''')

    append_once("database/evidence.yml", f'''  - id: {eid}
    name: "Wheel Cafe & Lounge at exact 503 Main by 16 May 1958"
    source: {sid}
    type: "Primary newspaper advertisement"
    claims:
      - "16 May 1958 advertisement directly reads WHEEL CAFE & LOUNGE."
      - "Advertisement directly prints 503 Main St. and Ph: 9106."
      - "It moves the earliest recovered exact-address Wheel advertisement back from 22 August 1958 without establishing an opening, proprietor, licensee, rename, or sale."
      - "Paired with E-032's 1957 Flor same-address control, this brackets an unresolved transition no later than 16 May 1958."
    confidence: "Very High / DOCUMENTED-DIRECT for name-address-phone; transition unresolved"
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_people: [P-025]
    related_sources: [{sid}]
    # {MARKER}''')

    append_once("database/timeline.yml", f'''  - id: {tid}
    date: 16 May 1958
    summary: "Wheel Cafe & Lounge is directly advertised at 503 Main Street, phone 9106."
    confidence: "Very High / DOCUMENTED-DIRECT for name-address-phone; proprietor and transition unresolved"
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_evidence: [{eid}]
    related_sources: [{sid}]
    # {MARKER}''')

    yaml_add_list_item("database/businesses.yml", "BUS-004", "related_evidence", eid)
    yaml_add_list_item("database/businesses.yml", "BUS-004", "related_sources", sid)
    yaml_replace_in_entity(
        "database/businesses.yml", "BUS-004",
        "Earliest currently registered exact-number primary anchor is 22 Aug 1958 — Wheel Cafe & Lounge, 503 Main St., phone 9106 (E-255/S-282); a 28 Nov 1958 repeat is preserved in the ownership-bridge capture and Feb 1959 continuation is OCR/text only.",
        f"Earliest currently recovered exact-number primary anchor is 16 May 1958 — Wheel Cafe & Lounge, 503 Main St., phone 9106 ({eid}/{sid}); the 22 Aug 1958 E-255/S-282 page remains later corroboration, with a 28 Nov repeat preserved in the ownership-bridge capture and Feb 1959 continuation OCR/text only."
    )
    yaml_add_list_item("database/buildings.yml", "B-001", "related_evidence", eid)
    yaml_add_list_item("database/buildings.yml", "B-001", "related_sources", sid)

    insert_before_line(
        "timelines/503-main.md", "| 22 Aug. 1958 |",
        f"| 16 May 1958 | **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106.** | **Exact, visually verified primary ad; earliest currently recovered exact-address Wheel advertisement.** Not an opening date; proprietor/licensee unnamed. | `BUS-004`; `{eid}`; `{sid}` |"
    )
    insert_before_line(
        "registers/business-timeline.md", "| 22 Aug. 1958 |",
        f"| 16 May 1958 | Wheel Cafe & Lounge | `BUS-004` | `{eid}` / `{sid}` | Very High / visually verified exact address | Direct ad: **503 Main St., Ph: 9106**. Earliest currently recovered exact-address Wheel advertisement; not an opening date and no proprietor/licensee named. |"
    )

    for path, heading, body in [
        ("businesses/the-wheel.md", "## 16 May 1958 — earlier exact-address Wheel anchor", f"`{sid}` / `{eid}` now preserves a visually reviewed **16 May 1958** advertisement reading **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**. This supersedes `S-282` / `E-255` only as the archive's earliest recovered exact-number Wheel advertisement; the 22 August page remains valid later corroboration. The May ad names no proprietor/licensee and is **not** an opening or ownership-transfer date. The current documentary bracket is therefore **1957 Flor same-address restaurant/cocktail-bar control → by 16 May 1958 Wheel Cafe & Lounge at 503**, with the mechanism unresolved."),
        ("businesses/kwality-cafe.md", "## 16 May 1958 — earlier Wheel endpoint for the Kwality/Flor transition", f"The visually verified `{sid}` / `{eid}` Wheel advertisement moves the later endpoint of the unresolved Kwality/Flor → Wheel transition from 22 August back to **16 May 1958**. It does not state `formerly Kwality`, name Flor/Remus, identify an owner/licensee, or record a sale. Preserve the 1953 `Al & Marge` and 1957 Flor controls separately until a direct bridge is recovered."),
        ("buildings/503-main.md", "## 16 May 1958 — occupancy/trade-name endpoint", f"`{eid}` / `{sid}` directly advertises **Wheel Cafe & Lounge, 503 Main St., phone 9106** on **16 May 1958**. This is an occupancy/trade-name endpoint only; it is not a real-estate conveyance, opening date, or business-sale record. `E-255` / `S-282` remains a later August corroboration."),
        ("people/profiles/albert-d-flor-family.md", "## Revised 1957 → 16 May 1958 transition boundary", f"A visually verified 16 May 1958 primary advertisement (`{eid}` / `{sid}`) now places **Wheel Cafe & Lounge at 503 Main, phone 9106**, earlier than the previously registered 22 August endpoint. Flor remains only the latest named 1957 same-address operator control from the City synthesis. Do not promote `P-025` to Wheel proprietor/owner or infer a Flor sale/rename from the tighter bracket."),
        ("evidence/open-questions.md", "## 7 September 2026 — Flor/Kwality → Wheel transition endpoint moved to 16 May 1958", f"`{eid}` / `{sid}` visually establishes **Wheel Cafe & Lounge, 503 Main, phone 9106** by **16 May 1958**, moving the earliest recovered exact-address Wheel advertisement back from 22 August. A visually inspected 9 May page carries a Gresham rather than Oregon City business guide, so it does not establish nonexistence one week earlier. Still open: who was the May 1958 proprietor/licensee, whether Flor continued under the Wheel name, and whether a rename/sale/transfer occurred before 16 May."),
        ("businesses/business-index.md", "## 7 September 2026 — Wheel exact-address date refinement", f"`BUS-004` now has a visually verified exact-address advertisement at **503 Main on 16 May 1958** (`{eid}` / `{sid}`), phone 9106. Treat this as the earliest currently recovered ad, not as an opening or ownership date. The 1957 Flor → Wheel transition remains unresolved."),
        ("timeline.md", "## 16 May 1958 — Wheel Cafe & Lounge at exact 503 Main", f"A visually verified *Clackamas County News* advertisement (`{sid}` / `{eid}`) directly reads **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**. This moves the earliest recovered exact-address Wheel advertisement back from 22 August 1958. It does not identify the proprietor/licensee or establish an opening, rename, sale, or transfer."),
        ("indexes/id-crosswalk.md", f"## {sid} / {eid} — 16 May 1958 Wheel exact-address control", f"| Record | Links | Handling rule |\n| --- | --- | --- |\n| `{sid}` / `{eid}` | `B-001`, `BUS-004`; compare `P-025` / `E-032` and later `S-282` / `E-255` | Visually verified 16 May 1958 ad directly gives **Wheel Cafe & Lounge, 503 Main, 9106**. Earliest currently recovered exact-address ad; not an opening, proprietor, license, rename, or sale record. |"),
        ("registers/research-log.md", "### 2026-09-07 — moved earliest recovered Wheel exact-address ad to 16 May 1958", f"- Visually inspected the **16 May 1958 p.2** Oregon City business guide and preserved the source as `{sid}` / `{eid}`: **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**.\n- This moves the earliest recovered exact-address Wheel advertisement back from 22 August 1958 while leaving the proprietor/licensee and Flor/Kwality transition unresolved.\n- Visually inspected the analogous **9 May p.7** guide and confirmed it is a **Gresham**, not Oregon City, business guide; no negative opening inference was made.\n- Recorded later repeat-ad controls and a July-4/June-27 source-association anomaly in `{CAPTURE}`.\n- Cross-record propagation completed; no ownership, licensee, sale, or opening event was invented."),
    ]:
        append_once(path, f"{heading}\n<!-- {MARKER} -->\n\n{body}")

    append_once(OLD_CAPTURE, f'''## 7 September 2026 correction — earlier exact-address Wheel advertisement
<!-- {MARKER} -->

The earlier conclusion in this capture that **22 August 1958** was the earliest recovered exact-number Wheel anchor is superseded **only on that point**. A visually verified **16 May 1958** *Clackamas County News* p.2 Oregon City business-guide advertisement directly reads **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106** (`{sid}` / `{eid}`). The 22 August and 28 November advertisements remain valid later corroboration.

This does not establish an opening date or identify a proprietor/licensee. A visually inspected 9 May guide is for Gresham rather than Oregon City, so it cannot serve as negative evidence. Detailed backward-pass capture: `{CAPTURE}`.''')

    append_once("MANUAL-FOLLOWUP.md", f'''### MF-052 Oregon-side date refinement — Wheel documented by 16 May 1958
<!-- {MARKER} -->

A visually verified primary advertisement now places **Wheel Cafe & Lounge at 503 Main, phone 9106, by 16 May 1958** (`{sid}` / `{eid}`), earlier than the prior 22 August endpoint. This does not identify the licensee/proprietor. For the Oregon-side MF-052 license-chain test, search **1951–1959**, with special attention to the 1957 renewal cycle and any change/transfer effective **before 16 May 1958**. No outreach was sent.''')

    # The prepared OLCC draft previously began at 1958; broaden it without changing the unsent status.
    replace_text_if_present(
        REQUEST,
        "**Historical licensee/trade-name lookup — Wheel Cafe, 503 Main Street, Oregon City, 1958–1967**",
        "**Historical licensee/trade-name lookup — Kwality / Wheel Cafe, 503 Main Street, Oregon City, 1951–1967**"
    )
    replace_text_if_present(
        REQUEST,
        "- date range **1958–1967**, extending later if necessary to capture the transfer into Raye LaFarlette / Raye Grisham's ownership",
        "- date range **1951–1967**, with special attention to **1957 through 16 May 1958**, extending later if necessary to capture the transfer into Raye LaFarlette / Raye Grisham's ownership"
    )
    append_once(REQUEST, f'''## 7 September 2026 OLCC draft refinement — earlier Wheel endpoint
<!-- {MARKER} -->

Before sending Request B, use the broadened **1951–1967** scope above. New visually verified evidence (`{sid}` / `{eid}`) places **Wheel Cafe & Lounge at 503 Main by 16 May 1958**, so the decisive transfer/renewal search must include records effective before that date as well as the earlier **1951 Flor + Margaret Remus** approval and the 1953 `Al & Marge Kwality Cafe` continuity lead. This remains a draft; nothing was sent automatically.''')

    print(f"Integrated May 16, 1958 Wheel endpoint as {sid}/{eid}/{tid}.")


if __name__ == "__main__":
    main()
