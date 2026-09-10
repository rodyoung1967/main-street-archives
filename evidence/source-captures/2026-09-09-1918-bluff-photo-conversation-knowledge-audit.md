# 1918 bluff photograph conversation-knowledge preservation audit — 9 September 2026

This checkpoint preserves the complete project-relevant knowledge from the conversation in which the project steward supplied **CCHS 2008.008.009.016, Oregon City from the Bluff at 4th Street Steps**, and identified the later-numbered 501/503/505 frontage in the image. It is an audit/checkpoint, not a new independent historical source.

## Repository synchronization control

Before this preservation pass, current `main` was re-read together with `AGENTS.md`, `RESEARCH-STANDARD.md`, and `MANUAL-FOLLOWUP.md`. Parallel project work had advanced `main`; none of that work was reset, reverted, force-pushed, or overwritten. The historical integration described below already existed on current `main`; this audit confirms completeness and removes only temporary automation artifacts that were no longer needed.

## Project-steward supplied 1918 photograph

Canonical institutional object and supplied metadata:

- Institution: **Clackamas County Historical Society (CCHS)**
- Name/Title: **Oregon City from the Bluff at 4th Street Steps**
- Entry/Object ID: **2008.008.009.016**
- Description: **Oregon City from the Bluff at 4th Street Steps. Huntley Drug Store Post Card negative.**
- Date made: **1918**
- City/County/State: **Oregon City, Clackamas County, Oregon**
- Medium: **Negative**
- Location of Negative: **Society Collection**
- Other Number: **Brewer-Green 16**
- Steward-supplied filename: `Oregon City from the Bluff at 4th Street Steps.jpg`
- Steward-supplied dimensions: **2048 × 1181**
- Steward-supplied bytes: **884,802**
- Steward-supplied SHA-256: `f41164c211f4934d1b80d769ede9ff898742861f0615b87d1e6f9d987db5025e`

The detailed canonical capture is:

`evidence/source-captures/2008-008-009-016-1918-bluff-4th-street-steps-target-frontage-2026-09-09.md`

Archive IDs are **S-311 / E-283 / IMG-0769 / T-103**. The institutional derivative is preserved at:

`media/photos/early-main-street/IMG-0769_1918-bluff-4th-street-steps-target-frontage-cchs-2008-008-009-016.jpg`

## Steward structural observation preserved exactly in evidentiary meaning

The project steward identifies the later-numbered **501, 503, and 505 Main** predecessor frontage in the 1918 view. The important structural observation is that the **upper false-front/parapet at the later 505 position is already partly lowered or missing**, whereas an earlier state showed a more uniform upper roof/facade line across the three-building group.

The photograph itself does **not** display readable 501/503/505 street numbers. Therefore the archive correctly preserves the individual-bay assignment as **ATTRIBUTED PROJECT-STEWARD SPATIAL TESTIMONY plus cross-source map/address geometry**, not as a street number directly read from the photograph.

The image itself was visually inspected. The visible uneven upper facade/roofline is **VISUALLY VERIFIED**; the exact later-address bay assignment retains the attribution/geometry qualification above.

## Later comparison photograph and structural bracket

The conversation also used the later CCHS photograph **P‑267 — Oregon City and the Arch Bridge as Seen from Bluff**, institutionally dated **1924–1928**, as a comparison state. Its canonical archive IDs are **S-312 / E-284 / IMG-0770 / T-104**, with the combined structural inference recorded as **E-285**.

The strongest combined conclusion remains:

> the target frontage underwent **material physical replacement/reconfiguration after the photographed 1918 state and by 1925**.

That conclusion is a **STRONG CROSS-SOURCE INFERENCE**, using the two photographs together with established target geometry and the independent 1925 Sanborn control. It does **not** establish an exact construction year for 501, 503, or 505; it does not prove that all three changed in one construction campaign; and it does not prove owner, builder, cause, or a direct causal relationship to the July 1922 fire.

