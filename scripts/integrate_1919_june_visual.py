#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 June Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 June Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-june-enterprise-courier-visual-review-2026-09-07.md"
SOURCE_NAME = "June 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"
EVIDENCE_NAME = "June 1919 visual review: bounded target-frontage coverage and business controls"


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
            indent = item_indent or "      "
            lines.insert(j, f"{indent}- {value}\n")
            block = "".join(lines)
    text = text[:m.start()] + block + text[m.end():]
    p.write_text(text, encoding="utf-8")
    return True


if Path(CAPTURE).exists():
    print("June capture already exists; refusing duplicate integration.")
    sys.exit(0)

S = next_id("evidence/source-register.md", "S")
E = next_id("evidence/evidence-register.md", "E")

capture = f'''# June 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 56/56 recovered June pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. January–June cumulative local-newspaper visual coverage: **366 pages**.

Archive IDs: source `{S}`; evidence `{E}`.

## Scope

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Courier* | 5, 12, 19, 26 Jun. 1919 | **24/24** |
| *Oregon City Enterprise* | 6, 13, 20, 27 Jun. 1919 | **32/32** |
| **June total** | **8 issues** | **56/56** |

Preserved originals:
- `newspapers/oregon-city-courier/1919-june/`
- `newspapers/oregon-city-enterprise/1919-june/`

Retrieval commit: `8c6ac10` (`Archive June 1919 Oregon City newspaper scans`).

Every recovered page was visually checked as a scan image for printed title/date/page identity before text-assisted discovery and high-resolution reopening of candidates. Courier issues contain six pages each and Enterprise issues eight pages each. No substituted-page, duplicate-page, or printed-date defect was found in the recovered June set.

## Target frontage — 501 / 503 / 505 Main

Across all 56 visually reviewed June pages and the post-visual text-discovery backstop:
- no defensible source-explicit **501 Main** occupant was recovered;
- no defensible source-explicit **503 Main** occupant was recovered;
- no defensible source-explicit **505 Main / 505½ Main** occupant was recovered;
- no defensible source-explicit **507 / 507½ / 509 / 511 Main** target-neighbor address occurrence was recovered;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move or fire event was recovered.

**This is bounded June coverage only. It is not evidence of vacancy, closure, demolition, non-use, relocation, or absence of an occupant.**

## May “Wolf building” follow-forward

The June batch produced no source-explicit continuation identifying the **Wolf building** whose alterations were reported on 16 May. No June page supplied an address, Wolf identity, proprietor, confectionery trade name, or other bridge to Wolf & Miller, S. Wolf, 503 Main or 505 Main.

This leaves the May item as an **unlocated / unresolved same-name building lead**. June silence does not establish that the confectionery closed, moved, changed name, or was outside the target block.

## 13 June — Clem Dollar court item visually resolved

The **13 Jun. Enterprise p1** scan was visually reopened. The item headed **“Judgment Given To Local Butcher”** reports a judgment in R. Petzold's dispute with **Clem Dollar** over goods alleged to have been sold mostly during 14–26 June 1915. It supplies **no business name, street address, pool-hall premises, or 501/503/505 relationship**.

This visually confirms the earlier OCR-candidate disposition in `1918-1920-505-transition-candidate-triage-2026-08-31.md`: the page is unrelated to the later exact 505½ pool-hall sequence. Do not back-project the documented 1920 block-level Clem Dollar pool hall to 1919 from this legal item.

## Farr Brothers — county-claim/vendor context

The **26 Jun. Courier p6** and **27 Jun. Enterprise p7** scans were visually reopened. The County Court claims material includes **Farr Bros.** as a named payee/vendor. This is a dated local-business appearance only. It prints no exact business address and supplies no individual Farr proprietor or bridge to Edwin/Alice Farr, Farr's Pool Hall at 505, Carl Harr or Harr's Recreation Center.

The two appearances are parallel publication of county-claims material, not independent evidence of a separate transaction.

## Theroux Music House — 210 Seventh Street through 27 June

The **27 Jun. Enterprise p7** scan directly prints a Theroux Music House classified advertisement at **210 Seventh St.** This extends the direct Seventh Street business-address chronology through **27 June 1919**. It does not establish the exact departure date from the earlier 519 Main location and does not concern 501/503/505.

## Non-target candidates resolved

### Falls Restaurant sale — address not printed in the June article
The **19 Jun. Courier p1** scan reports the **Falls Restaurant** sold to **Charles Griffin of Vancouver**, with former owner **John Bauer** disposing of the restaurant/confectionery business because of failing health. The June item prints no numbered address. Later repository evidence places a Falls restaurant at **Seventh and Main** in 1922; the June source itself does not justify projecting that later address backward or treating this as a Fifth/Main target-frontage event.

### Prouty confectionery / pool tables — Canby context
The **20 Jun. Enterprise p3** item headed **“PROUTY'S STORE IMPROVED”** describes improvements to Prouty's confectionery/ice-cream parlors and billiard/pool tables at the rear. The page's local-news context is **Canby**, not the 501/503/505 Oregon City frontage. This is a false target lead and is not promoted into the Main Street chronology.

## Cross-Record Propagation Audit

Updated: source/evidence registers and YAML; Farr Brothers business file; Theroux business/person files; 1918–1920 transition-candidate visual-status note; 1919–1920 construction checkpoint; May Wolf-building research lead; business timeline; ID crosswalk; year status; archive index; and research log.

Reviewed but deliberately **not** changed: 501/503/505 building records, master historical timeline, ownership timeline, and Wolf/S. Wolf entity relations. June supplies no source-explicit target occupant, target structural event, ownership event, or Wolf identity/premises bridge. A no-hit is not a historical event.

No new manual-followup item is created: July online newspaper work remains the next ordinary online step, while the existing Banner-Courier gap beginning 17 July 1919 remains `MF-030`.

## Next chronological step

Continue with **July 1919**. Build the title-transition inventory carefully: visually audit all online-exposed Enterprise pages and any early-July Courier pages, preserve the existing **17 Jul. 1919–31 Dec. 1920 Banner-Courier microfilm gap** as `MF-030`, and do not treat that inaccessible interval as negative evidence.
'''
write(CAPTURE, capture)

