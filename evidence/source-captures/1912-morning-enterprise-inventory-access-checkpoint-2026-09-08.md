# 1912 Morning Enterprise inventory / scan-access checkpoint — 8 September 2026

Status: **IN PROGRESS — COVERAGE / ACCESS CHECKPOINT**

This checkpoint continues the exhaustive 1912 online audit on `research/1912-online-audit`. It records title provenance, issue-size observations, and scan-recovery testing only. It does not certify a full title/year review.

## Title provenance

Historic Oregon Newspapers identifies *Morning Enterprise* (`sn00063701`) as an Oregon City daily title with frequency **Daily (except Mon.)**, 1911–1933, and notes irregularities in numbering.

The Oregon Digital Newspaper Program project blog independently documents that the **January 1912–December 1913 Morning Enterprise run was re-filmed** and added through the Oregon City Public Library digitization project. This is useful provenance for why this period may behave differently from older derivatives and reinforces the need to inventory the actual archive run rather than infer issue survival from the theoretical publication schedule.

Relevant public pages:

- Title record: https://oregonnews.uoregon.edu/lccn/sn00063701/
- ODNP project history / Oregon City content announcement: https://odnp.uoregon.edu/page/15/ (also mirrored in the older project-blog pagination)

## Issue-size irregularity confirmed

Do **not** assume four images for every 1912 *Morning Enterprise* issue.

Archive-indexed examples encountered during this checkpoint:

- **31 Jan 1912** — entire-issue result exposes **4 images**.
- **7 Mar 1912** — page 5 explicitly reports `of 8`; therefore this issue has **8 images**.
- **21 Mar 1912** — page 4 explicitly reports `of 4`; therefore this issue has **4 images**.
- **11 Aug 1912** — page 1 explicitly reports `of 4`; therefore this issue has **4 images**.
- **19 Dec 1912** — entire-issue result exposes **4 images**.

These are inventory controls only. They demonstrate real issue-size variation and justify issue-specific page counting under `RESEARCH-STANDARD.md`.

## Existing visual credit retained

The complete **19 Mar 1912** issue is already visually reviewed and integrated on current `main`; page 2 directly identifies Joe Wilson's Palace Saloon at **501 Main Street** (`S-118` / `E-104`). This checkpoint credits that prior visual work and does not repeat it.

The **7 Sep 1912** Willamette/Harding advertisement is also already visually verified in current `main` (`S-154` / `E-138`).

## Direct page-PDF recovery test — unsuccessful for certification

Search indexing can surface URLs ending in `.pdf` and sometimes render substantial extracted page text. A test on the 17 Mar 1912 page-2 PDF URL appeared in search as a direct PDF-style result.

However, the research screenshot function rejected the object because the returned content was **not actually `application/pdf`**. Therefore the result is still an extracted/search representation, not an inspectable faithful scan. It does **not** count as `VISUALLY VERIFIED`.

This route is now documented as another reasonable failed recovery attempt. Do not award visual credit from these search-rendered pseudo-PDF results.

## Discovery-only recurring Main Street anchors

OCR/search results from sampled 1912 *Morning Enterprise* pages repeatedly show the paper's sale-location box, including:

- Huntley Bros. Drugs — Main Street;
- J. W. McAnulty — Seventh and Main;
- **E. B. Anderson — Main near Sixth**;
- **M. E. Dunn Confectionery — Next door to P. O.**;
- City Drug Store — Electric Hotel;
- Schoenborn Confectionery — Seventh and J. Q. Adams.

These recurring lines are useful navigation/geographic controls, but this checkpoint does not promote them as new claim-level evidence because the current batch is OCR/search-only and current `main` already contains extensive Post Office-relative and adjacent-business reconstruction. Any historical promotion requires actual scan verification and a duplicate check against current registers.

## Audit consequence

The Morning Enterprise work remains **PENDING / RETRIEVAL GAP** at the title-year level. The actual 1912 issue calendar and issue-specific page counts still must be completed, and every retrievable scan must be visually reviewed or precisely routed to a manual callout after reasonable recovery attempts.

No `E-###`, `S-###`, person, business, building, timeline, YAML, or address-register change is warranted from this coverage-only checkpoint.

## Next work

1. Continue building the actual 1912 Morning Enterprise issue/date ledger from dated archive records rather than a theoretical six-days-per-week calendar.
2. Record issue-specific page counts; do not extrapolate four pages across the year.
3. Reconcile existing visual credits first.
4. Continue testing faithful scan delivery, including any alternate derivative/IIIF route exposed by archive metadata.
5. If faithful scans remain unavailable after reasonable attempts, preserve the exact issue/page ranges as retrieval gaps and place them into the eventual numbered 1912 manual-callout list.
