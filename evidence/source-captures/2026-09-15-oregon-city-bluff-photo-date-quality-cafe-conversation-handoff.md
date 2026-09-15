# Oregon City bluff photograph dating / Quality Cafe conversation handoff

Date: 15 September 2026 (Pacific)
Repository: `rodyoung1967/main-street-archives`
Branch: `main`
Main head at handoff start: `4be394b66cf5e8673097c58eb5fbb43b1f30f600`

## Required startup for the next chat

Treat current `main` as authoritative. Fetch/sync newest `main` first. Do not reset, revert, force-push, delete, overwrite, discard, or replace newer parallel work. Read `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md` completely. Review this handoff and all newer commits before researching. Visually inspect original archival scans whenever accessible; OCR/search text is discovery only. Preserve uncertainty and retrieval gaps. Keep business operation, business ownership, property ownership, tenancy, trade names, numbered addresses, and physical buildings separate. Do not send institutional requests or authorize fees without project-steward approval. Run `validate_archive.py` before/after writes when practical.

## User-supplied photograph

Uploaded filename in the conversation:
`Oregon City Main Street (Date Unnown - pre 1922)(2).jpg`

The image is a Clackamas County Historical Society copy/watermarked image and visibly carries the bottom caption:

**BUSINESS SECTION OF OREGON CITY, OREGON FROM THE BLUFFS**

At lower right is an apparent **Eddy** photographer/credit mark, consistent with Ralph Eddy, but the exact catalog identity and negative number have not yet been proved.

### Binary preservation status

The image is available in the active conversation/runtime but has **not yet been committed as a binary file to the repository** because the current GitHub connector path available in this chat does not directly transfer the uploaded binary into the repo without a separate binary-ingest step. Under `AGENTS.md`, preserve this as a technical ingest gap rather than omitting the photograph. The next environment with binary-upload capability should compare against existing media first, then commit it under `media/` if it is not already preserved, assign/confirm an IMG ID, and update `media/photo-metadata-register.md`.

## Why the filename's “pre 1922” date is not accepted

The photograph plainly shows the **Oregon City-West Linn concrete arch bridge**. Construction began in 1921, the old suspension bridge was used during construction, and the new bridge opened to the public on **28 December 1922**. Engineering histories state that the old suspension bridge was dismantled once the new arch was completed.

In this photograph:
- the concrete arch bridge appears essentially complete;
- the old suspension bridge towers/cables are not apparent in the reviewed image;
- therefore the image is **not defensibly “pre-1922.”**

Current conservative lower bound:
- **late 1922**, after the new arch had reached completed/near-completed form and the old suspension structure had been dismantled;
- **28 Dec. 1922 or later is plausible and may be the better working lower bound**, but do not call that direct proof until the exact bridge-completion/dismantling sequence is tied to the visible state.

## Current upper bound

The photograph clearly shows the **1884/1885 Clackamas County Courthouse with its clock tower** still standing at Main and Eighth.

Official/local sources say the replacement courthouse was constructed in **1936-1937** and replaced the old courthouse. The exact demolition/start date of the earlier courthouse has not yet been recovered in this photo-dating pass.

Therefore:
- the image is securely **before the old courthouse was removed/replaced**;
- current broad working bracket is approximately **late 1922 to 1935/36**;
- it is entirely possible the photograph is from the **later 1920s or early 1930s**, not just 1922-23.

Do not narrow further without an independent anchor.

## Automobile review

Roughly 18-20 automobiles/trucks are visible, mostly in the open lot and along the river/rail corridor.

Current conclusion:
- source resolution is insufficient to defensibly identify every make/model/model year;
- several vehicles are compatible with late-1910s/1920s touring/runabout forms;
- no vehicle has yet been securely identified with a feature that forces the exposure into 1923+ or another exact model year;
- cars should remain supporting evidence only unless a high-confidence model-year-specific feature can be established from the original/high-resolution negative.

The earlier tentative suggestion that one large vehicle forced a mid-1920s date was withdrawn after re-review.

## QUALITY CAFE versus KWALITY CAFE

This is now an important independent research question.

### 17 Aug. 1922 primary newspaper text lead

Historic Oregon Newspapers, *Banner-Courier*, **17 Aug. 1922, p.2**, contains a local Oregon City “Buy At Home” business list. The indexed/OCR text explicitly reads:

**QUALITY CAFE**

The same list includes Oregon City businesses such as Bank of Commerce, Oregon City Auto Co., Leland and Little, Oregon City Shoe Store, Dr. Freeze, and others, making the Oregon City context clear.

Evidence state at this handoff:
**OCR/TEXT ONLY — original scan still requires visual verification.**

Important limits:
- this establishes a serious contemporary **Quality Cafe** lead in Oregon City;
- it does **not** print a street number in the indexed text;
- it does **not yet prove Quality Cafe = 503 Main**;
- it does **not yet prove Quality Cafe and later Kwality Restaurant/Cafe are the same enterprise;
- it does mean we must not “correct” QUALITY to KWALITY merely because later records use the K spelling.

