# 1912 Oregon City Courier exhaustive audit — page-count / retrieval resume

Date: 9 September 2026  
Status: **IN PROGRESS — ISSUE-INVENTORY / RETRIEVAL CHECKPOINT**

Purpose: continue the current-standard 1912 *Oregon City Courier* audit from authoritative `main` without restarting the year or reviving the obsolete `research/1912-main-street` branch. This checkpoint records page-count controls, visual-credit inheritance, and retrieval gaps only. It does not create a historical claim from OCR or issue metadata.

## Synchronization / parallel-work control

- Parallel 1912 work on `main` visually reviewed and archived **19 January printed pages 1–4** as `S-307` and pages **5–8** as `S-310`; that issue is now complete at **8/8 VISUALLY VERIFIED**.
- A later controlled retrieval pass preserved `evidence/source-captures/retrieval-manifests/1912-courier-gap-recovery-2026-09-09.tsv` in commit `a7b1fb3fc3d845b2b9da492aa31fc1913508bd29`. That manifest resolves several issue-size questions but, by itself, does **not** supply visual-review credit.
- `1912` remains **IN PROGRESS** in `registers/year-status.md`.

## 19 January 1912 — current state

The issue is controlled as an **eight-image issue**. Earlier on 9 September, pages **1–4** were visually inspected and preserved as `S-307`. Later the project steward supplied pages **5–8**; all four actual scans were visually inspected and preserved as `S-310`. The 19 January issue is now **8/8 VISUALLY VERIFIED**.

Page 8 directly states that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot** (`E-282` / `S-310`):

- https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/

This **supersedes the earlier OCR/TEXT ONLY / pending-scan state** recorded in the first version of this checkpoint. The page prints no street number. `E-092` independently places George A. Harding at 511 Main on 5 January, so interpreting this as the same 511 store is a **STRONG CROSS-SOURCE INFERENCE**, not wording printed on page 8.

## Earlier explicit issue-size controls

The Historic Oregon Newspapers page header (`Page [Select] of N`) is used here as an archive issue-size control only; it is not visual-review credit.

| Issue date | Archive control | Result |
| --- | --- | --- |
| 14 Jun. 1912 | page 3 and page 7 live page headers report `of 8` | **8 images** |
| 30 Aug. 1912 | page 6 live page header reports `of 8` | **8 images** |
| 27 Sep. 1912 | page 4 live page header reports `of 8` | **8 images** |
| 11 Oct. 1912 | page 3 live page header reports `of 8` | **8 images** |
| 18 Oct. 1912 | page 8 live page header reports `of 8` | **8 images** |
| 8 Nov. 1912 | page 8 live page header reports `of 8` | **8 images** |
| 15 Nov. 1912 | page 7 live page header reports `of 8` | **8 images** |
| 6 Dec. 1912 | page 1 live page header reports `of 8` | **8 images** |

Representative canonical pages:

- 14 Jun. p3: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-06-14/ed-1/seq-3/
- 30 Aug. p6: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-08-30/ed-1/seq-6/
- 27 Sep. p4: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-09-27/ed-1/seq-4/
- 11 Oct. p3: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-10-11/ed-1/seq-3/
- 18 Oct. p8: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-10-18/ed-1/seq-8/
- 8 Nov. p8: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-11-08/ed-1/seq-8/
- 15 Nov. p7: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-11-15/ed-1/seq-7/
- 6 Dec. p1: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-12-06/ed-1/seq-1/

These controls reduce the page-count backlog but do not certify the underlying pages as visually reviewed.

## 9 September controlled PDF-sequence retrieval — count gaps resolved

The preserved retrieval manifest tested canonical native-PDF sequence URLs through **sequence 12** for the remaining suspect issues. A valid PDF means the canonical archive returned an actual PDF object; `404` means that tested sequence did not exist at that route. This is a **retrieval / issue-inventory control**, not a claim that every returned page has been visually reviewed.

| Issue date | Controlled result | Current issue-count conclusion |
| --- | --- | --- |
| **23 Feb. 1912** | seq. **1–8** valid PDFs; seq. **9–12 = 404** | **8 archive images** |
| **3 May 1912** | seq. **1–8** valid PDFs; seq. **9–12 = 404** | **8 archive images** |
| **17 May 1912** | seq. **1–8** return PDFs; seq. **9–12 = 404** | **8 archive slots**, but **seq. 2 is misassociated** and visibly/textually carries a **10 May** masthead; genuine 17 May page/image 2 remains a retrieval gap |
| **24 May 1912** | seq. **1–8** valid PDFs; seq. **9–12 = 404** | **8 archive images** |
| **2 Aug. 1912** | seq. **1–8** valid PDFs; seq. **9–12 = 404** | **8 archive images** |
| **13 Dec. 1912** | seq. **1–10** valid PDFs; seq. **11–12 = 404** | **10 archive images** — supersedes the earlier assumption/control that only an image-8 endpoint was known |

