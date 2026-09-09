#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 October Enterprise visual review — 2026-09-08 -->"
YAML_MARKER = "# 1919 October Enterprise visual review — 2026-09-08"
CAPTURE = "evidence/source-captures/1919-october-enterprise-visual-review-2026-09-08.md"
SOURCE_NAME = "October 1919 Oregon City Enterprise complete online visual-review batch with Banner-Courier gap"
EVIDENCE_NAME = "October 1919 online visual review: Theroux 210 Seventh continuity and bounded target coverage"


def read(path): return Path(path).read_text(encoding="utf-8")
def write(path,text): Path(path).write_text(text,encoding="utf-8")
def append_once(path, marker, block):
    p=Path(path); text=p.read_text(encoding="utf-8")
    if marker in text: return False
    if not text.endswith("\n"): text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text,encoding="utf-8"); return True

def next_id(path,prefix):
    nums=[int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", read(path))]
    if not nums: raise RuntimeError(f"No {prefix} ids in {path}")
    return f"{prefix}-{max(nums)+1:03d}"

def update_yaml_relation(path, entity_id, field, value):
    p=Path(path); text=p.read_text(encoding="utf-8")
    m=re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)", text)
    if not m: return False
    block=m.group(0)
    inline=re.search(rf"(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$", block)
    if inline:
        vals=[v.strip() for v in inline.group(1).split(',') if v.strip()]
        if value in vals: return False
        vals.append(value)
        repl=f"    {field}: [" + ", ".join(vals) + "]"
        block=block[:inline.start()] + repl + block[inline.end():]
    else:
        if not block.endswith("\n"): block += "\n"
        block += f"    {field}: [{value}]\n"
    p.write_text(text[:m.start()] + block + text[m.end():], encoding="utf-8")
    return True

def update_1919_status():
    p=Path("registers/year-status.md"); text=p.read_text(encoding="utf-8")
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("| 1919 |"):
            line=line.replace("October–December Enterprise visual work", "November–December Enterprise visual work")
            line=line.replace("Oct-Dec Enterprise still pending", "Nov-Dec Enterprise still pending")
            # Preserve prior prose, then add the October checkpoint only once.
            if "October Enterprise 40/40" not in line:
                if not line.rstrip().endswith("|"):
                    raise RuntimeError("Malformed 1919 year-status row")
                body=line.rstrip()[:-1].rstrip()
                if body.endswith(". ") or body.endswith(".   "):
                    pass
                body += " October Enterprise 40/40 visually verified; Jan-Oct cumulative online local-newspaper visual count 516 pages; Theroux Music House is directly at 210 Seventh through 31 Oct.; no exact target-number or target structural/ownership event. |"
                line=body
            lines[i]=line
            p.write_text("\n".join(lines)+"\n",encoding="utf-8")
            return
    raise RuntimeError("1919 row not found in year-status")

if Path(CAPTURE).exists():
    print("October capture already exists; refusing duplicate integration.")
    sys.exit(0)

# Runtime allocation deliberately occurs after checkout/rebase so parallel work wins.
S=next_id("evidence/source-register.md","S")
E=next_id("evidence/evidence-register.md","E")

