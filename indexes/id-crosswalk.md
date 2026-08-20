# ID Crosswalk

This file connects the archive's ID systems so related records can be audited without relying on memory or search.

## ID Systems

| Prefix | Meaning | Canonical location |
| --- | --- | --- |
| `B-###` | Building / address record | `buildings/`, `database/buildings.yml`, `ARCHIVE_INDEX.md` |
| `BUS-###` | Business record | `businesses/`, `businesses/business-index.md`, `database/businesses.yml` |
| `P-###` | Person / family / organization record | `people/`, `people/people-index.md`, `database/people.yml` |
| `E-###` | Evidence item / claim support | `evidence/evidence-register.md`; detailed standalone evidence notes may also live under `evidence/` |
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
| `IMG-0044` Oregonian 25 Aug. 1908 Brightbill | `newspapers/oregonian/1908-503-main-missing-girl-oregonian.png` | `E-042` | `S-049` | `B-001` 503 Main | Pending | `P-034` Henry Brightbill |
| `IMG-0045` Oregonian 12 June 1937 Kwality for sale | `newspapers/oregonian/1937-kwality-cafe-for-sale-oregonian.png` | `E-043` | `S-050` | `B-001` by archive association | `BUS-001` Kwality Cafe | Pending |
| `IMG-0046` Oregonian 30 Nov. 1960 Wheel Cafe | `newspapers/oregonian/1960-wheel-cafe-oregonian.png` | `E-044` | `S-051` | `B-001` 5th and Main | `BUS-004` The Wheel / Wheel Cafe | Pending |
| `IMG-0047` Oregonian 2 Sept. 1967 fire | `newspapers/oregonian/1967-09-wheel-505-fire-oregonian.png` | `E-045` | `S-052` | `B-001`, `B-002`, `B-003` | `BUS-004`, `BUS-005`, `BUS-007`, `BUS-023` | Pending |
| `IMG-0048` Oregonian 8 Feb. 1976 505 Tavern classified | `newspapers/oregonian/1976-505-main-classified-oregonian.png` | `E-046` | `S-053` | `B-002` 505 Main | `BUS-005` 505 Tavern | Pending |
| `IMG-0049` Oregonian 18 Apr. 1983 Wheel Cafe crop | `newspapers/oregonian/1983-the-wheel-oregonian.png` | `E-047` | `S-054` | `B-001` | `BUS-004` | Pending |
| `IMG-0050` Oregonian 18 Apr. 1983 Wheel Cafe fuller page | `newspapers/oregonian/1983-wheel-cafe-oregonian.png` | `E-047` | `S-058` | `B-001` | `BUS-004` | Pending |
| `IMG-0051` Oregonian 25 Apr. 1985 lottery list | `newspapers/oregonian/1985-the-wheel-oregonian.png` | `E-048` | `S-055` | `B-001` 503 Main | `BUS-004` | Pending |
| `IMG-0052` Oregonian 21 Aug. 1985 Wiitanen / Wheel | `newspapers/oregonian/1985-08-the-wheel-oregonian-2.png` | `E-049` | `S-056` | `B-001` 503 Main | `BUS-004` | `P-007` Richard M. Wiitanen |
| `IMG-0053` Oregonian 27 Aug. 1985 Wiitanen / Wheel | `newspapers/oregonian/1985-08-the-wheel-oregonian.png` | `E-049` | `S-057` | `B-001` 503 Main | `BUS-004` | `P-007` Richard M. Wiitanen |

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
| Aerial photocompare 1929–2025 | `S-023` | `media/photos/aerials/` (`IMG-0006`–`IMG-0043`) | `E-021`, `evidence/aerial-5th-main-photocompare-series.md` | `B-001`, `B-002`, `B-003`; `OQ-005`, `OQ-023` |

## Building / Business Crosswalk

