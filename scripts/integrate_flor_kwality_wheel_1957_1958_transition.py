#!/usr/bin/env python3
from pathlib import Path
import re

MARKER = "Flor Kwality Wheel 1957-1958 transition sync — 2026-09-06"
ROOT = Path(__file__).resolve().parents[1]
PDF_REL = "newspapers/clackamas-county-news/1958-08-22-p2-wheel-cafe-lounge-503-main.pdf"
PDF = ROOT / PDF_REL
CAPTURE = "evidence/source-captures/morton-wheel-to-oregon-city-wheel-ownership-bridge-pass-2026-09-05.md"
URL = "https://oregonnews.uoregon.edu/lccn/sn96088135/1958-08-22/ed-1/seq-2.pdf"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8")


def append_once(path, marker, section):
    text = read(path)
    if marker not in text:
        write(path, text.rstrip() + "\n\n" + section.strip())


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


def next_id(prefix, paths):
    nums = []
    pat = re.compile(rf"\b{re.escape(prefix)}-(\d+)\b")
    for path in paths:
        for m in pat.finditer(read(path)):
            nums.append(int(m.group(1)))
    return f"{prefix}-{max(nums, default=0)+1:03d}"


def yaml_add_list_item(path, entity_id, key, value):
    text = read(path)
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n(?P<body>.*?)(?=^  - id: |\Z)", text)
    if not m:
        raise RuntimeError(f"Entity {entity_id} not found in {path}")
    block = m.group(0)
    km = re.search(rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:      - .*\n)*)", block)
    if km:
        items = km.group("items")
        if re.search(rf"(?m)^      - {re.escape(value)}$", items):
            return
        newblock = block[:km.end("items")] + f"      - {value}\n" + block[km.end("items"):]
    else:
        # Add before the next known related_* list if possible, otherwise at block end.
        insert = f"    {key}:\n      - {value}\n"
        pos = len(block)
        newblock = block[:pos] + insert + block[pos:]
    write(path, text[:m.start()] + newblock + text[m.end():])


def yaml_replace_scalar(path, entity_id, key, new_value):
    text = read(path)
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n(?P<body>.*?)(?=^  - id: |\Z)", text)
    if not m:
        raise RuntimeError(f"Entity {entity_id} not found in {path}")
    block = m.group(0)
    pat = re.compile(rf"(?m)^    {re.escape(key)}:.*$")
    if not pat.search(block):
        raise RuntimeError(f"Key {key} not found for {entity_id} in {path}")
    newblock = pat.sub(f"    {key}: {new_value}", block, count=1)
    write(path, text[:m.start()] + newblock + text[m.end():])


