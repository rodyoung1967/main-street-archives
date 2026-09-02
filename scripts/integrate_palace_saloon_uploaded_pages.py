#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent.parent

DOWNLOADS = [
    {
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1907-05-24/ed-1/seq-5.pdf",
        "path": "newspapers/oregon-city-courier/1907-05-24-page-5-palace-saloon-city-list.pdf",
        "sha256": "6960e6963bfb3c11a00d32d80f8ab6c151f84632f09e83a152400404c4d1ba26",
        "size": 641615,
    },
    {
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-09-17/ed-1/seq-5.pdf",
        "path": "newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf",
        "sha256": "4682715f6ac882a21893a9d3e0729f0f2eef5544bde41517977ee5e7cb0c077a",
        "size": 677536,
    },
    {
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063701/1912-06-20/ed-1/seq-2.pdf",
        "path": "newspapers/morning-enterprise/1912-06-20-page-2-palace-saloon-joseph-wilson-license.pdf",
        "sha256": "72b3f8ddddfbd7703af82a1abfbea9353feb3e7a0c8a81055ce8c869fb858c9a",
        "size": 826263,
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
    write(path, text.rstrip() + "\n\n" + block.strip("\n") + "\n")


def replace_once(path, old, new, marker=None):
    text = read(path)
    if marker and marker in text:
        return
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:100]!r}")
    write(path, text.replace(old, new, 1))


def insert_after(path, anchor, marker, block):
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Anchor not found in {path}: {anchor[:100]!r}")
    write(path, text.replace(anchor, anchor + "\n\n" + block.strip("\n"), 1))


