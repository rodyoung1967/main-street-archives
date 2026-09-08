#!/usr/bin/env python3
from pathlib import Path
import re, sys

MARKER = "<!-- 1919 April Enterprise Courier visual review — 2026-09-07 -->"
YAML_MARKER = "# 1919 April Enterprise Courier visual review — 2026-09-07"
CAPTURE = "evidence/source-captures/1919-april-enterprise-courier-visual-review-2026-09-07.md"
SOURCE_NAME = "April 1919 Oregon City Enterprise + Courier complete monthly visual-review batch"
EVIDENCE_NAME = "April 1919 visual review: Post Office move to Fifth and Main and neighboring business controls"


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
    """Add one scalar to an entity relation list without reformatting the YAML file."""
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
    print("April capture already exists; refusing duplicate integration.")
    sys.exit(0)

S = next_id("evidence/source-register.md", "S")
E = next_id("evidence/evidence-register.md", "E")
T = next_id("database/timeline.yml", "T")

capture = f'''# April 1919 Oregon City newspaper scan-first visual review

{MARKER}

Status: **VISUALLY VERIFIED — 56/56 recovered April pages inspected from original scans.**  
Annual status: **1919 IN PROGRESS**. January–April cumulative local-newspaper visual coverage: **238 pages**.

Archive IDs: source `{S}`; evidence `{E}`; timeline `{T}`.

## Scope

| Title | Issues reviewed | Pages |
| --- | --- | ---: |
| *Oregon City Courier* | 3, 10, 17, 24 Apr. 1919 | **24/24** |
| *Oregon City Enterprise* | 4, 11, 18, 25 Apr. 1919 | **32/32** |
| **April total** | **8 issues** | **56/56** |

Preserved originals:
- `newspapers/oregon-city-courier/1919-april/`
- `newspapers/oregon-city-enterprise/1919-april/`

Retrieval commit: `4993c26` (`Archive April 1919 Oregon City newspaper scans`).

Every recovered page was visually checked for printed issue date and page number before OCR/text discovery. Courier issues visibly contain pages 1–6 and Enterprise issues pages 1–8. No substituted-page, duplicate-page, or printed-date defect was found in the April set.

## Major finding — 15 April Post Office move to Fifth and Main

### 18 April Enterprise p1 — actual move and room configuration

The original scan reports that on **15 April 1919** the Oregon City Post Office moved from its location opposite the courthouse to **Fifth and Main streets**. The article says the new quarters were secured through the efforts of **M. D. Latourette, vice president of First National Bank**.

It directly describes the postal quarters as **two store buildings combined into one large room**:

- one store building was owned by **First National Bank**;
- the other was owned by the **Barlow-David heirs**;
- First National Bank rented the Barlow-David heirs' store room;
- the two rooms together were sublet by First National Bank to the federal government.

The story also describes new postal fixtures, lobby/sorting-room arrangements and a vault/safe, and remarks that the relocation was expected to increase demand and rents in that section. It says that many years earlier the Post Office had occupied one of these store buildings before later moves to the I.O.O.F. building and then the Weinhard Estate building.

Classification: **DOCUMENTED / DIRECT** for the move date, Fifth/Main location, two-room combination, named ownership descriptions, bank rental/subletting arrangement and Latourette's bank role.

### Cross-source parcel geometry — Block 26 Lots 5 and 6

The visually verified **23 Oct. 1913 assessment** (`E-094`) separately identifies the opposite/even-side Block 26 owners as:

- Lot 5 — **Mary E. Barlow / Juliette E. David**;
- Lot 6 — **First National Bank**.

The April 1919 article's adjacent Barlow-David and First National Bank ownership descriptions therefore strongly align with the known **Block 26 Lot 5 + Lot 6 owner sequence** on the east/even side of Main. This materially sharpens the post-1918 Post Office geometry.

Classification: **STRONG CROSS-SOURCE INFERENCE** for correspondence to Block 26 Lots 5–6. The April article does not print lot numbers or a numbered Main Street bay, so no exact `504`, `506`, `508`, `510`, `512` or `514` assignment is made.

### 1918 vs. 1919 ownership-description conflict

A visually verified **12 Sep. 1918 Courier** report said the Post Office Department had leased a building on the east side of Main between Fifth and Sixth **owned by M. D. Latourette**. The 18 Apr. 1919 Enterprise instead says the actual new quarters consisted of two combined store buildings owned by **First National Bank** and the **Barlow-David heirs**, while describing Latourette as the bank's vice president and the person through whose efforts the location was secured.

Both contemporary source statements are preserved. Classification: **UNRESOLVED CONTEMPORARY OWNERSHIP-DESCRIPTION CONFLICT**. Possible differences in ownership date, agency, building-name usage or source precision are not resolved by these newspaper reports alone.

### Target-frontage implication

This new Post Office evidence is on the **opposite/even side of Main**, not a direct 501/503/505 occupancy event. It strengthens the facing-landmark geometry later used by advertisements such as `505½ Main — Opposite Postoffice`, but it does not by itself select a particular odd-side storefront or prove any 501/503/505 occupant.

## Ohio Dentists — 507½ Main over Harding's Drug Store

The **11 April Enterprise p4** scan directly repeats:

- **Ohio Dentists**;
- **Dr. J. G. Nash, Manager**;
- **507½ Main Street**;
- **over Harding's Drug Store**;
- **Phone 62**.

This extends the direct 507½-over-Harding office-location run through **11 April 1919**. The ad still does not print `Harding Drug Store, 507 Main`; Harding's exact lower-floor 507 assignment remains a **STRONG SPATIAL/ADDRESS INFERENCE**, not a source-explicit exact-number fact.

## Farr Brothers market-report continuation

The **4 Apr. p3, 11 Apr. p6, 18 Apr. p2 and 25 Apr. p2 Enterprise** market reports were visually reopened and each credits **Brady Mercantile Company and Farr Brothers**. These are dated local-business appearances only. They print no address or individual Farr proprietor and do not bridge this concern to Edwin/Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr or Harr's Recreation Center.

## Theroux Music House — 210 Seventh Street continuation

April Enterprise advertisements continue **Theroux Music House at 210 Seventh Street**; the **18 Apr. p3** and **25 Apr. p7** scans were specifically reopened at high resolution, with 25 Apr. directly printing the 210 Seventh address. This extends the direct Seventh Street chronology through **25 April 1919** and does not establish the exact move date from the earlier 519 Main premises.

## Rohberger / Rohrberg follow-forward

No April page produced a defensible local-business follow-forward for the February `Mr. Rohrberg` / March `F. D. Rohberger` billiard-parlor purchaser. An OCR hit for `Mrs. Jas. Rohrberg, 620 Knapp St., Pittsburgh, Pa.` is an unrelated testimonial and was rejected. No billiard/pool-hall premises number was recovered in April.

This is a **bounded April no-hit only**. It is not evidence that the billiard business closed, moved, changed name, or ceased operation.

## Target frontage — 501 / 503 / 505 Main

Across all 56 visually reviewed April pages and the post-visual text-discovery pass:

- no defensible source-explicit **501 Main** occupant was found;
- no defensible source-explicit **503 Main** occupant was found;
- no defensible source-explicit **505 Main** occupant was found;
- no April Wolf & Miller exact-address continuation was found;
- no target-specific construction, demolition, rebuilding, remodeling, lease, sale, move or fire event was found.

Numeric collisions, legal descriptions, monetary figures, and unrelated addresses were rejected as non-target context.

**This is bounded April coverage only. It is not evidence of vacancy, non-use, closure, demolition or absence of an occupant.**

## Cross-Record Propagation Audit

Propagated: source/evidence registers and YAML; post-office location/ownership-conflict captures; 1913 Block 26 geometry; Ohio Dentists/Nash and Harding spatial chronology; Farr Brothers; Theroux; master/business/address/ownership timelines; database timeline; open questions/research leads; crosswalk; year status; archive index; historical-society research supplement; and research log.

No 501/503/505 building event is created because April supplies no direct target-premises event.

## Next chronological step

Continue with **May 1919 Enterprise + Courier** under the same scan-first standard. High-value follow-forward targets include the **exact Post Office numbered bay**, the **1918 Latourette vs. 1919 First National Bank/Barlow-David ownership-description conflict**, **Rohberger/Rohrberg billiard premises**, and any exact 501/503/505 occupant or construction/property transition.
'''
write(CAPTURE, capture)

