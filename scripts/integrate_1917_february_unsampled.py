from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_ID = "S-248"
EVIDENCE_ID = "E-222"
SOURCE_NAME = "Oregon City Courier, 8/15/22 February 1917 complete-page visual-review batch"
EVIDENCE_NAME = "February 1917 continuation visually clears 28 pages and repeats selected downtown address anchors"
MARKER = "1917 February unsampled Courier visual review — 2026-09-05"


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


def create_once(rel, content):
    p = ROOT / rel
    if p.exists():
        existing = p.read_text(encoding="utf-8")
        if MARKER not in existing:
            raise SystemExit(f"{rel} exists without expected marker")
        return False
    write(rel, content)
    return True


for rel, ident in [
    ("evidence/source-register.md", SOURCE_ID),
    ("evidence/evidence-register.md", EVIDENCE_ID),
]:
    text = read(rel)
    if ident in text and MARKER not in text:
        raise SystemExit(f"{ident} already appears in {rel}; stop rather than reuse/renumber")

capture_rel = "evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md"
capture = r'''# 1917 Oregon City Courier — February 8, 15 and 22 unsampled issue visual review

<!-- 1917 February unsampled Courier visual review — 2026-09-05 -->

Status: **VISUALLY VERIFIED — 3 complete issues / 28 of 28 page scans reviewed. 1917 remains IN PROGRESS.**

Archive IDs: source `S-248`; evidence `E-222`.

Preserved originals: `newspapers/oregon-city-courier/1917-february-unsampled/`  
Retrieval commit: `a89ae39e96f8094e7556a0c0605b2093c7687491`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-february-unsampled/manifest.json`

## Scope and method

This pass continues the first-issue-of-each-month sample (`S-134` / `E-120`) and the completed January continuation (`S-247` / `E-221`) by reviewing every remaining February weekly *Oregon City Courier* issue: **8 February, 15 February and 22 February 1917**.

The actual page PDFs were retrieved from Historic Oregon Newspapers, preserved with SHA-256 hashes, rendered at readable resolution, and visually inspected page by page. Text extraction/OCR was used only after visual inspection as a discovery and checking aid.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 8 Feb. 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 15 Feb. 1917 | 10 | **VISUALLY VERIFIED 10/10** |
| 22 Feb. 1917 | 10 | **VISUALLY VERIFIED 10/10** |

Together with the already reviewed **1 February 1917** sample issue (8 pages), February now has **4 complete Courier issues / 36 page images visually reviewed**.

Across the non-overlapping structured monthly sample plus the January and February continuations, the project now has **18 complete tracked 1917 Courier issues / 148 page images visually verified**. That count is a progress measure for those documented batches only; it is not exhaustive annual certification.

## Selected dated address anchors

These are dated observations only. They do not prove uninterrupted occupancy or one-room succession.

| Date/page | Visible address evidence |
| --- | --- |
| 8 Feb. p.2 | Portland Railway Light & Power Co. **Electric Store — Andresen Bldg., 619 Main St.** |
| 8 Feb. p.4 | **Scripture & May — 108 Fifth St.** |
| 8 Feb. p.6 | **Williams Bros. Transfer & Storage — Office 612 Main Street** |
| 15 Feb. p.2 | Electric Store — **Andresen Bldg., 619 Main St.** |
| 15 Feb. p.8 | Williams Bros. Transfer & Storage — **Office 612 Main Street** |
| 22 Feb. p.2 | Electric Store — **Andresen Bldg., 619 Main St.** |
| 22 Feb. p.8 | Williams Bros. Transfer & Storage — **Office 612 Main Street** |

R. L. Holman's **Fifth and Main** undertaking advertising also recurs during this batch, consistent with the already established 1917 intersection control. These repeated advertisements strengthen date-specific observations but are not treated as proof that any business occupied the same room continuously between issues.

## Exact target-address result

Across these **28 newly reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was found in this February continuation either.

This is a bounded coverage result for the three specified February issues. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered, or absent from the city.

## Effect on 1917 status

1917 remains **IN PROGRESS**. The February continuation closes the remaining *Courier* issue/page gap for that month within the title, but annual certification still requires the unreviewed 1917 *Courier* issues outside the completed batches, the full relevant-title/source-class audit, and resolution or explicit retention of the known manual/retrieval gaps. In particular:

1. the true **13 December 1917 Courier page 21** remains unrecovered;
2. the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** remains uninspected; and
3. the remaining 1917 relevant newspaper issues/pages still require visual review.
'''
create_once(capture_rel, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 28/28 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issues: **8 February 1917 (8 pages); 15 February 1917 (10 pages); 22 February 1917 (10 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-02-08/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-february-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-february-unsampled/manifest.json`  
Retrieval commit: `a89ae39e96f8094e7556a0c0605b2093c7687491`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{capture_rel}`.  
Notes: This completes the three February issues not already represented by the 1 February monthly sample. Selected visible anchors include 619 Main, 108 Fifth, and 612 Main. No exact 501/503/505/507/509/511 Main occupant was established in this bounded batch; silence is not vacancy evidence.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **28 page scans** for the 8, 15 and 22 February 1917 *Oregon City Courier* issues were visually reviewed.
- With the already reviewed 1 February sample issue, February now has **4 complete issues / 36 pages visually verified**.
- Across the non-overlapping monthly-sample, January-continuation and February-continuation batches, the project now documents **18 complete tracked issues / 148 page images visually verified**; this is not exhaustive annual coverage.
- 8 February p.2 directly repeats the Electric Store at **Andresen Building, 619 Main St.**; 15 and 22 February p.2 repeat the same exact-number anchor.
- 8 February p.4 directly repeats **Scripture & May, 108 Fifth St.**
- 8 February p.6 directly prints **Williams Bros. Transfer & Storage, Office 612 Main Street**; 15 and 22 February p.8 repeat that exact-number anchor.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established in these 28 pages. This is bounded coverage only and is not evidence of vacancy, non-use, demolition or absence.
Classification: **DOCUMENTED / DIRECT** for the visual-review count and the printed dated address anchors; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible address wording; no occupancy-continuity inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if SOURCE_ID not in sources:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-02-08/ed-1/"
    type: "Primary newspaper page scans; visually verified 28/28 pages"
    date: "1917-02-08 through 1917-02-22"
    repository_file: "{capture_rel}"
    notes: "Preserved originals and manifest are under newspapers/oregon-city-courier/1917-february-unsampled/. Selected exact-number anchors repeat 619 Main, 108 Fifth and 612 Main; no exact 501/503/505/507/509/511 Main occupant was established in the bounded batch."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if EVIDENCE_ID not in evidence:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-02-08 through 1917-02-22"
    claims:
      - "All 28 page scans for the 8, 15 and 22 February 1917 Courier issues were visually reviewed."
      - "With the 1 February sample issue, February now has 4 complete issues / 36 visually verified pages."
      - "The non-overlapping monthly-sample, January-continuation and February-continuation batches now total 18 complete tracked issues / 148 visually verified pages; this is not exhaustive annual coverage."
      - "Selected direct anchors repeat Electric Store at 619 Main, Scripture & May at 108 Fifth, and Williams Bros. Transfer & Storage at 612 Main."
      - "No exact 501/503/505/507/509/511 Main occupant was established in these 28 pages; the bounded no-hit result is not vacancy or absence evidence."
    confidence: "Very High for the inspected-page count and visible dated address wording; no continuity inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## February 8–22 exhaustive continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears all **28/28 pages** of the remaining 8, 15 and 22 February *Courier* issues. Together with the previously reviewed 1 February sample, **February Courier coverage is now 4 complete issues / 36 pages visually verified**.

Selected exact-number repetitions include the Electric Store at **619 Main**, Scripture & May at **108 Fifth**, and Williams Bros. Transfer & Storage at **612 Main**. No exact 501/503/505/507/509/511 occupant was established in the 28-page continuation; this bounded result is not vacancy evidence.

Across the non-overlapping monthly sample plus January and February continuations, the documented progress count is now **18 complete tracked issues / 148 visually verified page images**. 1917 remains **IN PROGRESS**; see `{capture_rel}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## February continuation added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` adds complete visual review of the 8, 15 and 22 February *Courier* issues (**28/28 pages**). Including the already sampled 1 February issue, February is now **4 complete issues / 36 pages visually verified**. The structured non-overlapping monthly-sample + January + February batches total **18 complete tracked issues / 148 visually verified pages**. This remains partial annual coverage, not a closeout certification. The 13 December true-page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
changed = False
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md` | Structured monthly sample plus January and February continuations now give **18 complete tracked issues / 148 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February is **4 issues / 36 pages**. Jan. 25 adds direct 427 Main/corner Fifth and former Strebig Meat Market evidence; February repeats selected 619 Main, 108 Fifth and 612 Main anchors but establishes no target 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        changed = True
        break
if not changed:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk_block = f'''## {SOURCE_ID} / {EVIDENCE_ID} — February 1917 visual-review continuation
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120`; `S-247` / `E-221` | 8/15/22 Feb. complete-page batch, **28/28 pages visually reviewed**. Selected direct anchors repeat 619 Main, 108 Fifth and 612 Main. No exact 501/503/505/507/509/511 occupant established; no continuity or vacancy inference. |'''
append_once("indexes/id-crosswalk.md", crosswalk_block)

log_block = f'''### 2026-09-05 — continued exhaustive 1917 Courier review through remaining February issues
<!-- {MARKER} -->
- Preserved and visually inspected **28/28 actual page scans** for 8, 15 and 22 February 1917 (`{SOURCE_ID}`). Retrieval commit: `a89ae39e96f8094e7556a0c0605b2093c7687491`.
- With the previously reviewed 1 February sample, February is now **4 complete issues / 36 pages visually verified**.
- Selected dated controls: Electric Store / Andresen Building **619 Main** (8/15/22 Feb. p.2); Scripture & May **108 Fifth** (8 Feb. p.4); Williams Bros. Transfer & Storage **612 Main** (8 Feb. p.6; 15/22 Feb. p.8).
- No exact 501/503/505/507/509/511 Main occupant was established in these 28 pages. This is bounded coverage only, not vacancy/non-use evidence.
- Non-overlapping monthly sample + January + February continuation progress is now **18 complete tracked issues / 148 visually verified pages**.
- 1917 remains **IN PROGRESS**; true 13 Dec p21, Sohns & Woodbeck Oregon City section, and remaining annual relevant-title/page audit stay open.'''
append_once("registers/research-log.md", log_block)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID}")
