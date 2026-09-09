# 1912 native-PDF visual-review route — 8 September 2026

Status: **WORKING VISUAL ACCESS ROUTE CONFIRMED; BULK PRESERVATION STILL BLOCKED**

This checkpoint supersedes the earlier assumption in today's audit notes that the current research interface could not visually expose 1912 Historic Oregon Newspapers page PDFs.

## Breakthrough

When an indexed Historic Oregon Newspapers HTML page itself can be opened through the web research layer, its native **PDF** link is exposed as a clickable archive link. Clicking that link returns the actual one-page PDF (`application/pdf`), which can then be rendered as a screenshot and visually inspected.

Verified test:

- *Oregon City Courier*, 5 January 1912, page/image 6
- HTML page: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-05/ed-1/seq-6/
- Native page PDF: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-05/ed-1/seq-6.pdf
- The clicked result was returned as a one-page `application/pdf` and was rendered visually in the research environment.

## Visual verification result

The actual scan clearly reads, among other advertisements:

- **H. N. Smith — 503 Main Street**;
- **G. H. Young — 507 Main Street**;
- **H. P. Brightbill — 509 Main St.**;
- **Geo. A. Harding — 511 Main St.**

This independently re-confirms the existing current-main visual interpretation and again demonstrates the OCR errors on the same page (`603`, `609`, and truncated `51`). No new claim-level evidence is needed because these facts are already integrated; this is audit credit / method confirmation.

The scan also visually confirms the broader business-grid context already registered in the project, including Chicago Store just below the Post Office, M. E. Dunn near the Post Office, Tolpolar opposite the Post Office, Clems Chop House at Fifth/Main, Price Bros. at Sixth/Main and other adjacent businesses.

## Important distinction from failed pseudo-PDF route

Earlier search-engine results sometimes surfaced URLs ending in `.pdf` but returned extracted text rather than an actual PDF object. Those still do **not** count as visual review.

The valid route is:

1. open the indexed **HTML page**;
2. follow that page's native **PDF** link;
3. verify that the returned object is `application/pdf`;
4. render/screenshot the one-page PDF;
5. visually inspect the scan itself.

Only that actual-scan route earns visual credit.

## JP2 / IIIF status

The HTML page also exposes a JP2 link, but the test JP2 fetch still hit a cache miss. The native PDF route is therefore the currently reliable visual route.

The 1915 archive demonstrates a separate IIIF derivative route constructed from page JSON metadata, but the current web layer still does not expose arbitrary constructed `.json` metadata endpoints. The native PDF route avoids needing that metadata for visual inspection.

## Binary preservation status

After the PDF had been successfully opened in the web research layer, a separate container download of the same canonical PDF URL was attempted. It still failed because the container execution environment cannot resolve/retrieve the archive host. Therefore:

- **visual inspection is now possible online** for pages whose HTML page and native PDF link can be opened;
- **local binary mirroring/hashing into the repo is still blocked** through the current container path.

Do not confuse this preservation limitation with a visual-access limitation.

## Audit consequence

The exhaustive 1912 newspaper audit should continue using this native-PDF route wherever the page HTML can be opened. Pages for which the HTML or native PDF remains inaccessible after reasonable attempts should be logged individually/range-wise as retrieval gaps.

The year remains **IN PROGRESS**. This checkpoint does not certify annual or title-level completeness.
