# Eddy/CCHS bluff photograph — Elks comparison and Quality Cafe follow-up

Date: 15 September 2026
Repository: `rodyoung1967/main-street-archives`

## CCHS catalog metadata supplied by project steward

The project steward recovered the following catalog metadata for the photograph on 15 September 2026:

- **Name/Title:** Oregon City Main Street
- **Entry/Object ID:** C.0250.005060
- **Description:** Business Section of Oregon City from the Bluff.

Crucially, this metadata **does not state a 1922 or pre-1922 date**. The earlier words `pre 1922` came from the uploaded/inherited filename and must not be attributed to Clackamas County Historical Society catalog metadata.

This changes the purpose of the dating work: it should be framed as an effort to **help refine an undated catalog photograph**, not as a correction of a CCHS dating error.

## User-supplied image re-upload

Uploaded filename: `Oregon City Main Street (Date Unnown - pre 1922)(3).jpg`
Image dimensions inspected in this research environment: **1381 × 870 px**.
Visible caption: **BUSINESS SECTION OF OREGON CITY, OREGON FROM THE BLUFFS**.
Visible lower-right photographer mark appears to read **Eddy**.
The image carries a Clackamas County Historical Society watermark.

The filename wording is not institutional dating evidence.

### Binary preservation

The steward-supplied JPEG was inspected directly in the active runtime. Its control fingerprint is **1381 × 870 px**, **219,852 bytes**, SHA-256 `97b269e43fe38e85b9b8169e1a819870528e7f3ac676279e3a1594d6b3d302aa`.

The actual image binary is **not yet committed to current `main`**, so this item must not yet be described as fully preserved. However, the earlier assumption that a special local-binary upload capability was required is superseded. The repository already has a proven CCHS binary-ingest method: adapt the existing CatalogIt fetch script and GitHub Actions workflow documented in `BINARY-INGEST.md` and proven by `IMG-0771` / commit `d6fdf22de7df77b0e3ce30864b26a5155b25eb42`.

For the complete current procedure and handoff, see `evidence/source-captures/2026-09-15-c0250-005060-binary-ingest-and-conversation-handoff.md`.

## 1923 replacement Elks Lodge comparison

### Documentary controls

Oregon City Elks Lodge #1189's own history states that the lodge building burned on **2 December 1922**, that the replacement was completed in **1923**, and that the first meeting in the new building was held **7 December 1923**.

The September 1923 *Elks Magazine* describes the new Oregon City building as then being built, approximately **66 × 103 feet**, reinforced concrete, with completion expected in the fall. This independently supports a substantial new lodge structure reaching completion late in 1923.

The 2 December 1922 fire reporting places the destroyed predecessor at **Seventh and Water streets**. Existing project synthesis of the 1925 Sanborn places the replacement Elks Lodge on Water Street between Sixth and Seventh.

### Visual comparison

The re-uploaded bluff photograph was visually inspected at full available resolution and cropped/zoomed around the bridge/Water Street block.

Immediately on the Oregon City side of the concrete arch bridge is a large, long, lodge-sized building in the expected Seventh/Water location. Its placement, long rectangular mass, roof geometry, and relationship to the bridge approach agree closely with the clearly identifiable bridge-adjacent Elks Lodge in the cataloged **1945 Ralph Eddy bluff view**. The 1945 view supplies a particularly useful same-vantage spatial control.

The available bluff angle does **not** expose enough of the principal street facade to use the later Mission/Spanish-style parapet treatment as a direct facade match. Therefore the identification is not promoted to DOCUMENTED/DIRECT solely from architectural ornament.

**Evidence state: STRONG CROSS-SOURCE / VISUAL-SPATIAL INFERENCE.** The bridge-adjacent building in the user photograph is very likely the 1923 replacement Oregon City Elks Lodge.

### Dating consequence

This substantially weakens any 1922 or early-1923 date. Because the replacement was still under construction in September 1923 and the first lodge meeting in the completed new building was 7 December 1923, the most defensible working lower bound is now **late 1923**, with **December 1923 or later** favored if the photographed building is in completed form.

Do not yet express 7 December 1923 as an exact terminus post quem: the photograph does not independently prove whether every visible portion was complete before the first meeting.

Later research in the repository has since produced a stronger working date of approximately **1929–1935**, based principally on the post-improvement Railroad Avenue configuration and the still-standing old courthouse. See `evidence/source-captures/2026-09-15-eddy-bluff-photo-1929-1935-metadata-challenge-and-ohs-followup.md`.

## 17 August 1922 Banner-Courier — QUALITY CAFE

Public Historic Oregon Newspapers text for *Banner-Courier*, 17 Aug. 1922, p.2, continues to transcribe the Buy At Home/Friends of Labor list as **QUALITY CAFE**. However, this remains **OCR/TEXT ONLY**, not VISUALLY VERIFIED, until the faithful page scan is inspected.

The OCR occurrence supplies **no street address or proprietor**. It therefore does not establish that Quality Cafe was at 503 Main and does not establish identity with later Kwality Restaurant/Kwality Cafe.

## Current hypothesis — unchanged

Possible sequence requiring proof:

`Quality Cafe` (Oregon City, Aug. 1922; address unresolved) → restaurant at 503 on 1925 Sanborn → `Kwality Restaurant` at 503 in 1926 synthesis → `Kwality Cafe` in later records.

Do **not** merge these businesses or spellings until direct evidence supports the transition.

## Next actions

1. Use the proven CCHS binary-ingest workflow in `BINARY-INGEST.md` to preserve exact object **C.0250.005060** under `media/photos/main-street/`; assign the next valid `IMG-####` only after checking the current register/inventory.
2. Update `media/photo-metadata-register.md`, `media/photos/inventory.md`, and the relevant source records when the binary is actually committed.
3. Verify the JPEG exists on current `main` and record the binary-preservation commit before calling the ingest complete.
4. Continue refining the current circa 1929–1935 bracket, including exact Railroad Avenue completion and courthouse replacement milestones.
5. Recover the faithful scan of 17 Aug. 1922 *Banner-Courier* p.2 and visually verify `QUALITY CAFE`.
6. Do not send institutional requests or authorize fees without project-steward approval.

## Validation note

This write was made through the GitHub connector. `validate_archive.py` was not executable in that connector-only environment; no validator result is claimed.
