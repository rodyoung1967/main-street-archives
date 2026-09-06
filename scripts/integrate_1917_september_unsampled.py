from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 September 13-27 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-september-13-27-visual-review-2026-09-05.md"
SOURCE_NAME = "Oregon City Courier, 13/20/27 September 1917 complete-page visual-review batch"
EVIDENCE_NAME = "September 1917 continuation visually clears 24 pages and completes Courier coverage for the month"


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
        raise SystemExit("Existing September capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Courier — September 13, 20 and 27 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 3 complete issues / 24 of 24 page scans reviewed. September Courier is complete within the four-issue September inventory; 1917 remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-courier/1917-september-unsampled/`  
Retrieval commit: `8a3bee05860be735e2af968841050cbd2aca6a39`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-september-unsampled/manifest.json`

## Scope and method

This pass reviews every remaining September weekly *Oregon City Courier* issue after the already visually reviewed 6 September monthly-sample issue (`S-134` / `E-120`). All **24 actual page scans** for 13, 20 and 27 September were rendered and visually inspected page by page. Text extraction was used only after all page scans were visually cleared as a checking aid; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 13 September 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 20 September 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 27 September 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Together with the previously reviewed **6 September 1917** issue (8 pages), September now has **4 complete Courier issues / 32 page images visually verified**.

Across the non-overlapping structured monthly sample plus the January–September continuations, the project now has **42 complete tracked 1917 Courier issues / 340 page images visually verified**. This is a progress measure only, not annual certification.

## Selected dated address controls

These are dated observations only; they do not prove uninterrupted occupancy or one-room succession.

- **13 September p.5:** optometrist advertisement — **612 Main St.**
- **13 September p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. Transfer & Storage — **Office 612 Main Street**.
- **20 September p.5:** optometrist advertisement — **612 Main St.**
- **20 September p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **27 September p.2:** Theroux Music House notice prints **519 Main Street, Oregon City**.
- **27 September p.5:** optometrist advertisement — **612 Main St.**
- **27 September p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **27 September p.8:** Jones Drug Co. advertisement directly prints **617 Main St. — Oregon City**.

The 519 and 617 observations are surrounding dated controls only. They do not establish uninterrupted occupancy, a legal succession, or a relationship to the target storefronts.

## Exact target-address result

Across these **24 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this September continuation.

The post-review text backstop produced an apparent **505** on **20 September p.2**, but scan/context review shows it is part of a bank condition total, **$505,899.28**, not a street address. Other numeric candidates likewise resolved to amounts/statistics rather than target addresses. The backstop also recovered the legitimate 519, 612, 617 and 619 Main controls above. No hidden target-address hit survived scan/context review.

This is a bounded coverage result for the three specified issues. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

September *Courier* coverage is now complete within the four-issue September inventory: **4 issues / 32 pages visually verified**. 1917 remains **IN PROGRESS**. October and later unsampled weekly issues still require page-by-page review, as do the other outstanding annual source classes/gaps, including the true **13 December 1917 Courier page 21** retrieval gap and the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap.
'''

if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 24/24 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **13, 20 and 27 September 1917 (8 pages each)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-09-13/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-september-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-september-unsampled/manifest.json`  
Retrieval commit: `8a3bee05860be735e2af968841050cbd2aca6a39`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete visual review confirms dated 519, 612, 617 and 619 Main controls. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. The apparent 505 hit on 20 September p.2 is part of a $505,899.28 bank total, not an address; no vacancy inference is made.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **24 page scans** for the 13, 20 and 27 September 1917 *Oregon City Courier* issues were visually reviewed.
- With the already reviewed 6 September sample, September now has **4 complete issues / 32 visually verified pages**.
- Across the non-overlapping monthly-sample and January–September continuation batches, the project now documents **42 complete tracked 1917 Courier issues / 340 visually verified pages**; this is not exhaustive annual coverage.
- Selected dated controls directly confirm **Theroux Music House at 519 Main** and **Jones Drug Co. at 617 Main** on 27 September, alongside recurring **612 Main** and **619 Main** controls.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the 24-page batch.
- The apparent 505 text hit on 20 September p.2 is visibly part of the bank total **$505,899.28**, not a street address.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count, visible dated address wording and false-positive classification; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible wording; no occupancy-continuity or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-09-13/ed-1/"
    type: "Primary newspaper page scans; visually verified 24/24 pages"
    date: "1917-09-13 through 1917-09-27"
    repository_file: "{CAPTURE_REL}"
    notes: "Complete remaining-September Courier visual review. Dated controls confirm Theroux at 519 Main and Jones Drug at 617 Main on 27 September, plus recurring 612/619 Main. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; the 20 September 505 hit is a bank total, not an address."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-09-13 through 1917-09-27"
    claims:
      - "All 24 page scans for the 13, 20 and 27 September 1917 Courier issues were visually reviewed."
      - "With the 6 September sample, September now has 4 complete issues / 32 visually verified pages."
      - "The non-overlapping monthly-sample and January-September batches now total 42 complete tracked issues / 340 visually verified pages; this is not exhaustive annual coverage."
      - "27 September directly confirms Theroux Music House at 519 Main and Jones Drug Co. at 617 Main, alongside recurring 612 Main and 619 Main controls."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the 24-page batch; the apparent 505 hit on 20 September p.2 is part of a $505,899.28 bank total, not an address."
    confidence: "Very High for the inspected-page count, visible dated wording and false-positive classification; no continuity or vacancy inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## September 13–27 continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **24/24 pages** of the remaining 13, 20 and 27 September *Courier* issues. Together with the already reviewed 6 September sample, **September Courier coverage is now 4 complete issues / 32 pages visually verified**.

Direct controls include **Theroux Music House, 519 Main** and **Jones Drug Co., 617 Main** on 27 September, alongside recurring **612 Main** and **619 Main**. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Text-layer checking was performed only after visual review; the apparent 505 hit on 20 September p.2 is a bank total, not an address.

Across the non-overlapping monthly sample plus January–September continuations, the documented progress count is now **42 complete tracked issues / 340 visually verified pages**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## September completion added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` completes visual review of the remaining September 13/20/27 *Courier* issues (**24/24 pages**). With September 6, September is now **4 complete issues / 32 pages visually verified**. The non-overlapping monthly-sample + January–September batches total **42 complete tracked issues / 340 visually verified pages**. September 27 directly confirms 519 Main for Theroux Music House and 617 Main for Jones Drug; no exact target 501/503/505/507/509/511 occupant was established. This remains partial annual coverage, not closeout certification. The true 13 December page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-15-29-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-april-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-may-10-31-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-june-14-28-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-july-12-26-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-august-09-30-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-september-13-27-visual-review-2026-09-05.md` | Structured monthly sample plus January–September continuations now give **42 complete tracked issues / 340 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February **4 / 36**; March **5 / 46**; April **4 / 32**; May **5 / 40**; June **4 / 32**; July **4 / 32**; August **5 / 32**; September **4 / 32**. Jan. 25 supplies direct 427 Main/corner Fifth; Jones Drug is direct at 617 Main by Mar. 15 and again Sep. 27; Sep. 27 also directly gives Theroux Music House at 519 Main. Surrounding exact controls do not establish a target 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk = f'''## {SOURCE_ID} / {EVIDENCE_ID} — remaining September 1917 Courier visual review
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120` | 13/20/27 September batch, **24/24 pages visually reviewed**. September totals 4 issues / 32 pages with the September 6 sample. Sep. 27 directly confirms Theroux at 519 Main and Jones Drug at 617 Main; recurring 612/619 controls. No exact 501/503/505/507/509/511 or new 427 occupant; 20 Sep. apparent 505 is a bank total, not an address. |'''
append_once("indexes/id-crosswalk.md", crosswalk)

log = f'''### 2026-09-05 — completed remaining September 1917 Courier visual review
<!-- {MARKER} -->
- Synced against current `main`; source/evidence IDs are allocated dynamically from the authoritative register maxima at runtime because parallel workflows remain active.
- Visually inspected **24/24 actual page scans** for 13, 20 and 27 September 1917. Preserved source retrieval commit: `8a3bee05860be735e2af968841050cbd2aca6a39`.
- With the already reviewed 6 September sample, September is now **4 complete issues / 32 visually verified pages**.
- 27 September p.2 directly confirms **Theroux Music House, 519 Main Street**; p.8 directly confirms **Jones Drug Co., 617 Main St.** Recurring controls also include 612 Main and 619 Main.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in these 24 pages.
- Post-review text checks produced an apparent 505 on 20 September p.2; scan/context review confirms it is part of the bank total $505,899.28, not a street address.
- Non-overlapping tracked 1917 progress is now **42 complete issues / 340 visually verified page images**. 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} remaining September 1917 review")
