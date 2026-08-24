# The Main Street Archive

## Project Name

The Main Street Archive

History of 503 and 505 Main Street, Oregon City, Oregon, with the surrounding Fifth-to-Sixth Street frontage retained as research context.

## Mission

Preserve the complete documented and oral history of the buildings, businesses, and people associated with 503 and 505 Main Street. Retain 501, 507-511, 527, and other nearby addresses when they materially help establish block geography, predecessor structures, business movement, fire history, or ownership.

Every factual statement should be traceable to supporting evidence.

Preserve conflicting evidence rather than discarding it.

## Evidence Hierarchy

1. Primary documents: deeds, permits, tax records, newspapers, city directories
2. Primary artifacts: matchbooks, menus, photos, business cards, signage
3. Primary participant testimony: owners, employees, direct witnesses
4. Family oral history
5. Secondary published sources
6. Community recollections

## Repository Structure

- `buildings/`
- `businesses/`
- `people/`
- `evidence/`
- `artifacts/`
- `newspapers/`
- `maps/`
- `media/`
- `records/`
- `oral-history/`
- `database/`
- `registers/`
- `indexes/`
- `docs/`

See `DATA_LAYOUT.md` for canonical raw-source locations. The former top-level `photos/`, `deeds/`, and `tax-records/` paths are retired and must not be recreated.

## ID System

- `B-###`
- `BUS-###`
- `P-###`
- `E-###`
- `S-###`
- `A-###`
- `OH-###`
- `T-###`
- `RL-###`
- `OQ-###`

## Research Rules

- Never overwrite conflicting evidence.
- Record confidence for every evidence item.
- Preserve source URLs.
- Distinguish oral history from documentary evidence.
- Maintain a complete audit trail.
- Use only the year-status terms defined in `RESEARCH-STANDARD.md`; a targeted or OCR-assisted pass is not an online-complete year.
- Keep Markdown registers and maintained YAML sidecars synchronized in the same change.
