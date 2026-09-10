# 1924–1927 503/505 Main Street research — conversation handoff

Handoff date: **10 September 2026**  
Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Repository baseline immediately before this handoff write: `368260c02051f2a9513b27b4b157f2473a45dba0`  
Status: **IN PROGRESS**

This handoff supersedes `evidence/source-captures/2026-09-09-1924-1927-resume-pause-conversation-handoff.md` as the restart point for this specific 1924–1927 stream. The older file remains part of the audit trail and must not be deleted.

## Purpose of this conversation

The purpose of this research stream is to reconstruct the **1924–1927 history of 503 and 505 Main Street, Oregon City**, with special emphasis on the still-unresolved business/operator bridge between the post-1922 frontage state, the **May 1925 Sanborn uses**, and the first later named businesses.

The immediate historical questions are:

1. **Who operated the restaurant at 503 Main shown on the May 1925 Sanborn?**
2. **Who operated the billiards/cigars use at 505 Main shown on the May 1925 Sanborn?**
3. **Can the 1925 restaurant be directly bridged to the City historic-resource statement that 1926 newspaper advertisements called the 503 business `Kwality Restaurant`?**
4. **Can the 505 billiards/cigars use be directly bridged to Farr or another named operator without backdating later evidence?**
5. **Can contemporary 1924–1927 directories, telephone books, licenses, Commission records, advertisements, property records, photographs, or consultant working files establish exact dates, names, or transitions?**
6. Keep the **structural/frontage chronology** separate from the **occupancy/business chronology** unless a source directly bridges them.

This is not a narrative-fill exercise. The objective is the most defensible chronology possible while preserving uncertainty, retrieval gaps, conflicting possibilities, and source provenance.

---

# Mandatory startup for the next chat

Before doing any new research or repository changes:

1. Fetch/sync and inspect the newest `main`.
2. Do **not** reset, revert, force-push, delete, or overwrite newer parallel commits.
3. Read completely from the current repository:
   - `AGENTS.md`
   - `RESEARCH-STANDARD.md`
   - `MANUAL-FOLLOWUP.md`
4. Read this handoff completely.
5. Read the canonical captures listed below before repeating any source search.
6. Inspect newest relevant commits because parallel 503/505, Farr, Wheel, photo, newspaper, municipal, directory, and property workflows may have advanced `main` since this handoff.
7. Run `python3 scripts/validate_archive.py` before/after meaningful repository changes when the execution environment permits, or verify the repository’s equivalent validation result. Do not claim validation passed if it was not actually run.
8. Commit meaningful verified findings directly to `main`, but resync immediately before every write.
9. Do not send institutional correspondence, records requests, paid research, restricted-account actions, or fee authorizations without explicit project-steward approval.
10. OCR/search/index text is discovery only. Actual archival page images control visual verification.
11. Failed retrieval is a retrieval gap, not negative historical evidence.
12. Do not merge similarly named people/businesses or convert residence/subscriber/license/address evidence into ownership or proprietorship without a direct bridge.

---

# Canonical 1924–1927 state inherited from before this conversation

## May 1925 Sanborn — controlling direct map evidence

The May 1925 Sanborn is already visually verified and remains the direct-use control:

- **501 Main — store**;
- **503 Main — restaurant**;
- **505 Main — billiards / cigars**.

The map does **not** name the occupants/operators and does not itself prove building ownership, business ownership, or continuity into later businesses.

Therefore the correct current statements remain:

- **May 1925 — 503 Main: restaurant; business name/operator unresolved.**
- **May 1925 — 505 Main: billiards/cigars; business name/operator unresolved.**

Do not assign `Kwality` or `Farr` to those May 1925 uses without direct address/date evidence.

## 1926 Kwality secondary synthesis

The City of Oregon City historic-resource material for 503 states that:

- the building appears on the 1925 Sanborn as a restaurant;
- **1926 newspaper advertisements identify the business as Kwality Restaurant**;
- later sources use Kwality Cafe.

