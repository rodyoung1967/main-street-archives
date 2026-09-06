from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MARKER = "Myrtle Lodge Coaledo location and Town Club lead — 2026-09-06"
OUT_DIR = Path("newspapers/coquille-valley-sentinel/myrtle-lodge-coaledo")
MANIFEST_REL = str(OUT_DIR / "manifest.json")
CAPTURE_REL = "evidence/source-captures/myrtle-lodge-coaledo-location-and-town-club-lead-2026-09-06.md"
CHRONOLOGY_REL = "evidence/source-captures/raye-floyd-lafarlette-pre-wheel-hospitality-businesses-2026-09-05.md"
RAYE_REL = "people/profiles/raye-grisham.md"
FLOYD_REL = "people/profiles/floyd-lafarlette.md"
BUSINESS_PAGE_REL = "businesses/myrtle-lodge-coaledo.md"

PAGES = [
    ("1947-12-11", 1, "1947-12-11-p1-midway-renamed-myrtle-lodge.pdf", "https://oregonnews.uoregon.edu/lccn/sn96088222/1947-12-11/ed-1/seq-1.pdf"),
    ("1948-10-28", 12, "1948-10-28-p12-coaledo-myrtle-lodge-town-club-house.pdf", "https://oregonnews.uoregon.edu/lccn/sn96088222/1948-10-28/ed-1/seq-12.pdf"),
    ("1949-07-14", 15, "1949-07-14-p15-behind-myrtle-lodge-at-coaledo.pdf", "https://oregonnews.uoregon.edu/lccn/sn96088222/1949-07-14/ed-1/seq-15.pdf"),
    ("1952-10-09", 9, "1952-10-09-p9-myrtle-lodge-seven-miles-north-coquille.pdf", "https://oregonnews.uoregon.edu/lccn/sn96088222/1952-10-09/ed-1/seq-9.pdf"),
    ("1954-10-28", 1, "1954-10-28-p1-coaledo-myrtle-lodge-powers-polling-places.pdf", "https://oregonnews.uoregon.edu/lccn/sn96088222/1954-10-28/ed-1/seq-1.pdf"),
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
    raise SystemExit(f"Missing preservation manifest: {MANIFEST_REL}")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for date, page, filename, url in PAGES:
    p = ROOT / OUT_DIR / filename
    if not p.exists() or p.stat().st_size < 1000 or p.read_bytes()[:4] != b"%PDF":
        raise SystemExit(f"Missing/invalid preserved PDF: {p}")

source_register = read("evidence/source-register.md")
evidence_register = read("evidence/evidence-register.md")
business_index = read("businesses/business-index.md")

source_nums = [int(x) for x in re.findall(r"(?m)^## S-(\d{3})\b", source_register)]
evidence_nums = [int(x) for x in re.findall(r"(?m)^## E-(\d{3})\b", evidence_register)]
business_nums = [int(x) for x in re.findall(r"\bBUS-(\d{3})\b", business_index)]

sid = None
eid = None
bid = None
if (ROOT / CAPTURE_REL).exists():
    existing = read(CAPTURE_REL)
    m = re.search(r"Archive IDs: source `(S-\d{3})`; evidence `(E-\d{3})`; business `(BUS-\d{3})`", existing)
    if m:
        sid, eid, bid = m.groups()
if not sid:
    sid = f"S-{max(source_nums)+1:03d}"
    eid = f"E-{max(evidence_nums)+1:03d}"
    bid = f"BUS-{max(business_nums)+1:03d}"

retrieval_commit = subprocess.check_output(
    ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL], cwd=ROOT, text=True
).strip()

