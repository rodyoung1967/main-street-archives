# Media Catalog

This file is retained as a navigation shim for older references.

## Canonical Media Register

The canonical media and image metadata register is now:

```text
media/photo-metadata-register.md
```

Use that file for current media IDs, repository file paths, status values, and source/evidence links.

## Current High-Level Status

| Media ID | Canonical record | Current file/status |
| --- | --- | --- |
| `IMG-0001` / `A-001` | `media/photo-metadata-register.md` | Committed: `artifacts/images/A-001-new-kwality-cafe-matchbook.jpg` |
| `IMG-0002` / `A-002` | `media/photo-metadata-register.md` | Committed: `artifacts/images/A-002-larrys-kwality-cafe-matchcover.jpg` |
| `IMG-0003` | `media/photo-metadata-register.md` | Pending upload: `media/screenshots/thebeerchaser-505-tavern-comment-2021.png` |
| `IMG-0004` | `media/photo-metadata-register.md` | External / Time Capsule Maps metadata |
| `IMG-0005` | `media/photo-metadata-register.md` | External / Time Capsule Maps metadata |
| `IMG-0006`–`IMG-0043` | `media/photo-metadata-register.md` | Committed: `media/photos/aerials/` (38-frame 5th & Main photocompare series, `E-021` / `S-023`) |
| `IMG-0044`–`IMG-0053` | `media/photo-metadata-register.md` | Committed: `newspapers/oregonian/` (Oregonian clippings, `E-042`–`E-049`) |
| `IMG-0711`–`IMG-0713` | `media/photo-metadata-register.md` | Committed map crops/screenshots under `maps/images/`; exact editions unresolved (`S-146` / `E-131`) |
| `IMG-0714`–`IMG-0716` | `media/photo-metadata-register.md` | Committed and visually reconciled newspaper screenshots: Harding 1911, Dixon's 1964, unnamed 509 shop 1965 |
| `IMG-0717`–`IMG-0721` | `media/photo-metadata-register.md` | Committed 1915–1916 Polk directory page images (`S-132` / `E-118`) |
| `IMG-0722` | `media/photo-metadata-register.md` | Committed Tom Keene cigar-sign crop; date/source/location unresolved |

## Deprecated Older Paths

Older entries in this catalog previously pointed to placeholder paths such as `artifacts/matchbooks/*.md`, `photos/*/pending/`, and `sanborn-maps/pending/`. Those should not be treated as current repository file paths.

For Sanborn map files, use:

```text
maps/sanborn-map-register.md
maps/sanborn/originals/README.md
```

For artifact image files, use:

```text
artifacts/images/README.md
media/photo-metadata-register.md
```

## Import Workflow

1. Add the raw file to the appropriate committed-source folder.
2. Preserve original filename and source/provenance notes in the canonical register.
3. Assign or confirm a stable ID.
4. Link the item to evidence, source, building, business, person, timeline, and crosswalk records as needed.
5. Update `indexes/id-crosswalk.md` if the item participates in a multi-ID relationship.
