#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def p(rel):
    return ROOT / rel


def read(rel):
    return p(rel).read_text(encoding="utf-8")


def write(rel, text):
    p(rel).write_text(text, encoding="utf-8")


def replace_once(rel, old, new, required=True):
    text = read(rel)
    if old not in text:
        if required:
            raise RuntimeError(f"Expected text not found in {rel}: {old[:120]!r}")
        return False
    if text.count(old) != 1 and required:
        raise RuntimeError(f"Expected one occurrence in {rel}, found {text.count(old)}")
    write(rel, text.replace(old, new, 1))
    return True


def replace_section(rel, heading, next_heading, new_section):
    text = read(rel)
    pat = re.compile(rf"^{re.escape(heading)}\n.*?(?=^{re.escape(next_heading)}\n)", re.M | re.S)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"Section {heading!r} in {rel}: expected 1 match, got {len(matches)}")
    write(rel, text[:matches[0].start()] + new_section.rstrip() + "\n\n" + text[matches[0].end():])


def add_banner(rel, marker, banner):
    text = read(rel)
    if marker in text:
        return
    lines = text.splitlines(True)
    if not lines or not lines[0].startswith("#"):
        raise RuntimeError(f"No heading in {rel}")
    lines.insert(1, "\n" + banner.rstrip() + "\n\n")
    write(rel, "".join(lines))


# 1. Rewrite E-094 as the superseding cadastral-orientation correction.
write("evidence/E-094-original-plat-block26-lot5-boundary.md", """# E-094 — Original Oregon City Plat / Block 4–Block 26 Orientation Correction

## Evidence type
Primary official plat + visually verified primary newspaper assessment notice + primary Sanborn map, reconciled with current county-derived parcel/legal-description records and the official Clackamas County plat index.

## Sources
- `S-107` — *Morning Enterprise*, 23 October 1913, page 8.
- `S-108` — original Oregon City plat, county plat 2, cataloged 1850.
- `S-021` / `SM-008` — May 1925 Sanborn Sheet 6.
- `S-078` / `E-064` — 1906 William Tell / Gambrinus Lot 8, Block 26 anchor.
- Current parcel/legal-description cross-checks preserved in `evidence/source-captures/block4-block26-side-of-main-correction-task6-2026-08-26.md`.

## Visually verified primary facts
1. The 23 October 1913 assessment notice treats **Block 4** and **Block 26** as separate physical blocks in the same boundary description.
2. The same notice lists **G. A. Harding** at **Block 4 Lots 3 and 4**.
3. It separately lists Block 26 owners: Lot 5 Mary E. Barlow / Juliette E. David, Lot 6 First National Bank, Lot 7 Frank Jaggar, and Lot 8 Gambrinus Brewing Company.
4. The official original Oregon City plat confirms the original block/lot framework and the Applegate-area lot dimensions.
5. The 1925 Sanborn directly labels the odd-numbered Main frontage as 501, 503, 505, 507, etc.

## Task 6 cadastral correction
Current county-derived property records report **503, 505, 507 and 517 Main in Block 4**, while **504 Main on the opposite/even side is part of Lot 5, Block 26**. The Clackamas County subdivision index identifies McLoughlin's Oregon City plat as **Plat No. 0002** and does not show a Block 26-to-Block 4 replat for this frontage.

The earlier project inference that **501+503+505 ≈ original Block 26 Lot 5** and **507 ≈ Block 26 Lot 6** is therefore **withdrawn and superseded**. It resulted from placing the William Tell / Block 26 anchor on the wrong side of Main Street.

Corrected working orientation:
- odd-numbered 501/503/505/507 frontage between Fifth and Sixth = **original Block 4**;
- opposite/even-numbered frontage, including current 504 Main = **original Block 26**.

There is no longer a research need to find a hypothetical **Block 26 → Block 4 conversion instrument for 503/505**; that premise was false.

## Strong current-title implications
- Current 503 is reported as **part of Block 4 Lot 4**.
- Current 505 is reported as **parts of Block 4 Lots 3 and 4**.
- Current 507 is reported as **parts of Block 4 Lots 2, 3 and 4**.
- The 1913 assessment places **G. A. Harding at Block 4 Lots 3 and 4**, creating a direct correct-side cadastral lead for the later Harding → Wolf/Gates property sequence.
- The OHS MSS 1503 Box 19 title-abstract index entry for **Block 4, Lots 3 & 4 / Main & Fifth** is therefore a potentially direct target-property title lead, not a supposed bridge from Block 26 into a later Block 4 system. Its actual contents remain unretrieved.

## Remaining limits
- Current commercial property pages are strong county-derived legal-description leads, but official recorded deed/assessor images for the target parcels remain desirable.
- Historic **501 Main's exact Block 4 lot** is still unresolved.
- Modern 503/505 parcel boundaries must not be backdated automatically to 1922.
- The 1925 proportional observation that 501+503+505 span roughly one 66-foot original-lot width may remain useful, but it must be re-tested against **Block 4** geometry; it no longer proves any Block 26 lot assignment.
- The exact July 1922 Gates/Wolf dividing line and fire-origin storefront remain unresolved.

## Confidence
- **Very High** for the visually verified 1913 distinction between Blocks 4 and 26 and the printed owner listings.
- **High / strong convergence** for the corrected side-of-Main orientation from multiple current county-derived legal descriptions plus the original records.
- **Withdrawn** for the former 501/503/505≈Block 26 Lot 5 inference.
- **Unresolved** for exact historic lot boundaries of 501 and the 1922 Gates/Wolf internal division.
""")

