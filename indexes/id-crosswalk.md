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
| `SM-008` 1925 Sanborn | `S-021` | `maps/sanborn/originals/1925-6 (5th).pdf` | `E-020`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-003`; possible 501 question |
| `SM-009` 1950 Sanborn | `S-022` | `maps/sanborn/originals/1950-6 (5th).pdf` | `E-020`, `E-102`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-003` |
| Aerial photocompare 1929–2025 | `S-023` | `media/photos/aerials/` (`IMG-0006`–`IMG-0043`) | `E-021`, `evidence/aerial-5th-main-photocompare-series.md` | `B-001`, `B-002`, `B-003`; `OQ-005`, `OQ-023` |

## Building / Business Crosswalk

| Building | Primary related businesses | Important evidence / sources |
| --- | --- | --- |
| `B-001` 503 Main Street | `BUS-001` Kwality Cafe; `BUS-004` The Wheel / Wheel Cafe at **503 only** | `E-001`, `E-002`, `E-003`, `E-020`, `E-021`, `E-022`, `E-025`, `E-042`–`E-045`, `E-047`–`E-049`, `E-094`–`E-099`, `E-103`, `E-108`; `S-024`-`S-028`, `S-048`–`S-052`, `S-054`–`S-058`, `S-107`–`S-115`, `S-117`. **Do not attach `E-038` to 503; the former Mrs. Nemeth/Nesmeth 503 purchase claim is superseded.** `E-095` is an archival lead; `E-096`–`E-097` and `E-103` leave 503's Gates/Wolf assignment unresolved. |
| `B-002` 505 Main Street | `BUS-005` 505 Tavern; `BUS-006` Thirsty Duck; `BUS-010` Brass Rail; `BUS-016` Dug Inn | `E-004`, `E-005`, `E-022`, `E-026`-`E-039`, `E-041`, `E-045`, `E-046`, `E-094`–`E-103`, `E-108`; `S-028`, `S-032`-`S-043`, `S-048`, `S-052`, `S-053`, `S-107`–`S-117`. `E-038` records the corrected Wiitanen purchase of the **505 building** from Mrs. Nesmeth/Nemeth after they had already begun operating Brass Rail. `E-100`/`S-116` corroborate **1940** inventory date from 2009 resurvey; **`E-101`** holds unresolved rear-expansion hypothesis for that date; **`E-102`** records August 2026 Sanborn/aerial footprint pass; `E-103` preserves the 1922 fire page without resolving 505's role. Interval pass: `evidence/source-captures/1973-1987-503-505-research-pass.md`. Rear/1940 hypothesis: `evidence/source-captures/505-rear-expansion-1940-date-hypothesis.md`; footprint pass: `evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md`. |
| `B-003` 507-511 Main Street / Harding Building | `BUS-007` Harding Drug Store; `BUS-008` Tony's Restaurant; `BUS-023` Dixon's Bakery fire context | Original-building evidence `E-016`, `E-017`, `E-020`, `E-021`, `E-045`, `E-094`, `E-108`; OHS retrieval lead `E-095`; `S-052`, `S-107`–`S-110`. Present replacement building dated **1968** by `S-063`. |
| `B-004` 527 Main Street / Swartz Building | Bailey & Price (1912; unmerged); Price Bros. `BUS-028` / Al Price `P-043` (1915) | `S-061` documents Bailey & Price in 1912; `E-107` / `S-120` documents Price Bros. at 527 in the 5 August 1915 directory and the same-issue incident report. No succession/identity bridge. `E-053`, `S-062`, `S-063` date the present **Swartz Building** to **1935**. |
| `B-005` 501 Main Street (historic / removed) | `BUS-024` Palace Saloon (1912); `BUS-025` Hunsaker & Taylor liquor premises (1913); 1925 store occupant unknown | `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`; `S-021`, `S-023`, `S-064`–`S-069`, `S-107`, `S-108`, `S-111`–`S-113`, `S-117`–`S-119`. The 1912/1913 notices do not prove a transfer or continuity. Gates's corner site may map principally to 501 or include 503; 501 remains live until the July restaurant address is proved. |
| `B-006` 513 Fifth Street (historic residence) | No business established | `E-106` / `S-118`: H. M. Templeton home, then occupied by M. D. Phillips and family in March 1912. Residential record only; no commercial/fire-cluster relation inferred. |

## Person / Business Crosswalk

