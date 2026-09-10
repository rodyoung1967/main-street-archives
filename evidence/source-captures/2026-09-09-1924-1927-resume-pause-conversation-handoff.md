# 1924–1927 resume / pause conversation handoff — 9 September 2026

Repository: `rodyoung1967/main-street-archives`  
Branch: `main`  
Research stream: **1924–1927 503/505 Main occupancy, municipal records, directories, licenses, building/public-works context**  
Status: **PAUSED BY PROJECT STEWARD — CONTINUE FROM NEWEST MAIN**

## Purpose

This handoff preserves everything material from the short conversation in which the project steward asked to **pick up the 1924–1927 data collection**, then asked to **pause it** before any new archival research was performed.

No new historical source was inspected in that conversation, no new historical claim was established, no evidence/source/entity/timeline ID was assigned, and no existing historical record requires propagation from that conversation alone.

The useful contribution of the conversation was to re-establish the existing 1924–1927 checkpoint and the exact restart boundary. The authoritative historical work remains in the existing source captures and registers listed below.

## Mandatory startup for the next session

Before doing any new 1924–1927 work:

1. Fetch/sync and inspect the newest `main`.
2. Do not reset, revert, force-push, delete, relocate, or overwrite newer parallel commits.
3. Multiple 503/505, annual-closeout, Wheel, Farr/Harr, newspaper, photo, directory, OLCC and other workflows may advance `main` independently.
4. Read completely:
   - `AGENTS.md`
   - `RESEARCH-STANDARD.md`
   - `MANUAL-FOLLOWUP.md`
5. Review the newest commits and search for any 1924–1927 work added after this handoff before resuming.
6. Run `python3 scripts/validate_archive.py` before and after meaningful repository changes, or verify the equivalent repository validation workflow.
7. Commit meaningful verified findings directly to `main`.
8. Visually inspect original archival scans whenever accessible. OCR/searchable text is discovery only.
9. Treat failed retrieval as a retrieval gap, not negative evidence.
10. Do not merge similarly named people/businesses or commissioner surnames with business operators without contemporary bridging evidence.
11. Do not send institutional requests, authorize paid research, or use restricted-account access unless the project steward explicitly authorizes it.

## Synchronization state from this conversation

When the 1924–1927 work was first resumed in the conversation, the latest `main` observed at that moment was:

- `077f77918dc2bba93c08dcc69ddfd8f90f88f69e` — `Review and preserve full 1926 municipal report with fire and health leads`

That SHA was only the then-current checkpoint. By the time this handoff was created on 9 September 2026, parallel work had advanced `main` substantially. Immediately before this handoff write, observed `main` was:

- `f60c2bb8c100db7fca90d4b18693d784cba6b550` — `Fix temporary 1912 Courier gap retrieval workflow`

This is also only a synchronization checkpoint. Always inspect the live newest `main` before continuing.

## Canonical 1924–1927 files to read first

1. `evidence/source-captures/1924-oregon-city-directory-retrieval-review-2026-09-01.md`
2. `evidence/source-captures/1924-1927-municipal-minutes-access-review-2026-09-01.md`
3. `evidence/source-captures/1925-1926-503-505-business-identification-checkpoint-2026-09-01.md`
4. `evidence/source-captures/1925-municipal-report-fire-correction-and-fifth-street-review-2026-09-01.md`
5. `evidence/source-captures/1925-municipal-report-remaining-pages-review-2026-09-01.md`
6. `evidence/source-captures/1925-license-inspection-and-county-records-review-2026-09-01.md`
7. `evidence/source-captures/1926-municipal-report-visual-review-2026-09-01.md`
8. `evidence/research-leads.md`
9. `evidence/source-register.md`
10. `evidence/evidence-register.md`
11. `registers/research-log.md`
12. `MANUAL-FOLLOWUP.md`
13. `timeline.md`
14. `ARCHIVE_INDEX.md`

Also inspect the retained originals under:

- `records/municipal/annual-reports/`
- `records/municipal/commission-minutes/`

## Existing 1924 checkpoint

The 1924 directory work is **IN PROGRESS**.

