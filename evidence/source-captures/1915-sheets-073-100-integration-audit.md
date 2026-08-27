# 1915 sheets 73–100: address-history integration audit

Date: 27 August 2026. Scope: task 1 only, reconciling the saved `S-120` / `E-107` batch. Base commit: `03d46bd6845291b67ed683856468b555fb4920ea`.

This is an integration audit, not a second certification of all 108 images. The saved visual log was checked against address histories, source/evidence records, business/person indexes, timeline, and YAML. Saved scans for 5 August pages 1/3, 12 August page 5, and 23/30 September page 1 were visually rechecked; the Price incident and directory number were enlarged. No sheet after 100 was reviewed. **1915 remains IN PROGRESS.** Commit/push is the separate task 2.

## Disposition of material findings

| Finding in the saved batch | Integration and limits |
| --- | --- |
| 507 Main: W. W. Bradley, furniture | Existing building narrative retained; business/person IDs `BUS-026` / `P-041` and address-register, business-timeline, master-timeline and YAML links added. Dated listings, not uninterrupted occupancy or a proven Young-to-Bradley sale. |
| 509 Main: H. P. Brightbill, groceries | `BUS-027` / `P-042` registered and linked. Do not silently merge with Henry Brightbill `P-034`; the older 503/509 identity question remains open. |
| 511 Main: Geo. A. Harding, druggist | Existing `BUS-007` / `P-001` records now explicitly distinguish the 1915 **511** listing from later 507/Harding-block labels. No exact historic footprint or business continuity between distant dates inferred. |
| 519 Main: F. F. Theroux, pianos/sewing machines | 5 August p3 supports a dated number; `BUS-029` / `P-044` registered. Address register uses no invented building ID. Prior Fifth/Main wording is not a proven move, same storefront, or 501/503/505 assignment. |
| 527 Main: Price Bros. clothing store and incident | `BUS-028` / `P-043` (Al Price) linked to the 527 history, address/business registers, timeline, `E-107` and YAML. Publication date is 5 August; incident wording is Friday night of the preceding week. The number comes from the same issue's directory, not the incident text. |
| Holman/Randall at Fifth and Main | Existing `E-054` now links the batch's repeated notices and location-only corroboration. Still no exact 501/503/505 assignment. |
| Main repaving and municipal work | Existing repaving capture retained and linked into the 1915 timeline. Forecast completion, assessments and payments do not establish target-building removal or rebuilding. Other-block notices remain excluded from target parcel claims. |
| Bannon enlargement; Brunswick sale/planned repairs | Retained as named-business changes with unresolved exact numbers, now explicitly carried in `RL-043` below; not assigned to a numbered storefront or property-transfer chain. |
| Other named/intersection advertisements, unnamed pool halls, unrelated fires/property notices | Coverage/context only unless they change a supported address state. No new tenant, identity merge, or target event inferred. |
| January 14, October 14, September 2 source exceptions | All three existing manual callouts retained unchanged; neither new interpretation nor integration resolves them. |

## Price Bros. correction and evidence boundary

- **Direct scan, 5 August p1:** smoke was found in the clothing store on Friday night of the preceding week; an electric iron left on was burning boards at the rear; switching off the current averted a potentially serious fire. Al Price is named proprietor. No dollar loss or subsequent closure/repair is stated.
- **Direct scan, 5 August p3:** Price Bros., **527 Main St.**, phone 107. The advertised establishment year 1895 does not prove occupancy at this number since 1895.
- **Calendar derivation:** the stated Friday is **30 July 1915**. The earlier Thursday reading is superseded, not silently removed from the correction history.
- **Strong same-issue inference:** the incident concerns the business listed at 527. Neither page proves ownership of the building, continuity from the 1912 Bailey & Price billiard business, or identity of its Price partner with Al Price. The 1935 Swartz structure is not backdated to 1915.

Sources: [incident scan](../../newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-01.pdf), [directory scan](../../newspapers/oregon-city-courier/1915-sheets-073-100/1915-08-05-seq-03.pdf), media `IMG-0058` / `IMG-0060`. Original PDFs and manifest hashes are unchanged.

## Named-location follow-ups retained, not forced into an address

- **Bannon & Co., 12 August p5, “STORE ENLARGED”:** reports about 300 square feet being added upstairs for women's apparel; says Main Street but prints no number. This is reported work in progress, not a completion certificate. The saved September 30 advertisement names the Masonic Temple; exact-number and same-premises mapping remain follow-ups.
- **Brunswick hotel/restaurant, 23 September p1, “BRUNSWICK IS SOLD”:** reports a purchase on Main near Seventh and planned alterations, including a new plate-glass front. This is newspaper sale wording, not a deed or proof of which real-estate/business interest transferred.
- **30 September p1, “TROUBLE OVER NAME”:** describes a proposed rename on opening after $7,000 of repairs/alterations; neither the final name nor completion/opening is established by this report.

These remain active online leads under `RL-043`, not manual callouts: reasonable online recovery of their exact numbers has not been exhausted in this integration task.

## Preserved boundaries and checkpoint

- No finding changes the unresolved 503/505 occupant status.
- No uncertainty, prior source, or source exception was deleted; no ID was renumbered.
- Existing 501 license rows found under the 503 business-timeline heading were moved to a dedicated 501 section without changing their evidence or chronology.
- The archive index wrongly labeled `BUS-020` as Bailey & Price; the canonical business index and YAML assign that ID to L. Hylton. The index label is corrected with its reason preserved. Bailey & Price remains a separately sourced, unmerged 1912 business without a newly invented identity.
- Courier remains **100/123 sheets processed**; Enterprise **0/107**. This audit adds zero pages to those counts.
- Absence of a target mention remains coverage only, never vacancy or non-use evidence.

Local checks passed: archive validator, whitespace/diff check, all 108 manifest SHA-256 matches, preservation of existing YAML IDs, newly registered business-address links, and removal of the misplaced 501 rows from the 503 section. No source binaries or manifest entries changed. These checks do not constitute a commit or remote read-back; task 2 must check current remote state before committing/pushing.

## Task 2 pre-publication verification — 27 August 2026

The user authorized commit and push of the task 1 package. A fresh fetch confirmed local `main` and `origin/main` both at `03d46bd6845291b67ed683856468b555fb4920ea`, with no intervening upstream changes. Archive validation and diff checks were rerun before publication; source hashes, retained IDs and address relationships are also checked in the final package. The task 1 pause wording above is the historical pre-commit checkpoint, not a new research stop. Newspaper review remains paused before sheet 101, with no change to year status or page coverage. Push/read-back confirmation belongs to the task 2 handoff, not an assumed result of these local checks.
