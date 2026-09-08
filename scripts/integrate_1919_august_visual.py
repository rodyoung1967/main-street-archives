#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 August Enterprise visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 August Enterprise visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-august-enterprise-visual-review-2026-09-07.md"
SOURCE_NAME = "August 1919 Oregon City Enterprise complete online visual-review batch with Banner-Courier gap"
EVIDENCE_NAME = "August 1919 online visual review: bounded target coverage and repeated neighborhood controls"


def read(path): return Path(path).read_text(encoding="utf-8")
def write(path, text): Path(path).write_text(text, encoding="utf-8")
def append_once(path, marker, block):
    p=Path(path); text=p.read_text(encoding="utf-8")
    if marker in text: return False
    if not text.endswith("\n"): text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text, encoding="utf-8"); return True

def next_id(path, prefix):
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

if Path(CAPTURE).exists():
    print("August capture already exists; refusing duplicate integration.")
    sys.exit(0)

S=next_id("evidence/source-register.md", "S")
E=next_id("evidence/evidence-register.md", "E")

capture=f'''# August 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **ONLINE-EXPOSED PAGES VISUALLY VERIFIED — 40/40 recovered August Enterprise pages inspected from original scans; Banner-Courier manual retrieval gap remains.**  
Annual status: **1919 IN PROGRESS**. January–August online-exposed local-newspaper visual coverage: **444 pages**.

Archive IDs: source `{S}`; evidence `{E}`.

## Scope

| Title | Issues reviewed | Pages | Status |
| --- | --- | ---: | --- |
| *Oregon City Enterprise* | 1, 8, 15, 22, 29 Aug. 1919 | **40/40** | All five online-exposed August issues visually reviewed |
| *The Banner-Courier* | 7, 14, 21, 28 Aug. 1919 | **0** | **RETRIEVAL GAP — manual microfilm (`MF-030`)** |
| **Online visual total** | **5 issues** | **40/40** | Banner-Courier gap excluded from visual count |

Preserved originals / manifests:
- `newspapers/oregon-city-enterprise/1919-august/`
- `newspapers/banner-courier/1919-august/manifest.json`

Retrieval commit: `65001db` (`Archive August 1919 Oregon City newspaper scans and gap manifest`).

Every recovered Enterprise page was visually checked for printed publication/date/page identity before the text-assisted discovery backstop. The five issues each contain eight pages. No substituted-page, duplicate-page, or printed-date defect was found in the recovered Enterprise set.

## Target frontage — 501 / 503 / 505 Main

Across all **40 visually reviewed Enterprise pages** and the post-visual discovery pass:
- no source-explicit **501 Main** occupant was recovered;
- no source-explicit **503 Main** occupant was recovered;
- no source-explicit **505 Main / 505½ Main** occupant was recovered;
- no source-explicit **507 / 507½ / 509 / 511 Main** target-neighbor occurrence was recovered;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move or fire event was recovered;
- no local commercial pool-hall / pool-room / billiard premises was tied to the target frontage.

This is **bounded August Enterprise coverage only**. It does not establish vacancy, closure, non-use, demolition or absence of an occupant, and it cannot be projected across the inaccessible August Banner-Courier issues.

## Re-encountered evidence — cleaner/dyer, already `S-152` / `E-136`

The Enterprise page-7 scans on **1, 8, 15, 22 and 29 August** repeat the unnamed cleaner/dyer classified previously integrated in the eight-week repeat set. The settled direct scan reading is:
- `Clothes cleaned, pressed and dyed.`
- **`500 Fifth and Main streets`**;
- **`two doors south of new post office`**;
- **Phone 260**.

These August pages were already part of the dedicated visual repeat-set evidence (`S-152` / `E-136`) and are therefore referenced rather than registered as a duplicate claim. The advertiser remains unidentified; the unusual printed location is not silently normalized to 500 Main or 500 Fifth and is not merged with Pantorium solely from trade or proximity.

## Theroux Music House — 210 Seventh Street through 29 August

The August page-7 advertising directly continues **Theroux Music House, 210 Seventh St.** across the month, including the **29 August** issue. This extends the direct dated business-address chronology through **29 August 1919** without proving the exact date of the earlier move from 519 Main.

## Farr Brothers — recurring market-report provider, no address/proprietor bridge

Enterprise market reports on **1 Aug. p2, 8 Aug. p3, 15 Aug. p2, 22 Aug. p2 and 29 Aug. p2** credit **Brady Mercantile Company and Farr Brothers**. A county/court expense context on **29 Aug. p6** also prints `Farr Bros.` None of these occurrences gives an exact address or individual Farr proprietor. They do not bridge the concern to Edwin/Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr, or Harr's Recreation Center.

## Clem Dollar candidates — personal context only

The August Enterprise set contains personal/community notices involving **Clem Dollar** on 1, 15, 22 and 29 August. These notices concern motoring, outings and family/community activity; they supply no pool-hall premises, no 505/505½ address and no property/construction relationship. They remain non-premises person context only.

## Remodel / construction candidates resolved visually

Three potentially misleading discovery hits were reopened and resolved against the actual scans:

1. **15 Aug. p5 — Dr. Frank Mount residence.** The article directly says the home owned by Mr. and Mrs. H. J. Bigger at **Ninth and Center streets** had been purchased by Dr. Frank Mount and would be thoroughly remodeled into a modern home. This is a residential Ninth/Center event, not target frontage.
2. **22 Aug. p2 — same Frank Mount residence follow-up.** The scan says the residence was being remodeled, formerly owned by Mr. and Mrs. H. J. Bigger, and describes additions including a bathroom, sleeping porch and sun porch; it overlooks Main below the bluff. This continues the Ninth/Center residential project, not a 501/503/505 event.
3. **29 Aug. p6 — Oswego post office.** `Our postoffice has been remodeled` appears explicitly inside the **Oswego** community column, which says new lock boxes were added. It is not the Oregon City Fifth/Main Post Office.

Other generic building/remodel language is likewise unrelated to the target frontage.

## Banner-Courier retrieval gap

Direct probing reconfirmed that **7, 14, 21 and 28 August 1919 Banner-Courier issues are not exposed at the tested Historic Oregon Newspapers PDF route**. Institutional holdings confirm the paper exists in this period on microfilm. The gap remains under existing `MF-030`; no new manual ID is created.

## Cross-record propagation audit

Updated: source/evidence registers and YAML; Theroux business/person chronology; Farr Brothers continuation; 1919–1920 construction checkpoint; Banner-Courier access checkpoint; business timeline; ID crosswalk; year-status; archive index; and research log.

Reviewed but deliberately **not** changed: 501/503/505 building histories, ownership timeline, master historical timeline, Wolf/S. Wolf identity relations, and cleaner evidence `E-136`. August supplies no new source-explicit target occupant, target structural event, ownership event, or Wolf identity/premises bridge. The cleaner pages already have exact-page evidence and are not duplicated.

## Next chronological step

Continue with **September 1919 Enterprise** online scans while preserving all September Banner-Courier dates under `MF-030`. Verify the actual September Friday/Thursday issue calendar from the archive rather than assuming a five-issue month.
'''
write(CAPTURE, capture)

