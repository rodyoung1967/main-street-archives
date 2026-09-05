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
| `IMG-0044` Oregonian 25 Aug. 1908 Brightbill | `newspapers/oregonian/1908-503-main-missing-girl-oregonian.png` | `E-042` | `S-049` | `B-001` 503 Main | `BUS-078` Henry Brightbill's store | `P-034` Henry Brightbill |
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
| `SM-007` 1911 Sanborn Sheet 22, Canemah | `S-020` | `maps/sanborn/originals/1911-22 (5th).pdf` | `E-020`, `maps/sanborn-comparison-503-505-507.md` | Geographic control only; visually confirmed not to cover the downtown 501/503/505/507 frontage |
| `SM-008` 1925 Sanborn | `S-021` | `maps/sanborn/originals/1925-6 (5th).pdf` | `E-020`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-005`; separate 501 store, 503 restaurant, and 505 billiards/cigars uses established; tenants and continuity open |
| `SM-009` 1950 Sanborn | `S-022` | `maps/sanborn/originals/1950-6 (5th).pdf` | `E-020`, `E-102`, `evidence/sanborn-1925-1950-evidence.md` | `B-001`, `B-002`, `B-003` |
| Aerial photocompare 1929–2025 | `S-023` | `media/photos/aerials/` (`IMG-0006`–`IMG-0043`) | `E-021`, `evidence/aerial-5th-main-photocompare-series.md` | `B-001`, `B-002`, `B-003`; `OQ-005`, `OQ-023` |

## Building / Business Crosswalk

| Building | Primary related businesses | Important evidence / sources |
| --- | --- | --- |
| `B-001` 503 Main Street | `BUS-078` Brightbill; `BUS-019` Smith; `BUS-020` Hylton; `BUS-001`–`BUS-003` Kwality lineage; `BUS-004` Wheel; `BUS-018` White Rabbit / Black Ink | Unified chronology: `timelines/503-main.md`. `E-001`–`E-003`, `E-020`–`E-025`, `E-042`–`E-049`, `E-094`–`E-099`, `E-103`, `E-108`. **Do not attach `E-038` to 503.** Gates/Wolf assignment remains unresolved. |
| `B-002` 505 Main Street | `BUS-007` Harding catalog-photo context; `BUS-067` Young; `BUS-011`–`BUS-017`, `BUS-021`, `BUS-022`, plus `BUS-005`, `BUS-006`, `BUS-009`, `BUS-010`, `BUS-016` | Unified chronology: `timelines/505-main.md`. `S-148`/`E-133`/`IMG-0724` catalogs Harding at 505 in 1880/1880s but the pre-1906 number may be retrospective. `S-149`/`E-134`/`IMG-0725` visibly establishes Young at 505 in 1910. `S-150`/`E-135` adds a visually verified June 1920 exact-use anchor at 505½ Main; it is not construction proof. Includes distinct Farr (`BUS-013`) and Harr (`BUS-014`) records. Business operation, real-estate ownership and physical-building continuity remain separate. |
| `B-003` 507-511 Main Street / Harding Building | `BUS-007` Harding Drug Store; `BUS-008` Tony's Restaurant; `BUS-023` Dixon's Bakery/Pastry Shop; `BUS-026` W. W. Bradley; `BUS-027` H. P. Brightbill; `BUS-067` G. H. Young | `E-128` / `S-143` / `IMG-0714` directly places Harding at 511 in January 1911. `E-129`–`E-130` / `S-144`–`S-145` / `IMG-0715`–`IMG-0716` establish Dixon's at 509 in June 1964 and an unnamed 509 baking/coffee shop sale ad in December 1965. Present replacement dated **1968** by `S-063`; do not backdate that consolidated footprint. |
| `B-004` 527 Main Street / Swartz Building | Bailey & Price (1912; unmerged); Price Bros. `BUS-028` / Al Price `P-043` (1915) | `S-061` documents Bailey & Price in 1912; `E-107` / `S-120` documents Price Bros. at 527 in the 5 August 1915 directory and the same-issue incident report. No succession/identity bridge. `E-053`, `S-062`, `S-063` date the present **Swartz Building** to **1935**. |
| `B-005` 501 Main Street (historic / removed) | `BUS-045` A. J. Surber; `BUS-024` Palace Saloon; `BUS-025` Hunsaker & Taylor; 1925 store occupant unknown | Unified chronology: `timelines/501-main.md`. `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`. `E-151`–`E-153` refine Palace chronology, but only `E-104` directly prints Palace at 501; 1907/1909/June-1912 intersection/name context is not backfilled to the number. |
| `B-006` 513 Fifth Street (historic residence) | No business established | `E-106` / `S-118`: H. M. Templeton home, then occupied by M. D. Phillips and family in March 1912. Residential record only; no commercial/fire-cluster relation inferred. |
| `B-007` 107 Fifth Street | Tenant unresolved; Blacksmith use | `E-117` / `S-131`: exact ledger address/use; no named tenant inferred. |
| `B-008` 108 Fifth Street | `BUS-039` Scripture & May; later S. F. Scripture | `E-119`, `E-120`, `E-124`; `S-133`, `S-134`, `S-138`. No bridge to 110 Fifth, Fashion Stable or May & Washburn. |
| `B-009` 109 Fifth Street / Oregon City Laundry | `BUS-068`; Blakeslee and later Knoepel/Schofield chronology | `E-124`, `E-125`, `E-103`, `E-102`. Pre-fire plant destroyed July 1922; 1925 mapped laundry is later physical presence. |
| `B-010` 110 Fifth Street | Stable use; probable Scripture & May tenant reading only | `E-117` / `S-131`. Do not convert probable handwriting into a tenant fact. |
| `B-011` 519 Main Street | `BUS-029` Theroux; `BUS-073` Pantorium; temporary `BUS-068` laundry office | `E-107`, `E-120`, `E-103`. Temporary office is not production use. |
| `B-012` 526 Main Street | `BUS-032` Eddy's Dependable Store | `E-109` / `S-121`; one dated advertisement, proprietor/title unresolved. |
| `B-013` 617 Main / Beaver Building | `BUS-031`, `BUS-037`, `BUS-040` | `E-109`, `E-116`, `E-119`, `E-120`; dated occupants, not one-room succession. |
| `B-014` 619 Main / Andresen Building | `BUS-031` Electric Store/power offices | `E-119`, `E-120`; exact 1916–1917 address, earlier Andresen references not backdated. |
| `B-015` 516 Main Street | `BUS-079` B. J. Staats Hardware | `S-147` / `E-132` / `IMG-0723`: cataloged December 1919 snow photograph; address/date from institutional metadata, business fascia and sale signs visible. No closure/transfer/title inference. |

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
| `P-034` Henry Brightbill | `BUS-078`, `B-001` | Merchant with a store at 503 Main in 1908 (`E-042`). |
| `P-019` Alin Guria | `B-002`, `BUS-006`, `E-018`, `S-011` | Current lessee and operating-business owner. Earlier Alan / dual-spelling wording was a project typo. Not a 505 real-estate owner. |
| `P-035` S. Wolf of Portland | `E-096`, `E-103`; `S-111`, `S-117`; `B-001`, `B-002`, `B-005` unresolved | Reported buyer of Harding's remainder and owner of the ignition building. Full identity, deed, land-versus-improvement ownership, and exact modern storefront remain unresolved; do not merge with other Wolf people/businesses. |
| `P-036` C. / C. E. Gates of Portland | `E-096`, `E-097`; `B-001`, `B-002`, `B-005` unresolved | Reported buyer of Fifth Street Restaurant location and owner/developer of the corner replacement. Full identity and modern footprint unresolved. |
| `P-020` Skyline Property Management | `B-002`, `E-018`, `S-011` | 2025 lease property manager / authorized agent. |
| `P-037` Joe Wilson | `BUS-024`, `B-005`, `E-104`, `S-118` | Palace Saloon liquor-license applicant at 501 Main in March 1912. No continuity/ownership inference. |
| `P-038` Hunsaker & Taylor | `BUS-025`, `B-005`, `E-104`, `S-119` | Printed partnership/style at 501 Main in October 1913; individual identities unresolved. |
| `P-039` H. M. Templeton | `B-006`, `E-106`, `S-118` | 513 Fifth resident in March 1912; wife's given name not printed. |
| `P-040` M. D. Phillips | `B-006`, `E-106`, `S-118` | Occupied the Templeton 513 Fifth home with family in March 1912. |
| `P-076` G. H. Young / George Young | `BUS-067`, `B-002`, `B-003`, `E-085`, `E-092`, `E-134`, `S-149`, `IMG-0725` | Young's Secondhand Store visibly at 505 in CCHS 1910 photograph; 1911 Harding-to-Willamette move; 507 Main in 1912/1914. Strong 505→507 sequence; exact move day, ownership and physical continuity unresolved. |
| `P-077`–`P-081` Blakeslee / Knoepel / Schofield records | `BUS-068`, `B-009`, `E-103`, `E-124`, `E-125` | Distinct dated Oregon City Laundry roles; no silent identity or ownership merger. |
| `P-082` S. F. Scripture / `P-083` L. E. May | `BUS-039`, `B-008` | Scripture & May at 108 Fifth; later May & Washburn identity/succession unproved. |
| `P-085`–`P-088` Schieremann / Ketchner / Blake / Gage-Blake conflict | `BUS-070`, `BUS-072`, `BUS-075`, `E-103` | July 1922 fire cluster; address and owner/operator conflicts preserved. |
| `P-089`–`P-091` Leland / Little / Timms | `BUS-076`, `BUS-077`, `E-126` | Distinct billiards identities/records; no 505 or fire-adjacent assignment. |
| `P-092` R. A. Junken | `BUS-070`, `E-097` | Contractor for Gates's August 1922 replacement; exact footprint unresolved. |
| `P-093` F. Champion | `BUS-073` | Pantorium owner at 416 Main in 1914; later continuity unproved. |
| `P-094` Carl R. Harr | `BUS-014`, `B-002`, `E-127`, `S-142` | Directly named with Harr's Recreation Center, 505 Main, in late 1948. Distinct from Edwin F. and Alice Farr; exact Farr-to-Harr transition remains open. |
| `P-095` B. J. Staats | `BUS-079`, `B-015`, `E-132`, `S-147`, `IMG-0723` | Name displayed on the cataloged December 1919 516 Main hardware storefront; initials and ownership remain unresolved. |

## Maintenance Rule

When a source, evidence item, media item, artifact, person, business, building, or map changes, update this crosswalk if the change affects an ID relationship.

## 30 August 2026 media reconciliation

| Media | Repository location | Connected records / limits |
| --- | --- | --- |
| `IMG-0711`–`IMG-0713` | `maps/images/` | `S-146` / `E-131`; undated Sanborn-style crops, exact sheets/editions unresolved; `B-001`–`B-003`. |
| `IMG-0714` | `newspapers/morning-enterprise/1911-01-10-george-harding-druggist-511-main-screenshot.png` | `S-143` / `E-128`; `BUS-007`, `P-001`, `B-003`. Legacy c.1915–1916 Courier filename superseded. |
| `IMG-0715` | `newspapers/oregonian/1965-12-05-509-main-baking-coffee-shop-for-sale.png` | `S-145` / `E-130`; unnamed 509 shop, no Dixon/sale inference; `B-003`. |
| `IMG-0716` | `newspapers/oregonian/1964-06-10-dixons-pastry-shop-509-main.png` | `S-144` / `E-129`; `BUS-023`, `B-003`. Legacy Amplifier/1949/519 labels superseded. |
| `IMG-0717`–`IMG-0721` | `records/directories/1915-1916-polk-oregon-city/` | Existing `S-132` / `E-118` FamilySearch directory page set. |
| `IMG-0722` | `media/photos/early-main-street/IMG-0722_tom-keene-cigar-sign-crop-reported-1908.jpg` | Tom Keene cigar-sign crop; no source/evidence/address claim; former filename's 1908 assertion remains unverified. |
| `IMG-0723` | `media/photos/early-main-street/IMG-0723_1919-12-516-main-bj-staats-hardware-snow.jpg` | `S-147` / `E-132`; `B-015`, `BUS-079`, `P-095`. Catalog metadata supplies 516 Main/December 1919/22 inches; image visibly supplies storefront and sale signs; rights unresolved. |
| `IMG-0724` | `media/photos/early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg` | `S-148` / `E-133`; `B-002`, `BUS-007`, `P-001`. CCHS supplies 505 and 1880/1880s wording; crop supplies visible Harding fascia but no number. Retrospective-address and continuity limits preserved. |
| `IMG-0725` | `media/photos/early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg` | `S-149` / `E-134`; `B-002`, `B-003`, `BUS-067`, `P-076`. Image visibly shows 505/store name; CCHS supplies 1910 and George Young identification. Strong 505→507 sequence only. |

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

## 1915 Courier sheets101–110 batch

| ID | Connected records | Scope |
| --- | --- | --- |
| S-121 | E-109; IMG-0162–IMG-0202; RL-042/RL-043 | Forty preserved PDFs plus alternate IIIF header; checkpoint110/123, pause before Dec2. |
| E-109 | S-121; E-054/E-107; T-019–T-021; B-003/B-004 address context | Dated507/509/511/519/527 confirmations,526/617 anchors, Mass opening and Fifth road-work report. |
| BUS-007 / P-001; BUS-026 / P-041; BUS-027 / P-042; BUS-029 / P-044 | E-109; S-121; T-020 | Harding511, Bradley507, Brightbill509, Theroux519 through Nov25; no identity/transfer proof. |
| BUS-028 | E-109; S-121; B-004; T-020 | Price Bros.527 through Nov25; priorAlPrice evidence remainsE-107. |
| BUS-030 / P-045 | E-109; S-121; T-019; RL-043 | Mass's Hotel and Restaurant in former Brunswick quarters; exact number/title unresolved. |
| BUS-031 | E-109; S-121; T-020; RL-043 | Electric Store / company at617 Main, Beaver Building; no buildingID assigned. |
| BUS-032 | E-109; S-121; T-020; RL-043 | Eddy's at526 Main; no proprietor identity or buildingID assigned. |
| T-021 | E-109; S-121; RL-043 | Fifth Street road-work report only, no storefront/parcel assignment. |

## 1922 Tasks 5–6 identity and visual-verification checkpoint

Current synthesis: [Task 7 model test](../evidence/source-captures/1922-task-7-fire-origin-model-test-2026-08-28.md) refines `E-108` and connects `E-094`–`E-097`, `E-103`, `E-104`, `E-113`, `SM-008`, `B-001`/`B-002`/`B-005`, `P-035`/`P-036`/`P-046` and `BUS-012` **without new identity, ownership or occupancy assignments**. [Task 8 handoff](../evidence/source-captures/1922-task-8-integration-handoff-2026-08-28.md) consolidates eight `1922-F` callouts and remaining online work. Neither model selected; 1922 IN PROGRESS. No IDs renumbered or new IDs needed for the synthesis.

| ID | Connected records | Scope |
| --- | --- | --- |
| E-113 | S-125–S-127; P-046; BUS-012; T-024; OQ-031; RL-040 | Direct Springfield Miller association; candidate comparisons do not establish buyer identities or property boundaries. |
| S-125 / IMG-0409 | E-113; P-046; BUS-012; T-024 | 3 February 1916 Lane County News p1; targeted item and masthead verified. Not 1916 occupancy at 505. |
| S-126 / IMG-0410–IMG-0412 | E-113; P-035/P-036 comparison only | 1920 Portland directory pp542/543/1538; no candidate merger; clipped-edge limits preserved. |
| S-127 / IMG-0413 | E-113; P-036 comparison only | Secondary Medford Gates nomination, only PDF p15 reviewed; no Oregon City buyer bridge. |
| P-046 / T-024 | E-113; S-125; BUS-012 | Gilbert Miller directly named with Springfield firm; retain 1918 C. E. Miller discrepancy. |

## 1916 Courier pages 106–180

| IDs | Connected records | Scope |
| --- | --- | --- |
| S-130; IMG-0479–IMG-0553 | E-116; `newspapers/oregon-city-courier/1916-pages-106-180/` | 75 unchanged original page PDFs, visual ledger and hashes. |
| E-116 | S-130; B-001/B-002/B-003/B-004/B-005 | Coverage and neighboring context, no new target assignment. |
| P-047; P-048; P-049; P-050; P-051 | E-116; S-130 | Hall, Anderson, Martin, Holman, Randall; initials preserved. |
| BUS-033; BUS-034; BUS-035; BUS-036 | E-116; S-130 | Gas branch, chiropractic practice, undertaking establishment, Raasch/Lamb. |
| BUS-007/BUS-026/BUS-027/BUS-028/BUS-029/BUS-031 | E-116; P-001/P-041/P-042/P-044 | Dated neighborhood ad confirmations; no new proprietor or transfer inference. |

## 1915–1916 Polk gazetteer access audit

| IDs | Connected records | Scope |
| --- | --- | --- |
| S-132 / E-118 / RL-044 | B-001; B-002; B-003; B-005; P-001; P-042; P-050; P-051; BUS-007; BUS-027; completed manual callout 1915-D01 | Authenticated visual review of complete Oregon City town section pp. 260–262 and relevant druggist/undertaker classified pages. Trades/names corroborated, but no target Main/Fifth number is printed and no silence is treated as vacancy or absence. |

## 1916 first monthly Courier issues

| IDs | Connected records | Scope |
| --- | --- | --- |
| S-133; IMG-0554–IMG-0611 | E-119; `newspapers/oregon-city-courier/1916-first-monthly-june-december/` | 58 unchanged originals, seven complete monthly issues, hashes/page ledger. |
| E-119 | B-001/B-002/B-005; E-116/E-117 | Target/Fifth context and coverage; no new 503/505 occupant or ledger-to-street-number merger. |
| P-052; BUS-037 | P-053; BUS-038; E-119/S-133 | Schilling move announcement and Pruden advertised succession; transaction details unresolved. |
| BUS-039 | E-119/S-133; E-117 comparison only | Scripture & May 108 Fifth by September 7; no automatic ledger 110 or May & Washburn bridge. |
| BUS-040; BUS-041; BUS-042; BUS-043 | BUS-031; BUS-036; E-119/S-133 | Andresen rearrangement announced June 1; Electric Store completed-move wording July 6. |
| P-054; BUS-044 | E-119/S-133 | Proposed second Hawley unit postponed; not target construction proof. |
| P-050; P-051; BUS-035 | E-116; E-119/S-133 | Joint ad July 6, Holman-alone by August 3; April sale report remains controlling. |

## 1907–1908 uploaded Courier visual review

| Source / media | Evidence | Connected records |
| --- | --- | --- |
| S-135 / IMG-0708 | E-121, E-123 | B-005; T-025; dated 1907 entities below |
| S-136 / IMG-0709 | E-122 | P-056 / BUS-046; T-026; no numbered building assignment |
| S-137 / IMG-0710 | E-121, E-122, E-123 | T-026; intersection-only Surber/Justin; dated 1908 entities below |

| Person | Business | Evidence / source | Building relationship |
| --- | --- | --- | --- |
| P-055 — A. J. Surber | BUS-045 | E-121; S-135, S-137 | B-005, October 1907 only; 1908 number not printed |
| P-056 — Justin & Hitchman | BUS-046 | E-122; S-136, S-137 | No numbered target building assigned |
| P-057 — Strebig | BUS-047 | E-123; S-135 | No numbered target building assigned |
| P-058 — Thomas Hartman | BUS-048 | E-123; S-137 | No numbered target building assigned |
| P-059 — S. Rosenstein | BUS-049 | E-123; S-135 | No numbered target building assigned |
| P-060 — W. Rambo | BUS-050 | E-123; S-135 | No numbered target building assigned |
| P-061 — J. Stewart & Son | BUS-051 | E-123; S-135 | No numbered target building assigned |
| P-062 — John Gohra | BUS-052 | E-123; S-135 | No numbered target building assigned |
| P-063 — D. M. Klemsen | BUS-053 | E-123; S-135 | No numbered target building assigned |
| P-064 — Knapp & Nobel | BUS-054 | E-123; S-137 | No numbered target building assigned |
| P-065 — A. H. Griessen | BUS-055 | E-123; S-135 | No numbered target building assigned |
| P-066 — Carl G. Hodes | BUS-056 | E-123; S-137 | No numbered target building assigned |
| P-067 — Astman & Knightly | BUS-057 | E-123; S-137 | No numbered target building assigned |
| P-068 — L. Buconich | BUS-058 | E-123; S-137 | No numbered target building assigned |
| P-069 — D. McHenry | BUS-059 | E-123; S-137 | No numbered target building assigned |
| P-070 — Bennett & Moore | BUS-060 | E-123; S-137 | No numbered target building assigned |
| P-071 — Gordon E. Hayes | BUS-061 | E-123; S-137 | No numbered target building assigned |
| P-072 — Straight & Salisbury | BUS-062 | E-123; S-137 | No numbered target building assigned |
| P-073 — I. Selling | BUS-064 | E-123; S-135 | No numbered target building assigned |
| P-074 — Albright | BUS-065 | E-123; S-135 | No numbered target building assigned |
| P-096 — Herman Schrader | BUS-063 — Schrader's Bakery | E-123/S-137 business-name anchor; E-093/S-102/S-106 identifies Schrader and the 1912 sale | No numbered target building assigned |

OQ-032/RL-045 track unresolved identities and premises; OQ-026 retains Schrader address limits. [Full review](../evidence/source-captures/1907-1908-surber-justin-main-visual-review.md).

Separate spelling: **P-075 / BUS-066 — Knapp & Noebel**, E-123/S-135,712 Main in 1907; P-064/BUS-054 retains 1908 Knapp & Nobel only. No identity merger.

## 1912 Schrader bakery transfer

| People | Businesses | Evidence / sources | Limits |
| --- | --- | --- | --- |
| `P-096` Herman Schrader; `P-097` Wemmo & Haas | `BUS-063` Schrader's Bakery; `BUS-080` Wemmo & Haas bakeries | `E-093`; `S-102`, `S-106`; compare `E-123`/`S-137` | Main Street bakery among two sold in December 1912; exact number, individual purchaser names, real-estate ownership and later operating span unresolved. |

## 1925 municipal report — context without numbered-building assignment

| Evidence / source | Timeline | Location and limits |
| --- | --- | --- |
| `E-139` / `S-157` | `T-044`: 30 April fire; `T-045`: 18 August flue call | Main between Fifth and Sixth ($15), and unnumbered Fifth Street respectively. No street side, numbered premises, business or proprietor identified. April event appears in `B-005`/501, `B-001`/503 and `B-002`/505 timelines as **context only**; no building relationship is asserted in YAML. Supersedes the conflated April 18 / $2,500 lead. |
| `E-140` / `S-157` | `T-046`: 1925 paving | Fifth from High to Jackson, uphill from Main. Pavement widths do not establish legal street-width change or target-building reconstruction. No numbered-building assignment. |
| `E-141` / `S-157` | No property timeline event assigned | Citywide combined franchise/license revenue and police recordkeeping. Retrieval context only; no named payer, proprietor, premises or target construction event. Full report now 22/22 PDF pages visually reviewed, not annual completion. |

Original report: `records/municipal/annual-reports/1925-municipal-activities-report.pdf`; exact visual coverage and retrieval leads in [review capture](../evidence/source-captures/1925-municipal-report-fire-correction-and-fifth-street-review-2026-09-01.md).

Follow-up finding aid: `S-158`, State Archives Clackamas County inventory, supports retrieval planning for `RL-007`, `RL-010`, `RL-024` and `RL-026`. [Series table and manual callouts](../evidence/source-captures/1925-license-inspection-and-county-records-review-2026-09-01.md). **No `E-###`, `T-###`, entity or historical occupancy/ownership relationship assigned**: original records remain unreviewed and target entries are not yet known to exist.

