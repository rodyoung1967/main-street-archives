# 505 Main SHPO resource-ID and scanned-document retrieval route

Date reviewed: 5 September 2026

Status: **OFFICIAL SHPO MACHINE-READABLE RETRIEVAL ROUTE + PUBLIC SITE-SUMMARY CONTROL; EXACT 505 `RESOURCE_ID` NOT RECOVERED IN THIS PASS; RETRIEVAL GAP. NO FARR→HARR DATE CHANGED.**

Purpose: refine the already-established cumulative historic-inventory route for **505 Main Street** into a reproducible record-ID workflow. This pass does not repeat the completed 2021 ODOT / 2009-form work and does not promote a new 1945 Harr source or transition date.

Related controlling capture:

`evidence/source-captures/505-main-cumulative-inventory-and-2009-rls-online-retrieval-pass-2026-09-05.md`

That file already establishes that `S-116 / E-100` preserves the 19 January 2009 Oregon Historic Site Form for 505 Main and that the missing target is the **older cumulative survey/research lineage**, especially the 1983-era form, the individual 2000 form, prior-record identifiers, attachments, and source notes behind the legacy 1941 / 1945 / 1953 business chronology.

## 1. Official SHPO GIS layer exposes the record-key field

Oregon SHPO's current public GIS service exposes the statewide historic-sites feature layer directly through ArcGIS REST:

`https://maps.prd.state.or.us/arcgis/rest/services/Cultural/HistSites_GIS_FeaturesOnly/FeatureServer/0`

The live layer is named **Historic_Sites**, supports `Query`, and advertises JSON / geoJSON output. Its public field schema includes:

- `RESOURCE_ID` — alias `resource_ID`;
- `resource_ID_1` — integer copy of the resource ID;
- `propName`;
- `address`;
- `city`;
- `county`;
- `yrBuilt`;
- `elig`;
- `ilsDate`;
- `rlsDate`;
- `nrStat`;
- `HistDist`;
- `SHPO_REVIEWED`;
- source/confidence and edit metadata.

This is an **official access-route finding**, not historical occupancy evidence. It shows that the exact SHPO property identifier can in principle be recovered from the statewide layer by querying the Oregon City / 505 Main record rather than relying only on general web indexing.

## 2. The `RESOURCE_ID` is the pivot into the public Historic Sites Database record

Current indexed Oregon Historic Sites Database property pages use URLs of the form:

`https://heritagedata.prd.state.or.us/historic/index.cfm?do=v.dsp_siteSummary&resultDisplay=<RESOURCE_ID>`

An Oregon City Main Street control is the live record for **707–709 Main Street / Oregon City Masonic Lodge**, which uses `resultDisplay=30553`.

That public site-summary page exposes fields directly useful for the 505 provenance problem:

- **Scanned Document Links**, including an **Inventory Form**;
- address / current and historic names;
- survey/grouping associations;
- ILS/RLS survey dates;
- comments/notes;
- **RESEARCH INFORMATION** source-class flags;
- bibliography / source citations.

The 707–709 control specifically records both the 2000/2009 Oregon City survey context and cites a **Michelle L. Dennis historic-resource survey form** in its bibliography. This demonstrates that a recovered 505 resource ID could lead to more than a GIS point: the site-summary layer can expose scanned forms and detailed research-source metadata when those materials have been linked.

Do **not** transfer the Masonic Lodge's bibliography or record facts to 505 Main. It is a retrieval-structure control only.

## 3. SHPO confirms that online records may be incomplete

Oregon SHPO's current **Survey Historic Places** guidance describes the Oregon Statewide Inventory as the collection of physical and historical information received for built properties and directs researchers to the online Historic Sites Database.

Crucially, SHPO also instructs researchers to **contact SHPO to see whether additional information is available beyond what is found in the online database**.

Therefore even a successful 505 site-summary retrieval would not close the cumulative-file question if older forms, consultant worksheets, project databases, or supporting research are not linked publicly.

## 4. Survey guidance explains the database lineage

SHPO's 2011 historic-resource survey guidelines state that survey data are recorded in the Oregon Historic Sites Database and that professional surveyors worked from a **project database extracted from the master OHSD**. The returned project package could include the database plus maps/photos, and the guidelines allowed supplementary research materials and historic photographs to be returned to SHPO with the project.

Research consequence: for the 1983 / 2000 / 2009 505 lineage, a request should not be limited to a single PDF form. It should ask for:

- the current SHPO resource ID and any prior/linked record IDs;
- scanned-document links attached to that resource;
- all older inventory-form versions;
- the 2000 project record/form and source notes;
- any retained project-database export or record metadata that links the 2009 form backward;
- worksheets, supplementary research, photographs, correspondence, and consultant material when retained.

This is consistent with Oregon City's current statement that historic inventory forms are cumulative.

## 5. Exact online query attempted in this pass

The live ArcGIS layer's **Query** operation was opened successfully. The intended narrow query is conceptually:

- `city = 'Oregon City'`;
- address = `505 Main St` (with reasonable address-format variants if needed);
- return at minimum `RESOURCE_ID`, `resource_ID_1`, `propName`, `address`, `city`, `yrBuilt`, `elig`, `ilsDate`, `rlsDate`, and `nrStat`;
- no geometry required.

The current research interface can inspect the query form but cannot submit arbitrary populated ArcGIS query parameters. A direct parameterized URL is blocked by the browsing safety layer. The exact 505 `RESOURCE_ID` therefore remains **UNRECOVERED IN THIS PASS / INTERFACE RETRIEVAL GAP**.

This is not evidence that no 505 SHPO record exists. The repository already has the 2009 505 form (`S-116 / E-100`), and the previously completed 2021 ODOT review establishes the 505 SHPO-database record trail.

## 6. Recommended human / institutional workflow

Before or alongside `MF-047` outreach:

1. Search the public Oregon Historic Sites Database or ArcGIS historic-sites layer for **505 Main Street, Oregon City** and record the exact `RESOURCE_ID` / `resource_ID_1`.
2. Open the corresponding public site-summary page using `resultDisplay=<RESOURCE_ID>`.
3. Preserve every **Scanned Document Link**, especially older inventory forms.
4. Capture the site's survey/grouping associations, ILS/RLS dates, comments, bibliography, and research-information fields.
5. Follow any prior-record / associated-address identifiers rather than assuming one record contains the full cumulative history.
6. Use the recovered resource ID in the City/SHPO request for the **complete cumulative 505 Main file**, including material not linked online.
7. Specifically ask for the source behind **Dr. Roy Briggs — 1941**, **Harr's Recreation Center — 1945**, and **Well's Recreation — 1953**, including exact directory title/year/page if retained in the source notes.

The updated request draft is:

`registers/research-requests/505-1983-historic-inventory-owner-field-request-2026-09-05.md`

## 7. Farr→Harr evidence boundary

Nothing in the GIS schema, database-control record, or SHPO survey guidance identifies Farr or Harr at 505 Main on a new date.

The controlling chronology therefore remains unchanged:

- City historic-resource **directory synthesis** reports Harr's Recreation Center at 505 Main in **1945**, with exact underlying directory title/effective year/page unresolved;
- 11 February 1948 Commission text directly identifies Harr as a pool-hall operator but does not print the address;
- the later-1948 municipal liquor-license list directly identifies **Carl R. Harr — Harr's Recreation Center — 505 Main Street**;
- the exact Farr → Harr transition date remains unresolved.

Classification of this pass: **OFFICIAL DIGITAL ACCESS / PROVENANCE ROUTE + RETRIEVAL GAP**, not a new historical occupancy finding.
