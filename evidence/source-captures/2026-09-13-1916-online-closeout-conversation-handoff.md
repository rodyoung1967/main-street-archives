# 1916 ONLINE closeout conversation handoff — 13 September 2026

## Purpose

Continue the 503/505 Main Street, Oregon City historical research project from `rodyoung1967/main-street-archives`, branch `main`, workstream **ANNUAL-1916 / ONLINE CLOSEOUT**.

The immediate goal is to finish every reasonable public-online source class for 1916 and, if the repository standard is satisfied, formally change 1916 from **IN PROGRESS** to **ONLINE COMPLETE**. Do **not** call the year ONLINE COMPLETE merely because the newspaper run is essentially finished. Remaining inaccessible/restricted/physical sources must be preserved as explicit manual callouts rather than treated as negative evidence.

## Mandatory startup for the next conversation

1. Fetch/sync the newest `main` and treat it as authoritative.
2. Do not reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work.
3. Read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely from current `main`.
4. Read this handoff completely.
5. Read the current `registers/year-status.md`, `evidence/source-captures/1916-online-audit-checkpoint.md`, newest 1916 source-class/manual-callout captures, and all commits added after this handoff.
6. Run `validate_archive.py` before substantive repository changes if practical and again after writes.
7. Visually inspect original archival scans whenever accessible. OCR/search text is discovery/navigation only and never substitutes for visual inspection.
8. Preserve uncertainty and retrieval gaps. Do not treat source silence or an inaccessible source as proof of vacancy/non-use.
9. Keep business operation, business ownership, property ownership, licensing, tenancy, trade names, street addresses, and physical buildings separate.
10. Do not send institutional requests, authorize fees, purchase records, or initiate manual outreach without Rodney's explicit approval.

## Newspaper status at end of this conversation

The exhaustive ordinary 1916 newspaper audit has been carried through year-end.

- *Oregon City Courier*: **458/458 pages visually reviewed — complete**.
- *Oregon City Enterprise*: **425/426 pages certified visually reviewed**.
- Combined newspaper coverage: **883/884**.
- Every ordinary Enterprise issue through **29 December 1916** has been reviewed page-by-page.
- The sole uncertified page is the genuine weekly *Oregon City Enterprise* **12 May 1916 page 8**. The archive's apparent sequence-8 item is actually a *Morning Enterprise* page. This remains a documented retrieval gap and must not be treated as a negative finding.

Final year-end newspaper certification commit from this conversation:

- `37728c7bf2e8782afa31f8077ef11084300d8e56` — `Certify December 15 22 and 29 1916 Enterprise reviews`

Immediately preceding batches included:

- `e023213086b10677fddf535204ce633714d77a48` — Nov. 24 / Dec. 1 / Dec. 8 certification.
- `f748e66cd37fdb71dc64d49ca6cad687c4263462` — Nov. 3 / Nov. 10 / Nov. 17 certification.

All scans in those batches were visually inspected individually. Corrupt/unreadable local renders were re-rendered and the clean replacement image was visually verified before certification.

## What the newspaper audit found

No reviewed year-end page directly established a target-premises occupant, proprietor, owner, tenant, licensee, trade name, sale/transfer, construction, demolition, rebuilding, closure, vacancy, fire, or move at **501, 503, 505, 505½, or 507 Main Street**.

Recurring explicit non-target geographic controls included:

- Larsen & Company at **10th and Main**.
- Morgan's on/near **Seventh Street**.
- W. S. Eddy at the **Fashion Stable, between Fourth and Fifth on Main Street**.
- Printed real-estate-transfer sections with no source-explicit target-block transfer in the reviewed issues.

These controls are useful for showing that Main Street references were examined and geographically distinguished; they are not target-block occupancy evidence.

## Online gaps converted to manual closeout work in this conversation

A focused closeout pass determined that several previously vague ONLINE-FIRST items have exhausted reasonable public-online routes and can now be carried as precise manual tasks. The repository integration for the first group completed successfully with validation before and after integration.

