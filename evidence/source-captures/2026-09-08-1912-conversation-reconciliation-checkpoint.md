# 1912 Conversation Reconciliation / Save Checkpoint — 8 September 2026

Status: **KNOWLEDGE-PRESERVATION / CONVERSATION CHECKPOINT**. This file preserves and reconciles the 1912 work from the current conversation against the newest authoritative `main`. It does **not** create a new historical claim, source ID, evidence ID, person, business, building, or closeout status by itself.

## Why this checkpoint exists

A 1912 research branch created earlier in this conversation (`research/1912-main-street`) was later found to be stale after substantial parallel work landed on `main`. At the reconciliation check, the branch was **9 commits ahead but 1,325 commits behind** current `main`, with merge base `23664acf5edeeba1a9430ac0af270702a27247fb`. The stale branch must therefore **not** be merged, rebased by force, or used to overwrite the newer archive.

The verified 1912 findings developed in this conversation were then checked against current `main`. They are already preserved in the canonical 1912 research/evidence structure, including `evidence/source-captures/1912-main-street-research.md`, `E-089`–`E-093`, `S-102` onward, timeline/building/business/person records, YAML mirrors, and later parallel additions.

## Current authoritative year status

Under the current `RESEARCH-STANDARD.md`, **1912 remains IN PROGRESS**. The current `registers/year-status.md` explicitly says the 1912 pass is still a targeted reconstruction with selected visual pages and that a full title/issue/page inventory and other-source audit are not yet certified.

Do **not** describe 1912 as ONLINE COMPLETE until the exhaustive requirements are satisfied, especially page-by-page visual review of every online-retrievable page of every relevant issue and documentation/manual callouts for remaining retrieval gaps.

## Verified 1912 findings preserved on current main

### Exact Main Street address ladder — 5 January 1912

Visual inspection of the actual *Oregon City Courier* page corrects several OCR errors and establishes:

- **H. N. Smith — Pool Room, Cigars and Tobacco — 503 Main Street**;
- **G. H. Young — The Curio Man — 507 Main Street**;
- **H. P. Brightbill — 509 Main Street**;
- **Geo. A. Harding — 511 Main Street**.

The page also gives relative Post Office/Fifth/Sixth anchors, but those are not converted to exact numbers without independent mapping evidence.

### Smith pool-room / pool-hall sequence at 503

- 5 Jan. 1912: **H. N. Smith** visually verified at **503 Main**.
- 24 Mar. 1912: **H. H. Smith** legal notice applies for a pool-hall license at **503 Main Street**.
- 12 Jul. 1912: **H. H. Smith**, formerly conducting a pool hall at **Fifth and Main**, leaves for Aurora to open a pool hall there.

The **H. N. / H. H. initials conflict remains unresolved** and must not be silently normalized or merged without independent identity evidence.

### 501 Main / Palace Saloon

Parallel work now present on current `main` adds stronger 1912 context beyond the earlier conversation branch: the visually reviewed 19 March 1912 *Morning Enterprise* directly identifies **Joe Wilson's Palace Saloon at 501 Main Street** (`S-118` / `E-104`). Later June material uses **Joseph Wilson** at the Palace Saloon / Fifth-Main context; Joe=Joseph is treated as a strong same-business/location inference, not as explicit identity proof from one source.

### Gambrinus at Sixth & Main

A 24 March 1912 report identifies the **Gambrinus Saloon at Sixth and Main** and names **William Trudell** as proprietor. This extends the documented Gambrinus chronology after the 1906 William Tell/Gambrinus property transfer, the 1910 new Gambrinus block construction, and 1911 Electric Hotel annex occupancy. Exact numbered storefront remains unresolved.

### Main Street demolition/rebuilding — 10 May 1912

The *Courier* states in the present tense that Oregon City was **tearing down buildings on Main Street and building new buildings in their places**. This is direct evidence that 1912 was a Main Street structural-change year.

Critical limitation: the editorial gives **no block, owner, business, lot, or exact street number**. It must not be used as proof that 501, 503, 505, or 507 was demolished/rebuilt in 1912 unless an independent source maps the work to the target block.

### Schrader bakery transfer — December 1912

Herman Schrader sold two Oregon City bakeries, including one **on Main Street**, to **Wemmo & Haas**. Earlier advertising places Schrader near the Post Office, but no exact Main Street number is established by this transfer item.

## Address-status handling

Current direct 1912 evidence includes at least:

- **501 Main:** Palace Saloon / Joe Wilson, direct exact-address evidence from March 1912.
- **503 Main:** Smith pool-room/pool-hall sequence, direct exact-address evidence.
- **505 Main:** do not infer continuity solely from the Chicago Store's 1911 505 listing; the January 1912 page uses relative wording (`Main St. just below Postoffice`).
- **507 Main:** G. H. Young, direct exact-address evidence on 5 January.
- **509 Main:** H. P. Brightbill, direct exact-address evidence on 5 January.
- **511 Main:** Geo. A. Harding, direct exact-address evidence on 5 January.

Missing exact listings are research-status statements only, not vacancy evidence.

## Building-continuity guard

Exact 1912 address occupancy does **not** prove that the surviving present 503/505 structures already existed. Address continuity and building continuity remain separate questions. The May demolition/rebuilding statement makes structural change in this era important to investigate, but it does not identify the target premises.

## Newspaper-review status

The page-by-page method materially helped by:

- correcting OCR address errors on the 5 January page;
- exposing the dense 503/507/509/511 address ladder;
- recovering the May demolition/rebuilding statement;
- supporting smaller business/location transitions that keyword searches alone can miss.

However, the current 1912 annual record explicitly states that some issue/page images remain unreviewed or not fully inventoried under the later exhaustive standard. Those pages are not counted as visually reviewed. 1912 therefore remains **IN PROGRESS**.

## Cross-record propagation decision

This checkpoint reconciles knowledge already integrated into the newer authoritative `main`; it does not establish a new entity fact. No new source/evidence/person/business/building IDs or YAML relationships are warranted from this checkpoint itself. Existing current-main records control where they contain later or stronger evidence.

## Resume rule

When 1912 work resumes:

1. sync latest `main` first and reread `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md`;
2. do **not** merge the stale `research/1912-main-street` branch;
3. use `registers/year-status.md` and the current `evidence/source-captures/1912-main-street-research.md` as the authoritative annual-state controls;
4. complete the missing full newspaper title/issue/page inventory and page-by-page visual review required for ONLINE COMPLETE;
5. preserve all retrieval gaps as gaps/manual callouts, never negative evidence;
6. continue the construction/demolition/fire watch without mapping the May 1912 demolition statement to 501/503/505/507 absent independent location evidence.
