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
        raise RuntimeError(f"Expected one anchor in {rel}, found {count}: {old[:140]!r}")
    write(rel, text.replace(old, new, 1))


capture = "evidence/source-captures/1921-03-18-to-04-08-freeze-507-half-to-505-half-transition.md"

# Source register + YAML mirror.
append_once(
    "evidence/source-register.md",
    "## S-153 — Oregon City Enterprise, Dr. Freeze March–April 1921 relocation source set",
    '''## S-153 — Oregon City Enterprise, Dr. Freeze March–April 1921 relocation source set
Type: Primary newspaper scans; **VISUALLY VERIFIED TARGETED SOURCE SET** 31 August 2026.
Canonical PDFs:
- https://oregonnews.uoregon.edu/lccn/sn00063700/1921-03-18/ed-1/seq-5.pdf
- https://oregonnews.uoregon.edu/lccn/sn00063700/1921-03-25/ed-1/seq-3.pdf
- https://oregonnews.uoregon.edu/lccn/sn00063700/1921-04-01/ed-1/seq-3.pdf
Related evidence: `E-137`; related existing source: `S-035` (8 April 1921 at 505½ Main).
Repository source capture: `evidence/source-captures/1921-03-18-to-04-08-freeze-507-half-to-505-half-transition.md`.
Notes: The 18 March article reports Dr. Harvey Freeze moving his practice from Portland to Oregon City and locating **over Hardings Drug Store** but prints no Oregon City number. Direct scan review of 25 March and 1 April ads proves **507½ Main St.** on both dates; OCR `507` for 1 April is wrong. Existing visually verified 8 April evidence (`S-035` / `E-028`) then prints **505½ Main**. This establishes a 507½→505½ advertised-address change after 1 April and by 8 April, not the exact physical move day. Harding at numbered 507 is a strong cross-source inference, not source-explicit wording.'''
)
append_once(
    "database/sources.yml",
    "  - id: S-153\n",
    '''  - id: S-153
    name: Oregon City Enterprise Dr. Freeze March-April 1921 relocation source set
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1921-03-18/ed-1/seq-5.pdf
    notes: Three primary pages visually verified 31 Aug 2026. Mar 18 reports Harvey Freeze moving from Portland to Oregon City and locating over Hardings Drug Store without a number; Mar 25 and Apr 1 ads visibly print 507½ Main. Existing S-035/E-028 prints 505½ Main on Apr 8, proving an advertised-address shift after Apr 1 and by Apr 8. Harding-at-507 remains a strong inference until a source directly prints its number. Related evidence E-137; full provenance in the 1921 Freeze transition capture.'''
)

# New evidence + YAML mirror.
append_once(
    "evidence/evidence-register.md",
    "## E-137 — Dr. Freeze relocation from 507½ to 505½ Main, March–April 1921",
    '''## E-137 — Dr. Freeze relocation from 507½ to 505½ Main, March–April 1921
Type: Primary newspaper professional-location and relocation evidence; **direct visual inspection**.
Sources: `S-153`, existing `S-035` / `E-028` for 8 April 1921.
Related buildings: `B-003` (507/Harding context), `B-002` (505).
Related business/person: `BUS-021`, `P-027`.
Repository source capture: `evidence/source-captures/1921-03-18-to-04-08-freeze-507-half-to-505-half-transition.md`.
Claims:
- The 18 March 1921 *Oregon City Enterprise* headline reports **DOCTOR FREEZE TO MOVE OFFICES FROM PORTLAND**; the subhead says the well-known eye specialist is locating **over Hardings Drug Store**.
- The body names **Dr. Harvey Freeze**, says he had offices at Sixth and Washington streets in Portland for the prior twelve years, and says he **has moved to Oregon City to practice his profession**. It prints no numbered Oregon City address.
- Direct visual review of the 25 March advertisement clearly prints **507½ Main St., Oregon City**.
- Direct visual review of the 1 April advertisement also clearly prints **507½ Main St.**; an OCR reading of `507` is incorrect.
- Existing visually verified 8 April evidence (`E-028` / `S-035`) prints **505½ Main Street, Oregon City**.
- Therefore Freeze changed his advertised exact address from **507½ to 505½ after the 1 April issue and by the 8 April issue**. The exact physical move day is not established.
- Because the 18 March article says his first Oregon City office was over Harding's Drug Store and the next exact ads place Freeze at 507½, **Harding Drug Store at/under the 507 address is a strong spatial/address inference for late March 1921, not a source-explicit numbered fact**. Earlier direct evidence places Harding's own drug business at 511 Main in 1911–1915.
- The 505½ address reuse between A. Leland's June 1920 pool-hall permit (`E-135`) and Freeze by 8 April 1921 narrows occupancy chronology but does not prove room identity, succession, upstairs geometry, property ownership, or construction date of the surviving 505 building.
Confidence: **Very High** for the visually verified March 18 wording and 507½/505½ dates; **strong inference only** for Harding's numbered 507 association; unresolved for exact move day, physical room relationship, Leland succession, and construction timing.'''
)
append_once(
    "database/evidence.yml",
    "  - id: E-137\n",
    '''  - id: E-137
    name: Dr. Freeze relocation from 507½ to 505½ Main, March-April 1921
    type: Primary newspaper professional-location and relocation evidence; direct visual inspection
    claims:
      - The 18 March 1921 Oregon City Enterprise reports Dr. Harvey Freeze moving his practice from Portland to Oregon City and locating over Hardings Drug Store; it prints no Oregon City number.
      - The 25 March advertisement visibly prints 507½ Main St., Oregon City.
      - The 1 April advertisement also visibly prints 507½ Main St.; OCR 507 is incorrect.
      - Existing visually verified 8 April evidence E-028/S-035 prints 505½ Main Street.
      - Freeze therefore changed his advertised address from 507½ to 505½ after the 1 April issue and by the 8 April issue; exact physical move day is not proved.
      - Harding Drug Store at/under numbered 507 in late March is a strong cross-source spatial inference from the over-Harding wording plus Freeze's 507½ ads, not a directly printed Harding number.
      - Address reuse at 505½ after A. Leland's June 1920 permit narrows occupancy chronology but does not prove succession, room identity, upstairs geometry, ownership, or construction date.
    confidence: Very High for visually verified Freeze wording and exact-number dates; strong inference only for Harding at numbered 507; unresolved for physical relationship and construction timing.
    related_sources: [S-153, S-035]
    related_evidence: [E-028, E-128, E-135]
    related_buildings: [B-002, B-003]
    related_businesses: [BUS-021, BUS-007]
    related_people: [P-027, P-001]
    repository_file: evidence/source-captures/1921-03-18-to-04-08-freeze-507-half-to-505-half-transition.md'''
)

