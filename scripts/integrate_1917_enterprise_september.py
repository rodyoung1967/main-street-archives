from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise September visual closeout — 2026-09-07"
CAPTURE = "evidence/source-captures/1917-enterprise-september-07-28-visual-review-2026-09-07.md"
MANIFEST = "newspapers/oregon-city-enterprise/1917-september/manifest.json"
JCP_PAGE = "businesses/j-c-penney-golden-rule.md"


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


def update_entity_relations(rel, entity_id, evidence_id, source_id):
    text = r(rel)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing {entity_id} in {rel}")
    nxt = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + nxt.start() if nxt else len(text)
    block = text[m.start():end]

    def collect_and_strip(block_text, key):
        lines = block_text.splitlines()
        vals, out = [], []
        i = 0
        while i < len(lines):
            line = lines[i]
            mm = re.match(rf"^    {re.escape(key)}:\s*(.*)$", line)
            if not mm:
                out.append(line); i += 1; continue
            inline = mm.group(1).strip()
            if inline.startswith("[") and inline.endswith("]"):
                vals.extend(x.strip() for x in inline[1:-1].split(",") if x.strip())
                i += 1; continue
            i += 1
            while i < len(lines):
                lm = re.match(r"^      -\s+(.+?)\s*$", lines[i])
                if not lm:
                    break
                vals.append(lm.group(1).strip()); i += 1
        return vals, out

    evs, lines = collect_and_strip(block, "related_evidence")
    srcs, lines = collect_and_strip("\n".join(lines), "related_sources")
    if evidence_id not in evs: evs.append(evidence_id)
    if source_id not in srcs: srcs.append(source_id)
    insert_at = next((i for i,l in enumerate(lines) if l.startswith("    repository_file:")), len(lines))
    lines[insert_at:insert_at] = [
        "    related_evidence: [" + ", ".join(evs) + "]",
        "    related_sources: [" + ", ".join(srcs) + "]",
    ]
    newblock = "\n".join(lines) + ("\n" if block.endswith("\n") else "")
    w(rel, text[:m.start()] + newblock + text[end:])


if not (ROOT / MANIFEST).exists():
    raise SystemExit(f"Required September manifest missing: {MANIFEST}")
retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST], cwd=ROOT, text=True
).strip()

# Allocate identifiers only after workflow syncs latest main.
src = r("evidence/source-register.md")
ev = r("evidence/evidence-register.md")
SID = f"S-{max(int(x) for x in re.findall(r'(?m)^## S-(\\d{3})\\b', src)) + 1:03d}"
EID = f"E-{max(int(x) for x in re.findall(r'(?m)^## E-(\\d{3})\\b', ev)) + 1:03d}"

if (ROOT / JCP_PAGE).exists():
    m = re.search(r"Business ID: `(BUS-\d{3})`", r(JCP_PAGE))
    if not m:
        raise SystemExit("Existing JCP page lacks Business ID")
    JCP_BUS = m.group(1)
else:
    bus_text = r("database/businesses.yml") + "\n" + r("businesses/business-index.md")
    nums = [int(x) for x in re.findall(r"BUS-(\d{3})", bus_text)]
    JCP_BUS = f"BUS-{max(nums)+1:03d}"

if (ROOT / CAPTURE).exists():
    prior = r(CAPTURE)
    sm = re.search(r"source `(S-\d{3})`", prior); em = re.search(r"evidence `(E-\d{3})`", prior)
    bm = re.search(r"J\. C\. Penney business `(BUS-\d{3})`", prior)
    if sm: SID = sm.group(1)
    if em: EID = em.group(1)
    if bm: JCP_BUS = bm.group(1)

