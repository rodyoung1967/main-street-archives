#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise June pool-room regulatory amendment — 2026-09-06"
SID = "S-281"
EID = "E-254"
CAPTURE = "evidence/source-captures/1917-enterprise-june-01-29-visual-review-2026-09-06.md"

def r(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def w(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(rel, block):
    text = r(rel)
    if MARKER in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    w(rel, text + "\n" + block.strip() + "\n")

def append_to_heading_block(rel, heading, addition):
    text = r(rel)
    if MARKER in text:
        return
    m = re.search(rf"(?m)^## {re.escape(heading)}\b.*$", text)
    if not m:
        raise SystemExit(f"Missing heading {heading} in {rel}")
    n = re.search(r"(?m)^## ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    block = text[m.start():end].rstrip()
    newblock = block + "\n\n" + addition.strip() + "\n"
    w(rel, text[:m.start()] + newblock + text[end:])

def yaml_block(rel, entity_id):
    text = r(rel)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing {entity_id} in {rel}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    return text, m.start(), end, text[m.start():end]

def update_yaml_block(rel, entity_id, updater):
    text, start, end, block = yaml_block(rel, entity_id)
    newblock = updater(block)
    if newblock != block:
        w(rel, text[:start] + newblock + text[end:])

if not (ROOT / CAPTURE).exists():
    raise SystemExit(f"Missing June capture: {CAPTURE}")
cap = r(CAPTURE)
if f"source `{SID}`; evidence `{EID}`" not in cap:
    raise SystemExit("June capture IDs do not match expected S-281 / E-254")

timeline_md = r("timeline.md")
m_tid = re.search(rf"<!-- {re.escape(MARKER)} -->\s*\n.*?`(T-\d{{3}})`", timeline_md, re.S)
if m_tid:
    TID = m_tid.group(1)
else:
    nums = [int(x) for x in re.findall(r"\bT-(\d{3})\b", r("database/timeline.yml"))]
    TID = f"T-{max(nums)+1:03d}"

leads = r("evidence/research-leads.md")
m_rl = re.search(r"(?m)^## (RL-\d{3}) — Recover 1911 / 1917 Oregon City pool-room regulation", leads)
if m_rl:
    RLID = m_rl.group(1)
else:
    nums = [int(x) for x in re.findall(r"(?m)^## RL-(\d{3})\b", leads)]
    RLID = f"RL-{max(nums)+1:03d}"

capture_add = f'''## 8 June p.3 — citywide pool-room / cigar-stand licensing context
<!-- {MARKER} -->

Enlarged visual inspection of **8 June 1917, p.3** confirms a city-council report stating that **all of the pool rooms in the city** were said to be violating certain sections of the city ordinance. The discussion concerned a proposed ordinance amendment that would allow pool rooms to **operate cigar stands without paying additional licenses**. The same paragraph says the city's **strict pool-room legislation** had been made in **1911**, when saloons were still operating.

This is **DOCUMENTED / DIRECT** evidence for the printed 1917 council-report wording and a material regulatory backdrop for Oregon City's pool-room/cigar businesses. It does **not** identify any particular pool room, address, proprietor, licensee, violator, or enforcement case. In particular, it does not prove that the 1912 Smith pool room at 503 Main, any later 505 pool hall, Farr's Pool Hall, or any named operator violated the ordinance or paid/owed a cigar license.

A bounded online follow-up found additional discovery material: an official City minutes derivative describes **Ordinance 457** in December 1909 as amending earlier pool-room legislation, while April–May 1911 newspapers report a stricter pool-room measure under consideration with open-front and anti-gambling provisions. Those items help define the ordinance lineage but are not promoted here as visually certified source claims. `{RLID}` now targets the underlying 1911 enactment and the 1917 amendment/outcome.

### Propagation amendment

This finding materially changes the regulatory interpretation of the early pool-room evidence, so the June batch is additionally propagated to:
- master/business chronology (`{TID}`) as a **citywide regulatory event**, not a 503/505 occupancy event;
- the 1912 Smith pool-room evidence/business pages as later regulatory context only;
- the 503 unified timeline as a contextual note attached to the 1912 pool-room sequence, not as a 1917 occupant;
- research lead `{RLID}` for the actual 1911 ordinance and 1917 amendment outcome.

No building, occupant, proprietor, or ownership assignment changes. No open question is closed by this citywide article.
'''
append_once(CAPTURE, capture_add)

append_to_heading_block(
    "evidence/source-register.md",
    SID,
    f'''**June 8 regulatory amendment.** <!-- {MARKER} -->
The visually inspected 8 June p.3 council report also says city pool rooms were violating ordinance sections and records discussion of allowing pool-room cigar stands without additional licenses; it dates the strict pool-room legislation to 1911. This is citywide regulatory context only, not an address/operator finding. See `{TID}` / `{RLID}`.''',
)

append_to_heading_block(
    "evidence/evidence-register.md",
    EID,
    f'''**Additional direct claim — 8 June p.3.** <!-- {MARKER} -->
The page directly reports a citywide complaint that pool rooms were violating ordinance sections and a council discussion about amending the rules so pool rooms could operate cigar stands without additional licenses; it says the strict pool-room legislation was made in 1911. Classification: **DOCUMENTED / DIRECT** for the printed regulatory wording; no individual pool room, address, proprietor, violation, or license status is inferred. Related chronology/lead: `{TID}` / `{RLID}`.''',
)

def upd_source(block):
    if "citywide pool-room/cigar-license ordinance context" in block:
        return block
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("    notes:"):
            value = line.split(":", 1)[1].strip()
            if value.startswith('"') and value.endswith('"'):
                txt = value[1:-1]
                txt += " June 8 p3 also supplies citywide pool-room/cigar-license ordinance context dating strict legislation to 1911; no named room/address."
                lines[i] = f'    notes: "{txt}"'
            else:
                raise SystemExit("S-281 notes is not expected quoted scalar")
            return "\n".join(lines) + ("\n" if block.endswith("\n") else "")
    raise SystemExit("S-281 notes field not found")
update_yaml_block("database/sources.yml", SID, upd_source)

def upd_evidence(block):
    if "citywide pool-room ordinance sections" in block:
        return block
    lines = block.splitlines()
    insert = None
    for i, line in enumerate(lines):
        if line.startswith("    confidence:"):
            insert = i
            break
    if insert is None:
        raise SystemExit("E-254 confidence field not found")
    lines.insert(insert, '      - "8 June p3 directly reports citywide pool-room ordinance sections, proposed cigar-stand license relief, and says strict pool-room legislation was made in 1911; no individual room/address/violation is identified."')
    return "\n".join(lines) + ("\n" if block.endswith("\n") else "")
update_yaml_block("database/evidence.yml", EID, upd_evidence)

append_once(
    "timeline.md",
    f'''## 8 June 1917 — Oregon City pool-room / cigar-stand licensing discussion
<!-- {MARKER} -->

Timeline record: `{TID}`. Source/evidence: `{SID}` / `{EID}`.

A visually verified *Oregon City Enterprise* council report says all city pool rooms were being described as violating certain ordinance sections while the council discussed an amendment allowing pool rooms to operate **cigar stands without additional licenses**. The report says the city's strict pool-room legislation had been made in **1911**, when saloons were still operating.

This is a **citywide regulatory event**, useful context for interpreting the 1912 Smith pool room at 503 and later pool-hall/cigar evidence. It is **not** evidence that Smith, Farr, Timms, a 505 operator, or any particular premises violated the ordinance or had a particular license status. The underlying 1911 ordinance text and 1917 amendment outcome remain open under `{RLID}`.''',
)

timeline_yml = r("database/timeline.yml")
if not re.search(rf"(?m)^  - id: {re.escape(TID)}\s*$", timeline_yml):
    timeline_yml = timeline_yml.rstrip() + f'''

  - id: {TID}
    date: "8 June 1917"
    summary: "Oregon City Enterprise reports citywide pool-room ordinance violations were discussed while council considered allowing pool rooms to operate cigar stands without additional licenses; the article dates the strict pool-room legislation to 1911."
    confidence: "Very High for visually verified published council-report wording; no individual room, address, proprietor, violation, or license status identified"
    related_evidence:
      - {EID}
'''
    w("database/timeline.yml", timeline_yml)

append_once(
    "registers/business-timeline.md",
    f'''### 8 June 1917 — citywide pool-room regulatory context
<!-- {MARKER} -->

| Date | Location | Business / subject | Records | Evidence | Limits |
| --- | --- | --- | --- | --- | --- |
| 8 Jun. 1917 | Oregon City, citywide | Pool-room ordinance / cigar-stand licensing discussion | `{TID}` / `{RLID}` | `{EID}` / `{SID}` | Council report says pool rooms were violating ordinance sections and discusses cigar stands without additional licenses; strict legislation said to date to 1911. No room, address, proprietor or individual violation named. |''',
)

append_once(
    "evidence/E-089-1912-smith-pool-room-503-main.md",
    f'''## Later regulatory context from 1917
<!-- {MARKER} -->

`{EID}` / `{SID}` (8 June 1917 p.3) later reports that Oregon City's strict pool-room legislation had been made in **1911** and that the council was discussing whether pool rooms could operate cigar stands without paying additional licenses. Because the January 1912 Smith advertisement at 503 expressly offered **Pool Room, Cigars and Tobacco**, this is material regulatory backdrop.

It does **not** prove that Smith violated any ordinance, that his cigar/tobacco activity required or lacked a separate license, that his March 1912 application was granted, or that the 1917 report referred to 503 Main. Recover the underlying ordinance/amendment under `{RLID}`.''',
)

append_once(
    "businesses/h-h-smith-pool-hall.md",
    f'''## Regulatory backdrop
<!-- {MARKER} -->

A visually verified 8 June 1917 city-council report (`{EID}` / `{SID}`) says Oregon City's strict pool-room legislation had been made in **1911** and discusses whether pool rooms could operate cigar stands without additional licenses. This is relevant background to the January 1912 **Pool Room, Cigars and Tobacco** advertisement at 503, but it does not establish Smith's compliance, violation, additional-license status, or any 1917 connection to 503. Underlying ordinance text/outcome: `{RLID}`.''',
)

append_once(
    "timelines/503-main.md",
    f'''## 1911–1917 pool-room regulatory context — not a 503 occupancy event
<!-- {MARKER} -->

The 1912 Smith entries above sit within a broader city licensing regime. A visually verified 8 June 1917 council report (`{EID}` / `{SID}`; `{TID}`) says Oregon City's strict pool-room legislation dated to **1911** and records discussion of cigar stands and additional licenses. The report is **citywide** and names no pool room or address, so it is not added to the table as a 1917 503 occupant/event. It is retained only as context for interpreting Smith's 1912 “Pool Room, Cigars and Tobacco” wording. See `{RLID}` for the underlying ordinance-recovery task.''',
)

if MARKER not in leads:
    leads = leads.rstrip() + f'''

## {RLID} — Recover 1911 / 1917 Oregon City pool-room regulation
<!-- {MARKER} -->

**Status: OPEN — ONLINE-FIRST.**

`{EID}` / `{SID}` visually verifies an 8 June 1917 *Oregon City Enterprise* council report saying city pool rooms were violating certain ordinance sections while the council discussed an amendment that would let pool rooms operate cigar stands without additional licenses. The article says the city's strict pool-room legislation was made in **1911**, when saloons still operated.

Next work:
1. recover the enacted **1911 pool-room ordinance** (not merely newspaper summaries), including ordinance number, adoption/effective dates, license provisions, open-front requirements, prohibited games and any cigar/tobacco provisions;
2. trace its relationship to the earlier pool-room ordinance lineage, including the already discoverable 1907/1909 measures, without assuming the 1917 reporter's “made in 1911” phrase means there were no earlier regulations;
3. recover the **1917 amendment text and council outcome** associated with the cigar-stand/additional-license discussion;
4. compare the enacted rules cautiously with the 1912 Smith 503 application/advertisement and later 1920–1925 pool-hall/cigar evidence.

Do not infer that Smith, Farr, Timms, or any particular 503/505 operator violated the ordinance or owed/held a separate cigar license unless a source names that operator/premises.
'''
    w("evidence/research-leads.md", leads)

append_once(
    "indexes/id-crosswalk.md",
    f'''## {TID} / {RLID} — 1917 pool-room regulatory amendment
<!-- {MARKER} -->

| Records | Connection | Limit |
| --- | --- | --- |
| `{SID}` / `{EID}` | 8 Jun. 1917 Enterprise p3 citywide pool-room/cigar-license discussion | Direct published regulatory wording; no particular room/address/operator |
| `{TID}` | Dated citywide regulatory chronology | Not a 503/505 occupancy event |
| `{RLID}` | Underlying 1911 ordinance + 1917 amendment/outcome recovery | Online-first; ordinance lineage still unresolved |
| `BUS-019` / `B-001` | Context for 1912 Smith “Pool Room, Cigars and Tobacco” at 503 | Does not prove compliance, violation or separate cigar-license status |''',
)

append_once(
    "evidence/source-captures/1917-closeout.md",
    f'''## June pool-room regulatory-context amendment
<!-- {MARKER} -->

The already closed June Enterprise batch (`{SID}` / `{EID}`; 40/40 genuine pages) also contains a visually verified **8 June p.3** city-council report on citywide pool-room ordinance violations and a proposed cigar-stand/additional-license change. It dates the strict pool-room legislation to 1911. This adds regulatory context only; June coverage counts and the target-frontage no-hit do not change. Underlying ordinance/amendment recovery is `{RLID}`; chronology `{TID}`.''',
)

append_once(
    "ARCHIVE_INDEX.md",
    f'''## 1917 pool-room regulatory context
<!-- {MARKER} -->

The June Enterprise audit (`{SID}` / `{EID}`) includes an 8 June 1917 council report stating that Oregon City's strict pool-room legislation dated to 1911 and discussing cigar stands/additional licenses. This is useful context for `BUS-019` at 503 and later pool-hall/cigar evidence, but it identifies no particular pool room or address. See `{TID}` / `{RLID}`.''',
)

append_once(
    "registers/research-log.md",
    f'''### 2026-09-06 — June 1917 Enterprise pool-room regulatory amendment
<!-- {MARKER} -->

- Rechecked the already validated June closeout (`{SID}` / `{EID}`) against the scan review and found one omitted direct finding on **8 June p.3**.
- Visually verified citywide pool-room ordinance/cigar-stand licensing discussion and the article's statement that strict pool-room legislation dated to 1911.
- Added `{TID}` as citywide regulatory chronology and `{RLID}` to recover the enacted 1911 ordinance and 1917 amendment outcome.
- Added context to `BUS-019` / `E-089` / the 503 unified timeline without creating a 1917 503/505 occupant or alleging any operator violation.
- Reviewed buildings/people/businesses/open questions: no building, proprietor, person-identity or open-question status change is warranted by the citywide article.''',
)

print(f"June pool-room regulatory amendment prepared: {SID} {EID} {TID} {RLID}")
