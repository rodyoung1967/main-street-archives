# 1916 Enterprise annual-audit conversation handoff — 12 September 2026

## Purpose

Continue the exhaustive 1916 Oregon City Enterprise visual audit for the 503/505 Main Street research project without redoing certified work or overstating source silence.

Treat current `main` as authoritative. Before any new work, fetch/sync newest `main`, read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely, then review the newest 1916 commits/checkpoints. Do not reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work.

Original archival scans must be visually inspected whenever accessible. OCR/text extraction is discovery/navigation only and never substitutes for visual certification. Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, addresses, and physical-building facts separate. No-hit language is bounded coverage only and is never evidence of vacancy, closure, non-use, demolition, or non-ownership.

## Starting state inherited into this conversation

Canonical earlier handoff: `evidence/source-captures/2026-09-12-1916-june16-june23-conversation-handoff.md` at commit `f79d161d057e9aec1e29e581889d10ed11a071bc`.

June 16 and June 23 had already been integrated at `285d81d2c15d81e68e0a67da4edfdd745815dc92`. June 30 and July 7 were then visually reviewed and ultimately integrated after fixing a normalization mismatch. Their certification commit is `0a53748db5da820c2233c3cee4c4cae5f664cace`.

After June 30 / July 7 integration the canonical newspaper checkpoint was:

- Courier: **458/458 visually reviewed — complete**.
- Enterprise: **225/426 certified weekly pages through 7 July 1916**.
- Combined newspaper coverage: **683/884 certified**.
- **201 Enterprise pages remained uncertified**.
- The true weekly **12 May 1916 page 8 remains an explicit RETRIEVAL GAP**. The delivered sequence 8 is visibly *Morning Enterprise* and must not be counted as the genuine weekly page 8.
- Next ordinary issue at that point was 14 July 1916.

## 14 July 1916 — completed visual review

Original page PDFs were fetched from Historic Oregon Newspapers via repository workflow, sequences were probed beyond the expected count, and **8/8 genuine weekly pages were visually inspected** from rendered originals.

Source capture: `evidence/source-captures/1916-enterprise-july14-visual-review-2026-09-12.md`.

Commit documenting review: `22186d6e8d7163df276fe6f8f4da1bc5f5dd4553`.

Verified findings:

- No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, closure, vacancy, fire, demolition, or move to **501, 503, 505, 505½, or 507 Main Street**.
- **Page 4:** a city-improvements summary lists **Mrs. Mary E. Barlow and J. W. David, Main Street, between Fifth and Sixth streets**, for **improvements to a store building; cost $500**. This is valuable same-block physical-building context, but the scan prints no exact street number, so it must not be assigned to 501/503/505/505½/507 without an independent address bridge.
- **Page 4:** **Mrs. M. L. Foster, Fifth and Main streets**, improvements costing $800. Again, no target street number.
- **Page 3:** **A. H. Buckles, grocer, Eleventh and Main** — explicit non-target control.
- **Page 5:** **Larsen & Co., Corner 10th and Main Streets** — explicit non-target control.

## 21 July 1916 — completed visual review

Original PDFs were fetched and **8/8 genuine weekly pages were visually inspected**.

Source capture: `evidence/source-captures/1916-enterprise-july21-visual-review-2026-09-12.md`.

Commit documenting review: `d60c70ec23afe1735f45904db815ed67f0866530`.

Verified findings:

- No inspected page directly assigns a target-premises occupant, proprietor, business owner, property owner, tenant, licensee, trade name, transfer, closure, vacancy, fire, demolition, or move.
- **Page 1:** article **“Federal Building For Oregon City Now Seems Near.”** Congress had included **$75,000** in an omnibus appropriation bill for purchase of a site and erection of a suitable federal building in Oregon City. Postmaster **J. J. Cooke** had prepared reports concerning available sites and probable costs of several tentative locations. The article does **not identify any site by street address, intersection, owner, legal description, or existing building**. It is useful federal-building chronology only and cannot be connected to 501–507 Main from this evidence.
- The article mentions possible federal uses including post office/rural delivery, federal courtroom, locks engineering/executive offices, forest-service headquarters, and federal agricultural work. It does not establish acquisition, selected site, construction commencement, or target-block location.
- A later parallel commit `0f04e224243cc1d5fb72ecdcfc61d468611a2a40` added July 21 Portland House ownership/lease context. Review current main before relying on its exact wording.

