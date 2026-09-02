from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    {
        "source_id": "S-177", "evidence_id": "E-157",
        "repo_path": "newspapers/oregon-city-courier/1909-06-25-page-5-palace-saloon-smith-hall-interest.pdf",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-06-25/ed-1/seq-5.pdf",
        "uploaded_name": "Palace Saloon (sale of) Oregon City courier., June 25, 1909, Page 5, Image 5.pdf",
        "uploaded_sha256": "335bd8535856ef00b60ec36b56b5305dc4640418d2cc2b7c85dbe11be67bc1be",
        "uploaded_bytes": 730494,
    },
    {
        "source_id": "S-178", "evidence_id": "E-158",
        "repo_path": "newspapers/oregon-city-courier/1909-06-25-page-7-palace-saloon-ralph-o-smith-license.pdf",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-06-25/ed-1/seq-7.pdf",
        "uploaded_name": "Palace Saloon (Liquor License) Oregon City courier., June 25, 1909, Page 7, Image 7(1).pdf",
        "uploaded_sha256": "4009305a7b7bfeeaf816bc57a05f1c9f13dad284367efb58fe1c3176b145fe9a",
        "uploaded_bytes": 687344,
    },
    {
        "source_id": "S-179", "evidence_id": "E-159",
        "repo_path": "newspapers/morning-enterprise/1911-06-20-page-3-palace-saloon-joseph-wilson-license.pdf",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063701/1911-06-20/ed-1/seq-3.pdf",
        "uploaded_name": "Palace Saloon (Liquor License) Morning enterprise., June 20, 1911, Page 3, Image 3.pdf",
        "uploaded_sha256": "154f5e91dd6fe8e2299a01f4f270edebcba691804186473c11327eb38b94e7bf",
        "uploaded_bytes": 774744,
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
    write(path, text + "\n" + block.strip("\n") + "\n")


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:160]!r}")
    write(path, text.replace(old, new, 1))


def file_meta(item):
    p = ROOT / item["repo_path"]
    b = p.read_bytes()
    if not b.startswith(b"%PDF"):
        raise RuntimeError(f"Not a PDF: {item['repo_path']}")
    return len(b), hashlib.sha256(b).hexdigest()

for token, path in [
    ("S-177", "evidence/source-register.md"), ("S-178", "evidence/source-register.md"), ("S-179", "evidence/source-register.md"),
    ("E-157", "evidence/evidence-register.md"), ("E-158", "evidence/evidence-register.md"), ("E-159", "evidence/evidence-register.md"),
    ("P-100", "people/people-index.md"),
    ("T-053", "database/timeline.yml"), ("T-054", "database/timeline.yml"),
]:
    if token in read(path):
        raise RuntimeError(f"{token} already exists in {path}; resync and allocate new IDs")

for item in FILES:
    item["repo_bytes"], item["repo_sha256"] = file_meta(item)

