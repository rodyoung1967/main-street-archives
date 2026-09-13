# 1922 annual-audit stream save — 13 September 2026

## Purpose

Preserve every material result, correction, access discovery, repository change, and exact resume point from the stream that began with the project steward's instruction to finish the exhaustive 1922 online annual audit and ended with the instruction to save all stream knowledge to the repository.

This is a preservation checkpoint, not a 1922 closeout. **1922 remains IN PROGRESS.** No newly retrieved 1922 newspaper page in this stream received visual-review credit.

## Governing controls followed

- Fetched and fast-forwarded current `main` before research.
- Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md`, and `evidence/source-captures/2026-09-13-1922-conversation-handoff.md` completely.
- Reviewed the newest 1922 commits, targeted fire/property handoffs, year-status record, newspaper holdings boundary, existing source captures, and relevant registers.
- Ran `python3 scripts/validate_archive.py` before changes; baseline validation passed.
- Did not send institutional requests, purchase records, authorize fees, or initiate manual outreach.
- Preserved the separation among property ownership, building ownership/identity, business ownership/operation, tenancy, licensing, trade names, and street addresses.

## P-9594 steward-zoom preservation and correction

The prior handoff said the project-steward-supplied P-9594 crop remained outside the repository because the earlier session lacked a binary write route. That blocker was resolved.

- Source attachment: `IMG_5749.jpeg`
- Repository media ID: `IMG-0772`
- Repository path: `media/photos/main-street/IMG-0772_1922-p9594-501-503-505-zoom-steward-screenshot.jpg`
- Dimensions: **706 × 1536**
- Bytes: **183,943**
- SHA-256: `53a4ca00eabab2cebe14b36e1a54fe575c38ed6aabdda9e50eda16e51053b23f`
- Published commit: `53cf9cc18f0fc2d242b5bb5632511c889ce4c69d`

The original supplied JPEG was preserved unchanged. It is registered as a working derivative of `IMG-0760` / `S-239` / `E-213`, not as independent evidence.

The same published batch corrected the stale canonical language that still treated the light P-9594 corner mass as likely 501+503 construction. The controlling interpretation is now:

1. Rodney identifies the light building at left as **501 Main**.
2. The immediately adjacent apparent open/separated or low position is mapped as **503 Main**.
3. The substantial shadowed mass farther right is mapped as **505 Main** and is compatible with a newer/replacement structure.
4. Perspective, shadow, facade boundaries, and resolution prevent the apparent 503 separation from proving vacancy or absence of a building.
5. P-9594 must not be cited as affirmative evidence that 503 was rebuilt by November 1922.
6. If the mapping is correct, a later 503 structure may be bracketed after November 1922 and by the May 1925 Sanborn, but that remains hypothesis-dependent.

The correction was propagated across `S-239`, `E-213`, Markdown/YAML source and evidence records, 503/505 building histories, media metadata, research leads, the ID crosswalk, and both 13 September P-9594 handoffs. It created no new occupant, proprietor, owner, licensee, trade name, fire-origin address, or exact construction date.

## ODNP access breakthrough

The earlier handoff recorded a DNS/access failure to `oregonnews.uoregon.edu`. In this stream, direct archive access worked for:

- issue HTML pages;
- page-level PDF scans such as `/seq-1.pdf`;
- page-level OCR text such as `/seq-1/ocr.txt`.

The January 1922 test confirmed that issue HTML exposes a contiguous sequence inventory and that the page-PDF route returns faithful PDF scans. This removes the prior environment-access blocker and establishes a reproducible route for the exhaustive newspaper pass.

`scripts/fetch_1922_annual_newspapers.py` was created locally to:

- enumerate the expected weekly 1922 dates for both online Oregon City titles;
- read each issue page and inventory all exposed page sequences;
- require contiguous sequence numbering;
- preserve every page PDF and OCR text derivative;
- calculate byte counts and SHA-256 values;
- create monthly manifests whose status remains explicitly `RETRIEVAL ONLY` until separate visual review.

OCR is discovery-only. The script and its manifests do not award visual-review credit.

## Exact retrieval state when this stream was saved

Two relevant online local titles are confirmed for 1922:

- *Oregon City Enterprise* (`sn00063700`), Fridays, digitized through 29 December 1922;
- *The Banner-Courier* (`sn00063699`), Thursdays, digitized 5 January–28 December 1922.

Completed local retrieval manifests:

| Title | Months | Issues inventoried | Page PDFs + OCR files retrieved | Visual status |
| --- | --- | ---: | ---: | --- |
| *Oregon City Enterprise* | January–May | 21 | 168 | **PENDING — 0 newly credited in this stream** |
| *The Banner-Courier* | January–May | 21 | 210 | **PENDING — 0 newly credited in this stream** |
| **Total** | **January–May** | **42** | **378** | **RETRIEVAL ONLY** |

Monthly page counts:

| Month | Enterprise | Banner-Courier | Combined |
| --- | ---: | ---: | ---: |
| January | 32 | 36 | 68 |
| February | 32 | 42 | 74 |
| March | 40 | 52 | 92 |
| April | 32 | 40 | 72 |
| May | 32 | 40 | 72 |

The interrupted next step also downloaded all eight PDF/OCR pairs for the **2 June 1922 Enterprise** issue, but no June manifest was written before the preservation stop. Treat that directory as an incomplete local acquisition and rerun June from the script before giving it inventory or coverage credit.

The January–May binaries and manifests were retrieved into the local checkout but were not published as part of this stream-save commit. They are reproducible from the script and archive URLs. Do not call them repository-preserved or visually verified until a later batch publishes the source files and completes scan inspection.

## Repository publication mechanics

Normal `git push` from the local checkout lacked an interactive GitHub credential. The already-validated P-9594 binary/correction batch was therefore published through the authorized GitHub object API as a non-forced fast-forward commit. A first attempt correctly failed when parallel `main` advanced; the retry rebuilt on the newer parent and succeeded without overwriting parallel work.

Afterward, local `main` fetched and rebased onto current `origin/main`. Git dropped the two local duplicate commits because their exact content was already present upstream. Validation then passed on the synchronized tree.

## Cross-record propagation audit

The P-9594 batch materially changed structural interpretation and therefore updated the source/evidence registers and YAML, both building histories, media metadata, research leads, and crosswalk. It did not establish an event appropriate for the timeline or a new person/business/ownership relationship.

The newspaper work in this stream is acquisition/inventory only. Because none of the newly retrieved pages was visually reviewed and no new entity fact was established, no timeline, building, business, person, open-question, evidence, source, crosswalk, or YAML fact entry is manufactured from the retrieval batch. The annual status record receives only this bounded progress note.

## Exact resume point

1. Fetch/sync newest `main`; reread the governing files and this checkpoint.
2. Publish or reproducibly refetch the January–May source corpus using `scripts/fetch_1922_annual_newspapers.py`; rerun June because the local 2 June files lack a completed manifest.
3. Continue inventory/retrieval through December for both titles.
4. Visually inspect every actual page scan. Reuse earlier work only where a repository record explicitly says the original scan is `VISUALLY VERIFIED`; reconcile overlap rather than double-counting it.
5. Use OCR only to locate candidate passages, then verify each candidate on the corresponding scan.
6. Attempt alternate derivatives/direct files for every missing, misassociated, or non-rendering page; preserve unresolved items as `RETRIEVAL GAP` and create precise manual callouts after reasonable online recovery.
7. Finish the non-newspaper source-class audit required by `RESEARCH-STANDARD.md`, including directory, municipal, property, historic-resource, map, photograph, and official-database routes relevant to the 1922 fire, pool halls, Harding→Wolf/Gates questions, parcel geometry, rebuilding, and building continuity.
8. Perform the full cross-record propagation audit after each meaningful verified evidence batch.
9. Run validation after every repository-write batch.
10. Keep 1922 **IN PROGRESS** unless and until every online requirement is satisfied and the formal closeout/manual list is complete.

## Existing manual routes retained

At minimum, retain `MF-006`, `MF-007`, `MF-013`, `MF-019`, and `MF-041`, together with the more detailed stable `1922-F01`–`1922-F08` list in the targeted Task 8 handoff. No request was sent and no fee was authorized in this stream.

Absence of a retrieved or discovered item is not evidence of vacancy, demolition, closure, relocation, non-use, ownership, or non-ownership.