## July 14 / July 21 integration state

An integration workflow/script was created. The first run failed because its checkpoint string assumptions were stale, not because of evidence or validator failure. The failure was specifically an expected-string mismatch against the live checkpoint wording.

Corrections were committed in:

- `c9786e03b634bceef32916af379840f73a237ff1` — Fix July 14/21 checkpoint integration normalization.
- `63e334e7b7dae037907c8100baf4e4d095be88cd` — Run corrected July 14/21 integration.
- `30cb039e1fe594cc1365613b5b3a335a1d126bf3` — Normalize July 14/21 checkpoint next-issue wording.

The intended post-integration counts in the script are **241/426 Enterprise**, **699/884 combined**, **185 Enterprise pages remaining**, with **28 July 1916** as the next ordinary issue. Because parallel work was still landing during this conversation, do not assume those counts from this handoff alone: fetch current main and read `evidence/source-captures/1916-online-audit-checkpoint.md` and `registers/year-status.md` before continuing.

## 28 July 1916 — completed visual review now on main

A new fetch workflow preserved the original scans for 28 July and 4 August. Preservation commit: `d1916ebd6f330649ee2318c84767225cd679d69d`.

Current main at handoff time already contains a complete 28 July source capture:

`evidence/source-captures/1916-enterprise-july28-visual-review-2026-09-12.md`

Commit: `a07b1204a3321a12b4803e20a99d6d51c2f479ae` — **Document July 28 1916 Enterprise visual review**.

That commit records **8/8 genuine weekly pages visually inspected** and these bounded findings:

- No source-explicit target-premises event for 501/503/505/505½/507 Main.
- **Page 1:** automobile collision at **Tenth and Main** — exact non-target spatial control.
- **Page 5:** recurring **Larsen & Co., Corner Tenth and Main Streets** advertisement — exact non-target business-location control.

Do not infer anything about vacancy or target occupancy from this no-hit.

## 4 August 1916 — scans preserved; review was not completed in this conversation

The fetch workflow for 28 July / 4 August completed successfully and uploaded/preserved the originals. Repository directory:

`newspapers/oregon-city-enterprise/1916/1916-08-04/`

Artifact used during this conversation: `1916-enterprise-july28-aug04-visual-bundle` (artifact ID `10309499691`; artifact retention is temporary, but committed repository PDFs are authoritative).

The visual review of 4 August was **not completed before the user requested a knowledge checkpoint**. Therefore, on resume:

1. Sync current main first and check whether parallel work has already produced a 4 August visual-review source capture and integration.
2. If not, render and visually inspect **every genuine 4 August page** from the committed original PDFs. Do not rely on OCR alone.
3. Probe/confirm issue page count from the preserved fetch manifest and archive metadata before certifying.
4. Preserve any source-explicit target or same-block facts with the standard distinctions and uncertainty controls.
5. Integrate the certified review into source/evidence registers, database YAML, `1916-online-audit-checkpoint.md`, and `registers/year-status.md` only after visual review.
6. Run `python3 scripts/validate_archive.py` before and after meaningful writes; validator must pass.

## Current main at checkpoint

At the moment this handoff was prepared, `main` pointed to:

`a07b1204a3321a12b4803e20a99d6d51c2f479ae` — **Document July 28 1916 Enterprise visual review**.

Parallel work may advance main immediately after this file is committed. Always fetch newest main and inspect later commits before acting.

## Exact resume instruction

**Add any new information to the repo, then continue through the next unresolved Enterprise date(s). All accessible original newspaper scans must be visually verified. Start by checking whether 4 August 1916 is already reviewed/integrated on current main. If not, finish 4 August. Then proceed chronologically to the next ordinary unresolved issue. Keep the 12 May true weekly page-8 retrieval gap open unless genuinely recovered. Validate after writes. Do not send institutional/manual requests, authorize fees, or purchase records without explicit user approval.**
