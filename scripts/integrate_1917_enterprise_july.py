from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise July visual closeout — 2026-09-07"
CAPTURE = "evidence/source-captures/1917-enterprise-july-06-27-visual-review-2026-09-07.md"
MANIFEST = "newspapers/oregon-city-enterprise/1917-july/manifest.json"


def r(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def w(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block, marker=MARKER):
    text = r(rel)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    w(rel, text + "\n" + block.strip() + "\n")


def replace_line(rel, prefix, newline):
    text = r(rel)
    lines = text.splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            lines[i] = newline
            found = True
            break
    if not found:
        raise SystemExit(f"Missing line prefix {prefix!r} in {rel}")
    w(rel, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def update_entity_relations(rel, entity_id, evidence_id, source_id):
    """Add related evidence/source IDs to one YAML entity block without reformatting the file."""
    text = r(rel)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing {entity_id} in {rel}")
    nxt = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + nxt.start() if nxt else len(text)
    block = text[m.start():end]

    def collect_and_strip(block_text, key):
        lines = block_text.splitlines()
        vals = []
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            mm = re.match(rf"^    {re.escape(key)}:\s*(.*)$", line)
            if not mm:
                out.append(line)
                i += 1
                continue
            inline = mm.group(1).strip()
            if inline.startswith("[") and inline.endswith("]"):
                vals.extend(x.strip() for x in inline[1:-1].split(",") if x.strip())
                i += 1
                continue
            i += 1
            while i < len(lines):
                lm = re.match(r"^      -\s+(.+?)\s*$", lines[i])
                if not lm:
                    break
                vals.append(lm.group(1).strip())
                i += 1
        return vals, out

    evs, lines = collect_and_strip(block, "related_evidence")
    srcs, lines2 = collect_and_strip("\n".join(lines), "related_sources")
    lines = lines2
    if evidence_id not in evs:
        evs.append(evidence_id)
    if source_id not in srcs:
        srcs.append(source_id)
    insert_at = next((i for i, line in enumerate(lines) if line.startswith("    repository_file:")), len(lines))
    lines[insert_at:insert_at] = [
        "    related_evidence: [" + ", ".join(evs) + "]",
        "    related_sources: [" + ", ".join(srcs) + "]",
    ]
    newblock = "\n".join(lines)
    if block.endswith("\n"):
        newblock += "\n"
    w(rel, text[:m.start()] + newblock + text[end:])


if not (ROOT / MANIFEST).exists():
    raise SystemExit(f"Required July manifest missing: {MANIFEST}")

retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST], cwd=ROOT, text=True
).strip()

