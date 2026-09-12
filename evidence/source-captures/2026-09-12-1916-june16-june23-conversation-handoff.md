# 1916 Enterprise conversation handoff — through 23 June 1916 — 12 September 2026

## Resume instruction

Continue the exhaustive 1916 Oregon City Enterprise annual visual audit from current `main`. **June 16 and June 23 are complete, integrated, and certified. The next ordinary unresolved issue is 30 June 1916.** The project steward's standing cadence is: add new information to the repo, continue through the next two unresolved ordinary dates, and visually verify every delivered original scan before certification.

## Mandatory startup / repository rules

1. Fetch/sync newest `main` first; current `main` is authoritative.
2. Do not reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work.
3. Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely before research/integration.
4. Read `/home/oai/skills/pdfs/SKILL.md` before PDF work.
5. Original scans are the visual-review authority. OCR/text extraction/search is discovery/navigation only.
6. Preserve uncertainty/retrieval gaps. A no-hit is bounded coverage only, never evidence of vacancy, closure, non-use, demolition, or non-ownership.
7. Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, addresses, and physical buildings separate.
8. Keep Markdown registers and YAML/database mirrors synchronized.
9. Run `python3 scripts/validate_archive.py` after writes; require literal `Validation passed.`. Pull/rebase newest main and validate again immediately before final push.
10. Do not contact institutions, send requests, purchase records, authorize fees, or perform manual outreach without explicit project-steward authorization.

## Current canonical checkpoint

Current 1916 status after June 16/23 integration:

- Year status: **IN PROGRESS**.
- Total annual inventory: **104 issues / 884 pages**.
- Courier: **458/458 visually reviewed — complete**.
- Enterprise: **209/426 certified visually reviewed pages through 23 June 1916**.
- Combined certified newspaper coverage: **667/884**.
- Enterprise pages remaining uncertified: **217**.
- The genuine weekly Enterprise page 8 for **12 May 1916** remains an explicit **RETRIEVAL GAP**. Archive sequence 8 is visibly *Morning Enterprise*; bounded alternate-edition/title recovery attempts were already made. Carry the gap; do not count it as reviewed or use it as negative evidence.
- **Next ordinary unresolved Enterprise issue: 30 June 1916.**
- Other online source classes and final manual-callout reconciliation remain pending.

Canonical status file: `registers/year-status.md`.

## June 16 / June 23 acquisition and preservation

Fetch workflow:

- `.github/workflows/fetch-1916-enterprise-june16-june23.yml`
- workflow creation commit `ae356369db419b6739ea61fbc5a1e5d053ae15bd` — `Add June 16/23 1916 Enterprise fetch workflow`
- Actions run `34709147125`, job `103594579897`, conclusion **success**
- artifact `1916-enterprise-june16-june23-visual-bundle`, artifact ID `10302094478`
- artifact SHA-256 `ec140500c2856cb3d29742c3d806b21744c5ef1587a4c692ba2c347cd6961c50`
- raw-scan preservation commit `dce98ef0` — `Preserve Enterprise June 16 and June 23 1916 scans`

Each issue was probed through sequences 1–14. Sequences 1–8 were valid original PDFs; 9–14 returned 404. All 16 originals plus both fetch manifests are preserved under:

- `newspapers/oregon-city-enterprise/1916/1916-06-16/`
- `newspapers/oregon-city-enterprise/1916/1916-06-23/`

The fetch workflow ran the full archive validator before retrieval, after retrieval, and immediately before the scan-preservation push; each printed `Validation passed.`

## June 16 — completed visual review

Canonical source capture:

- `evidence/source-captures/1916-enterprise-june16-visual-review-2026-09-12.md`

Status: **VISUALLY VERIFIED — 8/8 genuine weekly pages inspected.** Every delivered PDF was rendered and the faithful page image individually visually inspected; OCR/text extraction was used only after visual review.

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

Material non-target control: **page 5**, headline `$30,500 MAIN STREET REALTY DEAL COMPLETED—NEW BUILDING MAY GO UP.` It concerns property on the **east side of Main Street between Seventh and Eighth Streets**. The tract runs toward the Southern Pacific tracks except for **one small corner belonging to George A. Harding**. Possible future brick construction is discussed after an existing lease expires. This is direct evidence that Harding held a small corner interest in a different Main Street tract in June 1916. **Do not project it onto the target Fifth/Sixth frontage or target-block ownership.**

Other controls: page 7 has unrelated professional-directory wording relative to Fourth/Fifth on Main; page 8 contains real-estate transfers and a Jones Drug Co. advertisement, but no target-address bridge.

## June 23 — completed visual review

Canonical source capture:

- `evidence/source-captures/1916-enterprise-june23-visual-review-2026-09-12.md`

Status: **VISUALLY VERIFIED — 8/8 genuine weekly pages inspected.** Every delivered PDF was rendered and the faithful page image individually visually inspected; OCR/text extraction was used only after visual review.

No inspected page directly assigns an occupant, proprietor, business owner, property owner, tenant, licensee, trade name, sale/transfer, construction, demolition, closure, vacancy, fire, or move to **501, 503, 505, 505½, or 507 Main Street**.

