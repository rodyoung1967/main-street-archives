# Agent Instructions

These instructions apply to any AI or automation working on The Main Street Archive.

## Core Rules

- Never delete historical information without preserving why it was superseded or moved.
- Do not delete or relocate legacy files/folders without explicit project-steward approval.
- Never renumber existing IDs.
- Always update related files when new information is added.
- Preserve uncertainty rather than inventing certainty.
- Prefer traceability over brevity.
- Treat Markdown registers and indexes as human-readable source-of-truth records unless a specific YAML/database file is explicitly designated as canonical.
- When YAML/database files exist for the same entity type, keep them synchronized with the Markdown indexes.
- Keep raw source files separate from interpretation.
- Do not use the repository root as permanent raw-source storage.

## Annual Research and Closeout Status

- Follow `RESEARCH-STANDARD.md` for every year-level research pass.
- Use only these year statuses: **IN PROGRESS**, **ONLINE COMPLETE**, and **ONLINE + MANUAL COMPLETE**.
- **ONLINE COMPLETE** requires the exhaustive online pass, page-by-page visual review of every online-retrievable newspaper page, integration of findings, and a numbered list of all remaining manual work.
- **ONLINE + MANUAL COMPLETE** requires ONLINE COMPLETE plus completion or project-steward closure of every manual callout.
- A documented online retrieval gap may become a manual callout after reasonable recovery attempts; it is never negative evidence.
- Do not use unqualified wording such as “closed,” “substantially complete,” or “complete enough” in place of the exact status.
- ONLINE COMPLETE is sufficient to proceed chronologically to the next year.
- Research-work completion does not imply that every historical question has a surviving answer.

## Canonical Source-File Placement

Use these destinations for new/integrated source files:

- Newspaper clippings and newspaper-page scans → `newspapers/`
- Historic photos, aerials, and screenshots → `media/`
- Sanborn and other original maps → `maps/`
- Deeds, tax, assessor, permit, lease, and other administrative/legal records → `records/`
- Physical-object images such as matchbooks and matchcovers → `artifacts/`

The former top-level `photos/`, `deeds/`, and `tax-records/` holding areas were retired after project-steward approval on 18 August 2026. Do not recreate them; use the canonical destinations above.

Use `media/photo-metadata-register.md` as the canonical image/media metadata register. `media/catalog.md` is a legacy navigation shim only.

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
- Store the committed image file under the correct source-file folder.
- Update `media/photo-metadata-register.md`; this is the canonical media/image metadata register.
- Link the artifact/image to supporting evidence, source, building, business, person, and `indexes/id-crosswalk.md` when applicable.

## Adding Newspaper Sources

If a newspaper clipping or page image is added:

- Store the source under `newspapers/<publication>/`.
- Preserve the original uploaded filename in metadata if the committed filename is normalized.
- Add or update the source in `evidence/source-register.md`.
- Add or update the claim-level evidence in `evidence/evidence-register.md`.
- Read the clipping before integrating historical claims; never infer a claim from the filename alone.
- Update related buildings, businesses, people, timeline, open questions, research leads, YAML, media metadata, and crosswalks as appropriate.

## Adding Administrative / Property Records

If a deed, tax record, assessor record, permit, lease, or similar document is added:

- Store it under `records/`, using a source-type subfolder when useful.
- Preserve document numbers, parcel/APN, dates, parties, provenance, and original filename when available.
- Add or update related source and evidence records.
- Keep real-estate ownership, business ownership, business operation, trade names, and liquor-license ownership as separate relationship questions.

## Adding Maps

If a Sanborn or other map source is added:

- Assign or confirm a stable `SM-###` map ID when it belongs in the Sanborn series.
- Add the binary source file under the appropriate map source folder.
- Update `maps/sanborn-map-register.md` and related evidence.

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

- **The Wheel (`BUS-004`) was only at 503 Main and was never a 505 Main business.** Never link it to 505 as a business location.
- **"The Wheel Tavern" was never an official business name.** Preserve that phrase only as wording from the 2017 secondary article.
- **Raye LaFarlette and Raye Grisham are the same woman.** The surname change is not a Wheel ownership transfer.
- **503 Wheel controlling family chronology:** Raye owned The Wheel business; **Dick and Sheila purchased The Wheel business from Raye; later Dick and Sheila purchased the 503 building; when they later sold The Wheel business, they also sold the 503 building.** Treat these as three distinct transactions: business purchase, later real-estate purchase, and later combined business/building sale. Exact dates, property seller, later buyer, deeds, business-sale agreements, and liquor-license transfers remain documentary research targets.
- Richard M. Wiitanen is independently documented as owner of The Wheel Cafe business at 503 Main in August 1985 (`E-049`).
- Do **not** attach Mrs. Nesmeth/Nemeth to the 503 property purchase. That family recollection belongs to **505 Main**.
- **505 controlling family chronology:** Dick and Sheila first operated Brass Rail while they did not own the 505 building; they later purchased the 505 building from Mrs. Nesmeth / Nemeth (spelling uncertain).
- After buying 505, the Wiitanens remained real-estate owners/landlords while later tavern businesses changed operators. Later Wiitanen appearances in 505 transfer records may reflect sale, repossession, default, or transfer intervals.
- The 6 April 1988 Wiitanen-to-Cotterell record (`E-030`) proves a 505 business-transfer role at that moment.
- Ray Hansen and Raye Grisham are different people. Hansen belongs to the separate 505 Tavern history.
- Before selling the tavern business to their son Mitch in March 1991, Dick and Sheila Wiitanen had renamed it **505 Tavern**. Mitch acquired it under that existing public/trade name; do not say he introduced or restored the name. Exact rename date and formal license/entity wording remain documentary research targets.
- Mitch / Mitchell (C.) Young ran **505 Tavern at 505 Main** from March 1991 through March 2004. This period is not The Wheel.
- Mitch Young, Mitchell Young, Mitch C. Young, and Mitchell C. Young are the same person (`P-011` / `P-018`).
- Sheila Wiitanen died in 2014. Wiitanen ownership of 505 Main continued through Richard / Dick Wiitanen's death in November 2024.
- After Dick's death, 505 Main passed to Rodney Young and Mitchell Young through his estate; current ownership/stewardship is through 505 LLC. Probate/deed documentation remains desirable.
- `P-019` is **Alin Guria**, the current 505 lessee and current operating-business owner. Earlier **Alan** and **Alan / Alin** wording was a project typo and is superseded. Do not confuse this business/lease role with ownership of the 505 real estate by 505 LLC.
- Property ownership, business ownership, business operation, and liquor-license ownership are separate questions.
- Sanborn maps are primary map sources for footprint, materials, street layout, and address numbering, but map readings still require careful transcription and symbol interpretation.