# Business/person YAML mirrors.
replace_once(
    "database/businesses.yml",
    '''  - id: BUS-021
    name: Dr. Freeze, Eye Specialist
    address: 505 / 505 1/2 Main
    notes: 1921-1922 newspaper ads; later Masonic Building.
    related_buildings:
      - B-002
    related_people:
      - P-027
    related_evidence:
      - E-028
    related_sources: [S-035]
    repository_file: businesses/dr-freeze.md''',
    '''  - id: BUS-021
    name: Dr. Freeze, Eye Specialist
    address: 507 1/2 Main (Mar-Apr 1921); 505 / 505 1/2 Main (Apr 1921-Jun 1922)
    notes: Mar 18 1921 move-from-Portland notice says locating over Harding Drug Store; visually verified Mar 25 and Apr 1 ads print 507½ Main, then Apr 8 prints 505½. Later Masonic Building after July 1, 1922. Exact physical move day and Harding numbered address remain limited as described in E-137.
    related_buildings:
      - B-002
      - B-003
    related_people:
      - P-027
    related_evidence:
      - E-028
      - E-137
    related_sources: [S-035, S-153]
    repository_file: businesses/dr-freeze.md'''
)
replace_once(
    "database/people.yml",
    '''    name: Dr. Freeze
    repository_file: people/profiles/dr-freeze.md
    role: Eye specialist
    notes: Advertised at 505 / 505 1/2 Main 1921-1922 using title Eye Specialist; later rooms 207-8 Masonic Building.
    related_buildings:
      - B-002
    related_businesses:
      - BUS-021
    related_evidence: [E-028]
    related_sources: [S-035]''',
    '''    name: Dr. Freeze
    repository_file: people/profiles/dr-freeze.md
    role: Eye specialist
    notes: Harvey Freeze moved his practice from Portland to Oregon City in March 1921. Visually verified ads place him at 507 1/2 Main on Mar 25 and Apr 1, then 505 1/2 Main by Apr 8 through late June 1922; later rooms 207-8 Masonic Building.
    related_buildings:
      - B-002
      - B-003
    related_businesses:
      - BUS-021
    related_evidence: [E-028, E-137]
    related_sources: [S-035, S-153]'''
)