capture_path = "evidence/source-captures/1909-1911-palace-saloon-partnership-license-supplement-2026-09-01.md"
capture = f"""# Palace Saloon partnership and license supplement, 1909–1911

Review date: **1 September 2026**.

Status: **THREE PROJECT-STEWARD NEWSPAPER PAGE UPLOADS VISUALLY VERIFIED; CANONICAL OREGON DIGITAL ISSUE/PAGE PDF DERIVATIVES PRESERVED.**

The findings below are based on visual inspection of the supplied page scans. OCR/search text is discovery support only.

## S-177 / E-157 — Oregon City Courier, 25 June 1909, p. 5

The local-and-personal column states that **Ralph O. Smith has purchased the interest of his former partner, F. E. Hall, in the Palace Saloon.**

What this proves:
- Ralph O. Smith and F. E. Hall had been partners in the Palace Saloon before 25 June 1909;
- by that date Smith was reported purchasing Hall's interest in the Palace Saloon;
- Hall is explicitly described as Smith's **former partner**.

Limits:
- the item does not print a street address;
- it does not identify the legal form, percentage interest, price, effective transaction date, liquor-license transfer, real-estate ownership, or building ownership;
- the wording does not by itself prove uninterrupted operation before or after the dated report.

Repository file: `{FILES[0]['repo_path']}`  
Canonical URL: {FILES[0]['url']}  
Original uploaded filename: `{FILES[0]['uploaded_name']}`  
Uploaded SHA-256: `{FILES[0]['uploaded_sha256']}` ({FILES[0]['uploaded_bytes']} bytes).  
Repository SHA-256: `{FILES[0]['repo_sha256']}` ({FILES[0]['repo_bytes']} bytes).

## S-178 / E-158 — Oregon City Courier, 25 June 1909, p. 7

A liquor-license notice states that **Ralph O. Smith** would apply at the next regular City Council meeting for a license to sell liquor at his place of business, **Palace Saloon, Fifth and Main streets**, for three months.

What this proves:
- Ralph O. Smith was the named Palace Saloon license applicant on 25 June 1909;
- the Palace Saloon was directly described at **Fifth and Main streets**;
- the notice is a three-month application.

Limits:
- the notice does not print street number 501;
- an application is not proof of grant;
- it does not prove property title or building ownership.

Read with p. 5 from the same issue, the two pages directly connect Smith's purchase of former partner F. E. Hall's Palace interest with Smith's same-date Palace Saloon license application. The archive does not invent an exact legal closing date or assume that a license transfer was automatic.

Repository file: `{FILES[1]['repo_path']}`  
Canonical URL: {FILES[1]['url']}  
Original uploaded filename: `{FILES[1]['uploaded_name']}`  
Uploaded SHA-256: `{FILES[1]['uploaded_sha256']}` ({FILES[1]['uploaded_bytes']} bytes).  
Repository SHA-256: `{FILES[1]['repo_sha256']}` ({FILES[1]['repo_bytes']} bytes).

## S-179 / E-159 — Morning Enterprise, 20 June 1911, p. 3

The visually inspected notice names **JOSEPH WILSON** and states that he would apply at the next regular City Council meeting for a liquor license at his place of business, **The Palace Saloon, corner 5th and Main streets**, for three months.

What this proves:
- Joseph Wilson was directly associated with the Palace Saloon by **20 June 1911**;
- the Palace was described at Fifth/Main;
- this is a liquor-license application, not proof of grant.

Chronology effect:
- this moves the currently verified **Joseph Wilson / Palace Saloon** relationship back from June 1912 to June 1911;
- the independently verified 19 March 1912 notice prints **Joe Wilson's Palace Saloon at exact 501 Main** (`S-118` / `E-104`);
- the independently verified 20 June 1912 notice again prints **Joseph Wilson** at the Palace, Fifth/Main (`S-173` / `E-153`);
- the 1911 and 1912 Joseph wording plus the March 1912 Joe wording strengthens the existing Joe = Joseph identity inference, but no source explicitly states that Joe is a nickname or gives a legal-name equivalence statement.

Limits:
- this 1911 page does not print 501;
- it does not prove license grant, real-estate ownership, building ownership, or uninterrupted operation through every intervening month.

Repository file: `{FILES[2]['repo_path']}`  
Canonical URL: {FILES[2]['url']}  
Original uploaded filename: `{FILES[2]['uploaded_name']}`  
Uploaded SHA-256: `{FILES[2]['uploaded_sha256']}` ({FILES[2]['uploaded_bytes']} bytes).  
Repository SHA-256: `{FILES[2]['repo_sha256']}` ({FILES[2]['repo_bytes']} bytes).

## Revised Palace sequence supported by visual primary pages

- **6 Apr. 1900:** Albert Knapp reported purchasing Palace Saloon (`E-154`).
- **24 Feb. 1905:** A. Knapp reported selling Palace Saloon to A. J. Surber (`E-155`).
- **24 May 1907:** Palace trade name listed among Oregon City saloons (`E-151`).
- **19 Jul. 1907:** Palace described on Fifth Street (`E-156`).
- **25 Jun. 1909:** Ralph O. Smith reported buying former partner F. E. Hall's Palace interest (`E-157`); same issue Smith applies at Palace Saloon, Fifth/Main (`E-158`).
- **17 Sep. 1909:** Smith again applies at Palace Saloon, corner Main/Fifth (`E-152`).
- **20 Jun. 1911:** Joseph Wilson applies at The Palace Saloon, Fifth/Main (`E-159`).
- **19 Mar. 1912:** Joe Wilson's Palace Saloon at exact 501 Main (`E-104`).
- **20 Jun. 1912:** Joseph Wilson applies at The Palace Saloon, Fifth/Main (`E-153`).

This sequence materially narrows the operator history, but it still does not establish every license grant, every transfer instrument, uninterrupted operation, or real-estate title.
"""
write(capture_path, capture)
write("evidence/source-captures/1909-1911-palace-saloon-partnership-license-manifest.json", json.dumps({
    "review_date": "2026-09-01",
    "status": "VISUALLY VERIFIED supplied scans; canonical issue/page PDFs preserved",
    "files": FILES,
}, indent=2) + "\n")

