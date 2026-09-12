# 1916 Enterprise June 16 / June 23 conversation handoff — 12 September 2026

## Purpose

Resume the exhaustive 1916 Oregon City Enterprise annual visual audit exactly where this conversation stopped. The active dates are **16 June 1916** and **23 June 1916**. The project steward explicitly requested: **add any new information to the repo, continue through the next two unresolved dates, and visually verify all scans.**

## Mandatory startup / repository rules

1. Fetch/sync the newest `main` first and treat current `main` as authoritative.
2. Do not reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work.
3. Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely before resuming research/integration.
4. Read `/home/oai/skills/pdfs/SKILL.md` before PDF work.
5. Original scans are the visual-review authority. OCR/text extraction/search is discovery/navigation only and does not certify a page.
6. Preserve uncertainty and retrieval gaps. A no-hit is bounded coverage only, never evidence of vacancy/non-use/closure/demolition.
7. Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, addresses, and physical buildings separate.
8. Keep Markdown registers and YAML/database mirrors synchronized.
9. Run `python3 scripts/validate_archive.py` after writes and verify the literal output `Validation passed.` before final push. Pull/rebase latest `main` and validate again immediately before push.
10. Do not contact institutions, send requests, purchase records, authorize fees, or perform manual outreach without explicit project-steward authorization.

## Last completed annual checkpoint before this batch

Before starting June 16/23, canonical 1916 status was:

- Courier: **458/458 visually reviewed — complete**.
- Enterprise: **193/426 certified visually reviewed pages through 9 June 1916**.
- Combined certified newspaper coverage: **651/884**.
- Enterprise pages still uncertified: **233**.
- The genuine weekly Enterprise page 8 for **12 May 1916** remains an explicit **RETRIEVAL GAP**. The archive's sequence 8 is visibly a *Morning Enterprise* page. Bounded alternate-edition/title recovery attempts were already exhausted. Do not count it as reviewed and do not convert it into negative evidence.
- Next ordinary unresolved issue was 16 June 1916.
- Last completed integration commit before this batch: `0913b8cc` — `Certify June 2 and June 9 1916 Enterprise reviews`.

## Work completed in this conversation for June 16 / June 23

### Fetch workflow

Created and pushed:

- `.github/workflows/fetch-1916-enterprise-june16-june23.yml`
- creation commit: `ae356369db419b6739ea61fbc5a1e5d053ae15bd` — `Add June 16/23 1916 Enterprise fetch workflow`

GitHub Actions fetch run:

- run ID: `34709147125`
- job ID: `103594579897`
- conclusion: **success**
- artifact: `1916-enterprise-june16-june23-visual-bundle`
- artifact ID: `10302094478`
- artifact SHA-256: `ec140500c2856cb3d29742c3d806b21744c5ef1587a4c692ba2c347cd6961c50`
- artifact contained 18 files: 8 PDFs + manifest for each issue.

The workflow synced current main and ran the full archive validator before and after retrieval. Both printed:

```text
Main Street Archive Validation
========================================

Validation passed.
```

The workflow then committed and pushed all retrieved originals:

- commit: `dce98ef0` — `Preserve Enterprise June 16 and June 23 1916 scans`
- 18 files added.
- Validator ran again immediately before that push and printed `Validation passed.`

Canonical source directories now preserved on `main`:

- `newspapers/oregon-city-enterprise/1916/1916-06-16/`
- `newspapers/oregon-city-enterprise/1916/1916-06-23/`

Each directory contains pages 1–8 plus `fetch-manifest.json`. The fetch attempted sequences 1–14; **8 valid PDF pages were saved for each date**. Thus each issue currently has an 8-page delivered set.

### Local review bundle

The Actions artifact was downloaded during the conversation to:

- `/mnt/data/1916-enterprise-june16-june23.zip`

It was unpacked/rendered under:

- `/mnt/data/june16_june23_review/`
- rendered page images under `/mnt/data/june16_june23_review/renders/`

All 16 original PDFs were rendered to page images. During the conversation, all eight June 16 page images and all eight June 23 page images were individually opened/displayed for visual inspection. Several pages/crops were reopened at higher attention, including:

- June 16 p1
- June 16 p2
- June 16 p3
- June 16 p4
- June 16 p5
- June 16 p6
- June 23 p1
- June 23 p2
- June 23 p3
- June 23 p4
- June 23 p5
- June 23 p6
- June 23 p7
- June 23 p8

Additional crops created locally included `june16_right_article.png`, `june16_main_realty.png`, and `june23_hawley.png` for closer reading.

**Important certification boundary:** although all 16 page scans have been rendered/opened visually, the conversation was interrupted before the substantive page-by-page screening, notes, source captures, register/YAML integration, updated counts, and final certification were completed. Therefore **do not yet mark June 16 or June 23 as certified in the annual ledger solely from this handoff**. Resume by rechecking each page image/source, finish the historical screening, then certify the two issues only after the reviewer is satisfied that every page has been visually inspected for the target categories.

## Target screening to finish

For every page of both issues, screen visually for:

