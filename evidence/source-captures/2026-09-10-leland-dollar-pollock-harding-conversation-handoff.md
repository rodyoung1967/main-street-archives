# 505 Main early-use and 1919–1920 conversation handoff

Handoff date: **10 September 2026** (America/Los_Angeles).

Repository: `rodyoung1967/main-street-archives`  
Authoritative branch: `main`

Status: **CONVERSATION KNOWLEDGE PRESERVATION / NO NEW HISTORICAL EVIDENCE IDs.** The source scans, photographs, historical claims, and uncertainty limits discussed in this conversation were already integrated in the canonical records identified below. This handoff reconciles them, records the supplied-page duplicate checks, and prevents the superseded OCR-only description of the A. Leland page from recurring.

## Mandatory startup for the next conversation

1. Fetch/sync and inspect the newest `main`; parallel research workflows continue to advance it.
2. Do not reset, revert, force-push, delete, or overwrite newer work.
3. Read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely.
4. Read this handoff together with:
   - `evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md`;
   - `evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md`;
   - `evidence/source-captures/1880-1910-505-main-harding-young-photo-records.md`;
   - `evidence/source-captures/2026-09-08-1919-1920-construction-occupancy-handoff.md`.
5. Treat the repository records below as controlling. Do not repeat the earlier conversation statement that the A. Leland page was OCR-only.
6. Run `python3 scripts/validate_archive.py` before and after any meaningful future repository changes.

Latest observed `main` before this preservation commit: `c7e04345eadfb24dab2d4626317ba3f83490b79e` (`Add temporary 1912 Courier gap retrieval workflow`). This SHA is only a synchronization marker and may already be obsolete.

## 1. A. Leland at 505½ Main — VISUALLY VERIFIED

Controlling records: `S-150` / `E-135`; 505 building and unified timeline records.

The actual scanned page was visually inspected:

- Source: *Oregon City Enterprise*, **4 June 1920**, p. 3.
- Reported event: the Wednesday evening City Council meeting, corresponding to **2 June 1920**.
- Printed wording: **“The application of A. Leland to operate a pool hall at 505½ Main street and to erect an electric street sign was granted.”**
- Evidence state: **VISUALLY VERIFIED / DIRECT PRIMARY NEWSPAPER REPORT**, with Very High confidence for the printed name, address, proposed use, sign, and reported grant.
- Canonical repository PDF: `newspapers/oregon-city-enterprise/1920-06-04-page-3.pdf`.

Rodney supplied `A. Leland to operate pool hall at 505 and a half jun 1920.pdf`. Its SHA-256 was checked as `3b419bb26e96d77aaf5be8dcb7f0954c7755ab9be890788fad119ca79702c245`, byte-identical to the canonical repository PDF. Therefore no duplicate binary or new evidence/source ID was required.

This proves an exact 505½ Main pool-hall/use and electric-sign approval. It does **not** prove:

- that the surviving 505 building was constructed in 1920;
- property or building ownership;
- the physical arrangement of 505 and 505½;
- that A. Leland and O. H. Leland were the same person;
- that A. Leland succeeded Clem Dollar or used the same pool hall.

Any earlier OCR-only description of this page is **superseded**. OCR discovery artifacts may retain their workflow labels, but the historical claim itself is visually verified.

## 2. Clem Dollar pool hall — VISUALLY VERIFIED, BLOCK-LOCATED ONLY

Controlling records: `S-150` / `E-135`.

- Source: *Oregon City Enterprise*, **13 February 1920**, p. 5.
- Headline: **“POOL HALL PROPRIETOR AND BOYS PAY FINES.”**
- The article identifies **Clem Dollar** as proprietor of a pool hall on Main between Fifth and Sixth streets.
- It reports that Dollar was fined **$20** for permitting minors in the resort; **Homer Selby** and **Raymond Hermann**, who were playing pool, were fined **$10 each**.
- Evidence state: **VISUALLY VERIFIED / DIRECT PRIMARY NEWSPAPER REPORT** for the printed person, role, block location, and fines.
- Canonical repository PDF: `newspapers/oregon-city-enterprise/1920-02-13-page-5.pdf`.

Rodney supplied `Clem Dollar proprietor of pool hall between 5th & 6th on main st feb 1920.pdf`. Its SHA-256 was checked as `dfd5be8e1fad8ad1c7dca8516590bb67d1a3d7c3f41cc5e4c1a1cb69a04eb004`, byte-identical to the canonical repository PDF. No duplicate binary or new evidence/source ID was required.

The article prints no numbered address. Do not equate this pool hall with A. Leland's later 505½ premises or with the separate December 1920 block-level pool-hall reference without an independent bridge.

## 3. Fifth Street Restaurant and W. W. Pollock — VISUALLY VERIFIED

Controlling records: `S-181` / `E-161`; `P-101`; `BUS-070`. Earlier 1916 association: `S-184` / `E-164`.

- Source: *Oregon City Enterprise*, **31 October 1919**, p. 5.
- Headline: **“RESTAURANT MAN FINED.”**
- The article directly describes **W. W. Pollock** as “conducting the Fifth street restaurant.”
- It reports a fine of **$15 and costs** in Justice Stipp's court, on the complaint of **W. B. Duncan**, an inspector of the state dairy and food department, charging Pollock with keeping a dirty and unsanitary place.
- Evidence state: **VISUALLY VERIFIED / DIRECT PRIMARY NEWSPAPER EVIDENCE**.
- Canonical repository PDF: `newspapers/oregon-city-enterprise/1919-10-31-page-5-fifth-street-restaurant-fine.pdf`.

