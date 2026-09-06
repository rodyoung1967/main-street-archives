from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 April 12-26 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-april-12-26-visual-review-2026-09-05.md"
SOURCE_NAME = "Oregon City Courier, 12/19/26 April 1917 complete-page visual-review batch"
EVIDENCE_NAME = "April 1917 continuation visually clears 24 pages and completes Courier coverage for the month"


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

if (ROOT / CAPTURE_REL).exists() and MARKER not in read(CAPTURE_REL):
    raise SystemExit(f"{CAPTURE_REL} exists without expected marker")
if (ROOT / CAPTURE_REL).exists():
    # Idempotent rerun: recover IDs from existing capture rather than allocate new ones.
    cap = read(CAPTURE_REL)
    sm = re.search(r"source `(S-\d{3})`", cap)
    em = re.search(r"evidence `(E-\d{3})`", cap)
    if not sm or not em:
        raise SystemExit("Existing April capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Courier — April 12, 19 and 26 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 3 complete issues / 24 of 24 page scans reviewed. April Courier is complete within the four-issue April inventory; 1917 remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-courier/1917-april-unsampled/`  
Retrieval commit: `f4a0007afa908fe36388157b96dad1e28037f076`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-april-unsampled/manifest.json`

## Scope and method

This pass reviews every remaining April weekly *Oregon City Courier* issue after the already visually reviewed 5 April monthly-sample issue (`S-134` / `E-120`). All **24 actual page scans** for 12, 19 and 26 April were rendered and visually inspected page by page. Text extraction was used only after visual inspection as a checking aid; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 12 Apr. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 19 Apr. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 26 Apr. 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Together with the previously reviewed **5 April 1917** issue (8 pages), April now has **4 complete Courier issues / 32 page images visually verified**.

Across the non-overlapping structured monthly sample plus the January–April continuations, the project now has **25 complete tracked 1917 Courier issues / 210 page images visually verified**. This is a progress measure only, not annual certification.

## Selected dated address controls

These are dated observations only; they do not prove uninterrupted occupancy or one-room succession.

- **12 Apr. p.3:** Williams Bros. Transfer & Storage — **Office 612 Main Street**; R. L. Holman — **Fifth and Main St.**
- **12 Apr. p.5:** optometrist advertisement — **612 Main Street**.
- **12 Apr. p.7:** Portland Railway Light & Power Co. Electric Store — **Andresen Bldg., 619 Main St.**; R. L. Holman — **Fifth and Main St.**
- **19 Apr. p.3:** Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **19 Apr. p.4:** optometrist advertisement — **612 Main St.**
- **19 Apr. p.7:** Electric Store — **Andresen Bldg., 619 Main St.**
- **19 Apr. p.8:** R. L. Holman — **Fifth and Main St.**
- **26 Apr. p.2:** R. L. Holman — **Fifth and Main St.**
- **26 Apr. p.3:** Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **26 Apr. p.5:** optometrist — **612 Main St.**; R. L. Holman — **Fifth and Main St.**
- **26 Apr. p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; R. L. Holman — **Fifth and Main St.**

## Exact target-address result

Across these **24 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this April continuation.

A post-review text-layer check was used only as a backstop. Apparent target-like numeric strings were rejected when the scan/context showed they were not target storefront addresses. In particular:

- **19 Apr. p.6** contains numbers such as `$21,505`, `$6,505`, `$4,505`, `$30,505`, and `$617.12` in a county-expenditure list; they are amounts/ledger figures, not Main Street addresses.
- **26 Apr. p.2** includes **509 Boss Street**, not 509 Main Street.

This is a bounded coverage result for the three specified issues. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

April *Courier* coverage is now complete within the four-issue April inventory: **4 issues / 32 pages visually verified**. 1917 remains **IN PROGRESS**. May and later unsampled weekly issues still require page-by-page review, as do the other outstanding annual source classes/gaps, including the true **13 December 1917 Courier page 21** retrieval gap and the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap.
'''

if not (ROOT / CAPTURE_REL).exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 24/24 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **12 April 1917 (8 pages); 19 April 1917 (8 pages); 26 April 1917 (8 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-04-12/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-april-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-april-unsampled/manifest.json`  
Retrieval commit: `f4a0007afa908fe36388157b96dad1e28037f076`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete visual review repeats dated 612 Main, 619 Main and Fifth/Main controls. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Text-layer false positives include county-expenditure amounts ending in 505/617 and 509 Boss Street; no vacancy inference.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **24 page scans** for the 12, 19 and 26 April 1917 *Oregon City Courier* issues were visually reviewed.
- With the already reviewed 5 April sample, April now has **4 complete issues / 32 visually verified pages**.
- Across the non-overlapping monthly-sample and January–April continuation batches, the project now documents **25 complete tracked 1917 Courier issues / 210 visually verified pages**; this is not exhaustive annual coverage.
- Selected dated controls directly repeat **612 Main**, **619 Main**, and **Fifth/Main**.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the 24-page batch.
- Post-review text checking did not change that result: April 19 target-like `505`/`617` strings are county-expenditure amounts, while April 26's `509` is **509 Boss Street**, not 509 Main.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count and visible dated address wording; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible wording; no occupancy-continuity or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-04-12/ed-1/"
    type: "Primary newspaper page scans; visually verified 24/24 pages"
    date: "1917-04-12 through 1917-04-26"
    repository_file: "{CAPTURE_REL}"
    notes: "Complete remaining-April Courier visual review. Dated controls repeat 612 Main, 619 Main and Fifth/Main. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; text-like numeric false positives were rejected against scan context."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-04-12 through 1917-04-26"
    claims:
      - "All 24 page scans for the 12, 19 and 26 April 1917 Courier issues were visually reviewed."
      - "With the 5 April sample, April now has 4 complete issues / 32 visually verified pages."
      - "The non-overlapping monthly-sample and January-April batches now total 25 complete tracked issues / 210 visually verified pages; this is not exhaustive annual coverage."
      - "Selected dated controls repeat 612 Main, 619 Main and Fifth/Main."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the 24-page batch; this is bounded coverage, not vacancy or absence evidence."
      - "Text-layer target-like strings on April 19 are county-expenditure amounts, and April 26's 509 is 509 Boss Street rather than 509 Main."
    confidence: "Very High for the inspected-page count and visible dated wording; no continuity or vacancy inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## April 12–26 continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **24/24 pages** of the remaining 12, 19 and 26 April *Courier* issues. Together with the already reviewed 5 April sample, **April Courier coverage is now 4 complete issues / 32 pages visually verified**.

Repeated controls include **612 Main**, **619 Main**, and **Fifth/Main**. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. A text-layer backstop was checked against the scans: target-like `505`/`617` numbers on April 19 are county-expenditure amounts, and April 26's `509` is **509 Boss Street**.

Across the non-overlapping monthly sample plus January–April continuations, the documented progress count is now **25 complete tracked issues / 210 visually verified pages**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## April completion added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` completes visual review of the remaining April 12/19/26 *Courier* issues (**24/24 pages**). With April 5, April is now **4 complete issues / 32 pages visually verified**. The non-overlapping monthly-sample + January–April batches total **25 complete tracked issues / 210 visually verified pages**. No exact target 501/503/505/507/509/511 occupant was established in the April continuation. This remains partial annual coverage, not closeout certification. The true 13 December page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-april-12-26-visual-review-2026-09-05.md` | Structured monthly sample plus January–April continuations now give **25 complete tracked issues / 210 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February **4 / 36**; March **5 / 46**; April **4 / 32**. Jan. 25 supplies direct 427 Main/corner Fifth; Jones Drug is direct at 617 Main by Mar. 15; April repeats 612 Main, 619 Main and Fifth/Main controls but establishes no target 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk = f'''## {SOURCE_ID} / {EVIDENCE_ID} — remaining April 1917 Courier visual review
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120` | 12/19/26 April batch, **24/24 pages visually reviewed**. April totals 4 issues / 32 pages with the April 5 sample. Repeated 612 Main, 619 Main and Fifth/Main controls; no exact 501/503/505/507/509/511 or new 427 occupant; no continuity/vacancy inference. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

log = f'''### 2026-09-05 — completed remaining April 1917 Courier visual review
<!-- {MARKER} -->
- Synced against current `main`; source/evidence IDs were allocated dynamically from the authoritative register maxima to avoid collision with active parallel ownership work.
- Visually inspected **24/24 actual page scans** for 12, 19 and 26 April 1917. Preserved source retrieval commit: `f4a0007afa908fe36388157b96dad1e28037f076`.
- With the already reviewed 5 April sample, April is now **4 complete issues / 32 visually verified pages**.
- Repeated direct controls include **612 Main**, **619 Main**, and **Fifth/Main**.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in these 24 pages.
- Text-layer backstop did not change the result: April 19 `505`/`617` strings are county-expenditure amounts; April 26's `509` is **509 Boss Street**.
- Non-overlapping tracked 1917 progress is now **25 complete issues / 210 visually verified page images**. 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} remaining April 1917 review")