capture=f'''# October 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **ONLINE-EXPOSED PAGES VISUALLY VERIFIED — 40/40 recovered October Enterprise pages inspected from original scans; Banner-Courier manual retrieval gap remains.**  
Annual status: **1919 IN PROGRESS**. January–October online-exposed local-newspaper visual coverage: **516 pages**.

Archive IDs: source `{S}`; evidence `{E}`.

## Scope

| Title | Issues reviewed | Pages | Status |
| --- | --- | ---: | --- |
| *Oregon City Enterprise* | 3, 10, 17, 24, 31 Oct. 1919 | **40/40** | All five online-exposed October issues visually reviewed |
| *The Banner-Courier* | 2, 9, 16, 23, 30 Oct. 1919 | **0** | **RETRIEVAL GAP — manual microfilm (`MF-030`)** |
| **Online visual total** | **5 issues** | **40/40** | Banner-Courier gap excluded from visual count |

Preserved originals / manifests:
- `newspapers/oregon-city-enterprise/1919-october/`
- `newspapers/banner-courier/1919-october/manifest.json`

Retrieval commit: `87f70a09ebcffd020abe4618aac28ee90d503848` (`Archive October 1919 Oregon City newspaper scans and gap manifest`).

All 40 Enterprise pages were visually inspected from the original scans. Text/OCR was used only as a discovery/navigation aid and does not substitute for the page review.

## Theroux Music House — 210 Seventh Street through 31 October

The original scans visibly print **Theroux Music House, 210 Seventh St.** in advertisements on:

- **3 Oct. 1919, p.7**;
- **17 Oct. 1919, p.7**;
- **31 Oct. 1919, p.3**.

OCR/text derivatives mangle the leading digit on some occurrences (`S10` / `110`), but the original scans clearly show **210**. This extends the direct dated Theroux address control from 26 September through **31 October 1919**. It does not prove the exact date of the earlier move from 519 Main and does not establish property ownership.

## Target frontage — 501 / 503 / 505 Main

Across all **40 visually reviewed Enterprise pages**:
- no source-explicit **501 Main** occupant was recovered;
- no source-explicit **503 Main** occupant was recovered;
- no source-explicit **505 Main / 505½ Main** occupant was recovered;
- no source-explicit **507 / 507½ / 509 / 511 Main** target-neighbor occurrence was recovered;
- no target-specific construction, demolition, rebuilding, remodeling, fire, sale, lease or ownership event was recovered.

This is **bounded October Enterprise coverage only**. It does not establish vacancy, closure, non-use, demolition, or absence of an occupant and cannot be projected across the inaccessible October Banner-Courier issues.

## Potentially misleading discovery hits resolved visually

- **3 Oct. p.2 — building south of a post office:** the item is in the **Estacada** local column and concerns U. S. Morgan renting a building south of the Estacada post office for a feed store. It is not an Oregon City Fifth/Main spatial control.
- **31 Oct. pool-room / pool-room-like wording:** the inspected contexts concern unrelated lodge/card-room or other pool-room activity and do not identify 501/503/505/505½ Main.
- A surname hit resembling `Wolf` is **Henry Wolfer**, not S. Wolf of Portland and not the unidentified Wolf & Miller partner.

These items are retained as review notes only and are not promoted as target evidence.

## Banner-Courier retrieval gap

The October Banner-Courier dates **2, 9, 16, 23 and 30 October 1919** remain unavailable at the tested online Historic Oregon Newspapers route. The institutional microfilm route remains `MF-030`. This is a retrieval gap, never negative evidence.

## Cross-record propagation

This batch updates the source/evidence registers and YAML mirrors, Theroux person/business chronology, address/business timeline controls, year status, construction checkpoint, archive index, ID crosswalk and research log. It deliberately does **not** change 501/503/505 building histories or ownership records because October supplies no target-number occupant or target physical/property event.

## Next chronological step

Continue with **November 1919 Enterprise** online scans while preserving the November Banner-Courier dates under `MF-030`.
'''
write(CAPTURE,capture)

