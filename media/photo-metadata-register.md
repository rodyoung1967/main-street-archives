# Photo and Metadata Register

This register records image and photo-metadata items that have been discussed or uploaded for the Main Street project.

## Media File Status Rule

- `committed` means the actual image file is present in the repository.
- `pending-upload` means the archive has metadata and an expected path, but the actual image file still needs to be uploaded.
- `external` means the file intentionally remains outside the repository.
- `Time Capsule Maps metadata` is a trusted internal project source because Rodney Young is Time Capsule Maps, but original photo/source details should still be captured when making external historical claims.

Repository audit, 31 August 2026: **69 raster files are committed and all 69 are recorded here by exact repository path.** Forty-two are photographs/aerials under `media/photos/`; the other 27 are source-document images kept with their newspapers, records, maps, or artifacts. No byte-identical raster duplicates were found. All three recent steward-supplied historical JPEGs are exact byte matches to `IMG-0723`–`IMG-0725`. See the [definitive photograph inventory](photos/inventory.md).

## IMG-0001 — New Kwality Cafe Matchbook

- Artifact ID: `A-001`
- Type: Matchbook / primary artifact image
- Related building: 503 Main Street
- Related business: New Kwality Cafe
- Evidence: `E-002`
- Source: `S-002`
- Repository file: `artifacts/images/A-001-new-kwality-cafe-matchbook.jpg`
- Status: `committed`
- Verification note: Actual JPEG file is committed at the repository path above.
- Notes: Places New Kwality Cafe at 503 Main St. and identifies J. Jager as proprietor.

## IMG-0002 — Larry's Kwality Cafe Matchcover

- Artifact ID: `A-002`
- Type: Matchcover / primary artifact image
- Related building: 503 Main Street
- Related business: Larry's Kwality Cafe
- Evidence: `E-003`
- Source: `S-003`
- Repository file: `artifacts/images/A-002-larrys-kwality-cafe-matchcover.jpg`
- Status: `committed`
- Verification note: Actual JPEG file is committed at the repository path above.
- Notes: Places Larry's Kwality Cafe at 503 Main Street, Oregon City, with telephone 6106.

## IMG-0003 — Thebeerchaser 505 Tavern Comment Screenshot

- Type: Screenshot / public web-comment evidence
- Related building: 505 Main Street
- Related business: 505 Tavern
- Evidence: `E-013`
- Source: `S-009`
- Expected repo path: `media/screenshots/thebeerchaser-505-tavern-comment-2021.png`
- Status: `pending-upload`
- Notes: Captures local-memory material about 505 Tavern, Publishers Paper workers, and a 1971 draft-number celebration.

## IMG-0004 — The Wheel at 503 / 505 Tavern Adjacent Photo Metadata

- Type: Time Capsule Maps photo metadata
- Related buildings: 503 Main Street and 505 Main Street
- Evidence: `E-015`
- Source: `S-010`
- Expected repo path if imported: `media/photos/503-main/the-wheel-503-main-505-tavern-adjacent.webp`
- Status: `external` / Time Capsule Maps metadata; no steward-supplied original binary is currently present. If one is supplied later, preserve it under the project photo-ingest rule unless it duplicates an existing file or an exclusion is documented.
- Title / label: "The Wheel: 503 Main St, Oregon City, OR"
- Location note: The metadata places The Wheel at 503 Main Street and states that 505 Tavern is to the right at 505 Main Street.
- Confidence: Trusted internal Time Capsule Maps metadata for what was entered and maintained there; original image source/date should still be recorded when available.

## IMG-0005 — 5th / McLoughlin / US99E / Main Street, circa 1910 Metadata

- Type: Time Capsule Maps photo metadata
- Related buildings: 503 Main Street, 505 Main Street, 507 Main Street
- Evidence: `E-015`, `E-017`
- Source: `S-010`
- Expected repo path if imported: `media/photos/main-street-block/5th-mcloughlin-us99e-main-street-oregon-city-circa-1910.webp`
- Status: `external` / Time Capsule Maps metadata; no steward-supplied original binary is currently present. If one is supplied later, preserve it under the project photo-ingest rule unless it duplicates an existing file or an exclusion is documented.
- Date: Approximate, labelled 1910 in the filename/metadata.
- Location: 5th Street / McLoughlin Boulevard / US99E and Main Street, Oregon City.
- Key metadata claims:
  - The first building in the picture is gone and is now 503 and 505 Main Street.
  - The 1925 Sanborn map shows a different building labelled 501, 503, and 505 Main Street.
  - It is unclear what was ever at 501 Main.
  - 503 Main Street underwent significant modification around 2017.
  - The taller Harding Building at 507 burned and was replaced by the current building.
- Confidence: Trusted internal Time Capsule Maps metadata for what was entered and maintained there; original source/date should still be recorded when available.

## IMG-0006–IMG-0043 — Oregon City Aerial Photocompare Series (5th & Main)

- Type: Aerial photograph screenshots
- Related buildings: 503, 505, and 507 Main Street (`B-001`, `B-002`, `B-003`)
- Evidence: `E-021`
- Source: `S-023`
- Status: `committed` (all 38 JPEG files present in repository)
- Analysis: `evidence/aerial-5th-main-photocompare-series.md`
- File index: `media/photos/aerials/README.md`
- Notes: Screenshots from Oregon City photocompare viewer, one frame per year 1929–2025. Key finding: 501 Main visible as separate roof in 1936 (`IMG-0007`); absent by 1944 (`IMG-0009`) — removal window 1936–1944 (`D-003`, `E-021`).

| Media ID | Year | Repository file |
| --- | --- | --- |
| IMG-0006 | 1929 | `media/photos/aerials/IMG-0006_aerial_5th-main_1929.jpg` |
| IMG-0007 | 1936 | `media/photos/aerials/IMG-0007_aerial_5th-main_1936.jpg` |
| IMG-0008 | 1940 | `media/photos/aerials/IMG-0008_aerial_5th-main_1940.jpg` |
| IMG-0009 | 1944 | `media/photos/aerials/IMG-0009_aerial_5th-main_1944.jpg` |
| IMG-0010 | 1955 | `media/photos/aerials/IMG-0010_aerial_5th-main_1955.jpg` |
| IMG-0011 | 1961 | `media/photos/aerials/IMG-0011_aerial_5th-main_1961.jpg` |
| IMG-0012 | 1974 | `media/photos/aerials/IMG-0012_aerial_5th-main_1974.jpg` |
| IMG-0013 | 1977 | `media/photos/aerials/IMG-0013_aerial_5th-main_1977.jpg` |
| IMG-0014 | 1980 | `media/photos/aerials/IMG-0014_aerial_5th-main_1980.jpg` |
| IMG-0015 | 1996 (Flood) | `media/photos/aerials/IMG-0015_aerial_5th-main_1996-flood.jpg` |
| IMG-0016 | 1999 | `media/photos/aerials/IMG-0016_aerial_5th-main_1999.jpg` |
| IMG-0017 | 2000 | `media/photos/aerials/IMG-0017_aerial_5th-main_2000.jpg` |
| IMG-0018 | 2001 | `media/photos/aerials/IMG-0018_aerial_5th-main_2001.jpg` |
| IMG-0019 | 2002 | `media/photos/aerials/IMG-0019_aerial_5th-main_2002.jpg` |
| IMG-0020 | 2003 | `media/photos/aerials/IMG-0020_aerial_5th-main_2003.jpg` |
| IMG-0021 | 2004 | `media/photos/aerials/IMG-0021_aerial_5th-main_2004.jpg` |
| IMG-0022 | 2005 (Leaf Off) | `media/photos/aerials/IMG-0022_aerial_5th-main_2005-leaf-off.jpg` |
| IMG-0023 | 2006 | `media/photos/aerials/IMG-0023_aerial_5th-main_2006.jpg` |
| IMG-0024 | 2007 | `media/photos/aerials/IMG-0024_aerial_5th-main_2007.jpg` |
| IMG-0025 | 2008 | `media/photos/aerials/IMG-0025_aerial_5th-main_2008.jpg` |
| IMG-0026 | 2009 | `media/photos/aerials/IMG-0026_aerial_5th-main_2009.jpg` |
| IMG-0027 | 2010 | `media/photos/aerials/IMG-0027_aerial_5th-main_2010.jpg` |
| IMG-0028 | 2011 | `media/photos/aerials/IMG-0028_aerial_5th-main_2011.jpg` |
| IMG-0029 | 2012 | `media/photos/aerials/IMG-0029_aerial_5th-main_2012.jpg` |
| IMG-0030 | 2012 (Leaf Off) | `media/photos/aerials/IMG-0030_aerial_5th-main_2012-leaf-off.jpg` |
| IMG-0031 | 2013 | `media/photos/aerials/IMG-0031_aerial_5th-main_2013.jpg` |
| IMG-0032 | 2014 | `media/photos/aerials/IMG-0032_aerial_5th-main_2014.jpg` |
| IMG-0033 | 2015 | `media/photos/aerials/IMG-0033_aerial_5th-main_2015.jpg` |
| IMG-0034 | 2016 | `media/photos/aerials/IMG-0034_aerial_5th-main_2016.jpg` |
| IMG-0035 | 2017 | `media/photos/aerials/IMG-0035_aerial_5th-main_2017.jpg` |
| IMG-0036 | 2018 | `media/photos/aerials/IMG-0036_aerial_5th-main_2018.jpg` |
| IMG-0037 | 2019 | `media/photos/aerials/IMG-0037_aerial_5th-main_2019.jpg` |
| IMG-0038 | 2020 | `media/photos/aerials/IMG-0038_aerial_5th-main_2020.jpg` |
| IMG-0039 | 2021 | `media/photos/aerials/IMG-0039_aerial_5th-main_2021.jpg` |
| IMG-0040 | 2022 | `media/photos/aerials/IMG-0040_aerial_5th-main_2022.jpg` |
| IMG-0041 | 2023 | `media/photos/aerials/IMG-0041_aerial_5th-main_2023.jpg` |
| IMG-0042 | 2024 | `media/photos/aerials/IMG-0042_aerial_5th-main_2024.jpg` |
| IMG-0043 | 2025 | `media/photos/aerials/IMG-0043_aerial_5th-main_2025.jpg` |

## IMG-0044 — Oregonian, 25 August 1908: Brightbill at 503 Main

- Type: Newspaper clipping / screenshot
- Original filename: `503 Main st Missing Girl 1908 Oregonian.png`
- Repository file: `newspapers/oregonian/1908-503-main-missing-girl-oregonian.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street
- Related people: `P-034` Henry Brightbill
- Evidence: `E-042`
- Source: `S-049`
- Notes: Article "Pretty Girl Is Missing" places merchant Henry Brightbill's store at 503 Main Street, Oregon City. Occupancy of the **address** in 1908; not proof the surviving building is that early.

## IMG-0045 — Oregonian, 12 June 1937: Kwality Cafe for sale

- Type: Newspaper classified / screenshot
- Original filename: `Kwality Cafe for sale 1937 Oregonian.png`
- Repository file: `newspapers/oregonian/1937-kwality-cafe-for-sale-oregonian.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street (by archive association; ad says Oregon City, not the street number)
- Related business: `BUS-001` Kwality Cafe
- Evidence: `E-043`
- Source: `S-050`
- Notes: "KWALITY cafe for sale, Oregon City. Manager retiring. Modern." Street number not in the visible ad.

## IMG-0046 — Oregonian, 30 November 1960: Wheel Cafe at 5th and Main

- Type: Newspaper clipping / screenshot
- Original filename: `Wheel Cafe 1960 Oregonian.png`
- Repository file: `newspapers/oregonian/1960-wheel-cafe-oregonian.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street (intersection; street number not in this article)
- Related business: `BUS-004` The Wheel / Wheel Cafe
- Evidence: `E-044`
- Source: `S-051`
- Notes: Places "the Wheel Cafe, 5th and Main Streets in Oregon City" as of late November 1960. Crime-story context; keep as location/date evidence, not a business-history narrative.

## IMG-0047 — Oregonian, 2 September 1967: Main Street fire; Wheel and 505 spared

- Type: Newspaper clipping / screenshot
- Original filename: `Wheel & 505 Fire September 1967.png`
- Repository file: `newspapers/oregonian/1967-09-wheel-505-fire-oregonian.png`
- Status: `committed`
- Related buildings: `B-001`, `B-002`, `B-003`
- Related businesses: `BUS-004`, `BUS-005`, `BUS-007`, `BUS-023`
- Evidence: `E-045`
- Source: `S-052`
- Notes: Friday-night fire on Main between 5th and 6th. Harding Drug Store and Dixon's Bakery among buildings gutted. Wheel Restaurant and 505 Tavern spared with smoke and water damage. Origin reported as Howard Cohn furniture warehouse. Supersedes the late-1968/1969 fire-date working claim in `E-016` for date; keep `E-016` as earlier notes.

## IMG-0048 — Oregonian, 8 February 1976: 505 Tavern classified

- Type: Newspaper classified / screenshot
- Original filename: `505 Classified 1976 Oregonian.png`
- Repository file: `newspapers/oregonian/1976-505-main-classified-oregonian.png`
- Status: `committed`
- Related building: `B-002` / 505 Main Street
- Related business: `BUS-005` 505 Tavern
- Evidence: `E-046`
- Source: `S-053`
- Notes: Pool-table classified: "505 Tavern, Oregon City, 655-4321." Documents the 505 Tavern trade name in 1976.

## IMG-0049 — Oregonian, 18 April 1983: Wheel Cafe (crop)

- Type: Newspaper clipping / screenshot
- Original filename: `Wheel 1983 Oregonian.png`
- Repository file: `newspapers/oregonian/1983-the-wheel-oregonian.png`
- Status: `committed`
- Related building: `B-001`
- Related business: `BUS-004`
- Evidence: `E-047`
- Source: `S-054`
- Notes: Same article as `IMG-0050`. Feature on Sid and Earl Cruzan; daily lunch at the Wheel Cafe in Oregon City. No street number in the visible text.

## IMG-0050 — Oregonian, 18 April 1983: Wheel Cafe (fuller page)

- Type: Newspaper clipping / screenshot
- Original filename: `Wheel Cafe 1983 Oregonian.png`
- Repository file: `newspapers/oregonian/1983-wheel-cafe-oregonian.png`
- Status: `committed`
- Related building: `B-001`
- Related business: `BUS-004`
- Evidence: `E-047`
- Source: `S-058`
- Notes: Fuller capture of the same 18 April 1983 Cruzan feature as `IMG-0049`. Photo caption: daily walks "to the Wheel Cafe to have lunch."

## IMG-0051 — Oregonian, 25 April 1985: Wheel Cafe lottery-outlet list

- Type: Newspaper clipping / screenshot
- Original filename: `Wheel 1985 Oregonian.png`
- Repository file: `newspapers/oregonian/1985-the-wheel-oregonian.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street
- Related business: `BUS-004`
- Evidence: `E-048`
- Source: `S-055`
- Notes: Clackamas lottery-ticket outlets list: "The Wheel Cafe, 503 Main St."

