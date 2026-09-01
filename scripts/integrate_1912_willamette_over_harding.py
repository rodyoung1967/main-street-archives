#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one anchor in {rel}, found {count}: {old[:160]!r}")
    write(rel, text.replace(old, new, 1))


capture = "evidence/source-captures/1912-09-07-willamette-building-over-harding-drug-store.md"
source_name = "Morning Enterprise, Willamette Building room over Harding Drug Store, 7 September 1912"
evidence_name = "Willamette Building room over Harding Drug Store, September 1912"

append_once(
    "evidence/source-register.md",
    "## S-154 — Morning Enterprise, Willamette Building room over Harding Drug Store, 7 September 1912",
    f'''## S-154 — {source_name}
Type: Primary newspaper advertisement; **VISUALLY VERIFIED TARGETED SOURCE** 31 August 2026.
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-09-07/ed-1/seq-3.pdf
Related evidence: `E-138`; related earlier evidence: `E-085`, `E-092`; later comparison: `E-137`.
Repository source capture: `{capture}`.
Notes: Direct scan review proves a Spirella Corsets advertisement for Mrs. Adalyn Davis stating **“Willamette Bldg., Room 4, Over Harding Drug Store.”** The page does not print a Main Street number in this advertisement. The source therefore establishes a 1912 vertical/building-name relationship but does not equate the Willamette Building with 507 alone or alter Harding's separately verified 511 Main business address. PDF SHA-256: `fa70ac7e96fb6ca9bf6fb7bccca9d350614ece348fc0fb21e7480b342bc550bb`.'''
)
append_once(
    "database/sources.yml",
    "  - id: S-154\n",
    f'''  - id: S-154
    name: {source_name}
    url: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-09-07/ed-1/seq-3.pdf
    notes: Visually verified 31 Aug 2026. Spirella advertisement prints “Willamette Bldg., Room 4, Over Harding Drug Store.” No numbered Main address is printed in the ad. Establishes a building-name/vertical relationship but does not prove Willamette=507 or change Harding's direct 511 listing. Related evidence E-138; full provenance in the 1912-09-07 Willamette-over-Harding source capture.'''
)

append_once(
    "evidence/evidence-register.md",
    "## E-138 — Willamette Building room over Harding Drug Store, September 1912",
    f'''## E-138 — {evidence_name}
Type: Primary newspaper building-name / vertical-space relationship evidence; **direct visual inspection**.
Source: `S-154`.
Related evidence: `E-085`, `E-092`, `E-137`.
Related building/business: `B-003`, `BUS-007`.
Repository source capture: `{capture}`.
Claims:
- The visually inspected 7 September 1912 *Morning Enterprise* page contains a Spirella Corsets advertisement for Mrs. Adalyn Davis that prints **“Willamette Bldg., Room 4, Over Harding Drug Store.”**
- This directly establishes that a room identified with the **Willamette Building** was described as being physically **over Harding Drug Store** in September 1912.
- The advertisement prints **no numbered Main Street address** for the Willamette Building, Room 4, or Harding Drug Store.
- `E-092` independently and visually places **G. H. Young at 507 Main**, **H. P. Brightbill at 509 Main**, and **Geo. A. Harding at 511 Main** in January 1912. `E-085` separately says Young moved one door north into the Willamette Building in March 1911, but continuity from that room to Young's January 1912 507 address is not proved.
- Therefore this source **strengthens the warning against a one-building-per-number reconstruction**. It permits, but does not prove, a multi-bay named building, a change of Young premises, or broader/imprecise building naming.
- The source does not justify moving Harding from the directly printed 511 Main address, does not prove the Willamette Building equals 507 alone, and does not date demolition/reconstruction of 503 or 505.
- In combination with `E-137` (Freeze “over Hardings Drug Store” in March 1921 followed by 507½ ads), it shows that historical “over” descriptions and half-numbered professional rooms require separate evidence from ground-floor storefront numbering.
Confidence: **Very High** for the visible 1912 wording and vertical/building-name relationship; **unresolved** for exact numbered building footprint, multi-bay extent, Young continuity, and implications for later 507/511 numbering.'''
)
append_once(
    "database/evidence.yml",
    "  - id: E-138\n",
    f'''  - id: E-138
    name: {evidence_name}
    type: Primary newspaper building-name / vertical-space relationship evidence; direct visual inspection
    claims:
      - The visually inspected 7 September 1912 Morning Enterprise page prints “Willamette Bldg., Room 4, Over Harding Drug Store” in a Spirella advertisement for Mrs. Adalyn Davis.
      - This directly establishes a September 1912 vertical/building-name relationship between a Willamette Building room and Harding Drug Store.
      - The advertisement prints no numbered Main Street address for the building, room, or Harding Drug Store.
      - Earlier exact-address evidence E-092 still directly places Young at 507, Brightbill at 509, and George A. Harding at 511 Main in January 1912; E-085's Young-to-Willamette continuity remains unresolved.
      - The result warns against assuming one named building equals one storefront number; a multi-bay building, changed Young premises, or broader building naming remain models to test, not conclusions.
      - It does not date demolition/reconstruction of 503 or 505 and does not change the direct 511 Harding business listing.
    confidence: Very High for visible wording and vertical relationship; unresolved for exact numbered footprint, multi-bay extent, and Young continuity.
    related_sources: [S-154]
    related_evidence: [E-085, E-092, E-137]
    related_buildings: [B-003]
    related_businesses: [BUS-007]
    repository_file: {capture}'''
)