## 1926 municipal report — no numbered-building assignment

| Source/evidence/media | Connections | Limits |
| --- | --- | --- |
| `S-159` / `E-142` | `T-047` July 10 Sixth/Main false alarm; `T-048` September 20 Sixth/Main damage; `T-049` November 11 Fifth/Main false alarm | No number, side or occupant. `T-049` appears in 501/503/505 timelines as context only; no YAML building relationship. Paramount Restaurant's separate fire has no address and is not assigned to Kwality or 503. |
| `S-159` / `E-143` | `RL-010` license/health-record follow-ups | County-labeled health payment, restaurant-inspection statement and aggregate accounts; no named target occupant or confirmed record custody. |
| `S-159` / `IMG-0726` | PDF 4 embedded downtown aerial | Exposure date and target roof mapping unresolved; no new construction/removal event. |

[Full review and original](../evidence/source-captures/1926-municipal-report-visual-review-2026-09-01.md); 23/23 PDF pages visually verified, **1926 IN PROGRESS**.

## 1919 Gilbert Miller residence / migration corroboration

| Source / evidence | Person | Scope and limit |
| --- | --- | --- |
| `S-160` / `E-144` | `P-046` Gilbert Miller | Visually verified 11 July 1919 family residence at Ninth/Division and move-from-Springfield context. **No direct 505, Wolf & Miller partner, property, or construction relationship assigned.** |

