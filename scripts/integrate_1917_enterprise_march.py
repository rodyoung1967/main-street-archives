from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise March visual review and page-5 gap — 2026-09-06"
CAPTURE_REL = "evidence/source-captures/1917-enterprise-march-02-30-visual-review-2026-09-06.md"
MANIFEST_REL = "newspapers/oregon-city-enterprise/1917-march/manifest.json"
RECOVERY_REL = "newspapers/oregon-city-enterprise/1917-march/recovery-march16-page5/recovery-manifest.json"
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


for rel in (MANIFEST_REL, RECOVERY_REL):
    if not (ROOT / rel).exists():
        raise SystemExit(f"Required preserved file missing: {rel}")

RETRIEVAL_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()
RECOVERY_COMMIT = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", RECOVERY_REL], cwd=ROOT, text=True
).strip()
if not RETRIEVAL_COMMIT or not RECOVERY_COMMIT:
    raise SystemExit("Could not determine March retrieval/recovery commit")

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]
if not source_nums or not evidence_nums:
    raise SystemExit("Could not determine current source/evidence maxima")
SOURCE_ID = f"S-{max(source_nums)+1:03d}"
EVIDENCE_ID = f"E-{max(evidence_nums)+1:03d}"

manual_text = read("MANUAL-FOLLOWUP.md")
manual_nums = [int(x) for x in re.findall(r"\bMF-(\d{3})\b", manual_text)]
if not manual_nums:
    raise SystemExit("Could not determine current manual-followup maximum")
MANUAL_ID = f"MF-{max(manual_nums)+1:03d}"

capture_path = ROOT / CAPTURE_REL
if capture_path.exists():
    cap = read(CAPTURE_REL)
    sm = re.search(r"source `(S-\d{3})`", cap)
    em = re.search(r"evidence `(E-\d{3})`", cap)
    mm = re.search(r"manual callout `(MF-\d{3})`", cap)
    if not sm or not em or not mm:
        raise SystemExit("Existing March Enterprise capture lacks recoverable IDs")
    SOURCE_ID, EVIDENCE_ID, MANUAL_ID = sm.group(1), em.group(1), mm.group(1)