| Person / entity | Related business or building | Notes |
| --- | --- | --- |
| `P-003` J. Jager | `BUS-002`, `B-001`, `A-001` / `IMG-0001` | Named proprietor on New Kwality Cafe matchbook. |
| `P-004` Larry | `BUS-003`, `B-001`, `A-002` / `IMG-0002` | Larry's Kwality Cafe name/person; surname unknown. |
| `P-005` Ray Hansen | `BUS-005`, `B-002` | Separate 505 Tavern history; distinct from Raye Grisham. Family history places him before Dick/Sheila's Brass Rail period; exact sale date pending. |
| `P-006` Raye LaFarlette / Raye Grisham | `BUS-004`, `B-001` | Same woman across surname change; grandmother; bought The Wheel at 503. The surname change is not a business transfer. No 505 tavern operator role. Supersedes older "Ray Grisham at 505" reading. |
| `P-007` Richard / Dick Wiitanen | `B-001`, `BUS-004`, `B-002`, `BUS-010` | Oregonian August 1985 names him owner of The Wheel Cafe **business** at 503. At 505, family history says Dick and Sheila **operated Brass Rail before owning the building**, then later purchased the **505 real estate** from Mrs. Nesmeth/Nemeth. They renamed the business 505 Tavern before selling it to their son Mitch. 2017 permit confirms continuing 505 property interest. Died November 2024; 505 then passed through his estate to Rodney and Mitch. |
| `P-008` Sheila Wiitanen | `B-001`, `B-002`, `BUS-010` | Daughter of Floyd and Raye. Operated Brass Rail at 505 with Dick before they owned the building; later co-purchased the 505 real estate from Mrs. Nesmeth/Nemeth. She and Dick renamed the business 505 Tavern before selling it to their son Mitch. Died 2014; Wiitanen property ownership continued through Dick's death in 2024. |
| `P-009` Willie | `B-002` | Bartender under Ray Hansen and later transition-era periods; full identity and exact employers still open. |
| `P-010` Victor | `BUS-004`, `B-001` | Restaurant manager in Raye Grisham's Wheel years and early Wiitanen years. |
| `P-011` Mitch / Mitchell (C.) Young | `BUS-005`, `BUS-009`, `B-002`, `E-004` | Same person as P-018; son of the Wiitanens. Acquired the already-named 505 Tavern in March 1991 and ran it through March 2004; not The Wheel. Do not claim he introduced or restored the name. Inherited 505 Main with Rodney from Dick's estate after Nov. 2024. |
| `P-012` Mike Berman | `BUS-005`, `B-002` | Told Commission he bought 505 Tavern in 2009; sold in 2017. |
| `P-013` Scott Forvilly | `BUS-006`, `B-002` | Purchased/reopened as Thirsty Duck in 2017. |
| `P-014` Rodney Young | `B-002`, archive steward | Inherited 505 Main with Mitchell Young from Dick Wiitanen's estate after Nov. 2024; co-owner through 505 LLC. |
| `P-018` Mitchell C. Young | `B-002`, `BUS-005` | Same person as P-011; legal/lease form of the name; 505 LLC managing member. Son of the Wiitanens; acquired the already-named 505 Tavern in March 1991. Inherited 505 with Rodney after Dick's death. |
| `P-034` Henry Brightbill | `B-001` | Merchant with a store at 503 Main in 1908 (`E-042`). |
| `P-019` Alin Guria | `B-002`, `BUS-006`, `E-018`, `S-011` | Current lessee and operating-business owner. Earlier Alan / dual-spelling wording was a project typo. Not a 505 real-estate owner. |
| `P-035` S. Wolf of Portland | `E-096`, `E-103`; `S-111`, `S-117`; `B-001`, `B-002`, `B-005` unresolved | Reported buyer of Harding's remainder and owner of the ignition building. Full identity, deed, land-versus-improvement ownership, and exact modern storefront remain unresolved; do not merge with other Wolf people/businesses. |
| `P-036` C. / C. E. Gates of Portland | `E-096`, `E-097`; `B-001`, `B-002`, `B-005` unresolved | Reported buyer of Fifth Street Restaurant location and owner/developer of the corner replacement. Full identity and modern footprint unresolved. |
| `P-020` Skyline Property Management | `B-002`, `E-018`, `S-011` | 2025 lease property manager / authorized agent. |
| `P-037` Joe Wilson | `BUS-024`, `B-005`, `E-104`, `S-118` | Palace Saloon liquor-license applicant at 501 Main in March 1912. No continuity/ownership inference. |
| `P-038` Hunsaker & Taylor | `BUS-025`, `B-005`, `E-104`, `S-119` | Printed partnership/style at 501 Main in October 1913; individual identities unresolved. |
| `P-039` H. M. Templeton | `B-006`, `E-106`, `S-118` | 513 Fifth resident in March 1912; wife's given name not printed. |
| `P-040` M. D. Phillips | `B-006`, `E-106`, `S-118` | Occupied the Templeton 513 Fifth home with family in March 1912. |

## Maintenance Rule

When a source, evidence item, media item, artifact, person, business, building, or map changes, update this crosswalk if the change affects an ID relationship.

## 1915 Courier sheets73–100 batch

| ID | Connected records | Scope |
| --- | --- | --- |
| S-120 | E-107; IMG-0054 through IMG-0161; RL-042 | 108 preserved PDF scans; per-image manifest in newspaper batch folder. |
| E-107 | S-120; B-003; B-004; E-054; RL-042; RL-043; T-017; T-018 | 507/509/511/519/527 listings, Price Bros. incident and Fifth/Main/repaving coverage; no 503/505 occupancy inference. |
| BUS-026 / P-041 | E-107; S-120; B-003; T-017 | W. W. Bradley at 507; transfer and uninterrupted occupancy unproven. |
| BUS-027 / P-042 | E-107; S-120; B-003; OQ-027; T-017 | H. P. Brightbill at 509; unmerged with Henry Brightbill P-034. |
| BUS-007 / P-001 | E-107; S-120; B-003; T-017 | Geo. A. Harding's 1915 business number is 511, not a backdated 507 building label. |
| BUS-028 / P-043 | E-107; S-120; B-004; IMG-0058; IMG-0060; OQ-028; RL-033; T-017; T-018 | Price Bros. / Al Price; incident-to-527 is same-issue inference. No Bailey & Price merger. |
| BUS-029 / P-044 | E-107; S-120; T-017; RL-043 | F. F. Theroux at 519 on 5 August; building identity/move unresolved. |
