# 1917 Enterprise September → October research handoff — 7 September 2026

Status: **HANDOFF CHECKPOINT — September Enterprise research is closed and integrated; October originals are preserved but have not yet been visually researched. 1917 remains IN PROGRESS.**

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Main observed immediately before this checkpoint: `1ef810a670719c11fa14ae1e296d5e135daa8903` (`Add Wheel ownership-dates handoff checkpoint`).  
September closeout commit: `fbaca8931112fd6707e200147bb8947ce43d35c7` (`Close September 1917 Enterprise visual audit`).

This checkpoint is deliberately subordinate to the live branch: **fetch current `main` again before resuming**, because parallel Wheel/LaFarlette/505 and other workflows are actively committing. Never reset or rewind `main` to any SHA named here.

## Required project controls on resume

Before new research:

1. fetch/sync current `main` without reset/revert/force-push;
2. read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely;
3. inspect the newest commits and this checkpoint;
4. follow the repository evidence classifications, ID allocation, source-selection, synchronization, building-continuity, and Cross-Record Propagation Audit rules;
5. visually inspect actual archival scans; OCR/search/text is discovery/navigation only;
6. verify printed issue date and printed page number on every Enterprise scan because March and April exposed archive page-association defects;
7. treat failed retrieval as a retrieval gap, never negative evidence;
8. never turn source silence/no-hit coverage into vacancy, non-use, closure, demolition, relocation, or absence;
9. keep similarly named people/businesses separate unless contemporary evidence bridges them;
10. keep business ownership, operation, tenancy, building ownership, licensing, trade-name use, address, and physical-building identity separate unless evidence explicitly connects them;
11. run `python3 scripts/validate_archive.py` before and after meaningful writes, or verify the equivalent GitHub validation workflow.

## Canonical 1917 newspaper state at handoff

### Oregon City Courier

Do **not** repeat the annual Courier pass.

- annual issue inventory: all **52 issue dates** reached;
- **435 genuine pages visually verified**;
- **13 December 1917 true page 21 remains a retrieval/manual gap** because the archive-supplied seq-21 is visibly a 27 December page.

### Oregon City Enterprise

January through **September** are now researched and integrated.

Canonical status from `registers/year-status.md` after the September closeout:

- **312 genuine intended-date Enterprise pages visually verified through September**;
- **314 January–September archive slots inspected**;
- true-page retrieval gaps remain:
  - **16 March 1917, true p5**;
  - **13 April 1917, true p8**;
- **102 exposed October–December archive slots remain** before final title-calendar reconciliation;
- 1917 remains **IN PROGRESS**, not ONLINE COMPLETE.

## Completed July–September batches

### July

- 6 / 13 / 20 / 27 July: **32/32 genuine pages visually verified**;
- integrated as `S-286` / `E-260`;
- closeout commit `1ba2a4e690b23566cccedafd6856df6fba0edb62`;
- W. S. Eddy / Fashion Stable directly continued at **Main between Fourth and Fifth** through 27 July, without a number;
- Farr Bros. received dated business/supplier observations without address or named proprietor;
- no exact target-frontage occupant established.

### August

- 3 / 10 / 17 / 24 / 31 August: **40/40 genuine pages visually verified**;
- integrated as `S-287` / `E-261`;
- closeout commit `a822d131b441cd06fb3feec639fff561571b3f2d`;
- W. S. Eddy / Fashion Stable continued through 31 August at the same relative Main Street location;
- Farr Bros. market-report credits on 3/10/17/24 August; 31 August instead names R. Petzold + Brady Mercantile. The provider-line change is **not** closure, sale, ownership-transfer, relocation, or non-operation evidence;
- 31 August Adams Department Store carries going-out-of-business/closing-out advertising, but no numbered address;
- visual reinspection corrected an older OCR-derived Courier summary: both **2 August Courier p1** and **3 August Enterprise p5** print **Mrs. J. C. Napier at 512½ Main**, not 612/613½. The separate 612 Main optometrist control remains distinct;
- no exact target-frontage occupant established.

### September

Capture: `evidence/source-captures/1917-enterprise-september-07-28-visual-review-2026-09-07.md`  
Source/evidence: **`S-288` / `E-262`**  
New business record: **`BUS-105` — J. C. Penney Co. / The Golden Rule**  
Closeout commit: `fbaca8931112fd6707e200147bb8947ce43d35c7`.

- 7 / 14 / 21 / 28 September: **32/32 genuine intended-date pages visually verified**;
- no September substitution, duplicate-page defect, or retrieval gap;
- W. S. Eddy / Fashion Stable continues through **28 September 1917**, still **between Fourth and Fifth on Main Street**, no number;
- Farr market-report wording varies:
  - 7 Sep p7 — R. Petzold + Brady Mercantile;
  - 14 Sep p7 — Farr Brothers + Brady Mercantile;
  - 21 Sep p7 — no local market-report column;
  - 28 Sep p7 — Brady Mercantile + Farr Brothers;
