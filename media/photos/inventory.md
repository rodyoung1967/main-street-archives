# Definitive Repository Photograph Inventory

Audit date: **31 August 2026**  
Scope: every committed raster file, with photographs distinguished from maps, newspaper clippings, directory pages, screenshots, and artifact images.

## Result

- **69 committed raster files** in the repository.
- **42 photographs/aerials**, all stored together under `media/photos/`.
- **27 source-document images** kept in their canonical source-class folders: 14 newspaper images, 8 record/directory images, 3 map images, and 2 artifact images.
- **All 69 raster files are recorded by exact repository path** in `media/photo-metadata-register.md`.
- **No byte-identical raster duplicates** were found.
- The three recent steward-supplied historical JPEGs are present as exact byte matches.
- No photograph is committed or currently cataloged as **514 Main Street**. The snow photograph is cataloged as **516 Main Street** and committed as `IMG-0723`.

This inventory is a repository-presence audit. It does not convert a catalog caption, filename, or visual interpretation into independent proof of an address, date, person, business, or building.

## Committed photographs

### Aerial series — 38 files

`IMG-0006` through `IMG-0043` are the Oregon City 5th-and-Main aerial/photocompare series covering 1929–2025. All 38 files and years are itemized in [`aerials/README.md`](aerials/README.md).

### Street-level and early photographs — 4 files

| Media ID | Cataloged subject/date | Canonical repository file | Status and limit |
| --- | --- | --- | --- |
| `IMG-0722` | Tom Keene cigar-sign crop; reported 1908 | [`early-main-street/IMG-0722_tom-keene-cigar-sign-crop-reported-1908.jpg`](early-main-street/IMG-0722_tom-keene-cigar-sign-crop-reported-1908.jpg) | Committed; date, place, full scene, source, and rights unresolved. |
| `IMG-0723` | B. J. Staats Hardware, cataloged 516 Main, December 1919 snow | [`early-main-street/IMG-0723_1919-12-516-main-bj-staats-hardware-snow.jpg`](early-main-street/IMG-0723_1919-12-516-main-bj-staats-hardware-snow.jpg) | Committed exact supplied-file match; museum metadata supplies address/date, while the image visibly shows the hardware fascia and closing-out/big-sale signs. The signs support a sale event, not by themselves a completed closure. |
| `IMG-0724` | George Harding Drug Store, cataloged 505 Main, 1880/1880s | [`early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg`](early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg) | Committed exact supplied-file match; structured date and caption conflict, the crop does not show 505, and the location may be retrospective. |
| `IMG-0725` | George Young's Second Hand Store, 505 Main, 1910 | [`early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg`](early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg) | Committed exact supplied-file match; storefront and 505 doorway are visible. |

## Recent supplied-file reconciliation

| Original supplied filename | SHA-256 | Canonical media ID/path | Result |
| --- | --- | --- | --- |
| `516 Main B.J. Staats hardware Store in 22 inches of snow 1919.jpg` | `c3cdabf87560ca79fa919a23b081407c5d069cd0fd196280253e39df838c8cac` | `IMG-0723` — `media/photos/early-main-street/IMG-0723_1919-12-516-main-bj-staats-hardware-snow.jpg` | Exact byte match |
| `George Harding Drug Store 1880 (Clackamas County Historical Society).jpg` | `532b58185f876a7651d578be9cb39f94a414d4daaa2169438cae1329ed99fe61` | `IMG-0724` — `media/photos/early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg` | Exact byte match |
| `George Young's Second Hand Store 1910 (Clackamas County Historical Society).jpg` | `875329cbd74094a80fc49b4e470b5b70e2dda48dc66594508240facdf2c75c04` | `IMG-0725` — `media/photos/early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg` | Exact byte match |

The original filenames remain preserved in the canonical media records. The repository filenames add stable media IDs and do not alter the image bytes.

## Not currently committed as photograph binaries

| Item | Status | Why it is not counted as a missing supplied photograph |
| --- | --- | --- |
| `IMG-0003` — Thebeerchaser 505 Tavern comment screenshot | `pending-upload` | Metadata and an expected path exist, but the screenshot file has not been supplied or recovered. |
| `IMG-0004` — The Wheel at 503 / 505 Tavern adjacent | `external` Time Capsule Maps metadata | The current repository has metadata, not a steward-supplied original binary. If supplied later, the preservation rule requires commit unless duplicate or an exclusion is documented. |
| `IMG-0005` — circa-1910 5th/Main scene | `external` Time Capsule Maps metadata | The current repository has metadata, not a steward-supplied original binary. A related public-source scan remains a planned import. |
| Four planned public-source early Main Street scenes | Research targets | Listed in [`early-main-street/README.md`](early-main-street/README.md); they were identified externally but were not among the recent supplied files. |
| A photograph described as 514 Main | No current item | No file or media record with that address was found. Do not relabel the cataloged 516 Main snow photograph as 514 without new evidence. |

## Storage decision

The current layout is the recommended one:

- Keep actual street-level and aerial photographs under `media/photos/`, using subject-specific subfolders as the collection grows.
- Keep the single canonical metadata register at `media/photo-metadata-register.md` and this count/reconciliation inventory at `media/photos/inventory.md`.
- Do not move newspaper clippings, map crops, directory scans, or artifact images into the photo tree merely because their files use JPG or PNG. Their source class controls preservation context and canonical location.
- Preserve steward-supplied photographs in the repository unless an exact/substantive duplicate is already present or a legal, safety, integrity, or technical reason is documented, as required by `AGENTS.md`.

The validator now checks that every committed raster has an exact-path entry in the canonical media register, resides in an approved source-class folder, and—when under `media/photos/`—begins with its stable `IMG-####` ID.
