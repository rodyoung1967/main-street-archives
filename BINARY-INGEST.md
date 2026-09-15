# Binary Source Ingest Workflow

## Purpose

This file documents the proven method for preserving photographs, PDFs, newspaper scans, and other binary source files when an AI/chat GitHub connector can edit repository text but cannot directly transfer an uploaded conversation binary into GitHub.

**Do not conclude that a steward-supplied image or other binary cannot be added merely because the GitHub contents action is text-only. Check this workflow first.**

## Proven solution

When the supplied file corresponds to a publicly retrievable archival object, use the repository itself to retrieve and commit the binary:

1. Treat the project-steward upload as the visual/provenance control. Record its dimensions, byte count, SHA-256, original filename when appropriate, and supplied institutional metadata.
2. Identify the exact public archival object using its stable catalog/object ID. Do not retrieve a merely similar image.
3. Add a small Python fetch script under `scripts/` that queries the institution's public API or stable download endpoint, verifies the exact object ID, selects the best appropriate public derivative, downloads the binary, verifies its type, computes dimensions/bytes/SHA-256 where applicable, and writes it to the canonical repository source folder.
4. Have that script update the relevant source capture, canonical register, inventory, and other records from `pending-upload` to `committed`. Preserve the steward-upload fingerprint separately because the public derivative may not be byte-identical to the steward's copy.
5. Add a GitHub Actions workflow under `.github/workflows/` with `contents: write`. The workflow checks out current `main`, runs the fetch script, runs `scripts/validate_archive.py`, commits the resulting binary and metadata changes, rebases on current `main`, validates again, and pushes to `main`.
6. Verify the resulting binary exists on current `main` before reporting the ingest complete. Do not equate metadata-only preservation with binary preservation.

## Proven precedent: 1960 CCHS Fifth/Main photograph

This workflow was successfully used for Clackamas County Historical Society object `2008.008.049.037`.

Reference implementation:

- Fetch script: `scripts/fetch_cchs_2008_008_049_037_1960_bluff.py`
- Workflow: `.github/workflows/fetch-cchs-2008-008-049-037-1960-bluff.yml`
- Resulting image: `media/photos/main-street/IMG-0771_1960-5th-main-from-bluff-cchs-2008-008-049-037.jpg`
- Binary-preservation commit: `d6fdf22de7df77b0e3ce30864b26a5155b25eb42`

The script searched the public CatalogIt API for the exact CCHS catalog number, verified the returned object, selected the largest non-thumbnail public derivative, downloaded the JPEG, fingerprinted it, wrote it into `media/photos/main-street/`, updated the photo metadata register/inventory/source capture, and produced an API provenance record. The GitHub Actions workflow then validated and committed the binary.

## CCHS / CatalogIt pattern

For another CCHS image, start by adapting the proven `2008.008.049.037` implementation rather than inventing a new ingest mechanism. Change the target catalog ID, canonical IMG ID/path, expected steward-upload fingerprint, source-capture path, and metadata/inventory updates. Preserve the distinction between:

- institutional catalog metadata;
- the steward-supplied copy and its fingerprint;
- the repository's downloaded public derivative and its fingerprint;
- project interpretation such as estimated date, address identification, or visual inference.

Never attribute a project filename, inferred date, or research conclusion to the holding institution unless its catalog actually states it.

## If no public binary can be retrieved

If the exact supplied source has no public API/download route, then this workflow cannot manufacture the uploaded bytes. Record a genuine technical ingest gap and preserve the steward fingerprint and metadata. Before declaring that gap, however, search the repository for prior fetch scripts/workflows and test the holding institution's public catalog/API/download routes. Do not ask the steward to re-upload a file that is already available in the conversation unless the conversation attachment itself is actually unavailable.

## Required completion checks

A binary ingest is complete only when all applicable checks pass:

- exact source/object identity verified;
- canonical repository path and stable ID assigned;
- binary visible on current `main`;
- steward and repository fingerprints distinguished where bytes differ;
- canonical metadata/source/evidence records updated;
- cross-record propagation reviewed;
- `scripts/validate_archive.py` passes after the binary is present;
- final response identifies the actual binary-preservation commit.

## Agent reminder

When a future conversation asks, "Why can't you add this uploaded photo/file to the repo?", do **not** stop at the connector's inability to transfer local binary bytes. Search `BINARY-INGEST.md`, existing `scripts/fetch_*` files, `.github/workflows/`, and recent commits containing `binary`, `fetch`, `photo`, or `preserve`. The repository may already contain a proven server-side retrieval-and-commit solution.