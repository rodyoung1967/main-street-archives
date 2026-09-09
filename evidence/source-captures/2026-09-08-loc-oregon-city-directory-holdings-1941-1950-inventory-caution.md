# Library of Congress Oregon City directory holdings metadata — 1941/1950 inventory caution

Date reviewed: **8 September 2026**

Status: **CURRENT LOC INVENTORY / DATASET COVERAGE CONTROL; METADATA ONLY; NON-COMPREHENSIVE BY LOC'S OWN WARNING; NO 505 OCCUPANCY CLAIM.**

Purpose: harvest the completed temporary Library of Congress directory-data probe on `main` and distinguish three separate propositions that must not be collapsed:

1. what the Library of Congress's **published/current directory inventory metadata explicitly lists** for Oregon City;
2. what LOC may actually hold outside or beyond that inventory; and
3. what the separate Gale/Research Publications **Reel 26** publisher index implies about a 1953 Oregon City directory.

This capture does **not** identify an occupant, proprietor, business owner, liquor licensee, tenant, telephone subscriber, sale party, or transfer event at 505 Main.

## Probe provenance

The temporary workflow committed as:

- `a8fc3617ef6db1d3a450f122d18e0653cbdc3c7d` — **Add temporary LOC Oregon directory holdings probe**

successfully downloaded the Library of Congress directory data packages but its logged summary did not unpack and row-search the full ZIP. The completed GitHub Actions artifact was therefore harvested directly rather than rerunning or deleting the workflow.

Harvested artifact:

- GitHub Actions artifact: `probe-loc-oregon-city-directory-data`
- artifact ID at harvest: `10084426603`
- downloaded outer ZIP SHA-256: `8d764463c12d49aa4d8b679f1bcde99d4cb72dd714979b5b3c9b7c23555bf7e9`

Relevant embedded LOC package:

- workflow artifact member: `candidate-010`
- size: `11,357,795` bytes
- SHA-256: `3cf3b5b994def2c042cef62ad981b0b371ecaf5888fa992d090c38f76aadcb83`
- package content: `directories/by-region/...`

Relevant Oregon metadata file inside that package:

- `directories/by-region/Oregon/metadata.csv`
- size in package: `510,345` bytes
- SHA-256: `18c6f56d0ebebbd589d3c429df88e27d20ae962bf24f58d9ce4e0b0d47c9d94d`
- parsed rows: `876`

The artifact itself is temporary workflow output; the durable result, exact hashes, extraction scope, and interpretation are preserved here.

## LOC dataset identity and explicit caution

The package README identifies the dataset as:

**Library of Congress holdings of United States Telephone Directories, City Directories, and Criss-cross Directories (Metadata only)**

README version:

- **Version 1.1**
- last updated **2023-07-26**

The README explains that the dataset is derived from Library Guide inventory tables and breaks locality/date ranges into one row per locality/year. Critically, LOC warns that the inventories were commonly compiled from directory **spine text**, which may omit localities represented inside a volume, and that inventories were **not created for all states held by the Library**. LOC expressly says the dataset **should not be interpreted as a comprehensive list of all directories held by the Library**.

Dataset route:

`https://data.labs.loc.gov/directories/`

Current city-directory guide:

`https://guides.loc.gov/united-states-city-telephone-directories/city-directories`

Classification consequence: a missing year in this metadata is an **inventory/description gap**, not proof that LOC does not hold that directory and not proof that the directory did not exist.

## Exact Oregon City rows recovered

Filtering the full Oregon metadata file to locality exactly **`Oregon City`** produced **two rows**:

### 1941 row

- `State_region`: Oregon
- `Locality`: Oregon City
- `Date`: **1941**
- `Source_collection`: City Directories of the United States
- `Location_text`: Oregon City
- `Date_text`: **1941, 1950**
- `Original_format`: Microfilm
- `Notes`: From library guide index entry: Oregon, Oregon City
- `Repository`: Library of Congress General Collections
- `Directory_type`: City Directory
- `Digitized`: blank
- `Url`: blank
- `Shelf_id`: blank

### 1950 row

The second row has the same collection/locality metadata and:

- `Date`: **1950**
- `Date_text`: **1941, 1950**

No exact Oregon City row with `Date = 1953` is present in the harvested Oregon metadata file.