append_once("evidence/source-register.md", MARKER, f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: Courier 5/12/19/26 Jun., 24 pages; Enterprise 6/13/20/27 Jun., 32 pages; **56/56 total**.  
Repository originals: `newspapers/oregon-city-courier/1919-june/` and `newspapers/oregon-city-enterprise/1919-june/`.  
Related evidence: `{E}`.  
Notes: No source-explicit 501/503/505/505½ occupant or target physical-building event. The May unlocated Wolf-building lead remains unidentified. Farr Bros. appears in county-claims material without address/proprietor; Theroux Music House is directly at 210 Seventh through 27 Jun.; a Clem Dollar legal item supplies no premises. Bounded coverage only.''')

append_once("evidence/evidence-register.md", MARKER, f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **56/56** recovered June pages were visually inspected after printed title/date/page identity review;
- no source-explicit 501/503/505/505½ occupant or target construction/property event was established;
- the May unlocated `Wolf building` lead was not identified or located by the June batch;
- 13 Jun. Enterprise p1 visually confirms the Clem Dollar item is an old debt/court dispute with no business premises or target-address relationship;
- 26/27 Jun. county-claims material names Farr Bros. without address or individual proprietor;
- 27 Jun. Enterprise p7 directly continues Theroux Music House at **210 Seventh Street**;
- the Falls Restaurant sale article prints no address, and the Prouty confectionery/pool-table item is Canby context rather than the target frontage.
Confidence: **Very High** for scan-visible wording and monthly page coverage; none for an unprinted target-premises or Wolf identity bridge.''')

