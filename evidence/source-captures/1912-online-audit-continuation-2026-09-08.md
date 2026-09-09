# 1912 exhaustive online audit — continuation checkpoint, 8 September 2026

Status: **IN PROGRESS — COVERAGE / ACCESS CHECKPOINT**

Purpose: continue the 1912 exhaustive online audit under the current `RESEARCH-STANDARD.md` without regressing newer parallel work on `main`.

## Synchronization and policy check

- Current `main` checked at `97d1de9893cc10f83e8dbcfdeda06d3acc5d3a2b` before this continuation.
- Active branch: `research/1912-online-audit`.
- Re-read current `AGENTS.md` and `RESEARCH-STANDARD.md` before continuing.
- Current canonical `registers/year-status.md` keeps **1912 = IN PROGRESS**.
- The former `research/1912-main-street` branch is not recreated. Current `main` already contains the substantial claim-level 1912 integration from that earlier work and later session reconciliation.

## Important current-main correction carried into this audit

The earlier targeted capture once said no exact 1912 occupant had been recovered for 501 Main. Current `main` has since superseded that research-status statement:

- the complete 19 March 1912 *Morning Enterprise* issue was visually reviewed;
- page 2 directly identifies **Joe Wilson's Palace Saloon at 501 Main Street** in a liquor-license application;
- this is preserved under the existing March 19 visual-review integration (`S-118`, `E-104`).

Therefore this audit treats **501 Main as positively occupied in 1912** and does not repeat the superseded no-hit status.

## Required local newspaper titles

Current title metadata confirms the three local Oregon City titles that must be covered for 1912:

1. **Oregon City Courier** — LCCN `sn00063698`, weekly Friday title.
2. **Morning Enterprise** — LCCN `sn00063701`, frequency listed by Historic Oregon Newspapers as **Daily (except Mon.)**.
3. **Oregon City Enterprise** — LCCN `sn00063700`, weekly title.

Title pages:

- https://oregonnews.uoregon.edu/lccn/sn00063698/
- https://oregonnews.uoregon.edu/lccn/sn00063701/
- https://oregonnews.uoregon.edu/lccn/sn00063700/

The Courier alone is not sufficient annual newspaper coverage.

## Courier issue-inventory reconciliation added in this continuation

The restart checkpoint already contained a provisional 52-Friday schedule with many issue/page counts confirmed. This continuation used issue/page search results and page headers to tighten several previously pending dates.

Newly or additionally confirmed as **8-image issues** in this continuation:

- **23 Feb 1912** — page 8 is exposed for the issue.
- **30 Aug 1912** — page header explicitly reports `of 8`.
- **13 Sep 1912** — page 8 is exposed and the page header reports the 8-page issue context.
- **20 Sep 1912** — issue landing page explicitly lists images 1–8.
- **27 Sep 1912** — page 4 header explicitly reports `of 8`.
- **11 Oct 1912** — page 3/page 8 headers expose an 8-page issue.
- **18 Oct 1912** — issue landing page explicitly lists images 1–8.
- **8 Nov 1912** — page 8 is exposed in an 8-page issue context.
- **15 Nov 1912** — page 7 header explicitly reports `of 8`; image 8 is also indexed.
- **22 Nov 1912** — issue landing page explicitly lists images 1–8.
- **6 Dec 1912** — page 1 header explicitly reports `of 8`, and page 8 is indexed.
- **13 Dec 1912** — page 8 is indexed; full issue-count reconciliation should still use a landing/page header before final certification.
- **20 Dec 1912** — page 8 is indexed; full issue-count reconciliation should still use a landing/page header before final certification.

Additional dates were re-encountered as online and consistent with the existing ledger, including 5 Jan, 26 Jan, 5 Apr (12 images), 19 Apr, 10 May, 31 May, 7 Jun, 21 Jun, 28 Jun, 5 Jul, 26 Jul, 25 Oct and 1 Nov.