## 1902–1904 legacy branch consolidation

| Source / evidence | Connected records | Scope / limits |
| --- | --- | --- |
| `S-161` / `E-145` | `P-096`; `BUS-063` | Schrader Main-Street Bakery background; no exact later storefront. |
| `S-163` / `E-146` | `BUS-081` | Union Store directly between Fifth/Sixth; later number unresolved. |
| `S-164` / `E-147` | `BUS-082`; `BUS-007` adjacency | Portland Clothing next to Harding; no number. |
| `S-165` / `E-148` | `BUS-083` | Fair Store opposite Post Office; move destination unresolved. |
| `S-166` / `E-149` | `P-001`; `BUS-007` | Harding Drug Store in Willamette Building; later number not backdated. |
| `S-169` | `E-061`; `RL-025` | 24 Aug 1906 Courier OCR corroboration of house-numbering ordinance; not a replacement for canonical plat evidence. |
| `S-170` / `E-150` | `P-050`; candidate `B-005` relationship | Holman move to his Fifth/Main building by 26 Feb 1914; exact 501 mapping unresolved. |

Complete old-branch files, diff and commit log are preserved in `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`.

## Palace Saloon 1909 person crosswalk

| Person / entity | Related business | Evidence / source | Limits |
| --- | --- | --- | --- |
| `P-098` Ralph O. Smith | `BUS-024` Palace Saloon | `E-152`, `S-172` | 17 Sep. 1909 applicant at Palace Saloon, corner Main/Fifth; 501, grant, title and succession unproved. |

