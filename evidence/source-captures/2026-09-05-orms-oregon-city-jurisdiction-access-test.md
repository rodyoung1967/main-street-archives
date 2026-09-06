# Oregon City ORMS jurisdiction/search-interface access test — 5 September 2026

Status: **CURRENT PUBLIC-RECORDS INTERFACE TEST / RETRIEVAL LIMITATION. NOT HISTORICAL OCCUPANCY EVIDENCE. NO FARR→HARR DATE CHANGED.**

Purpose: test whether the current Oregon Records Management Solution (ORMS) public search interface can still expose the missing Oregon City Commission minute chunks immediately before municipal pages **318** (1946) and **474** (1948), rather than repeatedly relying on web-search indexing or assuming that the legacy WebDrawer decade navigation remains functional.

Related controlling capture:

`evidence/source-captures/1946-1948-commission-minute-predecessor-retrieval-route-2026-09-04.md`

That capture already fixes the missing municipal targets as approximately **pp.314–317** before the 6 March 1946 material and **pp.470–473** before the 11 February 1948 material. This test addresses only the present public retrieval mechanism.

## 1. Current ORMS search form is live, but Oregon City is no longer a selectable jurisdiction

On 5 September 2026 the live ORMS search form at:

`https://ormswd.synergydcs.com/ORMSCMSearch/search/SearchMain.aspx`

was retrieved successfully through an independent GitHub Actions network runner. The form is an ASP.NET POST search form and its live jurisdiction selector contained these choices:

- Beaverton, City of (`005`)
- Department of Consumer and Business Services, Oregon (`009`)
- Department of Education (`025`)
- Douglas County (`019`)
- Forest Grove, City of (`036`)
- Hillsboro, City of (`008`)
- Milwaukie, City of (`003`)
- Springfield School District (`047`)
- St Helens, City of (`016`)
- Tillamook County (`077`)
- Tualatin Hills Parks/Rec (`001`)
- West Linn, City of (`007`)

**Oregon City is not present in the current jurisdiction dropdown.**

This is a direct statement about the current public search interface, not about whether Oregon City's historical records still exist. Known individual Oregon City legacy WebDrawer records remain retrievable by their direct record URLs.

The current form exposes these search-field types:

- Any Word
- Date Created
- Document Content
- Record Number
- Title (Free Text Part)
- Title Word

It also includes an archived-record checkbox. The interface observed in this test did **not** expose a selectable Oregon City jurisdiction or a Meeting Date search type.

## 2. All-jurisdiction archived-content fallback was tested and timed out

Because Oregon City was absent from the jurisdiction selector, the test attempted an all-jurisdiction archived-content POST while preserving the ASP.NET form state and cookies. The first narrow query used three document-content clauses:

- `Oregon City`
- `liquor`
- `1945`

The server did not return a result set within a 20-second read window and the request timed out.

This must be classified as **INTERFACE / SERVER RETRIEVAL FAILURE**, not as a zero-result search. No inference may be made that the missing 1945–46 liquor-license material lacks Harr, Farr, 505 Main, or any other applicant.

The timeout also makes an unscoped all-jurisdiction content search a poor practical substitute for the missing Oregon City jurisdiction filter.

## 3. Legacy Oregon City WebDrawer record-list query now returns 404

Oregon City's previously published 1940s Meeting Document Archive route used the legacy HPRM WebDrawer query with Oregon City archive code **`023`**, including the pattern:

`webdrawercode:"*023*"`

A second runner test queried the legacy HPRM `Record` endpoint directly with that Oregon City code and year-scoped City Commission title filters for **1945, 1946, 1947, and 1948**.

All four year-scoped record-list requests returned **HTTP 404 Not Found**.

This is distinct from the individual-record behavior. Direct known record/file URLs such as the already-established Oregon City Commission records remain separately retrievable when the exact record ID is known. The failure is therefore best understood as a **record-list/navigation retrieval failure under the current public system**, not evidence that the underlying minute records were destroyed or removed.

## 4. Research consequence for the Farr → Harr problem

This test materially changes the **retrieval strategy**, but not the historical chronology.

The current public ORMS routes have now been tested at three levels:

1. **new ORMS search interface:** live, but Oregon City absent from the jurisdiction selector;
2. **all-jurisdiction archived-content fallback:** technically postable, but the first narrow Oregon City/liquor/1945 query timed out before returning a result set;
3. **legacy Oregon City code-023 HPRM record-list route:** year-scoped 1945–48 requests return 404.

Meanwhile, exact known individual legacy WebDrawer record IDs continue to be useful. That means targeted web/index discovery of an already-known record can still succeed, but the public navigation/search layer is no longer a dependable way to enumerate the missing chronological chunks.

Accordingly, the page-specific City Recorder / Laserfiche request already prepared in the controlling capture is now the correct next route for:

- municipal pages immediately preceding **p.318**, provisionally **pp.314–317 plus enough earlier material to include the complete preceding meeting**; and
- municipal pages immediately preceding **p.474**, provisionally **pp.470–473 plus enough earlier material to include the complete preceding meeting(s)**.

Do not repeat broad WebDrawer keyword searches as if this current interface limitation were an untested lead. Re-test only if Oregon City reappears in ORMS/Laserfiche public navigation, a new direct record ID is discovered, or City staff provide a replacement archive route.

## 5. Evidence boundary

Nothing in this access test identifies Farr, Harr, McDougald, 505 Main, or a liquor-license applicant on a new historical date.

The controlling chronology remains:

- City historic-resource directory synthesis reports **Harr's Recreation Center at 505 Main in 1945**, exact underlying directory title/effective year/page unresolved;
- **11 February 1948** Commission text directly names Harr and McDougald as pool-hall operators without printing Harr's address in that line;
- late-1948 municipal text directly identifies **Carl R. Harr — Harr's Recreation Center — 505 Main Street**;
- exact Farr's Pool Hall → Harr's Recreation Center transition date remains unresolved.

Classification: **CURRENT OFFICIAL-DATA ACCESS / RETRIEVAL ROUTE TEST + RETRIEVAL GAP**.