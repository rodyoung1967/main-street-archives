# 1921 annual audit conversation handoff — 2026-09-20

## Purpose

This handoff preserves the exact state of the 1921 annual newspaper audit so the next chat can continue from current `main` without restarting completed work or overstating completion.

Treat current `main` as authoritative. Before continuing:
1. fetch/sync newest `main`;
2. read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely;
3. review the newest 1921 source captures, annual-status records, newspaper ledgers, and commits after this handoff;
4. do not reset/revert/overwrite newer parallel work;
5. use OCR/search only for discovery and visually inspect original scans for verification;
6. run `scripts/validate_archive.py` when practical, but note the current validator blocker recorded below.

## Current annual status

**1921 remains IN PROGRESS.**

The weekly **Oregon City Enterprise** run has been worked through January–December 1921. The intended year total is **52 weekly issues / 416 pages**.

However, 1921 must **not** be marked ONLINE COMPLETE yet because the separate **Morning Enterprise** daily newspaper also existed in 1921 and still requires:
- a complete 1921 issue/page inventory;
- acquisition of every online-retrievable issue/page;
- page-by-page visual inspection;
- investigation/integration of relevant hits;
- explicit retrieval-gap/manual-callout treatment where needed.

The next major workstream is therefore **January 1921 Morning Enterprise**, then continue chronologically through the daily run.

## Weekly Oregon City Enterprise coverage

The weekly audit used an expanded search scope:
- entire 500 block of Main Street;
- especially 501, 503, and 505 Main;
- occupants and business names;
- business ownership vs. property ownership;
- tenancy and leases;
- property sales/transfers;
- demolition, construction, rebuilding, remodeling;
- fires/damage;
- openings, closings, and relocations;
- adjacent businesses when useful for frontage/building continuity.

Negative/no-hit reviews are coverage controls only and are **not** evidence that no change occurred.

### January 7
- 8/8 pages reviewed.
- No new direct 501/503/505 fact.
- Page 8 contains Main Street merchants between Sixth and Eighth organizing a protective/night-police time-clock system; this is north of the target 500 block and is only a spatial control.
- Capture: `evidence/source-captures/2026-09-19-1921-annual-audit-kickoff-jan07-visual-review.md`

### January 14, 21, 28
- 24/24 pages reviewed.
- No new direct target fact.
- January 14 has a local mention of “C. G. Miller”; insufficient to identify Gilbert Miller or connect him to 503.
- January 28, page 8, “B. & A. Picture Display Viewed With Interest,” is an important photo-provenance lead. George Hankins arranged a Burmeister & Andresen display of historical Oregon City photographs loaned by Mrs. Anne Jones, Robert Wilson, Mrs. W. E. Pratt, Weldon Fuge, the Miller family through Miss Rose Miller, the city, and the publicity department. This does **not** prove any image depicts 503/505 or the 500 block.
- Capture: `evidence/source-captures/2026-09-20-1921-enterprise-jan14-28-visual-review.md`

### February–July
Standalone monthly/batch captures exist in `evidence/source-captures/`:
- `2026-09-20-1921-enterprise-feb04-18-visual-review.md`
- `2026-09-20-1921-enterprise-feb25-mar11-visual-review.md`
- `2026-09-20-1921-enterprise-mar18-25-visual-review.md`
- `2026-09-20-1921-enterprise-april-visual-review.md`
- `2026-09-20-1921-enterprise-may-visual-review.md`
- `2026-09-20-1921-enterprise-june-visual-review.md`
- `2026-09-20-1921-enterprise-july-visual-review.md`

No new sufficiently specific 500-block fact was promoted from these batches.

Useful completion commits visible on current history:
- May completion: `64011b3189dc800571a55350600911a468f039f3`
- June completion: `ec0fd6da222d0d1d5bcfc563afdc1de09d8c1311`
- July completion: `3840b7fa0b294a89431b904a5c085b1248baddde`

### August
- Render workflow committed: `22c45fbd42854aad199dcc5e575cf194e4132201`
- Artifact was produced for Aug. 5, 12, 19, 26: 32 pages total.
- Conversation state recorded the month as reviewed with no new sufficiently specific 500-block fact.
- **Repository reconciliation note:** as of this handoff, no standalone August visual-review capture is present in `evidence/source-captures/`. Before relying on August as a formally documented completed month, reconcile the review record against available renders/artifacts and create the missing capture if warranted.

