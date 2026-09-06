from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise February visual review — 2026-09-06"
CAPTURE_REL = "evidence/source-captures/1917-enterprise-february-02-23-visual-review-2026-09-06.md"
FARR_GUARD_REL = "evidence/source-captures/1922-farr-brothers-identity-clarification-2026-09-03.md"


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

manifest_rel = "newspapers/oregon-city-enterprise/1917-february/manifest.json"
if not (ROOT / manifest_rel).exists():
    raise SystemExit("February preserved manifest is not present on current checkout")
RETRIEVAL_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", manifest_rel], cwd=ROOT, text=True
).strip()
if not RETRIEVAL_COMMIT:
    raise SystemExit("Could not determine February retrieval commit")

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"

capture_path = ROOT / CAPTURE_REL
if capture_path.exists():
    cap = read(CAPTURE_REL)
    sm = re.search(r"source `(S-\d{3})`", cap)
    em = re.search(r"evidence `(E-\d{3})`", cap)
    if not sm or not em:
        raise SystemExit("Existing February Enterprise capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Enterprise — February 2, 9, 16 and 23 complete-issue visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 4 complete issues / 34 of 34 page scans reviewed. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-february/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Retrieval manifest: `{manifest_rel}`  
Annual issue/page inventory: `newspapers/oregon-city-enterprise/1917-issue-inventory/README.md`

## Scope and method

All **34 actual page scans** for the four February *Oregon City Enterprise* issues were rendered and visually inspected page by page. The 16 February issue is correctly treated as a **10-page issue**, not silently normalized to the usual eight pages. Embedded/extracted text was searched only after visual inspection as a backstop; scans control.

| Issue | Page images | Visual status |
| --- | ---: | --- |
| 2 February 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 9 February 1917 | 8 | **VISUALLY VERIFIED 8/8** |
| 16 February 1917 | 10 | **VISUALLY VERIFIED 10/10** |
| 23 February 1917 | 8 | **VISUALLY VERIFIED 8/8** |

With January's previously integrated 32 pages, Enterprise progress becomes **8/52 Friday issues and 66/416 exposed pages visually reviewed**, leaving **350 exposed pages**. The Friday-pattern inventory still requires archive-calendar reconciliation before final title certification.

## Dated controls and Farr identity guard

- **2 February p.5:** optometrist advertisement visually prints **612 Main St., Oregon City**.
- **16 February p.5:** the optometrist advertisement again visually prints **612 Main St., Oregon City**.
- **16 February p.6:** the county-court expenditure list includes **Farr Bros.** among county-poor suppliers, with named recipient/account contexts. This is direct evidence that a local Farr Brothers business was transacting with the county in 1917, but it supplies no Main Street target address.
- **16 February p.8:** the delinquent-tax list visibly names **Annis L. Farr, Oregon City**. The tax-list appearance is a person/property context only and is not a 505 business observation.
- The repository already separates **Farr Brothers**, the Clarence/Arthur Louis Farr grocery/meat business on Seventh Street, from the later **Edwin F. and Alice Farr / Farr's Pool Hall at 505 Main** question; see `{FARR_GUARD_REL}`. These February surname/business observations therefore **must not be merged with Edwin F. Farr or used to move Farr's Pool Hall back to 1917** without independent bridging evidence.

## Exact target-address result

Across these **34 February page scans**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established and no new exact 427 Main occupant was established.

The text backstop recovered no target-number candidate. It did recover Farr/Farr Brothers occurrences, but scan and repository context classify those as the separate Seventh Street Farr-family business/taxpayer contexts described above rather than evidence for the later 505 pool hall.

This is a bounded coverage result. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## Effect on 1917 status

The *Oregon City Enterprise* exhaustive pass now has **66/416 exposed pages visually reviewed** in eight January-February issues, leaving **350 exposed pages**. **1917 remains IN PROGRESS** because March-December Enterprise visual work, Enterprise title-calendar reconciliation, other online source-class closeout work, the true 13 December Courier page 21 retrieval gap, and the Sohns & Woodbeck 1916–1917 Oregon City directory section remain unresolved.
'''
if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Enterprise, February 1917 complete-page visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 34/34 pages** on 6 September 2026.  
Publication: *Oregon City Enterprise*  
Issues: **2, 9, 16 and 23 February 1917 (8, 8, 10 and 8 pages)**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-02-02/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-february/`  
Manifest: `{manifest_rel}`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Complete February scan review. 612 Main optometrist controls recur on 2 and 16 Feb. Farr Bros appears in county-poor expenditures and Annis L. Farr in the delinquent-tax list, but existing identity evidence separates the Seventh Street Farr Brothers grocery/meat business from Edwin/Alice Farr's later 505 pool-hall question. No exact target address was established.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — February 1917 Enterprise visual audit clears 34 pages and reinforces the Farr identity guard
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans; complete-page visual-review batch  
Claims:
- All **34 page scans** for the 2, 9, 16 and 23 February 1917 *Oregon City Enterprise* issues were visually reviewed; 16 February is a 10-page issue.
- Enterprise cumulative coverage is now **66/416 exposed pages** across eight January-February issues; **350 exposed pages remain**.
- **612 Main St.** is directly visible in optometrist advertisements on 2 and 16 February.
- **Farr Bros.** appears in the 16 February county-poor expenditure list and **Annis L. Farr, Oregon City** appears in the 16 February delinquent-tax list, but neither observation supplies a target Main Street address or bridges to Edwin F. Farr.
- Existing Farr identity control places the Farr Brothers grocery/meat business on Seventh Street; these observations are not evidence that Farr's Pool Hall operated at 505 Main in 1917.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact 427 Main occupant was established.
Classification: **DOCUMENTED / DIRECT** for scan counts, 612 wording, Farr Bros county-account wording and Annis L. Farr tax-list wording; **IDENTITY GUARD / NO-MERGE** for their relation to later 505 Farr history; **COVERAGE RESULT ONLY** for the no-target-address finding.  
Confidence: **Very High** for the visible dated wording; no continuity or vacancy inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Enterprise, February 1917 complete-page visual-review batch"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-02-02/ed-1/"
    type: "Primary newspaper page scans; visually verified 34/34 pages"
    date: "1917-02-02 through 1917-02-23"
    repository_file: "{CAPTURE_REL}"
    notes: "February Enterprise complete: 612 Main controls plus Farr Bros county-poor and Annis L. Farr tax contexts. Existing identity guard keeps these separate from the later Edwin/Alice Farr 505 pool-hall history."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "February 1917 Enterprise visual audit clears 34 pages and reinforces the Farr identity guard"
    type: "Primary newspaper page scans; complete-page visual-review batch"
    date: "1917-02-02 through 1917-02-23"
    claims:
      - "All 34 page scans for the four February Enterprise issues were visually reviewed; 16 February has 10 pages."
      - "Enterprise cumulative coverage is 66/416 exposed pages; 350 remain."
      - "612 Main St. is directly visible in optometrist advertisements on 2 and 16 February."
      - "Farr Bros appears in county-poor expenditures and Annis L. Farr in a delinquent-tax list; neither supplies a target Main address or an identity bridge to Edwin F. Farr."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established."
    confidence: "Very High for visible dated wording; Farr surname/business observations remain explicitly separated from later 505 history."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

closeout = f'''## Enterprise February audit added 6 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually clears all four February *Oregon City Enterprise* issues (**34/34 pages**, including the 10-page 16 February issue). Enterprise cumulative coverage is now **66/416 exposed pages**, leaving **350**. Direct 612 Main controls recur. Farr Bros county-poor and Annis L. Farr tax-list observations are retained with the existing no-merge guard: the Farr Brothers grocery/meat firm is a separate Seventh Street business and is not evidence that Edwin/Alice Farr's later 505 pool hall existed in 1917. No exact target 501/503/505/507/509/511 occupant was established.'''
append_once("evidence/source-captures/1917-closeout.md", closeout)

year = read("registers/year-status.md")
lines = year.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = "| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-december-13-27-year-end-review-2026-09-05.md`; `evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md`; `evidence/source-captures/1917-enterprise-february-02-23-visual-review-2026-09-06.md` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, one true-page retrieval gap. *Oregon City Enterprise*: Friday-pattern inventory exposes **52 issues / 416 pages**; January-February **8 issues / 66 pages visually verified**, **350 exposed pages remain**, and title-calendar reconciliation is still required. February adds 612 Main controls plus Farr identity-guard context but no target-address occupant. Other online source-class closeout and the Sohns & Woodbeck Oregon City directory section remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

idx = read("ARCHIVE_INDEX.md")
m = re.search(r"(?m)^- \*\*1917 — IN PROGRESS:\*\*.*$", idx)
if m:
    repl = "- **1917 — IN PROGRESS:** *Courier* reaches all 52 issue dates with **435 genuine pages visually verified** and one true-page retrieval gap. *Oregon City Enterprise* Friday-pattern inventory exposes **52 issues / 416 pages**; January-February are now **66/416 visually reviewed**, leaving **350 exposed pages**, with title-calendar reconciliation still required. February Farr Bros/Annis L. Farr observations are explicitly separated from the later 505 Farr pool-hall identity. Sohns & Woodbeck 1916–17 Oregon City directory section remains unresolved."
    idx = idx[:m.start()] + repl + idx[m.end():]
    write("ARCHIVE_INDEX.md", idx)

log = f'''| 2026-09-06 | Completed February 1917 Oregon City Enterprise visual batch | Visually reviewed **34/34 scans** for 2/9/16/23 February; Enterprise cumulative **66/416**. 612 Main optometrist controls recur. Farr Bros appears in county-poor expenditures and Annis L. Farr in the tax list; existing Farr identity control prevents merging the Seventh Street Farr Brothers grocery/meat firm with Edwin/Alice Farr's later 505 pool hall. No target-number occupant established. | Continue March Enterprise; preserve no-merge Farr identity discipline. |'''
append_once("registers/research-log.md", log)

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID}; retrieval {RETRIEVAL_COMMIT}")