The City sheet has been visually rechecked. It does **not** provide the exact 1926 newspaper title, date, page, proprietor, ad wording, or footnote locator for that statement.

Thus the 1926 Kwality-at-503 statement remains a **historic-resource synthesis whose underlying advertisement has not yet been recovered**. Do not promote it to direct primary-advertisement evidence until the actual newspaper page is inspected.

## 5 January 1927 municipal Kwality text lead

Existing repository capture:

`evidence/source-captures/1927-01-05-kwality-cafe-municipal-ocr-lead.md`

A City Commission/finance text layer for **5 January 1927**, described as a continuation of the December Finance Report, includes:

- `Kwality Cafe`
- expense description `Meals`.

Status remains **OCR/TEXT ONLY — original scan not visually verified**.

It does **not** print:

- 503 Main;
- a proprietor;
- an opening date;
- continuity to the May 1925 restaurant.

It supports only that a Kwality-named food business was known to Oregon City municipal finance records around the end of 1926 / beginning of 1927.

## Farr boundary

Farr is independently established at 505 in later/other work, but **this 1924–1927 stream still lacks a direct address-bearing primary source safely placing Farr at 505 during 1924–1927**.

Do not backdate later Farr evidence into May 1925 merely because the Sanborn use is functionally compatible with a pool hall.

Parallel Farr research has continued on `main`, including later directory and aerial work. Reconcile it for chronology, but do not project post-1927 findings backward without a source.

---

# Knowledge produced by this conversation — already committed

Everything substantive learned during this continuation was preserved in four source captures before this final handoff.

## 1. Municipal retrieval + Polk/PT&T source routes

Commit: **`5e0d37a8e21f7e3de6af380f3806f958ca859fd3`**  
File: `evidence/source-captures/2026-09-09-1924-1927-municipal-retrieval-and-directory-routes-continuation.md`

Key preserved state:

- Oregon City’s current Meeting Document Archive still links the 1920–1929 Commission series, but the checked legacy HPRM/WebDrawer decade query was returning **404**.
- The City’s Laserfiche/E-Vault route was not fully usable from the research reader. Treat access failures as retrieval gaps.
- A **19 April 1926 Special Meeting** City Commission record was recovered as a 7-page text layer, printed minute pp. 193–199.
- That record remained **OCR/TEXT ONLY** because the image-render route failed.
- Bounded text checks found no `503`, `505`, `Kwality`, `restaurant`, `billiard`, `pool`, `cigar`, or `Main Street` hit in that one text layer. This is not scan-certified negative evidence.
- The record pointed to a **28 April 1926** second-reading continuation for several ordinances; that follow-up record was not recovered in the pass.
- Physical/catalog survival was established for **1923–24 and 1925–26 R. L. Polk Oregon/Washington gazetteer/business directories** through multiple sources.
- A public historical-auction record documents a **June 1927 Pacific Telephone & Telegraph directory** explicitly covering Oregon City and Clackamas County along with Portland, Salem, Vancouver, and surrounding areas.

No occupant claim was promoted.

## 2. 27 October 1926 anniversary-edition / newspaper provenance + Polk holding

Commit: **`a6951cc400fb38160053535f9329265f5010738a`**  
File: `evidence/source-captures/2026-09-09-1926-anniversary-enterprise-polk-source-provenance.md`

Key preserved state:

- Oregon City’s official historical bibliography cites an **Anniversary Edition, October 27, 1926** for Enterprise articles by C. G. Miller and Tom Miller.
- A scholarly bibliography independently identifies an article from that exact date as **Morning Enterprise, Oregon City, October 27, 1926**, volume notation `Volume 32 (LXI)`, and cites a **Museum of the Oregon Territory Library vertical file**.
- This strongly narrows the first newspaper issue to inspect for the missing 1926 Kwality advertising, but does **not** prove the Kwality ad was in that issue.
- Oregon City Public Library’s current microfilm page documents long local Enterprise holdings spanning 1926.
- The **Oregon Historical Society microfilm inventory was visually inspected** and confirms 1926 coverage for both:
  - `Morning Enterprise — June 8, 1911–Nov. 2, 1933`;
  - weekly `Oregon City Enterprise — Jan. 5, 1923–Dec. 29, 1942`.