capture = f'''# 1917 Oregon City Enterprise — March 2, 9, 16, 23 and 30 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 39 genuine intended-date pages across five March issue dates; 2/9/23/30 March are complete, 16 March is 7/8 genuine with true page 5 a RETRIEVAL GAP. Enterprise annual visual audit remains IN PROGRESS.**

Archive IDs: source `{SOURCE_ID}`; evidence `{EVIDENCE_ID}`; manual callout `{MANUAL_ID}`.

Preserved March originals: `newspapers/oregon-city-enterprise/1917-march/`  
Original retrieval commit: `{RETRIEVAL_COMMIT}`  
Original manifest: `{MANIFEST_REL}`  
Recovery audit: `{RECOVERY_REL}`  
Recovery-audit commit: `{RECOVERY_COMMIT}`  
Annual issue/page inventory: `newspapers/oregon-city-enterprise/1917-issue-inventory/README.md`

## Scope and scan-first method

The archive exposes five Friday issue buckets in March 1917, eight PDF slots apiece. All **40 archive-supplied page files** were rendered and visually inspected. Printed dates were then audited page by page rather than trusting the archive issue metadata.

That audit discovered a material archive association error: the file exposed as **16 March, sequence 5 / page 5** visibly prints **“OREGON CITY ENTERPRISE, FRIDAY, MARCH 23, 1917”** and **“Page 5.”** It therefore cannot count as the true 16 March page 5.

The misassociated scan is also **not the same file** as the normal 23 March sequence-5 scan. Both visibly print 23 March and Page 5, but they are distinct scans/content variants. The 16 March slot is therefore classified as a misassociated 23 March page-5 variant rather than silently deduplicated or reassigned as the missing 16 March page.

| Archive issue bucket | Exposed slots | Genuine matching-date pages | Status |
| --- | ---: | ---: | --- |
| 2 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 9 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |
| 16 March 1917 | 8 | 7 | **PARTIAL 7/8 — true page 5 RETRIEVAL GAP** |
| 23 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8**, plus the separate misassociated 23 March Page-5 variant in the 16 March bucket |
| 30 March 1917 | 8 | 8 | **VISUALLY VERIFIED 8/8** |

Thus **40/40 exposed archive slots were visually inspected**, but only **39 are genuine intended-date March issue pages**. With January-February's 66 genuine pages, Enterprise progress becomes **105 genuine intended-date pages visually verified**. **310 later exposed April-December pages remain visually unreviewed**, and the true 16 March page 5 remains a separate retrieval gap. Do not convert the bad slot into 40/40 genuine March coverage.

## Recovery attempts for true 16 March page 5

The dedicated recovery audit tested independent derivatives and alternate routes before classifying the gap:

- Oregon Historic Newspapers PDF, JP2, OCR text, OCR XML, RDF and page HTML for the 16 March sequence-5 object all resolve to/described the same underlying scan that visibly prints **23 March**.
- The issue metadata exposes exactly eight source-image objects for the 16 March edition; the bad object occupies the fifth slot. No ninth source image is exposed.
- Alternate edition paths `ed-2` through `ed-4` were probed and did not expose a replacement page.
- Library of Congress / Chronicling America routes and LOC JSON searches did not expose a second usable copy of the missing page.
- The normal 23 March page 5 was retrieved separately and is a different scan from the misassociated 23 March variant.

Reasonable online recovery has therefore been attempted. The true **16 March 1917 Enterprise page 5** is retained as **RETRIEVAL GAP / MANUAL CALLOUT `{MANUAL_ID}`**, never as negative evidence.

## Dated context and identity discipline

Across the genuine March pages, the scan/text review found local context including Holman, Jones Drug and William Andresen references, but no new exact target-street-number observation for those references. Courier evidence already provides stronger dated exact-address controls where applicable, so the unnumbered Enterprise references do not create a new business-address chronology entry.

The misassociated 23 March Page-5 variant contains a local report that animals were sold to **Farr Brothers**. That wording belongs to the **23 March** scan variant, not 16 March. It supplies no 505 Main address and does not bridge the separate Seventh Street Farr Brothers grocery/meat business to **Edwin F. Farr / Alice Farr / Farr's Pool Hall at 505 Main**. Existing no-merge control remains in `{FARR_GUARD_REL}`.

## Exact target-address result

Across the **39 genuine intended-date March pages actually recovered and visually reviewed**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant was established and no new exact 427 Main occupant was established.

This statement deliberately excludes the unrecovered true 16 March page 5. The missing page means the March source class cannot be used to claim complete no-hit coverage for 16 March. Nothing here is evidence that a target storefront was vacant, unused, demolished, unnumbered or absent.

## Cross-record propagation audit

The following current authoritative entity/chronology records were reviewed against this batch:

- `buildings/503-main.md`
- `buildings/505-main.md`
- `timelines/503-main.md`
- `timelines/505-main.md`
- `businesses/farrs-pool-hall.md`
- `people/profiles/edwin-f-farr.md`
- `people/profiles/alice-farr.md`
- `evidence/open-questions.md`
- `evidence/research-leads.md`
- `registers/business-timeline.md`
- `timeline.md`

**Propagation decision:** the batch changes annual coverage, retrieval-gap, and source/evidence records, but establishes **no new 503/505 occupant, business operation, property ownership, building event, or Edwin/Alice Farr identity bridge**. Therefore no fabricated 1917 event is added to the 503/505 building/business/person timelines. The open 1917 occupancy question and research lead are updated with the new page gap and coverage state instead.

## Effect on 1917 status

1917 remains **IN PROGRESS**. Enterprise now has **105 genuine intended-date pages visually verified**, one known March 16 page-5 retrieval gap, and **310 later exposed April-December pages** still requiring page-by-page visual review. The Friday-pattern inventory still requires title-calendar reconciliation. Existing 1917 blockers also remain: the true 13 December *Courier* page 21 retrieval gap, the Sohns & Woodbeck 1916–1917 Oregon City directory section, and other online-source-class closeout work.
'''
if not capture_path.exists():
    write(CAPTURE_REL, capture)