capture = f'''# 1917 Oregon City Enterprise — September 7, 14, 21 and 28 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 32/32 genuine intended-date pages. September monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SID}`; evidence `{EID}`; J. C. Penney business `{JCP_BUS}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-september/`  
Retrieval commit: `{retrieval_commit}`  
Manifest: `{MANIFEST}`

## Page-identity audit

All 32 actual page scans for **7, 14, 21 and 28 September 1917** were visually inspected before text-layer searching. Each issue contains eight genuine matching-date pages. Printed issue dates and printed page numbers 1–8 were separately checked because March and April exposed archive page-association defects. **No September substitution, duplicate-page defect or retrieval gap was found.** OCR/text was used only after this scan-first pass as a small-print locator/backstop; candidate wording below was rechecked on the scans.

Enterprise cumulative genuine intended-date coverage advances from **280 through August to 312 through September**. The January–September archive-slot audit is **314 slots inspected / 312 genuine intended-date pages**, with the two earlier true-page retrieval gaps unchanged: **16 March p5** and **13 April p8**. **102 exposed October–December slots remain**, plus final title-calendar reconciliation.

## Direct September findings

### W. S. Eddy / Fashion Stable continues through 28 September

The professional-directory advertisement on **7, 14, 21 and 28 September p7** visibly repeats **W. S. Eddy, V.S., M.D.V.** and states that he is established at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the visually verified 1917 relative-location run from 6 April through **28 September 1917** (`P-396` / `BUS-103`). No street number is printed; do not assign Fashion Stable to 427 Main or any 501/503/505 frontage.

### Farr Brothers business/supplier continuation — and why market-credit changes are not ownership evidence

The local market-report provider line varies within September:

- **7 September p7:** visibly **R. Petzold and Brady Mercantile Company**;
- **14 September p7:** visibly **Farr Brothers and Brady Mercantile company**;
- **21 September p7:** the page does not carry the local market-report column;
- **28 September p7:** visibly **Brady Mercantile company and Farr Brothers**.

Separately, **14 September p6** visibly lists **Farr Bros. (Piezo), $14.00** in the County Court expenditure material, alongside other local suppliers. This is another direct dated `BUS-104` supplier/business appearance, but it prints no street address or individual Farr proprietor.

The alternating market-report credits demonstrate why a single provider-line change cannot be promoted to a sale, closure, ownership transfer, relocation or cessation. The controlling direct 1917 trade description remains the 25 May **Meat market** wording. None of these September items bridges Farr Brothers to Edwin F. Farr, Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr or Harr's Recreation Center.

### New block-relative anchor — J. C. Penney Co. / The Golden Rule

**14 September p3** contains a large advertisement visibly headed **J. C. Penney Co.**, with **THE GOLDEN RULE**, **175 BUSY STORES**, and the location line **Main Street Between Fifth and Sixth**, plus **Phone 270**. This is direct 1917 evidence for `JCP_BUS` = `{JCP_BUS}` at the Fifth-to-Sixth Main Street block.

The advertisement does **not** print a numbered address, side of Main, parcel, owner, lease, construction date or physical-building identity. It therefore must **not** be assigned to 501, 503, 505, 507, 509 or 511 Main. No matching J. C. Penney/Golden Rule advertisement was located in the completed August Enterprise text backstop or the other September issue text layers; that silence is not an opening/closure boundary.

### Adams Department Store closing-out advertising continues, unnumbered

The visually reviewed **7, 14 and 21 September p8** pages carry prominent Adams Department Store **QUIT BUSINESS / Quit Business Sale / closing-out** advertising. The September 28 issue does not provide a matching ad in the reviewed pages. This is dated unnumbered advertising context only. The disappearance of the ad by 28 September is **not** treated as proof of closure, sale completion, vacancy, relocation or demolition.

### Target frontage and rejected false positives

Across all **32 genuine September pages**, the scan-first review plus text backstop did not recover a defensible exact occupant for **501, 503, 505, 507, 509 or 511 Main**, nor a new exact **427 Main** occupant or numbered **106/107/108/109/110 Fifth** target occupant. No relevant pool-room/pool-hall/billiard exact-address hit was recovered.

Rejected numeric/context examples include **507 Corbett Building, Portland** (not 507 Main), **A. Smith, lots 6–7, block 106** (not 106 Fifth), and war/statistical numbers such as 107/108. A September 7 local item prints **411 Main street**, and September 14 prints **823 Main street** for unrelated people; neither resolves the target block. Personal George A. Harding appearances and county-payment entries are not converted into Harding Drug Store occupancy without an address/business bridge.

This target no-hit is a **bounded coverage statement only** — never vacancy, non-use, closure, demolition, relocation or absence evidence.

## Cross-Record Propagation Audit

Reviewed after the verified batch: source/evidence registers and YAML; master/business timelines; 501/503/505 building and unified timeline records; 427 Main and numbered Fifth controls; W. S. Eddy/Fashion Stable person/business records; Farr Brothers and Farr identity controls; business/address registers; J. C. Penney new business entity handling; open questions; research leads; crosswalk; archive index; year status; research log; database YAML.

Propagation decision:
- extend `P-396` / `BUS-103` Fashion Stable through **28 September 1917**;
- extend `BUS-104` with the 14/28 September Farr market-report credits and 14 September county-expenditure appearance while preserving the Petzold/Farr provider-line caution;
- create `{JCP_BUS}` for the direct **J. C. Penney Co. / The Golden Rule — Main Street Between Fifth and Sixth — Phone 270** observation, strictly without an exact number or building assignment;
- retain Adams closing-out advertising as unnumbered context only;
- advance Enterprise coverage to **312 genuine pages through September**, **102 exposed October–December slots remaining**, two earlier true-page gaps unchanged;
- make **no** 501/503/505/427 or numbered Fifth building-occupancy event because September establishes none;
- keep the 1917 exact 503/505 occupant question open.

## Status and next step

**September Enterprise monthly batch is closed: 32/32 visually verified genuine intended-date pages.** 1917 remains **IN PROGRESS**. Next chronological online step: **October 1917 Oregon City Enterprise**, after verifying the exposed October issue/page inventory (including the known six-page 19 October issue in the inventory).
'''
if not (ROOT / CAPTURE).exists():
    w(CAPTURE, capture)