The National Register nomination for the DeWitt Clinton Latourette House was visually checked and its bibliography directly cites **Polk, R. L. and Company, Oregon City Directory, 1924** on PDF page 7. That proves the nomination used/cited such a source; it does **not** prove the exact edition identity, present holding, address entries, or any 503/505 occupant.

No actual 1924 directory pages were recovered or visually inspected in that pass.

The project already preserved:

- the NPS nomination;
- the corrected citation-page locator;
- bounded institutional/catalog checks;
- the GFO shelflist excerpt showing alternate-year holdings;
- exact unsent manual retrieval targets.

Do not repeat the completed 1923–1924 regional OCR pass merely because the 1924 volume itself remains unrecovered. Do not treat catalog silence as evidence of vacancy, nonpublication, or demolition.

## Existing 1925 municipal-minutes checkpoint

The current public Laserfiche route was successfully identified through:

`Browse → City Recorder → Public Meeting Records → City Commission`

Using Advanced Name search with `1925*City Commission*`, the prior pass saved an inventory of:

- **81 named 1925 entries**;
- **159 listed scan pages** in aggregate.

Those numbers are catalog/inventory counts only. They are not deduplicated physical-page counts and do not certify annual completeness.

The **6 January 1925** entry was readable only through its OCR/rendered text layer in that pass. Its actual scanned page was not successfully visually inspected, so it remains **OCR/TEXT ONLY**.

The other 80 inventoried 1925 entries were still **PENDING** through that route at the checkpoint.

A download/export attempt was stopped by a browser URL-policy limitation. No workaround was attempted. That is a tool/retrieval limitation, not proof that the public record is unavailable.

## Existing 1925 annual-report checkpoint

The independent 1925 Municipal Activities Report was later retrieved and fully visually reviewed in the existing source captures.

Important preserved controls include:

- the annual report states **12 regular + 72 special = 84 meetings**; this must be reconciled by date against the 81 Laserfiche catalog entries rather than subtracting unlike units and declaring three missing meetings;
- the previously conflated target-block fire lead was corrected to **30 April 1925**, approximately **$15 damage**, **Main between Fifth and Sixth**, with no side, number, business or occupant identified;
- Fifth Street paving material reviewed in that report concerns **High–Jackson**, not proof of a width change at the target 500 block;
- the report identifies useful underlying record classes such as duplicate license receipts, restaurant inspections, assessment/lien material and engineering files, but those underlying address-level records were not recovered in that pass;
- the report did not identify the May 1925 503 restaurant or 505 billiards/cigars occupant.

The May 1925 Sanborn occupants therefore remain unresolved at this checkpoint.

## Existing 1926 annual-report checkpoint

The full 1926 Municipal Activities Report was retained and all **23 PDF pages** were visually reviewed.

Important preserved findings/limits include:

- **10 July 1926, Sixth and Main** — false alarm; no target premise identified;
- **20 September 1926, Sixth and Main** — unknown cause, approximately **$500 damage**; no number, side, business or proprietor identified;
- **11 November 1926, Fifth and Main** — false alarm; no target premise identified;
- a separate **4 August 1926 Paramount Restaurant** fire entry reports approximately **$4,500 damage**, but the report gives no address, so it must not be assigned to 503/Kwality without independent evidence;
- the report says all city restaurants were inspected but gives no restaurant names, addresses or inspection returns;
- a county-labeled health expenditure and license-account figures create record-retrieval leads but do not identify a target tenant;
- no 501/503/505 rebuild date or target occupant was established by the report.

The year remains **IN PROGRESS** under the project standard.

## Existing May 1927 bounded minute review

Six City Commission ledger pages linked from the Municipal Elevator history page were retained and visually inspected:

- printed pp. **322–325** from the 11 May 1927 source PDF;
- printed pp. **328–329** from the 23 May 1927 source PDF.

This was a bounded six-page review, **not** a review of all May 1927 or all 1927 minutes.

Preserved conclusions:

- Ordinance 1152 concerns Elevator Street / Block 34 / Sarah A. Chase heirs, not 503/505 Main;
- Water Street improvement language covers the Water Street segment from the south line of Fifth to the north line of Sixth and does not establish Fifth Street's overall width or alleged narrowing;
- portions of the May 16 and May 18 meetings are outside the retained six-page set;
- no 503/505 occupant, target pool-hall license, or target construction event was identified in those six pages;
- Commissioner **Farr** appears in the minutes, but that surname does **not** identify Edwin F. Farr or the proprietor of Farr's Pool Hall at 505.