- Therefore the 27 October 1926 issue is a **retrieval/access problem**, not merely an uncertain-survival question.
- University of Idaho Special Collections independently lists a surviving **1925–1926 Oregon and Washington Gazetteer (Polk)**.
- No defensible 1924–1927 `J. Jager` bridge was found; do not backdate undated New Kwality Cafe/J. Jager ephemera or the separate 1940 `JAGERS at 503` ad into 1926.

No occupant claim was promoted.

## 3. 1926 licensing structure / Ordinance 1090 lead

Commit: **`e691b878facddba8232af277ec745cb60f0241e0`**  
File: `evidence/source-captures/2026-09-09-1926-license-ordinance-1090-record-structure-lead.md`

Key preserved state:

- The 1963 Oregon City Municipal Code’s extracted/indexed text traces several business-definition provisions to **Ordinance 1090, 3 March 1926**, including auctioneer and bowling-alley language.
- The same later compilation traces **Billiard Room** to **Ordinance 1250, 7 March 1934**, not to Ordinance 1090.
- This is important **disconfirming evidence** against using Ordinance 1090 as a shortcut to identify or regulate the May 1925 505 billiards/cigars tenant.
- The actual 1963 code pages and original Ordinance 1090 were not visually certifiable in the research environment; specific extracted provisions remain **OCR/TEXT ONLY**.
- The later code suggests written license applications, Recorder/Commission routing, posting/inspection, and transfer procedures may have existed in the broader licensing system. Treat this only as a **record-structure lead** until original 1920s ordinance/application sources are recovered.
- The practical value is to reinforce existing `MF-017 + MF-024`: detailed license applications/receipts/ledgers could name applicant, trade, premises, date, transfer/change-of-location, etc., which annual aggregate revenue cannot.
- Do not infer that those exact fields existed unchanged in 1925–1927 without original evidence.

No occupant claim was promoted.

## 4. 1926–1927 Clackamas/Oregon City telephone-directory provenance

Commit: **`b46292ad39aa67420169943d5291360cf4c2dbc9`**  
File: `evidence/source-captures/2026-09-09-1926-1927-clackamas-telephone-directory-provenance.md`

Key preserved state:

- Public indexing of a **1988 Koler/Morrison West Linn inventory** exposes a bibliography line:
  - `Clackamas County Telephone Directory, 1920, 1926, 1927.`
- Because the very large West Linn PDF could not be rendered in the available environment, that exact 1920/1926/1927 citation remains **OCR/TEXT ONLY / visual verification required**.
- Repeated year-specific Clackamas telephone-directory citations in the same consultant corpus make this look like a systematic source class, not a one-off typo, but that is still provenance inference.
- **Visually verified Oregon City/Koler-Morrison control:** a 1990 Oregon City inventory explicitly cites `Oregon City Telephone Directory, 1916.`
- **Visually verified Wilsonville control:** its Northwest Heritage Index identifies:
  - `Telephone Directory, Oregon City, Clackamas County, Oregon, August 1932`
  - publisher **Pacific Telephone & Telegraph Co.**
- Washington State Library catalogs a 1916 PT&T regional directory including Oregon City/Clackamas County.
- The 1927 Koler/Morrison citation is compatible with the separately documented **June 1927 PT&T** auction copy, but same-issue identity is only a **working hypothesis** until title pages are compared.
- LOC’s separate Oregon per-state directory metadata dataset returned a bounded no-hit for Oregon City/Clackamas/1926/1927. That result applies only to that dataset and is not evidence that the directories did not exist.

No occupant claim was promoted.

---

# Newer parallel work on `main` that the next chat must inherit

These commits occurred after or alongside this conversation and materially improve the 1924–1927 source-recovery strategy.

