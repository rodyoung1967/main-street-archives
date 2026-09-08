#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 May Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 May Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-may-enterprise-courier-visual-review-2026-09-07.md"
SOURCE_NAME = "May 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"
EVIDENCE_NAME = "May 1919 visual review: unlocated Wolf building confectionery alterations and neighboring business controls"


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
        raise RuntimeError(f"No {prefix} ids in {path}")
    return f"{prefix}-{max(nums)+1:03d}"


def update_yaml_relation(path, entity_id, field, value):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    m = re.search(rf"(?ms)^  - id: {re.escape(entity_id)}\n.*?(?=^  - id: |\Z)", text)
    if not m:
        return False
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


if Path(CAPTURE).exists():
    print("May capture already exists; refusing duplicate integration.")
    sys.exit(0)

S = next_id("evidence/source-register.md", "S")
E = next_id("evidence/evidence-register.md", "E")
T = next_id("database/timeline.yml", "T")

capture = f'''# May 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 72/72 recovered May pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. January–May cumulative local-newspaper visual coverage: **310 pages**.

Archive IDs: source `{S}`; evidence `{E}`; timeline `{T}`.

## Scope

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Courier* | 1, 8, 15, 22, 29 May 1919 | **32/32** |
| *Oregon City Enterprise* | 2, 9, 16, 23, 30 May 1919 | **40/40** |
| **May total** | **10 issues** | **72/72** |

Preserved originals:
- `newspapers/oregon-city-courier/1919-may/`
- `newspapers/oregon-city-enterprise/1919-may/`

Retrieval commit: `a9bf195` (`Archive May 1919 Oregon City newspaper scans`).

Every recovered page was visually checked for printed issue date and page number before text-assisted discovery. The first four Courier issues contain six pages each; the 29 May Courier is a genuine eight-page issue. Every Enterprise issue contains eight pages. No substituted-page, duplicate-page, or printed-date defect was found in the recovered May set.

## Major lead — 16 May "Wolf building" alterations for a new confectionery

The original **16 May 1919 Enterprise p2** scan contains an item headed **NEW CONFECTIONERY OPEN.** It directly states that **“The alterations of the Wolf building are nearing completion.”** The article describes a full-length rustic porch along the front, a rustic pergola at the side, and a blue-and-white interior in connection with the new confectionery.

Classification: **DOCUMENTED / DIRECT** for the printed `Wolf building` wording, alteration activity, confectionery context and described physical improvements.

### Identity and location limitation

The item prints:
- no street address;
- no Wolf first name or initials;
- no confectionery proprietor or trade name;
- no statement connecting the building to Wolf & Miller;
- no statement connecting it to S. Wolf of Portland;
- no statement placing it at 501, 503 or 505 Main.

Therefore the May item is an **UNLOCATED / UNRESOLVED SAME-NAME BUILDING LEAD**. It must not be assigned to `BUS-012`, S. Wolf, 503 Main, 505 Main, or the later 1922 fire property without independent evidence.

The lead is still important because it documents a substantial Oregon City building alteration during the period when the surviving 503/505 construction chronology remains unresolved. It should be followed forward and backward through advertisements, confectionery notices, permits, directories, deeds and owner references, but it is not itself a target-frontage building event.

## Ohio Dentists — 507½ Main over Harding's Drug Store

The visually reopened **16 May Enterprise p6** advertisement directly prints:
- **Ohio Dentists**;
- **Dr. J. G. Nash, Manager**;
- **507½ Main Street**;
- **over Harding's Drug Store**;
- **Phone 62**.

This extends the direct 507½-over-Harding office-location run through **16 May 1919**. The ad still does not print Harding Drug Store's own lower-floor street number, so a direct exact `507 Main` assignment to Harding is not created from this source.

## Farr Brothers market-report continuation

The visually reopened Enterprise market reports on **2 May p2, 9 May p6, 16 May p6, 23 May p3 and 30 May p3** each credit **Brady Mercantile Company and Farr Brothers**. These are dated local-business appearances only. They print no exact address or individual Farr proprietor and do not bridge this business to Edwin/Alice Farr, Farr's Pool Hall at 505, Carl Harr or Harr's Recreation Center.

## Theroux Music House — 210 Seventh Street through 30 May

Visually reopened Enterprise advertisements on **2 May p3, 9 May p2, 16 May p2, 23 May p3 and 30 May p6** directly continue **Theroux Music House, 210 Seventh St.** This extends the direct Seventh Street address chronology through **30 May 1919**. It does not establish the exact date the business left its earlier 519 Main location.

## Fifth and Main Memorial Day meeting-point controls

The **8 May Courier p1** and **9 May Enterprise p3** describe a Memorial Day-related assembly at the **corner of Fifth and Main streets** before participants proceeded to the First Baptist Church. These are public meeting-point/location controls only. They do not identify the Post Office's exact numbered bay or any 501/503/505 occupant.

## Rohberger / Rohrberg and billiard-parlor follow-forward

No May page produced a defensible local-business occurrence of `Rohberger` or `Rohrberg`, and no commercial billiard/pool-hall premises was tied to the February–March Cox transfer sequence. A 29 May Courier report about a billiard table in a labor-temple payment dispute is unrelated to that commercial-parlor question.

This is bounded May coverage only, not evidence that the Cox/Rohberger business closed, moved or ceased operation.

## Post Office exact-bay follow-forward

No May page supplied a source-explicit numbered address for the Post Office that moved to Fifth and Main on 15 April. The April ownership/geometry findings remain controlling, and the exact postal bay is still unresolved.

## Target frontage — 501 / 503 / 505 Main

Across all 72 visually reviewed May pages and the post-visual text-discovery pass:
- no defensible source-explicit **501 Main** occupant was found;
- no defensible source-explicit **503 Main** occupant was found;
- no defensible source-explicit **505 Main** occupant was found;
- no May Wolf & Miller exact-address continuation was found;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move or fire event was found.

The unlocated **Wolf building** alteration item is deliberately not converted into a 503/505 event.

**This is bounded May coverage only. It is not evidence of vacancy, non-use, closure, demolition or absence of an occupant.**

## Cross-Record Propagation Audit

Propagated: source/evidence registers and YAML; Wolf same-name guardrails and 1922 S. Wolf lead; 1919–20 construction checkpoint; Ohio Dentists/Nash and Harding spatial chronology; Farr Brothers; Theroux; master/business/address timelines; database timeline; open questions/research leads; crosswalk; year status; archive index; historical-society supplement; and research log.

No 501/503/505 building event or Wolf identity relation is created because May does not supply a direct premises or person bridge.

## Next chronological step

Continue with **June 1919 Enterprise + Courier** under the same scan-first standard. High-value follow-forward targets include the identity/location of the May `Wolf building` confectionery, the exact Post Office numbered bay, Rohberger/Rohrberg billiard premises, and any exact 501/503/505 occupant or construction/property transition.
'''
write(CAPTURE, capture)

