# Evidence Control Guide

This directory separates source description, claim-level evidence, unresolved questions, and future work. Its principal files are:

- `source-register.md` — immutable `S-###` records describing where material came from, its verification state, and any repository copy.
- `evidence-register.md` — immutable `E-###` records stating the claims the source material actually supports.
- `open-questions.md` — unresolved historical questions (`OQ-###`), including questions narrowed by later evidence.
- `research-leads.md` — actionable research tasks (`RL-###`), including completed or superseded leads retained to prevent repeated work.
- `source-captures/` — detailed review notes, transcriptions, coverage records, and provenance manifests.

## Minimum Evidence Record

Every evidence entry must have:

- an immutable ID and synchronized Markdown/YAML name;
- a `Type:` classification;
- explicit `Claims:` or coverage statements;
- a `Confidence:` or verification-status statement;
- at least one related source;
- material building, business, person, map, question, and lead relationships where applicable;
- a valid `repository_file` in YAML when a standalone evidence or source-capture note exists.

Unknown dates, locations, identities, ownership, and continuity remain unknown. A source's silence is a bounded coverage result, not proof of vacancy, closure, demolition, relocation, or non-use.

## Evidence Classes and Precedence

Keep these classes distinct: primary documentary evidence; official secondary records; participant/family oral history; project-steward corrections; strong inference; hypothesis; unresolved conflict; OCR/text-only lead; retrieval gap; and review-coverage statement.

A later correction does not erase an earlier record. Preserve the earlier entry and state which later entry controls the affected interpretation. Important examples include:

- `E-022` and `E-038` for family, business, and property chronology;
- `E-094` for the corrected Block 4 / Block 26 orientation;
- `E-014` for the Mitch/505 handling rule.

Real-estate ownership, business ownership, business operation, public/trade name, liquor-license role, and physical-building continuity are separate propositions. Do not merge them without direct support.

## Stable IDs and Status Records

Never renumber or reuse an ID. Numeric gaps 030, 031, and 044 under the `S` prefix are historical unassigned gaps and must not be backfilled.

When evidence narrows a question or completes a lead, update the existing `OQ-###` or `RL-###` record with an explicit status. Retain completed and superseded leads so the repository shows what was checked and why the task should not be repeated.

Run `python3 scripts/validate_archive.py` after changing evidence controls or YAML sidecars.
