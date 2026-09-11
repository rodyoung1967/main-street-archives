# 2026-09-10 — CCHS photo-ingestion conversation handoff

Status: **conversation-state preservation / resume checkpoint**

Purpose: preserve all substantive knowledge from the conversation that focused on checking, identifying, validating, and ingesting project-steward-supplied Clackamas County Historical Society photographs relevant to the 503/505 Main Street project and its immediate Main/Fifth streetscape context.

Repository safety note: this handoff was prepared only after syncing/re-reading the current project rules on `main` and reviewing the then-current authoritative head `c80f7a6d8f78b235dc815f6f64f32319580ff0d4`. Parallel research had continued to advance `main`. Future work must always sync the newest `main` again before acting.

## Conversation purpose

The conversation's job was not to create a new historical narrative from photographs alone. It was to:

1. check whether each supplied image was already preserved;
2. avoid duplicate binaries/IDs when the same image was already present;
3. recover and verify the live CCHS/CatalogIt object record where possible;
4. preserve either the exact steward bytes or the current institutional high-resolution derivative, with the relationship stated accurately;
5. retain exact steward filename/hash/dimensions when the repository binary was not byte-identical;
6. record direct visual observations separately from catalog metadata and working spatial hypotheses;
7. connect useful images to source/evidence/media IDs without over-assigning 501/503/505 identities;
8. preserve dating/location uncertainty and create focused follow-up questions where warranted.

All substantive findings from the conversation are already integrated into canonical source/evidence/media records. This handoff is the continuity layer.

---

## 1. Two supplied 505 storefront photos were already preserved

### IMG-0724 — George Harding Drug Store

- Canonical file: `media/photos/early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg`
- Source/evidence: `S-148` / `E-133`
- CCHS object: `2008.008.046.080`
- Catalog context: George Harding Drug Store at 505 Main.
- Date boundary: structured CCHS date says **1880**; caption wording says **1880s**. Preserve that conflict.
- Exact steward-upload SHA-256: `532b58185f876a7651d578be9cb39f94a414d4daaa2169438cae1329ed99fe61`
- Result of this conversation's duplicate check: **exact byte match already in repository**.
- The crop shows Harding fascia but does not visibly show the number 505; the CCHS address may be retrospective because formal numbering is documented later. Do not use this image alone to prove present-building continuity.

### IMG-0725 — George Young's Second Hand Store

- Canonical file: `media/photos/early-main-street/IMG-0725_1910-505-main-george-young-second-hand-store.jpg`
- Source/evidence: `S-149` / `E-134`
- CCHS object: `MOT:P-391`
- Catalog date: **1910**
- Exact steward-upload SHA-256: `875329cbd74094a80fc49b4e470b5b70e2dda48dc66594508240facdf2c75c04`
- Result of this conversation's duplicate check: **exact byte match already in repository**.
- Direct visual value: the photograph visibly shows **505** over the doorway and **Young's Secondhand Store** on the windows.
- CCHS identifies George Young as the man in the white shirt without a coat.

No duplicate media IDs or binaries were created for either image.

---

## 2. IMG-0732 / S-203 / E-183 — CCHS P-1469 1890 flood scene

Canonical source capture:
`evidence/source-captures/1890-cchs-p1469-main-street-flood-photo-2026-09-03.md`

Canonical image:
`media/photos/early-main-street/IMG-0732_1890-main-street-flood-cchs-p1469.jpg`

Key facts:

- CCHS object: **P-1469**
- Catalog title: **1890 Flood - Oregon City Main Street**
- Catalog date: **1890**
- Catalog description/location: **Oregon City Main Street, 6th and Main, looking southwest**; unidentified people, flooding and debris.
- Current committed CCHS high-resolution derivative: **2400 × 1745**, **569359 bytes**
- SHA-256: `767915990ca00e17316f75ba2db51c5e0e2f36a2e36555020cf9caade4889e74`

Important recovery history:

- Earlier P-1469 staging chunks were incomplete and could not reconstruct a valid JPEG.
- Those corrupt/incomplete staged bytes were **not** committed.
- The authoritative CCHS CatalogIt object was recovered directly and its current public derivative was committed instead.
- The earlier steward-supplied upload is therefore **not claimed byte-identical** to the committed derivative.
- No exact 501/503/505 facade or physical-building continuity may be inferred from P-1469 alone.

Do not revive or merge experimental P-1469 staging branches/chunks into `main`; the canonical main-branch record supersedes them.

