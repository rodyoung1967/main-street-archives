# Municipal minutes: working catalog route and bounded scan review

Date: **1 September 2026**. Related: `RL-010`, `RL-018`, `S-155`, `S-156`.

Status: **IN PROGRESS**. This is an access/inventory checkpoint, not a completed 1924–1927 municipal review or a new identification of the May 1925 occupants at 503/505 Main.

## What changed

The old 1920s WebDrawer query again returned 404. The new public Laserfiche portal initially exposed only a loading shell to the web reader, and its welcome-page search stalled. However, **interactive folder browsing and Advanced Name search worked**. Do not describe the entire municipal collection as unavailable on the strength of the old link failure.

Starting points: [City Meeting Document Archive](https://www.orcity.org/1844/Meeting-Document-Archive), [Public Records Self-Service Portal](https://www.orcity.org/596/Public-Records-Self-Service-Portal), and [Laserfiche welcome page](https://portal.laserfiche.com/Portal/Welcome.aspx?repo=r-5a2dbf36).

### Reproduce the successful catalog search

1. In Laserfiche choose **Browse → City Recorder → Public Meeting Records → City Commission**.
2. The City Commission folder showed **7,619 entries**, legacy container **OCCF/15/11**, legacy URI **OR_3741323**, and title **Agenda Packets and Minutes**. Observed folder IDs were City Recorder `859`, Public Meeting Records `400786`, and City Commission `2012`.
3. Choose **Advanced**. Under **Customize Search**, add **Name** and remove the default **General Search** criterion.
4. Enter **`1925*City Commission*`** in **Enter the name to search for**, then **Submit**. The result list required a short load before populating.
5. Read all five result pages: **81 named entries / 159 listed scan pages**. The last page contains the 6 January entry. Opening a result created a new tab.

The [saved 81-row inventory](1925-city-commission-minute-inventory-2026-09-01.json) preserves every title, page count, legacy record number, legacy URI and review status. These are **catalog counts, not pages visually reviewed**. Adjacent meeting entries may share ledger pages; 159 is not a deduplicated physical-page count, nor proof that every meeting survives. The 1924, 1926 and 1927 runs have not been inventoried.

### Viewer/export limitation

The **1925-01-06 City Commission Minutes** entry opened (current document ID `386870`; legacy `OCRD/16/2839`, `OR_4794934`, one page). Its rendered OCR layer was readable and included printed ledger page 50, December 1924 meeting material, and the January 6 meeting about municipal buildings and finance. The actual scan was not successfully visually inspected: the page-fit screenshot was blank. This entry is **OCR/TEXT ONLY**, not VISUALLY VERIFIED.

After the visible download icon was clicked, the next browser operation was rejected by the browser's URL security policy. **The export route was stopped; no workaround was attempted and no January PDF was obtained.** This is a current tool-specific export/retrieval limitation, not proof that the public cannot obtain the record. The other 80 entries remain **PENDING**. No 1925 page counts toward visual coverage yet. The search result's session-specific URL was not saved as a durable citation.

## Six May 1927 pages actually retrieved and visually inspected

Independently of the Laserfiche export attempt, the City's [Municipal Elevator history page](https://www.orcity.org/1235/Municipal-Elevator) links two public DocumentCenter PDFs. Both original PDFs were retained under `records/municipal/commission-minutes/` and all six pages visually inspected (`S-155`).

| City source | Retained file | Printed ledger pages | Scope |
|---|---|---|---|
| [11 May 1927 minutes / Ordinance 1152](https://www.orcity.org/DocumentCenter/View/9617/1927-05-11-City-Commission-Minutes-Ordinance-No-1152pdf) | [1927-05-11-pages-322-325.pdf](../../records/municipal/commission-minutes/1927-05-11-pages-322-325.pdf) | 322–325 | May 11 meeting and beginning of May 16; **not complete May 16 coverage**. |
| [23 May 1927 minutes / second reading](https://www.orcity.org/DocumentCenter/View/9615/1927-05-23-City-Commission-Minutes-Ordinance-No-1152-second-readingpdf) | [1927-05-23-pages-328-329.pdf](../../records/municipal/commission-minutes/1927-05-23-pages-328-329.pdf) | 328–329 | Tail of May 18 and May 23 meeting; **not complete May 18 coverage**. |

Original source URL filenames are preserved in the links above; repository filenames are normalized. Provenance: City of Oregon City public DocumentCenter copies, downloaded 1 September 2026. No new reuse-rights determination is asserted.

SHA-256:

- May 11 PDF: `89f9e6614e89277687ecc729a4af93dd81fa93181d00a2b046437f5e8797ddaf`.
- May 23 PDF: `76def5cf677c7448878b9b2e5ac3acc841471ed7e4f96fdbb0999220ce7cd9c9`.

### Verified scope and exclusions

- **pp. 322–323:** Ordinance 1152 concerns an Elevator Street boundary/deed involving Block 34 and the Sarah A. Chase heirs. It is not a 503/505 Main property record. Other business includes sewer District 21 / Falls Vista Addition.
- **pp. 323–325:** a Water Street improvement resolution includes the segment from the **south line of Fifth Street to the north line of Sixth Street**. Plans were filed May 3 and the resolution passed May 11. The offsets described are measured from Water Street's east line; they do **not** establish Fifth Street's overall width or its alleged narrowing. This is a neighboring public-works context item, not a new numbered Fifth Street building or business.
- **p. 325:** the May 11 meeting ends and a May 16 meeting begins; its continuation is outside this PDF.
- **p. 328:** the opening material is the end of a May 18 street-improvement resolution whose street name lies on a preceding page not included here. Do not label it Main Street merely because Fourth and Fourteenth are mentioned. May 23 begins lower on the page.
- **p. 329:** May 23 business includes final passage of Ordinance 1152, sewer assessment Ordinance 1153, charter-ballot business and deferral of Ordinance 1151.
- Commissioner **Farr** appears in these minutes. This official's surname is **not** an identification of Edwin F. Farr or the operator of Farr's Pool Hall at 505. No new person/business relationship is made from it.
- No 503/505 occupant, target pool-hall license, or target construction event was identified in these **six pages only**. This does not establish absence elsewhere in the minutes.

## Resume targets and authorization boundary

1. **First historical target:** the underlying **2 June 1920** Council/Commission action for A. Leland at **505½ Main**, reported in the already visually verified June 4 newspaper (`E-135` / `S-150`). The new folder path is a promising catalog route, but this particular minute has **not** been located or reviewed in this pass. Check operator name, precise premises, sign permission, owner and building-work language; do not merge Leland identities.
2. **1925 target:** obtain readable copies through an authorized access route, then review the inventory in manageable batches. Start with January's six entries (**9 listed pages**), checking annual licenses, pool/billiards/cigars, restaurants, transfers, signs and all Main/Fifth address references. January 6 must still be visually checked. Preserve any numbered Fifth address with its exact wording and uncertainty.
3. Inventory 1924 and 1926–1927, then search/visually inspect license and building-work material. Text searching may prioritize pages but cannot replace scan review. Names to test include Farr, Leland, Little, Kwality/Quality, Jager, Timms, Holman and Pace; distinguish commissioners from business operators.
4. If a user-supplied download or institutional assistance is needed, request direction before expanding scope. No inquiry, records-request submission, payment, or restricted-account access has been performed. Do not retry the blocked export via an alternate technical route.

No evidence ID or building/business/person/timeline claim is added by this access pass. `S-155` records the retained bounded source set; `S-156` records the catalog inventory and explicit text-only limit. The May 1925 **503 restaurant** and **505 billiards/cigars** remain unnamed. Farr's at 505 remains undated; Kwality's reported 1926 presence remains unbridged to May 1925. Annual research statuses are unchanged; absence of a hit was not treated as absence of a business or event.