| `P-099` Albert Knapp / A. Knapp | `BUS-024`; `E-154`, `E-155`; `S-174`, `S-175` | 1900 Palace purchaser; 1905 A. Knapp reported seller to A. J. Surber. Same-person identity is a strong inference from same-business chronology, not surname alone. |
| `P-055` A. J. Surber — Palace supplement | `BUS-024`, `BUS-045`; `E-155`, `E-121`; `S-175`, `S-135`, `S-137` | 1905 Palace purchaser; later 1907 exact-501 liquor applicant. The 1905 Palace room is not automatically equated with 501. |

| E-157 | S-177; P-098/P-100; BUS-024 | Ralph O. Smith reported purchase of former partner F. E. Hall's Palace Saloon interest, 25 Jun. 1909. |
| E-158 | S-178; P-098; BUS-024 | Smith Palace Saloon liquor-license application at Fifth/Main, same date. |
| E-159 | S-179; P-037; BUS-024; B-005 | Joseph Wilson Palace Saloon application at Fifth/Main, 20 Jun. 1911; no exact 501 in notice. |
| P-100 F. E. Hall | E-157; S-177; BUS-024 | Former Palace Saloon partner of Ralph O. Smith; full name and legal terms unresolved. |

## 1 September 2026 Fifth Street Restaurant uploaded-page integration