append_once("evidence/source-register.md", MARKER, f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: Courier 1/8/15/22/29 May, 32 pages; Enterprise 2/9/16/23/30 May, 40 pages; **72/72 total**.  
Repository originals: `newspapers/oregon-city-courier/1919-may/` and `newspapers/oregon-city-enterprise/1919-may/`.  
Related evidence: `{E}`.  
Notes: 16 May Enterprise p2 directly reports alterations of an unlocated `Wolf building` nearing completion in a new-confectionery context, with rustic porch/pergola and blue-white interior; no address, Wolf identity or proprietor is printed, so no link to Wolf & Miller, S. Wolf, 503 or 505 is made. Ohio Dentists continues at 507½-over-Harding on 16 May; Farr Brothers market credits recur all five Enterprise issues; Theroux continues at 210 Seventh through 30 May. No source-explicit 501/503/505 occupant; bounded coverage only.''')

append_once("evidence/evidence-register.md", MARKER, f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **72/72** recovered May pages were visually inspected after printed date/page identity review;
- 16 May Enterprise p2 directly reports alterations of the **Wolf building** nearing completion in a new-confectionery context and describes a rustic front porch, side pergola and blue-and-white interior;
- the Wolf building's address, owner identity and confectionery proprietor are unprinted, so it is not linked to Wolf & Miller, S. Wolf, 503 Main or 505 Main;
- 16 May Enterprise p6 repeats **Ohio Dentists / Dr. J. G. Nash at 507½ Main over Harding's Drug Store**;
- all five May Enterprise market reports credit **Brady Mercantile Company and Farr Brothers** without address or proprietor;
- Theroux Music House continues at **210 Seventh Street** through 30 May;
- no source-explicit 501/503/505 occupant or target physical-building event was established; no-hit is bounded coverage only.
Confidence: **Very High** for scan-visible wording and monthly page coverage; **Unresolved** for Wolf-building identity/location; none for an unprinted target-premises bridge.''')

