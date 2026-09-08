# 1917 Oregon City Enterprise exhaustive audit — conversation handoff checkpoint — 7 September 2026

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Pre-handoff synchronized `main` HEAD reviewed: `534ced7917ec4c1e91e036bc55a1ec84786985a7`  
Research stream: **1917 annual closeout / Oregon City Enterprise page-by-page visual audit for the 501/503/505 Main project**  
Status: **ACTIVE — CONTINUE FROM CURRENT MAIN; DO NOT RESTART JANUARY–SEPTEMBER**

This checkpoint preserves the material learned, corrected, integrated, and queued during the conversation that began with the 1917 non-Courier title audit. It is a restart aid only. The repository remains authoritative, and any later commit on `main` supersedes stale counts or resume points in this file.

---

## Mandatory startup for the next session

Before any new research or repository edit:

1. Fetch/sync the newest `main`; do not reset, revert, force-push, overwrite, or discard newer parallel commits.
2. Read `AGENTS.md` completely from current `main`.
3. Read `RESEARCH-STANDARD.md` completely from current `main`.
4. Read `MANUAL-FOLLOWUP.md` and the current 1917 year/closeout records.
5. Review newest commits because parallel Wheel / 505 / 1919 / other workflows actively advance `main` and may consume sequential IDs.
6. Visually inspect original archival scans whenever available. OCR/search/text extraction is discovery/backstop only and never substitutes for visual certification.
7. A missing or misassociated page is a **RETRIEVAL GAP**, not negative evidence.
8. A no-hit is bounded coverage only; do not convert it into vacancy, non-use, demolition, closure, or absence.
9. After each meaningful source batch, perform the `AGENTS.md` **Cross-Record Propagation Audit** across timelines, buildings, businesses, people, open questions, research leads, registers, crosswalks, and YAML/database records.
10. Re-sync immediately before allocating any sequential IDs and run `python3 scripts/validate_archive.py` (or the equivalent GitHub Actions validator) before and after meaningful repository writes.

---

# Governing 1917 title correction and inventory

The missing second local 1917 newspaper title is the weekly **Oregon City Enterprise** (`sn00063700`), not the *Morning Enterprise*. Historic Oregon Newspapers' digitized *Morning Enterprise* run ends in 1913.

The 1917 *Oregon City Enterprise* Friday-pattern inventory exposes **52 issues / 416 archive page slots**.

The annual audit must separately verify printed issue date and printed page number on every scan because the March and April runs exposed source-association defects that archive metadata alone did not reveal.

The separate *Oregon City Courier* 1917 run had already reached year end before this Enterprise continuation: **52 issue dates inventoried, 51 complete issues plus one partial, 435 genuine page images visually verified**, with the true **13 December 1917 p21** still unrecovered. That Courier gap is retrieval/manual work, not a negative result.

---

# Conversation work preserved month by month

## January 1917 Enterprise — complete

Canonical capture: `evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md`  
IDs: `S-266` / `E-240`  
Coverage: **4 issues / 32 of 32 pages visually verified**.  
Preserved originals: `newspapers/oregon-city-enterprise/1917-january/`.

Result:
- no defensible exact 501/503/505/507/509/511 Main occupant and no new exact 427 Main occupant;
- bounded coverage only, never vacancy evidence.

## February 1917 Enterprise — complete

Canonical capture: `evidence/source-captures/1917-enterprise-february-02-23-visual-review-2026-09-06.md`  
IDs: `S-267` / `E-241`  
Coverage: **4 issues / 34 of 34 pages visually verified**, including the **10-page 16 February** issue.  
Preserved originals: `newspapers/oregon-city-enterprise/1917-february/`.

Direct/context controls:
- 612 Main controls recur;
- Farr Bros. appears in county-poor material;
- Annis/Annie L. Farr appears in tax/property material.

Identity discipline:
- these Farr observations do **not** establish Edwin F. Farr, Alice Farr, or Farr's Pool Hall at 505 Main in 1917;
- the Farr Brothers grocery/meat business remains a separate identity thread.

No exact target 501/503/505/507/509/511 occupant was established.

## March 1917 Enterprise — gap-aware closeout

Canonical capture: `evidence/source-captures/1917-enterprise-march-02-30-visual-review-2026-09-06.md`  
IDs: `S-272` / `E-246`; manual callout `MF-049`.  
Archive slots inspected: **40**.  
Genuine intended-date March pages: **39**.

Critical archive defect:
- archive object **16 March seq-5 / page 5** visibly prints **23 March 1917, Page 5**;
- it is a distinct March 23 Page 5 scan, not the normal March 23 seq-5 file;
- PDF, JP2, OCR, OCR XML/RDF, alternate-edition and LOC/Chronicling-America recovery routes were tested without recovering the true March 16 Page 5.

Classification:
- true **16 March p5 = RETRIEVAL GAP / MF-049**;
- no exact target occupant was established on the 39 genuine pages;
- the missing page prevents complete no-hit coverage for that issue.

