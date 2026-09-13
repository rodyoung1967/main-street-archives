# Conversation handoff — 1916 Enterprise audit at 25 August / 1 September

Date: 12 September 2026 (Pacific time)

Status: **IN PROGRESS**

Repository: `rodyoung1967/main-street-archives`, branch `main`

This handoff preserves the exact state of the 1916 annual audit at the point the project steward paused the conversation. It is intentionally conservative: it does **not** certify pages that were only inspected at contact-sheet scale or through OCR/text extraction.

## Mandatory restart rules

Before doing any new research or repository changes in the next chat:

1. Fetch/sync the newest `main` and treat current `main` as authoritative.
2. Do **not** reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work.
3. Read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely from the current repository.
4. Review the newest relevant commits/checkpoints before continuing.
5. Visually inspect original archival scans whenever accessible. OCR/search text is discovery only.
6. Preserve uncertainty and retrieval gaps.
7. Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, addresses, and physical buildings separate.
8. Commit meaningful verified findings to current `main` and run `validate_archive.py` after writes.
9. Do not send institutional requests, purchase records, authorize fees, or perform manual outreach without explicit project-steward approval.
10. A no-hit is a coverage statement only, never evidence of vacancy, closure, demolition, relocation, or non-use.

## Current authoritative checkpoint

At the start of this work, `evidence/source-captures/1916-online-audit-checkpoint.md` reported:

- *Oregon City Courier*: **458/458 visually reviewed — complete**.
- *Oregon City Enterprise*: **273/426 certified weekly pages through 18 August 1916**.
- Combined certified coverage: **731/884**.
- Enterprise pages remaining uncertified: **153**.
- The true 12 May 1916 weekly page 8 remains a **RETRIEVAL GAP**; the archive-delivered sequence 8 is visibly *Morning Enterprise* and is not the missing weekly page.
- The next ordinary unreviewed Enterprise issue is **25 August 1916**.
- 1916 remains **IN PROGRESS / NOT ONLINE COMPLETE**.
- Other outstanding year-closeout work includes the 1916–1917 Sohns & Woodbeck directory, any non-digitized 1916 *Morning Enterprise* material, other online source classes, and final manual-work reconciliation.

Do not replace these counts until the August 25 / September 1 pages are individually visually certified and integrated.

## Latest repository state seen before pause

Latest `main` commit checked immediately before this handoff:

- `402c4bd410ffe9bb9adb3fa895bbbb7238f04507`
- Commit message: `Preserve Enterprise August 25 and September 1 1916 scans`
- Commit timestamp: `2026-09-13T02:51:45Z`
- Parent: `6a41233ba2cab30fe117f0f504a521d80f7f5dcc`

That commit preserved original scans and fetch manifests for both issues:

- `newspapers/oregon-city-enterprise/1916/1916-08-25/1916-08-25-page-1.pdf` through page 8
- `newspapers/oregon-city-enterprise/1916/1916-08-25/fetch-manifest.json`
- `newspapers/oregon-city-enterprise/1916/1916-09-01/1916-09-01-page-1.pdf` through page 8
- `newspapers/oregon-city-enterprise/1916/1916-09-01/fetch-manifest.json`

The scans are preserved; **the two issues are not yet certified in the 1916 ledger**.

## Source-recovery / artifact provenance

The scan bundle came from GitHub Actions workflow:

- Workflow: `Fetch 1916 Enterprise August 25 and September 1 visual bundle`
- Workflow file: `.github/workflows/fetch-1916-enterprise-aug25-sep01.yml`
- Run ID: `34734039857`
- Conclusion: success
- Artifact ID: `10309974579`
- Artifact name: `1916-enterprise-aug25-sep01-visual-bundle`
- Artifact SHA256: `e02e1b906c772f88492076e39c469924f2a8c91661c6418f17f7671b9ba02979`

Local working copy during this conversation:

- `/mnt/data/1916-enterprise-aug25-sep01.zip`
- extracted under `/mnt/data/aug25sep01/`
- rendered page JPEGs under `/mnt/data/aug25sep01/jpg/1916-08-25/` and `/mnt/data/aug25sep01/jpg/1916-09-01/`
- contact sheets:
  - `/mnt/data/aug25sep01/1916-08-25-contact.jpg`
  - `/mnt/data/aug25sep01/1916-09-01-contact.jpg`