source_block = f"""
## S-177 — Oregon City Courier, 25 June 1909, p. 5 — Ralph O. Smith purchases F. E. Hall interest in Palace Saloon
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload; canonical archive PDF derivative retained.  
Canonical page/PDF: {FILES[0]['url']}  
Repository file: `{FILES[0]['repo_path']}`  
Original uploaded filename: `{FILES[0]['uploaded_name']}`  
Related evidence: `E-157`; people `P-098`, `P-100`; business `BUS-024`.  
Notes: Reports Ralph O. Smith purchased the interest of his former partner F. E. Hall in the Palace Saloon. No address, percentage, consideration, title, license-transfer mechanics, or exact effective date is printed. Uploaded SHA-256 `{FILES[0]['uploaded_sha256']}`; repository SHA-256 `{FILES[0]['repo_sha256']}`.

## S-178 — Oregon City Courier, 25 June 1909, p. 7 — Ralph O. Smith Palace Saloon liquor-license application
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload; canonical archive PDF derivative retained.  
Canonical page/PDF: {FILES[1]['url']}  
Repository file: `{FILES[1]['repo_path']}`  
Original uploaded filename: `{FILES[1]['uploaded_name']}`  
Related evidence: `E-158`; person `P-098`; business `BUS-024`.  
Notes: Ralph O. Smith applies for three months at Palace Saloon, Fifth and Main streets. Application is not proof of grant, exact 501 number, or property title. Uploaded SHA-256 `{FILES[1]['uploaded_sha256']}`; repository SHA-256 `{FILES[1]['repo_sha256']}`.

## S-179 — Morning Enterprise, 20 June 1911, p. 3 — Joseph Wilson Palace Saloon liquor-license application
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload; canonical archive PDF derivative retained.  
Canonical page/PDF: {FILES[2]['url']}  
Repository file: `{FILES[2]['repo_path']}`  
Original uploaded filename: `{FILES[2]['uploaded_name']}`  
Related evidence: `E-159`; person `P-037`; business `BUS-024`.  
Notes: Joseph Wilson applies for three months at The Palace Saloon, corner 5th and Main streets. This predates the March 1912 exact-501 Joe Wilson notice and June 1912 Joseph Wilson notice; application is not grant/title proof. Uploaded SHA-256 `{FILES[2]['uploaded_sha256']}`; repository SHA-256 `{FILES[2]['repo_sha256']}`.
"""
append_once("evidence/source-register.md", "## S-177 —", source_block)

evidence_block = """
## E-157 — Ralph O. Smith purchases F. E. Hall interest in Palace Saloon, 25 June 1909
Type: Primary newspaper / reported business-interest transaction
Date: 25 June 1909
Sources: `S-177`
Related record: `evidence/E-157-1909-palace-saloon-smith-hall-interest.md`
Claims:
- The *Oregon City Courier* reports that Ralph O. Smith purchased the interest of his former partner, F. E. Hall, in the Palace Saloon.
- The wording directly establishes a prior Smith/Hall Palace Saloon partnership relationship and a reported transfer of Hall's interest to Smith.
Limits:
- No address, percentage interest, price, formal transfer instrument, license transfer, real-estate title, or exact effective date is printed.
Confidence: Very High for the printed partnership/interest-transfer wording; legal terms and property implications unresolved.

## E-158 — Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June 1909
Type: Primary newspaper / liquor-license application
Date: 25 June 1909
Sources: `S-178`
Related record: `evidence/E-158-1909-palace-saloon-smith-license.md`
Claims:
- Ralph O. Smith is the named applicant.
- His place of business is Palace Saloon, Fifth and Main streets.
- The application is for three months.
Limits:
- No street number 501 is printed.
- Application is not proof of grant, real-estate ownership, or building ownership.
Confidence: Very High for applicant, trade name, intersection, and application wording.

## E-159 — Joseph Wilson Palace Saloon license application at Fifth/Main, 20 June 1911
Type: Primary newspaper / liquor-license application
Date: 20 June 1911
Sources: `S-179`
Related record: `evidence/E-159-1911-palace-saloon-joseph-wilson-license.md`
Claims:
- Joseph Wilson is the named liquor-license applicant at The Palace Saloon, corner 5th and Main streets.
- This directly establishes Joseph Wilson with the Palace by June 1911, earlier than the previously registered 1912 Wilson notices.
- Read with March 1912 Joe Wilson at exact 501 and June 1912 Joseph Wilson at Fifth/Main, it strengthens the Joe/Joseph same-person inference.
Limits:
- The 1911 notice does not print 501.
- It does not prove grant, title, or uninterrupted operation through every intervening month.
Confidence: Very High for 1911 wording; Strong for Joe/Joseph identity when read with `E-104` and `E-153`.
"""
append_once("evidence/evidence-register.md", "## E-157 —", evidence_block)