source_block = f'''## {SOURCE_ID} — Oregon City Enterprise, March 1917 scan-first visual-review batch with archive page-association conflict
<!-- {MARKER} -->
Type: Primary newspaper page scans; **40/40 exposed archive slots visually inspected; 39 genuine intended-date pages recovered** on 6 September 2026.  
Publication: *Oregon City Enterprise*  
Issue dates: **2, 9, 16, 23 and 30 March 1917**.  
Representative archive URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-03-16/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-march/`  
Manifest: `{MANIFEST_REL}`  
Original retrieval commit: `{RETRIEVAL_COMMIT}`  
Recovery manifest: `{RECOVERY_REL}`  
Recovery commit: `{RECOVERY_COMMIT}`  
Related evidence: `{EVIDENCE_ID}`.  
Manual callout: `{MANUAL_ID}`.  
Capture: `{CAPTURE_REL}`.  
Notes: Visual date audit shows 16 March seq-5 is actually a distinct 23 March Page-5 variant. True 16 March page 5 remains unrecovered after derivative/alternate-edition/LOC recovery attempts. No exact 501/503/505/507/509/511 occupant was established on the 39 genuine recovered pages; no vacancy inference is made.'''
append_once("evidence/source-register.md", source_block)

evidence_block = f'''## {EVIDENCE_ID} — March 1917 Enterprise visual audit finds one misassociated page and leaves true 16 March page 5 unrecovered
<!-- {MARKER} -->
Source: `{SOURCE_ID}`  
Type: Primary newspaper page scans plus recovery audit  
Claims:
- All **40 exposed March archive slots** were visually inspected, but only **39 are genuine intended-date March issue pages**.
- The archive file exposed as **16 March seq-5/page 5 visibly prints 23 March 1917, Page 5** and is a distinct scan from the normal 23 March page 5.
- True **16 March 1917 Enterprise page 5** remains a **RETRIEVAL GAP** after PDF/JP2/OCR/RDF/page-HTML, alternate-edition, and Library-of-Congress/Chronicling-America recovery attempts; manual callout `{MANUAL_ID}` preserves the next route.
- Enterprise cumulative genuine intended-date coverage is **105 pages through March**, with **310 later exposed April-December pages** still unreviewed.
- No defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact 427 Main occupant was established on the 39 genuine recovered March pages.
- A Farr Brothers reference appears only on the misassociated **23 March** Page-5 variant; it supplies no 505 address and does not bridge Edwin/Alice Farr to 505 in 1917.
Classification: **DOCUMENTED / DIRECT** for visible printed dates and scan identity; **RETRIEVAL GAP** for true 16 March page 5; **COVERAGE RESULT ONLY** for the no-target-address finding.  
Confidence: **Very High** for the page-date conflict and inspected-page counts; no continuity, vacancy, or Farr identity inference is made.'''
append_once("evidence/evidence-register.md", evidence_block)

sources = read("database/sources.yml")
if re.search(rf"(?m)^  - id: {re.escape(SOURCE_ID)}$", sources) is None:
    sources = sources.rstrip() + f'''

  - id: {SOURCE_ID}
    name: "Oregon City Enterprise, March 1917 scan-first visual-review batch with archive page-association conflict"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-03-16/ed-1/"
    type: "Primary newspaper page scans; 40 exposed slots inspected, 39 genuine intended-date pages recovered"
    date: "1917-03-02 through 1917-03-30"
    repository_file: "{CAPTURE_REL}"
    notes: "16 March seq-5 visibly belongs to 23 March; true 16 March page 5 remains a retrieval gap after alternate-derivative recovery. No exact target-address occupant established on the 39 genuine pages."
    related_evidence: [{EVIDENCE_ID}]
''' + "\n"
    write("database/sources.yml", sources)

evidence = read("database/evidence.yml")
if re.search(rf"(?m)^  - id: {re.escape(EVIDENCE_ID)}$", evidence) is None:
    evidence = evidence.rstrip() + f'''

  - id: {EVIDENCE_ID}
    name: "March 1917 Enterprise visual audit finds one misassociated page and leaves true 16 March page 5 unrecovered"
    type: "Primary newspaper page scans plus recovery audit"
    date: "1917-03-02 through 1917-03-30"
    claims:
      - "All 40 exposed March archive slots were visually inspected; 39 are genuine intended-date March issue pages."
      - "The 16 March seq-5 object visibly prints 23 March 1917 Page 5 and differs from the normal 23 March Page-5 scan."
      - "True 16 March page 5 remains a retrieval gap after alternate-derivative and alternate-edition recovery attempts."
      - "Enterprise cumulative genuine intended-date coverage through March is 105 pages; 310 later exposed April-December pages remain unreviewed."
      - "No exact 501/503/505/507/509/511 or new 427 Main occupant was established on the 39 genuine recovered pages."
      - "The Farr Brothers wording on the misassociated 23 March variant does not bridge Edwin/Alice Farr to 505 in 1917."
    confidence: "Very High for page-date conflict and counts; retrieval gap and no-merge limits explicitly retained."
    related_sources: [{SOURCE_ID}]
''' + "\n"
    write("database/evidence.yml", evidence)