## April 1917 Enterprise — gap-aware closeout and entity promotion

Canonical capture: `evidence/source-captures/1917-enterprise-april-06-27-visual-review-2026-09-06.md`  
IDs: `S-279` / `E-252`; `P-396` W. S. Eddy; `BUS-103` Fashion Stable; manual callout `MF-051`.  
Archive slots inspected: **32**.  
Genuine intended-date April pages: **31**.

Critical archive defect:
- archive **13 April seq-8** visibly prints another **Page 6** variant, with a Thursday masthead/date anomaly;
- true **13 April printed Page 8** was not recovered through the tested online derivatives/alternate routes;
- true April 13 p8 remains **RETRIEVAL GAP / MF-051**.

Entity chronology promoted from direct repeated ads:
- 1915 primary evidence had placed **W. S. Eddy / Fashion Stable on Fifth Street between Main and Water**;
- repeated April 1917 ads place **W. S. Eddy, V.S., M.D.V. / Fashion Stable between Fourth and Fifth on Main Street**;
- this supports a dated relative-location change / possible move or changed premises wording, **not** an exact move date, numbered address, lease, ownership, or physical-building continuity.

Strict guard:
- do **not** merge W. S. Eddy with **W. B. Eddy's Store at 427 Main**;
- do not assign Fashion Stable to 427 Main, 106 Fifth, 110 Fifth, or 501/503/505 without direct evidence.

## May 1917 Enterprise — complete

Canonical capture: `evidence/source-captures/1917-enterprise-may-04-25-visual-review-2026-09-06.md`  
IDs: `S-280` / `E-253`; building `B-018`; business `BUS-104`; timeline `T-094`.  
Integration commit: `4942c9a2cab43aaa1db070eb94fc2214ffbaa52d`.  
Coverage: **32/32 genuine intended-date pages visually verified**; no page substitution or retrieval gap.

Direct 25 May p8 exact-address finding:
- Oregon National Guard **"enlistments are being received at 106 Fifth street"**;
- this establishes `B-018` as a dated exact-address recruiting/enlistment-use record;
- it does **not** establish owner, ordinary tenant, room, parcel, footprint, construction date, physical continuity, or duration, and does not connect 106 Fifth to 501/503/505 Main.

Fashion Stable:
- ads on 4/11/18/25 May p7 extend `P-396` / `BUS-103` at **Main between Fourth and Fifth** through **25 May 1917**, still without an exact number.

Farr Brothers:
- 25 May p6 directly calls **Farr Brothers a "Meat market"**;
- combined with already preserved 1922 `Grocers, Butchers` evidence and official Farr Store history, this supported stable `BUS-104` **Farr Brothers Store / Meat Market**;
- the May page itself does not print 919 7th or identify Clarence/Louis individually;
- keep `BUS-104` strictly separate from Edwin F. Farr, Alice Farr, Farr's Pool Hall (`BUS-013`) at 505, Carl Harr, and Harr's Recreation Center.

Target result:
- no exact 501/503/505/507/509/511 Main or new 427 Main occupant on the 32 May pages;
- coverage only, not vacancy/non-use evidence.

## June 1917 Enterprise — complete, plus regulatory amendment

Canonical capture: `evidence/source-captures/1917-enterprise-june-01-29-visual-review-2026-09-06.md`  
IDs: `S-281` / `E-254`; regulatory timeline `T-095`; follow-up `RL-052`.  
Retrieval commit: `77ec7b746990740ba842e7f451b490cadd07763c`.  
Closeout commit: `dcdf30a4a9a7fe0b45ad0a8ce9147c186663f7c3`.  
Regulatory-context amendment commit: `25f85663cac04faf2c8b0c4a7c44a549e4ec66c7`.  
Coverage: **5 issues / 40 of 40 genuine intended-date pages visually verified**; no page substitution or retrieval gap.

Fashion Stable:
- p7 ads on 1/8/15/22/29 June extend W. S. Eddy / Fashion Stable at **Main between Fourth and Fifth** through **29 June 1917**, no exact number.

Farr Brothers:
- 22 June p6 includes **Farr Bros.** in County Court expenditures;
- no address, proprietor, or new trade description; the stronger 25 May `Meat market` wording remains the direct 1917 business-type control.

8 June p3 citywide pool-room regulatory context:
- enlarged visual inspection confirms a City Council report saying **all of the pool rooms in the city** were said to be violating certain ordinance sections;
- discussion concerned a proposed amendment allowing pool rooms to **operate cigar stands without paying additional licenses**;
- the report says the city's **strict pool-room legislation** had been made in **1911**, when saloons were still operating.

Limits:
- this does **not** identify a particular pool room, address, proprietor, licensee, violator, or enforcement case;
- it does not prove that the 1912 Smith pool room at 503, any later 505 pool hall, Farr's Pool Hall, or any named operator violated the ordinance or owed a cigar license.