Dates that still need explicit final landing/header reconciliation include at least **2 Aug, 27 Dec**, and any other date still marked pending in the restart ledger. Do not infer a final page count solely from an OCR result.

## Scan-delivery / visual-credit retest

The visual-review rule remains unchanged: OCR/search results do **not** count as visual review.

This continuation again tested direct Historic Oregon Newspapers page-PDF access. The archive search layer can expose a PDF result and sometimes a generated page-layout description, but direct page-PDF retrieval still fails in the current research viewer with cache/retrieval errors. The local execution environment also cannot resolve the archive host for direct binary download. Therefore no newly encountered OCR/search page is promoted to `VISUALLY VERIFIED` merely because its text or metadata was readable.

Existing visual credits in `main` remain valid, including:

- Courier 5 Jan 1912 p6;
- Courier 12 Jul 1912 p5;
- complete Morning Enterprise 19 Mar 1912 issue;
- Morning Enterprise 7 Sep 1912 Harding/Willamette page;
- other already registered visually inspected pages.

All other known online scans remain **PENDING** or **RETRIEVAL GAP** until a faithful scan can actually be viewed.

## OCR/search discovery check in this continuation

A fresh exact-address search across the three local titles re-encountered the visually known 5 January Courier business grid, including OCR errors `603` for the visually verified **503 Main** Smith address and `609` for the visually verified **509 Main** Brightbill address. It also re-encountered **G. H. Young — 507 Main**.

The search did **not** justify a new 1912 exact-address claim for 505 Main. Later/earlier 505 results surfaced from other years, especially the already known 1911 Chicago Store advertisements. Those are not backdated into 1912.

No new `E-###` or `S-###` is created from this discovery-only batch.

## Morning Enterprise inventory observation

Historic Oregon Newspapers identifies the *Morning Enterprise* as **Daily (except Mon.)**. A complete year issue inventory is therefore much larger than the Courier inventory and must be built from the archive's actual issue calendar, not only a theoretical day-of-week schedule, because the title notes irregularities in numbering and the archive may contain missing or irregular dates.

Known 1912 issues/pages are readily indexed (examples include 31 Jan, 24 Mar, 26 May, 11 Aug, 19 Dec), normally with four images. This is only sampling/metadata evidence and is not yet the required full issue inventory.

## Oregon City Enterprise inventory observation

The *Oregon City Enterprise* is a weekly title. Indexed 1912 issues generally expose eight images (examples include 19 Jan and 1 Mar). A complete 1912 issue/date/page-count ledger still needs to be reconciled from the archive itself rather than inferred from frequency.

## Cross-record propagation audit

This continuation changes **coverage state only**. It does not establish a new occupant, owner, building event, business identity, person identity, property transfer or address mapping.

Accordingly:

- no new claim-level evidence ID is created;
- no new source ID is created merely for archive metadata/search results;
- no business/building/person/YAML record is changed;
- no timeline event is added;
- no no-hit is converted into vacancy or absence.

The correct repository output is this coverage checkpoint while 1912 remains **IN PROGRESS**.

## Next exact actions

1. Finish explicit Courier issue/page-count reconciliation for every one of the 52 expected Friday dates.
2. Build the **actual 1912 Morning Enterprise archive issue calendar** and page counts; do not assume every theoretical daily-except-Monday issue survives online.
3. Build the **actual 1912 Oregon City Enterprise archive issue calendar** and page counts.
4. Continue reasonable alternate scan-delivery tests. If the scan remains inaccessible after reasonable attempts, preserve the exact issue/page ranges as retrieval gaps and route them to numbered manual callouts.
5. Reconcile all existing visually verified pages against those ledgers so they are credited rather than re-reviewed.
6. Run target-category OCR/search discovery over the full inventories only as navigation; promote findings only after scan verification.
7. Audit other online 1912 source classes (municipal records, directories, maps, property records, historic photos/resource records) before considering `ONLINE COMPLETE`.
8. Do not change the canonical year status until every current-standard requirement is either completed online or precisely routed to a manual callout.