# Entity pages.
replace_once(
    "businesses/dr-freeze.md",
    "Business ID: `BUS-021`. Addresses: 505 Main and 505½ Main (`B-002`). Person: `P-027`.\n\nPrimary 1921–1922 advertisements identify **Dr. Freeze, Eye Specialist**, at 505 or 505½ Main, opposite the post office, offering examinations, glasses, and lens grinding (`E-028` / `S-035`). By October 1922 he advertised from rooms 207–208, Masonic Building. Preserve the historical title. The sources do not prove property ownership, exact move day, or the physical relationship of 505 and 505½.",
    "Business ID: `BUS-021`. Addresses: **507½ Main** (`B-003` context) in March–1 April 1921; **505 / 505½ Main** (`B-002`) from 8 April 1921 through late June 1922. Person: `P-027`.\n\nA visually verified 18 March 1921 article says **Dr. Harvey Freeze** moved his practice from Portland to Oregon City and was locating **over Hardings Drug Store**. Ads on 25 March and 1 April visibly print **507½ Main St.**; an OCR reading of 507 on 1 April is wrong. The already verified 8 April ad prints **505½ Main**, establishing an advertised-address change after 1 April and by 8 April (`E-137` / `S-153`; `E-028` / `S-035`). Later June 1922 evidence places him at 505½ immediately before his move to rooms 207–208, Masonic Building. Preserve the historical title. The sources do not prove property ownership, exact physical move day, the physical relationship of the half-numbered rooms, or that Harding's own storefront number was directly printed as 507."
)
replace_once(
    "people/profiles/dr-freeze.md",
    "Person ID: `P-027`. Related business/address: `BUS-021`, `B-002`.\n\nNewspaper advertisements place Dr. Freeze, styled an eye specialist, at **505 / 505½ Main** in 1921–1922 and later in rooms 207–208 of the Masonic Building (`E-028`, `S-035`).\n\nThe evidence supports the dated professional location and later move, not ownership of 505, residence there, or an exact upstairs-room footprint.",
    "Person ID: `P-027`. Related business/addresses: `BUS-021`, `B-003` (507½ context), `B-002` (505/505½).\n\nA visually verified 18 March 1921 article names **Dr. Harvey Freeze** and reports that he moved his practice from Sixth and Washington in Portland to Oregon City, locating **over Hardings Drug Store**. Ads on 25 March and 1 April visibly place him at **507½ Main**; by 8 April the existing verified ad places him at **505½ Main** (`E-137`, `S-153`; `E-028`, `S-035`). He remained associated with 505/505½ through late June 1922 before moving to rooms 207–208 of the Masonic Building.\n\nThe evidence supports the dated professional locations and address change, not property ownership, residence, exact physical move day, or a proved upstairs-room/modern-building footprint."
)
append_once(
    "businesses/harding-drug-store.md",
    "## March 1921 Harding / 507½ address bridge",
    '''## March 1921 Harding / 507½ address bridge
`E-137` / `S-153` adds a new, carefully bounded bridge after the directly documented **511 Main** listings of 1911–1915. On 18 March 1921 the *Oregon City Enterprise* reports that Dr. Harvey Freeze had moved his practice from Portland to Oregon City and was locating **over Hardings Drug Store**. Directly inspected Freeze advertisements on **25 March** and **1 April** both print **507½ Main St.**; by 8 April Freeze is at 505½.

This combination strongly supports Harding Drug Store being the ground-floor/associated premises at **507** in late March 1921, but the article itself does not print `507` for Harding. The archive therefore treats Harding-at-507 in March 1921 as a **strong spatial/address inference**, not yet a direct exact-number fact. It nevertheless materially narrows the store's shift from its visually verified 511 Main location in 1911–1915. Find an independent advertisement/directory that directly prints Harding at 507 before promoting the number to source-explicit status.'''
)
append_once(
    "buildings/507-harding-building.md",
    "## March 1921 professional-office / Harding address bridge",
    '''## March 1921 professional-office / Harding address bridge
A new visually verified source set (`E-137` / `S-153`) tightens the pre-fire 507 chronology. On **18 March 1921** the *Oregon City Enterprise* says Dr. Harvey Freeze moved his practice from Portland to Oregon City and was locating **over Hardings Drug Store**. Freeze advertisements on **25 March** and **1 April** directly print **507½ Main St.** The next verified ad, 8 April, is at 505½ Main.

This proves an upstairs/half-number professional address at **507½** immediately before Freeze shifted to 505½. Read with the article's “over Hardings Drug Store” wording, Harding Drug Store at numbered **507** is a strong contemporary address inference, but no inspected source in this set directly prints Harding's number. The result is an important bridge from Harding's directly documented **511 Main** address in 1911–1915 toward the later Harding-block configuration; ownership, footprint, exact Harding move date, and physical arrangement remain open.'''
)

