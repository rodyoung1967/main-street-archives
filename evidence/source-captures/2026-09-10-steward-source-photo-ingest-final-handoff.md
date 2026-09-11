# 2026-09-10 — steward source/photo-ingest final conversation handoff

Status: **conversation knowledge saved; canonical newspaper integrations complete; early-photo reconciliation still pending for three CCHS objects plus one unidentified flood image**

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Synchronized pre-write HEAD: **11830dd3e26524c4b6dfa041d66fb0af1d65c8a2** — `Preserve Farr Harr municipal directory conversation handoff`

The archive validator for that exact HEAD completed successfully before this handoff was written (Validate archive run 34555892566).

## Purpose of this conversation

This conversation had two connected purposes:

1. **Steward-supplied source ingest.** Reconcile every supplied newspaper PDF and historic photograph against the authoritative repository; avoid duplicate binaries and duplicate IDs; preserve missing source files; integrate only what the source actually supports; and keep source, evidence, timeline, YAML, media, crosswalk, building, business and people records synchronized.
2. **501/503/505 physical-history reconstruction.** Use newly supplied primary newspaper pages and early Main Street photographs to improve the chronology and spatial understanding of the Fifth/Main frontage while keeping street address, physical building identity, parcel identity, business occupancy, business ownership, real-estate ownership, tenancy and licensing as separate questions.

The repository remains authoritative. Future work must always re-sync current `main`, reread current `AGENTS.md` and `RESEARCH-STANDARD.md`, preserve existing IDs, review newer parallel commits, validate before/after meaningful changes, and never treat retrieval failure or search silence as negative historical evidence.

No institutional/manual request was authorized or sent in this conversation.

## Canonical knowledge already saved elsewhere

The detailed newspaper-ingest and photo-ingest history from this conversation is already preserved in:

`evidence/source-captures/2026-09-10-steward-newspaper-photo-ingest-conversation-handoff.md`

Do not recreate that work from scratch. Current canonical records already preserve the following major conclusions:

- Fifth Street Restaurant sequence, including W. W. Pollock, Guy Proffit, 1916/1919/1920/1921/1922 evidence, and the Blake/Blakely/Gage/C. P. Gates conflicts.
- Wolf & Miller direct 505 Main evidence in September/October 1918 and the separate 31 October 1918 printed 503 Main conflict.
- Young's Second Hand Store and Chicago Store exact 505 Main evidence; December 1913 Chicago Store fire and George Harding building-owner wording.
- Palace Saloon chronology, including Ralph O. Smith at Fifth/Main and E. R. Case notices visibly printing 510 Main in June 1910; later Palace 501 evidence remains a separate unresolved address-transition question.
- Dr. Freeze rule: **505½ is an address designation, not proof of an upper floor.** Same-floor side-by-side, front/rear, upper-floor or another subdivision remain possible until physical evidence resolves it. The 507½ “over Harding Drug Store” wording is a separate stronger upper-floor clue for that earlier location.
- JAGERS at exact 503 Main in 1940 remains separate from J. Jager / New Kwality Cafe absent a direct identity/name-change bridge.
- 1920 Clem Dollar pool hall and A. Leland at 505½ remain separate unless directly bridged.
- Early Fifth/Main meat, Surber/Justin, Mt. Hood Cafe and Andresen/Stevens evidence is already integrated with its stated limits.

## Current early-photo state

Parallel work after the first photo discussion materially advanced the repository. Earlier provisional image IDs from this conversation are stale and must not be reused. Current media IDs extend well beyond the early `IMG-0727` range.

### CCHS object P‑1469 — already integrated

Current canonical repository record:

- media: **IMG-0732**
- source/evidence: **S-203 / E-183**
- path: `media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg`
- catalog title: **1890 Flood - Oregon City Main Street**
- date: **1890**
- CCHS description: **6th and Main, looking southwest; unidentified people; flooding; debris**

Steward-supplied attachment fingerprint from this conversation:

- filename: `Oregon City Main Street, 6th & Main, looking southwest down main.  (Clackamas County Historical Society).jpg`
- dimensions: **2048 × 1489**
- bytes: **677,988**
- SHA-256: `2f7243e7a8fd1fb6d444654796de5eb62836c20e75da4cc40568e547267bfc26`