# Allocate only after the workflow has pulled the newest main.
src_text = r("evidence/source-register.md")
ev_text = r("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", src_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", ev_text)]
SID = f"S-{max(source_nums) + 1:03d}"
EID = f"E-{max(evidence_nums) + 1:03d}"

if (ROOT / CAPTURE).exists():
    prior = r(CAPTURE)
    sm = re.search(r"source `(S-\d{3})`", prior)
    em = re.search(r"evidence `(E-\d{3})`", prior)
    if sm:
        SID = sm.group(1)
    if em:
        EID = em.group(1)

capture = f'''# 1917 Oregon City Enterprise — July 6, 13, 20 and 27 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 32/32 genuine intended-date pages. July monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SID}`; evidence `{EID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-july/`  
Retrieval commit: `{retrieval_commit}`  
Manifest: `{MANIFEST}`

## Page-identity audit

All 32 actual page scans for **6, 13, 20 and 27 July 1917** were visually inspected. Each issue contains eight genuine matching-date pages. Printed mastheads and printed page numbers 1–8 were separately checked because March and April exposed archive page-association defects. **No July substitution, duplicate-page defect or retrieval gap was found.** In particular, archive sequences whose listing labels were incomplete on 20 July were confirmed from the scans themselves as printed pages 3, 4 and 7.

OCR/text searching was used only after the scan-first pass to locate or backstop small-print candidates. Numeric and topical false positives were rejected as context rather than converted into address evidence.

Enterprise cumulative genuine intended-date coverage advances from **208 through June to 240 through July**. The January–July archive-slot audit is **242 slots inspected / 240 genuine intended-date pages**, with the two previously documented true-page retrieval gaps unchanged: **16 March p5** and **13 April p8**. **174 exposed August–December slots remain**, plus final title-calendar reconciliation.

## Direct July findings

### W. S. Eddy / Fashion Stable continues through 27 July

The professional-directory advertisement on **6, 13, 20 and 27 July p7** directly repeats **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the visually verified 1917 relative-location run from 6 April through **27 July 1917** (`P-396` / `BUS-103`).

No street number is printed. Do not assign Fashion Stable to **427 Main**, any numbered Fifth Street premises, or **501/503/505**; do not merge W. S. Eddy with W. B. Eddy.

### Farr Brothers continuation — 20 July

**20 July p7** prints a market-report credit stating that the report is furnished by **Farr Bros.** and Brady Mercantile Company. **20 July p8** also lists **Farr Bros.** in County Court expenditures, including separate lines associated with Mrs. Piezo and Tom Garner. These are direct dated local-business/supplier appearances but print **no Farr Brothers street address and no individual Farr proprietor**.

The stronger 25 May wording remains the direct 1917 **Meat market** description for `BUS-104`. The July material does **not** connect Farr Brothers Store / Meat Market to Edwin F. Farr, Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr, or Harr's Recreation Center.

Other July Farr OCR candidates are personal-name context and remain separate; they are not used to bridge the businesses.

### Target frontage and adjacent-address result

Across all **32 genuine July pages**, the scan-first review and follow-up text checks did not recover a defensible exact occupant for **501, 503, 505, 507, 509 or 511 Main**, nor a new exact **427 Main** occupant or a new numbered Fifth Street target occupant. A `pool` OCR occurrence on 13 July p5 refers to a **farmers' wool pool**, not a pool room or billiard business.

This is a **bounded coverage statement only**. It is not evidence of vacancy, non-use, closure, demolition, relocation, or absence at any target address.

## Cross-Record Propagation Audit

Explicitly reviewed after the verified July batch:

- source/evidence registers and database YAML;
- master and business timelines;
- 501/503/505 building pages and unified timelines;
- 427 Main and numbered Fifth Street controls;
- W. S. Eddy / Fashion Stable person/business pages, indexes and YAML;
- Farr Brothers Store / Meat Market and Farr identity controls, including the strict no-merge with Edwin/Alice Farr and 505;
- open questions and research leads;
- business and address registers;
- ID crosswalk and archive index;
- annual year status and research log.

Propagation decision:

- extend `P-396` / `BUS-103` Fashion Stable's direct Main-between-Fourth/Fifth observation through **27 July 1917**;
- add the two **20 July Farr Bros.** business/supplier observations to `BUS-104`, without creating an address, individual proprietor, or 505 relationship;
- advance the Enterprise annual audit to **240 genuine pages through July**, with **174 exposed August–December slots remaining** and the two earlier true-page gaps unchanged;
- do **not** add a 1917 target-building occupant/event to 501/503/505, 427 Main, or the numbered Fifth Street building records because July establishes none;
- do **not** change the address register for Fashion Stable because the direct wording remains relative rather than numbered;
- do **not** close the 1917 503/505 occupant question.

## Status and next step

**July Enterprise monthly batch is closed: 32/32 visually verified genuine intended-date pages.** 1917 remains **IN PROGRESS** with the Courier true-page gap, the two Enterprise true-page gaps, the unrecovered Sohns & Woodbeck Oregon City directory section, remaining Enterprise August–December pages, title-calendar reconciliation and other-source closeout work still active.

The next chronological online newspaper step is **August 1917 Oregon City Enterprise**, beginning with the exposed 3 August issue after verifying the August inventory/page counts.
'''

if not (ROOT / CAPTURE).exists():
    w(CAPTURE, capture)

append_once("evidence/source-register.md", f'''## {SID} — Oregon City Enterprise, July 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **32/32 genuine intended-date pages visually verified**.  
Issue dates: 6, 13, 20 and 27 July 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-07-27/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-july/`; manifest `{MANIFEST}`; retrieval commit `{retrieval_commit}`.  
Evidence: `{EID}`; capture: `{CAPTURE}`.  
Notes: W. S. Eddy/Fashion Stable repeats through 27 July at Main between Fourth/Fifth; 20 July carries Farr Bros. market-report and county-expenditure appearances. No exact target Main occupant.''')

append_once("evidence/evidence-register.md", f'''## {EID} — July 1917 Enterprise closes 32-page batch and extends Fashion Stable through July 27
<!-- {MARKER} -->
Source: `{SID}`  
Type: Primary newspaper visual review  
Claims:
- all **32/32 July scans** are visually verified genuine intended-date pages, with no July page-association defect;
- Enterprise cumulative genuine coverage is **240 pages through July**; **242 Jan–Jul archive slots** have been inspected, with the existing March/April true-page gaps unchanged; **174 August–December exposed slots remain**;
- 6/13/20/27 July p7 directly repeat W. S. Eddy / Fashion Stable **between Fourth and Fifth on Main Street**, extending the verified 1917 observation through 27 July;
- 20 July p7 credits a market report to Farr Bros. and Brady Mercantile Company, while 20 July p8 includes Farr Bros. in County Court expenditures; neither prints a Farr street address or individual proprietor;
- no exact 501/503/505/507/509/511 Main, new 427 Main, or new numbered Fifth Street target occupant was established.
Classification: **DOCUMENTED / DIRECT** for scan identity and printed Fashion Stable/Farr wording; **COVERAGE RESULT ONLY** for the target-address no-hit.  
Confidence: **Very High**, with exact-number, individual-identity and continuity limits preserved.''')

# Database source/evidence synchronization.
text = r("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(SID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {SID}\n    name: "Oregon City Enterprise, July 1917 complete scan-first visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-07-27/ed-1/"\n    type: "Primary newspaper page scans; 32/32 genuine pages visually verified"\n    date: "1917-07-06 through 1917-07-27"\n    repository_file: "{CAPTURE}"\n    notes: "July complete; Fashion Stable continues through 27 July and Farr Bros. appears twice on 20 July; no exact target Main occupant."\n    related_evidence: [{EID}]\n'''
    w("database/sources.yml", text)

text = r("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(EID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {EID}\n    name: "July 1917 Enterprise closes 32-page batch and extends Fashion Stable through July 27"\n    type: "Primary newspaper visual review"\n    date: "1917-07-06 through 1917-07-27"\n    claims:\n      - "All 32 July pages visually verified as genuine intended-date pages."\n      - "Enterprise cumulative genuine coverage: 240 pages through July; 174 August-December slots remain; March and April true-page gaps unchanged."\n      - "6/13/20/27 July p7 repeat W. S. Eddy/Fashion Stable between Fourth and Fifth on Main Street."\n      - "20 July p7 and p8 include Farr Bros. business/supplier references without address or named proprietor."\n      - "No exact target Main or new numbered Fifth target occupant established in July."\n    confidence: "Very High for visible wording and counts; inference limits retained."\n    related_businesses: [BUS-103, BUS-104]\n    related_people: [P-396]\n    related_sources: [{SID}]\n'''
    w("database/evidence.yml", text)

# Stable entity pages.
fs = r("businesses/fashion-stable.md")
fs = fs.replace("**6 April–29 June 1917:**", "**6 April–27 July 1917:**")
fs = fs.replace("and `E-254` / `S-281`).", f"and `E-254` / `S-281`; continued `{EID}` / `{SID}`).")
if MARKER not in fs:
    fs += f'''\n\n## July continuation\n<!-- {MARKER} -->\n\nAds on 6, 13, 20 and 27 July p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street, extending the verified 1917 span through **27 July** (`{EID}` / `{SID}`). No exact number is printed.\n'''
w("businesses/fashion-stable.md", fs)

ps = r("people/profiles/w-s-eddy.md")
ps = ps.replace("**6 April–29 June 1917:**", "**6 April–27 July 1917:**")
ps = ps.replace("and `E-254` / `S-281`).", f"and `E-254` / `S-281`; continued `{EID}` / `{SID}`).")
if MARKER not in ps:
    ps += f'''\n\n## July continuation\n<!-- {MARKER} -->\n\nThe 6/13/20/27 July p7 advertisements repeat the same name, credentials, business and relative location; latest verified date is **27 July 1917** (`{EID}` / `{SID}`).\n'''
w("people/profiles/w-s-eddy.md", ps)

fb = r("businesses/farr-brothers-store.md")
if MARKER not in fb:
    fb += f'''\n\n## July 1917 continuation\n<!-- {MARKER} -->\n\nOn **20 July p7**, a market-report credit says the report is furnished by **Farr Bros.** and Brady Mercantile Company; **20 July p8** also lists **Farr Bros.** in County Court expenditures (`{EID}` / `{SID}`). These are additional dated business/supplier appearances, but neither supplies an address or individual Farr proprietor. The 25 May **Meat market** wording remains the controlling direct 1917 trade description. No Edwin/Alice Farr or 505 Main merge is permitted.\n'''
w("businesses/farr-brothers-store.md", fb)

# Human-readable indexes.
people = r("people/people-index.md")
m = re.search(r"(?m)^\| P-396 \|.*$", people)
if m:
    row = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 Fifth-between-Main/Water; 6 Apr–27 Jul 1917 Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. `E-252` / `S-279`; `E-253` / `S-280`; `E-254` / `S-281`; `{EID}` / `{SID}`. |"
    people = people[:m.start()] + row + people[m.end():]
w("people/people-index.md", people)

biz = r("businesses/business-index.md")
m = re.search(r"(?m)^\| BUS-103 \|.*$", biz)
if m:
    row = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–27 Jul 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); no exact number. July ads extend direct observation through 27 July. `E-252` / `S-279`; `E-253` / `S-280`; `E-254` / `S-281`; `{EID}` / `{SID}`. |"
    biz = biz[:m.start()] + row + biz[m.end():]
if MARKER not in biz:
    biz += f'''\n\n## July 1917 Enterprise continuation\n<!-- {MARKER} -->\n\n`BUS-104` Farr Brothers receives two additional 20 July observations: a market-report credit on p7 and County Court expenditures on p8 (`{EID}` / `{SID}`). Neither prints an address or individual proprietor; no `BUS-013` / 505 merge.\n'''
w("businesses/business-index.md", biz)

# YAML entity relations; descriptions remain conservative and are supplemented by S/E records.
for rel, ent in [
    ("database/businesses.yml", "BUS-103"),
    ("database/businesses.yml", "BUS-104"),
    ("database/people.yml", "P-396"),
]:
    update_entity_relations(rel, ent, EID, SID)

# Master/business chronology: continuation evidence, not a new numbered target-building event.
append_once("timeline.md", f'''## 6–27 July 1917 — Enterprise continuation: Fashion Stable and Farr Brothers
<!-- {MARKER} -->

Four visually verified July professional ads extend **W. S. Eddy (`P-396`) / Fashion Stable (`BUS-103`) at Main between Fourth and Fifth** through **27 July 1917** (`{EID}` / `{SID}`). No exact street number is printed. On **20 July**, Farr Bros. appears in a market-report credit and County Court expenditures, still without a Farr address or named proprietor. These observations do not establish an occupant at 501/503/505 or bridge Farr Brothers Store to Farr's Pool Hall at 505.
''')

bt = r("registers/business-timeline.md")
m = re.search(r"(?m)^\| .*Fashion Stable / W\. S\. Eddy.*BUS-103.*$", bt)
if m:
    row = f"| 6 Apr.–27 Jul. 1917 verified span | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252`, `E-253`, `E-254`, `{EID}`; `S-279`, `S-280`, `S-281`, `{SID}` | Direct relative-location wording; no street number, move date, lease, ownership, or target-building continuity. |"
    bt = bt[:m.start()] + row + bt[m.end():]
if MARKER not in bt:
    bt += f'''\n\n| 20 Jul. 1917 | Not printed | Farr Bros. market-report credit + county expenditures | `BUS-104` | `{EID}` / `{SID}` | Dated business/supplier appearances only; no address or named proprietor; no Edwin/Alice Farr or 505 merge. |\n<!-- {MARKER} -->\n'''
w("registers/business-timeline.md", bt)

# Open question stays open; narrow only the reviewed source window.
append_once("evidence/open-questions.md", f'''## 7 September 2026 — 1917 Enterprise July coverage does not resolve 503/505 occupancy
<!-- {MARKER} -->

The complete July Enterprise visual batch (`{SID}` / `{EID}`) raises cumulative genuine Enterprise coverage to **240 pages through July** but does **not** identify an exact 503 or 505 Main occupant. This is bounded source coverage, not vacancy/non-use evidence. The 1917 occupant question remains open; the Sohns & Woodbeck Oregon City directory section and remaining Enterprise August–December pages remain material routes.
''')

append_once("evidence/research-leads.md", f'''## 7 September 2026 — Enterprise continuation after July
<!-- {MARKER} -->

July is complete **32/32** (`{SID}` / `{EID}`), cumulative **240 genuine Enterprise pages through July**. Continue with **August 3/10/17/24/31**, but first verify the actual exposed issue/page inventory rather than assuming eight pages per date. Preserve the March/April true-page gaps and the 1916–17 Sohns & Woodbeck Oregon City directory gap. Continue target-address, pool-room, Fashion Stable and Farr identity checks with the same scan-first/no-merge rules.
''')

append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise July audit added 7 September 2026
<!-- {MARKER} -->

`{SID}` / `{EID}` closes July at **32/32 genuine visually verified pages**, with no July page-identity defect. Enterprise cumulative genuine coverage is **240 pages through July**; **242 Jan–Jul archive slots** have been inspected, the true **16 March p5** and **13 April p8** retrieval gaps remain, and **174 exposed August–December slots** remain. W. S. Eddy / Fashion Stable continues through 27 July at Main between Fourth/Fifth; 20 July carries two Farr Bros. business/supplier observations without address or named proprietor. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Coverage only; 1917 remains **IN PROGRESS**.
''')

append_once("indexes/id-crosswalk.md", f'''## {SID} / {EID} — July 1917 Enterprise visual closeout
<!-- {MARKER} -->

- `{SID}` → preserved 6/13/20/27 July Enterprise scans and `{CAPTURE}`.
- `{EID}` → `P-396` / `BUS-103` Fashion Stable continuation through 27 July; `BUS-104` Farr Brothers 20 July market-report/expenditure observations.
- No `B-001` / `B-002` occupant relationship is created: the target-address result is bounded coverage only.
''')

# Canonical year-status row.
yr = r("registers/year-status.md")
newrow = f'| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 unresolved. *Oregon City Enterprise*: **240 genuine intended-date pages through July**; 242 Jan–Jul archive slots inspected, with true 16 Mar p5 and true 13 Apr p8 retrieval gaps; **174 Aug–Dec exposed slots remain**. July extends W. S. Eddy/Fashion Stable through 27 Jul and adds two 20 Jul Farr Bros. business/supplier controls; no target-frontage occupant. Title-calendar reconciliation, Sohns & Woodbeck Oregon City directory section, and other source-class closeout remain unresolved. |'
lines = yr.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = newrow
        break
else:
    raise SystemExit("Missing 1917 year-status row")
w("registers/year-status.md", "\n".join(lines) + ("\n" if yr.endswith("\n") else ""))

# Research log is a row-oriented audit record.
rl = r("registers/research-log.md")n = None
logrow = f"| 2026-09-07 | Completed July 1917 Oregon City Enterprise scan-first visual audit | **32/32 genuine pages** for 6/13/20/27 Jul; cumulative **240 genuine pages through July**, **174 Aug–Dec slots remain**; existing Mar/Apr page gaps unchanged. Fashion Stable / W. S. Eddy extends through 27 Jul; 20 Jul Farr Bros. market-report + expenditure controls remain unaddressed/no named proprietor. No exact target-frontage occupant; bounded coverage only. `{SID}` / `{EID}`. Cross-record propagation audit completed. |"
if MARKER not in rl:
    lines = rl.splitlines()
    sep_idx = next((i for i, line in enumerate(lines) if line.startswith("| ---") and i > 0), None)
    if sep_idx is None:
        rl = rl.rstrip() + "\n\n" + logrow + f"\n<!-- {MARKER} -->\n"
    else:
        lines.insert(sep_idx + 1, logrow)
        lines.insert(sep_idx + 2, f"<!-- {MARKER} -->")
        rl = "\n".join(lines) + ("\n" if r("registers/research-log.md").endswith("\n") else "")
    w("registers/research-log.md", rl)

append_once("ARCHIVE_INDEX.md", f'''## 1917 Enterprise — July complete visual batch
<!-- {MARKER} -->

- [`{SID}` / `{EID}` July Enterprise visual review]({CAPTURE}): 6/13/20/27 July, **32/32 genuine pages**, no page-association defect; cumulative Enterprise **240 genuine pages through July**.
- Preserved originals and checksums: [`newspapers/oregon-city-enterprise/1917-july/manifest.json`]({MANIFEST}).
- Entity propagation: `P-396` / `BUS-103` Fashion Stable through 27 July; `BUS-104` Farr Brothers 20 July controls. No exact target Main occupant created.
''')

print(f"Integrated July Enterprise as {SID} / {EID}; retrieval commit {retrieval_commit}")
