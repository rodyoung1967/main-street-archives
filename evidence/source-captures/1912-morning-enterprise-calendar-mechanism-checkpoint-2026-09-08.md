# 1912 exhaustive online audit — Morning Enterprise archive-calendar mechanism checkpoint

Date: 8 September 2026  
Status: **IN PROGRESS — INVENTORY-METHOD / ACCESS CHECKPOINT**

Purpose: preserve the archive-calendar method discovered while building the 1912 *Morning Enterprise* issue inventory, along with the current interface limitation. This is a coverage-method record only and does not certify the title/year or create a historical claim.

## Title metadata

Historic Oregon Newspapers identifies *Morning Enterprise* (`sn00063701`) as an Oregon City title published **Daily (except Mon.)** from 1911 onward, with irregularities in numbering. The Oregon Digital Newspaper Program separately records that the January 1912–December 1913 run was re-filmed from good print copies during the Oregon City digitization work.

Canonical title page: https://oregonnews.uoregon.edu/lccn/sn00063701/

## Archive-native issue-calendar route discovered

The title page exposes a **Browse Issues by Date** control. Opening that control reaches the title-specific calendar interface. In the current research viewer it opens on the title's initial calendar year, **1911**, and the calendar visibly lists actual surviving issue dates rather than merely describing the theoretical publication frequency.

This is the correct conceptual route for building the annual issue inventory because it can distinguish:

- actual archived issue dates;
- theoretical publication dates;
- irregular/missing dates;
- issue linkage around publication gaps such as Mondays.

The underlying site route is title/year specific. The desired 1912 calendar is conceptually the 1912 year of the same title calendar, but the current browser/tool interface does not expose the year-selector submission as a directly invokable link. Constructing the year URL manually has also been rejected by the current web-safety/cache layer rather than returned as a live archive page.

Therefore the 1912 annual calendar is **not yet certified/reconstructed from this route**. Do not substitute a theoretical six-days-per-week schedule.

## Adjacent-issue linkage control

A live 11 August 1912 *Morning Enterprise* page exposes archive-native previous/next issue links. Those links point toward **10 August** and **13 August**, skipping Monday 12 August, consistent with the title's stated daily-except-Monday frequency. This is useful evidence that archive issue linkage can help reconcile actual dates when the calendar selector is unavailable.

This does not prove every expected date survives elsewhere in 1912; each actual archived issue still requires inventory confirmation.

## Known 1912 issue-size controls retained

Issue-specific page/image counts vary, so no year-wide default is assumed. Current controls include:

- 31 Jan 1912 — 4 images;
- 7 Mar 1912 — 8 images;
- 21 Mar 1912 — 4 images;
- 19 Mar 1912 — complete issue already visually reviewed on current `main`;
- 11 Aug 1912 — live page reports Page 1 of 4;
- 23 Oct 1912 — live/indexed control reports Page 1 of 4;
- 19 Dec 1912 — 4 images.

These controls prove real issue-size variation and reinforce the requirement for issue-specific counts.

## Scan-delivery limitation remains

Opening live HTML page records works reliably enough for issue/date/page-count discovery. Native PDF links sometimes exist but are intermittently unavailable through the current cache/retrieval layer. A failed PDF retrieval is a **RETRIEVAL GAP**, not visual-review credit and not negative historical evidence.

Only actual scan images count as `VISUALLY VERIFIED` under `RESEARCH-STANDARD.md`.

## Repository consequence

This checkpoint changes coverage methodology/state only:

- no new `E-###` historical claim;
- no new `S-###` source record merely for calendar metadata;
- no building/business/person/timeline change;
- no year-status promotion.

## Next exact actions

1. Continue attempts to reach the title-specific **1912** calendar through an archive-exposed link/form or another safe route.
2. In parallel, build the actual 1912 issue ledger from live dated issue pages and archive-native previous/next issue linkage where those pages render.
3. Record an issue-specific page/image count for every surviving date; do not extrapolate four pages across the year.
4. Reconcile prior visual credits first, including the complete 19 March issue and the 7 September Harding/Willamette page.
5. Visually inspect every online-retrievable scan; preserve nonrendering pages as precise retrieval gaps after reasonable recovery attempts.
6. Keep **1912 = IN PROGRESS** until the full current-standard newspaper and other-source audit is complete.