## 1990 Park Place Polk methodology provenance

Commit: **`821f04923273c8b7bf9a1d7406acef9aea8cd79c`**  
File: `evidence/source-captures/2026-09-09-park-place-polk-methodology-provenance.md`

Visually verified from the actual official Oregon City PDF:

- the 1990 Koler/Morrison Park Place context statement bibliography explicitly cites an R. L. Polk **Oregon and Washington Gazetteer and Business Directory** sequence including **1925–1926**;
- the methodology says individual-property research used sources including business directories, newspapers, Sanborn maps, title records, and photographs;
- the report states that materials generated during the project were the property of Oregon City at project completion.

Research consequence: City Planning/preservation working files, worksheets, directory extracts, newspaper clippings, title notes, and consultant research files are a concrete provenance route, not mere speculation. Current survival/custody still must be established; do not assume every working file survives today.

## Library of Congress + Gale/Cengage 1925–26 Polk microfilm route

Commit: **`a969066482b311b7797b539155ab34115c90219d`**  
File: `evidence/source-captures/2026-09-09-1925-1926-polk-loc-cengage-microfilm-route.md`

This materially supersedes the earlier impression that LOC offered no Polk route:

- LOC’s **Business Directories** guide explicitly lists:
  - `Oregon / Washington Gazetteer - reel 135-146 - Business Group | 1903-20, 1923-26, 1931-32`.
- This is a different collection scope from the separate LOC Oregon per-state telephone-directory metadata dataset, so the two results are not contradictory.
- A visually inspected Gale/Cengage `City Directories of the United States — Author Index` page places the relevant Oregon/Washington Gazetteer ranges on:
  - reel 28: `1923/24-1925/26`;
  - reel 29: `1925/26-1931/32` with later missing-year notation.
- **Do not equate LOC Business Group reels 135–146 with Gale reel numbers 28/29.** No mapping between those reel-number systems is established.
- The target directory pages still have **not** been inspected.

This is now one of the strongest exact source-recovery routes for the 1925–26 Polk volume.

## 1924 photograph parallel work

Current canonical capture:

`evidence/source-captures/2026-09-09-1924-photo-hunt-checkpoint.md`

Finalization commit: **`4b196c94f2b50e04f300f2fea119268d06f67f5a`**.

Current photo boundary:

- CCHS P-267 / `S-312` / `E-284` / `IMG-0770` is dated **1924–1928** and has the target frontage spatially identified, but not an exact exposure year.
- Ralph Eddy negative No. 157 / CC0002 is an **exact-1924 Oregon City photo lead**, but the target 501/503/505 row has not been defensibly established from an archival-resolution image.
- OHS 371N5709 remains a broader 1923–1936 bluff-view lead.
- Do not call any of those an exact-1924 target-frontage photograph until the date/visibility requirements are met.

This photograph stream is complementary to, but separate from, the occupancy-identification problem.

---

# Already-reviewed municipal material that must not be duplicated

## May 1927 Commission pages

Existing `S-155` already covers the visually reviewed official City PDFs for:

- 11 May 1927, printed pp. **322–325**;
- 23 May 1927, printed pp. **328–329**.

A recheck in this conversation found no new 503/505/Main/license target item and confirmed these pages were already registered/reviewed. **Do not create duplicate source/evidence IDs or re-register them.**

The sequence points forward to the **1 June 1927 regular meeting** for ordinance continuations, but current City indexing did not expose the missing adjacent pages / June 1 scan through the routes checked here.

## 1925 Commission inventory

The repository already has a Laserfiche-derived inventory of **81 1925 minute entries / 159 listed pages** under `S-156`, but the inventory is metadata, not visual page review.

The unfinished **January 1925 scan-first batch** remains a priority whenever readable Commission scans become accessible. `MF-046` controls the readable-scan/manual gap after reasonable online recovery attempts.

Do not treat the inventory as 159 visually reviewed pages.

---

# Current evidence boundaries — do not accidentally upgrade these

## DOCUMENTED / DIRECT or visually verified controls