append_once(
    "evidence/E-085-1911-harding-building-location-ambiguity.md",
    "## 1912 Willamette-over-Harding constraint",
    '''## 1912 Willamette-over-Harding constraint
`E-138` / `S-154` adds a direct September 1912 relationship that makes the exact-building-number caution even more important. A visually verified Spirella advertisement prints **“Willamette Bldg., Room 4, Over Harding Drug Store.”** The advertisement gives no number. At the same time, `E-092` directly places George Young at 507 Main and George A. Harding's drug business at 511 Main in January 1912.

This means the archive must not simply equate **Willamette Building = 507 only** and **Harding Building/Drug Store = the adjacent single number**. Possible multi-bay building extent, a change in Young's premises, and broader contemporary building naming all remain open. Preserve the 1911 one-door-north statement, the 1912 exact address ladder, and the September 1912 “over Harding” wording as simultaneous constraints.'''
)
append_once(
    "evidence/E-092-1912-main-address-ladder-young-harding.md",
    "## September 1912 building-name constraint",
    '''## September 1912 building-name constraint
A later visually verified 7 September 1912 advertisement (`E-138` / `S-154`) states **“Willamette Bldg., Room 4, Over Harding Drug Store.”** It prints no number. That wording does not alter the exact January ladder on this page—Young 507, Brightbill 509, Harding 511—but it prevents treating the hypothesis “Young's Willamette Building = 507” as a proved one-building/one-number identity. The named Willamette Building may have encompassed multiple numbered bays, Young may have changed premises between March 1911 and January 1912, or the building naming may have been broader than storefront numbering. Those alternatives remain unresolved.'''
)
append_once(
    "businesses/harding-drug-store.md",
    "## September 1912 Willamette Building relationship",
    '''## September 1912 Willamette Building relationship
A visually verified 7 September 1912 *Morning Enterprise* Spirella advertisement (`E-138` / `S-154`) gives the location **“Willamette Bldg., Room 4, Over Harding Drug Store.”** This is direct evidence that a room identified with the Willamette Building was described as above Harding's store. The ad gives no number, so the direct January 1912 **511 Main** Harding listing remains controlling for that exact date. Do not convert the Willamette wording into an unsupported 507 Harding address or assume one named building equaled one numbered storefront.'''
)
append_once(
    "buildings/507-harding-building.md",
    "## September 1912 Willamette/Harding building-name constraint",
    '''## September 1912 Willamette/Harding building-name constraint
`E-138` / `S-154` visually verifies a Spirella advertisement locating **Willamette Bldg., Room 4, “Over Harding Drug Store.”** This new 1912 vertical relationship complicates any simple mapping of the Willamette Building to 507 alone, because the separate January 1912 address ladder directly places George Young at 507, Brightbill at 509, and George A. Harding's drug business at 511.

The evidence is compatible with a named building spanning more than one numbered storefront, with Young having changed premises, or with broader contemporary building-name usage. None is yet proved. For reconstruction, treat the named-building footprint, storefront numbers, and upstairs half-numbered rooms as separate layers until an original plan, Sanborn detail, lease, directory, or advertisement explicitly bridges them.'''
)
append_once(
    "maps/sanborn-comparison-503-505-507.md",
    "## Building-name caution added by September 1912 evidence",
    '''## Building-name caution added by September 1912 evidence
A visually verified September 1912 advertisement (`E-138` / `S-154`) places **Room 4 of the Willamette Building over Harding Drug Store** without a street number. Read alongside the January 1912 507/509/511 address ladder, this cautions against forcing each historical named building into a single numbered Sanborn bay. When comparing the 1911 and 1925 sheets, keep named-building identity, ground-floor storefront numbering, and upstairs/half-number rooms separate unless a source explicitly joins them.'''
)
append_once(
    "registers/research-log.md",
    "### 2026-08-31 — 1912 Willamette Building / Harding Drug Store vertical relationship verified",
    '''### 2026-08-31 — 1912 Willamette Building / Harding Drug Store vertical relationship verified
- Recovered and visually inspected the 7 Sep 1912 *Morning Enterprise*, p3, after indexed OCR surfaced a repeated Spirella ad.
- The scan directly prints **“Willamette Bldg., Room 4, Over Harding Drug Store.”** (`S-154` / `E-138`).
- Preserved the conflict/constraint with `E-085` and `E-092`: Young's later 507 address does not prove the Willamette Building was 507 alone, while Harding's direct January 1912 business listing remains 511 Main.
- No building-number merger, 503/505 construction date, or multi-bay footprint conclusion was made. The result instead strengthens the rule that named buildings, numbered storefronts, and upstairs half-numbers must be reconstructed separately.'''
)

print("Prepared S-154 / E-138 Willamette-over-Harding integration")