- 14 Sep p6 separately lists **Farr Bros. (Piezo), $14.00** in County Court expenditure material;
- none of those Farr items supplies a street address, individual proprietor, or bridge to Edwin F. Farr, Alice Farr, Farr's Pool Hall at 505, Carl Harr, or Harr's Recreation Center;
- **14 Sep p3** visibly advertises **J. C. Penney Co. / THE GOLDEN RULE / 175 BUSY STORES / Main Street Between Fifth and Sixth / Phone 270**. This is a direct block-relative business anchor only. It does **not** establish a numbered address, side of Main, parcel, building, ownership, lease, opening date, or continuity and must not be assigned to 501/503/505/507/509/511 without an independent bridge;
- Adams Department Store quit-business/closing-out advertising appears 7/14/21 Sep p8, unnumbered. Lack of a matching ad on 28 Sep is not closure/vacancy/demolition evidence;
- no defensible exact occupant was recovered for **501/503/505/507/509/511 Main**, new **427 Main**, or numbered **106/107/108/109/110 Fifth**;
- no relevant exact-address pool-room/pool-hall/billiard hit was recovered.

The September integration was protected by pre- and post-write validation. The final successful workflow reported `S-288 / E-262 / BUS-105`, and `python3 scripts/validate_archive.py` passed after the integrated changes and again immediately before push.

## October originals — RETRIEVAL ONLY, NOT VISUAL COVERAGE

Original PDFs are already preserved under:

`newspapers/oregon-city-enterprise/1917-october/`

with manifest:

`newspapers/oregon-city-enterprise/1917-october/manifest.json`

The October retrieval commit was `62eab672630059c805304e74d1568041052dd7b0` (`Archive October 1917 Oregon City Enterprise scans`). The scans were archived by a parallel retrieval workflow; **this does not count as visual research or certification**.

Manifest page counts:

- **5 October 1917 — 8 exposed pages**;
- **12 October 1917 — 8 exposed pages**;
- **19 October 1917 — 6 exposed pages**;
- **26 October 1917 — 8 exposed pages**;
- total October exposed slots: **30**.

No October page should be credited as visually verified until its printed date and printed page number have been inspected on the actual scan.

## Exact next research step

Resume with the **October 1917 Oregon City Enterprise scan-first audit**, not with September and not with the Courier.

For all 30 October PDFs:

1. verify printed issue date and printed page number before content credit;
2. visually inspect every actual page;
3. only after the page-level scan pass use OCR/text for small-print discovery;
4. visually re-open every candidate before promotion;
5. search especially for:
   - 501 / 503 / 505 / 507 / 509 / 511 Main;
   - 427 Main;
   - Fifth & Main;
   - 106 / 107 / 108 / 109 / 110 Fifth;
   - pool room / pool hall / billiards / cigars;
   - Fashion Stable / W. S. Eddy;
   - Farr / Farr Brothers;
   - J. C. Penney / Golden Rule;
   - Smith pool room;
   - Harding / Young / Brightbill / Bradley;
   - Adams Department Store;
   - moves, sales, leases, licenses, fire, construction, demolition, remodeling, ownership/agent language;
6. preserve numeric false positives as rejected context rather than address evidence;
7. perform the full Cross-Record Propagation Audit;
8. validate and commit the October closeout;
9. continue into November unless October exposes a source defect or a high-value source-class lead that warrants immediate switching.

## Cross-Record Propagation decision for this handoff

The September batch itself has already been propagated across source/evidence registers and YAML, timelines, businesses/people, open questions/leads, business/address registers, crosswalk/archive index, year status, research log, and database YAML as warranted.

The later **October scan-preservation batch is retrieval only**. It creates **no historical event, occupant, business continuity, vacancy/absence conclusion, or building change** until visual inspection occurs. Therefore this handoff records the retrieval state and next action but does not manufacture October S/E historical conclusions from unreviewed scans.

## Remaining major 1917 blockers

These remain open after September and do not prevent continuing October online review:

1. **1916–1917 Sohns & Woodbeck directory, Oregon City section** — actual Oregon City pages/full 500 Main block and relevant name/business indexes remain unrecovered; partial Oak Grove/Jennings Lodge material is not a substitute.
2. **Courier 13 December 1917 true p21** — retrieval/manual gap remains.
3. **Enterprise 16 March true p5** — retrieval/manual gap remains.
4. **Enterprise 13 April true p8** — retrieval/manual gap remains.
5. final Enterprise title-calendar reconciliation and other required online/source-class closeout work remain before any ONLINE COMPLETE claim.

## Resume rule

Do **not** redo January–September Enterprise work. Do **not** repeat the Courier annual pass. Fetch current `main`, respect any newer parallel commits, then start with the preserved **5 October 1917 Enterprise** scans and continue chronologically.