append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary scan batch, visually verified 72/72 May pages: 32 Courier and 40 Enterprise.\n      A 16 May Enterprise item directly reports alterations to an unlocated Wolf building in a\n      new-confectionery context but prints no address, Wolf identity or proprietor. Ohio Dentists,\n      Farr Brothers and Theroux controls continue. No exact 501/503/505 occupant was established.\n''')

append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper scan batch\n    claims:\n      - 72/72 recovered May 1919 pages visually verified.\n      - A 16 May Enterprise item reports alterations to the unlocated Wolf building in a new-confectionery context; no address, Wolf identity or proprietor is printed.\n      - Ohio Dentists and Dr. J. G. Nash continued at 507½ Main over Harding's Drug Store on 16 May.\n      - Farr Brothers appeared in all five May Enterprise market reports without address or individual proprietor.\n      - Theroux Music House continued at 210 Seventh Street through 30 May.\n      - No source-explicit 501, 503 or 505 Main occupant or target physical-building event was established.\n    confidence: Very High for scan-visible wording and page coverage; unresolved for Wolf-building identity and location\n    related_sources: [{S}]\n    related_evidence: []\n    related_businesses: [BUS-106, BUS-007, BUS-104, BUS-029]\n    related_people: [P-397, P-044]\n    related_buildings: [B-003]\n    sources: [{S}]\n    notes: >-\n      The May Wolf-building item is retained as an unlocated same-name research lead only. It must\n      not be assigned to BUS-012, S. Wolf, 503 Main or 505 Main without an independent bridge.\n''')

append_once("businesses/ohio-painless-dentists.md", MARKER, f'''## May 1919 continuation
{MARKER}

The visually verified **16 May Enterprise p6** advertisement (`{E}` / `{S}`) repeats **Ohio Dentists**, **Dr. J. G. Nash, Manager**, **507½ Main Street**, **over Harding's Drug Store**, Phone 62. This extends the direct office-location run through **16 May 1919**. Harding's own lower-floor number remains unprinted in this ad.
''')
append_once("people/profiles/j-g-nash.md", MARKER, f'''## May 1919 continuation
{MARKER}

`{E}` / `{S}` visually verifies Dr. J. G. Nash again as manager of Ohio Dentists at **507½ Main over Harding's Drug Store** on **16 May 1919**.
''')
append_once("businesses/harding-drug-store.md", MARKER, f'''## May 1919 507½-over-Harding continuation
{MARKER}

The visually verified **16 May 1919 Enterprise p6** Ohio Dentists advertisement (`{E}` / `{S}`) again places the **507½ Main** dental office **over Harding's Drug Store**. It preserves the spatial relationship but does not directly print Harding's ground-floor street number.
''')
append_once("buildings/507-harding-building.md", MARKER, f'''## May 1919 507½ office control
{MARKER}

`{E}` / `{S}` directly continues Ohio Dentists / Dr. J. G. Nash at **507½ Main, over Harding's Drug Store**, on **16 May 1919**. The half-number is a direct address designation; the source does not establish floor geometry or print Harding Drug Store's own exact number.
''')
append_once("businesses/farr-brothers-store.md", MARKER, f'''## May 1919 market-report continuation
{MARKER}

The visually reopened **2/9/16/23/30 May 1919 Enterprise** market reports each credit **Brady Mercantile Company and Farr Brothers** (`{E}` / `{S}`). No address or individual Farr proprietor is printed. This does not bridge the store to Edwin/Alice Farr or Farr's Pool Hall at 505 Main.
''')
append_once("businesses/ff-theroux.md", MARKER, f'''## May 1919 — 210 Seventh Street continuation
{MARKER}

`{E}` / `{S}` visually verifies Theroux Music House advertisements at **210 Seventh Street** on all five May Enterprise issue dates, extending the direct address chronology through **30 May 1919** without proving the exact move date from 519 Main.
''')
append_once("people/profiles/ff-theroux.md", MARKER, f'''## May 1919 address continuation
{MARKER}

`{E}` / `{S}` continues Theroux Music House at **210 Seventh Street** through **30 May 1919**. This is a dated business-location control, not a property-ownership claim.
''')