## IMG-0052 — Oregonian, 21 August 1985: Wiitanen / Wheel Cafe lottery sign

- Type: Newspaper clipping / screenshot
- Original filename: `The Wheel August 1985.png`
- Repository file: `newspapers/oregonian/1985-08-the-wheel-oregonian-2.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street
- Related business: `BUS-004`
- Related people: `P-007` Richard M. Wiitanen
- Evidence: `E-049`
- Source: `S-056`
- Notes: "Losses turn to profit." Richard M. Wiitanen identified as owner of The Wheel Cafe, 503 Main St. Lottery-ticket sign story.

## IMG-0053 — Oregonian, 27 August 1985: Wiitanen / Wheel Cafe lottery win

- Type: Newspaper clipping / screenshot
- Original filename: `The Wheel Aug 1985 Oregonian.png`
- Repository file: `newspapers/oregonian/1985-08-the-wheel-oregonian.png`
- Status: `committed`
- Related building: `B-001` / 503 Main Street
- Related business: `BUS-004`
- Related people: `P-007` Richard M. Wiitanen
- Evidence: `E-049`
- Source: `S-057`
- Notes: Follow-up: Oregon City man wins $100 at The Wheel Cafe, 503 Main St.; Richard M. Wiitanen named as restaurant owner.

## Media Import To-Do

- Upload Thebeerchaser screenshot to `media/screenshots/thebeerchaser-505-tavern-comment-2021.png`, if rights/usage are acceptable.
- Optionally import Time Capsule Maps webp images into `media/photos/` for preservation, while keeping original URLs/source metadata.
- Preserve original filenames, uploaded filenames, source URLs, and photographer/collection names.
- Add per-image YAML or JSON sidecar metadata if the project later needs machine-readable import/export.

## Courier batch media — S-120 / E-107, reviewed27 August2026

Task 1 recheck: `IMG-0058` (5 August p1) names Al Price and reports a **Friday**-night incident, correcting the batch's earlier Thursday reading. `IMG-0060` (p3) gives Price Bros. at **527** and Theroux at **519**, alongside the 507/509/511 ladder. These support `BUS-028` / `P-043` / `B-004` and `BUS-029` / `P-044` as qualified in the integration audit. Original source files, media IDs and manifest hashes are unchanged; diagnostic crops are not new source assets.

Each ID below represents one original PDF scan, not a separately asserted printed page. Canonical source URLs, hashes, endpoint filenames, printed-page readings and date qualifications are in `newspapers/oregon-city-courier/1915-sheets-073-100/manifest.json`. Source collection: Historic Oregon Newspapers / University of Oregon; publication: Oregon City Courier. All supplied images visually inspected. No user-uploaded filename. October14 seq4 and September2 seq6 exceptions remain explicit in the manifest and detailed capture.

| Media ID | Repository file | Issue association / sequence |
| --- | --- | --- |
| IMG-0054 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-07-29-seq-05.pdf` | 1915-07-29 / 5 |
| IMG-0055 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-07-29-seq-06.pdf` | 1915-07-29 / 6 |
| IMG-0056 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-07-29-seq-07.pdf` | 1915-07-29 / 7 |
| IMG-0057 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-07-29-seq-08.pdf` | 1915-07-29 / 8 |
| IMG-0058 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-01.pdf` | 1915-08-05 / 1 |
| IMG-0059 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-02.pdf` | 1915-08-05 / 2 |
| IMG-0060 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-03.pdf` | 1915-08-05 / 3 |
| IMG-0061 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-04.pdf` | 1915-08-05 / 4 |
| IMG-0062 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-05.pdf` | 1915-08-05 / 5 |
| IMG-0063 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-06.pdf` | 1915-08-05 / 6 |
| IMG-0064 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-07.pdf` | 1915-08-05 / 7 |
| IMG-0065 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-08.pdf` | 1915-08-05 / 8 |
| IMG-0066 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-01.pdf` | 1915-08-12 / 1 |
| IMG-0067 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-02.pdf` | 1915-08-12 / 2 |
| IMG-0068 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-03.pdf` | 1915-08-12 / 3 |
| IMG-0069 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-04.pdf` | 1915-08-12 / 4 |
| IMG-0070 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-05.pdf` | 1915-08-12 / 5 |
| IMG-0071 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-06.pdf` | 1915-08-12 / 6 |
| IMG-0072 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-07.pdf` | 1915-08-12 / 7 |
| IMG-0073 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-12-seq-08.pdf` | 1915-08-12 / 8 |
| IMG-0074 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-01.pdf` | 1915-08-19 / 1 |
| IMG-0075 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-02.pdf` | 1915-08-19 / 2 |
| IMG-0076 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-03.pdf` | 1915-08-19 / 3 |
| IMG-0077 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-04.pdf` | 1915-08-19 / 4 |
| IMG-0078 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-05.pdf` | 1915-08-19 / 5 |
| IMG-0079 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-06.pdf` | 1915-08-19 / 6 |
| IMG-0080 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-07.pdf` | 1915-08-19 / 7 |
| IMG-0081 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-19-seq-08.pdf` | 1915-08-19 / 8 |
| IMG-0082 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-01.pdf` | 1915-08-26 / 1 |
| IMG-0083 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-02.pdf` | 1915-08-26 / 2 |
| IMG-0084 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-03.pdf` | 1915-08-26 / 3 |
| IMG-0085 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-04.pdf` | 1915-08-26 / 4 |
| IMG-0086 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-05.pdf` | 1915-08-26 / 5 |
| IMG-0087 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-06.pdf` | 1915-08-26 / 6 |
| IMG-0088 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-07.pdf` | 1915-08-26 / 7 |
| IMG-0089 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-26-seq-08.pdf` | 1915-08-26 / 8 |
| IMG-0090 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-01.pdf` | 1915-09-02 / 1 |
| IMG-0091 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-02.pdf` | 1915-09-02 / 2 |
| IMG-0092 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-03.pdf` | 1915-09-02 / 3 |
| IMG-0093 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-04.pdf` | 1915-09-02 / 4 |
| IMG-0094 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-05.pdf` | 1915-09-02 / 5 |
| IMG-0095 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-06.pdf` | 1915-09-02 / 6 |
| IMG-0096 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-07.pdf` | 1915-09-02 / 7 |
| IMG-0097 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-08.pdf` | 1915-09-02 / 8 |
| IMG-0098 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-09.pdf` | 1915-09-02 / 9 |
| IMG-0099 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-10.pdf` | 1915-09-02 / 10 |
| IMG-0100 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-02-seq-11.pdf` | 1915-09-02 / 11 |
| IMG-0101 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-01.pdf` | 1915-09-09 / 1 |
| IMG-0102 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-02.pdf` | 1915-09-09 / 2 |
| IMG-0103 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-03.pdf` | 1915-09-09 / 3 |
| IMG-0104 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-04.pdf` | 1915-09-09 / 4 |
| IMG-0105 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-05.pdf` | 1915-09-09 / 5 |
| IMG-0106 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-06.pdf` | 1915-09-09 / 6 |
| IMG-0107 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-07.pdf` | 1915-09-09 / 7 |
| IMG-0108 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-09-seq-08.pdf` | 1915-09-09 / 8 |
| IMG-0109 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-01.pdf` | 1915-09-16 / 1 |
| IMG-0110 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-02.pdf` | 1915-09-16 / 2 |
| IMG-0111 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-03.pdf` | 1915-09-16 / 3 |
| IMG-0112 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-04.pdf` | 1915-09-16 / 4 |
| IMG-0113 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-05.pdf` | 1915-09-16 / 5 |
| IMG-0114 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-06.pdf` | 1915-09-16 / 6 |
| IMG-0115 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-07.pdf` | 1915-09-16 / 7 |
| IMG-0116 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-16-seq-08.pdf` | 1915-09-16 / 8 |
| IMG-0117 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-01.pdf` | 1915-09-23 / 1 |
| IMG-0118 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-02.pdf` | 1915-09-23 / 2 |
| IMG-0119 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-03.pdf` | 1915-09-23 / 3 |
| IMG-0120 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-04.pdf` | 1915-09-23 / 4 |
| IMG-0121 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-05.pdf` | 1915-09-23 / 5 |
| IMG-0122 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-06.pdf` | 1915-09-23 / 6 |
| IMG-0123 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-07.pdf` | 1915-09-23 / 7 |
| IMG-0124 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-23-seq-08.pdf` | 1915-09-23 / 8 |
| IMG-0125 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-01.pdf` | 1915-09-30 / 1 |
| IMG-0126 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-02.pdf` | 1915-09-30 / 2 |
| IMG-0127 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-03.pdf` | 1915-09-30 / 3 |
| IMG-0128 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-04.pdf` | 1915-09-30 / 4 |
| IMG-0129 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-05.pdf` | 1915-09-30 / 5 |
| IMG-0130 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-06.pdf` | 1915-09-30 / 6 |
| IMG-0131 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-07.pdf` | 1915-09-30 / 7 |
| IMG-0132 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-08.pdf` | 1915-09-30 / 8 |
| IMG-0133 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-09.pdf` | 1915-09-30 / 9 |
| IMG-0134 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-10.pdf` | 1915-09-30 / 10 |
| IMG-0135 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-09-30-seq-11.pdf` | 1915-09-30 / 11 |
| IMG-0136 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-01.pdf` | 1915-10-07 / 1 |
| IMG-0137 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-02.pdf` | 1915-10-07 / 2 |
| IMG-0138 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-03.pdf` | 1915-10-07 / 3 |
| IMG-0139 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-04.pdf` | 1915-10-07 / 4 |
| IMG-0140 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-05.pdf` | 1915-10-07 / 5 |
| IMG-0141 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-06.pdf` | 1915-10-07 / 6 |
| IMG-0142 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-07.pdf` | 1915-10-07 / 7 |
| IMG-0143 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-08.pdf` | 1915-10-07 / 8 |
| IMG-0144 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-09.pdf` | 1915-10-07 / 9 |
| IMG-0145 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-07-seq-10.pdf` | 1915-10-07 / 10 |
| IMG-0146 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-01.pdf` | 1915-10-14 / 1 |
| IMG-0147 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-02.pdf` | 1915-10-14 / 2 |
| IMG-0148 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-03.pdf` | 1915-10-14 / 3 |
| IMG-0149 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-04.pdf` | 1915-10-14 / 4 |
| IMG-0150 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-05.pdf` | 1915-10-14 / 5 |
| IMG-0151 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-06.pdf` | 1915-10-14 / 6 |
| IMG-0152 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-07.pdf` | 1915-10-14 / 7 |
| IMG-0153 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-14-seq-08.pdf` | 1915-10-14 / 8 |
| IMG-0154 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-01.pdf` | 1915-10-21 / 1 |
| IMG-0155 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-02.pdf` | 1915-10-21 / 2 |
| IMG-0156 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-03.pdf` | 1915-10-21 / 3 |
| IMG-0157 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-04.pdf` | 1915-10-21 / 4 |
| IMG-0158 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-05.pdf` | 1915-10-21 / 5 |
| IMG-0159 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-06.pdf` | 1915-10-21 / 6 |
| IMG-0160 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-07.pdf` | 1915-10-21 / 7 |
| IMG-0161 | `newspapers/oregon-city-courier/1915-sheets-073-100/1915-10-21-seq-08.pdf` | 1915-10-21 / 8 |

## Courier sheets 101–110 — S-121 / E-109, reviewed 27 August 2026

All 40 original single-page PDFs below are visually verified supplied images. Exact URLs, SHA-256 hashes, printed numbering and date status are in `newspapers/oregon-city-courier/1915-sheets-101-110/manifest.json`. November 11 seq 8 is printed 6; 1915-M04 remains unresolved. These records extend the checkpoint through November 25, not annual completion.

