# Building, Business, People, and Timeline Reconciliation — 29 August 2026

Status: repository-wide entity/navigation audit completed against the current evidence, source captures, registers, YAML sidecars, and master timeline. This is an archive-structure reconciliation, not an annual `ONLINE COMPLETE` certification and not new negative evidence.

## Audit method

1. Compared every existing building, business, and person YAML/index record to the standalone pages visible in `buildings/`, `businesses/`, and `people/`.
2. Searched source captures, evidence, registers, maps, and the timeline for central named entities that had never received stable IDs.
3. Added pages when an entity had a multi-date chronology, a central relationship to 503/505 or the Fifth/Main cluster, or an identity/address conflict requiring explanation.
4. Retained one-date or peripheral entities in the canonical indexes/YAML when a standalone page would merely duplicate one bounded row.
5. Reconciled `ARCHIVE_INDEX.md`, the address/business timelines, the ID crosswalk, and `database/timeline.yml`.

## Building/address corrections

The archive previously had six building records. It now has fourteen.

Added:

- `B-007` — 107 Fifth / Blacksmith (1914–1915 ledger).
- `B-008` — 108 Fifth / Scripture & May and later S. F. Scripture.
- `B-009` — 109 Fifth / Oregon City Laundry.
- `B-010` — 110 Fifth / Stable (probable Scripture & May tenant reading only).
- `B-011` — 519 Main / Theroux, later Pantorium and temporary laundry office.
- `B-012` — 526 Main / Eddy's Dependable Store.
- `B-013` — 617 Main / Beaver Building address record.
- `B-014` — 619 Main / Andresen Building address record.

No `102 Fifth`, `104 Fifth`, or `106 Fifth` building record was invented. The annual searches name those as desired reconstruction targets, but the current repository does not contain a direct exact-address occupant/use observation sufficient to establish an entity page. Unnumbered Fashion Stable, May & Washburn, Fifth Street Restaurant, and other relative-location premises likewise remain unassigned until an exact number is proved.

## Business corrections

The canonical business list now contains 77 stable records. Central businesses promoted from source captures include:

- G. H. Young / The Curio Man (`BUS-067`);
- Oregon City Laundry (`BUS-068`);
- May & Washburn (`BUS-069`);
- Fifth Street Restaurant (`BUS-070`);
- Gilbert Miller shoe repair (`BUS-071`);
- H. Ketchner home/confectionery (`BUS-072`);
- Pantorium (`BUS-073`);
- Red Front Clothing Store (`BUS-074`);
- Alex Schieremann tailor shop (`BUS-075`);
- Timms Pool Hall (`BUS-076`);
- Leland & Little Billiards (`BUS-077`).

Standalone pages were also added for already-indexed White Rabbit / Black Ink, Dug Inn, and Thirsty Duck.

The former `ARCHIVE_INDEX.md` business list was stale and incorrectly relabeled `BUS-018` through `BUS-023`. The corrected mapping is: White Rabbit / Black Ink (`BUS-018`), H. H. Smith pool hall (`BUS-019`), L. Hylton (`BUS-020`), Dr. Freeze (`BUS-021`), Dr. Roy Briggs (`BUS-022`), and Dixon's Bakery (`BUS-023`). G. H. Young now has `BUS-067`; no existing ID was renumbered.

## People corrections

The canonical people index now contains 93 stable records. New profiles/records cover the G. H. Young chronology; separate Blakeslee laundry operators; Knoepel and Schofield; S. F. Scripture, L. E. May, and Washburn; Schieremann, Ketchner, Blake, and the Gage/Blake conflict; Leland, Little, and Timms; contractor R. A. Junken; and Pantorium owner F. Champion.

Central existing records for Ray Hansen, Dick Wiitanen, Sheila Wiitanen, Rodney Young, Alin Guria, Henry Brightbill, and Joe Wilson now also have standalone profiles.

Group/business styles remain person records where the original source does not identify individuals. No people were merged by surname or initials alone.

## Timeline corrections

The master timeline was restored to chronological order by moving the appended 1915–1916 review blocks into their proper positions. Added chronology includes:

- 107/110 Fifth water-ledger anchors;
- the February–April 1916 Oregon City Laundry site change;
- 108 Fifth and 617/619 Main 1916–1917 address chains;
- the 24 October 1918 108/109 Fifth and 500/505 Main business snapshot;
- the 1920–June 1922 Fifth Street business cluster;
- the distinct Timms versus Leland & Little chronology;
- the full named July 1922 fire cluster and Gage/Blake conflict;
- post-fire laundry, Miller, and May & Washburn recovery;
- the 1925 rebuilt/re-established laundry presence;
- 1957–1960 503 restaurant/Wheel anchors;
- the 1988 Dug Inn/former Brass Rail transfer.

`database/timeline.yml` now contains 39 stable timeline records. Narrative chronology remains richer than the YAML summaries, but central events and ID relationships are synchronized.

## Page-coverage rule

The canonical indexes are complete entity lists. Standalone pages are an explanatory layer, not a second competing index. A missing standalone page does not mean a person/business is absent from the archive. New pages should be added when evidence becomes multi-date, project-central, or conflict-heavy; one-mention entities may remain index-only until then.

## Validation

Run `python3 scripts/validate_archive.py` after every later entity-page change. Any new stable ID must be synchronized across its Markdown index, YAML record, related building/business/person records, timeline when applicable, and `indexes/id-crosswalk.md`.