for path, body in {
    "evidence/E-157-1909-palace-saloon-smith-hall-interest.md": """# E-157 — Ralph O. Smith purchases F. E. Hall interest in Palace Saloon, 25 June 1909\n\nSource: `S-177`.\n\nThe visually verified *Oregon City Courier* page reports that Ralph O. Smith purchased the interest of his former partner, F. E. Hall, in the Palace Saloon. This proves a reported Smith/Hall Palace partnership relationship and Hall-interest transfer to Smith. It does not print an address, transaction price, percentage interest, formal transfer instrument, license-transfer action, or real-estate title.\n""",
    "evidence/E-158-1909-palace-saloon-smith-license.md": """# E-158 — Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June 1909\n\nSource: `S-178`.\n\nThe visually verified notice names Ralph O. Smith applying for a three-month liquor license at Palace Saloon, Fifth and Main streets. It does not print 501 and does not prove the license was granted or establish real-estate/building ownership.\n""",
    "evidence/E-159-1911-palace-saloon-joseph-wilson-license.md": """# E-159 — Joseph Wilson Palace Saloon license application at Fifth/Main, 20 June 1911\n\nSource: `S-179`.\n\nThe visually verified *Morning Enterprise* notice names Joseph Wilson applying for a three-month liquor license at The Palace Saloon, corner 5th and Main streets. This moves verified Joseph Wilson/Palace evidence back to June 1911. The page does not print 501 or prove grant/title/continuous operation. Read with `E-104` and `E-153`, Joe Wilson = Joseph Wilson remains a strong inference rather than an explicit legal-name statement.\n""",
}.items():
    write(path, body)

# YAML source records
append_once("database/sources.yml", "  - id: S-177\n", f"""
  - id: S-177
    name: Oregon City Courier, 25 June 1909, p. 5 — Ralph O. Smith purchases F. E. Hall interest in Palace Saloon
    url: {FILES[0]['url']}
    repository_file: {FILES[0]['repo_path']}
    notes: "Visually verified project-steward upload. Reports Ralph O. Smith purchased former partner F. E. Hall's interest in Palace Saloon. No address/percentage/price/title/license-transfer mechanics. E-157/P-098/P-100/BUS-024. Uploaded SHA-256 {FILES[0]['uploaded_sha256']}; repository SHA-256 {FILES[0]['repo_sha256']}."
  - id: S-178
    name: Oregon City Courier, 25 June 1909, p. 7 — Ralph O. Smith Palace Saloon liquor-license application
    url: {FILES[1]['url']}
    repository_file: {FILES[1]['repo_path']}
    notes: "Visually verified project-steward upload. Smith applies for three months at Palace Saloon, Fifth/Main. Application is not grant/title/exact-501 proof. E-158/P-098/BUS-024. Uploaded SHA-256 {FILES[1]['uploaded_sha256']}; repository SHA-256 {FILES[1]['repo_sha256']}."
  - id: S-179
    name: Morning Enterprise, 20 June 1911, p. 3 — Joseph Wilson Palace Saloon liquor-license application
    url: {FILES[2]['url']}
    repository_file: {FILES[2]['repo_path']}
    notes: "Visually verified project-steward upload. Joseph Wilson applies for three months at The Palace Saloon, corner 5th/Main. Earlier than the registered 1912 Wilson notices; no exact 501/grant/title proof. E-159/P-037/BUS-024. Uploaded SHA-256 {FILES[2]['uploaded_sha256']}; repository SHA-256 {FILES[2]['repo_sha256']}."
""")