append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary scan batch, visually verified 56/56 June pages: 24 Courier and 32 Enterprise.\n      No exact 501/503/505/505-half occupant or target physical-building event was established.\n      Farr Bros. appears in county-claims context and Theroux remains at 210 Seventh through 27 June.\n''')

append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper scan batch\n    claims:\n      - 56/56 recovered June 1919 pages visually verified.\n      - No source-explicit 501, 503, 505 or 505-half Main occupant or target physical-building event was established.\n      - June did not identify or locate the May unlocated Wolf-building lead.\n      - A 13 June Clem Dollar court item supplies no business premises or target-address relationship.\n      - Farr Bros. appears in late-June county-claims material without address or individual proprietor.\n      - Theroux Music House continued at 210 Seventh Street through 27 June.\n    confidence: Very High for scan-visible wording and page coverage; none for an unprinted target-premises or Wolf identity bridge\n    related_sources: [{S}]\n    related_evidence: []\n    related_businesses: [BUS-104, BUS-029]\n    related_people: [P-044]\n    related_buildings: []\n    sources: [{S}]\n    notes: >-\n      Bounded monthly coverage only. No target vacancy, closure, relocation, demolition, ownership,\n      construction or Wolf-identity inference is made from June silence.\n''')

append_once("businesses/farr-brothers-store.md", MARKER, f'''## June 1919 county-claims appearance
{MARKER}

The visually reopened **26 June Courier p6** and **27 June Enterprise p7** county-claims material names **Farr Bros.** (`{E}` / `{S}`). This is a dated business/payee appearance only. No exact address or individual Farr proprietor is printed, and the parallel newspaper appearances do not create a bridge to Edwin/Alice Farr or Farr's Pool Hall at 505 Main.
''')

append_once("businesses/ff-theroux.md", MARKER, f'''## June 1919 — 210 Seventh Street continuation
{MARKER}

The visually verified **27 June Enterprise p7** classified (`{E}` / `{S}`) directly prints **Theroux Music House, 210 Seventh St.**, extending the direct address chronology through **27 June 1919** without proving the exact move date from 519 Main.
''')

append_once("people/profiles/ff-theroux.md", MARKER, f'''## June 1919 address continuation
{MARKER}

`{E}` / `{S}` directly continues Theroux Music House at **210 Seventh Street** through **27 June 1919**. This is a business-location control, not a property-ownership claim.
''')

append_once("evidence/source-captures/1918-1920-505-transition-candidate-triage-2026-08-31.md", MARKER, f'''## 7 September 2026 visual follow-up on candidate 4
{MARKER}

Candidate **#4, 13 June 1919 Enterprise p1**, has now been visually inspected during the complete June monthly scan pass (`{S}` / `{E}`). The original scan confirms the prior disposition: the item is an old R. Petzold/Clem Dollar debt dispute over goods allegedly sold mostly in June 1915 and prints no pool-hall premises, numbered Main Street address, 505/505½ relationship, or construction event. The prior triage conclusion is unchanged.
''')

append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", MARKER, f'''## June 1919 complete monthly visual addition
{MARKER}

The complete June local-newspaper scan pass (`{S}` / `{E}`) reviewed **56/56 recovered pages** and found no source-explicit construction, demolition, rebuilding, remodeling, lease, sale, move or fire event assignable to **501, 503, 505 or 505½ Main**. It also supplied no address or identity bridge for the unlocated **Wolf building** alteration reported in May. This is bounded coverage only and does not establish that no physical work occurred.
''')

append_once("evidence/research-leads.md", MARKER, f'''## June 1919 follow-forward on May Wolf-building lead
{MARKER}

