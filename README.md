# The Main Street Archive

Working archive for the history of **503-507 Main Street, Oregon City, Oregon**.

This is a citation-first local history archive. It separates buildings, businesses, people, evidence, sources, research leads, open questions, media metadata, current records, maps, and oral history so the project can grow without losing track of what is known, what is inferred, and what still needs proof.

Start here: `ARCHIVE_INDEX.md`

Data layout guide: `DATA_LAYOUT.md`

ID crosswalk: `indexes/id-crosswalk.md`

## Cloud Workflow

Research on ChatGPT (project **Main Street**) → save **handoff** to `registers/research-intake/` → push to GitHub → integrate in Cursor per `docs/WORKFLOW.md`.

Full setup and iOS access: [`docs/CLOUD_WORKFLOW.md`](docs/CLOUD_WORKFLOW.md)

ChatGPT project file to upload once: [`docs/CHATGPT_PROJECT.md`](docs/CHATGPT_PROJECT.md)

Cursor integration prompt: **Integrate [handoff file] into the archive per WORKFLOW.md**

## Current Accuracy Rules

- Keep **503 Main**, **505 Main**, and **507 Main / Harding Building** as separate building records.
- Treat Mitch Young's direct testimony as confirming ownership/operation of the **505 Main Street business / The 505** from **March 1991 to March 2004**.
- Do not automatically label Mitch Young's 505 period as **The Wheel** or **The Wheel Tavern** unless documentary evidence confirms that exact name.
- Treat **The Wheel**, **The 505**, **Brass Rail Tavern**, **505 Tavern**, and **Thirsty Duck** as related but distinct business-name questions until primary records prove continuity.
- Treat Time Capsule Maps metadata as a trusted internal project source because Rodney Young is Time Capsule Maps; still cite original image/source details when making external historical claims.
- Preserve family/oral history, but separate it from deed/tax/assessor proof. Current family-name handling: grandmother's first marriage was Lafarlette and second marriage was Grisham; mother Sheila and stepfather Richard / Dick were Wiitanens.
- Treat Sanborn maps as primary map sources for footprint, materials, street layout, and address-numbering research; use the Sanborn key when interpreting symbols.

## Key Files

- `docs/CLOUD_WORKFLOW.md` - ChatGPT → GitHub → Cursor workflow; iOS access.
- `docs/CHATGPT_PROJECT.md` - upload to ChatGPT project **Main Street** (once).
- `registers/research-intake/` - ChatGPT handoff files before Cursor integration.
- `scripts/validate_archive.py` - ID consistency checker (see `requirements.txt`).
- `ARCHIVE_INDEX.md` - human-readable project index and search guide.
- `DATA_LAYOUT.md` - file/folder layout guide for maps, photos, artifacts, records, and metadata.
- `AGENTS.md` - update rules for AI/automation working in this archive.
- `indexes/id-crosswalk.md` - crosswalk connecting IDs across buildings, businesses, people, evidence, sources, media, artifacts, and maps.
- `timeline.md` - master timeline.
- `maps/sanborn-map-register.md` - Sanborn map source register and map-use notes.
- `maps/sanborn/originals/README.md` - committed Sanborn PDF filenames and folder notes.
- `artifacts/images/README.md` - committed artifact image filenames for matchbook/matchcover images.
- `media/artifacts/matchbooks/README.md` - matchbook/matchcover image location notes.
- `media/photo-metadata-register.md` - canonical photo and media metadata register.
- `media/catalog.md` - legacy media-catalog navigation shim; do not treat as canonical.
- `buildings/503-main.md` - 503 Main Street building record.
- `buildings/505-main.md` - 505 Main Street building record.
- `buildings/507-harding-building.md` - 507 Main / Harding Building record.
- `businesses/business-index.md` - business index.
- `businesses/the-505.md` - preferred working page for Mitch Young's confirmed 505 Main Street business period.
- `businesses/the-wheel.md` - related but unresolved The Wheel name/address question.
- `businesses/brass-rail-tavern.md` - Brass Rail Tavern research lead.
- `evidence/evidence-register.md` - evidence register with source type and confidence.
- `evidence/source-register.md` - source register and URL/source notes.
- `evidence/research-leads.md` - active research leads.
- `evidence/open-questions.md` - open questions register.
- `records/505-commercial-lease-2025.md` - current 2025 lease record for 505 Main.
- `oral-history/mitch-young.md` - Mitch Young direct testimony note.

## Current Media Status

The Sanborn key and Sanborn map sheet PDFs are committed under `maps/sanborn/originals/` using their current upload-style filenames. The New Kwality Cafe and Larry's Kwality Cafe matchbook/matchcover JPEG files are committed under `artifacts/images/` and are tracked in `media/photo-metadata-register.md` as `IMG-0001` / `A-001` and `IMG-0002` / `A-002`.

## Current Structure Notes

- Use `media/photo-metadata-register.md` as the canonical media/image register.
- Use `media/catalog.md` only as a legacy navigation shim.
- Keep `database/*.yml` synchronized with the Markdown indexes when machine-readable records are maintained.
- Use `indexes/id-crosswalk.md` to audit relationships across ID systems.

## Next Evidence Priorities

1. Build a Sanborn comparison table for 503, 505, 507, and possible 501 Main using 1884, 1888, 1890, 1892, 1900, 1925, and 1950 map sheets.
2. Upload Thebeerchaser screenshot to the expected media path if rights/usage are acceptable.
3. Transcribe tax statements and assessor records for 503 and 505.
4. Verify the 1925 Sanborn map labels for 501 / 503 / 505 Main.
5. Confirm The Wheel / The 505 / 505 Tavern / Brass Rail Tavern name chronology with directories, OLCC records, business licenses, ads, and tax records.
6. Find the exact 507 Harding Building fire date and replacement-building evidence.
7. Import source-backed photo files and sidecar metadata when rights/source information is clear.