#!/usr/bin/env python3
from pathlib import Path

MARKER = "Flor Kwality 1953 continuity bridge — 2026-09-06"

CAPTURE = Path("evidence/source-captures/albert-d-flor-morton-bridge-pass-2026-09-06.md")
PROFILE = Path("people/profiles/albert-d-flor-family.md")
BUSINESS = Path("businesses/kwality-cafe.md")
DIRECTORY = Path("evidence/source-captures/1953-oregon-city-vicinity-directory-lead.md")
REQUEST = Path("registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md")
MANUAL = Path("MANUAL-FOLLOWUP.md")


def append_once(path: Path, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"{path}: already updated")
        return
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def main() -> None:
    append_once(CAPTURE, f'''## September 1953 breakthrough — `Al & Marge Kwality Cafe`
<!-- {MARKER} -->

A follow-up search for the **licensed premises/trade name behind the December 1951 Albert D. Flor + Margaret Remus liquor application** produced a major intermediate bridge.

### Official September 1953 city record

The official Oregon City Commission record covering the **2 September 1953 regular meeting / 10 September 1953 adjourned regular meeting** includes **`Al & Marge Kwality Cafe`** in the City's finance/vendor list.

Official source:
https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4752017/File/document

Searchable PDF text controls:

- p. 1 text identifies **Oregon City, Oregon, September 2, 1953** and the adjournment to **September 10, 1953**;
- p. 3 text lists **`Al & Marge Kwality Cafe`** among named vendors/payees.

A required page-image screenshot was attempted for the page containing the business name, but the renderer returned a **cache miss**. Classification is therefore **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP**, not scan-certified evidence.

The record proves that an Oregon City business was styled **Al & Marge Kwality Cafe by September 1953**. It does **not** print a street address, surnames for Al/Marge, a liquor-license role, or an ownership statement.

### Independent 1953 Remus/Kwality control

The City of Oregon City's current historic-resource record for **902 5th Street** states that in **1953** the tenant there was **Fred Remus, a cook at the Kwality Cafe**:

https://www.orcity.org/2072/902-5th-Street

The linked 2002 historic inventory form gives the same statement. Classification: **OFFICIAL SECONDARY / DIRECTORY-DERIVED CONTEXT**. The inventory does not state Fred Remus's relationship to Margaret Remus and should not be used to invent one.

### Cross-source continuity assessment

Four controls now align chronologically:

1. **5 Dec. 1951 — DIRECT CITY TEXT:** `Albert D. Flor and Margaret Remus` are jointly listed among approved Oregon City liquor-license applicants. Premises/trade name absent.
2. **Sept. 1953 — DIRECT CITY TEXT:** the City finance/vendor list names **`Al & Marge Kwality Cafe`**. Address/surnames absent.
3. **1953 — OFFICIAL SECONDARY:** **Fred Remus** is identified as a **cook at the Kwality Cafe**.
4. **1957 — OFFICIAL SECONDARY:** the City's 503 Main historic-resource synthesis says **Mr. and Mrs. Albert D. Flor** managed the restaurant/cocktail bar at **503 Main**.

This is now a **STRONG CROSS-SOURCE CONTINUITY HYPOTHESIS** that `Al` in the 1953 business style may be **Albert D. Flor**, and that `Marge` may be **Margaret Remus**, with the Flor/Remus pair associated with Kwality Cafe between the 1951 liquor approval and the documented 1957 Flor management at 503.

It is **not yet direct identity proof**. The 1953 source gives first names only; the 1951 source gives full names but no business/address; the 1957 source gives Flor at 503 but does not name Margaret Remus; and Fred Remus's relationship to Margaret is unknown. Do not collapse those gaps into a proved partnership, marriage, business ownership, or 1951 503 tenancy.

### 503 address consequence

The City historic-resource record independently places **Kwality Cafe at 503 Main** in the relevant historical sequence and says the restaurant/cocktail bar under Mr./Mrs. Flor remained at that site in 1957. The September 1953 `Al & Marge Kwality Cafe` record therefore substantially narrows the search, but because that finance line itself lacks an address, preserve **September 1953 at 503** as a **strong cross-source inference**, not an exact-address primary fact, until the 1953 directory or another address-bearing record is visually recovered.

### Morton bridge consequence

Fresh public-index searches for **Al & Marge**, **Albert Flor**, **Margaret Remus**, and **Fred Remus** with Morton/eastern Lewis County/Wheel Cafe terms produced no reliable historical Morton hit. This remains a **PUBLIC-ONLINE RETRIEVAL GAP**, not negative evidence, because the target Morton Journal run and directory coverage limitations remain unchanged.

The Morton manual search should now include the distinctive business/person cluster:

- `Al & Marge` / `Al and Marge`;
- `Albert D. Flor` / `Albert Flor` / `A. D. Flor`;
- `Margaret Remus` / `Marge Remus`;
- `Fred Remus` as a lower-priority associate/employee control;
- `Kwality Cafe` as well as `Wheel Cafe`.

### Exact next document

The highest-value Oregon-side source is now the **_Oregon City & Vicinity Directory, 1953_ (T. W. Salisbury & Co.)**. Recover and visually inspect:

- alphabetical entries for **Flor, Albert / Albert D.**;
- **Remus, Margaret / Marge** and **Remus, Fred**;
- the **503 Main** street entry;
- restaurant/cafe classified listings;
- any **Kwality Cafe / Al & Marge Kwality Cafe** entry, including proprietor/manager names, phone and address.

An address-bearing 1953 directory entry or a 1951–53 OLCC/city license record naming both the Flor/Remus pair and Kwality/503 would convert the current continuity hypothesis into a direct bridge.''')

    append_once(PROFILE, f'''## 1953 `Al & Marge Kwality Cafe` continuity lead
<!-- {MARKER} -->

Official Oregon City Commission text for the **September 1953** finance report names **`Al & Marge Kwality Cafe`**. This falls between the **5 December 1951 Albert D. Flor + Margaret Remus** liquor-license approval and the City's official-secondary **1957 Mr./Mrs. Flor at 503 Main** restaurant/cocktail-bar control.

A separate City historic-resource record says **Fred Remus was a cook at the Kwality Cafe in 1953**, providing an independent Remus-surname connection to the business but not establishing Fred's relationship to Margaret.

Classification: **STRONG CROSS-SOURCE CONTINUITY HYPOTHESIS; NOT DIRECT IDENTITY PROOF**. It is plausible that `Al` = Albert D. Flor and `Marge` = Margaret Remus, but the 1953 finance line supplies no surnames/address and the 1951 liquor line supplies no business/address. Do not promote Margaret Remus to Mrs. Flor, co-owner, or 503 tenant without a direct record. The 1953 Salisbury directory is now the decisive primary-source target.''')

    append_once(BUSINESS, f'''## September 1953 — `Al & Marge Kwality Cafe`
<!-- {MARKER} -->

Official Oregon City Commission searchable text for the September 1953 finance report names **`Al & Marge Kwality Cafe`**. This is the first recovered dated city record in the current archive that combines personal first names with the **Kwality Cafe** business style in the early-1950s period.

The same research pass found that the City's 902 Fifth Street historic inventory identifies **Fred Remus as a cook at the Kwality Cafe in 1953**. Combined with the December 1951 liquor-license approval for **Albert D. Flor and Margaret Remus** and the City's 1957 secondary control for **Mr./Mrs. Albert D. Flor managing the restaurant/cocktail bar at 503 Main**, the evidence creates a strong continuity hypothesis that the 1953 `Al & Marge` style may refer to Flor and Margaret Remus.

Limits remain material: the 1953 finance line gives **no address or surnames**, the 1951 license list gives **no trade name/address**, and Fred Remus's relationship to Margaret is unknown. Preserve `Al & Marge Kwality Cafe` as a dated business-style control and do not yet treat Flor/Remus identity, ownership, or exact 503 occupancy in September 1953 as directly proved.

Official 1953 Commission PDF: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4752017/File/document  
City 902 Fifth historic-resource record: https://www.orcity.org/2072/902-5th-Street''')

    append_once(DIRECTORY, f'''## Flor / Remus / Kwality retrieval expansion
<!-- {MARKER} -->

The 1953 directory is now also the highest-value source for resolving the early-1950s **503 Main Kwality Cafe operator chain**. New official city text names **`Al & Marge Kwality Cafe`** in September 1953; a City historic-resource record separately says **Fred Remus was a cook at Kwality Cafe in 1953**; and the December 1951 city liquor list names **Albert D. Flor and Margaret Remus** jointly.

When the directory image is obtained, add these mandatory captures to the existing 505 work:

- alphabetical **Flor** entries, especially Albert / Albert D.;
- alphabetical **Remus** entries, especially Margaret/Marge and Fred;
- exact **503 Main** street-address entry and adjacent 501/505 controls;
- classified **restaurants / cafes / cocktail lounges**;
- any `Kwality Cafe`, `Al & Marge`, or variant business listing;
- proprietor/manager/spouse notation, home address, occupation and telephone number for the named people.

This is now a dual-purpose source: it can resolve both the 505 `Well's Recreation` question and the Flor/Remus → Kwality → Wheel transition at 503.''')

    append_once(REQUEST, f'''## Supplemental Oregon continuity target — 1951 Flor/Remus → 1953 `Al & Marge Kwality Cafe` → 1957 Flor at 503
<!-- {MARKER} -->

The Oregon-side license-chain request can now be made substantially more precise.

New official Oregon City Commission searchable text for **September 1953** names **`Al & Marge Kwality Cafe`** in the City's finance/vendor list. A separate City historic-resource record states that **Fred Remus was a cook at Kwality Cafe in 1953**. These controls sit between the **5 December 1951** city liquor approval for **Albert D. Flor and Margaret Remus** and the City's later official-secondary statement that **Mr. and Mrs. Albert D. Flor** managed the restaurant/cocktail bar at **503 Main in 1957**.

When requesting OLCC / predecessor licensing records or city/county license records, please specifically ask for records that can establish or reject this possible continuity:

- `Albert D. Flor` / `Albert Flor` / `A. D. Flor`;
- `Margaret Remus` / `Marge Remus`;
- `Al & Marge Kwality Cafe` / `Al and Marge Kwality Cafe`;
- `Kwality Cafe`, `503 Main Street`, Oregon City;
- years **1951–1958**, especially original applications, annual renewals, trade-name cards, premise/address cards, partner changes and ownership/license transfers.

The decisive questions are:

1. What premises/trade name was licensed to **Flor + Remus in December 1951**?
2. Do 1952–54 records identify **Albert Flor and/or Margaret Remus with Kwality Cafe / 503 Main**?
3. Who is `Al` and who is `Marge` in the **September 1953** business style?
4. Was **Fred Remus** related to or employed by the licensees beyond the directory-derived statement that he cooked at Kwality Cafe?
5. What change, if any, occurs between Flor's documented 1957 management and the **Wheel Cafe** name by 1960?

For the Morton-side requests, add **`Al & Marge` / `Al and Marge`, `Marge Remus`, `Fred Remus`, and `Kwality Cafe`** as discovery terms alongside Flor/Remus and Wheel Cafe. A fresh public-index pass did not find a Morton hit; treat that only as an access result.''')

    append_once(MANUAL, f'''### MF-052 Flor/Remus continuity breakthrough — September 1953
<!-- {MARKER} -->

The Flor candidate now has a much tighter Oregon-side chain. Official city text names **`Al & Marge Kwality Cafe`** in **September 1953**; the City's 902 Fifth historic inventory says **Fred Remus was a cook at Kwality Cafe in 1953**; the 1951 liquor list names **Albert D. Flor + Margaret Remus**; and the 503 historic-resource synthesis places **Mr./Mrs. Albert D. Flor** managing the restaurant/cocktail bar at 503 in 1957.

Classification: **STRONG CROSS-SOURCE CONTINUITY HYPOTHESIS**, not direct identity/ownership proof. The 1953 business line has no surnames/address and the 1951 license line has no premises/trade name.

Under MF-052, make the **1953 T. W. Salisbury Oregon City & Vicinity Directory** an explicit dual-purpose retrieval: capture Flor, Margaret/Marge Remus, Fred Remus, `Al & Marge Kwality Cafe`, the 503 Main street listing and restaurant/cafe classifieds. Add `Al & Marge`, `Marge Remus`, `Fred Remus`, and `Kwality Cafe` to the Morton Journal/directory/LCB search as secondary bridge terms. The fresh public-online Morton no-hit remains a retrieval gap, not negative evidence.''')

    print("Integrated September 1953 Al & Marge Kwality Cafe / Flor-Remus continuity breakthrough.")


if __name__ == "__main__":
    main()
