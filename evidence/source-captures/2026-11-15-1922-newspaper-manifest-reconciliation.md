# 1922 newspaper issue/page manifest reconciliation — 15 November 2026

**Year status: IN PROGRESS.** This is a repository-record reconciliation, not a new visual inspection or a declaration of ONLINE COMPLETE.

## Scope and method
Compared all **24 committed monthly JSON manifests** (`newspapers/banner-courier/1922-MM/manifest.json` and `newspapers/oregon-city-enterprise/1922-MM/manifest.json`) against the corresponding January–December 1922 monthly visual-review records. For every manifest, inspected issue dates, declared page counts, number of page entries, calendar absence flags, and manifest-level status. All listed issue `page_count` values matched the number of page entries. This is **not** a fresh inspection of 928 PDFs or a live re-query of the archive's 1922 calendars.

The monthly visual-review source captures support **104 issues / 928 page scans inspected**:
- Banner-Courier: **52 issues / 512 pages**
- Oregon City Enterprise: **52 issues / 416 pages**

## Issue-by-issue reconciliation

Each number after a date is the number of page sequences in the manifest; the corresponding monthly source capture records visual inspection. An asterisk flags source-image damage or a calendar exception described below.

| Month | Banner-Courier issue dates (pages) | Enterprise issue dates (pages) | Total issues / pages |
|---|---|---|---|
| Jan | 05(8), 12(10), 19(8), 26(10) | 06(8), 13(8), 20(8), 27(8) | 8 / 68 |
| Feb | 02(10), 09(10), 16(10), 23(12) | 03(8), 10(8), 17(8), 24(8) | 8 / 74 |
| Mar | 02(10), 09(10), 16(10), 23(12), 30(10) | 03(8), 10(8), 17(8), 24(8), 31(8) | 10 / 92 |
| Apr | 06(10), 13(10), 20(10), 27(10) | 07(8), 14(8), 21(8), 28(8) | 8 / 72 |
| May | 04(10), 11(10), 18(10), 25(10) | 05(8)*, 12(8), 19(8), 26(8) | 8 / 72 |
| Jun | 01(10), 08(14), 15(10), 22(9)*, 29(10) | 02(8), 09(8), 15(8)*, 23(8), 30(8) | 10 / 93 |
| Jul | 06(8), 13(8), 20(10), 27(10) | 07(8), 14(8), 21(8), 28(8) | 8 / 68 |
| Aug | 03(8), 10(10), 17(8), 24(10), 31(8) | 04(8), 11(8), 18(8), 25(8) | 9 / 76 |
| Sep | 07(9), 14(10), 21(8), 28(10) | 01(8), 08(8), 15(8), 22(8), 29(8) | 9 / 77 |
| Oct | 05(10), 12(10), 19(10), 26(10) | 06(8), 13(8), 20(8), 27(8) | 8 / 72 |
| Nov | 02(10), 09(10)*, 16(10), 23(10), 30(8) | 03(8), 10(8), 17(8), 24(8) | 9 / 80 |
| Dec | 07(12), 14(12), 21(12), 28(8)* | 01(8), 08(8), 15(8), 22(8), 29(8)* | 9 / 84 |
| **TOTAL** | **52 / 512** | **52 / 416** | **104 / 928** |

## Status reconciliation — do not erase prior audit work

- January–June: all 12 monthly manifests state **VISUALLY VERIFIED** (subject to May/June source defects).
- July–December: all 12 monthly manifests retain **RETRIEVAL ONLY** even though the separate July and August 13 September review records and September–December 14 September review records document inspection of all rendered page images.
- This is a **manifest-status synchronization defect**, not proof that July–December pages were never inspected. Before changing canonical manifest statuses, decide whether the monthly review records meet the standard for page-level visual credit; retain the source-damage qualifications.
- The September–December captures specifically distinguish gross page-integrity review from subsequent targeted article/advertisement verification. Therefore **page inspection must not be conflated with exhaustive content extraction**.

## Explicit exceptions / next recovery targets

1. **Enterprise 5 May 1922, sequences 1–2**: material missing source-image regions. Inspect alternate scans/microfilm for missing content.
2. **Banner-Courier 22 June 1922, sequence 9**: minor top-edge loss.
3. **Enterprise 15/16 June 1922 date exception**: June manifest inventories a **15 June** issue and flags expected Friday **16 June** as absent from archive calendar; check original masthead, publication scheduling, and alternate calendars before treating this as a missing issue or duplicate.
4. **Banner-Courier 9 November 1922, sequences 7–8**: large opaque obstructions in central/lower portions; priority alternate-image recovery.
5. **Banner-Courier 28 December 1922**: torn/missing edge and corner areas on several pages.
6. **Enterprise 29 December 1922**: ragged/torn edge and binding/scan loss.

These source defects are **not** negative evidence for missing businesses, ads, construction notices, or occupancy. The repository's issue inventories show no other expected-weekday absences besides the Enterprise June 16 flag; this finding is limited to the existing manifests, not an independently refreshed archive-calendar inventory.

## Annual closeout blockers
- Investigate/recover the above damaged or date-exception source material, documenting unsuccessful recovery and manual callouts where necessary.
- Verify monthly visual-review evidence and synchronize July–December manifest statuses without silently granting more historical-content coverage than was performed.
- Finish targeted page-level verification of relevant ads/notices, especially September–December.
- Reconcile all other online source classes, source/evidence records, entity crosslinks, research leads, and numbered manual follow-ups.
- Only then consider ONLINE COMPLETE; do not change `registers/year-status.md` based solely on this arithmetic audit.

## Cross-record propagation
This batch establishes an **audit/coverage fact only**, no new historical occupant, owner, business, exact-address assignment, construction event, or photograph interpretation. Therefore no timeline/business/person/building/YAML historical fact is added. The year remains IN PROGRESS.