### Later 503 controls

Current public/City synthesis says:
- **1925 Sanborn:** 503 Main is a restaurant, occupant unnamed;
- **1926 newspaper ads:** reported by the City synthesis as **Kwality Restaurant** at 503;
- **1927 municipal claims:** `Kwality Cafe` appears in City records for meals;
- **1947 directory:** City synthesis reports **Kwality Cafe** at 503;
- later matchbook evidence identifies **New Kwality Cafe, 503 Main, J. Jager, proprietor**.

Thus a possible sequence is:
**Quality Cafe (1922, Oregon City, address unresolved) -> unnamed restaurant at 503 (1925) -> Kwality Restaurant at 503 (1926) -> Kwality Cafe (1927+)**

That sequence is only a **working hypothesis** until a source directly bridges the 1922 Quality Cafe to 503 and/or documents the spelling/name transition.

### Photograph sign reading

At the resolution of the supplied photograph, the storefront/sign lettering is **not sufficiently resolved to distinguish Q from K with confidence**. Any earlier assertion that the photograph itself definitively reads QUALITY should be treated as too strong.

The reason **QUALITY CAFE** is now a serious candidate is the independent August 1922 newspaper text, not because the image pixels alone resolve the word.

## Related photo/catalog leads

1. Clackamas County Family History Society photo gallery includes:
   - **PC094 “Oregon City and Mount Hood-153 Eddy photograph”**, described as showing the 1922 bridge to the left and the first public elevator.
   - This may be related to the supplied image but an exact-image match has not yet been established.

2. Oregon Historical Society:
   - **371N5709 — “View of downtown Oregon City, Oregon”**, Oregon Journal Photographic Negatives, cataloged broadly **1923-1936**.
   - It is a bluff view including downtown and the Oregon City Bridge.
   - Oregon Encyclopedia publishes that image as approximately **c.1930**.
   - This is a useful comparison control, but it is not yet proved to be the same exposure or photographer.

3. Old Oregon Photos sitemap has:
   - **“Oregon City and Mount Hood - 1930”**
   - **“Oregon City Business District from the Bluff - 1945”**
   - **“Oregon City Elevator - 1924”**
   - Ralph Eddy photographed the 28 Dec. 1922 bridge dedication.
   These titles suggest a useful Ralph Eddy sequence for visual comparison.

## 1922 frontage context that must remain separate from photo dating

Current authoritative fire-frontage synthesis:
`timelines/1922-fire-frontage.md`

- 501 Main = Fifth Street Restaurant / Gates portion destroyed in 18 Jul. 1922 fire — **STRONG CROSS-SOURCE INFERENCE**.
- 503 Main = Gilbert Miller shoe-store premises + vacant former Alex Schiermann tailor half/portion; fire-origin building — **STRONG CROSS-SOURCE INFERENCE**.
- 505 Main = adjoining pool/billiard premises; survived with water damage and partial roof burning — **STRONG CROSS-SOURCE INFERENCE** for numbered match.
- 507 Main = Red Front Clothing Store, direct exact-address 1921 evidence and strong July 1922 continuity.

Post-fire 503:
- 1925 Sanborn: restaurant, unnamed.
- 1926 City synthesis: Kwality Restaurant.
- Before this photo is used to revise that chain, the exact photographed 501/503/505 frontage must be mapped and the exposure date tightened independently.

## Highest-value next steps

1. **Visually verify the 17 Aug. 1922 Banner-Courier p.2 original scan** and confirm whether the print really says QUALITY CAFE. Until then keep it OCR/TEXT ONLY.
2. Search late 1922-1927 newspapers/municipal records for **Quality Cafe / Kwality Cafe / Kwality Restaurant**, exact address, proprietor, and spelling transition.
3. Identify the exact supplied photograph in CCHS/Ralph Eddy catalogs using caption, crop geometry, negative number, and neighboring frames.
4. Compare the supplied image against **PC094**, Old Oregon's **Oregon City and Mount Hood - 1930**, and OHS **371N5709**.
5. Recover the exact demolition/start-construction date of the old 1884 courthouse to tighten the upper bound.
6. Compare visible downtown buildings against securely dated 1924, 1928, 1929, 1930, 1935 and 1936 images/aerials.
7. Test riverfront/highway/rail geometry and the parking lot/businesses in the foreground; these may date the image more tightly than cars.
8. Use automobiles only where a truly model-year-specific feature survives at sufficient resolution.
9. Do **not** call the photo 1922/1923 merely because of the bridge. Current defensible bracket is much broader: **late 1922 -> before the 1936-37 courthouse replacement**, pending further narrowing.

## User's desired resume point

The user explicitly believes the photograph may be later than 1922 or 1923 and wants that possibility tested aggressively rather than assumed away.

Resume by:
- visually verifying QUALITY CAFE if possible;
- tracing Quality -> Kwality;
- identifying the exact Eddy/CCHS image;
- tightening the date bracket with courthouse/building/bridge/riverfront controls;
- then return to the 503/505 interpretation only after the exposure date is better constrained.
