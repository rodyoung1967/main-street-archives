#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "Wheel Cafe March 1958 earliest recovered anchor — 2026-09-07"
PDF_REL = "newspapers/clackamas-county-news/1958-03-28-p3-wheel-cafe-lounge-503-main.pdf"
PDF_URL = "https://oregonnews.uoregon.edu/lccn/sn96088135/1958-03-28/ed-1/seq-3.pdf"
CAPTURE = "evidence/source-captures/1958-03-28-wheel-cafe-earliest-exact-address-control-and-february-guide-controls-2026-09-07.md"
REQ = "registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md"


def p(path): return ROOT / path

def read(path): return p(path).read_text(encoding="utf-8")

def write(path, text):
    p(path).write_text(text.rstrip() + "\n", encoding="utf-8")

def append_once(path, section):
    text = read(path)
    if MARKER not in text:
        write(path, text.rstrip() + "\n\n" + section.strip())

def next_id(prefix, paths):
    pat = re.compile(rf"\b{re.escape(prefix)}-(\d+)\b")
    vals=[]
    for path in paths:
        vals += [int(m.group(1)) for m in pat.finditer(read(path))]
    return f"{prefix}-{max(vals, default=0)+1:03d}"

def yaml_entity(path, entity_id):
    text=read(path)
    m=re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)", text)
    if not m: raise RuntimeError(f"Missing {entity_id} in {path}")
    return text,m,m.group(0)

def yaml_add(path, entity_id, key, value):
    text,m,block=yaml_entity(path,entity_id)
    km=re.search(rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:      - .*\n)*)",block)
    if km:
        if re.search(rf"(?m)^      - {re.escape(value)}$",km.group('items')): return
        nb=block[:km.end('items')]+f"      - {value}\n"+block[km.end('items'):]
    else:
        nb=block.rstrip()+f"\n    {key}:\n      - {value}\n"
    write(path,text[:m.start()]+nb+text[m.end():])

def yaml_replace(path, entity_id, old, new):
    text,m,block=yaml_entity(path,entity_id)
    if new in block: return
    if old not in block:
        print(f"WARN replacement text absent: {path} {entity_id}")
        return
    write(path,text[:m.start()]+block.replace(old,new,1)+text[m.end():])

def insert_row_before(path, needle, row):
    text=read(path)
    if row in text: return
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith(needle):
            lines.insert(i,row); write(path,"\n".join(lines)); return
    print(f"WARN no row insertion target {path}: {needle}")