# 2. Replace the detailed geometry note rather than leave a stale target-side reconstruction.
write("evidence/source-captures/1913-block26-lots5-8-owner-geometry.md", """# 1913 Blocks 4 and 26 — corrected side-of-Main geometry

Status: **PRIMARY SOURCES VISUALLY VERIFIED; PRIOR TARGET-BLOCK ORIENTATION SUPERSEDED BY TASK 6**

Related evidence: `E-064`, `E-094`, `E-095`, `E-096`
Related sources: `S-021`, `S-078`, `S-107`, `S-108`, `S-109`, `S-110`, `S-111`

## 23 October 1913 assessment notice — VISUALLY VERIFIED
The full-page *Morning Enterprise*, 23 October 1913, page 8 was visually inspected. The notice distinguishes **Block 4** from **Block 26** in the same assessment boundary and therefore proves they were separate physical blocks, not successive numbering systems.

Canonical page PDF:
https://oregonnews.uoregon.edu/lccn/sn00063701/1913-10-23/ed-1/seq-8.pdf

Repository PDF:
`newspapers/oregon-city-enterprise/1913-10-23-page-8-block-26-assessment.pdf`

Relevant owner listings include:
- **Block 4, Lot 3 — G. A. Harding**
- **Block 4, Lot 4 — G. A. Harding**
- **Block 26, Lot 5 — Mary E. Barlow / Juliette E. David**
- **Block 26, Lot 6 — First National Bank**
- **Block 26, Lot 7 — Frank Jaggar**
- **Block 26, Lot 8 — Gambrinus Brewing Company**

## Block 26 remains valid — on the opposite/even side
Separate 1906 primary evidence (`E-064`) ties the William Tell Hotel / Gambrinus property at Sixth & Main to **Lot 8, Block 26**. That evidence remains valid. The Task 6 correction changes its orientation relative to the target frontage: Block 26 is the **opposite/even-numbered side of Main**, not the 501/503/505 side.

Current 504 Main provides an independent modern cross-check because its county-derived legal description remains **part Lot 5, Block 26**.

## Correct target block: original Block 4
Multiple current county-derived property records report:
- 503 Main — part Lot 4, Block 4;
- 505 Main — parts Lots 3 & 4, Block 4;
- 507 Main — parts Lots 2, 3 & 4, Block 4;
- 517 Main — parts Lots 1 & 8, Block 4.

Read with the 1913 Harding ownership of Block 4 Lots 3–4, these records place the odd-numbered Fifth-to-Sixth Main frontage in **original Block 4**.

## Withdrawn inference
The former reconstruction that used Block 26 Lot 8 at Sixth/Main and then worked through Block 26 Lots 7, 6 and 5 to assign **501+503+505 to Block 26 Lot 5** is withdrawn. It crossed Main Street without recognizing that Block 4 and Block 26 occupied opposite sides.

The former 1925 proportional measurement itself—roughly 66–67 feet from the Fifth edge through the 505/507 wall—may still be a useful geometric observation. It must be re-tested against original **Block 4** lot geometry before any lot assignment is made.

## Corrected 1922 implication
The title search should no longer prioritize Barlow/David Block 26 Lot 5 for the odd-numbered fire frontage. Instead:
1. prioritize **G. A. Harding / Block 4 Lots 3–4** in 1913;
2. retrieve the OHS MSS 1503 Box 19 Block 4 Lots 3–4 abstract;
3. retrieve the July 1922 Harding → Wolf/Gates deed(s);
4. map those deed dimensions to 501/503/505 without backdating current parcel boundaries.

The July 1922 fire-origin address remains unresolved.
""")