- May 1925 Sanborn: **501 store / 503 restaurant / 505 billiards-cigar use**.
- OHS microfilm inventory: 1926 Morning Enterprise and weekly Oregon City Enterprise ranges survive in cataloged microfilm coverage.
- Wilsonville 1932 Oregon City/Clackamas PT&T directory source-family metadata.
- Oregon City 1990 inventory bibliography citing `Oregon City Telephone Directory, 1916`.
- Park Place 1990 report visually citing the 1925–26 Polk Oregon/Washington Gazetteer and documenting Koler/Morrison research methods/source custody at project completion.
- LOC Business Directories guide and visually verified Gale/Cengage index establish a microfilm route for the 1925–26 Polk source class.

## OCR/TEXT ONLY

- 5 Jan 1927 `Kwality Cafe — Meals` City finance entry; no address.
- 19 Apr 1926 Commission record text-layer review; no scan certification.
- 1963-code ordinance-history statements used to locate Ordinance 1090 and distinguish the later billiard-room definition.
- 1988 West Linn consultant bibliography line `Clackamas County Telephone Directory, 1920, 1926, 1927` until its actual scanned page can be rendered/inspected.

## SECONDARY / HISTORIC-RESOURCE SYNTHESIS

- City statement that **1926 newspaper advertisements identify the 503 business as Kwality Restaurant**. Underlying ad still missing.
- City/1983-era retrospective ownership statements remain separate from direct deeds/tax proof.

## RETRIEVAL GAPS / ACCESS TARGETS

- actual 1926 Kwality advertisement(s);
- full 27 Oct 1926 Morning Enterprise anniversary issue;
- actual Oregon City pages in the 1925–26 Polk volume;
- exact 1926/1927 local telephone-directory volume/pages;
- original Ordinance 1090 and any directly relevant 1925–27 business-license application/receipt/transfer records;
- missing 1925 Commission scan pages / broader 1927 pages including June 1 continuation;
- consultant/property working files that may contain copied newspaper or directory evidence.

---

# Manual-callout discipline

Do **not** create duplicate manual callouts for the source routes above unless a genuinely distinct task is discovered.

Existing relevant controls include:

- **MF-010** — 1924 directory/source-identification and directory-recovery problem;
- **MF-017 + MF-024** — detailed 1925–26 license/receipt/accounting/application records;
- **MF-031** — 1923–1926 local newspaper microfilm, including the newly prioritized 27 Oct 1926 anniversary issue;
- **MF-046** — readable 1925 Commission-minute scans / coverage reconciliation;
- other property/assessment or photo callouts remain under their existing IDs.

No correspondence, staff lookup, paid research, or restricted-account action was authorized or sent in this conversation.

---

# Exact next research order

The next chat should **not restart broad searching from scratch**. Continue in this order unless newest `main` contains a verified breakthrough that changes priorities.

## Priority 1 — recover the actual 1925–26 Polk Oregon City pages

Use the now-concrete microfilm/catalog routes:

- LOC **Business Group Oregon/Washington Gazetteer reels 135–146**;
- Gale/Cengage index ranges around **reels 28/29** as a separate numbering system;
- Spokane Public Library physical 1923–24 / 1925–26 volumes;
- University of Idaho Special Collections 1925–26 holding;
- CiNii / other bibliographic controls;
- City/Koler-Morrison working files that may contain extracts.

Before interpreting entries, inspect title/copyright/front-matter frames and establish exact volume identity, year span, geographic coverage, pagination, abbreviations, and whether Oregon City has a city section, address index, or classified listings.

Then check:

- 501, 503, 505, 505½, 507 and nearby Main/Fifth controls if address indexing exists;
- Farr;
- Jager/Jager variants;
- Leland;
- Little;
- Timms;
- Kwality/Quality;
- Holman;
- Pace;
- restaurants/cafes;
- billiards/pool;
- cigars/tobacco;
- soft drinks;
- relevant classified advertisements.

