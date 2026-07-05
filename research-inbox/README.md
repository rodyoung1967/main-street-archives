# Research Inbox

Staging folder for new research files before they are cataloged, renamed, and moved into the archive.

## Workflow

1. Drop raw files here (photos, scans, exports, screenshots).
2. Review content and assign stable IDs (`IMG-####`, `E-###`, `S-###`, etc.).
3. Move committed files to their canonical repository paths.
4. Update `media/photo-metadata-register.md`, evidence/source registers, related building pages, and YAML sidecars.
5. Run `python scripts/validate_archive.py`.

This folder should normally be empty after a batch is integrated. Do not treat inbox filenames as canonical IDs.
