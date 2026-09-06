# 1917 Oregon City Enterprise — April 6, 13, 20 and 27 visual review

<!-- 1917 Enterprise April visual review and page-8 gap — 2026-09-06 -->

Status: **VISUALLY VERIFIED — 31 genuine intended-date pages; 6/20/27 April are complete 8/8, 13 April is 7/8 with true printed page 8 a RETRIEVAL GAP. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `S-279`; evidence `E-252`; person `P-396`; business `BUS-103`; manual callout `MF-051`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-april/`  
Original retrieval commit: `9c50293b82e519382e76e8b7d1def95cf8eaf248`  
Manifest: `newspapers/oregon-city-enterprise/1917-april/manifest.json`  
Recovery audit: `newspapers/oregon-city-enterprise/1917-april/recovery-april13-page8/recovery-manifest.json`  
Recovery commit: `1cc5060d2d5b198f6f8a27930ffff702abfd8347`

## Scope and page-identity audit

All **32 archive-supplied April slots** were rendered and visually inspected. Because the March pass exposed a source-association defect, the April pass separately checked printed mastheads and page numbers instead of trusting archive sequence metadata.

| Archive issue bucket | Exposed slots | Genuine matching issue pages | Status |
| --- | ---: | ---: | --- |
| 6 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 13 April 1917 | 8 | 7 | **PARTIAL 7/8 — true printed Page 8 RETRIEVAL GAP** |
| 20 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 27 April 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |

The archive object exposed as **13 April sequence 8 / Page 8** is not a printed Page 8. Enlarged visual inspection shows **PAGE 6** at upper left. Its masthead prints **THURSDAY, APRIL [obscured], 1917**, with the date numeral physically obscured/marked and a handwritten `13` above the date area. The normal sequence 6 is already a separate Friday 13 April printed Page 6. Sequence 8 is therefore preserved as a **second Page-6/source variant**, not silently counted as Page 8.

The dedicated recovery audit tested Oregon PDF/JP2/OCR/XML/RDF/HTML derivatives, ed-1 sequences 9–12, editions 2–4, neighboring-issue source objects, Chronicling America/LOC routes, and LOC JSON discovery. No hidden replacement sequence or alternate edition exposed the true printed Page 8. All Oregon derivatives of seq-8 resolve to the same printed Page-6 variant. The true **13 April 1917 printed Page 8** is retained as **RETRIEVAL GAP / manual callout `MF-051`**, not as negative evidence.

With 105 genuine intended-date Enterprise pages through March, April adds **31**, making **136 genuine intended-date pages visually verified through April**. The archive has supplied **138 January-April slots**, two of which are source-association substitutions/gaps (16 Mar p5 and 13 Apr p8). **278 later May-December exposed slots remain unreviewed.**

## Direct April findings

### W. S. Eddy / Fashion Stable relative-location change

Repeated professional advertisements in the visually reviewed April issues identify **W. S. Eddy, V.S., M.D.V.** and say he is established at the **Fashion Stable, between Fourth and Fifth on Main Street**. The wording is directly visible on 6 April p.7 and recurs in the later April p.7 advertisements.

This materially changes the existing Fashion Stable chronology. The archive's visually verified 1915 Enterprise evidence (`E-112` / `S-124`, continued under `E-114` / `S-128`) places **W. S. Eddy at the Fashion Stable on Fifth Street between Main and Water Streets**. The exact initials, veterinary credentials and Fashion Stable name make the 1915 and 1917 observations a strong same-person/same-business bridge, while the different relative location means the archive must allow a **move, changed stable premises, or changed advertisement-location wording sometime after the 1915 observation and by April 1917**. No exact move date or street number is inferred.

This is **not** a bridge to **W. B. Eddy's Store (`BUS-100`) at 427 Main**. W. B. and W. S. remain separate printed identities. The April relative wording also does not prove that Fashion Stable was 427 Main, 110 Fifth, or any other numbered premises.

Because W. S. Eddy / Fashion Stable now has a multi-date chronology and a location-change problem requiring explanation, this integration promotes stable person `P-396` and business `BUS-103` records.

### Fifth/Main parade and Strebig context

**13 April p.1** directly reports that the preparedness parade started from **Fifth and Main streets at 7:30 p.m.** and that **Henry Strebig headed the line of march carrying a large American flag**. This is useful civic/person/intersection context only. It does not place Strebig's meat market at the target numbered storefronts on that date and does not alter the separate 427 Main former-Strebig-business evidence.

### Annie L. Farr and Farr Brothers identity controls

**20 April p.3** directly prints a real-estate transfer: **Annie L. Farr to W. P. Morris and Viola Morris, lot 6, block 92, Oregon City; $1.** This is a dated Oregon City Farr identity/property context. It does not identify Annie with Alice Farr, Edwin F. Farr, or the later 505 Main pool hall. The February source separately printed **Annis L. Farr**; spelling similarity is retained as an identity question, not normalized into one person.

**20 April p.8** directly includes **Farr Bros.** in county-poor expenditures. That reinforces the already separated Farr Brothers supplier/business context but supplies no 505 Main address and no bridge to Edwin/Alice Farr. Numeric strings such as dollar amounts that resemble target street numbers are rejected as address evidence.

## Exact target-address result

Across the **31 genuine intended-date April pages recovered and visually reviewed**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact **427 Main** occupant was established.

The unrecovered true 13 April Page 8 is excluded from that bounded no-hit statement. Nothing in the April silence or page gap proves vacancy, demolition, non-use, or absence of a target storefront.

## Cross-record propagation audit

Reviewed against this batch: `buildings/503-main.md`, `buildings/505-main.md`, `timelines/503-main.md`, `timelines/505-main.md`, `buildings/427-main.md`, `businesses/w-b-eddys-store-1917.md`, the Farr person/business records, `people/people-index.md`, `businesses/business-index.md`, `database/people.yml`, `database/businesses.yml`, `timeline.md`, `registers/address-register.md`, `registers/business-timeline.md`, `evidence/open-questions.md`, `evidence/research-leads.md`, and `indexes/id-crosswalk.md`.

**Propagation decision:**
- Promote W. S. Eddy / Fashion Stable to stable person/business records because the evidence is now multi-date and location-conflict-heavy.
- Update the master/address/business chronology and the 427/W. B. Eddy no-merge guard.
- Update open questions/leads with the new Fashion Stable location-change problem and April Page-8 retrieval gap.
- Do **not** add a 1917 503/505 occupant/building event: the batch establishes none.
- Do **not** create a numbered Fashion Stable building: both 1915 and 1917 evidence are relative-location statements.
- Do **not** merge Annie/Annis L. Farr, Farr Brothers, Edwin F. Farr, Alice Farr, W. S. Eddy, W. B. Eddy, or the earlier A. J. Eddy wording without independent bridges.

## Effect on 1917 status

1917 remains **IN PROGRESS**. Enterprise now has **136 genuine intended-date pages visually verified through April**, two known Enterprise page-level retrieval gaps (16 March p5 and 13 April p8), and **278 May-December exposed slots** still requiring page-by-page visual review. Existing Courier and directory/source-class blockers remain separately active.
