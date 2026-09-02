# Final branch deletion audit — 2026-09-01

ALL_NON_MAIN_BRANCH_REFS_ARCHIVED_V1

Authoritative `main` at archive start: `d94123fa03206a7cbda58ba9cf5e880b81160bee`  
Non-main branch refs archived: **24**  
Logical archive SHA-256: `ef666f75ba91fe2d9b3505ba126a3b22ccb96a61ea6afb05e35a9ac45f895c0a`  
Logical archive size: **3409556 bytes**  
Manifest: `records/repository-history/all-non-main-branch-refs-2026-09-01-manifest.json`

## Purpose

This is the final branch-ref safety archive. It does **not** make superseded hypotheses canonical. Instead, before any branch ref is deleted, it preserves every non-main branch's exact branch-only state: tip SHA, merge base, branch-only commit log, binary-capable diff, and tip versions/hashes of all paths changed from the merge base.

The previously substantive `research-1902-1903-courier` branch was separately reconciled into canonical records and fully snapshotted in `registers/branch-consolidation-research-1902-1903-courier-2026-09-01.md`. The current archive additionally preserves that ref together with every other non-main ref, including squash-merged, superseded, helper/no-op, Cursor, Codex, and closed-unmerged historical branches.

## Branch inventory

| Branch | Tip | Ancestor of main? | Main-only commits | Branch-only commits | Changed paths from merge base |
| --- | --- | ---: | ---: | ---: | ---: |
| `add-kwality-matchbook-photo` | `3efc61a9870b` | yes | 502 | 0 | 0 |
| `audit/ignore` | `181b7ce3ce09` | no | 459 | 12 | 10 |
| `codex/1915-polk-review` | `2d8d76d39e74` | no | 108 | 1 | 17 |
| `cursor/1965-forward-municipal-timeline-fbe0` | `d3d0ec424bef` | yes | 200 | 0 | 0 |
| `cursor/1973-1987-503-505-research-fbe0` | `528b0209028c` | yes | 197 | 0 | 0 |
| `noop-avoid` | `9fe4a40482ec` | no | 455 | 13 | 13 |
| `noop-avoid-1912` | `06bd6b3a6268` | no | 453 | 11 | 11 |
| `organize-aug20-newspapers` | `6902044d4e3f` | yes | 462 | 0 | 0 |
| `research-1902-1903-courier` | `dbdd56ff2bc4` | no | 462 | 18 | 18 |
| `research/1904-closeout-1905` | `ce9002df8fba` | no | 462 | 11 | 8 |
| `research/1906-main-street` | `181b7ce3ce09` | no | 459 | 12 | 10 |
| `research/1907-main-street` | `1aaaa8c3c663` | no | 458 | 11 | 11 |
| `research/1908-main-street` | `9edcf159061c` | no | 457 | 10 | 10 |
| `research/1909-main-street` | `7835f4baf0ff` | no | 456 | 11 | 11 |
| `research/1910-main-street` | `9fe4a40482ec` | no | 455 | 13 | 13 |
| `research/1911-main-street` | `81e07bea5a3d` | no | 454 | 11 | 11 |
| `research/1912-closeout` | `d184e3422aba` | no | 452 | 15 | 11 |
| `research/1912-main-street` | `e3c56e940d62` | no | 453 | 12 | 12 |
| `research/1913-pass` | `113194dadc8b` | no | 452 | 2 | 1 |
| `research/1914-pass` | `510c43dc252d` | yes | 448 | 0 | 0 |
| `research/1915-pass` | `80b402849648` | no | 447 | 34 | 10 |
| `research/1916-pass` | `f0ec2bb08ef0` | yes | 441 | 0 | 0 |
| `temp-ignore-1912` | `e3c56e940d62` | no | 453 | 12 | 12 |
| `tmp-noop-should-not-create` | `651a3381a717` | yes | 182 | 0 | 0 |

## Deletion safety rule

After this archive commit is present on `main` **and** `python3 scripts/validate_archive.py` passes, deleting these non-main branch refs will not discard their historical Git-side research state. Branch tips that are ancestors are already in `main` history; branch tips that are not ancestors are recoverable from this archive relative to their merge-base commit, which remains in `main` history.

This audit does not authorize deletion of the repository or of `main`; it applies only to the non-main branch refs listed above.
