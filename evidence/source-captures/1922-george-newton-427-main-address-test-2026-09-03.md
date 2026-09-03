# George Newton / Quality Restaurant address test

**Integrated 3 September 2026.** Research was initially held uncommitted at the steward's request; the subsequent instruction “commit new data and push” authorizes this integration. New primary claims are `E-179`–`E-182`; Newton → 427 remains **PROBABLE / WORKING HYPOTHESIS**. 1922 remains **IN PROGRESS**.

Research baseline: `2069df3c49211442a66aa00dd227a80cee489e13`. Integration fast-forwarded to current `main` at `34f6a4b`; no historical-file differences in the intervening cleanup commits. Current policies read and baseline archive validation passed. No earlier commit was restored.

## Original scans visually inspected

1. Morning Oregonian, 17 August 1922, printed p. 4 / image 4: https://oregonnews.uoregon.edu/lccn/sn83025138/1922-08-17/ed-1/seq-4/
   - Actual PDF retrieved and rendered; masthead and article inspected.
   - Article: “Firemen Are Dinner Guests.” Oregon City dateline 16 August.
   - Directly identifies George Newton as proprietor of the Quality restaurant and says he entertained the fire department at his business in gratitude for saving his restaurant from destruction during the recent Fifth Street fire.
   - “Last evening” relative to the 16 August dateline indicates the dinner was 15 August 1922, distinct from the 17 August publication date.
   - No street number or phone appears. Does not explicitly date the recent fire; association with the documented 18 July fire is contextual.
2. Banner-Courier, 8 June 1922, printed Page Ten / image 10: https://oregonnews.uoregon.edu/lccn/sn00063699/1922-06-08/ed-1/seq-10/
   - Actual PDF retrieved and rendered; masthead and complete advertisement inspected.
   - Direct advertisement for Quality Restaurant at 427 Main St., phone 517.
   - No proprietor appears in that advertisement.
   - Same-page merchant list separately names Fifth Street Restaurant and Quality Restaurant. A. D. Wheeler and Co. is a separate comma-delimited merchant, not the proprietor of Fifth Street Restaurant.
3. Banner-Courier, 17 August 1922, printed Page Two / image 2: https://oregonnews.uoregon.edu/lccn/sn00063699/1922-08-17/ed-1/seq-2/
   - Actual PDF retrieved and rendered; masthead and business roster inspected.
   - Directly lists QUALITY CAFE, but supplies neither proprietor nor address for it.
   - Roster adjacency is not geographic adjacency and does not establish that Cafe and Restaurant are the same firm.

The five original PDFs are retained at the canonical paths in the provenance table below. Rendering crops were inspection aids and are reproducible from those PDFs; no separate raster is committed. Review was targeted to relevant items, not certified full-page reading of every column.

## Limits of the initial three-source comparison

These three sources do not directly put Newton at 427 Main. Their name/place/date compatibility makes that a working hypothesis, but the two missing links are proprietor/address identity and continued occupancy from June to the fire/dinner date. No 503 occupancy, Quality-to-Kwality continuity, property ownership, or surviving-building identity follows from this evidence.

## Additional original scans visually verified

4. Banner-Courier, 17 August 1922, printed Page Eight / image 8: https://oregonnews.uoregon.edu/lccn/sn00063699/1922-08-17/ed-1/seq-8/
   - Article heading: FIREMEN HONORED WITH BANQUET AT THE “QUALITY”. Full article inspected on rendered scan.
   - Directly names George Newton as proprietor. Describes the fire that destroyed Oregon City Laundry and threatened his restaurant “across the way.” This is new relative-location evidence, not an exact address.
   - Banquet took place Tuesday evening, consistent with 15 August and the Oregonian's dateline.
   - The article also reports a silver-set presentation for John Fuson (later in the same article, Frison) on marriage to Ariel Newton. No kinship between Ariel and George is stated; do not infer one.
   - No numbered street address, phone, property ownership, or 503 reference occurs.
