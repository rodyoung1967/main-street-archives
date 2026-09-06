from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise June visual closeout — 2026-09-06"
CAPTURE = "evidence/source-captures/1917-enterprise-june-01-29-visual-review-2026-09-06.md"
MANIFEST = "newspapers/oregon-city-enterprise/1917-june/manifest.json"


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


def replace_once(rel, old, new):
    text = r(rel)
    if old in text:
        w(rel, text.replace(old, new, 1))
        return True
    return False


def normalize_yaml_relations(rel, root_key, entity_id, evidence_ids, source_ids):
    text = r(rel)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing {entity_id} in {rel}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    block = text[m.start():end]
    lines = block.splitlines()

    def strip_key(lines, key):
        out=[]; i=0
        while i < len(lines):
            line=lines[i]
            if re.match(rf"^    {re.escape(key)}:\s*", line):
                inline = line.split(":",1)[1].strip()
                i += 1
                if not inline:
                    while i < len(lines) and re.match(r"^\s{4,6}-\s+", lines[i]):
                        i += 1
                continue
            out.append(line); i += 1
        return out

    lines = strip_key(lines, "related_evidence")
    lines = strip_key(lines, "related_sources")
    insert_at = next((i for i,l in enumerate(lines) if l.startswith("    repository_file:")), len(lines))
    lines[insert_at:insert_at] = [
        "    related_evidence: [" + ", ".join(evidence_ids) + "]",
        "    related_sources: [" + ", ".join(source_ids) + "]",
    ]
    newblock = "\n".join(lines)
    if block.endswith("\n"):
        newblock += "\n"
    w(rel, text[:m.start()] + newblock + text[end:])


if not (ROOT / MANIFEST).exists():
    raise SystemExit(f"Required June manifest missing: {MANIFEST}")
retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST], cwd=ROOT, text=True
).strip()

src = r("evidence/source-register.md")
ev = r("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", src)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", ev)]
SID = f"S-{max(source_nums)+1:03d}"
EID = f"E-{max(evidence_nums)+1:03d}"
if (ROOT / CAPTURE).exists():
    cap = r(CAPTURE)
    ms = re.search(r"source `(S-\d{3})`", cap)
    me = re.search(r"evidence `(E-\d{3})`", cap)
    if ms: SID = ms.group(1)
    if me: EID = me.group(1)