| Record | Connected IDs | Note |
| --- | --- | --- |
| `S-180` / `E-160` | `BUS-070` | 31 Aug. 1916 inspection: Fifth Street Restaurant score 75.3; no proprietor/number. |
| `S-181` / `E-161` / `P-101` | `BUS-070` | W. W. Pollock conducting restaurant in 1919; sanitation fine. |
| `S-182` / `E-162` | `BUS-070` | 26 Aug. 1921 incident-place evidence. |
| `S-183` / `E-163` / `P-102` / `P-103` | `BUS-070`; compare `P-036`, `P-087`, `P-088` | 21 Jul. 1922 L. E. Blakely / C. P. Gates wording; identity conflicts preserved. |

| `S-184` / `E-164` / `P-101` | `BUS-070`; `T-059` | 1 Sep. 1916 direct Pollock / Fifth Street Restaurant / 75.3 inspection listing; exact premises and continuity unresolved. |
| `S-185` / `E-165` / `P-104` | `BUS-070`; `T-060` | 19 Nov. 1920 Guy Proffit reported business interest; legal character/percentage and exact premises unresolved. |
| `S-183` / `E-163` duplicate aliases | `BUS-070` | Two steward filenames uploaded 2 Sep. 2026 are byte-identical to existing 21 Jul. 1922 source; no duplicate PDF or ID created. |

| `S-186` | identity-triage only | 2 Jul. 1914 Courier page; unrelated Miller/Wolfe names, no target partnership evidence. |
| `S-187` / `E-166` | `BUS-012`; `B-002` | 20 Sep. 1918 direct Wolf & Miller advertisement at 505 Main. |
| `S-188` / `E-167` | `BUS-012`; `B-001`, `B-002` | 31 Oct. 1918 answer page prints 503 Main, conflicting with 505 evidence; no move inferred. |

| `S-189` / `E-168` | `BUS-067`; `B-002` | 16 Aug. 1907 Young's Second Hand Store exact 505 Main advertisement; George Young individual identity not explicit. |
| `S-190` / `E-169` | `BUS-024`; `P-037` inference | 14 Mar. 1911 Joseph Wilson Palace Saloon, Fifth/Main license notice; no exact 501 or grant proof. |

## 2 September 2026 Freeze / 514 Main uploaded-page integration
- `S-191` ↔ `E-170` — 20 May 1921 *Oregon City Enterprise* p. 3, W. O. Witham retrospective purchase of A. A. Munden's furniture store at **514 Main**; compared with `S-034` 10 Oct. 1918 **A. A. Mundin, 514 Main**.
- Existing `S-035` ↔ `E-028` expanded with exact preserved Freeze pages for 8 Apr., 20 May, 28 Oct. 1921 and 30 Jun. 1922; no new IDs assigned for repeated ads in the same source/evidence family.

| `S-192` / `E-171` | `BUS-011`; `P-001`; `B-002` | 25 Dec. 1913 Chicago Store fire page; George Harding building-owner wording visually verified; exact 505 mapping remains cross-source inference. |
| `S-193` / `E-172` | `BUS-084`; `B-001` | 18 Oct. 1940 JAGERS exact 503 Main advertisement; J. Jager/New Kwality relationship unresolved. |

## 2 September 2026 — 1907–1910 Fifth/Main supplied-page additions
- `S-194` ↔ `E-173` ↔ `BUS-085` — 1 Mar. 1907 R. A. Sawyer / Charles Albright meat-business succession at Fifth/Main; later `BUS-047` Strebig old-stand clue.
- Existing `S-135` ↔ `E-121` — 4 Oct. 1907 A. J. Surber exact No. 501; supplied PDF derivative reconciled without duplicate ID.
- `S-195` ↔ `E-174` ↔ `BUS-046`, `BUS-045` — 20 Mar. 1908 separate Justin & Hitchman and Surber Fifth/Main applications.
- `S-196` ↔ `E-175` ↔ contextual `BUS-041` — 11 Feb. 1910 Andresen/Stevens 60x210 Main-to-Water property and planned brick-block report; parcel unresolved.
- `S-197` ↔ `E-176` ↔ `BUS-086` — 18 Mar. 1910 M. Justin at Mt. Hood Cafe, Fifth/Main; relationship to `BUS-046` unresolved.
- Timeline IDs: `T-065` through `T-068`. Follow-up: `RL-047`.

