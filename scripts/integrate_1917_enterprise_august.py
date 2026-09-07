from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1917 Enterprise August visual closeout — 2026-09-07"
CAPTURE = "evidence/source-captures/1917-enterprise-august-03-31-visual-review-2026-09-07.md"
MANIFEST = "newspapers/oregon-city-enterprise/1917-august/manifest.json"
COURIER_AUG = "evidence/source-captures/1917-courier-august-issue-inventory.md"


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
    srcs, lines = collect_and_strip("\n".join(lines), "related_sources")
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
    raise SystemExit(f"Required August manifest missing: {MANIFEST}")

retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST], cwd=ROOT, text=True
).strip()

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

capture = f'''# 1917 Oregon City Enterprise — August 3, 10, 17, 24 and 31 visual review

<!-- {MARKER} -->

Status: **VISUALLY VERIFIED — 40/40 genuine intended-date pages. August monthly Enterprise batch complete; annual 1917 review remains IN PROGRESS.**

Archive IDs: source `{SID}`; evidence `{EID}`.

Preserved originals: `newspapers/oregon-city-enterprise/1917-august/`  
Retrieval commit: `{retrieval_commit}`  
Manifest: `{MANIFEST}`

## Page-identity audit

All 40 actual page scans for **3, 10, 17, 24 and 31 August 1917** were visually inspected. Each issue contains eight genuine matching-date pages. Printed issue dates and printed page numbers 1–8 were separately checked because March and April exposed archive page-association defects. **No August substitution, duplicate-page defect or retrieval gap was found.** OCR/text was used only after the scan-first pass as a small-print locator/backstop.

Enterprise cumulative genuine intended-date coverage advances from **240 through July to 280 through August**. The January–August archive-slot audit is **282 slots inspected / 280 genuine intended-date pages**, with the two previously documented true-page retrieval gaps unchanged: **16 March p5** and **13 April p8**. **134 exposed September–December slots remain**, plus final title-calendar reconciliation.

## Direct August findings

### W. S. Eddy / Fashion Stable continues through 31 August

The professional-directory advertisement on **3, 10, 17, 24 and 31 August p7** directly repeats **W. S. Eddy, V.S., M.D.V.** at **Fashion Stable, between Fourth and Fifth on Main Street**. This extends the visually verified 1917 relative-location run from 6 April through **31 August 1917** (`P-396` / `BUS-103`).

No street number is printed. Do not assign Fashion Stable to 427 Main, a numbered Fifth Street premise, or 501/503/505; do not merge W. S. Eddy with W. B. Eddy.

### Farr Brothers market-report continuation and August 31 credit change

The market report on **3, 10, 17 and 24 August p7** says it is furnished by **Farr Bros.** and Brady Mercantile Company. On **31 August p7**, the provider line instead names **R. Petzold and Brady Mercantile Company**.

The four Farr credits are direct dated business appearances for `BUS-104`, but they print no Farr street address or individual proprietor. The **31 August provider change is not closure, sale, relocation or non-operation evidence for Farr Brothers**; it proves only that this particular published market-report credit changed by that issue. The 25 May wording remains the direct 1917 **Meat market** description. No bridge to Edwin F. Farr, Alice Farr, Farr's Pool Hall at 505 Main, Carl Harr or Harr's Recreation Center is established.

### Mrs. J. C. Napier — visual correction to 512½ Main

**3 August p5** directly prints **Mrs. J. C. Napier, of 512½ Main street** in the article about household food preservation. A fresh visual reinspection of the already preserved **2 August Oregon City Courier p1** shows the same wording: **Mrs. J. C. Napier, of 512½ Main street**.

The older Courier August inventory summary had incorrectly written **612 Main** for Mrs. Napier because the source OCR dropped/misread the leading `5` and half-address. The underlying scan controls. This batch corrects that repository transcription to **512½ Main** while retaining the separate **612 Main** optometrist advertisement noted in the Courier issue. This is an opposite-side/adjacent address control only; no building continuity or relationship to 501/503/505 is inferred.

### Adams Department Store closing-out context

**31 August p8** visibly carries an **Adams Department Store** advertisement headed **GOING OUT OF BUSINESS** / closing-out sale language. The advertisement does not print a street number. It is retained as dated business/closure-advertising context only and is not assigned to a target building. Later Courier evidence already records Adams building-change language; this August page does not independently establish the store's address, legal closure date, ownership, demolition site or target-building identity.

### Target frontage result

Across all **40 genuine August pages**, the scan-first review and follow-up text checks did not recover a defensible exact occupant for **501, 503, 505, 507, 509 or 511 Main**, nor a new exact **427 Main** occupant or new numbered Fifth Street target occupant. Personal-name references to George A. Harding and others were not converted into business/address evidence. No usable pool-room/billiard exact-address hit was recovered.

This is a **bounded coverage statement only**. It is not evidence of vacancy, non-use, closure, demolition, relocation or absence at any target address.

## Cross-Record Propagation Audit

Explicitly reviewed after the verified August batch:

- source/evidence registers and database YAML;
- master and business timelines;
- 501/503/505 building pages and unified timelines;
- 427 Main and numbered Fifth Street controls;
- W. S. Eddy / Fashion Stable person/business pages, indexes and YAML;
- Farr Brothers Store / Meat Market and Farr identity controls;
- Courier August capture and address register for the 512½/612 transcription correction;
- open questions and research leads;
- business/address registers;
- ID crosswalk and archive index;
- annual year status and research log.

Propagation decision:

- extend `P-396` / `BUS-103` Fashion Stable's direct Main-between-Fourth/Fifth observation through **31 August 1917**;
- add the **3/10/17/24 August Farr Bros.** market-report credits to `BUS-104`, while treating the 31 August provider change only as a change in that published credit;
- correct the older Courier summary from **Mrs. Napier at 612 Main** to the visually verified **512½ Main**, keeping the separate 612 Main optometrist control distinct;
- retain Adams Department Store's 31 August closing-out advertisement as unnumbered business context only;
- advance the Enterprise annual audit to **280 genuine pages through August**, with **134 exposed September–December slots remaining** and the two earlier true-page gaps unchanged;
- do **not** add a 1917 target-building occupant/event to 501/503/505, 427 Main or the numbered Fifth Street building records because August establishes none;
- do **not** close the 1917 503/505 occupant question.

## Status and next step

**August Enterprise monthly batch is closed: 40/40 visually verified genuine intended-date pages.** 1917 remains **IN PROGRESS** with the Courier true-page gap, the two Enterprise true-page gaps, the unrecovered Sohns & Woodbeck Oregon City directory section, remaining Enterprise September–December pages, title-calendar reconciliation and other-source closeout work still active.

The next chronological online newspaper step is **September 1917 Oregon City Enterprise**, beginning with the exposed 7 September issue after verifying the September inventory/page counts.
'''

