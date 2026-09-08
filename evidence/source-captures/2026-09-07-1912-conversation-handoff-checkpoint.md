# 1912 Conversation Handoff Checkpoint — 7 September 2026

Purpose: preserve the exact restart state for a new session continuing the 503/505 Main Street annual research sequence at **1912**, without overwriting or regressing newer parallel work already on `main`.

## Critical synchronization warning

At handoff preparation, `main` had already advanced to commit **460b087d591c79b71b7f04f8f148939cd4d137c6** (`Add 1916 session knowledge-preservation checkpoint`). `main` is actively advancing in parallel and must be fetched again at the start of the next session.

The temporary branch name used earlier in this conversation, `research/1912-main-street`, is **not currently present on GitHub**. Do **not** recreate it from an old SHA and do **not** attempt to merge the stale conversational branch state. The core 1912 pass from this conversation was already incorporated historically into `main` as commit `06eb3be84308740b6fff7ed90d8019470d72f8cf` (`Research: document 1912 503 pool hall and Main Street rebuilding`), and `main` contains substantial later 1912 work beyond that initial pass.

Treat the newest `main` as authoritative.

## Mandatory startup for the next session

Before any research or repository edits:

1. Fetch/sync and inspect the newest `main`.
2. Do not reset, revert, force-push, overwrite, discard, or replace newer parallel commits.
3. Read `AGENTS.md` completely.
4. Read `RESEARCH-STANDARD.md` completely.
5. Read `MANUAL-FOLLOWUP.md`.
6. Review `registers/year-status.md`.
7. Review the newest commits because 1919 / Wheel / 503 / 505 / directory / other annual workflows are actively advancing `main`.
8. Read the current 1912 core capture: `evidence/source-captures/1912-main-street-research.md`.
9. Read the 7 September 1912 Willamette/Harding source capture: `evidence/source-captures/1912-09-07-willamette-building-over-harding-drug-store.md`.
10. Review current 1912-related entries in `evidence/evidence-register.md`, `evidence/source-register.md`, `evidence/research-leads.md`, `evidence/open-questions.md`, `timeline.md`, the relevant building/business/person files, `registers/business-timeline.md`, `indexes/id-crosswalk.md`, and YAML/database mirrors before assigning IDs or propagating findings.

**Never guess the next evidence/source/person/business/media IDs from this handoff.** Parallel work has consumed many IDs since the original annual pass. Read the current registers first.

## Current certification status

Canonical `registers/year-status.md` currently lists **1912 = IN PROGRESS**.

The project standard now requires, for `ONLINE COMPLETE`, an issue inventory and **page-by-page visual review of every online-retrievable page of every relevant newspaper title**, plus the other online source classes, documented retrieval gaps, integration, and numbered manual callouts.

The existing 1912 work is a targeted reconstruction with selected visually verified pages. It is historically valuable, but it **does not certify full-year visual coverage**. Do not describe 1912 as complete or online-complete unless the current standard has actually been satisfied.

## Research method the steward explicitly requested

The user specifically asked that the annual newspaper pass not rely on OCR/search alone.

For 1912:

- build/verify the complete online issue inventory for each relevant title;
- inspect the **actual scan image for every retrievable page**;
- use OCR/search only for discovery/navigation;
- record each inaccessible page as `RETRIEVAL GAP`, not as a negative finding;
- preserve an auditable issue/page checklist;
- continue the standing `RL-024` watch for fire, demolition, construction, rebuilding, remodeling, moves, and street/grade changes between Fifth and Sixth on Main;
- keep exact addresses, relative-location wording, building identity, legal parcel identity, business ownership, operation, tenancy and property ownership separate.

The page-by-page method has proved useful as a safety net: it has surfaced small ads/local items and corrected OCR address errors, while municipal/property sources remain important for structural and legal questions.

## Important current 1912 evidence already on `main`

### 1. Visually verified 5 January Main Street address ladder

The original `Oregon City Courier` page image was visually checked because OCR corrupts several numbers.

Direct readings:

- **H. N. Smith — Pool Room, Cigars and Tobacco — 503 Main Street** (OCR misreads 603).
- **G. H. Young — The Curio Man — 507 Main Street**.
- **H. P. Brightbill — 509 Main Street** (OCR misreads 609).
- **Geo. A. Harding — 511 Main Street** (OCR is garbled; scan reads 511).

