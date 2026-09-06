from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise January visual review — 2026-09-06"
CAPTURE_REL = "evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md"
RETRIEVAL_COMMIT = "9b19733a9dc82ab617f0c461a23651a70e96e3fd"
INVENTORY_REL = "newspapers/oregon-city-enterprise/1917-issue-inventory/README.md"


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
    sm = re.search(r"source `(S-\d{3})`", cap)
    em = re.search(r"evidence `(E-\d{3})`", cap)
    if not sm or not em:
        raise SystemExit("Existing January Enterprise capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Enterprise — January 5, 12, 19 and 26 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 4 complete issues / 32 of 32 page scans reviewed. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-january/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Retrieval manifest: `newspapers/oregon-city-enterprise/1917-january/manifest.json`  
Annual issue/page inventory: `{INVENTORY_REL}`

## Scope and method

The repository now has a Friday-pattern inventory of the 1917 weekly *Oregon City Enterprise*: **52 Friday issues / 416 exposed page PDFs**, with no missing expected Friday issue URL. Every January issue was independently retrieved and each of its **32 actual page scans** was rendered and visually inspected page by page. Embedded/extracted text was searched only after visual inspection as a checking aid; the scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 5 January 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 12 January 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 19 January 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 26 January 1917 | 8 | **VISUALLY VERIFIED 8/8** |

Enterprise progress after this batch is therefore **4/52 issues and 32/416 exposed pages visually reviewed**. The Friday-pattern inventory must still be reconciled against the archive title calendar/index before final title certification so an irregular non-Friday issue is not excluded merely by pattern.

## Target-address result

Across the **32 January page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established. No new exact 427 Main occupant was established.

The post-review text backstop found no target-number candidate that survived context review. Apparent `Farr` matches refer to unrelated names or places, not the later 505 Main Farr business. Jones Drug references occur without a target-storefront connection. A 19 January county-expense page names **Roswell L. Holman** but supplies no target Main Street number and is not used to map Holman's Fifth-and-Main business to 501/503/505.

This is a bounded coverage result. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

The *Oregon City Enterprise* annual online audit has now begun under the exhaustive standard: **32/416 exposed pages visually reviewed** in four January issues. The *Courier* remains at 435 genuine visually verified pages with the true 13 December page 21 as a retrieval gap. **1917 remains IN PROGRESS** because 384 exposed Enterprise pages remain visually unreviewed, the Enterprise Friday inventory still requires title-calendar reconciliation, other online source-class closeout work remains, and the Sohns & Woodbeck 1916–1917 Oregon City directory section is unresolved.
'''
if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Enterprise, January 1917 complete-page visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 32/32 pages** on 6 September 2026.  
Publication: *Oregon City Enterprise*  
Issues: **5, 12, 19 and 26 January 1917 (8 pages each)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-01-05/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-january/`  
Manifest: `newspapers/oregon-city-enterprise/1917-january/manifest.json`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: All 32 January scans were visually reviewed before text backstop. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Farr-like text hits are unrelated; Roswell L. Holman appears in a county-expense context without a target street number. No vacancy inference is made.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — January 1917 Enterprise visual audit clears 32 pages without a target-address assignment
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **32 page scans** for the 5, 12, 19 and 26 January 1917 *Oregon City Enterprise* issues were visually reviewed.
- The 1917 Enterprise Friday-pattern inventory currently exposes **52 issues / 416 pages**; after this batch, **4 issues / 32 pages** are visually reviewed and **384 exposed pages remain**.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant, and no new exact 427 Main occupant, was established in the January batch.
- Farr-like text matches are unrelated to the later 505 Main Farr business; Roswell L. Holman is named in county-expense material without an exact target Main Street number.
Classification: **DOCUMENTED / DIRECT** for the inspected-page count; **COVERAGE RESULT ONLY** for the no-target-address finding.  
Confidence: **Very High** for the visual-review count; no occupancy-continuity or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Enterprise, January 1917 complete-page visual-review batch"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-01-05/ed-1/"
    type: "Primary newspaper page scans; visually verified 32/32 pages"
    date: "1917-01-05 through 1917-01-26"
    repository_file: "{CAPTURE_REL}"
    notes: "All four January Enterprise issues, 32 pages, visually reviewed. No exact 501/503/505/507/509/511 or new 427 Main occupant established."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "January 1917 Enterprise visual audit clears 32 pages without a target-address assignment"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-01-05 through 1917-01-26"
    claims:
      - "All 32 page scans for the 5, 12, 19 and 26 January 1917 Oregon City Enterprise issues were visually reviewed."
      - "The Enterprise Friday-pattern inventory exposes 52 issues / 416 pages; 4 issues / 32 pages are now visually reviewed and 384 exposed pages remain."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the January batch."
      - "Farr-like text matches are unrelated; Roswell L. Holman is named in county-expense material without a target Main Street number."
    confidence: "Very High for the visual-review count; no continuity or vacancy inference is made."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

closeout_block = f'''## Enterprise January audit added 6 September 2026
<!-- {MARKER} -->

The missing second local title has now been identified correctly as the weekly *Oregon City Enterprise* (`sn00063700`); the Historic Oregon Newspapers digitized *Morning Enterprise* run ends in 1913. The Friday-pattern 1917 Enterprise inventory exposes **52 issues / 416 pages**. `{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears all four January issues (**32/32 pages**), leaving **384 exposed Enterprise pages**. No exact target 501/503/505/507/509/511 or new 427 Main occupant was established in January. This is coverage only, not vacancy evidence. Enterprise title-calendar reconciliation and the remaining February–December scans are still required.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

year = read("registers/year-status.md")
lines = year.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-december-13-27-year-end-review-2026-09-05.md`; `evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md` | *Courier*: all 52 issue dates inventoried, 51 complete issues plus 13 Dec at 23/24 genuine pages, **435 genuine pages visually verified**, one true-page retrieval gap. *Oregon City Enterprise*: Friday-pattern inventory exposes **52 issues / 416 pages**; January **4 issues / 32 pages visually verified**, **384 exposed pages remain**, and title-calendar reconciliation is still required. No exact 501/503/505/507/509/511 occupant established in the Enterprise January batch. Other online source-class closeout and the Sohns & Woodbeck Oregon City directory section remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

idx = read("ARCHIVE_INDEX.md")
old = re.search(r"(?m)^- \*\*1917 — IN PROGRESS:\*\*.*$", idx)
if old:
    replacement = "- **1917 — IN PROGRESS:** *Courier* reaches all 52 issue dates with **435 genuine pages visually verified** and one true-page retrieval gap (13 Dec p21). *Oregon City Enterprise* Friday-pattern inventory exposes **52 issues / 416 pages**; January is now **32/416 visually reviewed**, leaving **384 exposed pages**, with title-calendar reconciliation still required. Sohns & Woodbeck 1916–17 Oregon City directory section also remains unresolved."
    idx = idx[:old.start()] + replacement + idx[old.end():]
    write("ARCHIVE_INDEX.md", idx)

log_block = f'''| 2026-09-06 | Began exhaustive 1917 Oregon City Enterprise visual audit | Corrected title availability: Historic Oregon Newspapers' digitized *Morning Enterprise* ends in 1913; the relevant second 1917 local title is the weekly *Oregon City Enterprise*. Built a Friday-pattern inventory of **52 issues / 416 exposed pages** and visually reviewed all four January issues, **32/32 scans**. No exact 501/503/505/507/509/511 or new 427 Main occupant established; false/irrelevant Farr-like matches and unnumbered Holman/Jones contexts were not promoted. | Continue February Enterprise page-by-page; reconcile Friday inventory against archive title calendar before title certification. |'''
append_once("registers/research-log.md", log_block)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID}")