The complete June monthly scan pass (`{S}` / `{E}`) did **not** identify the May `Wolf building` confectionery by address, proprietor or Wolf identity. Continue the existing **ONLINE-FIRST** route into July: search opening advertisements, confectionery references, porch/pergola descriptions, Wolf-name property references and exact-address wording. June silence is coverage only and does not justify a 503/505 assignment or a same-person merge.
''')

append_once("registers/business-timeline.md", MARKER, f'''| 26–27 Jun. 1919 | address not printed | Farr Bros. county-claims payee/vendor | `BUS-104` | `{E}` | Parallel Courier/Enterprise claims material; no individual proprietor or 505 bridge. |
| 27 Jun. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | Direct classified continues the Seventh Street address. |
{MARKER}''')

append_once("indexes/id-crosswalk.md", MARKER, f'''## {S} / {E} — June 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` → **56/56** June pages visually verified; bounded 501/503/505/505½ coverage only.
- `{S}` / `{E}` → `BUS-104` Farr Bros. late-June county-claims appearance without address/proprietor.
- `{S}` / `{E}` → `BUS-029` / `P-044` Theroux Music House at 210 Seventh through 27 June.
- `{S}` / `{E}` → 13 June Clem Dollar candidate visually resolved as a non-premises debt/court item; no 505 bridge.
- No building, ownership or Wolf-identity relation created from June no-hit coverage.
''')

append_once("registers/research-log.md", MARKER, f'''| 2026-09-07 | Completed June 1919 Enterprise + Courier scan-first visual audit | **56/56 pages**: Courier 24/24 (5/12/19/26 Jun.) + Enterprise 32/32 (6/13/20/27 Jun.), bringing Jan–Jun cumulative local-newspaper visual coverage to **366 pages**. No source-explicit 501/503/505/505½ occupant or target construction/property event; bounded coverage only. May `Wolf building` remains unidentified. 13 Jun. Clem Dollar candidate visually resolved as non-premises debt litigation; Farr Bros. appears in late-June county claims without address/proprietor; Theroux remains at 210 Seventh through 27 Jun. Created `{S}` / `{E}`. No target-building/timeline/ownership event manufactured. Next chronological batch: July 1919, with existing Banner-Courier microfilm gap from 17 Jul. preserved under MF-030. |
{MARKER}''')

append_once("ARCHIVE_INDEX.md", MARKER, f'''## 1919 June complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- June local-newspaper coverage: **56/56 visually verified pages** (`{S}` / `{E}`); Jan–Jun cumulative **366 pages**.
- No source-explicit 501/503/505/505½ occupant or target construction/property event; bounded coverage only.
- May's unlocated `Wolf building` lead remains unidentified; June creates no Wolf/503/505 bridge.
- Farr Bros. appears in late-June county claims without address/proprietor; Theroux remains at 210 Seventh through 27 Jun.; the 13 Jun. Clem Dollar candidate is a non-premises debt/court item.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological batch: **July 1919**, with `MF-030` preserving the Banner-Courier microfilm gap beginning 17 Jul.
''')

# Canonical 1919 year-status row.
ys = read("registers/year-status.md")
lines = ys.splitlines()
found = False
for i, line in enumerate(lines):
    if line.startswith("| 1919 |"):
        lines[i] = (
            f"| 1919 | **IN PROGRESS** | `{CAPTURE}`; "
            "`evidence/source-captures/1919-may-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-april-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-march-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | "
            f"January–June scan-first local-newspaper coverage **366 visually verified pages**: January 70 + February 56 + March 56 + April 56 + May 72 + June 56 (`{S}`/`{E}` for June). "
            "June supplied no source-explicit 501/503/505/505½ occupant or target construction/property event and did not identify the May unlocated Wolf-building lead; bounded coverage only. "
            "Farr Bros. appears in late-June county claims without address/proprietor, Theroux continues at 210 Seventh through 27 Jun., and the 13 Jun. Clem Dollar candidate is visually resolved as a non-premises debt/court item. "
            "July–December annual visual work and other online source classes remain; Banner-Courier from 17 July 1919 has a documented manual microfilm gap (`MF-030`). |"
        )
        found = True
        break
if not found:
    raise RuntimeError("1919 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

# Synchronize relevant business/person YAML relations.
for entity in ["BUS-104", "BUS-029"]:
    update_yaml_relation("database/businesses.yml", entity, "related_evidence", E)
    update_yaml_relation("database/businesses.yml", entity, "related_sources", S)
update_yaml_relation("database/people.yml", "P-044", "related_evidence", E)
update_yaml_relation("database/people.yml", "P-044", "related_sources", S)

print(f"Integrated June 1919 as {S} / {E}")