### September
- Render workflow commit: `3dd0f4c28845e153d45d14f7ae3fd3930064193a`
- Completion commit: `35eef072a64c8167b93020cc38642f0ff92d2f7e`
- Standalone capture exists: `evidence/source-captures/2026-09-20-1921-enterprise-september-visual-review.md`
- 5 issues / 40 pages.
- No new sufficiently specific 500-block fact.

### October
- Render workflow committed: `fc0f5bb0c30b21fb75546578e57c3b326700d742`
- Artifact was produced for Oct. 7, 14, 21, 28: 32 pages.
- Conversation state recorded the month as reviewed with no new sufficiently specific 500-block fact.
- **Repository reconciliation note:** no standalone October visual-review capture is present as of this handoff.

### November
- Render workflow committed: `c090b852542b4ea36a64a06aa43918887f65b759`
- Artifact was produced for Nov. 4, 11, 18, 25: 32 pages.
- Conversation state recorded the month as reviewed with no new sufficiently specific 500-block fact.
- **Repository reconciliation note:** no standalone November visual-review capture is present as of this handoff.

### December
- Render workflow committed: `4eaef9e033b70a6fc217329c1fa19a8c41d8b266`
- Artifact was produced for Dec. 2, 9, 16, 23, 30: 40 pages.
- Conversation state recorded the month as reviewed with no new sufficiently specific 500-block fact.
- **Repository reconciliation note:** no standalone December visual-review capture is present as of this handoff.

## Weekly-run summary

Working conversation tally:
- 52 weekly issues
- 416 pages
- January 7 through December 30, 1921
- no new securely attributable 501/503/505/500-block chronology fact from the weekly run beyond the photo-provenance and spatial-control leads noted above.

Because August, October, November, and December do not currently have standalone visual-review source captures, the next chat should reconcile those records before treating the weekly-run completion as fully repository-audited.

## Next research action: Morning Enterprise

Build the complete **1921 Morning Enterprise** daily source universe and start with **January 1921**.

Required workflow:
1. establish the exact daily issue inventory and expected page counts for January;
2. identify missing/misdated/duplicate issues before review;
3. acquire/render all online-retrievable pages;
4. visually inspect every page individually;
5. search the same expanded 500-block scope used for the weekly Enterprise;
6. investigate any hit in original context and distinguish direct evidence from inference;
7. save a source capture for the completed batch;
8. propagate qualifying facts to building/business/person/timeline records;
9. update annual progress without calling 1921 ONLINE COMPLETE prematurely;
10. continue month by month.

Do not stop after rendering. Finish acquisition → visual review → investigation → repo capture before reporting a batch complete unless there is a real blocker.

## Important mistake immediately before this handoff

The user said “Do January” after the 1921 weekly Enterprise year was completed. That should have been interpreted as **January 1921 Morning Enterprise**.

Instead, a workflow was mistakenly created for **January 1922 Oregon City Enterprise**:
- commit: `9af19a8aa37210231c5a5b7f73992875b98bf0c4`
- workflow: `.github/workflows/render-1922-january-enterprise.yml`
- the render workflow completed successfully.

Do **not** treat that as the next step in the 1921 audit. It may be useful later for the existing 1922 workstream, but it is outside the immediate 1921 task. Do not delete/reset it without checking newer work and project policy.

## Validator status / current blocker

The archive validator run associated with commit `9af19a8aa37210231c5a5b7f73992875b98bf0c4` failed.

This failure is **not caused by the new render workflow itself**. The validator traceback shows a YAML parse error in the people registry:
- parsing begins at `people:`
- failure reported around line 1308
- unexpected `- id: P-403`
- error: expected block end but found '-'

Treat this as a pre-existing/current-main repository integrity blocker to inspect carefully. Do not overwrite or “fix” it blindly because parallel work may own that file. Sync first and identify the newest commit touching the people registry before making any repair.

## Existing 1921-related source captures to review on restart

At minimum:
- `evidence/source-captures/2026-09-19-1921-annual-audit-kickoff-jan07-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-jan14-28-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-feb04-18-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-feb25-mar11-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-mar18-25-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-april-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-may-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-june-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-july-visual-review.md`
- `evidence/source-captures/2026-09-20-1921-enterprise-september-visual-review.md`

Also review any 1921 files/commits added after this handoff before resuming.

## Research standards reminder

- Preserve uncertainty.
- Do not use absence as proof.
- Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, addresses, and physical buildings separate.
- Visual verification controls promotion; OCR is discovery only.
- Do not send manual research requests or incur fees without authorization.
- 1921 remains **IN PROGRESS** until the entire online source universe, including Morning Enterprise, satisfies `RESEARCH-STANDARD.md`.