# 3. Replace current-parcel reconciliation note with corrected interpretation.
write("evidence/source-captures/current-parcel-legal-descriptions-vs-historic-block26.md", """# Current parcel legal descriptions vs. original Blocks 4 and 26 — 503/505/507 Main

Status: **CADASTRAL ORIENTATION CORRECTED; NO BLOCK 26 → BLOCK 4 CONVERSION FOR THE TARGET FRONTAGE**

Purpose: preserve current parcel/legal-description leads and the Task 6 correction that the odd-numbered target frontage is original Block 4, while Block 26 lies across Main.

## Current target-side parcel leads
### 503 Main
- APN: **00572650**
- tax lot: **2-2E-31AB-08200**
- reported legal: **`2 OREGON CITY PT LT 4 BLK 4`**
- canonical lead: https://www.loopnet.com/property/503-main-st-oregon-city-or-97045/41005-00572650/

### 505 Main
- APN: **00572669**
- tax lot: **2-2E-31AB-08300**
- reported legal: **`2 OREGON CITY PT LTS 3&4 BLK 4`**
- canonical lead: https://www.loopnet.com/property/505-main-st-oregon-city-or-97045/41005-00572669/

### 507 Main
- APN: **00572678**
- reported legal: **`SUBDIVISION OREGON CITY 2 BLOCK 4 PT LTS 2, 3 & 4`**
- canonical lead: https://www.loopnet.com/property/507-main-st-oregon-city-or-97045/41005-00572678/

### Same odd-numbered side farther north
517 Main is reported as **`2 OREGON CITY PT LT 1&8 BLK 4`**, providing another same-side Block 4 check.

## Opposite-side control: 504 Main
Current **504 Main**, directly across Main from the target odd-numbered frontage, is reported as:
- APN **00572785**
- **`2 OREGON CITY PT LT 5 BLK 26 ...`**
- canonical lead: https://www.loopnet.com/property/504-main-st-oregon-city-or-97045/41005-00572785/

This is the decisive modern orientation check: Block 26 persists on the opposite/even side while 503/505/507 persist in Block 4.

## Primary 1913 reconciliation
The visually verified 23 October 1913 assessment notice (`S-107`) treats original Blocks 4 and 26 separately and lists **G. A. Harding at Block 4 Lots 3 and 4**, while separately listing the Block 26 Lots 5–8 owners. Therefore the current Block 4 descriptions do not require a later conversion from original Block 26.

## Meaning of leading `2`
The Clackamas County Surveyor's plat-name index identifies **OREGON CITY, PLAT OF (McLOUGHLIN'S)** as **Plat No. 0002**. Current Oregon City legal descriptions elsewhere retain other high original block numbers with the same `2 OREGON CITY` prefix. The leading 2 should therefore be treated as the plat/subdivision identifier, not as proof of a later block-renumbering system.

Official county index:
https://www.clackamas.us/surveyor/platnames

## OHS title-abstract lead reclassified
The visually verified OHS MSS 1503 Box 19 index entry titled **Block 4, Lots 3 & 4, Oregon City — Main St., 5th St.** is no longer treated as a possible bridge from original Block 26 to a later Block 4. It is now a potentially direct **original Block 4 target-property title abstract**, especially because G. A. Harding is independently listed on Lots 3–4 in 1913. The separate Lot field still reads 3,4,5 and that conflict remains preserved. The abstract itself remains a MANUAL CALLOUT.

## Current geometry caution
The modern storefront parcels cross underlying lot portions:
- 503 = part Lot 4;
- 505 = parts Lots 3 & 4;
- 507 = parts Lots 2, 3 & 4.

Do not assume these modern parcel boundaries existed identically in 1922. Use deed dimensions and title chains to reconstruct the Harding → Wolf/Gates division.

## Source-quality caution
The target legal-description wording is currently supported by public commercial property pages that state their data are gathered from Clackamas County tax records/public-record providers. City permit records independently support target APNs/tax-lot IDs. Official recorded deed/assessor images remain desirable before treating every current legal call as primary archival proof.

## Corrected research target
The historical title/deed search for the odd-numbered Fifth-to-Sixth frontage should use **original Block 4**, especially Lots 3–4, alongside exact addresses/APNs. Block 26 remains a valid opposite-side comparator and should not be deleted from the archive.
""")

# 4. Evidence register E-094.
replace_section("evidence/evidence-register.md", "## E-094 — Original Oregon City Plat / Block 26 Lot 5 Boundary Alignment", "## E-095 — OHS MSS 1503 Main/Fifth Title-Abstract Index Entry", """## E-094 — Original Oregon City Plat / Block 4–Block 26 Orientation Correction
Type: Primary official plat + primary newspaper assessment notice + primary Sanborn map, reconciled with current county-derived parcel/legal-description records
Dates: 1844/1849 survey narrative; plat cataloged 1850; assessment notice 23 October 1913; Sanborn May 1925; current parcel cross-check August 2026
Sources: `S-107`, `S-108`, `S-021`; cross-reference `S-078` / `E-064`
Related record: `evidence/E-094-original-plat-block26-lot5-boundary.md`
Claims: The visually verified 1913 assessment record treats original **Block 4** and **Block 26** as separate physical blocks and lists **G. A. Harding at Block 4 Lots 3 and 4**, while separately listing Block 26 Lots 5–8 owners. Current county-derived legal descriptions place **503/505/507 on Block 4** and **504 Main on opposite-side Block 26 Lot 5**. This corrects the prior project orientation: the odd-numbered 501/503/505/507 frontage is original **Block 4**, not Block 26. The former inference that 501+503+505 occupied Block 26 Lot 5 and 507 began in Block 26 Lot 6 is withdrawn. The OHS Block 4 Lots 3–4 abstract is now a potentially direct correct-side title lead rather than a supposed cadastral-conversion bridge.
Confidence: Very High for the visually verified 1913 Block 4/Block 26 distinction and owners; High / strong convergence for the corrected side-of-Main orientation from current county-derived records; Withdrawn for the former Block 26 target-frontage alignment; Unresolved for historic 501's exact Block 4 lot and the 1922 Gates/Wolf dividing line.""")

# 5. Database evidence E-094 plus the E-020 stale alignment claim.
yaml_rel = "database/evidence.yml"
y = read(yaml_rel)
m = re.search(r"(?ms)^  - id: E-094\n.*?(?=^  - id: E-095\n)", y)
if not m:
    raise RuntimeError("E-094 YAML block not found")
b = m.group(0)
b = re.sub(r"(?m)^    name: .*$", "    name: Original Oregon City Plat / Block 4–Block 26 Orientation Correction", b, count=1)
b = re.sub(r"(?m)^    type: .*$", "    type: Primary official plat and assessment evidence reconciled with current parcel records", b, count=1)
new_claims = """    claims:\n      - The visually verified 1913 assessment notice treats original Block 4 and Block 26 as separate physical blocks and lists G. A. Harding at Block 4 Lots 3 and 4.\n      - Current county-derived legal descriptions place 503, 505 and 507 Main in Block 4 while current 504 Main on the opposite side is part of Lot 5, Block 26.\n      - The prior inference that 501+503+505 occupied original Block 26 Lot 5 and 507 began in Block 26 Lot 6 is withdrawn and superseded.\n      - The corrected odd-numbered target frontage is original Block 4; historic 501's exact Block 4 lot and the 1922 Gates/Wolf division remain unresolved.\n      - The OHS Block 4 Lots 3 and 4 title abstract is now a potentially direct correct-side title lead rather than a supposed Block 26-to-Block 4 conversion bridge.\n"""
b2, n = re.subn(r"(?ms)^    claims:\n.*?(?=^    confidence:)", new_claims, b, count=1)
if n != 1:
    raise RuntimeError("E-094 YAML claims replacement failed")