---

## 3. IMG-0733 / S-204 / E-184 — CCHS P-1456 1890 flood looking south

Canonical source capture:
`evidence/source-captures/1890-cchs-p1456-main-street-looking-south-photo-2026-09-03.md`

Canonical image:
`media/photos/early-main-street/IMG-0733_1890-flood-6th-main-looking-south-cchs-p1456.jpg`

CCHS metadata verified from the live record:

- Object: **P-1456**
- Title: **1890 Flood - Oregon City at 6th and Main Street Looking South**
- Date made: **1890**
- Description: Main Street looking south after water had receded, between alley and Sixth Street; unidentified people.
- Tag: **Duplicate**
- Medium note: **Photographic Paper**
- CCHS duplicate group: **P-1456 / P-1616 / P-5519 / P-8885**

Steward attachment:

- 2048 × 1543
- 903423 bytes
- SHA-256 `9c684f8f59ec7e78c894f1e77b70ca5094e976994a3644244b6a1ded6631e1cb`

Committed institutional derivative:

- 1200 × 904
- 779120 bytes
- SHA-256 `7355ba848b586427c139ddfe4229748a2b9c49439bc26b605874f184747c41a7`

Relationship: **same P-1456 scene / substantive duplicate, not byte-identical**.

Do not turn CCHS's duplicate-group statement into a claim that all four current derivatives are byte-identical; they are cataloged duplicates with different present encodings/sizes.

No exact 501/503/505 facade mapping is asserted from this image alone.

---

## 4. IMG-0734 / S-205 / E-185 — 1888 Main Street alley/barber photograph

Canonical source capture:
`evidence/source-captures/1888-cchs-2008-008-002-309-main-street-alley-barber-photo-2026-09-03.md`

Canonical image:
`media/photos/early-main-street/IMG-0734_1888-main-street-alley-4th-5th-barber-cchs-2008-008-002-309.jpg`

Follow-up: **RL-049 / OQ-035**

CCHS metadata:

- Object: **2008.008.002.309**
- Title: **Buildings on Main Street, Oregon City**
- Date made: **1888**
- Catalog description is line-broken as:
  - **Buildings on Main Street**
  - **Alley between 4th and 5th Streets on Main Street**
  - **Oregon City**
- Notes: **Medium: Negative; Location of Negative: Society Collection**
- Other No.: **Gardner 309**
- Other Photo #: **Trembath, Beauliau #3**

Steward attachment:

- Original filename: `Alley between 4th-5th Strrets on Main, O.C., 1888(1).jpg`
- 2048 × 1544
- 1165272 bytes
- SHA-256 `12939244c3db5d8ac39e7db93ad4a1a8409909ff9d3445c17b2bb4756ef26e0a`

Committed CCHS derivative:

- 2400 × 1810
- 1075501 bytes
- SHA-256 `c0c507e4367883208fa44d75137f021ea1fee0aceb08d4bc32093fc0b75077ce`
- Not byte-identical to the steward upload.

Direct visual observations:

- The right storefront visibly reads **HAIR CUTTING** and **SHAVING**. Calling that visible storefront a barber shop/use is direct evidence.
- A narrow passage is visible immediately left of the barber storefront.
- The bluff rises directly behind the buildings.

Interpretive limits:

- The compressed catalog wording is best treated as buildings **on Main Street at/near the alley opening between Fourth and Fifth**, not proof that the buildings themselves were "in" the alley.
- The visible passage is compatible with being that alley, but that is not yet documented fact.
- Bluff geometry makes an east-side Main frontage photographed from the west side plausible; this remains **PROBABLE / WORKING HYPOTHESIS**.
- Do **not** identify the barber as Trembath or Beauliau. The lower handwriting and catalog cross-number are insufficient to establish proprietor identity.
- Do not assign a modern numbered address yet.
- This block is between Fourth and Fifth, one block south of the project's main Fifth-to-Sixth 501/503/505 frontage if the CCHS location is correct.

Highest-value next test: visually compare against **SM-003**, October 1888 Sanborn sheet 2 (`maps/sanborn/originals/1888-02 (5th).pdf`) for mid-block alley geometry, side of Main, footprint widths/depths and possible use.

---

## 5. IMG-0735 / S-206 / E-186 — CCHS 2019.001.00179 Downtown Oregon City overview

Canonical source capture:
`evidence/source-captures/undated-cchs-2019-001-00179-downtown-overview-4th-6th-photo-2026-09-03.md`