capture = f'''# Myrtle Lodge at Coaledo — location evidence and Town Club lead

<!-- {MARKER} -->

Date integrated: **6 September 2026**

Status: **MYRTLE LODGE LOCALITY DOCUMENTED; EXACT MODERN PARCEL UNRESOLVED; TOWN CLUB OWNERSHIP LEAD UNVERIFIED**

Archive IDs: source `{sid}`; evidence `{eid}`; business `{bid}`.

Preserved originals: `{OUT_DIR}/`  
Manifest: `{MANIFEST_REL}`  
Retrieval commit: `{retrieval_commit}`

## Question

Locate the Myrtle Lodge associated with Floyd LaFarlette and Charlie Elkins, and preserve Rodney Young's additional family recollection that Raye and Floyd owned a **Town Club** in the mid-1950s when Sheila was about ten.

## Myrtle Lodge location — Coaledo

The combined contemporary record fixes the Myrtle Lodge at **Coaledo, Coos County, Oregon**, on the then-**U.S. Highway 101** corridor between Coquille and Coos Bay.

- **11 Dec. 1947, p.1:** the *Coquille Valley Sentinel* reports that the Oregon State Liquor Commission permitted Mr. and Mrs. Van Spores to change the name of **their restaurant and club on Highway 101 from the Midway to the Myrtle Lodge**. It says the Spores had purchased the entire ownership some time earlier.
- **28 Oct. 1948, p.12:** the county polling-place list gives **“No. 31 Coaledo, The Myrtle Lodge.”**
- **14 Jul. 1949, p.15:** a classified advertisement for J. E. Parsons describes property **“Behind Myrtle Lodge at Coaledo.”**
- **9 Oct. 1952, p.9:** a Myrtle Lodge advertisement gives the location as **“Just 7 miles north of Coquille on Highway 101”** and phone Coos Bay 1-7355. This advertisement was visually reviewed through the archive's rendered page result during the research pass.
- **28 Oct. 1954, p.1:** the county polling-place list again gives **“No. 31 Coaledo, Myrtle Lodge.”** This confirms the named venue/locality association into late 1954.

Classification: **DOCUMENTED / DIRECT** for the printed locality and highway descriptions; **STRONG CROSS-SOURCE INFERENCE** that these references identify the same Midway → Myrtle Lodge site. The exact modern parcel, street number, surviving-building identity and footprint are **UNRESOLVED**.

The modern route context must be handled carefully. ODOT's U.S. 101 historic context explains that the old Coast Highway route through Coquille was bypassed in the 1956–60 Coos Bay–Bandon realignment and the old Coos Bay–Coquille portion became part of the Coos Bay–Roseburg Highway system. Therefore the historic “Highway 101” wording should be sought today along the **OR 42 / old Coos Bay–Coquille corridor**, not on the modern coastal U.S. 101 alignment. This modern-road equivalence is route context, not an exact Myrtle Lodge parcel assignment.

## Name/ownership sequence

- Before the Dec. 1947 rename, the restaurant/club was known as **the Midway / Club Midway**.
- The 11 Dec. 1947 article directly attributes the Midway → Myrtle Lodge name change and prior full ownership to **Mr. and Mrs. Van Spores**.
- Existing repository source `S-269` / `E-243` directly advertises **Charlie Elkins and Floyd LaFarlette as the new owners of The Myrtle Lodge on 18 Oct. 1951**.
- Existing `S-270` / `E-244` directly names **Mr. and Mrs. Floyd LaFarlette** among hosts of a Myrtle Lodge banquet/dance on 11 Jun. 1953; that source does not independently restate Raye's legal ownership.

A 13 Jun. 1946 Chevron-station list indexed by Historic Oregon Newspapers contains the wording **“MYRTLE LODGE — COALEDO,”** which predates the Dec. 1947 formal rename report. That is an **OCR/TEXT-ONLY NAMING ANOMALY** requiring separate visual/contextual resolution; it is not used here to invalidate the direct 1947 rename report.

## Town Club — project-steward family lead

On 6 Sep. 2026 Rodney Young added that Raye and Floyd **owned something called the Town Club in the mid-1950s, when Sheila was about ten**.

Classification: **PROJECT-STEWARD / FAMILY PROVENANCE — HIGH-VALUE UNVERIFIED LEAD.** It is not yet converted into a legal ownership, operator or exact-location claim.

Sheila's reported birth date is 13 Jun. 1944, and the visually preserved 11 Mar. 1954 Raye profile (`S-271` / `E-245`) says Sheila was nine. “About ten” therefore makes approximately **mid-1954 through mid-1955** the highest-value initial search window, with a broader 1953–57 bracket appropriate for ownership/license records.

## South Powers Town Club House — candidate, not a bridge

The same **28 Oct. 1948** county polling-place source that places Myrtle Lodge at Coaledo separately lists **“No. 39 South Powers, Town Club House.”** Earlier 16 May 1946 and 20 May 1948 polling lists also use the South Powers Town Club House wording.

This proves that a place called **Town Club House existed in South Powers in the 1940s**, but it does **not** prove that it was the Town Club remembered by Rodney, that it was a commercial nightclub, or that Raye/Floyd owned or operated it.

The **28 Oct. 1954** polling list instead places Powers precinct No. 39 at **Rebekah Hall** and another Powers precinct at the Rowena Munro residence. That change is a polling-place control only. It must **not** be treated as proof that the Town Club House had closed, moved, or ceased to exist.

Classification: **DOCUMENTED / DIRECT** for the South Powers Town Club House name/location in the 1940s; **UNVERIFIED LEAD** for any LaFarlette connection.

## Next research

1. Search 1953–57 Coos County/Powers/Myrtle Point liquor-license and assumed-business-name records for `Town Club`, `Town Club House`, `LaFarlette`, `La Farlette`, `Floyd`, `Raye`, and `Rae`.
2. Search local newspapers around 1954–55 for Town Club advertisements, ownership-change notices, entertainment listings and proprietor names.
3. Resolve whether the South Powers Town Club House was a commercial hospitality venue, community/social hall, or another type of building.
4. For Myrtle Lodge, use historic highway maps, tax/assessor cards and property records around **Coaledo / old U.S. 101 (modern OR 42 corridor)** to identify the exact former parcel and determine whether a building survives.

## Propagation audit

This finding changes the LaFarlette pre-Wheel business geography and warrants a dedicated business record plus updates to Raye/Floyd profiles and the research lead. It does **not** change any 503/505 Main building fact, Oregon City Wheel ownership date, or target-property timeline event, so no 503/505 building/timeline entry is manufactured from this off-site Coos County evidence.
'''
write(CAPTURE_REL, capture)