append_once("evidence/source-register.md", MARKER, f'''## {S} — {SOURCE_NAME}
{MARKER}
Type: Primary newspaper scans; **VISUALLY VERIFIED** 7 September 2026.  
Coverage: Courier 3/10/17/24 Apr., 24 pages; Enterprise 4/11/18/25 Apr., 32 pages; **56/56 total**.  
Repository originals: `newspapers/oregon-city-courier/1919-april/` and `newspapers/oregon-city-enterprise/1919-april/`.  
Related evidence: `{E}`.  
Notes: 18 Apr Enterprise p1 directly reports the Post Office's 15 Apr move to Fifth/Main into two combined store rooms owned by First National Bank and the Barlow-David heirs, creating an ownership-description conflict with the Sep 1918 Latourette report and a strong cross-source match to Block 26 Lots 5–6. Ohio Dentists continues at 507½-over-Harding on 11 Apr.; Farr Brothers market credits recur all four Enterprise issues; Theroux continues at 210 Seventh. No source-explicit 501/503/505 occupant or target construction event; bounded coverage only.''')

append_once("evidence/evidence-register.md", MARKER, f'''## {E} — {EVIDENCE_NAME}
{MARKER}
Type: Primary newspaper scan batch; **VISUALLY VERIFIED**.  
Sources: `{S}`.  
Claims:
- all **56/56** recovered April pages were visually inspected after printed date/page identity review;
- 18 Apr Enterprise p1 reports the Post Office moved **15 Apr. 1919 to Fifth and Main** into **two combined store buildings**, one owned by First National Bank and one by the Barlow-David heirs; the bank rented the heirs' room and sublet the combined quarters to the federal government;
- the named 1919 owners strongly align with the 1913 Block 26 Lot 5 Barlow/David and Lot 6 First National Bank owner sequence, but the exact numbered postal bay remains unresolved;
- the 1919 ownership wording conflicts with the 12 Sep. 1918 Courier description of the leased building as owned by M. D. Latourette; both source statements remain open;
- 11 Apr Enterprise p4 repeats **Ohio Dentists / Dr. J. G. Nash at 507½ Main over Harding's Drug Store**;
- all four April Enterprise market reports credit **Brady Mercantile Company and Farr Brothers** without address or proprietor;
- Theroux Music House continues at **210 Seventh Street** through 25 Apr.;
- no source-explicit 501/503/505 occupant or target physical-building event was found; no-hit is bounded coverage only.
Confidence: **Very High** for scan-visible April wording and page coverage; **Strong cross-source inference** for Block 26 Lots 5–6 correspondence; **Unresolved conflict** for 1918 vs. 1919 ownership descriptions; none for an unprinted exact Post Office bay.''')