append_once("evidence/source-register.md",MARKER,f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans plus retrieval-gap manifest; **40/40 online-exposed pages VISUALLY VERIFIED** 8 September 2026.  
Coverage: Enterprise 3/10/17/24/31 Oct., 40 pages; Banner-Courier 2/9/16/23/30 Oct. **manual retrieval gaps** under `MF-030`.  
Repository originals: `newspapers/oregon-city-enterprise/1919-october/`; gap manifest `newspapers/banner-courier/1919-october/manifest.json`.  
Related evidence: `{E}`.  
Notes: No source-explicit 501/503/505/505½ occupant or target physical-building/property event. Theroux Music House is directly at 210 Seventh on 3/17/31 Oct., extending direct continuity through 31 Oct.; OCR leading-digit errors are rejected after scan review.''')

append_once("evidence/evidence-register.md",MARKER,f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper online scan batch with explicit successor-title retrieval gap.  
Source: `{S}`.  
Claims:
- all **40/40 online-exposed October Enterprise pages** were visually inspected from the original scans;
- Theroux Music House is directly printed at **210 Seventh Street** on 3, 17 and 31 October, extending the dated address control through **31 October 1919**;
- OCR/text readings `S10` / `110` are rejected where the original scan visibly reads **210**;
- no source-explicit 501/503/505/505½ occupant or target construction/property event was established in the online pages;
- the 3 October `building south of the post office` hit is explicitly an **Estacada** item, not Oregon City;
- 31 October pool-room references and the Henry Wolfer surname hit do not bridge to the target frontage, S. Wolf, or Wolf & Miller;
- October Banner-Courier issues remain manual retrieval gaps under `MF-030`.
Classification: **DOCUMENTED / DIRECT** for scan-visible Theroux address and inspected-page count; **COVERAGE RESULT ONLY** for the no-target finding; **RETRIEVAL GAP** for inaccessible Banner-Courier issues.  
Confidence: **Very High** for scan-visible wording and page coverage.''')

