# Media Catalog

This catalog tracks all photos, scans, PDFs, maps, tax records, and other media items in The Main Street Archive.

## Status Key

- `planned` — known item, not yet imported
- `metadata-recorded` — image/document received and described, but raw binary file still needs repository import
- `imported` — file exists in this repository
- `transcribed` — text/OCR/transcription has been added
- `linked` — connected to Evidence Register and Source Register

## Catalog

| Media ID | Status | Type | File Path | Date | Related Buildings | Description | Related Evidence | Related Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOC-0001 | planned | Tax statement / tax record | `tax-records/pending/` | Unknown | 503 / 505 | Tax statement images previously uploaded in conversation; need import, transcription, and evidence linkage. | `E-012` | `S-007` | Use to test construction, addition, footprint, parcel, and ownership questions. |
| DOC-0002 | planned | Lease / modern ownership record | `deeds-or-leases/pending/` | 2025 | 505 | 505 commercial lease; useful modern context but not primary historical evidence for older periods. | Pending | Pending | File located in File Library as `505 Commerical Lease (2025) - Final.pdf`; decide whether to import because it may contain private/business terms. |
| DOC-0003 | planned | Working archive document | `docs/pending/` | 2026 | 503 / 505 / 507 | Main Street Archive v1 working document; useful as a generated project snapshot. | Pending | Pending | File located in File Library as `Main_Street_Archive_v1.docx`. |
| IMG-0001 | metadata-recorded | Matchbook image / primary artifact | `artifacts/matchbooks/IMG-0001_new-kwality-cafe-matchbook_503-main_j-jager.md` | Unknown | 503 | New Kwality Cafe matchbook: 503 Main St., J. Jager, Prop., "We Never Close." | `E-002` | `S-002` | Raw file received as `7B921FF8-6C93-47ED-AFB3-BA43C833B9FE.jpeg`; binary import pending. |
| IMG-0002 | metadata-recorded | Matchcover image / primary artifact | `artifacts/matchbooks/IMG-0002_larrys-kwality-cafe-matchcover_503-main.md` | Unknown | 503 | Larry's Kwality Cafe matchcover: 503 Main Street, Oregon City; telephone 6106; merchants lunches, steaks & chops. | `E-003` | `S-003` | Raw file received as `89DAC5BE-D333-44DD-9273-69C6E29F5563.jpeg`; binary import pending. |
| IMG-0003 | metadata-recorded | Web screenshot / comment evidence | `artifacts/web-screenshots/IMG-0003_thebeerchaser-comment_505-tavern_publishers-paper_2021.md` | 2021-06-28 | 505 | Thebeerchaser comment screenshot discussing 505 Tavern, Publishers Paper workers, and local bar culture. | `E-013` | `S-009` | Raw file received as `C6206FF1-051D-41C9-8FC8-C757CB3998E7.png`; binary import pending. |
| IMG-0004 | planned | Photo / scan | `photos/503-main/pending/` | Unknown | 503 | Placeholder for any 503 Main building photos or family-history images. | Pending | Pending | Needs actual file import. |
| IMG-0005 | planned | Photo / scan | `photos/505-main/pending/` | Unknown | 505 | Placeholder for any 505 Main building photos, tax-statement images, or rear-addition/footprint photos. | `E-010`, `E-011`, `E-012` | `S-007`, `S-008` | Needs actual file import. |
| IMG-0006 | planned | Photo / scan | `photos/507-main/pending/` | Unknown | 507 | Placeholder for Harding Building / 507 Main images. | Pending | Pending | Needs actual file import. |
| IMG-0007 | planned | Streetscape photo | `photos/streetscapes/pending/` | Unknown | 503 / 505 / 507 | Placeholder for wider Main Street / Oregon City streetscape photos. | Pending | Pending | Needs actual file import. |
| MAP-0001 | planned | Map / Sanborn excerpt | `sanborn-maps/pending/` | Unknown | 503 / 505 / 507 | Placeholder for Sanborn/fire insurance map excerpts. | Pending | Pending | Use to test construction, footprint, and business-use questions. |

## Import Workflow

1. Add raw file to the appropriate folder.
2. Preserve original filename in the catalog notes.
3. Assign or confirm a stable Media ID.
4. Add a short description.
5. Add transcription/OCR if useful.
6. Link the item to Evidence Register and Source Register.
7. Link related building, business, person, and timeline pages.