closeout_block = f'''## Enterprise March audit added 6 September 2026
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` audits all **40 exposed March Enterprise slots**, but visual printed-date checking shows only **39 genuine intended-date March pages**. The archive's 16 March seq-5/page-5 object visibly prints **23 March 1917, Page 5** and is distinct from the normal 23 March page 5. Reasonable alternate-derivative/edition/LOC recovery did not locate the true 16 March page 5, now retained as **RETRIEVAL GAP / `{MANUAL_ID}`**. Enterprise cumulative genuine coverage is **105 pages through March**, with **310 later exposed April-December pages** pending. No exact target 501/503/505/507/509/511 occupant was established on the recovered genuine pages; the missing page prevents complete 16 March no-hit coverage.'''
append_once("evidence/source-captures/1917-closeout.md", closeout_block)

# Update canonical year status.
year = read("registers/year-status.md")
lines = year.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = f"| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-december-13-27-year-end-review-2026-09-05.md`; `evidence/source-captures/1917-enterprise-january-05-26-visual-review-2026-09-06.md`; `evidence/source-captures/1917-enterprise-february-02-23-visual-review-2026-09-06.md`; `{CAPTURE_REL}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 retrieval gap. *Oregon City Enterprise*: Friday-pattern inventory exposes **52 issue buckets / 416 slots**; through March **105 genuine intended-date pages visually verified**. All 40 March slots were inspected, but 16 Mar seq-5 is visibly a 23 Mar Page-5 variant; true 16 Mar p5 is **RETRIEVAL GAP `{MANUAL_ID}`**. **310 later exposed Apr-Dec pages remain**, and title-calendar reconciliation is still required. Other online source-class closeout and the Sohns & Woodbeck Oregon City directory section remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
write("registers/year-status.md", "\n".join(lines) + "\n")

# Update archive navigation/status bullet if present.
idx = read("ARCHIVE_INDEX.md")
m = re.search(r"(?m)^- \*\*1917 — IN PROGRESS:\*\*.*$", idx)
if m:
    repl = f"- **1917 — IN PROGRESS:** *Courier* reaches all 52 issue dates with **435 genuine pages visually verified** and true 13 Dec p21 unresolved. *Oregon City Enterprise* Friday-pattern inventory exposes **52 issue buckets / 416 slots**; through March **105 genuine intended-date pages** are visually verified. All 40 March slots were inspected, but 16 Mar seq-5 is a visibly misassociated 23 Mar Page-5 variant; true 16 Mar p5 is retrieval gap `{MANUAL_ID}`. **310 later Apr-Dec exposed pages** remain, with title-calendar reconciliation and the Sohns & Woodbeck Oregon City directory section still unresolved."
    idx = idx[:m.start()] + repl + idx[m.end():]
    write("ARCHIVE_INDEX.md", idx)

# Preserve current open-question state rather than creating a duplicate OQ.
oq_block = f'''### 6 September 2026 — March Enterprise retrieval-gap refinement
<!-- {MARKER} -->

`{EVIDENCE_ID}` / `{SOURCE_ID}` advances 1917 newspaper coverage but **does not resolve the 503/505 occupant question**. Of 40 exposed March Enterprise slots, 39 are genuine intended-date pages; the archive's 16 March seq-5 visibly prints 23 March, and the true 16 March page 5 remains unrecovered under manual callout `{MANUAL_ID}` after reasonable online recovery attempts. No exact 501/503/505/507/509/511 occupant was established on the 39 genuine pages. Keep the missing page and newspaper silence as coverage/retrieval facts only, not vacancy or non-use evidence.'''
append_once("evidence/open-questions.md", oq_block)

