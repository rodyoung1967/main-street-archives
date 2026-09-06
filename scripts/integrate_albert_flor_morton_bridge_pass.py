#!/usr/bin/env python3
from pathlib import Path

MARKER = "Albert Flor Morton bridge pass — 2026-09-06"
CAPTURE = Path("evidence/source-captures/albert-d-flor-morton-bridge-pass-2026-09-06.md")
PROFILE = Path("people/profiles/albert-d-flor-family.md")
REQUEST = Path("registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md")
MANUAL = Path("MANUAL-FOLLOWUP.md")


def append_once(path: Path, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"{path}: already updated")
        return
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def main() -> None:
    if not CAPTURE.exists():
        CAPTURE.write_text(f'''# Albert D. Flor → Morton Wheel bridge pass — 6 September 2026
<!-- {MARKER} -->

## Purpose

Test a new candidate-person bridge between the known pre-Raye 503 Main restaurant/cocktail-bar operator **Albert D. Flor** and **Morton, Washington / the Morton Wheel Cafe**. The project already has official-secondary evidence associating **Mr. and Mrs. Albert D. Flor** with a restaurant/cocktail-bar operation at **503 Main, Oregon City, in 1957**. Because the project is trying to identify the person or people who operated the Oregon City Wheel before Raye LaFarlette / Raye Grisham and to test a family recollection that earlier Morton Wheel owners later became connected with the Oregon City Wheel, Flor is now a named bridge candidate rather than an anonymous pre-Raye operator.

This pass does **not** assume Flor owned the real estate, owned the business, used the Wheel trade name in 1957, or ever lived/worked in Morton.

## New Oregon City primary-text control — 5 December 1951

Searchable text from the official Oregon City Commission minutes for the **5 December 1951 regular meeting** states that the Commission approved a group of liquor-license applications and includes the joint entry:

> **Albert D. Flor and Margaret Remus**

Official source:
https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4732560/File/document

The same searchable record continues into the **11 December 1951 adjourned regular meeting**, which provides date/context control for the liquor-license list.

Classification: **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP**. The source-document endpoint timed out when opened directly in this research environment, so the underlying page image was not visually certified in this pass. The accessible text also does **not** state the licensed premises, street address, trade name, license class, or ownership relationship for Flor and Remus. Therefore this record proves only that **Albert D. Flor and Margaret Remus were named together among Oregon City liquor-license applicants approved in December 1951**. It must **not** yet be described as a 503 Main license.

This is still significant because it moves Flor's documented Oregon City liquor-business involvement back from the existing **1957 official-secondary 503 listing** to a direct city record in **1951**, creating a longer period in which license renewals, transfers, directories, and advertisements may identify the premises and trade name.

## Morton / eastern Lewis County online search

Public-indexed searches were run for **Albert D. Flor / Albert Flor / A. D. Flor** and **Margaret Remus**, alone and in restaurant/cafe/liquor/Wheel combinations, against:

- Morton, Washington;
- Lewis County / eastern Lewis County;
- Centralia and Chehalis;
- Randle, Packwood, Mossyrock and Mineral;
- Wheel Cafe / The Wheel Cafe;
- restaurant, cafe, cocktail-bar and liquor-license terminology.

### Result

**No reliable historical hit was recovered placing the Oregon City Albert D. Flor, Margaret Remus, or an explicitly linked Mrs. Albert D. Flor in Morton or eastern Lewis County. No indexed source connected Flor or Remus to the Morton Wheel Cafe.**

Classification: **PUBLIC-ONLINE NO-HIT / RETRIEVAL GAP — NOT NEGATIVE EVIDENCE**. The highest-value Morton source remains the **1945–7 August 1947 Morton Journal** run, which is not exposed as readable public issue pages in the current online environment, and Morton coverage in the 1946 Lewis County / Centralia-Chehalis directory remains unresolved. These access limits prevent a no-hit from being used as proof that Flor/Remus had no Morton connection.

## Wrong-person control

Searches also surfaced an **Albert Daniel Flor (1889–1984) of New Ulm, Minnesota**, including historical law-school/attorney records. Shared initials/name alone are insufficient to identify that man with the Oregon City liquor applicant. Keep all non-Oregon Albert Flor records separate unless a contemporary source explicitly supplies matching residence, spouse/partner, occupation, or migration evidence.

## Why Margaret Remus matters

The 1951 city record names **Margaret Remus jointly with Albert D. Flor**. She should now be searched alongside Flor in all relevant Oregon and Washington sources. A Morton or Wheel Cafe record under **Remus** could provide a bridge even if Flor himself is not indexed there, while Oregon City renewal/transfer records may clarify whether Remus was a partner, co-licensee, spouse, employee, or another business associate.

## Next evidence tests

Under existing manual item **MF-052**:

1. Add **Albert D. Flor / Albert Flor / A. D. Flor / Mrs. Albert D. Flor / Margaret Remus** to the *Morton Journal*, directory, and Washington liquor-license searches.
2. Ask Washington LCB to check those names in addition to the Wheel trade name for Morton/eastern Lewis County, especially **1944–1957**.
3. On the Oregon side, identify the **licensed premises and trade name** for the December 1951 Flor/Remus approval and trace renewals/transfers through the documented 1957 Flor-at-503 control and into the **Wheel Cafe** period by 1960.
4. Do not call Flor the pre-Raye **owner** until a business-sale, license-transfer, assumed-name, directory, deed/lease, or equivalent contemporary source establishes the role.

## Current conclusion

The Flor test produced **no Morton bridge yet**, but it did produce a meaningful earlier Oregon City control and a new named associate, **Margaret Remus**. Flor and Remus are now high-value named candidates for the restricted/manual sources that can actually resolve the Morton-to-Oregon City ownership hypothesis.
''', encoding="utf-8")
    else:
        print(f"{CAPTURE}: already exists")

    append_once(PROFILE, f'''## December 1951 liquor-license control and Morton bridge test
<!-- {MARKER} -->

Official Oregon City Commission searchable text for the **5 December 1951** regular meeting lists **Albert D. Flor and Margaret Remus** together among approved liquor-license applicants. This is a direct city-record control that moves Flor's documented Oregon City liquor-business involvement back before the existing 1957 503 Main secondary listing.

Classification: **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP**. The underlying document endpoint timed out during direct visual retrieval in this pass, and the accessible text does **not** identify the licensed premises, trade name, license class, or ownership role. Do **not** convert the 1951 approval into a 503 Main fact without a premises record.

A dedicated Morton/eastern Lewis County public-index pass found **no reliable historical Albert D. Flor, Mrs. Albert D. Flor, or Margaret Remus hit** and no connection to the Morton Wheel Cafe. This is a **retrieval gap, not negative evidence**, because the target 1945–47 *Morton Journal* issues remain outside the readable public-online route and 1946 directory coverage of Morton remains unresolved.

`Margaret Remus` is now an important associate-name control for Oregon license/renewal/transfer research and for the Morton Journal/directory/Washington liquor-license search. See `evidence/source-captures/albert-d-flor-morton-bridge-pass-2026-09-06.md`.''')

    append_once(REQUEST, f'''## Supplemental named-person bridge test — Albert D. Flor / Margaret Remus
<!-- {MARKER} -->

A new candidate-person pass should be incorporated into **Requests A–C** and the broader MF-052 search.

The project's existing official-secondary evidence places **Mr. and Mrs. Albert D. Flor** in a restaurant/cocktail-bar operation at **503 Main, Oregon City, in 1957**. Newly recovered searchable text from the official **5 December 1951 Oregon City Commission** minutes lists **Albert D. Flor and Margaret Remus** together among approved liquor-license applicants. The accessible 1951 text does **not** give their premises or trade name, so it must not yet be treated as a 503 Main license.

### Add to Washington / Morton searches

Please check these names and variants in the **1945–7 August 1947 Morton Journal**, any directory that actually covers Morton, and historical Washington liquor-license/application files:

- **Albert D. Flor**
- **Albert Flor**
- **A. D. Flor**
- **Mrs. Albert D. Flor**
- **Margaret Remus**
- OCR variants of `Flor` when practical (`Florr`, `Flore`, `Floor`) only as discovery terms, not identity matches

Search with **Wheel Cafe / The Wheel Cafe / Wheel**, restaurant/cafe/cocktail-bar terms, and owner/proprietor/manager/employee/licensee/transfer language. For Washington liquor records, extend the named-person check through approximately **1957** if the index permits, because the exact date of any hypothesized move from Morton to Oregon City is not established.

A broad public-index pass on 6 September 2026 found **no reliable Flor/Remus Morton or eastern Lewis County hit**. Treat that as an online-access result only; the principal Morton newspaper and directory coverage gaps remain.

### Add to Oregon license-chain search

Before limiting the Oregon OLCC lookup to 1958–1967, ask whether predecessor records can identify the **licensed premises, trade name, license class, renewals, partners and transfers** associated with **Albert D. Flor and Margaret Remus from December 1951 forward**. The goal is to determine whether the 1951 approval can be tied to **503 Main**, whether Flor/Remus continue there through the documented 1957 operation, and who succeeded them before/by the Wheel Cafe period.

Do **not** infer that Flor/Remus owned the 503 real estate or the Wheel business merely from liquor-license status. Preserve licensee, operator, business owner, tenant and property owner as separate roles unless contemporary evidence bridges them.''')

    append_once(MANUAL, f'''### MF-052 named-person refinement — Albert D. Flor / Margaret Remus
<!-- {MARKER} -->

A candidate-person bridge pass tested the known **1957 Mr./Mrs. Albert D. Flor restaurant/cocktail-bar operation at 503 Main** against Morton/eastern Lewis County. Public-index searching recovered **no reliable Flor/Remus Morton or Morton Wheel connection**, but official Oregon City Commission searchable text produced an earlier control: on **5 December 1951**, **Albert D. Flor and Margaret Remus** were listed together among approved liquor-license applicants.

The 1951 text does **not** state the premises or trade name and the source page could not be visually rendered in the current environment, so classify it **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP** and do not call it a 503 Main license yet.

Under **MF-052**, add **Albert D. Flor / Albert Flor / A. D. Flor / Mrs. Albert D. Flor / Margaret Remus** to the Morton Journal, verified-coverage directory, and Washington liquor-license searches. On the Oregon side, extend the license-chain test backward to the **December 1951 Flor/Remus approval** and identify its premises/trade name, then trace renewals/transfers through the documented 1957 Flor-at-503 control into the Wheel Cafe period. The public-online Morton no-hit remains a retrieval gap, not negative evidence.''')

    print("Integrated Albert D. Flor / Margaret Remus Morton bridge pass into MF-052.")


if __name__ == "__main__":
    main()