b2 = re.sub(r"(?m)^    confidence: .*$", "    confidence: Very High for the 1913 Block 4/Block 26 distinction; High for corrected orientation; former Block 26 target-frontage inference withdrawn; exact historic lot boundaries remain unresolved.", b2, count=1)
y = y[:m.start()] + b2 + y[m.end():]
y = y.replace("      - In combination with the official original plat, the 1925 printed scale supports the limited Lot 5/Lot 6 alignment recorded as E-094.\n", "      - E-094 now records the Task 6 correction that the odd-numbered target frontage is original Block 4, not Block 26; any proportional Sanborn lot-width test must be re-run against Block 4 geometry.\n", 1)
write(yaml_rel, y)

# 6. Open question OQ-029: false premise resolved.
replace_section("evidence/open-questions.md", "## OQ-029 — Original Block 26 / Later Block 4 Conversion", "## OQ-030 — Dr. Bailey / Harding Building Occupancy Claim", """## OQ-029 — Block 4 / Block 26 Orientation and Alleged Conversion
Status: **ANSWERED / PRIOR PREMISE CORRECTED (Task 6, 26 August 2026).**

No filing has been found converting the target 503/505 frontage from original Block 26 to later Block 4 because the evidence now shows that conversion was never required. The 1913 assessment record treats **Block 4** and **Block 26** as separate physical blocks and lists **G. A. Harding at Block 4 Lots 3–4**. Current county-derived property descriptions place **503/505/507 in Block 4**, while **504 Main across the street remains Block 26 Lot 5**. The odd-numbered target frontage was therefore assigned to the wrong side of Main in the former working model.

Superseded: `E-094`'s former inference that 501+503+505 ≈ Block 26 Lot 5 and 507 ≈ Block 26 Lot 6.

Still open as separate questions: historic 501's exact Block 4 lot, the exact 1922 Harding → Wolf/Gates deed boundaries, and whether modern 503/505 parcel divisions existed in the same form in 1922. The OHS MSS 1503 Box 19 **Block 4 Lots 3–4 / Main & Fifth** abstract is now a direct correct-side title-chain lead; its actual contents remain unretrieved.""")

# 7. Research lead RL-026 refocused on Block 4.
replace_section("evidence/research-leads.md", "## RL-026 — Reconstruct Block 26 Lot-to-Address Mapping", "## RL-027 — Identify the 1907 Pacific States Telephone Office Address and Lot", """## RL-026 — Reconstruct Original Block 4 Lot-to-Address Mapping
**Task 6 correction:** the prior Block 26 target-side reconstruction is superseded. `E-094` now establishes that original Block 4 and Block 26 are opposite-side blocks, not successive systems. Current 503/505/507 legal-description leads lie in **Block 4**, while current 504 Main lies in **Block 26 Lot 5**.

The title reconstruction should now start from:
- **1913 G. A. Harding — Block 4 Lots 3 and 4** (`S-107` / `E-094`);
- current 503 — part Lot 4, Block 4;
- current 505 — parts Lots 3 and 4, Block 4;
- current 507 — parts Lots 2, 3 and 4, Block 4;
- OHS MSS 1503 Box 19 — title field Block 4 Lots 3 & 4 / Main & Fifth, separate Lot field 3,4,5 (`E-095`).

Highest priority is to retrieve the OHS abstract and the **July 1922 Harding → S. Wolf / C. Gates deed(s)**, then fix the internal Gates/Wolf line against 501/503/505. Do not backdate modern parcel boundaries to 1922 and do not use the former Block 26 Lot 5 model.

Block 26 evidence (`E-064`, the 1913 Lots 5–8 owners) remains valid for the opposite/even side and is useful as a geographic control, not as the target title chain.""")

# 8. Building records.
replace_once("buildings/501-main.md",
"The visually verified official original Oregon City plat says lots in the target Applegate-surveyed portion are at least **66 feet front by 100 feet back**. Measured proportionally against the printed scale on the visually verified 1925 Sanborn, the combined 501+503+505 frontage is approximately 66–67 feet. This supports a **strong inference** that all three storefronts lie approximately within original **Block 26 Lot 5**, with the Lot 5/Lot 6 division at or near the 505/507 wall (`E-094`). It is not yet a deed/survey proof, and it does not identify the July 1922 fire-origin room.",
"Task 6 corrected the cadastral orientation: the odd-numbered 501/503/505/507 frontage is original **Block 4**, not Block 26 (`E-094`). Current 503 and 505 legal-description leads anchor the surviving frontage in Block 4, while current 504 across Main remains Block 26 Lot 5. Historic 501's exact Block 4 lot is still unresolved; the former claim placing 501 within Block 26 Lot 5 is withdrawn. The proportional 1925 frontage measurement may be re-tested against Block 4 geometry, but is not cadastral proof and does not identify the July 1922 fire-origin room.")
replace_once("buildings/501-main.md", "- Can a deed, title abstract or survey prove the strong working placement of 501 within original Block 26 Lot 5?", "- Which original Block 4 lot contained historic 501, and can a deed, title abstract, numbering plat, or survey prove it?")

