# 2026-09-10 — steward newspaper/photo-ingest conversation handoff

Status: **conversation knowledge saved / photo-ingest continuation pending**

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Pre-write synchronized HEAD: **c80f7a6d8f78b235dc815f6f64f32319580ff0d4** — `Fix CCHS catalog object references in handoffs`

## Purpose of this conversation

This conversation had two connected purposes:

1. **Steward-supplied source ingest.** Check every newspaper PDF and photograph supplied by the project steward against the authoritative repository, avoid duplicate binaries/IDs, preserve missing source files, integrate only historically supportable claims, and keep source/evidence/timeline/YAML/media records synchronized.
2. **501/503/505 physical-history reconstruction.** Use the newly supplied primary newspaper pages and early Main Street photographs to improve the chronology and spatial understanding of the Fifth/Main frontage while keeping address, business, building, ownership, tenancy, licensing, parcel identity and physical-building continuity separate.

The repository remains authoritative. Future work must fetch/sync current `main`, read current `AGENTS.md` and `RESEARCH-STANDARD.md` completely, inspect newer parallel commits, preserve existing IDs, and validate before/after meaningful changes.

No institutional/manual request was authorized or sent in this conversation.

---

## Validation repair performed immediately before this handoff

The latest pre-handoff `main` had a failing archive validator because three conversation-handoff files used CCHS photograph object numbers with the ASCII `P-###` pattern, which the validator interpreted as person IDs.

The affected catalog numbers were CCHS photo objects, **not people**:

- CCHS object P‑267
- CCHS object P‑372
- CCHS object P‑391

The three handoff files were corrected to use a non-person catalog notation (nonbreaking hyphen), without changing the historical meaning:

- `evidence/source-captures/2026-09-10-1922-fire-young-poolhall-conversation-save.md`
- `evidence/source-captures/2026-09-10-1924-1927-conversation-handoff.md`
- `evidence/source-captures/2026-09-10-flor-wheel-overlap-session-handoff.md`

The validator then **PASSED** on HEAD `c80f7a6d8f78b235dc815f6f64f32319580ff0d4` before this handoff was written.

---

# Newspaper-ingest knowledge from this conversation

Most newspaper work from this conversation is already integrated into the canonical repository. Do **not** recreate source/evidence IDs or repeat ingestion merely from this handoff; use the current source/evidence registers and source-capture files as controlling records.

Important findings preserved during this conversation include:

## Fifth Street Restaurant, 1916–1922

The supplied pages established or strengthened a dated sequence:

- **31 Aug 1916** — Fifth Street Restaurant inspection score 75.3.
- **1 Sep 1916** — W. W. Pollock is directly associated with the Fifth Street restaurant in the inspection/listing context.
- **31 Oct 1919** — W. W. Pollock is explicitly described as **conducting the Fifth street restaurant** and was fined for sanitary conditions.
- **19 Nov 1920** — Guy Proffit was reported as **interested in the Fifth Street Restaurant** and retaining his interest; do not convert “interest” into sole ownership or real-estate ownership.
- **26 Aug 1921** — fight occurred in the Fifth Street Restaurant; place-use evidence only.
- **18–21 Jul 1922 fire period** — Fifth Street Restaurant destroyed; one Enterprise account says surname-only **Blakely owned the Fifth street restaurant** immediately after naming L. E. Blakely, while the building is reported owned by **C. P. Gates**. Other 1922 accounts use J. Blake / Ed. Blake / Ed Gage variants. Keep the conflict.

Do not infer uninterrupted operator continuity, exact numbered address, or legal title from this sequence.

## Wolf & Miller / 505 versus 503 conflict

The supplied 1918 pages materially strengthened the address conflict:

- **20 Sep 1918** — Wolf & Miller directly at **505 Main**.
- **10 Oct 1918** — Wolf & Miller directly at **505 Main**.
- **31 Oct 1918** — Wolf & Miller printed at **503 Main**.

Preserve this as an **UNRESOLVED CONFLICT**. Do not silently correct the newspaper or infer a move without an independent bridge.

The 10 Oct page also directly prints **A. A. Mundin, 514 Main**; a 20 May 1921 article says W. O. Witham purchased **A. A. Munden's furniture store at 514 Main**. Preserve spelling variation and the separate unresolved 614 reading elsewhere.

## Young / Chicago Store / George Harding

This conversation preserved primary pages showing:

- **16 Aug 1907** — Young's Second Hand Store at exact **505 Main**.
- **31 Mar, 7 Apr, 14 Apr, 28 Apr 1911** — Chicago Store at exact **505 Main**.
- **25 Dec 1913** — Chicago clothing store on Main south of the post office was gutted by fire; the report explicitly says **the building was owned by George Harding**. The fire article itself does not print 505. Mapping it to the independently documented 505 Chicago Store is a **STRONG CROSS-SOURCE INFERENCE**, not deed-level proof or surviving-building continuity.