append_once("database/evidence.yml", "  - id: E-157\n", """
  - id: E-157
    name: Ralph O. Smith purchases F. E. Hall interest in Palace Saloon, 25 June 1909
    type: Primary newspaper / reported business-interest transaction
    claims:
      - Ralph O. Smith was reported purchasing the interest of his former partner, F. E. Hall, in the Palace Saloon.
      - The wording establishes a prior Smith/Hall Palace partnership relationship and a reported Hall-interest transfer to Smith.
      - No address, percentage, price, formal transfer instrument, license transfer, or real-estate title is printed.
    confidence: Very High for printed partnership/interest-transfer wording; legal and property terms unresolved.
    related_sources: [S-177]
    related_businesses: [BUS-024]
    related_people: [P-098, P-100]
    repository_file: evidence/E-157-1909-palace-saloon-smith-hall-interest.md

  - id: E-158
    name: Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June 1909
    type: Primary newspaper / liquor-license application
    claims:
      - Ralph O. Smith applies for three months at Palace Saloon, Fifth and Main streets.
      - No 501 number is printed; application is not proof of grant or property title.
    confidence: Very High for applicant, trade name, intersection, and application wording.
    related_sources: [S-178]
    related_businesses: [BUS-024]
    related_people: [P-098]
    repository_file: evidence/E-158-1909-palace-saloon-smith-license.md

  - id: E-159
    name: Joseph Wilson Palace Saloon license application at Fifth/Main, 20 June 1911
    type: Primary newspaper / liquor-license application
    claims:
      - Joseph Wilson applies for three months at The Palace Saloon, corner 5th and Main streets.
      - This establishes Joseph Wilson with the Palace by June 1911, earlier than the registered 1912 Wilson notices.
      - Read with March 1912 exact-501 Joe Wilson and June 1912 Joseph Wilson, Joe/Joseph identity is strengthened but remains an inference.
      - The 1911 notice does not print 501 or prove grant, title, or uninterrupted operation.
    confidence: Very High for 1911 wording; Strong for Joe/Joseph identity across the three dated notices.
    related_sources: [S-179, S-118, S-173]
    related_businesses: [BUS-024]
    related_people: [P-037]
    related_buildings: [B-005]
    repository_file: evidence/E-159-1911-palace-saloon-joseph-wilson-license.md
""")

# Business YAML updates
old_bus = """  - id: BUS-024
    name: Palace Saloon
    address: 501 Main exact in March 1912; Main/Fifth intersection in September 1909 and June 1912
    notes: 6 April 1900 report has Albert Knapp purchasing Palace Saloon opposite the post office/on a corner; 24 February 1905 reports A. Knapp selling Palace to A. J. Surber, directly establishing Surber's Palace relationship. May 1907 lists the trade name citywide; July 1907 places Palace on Fifth Street without number/proprietor; Ralph O. Smith is at Main/Fifth in Sep.1909; Joe Wilson is exact 501 in Mar.1912 and Joseph Wilson Fifth/Main in Jun.1912. Early exact number, grants, property title and uninterrupted succession remain unproved.
    related_buildings:
      - B-005
    related_people:
      - P-037
      - P-055
      - P-098
      - P-099
    related_evidence:
      - E-104
      - E-151
      - E-152
      - E-153
      - E-154
      - E-155
      - E-156
    related_sources:
      - S-118
      - S-171
      - S-172
      - S-173
      - S-174
      - S-175
      - S-176
    repository_file: businesses/palace-saloon.md
"""
new_bus = """  - id: BUS-024
    name: Palace Saloon
    address: 501 Main exact in March 1912; Fifth/Main intersection in June 1909, September 1909, June 1911 and June 1912
    notes: 6 April 1900 report has Albert Knapp purchasing Palace Saloon opposite the post office/on a corner; 24 February 1905 reports A. Knapp selling Palace to A. J. Surber. May 1907 lists the trade name citywide and July 1907 places Palace on Fifth Street. On 25 June 1909 Ralph O. Smith is reported buying former partner F. E. Hall's Palace interest and applies the same day at Palace Saloon, Fifth/Main; Smith applies again there in September 1909. Joseph Wilson applies at Palace, Fifth/Main in June 1911; Joe Wilson is exact 501 in March 1912 and Joseph Wilson is again Fifth/Main in June 1912. Early exact number, license grants, property title and uninterrupted succession remain unproved.
    related_buildings:
      - B-005
    related_people:
      - P-037
      - P-055
      - P-098
      - P-099
      - P-100
    related_evidence:
      - E-104
      - E-151
      - E-152
      - E-153
      - E-154
      - E-155
      - E-156
      - E-157
      - E-158
      - E-159
    related_sources:
      - S-118
      - S-171
      - S-172
      - S-173
      - S-174
      - S-175
      - S-176
      - S-177
      - S-178
      - S-179
    repository_file: businesses/palace-saloon.md
"""
replace_once("database/businesses.yml", old_bus, new_bus)

