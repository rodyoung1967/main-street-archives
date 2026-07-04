# ID Crosswalk

This file connects the archive's ID systems so related records can be audited without relying on memory or search.

## ID Systems

| Prefix | Meaning | Canonical location |
| --- | --- | --- |
| `B-###` | Building / address record | `buildings/`, `database/buildings.yml`, `ARCHIVE_INDEX.md` |
| `BUS-###` | Business record | `businesses/`, `businesses/business-index.md`, `database/businesses.yml` |
| `P-###` | Person / family / organization record | `people/`, `people/people-index.md`, `database/people.yml` |
| `E-###` | Evidence item / claim support | `evidence/evidence-register.md` |
| `S-###` | Source record | `evidence/source-register.md` |
| `IMG-####` | Media/image metadata item | `media/photo-metadata-register.md` |
| `A-###` | Artifact record / physical artifact ID | `artifacts/images/README.md`, `media/photo-metadata-register.md` |
| `SM-###` | Sanborn map register item | `maps/sanborn-map-register.md` |

## Artifact and Image Crosswalk

| Artifact / media | Repository file | Evidence | Source | Building | Business | People |
| --- | --- | --- | --- | --- | --- | --- |
| `A-001` / `IMG-0001` New Kwality Cafe matchbook | `artifacts/images/A-001-new-kwality-cafe-matchbook.jpg` | `E-002` | `S-002` | `B-001` 503 Main | `BUS-002` New Kwality Cafe | `P-003` J. Jager |
| `A-002` / `IMG-0002` Larry's Kwality Cafe matchcover | `artifacts/images/A-002-larrys-kwality-cafe-matchcover.jpg` | `E-003` | `S-003` | `B-001` 503 Main | `BUS-003` Larry's Kwality Cafe | `P-004` Larry |
| `IMG-0003` Thebeerchaser 505 Tavern comment screenshot | `media/screenshots/thebeerchaser-505-tavern-comment-2021.png` pending upload | `E-013` | `S-009` | `B-002` 505 Main | `BUS-005` 505 Tavern | Pending / unidentified commenters |
| `IMG-0004` The Wheel at 503 / 505 Tavern adjacent metadata | External / Time Capsule Maps metadata | `E-015` | `S-010` | `B-001`, `B-002` | `BUS-004`, `BUS-005` | Pending |
| `IMG-0005` 5th / McLoughlin / US99E / Main Street circa-1910 metadata | External / Time Capsule Maps metadata | `E-015`, `E-017` | `S-010` | `B-001`, `B-002`, `B-003` | Pending / contextual | Pending |

## Sanborn Map Crosswalk

| Map ID | Source | Repository file | Evidence / comparison | Buildings |
| --- | --- | --- | --- | --- |
| `SM-001` Sanborn key | `S-014` | `maps/sanborn/originals/sanborn key.pdf` | Supports interpretation of all Sanborn evidence | `B-001`, `B-002`, `B-003` |
| `SM-002` 1884 master map | `S-015` | `maps/sanborn/originals/1884-01- Master Map (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | `B-001`, `B-002`, `B-003` |
| `SM-003` 1888 Sanborn | `S-016` | `maps/sanborn/originals/1888-02 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | `B-001`, `B-002`, `B-003` |
| `SM-004` 1890 Sanborn | `S-017` | `maps/sanborn/originals/1890-02 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | `B-001`, `B-002`, `B-003` |
| `SM-005` 1892 Sanborn | `S-018` | `maps/sanborn/originals/1892-03 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | `B-001`, `B-002`, `B-003` |
| `SM-006` 1900 Sanborn | `S-019` | `maps/sanborn/originals/1900-13 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | `B-001`, `B-002`, `B-003` |
| `SM-007` 1911 Sanborn | `S-020` | `maps/sanborn/originals/1911-22 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | Use carefully; may cover a different 5th/Center context |
| `SM-008` 1925 Sanborn | `S-021` | `maps/sanborn/originals/1925-6 (5th).pdf` | `E-020`, `EV-SAN-1925-1950-001`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-003`; possible 501 question |
| `SM-009` 1950 Sanborn | `S-022` | `maps/sanborn/originals/1950-6 (5th).pdf` | `E-020`, `EV-SAN-1925-1950-001`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-003` |

## Building / Business Crosswalk

| Building | Primary related businesses | Important evidence / sources |
| --- | --- | --- |
| `B-001` 503 Main Street | `BUS-001` Kwality Cafe; `BUS-002` New Kwality Cafe; `BUS-003` Larry's Kwality Cafe; `BUS-004` The Wheel question | `E-001`, `E-002`, `E-003`, `E-011`, `E-015`, `E-020`; `S-001`, `S-002`, `S-003`, `S-010`, `S-014`-`S-022` |
| `B-002` 505 Main Street | `BUS-004` The Wheel question; `BUS-005` 505 Tavern; `BUS-006` Thirsty Duck; `BUS-009` The 505; `BUS-010` Brass Rail Tavern | `E-004`, `E-005`, `E-006`, `E-007`, `E-008`, `E-010`, `E-011`, `E-013`, `E-014`, `E-015`, `E-018`, `E-020`; `S-004`, `S-005`, `S-009`, `S-010`, `S-011`, `S-014`-`S-022` |
| `B-003` 507 Main Street / Harding Building | `BUS-007` Harding Drug Store; `BUS-008` Tony's Restaurant | `E-016`, `E-017`, `E-020`; `S-012`, `S-014`-`S-022` |

## Person / Business Crosswalk

| Person / entity | Related business or building | Notes |
| --- | --- | --- |
| `P-003` J. Jager | `BUS-002`, `B-001`, `A-001` / `IMG-0001` | Named proprietor on New Kwality Cafe matchbook. |
| `P-004` Larry | `BUS-003`, `B-001`, `A-002` / `IMG-0002` | Larry's Kwality Cafe name/person; surname unknown. |
| `P-005` Ray Hansen | `B-002` | Oral-history owner before Richard / Dick and Sheila. |
| `P-006` Ray Grisham | `BUS-004`, `B-002` | Keep distinct from Ray Hansen until documentary records clarify. |
| `P-007` Richard / Dick Wiitanen | `B-002` | Owned after Ray Hansen with Sheila; died November 2024. |
| `P-008` Sheila Wiitanen | `B-002` | Owned after Ray Hansen with Richard / Dick; died 2014. |
| `P-009` Willie | `B-002` | Bartender under Ray Hansen and Richard / Dick and Sheila. |
| `P-010` Victor | `BUS-004`, `B-002` | Restaurant manager in Ray Grisham / early Wiitanen context. |
| `P-011` Mitch Young | `BUS-009`, `B-002`, `E-004`, `E-014` | Owned and operated the 505 Main Street business / The 505 from March 1991 to March 2004; do not automatically label this period The Wheel. |
| `P-012` Mike Berman | `BUS-005`, `B-002` | Sold 505 Tavern in 2017. |
| `P-013` Scott Forvilly | `BUS-006`, `B-002` | Purchased/reopened as Thirsty Duck in 2017. |
| `P-014` Rodney Young | `B-002`, archive steward | Current owner/project steward. |
| `P-018` Mitchell C. Young | `B-002`, `BUS-009` | 505 LLC managing member / family-history participant. |
| `P-019` Alin Guria | `B-002`, `E-018`, `S-011` | 2025 lessee. |
| `P-020` Skyline Property Management | `B-002`, `E-018`, `S-011` | 2025 lease property manager / authorized agent. |

## Maintenance Rule

When a source, evidence item, media item, artifact, person, business, building, or map changes, update this crosswalk if the change affects an ID relationship.