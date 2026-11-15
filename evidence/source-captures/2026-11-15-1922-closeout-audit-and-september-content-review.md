# 1922 closeout audit, live inventory, and September content review

Reviewed: **15 November 2026**. Workstream: **ANNUAL-1922**. Status: **IN PROGRESS**.
Base: current main `c697c8d16510a2fa0db2772fd01a5cc8d15cfd77`; fetched before interpretation/writes. AGENTS.md, RESEARCH-STANDARD.md, MANUAL-FOLLOWUP.md, the 13 September handoff, monthly visual records, 15 November reconciliation/discovery records, and relevant entity/register/database records were reviewed.

## What must be completed first

The principal online blocker is now **content-level visual review of the September–December pages**, not downloading the corpus again. The September–December 14 September captures explicitly describe gross image-integrity/contact-sheet checks. Preserve that work, but do not promote it to exhaustive reading of all articles, ads and notices. Later OCR screening and selected article checks also do not supply that missing whole-page review.

January–August captures document content review of **615 page images** (subject to source defects). September–December contains **313 pages**. This session newly screened **13 complete page images** in that latter group; **300 remain in the conservative whole-page content-review queue**, including pages with prior item-specific visual checks. These numbers track work coverage, not 628 perfectly legible/certified source pages. Source damage remains separate.

Monthly manifests now distinguish those scopes: July–August are synchronized to existing content-review records; September–December retain visual integrity credit with explicit per-page exhaustive-content states. No old review was deleted, and no unviewed page was granted credit.

## Live title, calendar and issue inventory — completed in this pass

Direct HTTPS retrieval of both original 1922 archive calendars succeeded. Each calendar was compared to all monthly manifests. Every one of the **104 issue JSON records** was then fetched and its page-array count compared to its committed issue count.

| Title | LCCN | Live issues | Live page slots | Date/count differences from repository |
| --- | --- | ---: | ---: | --- |
| The Banner-Courier | sn00063699 | 52 | 512 | None |
| Oregon City Enterprise, weekly | sn00063700 | 52 | 416 | None |
| Total | — | 104 | 928 | None |

Raw calendars and issue JSON responses are retained under each title's `1922-inventory-recheck-2026-11-15/`. This is inventory verification, not visual content credit for 928 pages.

Official digitization/title controls checked online:
- Oregon City Public Library: https://www.orcity.org/475/Digitizing-Historic-Oregon-City-Newspape — weekly Enterprise through 29 Dec. 1922; Banner-Courier 5 Jan.–28 Dec. 1922; Morning Enterprise digital run only 1911–1913.
- ODNP: https://odnp.wordpress.com/2013/11/21/newspaper-image-quality-and-oregon-city-history/ — 1922 Banner-Courier and 1921–1922 Enterprise were re-filmed.
- UO title history: https://oregonnews.uoregon.edu/history/oregoncityenterprise — distinguishes daily Morning Enterprise from the weekly. The daily must remain a distinct manual source universe; do not silently omit it because it is not in the 928-page corpus.

## June 15/16 date discrepancy — original source now inspected

Visually inspected original masthead/header regions of **all eight** archive-key `1922-06-15` Enterprise pages and neighboring June 9 and June 23 front-page mastheads. These header inspections do not add ten whole-page content reviews.

- June 9 prints **Friday, June 9, 1922**, fifty-sixth year **No. 23**.
- The intervening issue prints **Friday, June 15, 1922**; front page **No. 24**. All eight running headers repeat June 15.
- June 23 prints **Friday, June 23, 1922**, **No. 25**.
- Calendar calculation: June 15, 1922 was Thursday; June 16 was Friday.
- Direct archive `1922-06-15/ed-1.json` returned HTTP 200 with eight pages. The analogous June 16 JSON returned HTTP 404. The refreshed calendar lists June 15, not June 16.