# Replace the entire 503 boundary section through the next heading.
replace_section("buildings/503-main.md", "## 503 / 505 Boundary and Footprint Issue", "## Research Priorities", """## 503 / 505 Boundary and Footprint Issue
There is an unresolved modern physical-boundary question between 503 and 505. Current owner observation suggests 505 may extend farther back than 503, while 503 may be somewhat wider. This still requires tax maps, assessor sketches, deeds, permits, Sanborn maps, and physical measurements.

**Task 6 corrected the original-block orientation.** The odd-numbered 501/503/505/507 frontage is original **Block 4**, not Block 26 (`E-094`). Current county-derived legal-description leads report:
- 503 = **part Lot 4, Block 4**;
- 505 = **parts Lots 3 & 4, Block 4**;
- 507 = **parts Lots 2, 3 & 4, Block 4**.

Current 504 across Main is reported as part Lot 5, **Block 26**, confirming the opposite-side relationship. The former 501/503/505≈Block 26 Lot 5 model is withdrawn.

The 1913 assessment independently places **G. A. Harding at Block 4 Lots 3 and 4**. The OHS MSS 1503 Box 19 index identifies a Main/Fifth abstract titled **Block 4, Lots 3 & 4**, with a separate Lot field reading 3,4,5 (`E-095`). That abstract is now a potentially direct correct-side title lead, but its contents remain unretrieved and it cannot yet prove the 503 chain.

The 1929–2025 aerial photocompare series (`E-021` / `S-023`) still shows three distinct roofs at 501, 503, and 505 Main in 1936 and 501 absent by 1944.""")
replace_once("buildings/503-main.md", "- Obtain deed/title/survey proof for the strong working placement of 503 within original Block 26 Lot 5.", "- Obtain recorded deed/title/assessor proof connecting 503 to original Block 4 Lot 4 and trace the Harding-era Block 4 title chain without backdating current parcel boundaries.")

replace_once("buildings/505-main.md",
"The **original-lot** placement is now narrower than the modern 503/505 boundary question. The visually verified original plat gives target Block 26 lots at least 66 feet of frontage; a proportional reading of the 1925 Sanborn makes 501+503+505 approximately 66–67 feet wide. The strong working alignment therefore places **505 within original Lot 5** and the Lot 5/Lot 6 division at or near the 505/507 wall (`E-094`). This supersedes the former 50-foot hypothesis that 505 might begin at Lot 6. Deed/title/survey proof and the Block 26-to-later-Block 4 conversion remain unresolved.",
"**Task 6 corrected the original-block placement.** The odd-numbered target frontage is original **Block 4**, not Block 26 (`E-094`). Current county-derived legal-description leads report **505 as parts of Block 4 Lots 3 and 4**, 503 as part Lot 4, and 507 as parts Lots 2–4; current 504 across Main remains Block 26 Lot 5. The former 505-within-Block-26-Lot-5 model and the supposed Block 26-to-Block 4 conversion are withdrawn. The exact 1922 boundaries and the relationship of modern parcel lines to the Harding/Wolf/Gates division remain unresolved.")

replace_once("buildings/507-harding-building.md",
"The visually verified original plat and a proportional reading of 1925 Sanborn Sheet 6 now support a **strong inference** that the original Block 26 Lot 5/Lot 6 division fell at or very near the 505/507 wall, so **507 began approximately on Lot 6** (`E-094`). This is not a deed or survey-overlay proof and must not be back-applied automatically to every later consolidated 507–511 footprint.",
"Task 6 corrected the cadastral orientation: 507 lies on the odd-numbered **original Block 4** frontage, not Block 26 (`E-094`). Current county-derived legal-description records place the present 507 parcel in parts of Block 4 Lots 2, 3 and 4. That modern consolidated parcel must not be back-applied automatically to the pre-1967 storefronts, and the former claim that 507 began in Block 26 Lot 6 is withdrawn.")