append_once("database/sources.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {S}\n    name: "{SOURCE_NAME}"\n    url: https://oregonnews.uoregon.edu/\n    notes: >-\n      Primary scan batch, visually verified 56/56 April pages: 24 Courier and 32 Enterprise.\n      The 18 April Enterprise directly reports the 15 April Post Office move to Fifth/Main into\n      two combined store rooms owned by First National Bank and the Barlow-David heirs. It also\n      preserves an ownership-description conflict with the September 1918 Latourette report.\n      Ohio Dentists, Farr Brothers and Theroux controls continue; no exact 501/503/505 occupant.\n''')

append_once("database/evidence.yml", YAML_MARKER, YAML_MARKER + f'''\n  - id: {E}\n    name: "{EVIDENCE_NAME}"\n    type: Primary newspaper scan batch\n    claims:\n      - 56/56 recovered April 1919 pages visually verified.\n      - The Oregon City Post Office moved 15 April 1919 to Fifth and Main into two combined store rooms owned by First National Bank and the Barlow-David heirs.\n      - The 1919 named-owner pair strongly aligns with the 1913 Block 26 Lot 5 Barlow/David and Lot 6 First National Bank sequence; exact numbered postal bay remains unresolved.\n      - The April 1919 ownership description conflicts with the September 1918 newspaper description of the leased building as owned by M. D. Latourette.\n      - Ohio Dentists continued at 507½ Main over Harding's Drug Store on 11 April; Farr Brothers market-report credits and Theroux at 210 Seventh continued.\n    confidence: Very High for scan-visible wording and page coverage; strong cross-source inference for Block 26 Lots 5-6 correspondence; unresolved for ownership-description conflict and exact postal bay\n    related_sources: [{S}]\n    related_evidence: [E-094]\n    related_businesses: [BUS-106, BUS-007, BUS-104, BUS-029]\n    related_people: [P-397, P-044]\n    related_buildings: [B-003]\n    sources: [{S}]\n    notes: >-\n      April monthly scan-first review. The Post Office is opposite-side spatial context, not a\n      501/503/505 occupancy event. No exact target occupant or target construction event was found.\n''')

append_once("evidence/source-captures/1918-1922-post-office-east-main-fifth-sixth-anchor.md", MARKER, f'''## 15 April 1919 actual move — two combined store rooms at Fifth and Main
{MARKER}

The complete April monthly scan-first review (`{S}` / `{E}`) adds a much stronger actual-occupancy control. **18 Apr. 1919 Enterprise p1**, visually verified, reports that the Oregon City Post Office moved on **15 April** from opposite the courthouse to **Fifth and Main streets**. It says the new quarters consisted of **two store buildings combined into one large room**: one owned by **First National Bank**, the other by the **Barlow-David heirs**. First National Bank rented the heirs' store room and sublet the combined rooms to the federal government. **M. D. Latourette** is identified as **vice president of First National Bank** and as instrumental in securing the location.

### Block 26 geometry refinement

The 1913 assessment (`E-094`) places **Mary E. Barlow / Juliette E. David on Block 26 Lot 5** and **First National Bank on Block 26 Lot 6**. Because Block 26 is the even/opposite side of Main, the 1919 adjacent-owner description is a **STRONG CROSS-SOURCE INFERENCE** that the new postal quarters occupied combined rooms associated with **Lots 5–6**. The 1919 article itself prints no lot numbers or exact street number, so the exact bay within the later 504–514 range remains unresolved.

### Ownership-description conflict now explicit

This April report conflicts with the **12 Sep. 1918 Courier** wording that described the leased east-side Fifth–Sixth Main building as **owned by M. D. Latourette**. The later article instead assigns the two component store rooms to First National Bank and the Barlow-David heirs while giving Latourette a bank-officer/transaction role. Preserve both direct contemporary statements as an **UNRESOLVED CONFLICT**; do not continue describing Latourette ownership as an uncontested fact.
''')

append_once("evidence/source-captures/1918-post-office-east-side-main-fifth-sixth-latourette.md", MARKER, f'''## April 1919 follow-up — actual move and conflicting ownership description
{MARKER}

`{S}` / `{E}` visually verifies the **18 Apr. 1919 Enterprise p1** report that the Post Office actually moved on **15 April 1919 to Fifth and Main**, into two store buildings combined into one large room. The article says one room was owned by **First National Bank** and the other by the **Barlow-David heirs**; First National Bank rented the latter and sublet the combined quarters to the federal government. It identifies **M. D. Latourette as vice president of First National Bank** and credits his efforts in securing the location.

This materially qualifies this capture's earlier statement that the September 1918 source proved Latourette ownership of the leased building. The **1918 source does directly print that ownership description**, but the **1919 source directly conflicts with it**. Current classification: **UNRESOLVED CONTEMPORARY OWNERSHIP-DESCRIPTION CONFLICT**. Possible agency, building-name, ownership-date or reporting differences remain hypotheses until lease/deed/property records resolve them.
''')

append_once("evidence/source-captures/1913-block26-lots5-8-owner-geometry.md", MARKER, f'''## April 1919 Post Office cross-source owner recurrence
{MARKER}

The 18 Apr. 1919 Enterprise Post Office story (`{S}` / `{E}`) says the new Fifth/Main postal quarters combined **two store buildings**, one owned by **First National Bank** and the other by the **Barlow-David heirs**. This closely reproduces the 1913 Block 26 owner sequence documented above: **Lot 5 Mary E. Barlow / Juliette E. David; Lot 6 First National Bank**.

Because Block 26 is independently established on the **even/opposite side of Main**, this is a **STRONG CROSS-SOURCE INFERENCE** that the April 1919 postal rooms correspond to the Lot 5–6 portion of the Block 26 frontage. Do not convert the inference into an exact 504/506/etc. postal address; the 1919 article does not print a lot number or numbered street bay.
''')

append_once("evidence/1912-main-street-postoffice-cluster.md", MARKER, f'''## April 1919 refinement of the later Post Office landmark
{MARKER}

`{S}` / `{E}` now directly dates the later Post Office's **actual move to Fifth and Main to 15 April 1919** and describes its quarters as two adjoining store buildings combined into one room, with First National Bank and the Barlow-David heirs named as owners. The 1913 Block 26 assessment strongly aligns those owner names with Lots 6 and 5 respectively on the even side. This improves the later landmark used for 1921–22 `opposite Post Office` evidence but does not alter the separate circa-1912 Post Office hypothesis on this page.
''')

append_once("businesses/ohio-painless-dentists.md", MARKER, f'''## April 1919 continuation
{MARKER}

The visually verified **11 Apr. Enterprise p4** advertisement (`{E}` / `{S}`) repeats **Ohio Dentists**, **Dr. J. G. Nash, Manager**, **507½ Main Street**, **over Harding's Drug Store**, Phone 62. This extends the direct office-location run through **11 April 1919**. Harding's exact lower-floor number remains unprinted and inferential.
''')
append_once("people/profiles/j-g-nash.md", MARKER, f'''## April 1919 continuation
{MARKER}

`{E}` / `{S}` visually verifies Dr. J. G. Nash as manager of Ohio Dentists at **507½ Main over Harding's Drug Store** on **11 April 1919**, extending his direct advertised role into April.
''')
append_once("businesses/harding-drug-store.md", MARKER, f'''## April 1919 507½-over-Harding continuation
{MARKER}

The visually verified **11 Apr. 1919 Enterprise p4** Ohio Dentists advertisement (`{E}` / `{S}`) again describes the **507½ Main** dental office as **over Harding's Drug Store**. This preserves the spatial relationship into April but still does not print Harding's own ground-floor number; `507 Main` remains a strong inference rather than a direct exact-address fact.
''')
append_once("businesses/farr-brothers-store.md", MARKER, f'''## April 1919 continuation
{MARKER}

All four April Enterprise market reports — **4 Apr. p3, 11 Apr. p6, 18 Apr. p2 and 25 Apr. p2** — were visually reopened and credit **Brady Mercantile Company and Farr Brothers** (`{E}` / `{S}`). These are dated business appearances only: no address or individual proprietor is printed. Do not merge this concern with Edwin/Alice Farr or Farr's Pool Hall at 505 Main.
''')
append_once("businesses/ff-theroux.md", MARKER, f'''## April 1919 — 210 Seventh Street continuation
{MARKER}

`{E}` / `{S}` visually verifies April advertising for **Theroux Music House at 210 Seventh Street**, including 18 Apr. p3 and 25 Apr. p7. This extends the direct Seventh Street business-address chronology through **25 April 1919** without establishing the exact move date from 519 Main.
''')
append_once("people/profiles/ff-theroux.md", MARKER, f'''## April 1919 address continuation
{MARKER}

`{E}` / `{S}` continues Theroux Music House at **210 Seventh Street** through **25 April 1919**. This updates the business-address chronology without proving the exact departure date from 519 Main.
''')

append_once("timeline.md", MARKER, f'''## 15 April 1919 — Post Office moves to Fifth and Main; April newspaper batch complete
{MARKER}

The **18 Apr. Enterprise p1** scan (`{S}` / `{E}`) directly reports that the Oregon City Post Office moved on **15 April 1919 to Fifth and Main**, into **two store buildings combined into one large room**. One is described as owned by First National Bank and the other by the Barlow-David heirs; the bank rented the latter and sublet the combined rooms to the federal government. The owner names strongly align with the 1913 Block 26 Lot 6/5 sequence on the even side of Main. The exact numbered postal bay remains unresolved, and the 1919 ownership wording conflicts with the 1918 report calling the leased building M. D. Latourette-owned.

The full April batch is **56/56 visually verified pages**, bringing January–April 1919 local-newspaper coverage to **238 pages**. Ohio Dentists/Nash continues at 507½-over-Harding on 11 Apr.; Farr Brothers appears in all four April market reports without address/proprietor; Theroux remains at 210 Seventh through 25 Apr. No source-explicit 501/503/505 occupant or target construction/property event was recovered; bounded coverage only.
''')

append_once("registers/business-timeline.md", MARKER, f'''| 11 Apr. 1919 | 507½ Main | Ohio Dentists / Dr. J. G. Nash | `BUS-106` | `{E}` | Direct ad says 507½ Main, over Harding's Drug Store; Harding's ground-floor number not printed. |
| Apr. 1919 | address not printed | Farr Brothers market-report provider | `BUS-104` | `{E}` | 4/11/18/25 Apr. Enterprise credits with Brady Mercantile; no proprietor/address bridge to 505. |
| 25 Apr. 1919 | 210 Seventh Street | Theroux Music House | `BUS-029` | `{E}` | Direct April advertising continues the Seventh Street address. |
{MARKER}''')
append_once("registers/address-register.md", MARKER, f'''| Fifth & Main — 15 Apr. 1919 Post Office combined rooms | Opposite/even side context; exact number unresolved | `evidence/source-captures/1918-1922-post-office-east-main-fifth-sixth-anchor.md` | U.S. Post Office | `{E}`; E-094 | 18 Apr. Enterprise says two store buildings owned by First National Bank and Barlow-David heirs were combined; strong cross-source alignment to Block 26 Lots 6 + 5, but no exact numbered postal bay. |
| 507½ Main — 11 Apr. 1919 | Upstairs office; exact physical-building continuity unresolved | `businesses/ohio-painless-dentists.md` | BUS-106 | `{E}` | Ohio Dentists / Dr. J. G. Nash; directly described as over Harding's Drug Store. |
{MARKER}''')
append_once("registers/ownership-timeline.md", MARKER, f'''| 12 Sep. 1918 vs. 18 Apr. 1919 Post Office reports | East/even Fifth–Sixth Main block | 1918 report: M. D. Latourette; 1919 report: First National Bank + Barlow-David heirs | **UNRESOLVED CONTEMPORARY OWNERSHIP-DESCRIPTION CONFLICT** | `{E}` plus existing 1918 Post Office evidence and E-094 | Very High for each source's printed wording; unresolved reconciliation | 1919 article says actual postal quarters combined two stores, bank renting heirs' room and subletting both; Latourette identified as bank VP. Do not collapse the sources into one ownership claim without lease/deed/property evidence. |
{MARKER}''')

append_once("evidence/open-questions.md", MARKER, f'''## April 1919 Post Office geometry / ownership questions
{MARKER}

1. What exact numbered Main Street bay or bays did the Post Office occupy after **15 April 1919** within the even-side Fifth–Sixth block?
2. Do lease, deed, assessment or bank/property records reconcile the **12 Sep. 1918 M. D. Latourette ownership description** with the **18 Apr. 1919 First National Bank + Barlow-David heirs ownership description**?
3. Can the strong Block 26 **Lots 5–6** owner-geometry inference be converted into a direct lot/bay identification from a 1919 lease, directory, postal record or contemporary map?
4. Once the postal bay is fixed, how tightly does it constrain 1921–22 `opposite Post Office` wording at 505½ Main and Miller's Shoe Store?
''')
append_once("evidence/research-leads.md", MARKER, f'''## 1919 Post Office exact-bay and ownership-conflict route
{MARKER}

**Priority: HIGH — ONLINE FIRST, then existing manual/property routes if needed.** The April monthly visual batch (`{S}` / `{E}`) directly dates the move to **15 Apr. 1919** and names **First National Bank + Barlow-David heirs** as owners of the two combined store rooms. Search 1919–1922 directories, postal notices, First National Bank/Latourette property references, deeds/assessments and federal Post Office lease/site records for an exact numbered bay and ownership reconciliation. Use the 1913 Block 26 Lot 5 Barlow/David + Lot 6 First National Bank sequence as a cross-source test, not as proof of a 1919 lot assignment. Preserve the 1918 Latourette ownership statement as a conflict until resolved.
''')

append_once("indexes/id-crosswalk.md", MARKER, f'''## {S} / {E} — April 1919 complete monthly local-newspaper visual batch
{MARKER}

- `{S}` / `{E}` → 15 Apr. Post Office move to Fifth/Main; two combined rooms owned as First National Bank + Barlow-David heirs; strong cross-source relation to `E-094` Block 26 Lots 6 + 5; exact numbered bay unresolved.
- `{S}` / `{E}` → unresolved 1918 Latourette vs. 1919 bank/Barlow-David Post Office ownership-description conflict.
- `{S}` / `{E}` → `BUS-106` / `P-397` and Harding spatial context: 507½ Main over Harding's Drug Store on 11 Apr.
- `{S}` / `{E}` → `BUS-104` Farr Brothers market-report continuation and `BUS-029` / `P-044` Theroux at 210 Seventh.
- `{T}` → 15 Apr. 1919 Post Office move event.
''')

append_once("records/historical-society/503-505-main-historical-society-research-supplement-2026-08-24.md", MARKER, f'''## April 1919 Post Office landmark refinement
{MARKER}

The 1919 monthly scan-first pass now directly dates the Post Office's actual move to **15 April 1919**. The 18 Apr. Enterprise says the Fifth/Main quarters combined two store buildings, one owned by First National Bank and one by the Barlow-David heirs. This strongly aligns with the independently verified 1913 Block 26 Lot 6 / Lot 5 owner sequence on the even side of Main and improves the spatial landmark opposite the 501/503/505 frontage. The exact numbered postal bay remains unresolved. The article also creates a contemporary conflict with the Sep. 1918 report that called the leased building M. D. Latourette-owned; the supplement should not present Latourette ownership as settled.
''')

append_once("registers/research-log.md", MARKER, f'''| 2026-09-07 | Completed April 1919 Enterprise + Courier scan-first visual audit | **56/56 pages**: Courier 24/24 (3/10/17/24 Apr.) + Enterprise 32/32 (4/11/18/25 Apr.), bringing Jan–Apr cumulative local-newspaper visual coverage to **238 pages**. Major direct finding: Post Office moved 15 Apr. to Fifth/Main into two combined store rooms owned by First National Bank and Barlow-David heirs; strong match to 1913 Block 26 Lots 6/5 and unresolved conflict with 1918 Latourette ownership wording. Ohio Dentists/Nash, Farr Brothers and Theroux controls extended. No exact 501/503/505 occupant or target construction event; bounded coverage only. Created `{S}` / `{E}` / `{T}`. 1919 remains IN PROGRESS; next chronological batch May. |
{MARKER}''')

append_once("ARCHIVE_INDEX.md", MARKER, f'''## 1919 April complete visual batch
{MARKER}

- **1919 remains IN PROGRESS.**
- April local-newspaper coverage: **56/56 visually verified pages** (`{S}` / `{E}`); Jan–Apr cumulative **238 pages**.
- 15 Apr. Post Office move to Fifth/Main: two combined store rooms owned by First National Bank and Barlow-David heirs; strong cross-source Block 26 Lots 6/5 alignment, exact numbered bay unresolved.
- 1918 Latourette vs. 1919 bank/Barlow-David ownership descriptions remain an explicit contemporary conflict.
- Ohio Dentists at 507½-over-Harding on 11 Apr.; Farr Brothers market-report continuation; Theroux at 210 Seventh through 25 Apr.
- No source-explicit 501/503/505 occupant or target construction/property event; bounded coverage only.
- Full review: [{CAPTURE}]({CAPTURE}).
- Next chronological batch: **May 1919 Enterprise + Courier**.
''')

# Database timeline event.
timeline_yml = read("database/timeline.yml")
if not re.search(rf"(?m)^  - id: {re.escape(T)}\s*$", timeline_yml):
    timeline_yml = timeline_yml.rstrip() + f'''\n\n  - id: {T}\n    date: 15 April 1919\n    summary: Oregon City Post Office moved to Fifth and Main into two combined store rooms described three days later as owned by First National Bank and the Barlow-David heirs; the ownership wording conflicts with the September 1918 report describing the leased building as M. D. Latourette-owned.\n    confidence: Very High for the visible move and ownership wording; strong cross-source inference for Block 26 Lots 5-6; unresolved for ownership reconciliation and exact numbered postal bay\n    related_evidence:\n      - {E}\n      - E-094\n    related_sources:\n      - {S}\n''' + "\n"
    write("database/timeline.yml", timeline_yml)

# Keep existing entity YAML relations synchronized.
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
            "`evidence/source-captures/1919-march-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-february-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-january-enterprise-courier-visual-review-2026-09-07.md`; "
            "`evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md` | "
            f"January–April scan-first local-newspaper coverage **238 visually verified pages**: January 70 + February 56 + March 56 + April 56 (`{S}`/`{E}` for April). "
            "April directly dates the Post Office move to Fifth/Main on 15 Apr. and describes two combined store rooms owned by First National Bank and Barlow-David heirs; this strongly aligns with 1913 Block 26 Lots 6/5 but leaves the exact numbered bay unresolved and creates an ownership-description conflict with the 1918 Latourette report. "
            "Ohio Dentists at 507½-over-Harding, Farr Brothers market credits and Theroux at 210 Seventh continue; no exact 501/503/505 occupant or target construction event. "
            "May–December annual visual work and other online source classes remain; Banner-Courier from July 1919 has a documented manual microfilm gap. |"
        )
        found = True
        break
if not found:
    raise RuntimeError("1919 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

print(f"Integrated April 1919 as {S} / {E} / {T}")
