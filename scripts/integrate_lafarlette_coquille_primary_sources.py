from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "LaFarlette Coquille primary-source preservation — 2026-09-06"
OUT_DIR = Path("newspapers/coquille-valley-sentinel/lafarlette-primary-sources")
MANIFEST_REL = str(OUT_DIR / "manifest.json")
CAPTURE_REL = "evidence/source-captures/lafarlette-coquille-primary-source-preservation-2026-09-06.md"
EXISTING_CAPTURE_REL = "evidence/source-captures/raye-floyd-lafarlette-pre-wheel-hospitality-businesses-2026-09-05.md"
RAYE_PROFILE_REL = "people/profiles/raye-grisham.md"
FLOYD_PROFILE_REL = "people/profiles/floyd-lafarlette.md"

SOURCES = [
    {
        "key": "1947",
        "date": "1947-08-07",
        "publication": "Coquille Valley Sentinel",
        "page": "13",
        "file": str(OUT_DIR / "1947-08-07-p13-anderson-lafarlette-mail-contract.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn96088222/1947-08-07/ed-1/seq-13.pdf",
        "source_name": "Coquille Valley Sentinel, 7 August 1947 p.13 — Anderson and LaFarlette mail-contract report",
        "evidence_name": "Anderson and LaFarlette business is documented in Coos County by 7 August 1947",
        "classification": "DOCUMENTED / DIRECT for the dated Anderson and LaFarlette business report; Floyd identification is cross-source and must not be inferred from surname alone.",
        "claims": [
            "The 7 August 1947 Coquille Valley Sentinel p.13 reports that Anderson and LaFarlette had been awarded the Coos Bay–Powers mail contract.",
            "This is a hard Coos County chronology control by August 1947; later records identify Floyd LaFarlette as the Anderson-LaFarlette partner, so the Floyd bridge is cross-source rather than supplied solely by this page.",
            "The page does not mention Morton and does not disprove an earlier brief Morton interval."
        ],
    },
    {
        "key": "1951",
        "date": "1951-10-18",
        "publication": "Coquille Valley Sentinel",
        "page": "4",
        "file": str(OUT_DIR / "1951-10-18-p4-myrtle-lodge-new-owners.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn96088222/1951-10-18/ed-1/seq-4.pdf",
        "source_name": "Coquille Valley Sentinel, 18 October 1951 p.4 — Myrtle Lodge new-ownership advertisement",
        "evidence_name": "Floyd LaFarlette and Charlie Elkins are directly advertised as new owners of The Myrtle Lodge in 1951",
        "classification": "DOCUMENTED / DIRECT — VISUALLY VERIFIED.",
        "claims": [
            "The advertisement states that The Myrtle Lodge is under the new ownership of Charlie Elkins and Floyd LaFarlette.",
            "The advertisement describes a dining establishment offering steaks, seafood and chicken and advertising Saturday-night dancing.",
            "The source establishes Floyd's co-ownership; it does not by itself state that Raye held a legal ownership interest."
        ],
    },
    {
        "key": "1953",
        "date": "1953-06-11",
        "publication": "Coquille Valley Sentinel",
        "page": "3",
        "file": str(OUT_DIR / "1953-06-11-p3-myrtle-lodge-banquet.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn96088222/1953-06-11/ed-1/seq-3.pdf",
        "source_name": "Coquille Valley Sentinel, 11 June 1953 p.3 — Myrtle Lodge banquet and dance",
        "evidence_name": "Raye and Floyd LaFarlette are directly named among Myrtle Lodge banquet-and-dance hosts in 1953",
        "classification": "DOCUMENTED / DIRECT — VISUALLY VERIFIED for hosting/involvement; no legal ownership inference for Raye.",
        "claims": [
            "The article names Mr. and Mrs. Floyd LaFarlette among the hosts of a banquet and dance at The Myrtle Lodge.",
            "The event included dancing after dinner.",
            "This directly establishes Raye's involvement at the venue as Mrs. Floyd LaFarlette but does not independently restate her legal ownership interest."
        ],
    },
    {
        "key": "1954",
        "date": "1954-03-11",
        "publication": "Coquille Valley Sentinel",
        "page": "1",
        "file": str(OUT_DIR / "1954-03-11-p1-raye-lafarlette-profile.pdf"),
        "url": "https://oregonnews.uoregon.edu/lccn/sn96088222/1954-03-11/ed-1/seq-1.pdf",
        "source_name": "Coquille Valley Sentinel, 11 March 1954 p.1 — Raye LaFarlette profile",
        "evidence_name": "Raye LaFarlette's 1954 profile directly documents the Chicago rooming-house and Coquille Hotel chronology",
        "classification": "DOCUMENTED / DIRECT — VISUALLY VERIFIED; preserved contemporary published account, with Morton omission treated as a chronology conflict rather than negative evidence.",
        "claims": [
            "The profile identifies Mrs. Floyd LaFarlette as Raye and says the family first came to Coos County on a 1944 vacation trip, returned to their home in Chicago, sold their rooming-house business and moved to Coquille.",
            "The profile says Raye was working at the Coquille Hotel coffee shop and had been employed at the hotel for several years.",
            "The profile gives daughters Carolyn as 15 and Sheila as 9 at publication.",
            "The article does not mention Morton; that omission is an unresolved conflict with family oral history and is not proof that no brief Morton stop occurred."
        ],
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


def add_ids_to_related_evidence(rel, ids):
    text = read(rel)
    m = re.search(r"(?m)^- Related evidence: (.+)$", text)
    if not m:
        return False
    existing = m.group(1)
    for eid in ids:
        if f"`{eid}`" not in existing:
            existing += f", `{eid}`"
    text = text[:m.start(1)] + existing + text[m.end(1):]
    write(rel, text)
    return True


manifest_path = ROOT / MANIFEST_REL
if not manifest_path.exists():
    raise SystemExit(f"Preservation manifest missing: {MANIFEST_REL}")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for item in SOURCES:
    p = ROOT / item["file"]
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"Preserved source missing or implausibly small: {item['file']}")
    if p.read_bytes()[:4] != b"%PDF":
        raise SystemExit(f"Preserved source is not a PDF: {item['file']}")

retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()

source_text = read("evidence/source-register.md")
evidence_text = read("evidence/evidence-register.md")
source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_text)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_text)]

ids = {}
if (ROOT / CAPTURE_REL).exists():
    cap = read(CAPTURE_REL)
    for item in SOURCES:
        m = re.search(rf"(?m)^- {item['key']}: source `(S-\d{{3}})`; evidence `(E-\d{{3}})`", cap)
        if not m:
            raise SystemExit(f"Existing preservation capture lacks IDs for {item['key']}")
        ids[item["key"]] = (m.group(1), m.group(2))
else:
    s0 = max(source_nums) + 1
    e0 = max(evidence_nums) + 1
    for i, item in enumerate(SOURCES):
        ids[item["key"]] = (f"S-{s0+i:03d}", f"E-{e0+i:03d}")

capture_lines = [
    "# LaFarlette Coquille primary-source preservation",
    "",
    f"<!-- {MARKER} -->",
    "",
    "Date integrated: **6 September 2026**",
    "",
    "Status: **PRIMARY SOURCE FILES PRESERVED — EXISTING HISTORICAL CLASSIFICATIONS RETAINED**",
    "",
    "Purpose: correct a repository-preservation gap. These newspaper pages had already been visually reviewed and were being cited in LaFarlette research captures and person profiles, but the underlying page PDFs had not been committed to the archive. Under `AGENTS.md`, newspaper scans belong under `newspapers/` and should be registered at source and claim level. This capture records the corrective preservation batch without changing the substantive evidence classifications.",
    "",
    f"Preserved folder: `{OUT_DIR}/`  ",
    f"Manifest: `{MANIFEST_REL}`  ",
    f"Retrieval commit: `{retrieval_commit}`",
    "",
    "## Archive IDs",
]
for item in SOURCES:
    sid, eid = ids[item["key"]]
    capture_lines.append(f"- {item['key']}: source `{sid}`; evidence `{eid}` — `{item['file']}`")
capture_lines += [
    "",
    "## Preservation finding",
    "",
    "The absence of these binaries was an archive-maintenance failure, not a historical-evidence problem. The earlier research notes retained stable external URLs and visual-review descriptions, but that did not satisfy the project's stronger repository-preservation expectation. The original page scans are now preserved locally in the repository with manifest hashes and claim-level registration.",
    "",
    "The 1962–1965 *Myrtle Point Herald* items remain **OCR/TEXT ONLY / RETRIEVAL GAP** because their original scans have not yet been retrieved. This preservation batch does not upgrade those later items.",
    "",
    "## Source summaries",
]
for item in SOURCES:
    sid, eid = ids[item["key"]]
    capture_lines += [
        "",
        f"### {item['date']} — `{sid}` / `{eid}`",
        "",
        f"Repository file: `{item['file']}`  ",
        f"Original archive URL: {item['url']}  ",
        f"Classification: **{item['classification']}**",
        "",
    ]
    capture_lines += [f"- {c}" for c in item["claims"]]
write(CAPTURE_REL, "\n".join(capture_lines).rstrip() + "\n")

for item in SOURCES:
    sid, eid = ids[item["key"]]
    smarker = f"{MARKER} / {item['key']} source"
    source_block = f'''## {sid} — {item['source_name']}
<!-- {smarker} -->
Type: Primary newspaper page scan; visually reviewed before integration and now preserved in-repository.  
Publication: *{item['publication']}*  
Date: **{item['date']}**  
Page: **{item['page']}**  
Original archive URL: {item['url']}  
Preserved source: `{item['file']}`  
Manifest: `{MANIFEST_REL}`  
Related evidence: `{eid}`.  
Capture: `{CAPTURE_REL}`.  
Classification: **{item['classification']}**'''
    append_once("evidence/source-register.md", smarker, source_block)

    emarker = f"{MARKER} / {item['key']} evidence"
    claims_md = "\n".join(f"- {c}" for c in item["claims"])
    evidence_block = f'''## {eid} — {item['evidence_name']}
<!-- {emarker} -->
Source: `{sid}`  
Type: Primary newspaper page scan  
Claims:
{claims_md}
Classification: **{item['classification']}**  
Confidence: **Very High for the visible dated wording; inference boundaries above are retained.**'''
    append_once("evidence/evidence-register.md", emarker, evidence_block)

sources_yml = read("database/sources.yml")
for item in SOURCES:
    sid, eid = ids[item["key"]]
    if re.search(rf"(?m)^  - id: {re.escape(sid)}$", sources_yml):
        continue
    sources_yml = sources_yml.rstrip() + f'''

  - id: {sid}
    name: "{item['source_name'].replace('"', "'")}"
    url: "{item['url']}"
    type: "Primary newspaper page scan; visually verified and preserved"
    date: "{item['date']}"
    repository_file: "{item['file']}"
    notes: "Corrective preservation of a page already used in LaFarlette research; see {CAPTURE_REL}."
    related_evidence: [{eid}]
''' + "\n"
write("database/sources.yml", sources_yml)

evidence_yml = read("database/evidence.yml")
for item in SOURCES:
    sid, eid = ids[item["key"]]
    if re.search(rf"(?m)^  - id: {re.escape(eid)}$", evidence_yml):
        continue
    claims = "\n".join(f"      - \"{c.replace(chr(34), chr(39))}\"" for c in item["claims"])
    evidence_yml = evidence_yml.rstrip() + f'''

  - id: {eid}
    name: "{item['evidence_name'].replace('"', "'")}"
    type: "Primary newspaper page scan"
    date: "{item['date']}"
    claims:
{claims}
    confidence: "Very High for visible dated wording; classification and inference boundaries preserved in the evidence register."
    related_sources: [{sid}]
''' + "\n"
write("database/evidence.yml", evidence_yml)

raye_eids = [ids[k][1] for k in ("1953", "1954")]
add_ids_to_related_evidence(RAYE_PROFILE_REL, raye_eids)

raye_block = f'''## Preserved primary-source pages
<!-- {MARKER} / Raye profile links -->

The primary page scans underlying the pre-Wheel chronology are now preserved in the repository rather than cited only by external URL:

- `{ids['1954'][0]}` / `{ids['1954'][1]}` — 11 March 1954 Raye profile: `{SOURCES[3]['file']}`;
- `{ids['1953'][0]}` / `{ids['1953'][1]}` — 11 June 1953 Myrtle Lodge banquet/dance: `{SOURCES[2]['file']}`.

Floyd's 1951 Myrtle Lodge ownership advertisement and the 1947 Coos County chronology control are preserved in the same batch. See `{CAPTURE_REL}`.'''
append_once(RAYE_PROFILE_REL, f"{MARKER} / Raye profile links", raye_block)

floyd_block = f'''## Preserved primary-source pages
<!-- {MARKER} / Floyd profile links -->

The newspaper scans supporting Floyd's pre-Wheel business chronology are now preserved in-repository:

- `{ids['1947'][0]}` / `{ids['1947'][1]}` — 7 August 1947 Anderson and LaFarlette mail-contract report: `{SOURCES[0]['file']}`;
- `{ids['1951'][0]}` / `{ids['1951'][1]}` — 18 October 1951 Myrtle Lodge new-ownership advertisement: `{SOURCES[1]['file']}`;
- `{ids['1953'][0]}` / `{ids['1953'][1]}` — 11 June 1953 Myrtle Lodge banquet/dance: `{SOURCES[2]['file']}`;
- `{ids['1954'][0]}` / `{ids['1954'][1]}` — 11 March 1954 Raye profile / family chronology: `{SOURCES[3]['file']}`.

See `{CAPTURE_REL}` for claim boundaries and preservation provenance.'''
append_once(FLOYD_PROFILE_REL, f"{MARKER} / Floyd profile links", floyd_block)

existing_block = f'''## Repository preservation correction — 6 September 2026
<!-- {MARKER} / existing capture link -->

The visually reviewed *Coquille Valley Sentinel* pages used above are now preserved under `{OUT_DIR}/` and registered in `{CAPTURE_REL}`. This corrects the earlier state in which the research capture retained archive URLs and visual-review notes but the underlying PDFs were not committed. The 1962–1965 *Myrtle Point Herald* pages remain OCR/TEXT ONLY / retrieval gaps and are not included in this preservation batch.'''
append_once(EXISTING_CAPTURE_REL, f"{MARKER} / existing capture link", existing_block)

cross_lines = [
    f"## LaFarlette Coquille primary-source preservation — 6 September 2026",
    f"<!-- {MARKER} / crosswalk -->",
    "",
]
for item in SOURCES:
    sid, eid = ids[item["key"]]
    people = "`P-006`, `P-022`" if item["key"] in ("1953", "1954") else "`P-022`"
    cross_lines.append(f"- `{sid}` / `{eid}` → {people} — `{item['file']}`")
append_once("indexes/id-crosswalk.md", f"{MARKER} / crosswalk", "\n".join(cross_lines))

log_block = f'''### 2026-09-06 — corrected LaFarlette primary-source preservation gap
<!-- {MARKER} / research log -->

- Confirmed that several visually reviewed *Coquille Valley Sentinel* pages supporting the Raye/Floyd chronology had been cited only by external archive URL and were not preserved as repository source files.
- Preserved the 7 Aug. 1947, 18 Oct. 1951, 11 Jun. 1953 and 11 Mar. 1954 page PDFs under `{OUT_DIR}/`, with hashes/URLs in `{MANIFEST_REL}`.
- Added source IDs {', '.join(f'`{ids[k][0]}`' for k in ('1947','1951','1953','1954'))} and evidence IDs {', '.join(f'`{ids[k][1]}`' for k in ('1947','1951','1953','1954'))}; synchronized Markdown/YAML registers and linked the Raye/Floyd profiles.
- This is a preservation correction, not an evidence upgrade. The later 1962–65 *Myrtle Point Herald* material remains OCR/TEXT ONLY pending actual scan retrieval.'''
append_once("registers/research-log.md", f"{MARKER} / research log", log_block)

print(json.dumps({"marker": MARKER, "ids": ids, "retrieval_commit": retrieval_commit}, indent=2))