The approximate historic-survey dates around **c.1919 for 503** and **c.1920 for 505** may fit this narrowed bracket, but remain estimates until primary construction/permit/assessment/deed evidence establishes more.

Canonical comparison capture:

`evidence/source-captures/1918-to-1925-target-frontage-photographic-structural-bracket-2026-09-09.md`

## P‑267 provenance correction preserved

During integration, a catalog-number-only CatalogIt lookup initially encountered an unrelated object sharing the external catalog number `P-267`. That source association was rejected and corrected. The correct institutional control requires both the catalog number and the Oregon City title:

- CCHS catalog: **P‑267**
- Title: **Oregon City and the Arch Bridge as Seen from Bluff.**
- Correct CatalogIt API entry: `d0789660-9b1e-11eb-b3ef-53e7205a00b4`
- Correct slug: `oregon-city-and-the-arch-bridge-as-seen-from-bluff.`
- Correct repository derivative: `media/photos/early-main-street/IMG-0770_1924-1928-arch-bridge-bluff-target-frontage-cchs-p-267.jpg`
- Correct repository dimensions: **2400 × 1902**
- Correct repository bytes: **784,067**
- Correct repository SHA-256: `8a084d7d48dc176e871e79b96be2653eaea276aa4210a02905a97117948d8e9f`
- Perceptual comparison to the steward-supplied photograph differed by only **1/256 dHash bits**, strongly confirming the same substantive image.

The detailed correction is already preserved in:

`evidence/source-captures/p-267-1924-1928-arch-bridge-bluff-target-frontage-2026-09-09.md`

The provenance/binary repair did **not** change the historical structural interpretation or confidence level.

## Existing integration and propagation

The photograph batch was integrated on `main` in commit:

- `6c3a3e0da904a0450f137e69dded83127c312ce4` — **Integrate 1918 and P-267 target-frontage photographs**

The corrected P‑267 source association was committed in:

- `103a1d0e3167d11a43e02afefdbc6a1897b2ba8f` — **Correct CCHS P-267 source association**

The batch is propagated through the appropriate source, evidence, media, building, timeline, crosswalk, open-question/research-lead, and YAML/database records under the marker `2026-09-09-cchs-1918-p267-target-transition`. No new person or business identity is established by these photographs.

## Manual/research status effect

This conversation does **not** close any outstanding primary-source construction-date question and does not justify a new manual callout. Existing permit, assessment, deed, and structural-continuity research routes remain the proper way to resolve exact construction/replacement dates. No institutional request or paid research was authorized or sent in this conversation.

## Temporary automation cleanup

The following one-purpose integration/diagnostic artifacts were removed from `main` after their results had been fully preserved in the canonical archive records and Git history:

- `.github/workflows/temp-integrate-cchs-1918-p267-target-transition.yml`
- `.github/workflows/temp-diagnose-cchs-p267.yml`
- `.github/workflows/temp-repair-cchs-p267-association.yml`
- `scripts/integrate_cchs_1918_p267_target_transition.py`

Cleanup commits:

- `572c31c5442620ad4538d0be7abf870e8e86938d` — Remove temporary 1918-P267 integration workflow
- `e0fef31a2d62c1c1507ccae51a0ba239de0153c1` — Remove temporary P-267 diagnostic workflow
- `df171d65d407bcb6cd219bc5415fc77c3d5eca8b` — Remove temporary P-267 source repair workflow
- `7ecbd1d183ec459b0dd3bd9c4d1630240b8be841` — Remove temporary 1918-P267 integration script

These deletions remove temporary tooling only; they do not delete historical evidence, source metadata, images, conclusions, uncertainty notes, or provenance corrections.

## Preservation conclusion

All project-relevant historical knowledge from this conversation is now represented in canonical repository records or this audit checkpoint. No additional historical claim is being manufactured from the conversation. The remaining uncertainty—especially the exact dates and causes of the 501/503/505 structural replacements—remains explicit and intentionally unresolved pending better primary evidence.
