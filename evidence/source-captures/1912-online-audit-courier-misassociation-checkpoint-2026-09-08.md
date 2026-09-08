# 1912 exhaustive online audit — Courier issue reconciliation / page-misassociation checkpoint

Date: 8 September 2026  
Status: **IN PROGRESS — COVERAGE / RETRIEVAL-GAP CHECKPOINT**

Purpose: continue the current-standard 1912 online audit on `research/1912-online-audit`, concentrating on unresolved Oregon City Courier issue/page-count controls and archive page-association quality. This is a coverage/retrieval record, not a replacement for the substantial claim-level 1912 research already on `main`.

## Synchronization caution

Parallel work has advanced `main` since this branch began. The branch is intentionally used only for additive coverage checkpoint files until it is reconciled/audited against current `main`. Do not overwrite master registers from this stale branch.

## Courier page-count reconciliation advanced

Fresh Historic Oregon Newspapers indexing confirms additional late-year and mid-year issue controls:

- **13 Dec 1912** — page/image 8 is positively indexed.
- **20 Dec 1912** — page/image 8 is positively indexed.
- **14 Jun 1912** — indexed page 7 is within an eight-image issue context, supporting an 8-image issue.
- **24 May 1912** — image 8 is positively indexed.
- **27 Dec 1912** — prior checkpoint already preserved an explicit page-header control showing an eight-image issue.

These controls improve the issue inventory, but a page-8 hit alone is not visual review and, where the archive does not expose an all-pages/landing control, should remain an inventory control rather than a claim that every page was faithfully associated.

## 17 May 1912 archive sequence — page misassociation detected

The online 17 May 1912 Courier sequence is **internally inconsistent**:

- image 1 is textually dated **Friday, May 17, 1912**;
- image 3 is textually dated **Friday, May 17, 1912**;
- image 4 is textually dated **Friday, May 17, 1912**;
- image 5 is textually dated **Friday, May 17, 1912**;
- image 6 is textually dated **Friday, May 17, 1912**;
- image 7 is textually dated **Friday, May 17, 1912**;
- but the archive result labeled **17 May 1912, image 2** contains the masthead/text **Friday, May 10, 1912**.

Therefore image 2 must **not** be credited as a valid 17 May page merely because the archive URL/metadata assigns it to that issue. It is a known online **MISASSOCIATED PAGE / RETRIEVAL GAP** until a faithful 17 May image 2 is recovered or an authoritative issue scan proves the intended sequence.

This matters for the annual standard: issue metadata alone cannot certify correct page association. The page-level date printed on the scan/text must be reconciled when archive sequencing conflicts with the source itself.

## 3 May 1912 and 2 August 1912 remaining controls

The archive indexes multiple genuine pages for both issues:

### 3 May

Images/pages 1, 3, 4, 5, and 6 are indexed under the date. Search recovery in this batch did not yet obtain an explicit all-pages control or reliable page-8 result for the Oregon City Courier. Do not infer the final image count solely from surrounding weekly patterns.

### 2 August

Images/pages 3, 4, 5, 6, and 7 are indexed and visibly/textually belong to 2 August. Search recovery in this batch did not yet obtain an explicit page-8/all-pages control. The issue remains online-confirmed but final issue-size certification is still pending.

## Visual-credit rule

Nothing in this checkpoint upgrades OCR/search results to `VISUALLY VERIFIED`. Search-index text and page metadata are inventory/discovery aids only. Actual scan inspection remains required under `RESEARCH-STANDARD.md`.

Existing visual credits already on `main` remain valid and should be credited rather than duplicated, especially Courier 5 Jan p6 and 12 Jul p5.

## Historical-result consequence

This batch establishes no new occupant, owner, building event, property transfer, or address mapping. Accordingly:

- no new `E-###` is created;
- no new `S-###` is created merely from issue metadata;
- no timeline/building/business/person record is changed;
- no archive sequencing error is treated as evidence about historical absence.

## Next exact actions

1. Recover an all-pages/page-count control for **3 May 1912**.
2. Recover an all-pages/page-count control for **2 Aug 1912**.
3. Recover the correct **17 May image/page 2**, or document all reasonable alternate-derivative attempts and route it to the eventual 1912 numbered manual callout list.
4. Check the remaining Courier ledger line-by-line for any similar wrong-date/misassociated scans before declaring the issue inventory reconciled.
5. Continue the actual 1912 *Morning Enterprise* and *Oregon City Enterprise* archive-calendar inventories and scan-review states.
6. Keep **1912 = IN PROGRESS** until the current exhaustive standard is satisfied.