# 9. Address and ownership registers.
replace_once("registers/address-register.md",
"| 501 Main Street, Oregon City, Oregon (historic / removed) | `B-005` | `buildings/501-main.md` | `BUS-024` Palace Saloon (1912); `BUS-025` Hunsaker & Taylor liquor premises (1913); 1925 store occupant unresolved | `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-104` | Strong working placement within original Block 26 Lot 5; not cadastral proof. The 1912 and 1913 liquor notices prove separately named premises, not business/ownership continuity. Gates's 1922 corner restaurant/replacement may map principally here or may include 503. If the July restaurant=501 equation is proved, 501 would be strongly disfavored as the Wolf ignition room; it remains live now. Distinct structure present in 1936 and gone by 1944. |",
"| 501 Main Street, Oregon City, Oregon (historic / removed) | `B-005` | `buildings/501-main.md` | `BUS-024` Palace Saloon (1912); `BUS-025` Hunsaker & Taylor liquor premises (1913); 1925 store occupant unresolved | `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-104` | Task 6 places the odd-numbered frontage in original Block 4; 501's exact Block 4 lot remains unresolved. The 1912 and 1913 liquor notices prove separately named premises, not business/ownership continuity. Gates's 1922 corner replacement may map principally here or may include 503. Distinct structure present in 1936 and gone by 1944. |")
replace_once("registers/address-register.md",
"| 503 Main Street, Oregon City, Oregon | `B-001` | `buildings/503-main.md` | `BUS-001`, `BUS-002`, `BUS-003`, `BUS-004`, `BUS-018`, `BUS-019`, `BUS-020` | `E-001`, `E-002`, `E-003`, `E-009`, `E-011`, `E-012`, `E-022`, `E-025`, `E-094`, `E-095`, `E-096`, `E-097`, `E-098`, `E-099` | Kwality Cafe lineage; The Wheel at 503 under Raye Grisham (`P-006`). Strong working placement within original Lot 5. 503 could be the start of Wolf's 1922 remainder or part of Gates's two-store replacement; exact line unresolved. `E-038` belongs to 505. OHS index is a retrieval lead, not title proof. |",
"| 503 Main Street, Oregon City, Oregon | `B-001` | `buildings/503-main.md` | `BUS-001`, `BUS-002`, `BUS-003`, `BUS-004`, `BUS-018`, `BUS-019`, `BUS-020` | `E-001`, `E-002`, `E-003`, `E-009`, `E-011`, `E-012`, `E-022`, `E-025`, `E-094`, `E-095`, `E-096`, `E-097`, `E-098`, `E-099` | Kwality Cafe lineage; The Wheel at 503 under Raye Grisham (`P-006`). Current legal-description lead: part Lot 4, original Block 4. 503 could be the start of Wolf's 1922 remainder or part of Gates's two-store replacement; exact historical line unresolved. OHS Block 4 abstract is a retrieval lead, not title proof. |")
replace_once("registers/address-register.md",
"| 507 Main Street, Oregon City, Oregon | `B-003` | `buildings/507-harding-building.md` | `BUS-007`, `BUS-008`, `BUS-023` | `E-016`, `E-017`, `E-045`, `E-094`, `E-095` | Strong working placement begins near original Lot 6. Original Harding Building gutted 1 September 1967; present 507-511 replacement is dated 1968 at the historic-inventory level. OHS index scope remains unresolved. |",
"| 507 Main Street, Oregon City, Oregon | `B-003` | `buildings/507-harding-building.md` | `BUS-007`, `BUS-008`, `BUS-023` | `E-016`, `E-017`, `E-045`, `E-094`, `E-095` | Original Block 4 frontage; current consolidated parcel is reported as parts Lots 2, 3 & 4. Do not backdate that parcel shape to pre-1967 storefronts. Original Harding Building gutted 1 September 1967; present 507-511 replacement is dated 1968 at the historic-inventory level. |")

old_rows = """| 23 Oct. 1913 assessment | Original Block 26, Lot 5 | Mary E. Barlow and Juliette E. David | Listed assessed owners | `E-094` / `S-107` | Very High for the printed assessment listing | Strong map inference places later 501/503/505 approximately in this lot. Not a 1922 title finding and not proof of improvement/building ownership. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 6 | First National Bank | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Strong map inference places its south boundary at or near later 505/507. Cadastral proof and 1922 chain remain open. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 7 | Frank Jaggar | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Main-side sequence anchor only; 1922 title chain not established. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 8 | Gambrinus Brewing Company | Listed assessed owner | `E-094` / `S-107`; cross-reference `E-064` | Very High for the printed assessment listing | Independently anchored at Sixth/Main by 1906 William Tell/Gambrinus evidence. |"""
new_rows = """| 23 Oct. 1913 assessment | Original Block 4, Lot 3 | G. A. Harding | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 505 is reported as including part Lot 3. Not proof that modern parcel lines existed in 1913/1922. |
| 23 Oct. 1913 assessment | Original Block 4, Lot 4 | G. A. Harding | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Correct target-side cadastral anchor; current 503 is reported as part Lot 4 and 505 as including part Lot 4. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 5 | Mary E. Barlow and Juliette E. David | Listed assessed owners | `E-094` / `S-107` | Very High for the printed assessment listing | Opposite/even side of Main; current 504 is reported as part Lot 5, Block 26. Former 501/503/505 linkage withdrawn. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 6 | First National Bank | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Opposite/even-side Block 26 evidence; not the target odd-numbered frontage. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 7 | Frank Jaggar | Listed assessed owner | `E-094` / `S-107` | Very High for the printed assessment listing | Opposite/even-side Block 26 evidence. |
| 23 Oct. 1913 assessment | Original Block 26, Lot 8 | Gambrinus Brewing Company | Listed assessed owner | `E-094` / `S-107`; cross-reference `E-064` | Very High for the printed assessment listing | Opposite/even side; independently anchored at Sixth/Main by 1906 William Tell/Gambrinus evidence. |"""
replace_once("registers/ownership-timeline.md", old_rows, new_rows)

# 10. Sanborn notes.
replace_once("maps/sanborn-map-register.md", "- Use: High-priority sheet for the 501 / 503 / 505 Main question and for testing 503/505 building footprint, address numbering, construction hypotheses, and the `E-094` proportional alignment of the original Lot 5/Lot 6 division near the 505/507 wall.", "- Use: High-priority sheet for the 501 / 503 / 505 Main question and for testing 503/505 building footprint, address numbering, construction hypotheses, and the corrected `E-094` original **Block 4** lot-to-address reconstruction. The former Block 26 Lot 5/Lot 6 target alignment is withdrawn.")

