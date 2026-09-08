# 1912 exhaustive online visual audit — restart checkpoint, 8 September 2026

Status: **IN PROGRESS — COVERAGE / ACCESS CHECKPOINT**

Purpose: resume 1912 under the current `RESEARCH-STANDARD.md` requirement for a complete online title/issue inventory and page-by-page visual review of every online-retrievable newspaper scan, without duplicating or regressing the substantial targeted 1912 research already integrated into `main`.

This file is a coverage ledger. It does **not** replace `evidence/source-captures/1912-main-street-research.md`, the 7 September conversation handoff, or the existing claim-level source/evidence files.

## Synchronization baseline

- Research branch: `research/1912-online-audit`.
- Branch was confirmed identical to current `main` at `97d1de9893cc10f83e8dbcfdeda06d3acc5d3a2b` before this checkpoint was written.
- Newer `main` always controls if parallel work advances the repository.
- The old `research/1912-main-street` branch must not be recreated from an old SHA.

## Current certification state

Canonical `registers/year-status.md` lists **1912 = IN PROGRESS**.

The remaining blocker is not lack of targeted findings. Current `main` already contains extensive 1912 exact-address, business, structural-context, and visually verified source work. The blocker is the later-adopted exhaustive standard: complete relevant-title inventory, issue/page inventory, actual scan review for every retrievable page, other-online-source audit, documented retrieval gaps, integration, and numbered manual callouts.

## Relevant local newspaper titles confirmed online

The current online audit treats these Oregon City titles as required local-newspaper coverage unless a later source audit documents a reason to exclude a title:

1. **Oregon City Courier** — LCCN `sn00063698`; weekly Friday title, online for the full 1912 year.
2. **Morning Enterprise** — LCCN `sn00063701`; daily local title (published daily except Monday during this period), online in 1912. ODNP documentation says the January 1912–December 1913 run was re-filmed.
3. **Oregon City Enterprise** — LCCN `sn00063700`; weekly local title, online through 1912.

The Oregon City Public Library digitization project identifies all three as Oregon City newspapers available through Historic Oregon Newspapers. Do not treat the Courier alone as full-year newspaper coverage.

## Visual-review rule applied in this session

A page is counted `VISUALLY VERIFIED` only when an actual scanned-page image/PDF/JP2 has been visually inspected, consistent with `RESEARCH-STANDARD.md`.

During this session Historic Oregon Newspapers reliably exposed:

- issue landing pages and page/image counts;
- OCR/text pages;
- page metadata;
- PDF/JP2 links in the HTML interface.

However, the current research viewer could not reliably open the underlying PDF/JP2 scan when requested directly. A direct page-PDF retrieval test for 5 January 1912 failed, and the web screenshot route could not resolve the page as an application/PDF object. Therefore:

- OCR/text inspected in this session is **OCR/TEXT ONLY**, not visual review;
- issue landing pages are valid for issue/page inventory but not visual certification;
- page scans already visually verified and preserved in existing repository source-captures retain their prior `VISUALLY VERIFIED` status;
- online pages whose scans remain inaccessible through this interface remain **PENDING / RETRIEVAL GAP** until an alternate scan route succeeds.

This access limitation is not negative historical evidence.

## Courier issue schedule and inventory progress

The Courier published on Fridays. Calendar reconstruction gives **52 expected Friday issue dates in 1912**. The issue-date list below is an expected schedule to reconcile against the online archive; it is not, by itself, proof that every issue survives online.

### January–March

| Issue date | Online issue/page-count state | Visual-credit state |
| --- | --- | --- |
| 5 Jan | online issue confirmed; 8 images | **p6 already VISUALLY VERIFIED in repo**; other pages pending |
| 12 Jan | online page evidence confirms 8 images | pending except any separately registered visual source |
| 19 Jan | online page evidence confirms 8 images | pending except any separately registered visual source |
| 26 Jan | online issue confirmed; 8 images | pending except any separately registered visual source |
| 2 Feb | online page evidence confirms 8 images | pending |
| 9 Feb | online page evidence confirms 8 images | pending |
| 16 Feb | online page/PDF search evidence shows 8-image issue context | pending |
| 23 Feb | expected Friday issue; online page-count confirmation still pending | pending |
| 1 Mar | online page evidence confirms 8 images | pending |
| 8 Mar | online issue confirmed; 8 images | pending |
| 15 Mar | online page evidence confirms 8 images | pending |
| 22 Mar | online issue confirmed; 8 images | pending |
| 29 Mar | online issue evidence confirms **10 images** | pending |