Steward directional interpretation: 6th & Main looking south toward the Fifth Street intersection. Keep this attributed separately from CCHS catalog wording.

Next action: if the exact steward fingerprint is not yet in the existing IMG-0732 provenance record, add it there. Do not create a second photo record.

### CCHS object P‑1460 — metadata and exact steward file preserved in this handoff; not yet found by object ID on current main

Catalog metadata supplied by steward:

- title: **1890 Flood - Oregon City Main Street**
- description: **Willamette River Flood 1890. Main Street Oregon City. Looking south from center of blocks between 6th and 5th streets. Unidentified people.**
- date: **1890**
- medium: **Photographic Paper**

Steward interpretation: camera position is near/between Sixth and Fifth looking south; **the two men on the right are standing in front of the frontage associated with the later 501–505 Main research area**. This is a project-steward spatial interpretation, not CCHS catalog metadata and not proof that the 1890 structure carried later street numbers.

Exact attachment:

- filename: `Flood 1890 on Main Street Oregon Citiy.  Looking south from north endof 5th street.jpg`
- dimensions: **2048 × 1500**
- bytes: **676,604**
- SHA-256: `2dd929aa3a479cd7e7e20d7ee453e7fb1c5694c784178a042850f05629dd5be6`

Current code search on synchronized main found no direct P‑1460 object-ID record.

Next action: compare against the committed 1890 flood-photo set, especially IMG-0732 / P‑1469 and IMG-0733 / P‑1456. If distinct, ingest under the next unused current IMG/S/E IDs after re-syncing. Preserve the steward frontage identification as attributed interpretation.

### CCHS object P‑1474 — metadata and exact steward file preserved in this handoff; not yet found by object ID on current main

Catalog metadata supplied by steward:

- title: **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon**
- description: **1890 Flood, after the water resided, Main Street, Oregon City, Oregon.**
- date: **1890**
- medium: **Photographic Paper**

Steward interpretation: **the building/frontage corresponding to the later 501–505 Main research area is directly on the left**.

Exact attachment:

- filename: `1890 Flood, after the water resided, looking north from 5th & Main Street, Oregon City, Oregon (503 & 505 1st on the laft & blacksmith visible on the right).jpg`
- dimensions: **2048 × 1174**
- bytes: **653,119**
- SHA-256: `c6fc21c3acb6c2ea182510870c407b16c05cd303f31b6471ad2948dad31b58df`

Current code search on synchronized main found no direct P‑1474 object-ID record.

Next action: compare image content and CCHS provenance with the existing 1890 flood set before deciding duplicate versus new record. Similar catalog language is not enough to declare a duplicate.

### CCHS object P‑9595 — “Helen,” 1893; reconcile against existing IMG-0747 before any new ingest

Steward-supplied CCHS metadata:

- title: **"Helen", Oregon City's First Streetcar, 1893**
- description: **Oregon City's First Streetcar, "Helen", 16 Feb 1893, at 6th Street. Tracks being laid on Main Street.**
- date: **1893**
- medium: **Negative**
- negative location: **Society Collection**
- other name: **2008.008.002.095**
- other numbers: **Gardner 95; Chamber of Commerce #2**
- steward orientation: camera at/near Sixth looking south along Main toward Fifth

Exact attachment:

- filename: `Helen, Oregon City's First Streetcar looking down south down 5th from 6th,1893.jpg`
- dimensions: **2048 × 1319**
- bytes: **1,523,883**
- SHA-256: `d7666895061fc649a0cb4f7268aa69d58f78d81c0b78015caa65575a36dec702`

Current repository already contains the same or a closely related 1893 Helen scene under:

- **IMG-0747**
- `media/photos/early-main-street/IMG-0747_1893-streetcar-helen-sixth-main-ee-williams.jpg`
- **S-218 / E-198**
- existing CCHS record P‑4452
- visible E. E. WILLIAMS / DRUGS signs

Current search found no direct P‑9595 record.