Canonical image:
`media/photos/early-main-street/IMG-0735_undated-downtown-oregon-city-4th-6th-overview-cchs-2019-001-00179.jpg`

Follow-up: **RL-050 / OQ-036**

CCHS metadata:

- Object: **2019.001.00179**
- Title: **Downtown Oregon City**
- Description: **Downtown Oregon City**
- Live CCHS record supplies **no exposure date**.

Steward filename context:

- Original steward filename includes **"focusing on 4th-6th streets (aerial view)"**.
- Preserve that phrase as **project-steward-supplied descriptive context**, not as CCHS catalog wording.
- The image is an elevated oblique overview. It may have been taken from high ground/bluff; an aircraft camera platform is not established.

File identity:

- 1401 × 1109
- 243009 bytes
- SHA-256 `d6e7b691b880d3c8bbb6dcbb58500d7b3e15e13d688834fda5fa68c8b949774f`
- The committed current CCHS derivative is an **exact byte-for-byte match** to the steward attachment.

Do not infer a 2019 exposure date from the object-number prefix.

Next work under RL-050/OQ-036: determine exposure date, camera position/direction and exact Fourth–Sixth block/building identities by fixed-landmark, Sanborn, street-geometry, river/falls and dated-photo comparison before assigning 501/503/505.

---

## 6. IMG-0736 / S-207 / E-187 — Post Office demolition at Fifth and Main

Canonical source capture:
`evidence/source-captures/undated-cchs-u1426-005098a-post-office-demolition-5th-main-photo-2026-09-03.md`

Canonical image:
`media/photos/early-main-street/IMG-0736_undated-post-office-demolition-5th-main-cchs-u1426-005098a.jpg`

CCHS metadata:

- Object: **U-1426.005098a**
- Title: **Demolition of the Post Office at 5th and Main, Oregon City - constructed in 1933.**
- Description: **Demolition of the Post Office, Oregon City, constructed in 1933**
- CCHS does not supply the demolition/photo exposure date.

File identity:

- 981 × 776
- 145571 bytes
- SHA-256 `75e60d9c374094d6729cc4204505f91f1311f85190690f7f6c5a446e956edaf2`
- **Exact byte match** between steward upload and current CCHS public high-resolution derivative.

Dating/spatial boundary:

- **1933 is the Post Office construction year**, not the demolition-photo date.
- Existing Sanborn evidence independently places the 1933 U.S. Post Office at the **southeast corner of Fifth and Main**.
- It is on the **same east side of Main as 501/503/505**, but **across Fifth Street from 501**, on the Fourth-to-Fifth block.
- It is not part of the 501/503/505 block.

Useful future task: independently date the demolition event/exposure if that becomes relevant.

---

## 7. IMG-0737 / S-208 / E-188 — CCHS P-9379 Oregon City aerial

Canonical source capture:
`evidence/source-captures/undated-cchs-p9379-aerial-oregon-city-photo-2026-09-03.md`

Canonical image:
`media/photos/aerials/IMG-0737_undated-oregon-city-aerial-cchs-p9379.jpg`

CCHS metadata:

- Object: **P-9379**
- Accession: **2022.012.001**
- Title: **Aerial Photograph Oregon City**
- Description: **Aerial Photograph Oregon City**
- Media label: **Aerial view of Oregon City**
- Live public record supplies **no exposure date**.
- The accession number is **not** treated as a photograph date.

Steward attachment:

- 2048 × 1676
- 1200394 bytes
- SHA-256 `2154e29eec46892888f04f9faeb1a09eb7f69b93fe2d0c338a6968af43b50e10`

Committed CCHS derivative:

- 2400 × 1965
- 1068263 bytes
- SHA-256 `410b8493e52365bc5968d983f82a015cfc4ec9ded2b89976799c019396d622bd`

Relationship: same P-9379 scene, **substantive duplicate, not byte-identical**.

Direct visual content includes a broad downtown Oregon City aerial, Willamette River, Oregon City–West Linn bridge, log rafts/booms and surrounding development.

### US 99 dating constraint added by the project steward

The project steward explicitly observed that this photograph was taken **after US 99 had changed its route through Fifth Street in Oregon City**.

Repository treatment:

- preserve this as a **terminus post quem / relative dating constraint**;
- keep the exact exposure date **unknown**;
- do not invent a calendar year from the observation alone;
- the repository has not yet independently established the documentary date when US 99 began using the visible Fifth Street alignment.