### MF-061 — 12 May 1916 weekly Enterprise page 8

Reasonable online recovery routes are exhausted. Preserve as a **YEAR-CLOSEOUT / MANUAL CALLOUT** for inspection of source film/microfilm or another authoritative physical/restricted copy. The missing page remains a retrieval gap, not negative evidence.

### MF-062 — Sohns & Woodbeck 1916–1917 directory

The directory's existence and holding/access routes are established. FamilySearch catalog/access routes, Oregon Historical Society holding information, the public Oak Lodge/Jennings Lodge excerpt, and reasonable open-web mirror routes were rechecked. No unrestricted Oregon City section surfaced. Remaining task is a restricted/physical lookup, targeting at least **501, 503, 503½, 505, 507, 509, and 511 Main** plus relevant proprietor/business names.

### MF-063 — Polk 1915–1916 Oregon/Washington gazetteer

FamilySearch parts/identifiers and physical holding routes are established, but no unrestricted online Oregon City pages were recovered. Remaining task is restricted/physical inspection of the Oregon City section and relevant business classifications/addresses.

The integration commit created during this conversation was:

- `24575421074ff097638aeef826d4259b99d0fc96` — `Convert three 1916 online gaps to manual callouts`

### MF-064 — 1916 Morning Enterprise

The *Morning Enterprise* continued beyond 1913, but the relevant public digitized Oregon City run ends in 1913; the longer run survives on microfilm. Therefore 1916 *Morning Enterprise* coverage is a manual/restricted-source issue, not unfinished ordinary public-online work.

### MF-065 — 1916 Clackamas County Tax List

The 1916 county tax-list volume is confirmed as a physical holding at the Museum of the Oregon Territory/appropriate archival route; no public 1916 image set was identified. This should be a year-closeout manual callout rather than an endless online search.

A second integration workflow was created to synchronize MF-064/MF-065 and the source-class checkpoint. Its workflow completed successfully, including baseline validation, integration, post-integration validation, commit, and push. Relevant setup commits include:

- `9713dc8a42bf4496af7ae14baeb92a3601214a0c` — `Classify 1916 Morning Enterprise tax and Sanborn source classes`
- `c5bf09bead5f84e19756a92a11c5614dd135b918` — integration script
- `5aac8ab27dbb823852acd4ce9f929ca1490d4877` — integration workflow

**Important:** on startup, inspect the newest commits to obtain the final integration commit SHA for MF-064/MF-065 rather than assuming the setup commit is the final research commit.

## Sanborn/map source class

The map class should not be represented as if a missing 1916 Sanborn edition exists. The available Oregon City Sanborn sequence brackets 1916 with **1911 and 1925**. No 1916 Sanborn edition was identified. Treat that as a reviewed source-class limitation, not an unresolved retrieval target.

The existing 1911 and 1925 maps remain important chronological controls, but neither should be projected into 1916 as if contemporaneous.

## Water/property source already reviewed

The **1916–1917 Water Rent Record Book 4** target Main Street run was previously visually reviewed and integrated. It establishes target-address/account evidence including 503, 503½, and 501 and the notable lack of a separate 505 Main water-account entry in the reviewed run. Preserve the repository's existing cautious interpretation: absence of a separate water account is not proof that 505 was vacant or unused.

## Highest-value remaining online block: municipal records

At the moment this handoff was requested, work had just begun on the final substantial public-online source class: **1916 Oregon City municipal records**.

A key new discovery in the current pass is that the City's historic-document structure exposes an **actual 1910–1919 City Commission archive/query route**, not merely a generic statement that old records exist. The search/index layer can see the decade link, but the underlying offsite **WebDrawer** content was not rendering cleanly through the search layer. The next conversation should continue from that exact point rather than restarting with generic web searches.

### Municipal audit targets

Systematically test the public City/WebDrawer routes for 1916:

