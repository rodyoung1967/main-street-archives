# Media Archive

This folder holds photographic/image media and the canonical media metadata register for The Main Street Archive.

The goal is to preserve original image files and connect each item to evidence, sources, buildings, people, businesses, maps, and timeline entries without mixing raw media with interpretation.

## Canonical Register

Use:

```text
media/photo-metadata-register.md
```

as the canonical image/media metadata register.

Use [`media/photos/inventory.md`](photos/inventory.md) for the definitive inventory of committed photographs and aerials, the supplied-photo reconciliation, and the distinction between photographs and source scans stored elsewhere.

`media/catalog.md` is retained only as a legacy navigation shim for older references. Do not add new canonical metadata there.

## Folder Structure

```text
media/
  photo-metadata-register.md
  photos/
    503-main/
    505-main/
    507-main/
    main-street-block/
    intersections/
    aerials/
  screenshots/
```

Use the most specific folder that fits the image.

Other source types belong elsewhere:

- Newspaper clippings/scans → `newspapers/`
- Sanborn and other original maps → `maps/`
- Deeds, tax, assessor, permit, lease, and other administrative/legal records → `records/`
- Physical-object images such as matchbooks/matchcovers → `artifacts/`

## Naming Convention

Use stable IDs where appropriate and descriptive lowercase-hyphenated filenames for new files and derivatives.

Examples:

```text
503-main-front-view-unknown-date.jpg
1925-503-505-507-main-crop.png
```

Do not rename a cataloged source casually. If a source file is renamed or moved, update `media/photo-metadata-register.md`, the source/evidence registers, crosswalks, and any direct links in the same change. Preserve the original uploaded filename in metadata.

## Handling Rule

Every imported image should eventually have, when applicable:

- Archive/media ID
- Canonical repository file path
- Original filename
- Date or estimated date
- Source / owner / repository
- Copyright or usage note
- Buildings shown or affected
- People/businesses shown or referenced
- Description
- Evidence IDs
- Source IDs
- Confidence level
- Transcription/OCR status

The former top-level `photos/` tree was retired after its placeholder guidance was consolidated here and in `media/photos/README.md`. Do not recreate it; use `media/photos/`.
