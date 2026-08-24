# The Main Street Archive

Working archive for the history of **503-507 Main Street, Oregon City, Oregon**.

This is a citation-first local history archive. It separates buildings, businesses, people, evidence, sources, research leads, open questions, media metadata, current records, maps, and oral history so the project can grow without losing track of what is known, what is inferred, and what still needs proof.

## First-Time Readers

If you want to **read the history in chronological order**, start with [`timeline.md`](timeline.md). It is the best single walkthrough of the Main Street story.

If you want to **navigate the archive and drill into specific buildings, businesses, people, evidence, and open questions**, use [`ARCHIVE_INDEX.md`](ARCHIVE_INDEX.md).

A useful reading order is:

1. `timeline.md` — chronological overview.
2. `buildings/503-main.md` and `buildings/505-main.md` — address-specific histories.
3. `businesses/the-wheel.md`, `businesses/brass-rail-tavern.md`, and `businesses/the-505.md` — business histories.
4. `registers/ownership-timeline.md` — separates business ownership/operation from real-estate ownership.
5. `evidence/evidence-register.md` and `evidence/source-register.md` — evidence and source audit trail.
6. `evidence/open-questions.md` — what remains uncertain.

Data layout guide: `DATA_LAYOUT.md`

ID crosswalk: `indexes/id-crosswalk.md`

## Cloud Workflow

Research on ChatGPT (project **Main Street**) → save **handoff** to `registers/research-intake/` → push to GitHub → integrate in Cursor per `docs/WORKFLOW.md`.

Full setup and iOS access: [`docs/CLOUD_WORKFLOW.md`](docs/CLOUD_WORKFLOW.md)

ChatGPT project file to upload once: [`docs/CHATGPT_PROJECT.md`](docs/CHATGPT_PROJECT.md)

Cursor integration prompt: **Integrate [handoff file] into the archive per WORKFLOW.md**

## Current Accuracy Rules

- Keep **503 Main**, **505 Main**, and **507 Main / Harding Building** as separate building records.
- Treat Mitch / Mitchell (C.) Young's testimony as confirming that Dick and Sheila Wiitanen had renamed the business **505 Tavern before selling it to their son Mitch in March 1991**. Mitch acquired it under that existing public/trade name and ran it at **505 Main Street** through **March 2004**. Keep `BUS-009` The 505 as an earlier handling label; do not say Mitch introduced or restored the name.
- **Mitch Young, Mitchell Young, Mitch C. Young, and Mitchell C. Young are the same person** (`P-011` / `P-018`).
- **The Wheel was only at 503 Main.** Do not label Mitch Young's 505 period as The Wheel, and do not use "The Wheel Tavern" as an official historical name.
- At **503 Main**, family history says Dick and Sheila Wiitanen **bought The Wheel business from Raye Grisham**, later **bought the 503 building**, and later **sold the business and building together**. Exact transaction dates, counterparties, and deed/business-sale records remain open.
- At **505 Main**, family history says Dick and Sheila **operated Brass Rail before owning the building**, then later **bought the 505 building from Mrs. Nesmeth / Nemeth** (spelling uncertain). Later business transfers/repossessions must be kept separate from continuing real-estate ownership.
- Treat **The Wheel**, **The 505**, **Brass Rail Tavern**, **505 Tavern**, and **Thirsty Duck** as related but distinct business-name records. Direct participant testimony establishes **505 Tavern** as the public/trade name already in use when Mitch acquired the business; the exact pre-sale rename date and formal license/entity continuity still require documents.
- Treat Time Capsule Maps metadata as a trusted internal project source because Rodney Young is Time Capsule Maps; still cite original image/source details when making external historical claims.
- Preserve family/oral history, but separate it from deed/tax/assessor proof. Current family-name handling: grandmother's first marriage was Lafarlette and second marriage was Grisham; mother Sheila and stepfather Richard / Dick were Wiitanens.
- Treat Sanborn maps as primary map sources for footprint, materials, street layout, and address-numbering research; use the Sanborn key when interpreting symbols.
- Whenever possible, preserve the **original source binary** in the appropriate repository folder **and** retain the canonical/original source URL in `evidence/source-register.md`. If a source can be verified online but the current tooling cannot transfer its binary, preserve a source-capture/provenance note with the canonical URL and put physical mirroring on the research backlog rather than implying the original file is already archived.

## Key Files

- `timeline.md` - **recommended first read**; master chronological walkthrough.
- `ARCHIVE_INDEX.md` - human-readable project index, search guide, and reading path.
- `registers/ownership-timeline.md` - separates property ownership, business ownership, and operation.
- `docs/CLOUD_WORKFLOW.md` - ChatGPT → GitHub → Cursor workflow; iOS access.
- `docs/CHATGPT_PROJECT.md` - upload to ChatGPT project **Main Street** (once).
- `registers/research-intake/` - ChatGPT handoff files before Cursor integration.
- `scripts/validate_archive.py` - ID consistency checker (see `requirements.txt`).
- `DATA_LAYOUT.md` - file/folder layout guide for maps, photos, artifacts, records, and metadata.
- `AGENTS.md` - update rules for AI/automation working in this archive.
- `indexes/id-crosswalk.md` - crosswalk connecting IDs across buildings, businesses, people, evidence, sources, media, artifacts, and maps.
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
- `businesses/the-wheel.md` - The Wheel history at 503 Main.
- `businesses/brass-rail-tavern.md` - Brass Rail Tavern history/research page for 505 Main.
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

1. Document the exact **503 Wheel sequence**: Raye-to-Wiitanen business sale, later Wiitanen purchase of the 503 building, and later combined sale of business and building.
2. Document the exact **505 sequence**: Brass Rail operation before property ownership, Nesmeth/Nemeth-to-Wiitanen deed, later business-transfer/repossession periods, the Wiitanens' pre-March 1991 rename to 505 Tavern, and 2024 estate succession.
3. Build a Sanborn comparison table for 503, 505, 507, and possible 501 Main using 1884, 1888, 1890, 1892, 1900, 1925, and 1950 map sheets.
4. Upload Thebeerchaser screenshot to the expected media path if rights/usage are acceptable.
5. Transcribe tax statements and assessor records for 503 and 505.
6. Verify the 1925 Sanborn map labels for 501 / 503 / 505 Main.
7. Confirm The Wheel / Brass Rail / The Dug Inn / Sports Keg / 505 Tavern / Thirsty Duck name chronology with directories, OLCC records, business licenses, ads, and tax records, including the exact date and formal paperwork for the Wiitanens' pre-March 1991 rename to 505 Tavern.
8. Find the exact 507 Harding Building replacement-building evidence.
9. Import source-backed photo files and sidecar metadata when rights/source information is clear.