append_once("evidence/source-register.md", MARKER, f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans plus retrieval-gap manifest; **40/40 online-exposed pages VISUALLY VERIFIED** 7 September 2026.  
Coverage: Enterprise 1/8/15/22/29 Aug., 40 pages; Banner-Courier 7/14/21/28 Aug. **manual retrieval gaps** under `MF-030`.  
Repository originals: `newspapers/oregon-city-enterprise/1919-august/`; gap manifest `newspapers/banner-courier/1919-august/manifest.json`.  
Related evidence: `{E}`.  
Notes: No source-explicit 501/503/505/505½ occupant or target physical-building event in the 40 Enterprise pages. Cleaner repeats reconfirm existing `S-152`/`E-136` and are not duplicated. Theroux continues at 210 Seventh through 29 Aug.; Farr Brothers recurs in market reports without address/proprietor.''')

append_once("evidence/evidence-register.md", MARKER, f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper online scan batch with explicit manual successor-title gap.  
Sources: `{S}`; existing exact-page cleaner control `S-152`.  
Claims:
- all **40/40 online-exposed August Enterprise pages** were visually inspected after printed title/date/page identity review;
- no source-explicit 501/503/505/505½ occupant or target construction/property event was established in those pages;
- August Banner-Courier issues remain manual retrieval gaps under `MF-030`;
- existing cleaner/dyer `E-136` is visibly reconfirmed but not duplicated;
- Theroux Music House continues at **210 Seventh Street through 29 August**;
- all five August Enterprise market reports credit Farr Brothers without address or individual proprietor;
- Frank Mount remodel references concern the residence at Ninth and Center; the post-office remodel reference is explicitly Oswego.
Confidence: **Very High** for scan-visible wording and online-page coverage; **RETRIEVAL GAP** for inaccessible Banner-Courier issues; none for an unprinted target occupant/event.''')

