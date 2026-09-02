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
| `B-005` 501 Main Street (historic / removed) | `BUS-045` A. J. Surber; `BUS-024` Palace Saloon; `BUS-025` Hunsaker & Taylor; 1925 store occupant unknown | Unified chronology: `timelines/501-main.md`. `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`. The records do not prove a transfer or uninterrupted continuity. |
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