## Palace Saloon chronology / address conflict

Supplied pages added or reinforced:

- Ralph O. Smith Palace Saloon license applications at **Fifth/Main** in 1909.
- **31 Dec 1909** — another direct Ralph O. Smith / Palace Saloon / Fifth-Main application.
- **17 Jun 1910** and **24 Jun 1910** — E. R. Case / Palace Saloon notices visibly print **510 Main street** in consecutive weekly issues.
- Later Palace evidence directly uses **501 Main** under Joe/Joseph Wilson.

The repeated 1910 `510 Main` wording is real and must not be normalized to 501. Because the second notice may repeat the same legal-copy error, the 510-vs-501 relationship remains an **UNRESOLVED CONFLICT / transition question**.

## Dr. Freeze / 505 versus 505½

The current rule created in this conversation is important:

**505½ is an address designation, not a floor designation.**

The documented sequence includes:

- 8 Apr 1921 — **505½ Main**
- 13 May 1921 — **505 Main**
- 20 May 1921 — **505½ Main**
- 28 Oct 1921 — **505 Main**
- 30 Jun 1922 — **505½ Main**, with move after July 1 to 207 Masonic Building

This alternation does **not** prove an upstairs/ground-floor move or any particular room arrangement. Plausible physical arrangements include same-floor side-by-side, front/rear, upper-floor, or another subdivision. Keep 507½ separate because the earlier 507½ evidence includes “over Harding Drug Store,” which does support an upper-floor inference for that earlier location.

The neutral 505½ wording was propagated into the Dr. Freeze business/person/source/timeline records.

## Other steward-page findings already integrated

- **18 Oct 1940** — `JAGERS` advertised at exact **503 Main**, “Cozy place for A Tasty Pickup.” Do not merge automatically with J. Jager / New Kwality Cafe.
- **1 Mar 1907** — R. A. Sawyer purchased Charles Albright's meat business and continued at the “old stand,” Fifth/Main. Do not force a 501/503/505 number.
- **20 Mar 1908** — Justin & Hitchman and A. J. Surber separately applied at Fifth/Main; shared intersection wording does not prove same room or succession.
- **18 Mar 1910** — M. Justin named the **Mt. Hood Cafe** at Fifth/Main. Do not automatically equate M. Justin with the earlier Justin & Hitchman partnership.
- **11 Feb 1910** — William Andresen / H. C. Stevens 60×210 Main-to-Water property and proposed brick construction; no safe bridge to 503/505 was established.
- **4 Jun 1920** — A. Leland permitted to operate a pool hall at **505½ Main** and erect an electric sign.
- **13 Feb 1920** — Clem Dollar was proprietor of a pool hall on Main between Fifth and Sixth; no numbered address. Keep separate from Leland unless bridged.

---

# Early Main Street photograph conversation — current authoritative state

The photo question evolved while parallel repository work continued. Earlier chat statements that “none of the four photos is in the repo” are now stale. Current `main` contains substantial additional photo integration. Always use current `media/photo-metadata-register.md` and `media/photos/inventory.md`.

At the pre-handoff sync, the photo inventory reported **77 committed raster files / 50 photographs-aerials**, and later media IDs already extend through at least `IMG-0770`. Therefore **do not reuse the earlier provisional IMG-0727/0728/etc assignments from this chat**. Assign only after re-syncing current IDs.

## A. CCHS object P‑1469 — already integrated

Steward metadata supplied in this conversation:

- Title: **1890 Flood - Oregon City Main Street**
- CCHS object: **P‑1469**
- Date: **1890**
- CCHS description: **Oregon City Main Street, 6th and Main, looking southwest. Unidentified people. Flooding. Debris.**
- Medium: Photographic Paper
- Steward directional note: **6th & Main looking south toward the Fifth Street intersection** (the user's wording at one point was “looking south down 5th St”; preserve as steward interpretation, not museum metadata).

Exact steward attachment fingerprint now recoverable in this conversation environment:

- filename: `Oregon City Main Street, 6th & Main, looking southwest down main.  (Clackamas County Historical Society).jpg`
- dimensions: **2048 × 1489**
- bytes: **677,988**
- SHA-256: `2f7243e7a8fd1fb6d444654796de5eb62836c20e75da4cc40568e547267bfc26`

Current repository state:

- media: **IMG-0732**
- source/evidence: **S-203 / E-183**
- canonical path: `media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg`
- current repository record says the institutional CCHS derivative is preserved and exact byte identity to the earlier steward upload was not claimed.

**Next action:** update the existing P‑1469 provenance record with the steward attachment fingerprint above if it is not already present. Do not create a second photo record.

## B. CCHS object P‑1460 — metadata supplied; direct object-ID search currently absent

Steward metadata:

- Title: **1890 Flood - Oregon City Main Street**
- CCHS object: **P‑1460**
- Description: **Willamette River Flood 1890. Main Street Oregon City. Looking south from center of blocks between 6th and 5th streets. Unidentified people.**
- Date: **1890**
- Medium: Photographic Paper
- Steward spatial interpretation: photo taken from the north end / between Sixth and Fifth looking south; **the two men on the right are standing in front of the building/frontage associated with the later 501–505 Main research area**.

Exact attachment:

- filename: `Flood 1890 on Main Street Oregon Citiy.  Looking south from north endof 5th street.jpg`
- dimensions: **2048 × 1500**
- bytes: **676,604**
- SHA-256: `2dd929aa3a479cd7e7e20d7ee453e7fb1c5694c784178a042850f05629dd5be6`

Current repo search finds **no P‑1460 record by object ID**.

**Next action:** compare visually/provenance-wise against the current CCHS flood set (especially IMG-0732 / P‑1469 and IMG-0733 / P‑1456) before assigning a new media/source/evidence ID. If distinct, ingest it. Keep the 501–505 identification steward-attributed and do not backdate modern street numbers or building identity to 1890 without cross-source geometry.

## C. CCHS object P‑1474 — metadata supplied; direct object-ID search currently absent

Steward metadata:

- Title: **1890 Flood - Main Street After Waters Resided - Oregon City, Oregon**
- CCHS object: **P‑1474**
- Description: **1890 Flood, after the water resided, Main Street, Oregon City, Oregon.**
- Date: **1890**
- Medium: Photographic Paper
- Steward spatial interpretation: **the building/frontage corresponding to the later 501–505 Main research area is directly on the left**.

Exact attachment:

- filename: `1890 Flood, after the water resided, looking north from 5th & Main Street, Oregon City, Oregon (503 & 505 1st on the laft & blacksmith visible on the right).jpg`
- dimensions: **2048 × 1174**
- bytes: **653,119**
- SHA-256: `c6fc21c3acb6c2ea182510870c407b16c05cd303f31b6471ad2948dad31b58df`

Current repo search finds **no P‑1474 record by object ID**.

**Next action:** compare against existing 1890 flood photographs before ingest. Note that current repo already contains IMG-0733 / CCHS P‑1456, whose CCHS metadata also describes Main Street looking south after flood waters receded. Similar wording alone is not enough to call P‑1474 a duplicate; compare image content and CatalogIt provenance.

## D. 1893 streetcar “Helen” — user supplies CCHS P‑9595, while repo already has same/similar scene under another CCHS record

Steward-supplied metadata:

- Title: **"Helen", Oregon City's First Streetcar, 1893**
- CCHS object: **P‑9595**
- Description: **Oregon City's First Streetcar, "Helen", 16 Feb 1893, at 6th Street. Tracks being laid on Main Street.**
- Date: **1893**
- Medium: Negative
- Negative location: Society Collection
- Other name: **2008.008.002.095**
- Other numbers: **Gardner 95; Chamber of Commerce #2**
- Steward orientation: camera at/near Sixth looking south along Main toward Fifth.

Exact attachment:

- filename: `Helen, Oregon City's First Streetcar looking down south down 5th from 6th,1893.jpg`
- dimensions: **2048 × 1319**
- bytes: **1,523,883**
- SHA-256: `d7666895061fc649a0cb4f7268aa69d58f78d81c0b78015caa65575a36dec702`

Current repository already contains:

- **IMG-0747**
- `media/photos/early-main-street/IMG-0747_1893-streetcar-helen-sixth-main-ee-williams.jpg`
- **S-218 / E-198**
- current repository capture identifies a CCHS catalog record **P‑4452** for an 1893 “Streetcar Helen / Oregon City's First Streetcar” scene and records visible **E. E. WILLIAMS** and **DRUGS** signs.

The user-supplied P‑9595 may be a duplicate/alternate CCHS catalog record for the same photograph or a closely related frame. **Do not create a duplicate media item until the images and catalog records are compared directly.**

**Next action:** compare P‑9595 / 2008.008.002.095 / Gardner 95 / Chamber #2 against the existing P‑4452 / IMG-0747 record. If same scene, update existing provenance with the additional institutional aliases and the exact steward-file fingerprint above. If genuinely distinct, ingest separately.

## E. One original 1890 aftermath image still lacks steward-supplied catalog metadata

Among the initial group of four flood/street photographs, one image remains without a catalog object number supplied in this conversation.

Exact attachment currently recoverable:

- filename: `1890 Flood - looking south down Main (from mid 6th), 5th Street is behind the crowd - Aftermath - Oregon City.jpg`
- dimensions: **2048 × 1337**
- bytes: **677,827**
- SHA-256: `d09c1781708db9a3c830d3e47b601c90b516b95312e9c99c7bbd9c4710c5f14a`

Visible scene: post-flood muddy Main Street with a large crowd; CCHS watermark; looking south toward Fifth/Main according to steward filename/context.

**Next action:** obtain or recover CCHS catalog metadata before assigning a new record, and compare against the existing 1890 flood set. Do not infer exact 501/503/505 facade mapping from filename alone.

---

# Existing 1890/1893 photo controls that future work must compare against

Current repository already contains important controls:

- **IMG-0732 / S-203 / E-183** — CCHS P‑1469, 1890 Main Street flood, 6th/Main looking southwest.
- **IMG-0733 / S-204 / E-184** — CCHS P‑1456, 1890 Flood - Oregon City at 6th and Main Street Looking South; CCHS duplicate group includes P‑1456 / P‑1616 / P‑5519 / P‑8885. The steward-supplied P‑1456 file in that existing record is 2048×1543, SHA-256 `9c684f8f59ec7e78c894f1e77b70ca5094e976994a3644244b6a1ded6631e1cb`.
- **IMG-0747 / S-218 / E-198** — 1893 Streetcar Helen at Sixth/Main; existing CCHS record P‑4452; visible E. E. WILLIAMS / DRUGS signs.
- Later current-main photo work also includes 1896 Fifth/Main controls (IMG-0765 / IMG-0766) and 1918/1924–28 elevated streetscape controls (IMG-0769 / IMG-0770).

Do not assume that identical/similar captions mean identical photographic frames. Compare image content, CCHS object IDs, media UUIDs, and derivative fingerprints.

---

# Spatial interpretation discipline for the early photographs

Project-steward identifications are valuable but must remain attributed unless independently bridged.

Safe wording:

- **DOCUMENTED / DIRECT:** what CCHS catalog metadata says about date/location/direction and what the image visibly depicts.
- **PROJECT-STEWARD SPATIAL INTERPRETATION:** identification of the visible frontage as corresponding to the later 501/503/505 research area.
- **NOT YET PROVED:** that any visible 1890/1893 building already carried later street numbers, that a pictured predecessor equals a surviving building, or that modern parcel/storefront boundaries map one-to-one onto the earlier facades.

The photo program should compare these views with Sanborn geometry, fixed landmarks, street/intersection position, rooflines, lot widths, cornices, neighboring structures, and later photographs.

---

# Exact restart instructions

Continue the steward-source / early-photo integration for the 503/505 Main Street project.

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`

1. Fetch/sync newest `main`; do not reset, revert, force-push, delete, renumber or overwrite newer parallel commits.
2. Read completely:
   - `AGENTS.md`
   - `RESEARCH-STANDARD.md`
   - this handoff: `evidence/source-captures/2026-09-10-steward-newspaper-photo-ingest-conversation-handoff.md`
3. Review current:
   - `media/photo-metadata-register.md`
   - `media/photos/inventory.md`
   - `media/photos/early-main-street/README.md`
   - `evidence/source-captures/1911-1925-physical-change-research-checkpoint-2026-09-02.md`
   - current Sanborn/photo comparison files.
4. Re-run repository searches for CCHS objects P‑1460, P‑1474 and P‑9595 because parallel work may have integrated them after this handoff.
5. Reconcile **P‑9595** with existing **IMG-0747 / P‑4452** before adding any duplicate.
6. Reconcile **P‑1474** and **P‑1460** against the current 1890 flood-photo set, including IMG-0732 / P‑1469 and IMG-0733 / P‑1456.
7. Add the exact steward-file fingerprints in this handoff to existing records whenever the repository currently has only an institutional derivative.
8. If an image is distinct and missing, assign the next unused IMG/S/E/T/RL IDs only after re-syncing.
9. Preserve museum metadata separately from project-steward spatial interpretation.
10. Validate before and after meaningful writes and commit verified changes directly to `main`.
11. Do not send institutional/manual requests without explicit project-steward authorization.

---

# Conversation closeout statement

The newspaper findings from this conversation have already been integrated into current repository records and should not be re-created from scratch.

The main unfinished work from this conversation is **photo provenance/reconciliation**, especially:

1. P‑1460 1890 flood image;
2. P‑1474 1890 aftermath image;
3. P‑9595 1893 “Helen” record versus existing P‑4452 / IMG-0747;
4. addition of the exact steward P‑1469 attachment fingerprint to the existing IMG-0732 record;
5. recovery of catalog metadata for the still-unidentified 1890 aftermath/crowd image.

No absence of evidence has been treated as evidence of absence.