- City Commission/Council minutes and proceedings.
- Ordinances and resolutions.
- Pool-room, billiard, cigar, soft-drink, saloon/liquor-related licensing or regulatory material relevant to the target block.
- Street-number/address matters.
- Building, repair, fire, demolition, construction, or occupancy matters.
- G. A. Harding and other already established target-block people/business names.
- Explicit references to 501, 503, 503½, 505, 505½, 507, 509, 511 Main; Fifth/Main; and the target Original Oregon City block/lots where appropriate.

Use newspaper-reported municipal actions only as discovery/cross-checks. Do not silently upgrade newspaper summaries into the underlying City record.

If the WebDrawer/public City route genuinely cannot expose the 1916 underlying records after a systematic documented pass, convert the specific municipal material into a numbered **YEAR-CLOSEOUT / MANUAL CALLOUT**, describing the exact record series, target dates/names/addresses, public-online routes attempted, and likely City/archival retrieval route.

## Other source-class reconciliation still needed

After the municipal audit, perform a concise reconciliation of the remaining classes required by `RESEARCH-STANDARD.md`:

- Historic-resource inventories/reports: identify what relevant 1916-facing material is already in the repo and whether any reasonable public-online target remains.
- Historic photographs: check whether a securely dated 1916 or tightly bracketed Fifth/Main image remains discoverable online; do not force a year attribution onto broadly dated photos.
- Property/assessment: water ledger is already reviewed; 1916 tax list is now manual. Confirm whether any other public-online parcel/assessment source remains genuinely outstanding.
- Maps: Sanborn class is already bounded as above.
- Directories/gazetteers: now manual callouts MF-062/MF-063 unless a genuinely new unrestricted source appears.
- Newspapers: ordinary online audit is complete except documented MF-061 retrieval gap; Morning Enterprise is MF-064.

The purpose of this reconciliation is to determine whether any **reasonable public-online work** remains, not to solve every historical question before ONLINE COMPLETE.

## Expected closeout logic

If the municipal audit and source-class reconciliation find no additional reasonable public-online sources, prepare a formal **1916 online-source-class closeout** modeled on the repository's 1917 ONLINE COMPLETE closeout.

The closeout should state at minimum:

- Status: **ONLINE COMPLETE** only if `RESEARCH-STANDARD.md` requirements are satisfied.
- Courier: **458/458 visually reviewed**.
- Enterprise: **425/426 visually certified**, with 12 May page 8 explicitly documented as MF-061 retrieval gap.
- Combined newspaper certification: **883/884**.
- All ordinary Enterprise issue dates through year-end reviewed.
- Other online source classes searched/reconciled and their results.
- Exact manual callouts, including MF-061 through MF-065 and any new municipal callout created by the final audit.
- Proven facts versus inferred/contextual findings.
- Retrieval gaps and unresolved conflicts.
- Explicit statement that absence/silence was not treated as proof of vacancy, non-operation, ownership, or tenancy.
- Exact resume/manual path for anything remaining.

Then update all required repo surfaces, especially:

- `registers/year-status.md`
- `evidence/source-captures/1916-online-audit-checkpoint.md`
- the new formal 1916 closeout capture
- `MANUAL-FOLLOWUP.md`
- source/evidence registers and YAML only where warranted by actual new source/evidence records
- leads/open questions where status changes require it

Run `validate_archive.py` before and after the final integration and publish only after validation passes.

## Do not do

- Do not call 1916 ONLINE COMPLETE solely because newspaper coverage is 883/884.
- Do not claim the missing May 12 page contains no target evidence.
- Do not treat inaccessible directory/gazetteer/tax/microfilm sources as searched negative evidence.
- Do not invent a 1916 Sanborn map.
- Do not project 1911 or 1925 map conditions into 1916 without explicit inference language.
- Do not send manual requests without Rodney's authorization.
- Do not redo already certified newspaper scans unless auditing a specific problem.

## Immediate resume point

**Resume the 1916 Oregon City municipal-record audit from the discovered 1910–1919 Commission archive/WebDrawer route.** Exhaust that public-online route systematically, document the results, then reconcile historic-resource/photo/property classes. If no reasonable online work remains, create the formal 1916 ONLINE COMPLETE closeout and validate/publish it.
