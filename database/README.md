# Database

Structured YAML files mirror cross-reference data from the Markdown registers and entity pages.

## Source of Truth

**Markdown is authoritative.** YAML is an optional sidecar for relationship graphs and machine-readable lookups. See `docs/DECISIONS.md` (D-001) for operating rules.

- Always update Markdown when adding findings.
- Update YAML when touching related entities; YAML lag is acceptable for low-priority entities.
- Never let YAML contradict Markdown.

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
| `timeline.yml` | `T-###` | `timeline:` |
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
