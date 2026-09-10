# 1912 Main Street Research — Conversation Reconciliation Checkpoint — 10 September 2026

Status: **KNOWLEDGE-PRESERVATION CHECKPOINT**. This file preserves the current conversation state and reconciles it against the newest authoritative `main`. It does not change the canonical 1912 year status by itself.

Repository: `rodyoung1967/main-street-archives`  
Authoritative branch: `main`  
Synchronization baseline used for this checkpoint: `5dd34eb163735453e0fb0cf4641e0e7c0e06c0c9` (`Preserve all current 505 Farr conversation knowledge`).  
Always sync newest `main` before further research because parallel workflows are active.

## Critical branch handling

The branch `research/1912-main-street` was created from the 1911-era `main` and is now stale by well over one thousand commits. **Do not merge, revive, reset from, or use that branch to overwrite current `main`.** Its verified 1912 claim-level knowledge has already been reconciled into newer canonical files on `main`.

The safe handling decision in this conversation was therefore:

1. compare the stale branch to current `main`;
2. identify whether any unique historical claim remained only on the stale branch;
3. verify current canonical 1912 files and later superseding work;
4. preserve only genuinely new conversation/process knowledge in this checkpoint.

No unique verified historical claim from the stale branch was found to be missing from current `main`.

## Canonical year status

**1912 remains IN PROGRESS.** Do not call 1912 ONLINE COMPLETE or simply “complete.” `registers/year-status.md` is the controlling status record.

The blocker is research coverage, not lack of findings: the later exhaustive standard requires complete relevant-title/issue/page inventories, page-by-page visual inspection of every online-retrievable newspaper page, other online source-class review, explicit retrieval-gap handling, final integration, and numbered manual callouts.

## Page-by-page review directive from the project steward

The project steward explicitly requested that the annual newspaper workflow continue beyond OCR/keyword searching and include page-by-page review of the *Oregon City Courier* issue-by-issue wherever the scans are retrievable.

This conversation also clarified the practical value of that method:

- it is worth retaining as a **coverage/completeness control and discovery safety net**;
- it can surface small advertisements, moves, repair notices, relative-location clues, and other material that exact-address OCR searching misses;
- the strongest discoveries may still come from other source classes such as municipal records, so page-by-page newspaper review supplements rather than replaces cross-source research;
- pages not actually viewed as faithful scans must remain `OCR/TEXT ONLY`, `RETRIEVAL GAP`, `PENDING`, or `MANUAL CALLOUT` as appropriate.

This directive is consistent with the current `RESEARCH-STANDARD.md`, which requires page-by-page visual review of every online-retrievable newspaper page before ONLINE COMPLETE certification.

## Verified 1912 findings from this conversation already preserved on current main

### 501 Main — later parallel work supersedes the earlier unresolved state

Later synchronized work on `main` visually verified **19 March 1912 Morning Enterprise** evidence identifying **Joe Wilson's Palace Saloon at 501 Main Street** (`E-104` / `S-118`). Any earlier 1912 summary text saying 501 was unresolved is superseded by that direct exact-address evidence.

### 503 Main — Smith pool room / pool-hall sequence

Current canonical `E-089` preserves the 1912 Smith sequence:

- **5 January 1912:** visually verified page shows **H. N. Smith — Pool Room, Cigars and Tobacco — 503 Main Street**. OCR incorrectly reads the address as 603.
- **24 March 1912:** a legal notice signed **H. H. Smith** states his pool-hall place of business was **503 Main Street**.
- Later July reporting places H. H. Smith's pool hall at the Fifth-and-Main context before his departure for Aurora.

Do **not** silently merge H. N. Smith and H. H. Smith; the initials conflict remains unresolved (`RL-037`).

### 505 Main

No direct exact-number 1912 occupant is currently established in the canonical annual synthesis. The 5 January Chicago Store advertisement uses the relative wording **Main St. just below Postoffice**. The exact 505 address documented in 1911 must not be mechanically carried forward into 1912 without continuity evidence. Lack of an exact-number hit is not vacancy evidence.