| Media ID | Original repository file | Issue / archive sequence / printed page |
| --- | --- | --- |
| IMG-0162 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-01.pdf` | 1915-10-28 / seq1 / printed1 |
| IMG-0163 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-02.pdf` | 1915-10-28 / seq2 / printed2 |
| IMG-0164 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-03.pdf` | 1915-10-28 / seq3 / printed3 |
| IMG-0165 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-04.pdf` | 1915-10-28 / seq4 / printed4 |
| IMG-0166 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-05.pdf` | 1915-10-28 / seq5 / printed5 |
| IMG-0167 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-06.pdf` | 1915-10-28 / seq6 / printed6 |
| IMG-0168 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-07.pdf` | 1915-10-28 / seq7 / printed7 |
| IMG-0169 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-10-28-seq-08.pdf` | 1915-10-28 / seq8 / printed8 |
| IMG-0170 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-01.pdf` | 1915-11-04 / seq1 / printed1 |
| IMG-0171 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-02.pdf` | 1915-11-04 / seq2 / printed2 |
| IMG-0172 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-03.pdf` | 1915-11-04 / seq3 / printed3 |
| IMG-0173 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-04.pdf` | 1915-11-04 / seq4 / printed4 |
| IMG-0174 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-05.pdf` | 1915-11-04 / seq5 / printed5 |
| IMG-0175 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-06.pdf` | 1915-11-04 / seq6 / printed6 |
| IMG-0176 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-07.pdf` | 1915-11-04 / seq7 / printed7 |
| IMG-0177 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-04-seq-08.pdf` | 1915-11-04 / seq8 / printed8 |
| IMG-0178 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-01.pdf` | 1915-11-11 / seq1 / printed1 |
| IMG-0179 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-02.pdf` | 1915-11-11 / seq2 / printed2 |
| IMG-0180 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-03.pdf` | 1915-11-11 / seq3 / printed3 |
| IMG-0181 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-04.pdf` | 1915-11-11 / seq4 / printed4 |
| IMG-0182 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-05.pdf` | 1915-11-11 / seq5 / printed5 |
| IMG-0183 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-06.pdf` | 1915-11-11 / seq6 / printed6 |
| IMG-0184 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-07.pdf` | 1915-11-11 / seq7 / printed7 |
| IMG-0185 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-08.pdf` | 1915-11-11 / seq8 / printed6 |
| IMG-0186 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-01.pdf` | 1915-11-18 / seq1 / printed1 |
| IMG-0187 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-02.pdf` | 1915-11-18 / seq2 / printed2 |
| IMG-0188 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-03.pdf` | 1915-11-18 / seq3 / printed3 |
| IMG-0189 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-04.pdf` | 1915-11-18 / seq4 / printed4 |
| IMG-0190 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-05.pdf` | 1915-11-18 / seq5 / printed5 |
| IMG-0191 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-06.pdf` | 1915-11-18 / seq6 / printed6 |
| IMG-0192 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-07.pdf` | 1915-11-18 / seq7 / printed7 |
| IMG-0193 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-18-seq-08.pdf` | 1915-11-18 / seq8 / printed8 |
| IMG-0194 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-01.pdf` | 1915-11-25 / seq1 / printed1 |
| IMG-0195 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-02.pdf` | 1915-11-25 / seq2 / printed2 |
| IMG-0196 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-03.pdf` | 1915-11-25 / seq3 / printed3 |
| IMG-0197 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-04.pdf` | 1915-11-25 / seq4 / printed4 |
| IMG-0198 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-05.pdf` | 1915-11-25 / seq5 / printed5 |
| IMG-0199 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-06.pdf` | 1915-11-25 / seq6 / printed6 |
| IMG-0200 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-07.pdf` | 1915-11-25 / seq7 / printed7 |
| IMG-0201 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-25-seq-08.pdf` | 1915-11-25 / seq8 / printed8 |
| IMG-0202 | `newspapers/oregon-city-courier/1915-sheets-101-110/1915-11-11-seq-08-iiif-header.jpg` | Alternate archive IIIF header; printed6 confirmed; provenance/hash in batch README |

## Courier December batch media - S-122 / E-110, reviewed 27 August 2026

Each ID below represents one unchanged original PDF scan. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-courier/1915-sheets-111-123/manifest.json`. All 46 supplied images are VISUALLY VERIFIED.

| Media ID | Repository file | Issue association / sequence |
| --- | --- | --- |
| IMG-0203 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-01.pdf` | 1915-12-02 / seq1 / printed1 |
| IMG-0204 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-02.pdf` | 1915-12-02 / seq2 / printed2 |
| IMG-0205 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-03.pdf` | 1915-12-02 / seq3 / printed3 |
| IMG-0206 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-04.pdf` | 1915-12-02 / seq4 / printed4 |
| IMG-0207 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-05.pdf` | 1915-12-02 / seq5 / printed5 |
| IMG-0208 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-06.pdf` | 1915-12-02 / seq6 / printed6 |
| IMG-0209 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-07.pdf` | 1915-12-02 / seq7 / printed7 |
| IMG-0210 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-08.pdf` | 1915-12-02 / seq8 / printed8 |
| IMG-0211 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-09.pdf` | 1915-12-02 / seq9 / printed9 |
| IMG-0212 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-02-seq-10.pdf` | 1915-12-02 / seq10 / printed10 |
| IMG-0213 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-01.pdf` | 1915-12-09 / seq1 / printed1 |
| IMG-0214 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-02.pdf` | 1915-12-09 / seq2 / printed2 |
| IMG-0215 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-03.pdf` | 1915-12-09 / seq3 / printed3 |
| IMG-0216 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-04.pdf` | 1915-12-09 / seq4 / printed4 |
| IMG-0217 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-05.pdf` | 1915-12-09 / seq5 / printed5 |
| IMG-0218 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-06.pdf` | 1915-12-09 / seq6 / printed6 |
| IMG-0219 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-07.pdf` | 1915-12-09 / seq7 / printed7 |
| IMG-0220 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-08.pdf` | 1915-12-09 / seq8 / printed8 |
| IMG-0221 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-09.pdf` | 1915-12-09 / seq9 / printed9 |
| IMG-0222 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-09-seq-10.pdf` | 1915-12-09 / seq10 / printed10 |
| IMG-0223 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-01.pdf` | 1915-12-16 / seq1 / printed1 |
| IMG-0224 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-02.pdf` | 1915-12-16 / seq2 / printed2 |
| IMG-0225 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-03.pdf` | 1915-12-16 / seq3 / printed3 |
| IMG-0226 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-04.pdf` | 1915-12-16 / seq4 / printed4 |
| IMG-0227 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-05.pdf` | 1915-12-16 / seq5 / printed5 |
| IMG-0228 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-06.pdf` | 1915-12-16 / seq6 / printed6 |
| IMG-0229 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-07.pdf` | 1915-12-16 / seq7 / printed7 |
| IMG-0230 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-08.pdf` | 1915-12-16 / seq8 / printed8 |
| IMG-0231 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-09.pdf` | 1915-12-16 / seq9 / printed9 |
| IMG-0232 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-16-seq-10.pdf` | 1915-12-16 / seq10 / printed10 |
| IMG-0233 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-01.pdf` | 1915-12-23 / seq1 / printed1 |
| IMG-0234 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-02.pdf` | 1915-12-23 / seq2 / printed2 |
| IMG-0235 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-03.pdf` | 1915-12-23 / seq3 / printed3 |
| IMG-0236 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-04.pdf` | 1915-12-23 / seq4 / printed4 |
| IMG-0237 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-05.pdf` | 1915-12-23 / seq5 / printed5 |
| IMG-0238 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-06.pdf` | 1915-12-23 / seq6 / printed6 |
| IMG-0239 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-07.pdf` | 1915-12-23 / seq7 / printed7 |
| IMG-0240 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-23-seq-08.pdf` | 1915-12-23 / seq8 / printed8 |
| IMG-0241 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-01.pdf` | 1915-12-30 / seq1 / printed1 |
| IMG-0242 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-02.pdf` | 1915-12-30 / seq2 / printed2 |
| IMG-0243 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-03.pdf` | 1915-12-30 / seq3 / printed3 |
| IMG-0244 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-04.pdf` | 1915-12-30 / seq4 / printed4 |
| IMG-0245 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-05.pdf` | 1915-12-30 / seq5 / printed5 |
| IMG-0246 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-06.pdf` | 1915-12-30 / seq6 / printed6 |
| IMG-0247 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-07.pdf` | 1915-12-30 / seq7 / printed7 |
| IMG-0248 | `newspapers/oregon-city-courier/1915-sheets-111-123/1915-12-30-seq-08.pdf` | 1915-12-30 / seq8 / printed8 |

## Morning Enterprise 1915 pages 1–120 — S-123 / E-111

