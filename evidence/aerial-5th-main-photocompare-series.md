# Aerial Photocompare Series — 5th & Main Street

Working analysis of the Oregon City photocompare aerial screenshot series (`S-023`), cataloged as `E-021` with media IDs `IMG-0006` through `IMG-0043`.

## Source and Scope

- **Source:** Oregon City historical aerial photocompare tool — [maps.orcity.org/galleries/photocompare](https://maps.orcity.org/galleries/photocompare/index.html) (`S-023`)
- **View center:** 5th Street and Main Street, Oregon City
- **Coverage:** One screenshot per available year, 1929–2025 (38 images)
- **Repository files:** `media/photos/aerials/` — see `media/photos/aerials/README.md`
- **Related buildings:** `B-001` (503 Main), `B-002` (505 Main), `B-003` (507 Main / Harding Building)
- **Related prior evidence:** `E-020` / Sanborn comparison — especially the 1925 `501` label at the **5th & Main** corner

## Method and Limits

These are **screenshots** from a city-hosted comparison viewer, not original survey negatives. Labels such as "McLoughlin Blvd" and "US99E" appear on some frames and help orientation, but:

- Early black-and-white frames have limited resolution; roofline reading improves with close comparison across adjacent years.
- **501 Main** on the 1925 Sanborn is at the **5th & Main** corner, not the 6th & Main corner. Aerial interpretation must use that corner, not a different intersection.
- This series supports **footprint, removal timing, and corridor-change observations**; it does **not** by itself prove business names, ownership, or the legal cause of demolition.

## Revision Note (2026-07-05)

An initial integration pass incorrectly stated that 501 Main could not be isolated in early B&W frames and that no removal year was visible. **Corrected per project steward review:** the **1936** frame shows three distinct roofs at **501, 503, and 505 Main**; by **1944** the **501 Main** footprint is gone, and the east-side building **across from 500 Main** (as shown on Sanborn sheets) is also no longer present. Prior wording is superseded below; it is not deleted from git history.

## McLoughlin Boulevard / US99E

| Period | Observation | Confidence |
| --- | --- | --- |
| 1929 (`IMG-0006`) | McLoughlin Blvd / US99E labeling visible west of Main; Main Street commercial frontage still reads as a continuous row between 5th and the river/highway side. | Moderate |
| 1936 (`IMG-0007`) | Highway corridor west of Main appears wider and more graded than 1929; three distinct roof structures visible at 501, 503, and 505 Main on the west-side Main frontage. | Moderate to high (501/503/505 roof separation) |
| 1940–1980 (`IMG-0008`–`IMG-0014`) | Main Street structures between 5th and McLoughlin remain visible north of the former 501 corner; highway and remaining buildings coexist. | Moderate |
| 1996 Flood (`IMG-0015`) | High water visible near riverfront / McLoughlin corridor. | Moderate |
| 2005 Leaf Off (`IMG-0022`) | Leaf-off frame improves roofline reading for the remaining block. | Moderate |
| 2012–2025 (`IMG-0029`–`IMG-0043`) | Color aerials show current commercial block including 503/505/507 context; replacement Harding Building footprint at 507 readable in later decades. | Moderate to high for current footprint |

**Working conclusion:** McLoughlin / US99E is an established labeled corridor by **1929**, with a visibly wider graded corridor by **1936**. The **501 Main removal window (1936–1940)** overlaps the period of visible highway-corridor change and should be tested against ODOT / county highway and acquisition records (`OQ-023`).

## 501 Main — Existence and Removal (Primary Aerial Finding)

Cross-reference: `E-020` and `maps/sanborn-comparison-503-505-507.md` place **501** at the **5th & Main** corner on the 1925 Sanborn sheet.

| Question | Aerial finding | Status |
| --- | --- | --- |
| Did 501 exist as a separate structure in the aerial era? | **Yes.** `IMG-0007` (1936) shows **three distinct roofs** at **501, 503, and 505 Main** on the west-side Main frontage. | **Supported** — moderate to high |
| When was 501 removed? | **Between 1936 and 1940.** Present in 1936 (`IMG-0007`); absent in the 1940 frame (`IMG-0008`), with 1944 (`IMG-0009`) as later confirmation. | **Partially answered** — narrower removal interval established; exact date/cause unresolved |
| East-side counterpart | By **1944**, the building **across from 500 Main** (east side of Main, as labelled on Sanborn sheets) is **also no longer present**. | **Supported** — moderate |
| Cause of removal | Timing overlaps McLoughlin / US99E corridor change, but aerials alone do not prove highway acquisition, fire, or voluntary demolition. | **Unresolved** — needs deeds, permits, highway project records |
| Business / ownership | Not readable from aerials. | **Unresolved** (`OQ-005` remainder) |

**Working conclusion:** The aerial series adds **positive evidence** that **501 Main existed as a separable building through at least 1936** and was **removed by the 1940 aerial**, narrowing the removal interval to **1936–1940**. The related east-side footprint across from **500 Main** is also gone by 1944. This **partially answers** `OQ-005` (existence + removal timing) while leaving business history, ownership, and removal **cause** open.

## 503 / 505 / 507 Block Observations

- **503 & 505:** Remain part of the Main frontage north from the former 501 corner. A focused **5 September 2026** re-review of the canonical local `S-023` frames now identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which 505 can be distinguished as extending farther rearward/westward than 503**. The 1936 frame does not securely show the later asymmetry, but that ambiguity is not negative evidence. The deeper state remains visible in later frames and is independently confirmed by 1975 CCHS `P-1293` (`E-203`). Exact construction date/scope remains open under `OQ-003` / `RL-005`; see `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.
- **507 / Harding Building:** Distinct roof mass visible in 1936; post-fire replacement footprint consistent with late-1960s fire narrative (`E-016`, `E-017`) in later color years — exact fire-year confirmation still needs newspapers / fire records.
- **Circa 2017 modification:** Time Capsule Maps metadata (`E-015`) reports significant 503 modification around 2017; 2017+ color aerials (`IMG-0035` onward) may support future permit/photo comparison but are not transcribed here frame-by-frame.

## Year Index

Full file list: `media/photos/aerials/README.md`

| Media ID | Year | Notes |
| --- | --- | --- |
| `IMG-0006` | 1929 | Earliest series frame; US99E / McLoughlin labeled |
| `IMG-0007` | 1936 | **Three distinct roofs: 501, 503, 505 Main** |
| `IMG-0008` | 1940 | **501 absent; first reviewed frame with distinguishable deeper 505 rear footprint relative to 503** |
| `IMG-0009` | 1944 | **501 Main absent**; east-side building across from 500 Main also absent |
| `IMG-0010` | 1955 | Mid-century built block without 501 corner structure |
| `IMG-0011` | 1961 | Pre-/around Harding fire era — 507 mass visible |
| `IMG-0012` | 1974 | Post-replacement 507 context likely |
| `IMG-0013` | 1977 | — |
| `IMG-0014` | 1980 | — |
| `IMG-0015` | 1996 (Flood) | Riverfront / McLoughlin flood water |
| `IMG-0016`–`IMG-0021` | 1999–2004 | — |
| `IMG-0022` | 2005 (Leaf Off) | Better roofline season |
| `IMG-0023`–`IMG-0028` | 2006–2011 | — |
| `IMG-0029` | 2012 | — |
| `IMG-0030` | 2012 (Leaf Off) | — |
| `IMG-0031`–`IMG-0043` | 2013–2025 | Color era; current block footprint |

## Follow-Up Research

- Pin the exact 501 removal date within the **1936–1940** aerial bracket using demolition/highway/property records; no intermediate aerial is presently established.
- Oregon Department of Transportation / county records for US99E / McLoughlin widening and acquisition dates near 5th & Main (**1936–1944 window**).
- Clackamas County assessor footprint sketches and demolition permits for **501 Main** and the east-side **500 Main** counterpart.
- Newspaper notices for highway construction impacts on Main Street addresses.
- Identify Sanborn-labelled occupant and owner records for 501 before removal.

## Independent 1975 CCHS P-1293 cross-check

CCHS `P-1293` (`S-229` / `E-203` / `IMG-0750`) is independent of the city photocompare screenshots and supplies a useful later-state control. In the established 5th/Main mapping, **505 extends farther rearward than 503** and the former **501** corner structure remains absent. The 501 observation now corroborates the **1936–1940** removal bracket established by the focused re-review. The 505 observation remains an independent later-state control; the earliest reviewed photocompare frame in which the 505-vs-503 depth asymmetry can be distinguished is now **1940**. The photograph itself does not date the change or prove a circa-1940 addition.