Material nearby but non-target control: **page 1** reports proposed Hawley Pulp & Paper Company expansion. Hawley sought a second paper mill extending from Third Street north on Main toward the alley between Fourth and Fifth, conditioned on vacation of Fourth Street from Main to the Southern Pacific track. Hawley also had an option on the **southern half of the block bounded by Main, the Southern Pacific tracks, Fourth and Fifth Streets**, owned by **James Tracy of Gladstone**; existing improvements would be removed if the additional mill were built. This is useful contemporary spatial/property context for the block immediately south of the target Fifth/Sixth frontage, but it establishes nothing about 501/503/505/505½/507 Main. Keep James Tracy ownership and proposed demolition/construction confined to the Fourth/Fifth block described by the source.

Other controls: pages 3 and 8 carry real-estate-transfer/county-court material; page 7 carries legal notices and professional-directory Main Street wording. None supplies a target-address bridge.

## Integration state

A parallel/current-main integration completed while this conversation was being handed off. **Do not redo June 16/23.**

Key integration commit:

- `285d81d2c15d81e68e0a67da4edfdd745815dc92` — `Certify June 16 and June 23 1916 Enterprise reviews`

A preceding correction commit was:

- `57a949275b90a267b6205129e011b5b14cde7e42` — `Fix June 16/23 evidence mirror names`

The integration updated the June 16/23 source captures, source/evidence registers, YAML mirrors, annual status/checkpoint, and propagation decisions. Current main's annual ledger already carries the 209/426 and 667/884 counts above.

This handoff itself was first saved, then corrected after discovering that the integration had already landed. The corrected handoff commit is the commit containing this version. Always fetch newer main before resuming because additional parallel commits may have landed.

## Existing 1916 controls still in force

- 24 Mar Enterprise p1 Oregon City federal-post-office proposal: one-story, ~4,800 sq ft, $55,000 building + $10,000 site; no site/address/acquisition/construction/move proof.
- 5 May Enterprise p4: Treasury estimate $70,000 building+site and $15,000 site, implying a $55,000 building component; still no target-site bridge.
- 21 Apr post-office-site article is Estacada, not Oregon City.
- 28 Apr new-site/lease article concerns Oregon Portland Railway, Light & Power Co. near Parkplace, not target property.
- 19 and 26 May Harding quiet-title material concerns Lots 1 and 2, Block 11, Oregon City — non-target, not Block 4.
- 26 May Enterprise p8 Jones Drug Company `Forced-Out-of-Location Sale`: landlord wants more room; Jones will move to the present Portland Railway Light & Power Co. room, two doors south; old location next to Burmeister & Andresen. No exact target street number; do not map the chain to target frontage without an independent bridge.
- 2 Jun Enterprise p1 `EXPANSION OF BURMEISTER & ANDRESEN WILL CAUSE GENERAL SHIFTING`: seven firms will move so Burmeister & Andresen can expand; no target street number.
- 9 Jun complete issue: no target event/address bridge.
- 16 Jun Harding Seventh/Eighth Main property control is explicitly non-target.
- 23 Jun Hawley/James Tracy Fourth/Fifth block expansion control is explicitly south of and separate from the target Fifth/Sixth frontage.
- 24 Mar 1912 Morning Enterprise p2 pool-hall license notice visibly signs `H. H. SMTHI`; do not normalize the signature to Smith without independent evidence.

## Exact next-chat resume sequence

1. Fetch/sync newest `main` and inspect commits after this handoff; preserve any newer parallel work.
2. Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely.
3. Read `/home/oai/skills/pdfs/SKILL.md` before handling scans.
4. Confirm `registers/year-status.md` still says Enterprise 209/426 through 23 June and next ordinary unresolved issue 30 June; if parallel work advanced it, follow the newer checkpoint instead.
5. Continue with the **next two ordinary unresolved Enterprise dates**, expected to be **30 June 1916 and 7 July 1916** if no newer work has advanced the ledger.
6. For each date, determine actual page count from the archive rather than assuming 8 pages. Probe enough sequences to establish the delivered issue extent and preserve a manifest.
7. Preserve original page PDFs under the canonical `newspapers/oregon-city-enterprise/1916/YYYY-MM-DD/` directory.
8. Render every valid original scan and visually inspect every page individually. Do not certify from OCR/search text.
9. Screen for 501/503/505/505½/507 Main; Harding/Young and associated businesses; Jones Drug/Burmeister & Andresen relocation chain; post-office/federal-building material; pool/billiard/cigar/liquor licensing; property transfers/legal descriptions/Block 4; sales/leases/moves; fires/construction/demolition/rebuilding/remodeling; and Main/Fifth spatial/address controls.
10. Only after visual inspection, use OCR/pdftotext as secondary discovery/deciphering aid. Visually confirm any candidate claim in the original scan.
11. Create issue-level source captures; add source/evidence register entries and synchronized YAML mirrors using IDs confirmed from current main.
12. Perform the cross-record propagation audit across timeline, buildings, businesses, people, open questions, research leads, crosswalk, and database/YAML. If only bounded no-hit coverage results, explicitly record that no entity/timeline propagation was warranted.
13. Update `registers/year-status.md` and `evidence/source-captures/1916-online-audit-checkpoint.md` using actual newly certified page counts. Continue to carry the 12 May page-8 retrieval gap explicitly.
14. Run full validator and require literal `Validation passed.`; commit meaningful work; pull/rebase newest main; validate again immediately before push; push without overwriting parallel work.
15. Report exact dates/pages reviewed, material findings and their limits, new coverage counts, carried May 12 gap, next ordinary unresolved date, and final integration commit.

## Project-steward continuation instruction

Continue chronologically when requested. The goal is exhaustive online coverage under `RESEARCH-STANDARD.md`, not merely keyword searching. No institutional/manual request should be sent without explicit authorization.