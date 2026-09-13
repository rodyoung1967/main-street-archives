# 1922 conversation handoff — 13 September 2026

## Purpose

Preserve the material knowledge, corrections, constraints, and resume point from the 13 September 2026 conversation in which the project steward said to **finish 1922** and then asked to **save all knowledge for this conversation to the repository**.

This handoff is intentionally conservative. It records what was actually established in the conversation and does not upgrade unverified leads into historical claims.

## Governing repository state

At the time this handoff was prepared, current `main` had advanced through commit `997b45be9e706a70de8a99f287f81883381f8472` (`Preserve Enterprise December 15 22 and 29 1916 scans`). Parallel annual work was active, so future 1922 work must again fetch/sync current `main` before modifying anything.

The current versions of `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` were re-read before this save. Their controlling rules remain in force: original scans are required for visual verification; OCR/search text is discovery only; uncertainty and retrieval gaps must be preserved; cross-record propagation must be audited; and no institutional/manual request may be sent without project-steward authorization.

## 1922 annual status — correction preserved

**1922 remains IN PROGRESS.**

The conversation explicitly corrected an earlier temptation to treat 1922 as nearly complete. No annual certification should be asserted until the full `RESEARCH-STANDARD.md` requirements are met, including:

1. complete title/issue/page inventory for every relevant online newspaper title;
2. page-by-page visual review of every online-retrievable page;
3. documented recovery attempts for missing or non-rendering pages;
4. review of the other relevant online source classes;
5. integration of verified findings, conflicts, OCR-only leads, and retrieval gaps;
6. a numbered manual-work callout list for everything that cannot be finished online.

A search or inaccessible page is only a coverage statement and is never evidence of vacancy, demolition, closure, relocation, or non-use.

## Newspaper / ODNP access work attempted in this conversation

The conversation tested 1922 Oregon Digital Newspaper Program routes for the Oregon City papers, including title/issue URLs for the Banner-Courier and Oregon City / Morning Enterprise family of titles.

A direct retrieval test against an ODNP 1922 page PDF failed in the execution environment because the local container could not resolve `oregonnews.uoregon.edu`. Web-search/open attempts were also insufficient to support a complete page-by-page annual certification during this conversation.

Therefore:

- this conversation did **not** certify a complete 1922 issue/page inventory;
- this conversation did **not** perform a complete page-by-page visual review of 1922 newspapers;
- the ODNP access limitation must be treated as a workflow/access constraint, not as evidence that pages do not exist;
- the next 1922 session should resume with a current issue inventory and visually inspect original page images wherever the archive renders them.

A practical review method considered in the conversation was to obtain the page scans, assemble manageable contact-sheet / page bundles, and visually inspect every page rather than relying on OCR or snippets.

## 1922 photograph / structural evidence discussed

The conversation worked with the project-steward-supplied image `IMG_5749.jpeg`, a zoom/crop associated with the 1922 Fifth/Main bridge photograph context (`CCHS P-9594`) and focused on the 501/503/505 Main storefront/building area.

Local technical facts recorded during the session for the supplied file:

- source attachment filename: `IMG_5749.jpeg`
- image dimensions observed locally: `706 × 1536` pixels
- file size observed locally: `183,943` bytes
- SHA-256 observed locally: `53a4ca00eabab2cebe14b36e1a54fe575c38ed6aabdda9e50eda16e51053b23f`

A compact derivative was also created locally during the session under the working name `IMG-0772_1922-p9594-501-503-505-zoom-steward-screenshot.jpg` for easier inspection. That working derivative had dimensions `320 × 696`, size `18,256` bytes, and SHA-256 `0ab6b037fb06b550d49699027a4d15751e2d2e76dd1c8b807f917758c81f4ae5`.

### Preservation status

The connected GitHub write interface available in this conversation can create/update UTF-8 text files but does not provide a binary repository-file upload action. A direct local `git clone` route also failed because the container could not resolve `github.com`. For that technical reason, this conversation could not safely preserve the supplied JPEG itself into `media/` through the available write path.