append_once("evidence/source-register.md", f'''## {SID} — Oregon City Enterprise, September 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **32/32 genuine intended-date pages visually verified**.  
Issue dates: 7, 14, 21 and 28 September 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-09-14/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-september/`; manifest `{MANIFEST}`; retrieval commit `{retrieval_commit}`.  
Evidence: `{EID}`; capture: `{CAPTURE}`.  
Notes: Fashion Stable continues through 28 Sep; Farr business/supplier controls on 14/28 Sep; 14 Sep p3 directly places J. C. Penney Co./The Golden Rule on Main between Fifth/Sixth, phone 270; no exact target Main occupant.''')

append_once("evidence/evidence-register.md", f'''## {EID} — September 1917 Enterprise closes 32-page batch and adds J. C. Penney Fifth-to-Sixth Main anchor
<!-- {MARKER} -->
Source: `{SID}`  
Type: Primary newspaper visual review  
Claims:
- **32/32 September scans** are genuine intended-date pages with no page-association defect;
- cumulative Enterprise coverage: **312 genuine pages through September / 314 slots inspected**, two earlier true-page gaps unchanged, **102 Oct–Dec exposed slots remain**;
- 7/14/21/28 Sep p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main;
- 14 and 28 Sep market reports credit Farr Brothers + Brady Mercantile; 14 Sep p6 separately lists Farr Bros. (Piezo), $14.00; 7 Sep instead credits R. Petzold + Brady and 21 Sep has no local market-report column;
- 14 Sep p3 visibly advertises **J. C. Penney Co. / The Golden Rule — Main Street Between Fifth and Sixth — Phone 270** (`{JCP_BUS}`), with no numbered address;
- no exact 501/503/505/507/509/511 Main, new 427 Main, or numbered Fifth target occupant was established.
Classification: **DOCUMENTED / DIRECT** for scan identity and printed wording; **COVERAGE RESULT ONLY** for the target-address no-hit.  
Confidence: **Very High**, with exact-number, side-of-street, identity and continuity limits preserved.''')

