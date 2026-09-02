#!/usr/bin/env python3
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(".")

ITEMS = [
    {
        "source_id": "S-180", "evidence_id": "E-160",
        "date": "31 August 1916", "short_date": "1916-08-31",
        "title": "Oregon City Courier", "page": "p. 3",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1916-08-31/ed-1/seq-3.pdf",
        "repo_path": "newspapers/oregon-city-courier/1916-08-31-page-3-fifth-street-restaurant-inspection.pdf",
        "uploaded_name": "Fifth Street Resturant Oregon City courier., August 31, 1916, Page 3, Image 3.pdf",
        "uploaded_sha": "4d9511abbc922fdfa394fa1397dfa6dfc67153e449589922c604f6a680243697",
        "uploaded_size": 811155,
    },
    {
        "source_id": "S-181", "evidence_id": "E-161",
        "date": "31 October 1919", "short_date": "1919-10-31",
        "title": "Oregon City Enterprise", "page": "p. 5",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1919-10-31/ed-1/seq-5.pdf",
        "repo_path": "newspapers/oregon-city-enterprise/1919-10-31-page-5-fifth-street-restaurant-fine.pdf",
        "uploaded_name": "Fifth Street Resturant (fine) Oregon City enterprise., October 31, 1919, Page Page 5, Image 5(1).pdf",
        "uploaded_sha": "eb793b35b119d1d88fb79953e1a1aed3fef7678918c70cb4fe3d43d1e573b754",
        "uploaded_size": 691715,
    },
    {
        "source_id": "S-182", "evidence_id": "E-162",
        "date": "26 August 1921", "short_date": "1921-08-26",
        "title": "Oregon City Enterprise", "page": "p. 4",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1921-08-26/ed-1/seq-4.pdf",
        "repo_path": "newspapers/oregon-city-enterprise/1921-08-26-page-4-fifth-street-restaurant-fight.pdf",
        "uploaded_name": "Fifth Street Resturant (Fight) Oregon City enterprise., August 26, 1921, Page Page 4, Image 4.pdf",
        "uploaded_sha": "f54e7283381f069c6b9bc493d08e65b791fc8ef3fb4adb97a4f2268fd4bcc15b",
        "uploaded_size": 932751,
    },
    {
        "source_id": "S-183", "evidence_id": "E-163",
        "date": "21 July 1922", "short_date": "1922-07-21",
        "title": "Oregon City Enterprise", "page": "p. 1",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1922-07-21/ed-1/seq-1.pdf",
        "repo_path": "newspapers/oregon-city-enterprise/1922-07-21-page-1-fifth-street-restaurant-fire-ownership.pdf",
        "uploaded_name": "Fifth Street Resturant (ownership) Oregon City enterprise., July 21, 1922, Image 1.pdf",
        "uploaded_sha": "ed47337b2918af305399cf62ed1b9cd29ddba1d9ec10c1ab02f198516adbe6d1",
        "uploaded_size": 849840,
    },
]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + "\n" + block.strip() + "\n")

def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

# Recover exact canonical page bytes and verify they match the steward uploads.
existing_hashes = {}
for p in ROOT.rglob("*.pdf"):
    try:
        existing_hashes.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), str(p))
    except OSError:
        pass

