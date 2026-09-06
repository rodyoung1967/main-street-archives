from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_ID = "S-252"
EVIDENCE_ID = "E-226"
SOURCE_NAME = "Oregon City Courier, 8 March 1917 complete-page visual-review checkpoint"
EVIDENCE_NAME = "8 March 1917 Courier visually clears 10 pages and repeats selected downtown address anchors"
MARKER = "1917 March 8 Courier visual review — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md"


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

capture = r'''# 1917 Oregon City Courier — 8 March complete-issue visual review

<!-- 1917 March 8 Courier visual review — 2026-09-05 -->

Status: **VISUALLY VERIFIED — 1 complete issue / 10 of 10 page scans reviewed. 1917 remains IN PROGRESS.**

Archive IDs: source `S-252`; evidence `E-226`.

Preserved originals: `newspapers/oregon-city-courier/1917-march-unsampled/`  
Retrieval commit: `413f0499335e7d4c21093b928038b33175bc7b6f`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-march-unsampled/manifest.json`

## Scope and method

This checkpoint continues the first-issue-of-each-month sample (`S-134` / `E-120`) and the completed January and February continuations by reviewing the **8 March 1917** *Oregon City Courier* issue in full.

All **10 actual scanned page images** were rendered and visually inspected page by page. Text extraction was used only after visual review as a checking aid for exact-number strings; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 8 Mar. 1917 | 10 | **VISUALLY VERIFIED 10/10** |

Together with the already reviewed **1 March 1917** sample issue (8 pages), March currently has **2 complete Courier issues / 18 page images visually verified**. March 15, 22 and 29 remain pending in the retrieved batch.

Across the non-overlapping structured monthly sample plus the January, February and March-8 continuations, the project now has **19 complete tracked 1917 Courier issues / 158 page images visually verified**. This is a progress count only, not annual certification.

## Selected dated address anchors

These are dated observations only; they do not establish uninterrupted occupancy or one-room succession.

- **8 Mar. p.2:** Portland Railway Light & Power Co. Electric Store — **Andresen Bldg., 619 Main St.**
- **8 Mar. p.4:** R. L. Holman undertaking advertisement — **Fifth and Main St.**
- **8 Mar. p.7:** optometrist advertisement — **612 Main Street**.
- **8 Mar. p.8:** Williams Bros. Transfer & Storage — **Office 612 Main Street**; R. L. Holman again prints **Fifth and Main St.**
- **8 Mar. p.10:** R. L. Holman again prints **Fifth and Main St.**

Page 5 and page 6 are dominated by the delinquent-tax list; their many numbers are property/tax-list data and are not treated as storefront-address hits without explicit address wording.

## Exact target-address result

Across the **10 visually reviewed page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established in this issue either.

A post-review text-layer check likewise produced no defensible target-address hit. This is a bounded coverage result for the 8 March issue only. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

1917 remains **IN PROGRESS**. The next retrieved March issues still requiring page-by-page visual inspection are:

1. **15 March 1917 — 8 pages**;
2. **22 March 1917 — 8 pages**; and
3. **29 March 1917 — 12 pages**.

The true **13 December 1917 Courier page 21** retrieval gap and the **Sohns & Woodbeck 1916–1917 directory, Oregon City section** gap also remain unresolved.
'''
create_once(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 10/10 pages** on 5 September 2026.  
Publication: *Oregon City Courier*  
Issue: **8 March 1917 (10 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-03-08/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-march-unsampled/`  
Manifest: `newspapers/oregon-city-courier/1917-march-unsampled/manifest.json`  
Retrieval commit: `413f0499335e7d4c21093b928038b33175bc7b6f`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete visual review of the 8 March issue repeats 619 Main, 612 Main and Fifth/Main anchors. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; this is bounded coverage, not vacancy evidence.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review checkpoint  
Claims:
- All **10 page scans** for the 8 March 1917 *Oregon City Courier* issue were visually reviewed.
- With the already reviewed 1 March sample issue, March currently has **2 complete issues / 18 visually verified pages**; 15/22/29 March remain pending.
- Across the non-overlapping monthly-sample, January, February and March-8 batches, the project now documents **19 complete tracked issues / 158 visually verified pages**; this is not exhaustive annual coverage.
- 8 March p.2 directly repeats the Electric Store at **Andresen Building, 619 Main St.**
- 8 March pp.4, 8 and 10 directly repeat R. L. Holman at **Fifth and Main St.**
- 8 March p.7 directly prints an optometrist advertisement at **612 Main Street**; p.8 directly prints Williams Bros. Transfer & Storage at **Office 612 Main Street**.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the ten-page issue. This is bounded coverage only and is not vacancy, demolition or absence evidence.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count and printed dated address anchors; **COVERAGE RESULT ONLY** for the no-target-number finding.  
Confidence: **Very High** for the inspected-page count and visible address wording; no occupancy-continuity inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if SOURCE_ID not in sources:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "{SOURCE_NAME}"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-03-08/ed-1/"
    type: "Primary newspaper page scans; visually verified 10/10 pages"
    date: "1917-03-08"
    repository_file: "{CAPTURE_REL}"
    notes: "Preserved originals and manifest are under newspapers/oregon-city-courier/1917-march-unsampled/. Exact-number/intersection anchors repeat 619 Main, 612 Main and Fifth/Main; no exact 501/503/505/507/509/511 or new 427 Main occupant was established."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if EVIDENCE_ID not in evidence:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "{EVIDENCE_NAME}"
    type: "Primary newspaper page scans; complete-page visual-review checkpoint"
    date: "1917-03-08"
    claims:
      - "All 10 page scans for the 8 March 1917 Courier issue were visually reviewed."
      - "With the 1 March sample issue, March currently has 2 complete issues / 18 visually verified pages; 15/22/29 March remain pending."
      - "The non-overlapping monthly-sample, January, February and March-8 batches now total 19 complete tracked issues / 158 visually verified pages; this is not exhaustive annual coverage."
      - "Selected direct anchors repeat Electric Store at 619 Main, R. L. Holman at Fifth/Main, and two 612 Main advertisements."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the ten-page issue; the bounded no-hit result is not vacancy or absence evidence."
    confidence: "Very High for the inspected-page count and visible dated address wording; no continuity inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

review_block = f'''## March 8 continuation — 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears **10/10 pages** of the 8 March *Courier*. Together with the previously reviewed 1 March sample, **March currently has 2 complete issues / 18 pages visually verified**; 15, 22 and 29 March remain pending.

Selected direct repetitions include the Electric Store at **619 Main**, R. L. Holman at **Fifth/Main**, an optometrist at **612 Main**, and Williams Bros. Transfer & Storage at **612 Main**. No exact 501/503/505/507/509/511 or new 427 Main occupant was established; this bounded result is not vacancy evidence.

Across the non-overlapping monthly sample plus January, February and March-8 continuations, the documented progress count is now **19 complete tracked issues / 158 visually verified page images**. 1917 remains **IN PROGRESS**; see `{CAPTURE_REL}`.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review_block)

closeout_block = f'''## March 8 continuation added 5 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` adds complete visual review of the 8 March *Courier* issue (**10/10 pages**). Including the already sampled 1 March issue, March currently has **2 complete issues / 18 pages visually verified**; March 15, 22 and 29 remain pending. The structured non-overlapping monthly-sample + January + February + March-8 batches total **19 complete tracked issues / 158 visually verified pages**. This remains partial annual coverage, not a closeout certification. The 13 December true-page-21 and Sohns & Woodbeck Oregon City section gaps remain open, as does the rest of the annual relevant-title/page audit.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year_status = read("registers/year-status.md")
lines = year_status.splitlines()
changed = False
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`; `evidence/source-captures/1917-courier-january-11-25-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-february-08-22-visual-review-2026-09-05.md`; `evidence/source-captures/1917-courier-march-08-visual-review-2026-09-05.md` | Structured monthly sample plus January, February and the 8 March continuation now give **19 complete tracked issues / 158 page images visually verified** in those non-overlapping batches. January is **4 issues / 32 pages**; February is **4 issues / 36 pages**; March currently is **2 issues / 18 pages**, with 15/22/29 March pending. Jan. 25 adds direct 427 Main/corner Fifth and former Strebig Meat Market evidence; later batches repeat selected 619 Main, 108 Fifth, 612 Main and Fifth/Main controls but establish no target 501/503/505/507/509/511 occupant. This is still not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit remains unfinished. |"
        changed = True
        break
if not changed:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

crosswalk_block = f'''## {SOURCE_ID} / {EVIDENCE_ID} — 8 March 1917 visual-review checkpoint
<!-- {MARKER} -->

| Record | Links | Notes |
| --- | --- | --- |
| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120`; `S-247` / `E-221`; `S-248` / `E-222` | 8 Mar. complete issue, **10/10 pages visually reviewed**. Direct controls repeat 619 Main, 612 Main and Fifth/Main. No exact 501/503/505/507/509/511 or new 427 Main occupant established; no continuity or vacancy inference. |'''
append_once("indexes/id-crosswalk.md", crosswalk_block)

log_block = f'''### 2026-09-05 — continued exhaustive 1917 Courier review through 8 March
<!-- {MARKER} -->
- Synced against current `main` after parallel Grisham/Wiitanen work consumed `S-249`–`S-251` / `E-223`–`E-225`; assigned this checkpoint the next free IDs `{SOURCE_ID}` / `{EVIDENCE_ID}`.
- Visually inspected **10/10 actual page scans** for 8 March 1917. Preserved source batch retrieval commit: `413f0499335e7d4c21093b928038b33175bc7b6f`.
- With the previously reviewed 1 March sample, March currently has **2 complete issues / 18 visually verified pages**.
- Selected dated controls: Electric Store / Andresen Building **619 Main** (p.2); R. L. Holman **Fifth/Main** (pp.4, 8, 10); optometrist **612 Main** (p.7); Williams Bros. Transfer & Storage **612 Main** (p.8).
- Pages 5–6 are delinquent-tax-list pages; numeric entries were not misclassified as storefront addresses.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the issue. This is bounded coverage only, not vacancy/non-use evidence.
- Documented non-overlapping 1917 progress is now **19 complete tracked issues / 158 visually verified page images**. March 15/22/29 remain pending; 1917 remains **IN PROGRESS**.'''
append_once("registers/research-log.md", log_block)

print("Integrated S-252 / E-226 March 8 1917 visual checkpoint")