# New block-relative business entity.
if not (ROOT / JCP_PAGE).exists():
    w(JCP_PAGE, f'''# J. C. Penney Co. / The Golden Rule — 1917 Oregon City

Business ID: `{JCP_BUS}`.

## Direct 1917 observation

A visually verified **14 September 1917 Oregon City Enterprise p3** advertisement (`{EID}` / `{SID}`) visibly prints **J. C. Penney Co.**, **THE GOLDEN RULE**, **175 BUSY STORES**, **Main Street Between Fifth and Sixth**, and **Phone 270**.

## Limits

The advertisement gives no numbered street address or side of Main. Do not assign this store to 501, 503, 505, 507, 509 or 511 Main, or to a specific parcel/building, without an independent numbered or spatial bridge. It does not establish property ownership, lease terms, construction, an opening date, or continuous occupancy before/after 14 September.

No matching ad was located in the already completed August Enterprise text backstop or the other September issue text layers. That silence is not an opening/closure boundary.
''')

# Database source/evidence.
text = r("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(SID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {SID}\n    name: "Oregon City Enterprise, September 1917 complete scan-first visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-09-14/ed-1/"\n    type: "Primary newspaper page scans; 32/32 genuine pages visually verified"\n    date: "1917-09-07 through 1917-09-28"\n    repository_file: "{CAPTURE}"\n    notes: "September complete; Fashion Stable through 28 Sep; Farr business controls; J. C. Penney/The Golden Rule Main between Fifth/Sixth phone 270; no exact target occupant."\n    related_evidence: [{EID}]\n'''
    w("database/sources.yml", text)

text = r("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(EID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {EID}\n    name: "September 1917 Enterprise closes 32-page batch and adds J. C. Penney Fifth-to-Sixth Main anchor"\n    type: "Primary newspaper visual review"\n    date: "1917-09-07 through 1917-09-28"\n    claims:\n      - "All 32 September pages visually verified as genuine intended-date pages."\n      - "Enterprise cumulative genuine coverage: 312 pages through September; 102 October-December slots remain; March/April true-page gaps unchanged."\n      - "7/14/21/28 September p7 repeat W. S. Eddy/Fashion Stable between Fourth and Fifth on Main Street."\n      - "14/28 September market reports credit Farr Brothers and Brady Mercantile; 14 September p6 separately lists Farr Bros. in county expenditures; provider-line changes are not ownership/closure evidence."\n      - "14 September p3 directly places J. C. Penney Co./The Golden Rule on Main Street between Fifth and Sixth, phone 270, without a number."\n      - "No exact target Main or numbered Fifth target occupant established in September."\n    confidence: "Very High for visible wording and counts; inference limits retained."\n    related_businesses: [BUS-103, BUS-104, {JCP_BUS}]\n    related_people: [P-396]\n    related_sources: [{SID}]\n'''
    w("database/evidence.yml", text)

text = r("database/businesses.yml")
if not re.search(rf"(?m)^  - id: {re.escape(JCP_BUS)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {JCP_BUS}\n    name: "J. C. Penney Co. / The Golden Rule — Oregon City 1917"\n    address: "Main Street between Fifth and Sixth (no number printed)"\n    notes: "14 Sep 1917 Enterprise p3 directly prints J. C. Penney Co., THE GOLDEN RULE, 175 BUSY STORES, Main Street Between Fifth and Sixth, Phone 270. No side/number/building assignment."\n    repository_file: "{JCP_PAGE}"\n    related_evidence: [{EID}]\n    related_sources: [{SID}]\n'''
    w("database/businesses.yml", text)
update_entity_relations("database/businesses.yml", "BUS-103", EID, SID)
update_entity_relations("database/businesses.yml", "BUS-104", EID, SID)
update_entity_relations("database/people.yml", "P-396", EID, SID)

# Entity continuations.
fs = r("businesses/fashion-stable.md")
fs = fs.replace("**6 April–31 August 1917:**", "**6 April–28 September 1917:**")
fs = fs.replace("and `E-261` / `S-287`).", f"and `E-261` / `S-287`; continued `{EID}` / `{SID}`).")
if MARKER not in fs:
    fs += f'''\n\n## September continuation\n<!-- {MARKER} -->\n\nAds on 7, 14, 21 and 28 September p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street, extending the verified 1917 span through **28 September** (`{EID}` / `{SID}`). No exact number is printed.\n'''
w("businesses/fashion-stable.md", fs)

ps = r("people/profiles/w-s-eddy.md")
ps = ps.replace("**6 April–31 August 1917:**", "**6 April–28 September 1917:**")
ps = ps.replace("and `E-261` / `S-287`).", f"and `E-261` / `S-287`; continued `{EID}` / `{SID}`).")
if MARKER not in ps:
    ps += f'''\n\n## September continuation\n<!-- {MARKER} -->\n\nThe 7/14/21/28 September p7 ads repeat the same name, credentials, business and relative location; latest verified date is **28 September 1917** (`{EID}` / `{SID}`).\n'''
w("people/profiles/w-s-eddy.md", ps)

fb = r("businesses/farr-brothers-store.md")
if MARKER not in fb:
    fb += f'''\n\n## September 1917 continuation\n<!-- {MARKER} -->\n\n**14 September p7** and **28 September p7** market reports visibly credit **Farr Brothers** with Brady Mercantile Company; **14 September p6** separately lists **Farr Bros. (Piezo), $14.00** in County Court expenditure material (`{EID}` / `{SID}`). By contrast, 7 September p7 credits R. Petzold + Brady, and 21 September p7 has no local market-report column. These variations are not closure, sale, ownership-transfer or relocation evidence. No address or individual Farr proprietor is printed; no Edwin/Alice Farr or 505 Main merge is permitted.\n'''
w("businesses/farr-brothers-store.md", fb)

# Human indexes.
people = r("people/people-index.md")
m = re.search(r"(?m)^\| P-396 \|.*$", people)
if m:
    row = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 Fifth-between-Main/Water; 6 Apr–28 Sep 1917 Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. Latest `{EID}` / `{SID}`. |"
    people = people[:m.start()] + row + people[m.end():]
w("people/people-index.md", people)

biz = r("businesses/business-index.md")
m = re.search(r"(?m)^\| BUS-103 \|.*$", biz)
if m:
    row = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–28 Sep 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); no exact number. September extends direct observation through 28 September. Latest `{EID}` / `{SID}`. |"
    biz = biz[:m.start()] + row + biz[m.end():]
if f"| {JCP_BUS} |" not in biz:
    table_anchor = re.search(r"(?m)^\| BUS-103 \|.*$", biz)
    row = f"| {JCP_BUS} | [J. C. Penney Co. / The Golden Rule](j-c-penney-golden-rule.md) | 14 Sep 1917: Main Street between Fifth and Sixth; phone 270 | Direct ad; no number/side/parcel/building assignment. `{EID}` / `{SID}`. |"
    if table_anchor:
        insert = table_anchor.end()
        biz = biz[:insert] + "\n" + row + biz[insert:]
    else:
        biz += "\n" + row + "\n"
if MARKER not in biz:
    biz += f'''\n\n## September 1917 Enterprise continuation\n<!-- {MARKER} -->\n\n`BUS-104` Farr Brothers receives direct 14/28 September market-report credits plus a 14 September county-expenditure appearance; alternating Petzold/Farr provider lines are not treated as business-transfer evidence. `{JCP_BUS}` records the new J. C. Penney/The Golden Rule Main-between-Fifth/Sixth relative-location anchor.\n'''
w("businesses/business-index.md", biz)

append_once("registers/address-register.md", f'''### Main Street between Fifth and Sixth — J. C. Penney / The Golden Rule, 14 September 1917
<!-- {MARKER} -->

`{SID}` / `{EID}` visually verifies a **J. C. Penney Co. / THE GOLDEN RULE** advertisement printing **Main Street Between Fifth and Sixth** and **Phone 270** (`{JCP_BUS}`). This is a direct block-relative location only. No side of Main or numbered address appears; do not allocate 501/503/505/507/509/511 or any parcel/building from this wording.
''')

append_once("timeline.md", f'''## 14 September 1917 — J. C. Penney / The Golden Rule on Main between Fifth and Sixth
<!-- {MARKER} -->

A visually verified *Oregon City Enterprise* p3 advertisement directly prints **J. C. Penney Co. — THE GOLDEN RULE — Main Street Between Fifth and Sixth — Phone 270** (`{JCP_BUS}`, `{EID}` / `{SID}`). This places the business in the Fifth-to-Sixth Main block but does not identify a numbered storefront, side of Main, parcel, owner, lease or building continuity. The same September batch extends W. S. Eddy/Fashion Stable through 28 September and adds Farr Brothers business/supplier observations without an address. No 501/503/505 occupant is established.
''')

bt = r("registers/business-timeline.md")
m = re.search(r"(?m)^\| .*Fashion Stable / W\. S\. Eddy.*BUS-103.*$", bt)
if m:
    row = f"| 6 Apr.–28 Sep. 1917 verified span | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | latest `{EID}` / `{SID}` | Direct relative-location wording; no number or target-building continuity. |"
    bt = bt[:m.start()] + row + bt[m.end():]
if MARKER not in bt:
    bt += f'''\n\n| 14 Sep. 1917 | Main Street between Fifth and Sixth; phone 270 | J. C. Penney Co. / The Golden Rule | `{JCP_BUS}` | `{EID}` / `{SID}` | Direct relative-location ad; no street number or building assignment. |\n| 14 & 28 Sep. 1917 | Address not printed | Farr Brothers market-report/supplier controls | `BUS-104` | `{EID}` / `{SID}` | 14 Sep p6 county expenditure also; provider-line variation does not prove transfer/closure. |\n<!-- {MARKER} -->\n'''
w("registers/business-timeline.md", bt)

append_once("evidence/open-questions.md", f'''## 7 September 2026 — September Enterprise still does not resolve exact 1917 503/505 occupants
<!-- {MARKER} -->

The complete September Enterprise visual batch (`{SID}` / `{EID}`) raises cumulative genuine Enterprise coverage to **312 pages through September** but still does not identify an exact 503 or 505 Main occupant. The new `{JCP_BUS}` block-relative J. C. Penney anchor is explicitly insufficient to assign a target number. Continue the Sohns & Woodbeck Oregon City directory route and remaining October–December Enterprise pages; source silence is not vacancy/non-use evidence.
''')

append_once("evidence/research-leads.md", f'''## 7 September 2026 — J. C. Penney exact-number lead and Enterprise continuation after September
<!-- {MARKER} -->

`{SID}` / `{EID}` directly places **J. C. Penney Co. / The Golden Rule (`{JCP_BUS}`)** on **Main Street between Fifth and Sixth, phone 270**, on 14 September 1917, but no number/side is printed. Seek a 1916–18 directory, telephone listing, business announcement, lease/property notice or another contemporary numbered advertisement before linking it to any 501–511 storefront.

September is complete **32/32**, cumulative **312 genuine Enterprise pages through September**. Continue October 5/12/19/26 using the inventory's actual exposed counts — notably **19 October has six exposed slots**, not eight — and retain the two earlier true-page gaps. Continue Fashion Stable/Farr/target-address checks without interpreting ad or market-report silence as closure.
''')

append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise September audit added 7 September 2026
<!-- {MARKER} -->

`{SID}` / `{EID}` closes September at **32/32 genuine visually verified pages** with no page-identity defect. Enterprise cumulative coverage is **312 genuine pages through September / 314 Jan–Sep slots inspected**; true **16 March p5** and **13 April p8** remain retrieval gaps; **102 exposed October–December slots remain**. Fashion Stable continues through 28 September. Farr Brothers appears directly in 14/28 September market-report credits and 14 September county expenditures, with Petzold/Farr credit variation explicitly not treated as ownership/closure evidence. 14 September p3 adds `{JCP_BUS}` J. C. Penney/The Golden Rule at Main between Fifth/Sixth, phone 270, without a number. No exact target-frontage occupant was established. 1917 remains **IN PROGRESS**.
''')

append_once("indexes/id-crosswalk.md", f'''## {SID} / {EID} — September 1917 Enterprise complete visual batch
<!-- {MARKER} -->

- `{SID}` / `{EID}` → `P-396` / `BUS-103`: Fashion Stable Main-between-Fourth/Fifth observation extended through **28 Sep 1917**.
- `{SID}` / `{EID}` → `BUS-104`: Farr Brothers direct 14/28 Sep market-report credits and 14 Sep county-expenditure appearance; no address/proprietor/505 merge.
- `{SID}` / `{EID}` → `{JCP_BUS}`: J. C. Penney Co. / The Golden Rule, **Main Street between Fifth and Sixth, phone 270**, 14 Sep 1917; no numbered-building assignment.
- No target building/tenancy/ownership event is created from the September no-hit.
''')

append_once("ARCHIVE_INDEX.md", f'''## 1917 Enterprise September complete visual batch
<!-- {MARKER} -->

- [`{CAPTURE}`]({CAPTURE}) — `{SID}` / `{EID}`; **32/32** September pages visually verified; cumulative Enterprise **312 genuine pages through September**.
- New `{JCP_BUS}` J. C. Penney/The Golden Rule Main-between-Fifth/Sixth relative-location anchor; Fashion Stable through 28 Sep; Farr controls on 14/28 Sep; no exact target Main occupant.
''')

yr = r("registers/year-status.md")
lines = yr.splitlines()
for i,line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = f"| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 unresolved. *Oregon City Enterprise*: **312 genuine intended-date pages through September**; 314 Jan–Sep archive slots inspected, with true 16 Mar p5 and true 13 Apr p8 retrieval gaps; **102 Oct–Dec exposed slots remain**. September extends Fashion Stable through 28 Sep, adds Farr business controls, and directly places J. C. Penney/The Golden Rule on Main between Fifth/Sixth without a number; no target-frontage occupant. Title-calendar reconciliation, Sohns & Woodbeck Oregon City directory section, and other source-class closeout remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
w("registers/year-status.md", "\n".join(lines) + ("\n" if yr.endswith("\n") else ""))

append_once("registers/research-log.md", f'''| 2026-09-07 | Completed September 1917 Oregon City Enterprise scan-first visual audit | **32/32 genuine pages** for 7/14/21/28 Sep; cumulative **312 genuine pages through September**, **102 Oct–Dec slots remain**; existing Mar/Apr page gaps unchanged. Fashion Stable continues through 28 Sep; Farr Brothers appears 14/28 Sep plus 14 Sep county expenditures with alternating market-report credits kept non-transfer evidence; created `{JCP_BUS}` for direct J. C. Penney/The Golden Rule Main-between-Fifth/Sixth phone-270 anchor. No exact target occupant. `{SID}` / `{EID}`. Cross-record propagation audit completed. |''')

print(f"Integrated September Enterprise as {SID} / {EID}; JCP={JCP_BUS}")