append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary August scan batch: 40/40 Enterprise pages visually verified. Banner-Courier 7, 14, 21 and 28 August remain MF-030 manual retrieval gaps. No exact 501/503/505 occupant or target structural event was established.\n''')
append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper online scan batch with explicit manual retrieval gap\n    claims:\n      - 40/40 online-exposed August 1919 Enterprise pages visually verified.\n      - No source-explicit 501, 503, 505 or 505-half Main occupant or target physical-building event was established.\n      - Banner-Courier 7, 14, 21 and 28 August remain manual microfilm retrieval gaps under MF-030.\n      - Existing cleaner/dyer E-136 was reconfirmed but not duplicated.\n      - Theroux Music House continued at 210 Seventh Street through 29 August.\n      - Farr Brothers appeared in all five August Enterprise market reports without address or individual proprietor.\n      - Remodel candidates were visually resolved as Ninth-and-Center residential work and an Oswego post-office item.\n    confidence: Very High for visible online pages; retrieval gap for inaccessible Banner-Courier issues\n    related_sources: [{S}]\n    related_evidence: [E-136]\n    related_businesses: [BUS-104, BUS-029]\n    related_people: [P-044]\n    related_buildings: []\n    sources: [{S}]\n    notes: >-\n      August is not a complete local-newspaper month because Banner-Courier is unavailable online. No negative inference is made across inaccessible issues.\n''')

append_once("businesses/farr-brothers-store.md", MARKER, f'''## August 1919 market-report continuation
{MARKER}

Visually reviewed Enterprise market reports on **1, 8, 15, 22 and 29 August 1919** (`{S}` / `{E}`) credit **Brady Mercantile Company and Farr Brothers**. A 29 August county/court expense list also prints `Farr Bros.` None gives an exact address or individual Farr proprietor; no bridge to Farr's Pool Hall at 505 is created.
''')
append_once("businesses/ff-theroux.md", MARKER, f'''## August 1919 — 210 Seventh Street continuation
{MARKER}

The visually reviewed August Enterprise advertising (`{S}` / `{E}`) continues **Theroux Music House at 210 Seventh Street** through **29 August 1919**, without proving the exact move date from the earlier 519 Main location.
''')
append_once("people/profiles/ff-theroux.md", MARKER, f'''## August 1919 address continuation
{MARKER}

`{S}` / `{E}` continues Theroux Music House at **210 Seventh Street through 29 August 1919**. This is a dated business-location control, not property ownership.
''')

append_once("evidence/source-captures/1919-1920-banner-courier-ocr-discovery.md", MARKER, f'''## August 1919 monthly visual-pass reconfirmation
{MARKER}

The August workflow (`{S}` / `{E}`) recovered and visually reviewed all **40 Enterprise pages** but again found no online Banner-Courier pages for **7/14/21/28 Aug. 1919**. The existing institutional microfilm route and `MF-030` remain controlling. This is a retrieval gap, not negative evidence.
''')
append_once("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", MARKER, f'''## August 1919 monthly visual addition
{MARKER}

The complete online-exposed August Enterprise pass (`{S}` / `{E}`) visually reviewed **40/40 pages** and found no source-explicit target-frontage construction, demolition, rebuilding or remodeling event. Potential remodel hits were visually resolved as **Dr. Frank Mount's Ninth-and-Center residence** (15/22 Aug.) and the **Oswego post office** (29 Aug.). Banner-Courier remains unavailable online under `MF-030`, so this is bounded Enterprise coverage only and cannot prove that no target work occurred.
''')

