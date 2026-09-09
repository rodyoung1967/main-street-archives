# 1912 Morning Enterprise July 6–9 visual-review checkpoint

Date: 8 September 2026  
Status: **IN PROGRESS — VISUAL NEWSPAPER AUDIT CHECKPOINT**

Purpose: continue the exhaustive 1912 online audit from the existing July/August *Morning Enterprise* ledger and convert a bounded set of pages from inventory/text-layer coverage into actual scan-review credit under `RESEARCH-STANDARD.md`.

## Repository synchronization control

Immediately before this batch, `research/1912-online-audit` was synchronized with then-current `main` through merge commit `e4fb1e94d8b64d5154d0d603fa8779878b7b3544`. The `main` parent incorporated by that synchronization was `cdf30a1e99277eb27367325d3dd68e58adc9532c` (`Add temporary live LOC Oregon City inventory probe`). A fresh branch check immediately before writing this capture confirmed that `main` was still at `cdf30a1e99277eb27367325d3dd68e58adc9532c`.

This remains additive 1912 coverage/provenance work. It does not replace newer master registers, timelines, databases, or parallel research.

## Faithful scan route recovered

The Oregon Historic Newspapers single-page PDF derivatives are presently accessible for many pages in this batch and render the actual scanned newspaper page. Those rendered scans were visually inspected page-by-page. This is materially different from OCR/text-layer review and therefore earns `VISUALLY VERIFIED` credit only for the pages explicitly listed below.

The earlier checkpoint's PDF/JP2 failure was therefore an access/interface limitation for that earlier attempt, not proof that all page-image derivatives were unavailable.

## Issue/page review ledger

| Issue date | Authoritative online count | Page/image | Audit state | Notes |
| --- | ---: | ---: | --- | --- |
| 6 Jul 1912 | **4** | 1 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 6 Jul 1912 | **4** | 2 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 6 Jul 1912 | **4** | 3 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 6 Jul 1912 | **4** | 4 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 7 Jul 1912 | **4** | 1 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 7 Jul 1912 | **4** | 2 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 7 Jul 1912 | **4** | 3 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 7 Jul 1912 | **4** | 4 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 9 Jul 1912 | **4** | 1 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 9 Jul 1912 | **4** | 2 | **OCR/TEXT ONLY + RETRIEVAL GAP FOR VISUAL REVIEW** | Archive page and one-page PDF text layer open, but repeated scan-render attempts failed; JP2 delivery is unsupported in the current route. Do not award visual credit. |
| 9 Jul 1912 | **4** | 3 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |
| 9 Jul 1912 | **4** | 4 | **VISUALLY VERIFIED** | Actual single-page PDF scan inspected. |

Thus this batch adds **11 visually verified pages**. The 6 July and 7 July issues are complete at 4/4 visually reviewed pages each. The 9 July issue remains incomplete at 3/4 visually reviewed pages because page/image 2 still requires a faithful visual derivative.

Canonical issue routes:

- 6 Jul 1912: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-06/ed-1/
- 7 Jul 1912: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-07/ed-1/
- 9 Jul 1912: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-09/ed-1/

9 Jul page/image 2 gap route:

- HTML/text layer: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-09/ed-1/seq-2/
- PDF object: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-09/ed-1/seq-2.pdf
- JP2 object: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-09/ed-1/seq-2.jp2

## Target-address / structural-event result

Visual inspection of the 11 accessible scans did **not** identify a safe new exact-address claim for **501, 503, 505, 507, 509, or 511 Main**, did not resolve the **H. N. Smith / H. H. Smith** initials conflict, and did not connect the 10 May 1912 Main Street demolition/rebuilding statement (`E-090` / `RL-038`) to the Fifth–Sixth target frontage.

This is a bounded coverage result only. It is not evidence that a target occupant, business, demolition, construction event, or building did not exist.

## Useful non-target controls observed on the scans

### Portland Railway Light & Power — 617 Main / Beaver Building

The 6 July page 3, 7 July page 3, and 9 July page 3 scans carry a large `Change of Location` advertisement stating that the Portland Railway Light & Power Company's light and power department would be located at **617 Main Street, in the Beaver Building, after July 4th**.

Classification: **DOCUMENTED / DIRECT, VISUALLY VERIFIED — NON-TARGET MAIN STREET CONTROL**.

This is outside the Fifth–Sixth target frontage. It must not be used to assign the May demolition/rebuilding statement to 501–511 Main. It is retained as useful 1912 Main Street address/building-name context only.

Canonical example:
- https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-07/ed-1/seq-3.pdf

### Fourth and Main saloon / poker-game reference

The 7 July page 1 scan contains the detective-agency report describing a small poker game `over the saloon on Fourth and Main streets`. This is a direct location statement but is outside the target Fifth–Sixth frontage and does not identify the May teardown buildings.

Classification: **DOCUMENTED / DIRECT, VISUALLY VERIFIED — NON-TARGET LOCATION CONTROL**.

Canonical page:
- https://oregonnews.uoregon.edu/lccn/sn00063701/1912-07-07/ed-1/seq-1.pdf

## Cross-record propagation decision

No new `E-###` or `S-###` is created from this bounded batch. No target building, business, person, timeline, crosswalk, or YAML/database fact changes. The verified 617 Main / Beaver Building and Fourth/Main controls are useful contextual observations but do not materially alter the current 503/505 histories or resolve an active target-address claim.

Accordingly, this source capture is the appropriate repository destination for the new coverage state. Do not manufacture target occupancy, vacancy, demolition, construction, or identity conclusions from the no-hit portion of the review.

## Next actions

1. Retry a faithful visual derivative for **9 Jul 1912 page/image 2**; if reasonable online derivative recovery remains unsuccessful, preserve it as an exact retrieval gap and eventually cross-reference it into the 1912 manual-closeout list.
2. Continue the actual-surviving-date *Morning Enterprise* July ledger after 9 July, obtaining authoritative issue counts and visually reviewing every accessible page scan.
3. Reuse the newly working one-page PDF scan route for earlier ledger dates that currently have count/text credit but lack actual visual-review credit.
4. Continue the weekly *Oregon City Enterprise* issue/page ledger and visual review in parallel.
5. Continue the *Oregon City Courier* audit, including unresolved complete counts for 3 May and 2 August and recovery of the genuine 17 May image 2.
6. Keep `RL-038` open unless a source directly or by defensible cross-source inference identifies which Main Street buildings were demolished/rebuilt in May 1912.
7. Preserve the H. N. Smith / H. H. Smith conflict until an independent identity bridge is found.
8. Keep **1912 = IN PROGRESS** until every current-standard online source/page is visually reviewed or converted into a precise documented retrieval/manual gap.