### April–June

| Issue date | Online issue/page-count state | Visual-credit state |
| --- | --- | --- |
| 5 Apr | online issue confirmed; **12 images** | pending |
| 12 Apr | online page evidence confirms 8 images | pending |
| 19 Apr | online issue confirmed; 8 images | pending |
| 26 Apr | online issue confirmed; 8 images | pending |
| 3 May | online page 1 confirmed; issue page count still to reconcile | pending |
| 10 May | online issue confirmed; 8 images | existing teardown/rebuild claim is already registered; full issue visual audit still pending |
| 17 May | online page 1 confirmed; issue page count still to reconcile | pending |
| 24 May | online page 1 confirmed; issue page count still to reconcile | pending |
| 31 May | online issue confirmed; 8 images | pending |
| 7 Jun | online issue confirmed; 8 images | pending |
| 14 Jun | online page 1 confirmed; issue page count still to reconcile | pending |
| 21 Jun | online issue confirmed; 8 images | pending |
| 28 Jun | online issue confirmed; 8 images | pending |

### July–September

| Issue date | Online issue/page-count state | Visual-credit state |
| --- | --- | --- |
| 5 Jul | online issue confirmed; 8 images | pending |
| 12 Jul | online issue confirmed; 8 images | **p5 already VISUALLY VERIFIED in repo**; other pages pending |
| 19 Jul | online page evidence confirms 8-image issue | pending |
| 26 Jul | online issue confirmed; 8 images | pending |
| 2 Aug | expected Friday issue; confirmation pending | pending |
| 9 Aug | online issue confirmed; 8 images | pending |
| 16 Aug | online issue confirmed; 8 images | pending |
| 23 Aug | online issue confirmed; 8 images | pending |
| 30 Aug | expected Friday issue; confirmation pending | pending |
| 6 Sep | online page evidence confirms an 8-image issue | pending |
| 13 Sep | expected Friday issue; confirmation pending | pending |
| 20 Sep | expected Friday issue; confirmation pending | pending |
| 27 Sep | expected Friday issue; confirmation pending | pending |

### October–December

| Issue date | Online issue/page-count state | Visual-credit state |
| --- | --- | --- |
| 4 Oct | online page evidence confirms 8-image issue | pending |
| 11 Oct | expected Friday issue; confirmation pending | pending |
| 18 Oct | expected Friday issue; confirmation pending | pending |
| 25 Oct | online issue confirmed; 8 images | pending |
| 1 Nov | online issue confirmed; 8 images | pending |
| 8 Nov | expected Friday issue; confirmation pending | pending |
| 15 Nov | expected Friday issue; confirmation pending | pending |
| 22 Nov | expected Friday issue; confirmation pending | pending |
| 29 Nov | online issue confirmed; 8 images | pending |
| 6 Dec | online front page confirmed; full page count still to reconcile | pending |
| 13 Dec | expected Friday issue; confirmation pending | pending |
| 20 Dec | expected Friday issue; confirmation pending | pending |
| 27 Dec | expected Friday issue; confirmation pending | pending |

## Existing Courier visual pages credited, not repeated

### 5 January 1912, page 6

Existing source capture: `evidence/source-captures/1912-jan-5-main-street-business-grid-visual.md`.

Status: **VISUALLY VERIFIED AT PAGE LEVEL**.

It directly reads the address ladder:

- H. N. Smith — pool room/cigars/tobacco — **503 Main**;
- G. H. Young — The Curio Man — **507 Main**;
- H. P. Brightbill — **509 Main**;
- Geo. A. Harding — **511 Main**;
- Bailey & Price — **527 Main**;
- separate Cox & Ward billiard/pool business on Main without a printed number.