The page also gives relative anchors including Chicago Store just below the Post Office, Tolpolar opposite the Post Office, M. E. Dunn near the Post Office, Schrader near the Post Office, Clems Chop House at Fifth/Main, and Price Bros. at Sixth/Main.

Do not convert those relative locations to exact numbers without independent mapping evidence.

### 2. 503 Main — Smith pool-room / pool-hall sequence

Current main preserves:

- 5 Jan. 1912: **H. N. Smith**, pool room, **503 Main**.
- 24 Mar. 1912: **H. H. Smith** signs a pool-hall license application for his place of business at **503 Main**.
- 12 Jul. 1912: **H. H. Smith**, described as having conducted a pool hall at **Fifth and Main**, had left for Aurora to open another pool hall.

The **H. N. vs H. H. Smith initials discrepancy remains unresolved**. Do not silently merge the identities solely because the address/use fits. Current project lead tracks the conflict.

### 3. 501 Main — Palace Saloon

The current 1912 consolidated capture has a later visual-review integration for the complete four-page **19 March 1912 Morning Enterprise** issue. Page 2 directly identifies **Joe Wilson's Palace Saloon, 501 Main Street** in a liquor-license application.

This is direct 1912 numbered-address evidence and supersedes any earlier conversational statement that no exact 501 occupant had been recovered.

### 4. 505 Main — avoid a false gap narrative

The original 1912 annual pass did not recover a source that directly printed an exact **505 Main** occupant for 1912; the 5 January Chicago Store ad instead says **Main St. just below Postoffice**.

However, newer `main` contains important cross-year evidence that must be considered before making any 505 reconstruction claim:

- current archive evidence visually shows **Young's Secondhand Store with `505` over the doorway in a CCHS photograph dated 1910** (`S-149` / `E-134` / `IMG-0725`);
- current main also contains earlier direct Young/505 evidence and later address movement evidence;
- 1911 directly documents the Chicago Store at **505 Main**;
- 1912 exact-number silence for Chicago Store is therefore a coverage/address-publication issue, **not evidence that 505 was vacant**.

Read the current `timelines/505-main.md`, George Young business/person records, `RL-035`, and photo source captures before synthesizing this sequence.

### 5. Harding / Willamette Building conflict is more advanced than the initial annual pass

A visually verified **7 September 1912 Morning Enterprise** advertisement for Mrs. Adalyn Davis prints:

- **Willamette Bldg., Room 4, Over Harding Drug Store.**

This is `S-154` / `E-138` in current main and is a direct physical/vertical relationship between the named Willamette Building and Harding Drug Store.

It must be reconciled with:

- March 1911: George Young moved one door north into the Willamette Building from a Harding Building premises on Main between Fifth and Sixth (`E-085`);
- 5 Jan. 1912: Young at **507**, Brightbill **509**, George A. Harding **511** (`E-092`);
- later 1921 Freeze/Harding upstairs-address evidence.

**Do not equate Willamette Building = 507 alone. Do not overwrite Harding's directly printed January 1912 business address of 511.** Named buildings may span or relate to multiple numbered bays/upstairs spaces. Current main explicitly preserves multiple possible models rather than selecting one.

### 6. Sixth & Main / Gambrinus continuity

24 Mar. 1912 reporting identifies the **Gambrinus Saloon at Sixth and Main** and names **William Trudell** as proprietor.

This extends the chronology from:

- 1906 William Tell / Gambrinus acquisition context,
- 1910 construction of a new Gambrinus business block,
- 1911 second-story Electric Hotel annex occupancy,
- to named Gambrinus Saloon operation in 1912.

Exact numbered storefront remains unresolved unless newer main evidence has since resolved it.

### 7. Confirmed 1912 Main Street demolition/rebuilding — location still unresolved

The **10 May 1912 Courier** editorial directly says Oregon City was **tearing down buildings on Main Street** and **building new buildings in their places**.

This is genuine structural-change evidence (`E-090`) but the item gives **no block, owner, business, street number or building name**.

Do **not** convert it into evidence that 501/503/505/507, the Harding/Willamette premises, or the Fifth–Sixth block was rebuilt in May 1912 unless another source independently maps the structures.

A high-value goal remains identifying the buildings referenced by this editorial.

### 8. Schrader bakery transfer

20 Dec. 1912 reporting says Herman Schrader sold two Oregon City bakeries to **Wemmo & Haas**, one at Seventh/John Adams and one **on Main Street**. Earlier advertising placed Schrader near the Post Office.