| Building | Primary related businesses | Important evidence / sources |
| --- | --- | --- |
| `B-001` 503 Main Street | `BUS-001` Kwality Cafe; `BUS-004` The Wheel / Wheel Cafe at **503 only** | `E-001`, `E-002`, `E-003`, `E-020`, `E-021`, `E-022`, `E-025`, `E-042`–`E-045`, `E-047`–`E-049`; `S-024`-`S-028`, `S-048`–`S-052`, `S-054`–`S-058`. **Do not attach `E-038` to 503; the former Mrs. Nemeth/Nesmeth 503 purchase claim is superseded.** |
| `B-002` 505 Main Street | `BUS-005` 505 Tavern; `BUS-006` Thirsty Duck; `BUS-010` Brass Rail; `BUS-016` Dug Inn | `E-004`, `E-005`, `E-022`, `E-026`-`E-039`, `E-041`, `E-045`, `E-046`; `S-028`, `S-032`-`S-043`, `S-048`, `S-052`, `S-053`. `E-038` records the corrected Wiitanen purchase of the **505 building** from Mrs. Nesmeth/Nemeth after they had already begun operating Brass Rail. |
| `B-003` 507-511 Main Street / Harding Building | `BUS-007` Harding Drug Store; `BUS-008` Tony's Restaurant; `BUS-023` Dixon's Bakery fire context | Original-building evidence `E-016`, `E-017`, `E-020`, `E-021`, `E-045`; `S-052`. Present replacement building dated **1968** by `S-063`. |
| `B-004` 527 Main Street / Swartz Building | Bailey & Price documented at 527 in 1912; current building/business chronology still being expanded | `S-061` documents Bailey & Price at 527 in 1912. `E-053`, `S-062`, `S-063` identify the present **Swartz Building** and date it to **1935**. Detailed note: `records/historic-surveys/527-main-swartz-building-1935-source-note.md`. |

## Person / Business Crosswalk

| Person / entity | Related business or building | Notes |
| --- | --- | --- |
| `P-003` J. Jager | `BUS-002`, `B-001`, `A-001` / `IMG-0001` | Named proprietor on New Kwality Cafe matchbook. |
| `P-004` Larry | `BUS-003`, `B-001`, `A-002` / `IMG-0002` | Larry's Kwality Cafe name/person; surname unknown. |
| `P-005` Ray Hansen | `BUS-005`, `B-002` | Separate 505 Tavern history; distinct from Raye Grisham. Family history places him before Dick/Sheila's Brass Rail period; exact sale date pending. |
| `P-006` Raye LaFarlette / Raye Grisham | `BUS-004`, `B-001` | Same woman across surname change; grandmother; bought The Wheel at 503. The surname change is not a business transfer. No 505 tavern operator role. Supersedes older "Ray Grisham at 505" reading. |
| `P-007` Richard / Dick Wiitanen | `B-001`, `BUS-004`, `B-002`, `BUS-010` | Oregonian August 1985 names him owner of The Wheel Cafe **business** at 503. At 505, family history says Dick and Sheila **operated Brass Rail before owning the building**, then later purchased the **505 real estate** from Mrs. Nesmeth/Nemeth. 2017 permit confirms continuing 505 property interest. Died November 2024; 505 then passed through his estate to Rodney and Mitch. |
| `P-008` Sheila Wiitanen | `B-001`, `B-002`, `BUS-010` | Daughter of Floyd and Raye. Operated Brass Rail at 505 with Dick before they owned the building; later co-purchased the 505 real estate from Mrs. Nesmeth/Nemeth. Died 2014; Wiitanen property ownership continued through Dick's death in 2024. |
| `P-009` Willie | `B-002` | Bartender under Ray Hansen and later transition-era periods; full identity and exact employers still open. |
| `P-010` Victor | `BUS-004`, `B-001` | Restaurant manager in Raye Grisham's Wheel years and early Wiitanen years. |
| `P-011` Mitch / Mitchell (C.) Young | `BUS-005`, `BUS-009`, `B-002`, `E-004` | Same person as P-018. Ran 505 Tavern March 1991-March 2004; not The Wheel. Do not claim he restored it. Inherited 505 Main with Rodney from Dick's estate after Nov. 2024. |
| `P-012` Mike Berman | `BUS-005`, `B-002` | Told Commission he bought 505 Tavern in 2009; sold in 2017. |
| `P-013` Scott Forvilly | `BUS-006`, `B-002` | Purchased/reopened as Thirsty Duck in 2017. |
| `P-014` Rodney Young | `B-002`, archive steward | Inherited 505 Main with Mitchell Young from Dick Wiitanen's estate after Nov. 2024; co-owner through 505 LLC. |
| `P-018` Mitchell C. Young | `B-002`, `BUS-005` | Same person as P-011; legal/lease form of the name; 505 LLC managing member. Inherited 505 with Rodney after Dick's death. |
| `P-034` Henry Brightbill | `B-001` | Merchant with a store at 503 Main in 1908 (`E-042`). |
| `P-019` Alan / Alin Guria | `B-002`, `E-018`, `S-011` | Current lessee. Lease spelling Alin; steward confirmation Alan. |
| `P-020` Skyline Property Management | `B-002`, `E-018`, `S-011` | 2025 lease property manager / authorized agent. |

## Maintenance Rule

When a source, evidence item, media item, artifact, person, business, building, or map changes, update this crosswalk if the change affects an ID relationship.