5. Oregon City Enterprise, 18 August 1922, printed p. 3 / image 3: https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-3/
   - Article heading: FIREMEN ARE FETED BY LOCAL RESTAURANT MAN. Masthead and relevant article visually inspected.
   - Directly names George Newton as Quality restaurant proprietor and says the fire department saved the restaurant during the recent Fifth Street fire. Banquet Tuesday evening at his business.
   - Names the newly married assistant chief John Frison and Ariel Newton. Does not connect Ariel to George by kinship.
   - No numbered street address or phone. Its opening closely parallels the Oregonian account; do not count those two as independent witnesses solely because they appear in different papers.

## Map compatibility check

The existing original May 1925 Sanborn Sheet 6 was visually inspected in the Fifth/Main area. It maps 427 at the corner south of Fifth, opposite the 501 corner; the laundry is north of Fifth and west of the Main frontage. This is geographically compatible with a 427 business being across Fifth from the laundry. It does not establish Newton's 1922 location or prove unchanged 1922/1925 building geometry. The 1925 map marks the 427 corner as clothing/gentlemen's furnishings, not a named Quality restaurant; do not claim Quality still occupied it in 1925.

## Completed bounded discovery

Bounded June–August 1922 local newspaper pass: **237 distinct OCR/text pages from 27 issues**, 14 Banner-Courier and 13 Enterprise. These are OCR-screening counts, not visual-review counts. Actual issue-page links supplied the page inventories. All 237 page texts retrieved successfully. Initial 31 August timeout was recovered; the apparently missing 16 June Enterprise issue was corrected using the existing repository inventory to the archive's **15 June** issue and all eight pages retrieved. No remaining retrieval gap in this selected page set. This is not an annual completeness review. Public archive search routes returned 403; known public issue and scan URLs were retrievable. Web search yielded no useful identity bridge.

Search terms included Newton, Geo./George context, Quality/Kwality Restaurant/Cafe, 427 Main and phone 517, with a second local pass for split names, dehyphenation, firemen, dinner and banquet. 26 pages matched the main discovery expressions. Results are preserved in `1922-newton-june-august-discovery.json`; all 237 OCR snapshots are retained under their publications in the raw-source files listed below. The discovery counts overlap previously reviewed issues and are not additive to annual visual coverage.

- Repeated exact-address ad leads: Banner-Courier 1 June p. 8; 8 June p. 10 (visually verified); 15 June p. 8; 22 June p. 7. Repeats outside the 8 June scan remain OCR/TEXT ONLY.
- Cafe roster leads: Banner-Courier 10 August p. 8; 17 August p. 2 (visually verified); 24 August p. 7; 31 August p. 7. No proprietor or address in those recovered roster texts.
- Enterprise 11 August p. 2 names Edith Caldwell taking a position at Quality Restaurant in Oregon City: OCR/TEXT ONLY, no proprietor or address. Do not attach her to Newton without an identity bridge.
- Enterprise 14 July p. 7 mentions Mrs. George Newton, two children and her sister Genevieve Steen going to Long Beach: OCR/TEXT ONLY. No restaurant or address identifier; possible family-research lead only, no identity merger.
- Other Newton hits concern different named people, places, county payments, or Isaac Newton, and were not promoted.
- Incidental OCR-only lead: Banner-Courier **24 August 1922 p. 10** contains Miller's Shoe Store at **419 Main** in classified text. This may move that business-style/address anchor earlier than the previously mentioned October ad, but requires the actual scan and must not automatically identify Gilbert Miller. URL: https://oregonnews.uoregon.edu/lccn/sn00063699/1922-08-24/ed-1/seq-10/

## Bounded result and next step

**George Newton → 427 Main: PROBABLE / WORKING HYPOTHESIS; no direct proprietor/address source recovered.** The known June Quality Restaurant advertisement and the newly verified across-the-way-from-laundry wording favor 427. A move between June and August, a different similarly named business, and ambiguity in the relative-location wording are not fully excluded. Therefore do not promote to DOCUMENTED / DIRECT or assign the saved business to 503. The finding is insufficient to choose Gates Model A or B; it reduces the value of the unproved Newton-at-503 theory.