def main():
    if MARKER in read("registers/research-log.md"):
        print("Flor/Kwality/Wheel transition already synchronized; no duplicate write.")
        return
    if not PDF.exists() or PDF.stat().st_size < 10000:
        raise RuntimeError(f"Expected preserved source PDF missing or too small: {PDF_REL}")

    sid = next_id("S", ["evidence/source-register.md", "database/sources.yml"])
    eid = next_id("E", ["evidence/evidence-register.md", "database/evidence.yml"])

    # Formal source/evidence registration for the previously visually reviewed primary page.
    append_once("evidence/source-register.md", MARKER, f'''## {sid} — Clackamas County News, 22 August 1958 p.2 — Wheel Cafe & Lounge at 503 Main
<!-- {MARKER} -->
Type: Primary newspaper page scan  
Publication: *The Clackamas County News*  
Date/page: **22 August 1958, p. 2**  
Repository file: `{PDF_REL}`  
Primary URL: {URL}  
Evidence: `{eid}`  
Capture: `{CAPTURE}`  
Classification: **DOCUMENTED / DIRECT — VISUALLY VERIFIED.** The original page was visually reviewed during the 5–6 September 2026 ownership-bridge pass; the preserved PDF is the same archive page. The advertisement directly reads **WHEEL CAFE & LOUNGE**, **503 Main St.**, **Ph: 9106**. It does not name a proprietor, owner, licensee, seller, buyer, or predecessor.''')

    append_once("evidence/evidence-register.md", MARKER, f'''## {eid} — Wheel Cafe & Lounge is directly documented at 503 Main by 22 August 1958
<!-- {MARKER} -->
Source: `{sid}`  
Related building/business: `B-001` / `BUS-004`  
Type: Primary newspaper advertisement  
Claims:
- On **22 August 1958**, *The Clackamas County News* directly advertises **WHEEL CAFE & LOUNGE**.
- The advertisement directly prints **503 Main St.** and **Ph: 9106**.
- This is the archive's earliest currently registered **exact-number** primary Wheel anchor at 503 Main.
- Compared with existing `E-032`, which places **Mr. and Mrs. Albert D. Flor** operating/managing the restaurant/cocktail bar at 503 in **1957**, the two documented endpoints narrow the unresolved restaurant/Kwality/Flor → Wheel transition to after the 1957 control and no later than **22 August 1958**.
Limits:
- `{sid}` does **not** name Albert Flor, Margaret Remus, Raye LaFarlette/Grisham, or any proprietor/licensee.
- The cross-source bracket does **not** prove Flor owned The Wheel, renamed Kwality Cafe, sold the business, or sold it to Raye.
Classification: **DOCUMENTED / DIRECT** for the 22 August 1958 Wheel name/address/phone; **UNRESOLVED TRANSITION** when paired with the 1957 Flor endpoint.''')

    append_once("database/sources.yml", MARKER, f'''  - id: {sid}
    name: "Clackamas County News, 22 August 1958 p.2 — Wheel Cafe & Lounge, 503 Main"
    url: "{URL}"
    type: "Primary newspaper page scan"
    date: "1958-08-22"
    repository_file: "{PDF_REL}"
    notes: "Visually reviewed primary advertisement: WHEEL CAFE & LOUNGE, 503 Main St., Ph: 9106. Does not name proprietor/licensee. See {CAPTURE}."
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_evidence: [{eid}]
    # {MARKER}''')

    append_once("database/evidence.yml", MARKER, f'''  - id: {eid}
    name: "Wheel Cafe & Lounge at exact 503 Main by 22 August 1958"
    source: {sid}
    type: "Primary newspaper advertisement"
    claims:
      - "22 August 1958 advertisement directly reads WHEEL CAFE & LOUNGE."
      - "Advertisement directly prints 503 Main St. and Ph: 9106."
      - "Paired with E-032's 1957 Flor same-address operator control, this brackets an unresolved transition; it does not identify the Wheel proprietor or prove a Flor ownership/rename/sale."
    confidence: "Very High / DOCUMENTED-DIRECT for 1958 name-address-phone; transition unresolved"
    related_buildings: [B-001]
    related_businesses: [BUS-004]
    related_people: [P-025]
    related_sources: [{sid}]
    # {MARKER}''')

    # Person record: make the predecessor boundary explicit without turning Flor into a Wheel proprietor.
    append_once("people/profiles/albert-d-flor-family.md", MARKER, f'''## 1957 → 22 August 1958 503 Main transition boundary
<!-- {MARKER} -->

The City historic-resource synthesis (`E-032` / `S-026`) places **Mr. and Mrs. Albert D. Flor** operating/managing the **restaurant and cocktail bar at 503 Main in 1957**. A now-preserved and formally registered primary advertisement (`{eid}` / `{sid}`) directly places **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106** there on **22 August 1958**.

These are two documented endpoints at the same address. They make Flor the **latest currently identified named operator control before the earliest exact-number Wheel anchor**, but they do not establish the mechanism of transition.

Classification: **DOCUMENTED ENDPOINTS / UNRESOLVED TRANSITION**. Do **not** infer that Flor owned The Wheel, renamed Kwality Cafe to The Wheel, sold The Wheel, or sold it to Raye LaFarlette/Grisham. The decisive targets are 1957–1958 liquor-license renewals/transfers, assumed-business-name filings, directories/telephone books, and contemporary sale/new-management notices.''')

    append_once("businesses/kwality-cafe.md", MARKER, f'''## 1957 → 1958 Kwality/Flor → Wheel transition bracket
<!-- {MARKER} -->

The early-1950s continuity evidence now has a firm later boundary. The City's 1957 historic-resource synthesis (`E-032` / `S-026`) places **Mr. and Mrs. Albert D. Flor** with the restaurant/cocktail-bar operation at **503 Main**. The visually verified **22 August 1958** advertisement (`{eid}` / `{sid}`) directly identifies **WHEEL CAFE & LOUNGE at 503 Main, phone 9106**.

Together with the 1953 **`Al & Marge Kwality Cafe`** line, these records make 1957–1958 the critical transition interval. They do **not** directly prove that `Al & Marge` were Flor/Remus, that Kwality was formally renamed The Wheel, that Flor owned either business, or that the Flor household sold to Raye. Preserve those as research hypotheses until a proprietor/license/transfer record names the parties and trade name.''')

    # Wheel page: add formal source and clarify earliest exact address.
    replace_once("businesses/the-wheel.md",
                 "- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`, `E-225`, `E-228`, `E-229`, `E-230`",
                 f"- Related evidence: `E-001`, `E-007`, `E-015`, `E-022`, `E-025`, `E-044`, `E-045`, `E-047`, `E-048`, `E-049`, `E-225`, `E-228`, `E-229`, `E-230`, `{eid}`")
    append_once("businesses/the-wheel.md", MARKER, f'''## Earliest exact-address Wheel anchor and 1957 predecessor boundary
<!-- {MARKER} -->

`{sid}` / `{eid}` preserves a visually reviewed **22 August 1958** *Clackamas County News* advertisement reading **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**. This moves the archive's earliest registered exact-number Wheel anchor earlier than the previously emphasized 30 November 1960 intersection-only advertisement. The ownership-bridge capture also records a visually reviewed **28 November 1958** repeat advertisement and an OCR/text-only **13 February 1959** continuation with the same 503/9106 wording.

The immediately preceding named same-address control is the City's official-secondary **1957 Mr./Mrs. Albert D. Flor restaurant/cocktail-bar operation** (`E-032` / `S-026`). Therefore the present documentary bracket is:

**1957 — Flor restaurant/cocktail bar at 503 → by 22 Aug. 1958 — Wheel Cafe & Lounge at 503.**

Classification: **DOCUMENTED ENDPOINTS / UNRESOLVED TRANSITION**. No recovered source yet says who owned or licensed the Wheel in August 1958, whether Flor continued under the Wheel name, whether a sale occurred, or who Raye later purchased from. `P-025` is therefore retained as a predecessor/operator control and is **not** promoted to a Wheel owner/operator without a direct bridge.''')

    # Building record: occupancy transition, explicitly not title evidence.
    replace_once("buildings/503-main.md",
                 "`E-225`, `E-228`, `E-229`, `E-230`",
                 f"`E-225`, `E-228`, `E-229`, `E-230`, `{eid}`")
    replace_once("buildings/503-main.md",
                 "`S-251`, `S-254`, `S-255`, `S-256`",
                 f"`S-251`, `S-254`, `S-255`, `S-256`, `{sid}`")
    append_once("buildings/503-main.md", MARKER, f'''## 1957–1958 occupancy/name transition at 503
<!-- {MARKER} -->

The 503 occupancy chronology can now be bracketed more tightly. `E-032` / `S-026` places **Mr. and Mrs. Albert D. Flor** operating/managing the restaurant/cocktail bar at this address in **1957**. `{eid}` / `{sid}` directly advertises **WHEEL CAFE & LOUNGE, 503 Main St., phone 9106** on **22 August 1958**.

This is an **occupancy/trade-name boundary, not a real-estate ownership event**. The records do not establish a property conveyance, a business sale, an assumed-name filing, or the identity of the August 1958 licensee. The exact Kwality/Flor → Wheel mechanism remains unresolved.''')

    # Address-specific and business timelines.
    replace_once("timelines/503-main.md",
                 "| 1957 | Mr./Mrs. Albert D. Flor operate restaurant/cocktail bar at 503. | Official secondary; folded into restaurant/Kwality context until distinct name found. | `BUS-001`; `P-025`; `E-032` |\n| 30 Nov. 1960 | **Wheel Cafe** at Fifth/Main. | Primary name/intersection; number omitted. | `BUS-004`; `E-044`; `S-051`; `IMG-0046` |",
                 f"| 1957 | Mr./Mrs. Albert D. Flor operate restaurant/cocktail bar at 503. | Official secondary; latest named same-address operator control before the earliest exact-number Wheel anchor. Does not prove Wheel ownership/rename/sale. | `BUS-001`; `P-025`; `E-032`; `S-026` |\n| 22 Aug. 1958 | **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106.** | **Exact, visually verified primary ad.** Proprietor/licensee not named; transition from the 1957 Flor endpoint unresolved. | `BUS-004`; `{eid}`; `{sid}` |\n| 30 Nov. 1960 | **Wheel Cafe** at Fifth/Main. | Primary name/intersection; number omitted; now a later corroboration rather than earliest Wheel anchor. | `BUS-004`; `E-044`; `S-051`; `IMG-0046` |")

    replace_once("registers/business-timeline.md",
                 "| 1926 / 1947 / 1957 | Kwality Restaurant / Cafe / Flor | `BUS-001` | `E-032` | Official secondary | |\n| Jun. 1937 | Kwality Cafe (for sale)",
                 f"| 1926 / 1947 / 1957 | Kwality Restaurant / Cafe / Flor | `BUS-001` | `E-032` | Official secondary | 1957 is the latest named same-address Flor operator control before Wheel appears directly at exact 503 in Aug. 1958; transition mechanism unresolved. |\n| Jun. 1937 | Kwality Cafe (for sale)")
    replace_once("registers/business-timeline.md",
                 "| Nov. 1960 | Wheel Cafe | `BUS-004` | `E-044` | Very High name/intersection | Oregonian: 5th and Main. Street number not stated. |",
                 f"| 22 Aug. 1958 | Wheel Cafe & Lounge | `BUS-004` | `{eid}` / `{sid}` | Very High / visually verified exact address | Direct ad: **503 Main St., Ph: 9106**. Proprietor/licensee not named; paired with 1957 Flor control only as an unresolved transition bracket. |\n| Nov. 1960 | Wheel Cafe | `BUS-004` | `E-044` | Very High name/intersection | Oregonian: 5th and Main. Street number not stated; later corroboration after the exact 1958 anchor. |")

    append_once("timeline.md", MARKER, f'''## 1957–22 August 1958 — 503 restaurant/Flor → Wheel boundary refined
<!-- {MARKER} -->

The earlier 1957–1960 bracket is now narrowed. The City historic-resource synthesis (`E-032` / `S-026`) reports **Mr. and Mrs. Albert D. Flor** operating/managing the restaurant and cocktail bar at **503 Main in 1957**. A preserved, visually reviewed **22 August 1958** *Clackamas County News* advertisement (`{eid}` / `{sid}`) directly reads **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**.

**Documented endpoints:** 1957 Flor operation at 503 → Wheel Cafe & Lounge at exact 503 by 22 August 1958. **Unresolved:** whether Flor renamed the business, sold it, was replaced by an intermediate operator, or had any ownership relationship to The Wheel. No property transfer is inferred from this occupancy/name change.''')

    # Human-readable business index gets a dated refinement without changing entity identity.
    append_once("businesses/business-index.md", MARKER, f'''## 6 September 2026 — 503 Kwality/Flor → Wheel transition refinement
<!-- {MARKER} -->

- `BUS-001` **Kwality Cafe lineage:** 1957 City synthesis places Mr./Mrs. Albert D. Flor at the 503 restaurant/cocktail bar; the 1953 `Al & Marge Kwality Cafe` identity remains a strong hypothesis, not direct proof.
- `BUS-004` **The Wheel:** `{sid}` / `{eid}` now supplies the earliest registered exact-number primary anchor: **Wheel Cafe & Lounge, 503 Main St., phone 9106, 22 August 1958**.
- Do not merge the endpoints into a Flor-owned Wheel or a proved Kwality→Wheel rename/sale without a direct transfer/license/trade-name record.''')

    # YAML synchronization.
    yaml_replace_scalar("database/people.yml", "P-025", "notes", '1957 City historic-resource synthesis places Mr./Mrs. Albert D. Flor operating/managing the restaurant/cocktail bar at 503 Main. This is the latest currently named same-address operator control before the direct 22 Aug 1958 Wheel Cafe & Lounge exact-address advertisement. The transition mechanism is unresolved; do not infer Flor owned, renamed, or sold The Wheel.')

    # Business YAML notes are long one-line scalars; replace their leading notes lines safely.
    bus = read("database/businesses.yml")
    bus = bus.replace(
        "    notes: Early cafe/restaurant occupant. Oregonian 12 June 1937 classified advertises KWALITY cafe for sale, Oregon City; street number not in the ad.",
        "    notes: Early cafe/restaurant occupant. Oregonian 12 June 1937 classified advertises KWALITY cafe for sale, Oregon City; street number not in the ad. September 1953 City text names Al & Marge Kwality Cafe; paired with the 1951 Flor/Remus liquor-license line and the 1957 Flor 503 operator control this is a strong continuity hypothesis, not direct identity proof. A direct 22 Aug 1958 Wheel Cafe & Lounge advertisement at exact 503 brackets the later transition without proving Flor owned, renamed, or sold The Wheel.", 1)
    bus = bus.replace(
        "    notes: The Wheel was only at 503 Main and was never a 505 Main business.",
        f"    notes: The Wheel was only at 503 Main and was never a 505 Main business. Earliest currently registered exact-number primary anchor is 22 Aug 1958: Wheel Cafe & Lounge, 503 Main St., Ph: 9106 ({eid}/{sid}); a 28 Nov 1958 repeat is preserved in the ownership-bridge capture and Feb 1959 continuation is OCR/text only. The 1957 Flor restaurant/cocktail-bar same-address control brackets the predecessor transition but does not prove Flor owned, renamed, or sold The Wheel.", 1)
    write("database/businesses.yml", bus)
    yaml_add_list_item("database/businesses.yml", "BUS-004", "related_evidence", eid)
    yaml_add_list_item("database/businesses.yml", "BUS-004", "related_sources", sid)

    # Building YAML had drifted from the Markdown record; repair that while adding the 1958 source.
    bld = read("database/buildings.yml")
    bld = bld.replace(
        "    notes: Associated with Kwality Cafe lineage and The Wheel, which was only at 503.",
        "    notes: Associated with Kwality Cafe lineage and The Wheel, which was only at 503. Occupancy/name chronology is now bracketed by the 1957 Mr./Mrs. Albert D. Flor restaurant/cocktail-bar control and the direct 22 Aug 1958 Wheel Cafe & Lounge exact-address advertisement; this is not title/deed evidence and the transition mechanism remains unresolved.", 1)
    write("database/buildings.yml", bld)
    for val in ("P-025",):
        yaml_add_list_item("database/buildings.yml", "B-001", "related_people", val)
    for val in ("E-032", eid):
        yaml_add_list_item("database/buildings.yml", "B-001", "related_evidence", val)
    for val in ("S-026", sid):
        yaml_add_list_item("database/buildings.yml", "B-001", "related_sources", val)

    # Replace existing T-038 rather than creating a duplicate chronology event.
    ty = read("database/timeline.yml")
    tm = re.search(r"(?ms)^  - id: T-038\n.*?(?=^  - id: |\Z)", ty)
    if not tm:
        raise RuntimeError("T-038 not found in database/timeline.yml")
    new_t = f'''  - id: T-038
    date: 1957–22 August 1958
    summary: City synthesis reports Mr./Mrs. Albert D. Flor operating/managing the restaurant/cocktail bar at 503 in 1957; visually reviewed 22 Aug 1958 Clackamas County News ad directly places Wheel Cafe & Lounge at 503 Main, phone 9106. Exact Kwality/Flor-to-Wheel transition and proprietor/licensee remain unresolved.
    confidence: Official secondary for 1957; DOCUMENTED/DIRECT primary newspaper page for 22 Aug 1958; transition unresolved.
    related_people: [P-025]
    related_businesses: [BUS-001, BUS-004]
    related_buildings: [B-001]
    related_evidence: [E-032, {eid}]
    related_sources: [S-026, {sid}]
'''
    write("database/timeline.yml", ty[:tm.start()] + new_t + ty[tm.end():])

    append_once("evidence/open-questions.md", MARKER, f'''## 6 September 2026 — who controlled 503 at the Kwality/Flor → Wheel transition?
<!-- {MARKER} -->

`E-032` / `S-026` places Mr./Mrs. Albert D. Flor with the 503 restaurant/cocktail bar in **1957**; `{eid}` / `{sid}` directly places **Wheel Cafe & Lounge at 503 Main** by **22 August 1958**. The exact transition is now narrowed but still unanswered.

Questions to resolve:
1. Was the 1953 **`Al & Marge Kwality Cafe`** line Albert D. Flor and Margaret Remus?
2. Who was the proprietor/licensee of **Wheel Cafe & Lounge, 503 Main** in August 1958?
3. Did Flor continue under a new Wheel trade name, sell/transfer the business, or leave before another operator renamed it?
4. If a sale occurred, who were the buyer and seller, and is either party connected to Raye LaFarlette/Grisham's later acquisition?
5. What dated record first uses the Wheel name and what dated record last uses Kwality/Flor wording?''')

    append_once("evidence/research-leads.md", MARKER, f'''## 6 September 2026 — 1957–1958 Flor/Kwality → Wheel transfer search
<!-- {MARKER} -->

Highest-value target is now the narrow **1957 through 22 August 1958** transition at 503 Main. Search Oregon City/OLCC liquor-license applications, renewals and transfers; assumed-business-name filings; 1957–1959 directories/telephone books; and newspaper sale/new-management notices using **Albert D. Flor**, **Mr./Mrs. Albert D. Flor**, **Margaret/Marge Remus**, **Al & Marge Kwality Cafe**, **Kwality Cafe**, **Wheel Cafe & Lounge**, **503 Main**, and **9106**.

Disconfirming test: actively look for a different proprietor/licensee at the Wheel in 1958. A different named operator would defeat any simple Flor=Wheel assumption and may identify the pre-Raye seller chain.''')

    append_once("indexes/id-crosswalk.md", MARKER, f'''## {sid} / {eid} — 1958 Wheel exact-address transition control
<!-- {MARKER} -->

| Record | Links | Handling rule |
| --- | --- | --- |
| `{sid}` / `{eid}` | `B-001`, `BUS-004`; compare `P-025` / `E-032` | 22 Aug. 1958 visually verified ad directly gives **Wheel Cafe & Lounge, 503 Main, 9106**. Pair with 1957 Flor only to bracket an unresolved transition; do not promote Flor to Wheel owner/operator without a bridge. |''')

    append_once("registers/research-log.md", MARKER, f'''### 2026-09-06 — synchronized Flor/Kwality → Wheel 1957–1958 transition
<!-- {MARKER} -->

- Preserved the previously visually reviewed **22 Aug. 1958 Clackamas County News p.2** page under `{PDF_REL}` and formally registered it as `{sid}` / `{eid}`.
- Direct source wording: **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**.
- Propagated the resulting 1957→1958 bracket across `P-025`, `BUS-001`, `BUS-004`, `B-001`, the 503 and master timelines, business timeline/index, YAML databases, open questions, research leads and crosswalk.
- Repaired pre-existing YAML drift for B-001 by carrying its already-established `P-025` / `E-032` / `S-026` Flor connection into `database/buildings.yml`.
- Evidence handling remains conservative: the 1957 Flor endpoint and 1958 Wheel endpoint are documented, but **ownership, rename, sale, licensee identity and Raye's seller remain unresolved**. No Flor→Wheel ownership relationship was manufactured.''')

    print(f"Integrated transition using {sid} / {eid}.")


if __name__ == "__main__":
    main()