**Do not treat the image as intentionally omitted.** Under `AGENTS.md`, the project-steward-supplied image should be committed when a binary-capable repository path is available. Until then, this handoff preserves the attachment identity, dimensions, hashes, provenance context, and the technical reason the binary was not added.

### Evidence caution

The zoom image is useful as photographic/structural evidence, but the conversation did not establish a new source-proven exact construction date merely from the crop. It should be interpreted alongside the full P-9594 photograph, the documented 1922 fire/rebuild evidence, deeds/tax records, and the 1925 Sanborn rather than used alone to collapse the building-continuity question.

## Existing 1922 documentary endpoints that remain controlling

The conversation carried forward the established 1922 workstream rather than replacing it. The important existing project endpoints remain:

- the Fifth/Main fire workstream identifying the tailor/cleaning-and-dyeing premises and the adjoining pool-hall context;
- A. Leland at 505½ Main in the 1920 pool-hall chain;
- Leland & Little / Timms pool-hall evidence during 1922;
- the distinction between pool-hall operation, tenancy, business ownership, property ownership, and building identity;
- the open Harding → Wolf / Gates property and parcel-division questions;
- the need to use the 1925 Sanborn and later photographs as structural controls without assuming same-address = same-building continuity.

No contrary evidence was established in this conversation that supersedes those endpoints.

## Manual 1922 routes still open

The current manual dashboard continues to identify high-value 1922 routes, including at minimum:

- `MF-006` — June–August 1922 Harding → Wolf/Gates deeds;
- `MF-007` — OHS MSS 1503, Series B, Box 19 title abstract;
- `MF-013` — 1922 poolroom applications/minutes;
- `MF-019` — 1920–1925 assessment rolls / ownership books / parcel controls;
- `MF-041` — underlying 2 June 1920 Council minutes and pool-room application/bond/license material relevant to A. Leland / 505½ Main.

These remain manual work unless a genuinely online copy is recovered. **No request was authorized or sent in this conversation.**

## Recommended resume point for finishing 1922

1. Fetch/sync newest `main` and reread the governing files.
2. Inspect the latest 1922 source captures, registers, year-status entry, and relevant commits so no parallel work is repeated or overwritten.
3. Build/confirm a complete 1922 online newspaper title → issue date → page-count inventory.
4. Visually inspect every retrievable page of every relevant 1922 issue; reuse only prior reviews that are explicitly documented as VISUALLY VERIFIED.
5. Record each page as VISUALLY VERIFIED, OCR/TEXT ONLY, RETRIEVAL GAP, PENDING, or MANUAL CALLOUT as required by `RESEARCH-STANDARD.md`.
6. Make reasonable online recovery attempts for every missing/misassociated/non-rendering page.
7. Review the non-newspaper online source classes relevant to the 1922 fire, rebuilding, pool-hall occupancy, property ownership, parcel geometry, and address/building continuity.
8. Integrate any verified changes across timeline, buildings, businesses, people, source/evidence registers, open questions, research leads, crosswalk, and YAML/database records.
9. Run the archive validator after writes.
10. Only then decide whether 1922 qualifies for **ONLINE COMPLETE**. If it does, create the required formal year closeout with numbered manual callouts. If not, leave it **IN PROGRESS** and state precisely what remains.

## Cross-record propagation decision for this handoff

This conversation primarily produced a corrected **research-status / workflow record**, plus preservation metadata for a steward-supplied 1922 photo crop. It did not establish a new verified occupant, business owner, property owner, liquor licensee, or exact building-construction event. Accordingly, this save does **not** manufacture timeline or entity-fact entries from the access failures or from the crop alone.

The supplied image itself still requires binary preservation under `media/` and registration in `media/photo-metadata-register.md` when a binary-capable write route is available.