Next action: directly compare P‑9595 / Gardner 95 / Chamber #2 with the existing P‑4452 / IMG-0747 record. If same frame, enrich existing provenance rather than adding a duplicate. If distinct, ingest separately.

### One 1890 aftermath/crowd image still lacks steward-supplied catalog metadata

Exact attachment:

- filename: `1890 Flood - looking south down Main (from mid 6th), 5th Street is behind the crowd - Aftermath - Oregon City.jpg`
- dimensions: **2048 × 1337**
- bytes: **677,827**
- SHA-256: `d09c1781708db9a3c830d3e47b601c90b516b95312e9c99c7bbd9c4710c5f14a`

Visible/contextual description: post-flood muddy Main Street with a large crowd and CCHS watermark; steward filename/context says looking south toward Fifth/Main.

Next action: recover CCHS catalog metadata before assigning a new record; compare against current committed flood images. Do not infer exact 501/503/505 facade identity from filename alone.

## Current photo controls

Future work should explicitly compare the pending images against these committed controls:

- **IMG-0732 / S-203 / E-183** — CCHS P‑1469, 1890 Main Street flood, 6th/Main looking southwest.
- **IMG-0733 / S-204 / E-184** — CCHS P‑1456, 1890 flood, 6th/Main looking south; repository also preserves a CCHS duplicate-object group for the same scene.
- **IMG-0747 / S-218 / E-198** — 1893 Streetcar Helen at Sixth/Main, current CCHS record P‑4452.
- 1896 Fifth/Main controls and later 1918 / 1924–28 streetscape controls already exist on current main and should be used in geometric comparison.
- The current physical-change checkpoint still treats **1911–1925** as the stronger bracket for the surviving/current 505 configuration and does not select a precise construction year or a Gates/Wolf storefront model.

## Spatial/evidence discipline

Use these labels consistently:

- **DOCUMENTED / DIRECT:** CCHS catalog metadata and what the photo visibly depicts.
- **PROJECT-STEWARD SPATIAL INTERPRETATION:** user identification of the visible frontage as corresponding to the later 501/503/505 research area.
- **NOT YET PROVED:** that a photographed 1890/1893 structure already carried later numbers, equals the surviving structure, or maps one-to-one to later parcel/storefront boundaries.

Compare fixed landmarks, intersection geometry, Sanborn footprints, lot widths, rooflines, cornices, setbacks and neighboring structures before promoting facade identity.

## Exact restart instructions

1. Fetch/sync newest `main`; do not reset/revert/force-push/overwrite newer parallel work.
2. Read current `AGENTS.md`, `RESEARCH-STANDARD.md`, this handoff, and the earlier detailed handoff `2026-09-10-steward-newspaper-photo-ingest-conversation-handoff.md`.
3. Review current `media/photo-metadata-register.md`, `media/photos/inventory.md`, `media/photos/early-main-street/README.md`, current crosswalk, and `evidence/source-captures/1911-1925-physical-change-research-checkpoint-2026-09-02.md`.
4. Re-run object-ID searches for P‑1460, P‑1474 and P‑9595 because parallel work may have advanced after this handoff.
5. Reconcile P‑9595 against existing IMG-0747 before creating any new media item.
6. Reconcile P‑1460 and P‑1474 against existing 1890 flood photos before ingest.
7. Add exact steward fingerprints to existing records when they represent alternate derivatives/aliases rather than distinct photographs.
8. Assign IDs only after re-syncing current maxima; never reuse the early provisional IMG-0727/0728/etc numbers from this conversation.
9. Preserve museum metadata separately from steward spatial interpretation.
10. Validate before and after meaningful changes and commit verified findings directly to `main`.
11. Do not send manual/institutional requests without explicit project-steward authorization.

## Conversation closeout

All meaningful newspaper-source knowledge from this conversation is already represented in canonical repository records and the earlier detailed handoff. This file updates the closeout to the latest synchronized repository state and preserves all still-pending photo metadata, exact steward-file fingerprints, provenance questions and next actions.

Main remaining work: **photo provenance/reconciliation**, not redoing the newspaper research.

No absence of evidence has been treated as evidence of absence.
