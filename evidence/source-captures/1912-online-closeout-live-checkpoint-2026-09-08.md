# 1912 Online Closeout — Live Knowledge Checkpoint — 8 September 2026

Status: **IN PROGRESS / KNOWLEDGE PRESERVATION CHECKPOINT**. This file preserves the meaningful research/process knowledge learned during the current 1912 closeout continuation before the full annual visual audit is finished. It does not certify 1912 as `ONLINE COMPLETE` and does not create a new historical relationship by itself.

## Repository synchronization state

The earlier `research/1912-main-street` branch was discovered to be dangerously stale after substantial parallel work advanced `main`. It must not be merged or force-rebased onto current work. The verified findings from that branch had already been reconciled into newer `main` in commit `a931840a1ae845c504c707bb7e3a7f0e40ea73fb` (`Save reconciled 1912 conversation knowledge checkpoint`).

A fresh closeout branch, `research/1912-online-closeout`, was created from current authoritative `main` and was fast-forwarded to `5995896bfe1ab117f6d98210d143df39c5111631` before the temporary archive probe was added. No main history was reset, reverted, force-pushed, or overwritten.

## Current canonical year state

`registers/year-status.md` still controls: **1912 = IN PROGRESS**.

Under `RESEARCH-STANDARD.md`, the remaining certification blocker is not the absence of useful 1912 facts. It is the lack of a complete auditable title → issue → page inventory and page-by-page visual review of every online-retrievable newspaper scan, plus final other-online-source and manual-callout reconciliation.

Existing 1912 evidence on current `main` already includes, among other things:

- direct 501 Main Palace Saloon / Joe Wilson evidence;
- direct 503 Main Smith pool-room / pool-hall evidence with the H. N. / H. H. initials conflict preserved;
- direct January 1912 address ladder at 503 / 507 / 509 / 511;
- Gambrinus Saloon at Sixth & Main;
- the May 1912 Main Street demolition/rebuilding statement, still geographically unresolved;
- Schrader Main Street bakery transfer;
- later visual Willamette-Building-over-Harding-Drug-Store evidence.

Those findings are not duplicated here; current entity/evidence/source files control.

## Archive-navigation finding — important for the exhaustive audit

The Historic Oregon Newspapers/Open ONI title calendar has a year-specific route that must be used explicitly. Open ONI's current URL definitions document the title/year form as:

`/lccn/<LCCN>/issues/<YYYY>/`

The non-year-specific title `Browse Issues` view can default to another year. Therefore an annual issue inventory must not assume that the first calendar shown is 1912.

The relevant current 1912 title IDs being inventoried are:

- `sn00063698` — *Oregon City Courier*;
- `sn00063700` — *Oregon City Enterprise*;
- `sn00063701` — *Morning Enterprise*.

Issue-page **archive sequence numbers** must be tracked separately from printed page numbers. Search/index results demonstrate that printed labels and archive sequence/image counts can differ, so the closeout denominator must use actual exposed issue scans rather than assuming printed pagination equals image sequence count.

## Temporary archive probe

A temporary GitHub Actions probe has been added on `research/1912-online-closeout`:

- `scripts/temp_1912_archive_probe.py`
- `.github/workflows/temp-1912-archive-probe.yml`

Purpose:

1. fetch the explicit 1912 title calendars;
2. enumerate actual issue dates and archive page sequences;
3. produce an auditable inventory;
4. screen OCR only for discovery/navigation;
5. retrieve *Courier* page-image derivatives and create contact sheets for visual review;
6. log retrieval failures separately rather than converting them to negative evidence.

The probe is instrumentation, not historical evidence. OCR hits remain `OCR/TEXT ONLY` until the corresponding original scan is visually inspected.

## New 19 January 1912 Harding drugstore lead

A current Historic Oregon Newspapers text/OCR page for *Oregon City Courier*, **19 January 1912, page 8 / image 8**, contains the local-news sentence identifying **Percy Cross** as having accepted a position in the **Harding drugstore** during the absence of **A. E. Wilmot**.

Canonical page route:

`https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/seq-8/`

Classification at this checkpoint: **OCR/TEXT ONLY / PENDING SCAN CERTIFICATION**.

Research value if the scan confirms the text:

- it independently shows the Harding drugstore operating in January 1912;
- it names two people associated with the drugstore at that moment, Percy Cross and A. E. Wilmot;
- it may help reconstruct Harding Drug Store staffing/continuity around the January `511 Main` George A. Harding address and the later September Willamette-Building-over-Harding-Drug-Store relationship.

Do **not** create a person/business relationship, exact-address claim, or new evidence ID from this OCR item until the original page image is visually inspected under the project standard.

A separate 12 January 1912 Courier OCR page mentions Percy Cross of Gladstone in a marriage/local-news item; that is identity/context discovery only and is not enough by itself to prove that every `Percy Cross` reference is the same person without corroboration.

## Visual-review rule being applied

The current continuation is explicitly following these states:

- `VISUALLY VERIFIED` only when the actual faithful page scan is inspected;
- `OCR/TEXT ONLY` for text/index discoveries pending scan review;
- `RETRIEVAL GAP` for known pages the online interface cannot expose after reasonable attempts;
- `PENDING` for inventoried pages not yet inspected;
- persistent online gaps will be copied into the year's numbered manual callout list before `ONLINE COMPLETE` can be assigned.

No search silence is being treated as vacancy, closure, demolition, relocation, or non-use.

## Resume point

Continue by harvesting the temporary probe artifact when its workflow completes, verify the title/issue/page counts, visually inspect the generated Courier contact sheets and hit-page images, record newly certified findings, then extend the same image-level coverage to the *Oregon City Enterprise* and *Morning Enterprise*. Re-sync against newest `main` before every meaningful write because parallel project workflows remain active.