All 120 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-001-120/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
| IMG-0249 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-01.pdf` | 1915-01-01 / seq1 / printed1 |
| IMG-0250 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-02.pdf` | 1915-01-01 / seq2 / printed2 |
| IMG-0251 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-03.pdf` | 1915-01-01 / seq3 / printed3 |
| IMG-0252 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-04.pdf` | 1915-01-01 / seq4 / printed4 |
| IMG-0253 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-05.pdf` | 1915-01-01 / seq5 / printed5 |
| IMG-0254 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-06.pdf` | 1915-01-01 / seq6 / printed6 |
| IMG-0255 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-07.pdf` | 1915-01-01 / seq7 / printed7 |
| IMG-0256 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-01-seq-08.pdf` | 1915-01-01 / seq8 / printed8 |
| IMG-0257 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-01.pdf` | 1915-01-08 / seq1 / printed1 |
| IMG-0258 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-02.pdf` | 1915-01-08 / seq2 / printed2 |
| IMG-0259 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-03.pdf` | 1915-01-08 / seq3 / printed3 |
| IMG-0260 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-04.pdf` | 1915-01-08 / seq4 / printed4 |
| IMG-0261 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-05.pdf` | 1915-01-08 / seq5 / printed5 |
| IMG-0262 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-06.pdf` | 1915-01-08 / seq6 / printed6 |
| IMG-0263 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-07.pdf` | 1915-01-08 / seq7 / printed7 |
| IMG-0264 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-08-seq-08.pdf` | 1915-01-08 / seq8 / printed8 |
| IMG-0265 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-01.pdf` | 1915-01-15 / seq1 / printed1 |
| IMG-0266 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-02.pdf` | 1915-01-15 / seq2 / printed2 |
| IMG-0267 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-03.pdf` | 1915-01-15 / seq3 / printed3 |
| IMG-0268 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-04.pdf` | 1915-01-15 / seq4 / printed4 |
| IMG-0269 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-05.pdf` | 1915-01-15 / seq5 / printed5 |
| IMG-0270 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-06.pdf` | 1915-01-15 / seq6 / printed6 |
| IMG-0271 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-07.pdf` | 1915-01-15 / seq7 / printed7 |
| IMG-0272 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-15-seq-08.pdf` | 1915-01-15 / seq8 / printed8 |
| IMG-0273 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-01.pdf` | 1915-01-22 / seq1 / printed1 |
| IMG-0274 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-02.pdf` | 1915-01-22 / seq2 / printed2 |
| IMG-0275 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-03.pdf` | 1915-01-22 / seq3 / printed3 |
| IMG-0276 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-04.pdf` | 1915-01-22 / seq4 / printed4 |
| IMG-0277 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-05.pdf` | 1915-01-22 / seq5 / printed5 |
| IMG-0278 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-06.pdf` | 1915-01-22 / seq6 / printed6 |
| IMG-0279 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-07.pdf` | 1915-01-22 / seq7 / printed7 |
| IMG-0280 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-22-seq-08.pdf` | 1915-01-22 / seq8 / printed8 |
| IMG-0281 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-01.pdf` | 1915-01-29 / seq1 / printed1 |
| IMG-0282 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-02.pdf` | 1915-01-29 / seq2 / printed2 |
| IMG-0283 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-03.pdf` | 1915-01-29 / seq3 / printed3 |
| IMG-0284 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-04.pdf` | 1915-01-29 / seq4 / printed4 |
| IMG-0285 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-05.pdf` | 1915-01-29 / seq5 / printed5 |
| IMG-0286 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-06.pdf` | 1915-01-29 / seq6 / printed6 |
| IMG-0287 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-07.pdf` | 1915-01-29 / seq7 / printed7 |
| IMG-0288 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-01-29-seq-08.pdf` | 1915-01-29 / seq8 / printed8 |
| IMG-0289 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-01.pdf` | 1915-02-05 / seq1 / printed1 |
| IMG-0290 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-02.pdf` | 1915-02-05 / seq2 / printed2 |
| IMG-0291 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-03.pdf` | 1915-02-05 / seq3 / printed3 |
| IMG-0292 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-04.pdf` | 1915-02-05 / seq4 / printed4 |
| IMG-0293 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-05.pdf` | 1915-02-05 / seq5 / printed5 |
| IMG-0294 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-06.pdf` | 1915-02-05 / seq6 / printed6 |
| IMG-0295 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-07.pdf` | 1915-02-05 / seq7 / printed7 |
| IMG-0296 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-05-seq-08.pdf` | 1915-02-05 / seq8 / printed8 |
| IMG-0297 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-01.pdf` | 1915-02-12 / seq1 / printed1 |
| IMG-0298 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-02.pdf` | 1915-02-12 / seq2 / printed2 |
| IMG-0299 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-03.pdf` | 1915-02-12 / seq3 / printed3 |
| IMG-0300 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-04.pdf` | 1915-02-12 / seq4 / printed4 |
| IMG-0301 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-05.pdf` | 1915-02-12 / seq5 / printed5 |
| IMG-0302 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-06.pdf` | 1915-02-12 / seq6 / printed6 |
| IMG-0303 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-07.pdf` | 1915-02-12 / seq7 / printed7 |
| IMG-0304 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-12-seq-08.pdf` | 1915-02-12 / seq8 / printed8 |
| IMG-0305 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-01.pdf` | 1915-02-19 / seq1 / printed1 |
| IMG-0306 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-02.pdf` | 1915-02-19 / seq2 / printed2 |
| IMG-0307 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-03.pdf` | 1915-02-19 / seq3 / printed3 |
| IMG-0308 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-04.pdf` | 1915-02-19 / seq4 / printed4 |
| IMG-0309 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-05.pdf` | 1915-02-19 / seq5 / printed5 |
| IMG-0310 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-06.pdf` | 1915-02-19 / seq6 / printed6 |
| IMG-0311 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-07.pdf` | 1915-02-19 / seq7 / printed7 |
| IMG-0312 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-19-seq-08.pdf` | 1915-02-19 / seq8 / printed8 |
| IMG-0313 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-01.pdf` | 1915-02-26 / seq1 / printed1 |
| IMG-0314 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-02.pdf` | 1915-02-26 / seq2 / printed2 |
| IMG-0315 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-03.pdf` | 1915-02-26 / seq3 / printed3 |
| IMG-0316 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-04.pdf` | 1915-02-26 / seq4 / printed4 |
| IMG-0317 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-05.pdf` | 1915-02-26 / seq5 / printed5 |
| IMG-0318 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-06.pdf` | 1915-02-26 / seq6 / printed6 |
| IMG-0319 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-07.pdf` | 1915-02-26 / seq7 / printed7 |
| IMG-0320 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-02-26-seq-08.pdf` | 1915-02-26 / seq8 / printed8 |
| IMG-0321 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-01.pdf` | 1915-03-05 / seq1 / printed1 |
| IMG-0322 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-02.pdf` | 1915-03-05 / seq2 / printed2 |
| IMG-0323 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-03.pdf` | 1915-03-05 / seq3 / printed3 |
| IMG-0324 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-04.pdf` | 1915-03-05 / seq4 / printed4 |
| IMG-0325 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-05.pdf` | 1915-03-05 / seq5 / printed5 |
| IMG-0326 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-06.pdf` | 1915-03-05 / seq6 / printed6 |
| IMG-0327 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-07.pdf` | 1915-03-05 / seq7 / printed7 |
| IMG-0328 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-05-seq-08.pdf` | 1915-03-05 / seq8 / printed8 |
| IMG-0329 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-01.pdf` | 1915-03-12 / seq1 / printed1 |
| IMG-0330 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-02.pdf` | 1915-03-12 / seq2 / printed2 |
| IMG-0331 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-03.pdf` | 1915-03-12 / seq3 / printed3 |
| IMG-0332 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-04.pdf` | 1915-03-12 / seq4 / printed4 |
| IMG-0333 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-05.pdf` | 1915-03-12 / seq5 / printed5 |
| IMG-0334 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-06.pdf` | 1915-03-12 / seq6 / printed6 |
| IMG-0335 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-07.pdf` | 1915-03-12 / seq7 / printed7 |
| IMG-0336 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-12-seq-08.pdf` | 1915-03-12 / seq8 / printed8 |
| IMG-0337 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-01.pdf` | 1915-03-19 / seq1 / printed1 |
| IMG-0338 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-02.pdf` | 1915-03-19 / seq2 / printed2 |
| IMG-0339 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-03.pdf` | 1915-03-19 / seq3 / printed3 |
| IMG-0340 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-04.pdf` | 1915-03-19 / seq4 / printed4 |
| IMG-0341 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-05.pdf` | 1915-03-19 / seq5 / printed5 |
| IMG-0342 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-06.pdf` | 1915-03-19 / seq6 / printed6 |
| IMG-0343 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-07.pdf` | 1915-03-19 / seq7 / printed7 |
| IMG-0344 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-19-seq-08.pdf` | 1915-03-19 / seq8 / printed8 |
| IMG-0345 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-01.pdf` | 1915-03-26 / seq1 / printed1 |
| IMG-0346 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-02.pdf` | 1915-03-26 / seq2 / printed2 |
| IMG-0347 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-03.pdf` | 1915-03-26 / seq3 / printed3 |
| IMG-0348 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-04.pdf` | 1915-03-26 / seq4 / printed4 |
| IMG-0349 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-05.pdf` | 1915-03-26 / seq5 / printed5 |
| IMG-0350 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-06.pdf` | 1915-03-26 / seq6 / printed6 |
| IMG-0351 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-07.pdf` | 1915-03-26 / seq7 / printed7 |
| IMG-0352 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-03-26-seq-08.pdf` | 1915-03-26 / seq8 / printed8 |
| IMG-0353 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-01.pdf` | 1915-04-02 / seq1 / printed1 |
| IMG-0354 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-02.pdf` | 1915-04-02 / seq2 / printed2 |
| IMG-0355 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-03.pdf` | 1915-04-02 / seq3 / printed3 |
| IMG-0356 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-04.pdf` | 1915-04-02 / seq4 / printed4 |
| IMG-0357 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-05.pdf` | 1915-04-02 / seq5 / printed5 |
| IMG-0358 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-06.pdf` | 1915-04-02 / seq6 / printed6 |
| IMG-0359 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-07.pdf` | 1915-04-02 / seq7 / printed7 |
| IMG-0360 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-02-seq-08.pdf` | 1915-04-02 / seq8 / printed8 |
| IMG-0361 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-01.pdf` | 1915-04-09 / seq1 / printed1 |
| IMG-0362 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-02.pdf` | 1915-04-09 / seq2 / printed2 |
| IMG-0363 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-03.pdf` | 1915-04-09 / seq3 / printed3 |
| IMG-0364 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-04.pdf` | 1915-04-09 / seq4 / printed4 |
| IMG-0365 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-05.pdf` | 1915-04-09 / seq5 / printed5 |
| IMG-0366 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-06.pdf` | 1915-04-09 / seq6 / printed6 |
| IMG-0367 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-07.pdf` | 1915-04-09 / seq7 / printed7 |
| IMG-0368 | `newspapers/oregon-city-enterprise/1915-pages-001-120/1915-04-09-seq-08.pdf` | 1915-04-09 / seq8 / printed8 |

## Morning Enterprise 1915 pages 121-160 - S-124 / E-112

All 40 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-121-160/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
| IMG-0369 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-01.pdf` | 1915-04-16 / seq1 / printed1 |
| IMG-0370 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-02.pdf` | 1915-04-16 / seq2 / printed2 |
| IMG-0371 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-03.pdf` | 1915-04-16 / seq3 / printed3 |
| IMG-0372 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-04.pdf` | 1915-04-16 / seq4 / printed4 |
| IMG-0373 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-05.pdf` | 1915-04-16 / seq5 / printed5 |
| IMG-0374 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-06.pdf` | 1915-04-16 / seq6 / printed6 |
| IMG-0375 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-07.pdf` | 1915-04-16 / seq7 / printed7 |
| IMG-0376 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-16-seq-08.pdf` | 1915-04-16 / seq8 / printed8 |
| IMG-0377 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-01.pdf` | 1915-04-23 / seq1 / printed1 |
| IMG-0378 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-02.pdf` | 1915-04-23 / seq2 / printed2 |
| IMG-0379 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-03.pdf` | 1915-04-23 / seq3 / printed3 |
| IMG-0380 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-04.pdf` | 1915-04-23 / seq4 / printed4 |
| IMG-0381 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-05.pdf` | 1915-04-23 / seq5 / printed5 |
| IMG-0382 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-06.pdf` | 1915-04-23 / seq6 / printed6 |
| IMG-0383 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-07.pdf` | 1915-04-23 / seq7 / printed7 |
| IMG-0384 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-23-seq-08.pdf` | 1915-04-23 / seq8 / printed8 |
| IMG-0385 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-01.pdf` | 1915-04-30 / seq1 / printed1 |
| IMG-0386 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-02.pdf` | 1915-04-30 / seq2 / printed2 |
| IMG-0387 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-03.pdf` | 1915-04-30 / seq3 / printed3 |
| IMG-0388 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-04.pdf` | 1915-04-30 / seq4 / printed4 |
| IMG-0389 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-05.pdf` | 1915-04-30 / seq5 / printed5 |
| IMG-0390 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-06.pdf` | 1915-04-30 / seq6 / printed6 |
| IMG-0391 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-07.pdf` | 1915-04-30 / seq7 / printed7 |
| IMG-0392 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-04-30-seq-08.pdf` | 1915-04-30 / seq8 / printed8 |
| IMG-0393 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-01.pdf` | 1915-05-07 / seq1 / printed1 |
| IMG-0394 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-02.pdf` | 1915-05-07 / seq2 / printed2 |
| IMG-0395 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-03.pdf` | 1915-05-07 / seq3 / printed3 |
| IMG-0396 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-04.pdf` | 1915-05-07 / seq4 / printed4 |
| IMG-0397 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-05.pdf` | 1915-05-07 / seq5 / printed5 |
| IMG-0398 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-06.pdf` | 1915-05-07 / seq6 / printed6 |
| IMG-0399 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-07.pdf` | 1915-05-07 / seq7 / printed7 |
| IMG-0400 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-07-seq-08.pdf` | 1915-05-07 / seq8 / printed8 |
| IMG-0401 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-01.pdf` | 1915-05-14 / seq1 / printed1 |
| IMG-0402 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-02.pdf` | 1915-05-14 / seq2 / printed2 |
| IMG-0403 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-03.pdf` | 1915-05-14 / seq3 / printed3 |
| IMG-0404 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-04.pdf` | 1915-05-14 / seq4 / printed4 |
| IMG-0405 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-05.pdf` | 1915-05-14 / seq5 / printed5 |
| IMG-0406 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-06.pdf` | 1915-05-14 / seq6 / printed6 |
| IMG-0407 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-07.pdf` | 1915-05-14 / seq7 / printed7 |
| IMG-0408 | `newspapers/oregon-city-enterprise/1915-pages-121-160/1915-05-14-seq-08.pdf` | 1915-05-14 / seq8 / printed8 |

## 1922 Tasks 5–6 identity-source batch — preserved 28 August 2026

Raw source files are unchanged. Exact SHA-256 hashes and detailed review limits: [identity audit](../evidence/source-captures/1922-tasks-5-6-identity-review-2026-08-28.md). Five page images inspected across five files; the 37-page nomination is credited for **page 15 only**. No annual completeness claim.

