# 1912 exhaustive online audit — continued Courier coverage / visual-access checkpoint

Date: 8 September 2026
Status: **IN PROGRESS — COVERAGE / VISUAL-REVIEW CHECKPOINT**

Purpose: continue the current-standard 1912 online audit without duplicating the substantial claim-level research already integrated into `main`.

## Synchronization

Current authoritative `main` at the start of this continuation was `97d1de9893cc10f83e8dbcfdeda06d3acc5d3a2b`. The active annual-audit branch is `research/1912-online-audit`. The obsolete `research/1912-main-street` branch must not be recreated from an older SHA.

Current `main` already contains the principal 1912 findings, including Palace Saloon / Joe Wilson at **501 Main** (`E-104` / `S-118`), Smith pool-room/pool-hall evidence at **503 Main** (`E-089`), G. H. Young at **507 Main**, Brightbill at **509 Main**, Harding at **511 Main** (`E-092`), Main Street demolition/rebuilding context (`E-090`), Gambrinus at Sixth/Main (`E-091`), and Schrader's Main Street bakery sale (`E-093`). This checkpoint changes coverage state only.

## Courier issue-inventory progress

Two dates that remained unresolved in the earlier issue ledger are now positively confirmed online:

- **2 August 1912** — Oregon City Courier issue exists online. Indexed pages include at least images/pages 3, 4, 5 and 6, and the surviving page text is dated Friday, 2 August 1912. The full issue page count still requires a page-header/landing-page control before final certification.
- **27 December 1912** — Oregon City Courier issue exists online. Page 7's live HTML page explicitly reports **1–8 of 8**, establishing an eight-image issue.

December 13 and December 20 had already surfaced image 8; December 20 image/page 8 is directly indexed. The remaining Courier inventory task is to reconcile every issue to an explicit issue/page count rather than rely on expected Friday publication alone.

## Native-PDF visual route re-confirmed

The working route documented in `1912-native-pdf-visual-route-2026-09-08.md` was independently re-confirmed in this continuation on **5 January 1912, page 6**:

1. open the live Historic Oregon Newspapers HTML page;
2. follow the page's native PDF link;
3. verify an actual one-page `application/pdf` object;
4. render the PDF as a scan image;
5. visually inspect the page.

The actual scan was viewed again. It visibly confirms the already-integrated address grid, including:

- **H. N. Smith — 503 Main Street**;
- **G. H. Young — 507 Main Street**;
- **H. P. Brightbill — 509 Main St.**;
- **Geo. A. Harding — 511 Main St.**;
- Chicago Store — Main St. just below Post Office;
- M. E. Dunn — near Post Office;
- J. Tolpolar — opposite Post Office;
- Clems Chop House — Fifth & Main;
- Price Bros. — Sixth & Main.

This again confirms that OCR errors `603`, `609`, and truncated `51` must not be propagated as address readings.

## Page-dependent PDF failure state

The native-PDF route is not uniformly retrievable in the current web cache. In this continuation:

- 5 Jan p6 native PDF opened successfully and was visually inspected;
- 5 Jan pp1–2 live HTML pages opened, but repeated native-PDF retrieval attempts returned cache misses;
- several neighboring 5 Jan HTML pages themselves intermittently returned cache misses.

These failures are **RETRIEVAL GAPS in the current interface**, not visual-review credit and not negative historical evidence. Continue retrying reasonable native-PDF/alternate derivative routes during the online pass. Persistent failures may be moved to a precise manual callout only after reasonable online recovery attempts, consistent with `RESEARCH-STANDARD.md`.

## Important methodological point

A live HTML/OCR page is useful for issue inventory and discovery, but does not satisfy visual review. Only actual scans earn `VISUALLY VERIFIED` status. The project must not use the presence of readable OCR to claim page-by-page review.

## Next exact actions

1. Finish explicit Courier page-count reconciliation for all 52 1912 Friday issues.
2. Continue Courier visual review issue-by-issue using the native-PDF route wherever the PDF object renders; credit prior visual pages rather than duplicate them.
3. Record each persistent non-rendering page/range as a retrieval gap with attempted routes.
4. Build/finish the actual 1912 Morning Enterprise issue/date/page-count ledger and visual/retrieval states.
5. Build/finish the 1912 Oregon City Enterprise weekly ledger and visual/retrieval states.
6. Audit other online source classes required by `RESEARCH-STANDARD.md` before year closeout.
7. Create the numbered 1912 manual-callout list only after online-recovery attempts are exhausted for the remaining gaps.
8. Keep `1912 = IN PROGRESS` until every ONLINE COMPLETE requirement is met or precisely routed as allowed by the standard.