These local paths are ephemeral and should not be relied on in a new chat. The repository PDFs are canonical.

## Visual-review work completed in this conversation

All sixteen PDFs were rendered to faithful page images at 110 dpi and both eight-page contact sheets were visually opened. This established that each preserved issue contains eight readable newspaper scans and allowed a first-pass page-level orientation.

However, **contact-sheet inspection is not being treated as full page certification** because much of the newspaper text is too small at that scale. Individual page images still need to be opened/zoomed as needed before marking 8/8 visually verified.

### 25 August 1916 — initial visual orientation

The contact sheet showed the normal eight-page weekly issue structure:

- page 1: general local/national news
- page 2: county/Candy-area material
- page 3: farm/garden material
- page 4: editorial page
- page 5: local briefs/legal/local stories; Larsen & Company advertisement visible in lower left
- page 6: Oswego Record
- page 7: legal/classified/professional material
- page 8: local news/roads/Hawley material

No obvious exact 501/503/505/505½/507 Main target event was visible at contact-sheet scale. This is **not** yet a certified no-hit.

### 1 September 1916 — initial visual orientation

The contact sheet likewise showed eight scanned pages:

- page 1: local/national news
- page 2: county/Candy-area material
- page 3: farm/garden material
- page 4: editorial page
- page 5: local briefs; Larsen & Company advertisement visible
- page 6: Oswego Record
- page 7: legal/classified/professional material
- page 8: local/news material

No obvious exact 501/503/505/505½/507 Main target event was visible at contact-sheet scale. This is **not** yet a certified no-hit.

## OCR/text discovery already performed

After the contact-sheet visual pass, `pdftotext -layout` was run across all sixteen PDFs and searched for discovery terms including:

`503`, `505`, `507`, `509`, `511`, `Main Street`, `Fifth and Main`, `Harding`, `Brightbill`, `Bradley`, `Raasch`, `Lamb`, `Young`, `Smith`, `Chicago Store`, `Palace`, `Schrader`, `Portland House`, `Foster`, and `Beck`.

The OCR output included many false or bare-number hits and must not be treated as evidence without checking the scan.

One useful bounded control from the 1 September page-7 OCR is the professional-directory wording referring to the **Fashion Stable, between Fourth and Fifth on Main Street**. If visually confirmed on the scan, this is south of the Fifth–Sixth target block and should remain a non-target geographic control, not a target-address finding.

## Exact next action — do not restart earlier issues

Resume **inside the 25 August / 1 September review** rather than starting over at an earlier date.

1. Use OCR/text only to prioritize candidate pages and phrases.
2. Open the **individual original page renderings/scans** for every candidate and inspect at readable zoom.
3. Ensure the remaining non-candidate pages are also meaningfully visually inspected, page by page, before certification.
4. Screen every page for:
   - 501 / 503 / 505 / 505½ / 507 / 509 / 511 Main
   - Fifth and Main / Main between Fifth and Sixth
   - Harding, Brightbill, Bradley, Raasch, Lamb, Young, Smith
   - Chicago Store, Palace Saloon, Schrader
   - Portland House, Foster, Beck
   - fires, construction, demolition, rebuilding, remodeling, sales, leases, moves, ownership, tenancy, licensing, and public works affecting the target block
5. Preserve exact wording, page number, and visual-verification status for anything material.
6. Do not infer target identity from a bare street number or generic `Main Street` reference.

## Required repository integration after visual certification

If both issues prove 8/8 visually verified:

- create a visual-review capture for 25 August 1916;
- create a visual-review capture for 1 September 1916;
- re-fetch and update `evidence/source-captures/1916-online-audit-checkpoint.md`;
- re-fetch and update `registers/year-status.md`;
- add/synchronize source and evidence records using the **next currently free IDs** after checking current `evidence/source-register.md`, `evidence/evidence-register.md`, `database/sources.yml`, and `database/evidence.yml`;
- perform the cross-record propagation audit required by `AGENTS.md`.

If there are no target-address findings, say so only as bounded coverage and explicitly record that no new occupant/business/ownership/building fact is being manufactured.

If both eight-page issues become certified with no parallel work changing the earlier totals, the arithmetic would become:

- Enterprise: **289/426 certified**
- Combined: **747/884 certified**
- Enterprise pages remaining uncertified: **137**
- next ordinary unreviewed Enterprise issue: **8 September 1916**