Manifest: `evidence/source-captures/retrieval-manifests/1912-courier-gap-recovery-2026-09-09.tsv`.

This substantially closes the previously listed count-control backlog. In particular, **3 May, 24 May, 2 August, and 13 December no longer remain unresolved issue-size questions**, and 23 February is controlled as eight images. The unusual **10-page 13 December issue** must be carried forward as such rather than normalized to the more common eight-page pattern.

## Remaining narrow Courier sequence gap

The remaining problem from this specific count-reconciliation set is **17 May 1912, sequence/image 2**. The archive exposes eight sequence slots, but its `seq-2` object is not the genuine 17 May page: it carries a **10 May 1912** masthead. Therefore:

- the archive-slot count can be recorded as **8**;
- **seq. 2 cannot receive 17 May visual-review credit**;
- the genuine 17 May page/image 2 remains a **RETRIEVAL GAP** unless recovered from another derivative, institution, microfilm, or alternate archive object;
- the misassociated 10 May object must not be silently counted twice or treated as 17 May historical evidence.

This is an archive-association defect, not evidence that the genuine page did not exist.

## Additional 1912 construction / street-work context surfaced while reconciling pages

Two OCR/indexed items are retained here as discovery/context only unless separately scan-certified elsewhere:

### 15 March — Straight & Salisbury move because a new block was being built

The *Courier* reports Straight & Salisbury moved to **Main and Ninth Streets** and says they were compelled to move because **a new block was being built on their old stand**.

Canonical page: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-03-15/ed-1/seq-5/

The recovered text does not identify the old stand well enough to place this construction at 501/503/505/507 or the Fifth–Sixth target frontage. It is therefore useful evidence that the 1912 citywide building cycle included at least one specifically reported new-block project, but it is **not a bridge to `E-090` or `RL-038`** without independent location evidence.

### 27 September — paving at Eleventh/Main, not target-block evidence

The *Courier* says Main Street **in front of Busch's** was torn up as work started on paving **from that point to the Abernethy**. Independent 1912 Busch advertising places **Frank Busch at Eleventh & Main**.

Canonical pages:

- 27 Sep. local item: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-09-27/ed-1/seq-5/
- 25 Oct. Busch ad: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-10-25/ed-1/seq-4/

This is northern Main Street paving context. It does **not** establish Fifth–Sixth paving or target-building demolition and must not be used as a location bridge for the 10 May teardown statement.

## Cross-record decision

No new historical `E-###` or external-source `S-###` is created from the issue-count manifest because these results are archive-coverage metadata, not new historical propositions. The manifest is preserved for auditability and this checkpoint carries the corrected issue-size states.

The Percy Cross / Harding Drug Store notice is no longer pending: it is separately registered as **VISUALLY VERIFIED `E-282` / `S-310`**. The March new-block and September paving items remain outside the target frontage unless independent location evidence provides a bridge.

The correct propagation from this count pass is the corrected inventory/retrieval checkpoint plus continued **1912 IN PROGRESS** status.

## Next exact actions

1. **19 January pages 1–8 are complete and visually verified; no further recovery is needed for that issue.**
2. Preserve **17 May genuine image/page 2** as the remaining specific Courier sequence-recovery target from this gap set; do not credit the misassociated 10 May object.
3. Continue actual scan-by-scan Courier visual review using the now-recovered PDFs for the count-controlled issues, crediting prior verified pages rather than repeating them.
4. Continue the *Morning Enterprise* July/August ledger and then remaining months.
5. Continue the weekly *Oregon City Enterprise* full-year ledger and visual/retrieval states.
6. Keep `RL-038` open: no independent bridge has yet mapped the 10 May Main Street teardown statement to 501/503/505/507 or the target Block 4 frontage.
7. Keep **1912 = IN PROGRESS** until the exhaustive online standard is actually satisfied or persistent gaps are precisely routed to manual follow-up.

## Current-main preservation note — 9 September 2026

This checkpoint is additive to the current `main` work and must not be used to revive or merge the obsolete `research/1912-main-street` branch. Current `main` contains the claim-level 1912 evidence, the complete 19 January visual review, and the controlled gap-retrieval manifest. No historical claim is inferred from a missing archive object or from issue-size metadata alone.
