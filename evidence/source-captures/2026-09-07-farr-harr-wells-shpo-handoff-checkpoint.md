# Farr → Harr → Well's / 505 Main SHPO handoff checkpoint — 7 September 2026

## Purpose

This checkpoint preserves the exact state of the active 505 Main occupancy-provenance research stream before a chat handoff. It is not a year closeout and does not change any year-level research status.

The immediate historical question is the business/occupancy sequence at **505 Main Street, Oregon City** from **Farr's Pool Hall** through **Harr's Recreation Center** and then **Well's Recreation**, with business operation, business ownership, building ownership, tenancy, and liquor licensing kept separate unless a source explicitly connects them.

## Repository state at handoff

- Branch: `main`
- Main observed immediately before this checkpoint: `fc1358494601d83d19d2f64a3d7366f694ce40e9` (`Propagate 1967 Wheel date correction`).
- The archive validation workflow for that observed HEAD completed successfully before this checkpoint was written.
- Parallel 503/Wheel/Floyd/Flor workflows were actively advancing `main`; the next researcher must fetch the newest `main` and must not reset or overwrite newer commits.

## Policy controls to re-read before continuing

Read current `AGENTS.md` and `RESEARCH-STANDARD.md` completely before new research or repository changes. In particular:

- original archival scans must be visually inspected whenever available;
- OCR/search text is discovery/navigation evidence unless the scan is actually viewed;
- absence/no-hit is not negative evidence;
- keep similarly named people/businesses separate unless contemporary evidence bridges them;
- keep business operation, business ownership, building ownership, tenancy, licensing, trade name, address identity, and physical-building identity separate;
- preserve provenance for every material finding;
- after meaningful evidence changes, audit timeline, building, business, person, open-question, research-lead, registers, crosswalks, and YAML/database records.

## What has now been completed in this stream

### 1. C. P. Farr municipal recreation-rent false path is separated from 505

The 1944–1946 municipal recreation-rent series previously considered as a possible Farr/Harr clue now has an exact February 1946 premises address of **708 Monroe**, not 505 Main. The payee `C. P. Farr` is strongly identified as **Clarence P. Farr** (`P-395`), distinct from **Edwin F. Farr** of Farr's Pool Hall.

Canonical records already synchronized:

- `S-273`–`S-276`
- `E-247`–`E-249`
- `P-395` Clarence P. Farr
- `B-017` 708 Monroe

This thread should not be reused as evidence for Farr's Pool Hall, Harr's Recreation Center, or the Farr→Harr transition at 505.

### 2. Exact Oregon SHPO resource for 505 Main recovered

The official Oregon SHPO Historic Sites GIS query returned one Oregon City record matching 505 Main:

- **RESOURCE_ID: 30539**
- resource/business label: **505 Tavern**
- address: **505 Main St, Oregon City**
- resurvey date in database: **01/19/2009**
- database year-built field: **1940**
- original use: Commercial: General
- style: Vernacular
- eligibility: not eligible/non-contributing

The raw official SHPO response and site-summary retrieval were preserved in the repository in the earlier SHPO retrieval commits, including `f2fa72ef…`, `208a4f6d…`, and `c532a418…`.

### 3. SHPO `30539.pdf` inventory scan recovered and visually reviewed

The original SHPO scanned inventory form for resource **30539 / 505 Main** was recovered, preserved, rendered, and visually inspected. The integration commit is:

- `67964c19c02ee3d0fb1fdc16c3801eef488276fb` — **Integrate 505 SHPO 30539 visual review**

Canonical source/evidence:

- `S-284` — Oregon SHPO resource 30539, 505 Main May 2000 Historic Resource Survey Form
- `E-257` — May 2000 survey visually confirms Harr 1945 and Well's 1953 directory-synthesis wording
- `E-258` — May 2000 survey owner field names Richard and Sheila Wiitanen

### 4. What the May 2000 form actually establishes

The visually inspected form says, in substance:

- **"The 1945 city directory lists Harr's Recreation Center at 505 Main."**
- It later reports the property in the **1953 city directory as "Well's Recreation."**
- The form's wording/spelling **"Well's Recreation"** is therefore scan-certified as the survey's wording.
- Page 3 records **Richard and Sheila Wiitanen** in the owner field, giving an official-survey ownership snapshot by May 2000.

Evidence limits:

- The form is an **official historic-resource survey synthesis**, not the underlying 1945 or 1953 directory page.
- It does **not** identify the exact 1945 or 1953 directory title/page in a way that resolves the source-provenance gap.
- It does **not** directly establish a Farr→Harr business transfer.
- It does **not** directly establish a Harr→Well transfer.
- It does **not** prove uninterrupted Harr operation between 1945 and 1953.
- The May 2000 owner field is not a deed and does not establish the Wiitanens' acquisition date, seller, consideration, or legal transfer date.

### 5. Well's Recreation is already a canonical business

- Business ID: `BUS-015`
- Canonical archive wording: **Well's Recreation**
- Address: **505 Main** (`B-002`)
- The 1953 occupancy remains official-secondary/survey synthesis until the original directory page is recovered.
- Proprietor/operator identity remains unresolved.

When searching, include spelling/index variants as discovery terms where useful: `Well's`, `Wells`, `Well`, `Welle`, `Welsh`. Do not normalize a variant into the canonical name without source support.