| `S-198` / `E-177` | `P-098`; `BUS-024`; `T-069` | 31 Dec. 1909 Ralph O. Smith six-month Palace Saloon application at Main/Fifth; no exact number or grant. |
| `S-199` / `E-178` / `P-105` | `BUS-024`; `E-080`; `T-070` | 17 Jun. 1910 E. R. Case Palace Saloon application prints **510 Main**; preserve address conflict/transition question. |
| `S-032` / `E-026` 14 Apr. 1911 supplement | `BUS-011`; `B-002` | Exact steward page now preserved; Chicago Store directly at 505 Main. |
| `S-035` / `E-028` 13 May 1921 supplement | `P-027`; `BUS-021`; `B-002`; `T-071` | Exact steward page prints 505 Main; 20 May returns to 505½; no physical-layout inference. |

## 2 September 2026 Palace / pool-hall upload reconciliation
- `S-178` / `E-158` / `P-098` / `BUS-024` — 25 Jun. 1909 Smith Palace Fifth/Main application plus newly preserved 2 Jul. repeat; no second application/grant inferred.
- `S-199` / `E-178` / `P-105` / `BUS-024` — 17 and 24 Jun. 1910 Case Palace notices both print 510 Main; repeated printed number strengthens source wording but does not resolve physical-address conflict.
- `S-172` / `E-152` — newly supplied 17 Sep. 1909 file is an exact duplicate alias of the existing repository PDF; no new ID.
- `S-150` / `E-135` — newly supplied 13 Feb. and 4 Jun. 1920 pool-hall PDFs are exact duplicate aliases of existing repository PDFs; no new IDs.
[Reconciliation record](../evidence/source-captures/1909-1920-palace-poolhall-steward-upload-reconciliation-2026-09-02.md).

## 3 September 2026 — Newton / 427 address test

| Claim | Direct record links | Boundary |
| --- | --- | --- |
| `E-179` / `S-141` / `IMG-0727` / `T-072` | `BUS-087`, `B-016` | June 8 exact 427/phone 517 ad, no proprietor. |
| `E-180` / `S-200`–`S-202` / `IMG-0729`–`IMG-0731` / `T-073` | `P-106`, `BUS-088`; contextual laundry `BUS-068` | Newton directly named; across-the-way report; exact number unresolved. |
| `E-181` / `S-141` / `IMG-0728` / `T-074` | `BUS-089` | Unnumbered Quality Cafe roster; no merger. |
| `E-182` / `S-021` / `SM-008` / `T-075` | `B-016`, `B-005`, `B-009` | 1925 map geometry and use only. |

`OQ-034` / `RL-048`: `P-106` → `B-016` is probable only, not a direct occupancy edge. No `BUS-087`/`BUS-088`/`BUS-089` identity merger and no 503 Kwality linkage. [Full capture](../evidence/source-captures/1922-george-newton-427-main-address-test-2026-09-03.md).

### CCHS P-1469 1890 flood photograph

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0732` / `S-203` / `E-183` / CCHS `P-1469` | `media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg`; `evidence/source-captures/1890-cchs-p1469-main-street-flood-photo-2026-09-03.md` | CCHS directly supplies 1890 and 6th/Main southwest scene metadata; do not infer an exact 501/503/505 facade or building continuity from the image alone. |

### CCHS P-1456 1890 flood photograph

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0733` / `S-204` / `E-184` / CCHS `P-1456` | `media/photos/early-main-street/IMG-0733_1890-flood-6th-main-looking-south-cchs-p1456.jpg`; `evidence/source-captures/1890-cchs-p1456-main-street-looking-south-photo-2026-09-03.md` | CCHS directly supplies the 1890, post-recession, Main-looking-south, alley-to-Sixth metadata and duplicate group P-1456/P-1616/P-5519/P-8885. Supplied and committed JPEGs are substantive duplicates, not byte-identical. No exact 501/503/505 facade or building continuity is inferred. |


### CCHS 2008.008.002.309 — 1888 Main Street alley/barber photograph

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0734` / `S-205` / `E-185` / CCHS `2008.008.002.309` | `media/photos/early-main-street/IMG-0734_1888-main-street-alley-4th-5th-barber-cchs-2008-008-002-309.jpg`; `evidence/source-captures/1888-cchs-2008-008-002-309-main-street-alley-barber-photo-2026-09-03.md` | 1888 Main Street at/near alley between 4th and 5th; visible barber lettering is direct. Exact modern address/side and any 501/503/505 relationship remain unresolved; follow `RL-049` / `OQ-035`. |

### CCHS 2019.001.00179 — Downtown Oregon City historic overview

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0735` / `S-206` / `E-186` / CCHS `2019.001.00179` | `media/photos/early-main-street/IMG-0735_undated-downtown-oregon-city-4th-6th-overview-cchs-2019-001-00179.jpg`; `evidence/source-captures/undated-cchs-2019-001-00179-downtown-overview-4th-6th-photo-2026-09-03.md` | CCHS identity/title/description direct; steward filename supplies 4th–6th/aerial-view context; exposure date, camera platform/position and exact building/address mapping remain unresolved under `RL-050` / `OQ-036`. |

