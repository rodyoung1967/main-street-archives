from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip("\n") + "\n")


def insert_before(path, anchor, marker, block):
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Anchor not found in {path}: {anchor[:80]!r}")
    write(path, text.replace(anchor, block.strip("\n") + "\n\n" + anchor, 1))


def replace_once(path, old, new, marker=None):
    text = read(path)
    if marker and marker in text:
        return
    if old not in text:
        raise RuntimeError(f"Replacement anchor not found in {path}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


visual_capture = '''# 11 July 1919 Oregon City Enterprise — Gilbert Miller family relocation visual review

Review date: **1 September 2026**. Source `S-160`; evidence `E-144`; person `P-046`.

Status: **VISUALLY VERIFIED PRIMARY NEWSPAPER PAGE; identity/residence context only — not 505 Main occupancy or construction evidence**.

## Source and visual inspection

Publication: *Oregon City Enterprise*, 11 July 1919, page 5.  
Archival page: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-11/ed-1/seq-5/  
Archival PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-11/ed-1/seq-5.pdf

The actual scanned newspaper page was opened and visually inspected on 1 September 2026. OCR had been used previously only to flag the page as a candidate; the finding below is promoted only after this scan review.

The society item headed **“IN SOCIETY CIRCLES”** reports the marriage of Lila Mae Elizabeth Miller and Francis Ray Logue. It identifies the bride as the eldest daughter of **Mr. and Mrs. Gilbert Miller of Ninth and Division streets** and reports that she had come to Oregon City about a year earlier with her parents from **Springfield, Oregon**, where she had lived for five years.

## Historical value and limits

This is strong contemporary corroboration that the Gilbert Miller household had relocated from Springfield to Oregon City by roughly 1918 and was living at Ninth and Division by July 1919. It independently fits the visually verified August 1918 Springfield-to-Oregon-City move chronology already preserved for Gilbert Miller.

It does **not**:

- name Wolf & Miller;
- place Gilbert Miller personally at 505 or 505½ Main;
- identify the unnamed `Miller` partner in the October 1918 505 Main advertisement by direct wording;
- resolve the genuine contemporary **C. E. Miller / Gilbert Miller** source discrepancy;
- identify a business owner, landlord, building owner, permit holder, or tenant at 501/503/505;
- report demolition, rebuilding, enlargement, remodeling, or other construction work.

Accordingly `E-144` is recorded as person/family migration and residence evidence only. The existing strong identity/continuity inference around Gilbert Miller and Wolf & Miller is corroborated but not converted into a direct 505-name proof.

## Preservation

The canonical archival page and PDF links are preserved above. The current integration path can write UTF-8 repository files but cannot transfer the remote PDF binary into the repository. The scan is therefore listed in the physical-source mirroring backlog (`RL-021`) rather than falsely described as locally retained. This is a preservation limitation, not a visual-verification gap.
'''
visual_path = "evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md"
if not Path(visual_path).exists():
    write(visual_path, visual_capture)


closeout = '''# 1919–1920 501/503/505 construction and occupancy — targeted online closeout

Closeout date: **1 September 2026**. Baseline reviewed before this continuation: `f437f71b6a69432d9bdf08bb711a15dfa5351d79` on `main`.

Status: **TARGETED PUBLIC/INDEXED ONLINE PATHS EXHAUSTED FOR THIS SPECIFIC PASS; AUTHENTICATED AND MANUAL RETRIEVAL REMAINS. 1919 AND 1920 ANNUAL STATUSES REMAIN IN PROGRESS.**

This checkpoint addresses the narrow 1919–1920 question of construction/physical change and occupancy around 501/503/505 Main. It does **not** certify either calendar year under `RESEARCH-STANDARD.md`.

## Work intentionally not repeated

The completed *Enterprise* OCR transition triage was **not repeated**. That prior pass covered **91 issues / 728 pages**, triaged all 18 candidates, and recovered no new 501/503/505 demolition, rebuilding, enlargement, or remodel notice. Its two target-specific anchors remain the visually verified 13 February 1920 Clem Dollar block-level pool hall and 4 June 1920 A. Leland 505½ Main pool-hall/sign approval (`E-135` / `S-150`).

## ONLINE work completed in this continuation

### 1. 2 June 1920 Oregon City Council/Commission record

The newer migrated catalog route already documented in the repository was honored: **City Recorder → Public Meeting Records → City Commission** in the City's Laserfiche system. Public/indexed searches were repeated for the exact date and target wording, and likely City DocumentCenter/indexed routes were also tested.

**Result:** the underlying 2 June 1920 minute image was not recovered or visually inspected. No additional owner/landlord, room/premises, remodeling, construction, permit, or license wording can be asserted beyond the already visually verified 4 June newspaper report. The record is retained as an exact **RETRIEVAL GAP / MANUAL OR USER-ASSISTED CALLOUT**, not as absent.

### 2. 1919–1920 R. L. Polk Oregon and Washington State Gazetteer and Business Directory

The exact FamilySearch catalog and two starting image routes were retried:

- catalog `1439422`;
- Part 1 starting ARK `3QS7-89NM-NZJG`;
- Part 2 starting ARK `3QS7-L9NM-N6ZR`.

The project previously demonstrated that authenticated FamilySearch image access can recover actual scans for the 1915–1916 edition. In this continuation, however, the current access path did not expose the 1919–1920 page images for visual inspection. Public alternate-copy searching found catalog/holding references but no independently accessible scan of the target edition.

**Result:** no Oregon City directory entry has been promoted from this edition. There is no omission/vacancy inference. Actual authenticated image review remains outstanding.

### 3. 11 July 1919 Gilbert Miller lead

**Completed and promoted from OCR-only to VISUALLY VERIFIED.** The actual *Oregon City Enterprise* page 5 scan was inspected. The society item identifies Mr. and Mrs. **Gilbert Miller at Ninth and Division streets** and reports that their daughter had come to Oregon City with her parents from **Springfield about a year earlier**.

Registered as `S-160` / `E-144`; detailed visual-review capture: `evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md`.

This corroborates Gilbert Miller's family relocation/residence chronology only. It does **not** name Wolf & Miller, put Gilbert at 505, resolve the C. E. Miller conflict, or supply construction evidence.

### 4. Block 4 Lots 3–4 / Harding property administrative records

Current official online finding aids and custody routes were rechecked for assessment/tax, deed/title, permit/improvement, and Harding-property records. They confirm potentially relevant surviving record series, but no underlying 1919–1922 target record image was recovered in this pass. Current City online permit search coverage is modern and does not substitute for a 1919–1922 permit archive search.

**Result:** no new deed, tax-roll, assessment, permit, lease, or improvement image was visually inspected, so no property/construction claim is promoted. Existing Block 4 geometry and July 1922 newspaper property-sale evidence remain unchanged.

## Construction / occupancy result

The only newly promoted primary fact is the Gilbert Miller household relocation/residence evidence (`E-144`). It is not a target-building construction fact.

The surviving physical-change question remains unresolved:

- the 1911→1925 map footprint/use change is real;
- Wolf & Miller is still directly documented at 505 in October 1918;
- A. Leland is still directly documented as approved for a pool hall at 505½ in June 1920;
- Dr. Freeze shifts into 505½ by 8 April 1921;
- no inspected source in this continuation dates demolition/rebuilding/enlargement/remodeling of the surviving 503 or 505 structure.

Absence of a recovered notice or record was **not** treated as evidence that work did not occur.

## AUTHENTICATED / MANUAL work still required

1. **1920-MIN01 — 2 June 1920 Council/Commission minutes.** Recover the actual scan through the migrated Oregon City Laserfiche catalog, the Oregon City Council/Commission Proceeding Index, City Recorder assistance, or another authorized route. Inspect A. Leland, 505½ Main, pool hall, electric sign, owner/landlord, premises/room wording, building work, and permit/license context.
2. **1919-D01 — 1919–1920 Polk directory scans.** Use an authenticated FamilySearch session to inspect the actual Oregon City section and relevant classified pages for 501, 503, 505, 505½, Wolf & Miller, Gilbert Miller, Clem Dollar, A. Leland, cleaners/dyers, pool/billiards/cigars, shoe repair, tailoring, and Post Office clues. Physical holding `WA-120.1919` remains an alternate manual route. Do not infer vacancy from omission.
3. **1919-BC01 — Banner-Courier microfilm, 17 July 1919 through December 1920.** Oregon City Public Library microfilm. Priority: construction/demolition/remodel/lease/sign notices; Wolf & Miller succession; Clem Dollar; A. Leland; 505/505½; Fifth–Sixth Main/Harding/Post Office location wording.
4. **1920-TAX01 — 1920 Clackamas County assessment/tax roll and index.** Inspect the underlying roll images/microfilm for the applicable original Block 4 parcel crosswalk and land/improvement changes; do not convert a valuation change alone into a construction date.
5. **1922-DEED01 — Harding / S. Wolf / C. Gates deed and title chain.** Recover recorded instruments and legal descriptions underlying the July 1922 newspaper sale; map them to original Block 4 only after the legal descriptions are read.
6. **1922-OHS01 — OHS MSS 1503, Box 19, Block 4 Lots 3–4 abstract.** The collection/index lead exists, but the underlying abstract itself remains uninspected and must not be replaced by catalog metadata.
7. **1920-PERMIT01 — pre-2002 City building/alteration permit or improvement files, if surviving.** Determine the historical custody/series and inspect original records for 1919–1921 target addresses/Block 4; modern online permit coverage is not a substitute.

## Annual-status boundary

This targeted closeout does **not** advance 1919 or 1920 to **ONLINE COMPLETE**. Full annual newspaper page-by-page visual coverage and other required source classes remain separate year-level work. For this specific construction/occupancy question, however, the meaningful ordinary public/indexed online paths identified in the handoff have been worked to either a verified finding or a precisely documented authenticated/manual retrieval boundary.
'''
closeout_path = "evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md"
if not Path(closeout_path).exists():
    write(closeout_path, closeout)


append_once(
    "evidence/source-register.md",
    "## S-160 — Oregon City Enterprise, 11 July 1919, p. 5, Gilbert Miller family relocation",
    '''## S-160 — Oregon City Enterprise, 11 July 1919, p. 5, Gilbert Miller family relocation
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026.  
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-11/ed-1/seq-5/  
PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-11/ed-1/seq-5.pdf  
Related evidence: `E-144`  
Repository source capture: `evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md`  
Notes: Society item identifies Mr. and Mrs. Gilbert Miller at Ninth and Division streets and reports that their daughter came to Oregon City with her parents from Springfield about a year earlier. Corroborates family migration/residence chronology only; does not name Wolf & Miller, place Gilbert at 505/505½, resolve the C. E. Miller discrepancy, or report construction. Remote scan visually inspected; binary mirroring remains under `RL-021`.'''
)

append_once(
    "database/sources.yml",
    "  - id: S-160\n",
    '''  - id: S-160
    name: Oregon City Enterprise, 11 July 1919, p. 5, Gilbert Miller family relocation
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-11/ed-1/seq-5/
    notes: Primary newspaper page visually verified 1 September 2026. Identifies the Gilbert Miller household at Ninth and Division and reports family relocation from Springfield about a year earlier. Identity/residence context only; not 505 occupancy, construction, or resolution of the C. E. Miller conflict. Repository capture evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md; remote binary still needs mirroring under RL-021.'''
)

append_once(
    "evidence/evidence-register.md",
    "## E-144 — Gilbert Miller family at Ninth and Division, July 1919",
    '''## E-144 — Gilbert Miller family at Ninth and Division, July 1919
Type: Primary newspaper social item; **VISUALLY VERIFIED** 1 September 2026.  
Source: `S-160`.  
Repository source capture: `evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md`.  
Claims:
- On 11 July 1919 the *Oregon City Enterprise* identified Mr. and Mrs. **Gilbert Miller** at **Ninth and Division streets**.
- The same item reported that their daughter had come to Oregon City with her parents from **Springfield, Oregon, about a year earlier**, corroborating the broader 1918 family-relocation chronology.
- The item does **not** name Wolf & Miller, identify Gilbert as the directly named 505 partner, resolve the contemporary C. E. Miller / Gilbert Miller discrepancy, or report target-building ownership, tenancy, demolition, rebuilding, enlargement, or remodeling.
Confidence: **Very High** for the printed residence and family-relocation report; business-partner identity, 505 relationship, and construction implications remain unresolved.'''
)

append_once(
    "database/evidence.yml",
    "  - id: E-144\n",
    '''  - id: E-144
    name: Gilbert Miller family at Ninth and Division, July 1919
    type: Primary newspaper social item; visually verified
    claims:
      - On 11 July 1919 the Oregon City Enterprise identified Mr. and Mrs. Gilbert Miller at Ninth and Division streets.
      - The same item reported that their daughter had come to Oregon City with her parents from Springfield about a year earlier, corroborating the broader 1918 family-relocation chronology.
      - The item does not name Wolf & Miller, identify Gilbert as the directly named 505 partner, resolve the C. E. Miller / Gilbert Miller discrepancy, or report target-building ownership, tenancy, demolition, rebuilding, enlargement, or remodeling.
    confidence: Very High for the printed residence and family-relocation report; business-partner identity, 505 relationship, and construction implications remain unresolved.
    related_sources: [S-160]
    related_people: [P-046]
    repository_file: evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md'''
)

append_once(
    "people/profiles/gilbert-miller.md",
    "## July 1919 residence and family-relocation corroboration",
    '''## July 1919 residence and family-relocation corroboration

`S-160` / `E-144` visually verifies the 11 July 1919 *Oregon City Enterprise* society item naming Mr. and Mrs. Gilbert Miller at **Ninth and Division streets** and reporting that their daughter came to Oregon City with her parents from Springfield about a year earlier. This materially corroborates the already documented 1918 Springfield→Oregon City family-move chronology.

It remains **identity/residence context only**. The article does not name Wolf & Miller or 505 Main, so it does not turn the strong Gilbert-Miller continuity inference into a direct 505 partner identification and does not erase the genuine `C. E. Miller` wording in the August 1918 *Eugene Daily Guard*.'''
)

append_once(
    "businesses/wolf-miller.md",
    "## July 1919 Gilbert Miller residence corroboration",
    '''## July 1919 Gilbert Miller residence corroboration

The visually verified 11 July 1919 *Enterprise* item (`S-160` / `E-144`) places the Gilbert Miller household at Ninth and Division and reports the family's arrival from Springfield about a year earlier. This independently supports the broader migration chronology used in the Gilbert Miller identity analysis.

The item does **not** name Wolf & Miller, print 505 Main, or identify a legal/business partner. It is therefore corroborating identity context only; the October 1918 505 advertisement remains the direct business/address evidence and the C. E. Miller/Gilbert Miller source conflict remains open.'''
)

append_once(
    "buildings/505-main.md",
    "### July 1919 Gilbert Miller context — no construction implication",
    '''### July 1919 Gilbert Miller context — no construction implication

`S-160` / `E-144` visually verifies a July 1919 society item placing the Gilbert Miller household at Ninth and Division and reporting the family's move from Springfield about a year earlier. It strengthens Gilbert Miller's Oregon City identity chronology but contains **no 505/505½ address, Wolf & Miller business wording, building ownership, tenancy, or construction statement**. It therefore does not change the construction-date assessment for the surviving 505 building.'''
)

old_timeline = '''| 10, 24 Oct. 1918 | **Wolf & Miller at 505 Main**, shoe/repair trade. | **Exact, visually verified**; Wolf identity and Miller discrepancy open. | `BUS-012`; `E-027`, `E-124`; `S-034`, `S-138` |
| 2/4 Jun. 1920 | City Council reportedly granted **A. Leland** permission to operate a pool hall at **505½ Main** and erect an electric street sign. |'''
new_timeline = '''| 10, 24 Oct. 1918 | **Wolf & Miller at 505 Main**, shoe/repair trade. | **Exact, visually verified**; Wolf identity and Miller discrepancy open. | `BUS-012`; `E-027`, `E-124`; `S-034`, `S-138` |
| 11 Jul. 1919 | Gilbert Miller household reported at **Ninth and Division**; family-move narrative places arrival from Springfield about a year earlier. | **Identity/residence context only**; not 505 occupancy, ownership, or construction evidence; C. E. Miller conflict preserved. | `P-046`; `E-144`; `S-160` |
| 2/4 Jun. 1920 | City Council reportedly granted **A. Leland** permission to operate a pool hall at **505½ Main** and erect an electric street sign. |'''
replace_once(
    "timelines/505-main.md",
    old_timeline,
    new_timeline,
    marker="| 11 Jul. 1919 | Gilbert Miller household reported",
)

append_once(
    "timeline.md",
    "### 11 July 1919 — Gilbert Miller family residence corroboration (context only)",
    '''### 11 July 1919 — Gilbert Miller family residence corroboration (context only)

A visually inspected *Oregon City Enterprise* society item identifies Mr. and Mrs. **Gilbert Miller at Ninth and Division streets** and reports that their daughter came to Oregon City with her parents from Springfield about a year earlier (`E-144` / `S-160`). This corroborates the broader 1918 Miller-family relocation chronology. It does **not** name Wolf & Miller, place Gilbert at 505 Main, resolve the C. E. Miller discrepancy, or date any construction at 501/503/505. This late-added context paragraph is cross-linked from the chronologically ordered 505 address timeline; no physical-building continuity is inferred.'''
)

insert_before(
    "evidence/open-questions.md",
    "## OQ-003 — 505 Rear Addition",
    "**1 September 2026 targeted 1919–1920 online closeout:**",
    '''**1 September 2026 targeted 1919–1920 online closeout:** `S-160` / `E-144` now visually verifies the Gilbert Miller family-relocation/residence lead, but it is identity context only and does not change the 503/505 construction-date questions. The exact 2 June 1920 Commission scan was not recovered through the current public/indexed routes; the 1919–1920 Polk images still require authenticated scan access; and the 1920 assessment roll, Harding/Wolf/Gates deed chain, and OHS Block 4 abstract remain underlying-record/manual tasks. No absence inference was made. See `evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md`.'''
)

old_rl024 = '''**1920 update:** `E-135` / `S-150` visually verifies Clem Dollar's block-located pool hall in February, A. Leland's exact **505½ Main** pool-hall/sign approval in June, and a block-located pool hall in December. These are occupancy/use anchors, **not construction evidence**. Do not merge the three hall references, A. Leland with O. H. Leland, or infer that the surviving 505 structure was new. Highest-value next source is the underlying **2 June 1920 Commission record**, followed by late-1918–1920 permit, lease, assessor, deed/improvement, and relocation records.'''
new_rl024 = old_rl024 + '''

**1 September 2026 targeted closeout:** the public/indexed online routes identified for this narrow question have now been worked to a verified result or a documented access boundary. The 11 July 1919 Gilbert Miller page is now visually verified (`E-144` / `S-160`) and supplies residence/migration context only. The exact 2 June 1920 Commission scan was not recovered; the 1919–1920 Polk scans require authenticated FamilySearch access; and no underlying 1919–1922 assessment, deed, permit or OHS abstract image was recovered. These are explicit authenticated/manual callouts, not negative evidence. See `evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md`.'''
replace_once(
    "evidence/research-leads.md",
    old_rl024,
    new_rl024,
    marker="**1 September 2026 targeted closeout:** the public/indexed online routes",
)

old_rl021 = '''Current priority includes newspaper pages `S-064` through `S-068`, NPS source `S-069`, and the previously noted government PDFs `S-062` and `S-063`.'''
new_rl021 = '''Current priority includes newspaper pages `S-064` through `S-068`, NPS source `S-069`, the previously noted government PDFs `S-062` and `S-063`, and the visually verified but not locally mirrored 11 July 1919 *Enterprise* page `S-160`.'''
replace_once(
    "evidence/research-leads.md",
    old_rl021,
    new_rl021,
    marker="visually verified but not locally mirrored 11 July 1919",
)

append_once(
    "evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md",
    "## 1 September 2026 targeted online closeout",
    '''## 1 September 2026 targeted online closeout

The handoff's remaining ordinary public/indexed online paths have now been worked without repeating the completed 18-candidate Enterprise triage. The one OCR-only candidate that still required visual review — **11 July 1919 p. 5, Gilbert Miller** — is now visually verified as `S-160` / `E-144`. It corroborates the family move from Springfield and the Ninth/Division residence, but it does not name 505, Wolf & Miller, or any construction event.

The exact 2 June 1920 Commission scan remains unrecovered; the 1919–1920 Polk images require authenticated FamilySearch access; and the 1920 assessment roll, Harding/Wolf/Gates deed chain, OHS Block 4 abstract and any surviving pre-2002 City permit/improvement files remain underlying-record/manual tasks. Full distinction between work completed online and manual/authenticated work remaining is saved in `evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md`. The 503/505 physical-change date remains unresolved and neither 1919 nor 1920 is advanced to ONLINE COMPLETE.'''
)

append_once(
    "evidence/source-captures/1918-1920-505-transition-candidate-triage-2026-08-31.md",
    "## 1 September 2026 visual follow-up on candidate 7",
    '''## 1 September 2026 visual follow-up on candidate 7

Candidate **#7, 11 July 1919 p. 5**, has now been visually inspected on the actual *Oregon City Enterprise* scan and promoted from OCR-only to `S-160` / `E-144`. The page confirms Gilbert Miller family residence/migration context described in the original triage. It does **not** name Wolf & Miller, 505/505½, property ownership, or construction. All other dispositions in this 31 August triage remain unchanged; the 18-page triage itself was not repeated.'''
)

append_once(
    "evidence/source-captures/1918-1920-505-transition-target-context.md",
    "## 1 September 2026 status change for candidate 7",
    '''## 1 September 2026 status change for candidate 7

The OCR excerpt for **1919-07-11 p. 5** above is no longer an unverified lead. The actual scanned page was visually inspected on 1 September 2026 and registered as `S-160` / `E-144`. It verifies Gilbert Miller family residence/migration context only; no 505 business, property, or construction relationship is promoted from it. See `evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md`.'''
)

append_once(
    "evidence/source-captures/1919-1920-municipal-directory-access-trail-2026-08-31.md",
    "## 1 September 2026 closeout continuation",
    '''## 1 September 2026 closeout continuation

The migrated Laserfiche folder path documented above remains the correct public-catalog direction, but the **exact 2 June 1920 minute scan was not recovered or visually inspected** in this continuation after additional exact-date/name/indexed searches. Preserve the record as a retrieval/manual gap; do not describe the minutes as nonexistent.

The exact 1919–1920 FamilySearch starting ARKs were also retried. The current session did not expose authenticated page images, and no alternate public scan of the target edition was recovered. Therefore **no directory listing from the 1919–1920 edition is asserted**. Authenticated FamilySearch review remains a manual/user-assisted callout.

The combined public-online/access-boundary checkpoint, including property-record callouts, is `evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md`.'''
)

append_once(
    "indexes/id-crosswalk.md",
    "## 1919 Gilbert Miller residence / migration corroboration",
    '''## 1919 Gilbert Miller residence / migration corroboration

| Source / evidence | Person | Scope and limit |
| --- | --- | --- |
| `S-160` / `E-144` | `P-046` Gilbert Miller | Visually verified 11 July 1919 family residence at Ninth/Division and move-from-Springfield context. **No direct 505, Wolf & Miller partner, property, or construction relationship assigned.** |'''
)

append_once(
    "ARCHIVE_INDEX.md",
    "## 1919–1920 targeted construction/occupancy closeout — 1 September 2026",
    '''## 1919–1920 targeted construction/occupancy closeout — 1 September 2026

- [Targeted online closeout](evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md): ordinary public/indexed paths for the specific 1919–1920 501/503/505 construction/occupancy question were worked to either a verified result or a documented authenticated/manual boundary. Annual 1919/1920 statuses remain **IN PROGRESS**.
- [Gilbert Miller visual review](evidence/source-captures/1919-07-11-gilbert-miller-family-relocation-visual-review.md): `S-160` / `E-144` upgrades the July 1919 lead to visually verified family residence/migration context only. It is **not** direct 505 occupancy or construction evidence.
- Outstanding authenticated/manual targets are the 2 June 1920 Commission scan, 1919–1920 Polk directory scans, Banner-Courier microfilm, 1920 assessment/tax roll, Harding/Wolf/Gates deed chain, OHS MSS 1503 Block 4 abstract, and any surviving pre-2002 City permit/improvement files.'''
)

append_once(
    "registers/research-log.md",
    "### 2026-09-01 — 1919–1920 construction/occupancy targeted online closeout",
    '''### 2026-09-01 — 1919–1920 construction/occupancy targeted online closeout
- Resumed from authoritative `main` at `f437f71b6a69432d9bdf08bb711a15dfa5351d79`; reviewed `AGENTS.md`, `RESEARCH-STANDARD.md`, the four handoff checkpoints and commit `475a4192da6e9503e3ccf147a5161eeef7eda3f9`. Did **not** repeat the finished 91-issue / 728-page / 18-candidate Enterprise OCR triage.
- Visually inspected the actual 11 July 1919 *Oregon City Enterprise* p. 5 scan. Registered `S-160` / `E-144`: Gilbert Miller household at Ninth/Division and family relocation from Springfield about a year earlier. Kept this as identity/residence context only; no 505 occupancy, partner-identity, ownership or construction inference.
- Re-ran current public/indexed retrieval paths for the exact 2 June 1920 Commission action; underlying minute scan still unrecovered. No owner/landlord/remodel/permit wording added beyond `E-135`.
- Retried the exact 1919–1920 Polk catalog/ARK routes and alternate public-copy searches; actual page images were not available in the current authenticated state, so no directory findings were asserted.
- Rechecked official online custody/finding-aid paths for 1920 assessment/tax, Harding/Wolf/Gates deeds/title, OHS Block 4 abstract and historical permit/improvement records. No underlying target image was recovered; each remains a precise authenticated/manual callout.
- Saved `evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md`, distinguishing ONLINE work completed from AUTHENTICATED/MANUAL work required. 1919 and 1920 annual statuses remain **IN PROGRESS**; absence of evidence was not treated as evidence of absence.
- The GitHub integration workflow runs `python3 scripts/validate_archive.py` both before and after these historical changes and commits/pushes only after the post-change validator succeeds.'''
)
