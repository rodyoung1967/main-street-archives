# CCHS C.0250.005060 — binary ingest, dating status, and conversation handoff

Date: 15 September 2026
Repository: `rodyoung1967/main-street-archives`
Branch: `main`

## Purpose

Preserve the current authoritative state of the conversation around the project-steward-supplied CCHS bluff photograph, including the dating evidence, exact catalog metadata, local steward-upload fingerprint, the discovered binary-ingest solution, the distinction between metadata preservation and binary preservation, and the remaining next steps.

This handoff is intended to prevent future sessions from repeating the incorrect conclusion that the uploaded JPEG cannot be added merely because the ordinary GitHub contents action is text-only.

## CCHS catalog metadata — institutional facts

Project steward supplied the following CCHS metadata:

- **Name/Title:** `Oregon City Main Street`
- **Entry/Object ID:** `C.0250.005060`
- **Description:** `Business Section of Oregon City from the Bluff.`
- **Date:** no date stated in the supplied CCHS metadata.

The research task is therefore **dating assistance for an undated CCHS photograph**, not correction of a CCHS dating error.

Do not attribute project filenames, local filenames, inferred dates, or project conclusions to CCHS unless the catalog record actually states them.

## Steward-supplied JPEG control

The actual JPEG is present in the active research environment and was directly inspected.

Fingerprint:

- format: JPEG
- dimensions: **1381 × 870 pixels**
- bytes: **219,852**
- SHA-256: `97b269e43fe38e85b9b8169e1a819870528e7f3ac676279e3a1594d6b3d302aa`

Two local runtime filenames were confirmed to be byte-identical copies with that same hash. One is the cleaned working filename `Oregon City Main Street c0250-005060 (c1929-1936).jpg`. A superseded local filename contained an incorrect `pre 1922` phrase. That phrase is **not CCHS metadata and must not appear in external CCHS-facing material**. Preserve it only as internal provenance if ever necessary to explain an old research note.

Visible image controls from direct inspection:

- printed caption: `BUSINESS SECTION OF OREGON CITY, OREGON FROM THE BLUFFS`;
- Clackamas County Historical Society watermark;
- lower-right mark appears to read `Eddy`;
- completed Oregon City–West Linn concrete arch bridge at left;
- Railroad Avenue / railroad corridor;
- old Clackamas County Courthouse clock tower;
- Main Street commercial district.

## Current binary-preservation status

**The JPEG binary is not yet committed to current `main`.**

Research notes and CCHS catalog metadata are preserved in repository source captures, but this must not be confused with preservation of the actual image binary.

Do not report this photograph as fully saved until all of the following are true:

1. an `IMG-####` ID has been assigned after checking the current canonical register/inventory;
2. the JPEG is present under the canonical `media/photos/main-street/` path on current `main`;
3. `media/photo-metadata-register.md` and `media/photos/inventory.md` point to that binary;
4. steward-upload and repository-derivative fingerprints are kept distinct if the bytes differ;
5. `scripts/validate_archive.py` passes after the binary is present;
6. the actual binary-preservation commit has been verified on `main`.

## Proven solution to the connector binary problem

The repository already contains a successful precedent and now documents it in `BINARY-INGEST.md`.

The proven solution is:

**exact archival object ID → repository Python fetch script → public institutional API/download route → GitHub Actions workflow with `contents: write` → binary + metadata updates → validator → commit/push to `main`.**

For CCHS/CatalogIt sources, adapt the proven 1960 workflow rather than treating the text-only GitHub contents action as a blocker.

### Proven precedent

CCHS object `2008.008.049.037` was preserved using:

- script: `scripts/fetch_cchs_2008_008_049_037_1960_bluff.py`
- workflow: `.github/workflows/fetch-cchs-2008-008-049-037-1960-bluff.yml`
- resulting image: `media/photos/main-street/IMG-0771_1960-5th-main-from-bluff-cchs-2008-008-049-037.jpg`
- binary-preservation commit: `d6fdf22de7df77b0e3ce30864b26a5155b25eb42`

That script searched the public CatalogIt API for the exact CCHS catalog number, verified the returned object, selected the largest non-thumbnail public derivative, downloaded the JPEG, verified/fingerprinted it, wrote the binary into the canonical media directory, updated source/register/inventory records, and produced API provenance. The GitHub Actions workflow ran the script and validator, committed the resulting binary and metadata changes, rebased on current `main`, revalidated, and pushed.

### Future shorthand

If this issue recurs, use:

> Use the repo's binary-ingest workflow — the CCHS fetch-script + GitHub Actions method. Check `BINARY-INGEST.md` and the `IMG-0771` precedent.

A future agent should **not** ask the steward to re-upload this image merely because the ordinary GitHub connector cannot transfer local bytes. The source is already available and the repository has a proven server-side retrieval-and-commit path.

## Next binary-ingest action for C.0250.005060

