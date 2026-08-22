# 1915 visual page-by-page review — current access blocker

Date: 2026-08-21

Project standard: every available newspaper page must be visually inspected from the actual scanned page image/PDF/JP2. OCR, search snippets, and extracted text are discovery aids only and do not count as page review.

## Initial attempt

A fresh attempt was made to begin the 1915 visual re-review using the Historic Oregon Newspapers scans for the Oregon City Courier (`sn00063698`). The archive issue indexes and individual page records are discoverable, including page-count information and links labelled PDF/JP2. However, the available research browser is currently returning cache/safety failures for the scan/PDF URLs rather than an image-renderable PDF object. Even a search result whose URL ends in `.pdf` is being exposed to the research browser as extracted text/HTML rather than as `application/pdf`, so the screenshot/visual-page operation cannot be invoked on it.

Examples attempted in the initial recovery turn included January 7, January 28, and December 16, 1915 Courier page/PDF URLs. Direct scan/PDF opens returned cache misses or URL-safety failures. A screenshot attempt against a surfaced `.pdf` search result failed because the browser reported that the result was not an `application/pdf` object and that webpage screenshot was not enabled.

Container/network retrieval was also attempted for a Courier page PDF and failed at DNS resolution for `oregonnews.uoregon.edu`.

## Second recovery attempt — 21 Aug 2026

The visual-recovery effort was continued rather than falling back to OCR.

What was successfully confirmed:

- Historic Oregon Newspapers is currently indexed well enough to expose whole-issue inventories and exact page counts for many 1915 Courier issues. Examples surfaced include Jan. 28 (10 images), Jun. 10 (8), Jun. 17 (10), Jun. 24 (archive index currently exposes 8 despite earlier page-navigation evidence suggesting 10), Jul. 8 (8), Jul. 15 (8), Jul. 22 (8), Jul. 29 (8), Sep. 16 (8), Nov. 4 (8), Nov. 18 (8), and Dec. 9 (10).
- Search indexing can surface exact `.pdf` URLs. For example, `https://oregonnews.uoregon.edu/lccn/sn00063698/1915-07-29/ed-1/seq-1.pdf` was surfaced directly.
- The same archive is also exposing 1915 Oregon City Enterprise records; e.g. Oct. 1, 1915 (`sn00063700`) is an 8-page issue.
- An alternate commercial archive, OldNews, currently lists both Oregon City Courier and Oregon City Enterprise holdings covering 1915. This is a potential alternate scan source if its page images can be exposed to the visual inspection path.

What still failed:

- Opening a surfaced Historic Oregon Newspapers `.pdf` URL still returned a cache miss rather than a renderable PDF.
- A direct screenshot call against that surfaced `.pdf` search result failed because the browser classified it as non-`application/pdf` extracted content and does not permit screenshots of ordinary webpages.
- A direct file download attempt for the surfaced July 29 Courier page-1 PDF also failed, so the page could not be handed to a local PDF/image renderer.
- Image-search attempts did not surface the 1915 page scans themselves; they returned unrelated newspaper imagery rather than the requested issue page.
- OldNews is confirmed as an alternate holder, but in the current research interface its scanned page image has not yet been exposed in a form that can be visually inspected.

## Third recovery attempt — 21 Aug 2026

Further recovery work was performed with the same rule: do not count OCR as visual review.

Newly confirmed:

- NewspaperArchive has a dedicated Oregon City Enterprise archive covering 1866–1922 and specifically indexes a **12 Feb 1915, page 2** item among its popular pages. Its public landing page states that full newspaper images require account/subscription access; the current research interface exposes the archive metadata and text but not the underlying scan image. This gives us a second independent online holder for 1915 Enterprise scans, but not yet a visually inspectable copy in this environment.
- Oregon City Public Library states that its Carnegie Center microfilm collection physically holds **Oregon City Courier, Sept. 23, 1883–July 3, 1919** and **Oregon City Enterprise Weekly, Nov. 10, 1871–Dec. 25, 1942**, which covers all of 1915 for both required titles. This is an authoritative fallback source for any digital-page gaps.
- Oregon Digital Newspaper Program confirms that its digitization includes **Oregon City Courier 1902–1919** and **Oregon City Enterprise 1891–1922**, so the target 1915 issues are unquestionably within the digitized corpus.
- Additional exact 1915 Courier page records continue to surface through web indexing (for example Jan. 7 page 7 and Feb. 4 page 9), proving that more pages exist than some earlier partial issue inventories suggested. This reinforces the need to derive the final page inventory from issue navigation/scan holdings rather than assume an 8-page default.

Recovery methods attempted in this pass:

