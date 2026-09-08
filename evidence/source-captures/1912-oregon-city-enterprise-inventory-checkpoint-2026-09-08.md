# 1912 Oregon City Enterprise issue-inventory checkpoint — 8 September 2026

Status: **IN PROGRESS — COVERAGE / ISSUE-INVENTORY CHECKPOINT**

Purpose: continue the exhaustive 1912 online audit under `RESEARCH-STANDARD.md`, concentrating on the weekly *Oregon City Enterprise* (`sn00063700`). This file records issue/date/image-count controls and archive anomalies only. It does not certify visual review of the pages and does not supersede the claim-level 1912 evidence already on current `main`.

## Synchronization caution

- Current `main` observed during this continuation: `e194a22a30705cb410429381fb204be4b33805fa`.
- Active additive audit branch: `research/1912-online-audit`.
- Parallel work continues to advance `main`; this stale audit branch must not overwrite master registers/timelines before final reconciliation.

## Title provenance

Historic Oregon Newspapers identifies *Oregon City Enterprise* (`sn00063700`) as a weekly Oregon City title and warns of irregularities in numbering.

Title record:

- https://oregonnews.uoregon.edu/lccn/sn00063700/

ODNP's 2013 digitization history states that the 1912 *Oregon City Enterprise* run was already online as part of the title's broader digitized coverage; the specifically re-filmed Enterprise portions were Jan. 1905–Jan. 1908 and July 1917–Dec. 1922, not 1912. Therefore 1912 may retain older filming/sequence irregularities and must be audited issue-by-issue.

## Confirmed 1912 issue/image-count controls

The following counts are based on archive page headers or `All Pages` records, not inferred from publication frequency:

| Issue date | Online image slots confirmed | Control / note |
| --- | ---: | --- |
| 12 Jan 1912 | **7** | Page-1 archive header explicitly says `1 2 3 4 5 6 7 of 7`. The archive also labels image 7 as printed page 8, so this issue requires sequence/missing-page caution rather than assuming a normal eight-image issue. |
| 19 Jan 1912 | **8** | `All Pages` record lists images 1–8. |
| 1 Mar 1912 | **8** | Page-1 archive header explicitly says `of 8`. |
| 5 Apr 1912 | **8** | Page-1 archive header explicitly says `1 ... 8 of 8`. |

Additional genuine 1912 issue/page controls encountered but not yet sufficient here to certify final image count include:

- 26 Jan 1912 — page 4 is indexed and textually dated 26 Jan;
- 8 Mar 1912 — image 1 is indexed and textually dated 8 Mar;
- 3 May 1912 — image 1 is indexed and textually dated 3 May;
- 17 May 1912 — image 5 is indexed and textually dated 17 May;
- 24 May 1912 — image 3 is indexed and textually associated with the issue;
- 5 Jul 1912 — page/image 7 is indexed.

These page hits confirm issue existence only; they are not final page-count controls unless an all-pages/header control is recovered.

## January 12 sequence anomaly

The 12 January issue is particularly important for audit handling:

- the archive page-1 header exposes only **seven image slots**;
- the archive separately labels image 7 as **printed page 8**;
- other indexed image/page labels are not a simple one-to-one printed-page sequence.

Therefore this issue must not be normalized to eight pages merely because surrounding weekly issues commonly have eight images. The annual audit should preserve the exact online image sequence and determine whether a printed page is absent, combined, mislabeled, or otherwise represented before final certification.

This is a **coverage/sequence question**, not evidence that any historical content was absent.

## Visual-review status

Nothing in this inventory checkpoint is promoted to `VISUALLY VERIFIED` solely from HTML/OCR/index metadata. Under `RESEARCH-STANDARD.md`, actual scan inspection is still required.

The current research interface continues to retrieve archive HTML/OCR much more reliably than the native page PDFs/JP2 scans. Attempts to follow page-PDF links frequently cache-miss, so those pages remain `PENDING` or `RETRIEVAL GAP` until the faithful scan is actually rendered or an alternate online derivative is exhausted and the gap is routed to a manual callout.

## Research consequence

This checkpoint creates no new occupant, address, business, building, ownership, fire, demolition, construction, or transfer claim. Accordingly:

- no new `E-###` or `S-###` is created;
- no building/business/person/timeline record is changed;
- no page-count anomaly is treated as historical negative evidence.

## Next exact actions

1. Continue the Friday-by-Friday *Oregon City Enterprise* issue ledger for all actual 1912 archive issues.
2. Record issue-specific image counts from page headers or all-pages records; do not extrapolate eight pages.
3. Reconcile printed-page labels against archive image slots where they diverge, especially 12 January.
4. Credit any existing visually verified 1912 Enterprise pages already on `main` before reviewing duplicates.
5. Continue faithful scan-delivery attempts; record persistent failures as exact retrieval gaps.
6. Continue the much larger *Morning Enterprise* actual-calendar inventory in parallel.
7. Keep **1912 = IN PROGRESS** until every current-standard requirement is completed or precisely routed to manual work.
