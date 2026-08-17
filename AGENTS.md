# Agent Instructions

These instructions apply to any AI or automation working on The Main Street Archive.

## Core Rules

- Never delete historical information without preserving why it was superseded or moved.
- Never renumber existing IDs.
- Always update related files when new information is added.
- Preserve uncertainty rather than inventing certainty.
- Prefer traceability over brevity.
- Treat Markdown registers and indexes as human-readable source-of-truth records unless a specific YAML/database file is explicitly designated as canonical.
- When YAML/database files exist for the same entity type, keep them synchronized with the Markdown indexes.

## Adding People

If a new person is introduced:

- Assign or confirm a stable `P-###` ID.
- Add the person to `people/people-index.md`.
- Add or update the person in `database/people.yml`.
- Create or update a profile under `people/profiles/` when the person has enough detail for a standalone page.
- Connect the person to related businesses, buildings, evidence, sources, timeline entries, and `indexes/id-crosswalk.md` when applicable.

## Adding Businesses

If a new business is introduced:

- Assign or confirm a stable `BUS-###` ID.
- Add the business to `businesses/business-index.md`.
- Add or update the business in `database/businesses.yml`.
- Create or update a business page under `businesses/` when the business has enough detail for a standalone page.
- Connect the business to related buildings, people, artifacts, media, evidence, sources, timeline entries, and `indexes/id-crosswalk.md` when applicable.

## Adding Buildings

If a new building or building-address question is introduced:

- Assign or confirm a stable `B-###` ID.
- Add or update the relevant page under `buildings/`.
- Add or update the building in `database/buildings.yml`.
- Update `ARCHIVE_INDEX.md` and `timeline.md` if the change affects navigation or chronology.
- Link related businesses, people, artifacts, media, maps, evidence, and sources.

## Adding Artifacts or Images

If a new artifact or image is added:

- Assign an `A-###` ID for physical artifacts when appropriate.
- Assign or confirm an `IMG-####` media ID for image/media tracking.
- Store the committed image file under the correct source-file folder, currently `artifacts/images/` for the New Kwality Cafe and Larry's Kwality Cafe artifact images.
- Update `artifacts/images/README.md` if the folder contents change.
- Update `media/photo-metadata-register.md`; this is the canonical media/image metadata register.
- Update `media/catalog.md` only as a navigation shim if needed; do not treat it as the canonical media register.
- Link the artifact/image to supporting evidence, source, building, business, person, and `indexes/id-crosswalk.md` when applicable.
- Preserve original filenames, uploaded filenames, source URLs, owner/collector notes, and visible captions or marks when known.

## Adding Maps

If a Sanborn or other map source is added:

- Assign or confirm a stable `SM-###` map ID when it belongs in the Sanborn series.
- Add the binary source file under the appropriate map source folder, currently `maps/sanborn/originals/` for original Sanborn PDFs.
- Update `maps/sanborn-map-register.md`.
- Update `evidence/source-register.md` and any evidence records that depend on the map.
- Use the Sanborn key before making claims about materials, openings, fireproofing, utilities, or map symbols.

## Updating Evidence

If evidence changes:

- Update `evidence/evidence-register.md`.
- Update `evidence/source-register.md` if source details or file paths changed.
- Update `evidence/open-questions.md` if a question is answered, narrowed, or reframed.
- Update `evidence/research-leads.md` if the change creates or resolves a research lead.
- Update `timeline.md` if appropriate.
- Update `indexes/id-crosswalk.md` when the evidence connects IDs across source/media/artifact/person/business/building records.
- Leave conflicting evidence intact until resolved; do not collapse uncertainty into a single unsupported conclusion.

## Current Accuracy Reminders

- Mitch / Mitchell (C.) Young's confirmed March 1991-March 2004 period belongs to **505 Tavern at 505 Main Street**. He **ran** the business. Do **not** say he restored the name, fixtures, or building. Keep `BUS-009` The 505 as an earlier handling label. Do not label this period The Wheel.
- **Mitch Young, Mitchell Young, Mitch C. Young, and Mitchell C. Young are the same person** (`P-011` / `P-018`). Do not treat them as two people. Do not renumber or merge the IDs.
- **The Wheel (`BUS-004`) is at 503 Main.** Raye Grisham (`P-006`, grandmother; formerly Raye LaFarlette) bought The Wheel at 503. Oregon City Commission minutes of 7 June 1967 place "the Wheel" at 503 Main Street.
- **Ray Hansen (`P-005`) and Raye Grisham (`P-006`) are different people.** Hansen sold the 505 Tavern **business** to Dick and Sheila Wiitanen. Do not merge Hansen with Grisham.
- Property ownership, business ownership, and liquor-license ownership are separate questions.
- After Richard Wiitanen's death, 505 Main real estate passed to **Rodney Young and Mitchell Young** jointly through 505 LLC.
- The Wheel, The 505, 505 Tavern, Brass Rail Tavern, The Dug Inn, and Thirsty Duck remain related but distinct business-name records until primary records prove continuity.
- Sanborn maps are primary map sources for footprint, materials, street layout, and address numbering, but map readings still require careful transcription and symbol interpretation.
