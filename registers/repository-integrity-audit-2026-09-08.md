# Repository integrity and consistency audit — 8 September 2026

- Audit baseline: `0dd2fc3013214293945faa92b5c56a03441660f4`
- Repository: `rodyoung1967/main-street-archives`
- Branch: `main`

## Result

The audit found **two critical preservation omissions**, structured-data schema drift, several missing cross-references, stale review-state metadata, and two manual-dashboard defects. The confirmed defects listed under **Repairs completed** were corrected. No corrupt Git object, malformed JSON file, zero-byte content file, unresolved Git LFS pointer, duplicate canonical ID, broken internal Markdown link, unknown archive ID, or mismatched resolved SHA-256 pair was found.

This was an archive-integrity audit, not a new primary-source research pass. It did not promote OCR-only material, change an evidence confidence classification, close a research year, infer absence from a no-hit, merge similarly named people, or resolve an open historical question.

## Scope and checks

- Synchronized and reviewed current `main`, repository policy, research standard, manual dashboard, newest integrations, and the high-risk 503/505 narratives.
- Audited **3,340 tracked files** and all structured YAML entity collections.
- Parsed **174 JSON files** successfully.
- Resolved and recalculated **1,824 file/SHA-256 pairs** found in structured manifests; **0 mismatches**.
- Ran `git fsck --full --no-reflogs`; no object corruption was reported.
- Checked committed files for zero-byte content and unresolved Git LFS pointer stubs; none found.
- Checked YAML ID uniqueness, Markdown/YAML ID synchronization, name synchronization, local repository paths, typed relationships, orphan references, unknown IDs, internal links, evidence/source required fields, raster registration/storage, annual-status syntax, and protected 503/505 accuracy rules.
- Reviewed relationship reciprocity separately as a completeness diagnostic; because older entity lists are selective rather than universally reciprocal, those results are recorded as normalization debt instead of being mass-filled without evidentiary review.

## Repairs completed

### 1. Critical — repository-history archives were claimed but absent

Two manifests and multiple narrative records said these archives had been committed, but `.gitignore` excluded `*.tar.gz`, so neither file existed:

- `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`
- `records/repository-history/all-non-main-branch-refs-2026-09-01.tar.gz`

All recorded historical tip commits were still recoverable by object ID. The archives were deterministically rebuilt from those recorded tips and historical `main` baselines. The focused archive contains the branch files, commit log, binary diff, and metadata for `research-1902-1903-courier`; the complete archive contains equivalent records for all **24** branch names in the 1 September manifest. Explicit `.gitignore` exceptions, current byte counts/hashes, original recorded hashes, recovery notes, and a repeatable recovery script were added. The validator now fails if either archive is absent, hash/size-mismatched, or unreadable.

### 2. High — relationship IDs stored under the wrong entity type

Eleven relationships were valid IDs but were placed in the wrong typed list, a defect the old validator did not detect:

- `B-001` had one person, four evidence records, and four sources inside `related_maps`.
- `BUS-004` had two evidence IDs inside `related_sources`.

The IDs were moved to `related_people`, `related_evidence`, and `related_sources` as appropriate. `related_maps` now contains only `SM-###` IDs. Validator rules now enforce the allowed prefix for every typed `related_*` field.

### 3. High — recent YAML schema drift hid relationships from normal tooling

Twenty legacy relationship fields (`source`, `sources`, or `evidence`) appeared in recent business, person, evidence, and timeline records even though the canonical schema uses `related_sources` and `related_evidence`. Their values were merged into the canonical lists and the aliases removed. The validator now rejects those deprecated fields.

### 4. Moderate — incomplete recent cross-references and file metadata