append_once("database/sources.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary October scan batch: 40/40 Enterprise pages visually verified. Banner-Courier 2, 9, 16, 23 and 30 October remain MF-030 manual retrieval gaps. Theroux Music House is directly at 210 Seventh through 31 October; no exact target-number occupant or target structural/property event was established.\n''')
append_once("database/evidence.yml",YAML_MARKER,YAML_MARKER+f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper online scan batch with explicit manual retrieval gap\n    claims:\n      - 40/40 online-exposed October 1919 Enterprise pages visually verified.\n      - Theroux Music House is directly printed at 210 Seventh Street on 3, 17 and 31 October 1919.\n      - OCR S10 or 110 readings are rejected where the original scans visibly read 210.\n      - No source-explicit 501, 503, 505 or 505-half Main occupant or target physical-building/property event was established.\n      - The 3 October building-south-of-post-office item is explicitly Estacada, not Oregon City.\n      - October Banner-Courier issues remain manual microfilm retrieval gaps under MF-030.\n    confidence: Very High for visible online pages; retrieval gap for inaccessible Banner-Courier issues\n    related_sources: [{S}]\n    related_businesses: [BUS-029]\n    related_people: [P-044]\n    related_buildings: []\n''')

append_once("businesses/ff-theroux.md",MARKER,f'''## October 1919 — 210 Seventh Street continuation
{MARKER}

The visually verified **3 Oct. p7, 17 Oct. p7 and 31 Oct. p3** Enterprise advertisements (`{S}` / `{E}`) print **Theroux Music House, 210 Seventh St.** OCR/text derivatives misread the leading digit on some occurrences, but the original scans clearly read **210**. This extends the direct dated business-address chronology through **31 October 1919** without proving the exact move date from 519 Main or property ownership.
''')
append_once("people/profiles/ff-theroux.md",MARKER,f'''## October 1919 address continuation
{MARKER}

`{S}` / `{E}` directly continues Theroux Music House at **210 Seventh Street through 31 October 1919**. OCR/text leading-digit errors are rejected after scan inspection. This is a business-location control, not property ownership.
''')

# Keep structured entity relations synchronized.
for path,eid in [("database/businesses.yml","BUS-029"),("database/people.yml","P-044")]:
    update_yaml_relation(path,eid,"related_evidence",E)
    update_yaml_relation(path,eid,"related_sources",S)

append_once("registers/address-register.md",MARKER,f'''| 210 Seventh Street | Theroux Music House (`BUS-029`) | `{E}` | Visually verified Enterprise ads on 3/17/31 Oct. 1919 extend the direct address control through 31 Oct.; OCR leading-digit errors rejected. |
{MARKER}''')
append_once("registers/business-timeline.md",MARKER,f'''| 31 Oct. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | October Enterprise ads on 3/17/31 Oct. directly continue the address through month end. |
{MARKER}''')
append_once("timeline.md",MARKER,f'''## October 1919 — Theroux continues at 210 Seventh; target frontage not identified
{MARKER}

The complete online-exposed October Enterprise batch (`{S}` / `{E}`) comprises **40/40 visually reviewed pages**. Original advertisements on **3, 17 and 31 October** directly print **Theroux Music House, 210 Seventh Street**, extending the dated control through month end. No source-explicit 501/503/505/505½ occupant or target construction/property event was established in the October Enterprise pages. October Banner-Courier remains a manual microfilm gap under `MF-030`; no negative inference is made across that inaccessible title.
''')
append_once("indexes/id-crosswalk.md",MARKER,f'''## {S} / {E} — October 1919 Enterprise visual review
{MARKER}

| Source / evidence | Entity / topic | Scope and limit |
| --- | --- | --- |
| `{S}` / `{E}` | `BUS-029` / `P-044` Theroux Music House | 40/40 October Enterprise pages visually verified; Theroux directly at 210 Seventh on 3/17/31 Oct. No exact 501/503/505/505½ occupant or target physical/property event. October Banner-Courier remains `MF-030`. |
''')
append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md",MARKER,f'''## October 1919 monthly visual addition
{MARKER}

The complete online-exposed October Enterprise pass (`{S}` / `{E}`) visually reviewed **40/40 pages** and found no source-explicit 501/503/505/505½ occupant or target construction, demolition, rebuilding, remodeling, fire, sale, lease or ownership event. The seemingly relevant **3 October building south of the post office** item was visually resolved as an **Estacada** feed-store notice. October Banner-Courier remains unavailable online under `MF-030`; this is bounded Enterprise coverage only, not evidence that no target work occurred.
''')
append_once("evidence/source-captures/1919-1920-session-save-checkpoint-2026-09-08.md",MARKER,f'''## October 1919 annual-review continuation
{MARKER}

After the narrow 1919–1920 construction pass reached its authenticated/manual boundary, year-level online work continued chronologically. `{S}` / `{E}` now records **40/40 October Enterprise pages visually verified**, bringing the January–October online local-newspaper visual count to **516 pages**. Theroux Music House is directly at 210 Seventh through 31 October. No exact target-number or target structural/property event emerged. November Enterprise is the next chronological online step; Banner-Courier remains `MF-030`.
''')
append_once("ARCHIVE_INDEX.md",MARKER,f'''## October 1919 complete online Enterprise visual batch
{MARKER}

- [`{CAPTURE}`]({CAPTURE}) — `{S}` / `{E}`; **40/40** October Enterprise pages visually verified.
- **1919 remains IN PROGRESS.** January–October cumulative online local-newspaper visual count: **516 pages**.
- Theroux Music House is directly at **210 Seventh Street through 31 Oct. 1919**.
- No source-explicit 501/503/505/505½ occupant or target physical/property event established in October Enterprise.
- Banner-Courier 2/9/16/23/30 Oct. remains `MF-030`; next chronological online step is November Enterprise.
''')
append_once("registers/research-log.md",MARKER,f'''### 2026-09-08 — October 1919 Enterprise complete visual review
{MARKER}
- Preserved originals are in retrieval commit `87f70a09ebcffd020abe4618aac28ee90d503848`; visually inspected **40/40** Enterprise pages for 3/10/17/24/31 Oct. 1919.
- Theroux Music House is directly at **210 Seventh Street** on 3/17/31 Oct.; OCR/text leading-digit errors were rejected against the scans.
- No source-explicit 501/503/505/505½ occupant or target construction/property event was found in the online October pages.
- The 3 Oct. `building south of the post office` candidate is Estacada, not Oregon City; 31 Oct. pool-room and Wolfer hits are unrelated to the target.
- Banner-Courier 2/9/16/23/30 Oct. remains `MF-030` manual microfilm gap.
- Integrated monthly batch as `{S}` / `{E}`; 1919 stays **IN PROGRESS** with **516** online local-newspaper pages visually reviewed Jan-Oct.
''')

update_1919_status()
print(f"Integrated October 1919 visual batch as {S} / {E}")