append_once("registers/business-timeline.md", MARKER, f'''| 29 Aug. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | August Enterprise advertising directly continues the published address through 29 Aug. |
| Aug. 1919 | address not printed | Farr Brothers market-report provider | `BUS-104` | `{E}` | All five Enterprise issues credit Farr Brothers with Brady Mercantile; no individual proprietor/address bridge to 505. |
{MARKER}''')
append_once("indexes/id-crosswalk.md", MARKER, f'''## {S} / {E} — August 1919 online Enterprise visual batch
{MARKER}

- `{S}` / `{E}` → `BUS-029` / `P-044`: Theroux Music House at 210 Seventh through 29 Aug.
- `{S}` / `{E}` → `BUS-104`: Farr Brothers market-report continuation without address/proprietor.
- `{S}` / `{E}` → existing `E-136` / `S-152`: cleaner/dyer repeat set reconfirmed, not duplicated.
- `{S}` / `{E}` → `MF-030`: Banner-Courier 7/14/21/28 Aug. remain manual retrieval gaps.
''')

# Update 1919 year-status row while preserving all current parallel content outside that row.
ys=read("registers/year-status.md"); lines=ys.splitlines(); found=False
for i,line in enumerate(lines):
    if line.startswith("| 1919 |"):
        # Preserve current blockers column if possible by replacing the source/capture summary conservatively.
        parts=line.split("|")
        blocker=parts[4].strip() if len(parts) > 4 else ""
        lines[i]=(f"| 1919 | **IN PROGRESS** | `{CAPTURE}`; `evidence/source-captures/1919-july-online-enterprise-courier-visual-review-2026-09-07.md`; "
                  "`evidence/source-captures/1919-june-enterprise-courier-visual-review-2026-09-07.md`; prior Jan-May monthly captures; "
                  "`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | "
                  f"{blocker or 'Banner-Courier 17 Jul. 1919 onward remains MF-030 manual microfilm gap; later 1919 online Enterprise months still pending.'} |")
        found=True; break
if not found: raise RuntimeError("1919 year-status row not found")
write("registers/year-status.md", "\n".join(lines)+"\n")

append_once("ARCHIVE_INDEX.md", MARKER, f'''### 1919 August online-newspaper checkpoint
{MARKER}
- **1919 remains IN PROGRESS.**
- August Enterprise coverage: **40/40 online-exposed pages visually verified** (`{S}` / `{E}`); Jan–Aug cumulative online-exposed local-newspaper visual coverage: **444 pages**.
- Banner-Courier 7/14/21/28 Aug. remains `MF-030` manual microfilm retrieval gap and is excluded from the visual count.
- No exact 501/503/505/505½ occupant or target structural/property event was established in the August Enterprise pages; bounded coverage only.
- Theroux continues at 210 Seventh through 29 Aug.; Farr Brothers appears in all five market reports without address/proprietor; cleaner repeats reconfirm existing `E-136` without duplication.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological online batch: **September 1919 Enterprise**.
''')
append_once("registers/research-log.md", MARKER, f'''## 2026-09-07 — August 1919 Enterprise full visual pass
{MARKER}

- Preserved all five online Enterprise issues (1/8/15/22/29 Aug.), **40 pages**, retrieval commit `65001db`.
- Visually inspected **40/40 actual scans**, including printed date/page identity; no source-association defect found.
- Banner-Courier 7/14/21/28 Aug. remained online retrieval gaps under existing `MF-030`.
- No source-explicit 501/503/505/505½ occupant or target structural/property event; bounded coverage only.
- Reopened target-like remodel hits: Dr. Frank Mount's Ninth/Center residence on 15/22 Aug.; Oswego post-office remodel on 29 Aug.; all non-target.
- Cleaner repeat ads reconfirm existing `S-152` / `E-136`; no duplicate evidence created.
- Theroux continues at 210 Seventh through 29 Aug.; Farr Brothers recurs without address/proprietor.
- Integrated monthly batch as `{S}` / `{E}`; validation required before push.
''')

# Synchronize related YAML relations when entities are present.
for pth,eid in [("database/businesses.yml","BUS-104"),("database/businesses.yml","BUS-029"),("database/people.yml","P-044")]:
    update_yaml_relation(pth,eid,"sources",S)
    update_yaml_relation(pth,eid,"evidence",E)

print(f"Integrated August 1919 online batch as {S} / {E}")
