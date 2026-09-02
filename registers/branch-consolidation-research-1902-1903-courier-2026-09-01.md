# Legacy branch consolidation audit — `research-1902-1903-courier`

LEGACY_BRANCH_INTEGRATED_V1

Integration date: **1 September 2026**  
Branch tip: `dbdd56ff2bc49f4b306439f2da6cc8ce769a34b5`  
Baseline `main` when integration script started: `565719b1b1d298f46805c9cb3246d024668d0b15`  
Snapshot SHA-256: `4a293f640b6e40e53110921aa858be5cba1ece5ad0cb0c324c5b0e68e3f782d5`

## Why the branch was not merged directly

The old branch reused evidence/source identifiers that now have different meanings on the authoritative archive. For example, its old `E-057` was a Schrader 1902 record while current `E-057` is Tolpolar 1904. A merge or cherry-pick would therefore corrupt canonical identity. The integration instead preserved the complete branch byte-for-byte and promoted missing claims under fresh IDs.

## Complete branch preservation

Archive: `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`  
Manifest: `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.json`

The archive contains the branch tip SHA, merge-base SHA, integration baseline SHA, full branch-only commit log, a binary-capable Git diff, and each of the 18 files changed on the branch:

- `buildings/501-main.md`
- `evidence/1902-1903-main-street-mapping-synthesis.md`
- `evidence/1904-main-street-mapping-synthesis.md`
- `evidence/E-054-holman-fifth-main-1915-1917.md`
- `evidence/E-057-schrader-main-street-bakery-1902.md`
- `evidence/E-058-huntley-two-store-remodel-1902.md`
- `evidence/E-059-union-store-main-between-5th-6th-1902.md`
- `evidence/E-060-portland-clothing-next-to-harding-1903.md`
- `evidence/E-061-fair-store-postoffice-move-1903.md`
- `evidence/E-062-harding-willamette-building-1903.md`
- `evidence/E-063-1906-house-numbering-context.md`
- `evidence/E-064-holman-moves-to-fifth-main-1914.md`
- `evidence/research-leads.md`
- `evidence/source-captures/1902-courier-main-street-review.md`
- `evidence/source-captures/1903-courier-main-street-review.md`
- `evidence/source-captures/1904-courier-main-street-review.md`
- `evidence/source-register.md`
- `timeline.md`

## Canonical promotion decisions

- Fresh evidence: `E-145`–`E-150`.
- Fresh sources: `S-161`–`S-170`.
- Fresh businesses: `BUS-081`–`BUS-083`.
- New follow-up: `RL-046`; new open question: `OQ-033`.
- The branch's 24 August 1906 house-numbering report was added as corroboration to existing `E-061`; its old conflicting evidence ID was not reused.
- The 1904 contextual review and Huntley remodel are preserved in the canonical consolidation capture and source register but were not over-promoted into target-address conclusions.
- The 26 February 1914 Holman notice was promoted because it materially advances the already accepted August 1914 chronology.

## Deletion criterion

Once this commit has passed `python3 scripts/validate_archive.py` and is present on authoritative `main`, no unique information from `research-1902-1903-courier` depends on retaining that Git branch: its complete branch-only state is preserved in the snapshot and its materially useful missing findings are represented in canonical archive records. This statement applies only to this branch; final all-branch deletion safety requires the separate post-integration branch audit.