- Added reciprocal `S-289`–`S-297` ↔ `E-263`–`E-271` links, source types/dates, and source-capture paths.
- Added missing explicit January/February 1919 entity relationships, including Ohio Dentists, Harding, Pantorium, Theroux, Farr Brothers, Nash, and the 507/Harding context while preserving the existing inference limits.
- Synchronized the Pantorium address summary through its directly documented 2 January 1919 continuation at 500 Main.
- Added the missing `IMG-0766` link to `E-220`, `BUS-102` to `E-250`, and `B-018` to `E-253`.
- Mapped all ten standalone `E-###` evidence files that lacked a YAML `repository_file` field (`E-094`–`E-100` and `E-168`–`E-170`). No standalone `evidence/E-###*.md` file is now unmapped.
- Validator path checks now cover both singular `repository_file` and list-form `repository_files`.

### 5. Moderate — review status and dashboard inconsistencies

- Sixteen January–September 1919 Enterprise/Courier manifests still said retrieval-only after their documented visual reviews. Their current status and exact review-record path are now recorded. Banner-Courier July–September manifests remain retrieval gaps and were not upgraded.
- Reconciled all **340** stale per-page labels in the twelve 1917 Courier continuation manifests against the canonical visual-review captures: **339 genuine intended-date pages** now say visually verified, while the inspected file served as 13 December sequence 21 is explicitly marked as a misassociated 27 December page. The true 13 December page 21 remains a retrieval gap. Each manifest now links its exact review record, and the validator checks item count, review state, page-file presence, SHA-256, and the substituted-page exception.
- Corrected the 1919 year-status wording from “August–December remains” to “October–December remains,” consistent with the preserved August and September reviews.
- Restored the missing active `MF-052` row in the dispatch tracker and removed a malformed duplicate `MF-056` row from the `MF-055` detail table. No manual-follow-up ID was renumbered or deleted.

### 6. Moderate — stale 503/Wheel structured chronology

Updated `B-001`, `P-025`, and the 503 page header to reflect the direct **28 March 1958** Wheel Cafe & Lounge exact-address anchor, with May and August as later corroboration. This remains a date bracket, not proof of opening, ownership, rename, licensee, or sale.

## High-risk narrative review

No current core narrative was found to violate the project’s protected distinctions:

- The Wheel is kept at **503 Main**, separate from the **505 Tavern** chain.
- “The Wheel Tavern” is not promoted as an official name.
- Raye LaFarlette / Raye Grisham remains one person and distinct from Ray Hansen.
- The Nesmeth/Nemeth purchase remains assigned to **505**, not 503.
- Mitch Young’s March 1991–March 2004 period remains the 505 Tavern at 505; the Wiitanens’ prior rename is preserved.
- The current 505 operator is spelled **Alin Guria**.
- Unresolved 1922 Gates/Wolf geometry, exact fire-origin room, and construction chronology remain unresolved rather than being forced into a model.

## Outstanding normalization debt

These findings are documented but were not bulk-rewritten because doing so requires record-by-record evidentiary judgment:

| Direction tested | Missing reciprocal links | Relationships tested |
| --- | ---: | ---: |
| Evidence → source | 266 | 361 |
| Evidence → building | 70 | 236 |
| Evidence → business | 54 | 278 |
| Evidence → person | 85 | 207 |
| Source → building | 6 | 20 |
| Source → business | 2 | 13 |
| Source → person | 9 | 14 |

The source-side `related_evidence` lists are historically selective: every relationship they do declare is valid, but they do not attempt to mirror every evidence-to-source relationship. A future schema decision should establish whether reciprocity is mandatory before a migration is attempted.

Source-register serial numbers **030, 031, and 044** are unassigned gaps. They have no live references and no occurrence in recoverable Git history, so the audit found no evidence that source records were deleted. IDs were not renumbered or reused.

## Research completeness remains open

No year is certified `ONLINE COMPLETE` or `ONLINE + MANUAL COMPLETE`. Every annual row remains `IN PROGRESS`, with exact blockers in `registers/year-status.md`; institutional/manual work remains in `MANUAL-FOLLOWUP.md`. The integrity repairs do not alter those research-completeness conclusions.

## Validation outcome

`python3 scripts/validate_archive.py` passes after all repairs. The validator now guards the failure classes that allowed the highest-impact defects: typed relationship misuse/legacy aliases, missing or altered repository-history archives, and regression of reconciled 1917 Courier page-review state.
