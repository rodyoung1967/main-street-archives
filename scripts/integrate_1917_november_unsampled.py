from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 November 08-29 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-november-08-29-visual-review-2026-09-05.md"
SOURCE_NAME = "Oregon City Courier, 8/15/22/29 November 1917 complete-page visual-review batch"
EVIDENCE_NAME = "November 1917 continuation visually clears 32 pages and completes Courier coverage for the month"
RETRIEVAL_COMMIT = "2bc2108c331034184d81cd1b182778b486f2d705"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block):
    text = read(rel)
    if MARKER in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")
    return True


source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
if not source_nums or not evidence_nums:
    raise SystemExit("Could not determine current source/evidence maxima")
SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"

capture_path = ROOT / CAPTURE_REL
if capture_path.exists():
    cap = read(CAPTURE_REL)
    if MARKER not in cap:
        raise SystemExit(f"{CAPTURE_REL} exists without expected marker")
    sm = re.search(r"source `(S-\d{3})`", cap)
    em = re.search(r"evidence `(E-\d{3})`", cap)
    if not sm or not em:
        raise SystemExit("Existing November capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Courier — November 8, 15, 22 and 29 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 4 complete issues / 32 of 32 page scans reviewed. November Courier is complete within the five-issue November inventory; 1917 remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-courier/1917-november-unsampled/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-november-unsampled/manifest.json`

## Scope and method

This pass reviews every remaining November weekly *Oregon City Courier* issue after the already visually reviewed 1 November monthly-sample issue (`S-134` / `E-120`). All **32 actual page scans** for 8, 15, 22 and 29 November were rendered and visually inspected page by page. Text extraction was used only after all scans were visually cleared as a checking aid; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 8 November 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 15 November 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 22 November 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 29 November 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Together with the previously reviewed **1 November 1917** issue (8 pages), November now has **5 complete Courier issues / 40 page images visually verified**.

Across the non-overlapping structured monthly sample plus the January-November continuations, the project now has **49 complete tracked 1917 Courier issues / 396 page images visually verified**. This is a progress measure only, not annual certification.

## Selected dated controls and contextual lead

These are dated observations only; they do not prove uninterrupted occupancy or one-room succession.

- **8 November p.5:** optometrist advertisement — **612 Main St.**
- **8 November p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **15 November p.5:** the optometrist advertisement visually repeats **612 Main St.**
- **15 November p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **22 November p.4:** optometrist advertisement — **612 Main St.**
- **22 November p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **29 November p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- Jones Drug Co. advertisements recur on 8 November p.2, 15 November p.8, 22 November p.6 and 29 November p.2, but those particular advertisements print only **Oregon City** and do not supply an exact Main Street number. The already reviewed **1 November p.3** sample remains the direct November observation of Jones Drug at **617 Main Street**.
- **15 November p.3, 22 November p.2 and 29 November p.3:** Adams Department Store closing-out advertisements explicitly say **“PART OF BUILDING TO BE TORN DOWN SOON.”** This moves the direct observation of that wording back from the 6 December monthly sample to **15 November 1917**. None of these advertisements prints a numbered street address, so the wording is retained only as an unnumbered downtown demolition/business-closure lead and is **not assigned to 501/503/505 or any other target storefront**.

## Exact target-address result

Across these **32 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this November continuation.

The post-review text backstop recovered the legitimate **612 and 619 Main** controls and the Adams building-removal wording above. Searches for 501, 503, 505, 507, 509, 511, 427, 519, 617 and 718 produced no address candidate in the extracted text for these four issues. Scan-visible Jones Drug advertisements without a number were not silently converted into 617 Main observations.

This is a bounded coverage result for the four specified issues. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

November *Courier* coverage is now complete within the five-issue November inventory: **5 issues / 40 pages visually verified**. The non-overlapping tracked total through November is **49 complete issues / 396 pages**. 1917 remains **IN PROGRESS**. December continuation work remains, including special handling of the known true **13 December 1917 Courier page 21** retrieval gap, and the **Sohns & Woodbeck 1916-1917 directory, Oregon City section** gap remains open.
'''

if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 32/32 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **8, 15, 22 and 29 November 1917 (8 pages each)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-11-08/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-november-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-november-unsampled/manifest.json`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete visual review confirms recurring 612/619 Main controls. Jones Drug ads in these four issues print Oregon City but not an exact number; Nov. 1 remains the month's direct 617 Main observation. Adams Department Store building-removal wording is directly visible by Nov. 15 but remains unnumbered and is not assigned to the target block. No exact 501/503/505/507/509/511 or new 427 Main occupant was established.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **32 page scans** for the 8, 15, 22 and 29 November 1917 *Oregon City Courier* issues were visually reviewed.
- With the already reviewed 1 November sample, November now has **5 complete issues / 40 visually verified pages**.
- Across the non-overlapping monthly-sample and January-November continuation batches, the project now documents **49 complete tracked 1917 Courier issues / 396 visually verified pages**; this is not exhaustive annual coverage.
- Recurring exact controls include **612 Main** and **619 Main**. Jones Drug advertisements recur in all four issues but those particular ads do not print an exact street number; the 1 November sample remains the direct November **617 Main** observation.
- Adams Department Store's **“PART OF BUILDING TO BE TORN DOWN SOON”** wording is directly visible by **15 November 1917** and repeats 22 and 29 November, but the ads are unnumbered and are not assigned to the target frontage.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the 32-page batch.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count and visible dated wording; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible wording; no occupancy-continuity, demolition-location or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-11-08/ed-1/"
    type: "Primary newspaper page scans; visually verified 32/32 pages"
    date: "1917-11-08 through 1917-11-29"
    repository_file: "{CAPTURE_REL}"
    notes: "Complete remaining-November Courier visual review. Recurring 612/619 Main controls; Jones Drug ads in these four issues lack an exact number; Adams building-removal wording is direct by Nov. 15 but remains unnumbered. No exact 501/503/505/507/509/511 or new 427 Main occupant was established."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-11-08 through 1917-11-29"
    claims:
      - "All 32 page scans for the 8, 15, 22 and 29 November 1917 Courier issues were visually reviewed."
      - "With the 1 November sample, November now has 5 complete issues / 40 visually verified pages."
      - "The non-overlapping monthly-sample and January-November batches now total 49 complete tracked issues / 396 visually verified pages; this is not exhaustive annual coverage."
      - "Recurring exact controls include 612 Main and 619 Main; the Jones Drug ads in these four issues do not print an exact street number."
      - "Adams Department Store building-removal wording is directly visible by 15 November and repeats 22 and 29 November, but the advertisements are unnumbered and are not assigned to the target frontage."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the 32-page batch."
    confidence: "Very High for the inspected-page count and visible dated wording; no continuity, demolition-location or vacancy inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## November 8-29 continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **32/32 pages** of the remaining 8, 15, 22 and 29 November *Courier* issues. Together with the already reviewed 1 November sample, **November Courier coverage is now 5 complete issues / 40 pages visually verified**.

Recurring exact controls include **612 Main** and **619 Main**. Jones Drug ads recur but those four ads do not print an exact street number; the Nov. 1 sample remains the direct November 617 Main observation. Adams Department Store's building-removal wording is directly visible by **15 November**, but remains unnumbered and is not assigned to the target block. No exact 501/503/505/507/509/511 or new 427 Main occupant was established.

Across the non-overlapping monthly sample plus January-November continuations, the documented progress count is now **49 complete tracked issues / 396 visually verified pages**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## November completion added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` completes visual review of the remaining November 8/15/22/29 *Courier* issues (**32/32 pages**). With November 1, November is now **5 complete issues / 40 pages visually verified**. The non-overlapping monthly-sample + January-November batches total **49 complete tracked issues / 396 visually verified pages**. Recurring 612/619 Main controls continue; the unsampled Jones ads do not print exact street numbers. Adams Department Store building-removal wording is directly visible by Nov. 15 but is unnumbered and is not assigned to the target block. No exact target 501/503/505/507/509/511 occupant was established. This remains partial annual coverage, not closeout certification. The true 13 December page-21 and Sohns & Woodbeck Oregon City section gaps remain open.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        refs = "`evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-april-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-may-10-31-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-june-14-28-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-july-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-august-09-30-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-september-13-27-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-october-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-november-08-29-visual-review-2026-09-05.md`"
        notes = "Structured monthly sample plus January-November continuations now give **49 complete tracked issues / 396 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February **4 / 36**; March **5 / 46**; April **4 / 32**; May **5 / 40**; June **4 / 32**; July **4 / 32**; August **5 / 32**; September **4 / 32**; October **4 / 32**; November **5 / 40**. Jan. 25 supplies direct 427 Main/corner Fifth; Jones Drug is direct at 617 Main by Mar. 15 and again Sep. 27, Oct. 11, Oct. 18 and Nov. 1; Sep. 27 also directly gives Theroux Music House at 519 Main. Adams Department Store building-removal wording is now direct by Nov. 15 but remains unnumbered and is not assigned to the target frontage. Surrounding exact controls do not establish a target 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished."
        lines[i] = f"| 1917 | **IN PROGRESS** | {refs} | {notes} |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk = f'''## {SOURCE_ID} / {EVIDENCE_ID} — remaining November 1917 Courier visual review
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120` | 8/15/22/29 November batch, **32/32 pages visually reviewed**. November totals 5 issues / 40 pages with the Nov. 1 sample. Recurring 612/619 controls; unsampled Jones ads lack exact numbers. Adams building-removal wording is direct by Nov. 15 but unnumbered. No exact 501/503/505/507/509/511 or new 427 occupant. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

log = f'''### 2026-09-05 — completed remaining November 1917 Courier visual review
<!-- {MARKER} -->
- Synced against current `main`; source/evidence IDs are allocated dynamically from the authoritative register maxima at runtime because parallel workflows remain active.
- Visually inspected **32/32 actual page scans** for 8, 15, 22 and 29 November 1917. Preserved source retrieval commit: `{RETRIEVAL_COMMIT}`.
- With the already reviewed 1 November sample, November is now **5 complete issues / 40 visually verified pages**.
- Recurring exact controls include **612 Main** and **619 Main**. The Jones Drug ads in the four continuation issues print Oregon City but not an exact street number; Nov. 1 remains the month's direct 617 Main observation.
- Adams Department Store's **PART OF BUILDING TO BE TORN DOWN SOON** wording is directly visible by **15 November 1917** and repeats on 22 and 29 November; the ads are unnumbered and are not assigned to the target frontage.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in these 32 pages.
- Text extraction was used only after all scans were visually reviewed.
- Non-overlapping tracked 1917 progress is now **49 complete issues / 396 visually verified page images**. 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} remaining November 1917 review")