# Chronology registers.
replace_once(
    "registers/business-timeline.md",
    "| 1921-1922 | Dr. Freeze, Eye Specialist | `BUS-021` | `E-028` | Very High | 505 / 505 1/2; later Masonic Building. |",
    "| 8 Apr. 1921–29 Jun. 1922 | Dr. Freeze, Eye Specialist | `BUS-021` | `E-028`, `E-137` | Very High | 505 / 505½; visually verified at 507½ on 25 Mar and 1 Apr immediately before shifting to 505½ by 8 Apr; later Masonic Building. |"
)
replace_once(
    "registers/business-timeline.md",
    "| Jan. 1912; again 1914 | G. H. Young — The Curio Man / second-hand and furniture | `BUS-067` | `E-092`; 1914 exact listing; compare `E-134` | Very High for dated 507 address | The visible 1910 505 storefront and March 1911 one-door-north move strongly support a 505→507 sequence and 507/Willamette bridge; exact move day and uninterrupted occupancy remain open. |\n| Dated listings, Aug.–Oct. 1915 | W. W. Bradley furniture | `BUS-026` | `E-107` | High, visual | 507 Main, not Harding's 511 listing. No continuous occupancy or Young-to-Bradley transfer inferred. |",
    "| Jan. 1912; again 1914 | G. H. Young — The Curio Man / second-hand and furniture | `BUS-067` | `E-092`; 1914 exact listing; compare `E-134` | Very High for dated 507 address | The visible 1910 505 storefront and March 1911 one-door-north move strongly support a 505→507 sequence and 507/Willamette bridge; exact move day and uninterrupted occupancy remain open. |\n| Dated listings, Aug.–Oct. 1915 | W. W. Bradley furniture | `BUS-026` | `E-107` | High, visual | 507 Main, not Harding's 511 listing. No continuous occupancy or Young-to-Bradley transfer inferred. |\n| 18 Mar.–1 Apr. 1921 | Dr. Freeze office over Harding Drug Store context | `BUS-021`; `BUS-007` | `E-137` | Very High for Freeze at 507½; strong inference for Harding at numbered 507 | 18 Mar says Freeze is locating over Harding's; 25 Mar and 1 Apr ads directly print 507½. No source in the set directly prints Harding's number. |"
)
replace_once(
    "timelines/505-main.md",
    "| 1921–1922 | **Dr. Freeze at 505/505½ Main**, opposite post office. | **Exact primary**; property/physical arrangement open. | `BUS-021`; `P-027`; `E-028`; `S-035` |",
    "| 8 Apr. 1921–29 Jun. 1922 | **Dr. Freeze at 505/505½ Main**, opposite post office. | **Exact primary**. `E-137` visually places him at 507½ on 25 Mar and 1 Apr, so the 505½ advertised-address shift occurred after 1 Apr and by 8 Apr. Property/room arrangement and Leland succession remain open. | `BUS-021`; `P-027`; `E-028`, `E-137`; `S-035`, `S-153` |"
)

# Construction checkpoint and research log.
append_once(
    "evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md",
    "## 1921 follow-forward: Freeze relocation narrows the 505½ occupancy sequence",
    '''## 1921 follow-forward: Freeze relocation narrows the 505½ occupancy sequence
A follow-forward *Enterprise* search produced a visually verified March–April 1921 transition (`E-137` / `S-153`). The 18 March paper says Dr. Harvey Freeze moved from Portland to Oregon City and was locating over Harding's Drug Store. Direct scans place Freeze at **507½ Main** on 25 March and 1 April, then existing visually verified evidence places him at **505½ Main** on 8 April.

This materially tightens the sequence after A. Leland's **505½** pool-hall/sign permit of June 1920: Freeze did not begin his Oregon City practice at 505½; he first advertised at 507½ and shifted to 505½ between the 1 and 8 April issues. It still does **not** prove what happened to Leland's pool hall, whether Leland and Freeze used the same physical room, or when the surviving 505 structure was constructed. A parallel strong inference places Harding Drug Store with the 507½ office in late March, but an independent exact-507 Harding source is still needed.'''
)
append_once(
    "registers/research-log.md",
    "### 2026-08-31 — Dr. Freeze 507½→505½ transition visually verified",
    '''### 2026-08-31 — Dr. Freeze 507½→505½ transition visually verified
- Followed the June 1920 505½ pool-hall anchor forward through the 1920–1922 *Enterprise* OCR corpus, then reduced 281 broad hits to a high-signal candidate set before scan review.
- Visually verified 18 Mar 1921 p5: Dr. Harvey Freeze moved his practice from Portland to Oregon City; subhead says he was locating **over Hardings Drug Store**. No Oregon City number is printed in that article.
- Visually verified 25 Mar and 1 Apr p3 advertisements: both print **507½ Main St.**; OCR `507` on 1 Apr is false.
- Existing visual evidence places Freeze at **505½ Main** on 8 Apr, proving an advertised-address change after 1 Apr and by 8 Apr (`S-153` / `E-137`, cross-reference `S-035` / `E-028`).
- Harding at numbered 507 is retained as a strong spatial/address inference only; earlier direct 511 evidence remains valid. No Leland→Freeze succession, physical room identity, ownership, or 505 construction date is inferred.'''
)

print("Prepared S-153 / E-137 Freeze transition integration")