map_rel = "maps/sanborn-comparison-503-505-507.md"
replace_once(map_rel,
"15. The original plat says target-area lots are at least **66 feet front by 100 feet back**. On the 1925 sheet's printed scale, 501+503+505 span approximately 66–67 feet. This supports a **strong inference** that those three storefronts occupy original Lot 5 and that original Lot 6 begins at or near the 505/507 wall (`E-094`). It is not a deed/survey proof.",
"15. **Task 6 corrects the cadastral orientation:** the odd-numbered 501/503/505/507 frontage is original **Block 4**, while Block 26 is across Main. The earlier inference assigning 501+503+505 to Block 26 Lot 5 and 507 to Block 26 Lot 6 is withdrawn (`E-094`). The approximately 66–67-foot 1925 frontage measurement may be re-tested against Block 4 geometry but is not a lot assignment by itself.")
replace_once(map_rel,
"| 1892 | `SM-005` | Block 26 at Main and 5th shows a developed row of Main-facing commercial spaces. Visible labels include clothing/gents furnishing, boots and shoes, grocery, store, millinery, crockery, and Commercial Bank near the 5th/Main corner. The modern 501/503/505 numbering is not the dominant labeling on this sheet. | Strong evidence of a pre-1919 commercial frontage in the relevant 5th/Main block. Use cautiously for exact modern address mapping until address-number transition is resolved. |",
"| 1892 | `SM-005` | The 5th/Main area shows developed commercial frontages with labels including clothing/gents furnishing, boots and shoes, grocery, store, millinery, crockery, and Commercial Bank. The prior project reading that assigned the target odd-numbered row to Block 26 is superseded by Task 6; re-read the sheet with Block 4/Block 26 side orientation explicit. | Strong evidence of pre-1919 commercial development, but exact modern-address mapping must be rebuilt on the corrected Block 4 target side. |")
replace_once(map_rel,
"| 1925 | `SM-008` | Sheet 6 shows modern-style Main address labels including `501`, `503`, `505`, `507`, `509`, `511`, `513`, and more. The 501 space appears as a store at/near the 5th/Main corner. The 503 space is labeled restaurant with concrete floor. The 505 space is labeled billiards and cigars. Adjacent/northern spaces include dry goods/clothing/gents furnishing, grocery, drugs, and billiards/cigars with I.O.O.F. Hall on the second floor. | This answers part of the 501 question: `501` was shown as an address/space on the 1925 Sanborn sheet. 503 and 505 were separate labeled occupancies. Scale comparison supports 501+503+505 ≈ Lot 5 and 505/507 ≈ Lot 5/Lot 6 (`E-094`). The use pattern is compatible with—but does not prove—Gates=501+503 or 503 ignition/505 pool. |",
"| 1925 | `SM-008` | Sheet 6 shows modern-style Main address labels including `501`, `503`, `505`, `507`, `509`, `511`, `513`, and more. The 501 space appears as a store at/near the 5th/Main corner. The 503 space is labeled restaurant with concrete floor. The 505 space is labeled billiards and cigars. Adjacent/northern spaces include dry goods/clothing/gents furnishing, grocery, drugs, and billiards/cigars with I.O.O.F. Hall on the second floor. | This answers part of the 501 question: `501` was shown as an address/space on the 1925 Sanborn sheet. 503 and 505 were separate labeled occupancies. Any scale-to-lot comparison must now use original **Block 4** geometry (`E-094`); the former Block 26 Lot 5 assignment is withdrawn. The use pattern remains compatible with multiple Gates/Wolf models. |")

# Replace the two interpretive sections while retaining later material.
replace_section(map_rel, "## 1906 Non-Sanborn Block 26 Anchors", "## Original Plat / 1925 Scale Alignment", """## 1906 Non-Sanborn Block 26 Anchors — Corrected Orientation
The 1906 evidence remains important, but Task 6 changes how it is used:

- `E-061` establishes Oregon City's formal street-numbering program and missing numbering plat.
- `E-064` establishes the William Tell Hotel / Gambrinus property at **Lot 8, Block 26, Sixth & Main**.
- Task 6 shows that Block 26 is the **opposite/even-numbered side of Main**, not the odd-numbered 501/503/505/507 target frontage.
- Current 504 Main, reported as part Lot 5 Block 26, independently supports that orientation.

Therefore the former strategy of walking from Block 26 Lot 8 south through Lots 7/6/5 to assign the odd-numbered storefronts is withdrawn. The target reconstruction must instead use **original Block 4**, the 1913 Harding Lots 3–4 ownership, current Block 4 parcel leads, and the missing numbering plat/title records.""")
replace_section(map_rel, "## Original Plat / 1925 Scale Alignment", "## July–August 1922 Property Division vs. the 1925 Frontage", """## Original Plat / 1925 Scale Alignment — Task 6 Correction
The original plat remains the controlling geometry source, but the prior project placed the target frontage on the wrong side of Main.

The 1913 assessment (`S-107`) simultaneously identifies **G. A. Harding at Block 4 Lots 3–4** and separate owners for Block 26 Lots 5–8. Current county-derived records place 503/505/507 on Block 4 and current 504 on Block 26. Thus the odd-numbered target frontage is original **Block 4**.

The 1925 scale observation that the Fifth edge through the 505/507 wall is approximately 66–67 feet is preserved only as a measurement. It no longer supports a Block 26 Lot 5/Lot 6 assignment. Re-test it against Block 4 lot geometry and deed calls before using it as a cadastral conclusion.

Corrected title focus:
- 1913 Harding — Block 4 Lots 3–4;
- current 503 — part Block 4 Lot 4;
- current 505 — parts Block 4 Lots 3–4;
- OHS MSS 1503 Box 19 — Block 4 Lots 3–4 / Main & Fifth;
- July 1922 Harding → Wolf/Gates deed(s).

Classification: **Block orientation corrected with high confidence; exact historic lot-to-storefront mapping still unresolved.**""")

