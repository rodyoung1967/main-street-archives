# Newspaper Sources

This folder holds original newspaper clippings, article scans, and newspaper-page images used as source material in The Main Street Archive.

## Canonical Layout

Organize first by publication:

```text
newspapers/
  banner-courier/
  oregonian/
  oregon-city-enterprise/
  oregon-city-courier/
  other/
```

Add year subfolders only when a publication folder becomes large enough to benefit from them.

## Naming

For newly integrated files, use descriptive lowercase-hyphenated filenames, preferably beginning with the publication date when known.

Examples:

```text
1937-kwality-cafe-for-sale-oregonian.png
1967-09-wheel-505-fire-oregonian.png
1976-505-classified-oregonian.png
```

Preserve the original uploaded filename in the media/source metadata whenever a file is renamed.

## Integration Rules

A newspaper file is raw source material, not an evidence conclusion by itself.

When a clipping is integrated:

1. Place the source file here.
2. Add or update its `S-###` entry in `evidence/source-register.md`.
3. Create or update the appropriate `E-###` evidence entry in `evidence/evidence-register.md`.
4. Record the exact claim the clipping establishes and its confidence.
5. Update affected building, business, person, timeline, open-question, research-lead, YAML, and crosswalk files as appropriate.
6. Register the image in `media/photo-metadata-register.md` when image-level tracking is useful.

Do not infer claims from a filename alone; read the clipping before integrating its historical content.

The `banner-courier/` folder currently preserves the visually verified July–August 1922 pages supporting `S-111`, `S-112`, and `S-117`. Related *Oregon City Enterprise* pages are stored under `oregon-city-enterprise/`.

## Root Uploads

Newspaper images temporarily uploaded to the repository root are intake items. They should be relocated here during integration. Root copies should not be removed until the project steward approves the cleanup.
