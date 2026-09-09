# 19 January 1912 Courier thread — knowledge preservation audit

Date: 9 September 2026  
Scope: thread-level repository preservation audit; **not a new historical-source claim**.  
Annual status: **1912 IN PROGRESS**.

## Repository synchronization control

Before this preservation write, current `main` was rechecked and had advanced through parallel work to `df5e74091bea17d0c746cbcf4e02c7a713d8f00c` (`Add Flor Morton new-chat handoff`). This audit is additive and does not reset, revert, overwrite, or reinterpret that parallel work.

Current `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` were re-read before writing. This checkpoint preserves what was learned in the Jan. 19, 1912 Courier page-review thread and verifies where that knowledge already lives in the authoritative repository.

## Knowledge preserved from the supplied Jan. 19 page set

### Primary pages and visual-review state

The project steward supplied *Oregon City Courier*, **19 January 1912**, printed pages **1–4**. All four pages were visually inspected from faithful page PDFs and count as **VISUALLY VERIFIED** under the annual newspaper audit.

Canonical repository binaries:

- `newspapers/oregon-city-courier/1912-01-19-page-1.pdf`
- `newspapers/oregon-city-courier/1912-01-19-page-2.pdf`
- `newspapers/oregon-city-courier/1912-01-19-page-3.pdf`
- `newspapers/oregon-city-courier/1912-01-19-page-4.pdf`

SHA-256 controls:

- page 1 — `47f0ee2c0e090e3ec6947831250ea06ee4fe64850382581dce5877aa96f85679`
- page 2 — `01e202249f48757ecada6946ca361c7d5b3cf5087d49a0778a382c4cab75af99`
- page 3 — `c261c85d058f2ac376fa59975ce49eea0fcbd66e8703e99908dfc2b3c4521611`
- page 4 — `36c385cc184da7d14070ebe3f645b4d1225e92ce03f48e39f267263839e7b07e`

The exact archive PDF derivatives were committed in `975e5b03ee365278f3b8fde8567b2ffd3a2f0187` only after hash verification against the supplied copies.

### Duplicate-upload reconciliation

The later uploads named `Courier Jan 19, 1912 p1(1).pdf` through `p4(1).pdf` are byte-for-byte duplicates of the first four supplied PDFs. Their SHA-256 values match page-for-page. Per repository policy, no duplicate binaries were created; the duplicate relationship and exclusion reason are preserved in the source capture, `S-307`, the research log, and this audit.

### Target-block screening result

The pages were screened for the active Fifth–Sixth Main Street targets, including **501 / 503 / 505 / 507 / 509 / 511 Main**, Fifth/Main, Post Office context, H. N. / H. H. Smith, G. H. Young, Geo. A. Harding / Harding Drug Store, H. P. Brightbill, Chicago Store, Palace Saloon / Joe Wilson, Gambrinus, Schrader, pool-room / pool-hall references, saloons, fires, demolition, construction, moves, property transactions, and related business-transition wording.

Visual inspection of pages 1–4 established **no defensible new target-address occupant, ownership, business-transition, or structural claim**, and did not resolve the H. N. Smith / H. H. Smith initials conflict. This is a bounded coverage result only and is not evidence of vacancy, non-operation, non-ownership, non-construction, or absence of an event.

No new `E-###`, building, business, person, ownership, crosswalk, open-question, research-lead, or target timeline event was warranted from the four-page no-hit result.

### Non-target Oregon City context retained

Page 1 directly reports a high-Willamette event in the article **“UP AND GOING SOME.”** The article says high water temporarily shut many mill departments, leaving about **1,200 workers** idle for several days; water was coming in at the **end of Main Street**, workmen built a plank barrier, Hawley pulp mill A was surrounded, Oregon City–Canemah street-car tracks were submerged, and Abernethy Creek was out of its banks. Classification remains **DOCUMENTED / DIRECT, VISUALLY VERIFIED — NON-TARGET CITY / INFRASTRUCTURE CONTEXT**. It does not prove flooding at 501–511 Main.

Page 1 also directly reports the article **“TO DREDGE THE CHANNEL.”** It describes a Secretary of War recommendation for a **$24,000** appropriation for a six-foot Portland–Oregon City Willamette River channel, with a proposed 200-foot width to Clackamas Rapids, 100 feet above that point, removal of County's Rock, and estimated **$3,500 annual maintenance**. This remains **DOCUMENTED / DIRECT, VISUALLY VERIFIED — NON-TARGET TRANSPORTATION / INFRASTRUCTURE CONTEXT** and is not propagated into a 503/505 property claim.

Pages 2–4 contain local/regional news, advertisements, editorial material, Clackamas Southern Railway bond advertising, Oregon City merchants, and a J. Levitt clearance advertisement, but no reviewed item supplied a defensible new target-block fact.

## Page-8 Harding Drug Store lead remains separate

The existing *Oregon City Courier*, **19 January 1912, page/image 8** lead stating that **Percy Cross accepted a position in the Harding drugstore during the absence of A. E. Wilmot** remains **OCR/TEXT ONLY**. Pages 1–4 do not certify page 8. The next high-value action for this issue is to obtain and visually inspect pages/images **5–8**, with priority on page 8.

## Canonical repository locations already synchronized

The thread's substantive knowledge is already preserved in the following authoritative locations:

- `evidence/source-captures/1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md` — detailed page-level review, hashes, findings, limits, and next actions.
- `evidence/source-register.md` — source **`S-307`**, including canonical issue, repository binaries, hashes, preservation commit, duplicate-upload handling, target-screen result, and page-8 state.
- `database/sources.yml` — YAML mirror for **`S-307`**.
- `registers/research-log.md` — 9 September 2026 thread integration entry recording visual-review credit, duplicate reconciliation, binary preservation, `S-307`, no new `E-###`, and the page-8 pending state.
- `newspapers/oregon-city-courier/1912-01-19-page-1.pdf` through `page-4.pdf` — exact preserved primary-source binaries.

The integration commit `77880a8b610bce18da8f208d1cb4d469c62c23ed` synchronized the source register, database source mirror, detailed source capture, and research log. Temporary ingest/integration automation used solely to move the binary/source metadata into `main` was removed after successful use and is not part of the permanent workflow.

## Propagation / completeness decision

This audit confirms that **all substantive knowledge learned in this Jan. 19 pages 1–4 thread is preserved in the repository**. No additional entity or claim-level propagation is justified unless a later source changes the historical interpretation.

The outstanding work is research, not unsaved knowledge:

1. visually inspect Jan. 19 pages/images 5–8, especially page 8;
2. continue the issue-by-issue 1912 Courier visual audit;
3. continue the broader 1912 source-class work required by `RESEARCH-STANDARD.md` before any annual status advance.

Do not infer historical absence from the four-page no-hit result, do not duplicate the `(1)` upload aliases, and do not upgrade the page-8 Harding Drug Store lead until the actual scan is visually inspected.