Propagation:
- citywide regulatory event `T-095`, not a 503/505 occupancy event;
- contextual note added to the early Smith/503 pool-room thread;
- `RL-052` targets the underlying 1911 enactment and 1917 amendment outcome.

Target result:
- no exact 501/503/505/507/509/511 Main or new 427 Main occupant on June's 40 genuine pages.

---

# Repository process correction adopted during this conversation

The project steward explicitly required that source-batch integration update not only source/evidence records but also **timelines, people, buildings, businesses, open questions, research leads, indexes/crosswalks, and YAML/database records whenever the historical content or evidence state changes**.

This requirement is now codified in `AGENTS.md` under **Cross-Record Propagation Audit**.

Important implementation rule:
- if a batch produces only bounded no-hit coverage or a retrieval gap and establishes no entity fact, record that propagation decision in the capture/log;
- do **not** manufacture a vacancy, occupant, ownership, business, or building event solely to make a timeline look complete.

May and June were integrated under this rule. The May integration initially failed validation because the new `B-018` building was missing validator-recognized Markdown synchronization and `E-253` lacked a Markdown `Type:` field. Those defects were corrected before the final May commit landed; no partial historical closeout was committed.

---

# Current live 1917 state at this handoff — later work supersedes the old June resume point

Current `registers/year-status.md` on the synchronized `main` reviewed for this checkpoint reports:

- 1917 status: **IN PROGRESS**;
- *Courier*: **435 genuine pages visually verified**, with true 13 Dec p21 unresolved;
- *Oregon City Enterprise*: **312 genuine intended-date pages through September**;
- **314 Jan–Sep archive slots inspected**, with the two true-page gaps unchanged:
  - true **16 March p5** (`MF-049`);
  - true **13 April p8** (`MF-051`);
- **102 exposed October–December Enterprise slots remain**;
- current September capture: `evidence/source-captures/1917-enterprise-september-07-28-visual-review-2026-09-07.md` (`S-288` / `E-262` / `BUS-105`).

Therefore **do not resume at June or July**. July, August and September have already been integrated by later work on `main`.

September's current direct controls include:
- W. S. Eddy / Fashion Stable continues through **28 September 1917** at Main between Fourth/Fifth, still unnumbered;
- Farr Brothers business/supplier controls continue without an exact address or bridge to Edwin/Alice Farr / 505;
- direct **J. C. Penney Co. / The Golden Rule — Main Street Between Fifth and Sixth — Phone 270** (`BUS-105`), without a numbered storefront/building assignment;
- no exact target 501/503/505/507/509/511 occupant was established in September.

Current chronological next online newspaper step from `main`:

**October 1917 Oregon City Enterprise**, after verifying the exposed October issue/page inventory, including the known **six-page 19 October issue**.

After October–December Enterprise page-by-page visual work, still required before `ONLINE COMPLETE`:
- final Enterprise title/calendar/page reconciliation;
- documented recovery/manual handling for the two Enterprise page gaps;
- true Courier 13 Dec p21 gap;
- actual Oregon City section of the **Sohns & Woodbeck 1916–1917 directory**;
- remaining relevant 1917 online non-newspaper source classes and final numbered manual-callout reconciliation.

---

# 1917 exact-address research boundary

Despite the large newspaper coverage, the exact 1917 occupant question for **503 and 505 Main** remains unresolved.

Safe wording:

> No defensible exact-address occupant for 503 or 505 Main has yet been recovered from the successfully accessed and visually reviewed 1917 newspaper pages.

Do **not** convert that into a statement that either address was vacant, unused, demolished, or nonexistent.

The highest-value non-newspaper source remains the **Sohns & Woodbeck 1916–1917 Oregon City directory section**, because a street/address listing could directly identify the published 500-block occupants in one source. Current repository/manual records treat the Oregon City section as unrecovered; the Oak Grove/Jennings Lodge partial scan is not a substitute.

---

# Files to read first when resuming this research stream

1. `AGENTS.md`
2. `RESEARCH-STANDARD.md`
3. `MANUAL-FOLLOWUP.md`
4. `registers/year-status.md`
5. `evidence/source-captures/1917-closeout.md`
6. `evidence/source-captures/1917-enterprise-september-07-28-visual-review-2026-09-07.md`
7. `evidence/source-captures/1917-enterprise-june-01-29-visual-review-2026-09-06.md`
8. `evidence/source-captures/1917-enterprise-may-04-25-visual-review-2026-09-06.md`
9. `evidence/source-captures/1917-enterprise-april-06-27-visual-review-2026-09-06.md`
10. `evidence/source-captures/1917-enterprise-march-02-30-visual-review-2026-09-06.md`
11. `evidence/source-captures/1917-enterprise-february-02-23-visual-review-2026-09-06.md`
12. `evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md`

This handoff intentionally preserves earlier monthly states for audit history while directing future work to the **newest current-main checkpoint** rather than restarting completed research.
