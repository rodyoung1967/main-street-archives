# Decisions

This file records project decisions for The Main Street Archive.

## Decision Log

| ID | Date | Decision | Reason | Related Evidence |
| --- | --- | --- | --- | --- |
| D-001 | 2026-07-01 | Markdown files remain the working narrative source; `database/*.yml` files hold structured cross-reference data as an optional sidecar mirror. | This preserves readable research notes while making people, businesses, buildings, sources, evidence, artifacts, and timeline entries easier to connect. YAML lag is acceptable for low-priority entities, but YAML must never contradict Markdown. | PROJECT.md; AGENTS.md |
| D-002 | 2026-07-04 | Standardize open question IDs on the `OQ-###` prefix. | `evidence/open-questions.md` already uses `OQ-001` through `OQ-021`. The earlier `Q-###` prefix in workflow docs was never adopted in practice. | evidence/open-questions.md; docs/WORKFLOW.md |
| D-003 | 2026-07-05 | **501 Main existed through at least 1936 and was removed by 1944** (removal window 1936–1944), based on aerial photocompare frames `IMG-0007` and `IMG-0009` under `E-021`. By 1944 the east-side building across from 500 Main (Sanborn-labelled counterpart) is also absent. | Project steward corrected an initial integration misread. The 1936 frame shows three distinct roofs at 501, 503, and 505 Main; the 1944 frame shows 501 gone. Business, ownership, and legal cause of removal remain open under `OQ-005` / `OQ-023`. | `E-021`; `IMG-0007`; `IMG-0009`; evidence/aerial-5th-main-photocompare-series.md |

## D-001 Operating Rules (Amended 2026-07-04)

1. **Always update Markdown** when adding findings (registers + entity pages).
2. **Update YAML when touching related entities** — but YAML lag is acceptable for low-priority entities.
3. **Never let YAML contradict Markdown** — if you cannot sync immediately, remove or correct the stale YAML entry rather than leaving a conflicting claim.

## YAML Scope (See database/README.md)

YAML files cover: buildings, businesses, people, evidence, sources, artifacts, oral history, timeline, and maps.

Markdown-only (no YAML file yet): open questions (`OQ-###`), research leads (`RL-###`), media catalog (`IMG-###`, `DOC-###`, `MAP-###`), and current records (`R-###`).