source_block = f'''## {sid} — Coquille Valley Sentinel Myrtle Lodge / Coaledo location batch, 1947–1954
<!-- {MARKER} / source -->
Type: Primary newspaper page scans preserved as a research batch.  
Publication: *Coquille Valley Sentinel*.  
Dates/pages: 11 Dec. 1947 p.1; 28 Oct. 1948 p.12; 14 Jul. 1949 p.15; 9 Oct. 1952 p.9; 28 Oct. 1954 p.1.  
Preserved originals: `{OUT_DIR}/`  
Manifest: `{MANIFEST_REL}`  
Related evidence/business: `{eid}`; `{bid}`.  
Capture: `{CAPTURE_REL}`.  
Classification: **PRIMARY SOURCE BATCH — DIRECT printed location/name evidence; exact modern parcel unresolved.**'''
append_once("evidence/source-register.md", f"{MARKER} / source", source_block)

claims = [
    "The 11 Dec. 1947 page reports that Mr. and Mrs. Van Spores received permission to rename their Highway 101 restaurant and club from the Midway to the Myrtle Lodge.",
    "The 28 Oct. 1948 polling list identifies No. 31 Coaledo at The Myrtle Lodge and separately No. 39 South Powers at Town Club House.",
    "The 14 Jul. 1949 classified describes property as behind Myrtle Lodge at Coaledo.",
    "The 9 Oct. 1952 Myrtle Lodge advertisement says the venue was just seven miles north of Coquille on Highway 101.",
    "The 28 Oct. 1954 polling list again identifies No. 31 Coaledo at Myrtle Lodge; Powers polling sites are then Rebekah Hall and a private residence.",
    "Together these sources document Myrtle Lodge at Coaledo on the historic U.S. 101 Coquille–Coos Bay corridor, but do not establish an exact modern parcel or surviving building.",
    "The South Powers Town Club House is a documentary candidate for Rodney Young's separate Town Club family recollection, but no LaFarlette ownership/operation bridge has been established."
]
claims_md = "\n".join(f"- {c}" for c in claims)
evidence_block = f'''## {eid} — Myrtle Lodge is documented at Coaledo; South Powers Town Club House remains an unbridged candidate
<!-- {MARKER} / evidence -->
Source: `{sid}`  
Related business: `{bid}`  
Claims:
{claims_md}
Classification: **DOCUMENTED / DIRECT for the printed source statements; STRONG CROSS-SOURCE INFERENCE for same-site Midway → Myrtle Lodge continuity; UNVERIFIED LEAD for any LaFarlette ↔ South Powers Town Club House connection.**  
Confidence: **Very High for Coaledo locality; exact modern parcel unresolved.**'''
append_once("evidence/evidence-register.md", f"{MARKER} / evidence", evidence_block)