append_once("businesses/wolf-miller.md", MARKER, f'''## 16 May 1919 unlocated “Wolf building” lead — NOT an identity bridge
{MARKER}

A visually verified **16 May 1919 Enterprise p2** item (`{E}` / `{S}`) reports alterations nearing completion to a **Wolf building** in connection with a new confectionery and describes a rustic front porch, side pergola and blue-and-white interior. The article prints **no address, no Wolf first name/initials, no proprietor, and no Wolf & Miller trade name**.

This is retained here only as a same-name research lead. It is **not evidence that the building belonged to Wolf & Miller, the firm's unidentified Wolf partner, S. Wolf of Portland, 503 Main, or 505 Main**. The existing 1918 Wolf & Miller address evidence and conflicts remain unchanged.
''')
append_once("evidence/source-captures/1922-fire-s-wolf-main-street-property-lead.md", MARKER, f'''## 16 May 1919 backward lead — unlocated “Wolf building” alteration
{MARKER}

A visually verified **16 May 1919 Enterprise p2** item (`{E}` / `{S}`) says alterations of **the Wolf building** were nearing completion in a new-confectionery context, with a rustic porch, side pergola and blue-and-white interior. It prints no address, Wolf first name/initials, proprietor or connection to the later 1922 property sequence.

This is a potentially useful backward lead but **does not identify S. Wolf**, does not establish that S. Wolf owned Oregon City property in May 1919, and does not bridge the building to the 1922 ignition property or the earlier Wolf & Miller business. Keep the 1919 item separate until independent address/identity evidence connects them.
''')
append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", MARKER, f'''## May 1919 monthly visual addition — unlocated Wolf building alteration
{MARKER}

The **16 May 1919 Enterprise p2** scan (`{E}` / `{S}`) directly reports alterations nearing completion to an unlocated **Wolf building** in connection with a new confectionery. Architectural details include a rustic front porch, side pergola and blue-and-white interior. Because the item gives no address, owner identity or proprietor, it **cannot be assigned to 501/503/505 or used as proof of the surviving 503/505 construction date**. It remains a high-value location/identity lead for the broader 1919 structural-change question.
''')

append_once("timeline.md", MARKER, f'''## 16 May 1919 — unlocated Wolf building alterations; May newspaper batch complete
{MARKER}

The **16 May Enterprise p2** scan (`{S}` / `{E}`) directly reports alterations nearing completion to **the Wolf building** in a new-confectionery context, describing a full-length rustic front porch, side pergola and blue-and-white interior. The item gives no address, Wolf identity or proprietor. It is therefore an **unlocated building-alteration lead**, not a 503/505 event and not a bridge to Wolf & Miller or S. Wolf.

