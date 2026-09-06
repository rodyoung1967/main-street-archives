from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 August 09-30 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-august-09-30-visual-review-2026-09-05.md"
SOURCE_NAME = "Oregon City Courier, 9/16/23/30 August 1917 complete-page visual-review batch"
EVIDENCE_NAME = "August 1917 continuation visually clears 26 pages and completes Courier coverage for the month"


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
        raise SystemExit("Existing August capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Courier — August 9, 16, 23 and 30 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 4 complete issues / 26 of 26 page scans reviewed. August Courier is complete within the five-issue August inventory; 1917 remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-courier/1917-august-unsampled/`  
Retrieval commit: `ba69171fdb3466baa958eae3b7d530b60ed05577`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-august-unsampled/manifest.json`

## Scope and method

This pass reviews every remaining August weekly *Oregon City Courier* issue after the already visually reviewed 2 August monthly-sample issue (`S-134` / `E-120`). All **26 actual page scans** for 9, 16, 23 and 30 August were rendered and visually inspected page by page. Text extraction was used only after all page scans were visually cleared as a checking aid; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 9 August 1917 | 6 | **VISUALLY VERIFIED 6/6** |
| 16 August 1917 | 6 | **VISUALLY VERIFIED 6/6** |
| 23 August 1917 | 6 | **VISUALLY VERIFIED 6/6** |
| 30 August 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Together with the previously reviewed **2 August 1917** issue (6 pages), August now has **5 complete Courier issues / 32 page images visually verified**.

Across the non-overlapping structured monthly sample plus the January–August continuations, the project now has **39 complete tracked 1917 Courier issues / 316 page images visually verified**. This is a progress measure only, not annual certification.

## Selected dated address controls

These are dated observations only; they do not prove uninterrupted occupancy or one-room succession.

- **9 August p.3:** optometrist advertisement — **612 Main St.**
- **9 August p.5:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **16 August p.3:** optometrist advertisement — **612 Main St.**
- **16 August p.5:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **23 August p.2:** Portland Gas & Coke Co. prints **Local Sales Agency — 718 Main St., Oregon City**, adding a dated surrounding-address control.
- **23 August p.3:** optometrist advertisement — **612 Main St.**
- **23 August p.5:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **30 August p.5:** optometrist advertisement — **612 Main St.**
- **30 August p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.

## Exact target-address result

Across these **26 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this August continuation.

The post-review text backstop produced apparent **507** and **509** hits on **9 August p.1**, but scan/context review shows they are draft-board identification numbers attached to men, not street addresses. The backstop also recovered the legitimate 612, 619 and 718 Main controls above. No hidden target-address hit survived scan/context review.

This is a bounded coverage result for the four specified issues. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

August *Courier* coverage is now complete within the five-issue August inventory: **5 issues / 32 pages visually verified**. 1917 remains **IN PROGRESS**. September and later unsampled weekly issues still require page-by-page review, as do the other outstanding annual source classes/gaps, including the true **13 December 1917 Courier page 21** retrieval gap and the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap.
'''

if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 26/26 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **9, 16, 23 and 30 August 1917 (6, 6, 6 and 8 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-08-09/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-august-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-august-unsampled/manifest.json`  
Retrieval commit: `ba69171fdb3466baa958eae3b7d530b60ed05577`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete visual review repeatedly confirms dated 612 and 619 Main controls and adds 718 Main on 23 August. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Apparent 507/509 text hits on 9 August p.1 are draft-board identifiers, not addresses; no vacancy inference is made.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **26 page scans** for the 9, 16, 23 and 30 August 1917 *Oregon City Courier* issues were visually reviewed.
- With the already reviewed 2 August sample, August now has **5 complete issues / 32 visually verified pages**.
- Across the non-overlapping monthly-sample and January–August continuation batches, the project now documents **39 complete tracked 1917 Courier issues / 316 visually verified pages**; this is not exhaustive annual coverage.
- Selected dated controls directly repeat **612 Main** and **619 Main**, while 23 August p.2 adds **718 Main Street** for Portland Gas & Coke's local sales agency.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the 26-page batch.
- Apparent 507/509 text hits on 9 August p.1 are visibly draft-board identification numbers, not street addresses.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count, visible dated address wording and false-positive classification; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible wording; no occupancy-continuity or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-08-09/ed-1/"
    type: "Primary newspaper page scans; visually verified 26/26 pages"
    date: "1917-08-09 through 1917-08-30"
    repository_file: "{CAPTURE_REL}"
    notes: "Complete remaining-August Courier visual review. Dated controls repeatedly confirm 612 and 619 Main; 23 August adds 718 Main. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; 507/509 text hits on 9 August p.1 are draft-board identifiers, not addresses."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-08-09 through 1917-08-30"
    claims:
      - "All 26 page scans for the 9, 16, 23 and 30 August 1917 Courier issues were visually reviewed."
      - "With the 2 August sample, August now has 5 complete issues / 32 visually verified pages."
      - "The non-overlapping monthly-sample and January-August batches now total 39 complete tracked issues / 316 visually verified pages; this is not exhaustive annual coverage."
      - "Selected dated controls repeatedly confirm 612 Main and 619 Main; 23 August p.2 adds 718 Main for Portland Gas & Coke's local sales agency."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the 26-page batch; apparent 507/509 hits on 9 August p.1 are draft-board identifiers, not addresses."
    confidence: "Very High for the inspected-page count, visible dated wording and false-positive classification; no continuity or vacancy inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## August 9–30 continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **26/26 pages** of the remaining 9, 16, 23 and 30 August *Courier* issues. Together with the already reviewed 2 August sample, **August Courier coverage is now 5 complete issues / 32 pages visually verified**.

Repeated exact controls include **612 Main** and **619 Main**; 23 August p.2 adds **718 Main Street**. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Text-layer checking was performed only after visual review; apparent 507/509 hits on 9 August p.1 are draft-board identifiers, not addresses.

Across the non-overlapping monthly sample plus January–August continuations, the documented progress count is now **39 complete tracked issues / 316 visually verified pages**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## August completion added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` completes visual review of the remaining August 9/16/23/30 *Courier* issues (**26/26 pages**). With August 2, August is now **5 complete issues / 32 pages visually verified**. The non-overlapping monthly-sample + January–August batches total **39 complete tracked issues / 316 visually verified pages**. No exact target 501/503/505/507/509/511 occupant was established in the August continuation; apparent 507/509 text hits on August 9 p.1 are draft-board identifiers rather than addresses. This remains partial annual coverage, not closeout certification. The true 13 December page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-april-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-may-10-31-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-june-14-28-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-july-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-august-09-30-visual-review-2026-09-05.md` | Structured monthly sample plus January–August continuations now give **39 complete tracked issues / 316 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February **4 / 36**; March **5 / 46**; April **4 / 32**; May **5 / 40**; June **4 / 32**; July **4 / 32**; August **5 / 32**. Jan. 25 supplies direct 427 Main/corner Fifth; Jones Drug is direct at 617 Main by Mar. 15; April–August repeatedly confirm surrounding exact controls but establish no target 501/503/505/507/509/511 occupant. August 23 adds 718 Main; August 9 apparent 507/509 hits are draft identifiers, not addresses. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk = f'''## {SOURCE_ID} / {EVIDENCE_ID} — remaining August 1917 Courier visual review
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120` | 9/16/23/30 August batch, **26/26 pages visually reviewed**. August totals 5 issues / 32 pages with the August 2 sample. Repeated 612/619 Main controls; 23 August adds 718 Main. No exact 501/503/505/507/509/511 or new 427 occupant. August 9 p.1 507/509 hits are draft identifiers, not addresses. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

log = f'''### 2026-09-05 — completed remaining August 1917 Courier visual review
<!-- {MARKER} -->
- Synced against current `main`; source/evidence IDs are allocated dynamically from the authoritative register maxima at runtime because parallel workflows remain active.
- Visually inspected **26/26 actual page scans** for 9, 16, 23 and 30 August 1917. Preserved source retrieval commit: `ba69171fdb3466baa958eae3b7d530b60ed05577`.
- With the already reviewed 2 August sample, August is now **5 complete issues / 32 visually verified pages**.
- Repeated direct controls include **612 Main** and **619 Main**; 23 August p.2 adds **718 Main Street**.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in these 26 pages.
- Post-review text checks produced 507/509 hits on 9 August p.1; scan/context review confirms they are draft-board identifiers attached to men, not street addresses.
- Non-overlapping tracked 1917 progress is now **39 complete issues / 316 visually verified page images**. 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} remaining August 1917 review")
