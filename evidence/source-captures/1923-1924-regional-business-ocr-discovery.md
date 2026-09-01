# 1923–1924 regional newspaper business OCR discovery

Status: **OCR DISCOVERY ONLY — NOT AN ANNUAL VISUAL REVIEW OR COMPLETION CLAIM**

Run date: **1 September 2026**

Purpose: search the online 1923–1924 gap for leads identifying the unnamed **503 Main restaurant** and **505 Main billiards/cigars** uses shown on the May 1925 Sanborn, while retaining promising Oregon City Fifth Street references encountered during the pass.

## Coverage

- Issues inventoried: **1,487**.
- OCR pages checked: **12,096**.
- Machine candidates retained by bounded co-occurrence rules: **750**.
- The public calendars for the *Banner-Courier* and *Oregon City Enterprise* expose no 1923–1924 issues. This run therefore covers regional titles with online scans, not the missing local-newspaper interval.
- OCR was used for discovery only. Search silence is not evidence that a business, person, address, or event did not exist.

| LCCN | Title | 1923 issues | 1924 issues | Total issues | Pages |
|---|---|---:|---:|---:|---:|
| `sn96088133` | Eastern Clackamas News | 52 | 52 | 104 | 424 |
| `sn97071044` | Gresham Outlook | 103 | 104 | 207 | 881 |
| `sn84006724` | Hillsboro Argus | 52 | 51 | 103 | 766 |
| `sn00063558` | Mt. Scott Herald | 16 | 0 | 16 | 64 |
| `sn98062568` | The Advocate | 33 | 48 | 81 | 336 |
| `sn90066132` | Capital Journal | 72 | 284 | 356 | 3,406 |
| `sn85042470` | Oregon Statesman | 312 | 308 | 620 | 6,219 |

## Exact-pattern discovery outcome

| Pattern | Candidate pages | OCR-stage result |
|---|---:|---|
| Edwin / Ed / E. F. Farr | 0 | No exact OCR match |
| Alice Farr | 0 | No exact OCR match |
| Farr | 29 | Ambiguous surname candidates; strongest Oregon City-context pages sent to scan review |
| Kwality / common OCR variant | 1 | Sent to scan review |
| Quality Restaurant / Cafe | 0 | No exact OCR match |
| J. Jager / Jager | 2 | Sent to scan review |
| Leland & Little | 0 | No exact OCR match |
| Clem Dollar | 0 | No exact OCR match |
| Fifth Street with bounded Oregon City/trade context | 6 | Strongest and representative pages sent to scan review |

The scan-review results are recorded in `1923-1924-regional-business-candidate-review-2026-09-01.md`. None of the reviewed candidates identified the 503 or 505 occupant.

## OCR retrieval gap resolved at scan level

The OCR endpoint for *Hillsboro Argus*, 5 June 1924, page 8, did not return usable text. The page PDF remained retrievable and was visually inspected. It is a full-page Weill's Department Store “Dollar Day Sales” advertisement in Hillsboro and contains no apparent target lead. Keep the failed endpoint recorded as an **OCR-layer gap**, not a missing-page gap.

- OCR endpoint: https://oregonnews.uoregon.edu/lccn/sn84006724/1924-06-05/ed-1/seq-8/ocr.txt
- Page scan: https://oregonnews.uoregon.edu/lccn/sn84006724/1924-06-05/ed-1/seq-8.pdf

## Limits and next step

- This was an every-exposed-page **OCR discovery** pass, followed by bounded scan review of exact-name-like and strongest contextual candidates. It was not a visual inspection of all 12,096 pages.
- The remaining highest-value newspaper source is 1923–1924 Oregon City local-newspaper microfilm.
- The 1924 Oregon City directory, municipal restaurant/pool-hall/cigar/business-license records, and the historic-resource research files remain higher-value address-level sources than another repetition of the same regional OCR search.
- Machine-readable coverage, all **100 shortlisted candidate records**, source links, and the single OCR error are preserved in `1923-1924-regional-business-ocr-discovery.json`. The file also retains the aggregate count of **750 raw rule matches**; low-score common-name/number co-occurrences are intentionally not duplicated into the committed artifact.