capture = f'''# 1917 Oregon City Enterprise — June 1, 8, 15, 22 and 29 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 40/40 genuine intended-date pages. June monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SID}`; evidence `{EID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-june/`  
Retrieval commit: `{retrieval_commit}`  
Manifest: `{MANIFEST}`

## Page-identity audit

All 40 actual page scans for **1, 8, 15, 22 and 29 June 1917** were visually inspected. Each issue contains eight genuine matching-date pages. Printed mastheads and page numbers 1–8 were separately checked because the March and April Enterprise runs exposed source-association defects. **No June substitution, duplicate-page defect or retrieval gap was found.** OCR/text was used only after the scan-first pass as a locator/backstop.

Enterprise cumulative genuine intended-date coverage advances from **168 through May to 208 through June**. The two earlier Enterprise retrieval gaps remain: true **16 March p5** and true **13 April p8**. **206 exposed July–December slots remain**, plus final title-calendar reconciliation.

## Direct June findings

### W. S. Eddy / Fashion Stable continues through 29 June

The professional-directory advertisement on **1, 8, 15, 22 and 29 June p7** directly repeats **W. S. Eddy, V.S., M.D.V.** and states that he is **established at Fashion Stable between Fourth and Fifth on Main Street**. This extends the visually verified 1917 relative-location run from 6 April through **29 June 1917** (`P-396` / `BUS-103`).

No street number is printed. Do not assign Fashion Stable to 427 Main, 106 Fifth, 110 Fifth, or a target Main storefront; do not merge W. S. Eddy with W. B. Eddy.

### Farr Brothers continuation

**22 June p6** includes **Farr Bros.** in the County Court expenditure list. This is a direct dated local-business/supplier appearance, but it prints no address, individual proprietor or new trade description. The stronger 25 May wording remains the direct 1917 **Meat market** description for `BUS-104`. This June item does not connect Farr Brothers to Edwin F. Farr, Alice Farr or Farr's Pool Hall at 505 Main.

### Other controls and target-frontage result

Jones Drug Co. appears in June advertising/expenditure material without an exact street number; the existing direct 617 Main observations remain the controlling exact-address evidence. Other Main/Fifth references in the month concern unrelated civic, road, legal or geographic contexts.

Across all **40 genuine June pages**, no defensible exact **501, 503, 505, 507, 509 or 511 Main** occupant and no new exact **427 Main** occupant was established. This is bounded coverage only — not vacancy, non-use, demolition or absence evidence.

## Cross-record propagation audit

Reviewed: 501/503/505 building/timeline records; 427 Main controls; W. S. Eddy/Fashion Stable records; Farr Brothers/Farr identity controls; people/business indexes and YAML; master/business timelines; source/evidence registers and YAML; open questions; research leads; annual status; archive index; crosswalk and research log.

Propagation decision:
- extend `P-396` / `BUS-103` Fashion Stable's direct Main-between-Fourth/Fifth observation through **29 June 1917**;
- add the 22 June Farr Bros. expenditure appearance to `BUS-104` without creating a new address, proprietor or 505 relationship;
- do **not** add a 1917 501/503/505 occupant/building event because June establishes none.

## Status

**June Enterprise monthly batch is closed: 40/40 visually verified.** 1917 remains **IN PROGRESS** with **208 genuine intended-date Enterprise pages through June**, the two earlier Enterprise page gaps, and **206 July–December exposed slots** still to review. Courier, directory and other-source blockers remain separately active.
'''
if not (ROOT / CAPTURE).exists():
    w(CAPTURE, capture)

append_once("evidence/source-register.md", f'''## {SID} — Oregon City Enterprise, June 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **40/40 genuine intended-date pages visually verified**.  
Issue dates: 1, 8, 15, 22 and 29 June 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-06-29/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-june/`; manifest `{MANIFEST}`; retrieval commit `{retrieval_commit}`.  
Evidence: `{EID}`; capture: `{CAPTURE}`.  
Notes: W. S. Eddy/Fashion Stable repeats through 29 June at Main between Fourth/Fifth; 22 June repeats Farr Bros. in county expenditures. No exact target Main occupant.''')

append_once("evidence/evidence-register.md", f'''## {EID} — June 1917 Enterprise closes 40-page batch and extends Fashion Stable through June 29
<!-- {MARKER} -->
Source: `{SID}`  
Type: Primary newspaper visual review  
Claims:
- all **40/40 June scans** are visually verified genuine intended-date pages;
- Enterprise cumulative genuine coverage is **208 pages through June**, with **206 July–December exposed slots remaining**;
- 1/8/15/22/29 June p7 directly repeat W. S. Eddy / Fashion Stable **between Fourth and Fifth on Main Street**, extending the verified 1917 observation through 29 June;
- 22 June p6 directly includes Farr Bros. in County Court expenditures but prints no address, proprietor or new trade description;
- no exact 501/503/505/507/509/511 Main or new 427 Main occupant was established.
Classification: **DOCUMENTED / DIRECT** for page identity and printed Fashion Stable/Farr wording; **COVERAGE RESULT ONLY** for the target-address no-hit.  
Confidence: **Very High**, with exact-number, identity and continuity limits preserved.''')

