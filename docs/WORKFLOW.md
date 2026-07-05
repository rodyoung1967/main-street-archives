# Archive Workflow

Use this workflow whenever new information is added to The Main Street Archive.

## First Rule

Do not replace uncertainty with certainty. If new information conflicts with existing information, preserve both claims and explain the conflict.

## Before Adding a Finding

1. Identify the evidence type:
   - Primary document
   - Primary artifact
   - Primary participant testimony
   - Family oral history
   - Secondary published source
   - Community recollection
2. Assign or reuse the correct ID:
   - `B-###` for buildings
   - `BUS-###` for businesses
   - `P-###` for people
   - `E-###` for evidence
   - `S-###` for sources
   - `A-###` for artifacts
   - `OH-###` for oral history
   - `T-###` for timeline entries
   - `RL-###` for research leads
   - `OQ-###` for open questions
3. Check existing IDs before creating a new one.
4. Never renumber existing IDs.

## Adding Evidence

When adding a new evidence item:

1. Add it to `evidence/evidence-register.md`.
2. Add or update the source in `evidence/source-register.md`.
3. Add it to `database/evidence.yml`.
4. Add or update related source data in `database/sources.yml`.
5. Link the evidence to related buildings, businesses, people, artifacts, oral history, and timeline entries.
6. Record confidence and evidence type.
7. Preserve source URLs and local file paths.

## Adding a Person

When adding a new person:

1. Add the person to `people/people-index.md`.
2. Add the person to `database/people.yml`.
3. Create `people/profiles/name.md` when there is enough context.
4. Link the person to related buildings, businesses, evidence, artifacts, oral history, and timeline entries.
5. If the person's identity is incomplete, preserve the uncertainty in the profile and open questions.

## Adding a Business

When adding a new business:

1. Add the business to `businesses/business-index.md`.
2. Add the business to `database/businesses.yml`.
3. Create `businesses/business-name.md` when there is enough context.
4. Link the business to related buildings, people, evidence, artifacts, sources, oral history, and timeline entries.
5. Keep alternate names separate until evidence proves they are the same legal business.

## Adding a Building Finding

When adding new building information:

1. Update the relevant building page in `buildings/`.
2. Update `database/buildings.yml` if the structured building data changes.
3. Link related businesses, people, evidence, sources, artifacts, and timeline entries.
4. If the finding affects construction, remodel, fire, or replacement history, update `timeline.md` and `database/timeline.yml`.
5. If the finding creates a new question, update `evidence/open-questions.md`.

## Adding an Artifact

When adding a new artifact:

1. Assign an `A-###` ID.
2. Add the artifact to `database/artifacts.yml`.
3. Add or update an artifact page in `artifacts/`.
4. Create an evidence record for the artifact in `evidence/evidence-register.md`.
5. Add the source or repository location to `evidence/source-register.md`.
6. Link the artifact to related buildings, businesses, people, and evidence.
7. Preserve image files, URLs, owner notes, and metadata when available.

## Adding Oral History

When adding oral history:

1. Assign an `OH-###` ID.
2. Add the item to `oral-history/oral-history-index.md`.
3. Create an oral history page in `oral-history/`.
4. Add structured data to `database/oral-history.yml`.
5. Create or update a related evidence record.
6. Distinguish direct participant testimony from family oral history or community recollection.
7. Add follow-up questions.

## Updating the Timeline

Update `timeline.md` and `database/timeline.yml` when a finding changes:

- Building construction or remodel dates
- Business opening or closing dates
- Ownership or operator periods
- Fires, rebuilds, or major events
- Documented occupant dates

Every timeline entry should link back to evidence.

## Handling Conflicts

When evidence conflicts:

1. Keep both claims.
2. Record the source and evidence type for each claim.
3. Note confidence separately for each claim.
4. Add the issue to `evidence/open-questions.md`.
5. Do not choose a winner unless the evidence clearly supports resolution.

## Ending a Research Session

Before stopping:

1. Make sure new IDs are linked everywhere relevant.
2. Check that every factual claim has evidence or is clearly marked as a lead/question.
3. Update `docs/DECISIONS.md` if a structural or interpretive decision was made.
4. Leave unresolved questions in `evidence/open-questions.md` or `evidence/research-leads.md`.
5. Run `git status --short` to see what changed.