### 507 / 509 / 511 Main — 5 January address ladder

Visual inspection of the 5 January 1912 *Oregon City Courier* page establishes:

- **G. H. Young — 507 Main**;
- **H. P. Brightbill — 509 Main**;
- **Geo. A. Harding — 511 Main**.

This visual review corrects OCR errors: Smith's 503 is misread as 603, Brightbill's 509 as 609, and Harding's number is garbled by OCR. The scan controls the archive interpretation.

George Young at 507 strengthens—but does not by itself prove—the hypothesis that his March 1911 Willamette Building premises were 507. Later 1912 evidence (`E-138` / `S-154`) describing the **Willamette Bldg., Room 4, Over Harding Drug Store** shows the building-name/address geometry is more complex than a simple one-building/one-number equation.

### Sixth & Main / Gambrinus

The 24 March 1912 newspaper page identifies the **Gambrinus Saloon at Sixth and Main** and names **William Trudell** as proprietor (`E-091`). This extends the documented sequence from the 1906 William Tell/Gambrinus property transfer, through the 1910 new Gambrinus block and 1911 Electric Hotel annex, into 1912 saloon use. No exact numbered Main storefront is assigned from the intersection wording alone.

### Main Street demolition and rebuilding

The 10 May 1912 *Oregon City Courier* states in the present tense that Oregon City was **tearing down buildings on Main Street and building new buildings in their places** (`E-090` / `S-105`).

This is direct evidence of active Main Street structural replacement in 1912, but it does **not** identify the block, lot, owner, business, or exact number. It must not be mapped to 501/503/505/507 without an independent bridge. `RL-038` remains open.

### Schrader bakery sale

Herman Schrader sold two Oregon City bakeries in December 1912, including one on Main Street, to **Wemmo & Haas** (`E-093`). Earlier advertising placed Schrader near the Post Office. The exact Main Street number remains unresolved.

## Later synchronized 1912 work that also controls

The current 1912 handoff on `main` records later work beyond the stale branch, including:

- `E-104` / `S-118` — Palace Saloon / Joe Wilson at **501 Main**, visually verified;
- `E-138` / `S-154` — September 1912 Willamette Building wording over Harding Drug Store;
- `E-282` / `S-310` — 19 January 1912 page 8 visually verified: **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot**. That item prints no exact street number, so the independent 5 January 511 Main evidence remains the address control.

These later records supersede earlier OCR-only or unresolved statements where applicable.

## Construction / demolition / fire handling

Continue the standing `RL-024` watch for new construction, demolition, building removal/moving, fire, major remodeling, excavation, permits, redevelopment, and street/grade work on Main between Fifth and Sixth.

For 1912 specifically, preserve two separate evidence tracks:

1. **exact-address occupancy evidence** at 501/503/507/509/511; and
2. **citywide Main Street structural-change evidence** from the May teardown/rebuilding statement.

Do not merge those tracks unless a source independently maps a specific demolition/rebuild event to the target block/address.

## Resume point

When 1912 work resumes:

1. sync newest `main` and review new parallel commits;
2. follow `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md`, and `registers/year-status.md`;
3. continue the exhaustive title → issue → page visual audit rather than repeating already-integrated targeted findings;
4. prioritize unresolved coverage and `RL-037` / `RL-038` rather than recreating `E-089`–`E-093`;
5. never treat source silence or retrieval failure as evidence of vacancy, demolition, closure, or non-use;
6. do not send institutional/manual requests without explicit project-steward authorization.

## Propagation decision

No master evidence/source/timeline/building/business/person/YAML rewrite is required from this checkpoint because the historical facts developed in the current conversation are already present—and in some cases superseded by later verified work—on current `main`. Rewriting those canonical files from the stale branch would risk regression. This checkpoint is therefore the appropriate collision-free preservation action.