- Exact-date searches against NewspaperArchive for 1915 Enterprise pages.
- Image searches targeting 1915 Courier/Enterprise scans at Historic Oregon Newspapers, OldNews, and NewspaperArchive.
- Direct attempts to surface JP2/PDF scan URLs from the Historic Oregon Newspapers page records.

Result:

- None of these paths exposed a 1915 scan as a renderable page image in the current tool environment.
- No page was promoted to `VISUALLY VERIFIED`.

## Fourth recovery attempt — 21 Aug 2026: Open ONI IIIF route

A more promising technical route was identified by checking the current Open ONI API documentation. Historic Oregon Newspapers runs Open ONI. Open ONI exposes IIIF representations in a predictable pattern:

- title collection: `/lccn/{lccn}.json`
- issue manifest: `/lccn/{lccn}/{YYYY-MM-DD}/ed-1.json`
- page canvas: `/lccn/{lccn}/{YYYY-MM-DD}/ed-1/seq-N.json`

The page-canvas JSON is designed to contain the IIIF image resource/service used by the viewer. Open ONI's configured image service normally lives under `/images/iiif`. If the Oregon page-canvas JSON can be fetched, it should reveal the exact image-service URL and permit a direct JPEG request such as the standard IIIF `.../full/full/0/default.jpg` form. This would bypass the failing PDF path and provide an actual scan image suitable for visual inspection.

Direct attempts to fetch the Oregon page-canvas JSON for `sn00063698/1915-07-29/ed-1/seq-3.json` still returned the same archive cache failure, and container retrieval still could not resolve the Oregon host. Therefore this route is technically identified but not yet operational in the current environment.

Additional inventory correction found during this pass:

- The **30 Sep 1915 Courier** issue index exposes **11 scan images**, not an 8-page default. The displayed labels are irregular: Image 6 has no printed-page label, followed by `Page 8, Image 7` through `Page 12, Image 11`. This is exactly the kind of issue-level irregularity that must be preserved and visually checked rather than inferred from OCR or nominal page numbers.

No page was promoted to `VISUALLY VERIFIED` in this fourth attempt.

## Fifth recovery attempt — 21 Aug 2026: cached scan copies on Oregon Theater Project

A useful alternate-image lead was found on the University of Oregon's Oregon Theater Project. Its Grand Theatre research page embeds cached image copies of several Historic Oregon Newspapers scans and exposes the exact underlying PNG asset paths when the image links are followed.

1915 Courier scan copies confirmed there include:

- **1 Apr 1915, page 5** — cached asset path exposed as `oregoncitycourier_04011915_pg5.PNG`.
- **15 Apr 1915, page 2** — cached asset path exposed as `oregoncitycourier_04151915_pg2.PNG`.
- **22 Apr 1915, page 8** — cached asset path exposed as `oregoncitycourier_04221915_pg8.PNG`.
- **23 Sep 1915, page 8** — cached asset path exposed as `oregoncitycourier_09231915_pg8.PNG`.

This is significant because it proves that independent PNG copies of at least some 1915 Courier scans exist outside the Historic Oregon Newspapers viewer. It also gives exact filenames that may be recoverable through another route or cache.

However, all attempts in this environment to fetch those PNG assets still failed with cache/DNS access errors. Direct container retrieval of the Oregon Theater Project PNG also failed at DNS resolution. Therefore these four pages are **not** promoted to `VISUALLY VERIFIED`; the assets are recovery leads only.

The Oregon Theater Project's citations also independently identify additional 1915 Courier pages used in its research, including April 1, April 15, April 22, September 23, December 2, and a February 1915 item. These references are useful for scan recovery, but the project standard still requires inspection of the full original page, not merely trusting a secondary citation.

## Audit consequence

- **No page is promoted to VISUALLY VERIFIED unless the actual scan was rendered and inspected.**
- The prior OCR-supported findings remain leads/evidence candidates only.
- Issue/page inventories and secondary cached-image paths are useful for ensuring the later visual pass does not omit pages, but they are not visual review by themselves.
- 1915 remains incomplete.
- The visual review cannot be truthfully certified while the scan renderer remains inaccessible.

## What will satisfy the standard

The visual pass can proceed as soon as actual scanned pages are available to the visual inspection tool, either because Historic Oregon Newspapers, its Open ONI IIIF endpoint, Oregon Theater Project's cached PNGs, OldNews, NewspaperArchive, or another holder returns renderable PDF/JP2/JPEG/PNG objects, or because the issue/page scans are supplied as files. At that point every page of both the Oregon City Courier and Oregon City Enterprise for 1915 must be visually inspected and logged page by page.