## Core unresolved occupancy questions in this stream

At the saved checkpoint:

- the **May 1925 Sanborn 503 restaurant** remains unnamed;
- the **May 1925 Sanborn 505 billiards/cigars use** remains unnamed;
- Farr's operation at 505 is still not safely dated into 1924–1927 by a direct address-bearing primary source from this stream;
- Kwality's reported **1926** presence at 503 remains unbridged to the May 1925 Sanborn occupant;
- no direct 1924 directory page has yet supplied a 503/505 occupant;
- no 1925 or 1926 annual-report finding establishes a target rebuild date.

Do not convert any of those gaps into a vacancy or non-use claim.

## Existing high-value manual/restricted routes

The prior 1924 directory capture already records unsent/manual targets, including:

- Oregon City Planning supporting material behind the NPS nomination's 1924 directory citation;
- OHS / CCFHS / other institutional holding confirmation for the cited 1924 directory;
- complete target-address and name/trade review if the volume is located;
- local newspaper microfilm and other inaccessible 1923–1926 coverage.

`MANUAL-FOLLOWUP.md` also preserves broader active calls relevant to this period, including property/assessment records, 1922/1920 municipal license records and the 1923–1926 local-newspaper microfilm route.

No outreach, paid lookup, institutional request, or restricted-login action was authorized or sent in this conversation.

## Best restart order

After syncing newest `main` and checking whether parallel work has changed the state, continue in this order unless newer evidence suggests a better route:

1. **Audit for newer 1924–1927 commits first.** Do not duplicate work completed after the 1 September checkpoints.
2. **Continue the public municipal-record inventory for 1924, 1926 and 1927** using the known City Commission Laserfiche route, preserving exact entry metadata and statuses.
3. **If an authorized readable scan route is now available, perform page-by-page visual review in manageable batches**, with the 1925 January entries as the first unfinished batch from the old inventory. OCR may prioritize but cannot substitute for the scan.
4. **Continue 1927 commission/minute review beyond the six already inspected pages**, prioritizing licenses, pool/billiards/cigars, restaurants, signs, transfers, building work, Main/Fifth addresses and exact numbered premises.
5. **Keep the 1924 directory route open** but do not send institutional requests or order research without explicit authorization.
6. **Use independent source classes when municipal returns diminish**: directories, exact-address newspaper advertisements/reporting, licenses, property/assessment records, permits, photographs and other address-bearing records.
7. When a new source changes an occupant, business, building, person, timeline, open question or lead, perform the full cross-record propagation audit required by `AGENTS.md`.

## Research-state / propagation audit for this conversation

This conversation itself produced **no new documentary historical fact**. Therefore:

- no new `S-###`, `E-###`, `T-###`, `P-###`, `BUS-###`, `B-###`, `IMG-####` or map ID is warranted;
- no historical timeline/building/business/person/YAML/database propagation is warranted from the conversation alone;
- no annual status changes are warranted;
- no no-hit was converted into negative evidence;
- no same-name people/businesses were merged;
- no existing source was superseded;
- no manual request was sent.

The purpose of this file is preservation of the **restart state**, the earlier checkpoint that was re-established, and the fact that the project steward then explicitly paused this research stream.

## Exact instruction for a new chat

Use this as the restart instruction:

> Continue the 1924–1927 503/505 Main Street Oregon City research from the current `main` branch of `rodyoung1967/main-street-archives`. First sync newest `main`, read `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md`, and `evidence/source-captures/2026-09-09-1924-1927-resume-pause-conversation-handoff.md`, then inspect any newer 1924–1927 commits before doing research. Do not restart completed 1 September work. Continue the unfinished municipal-record inventory/visual review and occupancy identification work, preserve retrieval gaps and uncertainty, visually inspect original scans, do not merge names without bridging evidence, do not send institutional/paid requests without my authorization, validate after meaningful changes, and commit verified findings directly to `main`.