# People YAML updates
old_p037 = """  - id: P-037
    name: Joe Wilson
    role: Palace Saloon liquor-license applicant
    notes: 19 March 1912 notice identifies Joe Wilson's Palace Saloon at 501 Main. A 20 June 1912 notice prints Joseph Wilson at The Palace Saloon, Fifth/Main; same business/location and close chronology make Joe=Joseph a strong identity inference, not explicit legal-name proof. No building ownership, license grant, uninterrupted operation or later succession is inferred.
    related_buildings:
      - B-005
    related_businesses:
      - BUS-024
    related_evidence:
      - E-104
      - E-153
    related_sources:
      - S-118
      - S-173
    repository_file: people/profiles/joe-wilson.md
"""
new_p037 = """  - id: P-037
    name: Joe Wilson
    role: Palace Saloon liquor-license applicant
    notes: A 20 June 1911 notice prints Joseph Wilson at The Palace Saloon, Fifth/Main. A 19 March 1912 notice identifies Joe Wilson's Palace Saloon at exact 501 Main, and 20 June 1912 again prints Joseph Wilson at the Palace, Fifth/Main. The repeated Joseph form around the exact-501 Joe notice strengthens Joe=Joseph as a strong identity inference, not explicit legal-name proof. No building ownership, license grant, uninterrupted operation or later succession is inferred.
    related_buildings:
      - B-005
    related_businesses:
      - BUS-024
    related_evidence:
      - E-104
      - E-153
      - E-159
    related_sources:
      - S-118
      - S-173
      - S-179
    repository_file: people/profiles/joe-wilson.md
"""
replace_once("database/people.yml", old_p037, new_p037)

old_p098 = """  - id: P-098
    name: Ralph O. Smith
    role: Palace Saloon liquor-license applicant
    notes: Visually verified 17 September 1909 Courier notice places Smith at the Palace Saloon, corner Main/Fifth, for a three-month liquor-license application. The notice does not print 501 or prove grant, real-estate ownership or succession to/from other Fifth/Main liquor applicants.
    related_businesses: [BUS-024]
    related_evidence: [E-152]
    related_sources: [S-172]
    repository_file: people/profiles/ralph-o-smith.md
"""
new_p098 = """  - id: P-098
    name: Ralph O. Smith
    role: Palace Saloon business-interest purchaser / liquor-license applicant
    notes: On 25 June 1909 the Courier reports Smith purchased the interest of his former Palace Saloon partner F. E. Hall; a same-issue notice places Smith applying at Palace Saloon, Fifth/Main for three months. A 17 September 1909 notice again places Smith at Palace Saloon, corner Main/Fifth. No exact 501 number, license grant, real-estate ownership, transaction price/percentage, or later succession is proved.
    related_businesses: [BUS-024]
    related_evidence: [E-152, E-157, E-158]
    related_sources: [S-172, S-177, S-178]
    repository_file: people/profiles/ralph-o-smith.md
"""
replace_once("database/people.yml", old_p098, new_p098)

append_once("database/people.yml", "  - id: P-100\n", """
  - id: P-100
    name: F. E. Hall
    role: Former Palace Saloon partner of Ralph O. Smith
    notes: The 25 June 1909 Courier says Ralph O. Smith purchased the interest of his former partner, F. E. Hall, in the Palace Saloon. Given names, partnership start/end, percentage interest, consideration, license role and property ownership are unresolved.
    related_businesses: [BUS-024]
    related_evidence: [E-157]
    related_sources: [S-177]
    repository_file: people/profiles/f-e-hall.md
""")

write("people/profiles/f-e-hall.md", """# F. E. Hall (`P-100`)\n\nRole: former Palace Saloon partner of Ralph O. Smith.\n\nA visually verified 25 June 1909 *Oregon City Courier* item says Ralph O. Smith purchased the interest of his former partner, **F. E. Hall**, in the Palace Saloon (`S-177` / `E-157`). The source does not give Hall's full name, partnership start date, percentage interest, consideration, liquor-license role, real-estate ownership or building ownership.\n""")
append_once("people/people-index.md", "| P-100 |", "| P-100 | [F. E. Hall](profiles/f-e-hall.md) | Former Palace Saloon partner | 25 June 1909 Courier says Ralph O. Smith purchased Hall's Palace Saloon interest; given names and transaction/legal terms unresolved. |")

append_once("database/timeline.yml", "  - id: T-053\n", """
  - id: T-053
    date: 25 June 1909
    summary: Ralph O. Smith is reported purchasing former partner F. E. Hall's interest in Palace Saloon; a same-issue license notice places Smith at Palace Saloon, Fifth/Main. No 501 number, license grant, transaction terms or real-estate title is proved.
    confidence: Very High for visually verified printed wording; legal terms and exact numbered room unresolved.
    related_evidence: [E-157, E-158]
    related_sources: [S-177, S-178]
    related_people: [P-098, P-100]
    related_businesses: [BUS-024]
    related_buildings: [B-005]
  - id: T-054
    date: 20 June 1911
    summary: Joseph Wilson applies for a three-month liquor license at The Palace Saloon, corner 5th/Main, moving verified Wilson/Palace evidence back to June 1911. The notice does not print 501 or prove grant/title.
    confidence: Very High for visually verified printed wording; Strong Joe/Joseph identity inference with 1912 notices.
    related_evidence: [E-159, E-104, E-153]
    related_sources: [S-179, S-118, S-173]
    related_people: [P-037]
    related_businesses: [BUS-024]
    related_buildings: [B-005]
""")