This is a business-transfer event, not a proven exact-address or real-estate transfer.

## Existing 1912 work that should not be duplicated blindly

Current `main` already contains later 1912/related integrations beyond the initial annual pass, including work reflected by commits such as:

- `06eb3be84308740b6fff7ed90d8019470d72f8cf` — initial integrated 1912 annual pass;
- `e86d81919e2114d583dcc8eb45dd3cc649478bac` — 1912 503 pool-hall anchor / Hylton transition work;
- `03302f98d27468dd73f8f3046fb958a7c89286f6` — visual January 1912 Smith / Cox-Ward evidence;
- `ea9f04aa662d824a279ecf2f9b27d7843bb04595` — Cox-Ward 1912 transition;
- `4ed8f5aef206cc3731f9aea84d71f36a16000981` — visual July 1912 H. H. Smith exit evidence;
- `3d4c54a0efbada7ef724ebe123d59add162c5b10` — 1912–1916 Scripture Fifth Street predecessor chain;
- `f88188ca12407468e2f7062c5e4e6c830f6e03ac` — separate 1912 Oregon City Dye Works cleaning business;
- `1ef55abac36a50c9a28c9df7aef8a0a69db5221c` — 1912–1913 Enterprise address evidence;
- `9ffcb01ee80f63d9a66e7da57bb8beeeedc70e50` — verified 1912 Willamette-over-Harding integration;
- `dff81a7859d4fc68dee0fe5586b94af557a77a74` — Palace Saloon primary-page integration through 1912.

These hashes are orientation only. Read the **current files on newest main**, because later commits may have refined or superseded wording.

## Best next task for 1912

The next session should **not start by re-running targeted keyword searches**. The unresolved certification blocker is the full visual audit.

Recommended sequence:

1. On newest main, determine exactly which 1912 newspaper titles are relevant and available online.
2. Build a title → issue date → page/image count inventory.
3. Reconcile that inventory against already visually verified 1912 pages so existing verified work is credited rather than repeated unnecessarily.
4. Begin the missing page-by-page visual review from the earliest unresolved issue/page and record every page state.
5. For each page, watch not only for `501/503/505/507`, but also `509/511`, Fifth/Main, Sixth/Main, Post Office-relative clues, Harding, Willamette, Young, Smith, Chicago Store, Brightbill, Gambrinus, Schrader, construction, demolition, moving, fire, repair, new building, excavation, sales and property transfers.
6. Run cross-title checks in the `Morning Enterprise` as well as the `Oregon City Courier`; do not treat the Courier alone as the entire year.
7. As new scan-verified findings appear, propagate them under the current `AGENTS.md` cross-record audit rule.
8. Precisely log all non-rendering/missing pages as retrieval gaps and route persistent gaps into numbered manual callouts.
9. Do not change 1912 from `IN PROGRESS` until every `RESEARCH-STANDARD.md` condition for `ONLINE COMPLETE` is met.

## High-value unresolved 1912 questions

- Are `H. N. Smith` and `H. H. Smith` the same 503 pool-hall operator? Find independent identity evidence; do not merge by fit alone.
- Which specific Main Street buildings were being demolished/replaced in May 1912?
- Can the Willamette Building be directly tied to a numbered Main Street address without flattening its upstairs/multi-bay relationship?
- Can Harding Drug Store be directly numbered in 1912 after/beyond the January 511 listing and reconciled with the Willamette-over-Harding wording?
- What was the exact 1912 505 Main occupant state? Use direct 1912 evidence if available; do not infer vacancy from silence or mechanically carry forward 1911.
- How do the early 501/503/505/507 premises relate physically to later surviving buildings and to the later c.1919/c.1920 construction estimates?
- Can the May teardown/rebuild context or another 1912 source establish a specific predecessor-building replacement event at the target frontage?

## Manual / institutional context

Do not create duplicate outreach. Check current `MANUAL-FOLLOWUP.md` first.

A particularly relevant shared callout remains the **original 1906 numbering plat / Ordinance 357 implementation records** (current manual dashboard `MF-014`), because it is foundational to exact pre-/post-numbering storefront geometry. The manual dashboard and current research leads control; use their prepared drafts/routes rather than creating new duplicate correspondence.

## Handoff rule

If the next session discovers that newer parallel work has changed any 1912 interpretation, **newer `main` controls**. Preserve this checkpoint as a record of the conversation state; do not use it to overwrite later evidence, IDs, status, or wording.
