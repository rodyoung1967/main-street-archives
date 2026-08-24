# Database

Structured YAML files mirror cross-reference data from the Markdown registers and entity pages.

## Source of Truth

**Markdown is authoritative.** Maintained YAML is a synchronized sidecar for relationship graphs and machine-readable lookups. See `docs/DECISIONS.md` (`D-001`, as amended by `D-008`) for operating rules.

- Always update Markdown when adding findings.
- Update the corresponding YAML sidecar in the same change.
- Never let YAML lag or contradict Markdown.

## YAML Scope

These entity types belong in `database/*.yml`:

| File | Entity prefix | Root key |
| --- | --- | --- |
| `people.yml` | `P-###` | `people:` |
| `businesses.yml` | `BUS-###` | `businesses:` |
| `buildings.yml` | `B-###` | `buildings:` |
| `evidence.yml` | `E-###` | `evidence:` |
| `sources.yml` | `S-###` | `sources:` |
| `artifacts.yml` | `A-###` | `artifacts:` |
| `oral-history.yml` | `OH-###` | `oral-history:` |
| `timeline.yml` | `T-###` | `timeline:` (curated milestones; `timeline.md` has no `T-###` mirror IDs) |
| `maps.yml` | `SM-###` | `maps:` |

## Markdown-Only Entities

These are tracked in Markdown registers only (no YAML file yet):

| Prefix | Register / location |
| --- | --- |
| `OQ-###` | `evidence/open-questions.md` |
| `RL-###` | `evidence/research-leads.md` |
| `IMG-###`, `DOC-###`, `MAP-###` | `media/catalog.md` |
| `R-###` | `records/` |
| `D-###` | `docs/DECISIONS.md` |

## Validation

Run `python scripts/validate_archive.py` to check ID cross-references and Markdown/YAML drift. See `scripts/README.md` for details.
