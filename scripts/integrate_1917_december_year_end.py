from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 December Courier year-end continuation — 2026-09-05"
CAPTURE_REL = "evidence/source-captures/1917-courier-december-13-27-year-end-review-2026-09-05.md"
SOURCE_NAME = "Oregon City Courier, 13/20/27 December 1917 year-end visual-review batch"
EVIDENCE_NAME = "December 1917 review reaches Courier year end with one true-page retrieval gap"
RETRIEVAL_COMMIT = "b15d41d11cd0d5749db05f207111c5c38ead85d8"


def read(rel): return (ROOT / rel).read_text(encoding="utf-8")
def write(rel, text):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")
def append_once(rel, block):
    text = read(rel)
    if MARKER in text: return False
    write(rel, text.rstrip() + "\n\n" + block.strip() + "\n")
    return True

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"

capture_path = ROOT / CAPTURE_REL
if capture_path.exists():
    cap = read(CAPTURE_REL)
    sm = re.search(r"source `(S-\d{3})`", cap); em = re.search(r"evidence `(E-\d{3})`", cap)
    if not sm or not em: raise SystemExit("Existing December capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID = sm.group(1), em.group(1)

capture = f'''# 1917 Oregon City Courier — December year-end visual review

<!-- {MARKER} -->

Status: **YEAR-END COURIER ISSUE INVENTORY REACHED — December has 3 complete issues plus one 23/24-page partial issue; one true page remains a RETRIEVAL GAP. 1917 remains IN PROGRESS under the project-wide standard.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`.

Preserved originals: `newspapers/oregon-city-courier/1917-december-continuation/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Retrieval manifest: `newspapers/oregon-city-courier/1917-december-continuation/manifest.json`

## Scope and method

The already reviewed 6 December monthly-sample issue supplies 8 visually verified pages. A prior scan audit visually inspected all 24 files supplied under the 13 December issue record: sequences 1–20 and 22–24 are genuine 13 December pages, while sequence 21 visibly carries a **27 December 1917** header. Therefore the genuine 13 December state remains **23/24 pages visually verified + one retrieval conflict/gap**.

This continuation independently retrieved the year-end files again without stopping at interior gaps, confirmed the same sequence-21 conflict, and newly rendered and visually inspected every page of the **20 December (8/8)** and **27 December (8/8)** issues. Text extraction was used only after visual inspection as a backstop; scans control.

| Issue | Genuine page state | Visual status |
| --- | ---: | --- |
| 6 December 1917 | 8/8 | **VISUALLY VERIFIED** in monthly sample |
| 13 December 1917 | 23/24 | **23 GENUINE PAGES VISUALLY VERIFIED; true page 21 RETRIEVAL GAP** |
| 20 December 1917 | 8/8 | **VISUALLY VERIFIED 8/8** |
| 27 December 1917 | 8/8 | **VISUALLY VERIFIED 8/8** |

December therefore contains **3 complete issues plus one partial issue, with 47 genuine pages visually verified out of 48 expected pages**.

Across the year, the tracked *Courier* inventory now reaches every 1917 issue date: **52 issue dates total; 51 complete issues plus the 13 December 23/24-page partial issue; 435 genuine page images visually verified; one genuine page retrieval gap remains**. This is a Courier-title progress result, not project-wide `ONLINE COMPLETE` certification.

## Dated controls

- **13 December p.18:** optometrist advertisement — **612 Main Street**.
- **13 December p.23:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **20 December p.3:** Jones Drug Co. advertisement visibly says **Main Street / Oregon City** but does not print 617; it is not promoted as an exact-number observation.
- **20 December p.5:** optometrist advertisement — **612 Main Street**.
- **20 December p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.
- **27 December p.2:** Jones Drug Co. again visibly says **Main Street / Oregon City** without an exact street number.
- **27 December p.5:** optometrist advertisement — **612 Main Street**.
- **27 December p.7:** Electric Store — **Andresen Bldg., 619 Main St.**; Williams Bros. — **Office 612 Main Street**.

These are dated controls only and do not prove uninterrupted occupancy or target-storefront succession.

## Exact target-address result

Across the genuine December pages reviewed, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established, and no new exact 427 Main occupant was established.

The post-review text backstop produced apparent target-number strings inside financial/agricultural totals, including 507, 511, 427 and 505; context confirms they are **not street addresses**. Legitimate 612 and 619 Main controls were recovered. Jones Drug ads on 20 and 27 December were not silently converted into 617 Main observations because those dated ads do not print the number.

This is a bounded coverage result. It is **not** evidence that any target address was vacant, unused, demolished, unnumbered or absent.

## The 13 December page-21 gap

The 13 December front page identifies a **24-page** Christmas-shopping issue. The archive exposes sequence positions 1–24, but sequence 21's printed header says **Thursday, December 27, 1917**. Fresh recovery attempts against the archive's issue index, page HTML/OCR/PDF derivatives and ordinary web discovery reproduced the same misassociation and did not surface an alternate genuine page 21.

The correct classification remains **RETRIEVAL GAP**. The next route is another derivative, microfilm, or holding-institution assistance. Failure to recover this page is not negative evidence about 501/503/505.

## Effect on 1917 status

The *Courier* chronological pass has now reached **27 December 1917**, the final issue date of the year, with only the true 13 December page 21 unresolved at page level. **1917 remains IN PROGRESS** because the project-wide standard also requires certification of all other relevant online newspaper-title/page coverage and the unresolved Sohns & Woodbeck 1916–1917 Oregon City directory section. The annual exact-occupant questions for 503 and 505 therefore remain open.
'''
if not capture_path.exists(): write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — {SOURCE_NAME}
<!-- {MARKER} -->
Type: Primary newspaper page scans; year-end Courier review with one retrieval conflict.  
Publication: *Oregon City Courier*  
Issues: **13, 20 and 27 December 1917**, combined with the previously reviewed 6 December sample.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-12-13/ed-1/  
Preserved originals: `newspapers/oregon-city-courier/1917-december-continuation/`  
Retrieval commit: `{RETRIEVAL_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: 20 and 27 December are visually verified 8/8 each. Prior and fresh review agree that 13 December has 23 genuine pages while archive sequence 21 is a 27 December page; the true page 21 remains a retrieval gap. Annual Courier inventory reaches 52 issue dates: 51 complete issues + one 23/24 partial, 435 genuine pages visually verified. No exact target occupant was established.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — {EVIDENCE_NAME}
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper scans; year-end issue/page audit  
Claims:
- **20 and 27 December 1917 are visually verified 8/8 pages each.**
- The archive's 13 December sequence 21 is visibly dated 27 December; **23 genuine 13 December pages are visually verified and true page 21 remains a RETRIEVAL GAP**.
- December totals **3 complete issues plus one 23/24 partial issue, 47 genuine pages visually verified of 48 expected**.
- The tracked 1917 Courier inventory reaches all **52 issue dates: 51 complete issues + one partial, 435 genuine pages visually verified, one genuine-page gap**.
- Dated December controls include 612 and 619 Main; Jones Drug ads on 20 and 27 December print Main Street/Oregon City but no exact number.
- No defensible exact 501/503/505/507/509/511 or new 427 Main occupant was established in the genuine December pages reviewed.
Classification: **DOCUMENTED / DIRECT** for inspected pages, visible headers/address wording and the sequence-21 conflict; **RETRIEVAL GAP** for true 13 December page 21; **COVERAGE RESULT ONLY** for no target-number finding.  
Confidence: **Very High** for page counts and visible wording; no vacancy or continuity inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''\n\n  - id: {SOURCE_ID}\n    name: "{SOURCE_NAME}"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-12-13/ed-1/"\n    type: "Primary newspaper page scans; year-end visual review with retrieval gap"\n    date: "1917-12-13 through 1917-12-27"\n    repository_file: "{CAPTURE_REL}"\n    notes: "20/27 December visually verified 8/8 each; 13 December has 23 genuine pages visually verified but archive seq-21 is dated 27 December. Courier inventory reaches 52 issue dates, 51 complete + one 23/24 partial, 435 genuine pages. No exact target occupant established."\n    related_evidence: [{EVIDENCE_ID}]\n''' 
    write("database/sources.yml", sources + "\n")

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''\n\n  - id: {EVIDENCE_ID}\n    name: "{EVIDENCE_NAME}"\n    type: "Primary newspaper scans; year-end issue/page audit"\n    date: "1917-12-13 through 1917-12-27"\n    claims:\n      - "20 and 27 December 1917 are visually verified 8/8 pages each."\n      - "13 December has 23 genuine pages visually verified; archive sequence 21 is visibly dated 27 December and the true page remains a retrieval gap."\n      - "December has 3 complete issues plus one 23/24 partial issue, 47 genuine pages visually verified of 48 expected."\n      - "The tracked 1917 Courier inventory reaches all 52 issue dates: 51 complete issues plus one partial, 435 genuine pages visually verified, one genuine-page gap."\n      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established in the genuine December pages reviewed."\n    confidence: "Very High for page counts, visible headers/address wording and gap classification; no vacancy or continuity inference."\n    related_sources: [{SOURCE_ID}]\n'''
    write("database/evidence.yml", evidence + "\n")

review = f'''## December year-end continuation — 5 September 2026\n<!-- {MARKER} -->\n\n`{SOURCE_ID}` / `{EVIDENCE_ID}` reaches the final 1917 *Courier* issue date. Dec. 20 and 27 are **8/8 visually verified**. Dec. 13 remains **23 genuine pages verified + true page 21 retrieval gap** because archive sequence 21 is visibly dated Dec. 27. December therefore has **3 complete issues + one 23/24 partial, 47 genuine pages**. The annual Courier inventory is **52 issue dates; 51 complete + one partial; 435 genuine pages verified; one page gap**. No exact target occupant was established. 1917 remains **IN PROGRESS** under the wider relevant-title/source standard.'''
append_once("evidence/source-captures/1917-courier-review-start.md", review)

closeout = f'''## December year-end Courier continuation added 5 September 2026\n<!-- {MARKER} -->\n\n`{SOURCE_ID}` / `{EVIDENCE_ID}` carries the Courier audit through **27 December 1917**. Dec. 20 and 27 are 8/8 visually verified; Dec. 13 remains 23/24 genuine pages because archive sequence 21 is visibly a Dec. 27 page. The year-level Courier inventory now reaches **52 issue dates: 51 complete issues plus one partial; 435 genuine pages visually verified; one true-page retrieval gap**. No exact 501/503/505/507/509/511 occupant was established in the genuine December pages. **1917 remains IN PROGRESS** because full other-relevant-title/page certification and the Sohns & Woodbeck Oregon City directory section remain unresolved.'''
append_once("evidence/source-captures/1917-closeout.md", closeout)

append_once("evidence/source-captures/1917-courier-october-december-review.md", f'''## Year-end continuation — 5 September 2026\n<!-- {MARKER} -->\n\nThe later structured pass visually verifies all 8 pages of both 20 and 27 December. The 13 December conflict remains unchanged: sequences 1–20 and 22–24 are genuine, sequence 21 is dated 27 December, and the true page 21 remains a retrieval gap. The Courier audit now reaches the final 1917 issue date with 51 complete issues plus one 23/24 partial and 435 genuine pages visually verified.''')

year = read("registers/year-status.md").splitlines()
for i,line in enumerate(year):
    if line.startswith("| 1917 |"):
        year[i] = f"| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE_REL}` | *Courier* issue inventory now reaches all **52 1917 issue dates**: **51 complete issues plus 13 Dec at 23/24 genuine pages; 435 genuine pages visually verified; one true-page retrieval gap**. December has 3 complete issues + one partial. No exact 501/503/505/507/509/511 occupant was established by the genuine December pages. Project-wide ONLINE COMPLETE is not yet certified because other relevant-title/page coverage remains uncertified and the Sohns & Woodbeck Oregon City directory section remains unresolved. |"
        break
else: raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(year) + "\n")