Most useful final identity test: the 1921–1922 Polk Oregon City alphabetical and restaurant listings, telephone/business listing for **517**, or restaurant-license records naming Newton and a street number. Exact directory routes and access boundaries already exist in the repository's `1921-1922-polk-gazetteer-directory-retrieval-lead.md`; no institutional request sent. For the physical-rebuild question, proceed to the fire-adjacent pool hall or Schieremann address rather than use Newton as a 503 anchor.

Integration retains the five original PDFs, all recovered OCR snapshots, the complete per-page discovery audit, stable entities and claim-level records. The historical identity question remains open; no existing ID is renumbered and no annual completion status is upgraded.


## Canonical provenance and ID mapping

| Source | Media | Claim | Original PDF | SHA-256 |
| --- | --- | --- | --- | --- |
| `S-141` | `IMG-0727` | `E-179` | `newspapers/banner-courier/1922-06-08-page-10-quality-restaurant-427-main.pdf` | `66bb4b5b6fb0c6d72a6c7cee41e21194e70f53bd6684c55c47773b5b4a7d06bf` |
| `S-141` | `IMG-0728` | `E-181` | `newspapers/banner-courier/1922-08-17-page-2-quality-cafe-roster.pdf` | `1a7dd10757bbb0b0534f5f0e3bd3ba51355d63248a10872b2fe4febabbeb0550` |
| `S-200` | `IMG-0729` | `E-180` | `newspapers/oregonian/1922-08-17-page-4-newton-quality-firemen-dinner.pdf` | `4ea60d3679b88edd1c24896a4a521e62370fd21fdd3f10d6a65375b3b9819f74` |
| `S-201` | `IMG-0730` | `E-180` | `newspapers/banner-courier/1922-08-17-page-8-newton-quality-across-laundry.pdf` | `12e83eb2f00e5213f791670920797cf50aefa1c1a17d0ec926916aab219857f2` |
| `S-202` | `IMG-0731` | `E-180` | `newspapers/oregon-city-enterprise/1922-08-18-page-3-newton-quality-firemen-banquet.pdf` | `a668b95e9ba4ce47f8fcec362fa2037a2aa6dbe68435d07c903071378d0a2b63` |

Two page URLs already belong to `S-141`; that source set is extended, not duplicated. No exact duplicate of the five PDFs was found among existing newspaper PDFs.

Raw OCR snapshots (lookup by `page_url`):
- `newspapers/banner-courier/ocr/1922-june-august-newton-address-test.json`
- `newspapers/oregon-city-enterprise/ocr/1922-june-august-newton-address-test.json`

Discovery inventory: `evidence/source-captures/1922-newton-june-august-discovery.json`. Source IDs `S-200`–`S-202` identify the three newly registered banquet pages. Business IDs `BUS-087`–`BUS-089` separate attestations without asserting three distinct firms. `P-106` is directly tied only to `BUS-088`; `B-016` directly to `BUS-087`. No machine-readable direct-occupancy link puts Newton at 427 or 503.

## Manual / restricted-source callouts for the remaining identity link

1. **Polk 1921–1922 directory:** inspect Oregon City alphabetical and restaurant listings for Newton/Quality/427 Main. Existing FamilySearch Parts 1–2 and physical holdings at Spokane Public Library and Stillaguamish Valley Genealogical Society are documented in `1921-1922-polk-gazetteer-directory-retrieval-lead.md`. Readable directory pages were not available in prior project work; the current bounded newspaper test does not resolve this access boundary. No request sent.
2. **Telephone directory / restaurant-license records:** ask Oregon City Library/Recorder to identify surviving 1921–1923 phone-517 listings or restaurant-license entries naming Newton and the exact premises; present custody and survival need confirmation. No such underlying record was retrieved. Check move/sale dates to bridge June to August. No request sent.

No absence of a matching notice was treated as proof of no move, no second business, vacancy, closure or building survival.