A residence/address entry is not automatically business proprietorship. A business listing is not property ownership.

## Priority 2 — recover and visually inspect the 27 October 1926 Morning Enterprise anniversary issue

This is the highest-value bounded newspaper target because Oregon City preservation research explicitly cited the issue and a scholarly source identifies the Morning Enterprise issue/volume and Museum vertical-file trail.

Inspect the **entire issue page by page**, not only OCR hits, for:

- Kwality / Quality;
- 503 / 505;
- Farr;
- Jager;
- Leland / Little / Timms;
- restaurant/cafe;
- billiards/pool;
- cigars/tobacco;
- opening/new-management/move/sale/lease language;
- ads from neighboring businesses that can supply address controls.

Also check the corresponding weekly Oregon City Enterprise issue(s) around the same date because the City bibliography uses generic Enterprise wording and both title streams existed.

Do not assume the missing Kwality ad is in the anniversary edition until the page is found.

## Priority 3 — recover 1926/1927 Oregon City / Clackamas telephone directory pages

Search exact title variants around:

- `Oregon City Telephone Directory`;
- `Clackamas County Telephone Directory`;
- the longer PT&T Portland/Oregon City/Salem/Clackamas regional title;
- June 1927 PT&T issue.

Establish title/month/publisher/coverage from the actual title pages first.

Then inspect Oregon City subscriber/business/advertisement material for:

- 503 / 505;
- Kwality / Quality;
- Farr;
- Jager;
- Leland;
- Little;
- Timms;
- restaurants/cafes;
- billiards/pool;
- cigars/tobacco.

Telephone listings establish subscriber/address associations, not automatically ownership or proprietorship.

## Priority 4 — City/Koler-Morrison preservation working files

Search open/current Oregon City and SHPO digital holdings for:

- 1983-era 503/505 inventory working files;
- 1990 Park Place project files;
- 1991/92 Latourette nomination research file;
- 2000 downtown context research materials;
- directory extracts;
- newspaper clippings;
- bibliography/source-code worksheets;
- title-company notes;
- field forms.

Highest-value target: anything behind the 503 sheet’s otherwise-unsourced statement that 1926 newspaper ads called the business `Kwality Restaurant`.

Do not assume present custody from the 1990 project statement; verify survival/current repository.

## Priority 5 — municipal/license scan recovery

When public City image access works again:

1. continue the **January 1925 Commission scan-first review** from the existing 81-entry inventory;
2. retrieve/visually verify the **5 January 1927 Kwality Cafe — Meals** page and surrounding Dec 1926 finance pages;
3. inspect earlier 1926 finance/license records for Kwality variants;
4. recover the missing May/June 1927 sequence, especially the **1 June 1927** regular meeting;
5. recover original **Ordinance 1090** only to establish what it actually regulated and what records it required—do not use it as a proxy for the 505 billiards tenant;
6. prioritize individual license applications/receipts/transfers over annual aggregate revenue totals because those records are more likely to name people and premises.

## Priority 6 — 1924 photo/date refinement only when it can change the structural bracket

Do not duplicate the completed photo hunt. Resume only if an archival-resolution copy or better date evidence appears for:

- CCHS P-267 / `IMG-0770`;
- Ralph Eddy No. 157 / CC0002;
- OHS 371N5709.

The structural-photo question is separate from business occupancy.

---

# What not to do

- Do not claim `Kwality` at 503 in May 1925 from the Sanborn + later synthesis alone.
- Do not claim Farr at 505 in 1925 from functional similarity or later Farr records.
- Do not backdate J. Jager/New Kwality from undated ephemera or the 1940 JAGERS ad.
- Do not interpret the 1927 `Kwality Cafe — Meals` municipal text as an address-bearing 503 record.
- Do not treat the 19 April 1926 text-layer no-hit as a scan-certified negative.
- Do not treat catalog/search failure as evidence of nonexistence.
- Do not confuse LOC Business Group reel numbers with Gale/Cengage reel numbers.
- Do not repeat the already reviewed May 1927 `S-155` pages or allocate duplicate source/evidence IDs.
- Do not call the 1924–1927 stream ONLINE COMPLETE. It remains **IN PROGRESS**.
- Do not send manual/institutional requests without explicit authorization.

