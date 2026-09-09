# 1912 Main Street Research — Final Handoff Checkpoint — 8 September 2026

Status: **CURRENT HANDOFF / KNOWLEDGE-PRESERVATION CHECKPOINT**. This file preserves the current 1912 research state and restart instructions. It does not create a historical claim or change the canonical year status by itself.

Repository: `rodyoung1967/main-street-archives`  
Authoritative branch: `main`  
Latest observed `main` immediately before this handoff file was written: `0b21d4aefa5ee10f3ba5f3394db7c10003d64b99` — `Archive 1912 exhaustive online-audit progress checkpoints` (PR #27).  
Always fetch/sync the newest `main` first because multiple parallel workflows are active and this SHA may already be obsolete.

## Mandatory startup for the next session

1. Fetch/sync newest `main`.
2. Do not reset, revert, force-push, delete, or overwrite newer parallel commits.
3. Read `AGENTS.md` completely.
4. Read `RESEARCH-STANDARD.md` completely.
5. Read `MANUAL-FOLLOWUP.md` completely/currently relevant portions.
6. Read `registers/year-status.md`; it is the canonical year-status control.
7. Read `evidence/source-captures/2026-09-08-1912-conversation-reconciliation-checkpoint.md`.
8. Read `evidence/source-captures/1912-main-street-research.md`.
9. Read the newest 1912 exhaustive-audit checkpoints now merged to `main`, especially:
   - `evidence/source-captures/1912-online-audit-progress-2026-09-08-pm.md`
   - `evidence/source-captures/1912-morning-enterprise-july-august-ledger-progress-2026-09-08-1830.md`
   - `evidence/source-captures/1912-courier-pagecount-progress-2026-09-08-1612.md`
   - `evidence/source-captures/1912-native-pdf-visual-route-2026-09-08.md`
   - `evidence/source-captures/1912-enterprise-inventory-reconciliation-checkpoint-2026-09-08.md`
10. Review newest commits before writing because 503/505/Wheel/1917/1919/directory/photo workflows may have advanced `main`.

## Branch handling

- **Do not merge or revive `research/1912-main-street`.** It was created from the 1911-era main and became more than a thousand commits stale. Its verified claim-level knowledge has already been reconciled into newer `main`.
- `research/1912-online-audit` was the live exhaustive-audit branch. Its 23 add-only source-capture/checkpoint files were preserved on `main` by PR #27; squash merge commit `0b21d4aefa5ee10f3ba5f3394db7c10003d64b99`.
- `research/1912-online-closeout` contains a useful closeout checkpoint plus **temporary probe scripts/workflows**. Do **not** merge that branch wholesale. Reuse only verified process/research knowledge after syncing to current `main`, and remove/avoid temporary instrumentation in final archive integration.

## Canonical 1912 status

**1912 remains IN PROGRESS.** Do not call it ONLINE COMPLETE.

The blocker is not lack of findings. The blocker is the later-adopted exhaustive standard: complete relevant-title inventory, issue/page-count inventory, visual inspection of every online-retrievable page scan, other-online-source audit, explicit retrieval gaps, final integration, and numbered manual callouts for anything that genuinely cannot be completed online.

A page counts as visually reviewed only if the faithful scan/image/PDF was inspected. OCR/search/HTML text is discovery and inventory evidence only.

## Core verified 1912 historical findings already on main

### 501 Main

- `E-104` / `S-118`: visually reviewed **19 March 1912 Morning Enterprise** directly identifies **Joe Wilson's Palace Saloon at 501 Main Street** in a liquor-license application.
- Later June material uses Joseph Wilson / Palace Saloon / Fifth-Main context. Treat Joe=Joseph as a strong same-business/location inference unless identity is independently explicit.

### 503 Main

`E-089` preserves the Smith sequence:

- 5 Jan 1912: **H. N. Smith — Pool Room, Cigars and Tobacco — 503 Main Street**, visually verified. OCR incorrectly reads 603.
- 24 Mar 1912: **H. H. Smith** applies for a pool-hall license at **503 Main Street**.
- 12 Jul 1912: H. H. Smith, who had conducted a pool hall at **Fifth and Main**, is reported leaving for Aurora to open a pool hall there.

Do not silently merge H. N. Smith and H. H. Smith. The initials conflict remains `RL-037`.

### 505 Main

No direct exact-number 1912 occupant is currently established in the annual synthesis. The 5 Jan Chicago Store advertisement says **Main St. just below Postoffice**. Do not mechanically carry the exact 505 address from 1911 forward without a 1912 continuity source. Missing exact evidence is not vacancy evidence.

### 507 / 509 / 511 Main — 5 January address ladder

`E-092` / `S-102`, visually verified:

- **G. H. Young — 507 Main**;
- **H. P. Brightbill — 509 Main**; OCR incorrectly reads 609;
- **Geo. A. Harding — 511 Main**; OCR garbles the number.

George Young's 507 address strengthens but does not prove the hypothesis that his March 1911 Willamette Building premises were 507. Later `E-138` / `S-154` says **“Willamette Bldg., Room 4, Over Harding Drug Store”** in September 1912, showing the building-name/address geometry is more complicated than a simple one-building/one-number equation.

Keep George Harding's own 511 business address separate from the separately named Harding Building.

### Sixth & Main / Gambrinus

`E-091`: 24 Mar 1912 identifies the **Gambrinus Saloon at Sixth and Main** and **William Trudell** as proprietor. This extends the 1906 William Tell/Gambrinus property transfer → 1910 new Gambrinus block → 1911 Electric Hotel annex → 1912 saloon chronology. Exact numbered storefront remains unresolved.

### Main Street demolition / rebuilding

`E-090` / `S-105`: 10 May 1912 *Courier* states in the present tense that Oregon City was **tearing down buildings on Main Street and building new buildings in their places**.

This is direct citywide Main Street structural-change evidence. It does **not** identify a block, lot, owner, business, or number. Do not map it to 501/503/505/507 without an independent bridge. `RL-038` remains open.

### Schrader bakery

`E-093`: Herman Schrader sold two bakeries in December 1912, including one on Main Street, to **Wemmo & Haas**. Earlier advertising placed Schrader near the Post Office. Exact Main Street number remains unresolved.

## Current exhaustive newspaper-audit progress

Relevant online newspaper titles currently being inventoried:

- `sn00063698` — *Oregon City Courier*;
- `sn00063700` — *Oregon City Enterprise*;
- `sn00063701` — *Morning Enterprise*.

Important archive-navigation rule: use the explicit title/year issue route `/lccn/<LCCN>/issues/1912/`; a generic Browse Issues page may default to a different year. Track archive sequence/image count separately from printed page numbers.

### Courier

- Continue reconciling all 52 expected Friday issue dates to actual surviving online issues and explicit archive page counts.
- 2 Aug 1912 is positively confirmed online, but its full issue count still needs a definitive `of N`/landing-page control.
- 27 Dec 1912 is explicitly **8 images/pages** (`1–8 of 8`).
- Native one-page PDFs can provide faithful visual review when they render. The route was re-confirmed on 5 Jan p6.
- PDF/HTML availability is page-dependent and sometimes cache-misses. A cache miss is a RETRIEVAL GAP, not visual-review credit and not negative evidence.

### Morning Enterprise

Firm archive `of N` controls already established include:

- 2 Jul — 4 pages;
- 3 Jul — 4 pages;
- 9 Aug — 4 pages;
- 11 Aug — 4 pages;
- 17 Aug — 4 pages.

The 4 Jul front page explicitly states there would be **no 5 July edition** because employees were observing Independence Day; this is a publication-calendar control, not a missing-issue inference.

Continue the July ledger beyond 3 July and the August ledger beyond the firm controls, preserving actual surviving dates and explicit issue counts.

### Oregon City Enterprise

Continue/finish the weekly 1912 ledger, page counts, visual states, and target screening in parallel with the daily *Morning Enterprise* and weekly *Courier*.

## OCR-only / pending visual lead that must survive handoff

On the separate `research/1912-online-closeout` checkpoint, *Oregon City Courier*, **19 January 1912, page/image 8**, has OCR/text saying **Percy Cross** accepted a position in the **Harding drugstore** during the absence of **A. E. Wilmot**.

Classification: **OCR/TEXT ONLY — PENDING SCAN CERTIFICATION**.

Do not create a new evidence/person relationship or exact-address claim until the actual page scan is visually inspected. If verified, it may help reconstruct Harding Drug Store staffing/continuity around the January Harding 511 listing and September Willamette-Building-over-Harding-Drug-Store evidence.

## No new demolition bridge found in the latest audit screens

Fresh July–August screening did not find a safe independent connection between the 10 May citywide Main Street demolition statement and 501/503/505/507/509/511. Keep `RL-038` open.

Relative-location controls encountered—such as E. B. Anderson Main near Sixth, M. E. Dunn next door to P.O., and Room 5 Willamette Building—remain relative/building-name evidence unless an exact-number source bridges them.

## Known synchronization cleanup

Some older summary text predates the later March 1912 Palace Saloon visual review:

- the earlier target-status paragraph inside `evidence/source-captures/1912-main-street-research.md` still says 501 was unresolved, but the later March 19 integration in the same file and `E-104` / `S-118` supersede that statement;
- the 1912 section of `maps/sanborn-comparison-503-505-507.md` also still contains an older sentence saying 501 was unresolved.

Current timeline/evidence and `E-104` / `S-118` control. Reconcile those stale summary sentences during the next safe synchronized integration; do not undo newer parallel map/source work to make the edit.

## Exact resume sequence

1. Sync newest `main` and inspect new parallel commits.
2. Re-read current policies and `registers/year-status.md`.
3. Continue the 1912 title → issue → page ledger and scan review from the newest audit checkpoints on `main`.
4. Visually certify the 19 Jan Courier p8 Harding-drugstore staffing lead if a faithful scan can be retrieved.
5. Continue Courier page-count reconciliation and visual review.
6. Continue Morning Enterprise July/August ledger and then remaining months.
7. Continue Oregon City Enterprise weekly ledger.
8. Keep target screening running during the visual pass: 501/503/505/507/509/511, Post Office cluster, Smith, Young, Harding, Chicago Store, Brightbill, Gambrinus, Schrader, construction, demolition, fire, repair, moves, excavation, old/new buildings, contractors, and property sales.
9. Audit other required online source classes after newspaper coverage.
10. After reasonable online recovery attempts, convert only persistent inaccessible pages/sources into precise numbered manual callouts.
11. Update related evidence/source/timeline/building/business/person/map/YAML records for any genuinely new verified findings.
12. Run `python3 scripts/validate_archive.py` or verify the equivalent GitHub validation workflow after meaningful writes.
13. Keep **1912 = IN PROGRESS** until every requirement for ONLINE COMPLETE is actually satisfied.

## Evidence-handling reminders

- OCR/search is discovery only; scan inspection controls visual certification.
- Failed retrieval is a retrieval gap, never negative evidence.
- Address occupancy is not building continuity.
- Relative location is not an exact numbered address.
- Do not merge people or businesses by name alone.
- Preserve conflicts and rejected interpretations.
- Do not send institutional/manual research requests unless the project steward explicitly authorizes them.