if not (ROOT / CAPTURE).exists():
    w(CAPTURE, capture)

append_once("evidence/source-register.md", f'''## {SID} — Oregon City Enterprise, August 1917 complete scan-first visual-review batch
<!-- {MARKER} -->
Type: Primary newspaper page scans; **40/40 genuine intended-date pages visually verified**.  
Issue dates: 3, 10, 17, 24 and 31 August 1917.  
Representative URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1917-08-31/ed-1/  
Preserved originals: `newspapers/oregon-city-enterprise/1917-august/`; manifest `{MANIFEST}`; retrieval commit `{retrieval_commit}`.  
Evidence: `{EID}`; capture: `{CAPTURE}`.  
Notes: Fashion Stable repeats through 31 August; Farr Bros. market-report credits continue through 24 August; 31 August provider line changes to R. Petzold + Brady Mercantile; Mrs. J. C. Napier directly prints at 512½ Main; no exact target Main occupant.''')

append_once("evidence/evidence-register.md", f'''## {EID} — August 1917 Enterprise closes 40-page batch and extends Fashion Stable through August 31
<!-- {MARKER} -->
Source: `{SID}`  
Type: Primary newspaper visual review  
Claims:
- all **40/40 August scans** are genuine intended-date pages with no August page-association defect;
- Enterprise cumulative genuine coverage is **280 pages through August**; **282 Jan–Aug archive slots** inspected; existing March/April true-page gaps unchanged; **134 September–December exposed slots remain**;
- 3/10/17/24/31 August p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street;
- 3/10/17/24 August p7 credit Farr Bros. + Brady Mercantile for the market report; 31 August credits R. Petzold + Brady Mercantile, a provider-line change only;
- 3 August p5 directly prints Mrs. J. C. Napier at **512½ Main**, corroborating fresh visual reinspection of 2 August Courier p1 and correcting the older 612 transcription;
- 31 August p8 carries an unnumbered Adams Department Store going-out-of-business/closing-out advertisement;
- no exact 501/503/505/507/509/511 Main, new 427 Main, or new numbered Fifth Street target occupant was established.
Classification: **DOCUMENTED / DIRECT** for scan identity and printed wording; **CORRECTION** for the Napier 512½ transcription; **COVERAGE RESULT ONLY** for target-address no-hit.  
Confidence: **Very High**, with exact-number, individual-identity, closure and continuity limits preserved.''')