lead_block = f'''## 6 September 2026 — 1917 Enterprise March gap-aware continuation
<!-- {MARKER} -->

`{SOURCE_ID}` / `{EVIDENCE_ID}` visually audits all 40 archive-supplied March slots and identifies a source-association defect: 16 March seq-5 visibly belongs to 23 March. The true 16 March page 5 remains **RETRIEVAL GAP `{MANUAL_ID}`** after PDF/JP2/OCR/RDF, alternate-edition and LOC/Chronicling-America recovery attempts. Enterprise cumulative genuine intended-date coverage is **105 pages through March**; **310 later Apr-Dec exposed pages** remain. Continue with April page-by-page visual review, but preserve the March gap for manual completion. The exact 1917 503/505 occupant question remains unresolved; no vacancy inference and no Farr identity merge is permitted.'''
append_once("evidence/research-leads.md", lead_block)

# Add the new annual retrieval gap to the central manual dashboard without promoting it into the immediate-action queue.
manual = read("MANUAL-FOLLOWUP.md")
if MARKER not in manual:
    manual = re.sub(r"Last amended: \*\*[^*]+\*\*[^\n]*", "Last amended: **6 September 2026** — added a visually confirmed 1917 Enterprise source-association gap and its exhausted online-recovery route; no existing MF ID was renumbered or removed.", manual, count=1)
    manual += f'''\n\n---\n\n## 6 September 2026 — 1917 Enterprise source-page retrieval gap\n<!-- {MARKER} -->\n\n| ID | Audited disposition | Still needed? | Audit decision |\n| --- | --- | --- | --- |\n| **{MANUAL_ID}** | **YEAR-CLOSEOUT / MANUAL CALLOUT** | **Yes for 1917 manual completion** | Obtain the **true printed page 5 of the 16 March 1917 Oregon City Enterprise** from Oregon City Public Library microfilm, Oregon Digital Newspaper Program source microfilm/original, or another institutional copy. The online archive's 16 Mar seq-5 PDF/JP2/OCR/RDF object is visually a **23 Mar 1917 Page 5**; alternate online derivatives and editions did not recover the correct page. Inspect the supplied scan visually for 501/503/505/507/509/511, occupants, business names, sales/moves, fire/construction/demolition and Fifth/Main controls, then integrate the result. This is a retrieval gap, **not negative evidence**. See `{CAPTURE_REL}` and `{RECOVERY_REL}`. |\n'''
    write("MANUAL-FOLLOWUP.md", manual)

# Record propagation audit and next action.
log_block = f'''| 2026-09-06 | Completed gap-aware March 1917 Oregon City Enterprise visual audit and cross-record propagation review | Inspected **40/40 exposed March slots**; **39 genuine intended-date pages**. 16 Mar seq-5 visibly prints 23 Mar Page 5 and differs from the normal 23 Mar p5; true 16 Mar p5 remains retrieval gap `{MANUAL_ID}` after alternate-derivative/edition/LOC recovery. Enterprise cumulative genuine coverage **105 pages**, with 310 later Apr-Dec exposed pages pending. Reviewed 503/505 buildings/timelines, Farr business/person profiles, master/business timelines, open questions and leads; no new target occupant/building/business/person fact warrants an entity chronology edit. | Continue April Enterprise page-by-page visual audit; preserve `{MANUAL_ID}` for year-closeout/manual retrieval. |'''
append_once("registers/research-log.md", log_block)

# Institutionalize the cross-record propagation check requested by the project steward.
agents = read("AGENTS.md")
policy_marker = "<!-- cross-record-propagation-audit-2026-09-06 -->"
if policy_marker not in agents:
    anchor = "## Updating Evidence\n"
    insert = '''## Cross-Record Propagation Audit\n<!-- cross-record-propagation-audit-2026-09-06 -->\n\nAfter every meaningful verified source batch, explicitly review the related **timeline, building, business, person, open-question, research-lead, register, crosswalk, and YAML/database records** before calling the integration complete. Update every record whose historical content or evidence state materially changes.\n\nIf the batch produces only bounded coverage, a retrieval gap, or a no-hit result and therefore **does not establish a new entity fact**, record that propagation decision in the source capture or research log rather than manufacturing a vacancy, occupant, business, ownership, or building-event entry. A no-hit is not a historical event.\n\n'''
    if anchor not in agents:
        raise SystemExit("AGENTS.md Updating Evidence anchor not found")
    agents = agents.replace(anchor, insert + anchor, 1)
    write("AGENTS.md", agents)

print(f"Integrated March as {SOURCE_ID} / {EVIDENCE_ID}; manual gap {MANUAL_ID}; retrieval {RETRIEVAL_COMMIT}; recovery {RECOVERY_COMMIT}")