# Add synchronized YAML source/evidence records.
text = r("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(SID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {SID}\n    name: "Oregon City Enterprise, June 1917 complete scan-first visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-06-29/ed-1/"\n    type: "Primary newspaper page scans; 40/40 genuine pages visually verified"\n    date: "1917-06-01 through 1917-06-29"\n    repository_file: "{CAPTURE}"\n    notes: "June complete; Fashion Stable continues through 29 June and Farr Bros. appears in 22 June county expenditures; no exact target Main occupant."\n    related_evidence: [{EID}]\n'''
    w("database/sources.yml", text)
text = r("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(EID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {EID}\n    name: "June 1917 Enterprise closes 40-page batch and extends Fashion Stable through June 29"\n    type: "Primary newspaper visual review"\n    date: "1917-06-01 through 1917-06-29"\n    claims:\n      - "All 40 June pages visually verified."\n      - "Enterprise cumulative genuine coverage: 208 pages through June; 206 July-December slots remain."\n      - "1/8/15/22/29 June p7 repeat W. S. Eddy/Fashion Stable between Fourth and Fifth on Main Street."\n      - "22 June p6 includes Farr Bros. in County Court expenditures without address or named proprietor."\n      - "No exact target Main occupant established in June."\n    confidence: "Very High for visible wording and counts; inference limits retained."\n    related_businesses: [BUS-103, BUS-104]\n    related_people: [P-396]\n    related_sources: [{SID}]\n'''
    w("database/evidence.yml", text)

# Entity pages.
fs = r("businesses/fashion-stable.md")
fs = fs.replace("**6 April–25 May 1917:** repeated ads place Fashion Stable", "**6 April–29 June 1917:** repeated ads place Fashion Stable")
fs = fs.replace("(`E-252` / `S-279`; continued `E-253` / `S-280`).", f"(`E-252` / `S-279`; continued `E-253` / `S-280` and `{EID}` / `{SID}`).")
if MARKER not in fs:
    fs += f'''\n\n## June continuation\n<!-- {MARKER} -->\n\nAds on 1, 8, 15, 22 and 29 June p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street, extending the verified 1917 span through **29 June** (`{EID}` / `{SID}`). No exact number is printed.\n'''
w("businesses/fashion-stable.md", fs)

ps = r("people/profiles/w-s-eddy.md")
ps = ps.replace("**6 April–25 May 1917:** repeated visually reviewed professional ads", "**6 April–29 June 1917:** repeated visually reviewed professional ads")
ps = ps.replace("(`E-252` / `S-279`; continued `E-253` / `S-280`).", f"(`E-252` / `S-279`; continued `E-253` / `S-280` and `{EID}` / `{SID}`).")
if MARKER not in ps:
    ps += f'''\n\n## June continuation\n<!-- {MARKER} -->\n\nThe 1/8/15/22/29 June p7 advertisements repeat the same name, credentials, business and relative location; latest verified date is **29 June 1917** (`{EID}` / `{SID}`).\n'''
w("people/profiles/w-s-eddy.md", ps)

fb = r("businesses/farr-brothers-store.md")
if MARKER not in fb:
    fb += f'''\n\n## June 1917 continuation\n<!-- {MARKER} -->\n\n**22 June p6** includes **Farr Bros.** in County Court expenditures (`{EID}` / `{SID}`). This confirms another dated local supplier/business appearance but supplies no address, individual proprietor or new trade type. The 25 May **Meat market** wording remains the stronger 1917 business-type observation.\n'''
w("businesses/farr-brothers-store.md", fb)

# Repair/extend index rows.
people = r("people/people-index.md")
mp = re.search(r"(?m)^\| P-396 \|.*$", people)
if mp:
    row = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 Fifth-between-Main/Water; 6 Apr–29 Jun 1917 Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. `E-252` / `S-279`; `E-253` / `S-280`; `{EID}` / `{SID}`. |"
    people = people[:mp.start()] + row + people[mp.end():]
w("people/people-index.md", people)

biz = r("businesses/business-index.md")
mb = re.search(r"(?m)^\| BUS-103 \|.*$", biz)
if mb:
    row = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–29 Jun 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); no exact number. June ads extend direct observation through 29 June. `E-252` / `S-279`; `E-253` / `S-280`; `{EID}` / `{SID}`. |"
    biz = biz[:mb.start()] + row + biz[mb.end():]
if MARKER not in biz:
    biz += f'''\n\n## June 1917 Enterprise continuation\n<!-- {MARKER} -->\n\n`BUS-104` Farr Brothers receives a second 1917 dated observation: 22 June p6 County Court expenditures include **Farr Bros.** (`{EID}` / `{SID}`), without address or new trade description. No 505 Main relationship is inferred.\n'''
w("businesses/business-index.md", biz)

# Normalize YAML relationship fields and remove duplicate-key artifacts from the May integration.
normalize_yaml_relations("database/businesses.yml", "businesses", "BUS-103", ["E-112","E-114","E-252","E-253",EID], ["S-124","S-128","S-279","S-280",SID])
normalize_yaml_relations("database/businesses.yml", "businesses", "BUS-104", ["E-253",EID], ["S-280",SID])
normalize_yaml_relations("database/people.yml", "people", "P-396", ["E-112","E-114","E-252","E-253",EID], ["S-124","S-128","S-279","S-280",SID])

# Master/business chronology.
append_once("timeline.md", f'''## 29 June 1917 — Fashion Stable relative-location observation continues
<!-- {MARKER} -->

The 1/8/15/22/29 June *Oregon City Enterprise* p7 professional ads continue to place **W. S. Eddy (`P-396`) / Fashion Stable (`BUS-103`) between Fourth and Fifth on Main Street**, extending the direct 1917 observation through **29 June** (`{EID}` / `{SID}`). No exact street number, ownership or physical-building continuity is established. The separate W. B. Eddy/427 Main identity remains unmerged.''')

bt = r("registers/business-timeline.md")
# Update the existing 1917 Fashion Stable chronology row if present.
bt = re.sub(
    r"(?m)^\| 6–27 Apr\. 1917 \| Main Street between Fourth and Fifth \| Fashion Stable / W\. S\. Eddy \| `BUS-103` / `P-396` \| `E-252` / `S-279` \| Repeated direct ads; exact move day/number unresolved\. Not W\. B\. Eddy/427 by assumption\. \|$",
    f"| 6 Apr.–29 Jun. 1917 | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252` / `S-279`; `E-253` / `S-280`; `{EID}` / `{SID}` | Repeated direct ads; exact move day/number unresolved. Not W. B. Eddy/427 by assumption. |",
    bt,
)
# Catch the May-updated row wording too.
bt = re.sub(
    r"(?m)^\| 6 Apr[.–]+25 May 1917 \| Main Street between Fourth and Fifth \| Fashion Stable / W\. S\. Eddy \|.*$",
    f"| 6 Apr.–29 Jun. 1917 | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252` / `S-279`; `E-253` / `S-280`; `{EID}` / `{SID}` | Repeated direct ads; exact move day/number unresolved. Not W. B. Eddy/427 by assumption. |",
    bt,
)
if MARKER not in bt:
    bt += f'''\n\n### June 1917 Farr Brothers continuation\n<!-- {MARKER} -->\n\n| Date | Address / location | Business | Evidence | Limits |\n| --- | --- | --- | --- | --- |\n| 22 Jun. 1917 | Oregon City; exact address not printed | Farr Bros. (`BUS-104`) | `{EID}` / `{SID}` | County Court expenditure appearance only; no proprietor, new trade type or 505 relationship. |\n'''
w("registers/business-timeline.md", bt)

# Leads/open questions/status/log/crosswalk.
append_once("evidence/research-leads.md", f'''## 6 September 2026 — June Enterprise extends Fashion Stable observation
<!-- {MARKER} -->

`{SID}` / `{EID}` extends the direct W. S. Eddy / Fashion Stable **Main-between-Fourth/Fifth** observation through **29 June 1917**. Continue searching move notices, directories, licenses and property records for the transition from the 1915 Fifth-between-Main/Water location. The longer 1917 span still supplies no exact number and does not bridge W. S. Eddy to W. B. Eddy/427 Main. June's Farr Bros. expenditure appearance likewise supplies no 505 Main bridge.''')

append_once("evidence/open-questions.md", f'''## 6 September 2026 — June Enterprise narrowing
<!-- {MARKER} -->

June is complete **40/40** under `{SID}` / `{EID}`. The exact 503/505 occupant question remains open: no target-number occupant was established. Fashion Stable's Main-between-Fourth/Fifth wording now persists through **29 June 1917**, narrowing its 1917 state but not its exact address. Continue with July Enterprise using the same printed-date/page-number audit.''')

append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise June audit added 6 September 2026
<!-- {MARKER} -->

`{SID}` / `{EID}` closes June at **40/40 genuine visually verified pages** with no June page-identity gap. Enterprise cumulative coverage is **208 genuine intended-date pages through June**; the prior March/April gaps remain and **206 exposed July–December slots** are pending. June extends W. S. Eddy/Fashion Stable at Main between Fourth/Fifth through 29 June and adds a Farr Bros. expenditure appearance without address. No exact target Main occupant was established; silence is not vacancy evidence.''')

append_once("indexes/id-crosswalk.md", f'''## {SID} / {EID} — June 1917 Enterprise continuation
<!-- {MARKER} -->

| Source / evidence | Related entities | Relationship |\n| --- | --- | --- |\n| `{SID}` / `{EID}` | `P-396`, `BUS-103` | Five June p7 ads continue W. S. Eddy / Fashion Stable at Main between Fourth and Fifth through 29 June; no number. |\n| `{SID}` / `{EID}` | `BUS-104` | 22 June p6 County Court expenditures include Farr Bros.; no address/proprietor/new trade description. |''')

append_once("registers/research-log.md", f'''### 2026-09-06 — closed June 1917 Enterprise visual batch
<!-- {MARKER} -->

- Visually reviewed **40/40 genuine pages** for 1/8/15/22/29 June; no June page-association gap.
- Enterprise cumulative genuine coverage is **208 pages through June**; **206 July–December exposed slots remain**. Earlier 16 Mar p5 and 13 Apr p8 gaps remain.
- `{SID}` / `{EID}` extend W. S. Eddy / Fashion Stable at Main between Fourth/Fifth through 29 June and add a 22 June Farr Bros. County Court expenditure appearance.
- No exact 501/503/505/507/509/511 or new 427 Main occupant was established. This is bounded coverage, not vacancy evidence.''')

# Canonical year status.
yr = r("registers/year-status.md")
newrow = f'| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 unresolved. *Oregon City Enterprise*: **208 genuine intended-date pages through June**; 210 Jan–Jun archive slots inspected, with true 16 Mar p5 and true 13 Apr p8 retrieval gaps; **206 July–Dec exposed slots remain**. June extends W. S. Eddy/Fashion Stable through 29 Jun and adds a Farr Bros. expenditure control; no target-frontage occupant. Title-calendar reconciliation, Sohns & Woodbeck Oregon City directory section, and other source-class closeout remain unresolved. |'
yr2,n = re.subn(r'^\| 1917 \| \*\*IN PROGRESS\*\* \|.*$', newrow, yr, count=1, flags=re.M)
if n != 1:
    raise SystemExit("Could not update 1917 year-status row")
w("registers/year-status.md", yr2)

ai = r("ARCHIVE_INDEX.md")
ai2,n = re.subn(
    r'^- \*\*1917 — IN PROGRESS:\*\*.*$',
    f'- **1917 — IN PROGRESS:** Courier 435 genuine pages with true 13 Dec p21 unresolved; Enterprise **208 genuine intended-date pages through June**, with true 16 Mar p5 and 13 Apr p8 gaps and **206 July–December exposed slots remaining**. June extends W. S. Eddy/Fashion Stable through 29 June and adds a Farr Bros. expenditure control; no exact target Main occupant.',
    ai, count=1, flags=re.M,
)
if n:
    w("ARCHIVE_INDEX.md", ai2)

print(f"June closeout integration finished: {SID} {EID}")