for item in ITEMS:
    with urllib.request.urlopen(item["url"], timeout=60) as r:
        data = r.read()
    got_sha = sha256_bytes(data)
    if got_sha != item["uploaded_sha"] or len(data) != item["uploaded_size"]:
        raise RuntimeError(
            f"Canonical PDF differs from uploaded file for {item['short_date']}: "
            f"got {got_sha}/{len(data)}, expected {item['uploaded_sha']}/{item['uploaded_size']}"
        )
    duplicate = existing_hashes.get(got_sha)
    if duplicate:
        item["actual_repo_path"] = duplicate
        item["already_preserved"] = True
    else:
        p = ROOT / item["repo_path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        item["actual_repo_path"] = item["repo_path"]
        item["already_preserved"] = False
        existing_hashes[got_sha] = item["repo_path"]

capture_path = "evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md"
capture = f"""# Fifth Street Restaurant uploaded primary pages, 1916–1922

Review date: **1 September 2026**.

Status: **FOUR PROJECT-STEWARD PAGE UPLOADS VISUALLY VERIFIED; EXACT UPLOADED PDF BYTES PRESERVED OR DEDUPLICATED BY SHA-256.**

These pages were checked against the current repository before integration. The 31 August 1916 article had already been visually researched in `1916-fifth-street-restaurant-inspection.md`, but its page PDF had not been preserved. The 31 October 1919, 26 August 1921, and 21 July 1922 exact pages were not previously preserved or registered as these source pages. OCR/search remains discovery support only.

## S-180 / E-160 — Oregon City Courier, 31 August 1916, p. 3

The state dairy-and-food-commissioner inspection summary lists **Fifth Street Restaurant — 75.3** among Oregon City hotels and restaurants.

Supported:
- a business/place called Fifth Street Restaurant existed in Oregon City by this date;
- inspection score **75.3**.

Limits:
- no proprietor or numbered address is printed;
- the source does not prove uninterrupted continuity to the 1919, 1921, or 1922 references.

Repository file: `{ITEMS[0]['actual_repo_path']}`  
Canonical URL: {ITEMS[0]['url']}  
Original upload: `{ITEMS[0]['uploaded_name']}`  
SHA-256: `{ITEMS[0]['uploaded_sha']}` ({ITEMS[0]['uploaded_size']} bytes).

## S-181 / E-161 — Oregon City Enterprise, 31 October 1919, p. 5

The item **“RESTAURANT MAN FINED”** states that **W. W. Pollock**, “conducting the Fifth street restaurant,” was fined **$15 and costs** in Justice Stipp's court on complaint of **W. B. Duncan**, an inspector of the state dairy and food department, who charged Pollock with keeping a **dirty and unsanitary place**.

Supported:
- W. W. Pollock was directly described as conducting the Fifth Street Restaurant on this date;
- the fine and sanitation charge are direct printed facts.

Limits:
- the article gives no numbered street address;
- “conducting” establishes an operating role but does not by itself prove real-estate ownership or uninterrupted business continuity.

Repository file: `{ITEMS[1]['actual_repo_path']}`  
Canonical URL: {ITEMS[1]['url']}  
Original upload: `{ITEMS[1]['uploaded_name']}`  
SHA-256: `{ITEMS[1]['uploaded_sha']}` ({ITEMS[1]['uploaded_size']} bytes).

## S-182 / E-162 — Oregon City Enterprise, 26 August 1921, p. 4

The item **“Identity Mistaken; Two Men Start Fight”** reports a fight **in the Fifth Street Restaurant** involving **S. Cox** and **Ray Doane**, arising from a mistaken-identity dispute connected with an automobile. Both were taken into custody; Doane was fined $10 and Cox failed to appear, forfeiting bail.

Supported:
- the newspaper directly places an operating/recognizable Fifth Street Restaurant in Oregon City in August 1921;
- the incident details are dated place-use evidence.

Limits:
- no proprietor, numbered address, lease, or property owner is supplied;
- the incident does not prove continuity of operator from W. W. Pollock in 1919.

Repository file: `{ITEMS[2]['actual_repo_path']}`  
Canonical URL: {ITEMS[2]['url']}  
Original upload: `{ITEMS[2]['uploaded_name']}`  
SHA-256: `{ITEMS[2]['uploaded_sha']}` ({ITEMS[2]['uploaded_size']} bytes).

## S-183 / E-163 — Oregon City Enterprise, 21 July 1922, p. 1

The post-fire account **“MAIN STREET FIRE DAMAGE $56,000; CAUSE IS ENIGMA”** reports the 18 July Fifth/Main fire. In the restaurant portion it names **L. E. Blakely** among people occupying rooms adjacent to the burned structures and immediately states that **“Blakely owned the Fifth street restaurant,”** which was a total loss. It then says **“The building was owned by C. P. Gates, of Portland.”**

Supported:
- the article reports a Blakely ownership role for the Fifth Street Restaurant and a C. P. Gates building-ownership role;
- because the initials **L. E.** appear immediately before the surname-only ownership sentence, treating that “Blakely” as L. E. Blakely is a **strong same-paragraph inference**, not a separate legal-identity record;
- the report is a newspaper ownership statement, not a deed/title instrument.

Conflict handling:
- existing July fire accounts variously print **J. Blake**, **Ed. Blake**, and **Ed Gage** in restaurant operator/owner roles;
- existing property-sale/rebuild sources print **C. Gates** and **C. E. Gates**;
- this page adds **L. E. Blakely** and **C. P. Gates**. These variants are preserved as conflicts and are **not silently merged**.

Repository file: `{ITEMS[3]['actual_repo_path']}`  
Canonical URL: {ITEMS[3]['url']}  
Original upload: `{ITEMS[3]['uploaded_name']}`  
SHA-256: `{ITEMS[3]['uploaded_sha']}` ({ITEMS[3]['uploaded_size']} bytes).

## Revised bounded chronology

- **31 Aug. 1916:** Fifth Street Restaurant scores 75.3 in a state inspection summary.
- **31 Oct. 1919:** W. W. Pollock is directly described as conducting it and is fined on an unsanitary-place charge.
- **26 Aug. 1921:** a reported fight occurs inside the Fifth Street Restaurant.
- **8 Jun. 1922:** existing archive evidence separately lists Fifth Street Restaurant in the Buyers' Carnival roster.
- **13 Jul. 1922:** existing `E-096` property-sale report assigns the restaurant location to C. Gates.
- **18 Jul. 1922:** the restaurant is destroyed in the Fifth/Main fire.
- **21 Jul. 1922:** this Enterprise account reports Blakely as restaurant owner and C. P. Gates as building owner.
- **17–18 Aug. 1922:** existing `E-097` identifies C. E. Gates with the hollow-tile replacement project.

The sequence substantially strengthens the business chronology but does not prove an unchanged room, unchanged operator, exact street number, or a single legal identity across the Blake/Blakely/Gage or C./C. P./C. E. Gates variants.
"""
if not (ROOT / capture_path).exists():
    write(capture_path, capture)

append_once(
    "evidence/source-captures/1916-fifth-street-restaurant-inspection.md",
    "Repository PDF preservation update — 1 September 2026",
    f"""
## Repository PDF preservation update — 1 September 2026

The exact project-steward upload / Oregon Digital page PDF is now preserved at
`{ITEMS[0]['actual_repo_path']}` as `S-180` / `E-160`.
SHA-256: `{ITEMS[0]['uploaded_sha']}`. This adds durable source preservation; it does not alter the earlier continuity cautions.
"""
)

source_md = f"""
## S-180 — Oregon City Courier, 31 August 1916, p. 3, Fifth Street Restaurant inspection
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact uploaded PDF bytes preserved.  
Canonical page/PDF: {ITEMS[0]['url']}  
Repository file: `{ITEMS[0]['actual_repo_path']}`  
Original uploaded filename: `{ITEMS[0]['uploaded_name']}`  
Related evidence: `E-160`; business `BUS-070`.  
Notes: State inspection summary lists Fifth Street Restaurant at 75.3; no proprietor or exact number printed. SHA-256 `{ITEMS[0]['uploaded_sha']}`.

## S-181 — Oregon City Enterprise, 31 October 1919, p. 5, Fifth Street Restaurant fine
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact uploaded PDF bytes preserved.  
Canonical page/PDF: {ITEMS[1]['url']}  
Repository file: `{ITEMS[1]['actual_repo_path']}`  
Original uploaded filename: `{ITEMS[1]['uploaded_name']}`  
Related evidence: `E-161`; business `BUS-070`; person `P-101`.  
Notes: W. W. Pollock, conducting Fifth Street Restaurant, fined $15 and costs on state food-inspector dirty/unsanitary-place complaint. No numbered address. SHA-256 `{ITEMS[1]['uploaded_sha']}`.

## S-182 — Oregon City Enterprise, 26 August 1921, p. 4, Fifth Street Restaurant fight
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact uploaded PDF bytes preserved.  
Canonical page/PDF: {ITEMS[2]['url']}  
Repository file: `{ITEMS[2]['actual_repo_path']}`  
Original uploaded filename: `{ITEMS[2]['uploaded_name']}`  
Related evidence: `E-162`; business `BUS-070`.  
Notes: Reports mistaken-identity fight involving S. Cox and Ray Doane inside Fifth Street Restaurant; place-use evidence only, no proprietor or number. SHA-256 `{ITEMS[2]['uploaded_sha']}`.

## S-183 — Oregon City Enterprise, 21 July 1922, p. 1, Fifth Street Restaurant fire ownership account
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact uploaded PDF bytes preserved.  
Canonical page/PDF: {ITEMS[3]['url']}  
Repository file: `{ITEMS[3]['actual_repo_path']}`  
Original uploaded filename: `{ITEMS[3]['uploaded_name']}`  
Related evidence: `E-163`; business `BUS-070`; people `P-102`, `P-103`.  
Notes: Same-paragraph wording names L. E. Blakely then says Blakely owned Fifth Street Restaurant; says restaurant building was owned by C. P. Gates of Portland. Preserve Blake/Blakely/Gage and C./C. P./C. E. Gates conflicts; newspaper report is not deed proof. SHA-256 `{ITEMS[3]['uploaded_sha']}`.
"""
append_once("evidence/source-register.md", "## S-180 — Oregon City Courier, 31 August 1916", source_md)

source_yml = f"""
  - id: S-180
    name: Oregon City Courier, 31 August 1916, p. 3, Fifth Street Restaurant inspection
    url: {ITEMS[0]['url']}
    repository_file: {ITEMS[0]['actual_repo_path']}
    notes: "Visually verified exact steward-upload page. Fifth Street Restaurant scored 75.3 in state inspection summary; no proprietor or exact number. E-160/BUS-070. SHA-256 {ITEMS[0]['uploaded_sha']}."
  - id: S-181
    name: Oregon City Enterprise, 31 October 1919, p. 5, Fifth Street Restaurant fine
    url: {ITEMS[1]['url']}
    repository_file: {ITEMS[1]['actual_repo_path']}
    notes: "Visually verified exact steward-upload page. W. W. Pollock, conducting Fifth Street Restaurant, fined $15 and costs on dirty/unsanitary-place complaint. E-161/P-101/BUS-070. SHA-256 {ITEMS[1]['uploaded_sha']}."
  - id: S-182
    name: Oregon City Enterprise, 26 August 1921, p. 4, Fifth Street Restaurant fight
    url: {ITEMS[2]['url']}
    repository_file: {ITEMS[2]['actual_repo_path']}
    notes: "Visually verified exact steward-upload page. Fight involving S. Cox and Ray Doane occurred in Fifth Street Restaurant; no proprietor or number. E-162/BUS-070. SHA-256 {ITEMS[2]['uploaded_sha']}."
  - id: S-183
    name: Oregon City Enterprise, 21 July 1922, p. 1, Fifth Street Restaurant fire ownership account
    url: {ITEMS[3]['url']}
    repository_file: {ITEMS[3]['actual_repo_path']}
    notes: "Visually verified exact steward-upload page. Names L. E. Blakely immediately before saying Blakely owned Fifth Street Restaurant and reports C. P. Gates owned the building. Preserve identity/initial conflicts; not deed proof. E-163/P-102/P-103/BUS-070. SHA-256 {ITEMS[3]['uploaded_sha']}."
"""
append_once("database/sources.yml", "  - id: S-180\n", source_yml)

evidence_md = """
## E-160 — Fifth Street Restaurant in state inspection summary, 31 August 1916
Source: `S-180` — *Oregon City Courier*, 31 August 1916, p. 3.  
Status: **VISUALLY VERIFIED**.  
Claims:
- Oregon City inspection list directly prints **Fifth Street Restaurant — 75.3**.
- This proves a named Fifth Street Restaurant existed by August 1916.
- No proprietor or numbered address is printed, and continuity to later references remains unproved.
Related business: `BUS-070`.  
Repository capture: `evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md`.

## E-161 — W. W. Pollock conducting Fifth Street Restaurant and fined, 31 October 1919
Source: `S-181` — *Oregon City Enterprise*, 31 October 1919, p. 5.  
Status: **VISUALLY VERIFIED**.  
Claims:
- W. W. Pollock is directly described as **conducting the Fifth street restaurant**.
- He was fined **$15 and costs** on a state dairy-and-food inspector complaint charging a **dirty and unsanitary place**.
- The article supplies no exact street number and does not prove real-estate ownership.
Related person: `P-101`; business: `BUS-070`.  
Repository capture: `evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md`.

## E-162 — Fifth Street Restaurant active-place evidence from reported fight, 26 August 1921
Source: `S-182` — *Oregon City Enterprise*, 26 August 1921, p. 4.  
Status: **VISUALLY VERIFIED**.  
Claims:
- The paper reports a mistaken-identity fight **in the Fifth Street Restaurant**, involving S. Cox and Ray Doane.
- This is direct dated evidence that the named place was active/recognized in August 1921.
- The item does not name a proprietor, numbered address, leaseholder, or property owner.
Related business: `BUS-070`.  
Repository capture: `evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md`.

## E-163 — 21 July 1922 Enterprise restaurant/building ownership wording after Fifth/Main fire
Source: `S-183` — *Oregon City Enterprise*, 21 July 1922, p. 1.  
Status: **VISUALLY VERIFIED**.  
Claims:
- The article names **L. E. Blakely** among occupants adjacent to the burned structures and immediately states that **Blakely owned the Fifth street restaurant**.
- Reading the surname-only ownership sentence as L. E. Blakely is a **strong same-paragraph inference**, not separate legal-identity proof.
- It states that **the building was owned by C. P. Gates, of Portland**.
- The newspaper wording is not a deed/title instrument.
- Existing records print J. Blake / Ed. Blake / Ed Gage and C. Gates / C. E. Gates. The new L. E. Blakely and C. P. Gates forms are preserved as unresolved identity/initial conflicts.
Related people: `P-102`, `P-103`; business: `BUS-070`; compare `P-036`, `P-087`, `P-088`, `E-096`, `E-097`, `E-103`.  
Repository capture: `evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md`.
"""
append_once("evidence/evidence-register.md", "## E-160 — Fifth Street Restaurant in state inspection", evidence_md)

evidence_yml = """
  - id: E-160
    name: Fifth Street Restaurant in state inspection summary, 31 August 1916
    type: Primary newspaper / state inspection summary; visually verified
    claims:
      - Fifth Street Restaurant is directly listed in Oregon City with inspection score 75.3.
      - No proprietor or numbered address is printed; later continuity remains unproved.
    confidence: Very High for printed name and score; exact premises/operator unresolved.
    related_sources: [S-180]
    related_businesses: [BUS-070]
    repository_file: evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md

  - id: E-161
    name: W. W. Pollock conducting Fifth Street Restaurant and fined, 31 October 1919
    type: Primary newspaper / operator and sanitation-enforcement evidence; visually verified
    claims:
      - W. W. Pollock is directly described as conducting the Fifth street restaurant.
      - He was fined $15 and costs on a state dairy-and-food inspector complaint charging a dirty and unsanitary place.
      - No numbered address or real-estate ownership is established.
    confidence: Very High for printed operator wording, fine and charge; property role and continuity unresolved.
    related_sources: [S-181]
    related_businesses: [BUS-070]
    related_people: [P-101]
    repository_file: evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md

  - id: E-162
    name: Fifth Street Restaurant active-place evidence, 26 August 1921
    type: Primary newspaper / incident-place evidence; visually verified
    claims:
      - A reported mistaken-identity fight involving S. Cox and Ray Doane occurred in the Fifth Street Restaurant.
      - The item establishes the named place in August 1921 but gives no proprietor, numbered address, leaseholder or property owner.
    confidence: Very High for printed incident location; business continuity and premises unresolved.
    related_sources: [S-182]
    related_businesses: [BUS-070]
    repository_file: evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md

  - id: E-163
    name: 21 July 1922 Enterprise restaurant and building ownership wording after Fifth/Main fire
    type: Primary newspaper / reported business and building ownership evidence; visually verified
    claims:
      - The article names L. E. Blakely and immediately states that Blakely owned the Fifth street restaurant; the same-paragraph identity is a strong inference.
      - It states that the building was owned by C. P. Gates of Portland.
      - These forms conflict with existing J. Blake / Ed. Blake / Ed Gage and C. Gates / C. E. Gates records and are not silently merged.
      - Newspaper ownership wording is not deed/title proof.
    confidence: Very High for printed wording; Strong for L. E. Blakely same-paragraph referent; legal identity/title unresolved.
    related_sources: [S-183]
    related_businesses: [BUS-070]
    related_people: [P-102, P-103]
    related_evidence: [E-096, E-097, E-103]
    repository_file: evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md
"""
append_once("database/evidence.yml", "  - id: E-160\n", evidence_yml)

profiles = {
"people/profiles/w-w-pollock.md": """# W. W. Pollock

Person ID: `P-101`. Related business: `BUS-070` Fifth Street Restaurant.

The 31 October 1919 *Oregon City Enterprise* directly describes **W. W. Pollock** as “conducting the Fifth street restaurant” and reports that he was fined $15 and costs on a state dairy-and-food inspector complaint charging a dirty and unsanitary place (`E-161` / `S-181`).

This establishes an operating role on the dated report, not real-estate ownership, exact street number, or uninterrupted operation before/after it.
""",
"people/profiles/l-e-blakely.md": """# L. E. Blakely

Person ID: `P-102`. Related business: `BUS-070` Fifth Street Restaurant.

The 21 July 1922 *Oregon City Enterprise* names **L. E. Blakely** among occupants of rooms adjacent to the burned structures and immediately states that **“Blakely owned the Fifth street restaurant”** (`E-163` / `S-183`). Treating the surname-only ownership sentence as L. E. Blakely is a strong same-paragraph inference.

Do **not** silently merge this person with `P-087` J. Blake or the `P-088` Ed Gage / Ed Blake source conflict. The variants require an independent identity bridge.
""",
"people/profiles/c-p-gates-1922.md": """# C. P. Gates (1922 Enterprise wording)

Person ID: `P-103`. Related business/site: `BUS-070` Fifth Street Restaurant.

The 21 July 1922 *Oregon City Enterprise* states that the Fifth Street Restaurant **building was owned by C. P. Gates, of Portland** (`E-163` / `S-183`). This is reported newspaper ownership wording, not a deed/title instrument.

Existing 13 July property-sale evidence prints **C. Gates**, while 17–18 August replacement-building reports print **C. E. Gates** (`P-036`, `E-096`, `E-097`). Preserve **C. P. Gates** separately until an independent record resolves whether this is the same person, a newspaper initials error, or a different person.
"""
}
for p, text in profiles.items():
    if not (ROOT / p).exists():
        write(p, text)

people_index = """
## Fifth Street Restaurant people added from uploaded primary pages

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-101 | [W. W. Pollock](profiles/w-w-pollock.md) | Fifth Street Restaurant operator/conductor | 31 Oct. 1919 article directly says he was conducting the restaurant; fined $15 and costs on dirty/unsanitary-place complaint. `E-161` / `S-181`. |
| P-102 | [L. E. Blakely](profiles/l-e-blakely.md) | Reported Fifth Street Restaurant owner | 21 Jul. 1922 Enterprise names L. E. Blakely then immediately says Blakely owned the restaurant. Strong same-paragraph identity inference; do not merge with Blake/Gage variants. `E-163` / `S-183`. |
| P-103 | [C. P. Gates](profiles/c-p-gates-1922.md) | Reported owner of Fifth Street Restaurant building | 21 Jul. 1922 Enterprise wording. Preserve separately from C./C. E. Gates until initials/identity are independently resolved. `E-163` / `S-183`. |
"""
append_once("people/people-index.md", "## Fifth Street Restaurant people added from uploaded primary pages", people_index)

people_yml = """
  - id: P-101
    name: W. W. Pollock
    role: Fifth Street Restaurant operator / conductor
    notes: 31 October 1919 Enterprise directly describes Pollock as conducting the Fifth street restaurant and reports a $15-and-costs sanitation fine. No exact address or property ownership.
    related_businesses: [BUS-070]
    related_evidence: [E-161]
    related_sources: [S-181]
    repository_file: people/profiles/w-w-pollock.md

  - id: P-102
    name: L. E. Blakely
    role: Reported Fifth Street Restaurant owner
    notes: 21 July 1922 Enterprise names L. E. Blakely immediately before saying Blakely owned the restaurant. Same-paragraph identity is strong inference; do not merge with J. Blake or Ed Gage / Ed Blake variants without proof.
    related_businesses: [BUS-070]
    related_evidence: [E-163]
    related_sources: [S-183]
    repository_file: people/profiles/l-e-blakely.md

  - id: P-103
    name: C. P. Gates
    role: Reported owner of Fifth Street Restaurant building
    notes: 21 July 1922 Enterprise says the building was owned by C. P. Gates of Portland. Preserve separately from C. Gates / C. E. Gates P-036 until independent identity evidence resolves the initials.
    related_businesses: [BUS-070]
    related_evidence: [E-163]
    related_sources: [S-183]
    repository_file: people/profiles/c-p-gates-1922.md
"""
append_once("database/people.yml", "  - id: P-101\n", people_yml)

append_once(
    "people/profiles/c-e-gates-1922.md",
    "21 July 1922 initials conflict",
    """
## 21 July 1922 initials conflict

`S-183` / `E-163` adds a distinct *Oregon City Enterprise* wording: the Fifth Street Restaurant building was reportedly owned by **C. P. Gates, of Portland**. Existing sale/rebuild sources print **C. Gates** and **C. E. Gates**. The archive therefore retains `P-103` C. P. Gates separately and does not silently merge the initials.
"""
)

replace_once(
    "database/people.yml",
    "    notes: July source prints C. Gates and assigns him the Fifth Street Restaurant location; August sources print C. E. Gates and document his hollow-tile fire-replacement building at Fifth/Main. Full identity and exact modern storefront footprint remain unresolved. Do not merge with same-initial people elsewhere without direct proof.\n",
    "    notes: July sale source prints C. Gates and assigns him the Fifth Street Restaurant location; August sources print C. E. Gates and document his hollow-tile fire-replacement building at Fifth/Main. A separate 21 July Enterprise account prints C. P. Gates as owner of the restaurant building; that form is retained separately as P-103. Full identity and exact modern storefront footprint remain unresolved. Do not merge initials without direct proof.\n"
)

business_add = """
## Uploaded primary-page chronology added 1 September 2026

Four exact page PDFs add bounded chronology (`E-160`–`E-163`):

- **31 Aug. 1916:** state inspection summary lists Fifth Street Restaurant at **75.3**; no proprietor/number.
- **31 Oct. 1919:** **W. W. Pollock** is directly described as conducting the restaurant and is fined $15 and costs on a dirty/unsanitary-place complaint.
- **26 Aug. 1921:** a reported mistaken-identity fight occurs **in the Fifth Street Restaurant**, confirming the named place in use.
- **21 Jul. 1922:** an Enterprise fire account names **L. E. Blakely** and immediately says “Blakely owned the Fifth street restaurant”; it separately says the building was owned by **C. P. Gates, of Portland**.

The 1922 page **adds rather than resolves** the owner/operator conflict: existing reports print J. Blake, Ed. Blake, and Ed Gage, and existing property/rebuild sources print C. Gates / C. E. Gates. `P-102` L. E. Blakely and `P-103` C. P. Gates are therefore retained as separate source forms pending independent identity evidence.
"""
append_once("businesses/fifth-street-restaurant.md", "## Uploaded primary-page chronology added 1 September 2026", business_add)

old_bus = """  - id: BUS-070
    name: Fifth Street Restaurant
    address: Fifth/Main corner property; exact number unresolved
    notes: Gates received restaurant location in July 1922 Harding property sale; building burned five days later and was replaced with a two-story hollow-tile building. Gage/Blake owner-operator conflict preserved.
    related_people: [P-036, P-087, P-088, P-092]
    related_evidence: [E-096, E-097, E-103]
    related_sources: [S-111, S-112, S-113, S-117]
    repository_file: businesses/fifth-street-restaurant.md
"""
new_bus = """  - id: BUS-070
    name: Fifth Street Restaurant
    address: Fifth/Main corner property by July 1922; exact number unresolved; earlier 1916-1921 exact premises unresolved
    notes: Named by 1916 inspection, W. W. Pollock conducting it in 1919, and active-place evidence in 1921. July 1922 property/fire records place the restaurant in the Fifth/Main cluster; one Enterprise account prints L. E. Blakely/Blakely for restaurant ownership and C. P. Gates for building ownership, while other reports print J. Blake / Ed. Blake / Ed Gage and C. / C. E. Gates. Conflicts preserved; building burned and C. E. Gates replacement followed.
    related_people: [P-036, P-087, P-088, P-092, P-101, P-102, P-103]
    related_evidence: [E-096, E-097, E-103, E-160, E-161, E-162, E-163]
    related_sources: [S-111, S-112, S-113, S-117, S-180, S-181, S-182, S-183]
    repository_file: businesses/fifth-street-restaurant.md
"""
replace_once("database/businesses.yml", old_bus, new_bus)

replace_once(
    "businesses/business-index.md",
    "| BUS-070 | [Fifth Street Restaurant](fifth-street-restaurant.md) | Fifth/Main corner property; exact number unresolved | Gates received the location and rebuilt after July fire. Gage/Blake owner-operator conflict preserved. `E-096`, `E-097`, `E-103`. |",
    "| BUS-070 | [Fifth Street Restaurant](fifth-street-restaurant.md) | Fifth/Main corner property by Jul. 1922; earlier exact premises and number unresolved | 1916 inspection; W. W. Pollock conducting it in 1919; active-place evidence in 1921; July 1922 fire account adds L. E. Blakely / C. P. Gates wording. Preserve Blake/Blakely/Gage and C./C. P./C. E. Gates conflicts. `E-096`, `E-097`, `E-103`, `E-160`–`E-163`. |"
)

timeline_section = """
## 1916–1922 — Fifth Street Restaurant primary-page supplement

Four project-steward page uploads now provide a tighter sequence for `BUS-070`: **31 August 1916** state inspection lists Fifth Street Restaurant at 75.3 (`E-160`); **31 October 1919** W. W. Pollock is directly described as conducting it and is fined on an unsanitary-place complaint (`E-161`); **26 August 1921** a reported fight occurs inside the named restaurant (`E-162`); and the **21 July 1922** Enterprise fire account reports Blakely restaurant ownership and C. P. Gates building ownership (`E-163`). The last account adds unresolved L. E. Blakely vs. Blake/Gage and C. P. vs. C. E. Gates conflicts; it does not settle legal title or exact street number.
"""
append_once("timeline.md", "## 1916–1922 — Fifth Street Restaurant primary-page supplement", timeline_section)

business_timeline = """
## Fifth Street Restaurant uploaded-page supplement

| Date | Business / Event | Business ID | Evidence | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| 31 Aug. 1916 | Fifth Street Restaurant inspection | `BUS-070` | `E-160` | Very High | Named restaurant scored 75.3; proprietor/number not printed. |
| 31 Oct. 1919 | W. W. Pollock conducting Fifth Street Restaurant | `BUS-070` | `E-161` | Very High | Pollock fined $15 and costs on dirty/unsanitary-place complaint; no property-title inference. |
| 26 Aug. 1921 | Fight reported inside Fifth Street Restaurant | `BUS-070` | `E-162` | Very High for place wording | Active-place evidence; no proprietor/number. |
| 21 Jul. 1922 | Post-fire ownership wording | `BUS-070` | `E-163` | Very High wording; Strong same-paragraph Blakely identity inference | Prints L. E. Blakely then Blakely restaurant ownership; prints C. P. Gates building ownership; conflicts preserved. |
"""
append_once("registers/business-timeline.md", "## Fifth Street Restaurant uploaded-page supplement", business_timeline)

timeline_yml = """
  - id: T-055
    date: 31 August 1916
    summary: State inspection summary lists Fifth Street Restaurant in Oregon City with score 75.3; proprietor and exact number are not printed.
    confidence: Very High for printed business name and score; premises/operator unresolved.
    related_evidence: [E-160]
    related_sources: [S-180]
    related_businesses: [BUS-070]

  - id: T-056
    date: 31 October 1919
    summary: W. W. Pollock is directly described as conducting Fifth Street Restaurant and is fined $15 and costs on a state food-inspector dirty/unsanitary-place complaint.
    confidence: Very High for printed operator wording and enforcement event; exact address/property role unresolved.
    related_evidence: [E-161]
    related_sources: [S-181]
    related_people: [P-101]
    related_businesses: [BUS-070]

  - id: T-057
    date: 26 August 1921
    summary: Enterprise reports a mistaken-identity fight involving S. Cox and Ray Doane in the Fifth Street Restaurant, providing dated active-place evidence.
    confidence: Very High for printed place/event wording; proprietor, number and continuity unresolved.
    related_evidence: [E-162]
    related_sources: [S-182]
    related_businesses: [BUS-070]

  - id: T-058
    date: 21 July 1922
    summary: Enterprise post-fire account names L. E. Blakely and immediately says Blakely owned Fifth Street Restaurant; it reports C. P. Gates of Portland owned the building. Blake/Blakely/Gage and C./C. P./C. E. Gates conflicts remain unresolved.
    confidence: Very High for printed wording; Strong same-paragraph inference for L. E. Blakely referent; legal identity/title unresolved.
    related_evidence: [E-163]
    related_sources: [S-183]
    related_people: [P-102, P-103]
    related_businesses: [BUS-070]
"""
append_once("database/timeline.yml", "  - id: T-055\n", timeline_yml)

crosswalk = """
## 1 September 2026 Fifth Street Restaurant uploaded-page integration

| Record | Connected IDs | Note |
| --- | --- | --- |
| `S-180` / `E-160` | `BUS-070` | 31 Aug. 1916 inspection: Fifth Street Restaurant score 75.3; no proprietor/number. |
| `S-181` / `E-161` / `P-101` | `BUS-070` | W. W. Pollock conducting restaurant in 1919; sanitation fine. |
| `S-182` / `E-162` | `BUS-070` | 26 Aug. 1921 incident-place evidence. |
| `S-183` / `E-163` / `P-102` / `P-103` | `BUS-070`; compare `P-036`, `P-087`, `P-088` | 21 Jul. 1922 L. E. Blakely / C. P. Gates wording; identity conflicts preserved. |
"""
append_once("indexes/id-crosswalk.md", "## 1 September 2026 Fifth Street Restaurant uploaded-page integration", crosswalk)

leads = """
## Fifth Street Restaurant identity / title follow-up from 1 September uploads

- Resolve **W. W. Pollock** (`P-101`) through 1919–1921 directories, restaurant licenses, inspection records, or advertisements; do not infer exact premises from the trade name alone.
- Resolve the July 1922 **L. E. Blakely / J. Blake / Ed. Blake / Ed Gage** variants with directories, deeds/leases, court records, or independent same-person evidence.
- Resolve **C. P. Gates** (`P-103`) versus **C. Gates / C. E. Gates** (`P-036`) using the 13 July sale instrument, recorded deed/title chain, assessment rolls, and August replacement-building records. Do not normalize initials until independent proof.
"""
append_once("evidence/research-leads.md", "## Fifth Street Restaurant identity / title follow-up from 1 September uploads", leads)

openq = """
### 1 September 2026 Fifth Street Restaurant update

`E-160`–`E-163` substantially strengthen the 1916–1922 restaurant chronology. They also add two explicit conflicts that remain open: **L. E. Blakely** versus the existing J. Blake / Ed. Blake / Ed Gage forms, and **C. P. Gates** versus C. Gates / C. E. Gates. No exact pre-fire street number is inferred from these pages.
"""
append_once("evidence/open-questions.md", "### 1 September 2026 Fifth Street Restaurant update", openq)

archive = """
## 1 September 2026 — Fifth Street Restaurant primary-page preservation

- [`S-180`–`S-183` / `E-160`–`E-163`](evidence/source-captures/1916-1922-fifth-street-restaurant-uploaded-pages-visual-review-2026-09-01.md) — exact page PDFs preserved for 31 Aug. 1916 inspection, 31 Oct. 1919 W. W. Pollock sanitation fine, 26 Aug. 1921 restaurant fight, and 21 Jul. 1922 post-fire ownership wording. The 1922 page adds unresolved L. E. Blakely and C. P. Gates variants.
"""
append_once("ARCHIVE_INDEX.md", "## 1 September 2026 — Fifth Street Restaurant primary-page preservation", archive)

log = """
| 2026-09-01 | Preserved and integrated four steward-uploaded Fifth Street Restaurant primary pages (1916, 1919, 1921, 1922) | Exact PDF hashes verified against Oregon Digital before preservation. Added S-180–S-183 / E-160–E-163; formalized 1916 inspection source, added W. W. Pollock operator/sanitation fine, 1921 active-place incident, and 1922 L. E. Blakely / C. P. Gates ownership wording. Preserved Blake/Blakely/Gage and C./C. P./C. E. Gates conflicts; no exact-number or title inference. |
"""
append_once("registers/research-log.md", "Preserved and integrated four steward-uploaded Fifth Street Restaurant primary pages", log)

print("Integrated Fifth Street Restaurant pages:")
for item in ITEMS:
    print(item["source_id"], item["actual_repo_path"], item["uploaded_sha"], "existing" if item["already_preserved"] else "new")