append_once("businesses/palace-saloon.md", "## 25 June 1909 partnership / license evidence", """
## 25 June 1909 partnership / license evidence

Two visually verified pages from the same *Oregon City Courier* issue materially tighten the operator chronology (`S-177`–`S-178`, `E-157`–`E-158`). Page 5 reports that **Ralph O. Smith purchased the interest of his former partner, F. E. Hall, in the Palace Saloon**. Page 7 separately names **Ralph O. Smith** applying for a three-month liquor license at **Palace Saloon, Fifth and Main streets**.

Together these establish a Smith/Hall Palace partnership relationship before 25 June 1909, a reported purchase of Hall's business interest by Smith, and Smith's same-date license application at the Fifth/Main Palace. They do **not** establish a street number, price or percentage interest, formal transfer instrument, automatic license transfer/grant, real-estate ownership or building ownership.

## 20 June 1911 Joseph Wilson evidence

A visually verified *Morning Enterprise* notice (`S-179` / `E-159`) names **Joseph Wilson** applying for a three-month liquor license at **The Palace Saloon, corner 5th and Main streets**. This moves verified Joseph Wilson / Palace Saloon evidence back to June 1911. The notice does not print 501. Read with the 19 March 1912 exact-501 **Joe Wilson** notice and 20 June 1912 **Joseph Wilson** notice, Joe = Joseph is a stronger identity inference but remains an inference rather than an explicit legal-name statement.
""")
append_once("people/profiles/ralph-o-smith.md", "## 25 June 1909 update", """
## 25 June 1909 update

`S-177` / `E-157` reports that Ralph O. Smith purchased the interest of his former partner **F. E. Hall** in the Palace Saloon. `S-178` / `E-158` from the same issue separately names Smith applying for a three-month liquor license at Palace Saloon, Fifth/Main. This materially precedes and strengthens the already registered 17 September 1909 Smith/Palace notice (`S-172` / `E-152`). No exact 501 number, license grant, transaction percentage/price or real-estate title is proved.
""")
append_once("people/profiles/joe-wilson.md", "## 20 June 1911 update", """
## 20 June 1911 update

`S-179` / `E-159` visually verifies **Joseph Wilson** applying at **The Palace Saloon, corner 5th and Main streets** on 20 June 1911. This predates the exact-501 Joe Wilson notice of 19 March 1912 (`S-118` / `E-104`) and the Joseph Wilson Fifth/Main notice of 20 June 1912 (`S-173` / `E-153`). The three-source sequence strengthens Joe = Joseph while preserving it as an inference rather than an explicit legal-name equivalence.
""")
append_once("buildings/501-main.md", "## 1909–1911 Palace Saloon context", """
## 1909–1911 Palace Saloon context

New visually verified pages add operator history around the later exact-501 Palace Saloon without back-projecting the number. On 25 June 1909 Ralph O. Smith was reported buying former partner F. E. Hall's interest in the Palace Saloon and, in the same issue, applying at Palace Saloon, Fifth/Main (`E-157`–`E-158`). On 20 June 1911 Joseph Wilson applied at The Palace Saloon, Fifth/Main (`E-159`). Neither 1909 nor 1911 page prints **501**. Exact 501 remains directly printed in the 19 March 1912 Joe Wilson notice (`E-104`).
""")
append_once("timeline.md", "### 25 June 1909 — Smith buys Hall interest in Palace; same-day Palace license application", """
### 25 June 1909 — Smith buys Hall interest in Palace; same-day Palace license application

A visually verified *Oregon City Courier* page reports **Ralph O. Smith** purchased the interest of his former partner **F. E. Hall** in the **Palace Saloon** (`S-177` / `E-157`). A second page in the same issue names Smith applying for a three-month liquor license at **Palace Saloon, Fifth and Main streets** (`S-178` / `E-158`). This establishes the Smith/Hall Palace relationship and reported interest transfer, but not exact 501, license grant, property title, transaction percentage or price.

### 20 June 1911 — Joseph Wilson at Palace Saloon, Fifth/Main

A visually verified *Morning Enterprise* notice names **Joseph Wilson** applying for a three-month liquor license at **The Palace Saloon, corner 5th and Main streets** (`S-179` / `E-159`). This moves verified Wilson/Palace evidence back to June 1911. The notice does not print 501; exact 501 is separately printed for **Joe Wilson** on 19 March 1912 (`E-104`).
""")
append_once("registers/business-timeline.md", "### Palace Saloon supplement — 1909–1911", """
### Palace Saloon supplement — 1909–1911

| Date | Business | ID | Evidence | Confidence | Note |
| --- | --- | --- | --- | --- | --- |
| 25 Jun. 1909 | Palace Saloon / Ralph O. Smith / F. E. Hall | `BUS-024` | `E-157`, `E-158` | Very High for printed wording | Smith reported buying former partner Hall's Palace interest; same issue Smith applies at Palace, Fifth/Main. No 501/grant/title/transaction terms. |
| 20 Jun. 1911 | Palace Saloon / Joseph Wilson | `BUS-024` | `E-159` | Very High wording; Strong Joe/Joseph identity inference | Joseph Wilson applies at Palace, Fifth/Main; predates 1912 Wilson evidence; no 501 in this notice. |
""")
append_once("indexes/id-crosswalk.md", "| E-157 |", """
| E-157 | S-177; P-098/P-100; BUS-024 | Ralph O. Smith reported purchase of former partner F. E. Hall's Palace Saloon interest, 25 Jun. 1909. |
| E-158 | S-178; P-098; BUS-024 | Smith Palace Saloon liquor-license application at Fifth/Main, same date. |
| E-159 | S-179; P-037; BUS-024; B-005 | Joseph Wilson Palace Saloon application at Fifth/Main, 20 Jun. 1911; no exact 501 in notice. |
| P-100 F. E. Hall | E-157; S-177; BUS-024 | Former Palace Saloon partner of Ralph O. Smith; full name and legal terms unresolved. |
""")
append_once("evidence/open-questions.md", "**1 September 2026 Palace supplement:** `E-157`", """
**1 September 2026 Palace supplement:** `E-157` / `S-177` now directly establishes **F. E. Hall** as Ralph O. Smith's former Palace Saloon partner and reports Smith purchasing Hall's interest on 25 June 1909. `E-158` / `S-178` places Smith applying at Palace Saloon, Fifth/Main the same day. `E-159` / `S-179` places **Joseph Wilson** at The Palace Saloon, Fifth/Main by 20 June 1911. Still unresolved: license grants/council action, exact legal transfer terms, uninterrupted operator succession, and whether the Palace occupied the later-numbered 501 room throughout these earlier dates. Do not back-project 501 from the 1912 exact-number notice.
""")
append_once("evidence/research-leads.md", "### Palace Saloon 1909–1911 follow-up", """
### Palace Saloon 1909–1911 follow-up

- Recover City Council minutes immediately following **25 June 1909** for Ralph O. Smith's Palace Saloon application; determine grant, bond/fee, premises wording, and any reference to F. E. Hall or license transfer.
- Search deeds, business notices and liquor-license records around June 1909 for **F. E. Hall** and Ralph O. Smith to determine partnership formation, transaction terms and whether any business-interest transfer coincided with a premises/license change. Do not infer real-estate title from the newspaper business-interest item.
- Recover City Council minutes immediately following **20 June 1911** for Joseph Wilson's Palace Saloon application; test grant/bond/fee/premises wording and whether a street number is supplied.
""")
append_once("ARCHIVE_INDEX.md", "### Palace Saloon 1909–1911 primary-page supplement", """
### Palace Saloon 1909–1911 primary-page supplement

- `S-177` / `E-157`: 25 Jun. 1909 *Courier* — Ralph O. Smith reported purchasing former partner F. E. Hall's Palace Saloon interest.
- `S-178` / `E-158`: same issue — Smith Palace Saloon liquor-license application at Fifth/Main.
- `S-179` / `E-159`: 20 Jun. 1911 *Morning Enterprise* — Joseph Wilson Palace Saloon application at Fifth/Main, moving verified Wilson/Palace evidence back to 1911.
- Detailed provenance and uploaded/repository hashes: `evidence/source-captures/1909-1911-palace-saloon-partnership-license-supplement-2026-09-01.md`.
""")
append_once("registers/research-log.md", "Palace Saloon 1909–1911 uploaded-page supplement", "| 2026-09-01 | Palace Saloon 1909–1911 uploaded-page supplement | Visually verified three steward-supplied pages; added S-177–S-179 / E-157–E-159 and P-100 F. E. Hall. Smith/Hall partnership-interest transfer and same-day 25 Jun. 1909 Smith Palace license application established; Joseph Wilson Palace application moved back to 20 Jun. 1911. Exact 501 is not back-projected; grants/title/continuous succession remain open. |")

print("Integrated Palace Saloon 1909–1911 supplement")
for item in FILES:
    print(item["repo_path"], item["repo_bytes"], item["repo_sha256"])