text = r("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(SID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {SID}\n    name: "Oregon City Enterprise, August 1917 complete scan-first visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1917-08-31/ed-1/"\n    type: "Primary newspaper page scans; 40/40 genuine pages visually verified"\n    date: "1917-08-03 through 1917-08-31"\n    repository_file: "{CAPTURE}"\n    notes: "August complete; Fashion Stable through 31 Aug; Farr market credits through 24 Aug; Napier 512½ Main visual correction; no exact target Main occupant."\n    related_evidence: [{EID}]\n'''
    w("database/sources.yml", text)

text = r("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(EID)}$", text):
    text = text.rstrip() + f'''\n\n  - id: {EID}\n    name: "August 1917 Enterprise closes 40-page batch and extends Fashion Stable through August 31"\n    type: "Primary newspaper visual review"\n    date: "1917-08-03 through 1917-08-31"\n    claims:\n      - "All 40 August pages visually verified as genuine intended-date pages."\n      - "Enterprise cumulative genuine coverage: 280 pages through August; 134 September-December slots remain; March and April true-page gaps unchanged."\n      - "3/10/17/24/31 August p7 repeat W. S. Eddy/Fashion Stable between Fourth and Fifth on Main Street."\n      - "3/10/17/24 August p7 credit Farr Bros. and Brady Mercantile; 31 August changes the market-report provider line to R. Petzold and Brady Mercantile."\n      - "3 August p5 and fresh visual reinspection of 2 August Courier p1 print Mrs. J. C. Napier at 512½ Main; older 612 summary corrected."\n      - "31 August p8 has unnumbered Adams Department Store closing-out advertising."\n      - "No exact target Main or new numbered Fifth target occupant established in August."\n    confidence: "Very High for visible wording and counts; inference limits retained."\n    related_businesses: [BUS-103, BUS-104]\n    related_people: [P-396]\n    related_sources: [{SID}]\n'''
    w("database/evidence.yml", text)

ct = r(COURIER_AUG)
old = "The 2 Aug issue contains a separately useful numbered-address item at **612 Main** (Mrs. J. C. Napier, in a household-canning story) and a 612 Main optometrist advertisement. These are on the even-numbered side and do not resolve the target block."
new = "The 2 Aug issue contains a separately useful numbered-address item at **512½ Main** (Mrs. J. C. Napier, in a household-canning story) and a separate **612 Main** optometrist advertisement. Fresh scan reinspection on 7 September 2026 corrected the prior `612 Main` Napier transcription: the printed article visibly reads **512½ Main street**; OCR had misread the half-address. These opposite-side controls do not resolve the target block."
if old in ct:
    ct = ct.replace(old, new, 1)
elif "Mrs. J. C. Napier" in ct and "512½ Main" not in ct:
    raise SystemExit("Courier Napier summary changed unexpectedly; manual reconciliation required")
if MARKER not in ct:
    ct += f'''\n\n## 7 September 2026 visual correction — Mrs. J. C. Napier\n<!-- {MARKER} -->\n\nFresh visual reinspection of preserved **2 August 1917 p1** confirms **Mrs. J. C. Napier, of 512½ Main street**. The prior summary's 612 attribution came from OCR/transcription error. A separate 612 Main optometrist advertisement remains valid and distinct. The 3 August Enterprise p5 independently prints the same **512½ Main** Napier address (`{EID}` / `{SID}`).\n'''
w(COURIER_AUG, ct)

fs = r("businesses/fashion-stable.md")
fs = fs.replace("**6 April–27 July 1917:**", "**6 April–31 August 1917:**")
fs = fs.replace("continued `E-260` / `S-286`).", f"continued `E-260` / `S-286` and `{EID}` / `{SID}`).")
if MARKER not in fs:
    fs += f'''\n\n## August continuation\n<!-- {MARKER} -->\n\nAds on 3, 10, 17, 24 and 31 August p7 repeat W. S. Eddy / Fashion Stable between Fourth and Fifth on Main Street, extending the verified 1917 span through **31 August** (`{EID}` / `{SID}`). No exact number is printed.\n'''
w("businesses/fashion-stable.md", fs)

ps = r("people/profiles/w-s-eddy.md")
ps = ps.replace("**6 April–27 July 1917:**", "**6 April–31 August 1917:**")
ps = ps.replace("continued `E-260` / `S-286`).", f"continued `E-260` / `S-286` and `{EID}` / `{SID}`).")
if MARKER not in ps:
    ps += f'''\n\n## August continuation\n<!-- {MARKER} -->\n\nThe 3/10/17/24/31 August p7 advertisements repeat the same name, credentials, business and relative location; latest verified date is **31 August 1917** (`{EID}` / `{SID}`).\n'''
w("people/profiles/w-s-eddy.md", ps)

fb = r("businesses/farr-brothers-store.md")
if MARKER not in fb:
    fb += f'''\n\n## August 1917 continuation\n<!-- {MARKER} -->\n\nThe market report on **3, 10, 17 and 24 August p7** says it is furnished by **Farr Bros.** and Brady Mercantile Company (`{EID}` / `{SID}`). On **31 August p7** the provider line changes to **R. Petzold and Brady Mercantile Company**. The change is evidence only about that published report credit; it does not prove Farr Brothers closed, sold, relocated or ceased operating. No address or individual Farr proprietor is printed, and no Edwin/Alice Farr or 505 Main merge is permitted.\n'''
w("businesses/farr-brothers-store.md", fb)

people = r("people/people-index.md")
m = re.search(r"(?m)^\| P-396 \|.*$", people)
if m:
    row = f"| P-396 | [W. S. Eddy](profiles/w-s-eddy.md) | Veterinarian / Fashion Stable professional | 1915 Fifth-between-Main/Water; 6 Apr–31 Aug 1917 Main between Fourth/Fifth. Exact move date/number unresolved; not merged with W. B. Eddy. `E-252` / `S-279`; `E-253` / `S-280`; `E-254` / `S-281`; `E-260` / `S-286`; `{EID}` / `{SID}`. |"
    people = people[:m.start()] + row + people[m.end():]
w("people/people-index.md", people)

biz = r("businesses/business-index.md")
m = re.search(r"(?m)^\| BUS-103 \|.*$", biz)
if m:
    row = f"| BUS-103 | [Fashion Stable](fashion-stable.md) | 1915 Fifth between Main/Water; 6 Apr–31 Aug 1917 Main between Fourth/Fifth | W. S. Eddy (`P-396`); no exact number. August ads extend direct observation through 31 August. `E-252` / `S-279`; `E-253` / `S-280`; `E-254` / `S-281`; `E-260` / `S-286`; `{EID}` / `{SID}`. |"
    biz = biz[:m.start()] + row + biz[m.end():]
if MARKER not in biz:
    biz += f'''\n\n## August 1917 Enterprise continuation\n<!-- {MARKER} -->\n\n`BUS-104` Farr Brothers receives direct market-report credits on 3/10/17/24 August p7 (`{EID}` / `{SID}`). The 31 August provider line names R. Petzold + Brady Mercantile instead; this is not treated as a Farr closure/sale/relocation. No address or `BUS-013` / 505 merge.\n'''
w("businesses/business-index.md", biz)

for rel, ent in [
    ("database/businesses.yml", "BUS-103"),
    ("database/businesses.yml", "BUS-104"),
    ("database/people.yml", "P-396"),
]:
    update_entity_relations(rel, ent, EID, SID)

append_once("timeline.md", f'''## 3–31 August 1917 — Enterprise continuation and 512½ Main address correction
<!-- {MARKER} -->

Five visually verified August professional ads extend **W. S. Eddy (`P-396`) / Fashion Stable (`BUS-103`) at Main between Fourth and Fifth** through **31 August 1917** (`{EID}` / `{SID}`). Farr Bros. receives market-report credits on 3/10/17/24 August; the 31 August credit instead names R. Petzold + Brady Mercantile, a provider-line change only. **3 August p5 directly prints Mrs. J. C. Napier at 512½ Main**, matching fresh visual reinspection of 2 August Courier p1 and correcting an older 612 transcription. Adams Department Store has an unnumbered going-out-of-business ad on 31 August p8. None of these observations establishes a 501/503/505 occupant.
''')

bt = r("registers/business-timeline.md")
m = re.search(r"(?m)^\| .*Fashion Stable / W\. S\. Eddy.*BUS-103.*$", bt)
if m:
    row = f"| 6 Apr.–31 Aug. 1917 verified span | Main Street between Fourth and Fifth | Fashion Stable / W. S. Eddy | `BUS-103` / `P-396` | `E-252`, `E-253`, `E-254`, `E-260`, `{EID}`; `S-279`, `S-280`, `S-281`, `S-286`, `{SID}` | Direct relative-location wording; no street number, move date, lease, ownership, or target-building continuity. |"
    bt = bt[:m.start()] + row + bt[m.end():]
if MARKER not in bt:
    bt += f'''\n\n| 3–24 Aug. 1917 | Not printed | Farr Bros. market-report credits with Brady Mercantile | `BUS-104` | `{EID}` / `{SID}` | Dated business appearances only; 31 Aug provider line changes to R. Petzold + Brady Mercantile; no closure inference, address or named proprietor. |\n<!-- {MARKER} -->\n'''
w("registers/business-timeline.md", bt)

append_once("registers/address-register.md", f'''### 512½ Main Street — August 1917 direct address control
<!-- {MARKER} -->

Fresh visual review confirms **Mrs. J. C. Napier at 512½ Main street** in both the 2 August *Oregon City Courier* p1 and 3 August *Oregon City Enterprise* p5 (`{EID}` / `{SID}` for the Enterprise batch; Courier monthly-sample source already registered). This corrects an older repository summary that wrote 612 Main for Napier after OCR misread the half-address. A separate 612 Main optometrist advertisement remains distinct. This establishes a dated address use only, not parcel/building continuity or a relationship to 501/503/505.
''')

append_once("evidence/open-questions.md", f'''## 7 September 2026 — 1917 Enterprise August coverage does not resolve 503/505 occupancy
<!-- {MARKER} -->

The complete August Enterprise visual batch (`{SID}` / `{EID}`) raises cumulative genuine Enterprise coverage to **280 pages through August** but does **not** identify an exact 503 or 505 Main occupant. This is bounded source coverage, not vacancy/non-use evidence. The 1917 occupant question remains open; the Sohns & Woodbeck Oregon City directory section and remaining Enterprise September–December pages remain material routes.
''')

append_once("evidence/research-leads.md", f'''## 7 September 2026 — Enterprise continuation after August
<!-- {MARKER} -->

August is complete **40/40** (`{SID}` / `{EID}`), cumulative **280 genuine Enterprise pages through August**. Continue with **September 7/14/21/28**, verifying the actual exposed issue/page inventory first. Preserve the March/April true-page gaps and the 1916–17 Sohns & Woodbeck Oregon City directory gap. Continue target-address, pool-room, Fashion Stable and Farr identity checks with the same scan-first/no-merge rules. The 31 August Farr market-report credit change is not a closure event unless an independent source explicitly says so.
''')

append_once("evidence/source-captures/1917-closeout.md", f'''## Enterprise August audit added 7 September 2026
<!-- {MARKER} -->

`{SID}` / `{EID}` closes August at **40/40 genuine visually verified pages**, with no August page-identity defect. Enterprise cumulative genuine coverage is **280 pages through August**; **282 Jan–Aug archive slots** have been inspected, the true **16 March p5** and **13 April p8** retrieval gaps remain, and **134 exposed September–December slots** remain. W. S. Eddy / Fashion Stable continues through 31 August at Main between Fourth/Fifth; Farr Bros. market-report credits continue through 24 August, with the 31 August provider-line change explicitly not treated as closure evidence. Fresh scan review corrects Mrs. J. C. Napier to **512½ Main** in both Courier and Enterprise. No exact 501/503/505/507/509/511 or new 427 Main occupant was established. Coverage only; 1917 remains **IN PROGRESS**.
''')

append_once("indexes/id-crosswalk.md", f'''## {SID} / {EID} — August 1917 Enterprise complete visual batch
<!-- {MARKER} -->

- `{SID}` / `{EID}` → `P-396` / `BUS-103`: Fashion Stable Main-between-Fourth/Fifth observation extended through **31 Aug 1917**.
- `{SID}` / `{EID}` → `BUS-104`: Farr Bros. market-report credits on 3/10/17/24 Aug; 31 Aug provider-line change does not establish closure/sale/relocation.
- `{SID}` / `{EID}` → address register: 3 Aug p5 directly prints Mrs. J. C. Napier at **512½ Main**, corroborating reinspection of the already registered 2 Aug Courier source and correcting its older summary transcription.
- No target building, tenancy, ownership or 505 Farr/Harr bridge is created by this batch.
''')

append_once("ARCHIVE_INDEX.md", f'''## 1917 Enterprise August complete visual batch
<!-- {MARKER} -->

- [`{CAPTURE}`]({CAPTURE}) — `{SID}` / `{EID}`; **40/40** August pages visually verified; cumulative Enterprise **280 genuine pages through August**.
- Fashion Stable / W. S. Eddy extends through 31 August; Farr Bros. market-report credits through 24 August; Napier address corrected to 512½ Main; no exact target Main occupant.
''')

yr = r("registers/year-status.md")
lines = yr.splitlines()
for i, line in enumerate(lines):
    if line.startswith("| 1917 |"):
        lines[i] = f"| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `{CAPTURE}` | *Courier*: all 52 issue dates inventoried, **435 genuine pages visually verified**, true 13 Dec p21 unresolved. *Oregon City Enterprise*: **280 genuine intended-date pages through August**; 282 Jan–Aug archive slots inspected, with true 16 Mar p5 and true 13 Apr p8 retrieval gaps; **134 Sep–Dec exposed slots remain**. August extends W. S. Eddy/Fashion Stable through 31 Aug, carries Farr Bros. market-report credits through 24 Aug, and corrects Mrs. J. C. Napier to 512½ Main; no target-frontage occupant. Title-calendar reconciliation, Sohns & Woodbeck Oregon City directory section, and other source-class closeout remain unresolved. |"
        break
else:
    raise SystemExit("1917 year-status row not found")
w("registers/year-status.md", "\n".join(lines) + ("\n" if yr.endswith("\n") else ""))

append_once("registers/research-log.md", f'''| 2026-09-07 | Completed August 1917 Oregon City Enterprise scan-first visual audit | **40/40 genuine pages** for 3/10/17/24/31 Aug; cumulative **280 genuine pages through August**, **134 Sep–Dec slots remain**; existing Mar/Apr page gaps unchanged. Fashion Stable continues through 31 Aug; Farr Bros. market credits through 24 Aug with 31 Aug provider-line change not treated as closure; visual reinspection corrects Mrs. J. C. Napier from OCR-derived 612 to **512½ Main** in both Courier/Enterprise; Adams closing-out ad unnumbered. No exact target occupant. `{SID}` / `{EID}`. Cross-record propagation audit completed. |''')

print(f"Integrated August Enterprise as {SID} / {EID}")
