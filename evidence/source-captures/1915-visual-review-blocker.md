# 1915 visual page-by-page review — current access blocker

Date: 2026-08-21

Project standard: every available newspaper page must be visually inspected from the actual scanned page image/PDF/JP2. OCR, search snippets, and extracted text are discovery aids only and do not count as page review.

## Attempt made in this research turn

A fresh attempt was made to begin the 1915 visual re-review using the Historic Oregon Newspapers scans for the Oregon City Courier (`sn00063698`). The archive issue indexes and individual page records are discoverable, including page-count information and links labelled PDF/JP2. However, the available research browser is currently returning cache/safety failures for the scan/PDF URLs rather than an image-renderable PDF object. Even a search result whose URL ends in `.pdf` is being exposed to the research browser as extracted text/HTML rather than as `application/pdf`, so the screenshot/visual-page operation cannot be invoked on it.

Examples attempted in this turn include January 7, January 28, and December 16, 1915 Courier page/PDF URLs. Direct scan/PDF opens returned cache misses or URL-safety failures. A screenshot attempt against a surfaced December 16 `.pdf` search result failed because the browser reported that the result was not an `application/pdf` object and that webpage screenshot was not enabled.

Container/network retrieval was also attempted for a Courier page PDF and failed at DNS resolution for `oregonnews.uoregon.edu`.

## Audit consequence

- **No page is promoted to VISUALLY VERIFIED from this turn unless the actual scan was rendered and inspected.**
- The prior OCR-supported findings remain leads/evidence candidates only.
- 1915 remains incomplete.
- The visual review cannot be truthfully certified while the scan renderer is inaccessible.

## What will satisfy the standard

The visual pass can proceed as soon as actual scanned pages are available to the visual inspection tool, either because the archive begins returning renderable PDF/JP2/image objects or because the issue/page scans are supplied as files. At that point every page of both the Oregon City Courier and Oregon City Enterprise for 1915 must be visually inspected and logged page by page.