The wording supports treating Pollock as the reported operator/conductor of the Fifth Street Restaurant at that time. It does not, by itself, prove real-estate ownership. The article gives no numbered address, so it does **not directly prove 501 Main**. The water-ledger/business-cluster evidence makes 501 a relevant location hypothesis/control, but the exact address connection remains unresolved unless a source explicitly bridges it.

A separate visually verified 1 September 1916 inspection record directly associates **Fifth Street restaurant — W. W. Pollock — 75.3**. It supports an earlier person/business association, not uninterrupted operation through 1919.

## 4. Harding Drug Store photograph and the early 505 site

Controlling early record: `S-148` / `E-133` / `IMG-0724`.  
Later full-frame record: `S-211` / `E-191` / `IMG-0740`.

Rodney's identification is accepted in the following precise sense:

- Clackamas County Historical Society object `2008.008.046.080` is institutionally titled/identified **George Harding Drug Store - 505 Main Street**.
- Its structured date is **1880**, while its caption says **1880s**.
- The preserved crop visibly shows the George A. Harding fascia, but no street number.
- Repository crop: `media/photos/early-main-street/IMG-0724_1880-505-main-george-harding-drug-store.jpg`.

A later CCHS record, `MOT:P-498`, preserves the apparent same underlying exposure as a full-frame image:

- institutional location: Harding Drug Store, 505 Main;
- date: **circa 1885**;
- repository record: `IMG-0740` / `S-211` / `E-191`;
- it supplies different catalog metadata and a fuller storefront view, so both institutional records are retained and the date variation is preserved rather than collapsed.

The correct synthesis is that the archive has institutional photographic evidence connecting the Harding drug-store scene to the location cataloged as 505 Main in the **1880/1880s–circa-1885** period. Because Oregon City's formal citywide numbering is documented in 1906 and no street number is visible in the photograph, “505 Main” may be a retrospective institutional location label. Neither photograph proves that the photographed structure is the surviving 505 building or that the modern building existed in the 1880s.

## 5. Reconciled chronology relevant to this conversation

1. **1880/1880s–circa 1885:** Harding Drug Store photograph institutionally cataloged at 505 Main; retrospective address/date precision and building continuity remain limited.
2. **1910:** Young's Second Hand Store photograph visibly shows 505 (`S-149` / `E-134` / `IMG-0725`).
3. **1911–1913:** Chicago Store address evidence at 505.
4. **1916:** W. W. Pollock directly associated with Fifth Street Restaurant; exact numbered premises not printed.
5. **October 1918:** Wolf & Miller exact 505 evidence, with the separately preserved 503/505 source conflict in current records.
6. **31 October 1919:** Pollock reported conducting Fifth Street Restaurant and fined on an unsanitary-place complaint.
7. **13 February 1920:** Clem Dollar, block-located pool-hall proprietor between Fifth and Sixth.
8. **2/4 June 1920:** A. Leland's pool hall and electric-sign approval at exact 505½ Main.
9. **1921–1922:** Dr. Freeze uses 505/505½ in advertisements; room arrangement and succession remain unresolved.
10. **1925:** Sanborn Sheet 6 maps 505 as billiards/cigars but does not identify the operator.

This is an occupancy/use chronology, **not a physical-building continuity chain**.

## 6. Current research status and resume point

- **1919 is ONLINE COMPLETE**, following the later annual closeout at `S-306` / `E-280`; it is not ONLINE + MANUAL COMPLETE.
- The targeted public/indexed online 1919–1920 construction/occupancy pass is exhausted and documented.
- The exact construction, reconstruction, enlargement, or remodeling date of the surviving 503 and 505 buildings remains unresolved.
- Do not restart the completed ordinary online search from scratch.

Highest-value remaining work:

1. **MF-041:** recover the 2 June 1920 Council minutes and A. Leland application/bond/license/sign material.
2. Identify A. Leland through an independent directory, license, census, or other record before comparing him with O. H. Leland.
3. Test whether Clem Dollar's hall and A. Leland's premises were the same through exact-address license/transfer evidence.
4. Recover 1919–1921 permit/improvement and Block 4 assessment records under the current manual callouts.
5. Recover the Harding → Wolf/Gates deeds and OHS title abstract for the 1922 property split.
6. Seek an exact-address source connecting Fifth Street Restaurant/Pollock to 501; do not promote the current location hypothesis without that bridge.

No institutional request or paid research is authorized by this handoff.

## 7. Propagation and integrity audit

No new person, business, building, source, evidence, media, or timeline fact was created here. The controlling facts are already propagated through the current source/evidence registers, building/business/person records, unified timeline, crosswalks, and YAML database. This handoff therefore adds no IDs and does not modify those canonical claims.

The supplied Leland and Dollar PDFs are exact duplicates of already preserved binaries and are documented as such in the controlling visual-verification capture. The Pollock PDF and Harding photographs are already preserved under their canonical records. No source file was omitted, and no duplicate binary was manufactured.

Annual status is unchanged by this handoff.