business_page = f'''# Myrtle Lodge / former Club Midway — Coaledo, Oregon

<!-- {MARKER} / business page -->

Business ID: `{bid}`.

## Location

Contemporary evidence places the venue at **Coaledo, Coos County, Oregon**, on the historic U.S. Highway 101 corridor between Coquille and Coos Bay. A 1952 advertisement says **seven miles north of Coquille on Highway 101**; polling-place lists in 1948 and 1954 explicitly identify **Coaledo, Myrtle Lodge**. A 1949 classified describes property **behind Myrtle Lodge at Coaledo**.

The exact modern parcel/address and building survival are unresolved. The historic highway route was later reassigned after the U.S. 101 realignment; investigate the modern **OR 42 / old Coos Bay–Coquille corridor** rather than assuming the site lies on today's coastal U.S. 101.

## Name and ownership controls

- **11 Dec. 1947:** Oregon State Liquor Commission permission reported for Mr. and Mrs. Van Spores to rename their Highway 101 restaurant/club from **the Midway** to **the Myrtle Lodge**; article says the Spores had purchased full ownership earlier.
- **18 Oct. 1951:** existing `S-269` / `E-243` advertises **Charlie Elkins and Floyd LaFarlette as new owners**.
- **11 Jun. 1953:** existing `S-270` / `E-244` names Mr. and Mrs. Floyd LaFarlette among banquet/dance hosts; this is involvement evidence, not an independent legal-ownership statement for Raye.
- **28 Oct. 1954:** county polling-place list still uses **Coaledo, Myrtle Lodge**.

## Evidence boundary

Do not merge this business with the later **Myrtle Hotel / Myrtle Coffee Shop / Club Lehua** complex in Myrtle Point. Do not merge it with the **South Powers Town Club House** unless a person, license, transaction or other contemporary bridge is recovered.

Primary location batch: `{sid}` / `{eid}`.  
Capture: `{CAPTURE_REL}`.
'''
write(BUSINESS_PAGE_REL, business_page)

business_index_block = f'''## 6 September 2026 — LaFarlette Coos County hospitality context
<!-- {MARKER} / business index -->

| ID | Business | Address | Notes |
| --- | --- | --- | --- |
| {bid} | [Myrtle Lodge / former Club Midway](myrtle-lodge-coaledo.md) | Coaledo, historic U.S. 101 corridor; exact modern parcel unresolved | Midway → Myrtle Lodge rename directly reported 11 Dec. 1947; Floyd LaFarlette and Charlie Elkins advertised as new owners 18 Oct. 1951 (`E-243`). Coaledo location independently documented in 1948, 1949, 1952 and 1954 (`{eid}`). Do not merge with Myrtle Point hotel/Club Lehua or South Powers Town Club House. |'''
append_once("businesses/business-index.md", f"{MARKER} / business index", business_index_block)

businesses_yml = read("database/businesses.yml")
if not re.search(rf"(?m)^  - id: {re.escape(bid)}$", businesses_yml):
    businesses_yml = businesses_yml.rstrip() + f'''

  - id: {bid}
    name: "Myrtle Lodge / former Club Midway"
    repository_file: "{BUSINESS_PAGE_REL}"
    address: "Coaledo, Coos County, Oregon; historic U.S. Highway 101 corridor; exact modern parcel unresolved"
    notes: "Van Spores rename Midway to Myrtle Lodge in 1947; Charlie Elkins and Floyd LaFarlette advertised as new owners in 1951. Keep separate from Myrtle Point hotel/Club Lehua and South Powers Town Club House."
    related_people: [P-006, P-022]
    related_evidence: [{eid}, E-243, E-244]
    related_sources: [{sid}, S-269, S-270]
''' + "\n"
    write("database/businesses.yml", businesses_yml)

sources_yml = read("database/sources.yml")
if not re.search(rf"(?m)^  - id: {re.escape(sid)}$", sources_yml):
    sources_yml = sources_yml.rstrip() + f'''

  - id: {sid}
    name: "Coquille Valley Sentinel Myrtle Lodge / Coaledo location batch, 1947-1954"
    url: "https://oregonnews.uoregon.edu/lccn/sn96088222/"
    type: "Primary newspaper page scan batch"
    date: "1947-12-11 to 1954-10-28"
    repository_file: "{OUT_DIR}/"
    notes: "Preserved pages documenting Midway rename, Coaledo locality, highway location and South Powers Town Club House candidate."
    related_evidence: [{eid}]
''' + "\n"
    write("database/sources.yml", sources_yml)

evidence_yml = read("database/evidence.yml")
if not re.search(rf"(?m)^  - id: {re.escape(eid)}$", evidence_yml):
    yclaims = "\n".join(f"      - \"{c.replace(chr(34), chr(39))}\"" for c in claims)
    evidence_yml = evidence_yml.rstrip() + f'''

  - id: {eid}
    name: "Myrtle Lodge documented at Coaledo; Town Club candidate remains unbridged"
    type: "Primary newspaper page scan batch"
    date: "1947-12-11 to 1954-10-28"
    claims:
{yclaims}
    confidence: "Very High for Coaledo locality; exact modern parcel unresolved; no LaFarlette-Town Club bridge yet."
    related_sources: [{sid}]
''' + "\n"
    write("database/evidence.yml", evidence_yml)

