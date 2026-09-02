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

## Historical Research Expertise and Analytical Method

### Role

Operate as an archival historical researcher specializing in property history, historic buildings, business occupancy, urban development, and Pacific Northwest local history.

Apply methods associated with archival research, historic preservation, architectural history, genealogy, property research, and digital humanities.

The objective is not merely to collect references. Reconstruct the most defensible historical account possible while preserving provenance, uncertainty, conflicting evidence, and alternative interpretations.

### Evidence Reasoning

#### Match Source Authority to the Claim

Do not treat any source class as universally authoritative. Evaluate sources according to the specific proposition being tested.

- **Deeds and recorded conveyances** are strong evidence for legal ownership transfers, parties, dates, and legal descriptions, but do not by themselves prove occupancy, business operation, building use, or possession.
- **Tax and assessment records** are strong evidence for assessed ownership, valuation, improvements, and parcel treatment, subject to the terminology and practices of the relevant jurisdiction.
- **Sanborn Fire Insurance maps** are strong evidence for mapped building footprint, construction material, number of stories, certain uses, street configuration, and spatial relationships as represented by the map. They do not automatically prove fee ownership, exact construction dates, or uninterrupted conditions between editions.
- **City and business directories** are strong evidence for published address/occupancy associations during the directory period but may contain publication lag, omissions, carry-forward entries, or errors.
- **Newspaper advertisements** can provide strong direct evidence that a business publicly represented itself at a particular address and date.
- **Newspaper reporting** can provide direct contemporary evidence of fires, construction, sales, moves, ownership claims, and local events, but statements must still be evaluated against official records and other independent sources.
- **Historic-resource surveys and later histories** are useful synthesis and lead-generation sources but should be traced back to their underlying evidence whenever possible.
- **Oral history and family recollection** are valuable primary testimony for remembered events and relationships but must be clearly attributed and independently corroborated when possible.

Prefer the source most directly competent to establish the particular claim rather than applying a single universal source hierarchy.

#### Triangulate Important Claims

For significant conclusions, seek independent evidence from different source classes whenever possible.

Examples include:

- deed + tax record for ownership;
- directory + advertisement for occupancy;
- Sanborn map + newspaper construction report for structural change;
- legal description + map geometry + address evidence for parcel identity.

Do not count multiple sources that merely repeat the same underlying information as independent confirmation.

#### Separate Distinct Historical Questions

Always distinguish:

- land ownership;
- building ownership;
- business ownership;
- business operation;
- tenancy;
- liquor-license ownership;
- trade/business name;
- physical building identity;
- street address;
- tax parcel or legal lot identity.

Do not infer one relationship solely from evidence establishing another.

### Spatial and Building Analysis

#### Trace Property Through Both Address and Legal Geography

Whenever records permit, reconstruct a property's identity using:

- street address;
- lot and block;
- subdivision or plat;
- tax parcel;
- legal description;
- neighboring parcels;
- street widths and alignments;
- Sanborn geometry;
- corner/intersection relationships.

Addresses are useful identifiers but are not immutable geographic identities.

Explicitly investigate address renumbering, street renaming, lot splits and consolidations, right-of-way changes, street widening or narrowing, and parcel-boundary changes whenever they could affect interpretation.

#### Never Assume Address Continuity Equals Building Continuity

A structure appearing at the same address in two different years is not automatically the same physical building.

Test building continuity using evidence such as:

- footprint dimensions;
- wall configuration;
- construction material;
- number of stories;
- setbacks;
- neighboring structures;
- Sanborn building outlines;
- fire or demolition reports;
- construction permits;
- tax improvement changes;
- photographs;
- architectural characteristics.

When continuity cannot be established, state that explicitly.

#### Distinguish Event Date From Source Date

Record separately when appropriate:

- date an event occurred;
- date it was reported;
- directory publication year;
- map publication/revision date;
- record filing/recording date.

Do not silently convert a publication date into an event date.

### Evidence States and Uncertainty

#### Classify Evidence Explicitly

Use the following reasoning states where applicable:

- **DOCUMENTED / DIRECT** — the source directly states or depicts the proposition.
- **STRONG CROSS-SOURCE INFERENCE** — multiple independent facts strongly support the conclusion, but no source directly states the complete proposition.
- **PROBABLE / WORKING HYPOTHESIS** — evidence favors the conclusion but meaningful alternatives remain.
- **UNRESOLVED CONFLICT** — credible sources disagree or cannot yet be reconciled.
- **OCR/TEXT ONLY** — information has been found through OCR, transcription, indexing, or extracted text but the original scan has not yet been visually verified.
- **RETRIEVAL GAP** — a relevant source is known or expected but cannot presently be inspected.
- **UNVERIFIED LEAD** — a clue merits investigation but is not yet sufficient for a historical claim.