1. Fetch/sync newest `main`; reread `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md`, and `BINARY-INGEST.md`.
2. Check `media/photo-metadata-register.md` and `media/photos/inventory.md` for the next valid unused `IMG-####`; do not guess or renumber.
3. Adapt the `IMG-0771` CCHS fetch script to exact target `C.0250.005060`.
4. Query the public CatalogIt/CCHS endpoint and require exact catalog-number match before downloading anything.
5. Select the best appropriate non-thumbnail public derivative and verify it is the same archival object as the steward-supplied photograph.
6. Write it to `media/photos/main-street/` using a canonical filename reflecting the then-current project date estimate; current preference is approximately `c1929-1935`, with 1936 treated as an upper-bound uncertainty in the dating note rather than necessarily the primary filename.
7. Record repository derivative dimensions, bytes, and SHA-256 separately from the steward-upload fingerprint above.
8. Update the canonical photo metadata register, photo inventory, source capture, and any directly affected cross-record links.
9. Run `scripts/validate_archive.py` in the workflow before and after rebase/push.
10. Verify the JPEG exists on current `main` and identify the binary-preservation commit before calling the task complete.

## Dating evidence — current best synthesis

### Completed Oregon City–West Linn bridge

The completed concrete arch bridge is visible. Its opening/dedication on 28 December 1922 provides an early chronological control.

Evidence state: **DOCUMENTED chronology + DIRECT VISUAL landmark**.

### Replacement Elks Lodge

A large bridge-adjacent building is strongly consistent in location, massing, roof relationship, and bridge approach with the replacement Oregon City Elks Lodge.

Documentary controls preserved elsewhere show:

- predecessor Elks building burned 2 December 1922;
- replacement was under construction in September 1923;
- replacement completed in 1923;
- first meeting in the new lodge occurred 7 December 1923.

Because the target view does not expose enough principal-facade detail for a direct architectural identification, keep this at **STRONG CROSS-SOURCE / VISUAL-SPATIAL INFERENCE**, not DOCUMENTED/DIRECT.

This supports a post-1923 setting but is weaker than the later Railroad Avenue control.

### Railroad Avenue improvement — strongest lower-bound control

The 1929 Municipal Activities Report documents reconstruction of Railroad Avenue from Fifth to Seventh Streets, including full 40-foot grading, an 8-foot concrete sidewalk/curb, 32-foot six-inch concrete pavement, sewer work, 1,853 square yards of concrete, and reported cost of $7,593.73.

The 1934 Municipal Activities Report contains matched photographs captioned `Railroad Avenue from Fifth to Sixth Street, before improvement` and `after improvement`.

Direct comparison shows the target bluff photograph is strongly consistent with the **after-improvement** condition. Important comparison points include:

- stop sign in the same Railroad Avenue/Fifth Street spatial relationship;
- conspicuous alternating light/dark or banded stop-sign post treatment;
- developed roadway/sidewalk/curb geometry;
- west-side building relationship;
- developed railroad/street edge.

Evidence state: **STRONG CROSS-SOURCE / VISUAL-SPATIAL INFERENCE**.

The strongest present lower-bound year is **1929**, pending recovery of the exact project completion date.

### Old courthouse — upper-bound control

The old Clackamas County Courthouse and clock tower remain plainly visible. Current documentary synthesis places the replacement courthouse construction in 1936–1937.

Until exact demolition/start-of-replacement chronology is recovered, use approximately **1935 / early 1936** as the practical upper boundary rather than claiming an exact cutoff.

Evidence state: **DIRECT VISUAL landmark + DOCUMENTED replacement chronology**.

### Current project date recommendation

For ordinary catalog-facing wording, use approximately **circa 1929–1935**.

In detailed research notes, preserve **1935 / early 1936** as the upper-bound uncertainty until the exact courthouse milestone is documented.

This date range is a **project research estimate**, not CCHS metadata.

## Photographer / provenance lead

The visible lower-right mark appears to read `Eddy`, so **Ralph Eddy is a probable attribution**, not yet a catalog-established fact from the supplied metadata.

Related lead: Clackamas County Family History Society lists `PC094 Oregon City and Mount Hood-153 Eddy photograph`, described as showing the 1922 bridge at left and first public elevator. This is a strong related-image/provenance lead, but exact-image identity with C.0250.005060 has not been established.

Old Oregon Photos has an indexed `Oregon City and Mount Hood - 1930` candidate compatible with the independently derived date range, but exact-image identity remains an **UNVERIFIED EXACT-MATCH LEAD** until directly compared.

## CCHS-facing wording rules

External dating-assistance material should:

- identify `C.0250.005060` exactly;
- state that the supplied CCHS metadata is undated;
- frame the work as assistance in narrowing the date;
- present the bridge as an early chronological control;
- emphasize the 1929 Railroad Avenue after-improvement match;
- use the old courthouse as upper-bound evidence;
- suggest approximately 1929–1935, with provisional language;
- invite CCHS to compare original negative/accession notes and related Eddy images.