def main():
    if not p(PDF_REL).exists() or p(PDF_REL).stat().st_size < 10000:
        raise RuntimeError("March 28 primary PDF missing or implausibly small")
    if MARKER in read("evidence/source-register.md"):
        print("March Wheel endpoint already integrated")
        return

    sid=next_id("S",["evidence/source-register.md","database/sources.yml"])
    eid=next_id("E",["evidence/evidence-register.md","database/evidence.yml"])
    tid=next_id("T",["database/timeline.yml"])

    append_once("evidence/source-register.md",f'''## {sid} — Clackamas County News, 28 March 1958 p.3 — Wheel Cafe & Lounge at 503 Main
<!-- {MARKER} -->
Type: Primary newspaper page scan  
Publication: *The Clackamas County News*  
Date/page: **28 March 1958, p. 3**  
Repository file: `{PDF_REL}`  
Primary URL: {PDF_URL}  
Evidence: `{eid}`  
Capture: `{CAPTURE}`  
Classification: **DOCUMENTED / DIRECT — VISUALLY VERIFIED.** The Oregon City business guide directly advertises **WHEEL CAFE & LOUNGE**, **STEAKS**, **503 Main St.**, **Ph: 9106**. It names no proprietor/licensee and is an advertising/occupancy endpoint, not an opening, ownership, rename, sale, or transfer date.''')

    append_once("evidence/evidence-register.md",f'''## {eid} — Wheel Cafe & Lounge at exact 503 Main by 28 March 1958
<!-- {MARKER} -->
Source: `{sid}`  
Related building/business: `B-001` / `BUS-004`  
Type: Primary newspaper advertisement  
Claims:
- The visually inspected **28 March 1958** page directly advertises **WHEEL CAFE & LOUNGE** in the recurring Oregon City business guide.
- The advertisement directly prints **503 Main St.** and **Ph: 9106**.
- This supersedes 16 May 1958 (`E-256` / `S-283`) only as the archive's **earliest currently recovered exact-address Wheel advertisement**; May and August remain valid later corroboration.
- Comparable visually inspected Oregon City guides on **31 Jan., 7 Feb., 14 Feb., and 21 Feb. 1958** do not carry the Wheel advertisement. This is an advertising-state control only, **not proof the business did not exist**.
- Missing intervening March issues are a **RETRIEVAL / COVERAGE GAP**, so no precise first-ad or opening date is inferred.
Confidence: **Very High / DOCUMENTED-DIRECT for 28 March name/address/phone; transition unresolved.**  
Classification: **DOCUMENTED / DIRECT** for the ad; **UNRESOLVED TRANSITION** when paired with the 1957 Flor endpoint.''')

    # YAML root-list appends retain two-space indentation.
    with p("database/sources.yml").open("a",encoding="utf-8") as f:
        f.write(f'''\n  - id: {sid}\n    name: "Clackamas County News, 28 March 1958 p.3 — Wheel Cafe & Lounge at 503 Main"\n    url: "{PDF_URL}"\n    type: "Primary newspaper page scan"\n    date: "1958-03-28"\n    repository_file: "{PDF_REL}"\n    notes: "Visually reviewed Oregon City business-guide ad: WHEEL CAFE & LOUNGE, STEAKS, 503 Main St., Ph: 9106. Earliest currently recovered exact-address Wheel advertisement; no proprietor/licensee or opening/transfer wording."\n    related_buildings: [B-001]\n    related_businesses: [BUS-004]\n    related_evidence: [{eid}]\n    # {MARKER}\n''')
    with p("database/evidence.yml").open("a",encoding="utf-8") as f:
        f.write(f'''\n  - id: {eid}\n    name: "Wheel Cafe & Lounge at exact 503 Main by 28 March 1958"\n    source: {sid}\n    type: "Primary newspaper advertisement"\n    claims:\n      - "28 March 1958 advertisement directly reads WHEEL CAFE & LOUNGE at 503 Main St., Ph: 9106."\n      - "It moves the earliest recovered exact-address Wheel advertisement back from 16 May 1958 without establishing an opening, proprietor, licensee, rename, sale, or transfer."\n      - "Comparable Jan. 31-Feb. 21 Oregon City guides lack the ad, but missing March issues prevent a precise first-ad boundary and silence is not business nonexistence."\n    confidence: "Very High / DOCUMENTED-DIRECT for name-address-phone; transition unresolved"\n    related_buildings: [B-001]\n    related_businesses: [BUS-004]\n    related_people: [P-025]\n    related_sources: [{sid}]\n    # {MARKER}\n''')
    with p("database/timeline.yml").open("a",encoding="utf-8") as f:
        f.write(f'''\n  - id: {tid}\n    date: 28 March 1958\n    summary: "Wheel Cafe & Lounge is directly advertised at 503 Main Street, phone 9106."\n    confidence: "Very High / DOCUMENTED-DIRECT for name-address-phone; proprietor and transition unresolved"\n    related_buildings: [B-001]\n    related_businesses: [BUS-004]\n    related_evidence: [{eid}]\n    related_sources: [{sid}]\n    # {MARKER}\n''')

    yaml_add("database/businesses.yml","BUS-004","related_evidence",eid)
    yaml_add("database/businesses.yml","BUS-004","related_sources",sid)
    yaml_replace("database/businesses.yml","BUS-004",
        "Earliest currently recovered exact-number primary anchor is 16 May 1958 — Wheel Cafe & Lounge, 503 Main St., phone 9106 (E-256/S-283)",
        f"Earliest currently recovered exact-number primary anchor is 28 Mar 1958 — Wheel Cafe & Lounge, 503 Main St., phone 9106 ({eid}/{sid}); 16 May 1958 E-256/S-283 remains later corroboration")
    yaml_add("database/buildings.yml","B-001","related_evidence",eid)
    yaml_add("database/buildings.yml","B-001","related_sources",sid)

    append_once("businesses/the-wheel.md",f'''## 28 March 1958 — earliest currently recovered exact-address Wheel advertisement
<!-- {MARKER} -->

`{sid}` / `{eid}` preserves the visually reviewed **28 March 1958** advertisement reading **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106**. It supersedes the May and August controls only as the earliest recovered exact-number Wheel advertisement; those later pages remain corroboration. Comparable recurring Oregon City guide panels on 31 January and 7/14/21 February do not carry this ad, but missing intervening March issues prevent a precise first-ad boundary. **Do not treat guide silence as proof the Wheel business did not exist.** The ad names no proprietor/licensee and does not prove a Kwality rename, Flor ownership, sale, or Raye acquisition.''')

    append_once("businesses/kwality-cafe.md",f'''## 28 March 1958 — revised later endpoint for the Kwality/Flor transition
<!-- {MARKER} -->

The visually verified `{sid}` / `{eid}` advertisement moves the later endpoint of the unresolved Kwality/Flor → Wheel transition back to **28 March 1958**. It does not state `formerly Kwality`, name Flor/Remus, identify an owner/licensee, or record a sale. Preserve the 1953 `Al & Marge` and 1957 Flor controls separately until a direct bridge is recovered.''')

    append_once("buildings/503-main.md",f'''## 28 March 1958 — occupancy/trade-name endpoint
<!-- {MARKER} -->

`{eid}` / `{sid}` directly advertises **Wheel Cafe & Lounge, 503 Main St., phone 9106** on **28 March 1958**. This is an occupancy/trade-name advertising endpoint only; it is not a real-estate conveyance, opening date, business sale, assumed-name filing, or license transfer.''')

    append_once("people/profiles/albert-d-flor-family.md",f'''## 1957 → 28 March 1958 same-address transition boundary
<!-- {MARKER} -->

The current documented endpoints are the City's **1957** official-secondary Mr./Mrs. Albert D. Flor restaurant/cocktail-bar control at 503 (`E-032` / `S-026`) and the visually verified **28 March 1958** Wheel Cafe & Lounge advertisement at exact 503 (`{eid}` / `{sid}`). This narrows chronology but does **not** make Flor a Wheel proprietor or prove a rename, sale, or transfer.''')

    insert_row_before("timelines/503-main.md","| 16 May 1958 |",f"| 28 Mar. 1958 | **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106.** | **Exact, visually verified primary ad; earliest currently recovered exact-address Wheel advertisement.** Missing intervening March issues prevent precise first-ad/opening inference; proprietor/licensee unnamed. | `BUS-004`; `{eid}`; `{sid}` |")
    insert_row_before("registers/business-timeline.md","| 16 May 1958 |",f"| 28 Mar. 1958 | Wheel Cafe & Lounge | `BUS-004` | `{eid}` / `{sid}` | Very High / visually verified exact address | Direct ad: **503 Main St., Ph: 9106**. Earliest currently recovered exact-address Wheel advertisement; not opening/ownership/transfer date. |")

    append_once("timeline.md",f'''## 28 March 1958 — Wheel Cafe & Lounge directly at 503 Main
<!-- {MARKER} -->

A visually verified *Clackamas County News* advertisement directly prints **WHEEL CAFE & LOUNGE — 503 Main St. — Ph: 9106** (`{sid}` / `{eid}`, `{tid}`). This is the earliest currently recovered exact-address Wheel advertisement. It does not identify proprietor/licensee or establish an opening, rename, ownership change, or sale.''')

    append_once("indexes/id-crosswalk.md",f'''## {sid} / {eid} — 28 March 1958 Wheel exact-address control
<!-- {MARKER} -->

| Record | Links | Handling rule |
| --- | --- | --- |
| `{sid}` / `{eid}` | `B-001`, `BUS-004`; compare `P-025` / `E-032`, later `S-283` / `E-256` and `S-282` / `E-255` | Visually verified 28 Mar. 1958 ad directly gives **Wheel Cafe & Lounge, 503 Main, 9106**. Earliest currently recovered exact-address ad; not an opening, proprietor, license, rename, sale, or transfer date. |''')

    append_once("evidence/open-questions.md",f'''### 7 September 2026 — Wheel advertising endpoint moves to 28 March 1958
<!-- {MARKER} -->

`{sid}` / `{eid}` moves the earliest recovered exact-address Wheel advertisement from 16 May to **28 March 1958**. Comparable 31 Jan.–21 Feb. Oregon City guide panels lack the ad, but missing intervening March issues are a **retrieval/coverage gap** and cannot date the opening or transition. The core question remains: who controlled/licensed 503 when the Kwality/Flor operation became The Wheel, and what record identifies the transfer/rename mechanism?''')

    append_once("registers/research-log.md",f'''### 2026-09-07 — Wheel newspaper boundary moved to 28 March 1958
<!-- {MARKER} -->

- Preserved and registered the visually verified 28 Mar. 1958 *Clackamas County News* p.3 Wheel Cafe & Lounge ad at exact 503 Main as `{sid}` / `{eid}` / `{tid}`.
- Propagated the revised earliest-recovered advertising endpoint across Wheel/Kwality/503/person/timeline/crosswalk/database records.
- Visually comparable Oregon City guide panels on 31 Jan. and 7/14/21 Feb. do not carry the Wheel ad; missing intervening March issues remain a retrieval/coverage gap, so no business opening or transfer date is inferred.
- Telephone-number searching recovered no dated pre-Wheel 9106 or 6106 bridge. This is a retrieval gap, not evidence of a number/operator change.
- State Archives inventory confirms Clackamas County assumed-business-name registers span 1928–1964, but currently listed holdings expose 1928–35 certificates and 1959–64 record volumes; the 1957–58 target register/index is not located online in this pass. No outreach sent.''')

    append_once("MANUAL-FOLLOWUP.md",f'''### MF-052 refinement — Wheel now documented by 28 March 1958; assumed-name register gap
<!-- {MARKER} -->

A visually verified primary ad now places **Wheel Cafe & Lounge at 503 Main, phone 9106, by 28 March 1958** (`{sid}` / `{eid}`), earlier than the May/August controls. For the Oregon-side license/ownership chain, prioritize late 1957 through **28 March 1958**. The Oregon State Archives Clackamas County inventory says assumed-business-name registers cover 1928–1964 and can name owners/filing dates, but its listed available holdings expose 1928–35 certificates and 1959–64 record volumes; the **1957–58 register/index remains an access gap**. No outreach was sent.''')

    append_once(REQ,f'''### Date refinement — 28 March 1958 Wheel endpoint
<!-- {MARKER} -->

The earliest currently recovered exact-address Wheel advertisement is now **28 March 1958**, not August/May 1958. Any Oregon-side historical license/trade-name lookup should specifically test late **1957 through 28 March 1958**, while retaining the broader 1951–1959 chain. The Clackamas County assumed-business-name register series is a high-value parallel record type because it can include business name, filing date, and owner; the 1957–58 volume/index was not located online in the current pass.''')

    # Mark the capture as propagated without rewriting its research narrative.
    append_once(CAPTURE,f'''## 7 September 2026 propagation completion
<!-- {MARKER} -->

The March 28 endpoint has now been formally registered as `{sid}` / `{eid}` / `{tid}`, its primary PDF preserved in the repository, and its chronology/limits propagated across the canonical archive. May and August records remain valid later corroboration.''')

    print(f"Integrated March 28, 1958 Wheel endpoint as {sid}/{eid}/{tid}")

if __name__ == "__main__": main()
