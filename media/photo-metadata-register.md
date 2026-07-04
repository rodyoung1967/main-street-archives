# Photo and Metadata Register

This register records image and photo-metadata items that have been discussed or uploaded for the Main Street project.

## Media File Status Rule

- `committed` means the actual image file is present in the repository.
- `pending-upload` means the archive has metadata and an expected path, but the actual image file still needs to be uploaded.
- `external` means the file intentionally remains outside the repository.
- `Time Capsule Maps metadata` is a trusted internal project source because Rodney Young is Time Capsule Maps, but original photo/source details should still be captured when making external historical claims.

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
- Status: `external` / Time Capsule Maps metadata; local repository import optional.
- Title / label: "The Wheel: 503 Main St, Oregon City, OR"
- Location note: The metadata places The Wheel at 503 Main Street and states that 505 Tavern is to the right at 505 Main Street.
- Confidence: Trusted internal Time Capsule Maps metadata for what was entered and maintained there; original image source/date should still be recorded when available.

## IMG-0005 — 5th / McLoughlin / US99E / Main Street, circa 1910 Metadata

- Type: Time Capsule Maps photo metadata
- Related buildings: 503 Main Street, 505 Main Street, 507 Main Street
- Evidence: `E-015`, `E-017`
- Source: `S-010`
- Expected repo path if imported: `media/photos/main-street-block/5th-mcloughlin-us99e-main-street-oregon-city-circa-1910.webp`
- Status: `external` / Time Capsule Maps metadata; local repository import optional.
- Date: Approximate, labelled 1910 in the filename/metadata.
- Location: 5th Street / McLoughlin Boulevard / US99E and Main Street, Oregon City.
- Key metadata claims:
  - The first building in the picture is gone and is now 503 and 505 Main Street.
  - The 1925 Sanborn map shows a different building labelled 501, 503, and 505 Main Street.
  - It is unclear what was ever at 501 Main.
  - 503 Main Street underwent significant modification around 2017.
  - The taller Harding Building at 507 burned and was replaced by the current building.
- Confidence: Trusted internal Time Capsule Maps metadata for what was entered and maintained there; original source/date should still be recorded when available.

## Media Import To-Do

- Upload Thebeerchaser screenshot to `media/screenshots/thebeerchaser-505-tavern-comment-2021.png`, if rights/usage are acceptable.
- Optionally import Time Capsule Maps webp images into `media/photos/` for preservation, while keeping original URLs/source metadata.
- Preserve original filenames, uploaded filenames, source URLs, and photographer/collection names.
- Add per-image YAML or JSON sidecar metadata if the project later needs machine-readable import/export.