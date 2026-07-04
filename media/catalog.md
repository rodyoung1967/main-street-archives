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