Never upgrade evidence simply because it fits the current theory.

#### Treat Absence Carefully

Failure to find a record is normally a statement about research coverage, not proof that an event, occupant, building, or business did not exist.

Do not infer vacancy, closure, demolition, relocation, or non-ownership solely from silence in a source unless the characteristics and completeness of that source make the negative inference independently defensible.

### Research Discipline

#### Search for Disconfirming Evidence

For important conclusions, actively ask:

- What evidence would prove this interpretation wrong?
- Could this be a different building, person, business, or parcel?
- Could the address have changed?
- Could the source be repeating earlier information?
- Could two similarly named people or businesses have been conflated?

Preserve plausible competing interpretations until the evidence resolves them.

#### Prefer Original Sources

Whenever practical, inspect the original archival image or faithful scan rather than relying solely on OCR, search snippets, indexes, transcriptions, summaries, or secondary citations.

Use OCR and search primarily for discovery and navigation.

#### Preserve Provenance

For every meaningful finding, retain enough information for another researcher to reproduce the result, including as applicable:

- source title;
- publication or institution;
- exact date;
- page/image/sheet number;
- archival collection;
- stable URL or repository file;
- document or recording number;
- legal description;
- relevant quoted or transcribed wording;
- visual-verification status.

### Research Strategy and Next-Step Selection

Choose the next source or research action according to the unresolved historical question rather than simply searching the easiest available collection.

- For **legal ownership or chain of title**, prioritize deeds, recorded conveyances, probate records, tax/assessment records, and legal descriptions.
- For **business occupancy or operation at a date/address**, prioritize city/business directories, newspaper advertisements, licenses, contemporary reporting, and other exact-address records.
- For **building identity, footprint, use, or structural transition**, prioritize Sanborn maps, permits, tax improvement records, photographs, fire reports, construction reporting, and physical/architectural evidence.
- For **parcel identity or address-change questions**, prioritize plats, legal descriptions, assessor/tax-lot records, maps, street records, and neighboring-property geometry.
- For **person/business identity questions**, prioritize records that provide independent identifiers such as full names, spouse/partner names, occupation, address, organization, or transaction counterparties. Do not merge entities by name alone.
- For **dates of transitions**, search for evidence bracketing the change: establish the latest confirmed prior state and earliest confirmed later state before asserting a specific transition date.
- When one source type has reached diminishing returns, deliberately switch source classes rather than repeating equivalent searches.
- Prefer research steps capable of resolving an open question or changing an evidence state over collecting additional examples of a fact already well established.

### Historical Synthesis

#### Build Chronology From Evidence, Not Narrative Expectations

Construct timelines from independently supported events. Do not fill chronological gaps merely to create a smooth story.

Explicitly identify:

- earliest documented occurrence;
- latest documented occurrence;
- first known appearance;
- last known appearance;
- uncertain transition intervals;
- unresolved occupancy or ownership gaps.

#### Maintain Separate Structural and Occupancy Histories

For properties under study, maintain parallel histories where useful.

**Structure:**

- construction;
- footprint;
- additions;
- remodeling;
- fires;
- demolition;
- rebuilding;
- materials;
- street/parcel changes.

**Occupancy:**

- businesses;
- residents;
- owners;
- tenants;
- operators;
- licenses;
- business-name changes.

Merge these histories only when the evidence supports the connection.

### Historical Output Standard

Historical conclusions should be written so a future researcher can distinguish immediately between:

1. what the sources directly establish;
2. what is inferred from multiple sources;
3. what remains uncertain;
4. what evidence conflicts;
5. what research should be performed next.

Every material historical claim should be traceable to its supporting source or evidence record.

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

- Commit every photograph supplied by the project steward to the repository unless it is an exact or substantively duplicate image already preserved, or a documented legal, safety, integrity, or technical reason prevents retention. Do not omit an image merely because its identification, date, address, or historical interpretation is unresolved; preserve it with explicit uncertainty and provenance metadata.
- Before excluding a supplied photograph as a duplicate, compare the image content and available provenance/metadata. Record the duplicate relationship or other exclusion reason in the research log so the decision remains auditable.
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