These are **prospective counts only** until the two issues are actually certified and the current checkpoint is re-fetched immediately before writing.

## User's instruction at interruption

The project steward's active instruction immediately before requesting this handoff was:

> Add any new info to the repo then Continue through the next two unresolved dates. All scans should be visually verified.

Interpretation for the next chat:

- First finish and integrate **25 August 1916** and **1 September 1916**, because work on those scans is already in progress but not yet certified.
- Then continue through the **next two unresolved ordinary Enterprise dates** shown by the current ledger after integration. If no parallel work has changed the sequence, those should be **8 September 1916** and **15 September 1916**.
- All scans for those dates must be visually inspected page by page before counting them as complete.
- Save verified findings and no-hit coverage to the repository and run validation after writes.

## Earlier certified Enterprise sequence immediately preceding this handoff

Do not redo these unless current `main` shows a correction is needed:

- 16 June 1916 — 8/8 visually verified
- 23 June 1916 — 8/8 visually verified
- 30 June 1916 — 8/8 visually verified; no target-address event; H. P. Brightbill described as a Main Street grocer without exact target address
- 7 July 1916 — 8/8 visually verified; no target-address event
- 14 July 1916 — 8/8 visually verified; page 4 reports Mrs. M. U. Foster, Fifth and Main, improvements to Portland House ($800), and Mrs. Mary E. Barlow / J. W. David, Main Street between Fifth and Sixth, store-building improvement ($500); the latter is block-bounded but not exact-address-specific
- 21 July 1916 — 8/8 visually verified; page 5 reports Minnie L. Foster as owner of Portland House, located on Main and Fifth, recently rebuilt; Frank Beck and Mark Beck held a three-year lease dating from 1 June 1916. Contextual only; no exact target-address bridge
- 28 July 1916 — 8/8 visually verified; no target event
- 4 August 1916 — 8/8 visually verified; no target event; Hawley construction between Fourth and Fifth is south of the target block
- 11 August 1916 — 8/8 visually verified; no target event; controls include Larsen & Co. at 10th/Main and other non-target Main references
- 18 August 1916 — 8/8 visually verified; no target event. Page 4 city-hall proposal concerns east side Main between Seventh and Eighth; page 7 includes `501 Division street` and Fashion Stable between Fourth and Fifth, useful controls showing why bare numbers / generic Main references cannot be assigned to target addresses

## Important project-wide interpretation controls

Continue to preserve these distinctions:

- The Wheel was at **503 Main**, never a 505 Main business.
- `The Wheel Tavern` was not an official business name.
- Farr/Harr/Well's/505 Tavern history belongs to **505 Main**; Flor/Remus/Kwality/Wheel history belongs to **503 Main**.
- A business name, liquor action, or operating reference does not by itself prove real-estate ownership.
- Same address across years does not prove same physical building.
- User-derived photo dating / sign readings remain comparative interpretations unless independently documented.

## Related unresolved project controls worth carrying forward

- 503 owner-date research remains a major focus, especially the Kwality → Wheel and Raye → Wiitanen business transition.
- 505 unresolved questions include who replaced Carl R. Harr, who operated `Well's Recreation`, who placed the 20 Nov. 1955 505 Main sale ad / phone 9179, who bought afterward, and when the `505 Tavern` name first appears.
- The user-derived building-replacement hypothesis currently brackets replacement of the earlier 503/505 buildings roughly to **1918–1922**, because the November 1922 photo appears to show the later buildings; this remains a hypothesis pending stronger direct structural evidence.
- Manual follow-ups such as MF-001, MF-048, MF-052, MF-053, MF-056 and other dashboard items remain unsent unless explicitly authorized.

## Stop condition for the resumed session

For the user's current request, the resumed session should not stop merely after retrieving scans or OCR. The requested unit of completion is:

1. finish page-by-page visual verification and integration of 25 August and 1 September 1916;
2. continue through the next two unresolved Enterprise dates in chronological order;
3. visually verify all retrieved scans for those two dates;
4. save all meaningful verified findings / bounded no-hit coverage to the repository;
5. update counts/checkpoints only from verified work;
6. run the archive validator after writes;
7. report the new next unresolved date and whether 1916 remains IN PROGRESS.