**DIRECT:** the inconsistency exists on the printed scans, not only in archive metadata. **STRONG CROSS-SOURCE INFERENCE:** No. 24 fills the weekly interval between Nos. 23 and 25; the inventory gives no evidence of a second missing weekly issue. **PROBABLE:** the day-of-month is a typesetting error for Friday June 16. Exact actual publication day still needs an independent control; preserve literal print date and URL/file key without silently renaming/re-dating. `MF-075` records that final date check.

The old fetching script's comment calling June 15 a Wednesday is also corrected; it was Thursday. This is a documentation correction, not a new issue or a schedule claim.

## Damaged-source recovery — alternate JP2 derivatives inspected

Directly retrieved and visually inspected alternate original-archive JP2 derivatives for these five pages, comparing the first four with the retained PDF renders. Requests succeeded, superseding the earlier environment-specific access failures; they did **not** recover lost text.

| Source/date | Sequence | Visual outcome |
| --- | ---: | --- |
| Enterprise, 5 May | 1 | Same large lower-right missing/black area as retained PDF |
| Enterprise, 5 May | 2 | Same large lower-left missing/black area as retained PDF |
| Banner-Courier, 9 November | 7 | Same large lower-right missing/black area as retained PDF |
| Banner-Courier, 9 November | 8 | Same large lower-left missing/black area as retained PDF |
| Banner-Courier, 22 June | 9 | Supplement with torn/lost upper title edge; article bodies appear present below it, but no claim that all lost edge content is recovered |

URLs are the issue/sequence paths in existing manifests with `.jp2` extension. Byte counts and SHA-256 are retained in `newspapers/1922-recovery-2026-11-15/manifest.json`. JP2 and PDF are derivatives of the same underlying source, not independent intact copies. Duplicate-content JP2 binaries were not added: retained PDFs preserve the same damage; reproducible alternate-route URLs/hashes are recorded. No steward-supplied photograph was excluded.

Reasonable PDF/JP2 and public alternate-holding discovery now support carrying these exact lost regions as **RETRIEVAL GAP / MANUAL CALLOUT MF-074**. Ask Oregon City Public Library/UO to compare original or older/alternate microfilm if authorized later. No request sent. **December damage is still ONLINE-FIRST**: exact sequences/regions and alternative-image comparisons remain to be logged, rather than moving an unattempted recovery task to manual status.

## New full-page content screens — 13 pages

Original retained PDFs were rendered individually with PyMuPDF at 129.6 dpi, displayed and visually inspected for relevant article/ad/notice content, not merely gross integrity. OCR served only as prior discovery. Scope: 501/503/505/505½/507 and useful 500-block anchors; Fifth/Main; named merchants, owners, contractors, transactions, licensing, moves, fire, demolition, rebuilding and completion notices.

| Publication/date | Pages/sequences | Outcome and controls |
| --- | --- | --- |
| Banner-Courier, 7 Sep. | 1–9, all 9 pages | Full issue content screen, including the smaller ninth-page supplement. No exact 503/505 rebuilding/occupancy/completion notice identified. Specific controls below. |
| Banner-Courier, 14 Sep. | 9 | Entire page reviewed; merchant list directly repeats Leland and Little, Billiards, and separately McAnulty and Barry, Cigars, Restaurant. Neither entry gives street number. Milwaukie assessment/sale notices are not target Block 4 title evidence. |
| Banner-Courier, 28 Sep. | 4 | Entire page reviewed; same separately listed firms without addresses. Separate Portland Overtire Co. advertisement gives 209 5th St.; do not attach its address to a neighboring ad. |
| Enterprise, 22 Sep. | 5 | Entire page reviewed. “New Building Occupied” is a subhead within the Bank of Commerce article, not a Gates/503/505 occupancy notice. Other historic snippets explicitly reproduce 1892/1868 items and are not 1922 events. |
| Enterprise, 29 Sep. | 5 | Entire page reviewed. The Fifth/Main arrests occur in a light truck with blackberry moonshine; intersection evidence only, not a building/tavern/operator identification. Abernethy Grange replacement hall and general jaywalking proposal do not establish target-frontage construction. |