profile_block = f'''## Myrtle Lodge location refined to Coaledo
<!-- {MARKER} / profile -->

New primary-source location batch `{sid}` / `{eid}` fixes the Myrtle Lodge associated with Floyd's 1951 ownership at **Coaledo, Coos County**, on the historic U.S. 101 corridor. A 1952 ad says seven miles north of Coquille; 1948 and 1954 polling lists explicitly say Coaledo, Myrtle Lodge; a 1949 classified says “behind Myrtle Lodge at Coaledo.” Exact modern parcel remains unresolved. Business record: `{bid}`.

Rodney Young additionally recalls that Raye and Floyd owned a **Town Club** in the mid-1950s when Sheila was about ten. A **South Powers Town Club House** is independently documented in 1946–48, but no LaFarlette bridge has been recovered. Treat this as **PROJECT-STEWARD / FAMILY PROVENANCE / HIGH-VALUE UNVERIFIED LEAD**, not ownership fact.'''
append_once(RAYE_REL, f"{MARKER} / profile", profile_block)
append_once(FLOYD_REL, f"{MARKER} / profile", profile_block)

chronology_block = f'''## Location refinement and mid-1950s Town Club lead — 6 September 2026
<!-- {MARKER} / chronology -->

Primary-source batch `{sid}` / `{eid}` now fixes **Myrtle Lodge at Coaledo, Coos County**, on the historic U.S. 101 Coquille–Coos Bay corridor. The exact modern parcel remains unresolved. This sharpens, but does not change, the existing 1951–53 Floyd/Raye Myrtle Lodge chronology. Business record: `{bid}`.

Rodney Young also recalls that Raye and Floyd owned a **Town Club** in the mid-1950s when Sheila was about ten. The initial documentary pass found a **South Powers Town Club House** in 1946–48 polling-place records, but no evidence yet connects it to the LaFarlettes. With Sheila born 13 June 1944 and age nine in the March 1954 profile, prioritize roughly **mid-1954 through mid-1955**, while searching 1953–57 ownership/license records. Do not merge the Town Club lead with Myrtle Lodge, Myrtle Hotel/Club Lehua, or the South Powers building without a direct bridge.'''
append_once(CHRONOLOGY_REL, f"{MARKER} / chronology", chronology_block)

lead_block = f'''### 6 September 2026 — LaFarlette “Town Club” mid-1950s family lead
<!-- {MARKER} / research lead -->

Project steward Rodney Young recalls that Raye and Floyd LaFarlette owned a **Town Club** in the mid-1950s when Sheila was about ten. Source `{sid}` / evidence `{eid}` independently documents a **South Powers Town Club House** in 1948, but there is no LaFarlette ownership/operator bridge and the building's commercial/social function is unresolved. Prioritize 1953–57 liquor-license, assumed-business-name, directory and newspaper records; first target mid-1954 through mid-1955. Keep this lead separate from `{bid}` Myrtle Lodge and the Myrtle Point hotel/Club Lehua complex.'''
append_once("evidence/research-leads.md", f"{MARKER} / research lead", lead_block)

crosswalk_block = f'''## Myrtle Lodge / Coaledo location batch — 6 September 2026
<!-- {MARKER} / crosswalk -->

- `{sid}` / `{eid}` / `{bid}` → `P-006`, `P-022` — primary Coaledo location/name batch and Myrtle Lodge business record.
- Existing `S-269` / `E-243` → `{bid}`, `P-022` — 18 Oct. 1951 Elkins/Floyd new-ownership advertisement.
- Existing `S-270` / `E-244` → `{bid}`, `P-006`, `P-022` — 11 Jun. 1953 Raye/Floyd hosting/involvement record; no independent Raye legal-ownership upgrade.
- South Powers Town Club House remains an unassigned business/entity lead pending identification and a LaFarlette bridge.'''
append_once("indexes/id-crosswalk.md", f"{MARKER} / crosswalk", crosswalk_block)

log_block = f'''### 6 September 2026 — Myrtle Lodge located at Coaledo; Town Club lead opened
<!-- {MARKER} / research log -->

Preserved and registered five *Coquille Valley Sentinel* pages as `{sid}` / `{eid}`. The combined record fixes Myrtle Lodge at **Coaledo on historic U.S. 101**, creates `{bid}` for Myrtle Lodge / former Club Midway, and retains the exact modern parcel as unresolved. Rodney Young's separate family recollection of a LaFarlette-owned **Town Club** around Sheila's age ten is preserved as an unverified lead. A South Powers Town Club House existed in 1946–48, but no LaFarlette bridge is established. No 503/505 building or Oregon City timeline claim was changed by this off-site finding.'''
append_once("registers/research-log.md", f"{MARKER} / research log", log_block)

print(f"Integrated {sid} {eid} {bid}")