## What this establishes

The strongest defensible LOC-specific statement is now:

> The Library of Congress's published/current directory inventory metadata explicitly lists **Oregon City city-directory coverage for 1941 and 1950**, and does **not explicitly list 1953** in the Oregon City rows recovered from the full state metadata file.

This supersedes the earlier temporary working state in which the Oregon LOC data file had been identified but not successfully row-inspected.

It does **not** establish:

- that LOC lacks any 1953 Oregon City directory;
- that the 1953 Salisbury volume is absent from all LOC microfilm holdings;
- that no larger reel or volume contains Oregon City despite incomplete spine-level description;
- that the Gale/Research Publications Reel 26 inference is false;
- anything about the occupant or operator of 505 Main.

## Relationship to Gale / Research Publications Reel 26

The separate Gale/Cengage publisher author index for **City Directories of the United States** assigns **Oregon City to Reel 26** and prints an internally inconsistent Oregon City entry:

- range label: `1941-1950`;
- missing-year list continues through **1959**;
- that missing-year list names 1942–1952 except **1953**, then 1954–1959;
- reel: **26**.

The Gale page was subsequently visually inspected in this continuation after the earlier cache-miss limitation. The entry itself is visible on the publisher PDF page carrying the Oregon City listing.

This remains a **strong catalog inference** that 1953 is represented on Gale/Research Publications Oregon City Reel 26, but the reel or original 1953 volume has not been visually inspected. The LOC state inventory and Gale publisher index are therefore **different metadata controls** and should not be forced into artificial agreement.

Correct interpretation:

- **LOC current inventory:** explicitly lists 1941 and 1950 for Oregon City; 1953 is not explicitly inventoried in the harvested state rows; inventory is non-comprehensive by LOC's own warning.
- **Gale publisher Reel 26 index:** internally inconsistent range text, but missing-year pattern supports 1953 as a strong reel-content inference.
- **Actual 1953 Salisbury directory:** independently established as a real source by Oregon City preservation bibliography and other official citations; actual 505 page remains unrecovered.

## Research-route correction

Future handoffs and source notes should **not** say simply that “Library of Congress microfilm” is a verified holder of the 1953 Salisbury volume.

Use more precise language:

> **Library of Congress collection/access route:** LOC holds the broader `City Directories of the United States` microfilm collection, but its current published Oregon City inventory explicitly lists only 1941 and 1950. Because LOC says the inventory is non-comprehensive, 1953 cannot be ruled out. Gale/Research Publications Reel 26 remains a separate strong catalog inference requiring direct reel inspection.

This preserves the potentially useful LOC route without overstating a specific 1953 holding.

## Relationship to the 505 Main question

This result does not change the documentary chronology:

- late 1948 — Carl R. Harr / Harr's Recreation Center / 505 Main directly named in municipal text;
- 1950 — billiards / cigars / beer use mapped at 505, operator unnamed;
- 1953 — visually verified SHPO survey says the city directory lists **“Well's Recreation”** at 505, underlying Salisbury page/proprietor unresolved;
- 20 Nov. 1955 — unnamed established beer/pool business at 505 offered for sale, contact **9179** visually verified;
- later successor chain remains unresolved.

The immediate value is source triage: it prevents treating LOC's public inventory as if it already proved possession of the target 1953 volume, while preserving direct Reel 26 inspection as a potentially decisive route.

## Next source work

1. Recover or directly inspect the actual **_Oregon City & Vicinity Directory, 1953_ — T. W. Salisbury & Co.** through a verified image/reel/institutional route.
2. If Gale/Research Publications **Reel 26** becomes inspectable, establish its actual reel contents visually before calling 1953 present on the reel.
3. If LOC is used later, verify the exact physical reel/title sequence rather than relying solely on the published inventory rows.
4. Continue the independent high-value route for a **1953–1956 Oregon City telephone directory** identifying subscriber **9179**.
5. Do not send an institutional request without project-steward authorization.

## Cross-record propagation decision

This is a **source-access / holdings-control correction**, not a new historical entity fact. It warrants correction of directory-retrieval language but does **not** warrant a new occupant/proprietor/person/business relationship, 505 timeline event, building fact, source/evidence claim ID, or YAML relationship.