### CCHS U-1426.005098a — Post Office demolition at Fifth/Main

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0736` / `S-207` / `E-187` / CCHS `U-1426.005098a` | `media/photos/early-main-street/IMG-0736_undated-post-office-demolition-5th-main-cchs-u1426-005098a.jpg`; `evidence/source-captures/undated-cchs-u1426-005098a-post-office-demolition-5th-main-photo-2026-09-03.md` | Exact supplied/CCHS JPEG. Post Office is southeast Fifth/Main, same east side as 501/503/505 but across Fifth from 501; 1933 is construction year, demolition date unresolved. |

### CCHS P-9379 — Aerial Photograph Oregon City

| Media/source/evidence | Repository record | Boundary |
| --- | --- | --- |
| `IMG-0737` / `S-208` / `E-188` / CCHS `P-9379` / accession `2022.012.001` | `media/photos/aerials/IMG-0737_undated-oregon-city-aerial-cchs-p9379.jpg`; `evidence/source-captures/undated-cchs-p9379-aerial-oregon-city-photo-2026-09-03.md` | CCHS identity/title/description and broad aerial scene are direct. The public record supplies no exposure date; accession `2022.012.001` is not a date. Exact camera details and 501/503/505 building mapping remain unresolved. |

## S-209 / E-189 / IMG-0738 — CCHS MOT:P-502 G. H. Young Store

- Source: `S-209` — CCHS public catalog / steward-supplied photograph, external object `MOT:P-502`.
- Evidence: `E-189` — cataloged **507 Main / 1916** with explicit W. W. Bradley conflict.
- Media: `IMG-0738` — `media/photos/early-main-street/IMG-0738_1916-g-h-young-store-507-main-cchs-p502.jpg`.
- Related entities: `P-076`, `BUS-067`, `B-003`; conflict context `P-041` / `BUS-026`.
- Review: `evidence/source-captures/1916-cchs-p502-gh-young-store-507-main-photo-2026-09-03.md`.

## S-210 / E-190 / IMG-0739 — CCHS MOT:P-370 Young's Curio Store

- Source: `S-210` — CCHS MOT:P-370 and visually verified steward photograph.
- Evidence: `E-190` — visible Young's Curio Store signage, cataloged 507 Main, with 1907/1916 duplicate-date conflict.
- Media: `IMG-0739` — `media/photos/early-main-street/IMG-0739_1907-1916-date-conflict-young-curio-store-507-main-cchs-p370.jpg`.
- Related: `P-076`, `BUS-067`, `B-003`; 1916 conflict context `P-041` / `BUS-026`.
- Research lead: `RL-051` — retrieve and reconcile duplicate MOT:P-6253.
- Review: `evidence/source-captures/1907-1916-cchs-p370-young-curio-store-507-main-date-conflict-2026-09-04.md`.

## S-211 / E-191 / IMG-0740 — CCHS MOT:P-498 Harding Drug Store

- Source: `S-211` — CCHS MOT:P-498 catalog record.
- Evidence: `E-191` — circa-1885 catalog/address and direct full-frame visual content, with retrospective-address caution.
- Media: `IMG-0740` — full Harding storefront frame.
- Related entities: `BUS-007` Harding Drug Store; `P-001` George A. Harding; `B-002` 505 Main; context `BUS-067` / `P-076` George Young.
- Related prior image record: `S-148` / `E-133` / `IMG-0724` (apparent same exposure, 400 × 400 crop, distinct CCHS object and 1880/1880s metadata).
- Review: `evidence/source-captures/circa-1885-cchs-p498-harding-drug-store-505-main-photo-2026-09-04.md`.

## S-212 / E-192 / IMG-0741 — CCHS 2008.008.049.056 Bank of Commerce interior

- Source: `S-212` — exact CCHS catalog-number record for **Interior of the Oregon City Bank of Commerce**.
- Evidence: `E-192` — cataloged **1890 / 512 Main** and direct interior-image content, with attribution limits.
- Media: `IMG-0741` — `media/photos/early-main-street/IMG-0741_1890-oregon-city-bank-of-commerce-interior-512-main-cchs-2008-008-049-056.jpg`.
- Other institutional identifiers: **Lynch-Criteser 056**; **Freytag Collection #1**.
- Limits: **“(1st National)”** and **“Latourette and Myers ?”** remain catalog/uncertain wording; no modern-building, ownership, person-identity, or 503/505 continuity is asserted.
- Review: `evidence/source-captures/1890-cchs-2008-008-049-056-bank-of-commerce-interior-512-main-2026-09-04.md`.

## S-213 / E-193 / IMG-0742 / T-076 — CCHS 1895 lower-Main bluff photograph

- Source: `S-213` — CCHS `2008.008.003.125`.
- Evidence: `E-193` — direct 1895 streetscape; probable/working-hypothesis target-frontage roofline assignment.
- Media: `IMG-0742` — full public CCHS derivative.
- Timeline: `T-076` — 1895 photograph context.
- Related buildings: `B-005` 501, `B-001` 503, `B-002` 505 (later-address mapping only).
- Related map context: `SM-005` / `S-018` / `E-020`.
- Limit: no pre-1906 numbered-address, one-building, occupancy, ownership or continuity inference.
- Review: `evidence/source-captures/1895-cchs-2008-008-003-125-lower-main-third-stairs-target-frontage-2026-09-04.md`.

## S-214 / E-194 / IMG-0743 / T-077 — CCHS 1890–1899 Main Street photograph

- Source: `S-214` — CCHS `2008.008.003.104`.
- Evidence: `E-194` — direct Main Street/date-range streetscape; probable Sixth-to-Fifth viewpoint and later-address mapping.
- Media: `IMG-0743` — full public CCHS derivative.
- Timeline: `T-077` — 1890–1899 photograph context.
- Related buildings: `B-005` 501, `B-001` 503, `B-002` 505 (later-address spatial context only).
- Related fixed-location photo: `S-204` / `E-184` / `IMG-0733`.
- Related map context: `SM-005` / `S-018`; `SM-006` / `S-019`; `E-020`.
- Limit: no pre-1906 numbered-address, exact exposure-year, storefront-boundary, occupancy, ownership or continuity inference.
- Review: `evidence/source-captures/1890-1899-cchs-2008-008-003-104-main-street-sixth-fifth-context-2026-09-04.md`.

## S-215 / E-195 / IMG-0744 / T-078 — CCHS 1895 Welcome Arch at Sixth/Main
- Source: `S-215` — CCHS `2008.008.046.040`, **Oregon City "Welcome Arch"**, 6th and Main, 1895.
- Evidence: `E-195` — fixed Sixth/Main streetscape with steward-identified later 501/503/505 predecessor frontage in right-hand background.
- Media: `IMG-0744` — `media/photos/early-main-street/IMG-0744_1895-oregon-city-welcome-arch-6th-main-cchs-2008-008-046-040.jpg`.
- Timeline: `T-078` — 1895 fixed-location target-block photo context.
- Related buildings: `B-005` / `B-001` / `B-002`; comparisons `S-204` / `E-184`, `S-214` / `E-194`; map `SM-005` / `S-018` / `E-020`.
- Limit: later street numbers are not visible or backdated; exact individual storefront boundaries and structural continuity remain unresolved.
- Review: `evidence/source-captures/1895-cchs-2008-008-046-040-welcome-arch-6th-main-target-frontage-2026-09-04.md`.

- Signage re-review: `IMG-0744` directly shows **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** and a separate sign containing **FASHION**; later 501/503/505 storefront assignment remains unresolved. The `(1)` steward re-upload is an exact byte duplicate and does not create a new ID.
## S-216 / E-196 / IMG-0745 / T-079 — CCHS 1960 Promenade at Fifth Street downtown view
- Source: `S-216` — CCHS `2008.008.003.257`, **Oregon City (view from the Promenade at 5th St.)**, 1960.
- Evidence: `E-196` — dated elevated downtown context; exact 501/503/505 building assignment unresolved.
- Media: `IMG-0745` — `media/photos/early-main-street/IMG-0745_1960-oregon-city-promenade-5th-street-cchs-2008-008-003-257.jpg`.
- Timeline: `T-079` — 1960 downtown view.
- Review: `evidence/source-captures/1960-cchs-2008-008-003-257-promenade-5th-view-2026-09-04.md`.

## S-217 / E-197 / IMG-0746 / T-080 — CCHS P-1317 Fifth Street bluff view
- Source: `S-217` — CCHS `P-1317`, **Oregon City - View from Bluff**, description fixes Bluff at Fifth Street.
- Evidence: `E-197` — project-steward probable identification of the branch-obscured predecessor 501/503/505 frontage; individual later-address mapping and exposure date unresolved.
- Media: `IMG-0746` — `media/photos/early-main-street/IMG-0746_undated-oregon-city-view-from-bluff-5th-street-cchs-p1317.jpg`.
- Timeline: `T-080` — undated bluff-view context.
- Review: `evidence/source-captures/undated-cchs-p1317-oregon-city-view-from-bluff-5th-street-target-frontage-2026-09-04.md`.

## CCHS P-6974 — 1908 510–512 7th Street photograph

- Source/evidence/media: `S-219` / `E-199` / `IMG-0748`.
- Businesses: `BUS-090` Friedrich's Hardware; `BUS-091` Little's Confectionery.
- Cataloged people: `P-392` Richard Friedrichs; `P-393` Walter Little (1908 confectionery identification).
- Identity guardrail: `P-393` is **not merged** with `P-090` Walter L. Little; same-person question remains unresolved.
- Catalog identifiers: `P-6974`; `2008.008.001.320`; Society 320; Society Photo #320; Ferguson Collection #18.
- Review: `evidence/source-captures/1908-cchs-p6974-friedrich-little-510-512-7th-2026-09-04.md`.

| `IMG-0749` CCHS `P-4565` | `S-220`, `E-200`, `T-081`, `BUS-004`, `BUS-005`, `BUS-007`, `BUS-023`, `BUS-092`, `BUS-093`, `BUS-094`, `B-001`, `B-002`, `B-003` | Circa-mid-1960s pre-fire Main Street business lineup; directly shows TAVERN/505 and multiple neighboring signs; visible 5th/Main blades conflict with catalog Main/McLoughlin wording. |

| `IMG-0750` CCHS `P-1293` | `S-229`, `E-203`, `T-082`, `B-001`, `B-002`, `B-005`, `E-011`, `E-021`, `E-101`, `E-102` | CCHS-cataloged 1975 aerial; 505 visibly deeper rearward than 503; 501 absent; supplied title says 1981, catalog metadata says 1975. |

| `IMG-0751` CCHS `P-4564` | `S-230`, `E-204`, `T-083`, `BUS-095`, `BUS-096`, `BUS-004`, `B-001` | Circa-mid-1960s Mobil/Hagen opposite-corner scene. Mobil and Hagen signage direct; project steward places camera at/near The Wheel/503 looking southeast. `BUS-004` / `B-001` are camera-position context only; 503/505 facades are not depicted. |

| `IMG-0752` CCHS `P-4563` | `S-231`, `E-205`, `T-084`, `BUS-097`, `BUS-098` | Circa-mid-1960s northeast 5th/Main neighboring-corner scene; American Cleaners and Outdoor Store documented; target 503/505 facades not shown. |

| `IMG-0753` CCHS `P-1311` | `S-232`, `E-206`, `T-085`, `BUS-004`, `B-001`, `BUS-005`, `B-002` | 1955–1965 bluff-at-4th view; enlarged review supports The Wheel on 503 and 505 Tavern signage on adjacent 505; exact exposure year unresolved. |

| `IMG-0754` / `S-233` / `E-207` / CCHS `P-4562` | `media/photos/main-street/IMG-0754_circa-mid-1960s-us-post-office-rear-5th-main-cchs-p4562.jpg`; `evidence/source-captures/cchs-p4562-mid-1960s-post-office-rear-5th-main-2026-09-05.md` | Supplied CCHS metadata identifies intact U.S. Post Office rear view at Fifth/Main, related `U-1426.005109d`; cross-check `E-102` and demolition image `S-207` / `E-187` / `IMG-0736`. “Circa mid-1960s?” remains tentative. |

## S-234 / E-208 / IMG-0755 — CCHS 2008.008.049.057 Bank of Commerce exterior

| Record | Links | Notes |
| --- | --- | --- |
| `S-234` / `E-208` / `IMG-0755` | `S-212` / `E-192` / `IMG-0741` related interior | 1891 exterior: **COMMERCIAL BANK** directly visible; CCHS catalogs 512 Main. Later demolition/renumbering, stone-remnant, and moved-rooming-house history retained as attributed catalog annotation. |

| `IMG-0756` / `S-235` / `E-209` / CCHS `2008.008.002.425` | `media/photos/aerials/IMG-0756_1947-oregon-city-aerial-cchs-2008-008-002-425.jpg`; `evidence/source-captures/cchs-2008-008-002-425-1947-oregon-city-aerial-2026-09-05.md` | CCHS catalogs the high-oblique Oregon City aerial as **1947**; independent chronological control between `IMG-0009` and `IMG-0010`. Exact 501/503/505 roof mapping remains unresolved pending fixed-landmark alignment. |

## S-236 / E-210 / IMG-0757 / T-087 — CCHS P-1128, 1936 Fifth/Main bluff view

| Record | Links | Notes |
| --- | --- | --- |
| `S-236` / `E-210` / `IMG-0757` / `T-087` | `B-002`; `BUS-013`; `S-036` / `E-033` | Exact 1936 CCHS photograph. Steward maps target storefront to 505; probable **FARR'S** sign and likely pool wording combine with independent City business/address evidence to strongly support Farr's Pool Hall at 505 in 1936. Exact full sign text/opening date remain unresolved. |

## S-237 / E-211 / IMG-0758 / T-088 — CCHS P-1043, 1930s Sixth-to-Fifth Main Street view

| Record | Links | Notes |
| --- | --- | --- |
| `S-237` / `E-211` / `IMG-0758` / `T-088` | `B-001`, `B-002`, `B-003`; cross-check `S-236` / `E-210` / `IMG-0757` | 1930–1939 streetscape from Sixth toward Fifth; direct business-sign roster. 503/505 exact signage unresolved in this frame; use as spatial/address-sequence control. |

| `IMG-0759` / `S-238` / `E-212` / CCHS `P-1032` | `media/photos/main-street/IMG-0759_1936-1939-oregon-city-from-bluff-highway99e-cchs-p1032.jpg`; `evidence/source-captures/cchs-p1032-1936-1939-oregon-city-from-bluff-highway99e-2026-09-05.md` | CCHS 1936–1939 bluff view. Direct broad transportation/commercial context; 503/505 sign text remains unresolved at current image scale and is not treated as negative occupancy evidence. |