The full May batch is **72/72 visually verified pages**, bringing January–May 1919 local-newspaper coverage to **310 pages**. Ohio Dentists/Nash continues at 507½-over-Harding on 16 May; Farr Brothers appears in all five May market reports without address/proprietor; Theroux remains at 210 Seventh through 30 May. No source-explicit 501/503/505 occupant or target construction/property event was established; bounded coverage only.
''')
append_once("registers/business-timeline.md", MARKER, f'''| 16 May 1919 | address not printed | New confectionery / “Wolf building” alterations | Unresolved | `{E}` | Article reports alterations nearing completion and physical improvements; no proprietor, Wolf identity or address. Do not assign to BUS-012, S. Wolf, 503 or 505. |
| 16 May 1919 | 507½ Main | Ohio Dentists / Dr. J. G. Nash | `BUS-106` | `{E}` | Direct ad says 507½ Main, over Harding's Drug Store; Harding's own number not printed. |
| May 1919 | address not printed | Farr Brothers market-report provider | `BUS-104` | `{E}` | 2/9/16/23/30 May Enterprise credits with Brady Mercantile; no proprietor/address bridge to 505. |
| 30 May 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | Direct May advertising continues the Seventh Street address. |
{MARKER}''')
append_once("registers/address-register.md", MARKER, f'''| 507½ Main — 16 May 1919 | Upstairs/internal geometry unresolved | `businesses/ohio-painless-dentists.md` | BUS-106 | `{E}` | Ohio Dentists / Dr. J. G. Nash; directly described as over Harding's Drug Store. |
| Fifth & Main corner — 8–9 May 1919 | Public meeting-point control only; exact corner/bay not assigned | `evidence/source-captures/1919-may-enterprise-courier-visual-review-2026-09-07.md` | Memorial Day assembly | `{E}` | Courier/Enterprise describe assembly at Fifth and Main before proceeding to First Baptist Church; not an occupant or Post Office bay identification. |
{MARKER}''')

append_once("evidence/open-questions.md", MARKER, f'''## May 1919 “Wolf building” questions
{MARKER}

1. Where was the **Wolf building** whose alterations were nearing completion on 16 May 1919?
2. Who owned or controlled that building, and who opened/operated the new confectionery?
3. Is the `Wolf` name connected to the unidentified Wolf partner in Wolf & Miller, to **S. Wolf of Portland** in 1922, to another Wolf family, or merely to a building name with no relevant identity continuity?
4. Can contemporary advertisements, permits, directories, deeds or later confectionery references supply a numbered address without projecting the later 1922 property evidence backward?
''')
append_once("evidence/research-leads.md", MARKER, f'''## May 1919 Wolf-building / confectionery identification route
{MARKER}

**Priority: HIGH — ONLINE FIRST.** The 16 May 1919 Enterprise (`{S}` / `{E}`) directly documents substantial alterations to an unlocated **Wolf building** in a new-confectionery context. Search May–July 1919 Enterprise/Courier advertising and local items for the confectionery opening, porch/pergola descriptions, `Wolf building`, proprietor names, address wording and later business references. Cross-check 1919–20 directories and property/permit sources. Treat Wolf & Miller (`BUS-012`) and S. Wolf of Portland as separate candidates unless a contemporary source explicitly bridges identity or premises.
''')
append_once("indexes/id-crosswalk.md", MARKER, f'''## {S} / {E} — May 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` → unlocated **Wolf building** alteration/new-confectionery lead on 16 May; no entity/address bridge created.
- `{S}` / `{E}` → `BUS-106` / `P-397` and `B-003` context: Ohio Dentists at 507½ Main over Harding's Drug Store on 16 May.
- `{S}` / `{E}` → `BUS-104` Farr Brothers market-report continuation across all five Enterprise issues.
- `{S}` / `{E}` → `BUS-029` / `P-044` Theroux Music House at 210 Seventh through 30 May.
- `{T}` → 16 May 1919 unlocated Wolf-building alteration event.
''')
append_once("records/historical-society/503-505-main-historical-society-research-supplement-2026-08-24.md", MARKER, f'''## May 1919 unlocated Wolf-building alteration lead
{MARKER}

