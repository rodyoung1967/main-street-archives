# 1917 Oregon City Enterprise — March 2, 9, 16, 23 and 30 visual review

<!-- 1917 Enterprise March visual review and page-5 gap — 2026-09-06 -->

Status: **VISUALLY VERIFIED — 39 genuine intended-date pages across five March issue dates; 2/9/23/30 March are complete, 16 March is 7/8 genuine with true page 5 a RETRIEVAL GAP. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `S-272`; evidence `E-246`; manual callout `MF-049`.

Preserved March originals: `newspapers/oregon-city-enterprise/1917-march/`  
Original retrieval commit: `e65bd35360e6c6cea20b88184671407841ba73b5`  
Original manifest: `newspapers/oregon-city-enterprise/1917-march/manifest.json`  
Recovery audit: `newspapers/oregon-city-enterprise/1917-march/recovery-march16-page5/recovery-manifest.json`  
Recovery-audit commit: `4d4853ddb0cd81ceefe147a335dd83e940d93cdd`  
Annual issue/page inventory: `newspapers/oregon-city-enterprise/1917-issue-inventory/README.md`

## Scope and scan-first method

The archive exposes five Friday issue buckets in March 1917, eight PDF slots apiece. All **40 archive-supplied page files** were rendered and visually inspected. Printed dates were then audited page by page rather than trusting the archive issue metadata.

That audit discovered a material archive association error: the file exposed as **16 March, sequence 5 / page 5** visibly prints **“OREGON CITY ENTERPRISE, FRIDAY, MARCH 23, 1917”** and **“Page 5.”** It therefore cannot count as the true 16 March page 5.

The misassociated scan is also **not the same file** as the normal 23 March sequence-5 scan. Both visibly print 23 March and Page 5, but they are distinct scans/content variants. The 16 March slot is therefore classified as a misassociated 23 March page-5 variant rather than silently deduplicated or reassigned as the missing 16 March page.

| Archive issue bucket | Exposed slots | Genuine matching-date pages | Status |
| --- | ---: | ---: | --- |
| 2 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 9 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 16 March 1917 | 8 | 7 | **PARTIAL 7/8 — true page 5 RETRIEVAL GAP** |
| 23 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8**, plus the separate misassociated 23 March Page-5 variant in the 16 March bucket |
| 30 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |

Thus **40/40 exposed archive slots were visually inspected**, but only **39 are genuine intended-date March issue pages**. With January-February's 66 genuine pages, Enterprise progress becomes **105 genuine intended-date pages visually verified**. **310 later exposed April-December pages remain visually unreviewed**, and the true 16 March page 5 remains a separate retrieval gap. Do not convert the bad slot into 40/40 genuine March coverage.

## Recovery attempts for true 16 March page 5

The dedicated recovery audit tested independent derivatives and alternate routes before classifying the gap:

- Oregon Historic Newspapers PDF, JP2, OCR text, OCR XML, RDF and page HTML for the 16 March sequence-5 object all resolve to/described the same underlying scan that visibly prints **23 March**.
- The issue metadata exposes exactly eight source-image objects for the 16 March edition; the bad object occupies the fifth slot. No ninth source image is exposed.
- Alternate edition paths `ed-2` through `ed-4` were probed and did not expose a replacement page.
- Library of Congress / Chronicling America routes and LOC JSON searches did not expose a second usable copy of the missing page.
- The normal 23 March page 5 was retrieved separately and is a different scan from the misassociated 23 March variant.

Reasonable online recovery has therefore been attempted. The true **16 March 1917 Enterprise page 5** is retained as **RETRIEVAL GAP / MANUAL CALLOUT `MF-049`**, never as negative evidence.

## Dated context and identity discipline

Across the genuine March pages, the scan/text review found local context including Holman, Jones Drug and William Andresen references, but no new exact target-street-number observation for those references. Courier evidence already provides stronger dated exact-address controls where applicable, so the unnumbered Enterprise references do not create a new business-address chronology entry.

The misassociated 23 March Page-5 variant contains a local report that animals were sold to **Farr Brothers**. That wording belongs to the **23 March** scan variant, not 16 March. It supplies no 505 Main address and does not bridge the separate Seventh Street Farr Brothers grocery/meat business to **Edwin F. Farr / Alice Farr / Farr's Pool Hall at 505 Main**. Existing no-merge control remains in `evidence/source-captures/1922-farr-brothers-identity-clarification-2026-09-03.md`.

## Exact target-address result

Across the **39 genuine intended-date March pages actually recovered and visually reviewed**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established and no new exact 427 Main occupant was established.

This statement deliberately excludes the unrecovered true 16 March page 5. The missing page means the March source class cannot be used to claim complete no-hit coverage for 16 March. Nothing here is evidence that a target storefront was vacant, unused, demolished, unnumbered or absent.

## Cross-record propagation audit

The following current authoritative entity/chronology records were reviewed against this batch:

- `buildings/503-main.md`
- `buildings/505-main.md`
- `timelines/503-main.md`
- `timelines/505-main.md`
- `businesses/farrs-pool-hall.md`
- `people/profiles/edwin-f-farr.md`
- `people/profiles/alice-farr.md`
- `evidence/open-questions.md`
- `evidence/research-leads.md`
- `registers/business-timeline.md`
- `timeline.md`

**Propagation decision:** the batch changes annual coverage, retrieval-gap, and source/evidence records, but establishes **no new 503/505 occupant, business operation, property ownership, building event, or Edwin/Alice Farr identity bridge**. Therefore no fabricated 1917 event is added to the 503/505 building/business/person timelines. The open 1917 occupancy question and research lead are updated with the new page gap and coverage state instead.

## Effect on 1917 status

1917 remains **IN PROGRESS**. Enterprise now has **105 genuine intended-date pages visually verified**, one known March 16 page-5 retrieval gap, and **310 later exposed April-December pages** still requiring page-by-page visual review. The Friday-pattern inventory still requires title-calendar reconciliation. Existing 1917 blockers also remain: the true 13 December *Courier* page 21 retrieval gap, the Sohns & Woodbeck 1916–1917 Oregon City directory section, and other online-source-class closeout work.