The visual source corrects OCR errors including 603→503 and 609→509.

### 12 July 1912, page 5

Existing source capture: `evidence/source-captures/1912-smith-pool-hall-exit-visual.md`.

Status: **VISUALLY VERIFIED AT PAGE LEVEL**.

It reports H. H. Smith, who had conducted a pool hall at Fifth & Main, leaving for Aurora to open another pool hall. This does not resolve the H. N. Smith vs H. H. Smith initials conflict.

## Existing Morning Enterprise visual credit to preserve

Current `main` already contains visually verified 1912 Morning Enterprise pages that must be credited when the title ledger is built, including:

- all four pages of the **19 March 1912** issue; page 2 directly identifies Joe Wilson's Palace Saloon at **501 Main Street**;
- the **7 September 1912** Willamette Building / Harding Drug Store advertisement stating `Willamette Bldg., Room 4, Over Harding Drug Store`;
- other selected pages incorporated in later 1912 integrations.

These are page-level credits only. They do not certify the surrounding issues or the title/year as fully visually reviewed.

## OCR/text-only item encountered in this restart

The 9 February 1912 Courier front page contains a large city-development article headed approximately **“BUILDING ON EVERY STREET”** / “biggest boom in city's history.” The online text is potentially useful structural context, but this session did **not** obtain the actual scan through the available viewer. It therefore remains **OCR/TEXT ONLY** here and is not promoted as new evidence. Check current `main` for prior treatment before any future integration.

## Alternate scan-recovery attempts

Reasonable recovery routes tested in this restart:

1. Historic Oregon Newspapers HTML issue/page view — succeeds for metadata/OCR, but current viewer does not expose the embedded scan as a visually inspectable object.
2. Direct `.pdf` page URL — failed through the current fetch/download paths.
3. Web screenshot of the page-PDF search result — could not resolve as `application/pdf`.
4. Direct JP2-style route — search resolves back to the issue/page metadata rather than a usable scan object in this interface.
5. OldNews — confirms an alternate Oregon City Courier scan collection exists, but current public search results did not expose a page-image route adequate for visual certification.
6. Library of Congress / Chronicling America mirror — targeted searches did not recover this exact Courier issue under the same LCCN.

Do not downgrade online pages to absent because these viewer routes failed.

## Cross-record propagation audit for this batch

This restart batch establishes **coverage state and access limitations**, not a new historical occupant, ownership fact, building event, person identity, or address mapping.

Accordingly:

- no new `E-###` claim record is created;
- no new `S-###` source record is created merely for the coverage ledger;
- no building/business/person/YAML entry is changed;
- `timeline.md` is not changed;
- the appropriate output is this source-capture/checklist plus the unchanged `IN PROGRESS` year status.

## Next exact research actions

1. Finish Courier online issue/page-count reconciliation for the still-unconfirmed Friday dates above.
2. Test an alternate image-delivery route for the Courier scans; once a route works, begin full scan review at **5 January page 1**, skipping/crediting page 6 as already visually verified.
3. Build the Morning Enterprise 1912 issue/date/page-count ledger and reconcile all previously visually verified pages before reviewing missing pages.
4. Build the weekly Oregon City Enterprise 1912 ledger and reconcile existing visual credits.
5. Maintain `RL-024` watch during every visual page: 501/503/505/507/509/511, Fifth/Main, Sixth/Main, Post Office-relative businesses, Harding, Willamette, Young, Smith, Chicago Store, Brightbill, Gambrinus, Schrader, fire, demolition, construction, rebuilding, repair, moves, sales and property transfers.
6. Preserve every inaccessible scan as a precise retrieval gap; after reasonable online recovery attempts, route persistent gaps into the year-specific manual callout list rather than using them as negative evidence.
7. Do not change 1912 from `IN PROGRESS` until all `RESEARCH-STANDARD.md` certification requirements are satisfied.