The complete May 1919 scan-first pass (`{S}` / `{E}`) found a 16 May Enterprise report that alterations to **the Wolf building** were nearing completion in a new-confectionery context. The source does **not** print an address, Wolf identity or proprietor. It therefore cannot be used to date construction/remodeling at 503 or 505 and should not be connected to the 1918 Wolf & Miller business or 1922 S. Wolf property owner without independent evidence. It remains a potentially important clue for the unresolved c.1919/c.1920 building-change question.
''')
append_once("registers/research-log.md", MARKER, f'''| 2026-09-07 | Completed May 1919 Enterprise + Courier scan-first visual audit | **72/72 pages**: Courier 32/32 (1/8/15/22/29 May; 29 May is eight pages) + Enterprise 40/40 (2/9/16/23/30 May), bringing Jan–May cumulative local-newspaper visual coverage to **310 pages**. Major lead: 16 May Enterprise reports alterations to an unlocated `Wolf building` in a new-confectionery context; no address/identity bridge, so no 503/505 or Wolf & Miller/S. Wolf assignment. Ohio Dentists/Nash, Farr Brothers and Theroux controls extended. No exact 501/503/505 occupant or target construction event; bounded coverage only. Created `{S}` / `{E}` / `{T}`. 1919 remains IN PROGRESS; next chronological batch June. |
{MARKER}''')
append_once("ARCHIVE_INDEX.md", MARKER, f'''## 1919 May complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- May local-newspaper coverage: **72/72 visually verified pages** (`{S}` / `{E}`); Jan–May cumulative **310 pages**.
- 16 May: unlocated **Wolf building** alterations/new-confectionery lead; no address, Wolf identity or proprietor, and no 503/505 assignment.
- Ohio Dentists at 507½-over-Harding on 16 May; Farr Brothers market-report continuation on all five Enterprise dates; Theroux at 210 Seventh through 30 May.
- No source-explicit 501/503/505 occupant or target construction/property event; bounded coverage only.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological batch: **June 1919 Enterprise + Courier**.
''')

# Database timeline event for the dated, unlocated alteration lead.
timeline_yml = read("database/timeline.yml")
if not re.search(rf"(?m)^  - id: {re.escape(T)}\s*$", timeline_yml):
    timeline_yml = timeline_yml.rstrip() + f'''\n\n  - id: {T}\n    date: 16 May 1919\n    summary: Oregon City Enterprise reports alterations to the unlocated Wolf building nearing completion in a new-confectionery context, with a rustic front porch, side pergola and blue-and-white interior; no address, Wolf identity or proprietor is printed.\n    confidence: Very High for visible article wording and alteration details; unresolved for building location, Wolf identity and any connection to 503/505, Wolf & Miller or S. Wolf\n    related_evidence:\n      - {E}\n    related_sources:\n      - {S}\n''' + "\n"
    write("database/timeline.yml", timeline_yml)

# Synchronize only entities directly named/located by May evidence. Deliberately do NOT link BUS-012 or a 503/505 building.
for entity in ["BUS-106", "BUS-007", "BUS-104", "BUS-029"]:
    update_yaml_relation("database/businesses.yml", entity, "related_evidence", E)
    update_yaml_relation("database/businesses.yml", entity, "related_sources", S)
for entity in ["P-397", "P-044"]:
    update_yaml_relation("database/people.yml", entity, "related_evidence", E)
    update_yaml_relation("database/people.yml", entity, "related_sources", S)
update_yaml_relation("database/buildings.yml", "B-003", "related_evidence", E)
update_yaml_relation("database/buildings.yml", "B-003", "related_sources", S)

# Canonical annual status row.
ys = read("registers/year-status.md")
lines = ys.splitlines()
found = False
for i, line in enumerate(lines):
    if line.startswith("| 1919 |"):
        lines[i] = (
            f"| 1919 | **IN PROGRESS** | `{CAPTURE}`; "
            "`evidence/source-captures/1919-april-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-march-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | "
            f"January–May scan-first local-newspaper coverage **310 visually verified pages**: January 70 + February 56 + March 56 + April 56 + May 72 (`{S}`/`{E}` for May). "
            "May directly documents alterations to an unlocated `Wolf building` in a new-confectionery context but supplies no address, Wolf identity or proprietor, so no link is made to 503/505, Wolf & Miller or S. Wolf. "
            "Ohio Dentists at 507½-over-Harding, Farr Brothers market credits and Theroux at 210 Seventh continue; no exact 501/503/505 occupant or target construction event. "
            "June–December annual visual work and other online source classes remain; Banner-Courier from 17 July 1919 has a documented manual microfilm gap. |"
        )
        found = True
        break
if not found:
    raise RuntimeError("1919 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

print(f"Integrated May 1919 as {S} / {E} / {T}")
