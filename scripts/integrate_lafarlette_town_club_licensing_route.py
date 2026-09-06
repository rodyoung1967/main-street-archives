from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "LaFarlette Town Club licensing route — 2026-09-06"
OUT_DIR = Path("newspapers/town-club-lafarlette-licensing-controls")
MANIFEST_REL = str(OUT_DIR / "manifest.json")
CAPTURE_REL = "evidence/source-captures/myrtle-lodge-coaledo-location-and-town-club-lead-2026-09-06.md"
REQUEST_REL = "registers/research-requests/coos-town-club-lafarlette-1953-1957-liquor-business-record-request-2026-09-06.md"

PAGES = [
    {
        "date": "1954-12-09",
        "publication": "Coquille Valley Sentinel",
        "page": "3",
        "file": str(OUT_DIR / "1954-12-09-p3-coos-county-liquor-renewal-control.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn96088222/1954-12-09/ed-1/seq-3.pdf",
    },
    {
        "date": "1955-12-07",
        "publication": "Medford Mail Tribune",
        "page": "7",
        "file": str(OUT_DIR / "1955-12-07-p7-olcc-renewal-action-coos-county-control.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn97071090/1955-12-07/ed-1/seq-7.pdf",
    },
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")
    return True


manifest_path = ROOT / MANIFEST_REL
if not manifest_path.exists():
    raise SystemExit(f"Missing manifest: {MANIFEST_REL}")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for item in PAGES:
    p = ROOT / item["file"]
    if not p.exists() or p.stat().st_size < 1000 or p.read_bytes()[:4] != b"%PDF":
        raise SystemExit(f"Missing/invalid preserved PDF: {item['file']}")

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]

sid = None
eid = None
capture = read(CAPTURE_REL)
m = re.search(rf"<!-- {re.escape(MARKER)} / capture -->.*?Archive IDs: source `(S-\d{{3}})`; evidence `(E-\d{{3}})`", capture, re.S)
if m:
    sid, eid = m.groups()
else:
    sid = f"S-{max(source_nums)+1:03d}"
    eid = f"E-{max(evidence_nums)+1:03d}"

retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()

capture_block = f'''## 1954–1955 Town Club licensing-route pass — 6 September 2026
<!-- {MARKER} / capture -->

Archive IDs: source `{sid}`; evidence `{eid}`.  
Manual callout: **MF-050**.  
Ready-to-send request: `{REQUEST_REL}`.  
Preserved licensing-control pages: `{OUT_DIR}/`.  
Retrieval commit: `{retrieval_commit}`.

### Chronology control at the start of the family-memory window

Existing visually preserved source `S-271` / `E-245`, the **11 March 1954 Coquille Valley Sentinel** profile of Raye, says Raye was then working at the **Coquille Hotel coffee shop** and Floyd worked at the **Coos Bay Lumber Company**; daughter Sheila was nine. This does not rule out a simultaneous business interest, but it makes a **post-March-1954 acquisition/license change** a particularly important hypothesis to test if the family recollection that they owned a Town Club when Sheila was about ten is substantially correct.

### 9 December 1954 — Coos County renewal universe

The preserved 9 Dec. 1954 *Coquille Valley Sentinel* page reports that all current liquor-license certificates would expire at midnight Dec. 31, that renewal forms had been sent to **Coos County's 166 retail licensees**, and that renewal applications should bear approval of the licensee's **local governing body — city council or county court**.

This is not evidence that the LaFarlettes or a Town Club held one of those licenses. It is a direct **record-route control** showing that late-1954 County Court/city approval records and OLCC renewal files are the correct source class for testing a 1955 ownership/license hypothesis.

### 7 December 1955 — OLCC renewal-action control

The preserved 7 Dec. 1955 *Medford Mail Tribune* page reports OLCC action after investigation of complaints involving Coos County enforcement and states that the Commission rejected **28 renewal applications statewide**, naming several Coos County establishments among the reported actions.

Again, this page does not name the LaFarlettes or a Town Club in the recovered text. Its value is to identify a concrete **December 1955 Commission-action window** in which renewal/denial minutes or lists should be checked.

### Aggressive online Town Club search result

Targeted public-web and Historic Oregon Newspapers searches were run across **1953–1957**, emphasizing 1954–55, for combinations of `Town Club`, `Town Club House`, `South Powers`, `Powers`, `Coquille`, `Myrtle Point`, `Floyd LaFarlette`, `Raye`, `Rae`, `Ray`, and `La Farlette` variants. The searches repeatedly recovered unrelated Town Clubs elsewhere in Oregon and the already preserved 1940s **South Powers Town Club House**, but did **not** recover a contemporary online source that connects Raye or Floyd to the Town Club name.

Classification: **ONLINE SEARCH COVERAGE / RETRIEVAL GAP — NOT NEGATIVE EVIDENCE.** The absence of an indexed online hit does not establish that the family recollection is wrong. The highest-value next evidence is now the surviving County Court/Board and OLCC licensing record.

### Archival route now identified

The Oregon State Archives' official Coos County inventory identifies **County Court Journal Index, vol. 1–3, 1947–2001**, **County Court Journal, vol. 1–28, 1859–1965**, County Court orders, and related administrative records at the Coos County Courthouse. The inventory explicitly states that County Commissioners administrative journals can include licenses such as **liquor licenses**.

Accordingly **MF-050** requests a 1953–57 lookup, prioritizing March 1954–Dec. 1955, from:

1. **Coos County Clerk** — County Court journal/index/orders/local approval material; and
2. **Oregon State Archives** — historical OLCC applications, renewals, transfers, indexes and Commission actions.

The request expressly tests both the general Town Club family recollection and the separate **South Powers Town Club House candidate** without merging them in advance.

### Evidence status

- **DOCUMENTED / DIRECT — VISUALLY VERIFIED:** March 1954 Raye profile (`S-271` / `E-245`) for Raye/Floyd employment and Sheila age control.
- **OCR/TEXT ONLY / ORIGINAL PDF PRESERVED:** `{sid}` / `{eid}` licensing-route controls. The page PDFs are preserved in-repository, but this integration does not promote them to scan-certified visual evidence.
- **FAMILY / PROJECT-STEWARD PROVENANCE:** Raye and Floyd owned something remembered as the Town Club when Sheila was about ten.
- **DOCUMENTED / DIRECT:** South Powers Town Club House existed as a named polling place in the 1940s (`S-277` / `E-250`).
- **UNVERIFIED LEAD:** South Powers Town Club House = the remembered Town Club; LaFarlette ownership/operation/license.
- **RETRIEVAL GAP:** 1953–57 licensing/ownership bridge pending MF-050.
'''
append_once(CAPTURE_REL, f"{MARKER} / capture", capture_block)

source_name = "1954-1955 Oregon liquor-license renewal controls for Coos County Town Club research"
source_block = f'''## {sid} — {source_name}
<!-- {MARKER} / source -->
Type: Primary newspaper page scans preserved in-repository; text/OCR reviewed, not scan-certified in this integration.  
Pages: *Coquille Valley Sentinel*, 9 Dec. 1954 p.3; *Medford Mail Tribune*, 7 Dec. 1955 p.7.  
Preserved originals: `{OUT_DIR}/`  
Manifest: `{MANIFEST_REL}`  
Retrieval commit: `{retrieval_commit}`  
Related evidence: `{eid}`.  
Related manual callout: `MF-050`.  
Capture: `{CAPTURE_REL}`.  
Classification: **OCR/TEXT ONLY / ORIGINAL PDF PRESERVED — licensing-record route controls, not a Town Club or LaFarlette license identification.**'''
append_once("evidence/source-register.md", f"{MARKER} / source", source_block)

evidence_name = "1954-1955 liquor-renewal notices define the direct licensing-record route for the Town Club hypothesis"
evidence_block = f'''## {eid} — {evidence_name}
<!-- {MARKER} / evidence -->
Source: `{sid}`  
Type: Primary newspaper page scans; OCR/text discovery with original PDFs preserved  
Claims:
- The 9 Dec. 1954 *Coquille Valley Sentinel* reports that renewal forms had been sent to **166 Coos County retail licensees** and that 1955 renewals should bear approval of the local governing body, city council or county court.
- The 7 Dec. 1955 *Medford Mail Tribune* reports a contemporaneous OLCC renewal-action window following investigation involving Coos County and says **28 renewal applications statewide** were rejected.
- Neither preserved page, in the text recovered during this pass, identifies Raye/Floyd LaFarlette or a Town Club license.
- These controls make the late-1954/1955 County Court approval record and OLCC renewal/Commission records the highest-value next source for testing the family Town Club ownership lead.
Classification: **OCR/TEXT ONLY / RECORD-ROUTE CONTROL; NO TOWN CLUB OWNERSHIP CLAIM.**  
Confidence: **High for research-route selection; Town Club/LaFarlette identity remains unresolved.**'''
append_once("evidence/evidence-register.md", f"{MARKER} / evidence", evidence_block)

# YAML source/evidence mirrors
sources_yml = read("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(sid)}$", sources_yml):
    sources_yml = sources_yml.rstrip() + f'''\n\n  - id: {sid}\n    name: "{source_name}"\n    url: "https://oregonnews.uoregon.edu/"\n    type: "Primary newspaper page scans; OCR/text reviewed, PDFs preserved"\n    date: "1954-12-09/1955-12-07"\n    repository_file: "{OUT_DIR}/"\n    notes: "Licensing-route controls for MF-050; no Town Club or LaFarlette license identification. See {CAPTURE_REL}."\n    related_evidence: [{eid}]\n''' + "\n"
write("database/sources.yml", sources_yml)

evidence_yml = read("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(eid)}$", evidence_yml):
    evidence_yml = evidence_yml.rstrip() + f'''\n\n  - id: {eid}\n    name: "{evidence_name}"\n    type: "Primary newspaper page scans; OCR/text-only route control"\n    date: "1954-12-09/1955-12-07"\n    claims:\n      - "The 1954 notice gives a 166-licensee Coos County renewal universe and local governing-body approval route."\n      - "The 1955 report gives a concrete OLCC renewal-action window involving Coos County context."\n      - "No Town Club or LaFarlette license is identified by these pages; MF-050 targets the underlying licensing records."\n    confidence: "High for research-route selection; Town Club ownership remains unresolved."\n    related_sources: [{sid}]\n''' + "\n"
write("database/evidence.yml", evidence_yml)

lead_block = f'''### 6 September 2026 — Town Club licensing bridge becomes MF-050
<!-- {MARKER} / research lead -->

The family recollection that Raye and Floyd LaFarlette owned a **Town Club** when Sheila was about ten remains unverified. Existing `S-271` / `E-245` puts Raye at the Coquille Hotel and Floyd at Coos Bay Lumber Company on 11 Mar. 1954, making a later-1954/1955 ownership or license transition especially important to test. Preserved licensing-route controls `{sid}` / `{eid}` show the local-governing-body/OLCC renewal pathway but do not name a Town Club or LaFarlette license.

Public online searching across 1953–57 did not produce a direct bridge. This is a **RETRIEVAL GAP, not negative evidence**. Proceed under **MF-050** with the Coos County Court Journal Index/Journal/orders and historical OLCC files. Keep the 1940s South Powers Town Club House (`S-277` / `E-250`) separate until an applicant, licensee, address or transaction source bridges it.

Request: `{REQUEST_REL}`.'''
append_once("evidence/research-leads.md", f"{MARKER} / research lead", lead_block)

openq_block = f'''### Town Club / LaFarlette mid-1950s ownership bridge — MF-050
<!-- {MARKER} / open question -->

**Question:** What establishment did the Young family remember as Raye and Floyd LaFarlette's **Town Club** when Sheila was about ten, and were they owners, operators and/or liquor licensees? Was it the documented 1940s **South Powers Town Club House**, or a different Coos County business?

**Current state:** **UNVERIFIED LEAD / RETRIEVAL GAP.** No public online 1953–57 source recovered in the 6 Sep. pass directly connects LaFarlette to the Town Club name. Existing March 1954 evidence places Raye at the Coquille Hotel coffee shop and Floyd at Coos Bay Lumber Company; preserved licensing controls `{sid}` / `{eid}` identify late-1954/1955 County Court and OLCC records as the decisive next source.

**Next action:** `MF-050`; request `{REQUEST_REL}`. Do not merge the South Powers Town Club House with the remembered business without a direct identity/ownership/license bridge.'''
append_once("evidence/open-questions.md", f"{MARKER} / open question", openq_block)

crosswalk_block = f'''## Town Club licensing-route control — 6 September 2026
<!-- {MARKER} / crosswalk -->

- `{sid}` / `{eid}` → `P-006`, `P-022`, `MF-050` — 1954–55 Coos County/OLCC renewal-route controls; no Town Club license identity established.
- `MF-050` → `{REQUEST_REL}` — Coos County Clerk + Oregon State Archives targeted 1953–57 licensing/ownership requests.
- Candidate remains separate: `S-277` / `E-250` documents the 1940s South Powers Town Club House but does not bridge it to the LaFarlettes.'''
append_once("indexes/id-crosswalk.md", f"{MARKER} / crosswalk", crosswalk_block)

log_block = f'''## 6 September 2026 — LaFarlette Town Club 1953–57 licensing-route pass
<!-- {MARKER} / research log -->

- Ran targeted online searches for Town Club / Town Club House / South Powers / Powers / Coquille / Myrtle Point combined with LaFarlette variants across 1953–57, prioritizing 1954–55.
- No direct online source recovered tying Raye or Floyd to a Town Club; result retained as **RETRIEVAL GAP / bounded search coverage**, not negative evidence.
- Existing `S-271` / `E-245` supplies a 11 Mar. 1954 current-state control: Raye at the Coquille Hotel coffee shop, Floyd at Coos Bay Lumber Company, Sheila age 9.
- Preserved two liquor-renewal route-control pages as `{sid}` / `{eid}` under `{OUT_DIR}/`; classification remains **OCR/TEXT ONLY / ORIGINAL PDF PRESERVED** for this integration.
- Official Coos County inventory confirms 1947–2001 County Court Journal Index and County Court Journal through 1965, with administrative journals capable of containing liquor-license actions.
- Created **MF-050** and the ready-to-send Coos County Clerk / Oregon State Archives request `{REQUEST_REL}`.
- No Town Club business ID was created because identity, location, commercial status and LaFarlette relationship remain unresolved.'''
append_once("registers/research-log.md", f"{MARKER} / research log", log_block)

# Manual dashboard: ensure MF-050 is unused, insert active row and dispatch tracker.
manual_rel = "MANUAL-FOLLOWUP.md"
manual = read(manual_rel)
if "MF-050" not in manual:
    active_anchor = "### Recommended batching"
    if active_anchor not in manual:
        raise SystemExit("MANUAL-FOLLOWUP active queue anchor not found")
    active_row = f'''| 19 | **MF-050** | Search **1953–1957 Coos County Court / historical OLCC licensing records for Town Club / Town Club House / LaFarlette**, prioritizing Mar. 1954–Dec. 1955 | Public online searching did not recover the ownership/license bridge; official inventory confirms surviving County Court journals/indexes that can include liquor-license actions | **ACTIVE MANUAL — TWO DRAFTS READY**. [Coos County Clerk + Oregon State Archives drafts]({REQUEST_REL}) |\n\n'''
    manual = manual.replace(active_anchor, active_row + active_anchor, 1)
    dispatch_anchor = "When a request is sent, record the actual date"
    if dispatch_anchor not in manual:
        raise SystemExit("MANUAL-FOLLOWUP dispatch anchor not found")
    dispatch_row = "| **MF-050** | **NOT SENT — TWO DRAFTS READY** | — | — | — | — | No |\n\n"
    manual = manual.replace(dispatch_anchor, dispatch_row + dispatch_anchor, 1)
    manual += f'''\n\n---\n\n## 6 September 2026 — LaFarlette Town Club licensing bridge\n<!-- {MARKER} / manual -->\n\n| ID | Audited disposition | Still needed? | Audit decision |\n| --- | --- | --- | --- |\n| **MF-050** | **ACTIVE MANUAL** | **Yes** | Search the **1953–1957 Coos County Court Journal Index/Journal/orders** and historical **OLCC application/renewal/transfer/Commission-action records**, prioritizing **March 1954–December 1955**, for `Town Club`, `Town Club House`, `South Powers`, `Powers`, and LaFarlette name variants. The public-online pass found no direct identity bridge; this is a **RETRIEVAL GAP, not negative evidence**. Ready-to-send County Clerk and State Archives drafts: `{REQUEST_REL}`. |\n'''
    manual = manual.replace("The current practical list is the **18-item active queue in section 1**.", "The current practical list is the **19-item active queue in section 1**.")
    write(manual_rel, manual)

print(f"Integrated {sid} {eid} MF-050")