def download_exact(item):
    dest = ROOT / item["path"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(item["url"], headers={"User-Agent": "main-street-archives-research/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != item["size"] or digest != item["sha256"]:
        raise RuntimeError(
            f"Canonical download mismatch for {item['path']}: "
            f"size={len(data)} sha256={digest}; expected size={item['size']} sha256={item['sha256']}"
        )
    dest.write_bytes(data)


for item in DOWNLOADS:
    download_exact(item)

capture = """# Palace Saloon uploaded newspaper pages, 1907–1912 — visual review

Review date: **1 September 2026**.

Status: **THREE USER-SUPPLIED PRIMARY NEWSPAPER PAGES VISUALLY VERIFIED AND PRESERVED**. OCR/text extraction is not the basis for the historical claims below; the supplied page scans were visually inspected before integration.

## S-171 / E-151 — 24 May 1907 Oregon City Courier, p. 5

The article **“HOW LITTLE OR HOW MUCH — Liquor Licenses May Be Doubled By City”** reports that Oregon City then had sixteen saloons and lists **“The Palace Saloon”** among them.

What this proves:
- the **Palace Saloon trade name was in current Oregon City use by 24 May 1907**.

Limits:
- the list does **not** print an address or proprietor for the Palace Saloon;
- it does not identify A. J. Surber, 501 Main, or a transfer;
- it therefore cannot be used to say Surber operated the Palace Saloon or that the May 1907 Palace occupied 501 Main.

Repository file: `newspapers/oregon-city-courier/1907-05-24-page-5-palace-saloon-city-list.pdf`  
Original uploaded filename: `Palace Saloon Oregon City Courier May 1907(1).pdf`  
SHA-256: `6960e6963bfb3c11a00d32d80f8ab6c151f84632f09e83a152400404c4d1ba26`.

## S-172 / E-152 — 17 September 1909 Oregon City Courier, p. 5

The liquor-license notice states that **Ralph O. Smith** would apply at the next regular City Council meeting for a license to sell liquor at his place of business, **“the Palace Saloon, corner Main and Fifth Sts.”**, for three months.

What this proves:
- **Ralph O. Smith** was the named applicant associated with the Palace Saloon on 17 September 1909;
- the Palace Saloon was then described at the **corner of Main and Fifth Streets**;
- the notice is an application, not proof that the Council granted the license.

Limits:
- the notice does **not** print street number 501;
- it does not prove real-estate ownership, uninterrupted operation from 1907, succession from A. J. Surber/Justin & Hitchman, or succession to E. R. Case/Joe Wilson.

Repository file: `newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf`  
Original uploaded filename: `Palace Saloon (Liquor License) Oregon City courier., September 17, 1909, Page 5, Image 5.pdf`  
SHA-256: `4682715f6ac882a21893a9d3e0729f0f2eef5544bde41517977ee5e7cb0c077a`.

## S-173 / E-153 — 20 June 1912 Morning Enterprise, p. 2

The notice states that **Joseph Wilson** would apply at the next regular City Council meeting for a liquor license at his place of business, **“The Palace Saloon”**, **Fifth and Main streets**, for three months.

This follows the independently visually verified **19 March 1912** notice that prints **Joe Wilson's Palace Saloon at 501 Main Street** (`E-104` / `S-118`).

Interpretation:
- the June notice directly proves the **Joseph Wilson** name form, Palace Saloon trade name, Fifth/Main location, and application;
- the same trade name/location only three months after the exact-501 Joe Wilson notice makes **Joe Wilson = Joseph Wilson a strong identity inference**, but the June page itself does not explicitly state that Joe is a nickname or otherwise prove legal identity;
- the pair strengthens a March→June 1912 Palace Saloon continuity sequence, but neither application proves license grant, property ownership, or uninterrupted operation outside the dated notices.

Repository file: `newspapers/morning-enterprise/1912-06-20-page-2-palace-saloon-joseph-wilson-license.pdf`  
Original uploaded filename: `Palace Saloon (Liquor Licence) Morning enterprise., June 20, 1912, Page 2, Image 2.pdf`  
SHA-256: `72b3f8ddddfbd7703af82a1abfbea9353feb3e7a0c8a81055ce8c869fb858c9a`.

## Chronology impact

The three pages materially refine, but do not close, the early Palace Saloon chain:

- **24 May 1907:** Palace Saloon trade name exists in Oregon City; address/operator unprinted.
- **4 Oct 1907:** A. J. Surber is directly at **No. 501**, Main/Fifth (`E-121` / `S-135`), but that notice does not call his premises Palace Saloon.
- **18 Sep 1908:** Surber and Justin & Hitchman are separately named at Fifth/Main without numbers (`E-121`–`E-123` / `S-137`).
- **17 Sep 1909:** Ralph O. Smith applies at **Palace Saloon, corner Main/Fifth** (`E-152` / `S-172`).
- **1 Jun 1910:** E. R. Case is separately documented with a saloon at Fifth/Main (`E-080`); no Palace continuity is inferred.
- **19 Mar 1912:** Joe Wilson's **Palace Saloon, 501 Main** (`E-104` / `S-118`).
- **20 Jun 1912:** Joseph Wilson applies at **The Palace Saloon, Fifth/Main** (`E-153` / `S-173`).
- **3 Oct 1913:** Hunsaker & Taylor apply at **501 Main** (`E-104` / `S-119`), without the Palace trade name.

The open question is now narrower: determine which of these dated liquor premises represent the same licensed establishment, what transfers/grants occurred, and whether the Palace trade name remained at the same 501 room through the intervening operator changes. No continuity is inferred merely from a shared intersection.
"""
write("evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md", capture)

ralph_profile = """# Ralph O. Smith

Person ID: `P-098`. Related business: `BUS-024`.

A visually verified **17 September 1909 Oregon City Courier** liquor-license notice names **Ralph O. Smith** as the applicant at **the Palace Saloon, corner Main and Fifth Streets**, for a three-month license period (`E-152` / `S-172`).

The notice proves the dated applicant/business/location wording, not license grant, real-estate ownership, exact numbered address, or succession from A. J. Surber / Justin & Hitchman to later E. R. Case or Joe/Joseph Wilson. No same-name identity elsewhere is merged without an independent bridge.
"""
write("people/profiles/ralph-o-smith.md", ralph_profile)

source_block = """## S-171 — Oregon City Courier, 24 May 1907, p. 5, Palace Saloon city saloon list
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload.  
Canonical page/PDF: https://oregonnews.uoregon.edu/lccn/sn00063698/1907-05-24/ed-1/seq-5.pdf  
Repository file: `newspapers/oregon-city-courier/1907-05-24-page-5-palace-saloon-city-list.pdf`  
Original uploaded filename: `Palace Saloon Oregon City Courier May 1907(1).pdf`  
Related evidence: `E-151`; business `BUS-024`.  
Notes: City saloon-license article lists “The Palace Saloon” among Oregon City's sixteen saloons. No Palace address or proprietor is printed; no Surber/501 continuity is inferred. SHA-256 `6960e6963bfb3c11a00d32d80f8ab6c151f84632f09e83a152400404c4d1ba26`.

## S-172 — Oregon City Courier, 17 September 1909, p. 5, Ralph O. Smith Palace Saloon license application
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload.  
Canonical page/PDF: https://oregonnews.uoregon.edu/lccn/sn00063698/1909-09-17/ed-1/seq-5.pdf  
Repository file: `newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf`  
Original uploaded filename: `Palace Saloon (Liquor License) Oregon City courier., September 17, 1909, Page 5, Image 5.pdf`  
Related evidence: `E-152`; person `P-098`; business `BUS-024`.  
Notes: Ralph O. Smith applies for a three-month liquor license at “the Palace Saloon, corner Main and Fifth Sts.” Application does not prove grant, title, exact 501 number, or operator succession. SHA-256 `4682715f6ac882a21893a9d3e0729f0f2eef5544bde41517977ee5e7cb0c077a`.

## S-173 — Morning Enterprise, 20 June 1912, p. 2, Joseph Wilson Palace Saloon license application
Type: Primary newspaper scan; **VISUALLY VERIFIED** 1 September 2026 from project-steward upload.  
Canonical page/PDF: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-06-20/ed-1/seq-2.pdf  
Repository file: `newspapers/morning-enterprise/1912-06-20-page-2-palace-saloon-joseph-wilson-license.pdf`  
Original uploaded filename: `Palace Saloon (Liquor Licence) Morning enterprise., June 20, 1912, Page 2, Image 2.pdf`  
Related evidence: `E-153`; business `BUS-024`; probable same-person context `P-037`.  
Notes: Joseph Wilson applies for three months at “The Palace Saloon,” Fifth and Main streets. Compared with the 19 March 1912 exact-501 Joe Wilson notice, same-person identity is a strong inference from name form + same business + same location + close date, not an explicit statement in this page. No license grant or property ownership inferred. SHA-256 `72b3f8ddddfbd7703af82a1abfbea9353feb3e7a0c8a81055ce8c869fb858c9a`.
"""
append_once("evidence/source-register.md", "## S-171 —", source_block)

evidence_block = """## E-151 — Palace Saloon trade name in Oregon City by 24 May 1907
Type: Primary newspaper city saloon-license article; **VISUALLY VERIFIED** 1 September 2026.  
Source: `S-171`.  
Capture: `evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md`.  
Claims:
- The 24 May 1907 *Oregon City Courier* reports that Oregon City had sixteen saloons and includes **The Palace Saloon** in its list.
- The page does not print the Palace Saloon's address or proprietor.
- This establishes the trade name in current city use by the date, but does not place the business at 501 Main or identify A. J. Surber as its operator.
Confidence: **Very High** for printed trade-name presence; address, operator, and continuity unresolved.

## E-152 — Ralph O. Smith at Palace Saloon, Main/Fifth, 17 September 1909
Type: Primary newspaper liquor-license application; **VISUALLY VERIFIED** 1 September 2026.  
Source: `S-172`.  
Capture: `evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md`.  
Claims:
- The notice names **Ralph O. Smith** as the applicant.
- His place of business is printed as **the Palace Saloon, corner Main and Fifth Sts.**
- He says he will apply for a three-month liquor license at the next regular City Council meeting.
- The notice does not print 501, prove grant, establish real-estate ownership, or prove succession from/to other Fifth/Main liquor applicants.
Confidence: **Very High** for applicant, trade name, intersection, and application wording; exact number, grant, ownership, and succession unresolved.

## E-153 — Joseph Wilson at Palace Saloon, Fifth/Main, 20 June 1912
Type: Primary newspaper liquor-license application; **VISUALLY VERIFIED** 1 September 2026.  
Source: `S-173`; compare `S-118` / `E-104`.  
Capture: `evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md`.  
Claims:
- The notice names **Joseph Wilson** and his place of business as **The Palace Saloon, Fifth and Main streets**.
- He says he will apply for a three-month liquor license at the next regular City Council meeting.
- The independently verified 19 March 1912 notice prints **Joe Wilson's Palace Saloon at 501 Main**. Same business/location and close chronology make Joe/Joseph identity a **strong inference**, but the June notice does not explicitly prove the name equivalence.
- The June notice does not itself print 501, prove grant, property ownership, or operation outside the dated application.
Confidence: **Very High** for June printed wording; **Strong inference** for Joe Wilson = Joseph Wilson; grant/title/uninterrupted continuity unresolved.
"""
append_once("evidence/evidence-register.md", "## E-151 —", evidence_block)

sources_yaml = """  - id: S-171
    name: Oregon City Courier, 24 May 1907, p. 5, Palace Saloon city saloon list
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1907-05-24/ed-1/seq-5.pdf
    repository_file: newspapers/oregon-city-courier/1907-05-24-page-5-palace-saloon-city-list.pdf
    notes: "Visually verified project-steward upload. Lists The Palace Saloon among sixteen Oregon City saloons; no address or proprietor printed. Original filename: Palace Saloon Oregon City Courier May 1907(1).pdf. E-151. SHA-256 6960e6963bfb3c11a00d32d80f8ab6c151f84632f09e83a152400404c4d1ba26."

  - id: S-172
    name: Oregon City Courier, 17 September 1909, p. 5, Ralph O. Smith Palace Saloon license application
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1909-09-17/ed-1/seq-5.pdf
    repository_file: newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf
    notes: "Visually verified project-steward upload. Ralph O. Smith applies at the Palace Saloon, corner Main/Fifth, for three months. Application is not grant/title/exact-501 proof. Original filename preserved in source capture. E-152/P-098/BUS-024. SHA-256 4682715f6ac882a21893a9d3e0729f0f2eef5544bde41517977ee5e7cb0c077a."

  - id: S-173
    name: Morning Enterprise, 20 June 1912, p. 2, Joseph Wilson Palace Saloon license application
    url: https://oregonnews.uoregon.edu/lccn/sn00063701/1912-06-20/ed-1/seq-2.pdf
    repository_file: newspapers/morning-enterprise/1912-06-20-page-2-palace-saloon-joseph-wilson-license.pdf
    notes: "Visually verified project-steward upload. Joseph Wilson applies at The Palace Saloon, Fifth and Main, for three months. Compare March exact-501 Joe Wilson source S-118/E-104; same-person identity is strong inference, not explicit June wording. Original filename preserved in source capture. E-153/BUS-024. SHA-256 72b3f8ddddfbd7703af82a1abfbea9353feb3e7a0c8a81055ce8c869fb858c9a."
"""
append_once("database/sources.yml", "  - id: S-171", sources_yaml)

evidence_yaml = """  - id: E-151
    name: Palace Saloon trade name in Oregon City by 24 May 1907
    type: Primary newspaper city saloon-license article; visually verified
    claims:
      - The 24 May 1907 Oregon City Courier lists The Palace Saloon among sixteen Oregon City saloons.
      - The page prints no Palace address or proprietor; it does not place the business at 501 or identify A. J. Surber as operator.
    confidence: Very High for printed trade-name presence; address, operator and continuity unresolved.
    related_sources: [S-171]
    related_businesses: [BUS-024]
    repository_file: evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md

  - id: E-152
    name: Ralph O. Smith at Palace Saloon, Main/Fifth, 17 September 1909
    type: Primary newspaper liquor-license application; visually verified
    claims:
      - Ralph O. Smith is the named applicant.
      - His place of business is printed as the Palace Saloon, corner Main and Fifth Sts.
      - The notice announces a three-month application and does not prove grant, exact 501 number, property ownership or succession.
    confidence: Very High for applicant, trade name, intersection and application wording; exact number, grant, title and succession unresolved.
    related_sources: [S-172]
    related_businesses: [BUS-024]
    related_people: [P-098]
    repository_file: evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md

  - id: E-153
    name: Joseph Wilson at Palace Saloon, Fifth/Main, 20 June 1912
    type: Primary newspaper liquor-license application; visually verified
    claims:
      - Joseph Wilson is named with The Palace Saloon at Fifth and Main streets in a three-month liquor-license application notice.
      - The 19 March 1912 source separately prints Joe Wilson's Palace Saloon at 501 Main.
      - Joe Wilson equals Joseph Wilson is a strong inference from same business/location and close chronology, not an explicit statement in the June notice.
      - The June page does not itself print 501 or prove license grant, title or uninterrupted operation.
    confidence: Very High for June wording; Strong inference for Joe/Joseph identity; grant, title and uninterrupted continuity unresolved.
    related_sources: [S-173, S-118]
    related_businesses: [BUS-024]
    related_people: [P-037]
    repository_file: evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md
"""
append_once("database/evidence.yml", "  - id: E-151", evidence_yaml)

old_bus = """  - id: BUS-024
    name: Palace Saloon
    address: 501 Main
    notes: Joe Wilson's liquor-license application identifies the Palace Saloon at 501 Main in March 1912. No ownership, continuity, or later business relationship is assumed.
    related_buildings:
      - B-005
    related_people:
      - P-037
    related_evidence:
      - E-104
    related_sources:
      - S-118
    repository_file: businesses/palace-saloon.md"""
new_bus = """  - id: BUS-024
    name: Palace Saloon
    address: 501 Main exact in March 1912; Main/Fifth intersection in September 1909 and June 1912
    notes: The Palace Saloon trade name is listed citywide by May 1907 without address/operator. Ralph O. Smith is a September 1909 applicant at the Palace Saloon, corner Main/Fifth. Joe Wilson is exact at 501 in March 1912; a June 1912 notice prints Joseph Wilson at the Palace, Fifth/Main. Joe/Joseph identity is a strong inference, not explicit name-equivalence proof. No license grant, property ownership, Surber/Case/Hunsaker succession or uninterrupted 1907-1913 continuity is assumed.
    related_buildings:
      - B-005
    related_people:
      - P-037
      - P-098
    related_evidence:
      - E-104
      - E-151
      - E-152
      - E-153
    related_sources:
      - S-118
      - S-171
      - S-172
      - S-173
    repository_file: businesses/palace-saloon.md"""
replace_once("database/businesses.yml", old_bus, new_bus)

old_p37 = """  - id: P-037
    name: Joe Wilson
    role: Palace Saloon liquor-license applicant
    notes: 19 March 1912 notice identifies his Palace Saloon place of business as 501 Main. No building-ownership, business-continuity, or 1922 identity inference.
    related_buildings:
      - B-005
    related_businesses:
      - BUS-024
    related_evidence:
      - E-104
    related_sources:
      - S-118
    repository_file: people/profiles/joe-wilson.md"""
new_p37 = """  - id: P-037
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
    repository_file: people/profiles/joe-wilson.md"""
replace_once("database/people.yml", old_p37, new_p37)

p98_yaml = """  - id: P-098
    name: Ralph O. Smith
    role: Palace Saloon liquor-license applicant
    notes: Visually verified 17 September 1909 Courier notice places Smith at the Palace Saloon, corner Main/Fifth, for a three-month liquor-license application. The notice does not print 501 or prove grant, real-estate ownership or succession to/from other Fifth/Main liquor applicants.
    related_businesses: [BUS-024]
    related_evidence: [E-152]
    related_sources: [S-172]
    repository_file: people/profiles/ralph-o-smith.md
"""
append_once("database/people.yml", "  - id: P-098", p98_yaml)

replace_once(
    "businesses/business-index.md",
    "| BUS-024 | [Palace Saloon](palace-saloon.md) | 501 Main | Joe Wilson's 19 March 1912 application; no ownership/continuity inferred. |",
    "| BUS-024 | [Palace Saloon](palace-saloon.md) | 501 Main exact Mar. 1912; Main/Fifth in Sep. 1909 & Jun. 1912 | Trade name attested by May 1907; Ralph O. Smith applicant 1909; Joe/Joseph Wilson 1912. Grants, property ownership and operator succession remain unresolved. |",
)

people_index_block = """## Palace Saloon applicant added from uploaded primary source

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-098 | [Ralph O. Smith](profiles/ralph-o-smith.md) | Palace Saloon liquor-license applicant | 17 Sep. 1909 notice places him at Palace Saloon, corner Main/Fifth. Application is not grant/title/exact-501 or succession proof. `E-152` / `S-172`. |
"""
append_once("people/people-index.md", "| P-098 |", people_index_block)

palace_page = """# Palace Saloon

Business ID: `BUS-024`. Exact numbered address is directly proved at **501 Main Street (`B-005`) in March 1912**; separate 1909 and June 1912 notices use the **Main/Fifth** intersection.

## Verified chronology

- **24 May 1907 — `E-151` / `S-171`:** an *Oregon City Courier* article listing the city's sixteen saloons includes **The Palace Saloon**. No Palace address or proprietor is printed.
- **17 September 1909 — `E-152` / `S-172`:** **Ralph O. Smith (`P-098`)** announces a three-month liquor-license application at **the Palace Saloon, corner Main and Fifth Sts.** The notice does not print 501 or prove the Council granted the license.
- **19 March 1912 — `E-104` / `S-118`:** **Joe Wilson (`P-037`)** is directly identified with **the Palace Saloon, 501 Main Street**.
- **20 June 1912 — `E-153` / `S-173`:** **Joseph Wilson** announces a three-month liquor-license application at **The Palace Saloon, Fifth and Main streets**. Because this is the same trade name/location only three months after the Joe Wilson exact-501 notice, Joe/Joseph same-person identity is treated as a **strong inference**, not an explicit legal-name statement.
- **3 October 1913 — `E-104` / `S-119`:** **Hunsaker & Taylor** are separately named at **501 Main**, but the notice does not use the Palace Saloon trade name.

## Limits

The archive does **not** presently prove:
- that the May 1907 Palace Saloon occupied 501 Main;
- that A. J. Surber's October 1907 exact-501 liquor premises were the Palace Saloon;
- a continuous Palace Saloon operation from 1907 through 1912;
- the transfer sequence among Surber, Justin & Hitchman, Ralph O. Smith, E. R. Case, Joe/Joseph Wilson, or Hunsaker & Taylor;
- license grants, real-estate ownership, or building ownership from these application notices.

The 1909 and June 1912 intersection descriptions are therefore not silently normalized to 501. The March 1912 notice remains the direct exact-number anchor.

See the [uploaded-page visual review](../evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md), [501 Main unified timeline](../timelines/501-main.md), `OQ-032`, and `RL-045`.
"""
write("businesses/palace-saloon.md", palace_page)

joe_page = """# Joe Wilson

Person ID: `P-037`. Related business/building: `BUS-024`, `B-005`.

The visually reviewed **19 March 1912 Morning Enterprise** liquor-license notice identifies **Joe Wilson's Palace Saloon at 501 Main Street** (`E-104` / `S-118`).

A second visually reviewed notice dated **20 June 1912** prints **Joseph Wilson** at **The Palace Saloon, Fifth and Main streets**, again applying for a three-month liquor license (`E-153` / `S-173`). Same trade name, same intersection, and close chronology make **Joe Wilson = Joseph Wilson a strong identity inference**. The June notice does not itself state that Joe is a nickname or otherwise supply independent legal-name proof, so that distinction is preserved.

The notices prove dated applicants, trade-name/location wording, and the March exact address. They do not establish real-estate ownership, license grant, uninterrupted operation, or a direct Surber / Ralph O. Smith / E. R. Case → Wilson → Hunsaker & Taylor business succession.
"""
write("people/profiles/joe-wilson.md", joe_page)

replace_once(
    "timelines/501-main.md",
    "| 4 Oct. 1907 | A. J. Surber liquor-renewal application at **No. 501**, Main/Fifth. | **Exact, visually verified**; application is not grant/title/later continuity. | `BUS-045`; `P-055`; `E-121`; `S-135` |",
    "| 24 May 1907 | **Palace Saloon** named among Oregon City's sixteen saloons. | **Citywide business-name context only**; no address/operator printed, so not assigned to 501. | `BUS-024`; `E-151`; `S-171` |\n| 4 Oct. 1907 | A. J. Surber liquor-renewal application at **No. 501**, Main/Fifth. | **Exact, visually verified**; application is not grant/title/later continuity and the notice does not call it Palace Saloon. | `BUS-045`; `P-055`; `E-121`; `S-135` |",
)
replace_once(
    "timelines/501-main.md",
    "| 18 Sep. 1908 | Surber and separately Justin & Hitchman apply at Fifth/Main; numbers omitted. | Intersection context; no 501 continuity/shared-room inference. | `E-121`, `E-122`; `S-137` |",
    "| 18 Sep. 1908 | Surber and separately Justin & Hitchman apply at Fifth/Main; numbers omitted. | Intersection context; no 501 continuity/shared-room inference. | `E-121`, `E-122`; `S-137` |\n| 17 Sep. 1909 | Ralph O. Smith applies at **Palace Saloon, corner Main/Fifth**. | **Intersection/trade-name context**; 501 not printed; application is not grant/title/succession proof. | `BUS-024`; `P-098`; `E-152`; `S-172` |",
)
replace_once(
    "timelines/501-main.md",
    "| 19 Mar. 1912 | Joe Wilson's **Palace Saloon, 501 Main** license application. | **Exact, visually verified**; no Surber succession, grant, title, or continuity. | `BUS-024`; `P-037`; `E-104`; `S-118` |",
    "| 19 Mar. 1912 | Joe Wilson's **Palace Saloon, 501 Main** license application. | **Exact, visually verified**; no Surber succession, grant, title, or continuity. | `BUS-024`; `P-037`; `E-104`; `S-118` |\n| 20 Jun. 1912 | **Joseph Wilson**, The Palace Saloon, **Fifth/Main**, three-month application. | **Visually verified intersection context**; June page omits 501. Joe=Joseph is a strong inference from same business/location/date sequence, not explicit name proof. | `BUS-024`; `P-037`; `E-153`; `S-173` |",
)

replace_once(
    "registers/business-timeline.md",
    "| 4 Oct.1907 | A. J. Surber liquor premises | `BUS-045` | `E-121` | Very High for wording | Renewal notice prints No.501; no grant, deed or Palace trade name. |\n| 19 Mar. 1912 | Joe Wilson's Palace Saloon | `BUS-024` | `E-104` | Very High | Liquor-license application at 501 Main; no transfer or later-continuity claim. |",
    "| 24 May 1907 | Palace Saloon | `BUS-024` | `E-151` | Very High for trade-name presence | Listed among sixteen city saloons; no address/operator printed. |\n| 4 Oct.1907 | A. J. Surber liquor premises | `BUS-045` | `E-121` | Very High for wording | Renewal notice prints No.501; no grant, deed or Palace trade name. |\n| 17 Sep. 1909 | Palace Saloon / Ralph O. Smith | `BUS-024` | `E-152` | Very High for printed intersection/application | Palace Saloon at corner Main/Fifth; 501 not printed; grant/succession unproved. |\n| 19 Mar. 1912 | Joe Wilson's Palace Saloon | `BUS-024` | `E-104` | Very High | Liquor-license application at 501 Main; no transfer or later-continuity claim. |\n| 20 Jun. 1912 | Palace Saloon / Joseph Wilson | `BUS-024` | `E-153` | Very High wording; Strong Joe/Joseph identity inference | Fifth/Main application; exact 501 omitted in June; compare March exact-501 notice. |",
)

insert_after(
    "buildings/501-main.md",
    "The September 18, 1908 Surber notice repeats Fifth/Main without a number; the same page separately names Justin & Hitchman at that intersection. Neither the partnership nor Strebig's unnumbered Fifth/Main market is assigned to501 (E-122/E-123). [Full review](../evidence/source-captures/1907-1908-surber-justin-main-visual-review.md). OQ-032/RL-045 retain license, identity and corner questions.",
    "## Palace Saloon context added from 1907–1912 uploads",
    """## Palace Saloon context added from 1907–1912 uploads

New visually verified Palace Saloon pages refine the business chronology without changing the standard for exact 501 assignment (`E-151`–`E-153`; `S-171`–`S-173`). The trade name is present citywide by **24 May 1907** but without address/operator. On **17 September 1909**, Ralph O. Smith applies at the **Palace Saloon, corner Main/Fifth**, again without a number. The **20 June 1912** Joseph Wilson notice repeats Palace Saloon at Fifth/Main three months after the separate exact-501 Joe Wilson notice.

Only the **19 March 1912** source directly prints **501 Main** for Palace Saloon. Do not backfill 501 onto the 1907 or 1909 pages, equate Surber's exact-501 premises with Palace solely from proximity, or treat application notices as license grants/title.""",
)

insert_after(
    "timeline.md",
    "Contemporary geographic anchors include the **Mount Hood Cafe at the Fifth/Main context** (`E-067`) and **John Gohra's saloon at Main & Sixth** (`E-068`). An August advertisement also places **I. Tolpolar on Main Street opposite the Post Office** (`E-069`). Those earlier sources did not print an exact target number. **A newly reviewed 4 October 1907 Courier p3 notice now directly identifies A. J. Surber at No.501, Main/Fifth** (E-121/S-135), superseding the earlier no-target-result summary. December 13 p3 names Justin & Hitchman at unnumbered Fifth/Main (E-122/S-136). Strebig fresh meats at Albright's Old Stand, Fifth/Main, and other dated Main anchors are in E-123. No business grant, property transfer or structural continuity is inferred.",
    "The Palace Saloon trade name is now independently attested by **24 May 1907**",
    "The Palace Saloon trade name is now independently attested by **24 May 1907** (`E-151` / `S-171`), when a *Courier* city-saloon article lists it among sixteen saloons. That page gives no proprietor or address, so it does not identify Surber's later exact-501 premises as Palace Saloon.",
)
insert_after(
    "timeline.md",
    "At the north end of the block, the 6 October Council record places **Carl G. Hodes at Sixth & Main** as a saloon-license renewal applicant (`E-076`). On 1 December the Council ordered **Philip Street** to remove rubbish from Sixth Street caused by **repair of his building at Sixth & Main** (`E-075`). These are strong intersection anchors, but the evidence does not establish that the Hodes saloon, Philip Street's building, and the earlier William Tell/Gambrinus lot-8 property were the same premises.",
    "A newly supplied **17 September 1909**",
    "A newly supplied **17 September 1909** *Courier* license notice identifies **Ralph O. Smith** (`P-098`) at **the Palace Saloon, corner Main and Fifth Streets** (`E-152` / `S-172`). The notice does not print 501 or prove the license was granted. It narrows the Palace trade-name chronology but does not establish succession from Surber/Justin & Hitchman or forward to E. R. Case.",
)
insert_after(
    "timeline.md",
    "On 19 March, a visually verified *Morning Enterprise* liquor-license notice identifies **Joe Wilson's Palace Saloon at 501 Main Street** (`E-104` / `S-118`). A separate local item identifies the H. M. Templeton home at **513 Fifth Street**, then occupied by M. D. Phillips and family (`E-106`). The 501 notice does not establish building ownership, continuity into later occupants, or the 1922 fire-origin location; 513 Fifth is not mapped to the target commercial/fire cluster.",
    "A second Palace Saloon application on **20 June 1912**",
    "A second Palace Saloon application on **20 June 1912** names **Joseph Wilson** at **The Palace Saloon, Fifth and Main streets** (`E-153` / `S-173`). Same trade name/location only three months after the exact-501 Joe Wilson notice makes Joe/Joseph identity a strong inference; the June page itself does not explicitly prove the name equivalence and does not print 501.",
)

insert_after(
    "evidence/open-questions.md",
    "No shared business, succession, property title, exact Justin/Hartman number or 1922 room is established. Track the independently dated Stewart327/Hodes327/Sixth-Main chain without inventing transfers. See E-123, RL-045 and [review](source-captures/1907-1908-surber-justin-main-visual-review.md).",
    "**Palace Saloon supplement:**",
    "**Palace Saloon supplement:** `E-151`–`E-153` now establishes the Palace trade name by May 1907, **Ralph O. Smith at Palace Saloon, Main/Fifth in September 1909**, and **Joseph Wilson at Palace Saloon, Fifth/Main in June 1912**, alongside the existing March 1912 exact-501 Joe Wilson notice. Still unresolved: whether May 1907 Palace was at 501; whether Surber's 1907/1908 premises were Palace; the Smith→Case→Wilson transfer/grant sequence; and whether Joe/Joseph Wilson can be independently identified beyond the strong same-business/location inference.",
)
insert_after(
    "evidence/research-leads.md",
    "4. Test Strebig/Streibig/Albright and Stewart327→Hodes327→Sixth/Main through explicit identity/transition records. Do not infer a transfer from a common corner/address.",
    "5. Use `E-151`–`E-153`",
    "5. Use `E-151`–`E-153` / `S-171`–`S-173` to target Council/license records for the **Palace Saloon**: May 1907 trade-name presence (no address/operator), Ralph O. Smith's September 1909 Main/Fifth application, and Joe/Joseph Wilson's March–June 1912 applications. Recover actual grants, applicant/proprietor identities, transfer dates and precise premises. Do not backfill 501 onto the 1907/1909 notices or assume Surber/Case/Wilson succession.",
)

replace_once(
    "indexes/id-crosswalk.md",
    "| `B-005` 501 Main Street (historic / removed) | `BUS-045` A. J. Surber; `BUS-024` Palace Saloon; `BUS-025` Hunsaker & Taylor; 1925 store occupant unknown | Unified chronology: `timelines/501-main.md`. `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`. The records do not prove a transfer or uninterrupted continuity. |",
    "| `B-005` 501 Main Street (historic / removed) | `BUS-045` A. J. Surber; `BUS-024` Palace Saloon; `BUS-025` Hunsaker & Taylor; 1925 store occupant unknown | Unified chronology: `timelines/501-main.md`. `E-020`, `E-021`, `E-054`–`E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`. `E-151`–`E-153` refine Palace chronology, but only `E-104` directly prints Palace at 501; 1907/1909/June-1912 intersection/name context is not backfilled to the number. |",
)
append_once(
    "indexes/id-crosswalk.md",
    "| `P-098` Ralph O. Smith |",
    """## Palace Saloon 1909 person crosswalk

| Person / entity | Related business | Evidence / source | Limits |
| --- | --- | --- | --- |
| `P-098` Ralph O. Smith | `BUS-024` Palace Saloon | `E-152`, `S-172` | 17 Sep. 1909 applicant at Palace Saloon, corner Main/Fifth; 501, grant, title and succession unproved. |""",
)

archive_block = """## Palace Saloon uploaded primary pages — 1907, 1909, 1912

[Visual review](evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md) preserves all three supplied PDFs as `S-171`–`S-173` / `E-151`–`E-153`. The Palace Saloon trade name is now verified by May 1907 without address/operator; Ralph O. Smith is verified at the Palace Saloon, Main/Fifth in September 1909; and Joseph Wilson is verified there in June 1912. The existing March 1912 Joe Wilson source remains the direct exact-501 anchor. Grants, property title and operator succession remain open; no intersection-only notice is silently converted to 501.
"""
append_once("ARCHIVE_INDEX.md", "## Palace Saloon uploaded primary pages", archive_block)

research_log_block = """### 2026-09-01 — three Palace Saloon pages integrated
- Visually reviewed and preserved three project-steward supplied newspaper pages: 24 May 1907 *Oregon City Courier* p. 5, 17 September 1909 *Oregon City Courier* p. 5, and 20 June 1912 *Morning Enterprise* p. 2 (`S-171`–`S-173`; `E-151`–`E-153`).
- May 1907 proves the Palace Saloon trade name in Oregon City but prints no address/proprietor.
- September 1909 names new person `P-098` Ralph O. Smith at the Palace Saloon, corner Main/Fifth, in a three-month license application; no 501/grant/title/succession inference.
- June 1912 names Joseph Wilson at The Palace Saloon, Fifth/Main. Compared with March 1912 Joe Wilson at exact 501, Joe=Joseph is recorded as a strong same-business/location inference, not explicit name proof.
- Original uploaded filenames and SHA-256 hashes are preserved in the source capture/register. Palace business/person/timeline/crosswalk/open-question/research-lead/YAML mirrors synchronized.
"""
append_once("registers/research-log.md", "### 2026-09-01 — three Palace Saloon pages integrated", research_log_block)

manifest = {
    "review_date": "2026-09-01",
    "status": "VISUALLY VERIFIED",
    "files": [
        {
            "source_id": "S-171",
            "evidence_id": "E-151",
            "repository_file": DOWNLOADS[0]["path"],
            "original_uploaded_filename": "Palace Saloon Oregon City Courier May 1907(1).pdf",
            "sha256": DOWNLOADS[0]["sha256"],
            "bytes": DOWNLOADS[0]["size"],
            "canonical_url": DOWNLOADS[0]["url"],
        },
        {
            "source_id": "S-172",
            "evidence_id": "E-152",
            "repository_file": DOWNLOADS[1]["path"],
            "original_uploaded_filename": "Palace Saloon (Liquor License) Oregon City courier., September 17, 1909, Page 5, Image 5.pdf",
            "sha256": DOWNLOADS[1]["sha256"],
            "bytes": DOWNLOADS[1]["size"],
            "canonical_url": DOWNLOADS[1]["url"],
        },
        {
            "source_id": "S-173",
            "evidence_id": "E-153",
            "repository_file": DOWNLOADS[2]["path"],
            "original_uploaded_filename": "Palace Saloon (Liquor Licence) Morning enterprise., June 20, 1912, Page 2, Image 2.pdf",
            "sha256": DOWNLOADS[2]["sha256"],
            "bytes": DOWNLOADS[2]["size"],
            "canonical_url": DOWNLOADS[2]["url"],
        },
    ],
    "interpretive_limits": [
        "May 1907 Palace Saloon has no printed address or proprietor.",
        "September 1909 Palace notice prints Main/Fifth but not 501 and is an application, not a grant.",
        "June 1912 prints Joseph Wilson at Palace Saloon Fifth/Main; Joe/Joseph identity is strong inference, not explicit legal-name proof.",
    ],
}
write(
    "evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-manifest.json",
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
)

print("Palace Saloon uploaded-page integration prepared.")