| Media ID | Repository file | Original filename / source | Verification and related records |
| --- | --- | --- | --- |
| IMG-0409 | `newspapers/lane-county-news/1916-02-03-page-1-gilbert-miller.pdf` | `seq-1.pdf`; [UO page PDF](https://oregonnews.uoregon.edu/lccn/sn97071002/1916-02-03/ed-1/seq-1.pdf) | VISUALLY VERIFIED targeted p1/col4 item and masthead; S-125/E-113/P-046/BUS-012. Not whole-issue coverage. |
| IMG-0410 | `records/directories/1920-polk-portland-page-542.jpg` | `n545.jpg`; [Newberry/Internet Archive Vol. I image](https://archive.org/download/CITY_DIRECTORY_PORTLAND_1920_1/page/n545.jpg) | VISUALLY VERIFIED Gates surname start at bottom right; S-126/E-113. Image-edge limits retained. |
| IMG-0411 | `records/directories/1920-polk-portland-page-543.jpg` | `n546.jpg`; [Newberry/Internet Archive Vol. I image](https://archive.org/download/CITY_DIRECTORY_PORTLAND_1920_1/page/n546.jpg) | VISUALLY VERIFIED Gates continuation, no buyer identification; S-126/E-113. Image-edge limits retained. |
| IMG-0412 | `records/directories/1920-polk-portland-page-1538.jpg` | `n571.jpg`; [Newberry/Internet Archive Vol. II image](https://archive.org/download/CITY_DIRECTORY_PORTLAND_1920_2/page/n571.jpg) | VISUALLY VERIFIED cited left-column Wolf entries; right column clipped. S-126/E-113; P-035 comparison only, no identity merger. |
| IMG-0413 | `records/historic-resource/1990-medford-pop-gates-house-nomination.pdf` | NPS asset `b463e75a-f84f-4c46-b1e2-1859a13aa4c2`; [original PDF](https://npgallery.nps.gov/GetAsset/b463e75a-f84f-4c46-b1e2-1859a13aa4c2) | VISUALLY VERIFIED PDF p15 / section8 printed1B only; full37-page file preserved. Secondary biography, S-127/E-113; P-036 comparison only. |

## Morning Enterprise 1915 pages 161-200 - S-128 / E-114

All 40 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-161-200/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
| IMG-0414 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-01.pdf` | 1915-05-21 / seq1 / printed1 |
| IMG-0415 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-02.pdf` | 1915-05-21 / seq2 / printed2 |
| IMG-0416 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-03.pdf` | 1915-05-21 / seq3 / printed3 |
| IMG-0417 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-04.pdf` | 1915-05-21 / seq4 / printed4 |
| IMG-0418 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-05.pdf` | 1915-05-21 / seq5 / printed5 |
| IMG-0419 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-06.pdf` | 1915-05-21 / seq6 / printed6 |
| IMG-0420 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-07.pdf` | 1915-05-21 / seq7 / printed7 |
| IMG-0421 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-21-seq-08.pdf` | 1915-05-21 / seq8 / printed8 |
| IMG-0422 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-01.pdf` | 1915-05-28 / seq1 / printed1 |
| IMG-0423 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-02.pdf` | 1915-05-28 / seq2 / printed2 |
| IMG-0424 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-03.pdf` | 1915-05-28 / seq3 / printed3 |
| IMG-0425 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-04.pdf` | 1915-05-28 / seq4 / printed4 |
| IMG-0426 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-05.pdf` | 1915-05-28 / seq5 / printed5 |
| IMG-0427 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-06.pdf` | 1915-05-28 / seq6 / printed6 |
| IMG-0428 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-07.pdf` | 1915-05-28 / seq7 / printed7 |
| IMG-0429 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-05-28-seq-08.pdf` | 1915-05-28 / seq8 / printed8 |
| IMG-0430 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-01.pdf` | 1915-06-04 / seq1 / printed1 |
| IMG-0431 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-02.pdf` | 1915-06-04 / seq2 / printed2 |
| IMG-0432 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-03.pdf` | 1915-06-04 / seq3 / printed3 |
| IMG-0433 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-04.pdf` | 1915-06-04 / seq4 / printed4 |
| IMG-0434 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-05.pdf` | 1915-06-04 / seq5 / printed5 |
| IMG-0435 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-06.pdf` | 1915-06-04 / seq6 / printed6 |
| IMG-0436 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-07.pdf` | 1915-06-04 / seq7 / printed7 |
| IMG-0437 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-04-seq-08.pdf` | 1915-06-04 / seq8 / printed8 |
| IMG-0438 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-01.pdf` | 1915-06-11 / seq1 / printed1 |
| IMG-0439 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-02.pdf` | 1915-06-11 / seq2 / printed2 |
| IMG-0440 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-03.pdf` | 1915-06-11 / seq3 / printed3 |
| IMG-0441 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-04.pdf` | 1915-06-11 / seq4 / printed4 |
| IMG-0442 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-05.pdf` | 1915-06-11 / seq5 / printed5 |
| IMG-0443 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-06.pdf` | 1915-06-11 / seq6 / printed6 |
| IMG-0444 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-07.pdf` | 1915-06-11 / seq7 / printed7 |
| IMG-0445 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-11-seq-08.pdf` | 1915-06-11 / seq8 / printed8 |
| IMG-0446 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-01.pdf` | 1915-06-18 / seq1 / printed1 |
| IMG-0447 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-02.pdf` | 1915-06-18 / seq2 / printed2 |
| IMG-0448 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-03.pdf` | 1915-06-18 / seq3 / printed3 |
| IMG-0449 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-04.pdf` | 1915-06-18 / seq4 / printed4 |
| IMG-0450 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-05.pdf` | 1915-06-18 / seq5 / printed5 |
| IMG-0451 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-06.pdf` | 1915-06-18 / seq6 / printed6 |
| IMG-0452 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-07.pdf` | 1915-06-18 / seq7 / printed7 |
| IMG-0453 | `newspapers/oregon-city-enterprise/1915-pages-161-200/1915-06-18-seq-08.pdf` | 1915-06-18 / seq8 / printed8 |

## Morning Enterprise 1915 pages 201-225 - S-129 / E-115

All 25 original page PDFs are VISUALLY VERIFIED. Exact source URLs and SHA-256 hashes are in `newspapers/oregon-city-enterprise/1915-pages-201-225/manifest.json`.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
| IMG-0454 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-01.pdf` | 1915-06-25 / seq1 / printed1 |
| IMG-0455 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-02.pdf` | 1915-06-25 / seq2 / printed2 |
| IMG-0456 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-03.pdf` | 1915-06-25 / seq3 / printed3 |
| IMG-0457 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-04.pdf` | 1915-06-25 / seq4 / printed4 |
| IMG-0458 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-05.pdf` | 1915-06-25 / seq5 / printed5 |
| IMG-0459 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-06.pdf` | 1915-06-25 / seq6 / printed6 |
| IMG-0460 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-07.pdf` | 1915-06-25 / seq7 / printed7 |
| IMG-0461 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-06-25-seq-08.pdf` | 1915-06-25 / seq8 / printed8 |
| IMG-0462 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-01.pdf` | 1915-07-02 / seq1 / printed1 |
| IMG-0463 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-02.pdf` | 1915-07-02 / seq2 / printed2 |
| IMG-0464 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-03.pdf` | 1915-07-02 / seq3 / printed3 |
| IMG-0465 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-04.pdf` | 1915-07-02 / seq4 / printed4 |
| IMG-0466 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-05.pdf` | 1915-07-02 / seq5 / printed5 |
| IMG-0467 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-06.pdf` | 1915-07-02 / seq6 / printed6 |
| IMG-0468 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-07.pdf` | 1915-07-02 / seq7 / printed7 |
| IMG-0469 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-02-seq-08.pdf` | 1915-07-02 / seq8 / printed8 |
| IMG-0470 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-01.pdf` | 1915-07-09 / seq1 / printed1 |
| IMG-0471 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-02.pdf` | 1915-07-09 / seq2 / printed2 |
| IMG-0472 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-03.pdf` | 1915-07-09 / seq3 / printed3 |
| IMG-0473 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-04.pdf` | 1915-07-09 / seq4 / printed4 |
| IMG-0474 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-05.pdf` | 1915-07-09 / seq5 / printed5 |
| IMG-0475 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-06.pdf` | 1915-07-09 / seq6 / printed6 |
| IMG-0476 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-07.pdf` | 1915-07-09 / seq7 / printed7 |
| IMG-0477 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-09-seq-08.pdf` | 1915-07-09 / seq8 / printed8 |
| IMG-0478 | `newspapers/oregon-city-enterprise/1915-pages-201-225/1915-07-16-seq-01.pdf` | 1915-07-16 / seq1 / printed1 |

## Courier 1916 pages 106–180 — S-130 / E-116

All 75 original PDFs committed and VISUALLY VERIFIED; normalized filenames preserve original archive URLs in the manifest. No screenshots substitute for originals.

| Media ID | Repository file | Issue / sequence |
| --- | --- | --- |
| IMG-0479 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-01.pdf` | 1916-03-23 / seq1 / printed1 |
| IMG-0480 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-02.pdf` | 1916-03-23 / seq2 / printed2 |
| IMG-0481 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-03.pdf` | 1916-03-23 / seq3 / printed3 |
| IMG-0482 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-04.pdf` | 1916-03-23 / seq4 / printed4 |
| IMG-0483 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-05.pdf` | 1916-03-23 / seq5 / printed5 |
| IMG-0484 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-06.pdf` | 1916-03-23 / seq6 / printed6 |
| IMG-0485 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-07.pdf` | 1916-03-23 / seq7 / printed7 |
| IMG-0486 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-23-page-08.pdf` | 1916-03-23 / seq8 / printed8 |
| IMG-0487 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-01.pdf` | 1916-03-30 / seq1 / printed1 |
| IMG-0488 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-02.pdf` | 1916-03-30 / seq2 / printed2 |
| IMG-0489 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-03.pdf` | 1916-03-30 / seq3 / printed3 |
| IMG-0490 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-04.pdf` | 1916-03-30 / seq4 / printed4 |
| IMG-0491 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-05.pdf` | 1916-03-30 / seq5 / printed5 |
| IMG-0492 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-06.pdf` | 1916-03-30 / seq6 / printed6 |
| IMG-0493 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-07.pdf` | 1916-03-30 / seq7 / printed7 |
| IMG-0494 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-03-30-page-08.pdf` | 1916-03-30 / seq8 / printed8 |
| IMG-0495 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-01.pdf` | 1916-04-06 / seq1 / printed1 |
| IMG-0496 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-02.pdf` | 1916-04-06 / seq2 / printed2 |
| IMG-0497 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-03.pdf` | 1916-04-06 / seq3 / printed3 |
| IMG-0498 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-04.pdf` | 1916-04-06 / seq4 / printed4 |
| IMG-0499 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-05.pdf` | 1916-04-06 / seq5 / printed5 |
| IMG-0500 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-06.pdf` | 1916-04-06 / seq6 / printed6 |
| IMG-0501 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-07.pdf` | 1916-04-06 / seq7 / printed7 |
| IMG-0502 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-06-page-08.pdf` | 1916-04-06 / seq8 / printed8 |
| IMG-0503 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-01.pdf` | 1916-04-13 / seq1 / printed1 |
| IMG-0504 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-02.pdf` | 1916-04-13 / seq2 / printed2 |
| IMG-0505 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-03.pdf` | 1916-04-13 / seq3 / printed3 |
| IMG-0506 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-04.pdf` | 1916-04-13 / seq4 / printed4 |
| IMG-0507 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-05.pdf` | 1916-04-13 / seq5 / printed5 |
| IMG-0508 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-06.pdf` | 1916-04-13 / seq6 / printed6 |
| IMG-0509 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-07.pdf` | 1916-04-13 / seq7 / printed7 |
| IMG-0510 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-13-page-08.pdf` | 1916-04-13 / seq8 / printed8 |
| IMG-0511 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-01.pdf` | 1916-04-20 / seq1 / printed1 |
| IMG-0512 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-02.pdf` | 1916-04-20 / seq2 / printed2 |
| IMG-0513 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-03.pdf` | 1916-04-20 / seq3 / printed3 |
| IMG-0514 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-04.pdf` | 1916-04-20 / seq4 / printed4 |
| IMG-0515 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-05.pdf` | 1916-04-20 / seq5 / printed5 |
| IMG-0516 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-06.pdf` | 1916-04-20 / seq6 / printed6 |
| IMG-0517 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-07.pdf` | 1916-04-20 / seq7 / printed7 |
| IMG-0518 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-08.pdf` | 1916-04-20 / seq8 / printed8 |
| IMG-0519 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-09.pdf` | 1916-04-20 / seq9 / printed9 |
| IMG-0520 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-10.pdf` | 1916-04-20 / seq10 / printed10 |
| IMG-0521 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-11.pdf` | 1916-04-20 / seq11 / printed11 |
| IMG-0522 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-20-page-12.pdf` | 1916-04-20 / seq12 / printed12 |
| IMG-0523 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-01.pdf` | 1916-04-27 / seq1 / printed1 |
| IMG-0524 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-02.pdf` | 1916-04-27 / seq2 / printed2 |
| IMG-0525 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-03.pdf` | 1916-04-27 / seq3 / printed3 |
| IMG-0526 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-04.pdf` | 1916-04-27 / seq4 / printed4 |
| IMG-0527 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-05.pdf` | 1916-04-27 / seq5 / printed5 |
| IMG-0528 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-06.pdf` | 1916-04-27 / seq6 / printed6 |
| IMG-0529 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-07.pdf` | 1916-04-27 / seq7 / printed7 |
| IMG-0530 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-04-27-page-08.pdf` | 1916-04-27 / seq8 / printed8 |
| IMG-0531 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-01.pdf` | 1916-05-04 / seq1 / printed1 |
| IMG-0532 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-02.pdf` | 1916-05-04 / seq2 / printed2 |
| IMG-0533 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-03.pdf` | 1916-05-04 / seq3 / printed3 |
| IMG-0534 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-04.pdf` | 1916-05-04 / seq4 / printed4 |
| IMG-0535 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-05.pdf` | 1916-05-04 / seq5 / printed5 |
| IMG-0536 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-06.pdf` | 1916-05-04 / seq6 / printed6 |
| IMG-0537 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-07.pdf` | 1916-05-04 / seq7 / printed7 |
| IMG-0538 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-08.pdf` | 1916-05-04 / seq8 / printed8 |
| IMG-0539 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-09.pdf` | 1916-05-04 / seq9 / printed9 |
| IMG-0540 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-04-page-10.pdf` | 1916-05-04 / seq10 / printed10 |
| IMG-0541 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-01.pdf` | 1916-05-11 / seq1 / printed1 |
| IMG-0542 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-02.pdf` | 1916-05-11 / seq2 / printed2 |
| IMG-0543 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-03.pdf` | 1916-05-11 / seq3 / printed3 |
| IMG-0544 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-04.pdf` | 1916-05-11 / seq4 / printed4 |
| IMG-0545 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-05.pdf` | 1916-05-11 / seq5 / printed5 |
| IMG-0546 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-06.pdf` | 1916-05-11 / seq6 / printed6 |
| IMG-0547 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-07.pdf` | 1916-05-11 / seq7 / printed7 |
| IMG-0548 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-08.pdf` | 1916-05-11 / seq8 / printed8 |
| IMG-0549 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-09.pdf` | 1916-05-11 / seq9 / printed9 |
| IMG-0550 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-11-page-10.pdf` | 1916-05-11 / seq10 / printed10 |
| IMG-0551 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-18-page-01.pdf` | 1916-05-18 / seq1 / printed1 |
| IMG-0552 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-18-page-02.pdf` | 1916-05-18 / seq2 / printed2 |
| IMG-0553 | `newspapers/oregon-city-courier/1916-pages-106-180/1916-05-18-page-03.pdf` | 1916-05-18 / seq3 / printed3 |

## 1916 first monthly Courier issues — S-133 / E-119

58 unchanged original page PDFs, retrieved and visually reviewed 28 August 2026. Original `seq-N.pdf` filenames, exact URLs, SHA-256 hashes, printed dates/pages and page notes are in `newspapers/oregon-city-courier/1916-first-monthly-june-december/manifest.json`. No image transformation was committed.

| Media ID | Repository file | Date / archive sequence / printed page |
| --- | --- | --- |
| IMG-0554 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-01.pdf` | 1916-06-01 / seq1 / printed1 |
| IMG-0555 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-02.pdf` | 1916-06-01 / seq2 / printed2 |
| IMG-0556 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-03.pdf` | 1916-06-01 / seq3 / printed3 |
| IMG-0557 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-04.pdf` | 1916-06-01 / seq4 / printed4 |
| IMG-0558 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-05.pdf` | 1916-06-01 / seq5 / printed5 |
| IMG-0559 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-06.pdf` | 1916-06-01 / seq6 / printed6 |
| IMG-0560 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-07.pdf` | 1916-06-01 / seq7 / printed7 |
| IMG-0561 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-06-01-page-08.pdf` | 1916-06-01 / seq8 / printed8 |
| IMG-0562 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-01.pdf` | 1916-07-06 / seq1 / printed1 |
| IMG-0563 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-02.pdf` | 1916-07-06 / seq2 / printed2 |
| IMG-0564 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-03.pdf` | 1916-07-06 / seq3 / printed3 |
| IMG-0565 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-04.pdf` | 1916-07-06 / seq4 / printed4 |
| IMG-0566 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-05.pdf` | 1916-07-06 / seq5 / printed5 |
| IMG-0567 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-06.pdf` | 1916-07-06 / seq6 / printed6 |
| IMG-0568 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-07.pdf` | 1916-07-06 / seq7 / printed7 |
| IMG-0569 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-07-06-page-08.pdf` | 1916-07-06 / seq8 / printed8 |
| IMG-0570 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-01.pdf` | 1916-08-03 / seq1 / printed1 |
| IMG-0571 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-02.pdf` | 1916-08-03 / seq2 / printed2 |
| IMG-0572 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-03.pdf` | 1916-08-03 / seq3 / printed3 |
| IMG-0573 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-04.pdf` | 1916-08-03 / seq4 / printed4 |
| IMG-0574 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-05.pdf` | 1916-08-03 / seq5 / printed5 |
| IMG-0575 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-06.pdf` | 1916-08-03 / seq6 / printed6 |
| IMG-0576 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-07.pdf` | 1916-08-03 / seq7 / printed7 |
| IMG-0577 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-08-03-page-08.pdf` | 1916-08-03 / seq8 / printed8 |
| IMG-0578 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-01.pdf` | 1916-09-07 / seq1 / printed1 |
| IMG-0579 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-02.pdf` | 1916-09-07 / seq2 / printed2 |
| IMG-0580 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-03.pdf` | 1916-09-07 / seq3 / printed3 |
| IMG-0581 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-04.pdf` | 1916-09-07 / seq4 / printed4 |
| IMG-0582 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-05.pdf` | 1916-09-07 / seq5 / printed5 |
| IMG-0583 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-06.pdf` | 1916-09-07 / seq6 / printed6 |
| IMG-0584 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-07.pdf` | 1916-09-07 / seq7 / printed7 |
| IMG-0585 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-09-07-page-08.pdf` | 1916-09-07 / seq8 / printed8 |
| IMG-0586 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-01.pdf` | 1916-10-05 / seq1 / printed1 |
| IMG-0587 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-02.pdf` | 1916-10-05 / seq2 / printed2 |
| IMG-0588 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-03.pdf` | 1916-10-05 / seq3 / printed3 |
| IMG-0589 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-04.pdf` | 1916-10-05 / seq4 / printed4 |
| IMG-0590 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-05.pdf` | 1916-10-05 / seq5 / printed5 |
| IMG-0591 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-06.pdf` | 1916-10-05 / seq6 / printed6 |
| IMG-0592 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-07.pdf` | 1916-10-05 / seq7 / printed7 |
| IMG-0593 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-10-05-page-08.pdf` | 1916-10-05 / seq8 / printed8 |
| IMG-0594 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-01.pdf` | 1916-11-02 / seq1 / printed1 |
| IMG-0595 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-02.pdf` | 1916-11-02 / seq2 / printed2 |
| IMG-0596 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-03.pdf` | 1916-11-02 / seq3 / printed3 |
| IMG-0597 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-04.pdf` | 1916-11-02 / seq4 / printed4 |
| IMG-0598 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-05.pdf` | 1916-11-02 / seq5 / printed5 |
| IMG-0599 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-06.pdf` | 1916-11-02 / seq6 / printed6 |
| IMG-0600 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-07.pdf` | 1916-11-02 / seq7 / printed7 |
| IMG-0601 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-08.pdf` | 1916-11-02 / seq8 / printed8 |
| IMG-0602 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-09.pdf` | 1916-11-02 / seq9 / printed9 |
| IMG-0603 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-11-02-page-10.pdf` | 1916-11-02 / seq10 / printed10 |
| IMG-0604 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-01.pdf` | 1916-12-07 / seq1 / printed1 |
| IMG-0605 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-02.pdf` | 1916-12-07 / seq2 / printed2 |
| IMG-0606 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-03.pdf` | 1916-12-07 / seq3 / printed3 |
| IMG-0607 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-04.pdf` | 1916-12-07 / seq4 / printed4 |
| IMG-0608 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-05.pdf` | 1916-12-07 / seq5 / printed5 |
| IMG-0609 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-06.pdf` | 1916-12-07 / seq6 / printed6 |
| IMG-0610 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-07.pdf` | 1916-12-07 / seq7 / printed7 |
| IMG-0611 | `newspapers/oregon-city-courier/1916-first-monthly-june-december/1916-12-07-page-08.pdf` | 1916-12-07 / seq8 / printed8 |

## 1917 Courier first-issue monthly sample — S-134 / E-120

All 96 unchanged original page PDFs are **VISUALLY VERIFIED**. Exact source URLs and SHA-256 hashes are preserved in `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/manifest.json`. This is a sampling pass only.

| Media ID | Repository file | Issue / sequence / status |
| --- | --- | --- |
| IMG-0612 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-01.pdf` | 1917-01-04 / seq1 / visually verified |
| IMG-0613 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-02.pdf` | 1917-01-04 / seq2 / visually verified |
| IMG-0614 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-03.pdf` | 1917-01-04 / seq3 / visually verified |
| IMG-0615 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-04.pdf` | 1917-01-04 / seq4 / visually verified |
| IMG-0616 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-05.pdf` | 1917-01-04 / seq5 / visually verified |
| IMG-0617 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-06.pdf` | 1917-01-04 / seq6 / visually verified |
| IMG-0618 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-07.pdf` | 1917-01-04 / seq7 / visually verified |
| IMG-0619 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-01-04-seq-08.pdf` | 1917-01-04 / seq8 / visually verified |
| IMG-0620 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-01.pdf` | 1917-02-01 / seq1 / visually verified |
| IMG-0621 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-02.pdf` | 1917-02-01 / seq2 / visually verified |
| IMG-0622 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-03.pdf` | 1917-02-01 / seq3 / visually verified |
| IMG-0623 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-04.pdf` | 1917-02-01 / seq4 / visually verified |
| IMG-0624 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-05.pdf` | 1917-02-01 / seq5 / visually verified |
| IMG-0625 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-06.pdf` | 1917-02-01 / seq6 / visually verified |
| IMG-0626 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-07.pdf` | 1917-02-01 / seq7 / visually verified |
| IMG-0627 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-02-01-seq-08.pdf` | 1917-02-01 / seq8 / visually verified |
| IMG-0628 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-01.pdf` | 1917-03-01 / seq1 / visually verified |
| IMG-0629 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-02.pdf` | 1917-03-01 / seq2 / visually verified |
| IMG-0630 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-03.pdf` | 1917-03-01 / seq3 / visually verified |
| IMG-0631 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-04.pdf` | 1917-03-01 / seq4 / visually verified |
| IMG-0632 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-05.pdf` | 1917-03-01 / seq5 / visually verified |
| IMG-0633 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-06.pdf` | 1917-03-01 / seq6 / visually verified |
| IMG-0634 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-07.pdf` | 1917-03-01 / seq7 / visually verified |
| IMG-0635 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-08.pdf` | 1917-03-01 / seq8 / visually verified |
| IMG-0636 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-09.pdf` | 1917-03-01 / seq9 / visually verified |
| IMG-0637 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-03-01-seq-10.pdf` | 1917-03-01 / seq10 / visually verified |
| IMG-0638 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-01.pdf` | 1917-04-05 / seq1 / visually verified |
| IMG-0639 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-02.pdf` | 1917-04-05 / seq2 / visually verified |
| IMG-0640 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-03.pdf` | 1917-04-05 / seq3 / visually verified |
| IMG-0641 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-04.pdf` | 1917-04-05 / seq4 / visually verified |
| IMG-0642 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-05.pdf` | 1917-04-05 / seq5 / visually verified |
| IMG-0643 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-06.pdf` | 1917-04-05 / seq6 / visually verified |
| IMG-0644 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-07.pdf` | 1917-04-05 / seq7 / visually verified |
| IMG-0645 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-04-05-seq-08.pdf` | 1917-04-05 / seq8 / visually verified |
| IMG-0646 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-01.pdf` | 1917-05-03 / seq1 / visually verified |
| IMG-0647 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-02.pdf` | 1917-05-03 / seq2 / visually verified |
| IMG-0648 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-03.pdf` | 1917-05-03 / seq3 / visually verified |
| IMG-0649 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-04.pdf` | 1917-05-03 / seq4 / visually verified |
| IMG-0650 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-05.pdf` | 1917-05-03 / seq5 / visually verified |
| IMG-0651 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-06.pdf` | 1917-05-03 / seq6 / visually verified |
| IMG-0652 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-07.pdf` | 1917-05-03 / seq7 / visually verified |
| IMG-0653 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-05-03-seq-08.pdf` | 1917-05-03 / seq8 / visually verified |
| IMG-0654 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-01.pdf` | 1917-06-07 / seq1 / visually verified |
| IMG-0655 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-02.pdf` | 1917-06-07 / seq2 / visually verified |
| IMG-0656 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-03.pdf` | 1917-06-07 / seq3 / visually verified |
| IMG-0657 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-04.pdf` | 1917-06-07 / seq4 / visually verified |
| IMG-0658 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-05.pdf` | 1917-06-07 / seq5 / visually verified |
| IMG-0659 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-06.pdf` | 1917-06-07 / seq6 / visually verified |
| IMG-0660 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-07.pdf` | 1917-06-07 / seq7 / visually verified |
| IMG-0661 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-06-07-seq-08.pdf` | 1917-06-07 / seq8 / visually verified |
| IMG-0662 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-01.pdf` | 1917-07-05 / seq1 / visually verified |
| IMG-0663 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-02.pdf` | 1917-07-05 / seq2 / visually verified |
| IMG-0664 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-03.pdf` | 1917-07-05 / seq3 / visually verified |
| IMG-0665 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-04.pdf` | 1917-07-05 / seq4 / visually verified |
| IMG-0666 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-05.pdf` | 1917-07-05 / seq5 / visually verified |
| IMG-0667 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-06.pdf` | 1917-07-05 / seq6 / visually verified |
| IMG-0668 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-07.pdf` | 1917-07-05 / seq7 / visually verified |
| IMG-0669 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-07-05-seq-08.pdf` | 1917-07-05 / seq8 / visually verified |
| IMG-0670 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-01.pdf` | 1917-08-02 / seq1 / visually verified |
| IMG-0671 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-02.pdf` | 1917-08-02 / seq2 / visually verified |
| IMG-0672 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-03.pdf` | 1917-08-02 / seq3 / visually verified |
| IMG-0673 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-04.pdf` | 1917-08-02 / seq4 / visually verified |
| IMG-0674 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-05.pdf` | 1917-08-02 / seq5 / visually verified |
| IMG-0675 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-08-02-seq-06.pdf` | 1917-08-02 / seq6 / visually verified |
| IMG-0676 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-01.pdf` | 1917-09-06 / seq1 / visually verified |
| IMG-0677 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-02.pdf` | 1917-09-06 / seq2 / visually verified |
| IMG-0678 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-03.pdf` | 1917-09-06 / seq3 / visually verified |
| IMG-0679 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-04.pdf` | 1917-09-06 / seq4 / visually verified |
| IMG-0680 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-05.pdf` | 1917-09-06 / seq5 / visually verified |
| IMG-0681 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-06.pdf` | 1917-09-06 / seq6 / visually verified |
| IMG-0682 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-07.pdf` | 1917-09-06 / seq7 / visually verified |
| IMG-0683 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-09-06-seq-08.pdf` | 1917-09-06 / seq8 / visually verified |
| IMG-0684 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-01.pdf` | 1917-10-04 / seq1 / visually verified |
| IMG-0685 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-02.pdf` | 1917-10-04 / seq2 / visually verified |
| IMG-0686 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-03.pdf` | 1917-10-04 / seq3 / visually verified |
| IMG-0687 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-04.pdf` | 1917-10-04 / seq4 / visually verified |
| IMG-0688 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-05.pdf` | 1917-10-04 / seq5 / visually verified |
| IMG-0689 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-06.pdf` | 1917-10-04 / seq6 / visually verified |
| IMG-0690 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-07.pdf` | 1917-10-04 / seq7 / visually verified |
| IMG-0691 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-10-04-seq-08.pdf` | 1917-10-04 / seq8 / visually verified |
| IMG-0692 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-01.pdf` | 1917-11-01 / seq1 / visually verified |
| IMG-0693 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-02.pdf` | 1917-11-01 / seq2 / visually verified |
| IMG-0694 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-03.pdf` | 1917-11-01 / seq3 / visually verified |
| IMG-0695 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-04.pdf` | 1917-11-01 / seq4 / visually verified |
| IMG-0696 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-05.pdf` | 1917-11-01 / seq5 / visually verified |
| IMG-0697 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-06.pdf` | 1917-11-01 / seq6 / visually verified |
| IMG-0698 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-07.pdf` | 1917-11-01 / seq7 / visually verified |
| IMG-0699 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-11-01-seq-08.pdf` | 1917-11-01 / seq8 / visually verified |
| IMG-0700 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-01.pdf` | 1917-12-06 / seq1 / visually verified |
| IMG-0701 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-02.pdf` | 1917-12-06 / seq2 / visually verified |
| IMG-0702 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-03.pdf` | 1917-12-06 / seq3 / visually verified |
| IMG-0703 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-04.pdf` | 1917-12-06 / seq4 / visually verified |
| IMG-0704 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-05.pdf` | 1917-12-06 / seq5 / visually verified |
| IMG-0705 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-06.pdf` | 1917-12-06 / seq6 / visually verified |
| IMG-0706 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-07.pdf` | 1917-12-06 / seq7 / visually verified |
| IMG-0707 | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/1917-12-06-seq-08.pdf` | 1917-12-06 / seq8 / visually verified |

## IMG-0708 — Oregon City Courier, 4 October 1907, page 3
File: `newspapers/oregon-city-courier/1907-1908-surber-justin-review/1907-10-04-seq-03.pdf`
Original uploaded filename: `501 Main st (A. J. Surber) Oregon City courier., October 04, 1907, Page 3, Image 3.pdf`
Provenance: user-supplied archival PDF; unchanged copy, one page.
Source: `S-135`; evidence: E-121, E-123.
Archive locator: https://oregonnews.uoregon.edu/lccn/sn00063698/1907-10-04/ed-1/seq-3.pdf
SHA-256: `beb6866b1046249b86eb0548d0b6963909be706d35a6c60ed63a705974bc679e`
Review: full supplied page VISUALLY VERIFIED on 2026-08-28; enlarged crops used for small print. Live archive locator not successfully retrieved in this task.
Interpretation: `evidence/source-captures/1907-1908-surber-justin-main-visual-review.md`.

## IMG-0709 — Oregon City Courier, 13 December 1907, page 3
File: `newspapers/oregon-city-courier/1907-1908-surber-justin-review/1907-12-13-seq-03.pdf`
Original uploaded filename: `5th & Main (Justin & Hitchman) Oregon City courier., December 13, 1907, Page 3, Image 3.pdf`
Provenance: user-supplied archival PDF; unchanged copy, one page.
Source: `S-136`; evidence: E-122.
Archive locator: https://oregonnews.uoregon.edu/lccn/sn00063698/1907-12-13/ed-1/seq-3.pdf
SHA-256: `3c42bc92aca99f178e60e76c0430571b1aaee47869fd26e52b17fd614be0ae50`
Review: full supplied page VISUALLY VERIFIED on 2026-08-28; enlarged crops used for small print. Live archive locator not successfully retrieved in this task.
Interpretation: `evidence/source-captures/1907-1908-surber-justin-main-visual-review.md`.

## IMG-0710 — Oregon City Courier, 18 September 1908, image 9
File: `newspapers/oregon-city-courier/1907-1908-surber-justin-review/1908-09-18-seq-09.pdf`
Original uploaded filename: `5th & Main (Justin & Hitchman) Oregon City courier., September 18, 1908, Image 9.pdf`
Provenance: user-supplied archival PDF; unchanged copy, one page.
Source: `S-137`; evidence: E-121, E-122, E-123.
Archive locator: https://oregonnews.uoregon.edu/lccn/sn00063698/1908-09-18/ed-1/seq-9.pdf
SHA-256: `62ce8e70f6e13a3614bc85eae7c3071a33dd83f36eda9973bf1ba75f4b7fe11a`
Review: full supplied page VISUALLY VERIFIED on 2026-08-28; enlarged crops used for small print. Live archive locator not successfully retrieved in this task.
Interpretation: `evidence/source-captures/1907-1908-surber-justin-main-visual-review.md`.

## IMG-0711 — Undated Sanborn-style Main/Water/Fifth/Sixth detail 01
File: `maps/images/sanborn-main-water-5th-6th-detail-01.jpg`
Type: Map crop / screenshot.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-146` / `E-131`.
Related buildings: `B-001`, `B-002`, `B-003`.
Dimensions: 1206 × 1175. SHA-256: `246303efbd50cb8ce1cf9a822289b703a95925d3204c13f67c0de0558bb08bd1`.
Limits: Exact Sanborn edition, sheet, source URL, and crop date unresolved; visible labels are not assigned to a year from the crop alone.

## IMG-0712 — Undated Sanborn-style Main/Water/Fifth/Sixth detail 02
File: `maps/images/sanborn-main-water-5th-6th-detail-02.jpg`
Type: Map crop / screenshot.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-146` / `E-131`.
Related buildings: `B-001`, `B-002`, `B-003`.
Dimensions: 1206 × 1011. SHA-256: `7e050014adbe9a040eca2ea3d10186e177775d036c1a2a01d52423ea9ae2f2c6`.
Limits: Exact Sanborn edition, sheet, source URL, and crop date unresolved; visible labels are not assigned to a year from the crop alone.

## IMG-0713 — orcity.org Sanborn-style mobile screenshot
File: `maps/images/sanborn-main-water-5th-6th-orcity-screenshot.jpg`
Type: Mobile map screenshot with visible `orcity.org` header.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-146` / `E-131`.
Related buildings: `B-001`, `B-002`, `B-003`.
Dimensions: 588 × 1280. SHA-256: `aa52081c0c67616e5c40036f3b3c1ff9a3c631c134aa8bde973a99b41bafabbe`.
Limits: The screenshot helps identify the source domain but does not preserve the exact URL, map edition, or sheet.

## IMG-0714 — George A. Harding, 511 Main, 10 January 1911
File: `newspapers/morning-enterprise/1911-01-10-george-harding-druggist-511-main-screenshot.png`
Original/legacy repository path: `newspapers/oregon-city-courier/c1915-1916-harding-druggist-511-main.png`.
Type: Primary newspaper screenshot.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-143` / `E-128`.
Related building/business/person: `B-003`; `BUS-007`; `P-001`.
Visible source header: *Morning Enterprise*, 10 January 1911, page 3, image 3. Advertisement prints George A. Harding, Druggist, 511 Main Street, “Next Door to Postoffice.”
Dimensions: 1588 × 1446. SHA-256: `14793fe7f2e1ec28fe139edd2c8c820219966c1b46a8c95ed9a0d0986c628c26`.
Correction: The legacy filename's c.1915–1916 *Courier* description is superseded by the visible source header.

## IMG-0715 — Unnamed baking and coffee shop, 509 Main, 5 December 1965
File: `newspapers/oregonian/1965-12-05-509-main-baking-coffee-shop-for-sale.png`
Original/legacy repository path: `newspapers/other/undated-509-main-coffee-shop.png`.
Type: Primary newspaper classified screenshot.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-145` / `E-130`.
Related building: `B-003` / 509 Main address context.
Visible source header: *The Oregonian*, 5 December 1965. The classified offers an unnamed baking and coffee shop for sale through 509 Main St., Oregon City.
Dimensions: 1760 × 1036. SHA-256: `83480afc134861864ef99f8fc5925c2e548baecb78b7de4901c74f3d5bc0cff3`.
Limits: No Dixon identity, completed sale, seller, buyer, or property ownership is inferred.

## IMG-0716 — Dixon's Pastry Shop, 509 Main, 10 June 1964
File: `newspapers/oregonian/1964-06-10-dixons-pastry-shop-509-main.png`
Original/legacy repository path: `newspapers/the-amplifier/1949-05-06-dixons-pastry-shop-519-main.png`.
Type: Primary newspaper classified screenshot.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-144` / `E-129`.
Related building/business: `B-003`; `BUS-023`.
Visible source header: *The Oregonian*, 10 June 1964. The advertisement directly prints Dixon's Pastry Shop, 509 Main St., Oregon City.
Dimensions: 1252 × 1096. SHA-256: `a4fc5d92bc7ded91bcc44418dffe70ba610fd0eddef8937143d2620ee4bc0bb7`.
Correction: The legacy path's *Amplifier*, 1949, and 519 Main labels are superseded by the visible header and text.

## IMG-0717–IMG-0721 — 1915–1916 Polk directory review pages
Type: Authenticated FamilySearch directory-page images assembled from Deep Zoom tiles.
Status: `committed`; visually reviewed during `1915-D01` and reconfirmed in the 30 August 2026 media audit.
Source/evidence: `S-132` / `E-118`.
Provenance and image locators: `records/directories/1915-1916-polk-oregon-city/README.md`.

| Media ID | Repository file | Printed page / scope | SHA-256 |
| --- | --- | --- | --- |
| IMG-0717 | `records/directories/1915-1916-polk-oregon-city/1915-1916-polk-oregon-city-p260-familysearch-image400.jpg` | 260 / Oregon City A–F | `b6620cc1ff6335ba41ec2acd8eb255de5fb118f13e8370bf95dede7baf50a3ee` |
| IMG-0718 | `records/directories/1915-1916-polk-oregon-city/1915-1916-polk-oregon-city-p261-familysearch-image401.jpg` | 261 / Oregon City F–M | `dfb332b2262bc5f3472753cc1540ca77c1db699f40dcf98e9f1e10c4eb2ff6e7` |
| IMG-0719 | `records/directories/1915-1916-polk-oregon-city/1915-1916-polk-oregon-city-p262-familysearch-image402.jpg` | 262 / Oregon City M–Y | `debc8dc3373f6f2b6774da3b6baee89d69575897b7c3af8f8b17153ff61644bf` |
| IMG-0720 | `records/directories/1915-1916-polk-oregon-city/1915-1916-polk-undertakers-familysearch-image291.jpg` | 1641 / Undertakers begins | `d3cd3044377f08e946f54cac0abb7e267bd59394f2805d227476f0bff30f2462` |
| IMG-0721 | `records/directories/1915-1916-polk-oregon-city/1915-1916-polk-undertakers-contd-p1642-familysearch-image292.jpg` | 1642 / Oregon City—Holman R. L. | `d265924650f1cc3452092140491311c70bea8a5c30306ab0cf1aae5b44973911` |

## IMG-0722 — Tom Keene cigar advertising-sign crop
File: `media/photos/early-main-street/IMG-0722_tom-keene-cigar-sign-crop-reported-1908.jpg`
Original filename/path: `research-inbox/tom keene cigars 1908 photo.jpg`.
Type: Historic-photo crop / advertising sign.
Status: `committed`; moved from staging and visually reviewed 30 August 2026; provenance unresolved.
Visible content: a diamond-shaped “Tom Keene” cigar advertising sign.
Dimensions: 181 × 218. SHA-256: `a85ec01b02c5748a47aac1e635a06023afd3f035a20b5e52ee9f39f94a1a6b55`.
Limits: “1908” is retained only as an assertion from the former filename. The full photograph, location, date, photographer, collection, and source are unknown. This crop does not establish a Tom Keene business or occupant at any project address.
Audit: `evidence/source-captures/media-reconciliation-uncataloged-images-2026-08-30.md`.

## IMG-0723 — B. J. Staats Hardware at 516 Main in December 1919 snow
File: `media/photos/early-main-street/IMG-0723_1919-12-516-main-bj-staats-hardware-snow.jpg`
Original uploaded filename: `516 Main B.J. Staats hardware Store in 22 inches of snow 1919.jpg`.
Type: Historic photograph / user-supplied digital access copy of institutional negative.
Status: `committed`; visually reviewed 30 August 2026.
Source/evidence: `S-147` / `E-132`.
Catalog: Clackamas County Historical Society, object `2008.008.004.169`; other number `Cochran 169`; medium `Negative`; negative location `Society Collection`.
Catalog title/date/place: “516 Main Street, 22 inches of Snow 1919”; December 1919; Oregon City, Clackamas County, Oregon.
Visible content: storefront fascia **B. J. Staats Hardw…**; **Closing Out Sale** and **Big Sale** signs; deep snow; at least two unidentified people; Clackamas County Historical Society watermark.
Dimensions: 2048 × 1213. SHA-256: `c3cdabf87560ca79fa919a23b081407c5d069cd0fd196280253e39df838c8cac`.
Rights: not supplied; watermarked access copy; no public-domain assertion.
Limits: The catalog metadata—not a visible street number—supplies 516 Main, December 1919, and 22 inches. The photograph does not establish the exact exposure day, expanded initials, business/building ownership, completed sale, closing date, or survival of the pictured fabric.
Record: `evidence/source-captures/1919-516-main-bj-staats-hardware-snow-photo.md`.

## IMG-0724 — George Harding Drug Store cataloged at 505 Main, 1880/1880s
File: `media/photos/early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg`
Original uploaded filename: `George Harding Drug Store 1880 (Clackamas County Historical Society).jpg`.
Type: Historic photograph crop / user-supplied digital access copy.
Status: `committed`; visually reviewed 30 August 2026; live catalog record reviewed.
Source/evidence: `S-148` / `E-133`.
Catalog: Clackamas County Historical Society object `2008.008.046.080`; other number `Culp, Ed 80`; negative in Society Collection.
Catalog title/location: **George Harding Drug Store - 505 Main Street**, Oregon City.
Catalog date conflict: structured date made `1880`; image caption `1880s`.
Visible content: cropped upper storefront with **GEO. A. HARDING** or closely equivalent fascia lettering; no visible street number.
Dimensions: 400 × 400. SHA-256: `532b58185f876a7651d578be9cb39f94a414d4daaa2169438cae1329ed99fe61`.
Rights: not supplied; no public-domain assertion.
Limits: The institution supplies the business, 505 location, and date wording. Because formal citywide numbering is documented in 1906, 505 may be retrospective for the 1880/1880s image. No present-building, Harding Building, title, or continuity conclusion.
Record: `evidence/source-captures/1880-1910-505-main-harding-young-photo-records.md`.

## IMG-0726 — Downtown oblique aerial reproduced in the 1926 municipal report
File/container: `records/municipal/annual-reports/1926-municipal-activities-report.pdf`, **PDF page 4**, lower image.
Type: Historic aerial photograph reproduced within a municipal report; no separate raster derivative committed.
Source: `S-159`; report transmittal January 25, 1927. **Exposure date unknown**; the report year is not a verified photograph date.
Status: `committed` within the original PDF; visually reviewed 1 September 2026, including a higher-resolution render.
Caption identifies an airplane view of Oregon City from Fourth Street north toward Sixteenth Street. No photographer or original negative ID established. The general city map above is a different image, not a Sanborn sheet or a photograph-date source.
Limits: Individual 501/503/505 roofs and boundaries not conclusively traced; no construction/removal date, measurement or named tenant inferred. Related buildings are research targets only, not established image assignments.
Integrity: container SHA-256 `433753736a08a225e8437cea6b91123d1e867481703b87ea93d657e9dd11c790`.
Rights: original-photo provenance and rights not independently established; preserved as part of the official report.
Review: `evidence/source-captures/1926-municipal-report-visual-review-2026-09-01.md`. Other report illustrations remain preserved in that PDF with page locators in the review; standalone-raster counts are unchanged.

## IMG-0725 — George Young's Second Hand Store at 505 Main, 1910
File: `media/photos/early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg`
Original uploaded filename: `George Young's Second Hand Store 1910 (Clackamas County Historical Society).jpg`.
Type: Historic photograph / user-supplied digital access copy.
Status: `committed`; visually reviewed 30 August 2026; live catalog record reviewed.
Source/evidence: `S-149` / `E-134`.
Catalog: Clackamas County Historical Society object `MOT:P-391` (institutional photo ID, not an archive person ID); medium `Photographic Paper`.
Catalog date/description: `1910`; George Young's Second Hand Store, 505 Main; George Young identified as the man in the white shirt without a coat.
Visible content: **505** above the entrance; **Young's Secondhand Store** on both windows; four men; tools/second-hand merchandise; Clackamas County Historical Society watermark.
Dimensions: 2048 × 1324. SHA-256: `875329cbd74094a80fc49b4e470b5b70e2dda48dc66594508240facdf2c75c04`.
Rights: not supplied; watermarked access copy; no public-domain assertion.
Limits: Other people, property/business ownership, exact move day, building name, uninterrupted operation, and survival of the photographed structure are unresolved.
Record: `evidence/source-captures/1880-1910-505-main-harding-young-photo-records.md`.

## IMG-0727 — Banner-Courier, 8 June 1922, page 10, Quality Restaurant at 427 Main
File: `newspapers/banner-courier/1922-06-08-page-10-quality-restaurant-427-main.pdf`
Type: Original full-page newspaper PDF; source-page image retained within PDF.
Status: `committed`; **VISUALLY VERIFIED**, targeted Quality Restaurant advertisement and separate merchant-roster entries; not a certification of reading every column.
Provenance: Historic Oregon Newspapers direct download, https://oregonnews.uoregon.edu/lccn/sn00063699/1922-06-08/ed-1/seq-10/; working download filename `banner-1922-06-08-p10.pdf`.
Source/evidence: `S-141` / `E-179`.
Integrity: SHA-256 `66bb4b5b6fb0c6d72a6c7cee41e21194e70f53bd6684c55c47773b5b4a7d06bf`; 524294 bytes.
Limits: Quality Restaurant directly advertises 427 Main St., phone 517. No proprietor is printed in the advertisement.
Rights: 1922 US newspaper publication; archival access copy. No separate raster derivative added.

## IMG-0728 — Banner-Courier, 17 August 1922, page 2, Quality Cafe roster
File: `newspapers/banner-courier/1922-08-17-page-2-quality-cafe-roster.pdf`
Type: Original full-page newspaper PDF; source-page image retained within PDF.
Status: `committed`; **VISUALLY VERIFIED**, targeted Quality Cafe row in the business roster; not a certification of reading every column.
Provenance: Historic Oregon Newspapers direct download, https://oregonnews.uoregon.edu/lccn/sn00063699/1922-08-17/ed-1/seq-2/; working download filename `banner-1922-08-17-p2.pdf`.
Source/evidence: `S-141` / `E-181`.
Integrity: SHA-256 `1a7dd10757bbb0b0534f5f0e3bd3ba51355d63248a10872b2fe4febabbeb0550`; 579436 bytes.
Limits: The roster prints QUALITY CAFE without proprietor, phone or street address. It does not prove identity with either Quality Restaurant record.
Rights: 1922 US newspaper publication; archival access copy. No separate raster derivative added.

## IMG-0729 — Morning Oregonian, 17 August 1922, George Newton Quality restaurant fire-survival dinner
File: `newspapers/oregonian/1922-08-17-page-4-newton-quality-firemen-dinner.pdf`
Type: Original full-page newspaper PDF; source-page image retained within PDF.
Status: `committed`; **VISUALLY VERIFIED**, targeted Firemen Are Dinner Guests article; not a certification of reading every column.
Provenance: Historic Oregon Newspapers direct download, https://oregonnews.uoregon.edu/lccn/sn83025138/1922-08-17/ed-1/seq-4/; working download filename `oregonian-1922-08-17-p4.pdf`.
Source/evidence: `S-200` / `E-180`.
Integrity: SHA-256 `4ea60d3679b88edd1c24896a4a521e62370fd21fdd3f10d6a65375b3b9819f74`; 770099 bytes.
Limits: Names George Newton as Quality restaurant proprietor and reports firefighters saved his restaurant during the recent Fifth Street fire. The August 16 dateline and last-evening wording place the dinner on August 15. No address or phone. Its wording closely parallels the Enterprise account; separate publication is not proof of an independent witness.
Rights: 1922 US newspaper publication; archival access copy. No separate raster derivative added.

## IMG-0730 — Banner-Courier, 17 August 1922, Newton restaurant across the way from the laundry
File: `newspapers/banner-courier/1922-08-17-page-8-newton-quality-across-laundry.pdf`
Type: Original full-page newspaper PDF; source-page image retained within PDF.
Status: `committed`; **VISUALLY VERIFIED**, targeted Firemen Honored with Banquet at the Quality article; not a certification of reading every column.
Provenance: Historic Oregon Newspapers direct download, https://oregonnews.uoregon.edu/lccn/sn00063699/1922-08-17/ed-1/seq-8/; working download filename `banner-1922-08-17-p8.pdf`.
Source/evidence: `S-201` / `E-180`.
Integrity: SHA-256 `12e83eb2f00e5213f791670920797cf50aefa1c1a17d0ec926916aab219857f2`; 662444 bytes.
Limits: Names George Newton as proprietor and says the fire destroyed Oregon City Laundry and threatened his restaurant across the way. Tuesday-evening banquet is consistent with August 15. No numbered address or phone. John Fuson/Frison and Ariel Newton are mentioned in a marriage/gift account; no kinship between Ariel and George is stated.
Rights: 1922 US newspaper publication; archival access copy. No separate raster derivative added.

## IMG-0731 — Oregon City Enterprise, 18 August 1922, Newton Quality restaurant banquet
File: `newspapers/oregon-city-enterprise/1922-08-18-page-3-newton-quality-firemen-banquet.pdf`
Type: Original full-page newspaper PDF; source-page image retained within PDF.
Status: `committed`; **VISUALLY VERIFIED**, targeted Firemen Are Feted by Local Restaurant Man article; not a certification of reading every column.
Provenance: Historic Oregon Newspapers direct download, https://oregonnews.uoregon.edu/lccn/sn00063700/1922-08-18/ed-1/seq-3/; working download filename `enterprise-1922-08-18-p3.pdf`.
Source/evidence: `S-202` / `E-180`.
Integrity: SHA-256 `a668b95e9ba4ce47f8fcec362fa2037a2aa6dbe68435d07c903071378d0a2b63`; 840717 bytes.
Limits: Names George Newton as Quality restaurant proprietor and reports the restaurant was saved during the Fifth Street fire; banquet Tuesday evening. No address or phone. Opening closely parallels the Oregonian dispatch; do not count the two as independent witnesses. John Frison and Ariel Newton marriage context does not establish kinship to George.
Rights: 1922 US newspaper publication; archival access copy. No separate raster derivative added.

## IMG-0732 — CCHS P-1469, 1890 Main Street flood at 6th and Main
File: `media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg`  
Type: Historic photograph / institutional public derivative  
Status: `committed`  
Source: `S-203`; evidence `E-183`  
Holding institution / object: Clackamas County Historical Society, **P-1469**  
Catalog title: **1890 Flood - Oregon City Main Street**  
Catalog description: **Oregon City Main Street, 6th and Main, looking southwest.  Unidentified people.  Flooding.  Debris.**  
Date made: **1890**  
Catalog entry UUID: `de65a6a0-9b1e-11eb-b3ef-53e7205a00b4`  
CatalogIt media UUID: `3c630c60-b5ce-11f0-b5a3-a3a9be51ef91`  
Public catalog page: https://hub.catalogit.app/clackamas-county-historical-society/folder/entry/1890-flood-oregon-city-main-street-1  
Recovered derivative: https://d8e7jbdw4fu0e.cloudfront.net/4813/3c630c60-b5ce-11f0-b5a3-a3a9be51ef91-vdUeg2T.lg@2x.jpg  
Dimensions: 2400 × 1745  
SHA-256: `767915990ca00e17316f75ba2db51c5e0e2f36a2e36555020cf9caade4889e74`  
File size: 569359 bytes  
Provenance note: the temporary steward-upload staging chunks were incomplete and could not reconstruct a valid JPEG. This committed file is the exact current CCHS public high-resolution derivative for P-1469; byte identity to the earlier steward upload is not claimed.  
Historical-use limit: the institutional record directly supplies the 6th/Main southwest location context, but this image alone does not assign an exact 501/503/505 facade or prove physical-building continuity.

## IMG-0733 — CCHS P-1456, 1890 flood at 6th/Main looking south
File: `media/photos/early-main-street/IMG-0733_1890-flood-6th-main-looking-south-cchs-p1456.jpg`  
Type: Historic photograph / institutional public derivative; substantive duplicate of steward-supplied P-1456 JPEG  
Status: `committed`  
Source: `S-204`; evidence `E-184`  
Holding institution / object: Clackamas County Historical Society, **P-1456**; catalog tag **Duplicate**  
Catalog title: **1890 Flood - Oregon City at 6th and Main Street Looking South**  
Catalog description: **Flood of 1890. Main Street of Oregon City looking south after water had receded. Between Alley and 6th Street. Unidentified people. (See Sanborn Map below for location of visible structures)**  
Catalog duplicate wording: **Duplicates P-1456, P-1616, P-5519, P-8885**  
Date/place: **1890; Oregon City, Clackamas County, Oregon, United States of America, North America**  
Medium note: **Photographic Paper**  
Catalog entry UUID: `de0cb130-9b1e-11eb-b3ef-53e7205a00b4`; photograph media UUID `21604e00-9b84-11eb-8d59-b7d9fd36cc45`; associated Sanborn media UUID `17d3a3c0-8613-11ed-8c19-377cb8658c65`  
Public catalog page: https://hub.catalogit.app/clackamas-county-historical-society/folder/entry/1890-flood-oregon-city-at-6th-and-main-street-looking-south-3  
Repository derivative: https://d8e7jbdw4fu0e.cloudfront.net/4813/21604e00-9b84-11eb-8d59-b7d9fd36cc45-vdUegXk.lg@2x.jpg  
Repository dimensions: 1200 × 904; SHA-256 `7355ba848b586427c139ddfe4229748a2b9c49439bc26b605874f184747c41a7`; 779120 bytes  
Original supplied filename: `1890 Flood - Oregon City at 6th and Main Street Looking South.jpg`  
Original supplied attachment: 2048 × 1543; SHA-256 `9c684f8f59ec7e78c894f1e77b70ca5094e976994a3644244b6a1ded6631e1cb`; 903423 bytes; visually inspected.  
Derivative relationship: the committed current CatalogIt derivative is not byte-identical to the supplied attachment; both represent the same P-1456 photograph and are treated as substantive duplicates. The supplied exact file signature is retained for future recognition.  
Historical-use limit: CCHS directly supplies the Main Street / looking-south / post-flood / alley-to-Sixth context, but this source alone does not assign exact 501/503/505 facades or prove building continuity. The associated Sanborn attachment is not interpreted in this record.