- exact target addresses: 501, 503, 505, 505½, 507 Main (and neighboring address anchors where useful);
- Harding / George A. Harding;
- Young and known target-associated people;
- Chicago Store, Palace Saloon, Schrader and other established early target businesses;
- Jones Drug / Burmeister & Andresen relocation chain from late May / 2 June;
- Oregon City post-office / federal-building/site material;
- pool room / pool hall / billiards / cigar / liquor-license material;
- real-estate transfers, legal descriptions, Block 4 / lot controls, sales, leases, moves, vacancies;
- fires, construction, demolition, rebuilding, remodeling, structural change;
- Main Street / Fifth Street location anchors that could independently bridge an unnumbered business to the target frontage.

Use OCR/pdftotext only after visual review to locate difficult text. Any exact-address or material claim discovered in OCR must be checked against the visible original before integration.

## Existing 1916 controls that remain in force

- 24 Mar 1916 Enterprise p1 Oregon City federal-post-office proposal: one-story, ~4,800 sq ft, $55,000 building + $10,000 site; no site/address/acquisition/construction/move proof.
- 5 May 1916 Enterprise p4 federal-building prospects: Treasury estimate $70,000 building+site and $15,000 site, arithmetically implying $55,000 building component; still no target-site bridge.
- 21 Apr post-office site article is Estacada, not Oregon City.
- 28 Apr new-site/lease article concerns Oregon Portland Railway, Light & Power Co. near Parkplace, not target property.
- 19 and 26 May Harding quiet-title material concerns Lots 1 and 2, Block 11, Oregon City — explicitly non-target, not Block 4.
- 26 May Enterprise p8 Jones Drug Company `Forced-Out-of-Location Sale`: landlord wants more room; Jones says it will move to the present Portland Railway Light & Power Co. room, two doors south; old location next to Burmeister & Andresen. No exact target street number; do not map this chain to 501/503/505/507 without an independent address bridge.
- 2 Jun Enterprise p1: `EXPANSION OF BURMEISTER & ANDRESEN WILL CAUSE GENERAL SHIFTING.` Seven firms will move so Burmeister & Andresen can expand. No target street number. Context only, not a target-address bridge.
- 9 Jun complete issue gave no target event or exact-address bridge.
- 24 Mar 1912 Morning Enterprise p2 pool-hall license notice visibly signs `H. H. SMTHI`; do not normalize that signature to Smith without independent evidence.

## What has NOT yet been done for June 16 / June 23

Do not assume any of the following are complete:

- no final source capture for June 16;
- no final source capture for June 23;
- no June 16/23 source-register entries;
- no June 16/23 evidence-register entries;
- no YAML mirrors for those entries;
- no annual-status/checkpoint count update for these 16 pages;
- no final propagation audit across timeline/building/business/person/open-question/research-lead/crosswalk records;
- no final integration commit certifying the two issue dates.

The raw scans themselves **are** safely preserved on main at `dce98ef0`.

## Expected IDs / counts — verify before using

At the prior checkpoint the newest entries were S-338/S-339 and E-311/E-312. If no parallel work has consumed IDs, June 16/23 would likely use **S-340/S-341** and **E-313/E-314**, but **re-fetch current main and check the actual next IDs before assigning anything**.

If, after final review, both 8-page issues are certified and no parallel status changes occurred, the arithmetic would become:

- Enterprise: 193 + 16 = **209/426 certified**
- Combined: 651 + 16 = **667/884 certified**
- Enterprise remaining uncertified: 426 - 209 = **217**
- next ordinary unresolved Enterprise issue: **30 June 1916**

These are provisional arithmetic only. Confirm current main, actual page counts, and certification before writing them into canonical status files. The 12 May true weekly p8 retrieval gap remains carried separately.

## Exact resume sequence

1. Fetch/sync newest `main`; inspect commits after `dce98ef0` for parallel work.
2. Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md` completely.
3. Read `/home/oai/skills/pdfs/SKILL.md`.
4. Confirm the preserved June 16/23 source directories and manifests.
5. Re-render/reopen originals if the local `/mnt/data` review bundle is unavailable in the new chat. Do not rely on this handoff as a substitute for seeing the scans.
6. Finish page-by-page visual screening of all 8 June 16 pages and all 8 June 23 pages. Reopen any ambiguous page/crop at higher resolution.
7. Only after visual screening, use text extraction/search as secondary discovery/deciphering aid and visually verify any candidate claim.
8. Write separate source captures for June 16 and June 23 documenting page count, visual status, findings/no-hit limits, and propagation decisions.
9. Add source/evidence register entries and synchronized YAML mirrors using IDs confirmed from current main.
10. Update `registers/year-status.md` and `evidence/source-captures/1916-online-audit-checkpoint.md` with actual certified counts.
11. Audit timeline, buildings, businesses, people, open questions, research leads, crosswalk, and database/YAML records. If the batch is only bounded no-hit coverage, explicitly say no entity/timeline propagation was warranted rather than manufacturing a historical event.
12. Run `python3 scripts/validate_archive.py` and require literal `Validation passed.`
13. Commit meaningful integration changes. Before final push, pull/rebase latest `main`, resolve only by preserving newer parallel work, rerun the validator, then push.
14. Report the final integration commit, exact issue/page certification, material findings, updated coverage counts, carried May 12 gap, and next ordinary unresolved date.

## Project-steward continuation instruction

After finishing and saving June 16 and June 23, the user's standing cadence is to continue chronologically through unresolved dates when requested. Do not skip the 12 May retrieval gap conceptually; carry it explicitly while continuing ordinary issue dates. No institutional/manual request should be sent without explicit authorization.