## Current 505 occupancy bracket

### 1936 — Farr's Pool Hall

- CCHS `P-1128` photograph is independently dated to 1936.
- Official City identification plus the probable visible Farr signage support **Farr's Pool Hall at 505** as a strong cross-source operating-state anchor.
- Edwin F. Farr and Clarence P. Farr must remain separate people.

### 1945 — Harr's Recreation Center

- The May 2000 SHPO form now visually confirms that the survey explicitly attributes **Harr's Recreation Center — 505 Main** to a **1945 city directory**.
- This improves provenance for the City's later synthesis but **does not recover the original 1945 directory page**.

### 11 February 1948 — Harr named as pool-hall operator

- Oregon City Commission text directly names Harr and McDougald in the pool-hall context.
- That line does not itself give Harr's first name, business name, or address.

### Late 1948 — exact primary municipal Harr/505 anchor

- Direct municipal liquor-license text gives **Carl R. Harr — Harr's Recreation Center — 505 Main**.
- This remains the strongest exact-address primary municipal anchor for Harr currently in the archive.

### 1950 — use continuity class

- Sanborn evidence shows **billiards / cigars / beer** use at 505.
- This supports the use class at the address but does not by itself identify Harr or Well's as operator.

### 1953 — Well's Recreation

- The visually verified May 2000 SHPO form explicitly says the 1953 city directory lists **Well's Recreation** at 505.
- The original 1953 directory page, proprietor, exact opening/closing dates, and transfer relationship to Harr remain unresolved.

## Questions that remain open

1. **When exactly did Farr's Pool Hall cease and Harr's Recreation Center begin at 505?**
2. **What original directory/source page underlies the survey's 1945 Harr statement?**
3. **Was Carl R. Harr already operating at 505 when the 1947–48 county directory was canvassed in Aug–Sep 1946?**
4. **When did Harr cease and Well's Recreation begin?**
5. **Who was the proprietor/operator behind Well's Recreation?**
6. **What exact 1953 directory page underlies the survey's Well's statement?**
7. **Do liquor-license applications, renewals, endorsements, or transfers directly document either handoff?**
8. **What are the acquisition date and deed details for Richard and Sheila Wiitanen's later ownership of 505?** The May 2000 survey only supplies a dated ownership snapshot.

## Best next research actions

### Priority 1 — MF-001: 1947–48 Clackamas County Directory

This remains the single highest-value source for the **Farr→Harr transition**. The Pacific Directory Service volume was canvassed in **August–September 1946**, so it may place Farr or Harr at 505 during the exact transition interval.

When the volume is obtained, visually inspect rather than relying only on OCR/indexing. Check:

- Farr, Edwin / Edwin F. Farr
- Farr, Alice
- Farr's Pool Hall
- Harr, Carl / Carl R. Harr
- Harr's Recreation Center
- pool halls / billiards / recreation classifications
- street/address listings for **505**, **505½**, and neighboring **501–511 Main**
- title/front matter and canvass/publication dating

Known access lead remains GFO `TF0767` / the 1947–48 Clackamas County directory route documented in `MANUAL-FOLLOWUP.md` and the existing source captures.

### Priority 2 — MF-002: missing 1944–48 Oregon City liquor-license proceedings

Search the missing annual and in-year license proceedings for:

- Edwin F. Farr / Farr's Pool Hall
- Carl R. Harr / Harr's Recreation Center
- transfers, endorsements, applications, renewals, discontinuances, or address changes at 505

The late-1948 exact-address list provides the best procedural template for what an earlier surviving annual list may look like.

### Priority 3 — original 1953 directory page / Well's proprietor

Use the 1953 directory lead already preserved in `evidence/source-captures/1953-oregon-city-vicinity-directory-lead.md` and search spelling variants only as discovery terms. The goal is to recover the original page and identify the proprietor/operator, not merely collect more repetitions of the City/SHPO synthesis.

### Priority 4 — switch source class rather than repeat generic web searches

Broad generic Farr/Harr web searches have reached diminishing returns. Do not restart them unless a new collection, exact identifier, or access route appears. Prioritize original directories, municipal licensing, contemporary advertisements/reporting, and exact-address records.

## Files to review first in the next chat

After syncing current `main` and reading policy files, review at minimum:

- `evidence/source-captures/2026-09-05-farr-harr-closeout-checkpoint.md`
- this checkpoint
- `records/historic-surveys/505-main-shpo-resource-30539-inventory-form-provenance.md`
- `businesses/farrs-pool-hall.md`
- `businesses/harrs-recreation-center.md`
- `businesses/wells-recreation.md`
- `timelines/505-main.md`
- `evidence/source-captures/1948-harrs-recreation-center-505-main.md`
- `evidence/source-captures/1953-oregon-city-vicinity-directory-lead.md`
- `evidence/source-captures/1945-harr-online-citation-sweep-2026-09-05.md`
- `MANUAL-FOLLOWUP.md`
- relevant entries in `evidence/source-register.md`, `evidence/evidence-register.md`, `evidence/open-questions.md`, and `evidence/research-leads.md`

## Handoff instruction

Continue from this repository state; do not restart completed SHPO resource-ID or scan-retrieval work. The SHPO 30539 scan has already been retrieved and visually reviewed. The next useful work is to recover **original contemporary evidence** capable of tightening either transition:

**Farr → Harr → Well's**.