### 7 September issue, page-level controls

1. Page 1: September bank-building fire; upper-floor offices, water damage, architect/rebuilding estimates. It is the **Bank of Oregon City** fire, not the July Fifth/Main fire or Gates project. No exact target number inferred. Several office relocations concern the Andresen Building.
2. Page 2: one ruled ad explicitly gives **419 MAIN STREET**, **The New Location Of Miller's Shoe Store**, and signature **GILBERT MILLER**. Same ad describes installing shoe-repair machinery after the fire and liquidating H. S. Goldman's second-hand goods. This directly bridges person + trade name + dated address (`E-358` / `S-392`).
3. Page 3: bank advertisement says fire confined to upper floor and vault/safe undamaged; separate community columns, not target replacement construction.
4. Page 4: Dr. Freeze advertises **207–8 Masonic Bldg.**; First National Bank **512 Main**; no target-503/505 completion notice identified. Freeze corroborates an existing post-move location, not a new move date.
5. Page 5: S. F. Scripture advertises **108 Fifth St., between Main and Water**. Repeated dated advertising control, not proof that the July fire did/did not affect a particular wall or that a new building was completed.
6. Page 6: legal notices/assessments explicitly concern Milwaukie; professional cards and out-of-target address controls. No target property transfer identified.
7. Page 7: regional community material and city merchant advertisements; no numbered target rebuilding notice identified. Adjacency between advertisements is not shared premises.
8. Page 8: classified gives Miller's Shoe Store **419 Main** and liquidation of second-hand goods, independently corroborating p.2. Other sale/rent ads concern farms, goods and out-of-target premises; no target-frontage property transaction identified.
9. Page 9: smaller **Banner-Courier Supplement**, Canby/Jennings Lodge news. A Louis Barry hunting-trip mention supplies no firm/occupation/address bridge to McAnulty & Barry; do not merge by surname.

## Cross-record propagation audit

- `E-126` / `S-141`, BUS-077, business index/YAML and T-035/timeline now include September 14/28 billiards listings. No street number or partner identity was supplied, so P-089/P-090/P-091 identities remain unchanged.
- `E-358` / `S-392` register the signed September 7 Miller advertisement; BUS-071, P-046 and their indexes/profile/YAML, main timeline, business timeline and crosswalk are synchronized. The earlier **209 Fifth** assertion was still present in several authoritative records; it is now explicitly superseded there, with the adjacent-ad explanation preserved.
- Main 503/505 building records, building YAML and address assignments were reviewed for effects: no new construction, owner, tenant, pre-fire number or physical-building identity is proved by this batch, so no building-event or occupancy row is invented.
- Open questions and research leads retain unresolved pre-fire premises and pool-hall succession. McAnulty & Barry's exact 1922 premises and full identity remain unresolved; this batch upgrades the two source-specific lists, not a 505 assignment.
- No new media object/IMG ID: the actual original pages already exist under newspapers; temporary renders are viewing derivatives. No new map or person introduced.
- Source silence is coverage only. **Absence of evidence has not been treated as evidence of absence.**

## Validation / remaining integration work

The startup validator crashed on existing BUS-109 YAML indentation. Correcting only that indentation allowed execution and exposed **46 pre-existing errors**, principally missing earlier source/evidence YAML mirrors, ambiguous institution photo numbers parsed as person IDs, required evidence fields and one existing person-name mismatch. They predate this batch. The batch's new E-358/S-392 are mirrored and checked; the full archive validator remains failed on that baseline backlog. Do not represent it as passed. The numbered completion checklist retains this integration task.

## Resume

Read `registers/1922-online-completion-checklist.md`. The earliest September page still pending in both-paper chronological order is **Enterprise, 1 September, sequence 1**. Next Banner-Courier after the completed September 7 issue is **14 September sequence 1** (page 9 already done). Later partial pages must be skipped only with explicit ledger credit. Keep 1922 **IN PROGRESS** until the content queue, remaining online classes, precise manual list and integration are finished.