append_once("indexes/id-crosswalk.md", f'''## {SOURCE_ID} / {EVIDENCE_ID} — December 1917 Courier year end\n<!-- {MARKER} -->\n\n| Record | Links | Notes |\n| --- | --- | --- |\n| `{SOURCE_ID}` / `{EVIDENCE_ID}` | 1917 annual audit; `S-134` / `E-120` | Dec. 20/27 8/8 each; Dec. 13 23 genuine pages + true-page-21 gap. Annual Courier: 52 issue dates, 51 complete + one partial, 435 genuine pages. No exact target occupant. |''')

append_once("registers/research-log.md", f'''### 2026-09-05 — carried 1917 Courier review through year end\n<!-- {MARKER} -->\n- Preserved gap-aware December retrieval in commit `{RETRIEVAL_COMMIT}`.\n- Visually inspected all 8 pages of both 20 and 27 December; prior scan-certified review supplies 23 genuine pages for 13 December.\n- Confirmed again that archive 13 December sequence 21 is visibly dated 27 December; ordinary alternate-derivative/web recovery did not surface the true page.\n- Courier annual inventory now reaches 52 issue dates: 51 complete + one 23/24 partial, 435 genuine pages visually verified, one retrieval gap.\n- December controls include 612 and 619 Main. Jones Drug ads on 20/27 December say Main Street but not 617. No exact 501/503/505/507/509/511 occupant was established.\n- 1917 remains IN PROGRESS under the project-wide standard because other relevant-title/page coverage is not certified and the Sohns & Woodbeck Oregon City directory section remains unresolved.''')

print(f"Integrated {SOURCE_ID} / {EVIDENCE_ID} December 1917 year-end review")
