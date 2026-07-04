# Main Street Archive Data Layout

This file defines where source files, metadata, evidence, and narrative research should live in the repository.

## Core Rule

Keep original source files separate from interpretation.

- Original source files go under `media/`, `maps/`, `records/`, or `artifacts/` depending on source type.
- Evidence summaries go under `evidence/`.
- Building narratives go under `buildings/`.
- Business narratives go under `businesses/`.
- People and family context go under `people/`.
- Oral-history notes go under `oral-history/`.

## Maps

### Sanborn PDFs

Original committed Sanborn PDFs live here:

```text
maps/sanborn/originals/
  sanborn key.pdf
  1884-01- Master Map (5th).pdf
  1888-02 (5th).pdf
  1890-02 (5th).pdf
  1892-03 (5th).pdf
  1900-13 (5th).pdf
  1911-22 (5th).pdf
  1925-6 (5th).pdf
  1950-6 (5th).pdf
```

These committed PDFs currently preserve their upload-style filenames, including spaces and parentheses. Use the exact filenames above when linking to the existing source PDFs. If the project later renames them to normalized lowercase hyphenated filenames, update the Sanborn register, source register, folder README, and any related references in the same change.

Sanborn metadata and map-use notes live here:

```text
maps/sanborn-map-register.md
```

Future cropped map images should go here:

```text
maps/sanborn/crops/
  1925-503-505-507-main-crop.png
  1950-503-505-507-main-crop.png
```

## Photos, Images, and Artifacts

### Matchbooks / Matchcovers

The committed New Kwality Cafe and Larry's Kwality Cafe artifact images currently live here:

```text
artifacts/images/
  A-001-new-kwality-cafe-matchbook.jpg
  A-002-larrys-kwality-cafe-matchcover.jpg
```

The older folder `media/artifacts/matchbooks/` is retained for location notes, but the current committed JPEGs are under `artifacts/images/`. Use the exact artifact image paths above unless the binary files are moved and all references are updated in the same change.

Image metadata is tracked here:

```text
media/photo-metadata-register.md
```

### Historic photos

General historic photos should go under:

```text
media/photos/
  503-main/
  505-main/
  507-main/
  main-street-block/
  intersections/
```

Use the most specific folder that fits the image.

### Screenshots

Screenshots used as evidence should go under:

```text
media/screenshots/
```

Example:

```text
media/screenshots/thebeerchaser-505-tavern-comment-2021.png
```

## Records

Current administrative/legal records go under:

```text
records/
```

Examples:

```text
records/505-commercial-lease-2025.md
records/505-commercial-lease-2025.pdf
```

## Evidence and Sources

Evidence and source summaries live under:

```text
evidence/evidence-register.md
evidence/source-register.md
evidence/research-leads.md
evidence/open-questions.md
```

Use evidence IDs such as `E-001`, source IDs such as `S-001`, artifact IDs such as `A-001`, image IDs such as `IMG-0001`, and map IDs such as `SM-001`.

## Buildings

Building-specific narrative files live under:

```text
buildings/503-main.md
buildings/505-main.md
buildings/507-main.md
```

## Businesses

Business-specific narrative files live under:

```text
businesses/
```

Examples:

```text
businesses/kwality-cafe.md
businesses/the-505.md
businesses/the-wheel.md
businesses/brass-rail-tavern.md
```

## People / Family Context

People and family context live under:

```text
people/people-index.md
people/profiles/
```

Current family handling:

- Grandmother's first marriage: Lafarlette.
- Grandmother's second marriage: Grisham.
- Rodney's mother Sheila and stepfather Richard / Dick were Wiitanens.
- Sheila died in 2014.
- Richard / Dick died in November 2024.

## File Naming Rules

Use lowercase, hyphens, and meaningful names for new text files, metadata files, derivative images, and future normalized source filenames.

Good:

```text
new-kwality-cafe-matchbook-503-main-j-jager.jpg
1925-503-505-507-main-crop.png
505-commercial-lease-2025.pdf
```

Avoid:

```text
IMG_1234.JPG
scan.pdf
file-final-final.pdf
```

Existing Sanborn source PDFs and artifact images are exceptions because they currently preserve their committed filenames. Do not point to normalized filenames unless the binary files are actually renamed.

## Status Terms

Use these status terms in metadata registers:

- `committed` — actual source file is in the repository.
- `referenced` — source is known but file is not in the repository.
- `pending-upload` — planned repo path exists in metadata but source file still needs upload.
- `external` — source remains outside repo by design.
- `needs-transcription` — source file exists but has not yet been transcribed/summarized.
- `needs-verification` — claim requires checking against the source.