External material should **not** mention internal repository paths, technical connector issues, superseded local filenames, or imply CCHS made a dating error.

## Suggested catalog metadata / note for consideration

Potential project-supplied wording:

- **Name/Title:** Oregon City Main Street
- **Entry/Object ID:** C.0250.005060
- **Suggested Date:** circa 1929–1935
- **Description:** Business section of Oregon City viewed from the bluff, looking toward downtown and the Willamette River. The Oregon City–West Linn arch bridge is visible at left. A large building near the Oregon City end of the bridge is strongly consistent with the replacement Elks Lodge completed in 1923. The old Clackamas County Courthouse and clock tower are visible near Eighth and Main streets. Railroad Avenue and the Main Street commercial district appear in the foreground.
- **Dating note:** Research comparison suggests circa 1929–1935. The completed bridge provides post-1922 control. Railroad Avenue appears consistent with documented 1929 improvements. The old courthouse remains visible; replacement work belongs to the 1936–1937 transition. The range is provisional and may be refined by original negative/catalog notes or additional dated comparison photographs.
- **Photographer:** Ralph Eddy — probable attribution based on the visible `Eddy` mark; confirm against the original catalog/negative record.

## Separate Quality Cafe / Kwality thread preserved from this conversation

Historic Oregon Newspapers indexed/OCR text for *Banner-Courier*, 17 August 1922, p.2, transcribes a `BUY AT HOME` / local-business list entry as **QUALITY CAFE**.

Current evidence state remains **OCR/TEXT ONLY** because the faithful page scan has not yet been visually verified.

The indexed text provides no street number and no proprietor. Therefore it does **not** prove:

- Quality Cafe was at 503 Main;
- Quality Cafe was the same business as later Kwality Restaurant/Kwality Cafe;
- continuity from the 1922 Quality spelling to later Kwality spelling.

Working hypothesis only:

`Quality Cafe` (Oregon City, Aug. 1922; address unresolved) → unnamed restaurant at 503 on the 1925 Sanborn → `Kwality Restaurant` at 503 in 1926 synthesis → `Kwality Cafe` in later records.

Do not merge or normalize the names until direct evidence supports the transition. The target bluff photograph is too soft to distinguish a Q/K initial reliably and must not be used as direct proof of either spelling.

## Related repository records

Read together with:

- `BINARY-INGEST.md`
- `evidence/source-captures/2026-09-15-eddy-bluff-photo-elks-comparison-and-quality-cafe-followup.md`
- `evidence/source-captures/2026-09-15-eddy-bluff-photo-1929-1935-metadata-challenge-and-ohs-followup.md`
- `evidence/source-captures/2026-09-15-bluff-photo-1925-1929-dating-controls.md`
- `scripts/fetch_cchs_2008_008_049_037_1960_bluff.py`
- `.github/workflows/fetch-cchs-2008-008-049-037-1960-bluff.yml`

## Repository-state clarification from this conversation

An earlier conversational answer blurred these distinct states:

- file available in the conversation/runtime;
- metadata/research saved in the repository;
- actual JPEG binary committed to GitHub.

For this object the first two are true; the third is **not yet true** as of this handoff. Future responses must make that distinction explicit and must verify current `main` before saying a binary is preserved.

## Propagation audit

This conversation materially changed **workflow knowledge and binary-ingest status**, but did not establish a new 503/505 occupant, ownership event, business transfer, or building event. Therefore no artificial timeline/business/person entry should be created from this handoff.

The photo dating evidence already exists in the linked source captures. The immediate propagation requirement when the binary is finally committed is the photo metadata register, photo inventory, source capture, and any appropriate crosswalk/source/evidence links.

## Validation note

This handoff was written through the GitHub connector. The connector session cannot execute `scripts/validate_archive.py`; no validator pass is claimed for this text-only write. The eventual C.0250.005060 binary-ingest workflow must run the validator before and after its commit/push sequence.
## Binary ingest completion

The exact CCHS catalog object `C.0250.005060` was recovered through the public CatalogIt API and its largest non-thumbnail public JPEG derivative was committed as `media/photos/main-street/IMG-0773_c1929-1935-oregon-city-main-street-bluff-cchs-c0250-005060.jpg`.

- Repository derivative: 1381 × 870; 219,852 bytes
- Repository SHA-256: `97b269e43fe38e85b9b8169e1a819870528e7f3ac676279e3a1594d6b3d302aa`
- Steward-upload SHA-256 control: `97b269e43fe38e85b9b8169e1a819870528e7f3ac676279e3a1594d6b3d302aa`
- Public CCHS record: https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/oregon-city-main-street-9
- Evidence-state note: the circa 1929–1935 date remains a project research estimate, not institutional metadata.
