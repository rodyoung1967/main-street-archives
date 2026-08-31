# Evidence-Control Audit — 30 August 2026

## Scope

This audit reconciles the archive's evidence layer after the entity-page and unified 501/503/505 timeline reviews. It covers the source register, evidence register, YAML sidecars, open questions, research leads, crosswalk, navigation, and automated validation. It does not add newspaper coverage, select a 1922 fire-origin model, or change any annual research status.

## Inventory and Integrity Results

| Record class | Count | Result |
| --- | ---: | --- |
| Evidence (`E-###`) | 134 | Markdown/YAML IDs and names synchronized; no duplicate or missing IDs |
| Sources (`S-###`) | 146 | Markdown/YAML IDs and names synchronized; no duplicate IDs |
| Open questions (`OQ-###`) | 32 | Continuous `OQ-001`–`OQ-032`; no duplicate IDs |
| Research leads (`RL-###`) | 45 | Continuous `RL-001`–`RL-045`; no duplicate IDs |

The source sequence intentionally retains historical unassigned numeric gaps 030, 031, and 044 under the `S` prefix. They were not backfilled. Every existing YAML `repository_file` path resolved during the audit.

## Corrections Made

- Reframed `OQ-005`: the 1925 separate 501 store and the 1936–1944 removal window are settled portions; tenants, title, continuity, and removal cause remain open.
- Corrected `RL-038` from the withdrawn Block 26 target to the odd-numbered original Block 4 frontage, with Block 26 retained only as an opposite/even-side control.
- Marked the map portion of `RL-010`, the Oregonian clipping backlog `RL-015`, and the recovered 1914 Holman notice `RL-020` complete while preserving their unresolved downstream questions.
- Clarified in `RL-003` and archive navigation that `BUS-009` “The 505” is an archive handling label, not a documented historical trade name.
- Synchronized `S-021`, `S-078`, and `E-064` wording with the corrected Block 4 / Block 26 orientation.
- Added missing explanatory notes to `S-002`, `S-003`, and `S-004` without upgrading those web presentation/secondary sources.
- Standardized explicit `Claims:` labels in the newest evidence entries and strengthened validation for required evidence/source metadata.

## Retained Overlaps and Precedence

No evidence entries were deleted merely because later records refine them. In particular, `E-009`, `E-019`, `E-022`, and `E-038` remain separate because they preserve different family/property statements and correction history. Later correction entries control only the propositions they explicitly supersede.

`E-094` controls the cadastral orientation: the target odd-numbered 501/503/505/507 frontage is original Block 4; Block 26 is the opposite side. Earlier Block 26 target-side models remain visible as superseded reasoning rather than being silently erased.

The Mitch/505 controls remain unchanged: `E-014` and the current accuracy rules separate 505 Tavern from The Wheel, treat `BUS-009` as a handling label, and keep business operation, business ownership, real-estate ownership, liquor-license role, and trade-name usage distinct.

## Completeness Boundary

This is a repository-control audit, not new historical research. It changes no annual status in `registers/year-status.md`; all existing coverage, retrieval gaps, manual callouts, and unresolved 501/503/505 questions remain governed by `RESEARCH-STANDARD.md`.