---

# Conversation commit chain

This conversation directly produced:

1. `5e0d37a8e21f7e3de6af380f3806f958ca859fd3` — **Preserve 1924-1927 municipal and directory route continuation**
2. `a6951cc400fb38160053535f9329265f5010738a` — **Preserve 1926 anniversary-edition and Polk source provenance**
3. `e691b878facddba8232af277ec745cb60f0241e0` — **Preserve 1926 licensing structure and Ordinance 1090 lead**
4. `b46292ad39aa67420169943d5291360cf4c2dbc9` — **Preserve 1926-1927 Clackamas telephone directory provenance**
5. this handoff commit — see repository history after write.

Important newer parallel commits that must be inherited rather than overwritten:

- `821f04923273c8b7bf9a1d7406acef9aea8cd79c` — **Add visual Park Place Polk research provenance**
- `a969066482b311b7797b539155ab34115c90219d` — **Add LOC and Gale 1925-1926 Polk microfilm route**
- `4b196c94f2b50e04f300f2fea119268d06f67f5a` — **Finalize 1924 photo hunt checkpoint and propagation audit**
- newer Farr/505 and other project commits on `main` should be inspected before continuing because this handoff’s baseline may already be stale.

---

# Exact restart prompt for a new chat

Continue the **1924–1927 503/505 Main Street, Oregon City historical research** from the current GitHub repository.

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`

Treat the repository as authoritative.

First:

1. Fetch/sync and inspect the newest `main`; do not reset, revert, force-push, delete, or overwrite newer parallel commits.
2. Read completely:
   - `AGENTS.md`
   - `RESEARCH-STANDARD.md`
   - `MANUAL-FOLLOWUP.md`
   - `evidence/source-captures/2026-09-10-1924-1927-conversation-handoff.md`
3. Also read the canonical continuation files referenced in that handoff, especially the 1926 anniversary-edition provenance, 1926 licensing/Ordinance 1090 lead, 1926–1927 telephone-directory provenance, Park Place Polk methodology provenance, and LOC/Gale Polk microfilm route.
4. Pick up **exactly at the handoff’s `Exact next research order`**. Do not restart broad 1923–1924 regional OCR searches, do not redo the already reviewed May 1927 `S-155` pages, and do not backdate later Farr/Kwality/Jager evidence into May 1925.
5. Prioritize recovery of the actual **1925–26 Polk Oregon City pages**, then the **27 October 1926 Morning Enterprise anniversary issue**, then the **1926/1927 Oregon City/Clackamas telephone directory**, with City/Koler-Morrison working files and municipal/license scans in parallel when accessible.
6. Visually inspect original scans whenever possible. OCR/search/index text is discovery only.
7. Keep 503 restaurant, 505 billiards/cigars, Kwality, Farr, Jager, licenses, business ownership, operation, tenancy, and property ownership as separate questions unless directly bridged.
8. Commit meaningful verified findings directly to `main` after resyncing, run/verify archive validation when possible, and record retrieval gaps/no-hits without manufacturing historical absence.
9. Do not send institutional correspondence, paid lookups, or restricted-access requests without explicit project-steward authorization.

Current controlling historical boundary at restart:

- **May 1925 — 503 Main: restaurant; name/operator unresolved.**
- **May 1925 — 505 Main: billiards/cigars; name/operator unresolved.**
- City historic synthesis reports **1926 Kwality Restaurant** advertising at 503, but the underlying advertisement is still unrecovered.
- **5 January 1927 `Kwality Cafe — Meals`** remains OCR/TEXT ONLY and addressless.
- No direct 1924–1927 exact-address primary source in this stream yet safely places Farr at 505.
- 1924–1927 research status remains **IN PROGRESS**.

No absence of evidence has been treated as evidence of absence.