Highest-value dating follow-up: establish the US 99 routing-change date from ODOT/Oregon State Highway Commission maps/records, Oregon City street records, dated highway maps/aerials, or contemporary newspapers. Once independently established, that date becomes a defensible earliest-possible date for P-9379.

Do not assign an exact 501/503/505 building identity from this broad aerial without a separate spatial comparison.

---

## 8. Temporary branches and failed staging work are not authoritative

This conversation used several temporary staging branches/workflows while recovering institutional derivatives and validating archive writes. Some may remain visible in GitHub.

Rules for the next session:

- **Treat current `main` as authoritative.**
- Do not merge a temp branch merely because it contains a photo-ingest name.
- In particular, the old P-1469 chunk staging was incomplete/corrupt and was intentionally superseded by the live CCHS recovery.
- P-9379 had an initial validator failure because the Markdown evidence register lacked the literal `Claims:` and `Confidence:` headings; the record was corrected, revalidated, and the clean commit was fast-forwarded to `main`.
- Experimental helper workflows/scripts on temp branches are implementation history, not evidence.
- Later parallel work has already added additional media IDs beyond IMG-0737; do not assume IMG-0737 is the latest global image ID.

---

## 9. Open questions / useful continuation work

### Highest-value photo-specific work

1. **RL-049 / OQ-035 — 1888 alley/barber scene**
   - Compare IMG-0734 directly to SM-003.
   - Resolve exact alley opening, side of Main, footprint match and historical street numbers.
   - Search 1888-era barber/business directories only after the map geometry narrows the premises.
   - Research what CCHS cross-reference **"Trembath, Beauliau #3"** means; do not assume it names the barber.

2. **RL-050 / OQ-036 — Downtown Oregon City overview**
   - Date IMG-0735.
   - Resolve camera location/direction.
   - Identify Fourth–Sixth street structures with dated maps/photos.
   - Preserve the distinction between an elevated oblique view and a proven aircraft aerial.

3. **P-9379 dating**
   - Independently date the US 99 route change through Fifth Street.
   - Use that only as a lower-bound date unless another source supplies the exposure date.

4. **Post Office demolition**
   - If historically useful, establish the demolition date for U-1426.005098a.
   - Keep 1933 as construction year only.

5. **1890 flood photographs**
   - P-1469 and P-1456 provide strong fixed-location context around Sixth/Main.
   - They may help map predecessor frontage, but any 501/503/505 identification must come from documented geometry/cross-source comparison, not visual resemblance alone.

### No outreach performed

No institutional email/request, paid order, fee authorization, or manual-record request was sent during this photo-ingestion conversation.

---

## 10. Canonical files to read first when resuming

Always sync newest `main` first, then read completely:

1. `AGENTS.md`
2. `RESEARCH-STANDARD.md`
3. `MANUAL-FOLLOWUP.md`
4. this handoff:
   `evidence/source-captures/2026-09-10-cchs-photo-ingestion-conversation-handoff.md`
5. `media/photo-metadata-register.md`
6. `media/photos/inventory.md`
7. `evidence/evidence-register.md`
8. `evidence/source-register.md`
9. `indexes/id-crosswalk.md`
10. `registers/research-log.md`

For photo-specific detail, read the six source captures listed above for IMG-0732 through IMG-0737.

---

## 11. Resume prompt for a new conversation

> Continue the 503/505 Main Street, Oregon City historical research project from the current GitHub repository `rodyoung1967/main-street-archives`, branch `main`. Treat the repository as authoritative. First sync the newest main and read `AGENTS.md`, `RESEARCH-STANDARD.md`, `MANUAL-FOLLOWUP.md`, and `evidence/source-captures/2026-09-10-cchs-photo-ingestion-conversation-handoff.md` completely. Do not reset, revert, force-push, renumber IDs, or overwrite newer parallel work. The photo-ingestion conversation verified existing IMG-0724/IMG-0725 exact duplicates and integrated IMG-0732 through IMG-0737 with CCHS provenance. Preserve all evidence-state limits in the handoff. For P-9379, exposure date remains unknown but the project steward states it postdates US 99's routing through Fifth Street; treat that only as a relative dating constraint until the reroute date is independently documented. For IMG-0734 and IMG-0735, continue RL-049/OQ-035 and RL-050/OQ-036 rather than assigning unsupported addresses or dates.

