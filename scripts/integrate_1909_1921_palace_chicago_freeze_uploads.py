#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import urllib.request

PAGES = [
    {
        "key": "pal1909",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-12-31/ed-1/seq-7.pdf",
        "sha256": "ef4faeabb47ad6c6d91f0f642a07dd55bbc1a8ac6ea69e705224752517e1de02",
        "size": 716264,
        "repo_path": "newspapers/oregon-city-courier/1909-12-31-page-7-palace-saloon-ralph-o-smith-license.pdf",
        "upload_name": "Palace Saloon (Liquor License) Oregon City courier., December 31, 1909, Image 7.pdf",
    },
    {
        "key": "pal1910",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1910-06-17/ed-1/seq-7.pdf",
        "sha256": "1030dd2e183a480980cb29fc3b581599b9a083008ced224dd20fe8131ce9ae9e",
        "size": 677673,
        "repo_path": "newspapers/oregon-city-courier/1910-06-17-page-7-palace-saloon-er-case-510-main.pdf",
        "upload_name": "Palace Saloon (Liquor Licence) Oregon City courier., June 17, 1910, Page 7, Image 7.pdf",
    },
    {
        "key": "chi1911",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1911-04-14/ed-1/seq-7.pdf",
        "sha256": "f8aa2ced33d9a4f4752663a3163c6c85992e477f0533df4800bdacecef6a5f99",
        "size": 728085,
        "repo_path": "newspapers/oregon-city-courier/1911-04-14-page-7-chicago-store-505-main.pdf",
        "upload_name": "505 Main (Chicago Store) Oregon City courier., April 14, 1911, Page 7, Image 7.pdf",
    },
    {
        "key": "freeze1921",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1921-05-13/ed-1/seq-8.pdf",
        "sha256": "58b02eaa1db84acdc61b86492170d7bc4af5ebe447bb2c17a6fd83324ffbd8d9",
        "size": 836158,
        "repo_path": "newspapers/oregon-city-enterprise/1921-05-13-page-8-dr-freeze-505-main.pdf",
        "upload_name": "505 & half Main (Dr Freeze) Oregon City enterprise., May 13, 1921, Page Page 8, Image 8.pdf",
    },
]

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def write(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")

def append_to_md_section(path: str, heading: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    pattern = re.compile(r"(?ms)^" + re.escape(heading) + r"\n.*?(?=^## |\Z)")
    m = pattern.search(text)
    if not m:
        raise SystemExit(f"Missing section {heading!r} in {path}")
    section = m.group(0).rstrip() + "\n\n" + block.rstrip() + "\n"
    write(path, text[:m.start()] + section + "\n" + text[m.end():])

def yaml_record(path: str, ident: str) -> tuple[str, re.Match]:
    text = read(path)
    pattern = re.compile(r"(?ms)^  - id: " + re.escape(ident) + r"\n.*?(?=^  - id: |\Z)")
    m = pattern.search(text)
    if not m:
        raise SystemExit(f"Missing YAML record {ident} in {path}")
    return text, m

def mutate_yaml_record(path: str, ident: str, mutator) -> None:
    text, m = yaml_record(path, ident)
    old = m.group(0)
    new = mutator(old)
    if new == old:
        raise SystemExit(f"Mutation for {ident} in {path} made no change")
    write(path, text[:m.start()] + new.rstrip() + "\n\n" + text[m.end():])

def append_yaml_once(path: str, ident: str, block: str) -> None:
    text = read(path)
    if re.search(r"(?m)^  - id: " + re.escape(ident) + r"$", text):
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")

# Immutable ID guards. Never reuse or renumber an assigned ID.
guards = [
    ("S-198", "evidence/source-register.md", r"(?m)^## S-198\b"),
    ("S-199", "evidence/source-register.md", r"(?m)^## S-199\b"),
    ("E-177", "evidence/evidence-register.md", r"(?m)^## E-177\b"),
    ("E-178", "evidence/evidence-register.md", r"(?m)^## E-178\b"),
    ("P-105", "people/people-index.md", r"(?m)^\| P-105 \|"),
    ("T-069", "database/timeline.yml", r"(?m)^  - id: T-069$"),
    ("T-070", "database/timeline.yml", r"(?m)^  - id: T-070$"),
    ("T-071", "database/timeline.yml", r"(?m)^  - id: T-071$"),
]
for ident, path, pattern in guards:
    if re.search(pattern, read(path)):
        raise SystemExit(f"{ident} is already assigned in {path}; stop rather than reuse/renumber.")

# Reconcile exact supplied binaries by SHA-256 across the whole repository.
existing_by_hash = {}
for pdf in Path(".").rglob("*.pdf"):
    try:
        existing_by_hash.setdefault(digest(pdf), str(pdf))
    except OSError:
        pass

for item in PAGES:
    found = existing_by_hash.get(item["sha256"])
    if found:
        if Path(found).stat().st_size != item["size"]:
            raise SystemExit(f"Hash match with unexpected size: {found}")
        item["actual_path"] = found
        item["handling"] = "already present; exact SHA-256 deduplicated"
        continue

    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    got = hashlib.sha256(data).hexdigest()
    if got != item["sha256"] or len(data) != item["size"]:
        raise SystemExit(
            f"Canonical page mismatch for {item['key']}: got sha={got}, bytes={len(data)}; "
            f"expected uploaded sha={item['sha256']}, bytes={item['size']}"
        )
    target = Path(item["repo_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    item["actual_path"] = item["repo_path"]
    item["handling"] = "newly preserved; byte-for-byte identical to steward upload"
    existing_by_hash[item["sha256"]] = item["repo_path"]

by = {x["key"]: x for x in PAGES}

# Permanent four-file reconciliation/provenance record.
capture = f"""# 1909–1921 Palace / Chicago / Freeze steward-upload reconciliation

Review date: **2 September 2026**.

Status: **FOUR PROJECT-STEWARD NEWSPAPER PDF UPLOADS VISUALLY REVIEWED AND RECONCILED BY SHA-256.** Page-level integration does not change any annual research status.

## File reconciliation

| Supplied file | SHA-256 / bytes | Repository PDF | Handling | Source/evidence |
| --- | --- | --- | --- | --- |
| `{by['pal1909']['upload_name']}` | `{by['pal1909']['sha256']}` / {by['pal1909']['size']} | `{by['pal1909']['actual_path']}` | **{by['pal1909']['handling']}** | `S-198` / `E-177` |
| `{by['pal1910']['upload_name']}` | `{by['pal1910']['sha256']}` / {by['pal1910']['size']} | `{by['pal1910']['actual_path']}` | **{by['pal1910']['handling']}** | `S-199` / `E-178` |
| `{by['chi1911']['upload_name']}` | `{by['chi1911']['sha256']}` / {by['chi1911']['size']} | `{by['chi1911']['actual_path']}` | **{by['chi1911']['handling']}** | existing grouped `S-032` / `E-026` |
| `{by['freeze1921']['upload_name']}` | `{by['freeze1921']['sha256']}` / {by['freeze1921']['size']} | `{by['freeze1921']['actual_path']}` | **{by['freeze1921']['handling']}** | existing grouped `S-035` / `E-028` |

## 31 December 1909 — Ralph O. Smith / Palace Saloon

The visually inspected *Oregon City Courier* page prints a liquor-license application by **Ralph O. Smith** at **the Palace Saloon, corner Main and Fifth Sts.**, for **six months**.

This directly extends Smith's documented Palace association beyond his 17 September 1909 three-month application. It does not print 501, prove the Council granted the license, establish real-estate ownership, or prove uninterrupted operation between the dated notices.

## 17 June 1910 — E. R. Case / Palace Saloon / printed 510 Main

The visually inspected *Courier* page directly prints an application by **E. R. Case** at **the Palace Saloon, 510 Main street**, for three months.

This is independently consistent with the 1 June 1910 City Council record (`S-093` / `E-080`) placing **E. R. Case's saloon at Fifth and Main** with an adjoining restaurant. The newspaper adds the Palace trade name and a printed exact number.

The archive preserves **510 Main exactly as printed**. It is not normalized to 501. Later evidence directly places Joe Wilson's Palace Saloon at **501 Main** in March 1912, while separate advertisements place Pacific Telephone & Telegraph at **510 Main** beginning in August 1910. The possibilities include a Palace move, an address/numbering issue, a newspaper error, or another explanation; the present evidence does not select among them.

## 14 April 1911 — Chicago Store / exact 505 Main

The visually inspected *Courier* page directly advertises **The Chicago Store** at **505 Main St., Oregon City, Or.**, offering new and second-hand clothing plus cleaning and repairing. This was already represented historically under `S-032` / `E-026`; this integration preserves the previously missing exact 14 April page PDF and upgrades that specific page to a steward-supplied visually verified scan.

The ad does not name Wolf & Nat, prove property ownership, or prove continuity of the physical building.

## 13 May 1921 — Dr. Freeze / printed 505 Main

Despite the steward filename containing “505 & half,” the actual visually inspected advertisement prints **Dr. Freeze, Eye Specialist, 505 Main St. Oregon City**, with **no half-number visible**.

The directly verified sequence now includes:
- 8 April 1921 — **505½ Main**
- 13 May 1921 — **505 Main**
- 20 May 1921 — **505½ Main**
- 28 October 1921 — **505 Main**
- 30 June 1922 — **505½ Main**

This alternating printed usage strengthens the archive rule that `505` versus `505½` is an address-form variation unless a source independently establishes the physical arrangement. It does **not** prove an upper floor, ground floor, side-by-side split, front/rear split, or a physical move between subdivisions.

## Method / limits

- Claims above come from direct visual inspection of the supplied page scans, not filenames or OCR alone.
- Applications are not treated as license grants.
- Business operation, business ownership, real-estate ownership, street address, and physical building identity remain separate questions.
- Conflicting address evidence is retained rather than silently corrected.
- No annual year-closeout status is changed by this targeted four-page integration.
"""
write("evidence/source-captures/1909-1921-palace-chicago-freeze-steward-upload-reconciliation-2026-09-02.md", capture)

# Existing grouped source/evidence records: preserve existing information and add exact-page provenance.
append_to_md_section(
    "evidence/source-register.md",
    "## S-032 — Chicago Store advertisements, 1911-1913",
    "14 April 1911 steward-page preservation — 2 September 2026",
    f"""### 14 April 1911 steward-page preservation — 2 September 2026
The exact visually inspected page is now preserved at `{by['chi1911']['actual_path']}`. Original uploaded filename: `{by['chi1911']['upload_name']}`. SHA-256 `{by['chi1911']['sha256']}` ({by['chi1911']['size']} bytes). The ad directly prints **The Chicago Store, 505 Main St.**, plus new/second-hand clothing and cleaning/repairing. Existing `E-026` continues to carry the claim; no duplicate source/evidence ID is created."""
)
append_to_md_section(
    "evidence/source-register.md",
    "## S-035 — Dr. Freeze Eye Specialist advertisements, 1921-1922",
    "13 May 1921 steward-page preservation — 2 September 2026",
    f"""### 13 May 1921 steward-page preservation — 2 September 2026
The exact visually inspected page is now preserved at `{by['freeze1921']['actual_path']}`. Original uploaded filename: `{by['freeze1921']['upload_name']}`. SHA-256 `{by['freeze1921']['sha256']}` ({by['freeze1921']['size']} bytes). The advertisement itself prints **505 Main St.**, not 505½. Existing `E-028` retains this as printed address variation; no physical room/floor/layout inference is made."""
)
append_to_md_section(
    "evidence/evidence-register.md",
    "## E-026 — The Chicago Store at 505 Main, 1911-1913",
    "14 April 1911 visual-preservation update",
    """### 14 April 1911 visual-preservation update
The exact 14 April 1911 *Courier* page is now physically preserved and visually verified. It directly repeats **The Chicago Store, 505 Main St.** and its clothing/cleaning/repairing services. This strengthens page-level provenance but does not add proprietor, title, or surviving-building continuity."""
)
append_to_md_section(
    "evidence/evidence-register.md",
    "## E-028 — Dr. Freeze, Eye Specialist, 505 / 505 1/2 Main, 1921-1922",
    "13 May 1921 printed-address update",
    """### 13 May 1921 printed-address update
A visually verified 13 May 1921 *Enterprise* advertisement prints **505 Main St.** without the half-number; the 20 May page returns to **505½ Main**. The one-week alternation makes the source-level `505`/`505½` variation especially clear and further cautions against inferring a floor, room, storefront section, or physical move from the number form alone."""
)

def s032_mut(block: str) -> str:
    old = '    notes: "Exact supplied page PDFs preserved for 31 March, 7 April and 28 April 1911 at 505 Main; also 14 April 1911 Courier and 8 January 1913 Morning Enterprise. Related evidence E-026. Repository PDFs: newspapers/oregon-city-courier/1911-03-31-page-6-chicago-store-505-main.pdf; newspapers/oregon-city-courier/1911-04-07-page-6-chicago-store-505-main.pdf; newspapers/oregon-city-courier/1911-04-28-page-7-chicago-store-505-main.pdf."'
    new = f'    notes: "Exact steward-supplied page PDFs preserved for 31 March, 7 April, 14 April and 28 April 1911 at 505 Main; also 8 January 1913 Morning Enterprise. Related evidence E-026. Repository PDFs: newspapers/oregon-city-courier/1911-03-31-page-6-chicago-store-505-main.pdf; newspapers/oregon-city-courier/1911-04-07-page-6-chicago-store-505-main.pdf; {by["chi1911"]["actual_path"]}; newspapers/oregon-city-courier/1911-04-28-page-7-chicago-store-505-main.pdf."'
    if old not in block:
        raise SystemExit("Unexpected S-032 YAML notes; refusing blind replacement")
    return block.replace(old, new, 1)
mutate_yaml_record("database/sources.yml", "S-032", s032_mut)

def s035_mut(block: str) -> str:
    needle = "20 May 1921 at 505½ Main (newspapers/oregon-city-enterprise/1921-05-20-page-3-dr-freeze-505-half-witham-munden-514-main.pdf),"
    replacement = f"13 May 1921 at printed 505 Main ({by['freeze1921']['actual_path']}), 20 May 1921 at 505½ Main (newspapers/oregon-city-enterprise/1921-05-20-page-3-dr-freeze-505-half-witham-munden-514-main.pdf),"
    if needle not in block:
        raise SystemExit("Unexpected S-035 YAML notes; refusing blind replacement")
    return block.replace(needle, replacement, 1)
mutate_yaml_record("database/sources.yml", "S-035", s035_mut)

def e026_mut(block: str) -> str:
    old = "31 March, 7 April and 28 April"
    if old not in block:
        raise SystemExit("Expected E-026 visual-page phrase not found")
    return block.replace(old, "31 March, 7 April, 14 April and 28 April", 1)
mutate_yaml_record("database/evidence.yml", "E-026", e026_mut)

def e028_mut(block: str) -> str:
    needle = "      - 8 April and 20 May 1921 Enterprise advertisements print Dr. Freeze, Eye Specialist, at 505 1/2 Main.\n"
    insert = (
        "      - 8 April and 20 May 1921 Enterprise advertisements print Dr. Freeze, Eye Specialist, at 505 1/2 Main.\n"
        "      - A visually verified 13 May 1921 Enterprise advertisement between those dates prints 505 Main without the half-number; this one-week alternation is source-level address variation, not proof of a physical room or floor move.\n"
    )
    if needle not in block:
        raise SystemExit("Expected E-028 claim not found")
    return block.replace(needle, insert, 1)
mutate_yaml_record("database/evidence.yml", "E-028", e028_mut)

# New Palace source records.
append_once(
    "evidence/source-register.md",
    "## S-198 — Oregon City Courier, 31 December 1909, Ralph O. Smith Palace Saloon license application",
    f"""## S-198 — Oregon City Courier, 31 December 1909, Ralph O. Smith Palace Saloon license application
Canonical PDF: {by['pal1909']['url']}  
Repository PDF: `{by['pal1909']['actual_path']}`  
Original uploaded filename: `{by['pal1909']['upload_name']}`  
Type: Primary newspaper liquor-license application; **VISUALLY VERIFIED**.  
Related evidence: `E-177`; person `P-098`; business `BUS-024`.  
Notes: Ralph O. Smith applies at **the Palace Saloon, corner Main and Fifth Sts.**, for **six months**. The notice does not print 501, prove the license was granted, establish real-estate ownership, or prove uninterrupted operation from the prior September notice. SHA-256 `{by['pal1909']['sha256']}` ({by['pal1909']['size']} bytes)."""
)
append_once(
    "evidence/source-register.md",
    "## S-199 — Oregon City Courier, 17 June 1910, E. R. Case Palace Saloon at printed 510 Main",
    f"""## S-199 — Oregon City Courier, 17 June 1910, E. R. Case Palace Saloon at printed 510 Main
Canonical PDF: {by['pal1910']['url']}  
Repository PDF: `{by['pal1910']['actual_path']}`  
Original uploaded filename: `{by['pal1910']['upload_name']}`  
Type: Primary newspaper liquor-license application; **VISUALLY VERIFIED**.  
Related evidence: `E-178`, cross-reference `E-080`; person `P-105`; business `BUS-024`.  
Notes: E. R. Case applies for a three-month liquor license at **the Palace Saloon, 510 Main street**. Preserve `510` exactly as printed. A 1 June municipal record independently places Case's saloon at Fifth/Main; later Palace evidence prints 501 under Joe Wilson, and Pacific Telephone later prints 510. No move, typo, renumbering, grant, ownership, or physical-premises explanation is assumed. SHA-256 `{by['pal1910']['sha256']}` ({by['pal1910']['size']} bytes)."""
)

append_once(
    "evidence/evidence-register.md",
    "## E-177 — Ralph O. Smith at Palace Saloon, Main/Fifth, 31 December 1909",
    """## E-177 — Ralph O. Smith at Palace Saloon, Main/Fifth, 31 December 1909
Type: Primary newspaper liquor-license application; **VISUALLY VERIFIED**  
Source: `S-198`  
Claims: The 31 December 1909 *Oregon City Courier* directly names **Ralph O. Smith** applying for a **six-month** liquor license at **the Palace Saloon, corner Main and Fifth Sts.** This extends Smith's directly documented Palace association beyond the 17 September 1909 three-month application. The source does not print 501, prove a license grant, property ownership, or uninterrupted operation between notices.  
Confidence: **Very High** for applicant, trade name, intersection, date, and requested term; exact number, grant, title, and continuity unresolved.  
Related record: `evidence/E-177-1909-12-31-ralph-o-smith-palace-saloon.md`"""
)
append_once(
    "evidence/evidence-register.md",
    "## E-178 — E. R. Case applies at Palace Saloon, printed 510 Main, 17 June 1910",
    """## E-178 — E. R. Case applies at Palace Saloon, printed 510 Main, 17 June 1910
Type: Primary newspaper liquor-license application plus municipal cross-reference; **VISUALLY VERIFIED** newspaper page  
Sources: `S-199`; cross-reference `S-093` / `E-080`  
Claims: The 17 June 1910 *Oregon City Courier* directly names **E. R. Case** applying for a three-month liquor license at **the Palace Saloon, 510 Main street**. The 1 June 1910 City Council record independently places **E. R. Case's saloon at Fifth and Main** with an adjoining restaurant. Together the sources strongly connect the same named operator/trade context, but the archive preserves the newspaper's exact `510` and does not normalize it to 501. Later Joe Wilson Palace evidence directly prints 501 in March 1912, while Pacific Telephone advertisements print 510 beginning in August 1910. The reason for the 510/501 and June/August 510 sequence is unresolved.  
Confidence: **Very High** for the printed Case/Palace/510 application and the separate municipal Case/Fifth-Main statement; **Unresolved conflict** for how 510 relates to later 501 Palace and later 510 telephone occupancy.  
Related record: `evidence/E-178-1910-06-17-er-case-palace-saloon-510-main.md`"""
)

write("evidence/E-177-1909-12-31-ralph-o-smith-palace-saloon.md", """# E-177 — Ralph O. Smith at Palace Saloon, Main/Fifth, 31 December 1909

Type: Primary newspaper liquor-license application.  
Source: `S-198`. Related person: `P-098`; business: `BUS-024`.

The visually verified **31 December 1909** *Oregon City Courier* notice names **Ralph O. Smith** applying at **the Palace Saloon, corner Main and Fifth Sts.**, for a **six-month** liquor license.

This extends direct Smith/Palace evidence beyond the 17 September 1909 three-month application. It does not print `501`, prove the Council granted either application, establish land/building ownership, or prove uninterrupted operation between the notices.
""")
write("evidence/E-178-1910-06-17-er-case-palace-saloon-510-main.md", """# E-178 — E. R. Case applies at Palace Saloon, printed 510 Main, 17 June 1910

Type: Primary newspaper liquor-license application with independent municipal cross-reference.  
Source: `S-199`; related municipal evidence: `E-080` / `S-093`; person: `P-105`; business: `BUS-024`.

The visually verified **17 June 1910** *Oregon City Courier* notice directly states that **E. R. Case** would apply for a three-month liquor license at his place of business, **the Palace Saloon, 510 Main street**.

A separate **1 June 1910** City Council record directly places **E. R. Case's saloon at Fifth and Main Streets** and describes an adjoining restaurant. This independently corroborates Case's saloon/intersection context, while the newspaper adds the Palace trade name and printed number.

## Address conflict / limits

Preserve **510 Main** exactly as printed. Do not silently convert it to `501`.

- March 1912 evidence directly places Joe Wilson's Palace Saloon at **501 Main**.
- Repeated Pacific Telephone & Telegraph advertisements place that business at **510 Main** beginning in August 1910.
- The present evidence does not establish whether Palace moved, `510` was a newspaper error, address usage changed, or another explanation applies.
- The application is not a license grant, deed, tenancy instrument, or proof of business/property ownership.

The appropriate state is **UNRESOLVED CONFLICT / OPEN TRANSITION QUESTION** for the number and June-to-August 1910 510 occupancy sequence.
""")

append_yaml_once(
    "database/sources.yml",
    "S-198",
    f"""  - id: S-198
    name: Oregon City Courier, 31 December 1909, Ralph O. Smith Palace Saloon license application
    url: {by['pal1909']['url']}
    repository_file: {by['pal1909']['actual_path']}
    notes: >-
      Visually verified Ralph O. Smith six-month liquor-license application at the Palace Saloon, corner Main/Fifth. No 501 number, grant, title or uninterrupted continuity proved. Original upload {by['pal1909']['upload_name']}; SHA-256 {by['pal1909']['sha256']} ({by['pal1909']['size']} bytes). Related E-177/P-098/BUS-024."""
)
append_yaml_once(
    "database/sources.yml",
    "S-199",
    f"""  - id: S-199
    name: Oregon City Courier, 17 June 1910, E. R. Case Palace Saloon at printed 510 Main
    url: {by['pal1910']['url']}
    repository_file: {by['pal1910']['actual_path']}
    notes: >-
      Visually verified E. R. Case three-month liquor-license application at the Palace Saloon, printed 510 Main street. Preserve 510 exactly; relationship to later 501 Palace and later 510 Pacific Telephone occupancy remains unresolved. Original upload {by['pal1910']['upload_name']}; SHA-256 {by['pal1910']['sha256']} ({by['pal1910']['size']} bytes). Related E-178/P-105/BUS-024 and cross-reference E-080."""
)
append_yaml_once(
    "database/evidence.yml",
    "E-177",
    """  - id: E-177
    name: Ralph O. Smith at Palace Saloon, Main/Fifth, 31 December 1909
    type: Primary newspaper liquor-license application; visually verified
    claims:
      - Ralph O. Smith applies for a six-month liquor license at the Palace Saloon, corner Main and Fifth Sts.
      - The notice does not print 501, prove a license grant, property ownership, or uninterrupted operation from the September 1909 notice.
    confidence: Very High for applicant, trade name, intersection, date and requested term; exact number, grant, title and continuity unresolved.
    related_sources: [S-198]
    related_people: [P-098]
    related_businesses: [BUS-024]
    repository_file: evidence/E-177-1909-12-31-ralph-o-smith-palace-saloon.md"""
)
append_yaml_once(
    "database/evidence.yml",
    "E-178",
    """  - id: E-178
    name: E. R. Case applies at Palace Saloon, printed 510 Main, 17 June 1910
    type: Primary newspaper liquor-license application plus municipal cross-reference; visually verified
    claims:
      - The 17 June 1910 Courier directly names E. R. Case applying for a three-month liquor license at the Palace Saloon, 510 Main street.
      - The 1 June 1910 Council record independently places E. R. Case's saloon at Fifth/Main with an adjoining restaurant.
      - Preserve 510 exactly as printed; its relationship to later 501 Palace evidence and Pacific Telephone at 510 beginning August 1910 remains unresolved.
    confidence: Very High for printed Case/Palace/510 and separate municipal Case/Fifth-Main wording; Unresolved conflict for address/transition explanation.
    related_sources: [S-199, S-093]
    related_people: [P-105]
    related_businesses: [BUS-024]
    repository_file: evidence/E-178-1910-06-17-er-case-palace-saloon-510-main.md"""
)

# Formalize E. R. Case as a person now that two independent primary sources identify him.
append_once(
    "people/people-index.md",
    "| P-105 | [E. R. Case](profiles/e-r-case.md) | Palace Saloon / saloon operator-license applicant |",
    """## 2 September 2026 — E. R. Case formalized

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-105 | [E. R. Case](profiles/e-r-case.md) | Saloon operator / liquor-license applicant | 1 Jun. 1910 Council record places Case's saloon at Fifth/Main with adjoining restaurant; 17 Jun. Courier directly calls his place the **Palace Saloon, 510 Main street**. Printed 510 is retained as an unresolved address conflict/transition question. `E-080`, `E-178`; `S-093`, `S-199`. |"""
)
write("people/profiles/e-r-case.md", """# E. R. Case

Person ID: `P-105`.

Two independent primary sources identify E. R. Case in the Fifth/Main saloon context in June 1910.

- **1 June 1910:** Oregon City Council considered a complaint involving a restaurant adjoining **E. R. Case's saloon at Fifth and Main Streets** (`E-080` / `S-093`).
- **17 June 1910:** a visually verified *Oregon City Courier* liquor-license notice identifies Case's place of business as **the Palace Saloon, 510 Main street** and says he would apply for a three-month license (`E-178` / `S-199`).

The second source establishes the Palace trade-name relationship and printed number. It does not prove license grant, land/building ownership, or an uninterrupted transfer from Ralph O. Smith or to Joe/Joseph Wilson.

The archive preserves **510 Main** exactly as printed and does not normalize it to the later **501 Main** Palace address. The 510/501 relationship and the later August 1910 Pacific Telephone use of 510 remain unresolved.
""")
append_yaml_once(
    "database/people.yml",
    "P-105",
    """  - id: P-105
    name: E. R. Case
    role: Saloon operator / liquor-license applicant
    notes: 1 Jun 1910 Council record places Case's saloon at Fifth/Main with adjoining restaurant; 17 Jun 1910 Courier directly identifies his place as Palace Saloon, printed 510 Main. Preserve 510 as printed; license grant, property ownership and later 501 relationship unresolved.
    repository_file: people/profiles/e-r-case.md
    related_businesses: [BUS-024]
    related_evidence: [E-080, E-178]
    related_sources: [S-093, S-199]"""
)

def p098_mut(block: str) -> str:
    needle = "A 17 September 1909 notice again places Smith at Palace Saloon, corner Main/Fifth."
    replacement = "A 17 September 1909 notice again places Smith at Palace Saloon, corner Main/Fifth; a visually verified 31 December 1909 notice repeats the same trade name/intersection and requests a six-month license."
    if needle not in block:
        raise SystemExit("Unexpected P-098 notes")
    block = block.replace(needle, replacement, 1)
    if "E-177" not in block and "related_evidence:" in block:
        block = re.sub(r"(related_evidence:\s*\[)([^\]]*)(\])", lambda m: m.group(1) + m.group(2).rstrip() + ", E-177" + m.group(3), block, count=1)
    return block
mutate_yaml_record("database/people.yml", "P-098", p098_mut)

# Add P-105 to E-080's machine-readable relationship without changing the dated claim.
def e080_mut(block: str) -> str:
    if "P-105" in block:
        return block + "\n# P-105 already linked"
    if "    repository_file:" in block:
        return block.replace("    repository_file:", "    related_people: [P-105]\n    repository_file:", 1)
    return block.rstrip() + "\n    related_people: [P-105]\n"
mutate_yaml_record("database/evidence.yml", "E-080", e080_mut)

# Business mirrors: extend existing chronology, keep roles/addresses distinct.
def bus011_mut(block: str) -> str:
    old = "    notes: April 1911 and January 1913 newspaper ads for new/second-hand clothing, cleaning and repairing."
    new = "    notes: Visually verified 31 March, 7 April, 14 April and 28 April 1911 newspaper ads place the Chicago Store at 505 Main with new/second-hand clothing and cleaning/repairing; January 1913 again prints 505. Proprietor and surviving-building continuity remain unresolved."
    if old not in block:
        raise SystemExit("Unexpected BUS-011 notes")
    return block.replace(old, new, 1)
mutate_yaml_record("database/businesses.yml", "BUS-011", bus011_mut)

def bus021_mut(block: str) -> str:
    needle = "505½ Main on Apr 8 and May 20; 505 Main, Opposite Postoffice, on Oct 28;"
    replacement = "505½ Main on Apr 8; 505 Main on May 13; 505½ Main again on May 20; 505 Main, Opposite Postoffice, on Oct 28;"
    if needle not in block:
        raise SystemExit("Unexpected BUS-021 notes")
    return block.replace(needle, replacement, 1)
mutate_yaml_record("database/businesses.yml", "BUS-021", bus021_mut)

def bus024_mut(block: str) -> str:
    old_addr = "    address: 501 Main exact in March 1912; Fifth/Main intersection in June 1909, September 1909, June 1911 and June 1912"
    new_addr = "    address: 501 Main exact in March 1912; Fifth/Main in 1909-1912 notices; one 17 Jun 1910 Palace notice prints conflicting 510 Main"
    if old_addr not in block:
        raise SystemExit("Unexpected BUS-024 address")
    block = block.replace(old_addr, new_addr, 1)
    needle = "Smith applies again there in September 1909."
    replacement = "Smith applies again there in September 1909 and on 31 December 1909 requests a six-month license. On 17 June 1910 E. R. Case directly applies at the Palace Saloon with the printed address 510 Main; this is preserved as an unresolved conflict/transition question, not normalized to 501."
    if needle not in block:
        raise SystemExit("Unexpected BUS-024 notes")
    block = block.replace(needle, replacement, 1)
    if "      - P-105\n" not in block:
        block = block.replace("      - P-100\n", "      - P-100\n      - P-105\n", 1)
    if "      - E-177\n" not in block:
        block = block.replace("      - E-169\n", "      - E-169\n      - E-177\n      - E-178\n", 1)
    if "      - S-198\n" not in block:
        m = re.search(r"(?m)(    related_sources:\n(?:      - [^\n]+\n)+)", block)
        if not m:
            raise SystemExit("BUS-024 related_sources list not found")
        repl = m.group(1).rstrip() + "\n      - S-198\n      - S-199\n"
        block = block[:m.start()] + repl + block[m.end():]
    return block
mutate_yaml_record("database/businesses.yml", "BUS-024", bus024_mut)

append_once(
    "businesses/business-index.md",
    "## 2 September 2026 — Palace / Chicago / Freeze steward-page supplement",
    """## 2 September 2026 — Palace / Chicago / Freeze steward-page supplement
- `BUS-024` Palace Saloon: `S-198` / `E-177` extends Ralph O. Smith at Main/Fifth through 31 Dec. 1909; `S-199` / `E-178` directly prints **E. R. Case / Palace Saloon / 510 Main** on 17 Jun. 1910. The printed 510 is an unresolved conflict/transition question and is not silently changed to 501.
- `BUS-011` Chicago Store: exact 14 Apr. 1911 page now preserved and visually verified at **505 Main** under existing `S-032` / `E-026`.
- `BUS-021` Dr. Freeze: exact 13 May 1921 page prints **505 Main**, while 20 May prints **505½ Main**; this reinforces address-form uncertainty rather than a physical-layout conclusion."""
)

# Business/person narrative pages.
append_once(
    "businesses/palace-saloon.md",
    "## 31 December 1909 and 17 June 1910 steward-page update",
    """## 31 December 1909 and 17 June 1910 steward-page update

Two newly supplied, visually verified *Courier* pages materially tighten the Smith→Case interval without proving a transfer.

- **31 Dec. 1909 — `S-198` / `E-177`:** Ralph O. Smith applies for a **six-month** license at **the Palace Saloon, corner Main and Fifth Sts.** No number or grant is printed.
- **17 Jun. 1910 — `S-199` / `E-178`:** E. R. Case applies for a **three-month** license at **the Palace Saloon, 510 Main street**. A separate 1 Jun. municipal record already places Case's saloon at Fifth/Main (`E-080`).

The 17 June page is direct Palace trade-name evidence for Case, but **510 Main must remain exactly as printed**. It conflicts with/complicates the later exact **501 Main** Palace anchor under Joe Wilson and precedes repeated Pacific Telephone advertising at **510 Main** beginning in August 1910. Current evidence does not distinguish among a business move, numbering issue, newspaper error, or another explanation. No Smith→Case transfer instrument or license grant is proved."""
)
append_once(
    "businesses/chicago-store.md",
    "## 14 April 1911 exact-page preservation",
    f"""## 14 April 1911 exact-page preservation
The visually verified 14 April 1911 *Courier* page is now physically preserved at `{by['chi1911']['actual_path']}` under existing `S-032` / `E-026`. The ad directly prints **The Chicago Store, 505 Main St.** and repeats new/second-hand clothing plus cleaning/repairing. It does not name Wolf & Nat or prove real-estate ownership or surviving-building continuity."""
)
append_once(
    "businesses/dr-freeze.md",
    "## 13–20 May 1921 address-form alternation",
    """## 13–20 May 1921 address-form alternation
A newly supplied visually verified **13 May 1921** *Enterprise* ad prints **505 Main St.** without a half-number (`S-035` / `E-028`). The already preserved **20 May** ad prints **505½ Main St.** This one-week alternation reinforces that the newspaper's `505` / `505½` forms cannot by themselves establish the physical layout or a move between floors, side-by-side spaces, front/rear sections, or other subdivisions."""
)
append_once(
    "people/profiles/ralph-o-smith.md",
    "## 31 December 1909 six-month Palace application",
    """## 31 December 1909 six-month Palace application
`S-198` / `E-177` visually verifies another Ralph O. Smith notice at **the Palace Saloon, corner Main and Fifth Sts.**, this time requesting a **six-month** license. It extends Smith's direct Palace association beyond the 17 September notice but does not print 501, prove grant, title, or uninterrupted operation."""
)
append_once(
    "people/profiles/dr-freeze.md",
    "## 13 May 1921 printed 505 / 20 May printed 505½",
    """## 13 May 1921 printed 505 / 20 May printed 505½
A visually verified 13 May 1921 advertisement prints **505 Main St.**; seven days later the 20 May advertisement prints **505½ Main St.** (`S-035` / `E-028`). The alternating forms are preserved literally and do not establish where the separately numbered space sat within the building."""
)
append_once(
    "evidence/E-080-1910-er-case-saloon-fifth-main.md",
    "## 17 June 1910 newspaper corroboration",
    """## 17 June 1910 newspaper corroboration
A separately supplied and visually verified *Oregon City Courier* notice (`S-199` / `E-178`) directly identifies **E. R. Case's place of business as the Palace Saloon, 510 Main street**. This independently supports the 1 June Council record's Case/Fifth-Main saloon context and adds a trade name and printed number.

The archive does not silently turn `510` into `501`. The exact relationship among the Council's intersection wording, the newspaper's `510`, later Palace `501`, and Pacific Telephone's later 1910 `510` advertisements remains unresolved."""
)

# Relevant checkpoints / leads: resolve OCR-only status where applicable without changing annual closeout.
append_once(
    "evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md",
    "## 2 September 2026 addendum — 31 Dec. 1909 and 17 Jun. 1910",
    """## 2 September 2026 addendum — 31 Dec. 1909 and 17 Jun. 1910
Two further steward pages are now visually verified and preserved. `S-198` / `E-177` repeats Ralph O. Smith at Palace Saloon, Main/Fifth on 31 Dec. 1909 with a six-month application. `S-199` / `E-178` directly identifies E. R. Case at **Palace Saloon, 510 Main** on 17 Jun. 1910. The latter is retained as a printed address conflict/transition question rather than normalized to the later exact-501 Palace evidence."""
)
append_once(
    "evidence/source-captures/1910-main-street-research.md",
    "## 2 September 2026 steward-page supplement — E. R. Case Palace at printed 510 Main",
    """## 2 September 2026 steward-page supplement — E. R. Case Palace at printed 510 Main
A newly supplied and visually verified **17 June 1910 Courier p. 7** (`S-199` / `E-178`) directly identifies **E. R. Case** applying at **the Palace Saloon, 510 Main street**. This corroborates the existing 1 June Council record placing Case's saloon at Fifth/Main (`E-080`) and adds the trade name/exact printed number.

The printed `510` is not normalized to later Palace `501`. It also creates a high-value transition question because Pacific Telephone & Telegraph is independently advertised at `510 Main` beginning in August 1910 (`E-082` / `S-095`). Determine whether this reflects a move, numbering/error issue, short occupancy, or another explanation.

**Year status remains IN PROGRESS.** This targeted page addition does not certify a full 1910 visual pass."""
)
append_once(
    "evidence/source-captures/1911-chicago-store-wolf-nat-405-to-505.md",
    "## 14 April 1911 — exact page now visually preserved",
    f"""## 14 April 1911 — exact page now visually preserved
A project-steward page upload has now been visually inspected and preserved at `{by['chi1911']['actual_path']}`. It directly repeats **The Chicago Store, 505 Main St.**, with new/second-hand clothing and cleaning/repairing (`S-032` / `E-026`). This confirms the previously noted 14 April continuation with exact page-level provenance; it still does not identify post-move proprietors or prove physical-building continuity."""
)
append_once(
    "evidence/source-captures/1920-1922-505-poolhall-strong-candidates.md",
    "## 2 September 2026 resolution — 13 May 1921 Dr. Freeze candidate",
    """## 2 September 2026 resolution — 13 May 1921 Dr. Freeze candidate
The previously OCR-discovered **13 May 1921 page 8** candidate has now been supplied as a full page scan, visually inspected, and preserved under `S-035` / `E-028`. The advertisement visibly prints **505 Main St.**, with no half-number. This candidate is no longer OCR-only. The adjacent 8 April / 20 May `505½` evidence means the number-form variation must not be converted into a physical-layout claim."""
)
append_once(
    "evidence/source-captures/1918-1922-freeze-514-main-steward-upload-supplement-2026-09-02.md",
    "## Addendum — 13 May 1921 exact 505 Main",
    """## Addendum — 13 May 1921 exact 505 Main
A later steward upload of the 13 May 1921 *Enterprise* p. 8 was visually inspected and preserved under `S-035` / `E-028`. Despite its uploaded filename saying `505 & half`, the printed advertisement itself reads **505 Main St.** The directly verified sequence now alternates 505½ (8 Apr.), 505 (13 May), 505½ (20 May), 505 (28 Oct.), and 505½ (30 Jun. 1922). This strengthens the no-layout-inference rule."""
)

# Address/building timelines and narrative context.
append_once(
    "timelines/501-main.md",
    "## 1909–1910 Palace address update — printed 510 conflict retained",
    """## 1909–1910 Palace address update — printed 510 conflict retained
- **31 Dec. 1909:** Ralph O. Smith applies at **Palace Saloon, corner Main/Fifth** for six months (`S-198` / `E-177`); no 501 printed.
- **17 Jun. 1910:** E. R. Case applies at **Palace Saloon, 510 Main street** (`S-199` / `E-178`). This is **context/conflict evidence only for the 501 history** and is not assigned to B-005.
- **19 Mar. 1912:** Joe Wilson's Palace Saloon is directly printed at **501 Main** (`S-118` / `E-104`).

The archive does not assume the 1910 `510` is a typo or a move; the number relationship remains unresolved."""
)
append_once(
    "timelines/505-main.md",
    "## 14 April 1911 / 13 May 1921 steward-page update",
    """## 14 April 1911 / 13 May 1921 steward-page update
- **14 Apr. 1911:** exact visually preserved Chicago Store ad prints **505 Main** (`S-032` / `E-026`), extending the exact preserved March/April scan set.
- **13 May 1921:** Dr. Freeze ad prints **505 Main**; **20 May** prints **505½ Main** (`S-035` / `E-028`). The week-to-week variation is not evidence of a physical floor or room move."""
)
append_once(
    "buildings/505-main.md",
    "## 2 September 2026 exact-page additions",
    """## 2 September 2026 exact-page additions
The exact 14 April 1911 Chicago Store page is now visually preserved under `S-032` / `E-026` and directly prints **505 Main**. The exact 13 May 1921 Dr. Freeze page is now visually preserved under `S-035` / `E-028` and prints **505 Main**, followed one week later by the already preserved **505½ Main** form. These are occupancy/address anchors only and do not establish surviving-building continuity or physical subdivision layout."""
)
append_once(
    "buildings/501-main.md",
    "## 17 June 1910 Palace Saloon printed-510 conflict",
    """## 17 June 1910 Palace Saloon printed-510 conflict
A visually verified *Courier* notice (`S-199` / `E-178`) identifies **E. R. Case / Palace Saloon / 510 Main street**. Because the Palace is later directly printed at **501 Main** under Joe Wilson, this source is retained as an unresolved address/transition conflict and is **not assigned as B-005 occupancy** without a bridge."""
)

# Master/business timelines.
append_once(
    "timeline.md",
    "## 31 December 1909 — Ralph O. Smith remains at Palace Saloon, Main/Fifth",
    """## 31 December 1909 — Ralph O. Smith remains at Palace Saloon, Main/Fifth
A visually verified *Courier* notice has **Ralph O. Smith** applying for a **six-month** liquor license at **the Palace Saloon, corner Main and Fifth Sts.** (`S-198` / `E-177`, `T-069`). It does not print 501 or prove grant/title/continuous operation."""
)
append_once(
    "timeline.md",
    "## 17 June 1910 — E. R. Case / Palace Saloon / printed 510 Main",
    """## 17 June 1910 — E. R. Case / Palace Saloon / printed 510 Main
A visually verified *Courier* notice directly prints **E. R. Case** applying at **the Palace Saloon, 510 Main street** (`S-199` / `E-178`, `P-105`, `T-070`). The separate 1 June Council record places Case's saloon at Fifth/Main. Preserve 510 literally: its relationship to later Palace 501 and Pacific Telephone at 510 later in 1910 is unresolved."""
)
append_once(
    "timeline.md",
    "## 13 May 1921 — Dr. Freeze advertisement prints 505 Main",
    """## 13 May 1921 — Dr. Freeze advertisement prints 505 Main
A visually verified *Enterprise* advertisement prints **Dr. Freeze, Eye Specialist, 505 Main St.** (`S-035` / `E-028`, `T-071`). The 20 May ad returns to **505½ Main**. This alternation strengthens the source-level address-variation interpretation and does not prove a physical move or floor arrangement."""
)
append_once(
    "registers/business-timeline.md",
    "## 31 December 1909 — Ralph O. Smith Palace Saloon application",
    """## 31 December 1909 — Ralph O. Smith Palace Saloon application
`S-198` / `E-177` directly places Ralph O. Smith at **Palace Saloon, Main/Fifth**, applying for six months. No exact number or grant is proved."""
)
append_once(
    "registers/business-timeline.md",
    "## 17 June 1910 — E. R. Case Palace Saloon at printed 510 Main",
    """## 17 June 1910 — E. R. Case Palace Saloon at printed 510 Main
`S-199` / `E-178` directly prints **E. R. Case / Palace Saloon / 510 Main**. A 1 June municipal record independently places Case's saloon at Fifth/Main. The printed 510 is retained as an unresolved address/transition conflict rather than normalized to later Palace 501."""
)
append_once(
    "registers/business-timeline.md",
    "## 13 May 1921 — Dr. Freeze printed 505 Main",
    """## 13 May 1921 — Dr. Freeze printed 505 Main
`S-035` / `E-028` adds an exact visually verified **505 Main** advertisement between 8 April **505½** and 20 May **505½**. No physical-layout change is inferred."""
)

append_yaml_once(
    "database/timeline.yml",
    "T-069",
    """  - id: T-069
    date: 31 December 1909
    summary: Ralph O. Smith applies for a six-month liquor license at the Palace Saloon, corner Main and Fifth Sts.
    confidence: Very High for visually verified applicant/trade-name/intersection/term; exact number, grant, title and uninterrupted continuity unresolved.
    related_evidence: [E-177]
    related_sources: [S-198]
    related_people: [P-098]
    related_businesses: [BUS-024]"""
)
append_yaml_once(
    "database/timeline.yml",
    "T-070",
    """  - id: T-070
    date: 17 June 1910
    summary: E. R. Case applies for a three-month liquor license at the Palace Saloon, printed 510 Main street; separate 1 June Council evidence places Case's saloon at Fifth/Main.
    confidence: Very High for direct printed wording; 510 relationship to later Palace 501 and later 1910 Pacific Telephone 510 remains unresolved.
    related_evidence: [E-178, E-080]
    related_sources: [S-199, S-093]
    related_people: [P-105]
    related_businesses: [BUS-024]"""
)
append_yaml_once(
    "database/timeline.yml",
    "T-071",
    """  - id: T-071
    date: 13 May 1921
    summary: Dr. Freeze advertisement prints 505 Main St.; the 20 May advertisement returns to 505 1/2 Main.
    confidence: Very High for visually verified printed address; physical room/floor/layout implication unresolved and not inferred.
    related_evidence: [E-028]
    related_sources: [S-035]
    related_people: [P-027]
    related_businesses: [BUS-021]
    related_buildings: [B-002]"""
)

# Open questions, leads, crosswalk, archive index, research log.
append_once(
    "evidence/open-questions.md",
    "### OQ-032 update — 31 Dec. 1909 Smith and 17 Jun. 1910 Case/510 evidence",
    """### OQ-032 update — 31 Dec. 1909 Smith and 17 Jun. 1910 Case/510 evidence
`E-177` extends Ralph O. Smith at Palace Saloon, Main/Fifth through 31 Dec. 1909. `E-178` then directly identifies **E. R. Case at Palace Saloon, 510 Main** on 17 Jun. 1910, independently consistent with the 1 Jun. Case/Fifth-Main municipal record. The open question is now sharper: recover actual license grants/transfer records and determine why Case's Palace notice prints 510 when later Palace evidence prints 501 and Pacific Telephone occupies printed 510 by Aug. 1910. Do not choose typo, move, renumbering, or same-premises continuity without evidence."""
)
append_once(
    "evidence/research-leads.md",
    "### RL-045 supplement — test the 1909–1910 Palace Smith→Case and 510 transition",
    """### RL-045 supplement — test the 1909–1910 Palace Smith→Case and 510 transition
Use `S-198` / `E-177` and `S-199` / `E-178` to search City Council license grants, transfer/sale notices, directories, and exact-address advertising from **31 Dec. 1909 through Aug. 1910**. Determine:
1. whether Smith's six-month Palace application was granted and when Smith exited;
2. whether Case acquired/leased/operated the same Palace business or merely used the trade name;
3. whether the printed **510 Main** can be independently corroborated;
4. how Palace/Case at printed 510 relates chronologically and spatially to Pacific Telephone's repeated 510 Main advertisements beginning Aug. 1910.
Preserve 510/501 as an unresolved conflict until direct evidence resolves it."""
)
append_once(
    "indexes/id-crosswalk.md",
    "| `S-198` / `E-177` | `P-098`; `BUS-024`; `T-069` |",
    """| `S-198` / `E-177` | `P-098`; `BUS-024`; `T-069` | 31 Dec. 1909 Ralph O. Smith six-month Palace Saloon application at Main/Fifth; no exact number or grant. |
| `S-199` / `E-178` / `P-105` | `BUS-024`; `E-080`; `T-070` | 17 Jun. 1910 E. R. Case Palace Saloon application prints **510 Main**; preserve address conflict/transition question. |
| `S-032` / `E-026` 14 Apr. 1911 supplement | `BUS-011`; `B-002` | Exact steward page now preserved; Chicago Store directly at 505 Main. |
| `S-035` / `E-028` 13 May 1921 supplement | `P-027`; `BUS-021`; `B-002`; `T-071` | Exact steward page prints 505 Main; 20 May returns to 505½; no physical-layout inference. |"""
)
append_once(
    "ARCHIVE_INDEX.md",
    "## 2 September 2026 — Palace / Chicago / Freeze four-page steward supplement",
    """## 2 September 2026 — Palace / Chicago / Freeze four-page steward supplement
[Reconciliation audit](evidence/source-captures/1909-1921-palace-chicago-freeze-steward-upload-reconciliation-2026-09-02.md) accounts for four supplied newspaper PDFs by exact SHA-256. New Palace source/evidence pairs are `S-198` / `E-177` (Ralph O. Smith, 31 Dec. 1909) and `S-199` / `E-178` (E. R. Case, Palace Saloon, printed **510 Main**, 17 Jun. 1910; `P-105`). Existing grouped records `S-032` / `E-026` now preserve the exact 14 Apr. 1911 Chicago Store **505 Main** page, and `S-035` / `E-028` now preserve the exact 13 May 1921 Dr. Freeze **505 Main** page between nearby `505½` advertisements. Printed address conflicts/variation are retained; annual status is unchanged."""
)
append_once(
    "registers/research-log.md",
    "### 2026-09-02 — Palace / Chicago / Freeze four-page steward integration",
    """### 2026-09-02 — Palace / Chicago / Freeze four-page steward integration
- Followed startup protocol: synced current `main`, reread `AGENTS.md` and `RESEARCH-STANDARD.md`, reviewed relevant Palace/Chicago/Freeze checkpoints, and required archive validation before/after.
- Reconciled four supplied newspaper PDFs by exact SHA-256 and preserved missing exact pages under canonical `newspapers/` paths.
- Added `S-198` / `E-177` for Ralph O. Smith at Palace Saloon, Main/Fifth on 31 Dec. 1909.
- Added `S-199` / `E-178` and `P-105` for E. R. Case at Palace Saloon, **printed 510 Main**, 17 Jun. 1910; retained the 510-vs-later-501 and later-510-telephone question as unresolved.
- Extended existing `S-032` / `E-026` with the exact 14 Apr. 1911 Chicago Store 505 Main page.
- Extended existing `S-035` / `E-028` with the exact 13 May 1921 Dr. Freeze 505 Main page; 20 May returns to 505½, reinforcing address-form uncertainty and the no-physical-layout-inference rule.
- No annual completion status changed. Permanent audit: `evidence/source-captures/1909-1921-palace-chicago-freeze-steward-upload-reconciliation-2026-09-02.md`."""
)

print("Integration records prepared.")
for item in PAGES:
    print(f"{item['key']}: {item['handling']} -> {item['actual_path']}")