# 11. Mark older task/research notes with a prominent supersession banner.
banner = "> **Task 6 cadastral correction (26 Aug 2026):** the odd-numbered 501/503/505/507 frontage is original **Block 4**, not Block 26. Current 504 across Main remains Block 26. Any passages below that call Block 26 the target odd-numbered block or place 501/503/505 in Block 26 Lot 5 are superseded by `E-094` and `evidence/source-captures/block4-block26-side-of-main-correction-task6-2026-08-26.md`."
for rel in [
    "evidence/source-captures/1906-ordinance-357-retrieval-audit-2026-08-26.md",
    "evidence/source-captures/ordinance-357-visual-inspection-task3-2026-08-26.md",
    "evidence/source-captures/1906-numbering-plat-locator-task4-2026-08-26.md",
    "evidence/source-captures/numbering-plat-task5-blocked-2026-08-26.md",
    "evidence/source-captures/ohs-mss1503-block4-lots3-4-title-abstract-lead.md",
    "evidence/source-captures/1922-fire-s-wolf-main-street-property-lead.md",
    "evidence/source-captures/1913-building-vs-land-ownership-caution-for-1922-wolf-search.md",
    "maps/original-plats/README.md",
    "timeline.md",
    "records/historical-society/503-505-main-historical-society-research-supplement-2026-08-24.md",
]:
    if p(rel).exists():
        add_banner(rel, "Task 6 cadastral correction", banner)

# Task 5 specific stale sentence.
replace_once("evidence/source-captures/numbering-plat-task5-blocked-2026-08-26.md",
"Until the actual plat/plan is retrieved and visually inspected, do not claim that it directly assigns any specific early building or lot to 501, 503, 505, or 507 Main. The working 501/503/505 ≈ original Block 26 Lot 5 and 507 ≈ original Block 26 Lot 6 alignment remains a strong inference from independent cadastral/Sanborn geometry, not a finding from the missing numbering plat.",
"Until the actual plat/plan is retrieved and visually inspected, do not claim that it directly assigns any specific early building or lot to 501, 503, 505, or 507 Main. Task 6 has separately corrected the cadastral orientation: the odd-numbered frontage is original Block 4, not Block 26. Exact historic lot-to-address assignments, especially for removed 501, remain unresolved pending the plat/title/deed evidence.")

# OHS note: promote correct interpretation without claiming contents.
ohs_rel = "evidence/source-captures/ohs-mss1503-block4-lots3-4-title-abstract-lead.md"
if p(ohs_rel).exists():
    t = read(ohs_rel)
    if "Task 6 reclassification" not in t:
        t += "\n\n## Task 6 reclassification\nThe Block 4 / Block 26 orientation problem is now corrected. The OHS Box 19 row is no longer treated as a possible bridge from original Block 26 into a later Block 4 system. The 1913 assessment independently lists G. A. Harding at original **Block 4 Lots 3–4**, and current 503/505 legal-description leads also use Block 4 Lots 3–4. The abstract is therefore a potentially direct target-property title source. Its actual contents remain unretrieved, so no Harding-to-Wolf chain, parcel boundary, or owner may be asserted from the index alone.\n"
        write(ohs_rel, t)

# 12. Research log adds the correction without rewriting prior historical rows.
log_rel = "registers/research-log.md"
log = read(log_rel)
new_log_row = "| 2026-08-26 | Corrected original Block 4 / Block 26 orientation during Task 6 | Cross-checking the visually verified 1913 assessment against current county-derived legal descriptions shows the odd-numbered 501/503/505/507 frontage is original **Block 4**, while 504 across Main remains **Block 26 Lot 5**. The prior 501+503+505≈Block 26 Lot 5 model is withdrawn. G. A. Harding's 1913 Block 4 Lots 3–4 ownership and the OHS Box 19 Block 4 abstract are now the correct title-chain focus. | Retrieve the OHS abstract and Harding→Wolf/Gates deeds; re-test 1925 geometry against Block 4. |\n"
if new_log_row not in log:
    anchor = "| --- | --- | --- | --- |\n"
    if anchor not in log:
        raise RuntimeError("Research log table anchor missing")
    log = log.replace(anchor, anchor + new_log_row, 1)
    write(log_rel, log)

# 13. Source register Sanborn note update; source facts otherwise preserved.
replace_once("evidence/source-register.md", "Notes: May 1925 Sanborn sheet 6; repository binary at maps/sanborn/originals/1925-6 (5th).pdf. High-priority source for 501/503/505 Main and E-094 scale alignment. Related map SM-008.", "Notes: May 1925 Sanborn sheet 6; repository binary at maps/sanborn/originals/1925-6 (5th).pdf. High-priority source for 501/503/505 Main. Task 6 corrected E-094's cadastral orientation to original Block 4; the former Block 26 Lot 5/Lot 6 scale alignment is withdrawn. Related map SM-008.")

# 14. Remove temporary migration files from the resulting commit.
for rel in ["scripts/task6_correct_block_mapping.py", ".github/workflows/task6-correction.yml"]:
    try:
        p(rel).unlink()
    except FileNotFoundError:
        pass

print("Task 6 Block 4 / Block 26 correction applied.")
