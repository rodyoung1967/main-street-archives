#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import urllib.request
import yaml

ROOT = Path(".")

PAGES = [
    {
        "key": "smith_1909_07_02",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-07-02/ed-1/seq-7.pdf",
        "sha256": "94e004ddf110f08ace6ccd9609d1be2243130d5f3248f37c6a5806ecf27fa704",
        "size": 691304,
        "repo_path": "newspapers/oregon-city-courier/1909-07-02-page-7-palace-saloon-ralph-o-smith-license.pdf",
        "upload_name": "Palace Saloon (Liquor License) Oregon City courier., July 02, 1909, Page 7, Image 7.pdf",
        "existing_id": "S-178 / E-158",
    },
    {
        "key": "case_1910_06_24",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1910-06-24/ed-1/seq-7.pdf",
        "sha256": "39292ce2a44c7cb0b29b53c08cc1ec4eb7968ff7a3d19cde3911712db26974c0",
        "size": 700071,
        "repo_path": "newspapers/oregon-city-courier/1910-06-24-page-7-palace-saloon-er-case-510-main.pdf",
        "upload_name": "Palace Saloon (Liquor License) Oregon City courier., June 24, 1910, Page 7, Image 7.pdf",
        "existing_id": "S-199 / E-178",
    },
    {
        "key": "smith_1909_09_17",
        "sha256": "4682715f6ac882a21893a9d3e0729f0f2eef5544bde41517977ee5e7cb0c077a",
        "size": 677536,
        "repo_path": "newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf",
        "upload_name": "Palace Saloon (Liquor License) Oregon City courier., September 17, 1909, Page 5, Image 5(1).pdf",
        "existing_id": "S-172 / E-152",
        "duplicate": True,
    },
    {
        "key": "leland_1920_06_04",
        "sha256": "3b419bb26e96d77aaf5be8dcb7f0954c7755ab9be890788fad119ca79702c245",
        "size": 632535,
        "repo_path": "newspapers/oregon-city-enterprise/1920-06-04-page-3.pdf",
        "upload_name": "A. Leland to operate pool hall at 505 and a half jun 1920(1).pdf",
        "existing_id": "S-150 / E-135",
        "duplicate": True,
    },
    {
        "key": "dollar_1920_02_13",
        "sha256": "dfd5be8e1fad8ad1c7dca8516590bb67d1a3d7c3f41cc5e4c1a1cb69a04eb004",
        "size": 718961,
        "repo_path": "newspapers/oregon-city-enterprise/1920-02-13-page-5.pdf",
        "upload_name": "Clem Dollar proprietor of pool hall between 5th & 6th on main st feb 1920(1).pdf",
        "existing_id": "S-150 / E-135",
        "duplicate": True,
    },
]

def read(path):
    return Path(path).read_text(encoding="utf-8")

def write(path, text):
    Path(path).write_text(text, encoding="utf-8")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def all_file_hashes():
    out = {}
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        try:
            digest = sha256(p)
        except OSError:
            continue
        out.setdefault(digest, []).append(p.as_posix())
    return out

def replace_md_id_section(path, ident, new_section):
    text = read(path)
    pat = re.compile(rf"(?ms)^## {re.escape(ident)} —.*?(?=^## |\Z)")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Could not find Markdown section {ident} in {path}")
    new_section = new_section.rstrip() + "\n\n"
    write(path, text[:m.start()] + new_section + text[m.end():])

def append_once(path, marker, content):
    text = read(path)
    if marker in text:
        return
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    write(path, text + sep + content.rstrip() + "\n")

def get_yaml_record(path, ident):
    text = read(path)
    pat = re.compile(rf"(?ms)^  - id: {re.escape(ident)}\n.*?(?=^  - id: |\Z)")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Could not find YAML record {ident} in {path}")
    block = m.group(0)
    parsed = yaml.safe_load(block[2:])
    if not isinstance(parsed, list) or len(parsed) != 1:
        raise SystemExit(f"Unexpected YAML record shape for {ident} in {path}")
    return text, m, parsed[0]

def replace_yaml_record(path, ident, mutate):
    text, m, rec = get_yaml_record(path, ident)
    mutate(rec)
    dumped = yaml.safe_dump([rec], sort_keys=False, allow_unicode=True, width=1000).rstrip()
    dumped = "\n".join("  " + line for line in dumped.splitlines()) + "\n\n"
    write(path, text[:m.start()] + dumped + text[m.end():])

def add_sentence(value, sentence):
    value = value or ""
    if sentence in value:
        return value
    value = value.rstrip()
    return (value + (" " if value else "") + sentence).strip()

required = [
    ("evidence/source-register.md", r"(?m)^## S-172 —"),
    ("evidence/source-register.md", r"(?m)^## S-178 —"),
    ("evidence/source-register.md", r"(?m)^## S-199 —"),
    ("evidence/source-register.md", r"(?m)^## S-150 —"),
    ("evidence/evidence-register.md", r"(?m)^## E-152 —"),
    ("evidence/evidence-register.md", r"(?m)^## E-158 —"),
    ("evidence/evidence-register.md", r"(?m)^## E-178 —"),
    ("evidence/evidence-register.md", r"(?m)^## E-135 —"),
]
for path, pat in required:
    if not re.search(pat, read(path)):
        raise SystemExit(f"Required stable ID missing: {pat} in {path}")

hashes = all_file_hashes()
for item in PAGES:
    expected = item["repo_path"]
    existing = hashes.get(item["sha256"], [])
    if item.get("duplicate"):
        if expected not in existing:
            raise SystemExit(f"Expected duplicate {item['key']} not found at {expected}; hash occurs at {existing}")
        if Path(expected).stat().st_size != item["size"]:
            raise SystemExit(f"Size mismatch for existing {expected}")
        item["actual_path"] = expected
        item["handling"] = "already preserved; exact duplicate upload alias recorded"
        print(f"{item['key']}: exact duplicate already preserved -> {expected}")
        continue
    if existing:
        item["actual_path"] = existing[0]
        item["handling"] = "already preserved elsewhere by exact hash; no duplicate created"
        print(f"{item['key']}: exact hash already in repo -> {existing[0]}")
        continue
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    got = hashlib.sha256(data).hexdigest()
    if got != item["sha256"] or len(data) != item["size"]:
        raise SystemExit(f"Canonical page mismatch for {item['key']}: sha={got}, bytes={len(data)}; expected sha={item['sha256']}, bytes={item['size']}")
    target = Path(item["repo_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    item["actual_path"] = item["repo_path"]
    item["handling"] = "newly preserved; byte-for-byte identical to steward upload"
    hashes.setdefault(item["sha256"], []).append(item["repo_path"])
    print(f"{item['key']}: newly preserved exact upload bytes -> {item['repo_path']}")

by = {x["key"]: x for x in PAGES}

replace_md_id_section("evidence/source-register.md", "S-178", f"""## S-178 — Oregon City Courier, 25 June and 2 July 1909, Ralph O. Smith Palace Saloon license notices
Canonical PDFs:
- https://oregonnews.uoregon.edu/lccn/sn00063698/1909-06-25/ed-1/seq-7.pdf
- {by['smith_1909_07_02']['url']}
Repository PDFs:
- `newspapers/oregon-city-courier/1909-06-25-page-7-palace-saloon-ralph-o-smith-license.pdf`
- `{by['smith_1909_07_02']['actual_path']}`
Original steward filenames include:
- `Palace Saloon (Liquor License) Oregon City courier., June 25, 1909, Page 7, Image 7(1).pdf`
- `{by['smith_1909_07_02']['upload_name']}`
Type: Primary newspaper liquor-license notices; **VISUALLY VERIFIED**.
Related evidence: `E-158`; person `P-098`; business `BUS-024`.
Notes: Both pages print the same three-month liquor-license application by **Ralph O. Smith** at **Palace Saloon, Fifth and Main streets**. The 2 July publication is treated as a repeat publication of the same application, not a second application or a license grant. The notices do not print 501 or establish real-estate/building ownership. The newly supplied 2 July PDF is preserved byte-for-byte, SHA-256 `{by['smith_1909_07_02']['sha256']}` ({by['smith_1909_07_02']['size']} bytes).""")

replace_md_id_section("evidence/source-register.md", "S-199", f"""## S-199 — Oregon City Courier, 17 and 24 June 1910, E. R. Case Palace Saloon at printed 510 Main
Canonical PDFs:
- https://oregonnews.uoregon.edu/lccn/sn00063698/1910-06-17/ed-1/seq-7.pdf
- {by['case_1910_06_24']['url']}
Repository PDFs:
- `newspapers/oregon-city-courier/1910-06-17-page-7-palace-saloon-er-case-510-main.pdf`
- `{by['case_1910_06_24']['actual_path']}`
Original steward filenames include:
- `Palace Saloon (Liquor Licence) Oregon City courier., June 17, 1910, Page 7, Image 7.pdf`
- `{by['case_1910_06_24']['upload_name']}`
Type: Primary newspaper liquor-license notices; **VISUALLY VERIFIED**.
Related evidence: `E-178`, cross-reference `E-080`; person `P-105`; business `BUS-024`.
Notes: Both 17 and 24 June pages print **E. R. Case** applying for a three-month liquor license at **the Palace Saloon, 510 Main street**. The 24 June publication is treated as a repeat publication of the same application. Repetition in two consecutive issues confirms that `510` is not an OCR-only or one-scan transcription artifact, but it does not rule out repeated newspaper-copy/address error and does not prove a physical move or true legal premises number. A separate 1 June municipal record places Case's saloon at Fifth/Main; later Palace evidence prints 501 under Joe Wilson, while Pacific Telephone later prints 510. Preserve the conflict. Newly supplied 24 June PDF SHA-256 `{by['case_1910_06_24']['sha256']}` ({by['case_1910_06_24']['size']} bytes).""")

def add_alias_to_section(path, ident, sentence):
    text = read(path)
    pat = re.compile(rf"(?ms)^## {re.escape(ident)} —.*?(?=^## |\Z)")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Missing section {ident}")
    section = m.group(0).rstrip()
    if sentence not in section:
        section += "\n\n" + sentence
        write(path, text[:m.start()] + section + "\n\n" + text[m.end():])

add_alias_to_section("evidence/source-register.md", "S-172", f"Duplicate steward-upload alias reviewed 2 September 2026: `{by['smith_1909_09_17']['upload_name']}` is byte-identical to the already preserved repository PDF, SHA-256 `{by['smith_1909_09_17']['sha256']}` ({by['smith_1909_09_17']['size']} bytes); no duplicate file or ID was created.")
add_alias_to_section("evidence/source-register.md", "S-150", f"Duplicate steward-upload aliases reviewed 2 September 2026: `{by['dollar_1920_02_13']['upload_name']}` is byte-identical to `{by['dollar_1920_02_13']['repo_path']}` (SHA-256 `{by['dollar_1920_02_13']['sha256']}`), and `{by['leland_1920_06_04']['upload_name']}` is byte-identical to `{by['leland_1920_06_04']['repo_path']}` (SHA-256 `{by['leland_1920_06_04']['sha256']}`). No duplicate binaries or IDs were created.")

replace_md_id_section("evidence/evidence-register.md", "E-158", """## E-158 — Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June; repeated 2 July 1909
Type: Primary newspaper liquor-license notices; **VISUALLY VERIFIED**.
Sources: `S-178`
Related person: `P-098`; business: `BUS-024`.
Claims:
- The 25 June and 2 July 1909 *Oregon City Courier* pages both print Ralph O. Smith applying for a three-month liquor license at **Palace Saloon, Fifth and Main streets**.
- The 2 July notice is a repeat publication of the same application, not evidence of a second application or grant.
- Neither notice prints 501 Main or establishes property/building ownership.
Confidence: Very High for the repeated printed applicant, trade name, intersection and requested three-month period; license grant, exact numbered address and title remain unresolved.""")

replace_md_id_section("evidence/evidence-register.md", "E-178", """## E-178 — E. R. Case Palace Saloon application, printed 510 Main, 17 and 24 June 1910
Type: Primary newspaper liquor-license notices with independent municipal cross-reference; **VISUALLY VERIFIED**.
Sources: `S-199`; related municipal evidence: `E-080` / `S-093`.
Related person: `P-105`; business: `BUS-024`.
Claims:
- Both 17 and 24 June 1910 *Oregon City Courier* notices print **E. R. Case** applying for a three-month liquor license at **the Palace Saloon, 510 Main street**.
- The 24 June notice is a repeat publication of the same application.
- The repeated `510` establishes that the number occurs on two separate scanned issue pages, not merely in OCR or a single visual transcription.
- A separate 1 June Council record places E. R. Case's saloon at Fifth/Main and describes an adjoining restaurant.
Limits / conflict:
- Repeated publication may repeat the same underlying newspaper-copy or address error; it does not prove the physical/legal premises were truly 510.
- Later March 1912 evidence directly places Joe Wilson's Palace Saloon at **501 Main**.
- Pacific Telephone advertisements place that business at **510 Main** beginning in August 1910.
- No move, renumbering, typo correction, license grant, tenancy, business ownership, real-estate ownership, or physical-premises explanation is assumed.
Confidence: Very High for the two printed 510 notices and Case/Palace relationship; **UNRESOLVED CONFLICT** for how 510 relates to later Palace 501 and later 1910 Pacific Telephone 510.""")

write("evidence/E-158-1909-palace-saloon-smith-license.md", """# E-158 — Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June; repeated 2 July 1909

Source: `S-178`.

Two visually verified *Oregon City Courier* pages, **25 June 1909** and **2 July 1909**, print the same three-month liquor-license application by **Ralph O. Smith** at **Palace Saloon, Fifth and Main streets**.

The 2 July page is treated as a repeat publication of the same application, not as a second application or proof that the license was granted. Neither notice prints 501 or establishes real-estate/building ownership.
""")

write("evidence/E-178-1910-06-17-er-case-palace-saloon-510-main.md", """# E-178 — E. R. Case Palace Saloon application, printed 510 Main, 17 and 24 June 1910

Type: Primary newspaper liquor-license notices with independent municipal cross-reference.  
Source: `S-199`; related municipal evidence: `E-080` / `S-093`; person: `P-105`; business: `BUS-024`.

The visually verified **17 June and 24 June 1910** *Oregon City Courier* notices both state that **E. R. Case** would apply for a three-month liquor license at his place of business, **the Palace Saloon, 510 Main street**. The 24 June notice is treated as a repeat publication of the same application.

A separate **1 June 1910** City Council record directly places **E. R. Case's saloon at Fifth and Main Streets** and describes an adjoining restaurant. This independently corroborates Case's saloon/intersection context, while the newspaper supplies the Palace trade name and printed number.

## Address conflict / limits

Preserve **510 Main** exactly as printed on both weekly pages. Do not silently convert it to `501`.

- The second page proves that `510` appears on two separate issue scans and is not merely an OCR or one-scan transcription artifact.
- A repeated legal notice can repeat the same source-copy/address error, so repetition does **not** prove the physical/legal premises were truly 510.
- March 1912 evidence directly places Joe Wilson's Palace Saloon at **501 Main**.
- Repeated Pacific Telephone & Telegraph advertisements place that business at **510 Main** beginning in August 1910.
- The present evidence does not establish whether Palace moved, `510` was erroneous, address usage changed, or another explanation applies.
- The notices are applications, not license grants, deeds, tenancy instruments, or proof of business/property ownership.

The appropriate state remains **UNRESOLVED CONFLICT / OPEN TRANSITION QUESTION** for the number and June-to-August 1910 510 occupancy sequence.
""")

def mut_s178(rec):
    rec["name"] = "Oregon City Courier, 25 June and 2 July 1909, Ralph O. Smith Palace Saloon license notices"
    rec["url"] = "https://oregonnews.uoregon.edu/lccn/sn00063698/1909-06-25/ed-1/seq-7.pdf"
    rec["notes"] = f"Visually verified 25 June and 2 July 1909 pages both print Ralph O. Smith applying for a three-month liquor license at Palace Saloon, Fifth and Main streets. The 2 July page is preserved at {by['smith_1909_07_02']['actual_path']} and is treated as a repeat publication, not a second application or grant. No exact 501, title or building ownership is proved. 2 July SHA-256 {by['smith_1909_07_02']['sha256']} ({by['smith_1909_07_02']['size']} bytes). Related evidence E-158."
replace_yaml_record("database/sources.yml", "S-178", mut_s178)

def mut_s199(rec):
    rec["name"] = "Oregon City Courier, 17 and 24 June 1910, E. R. Case Palace Saloon at printed 510 Main"
    rec["url"] = "https://oregonnews.uoregon.edu/lccn/sn00063698/1910-06-17/ed-1/seq-7.pdf"
    rec["notes"] = f"Visually verified 17 and 24 June 1910 pages both print E. R. Case applying for a three-month liquor license at the Palace Saloon, 510 Main street. The 24 June page is preserved at {by['case_1910_06_24']['actual_path']}. Repetition confirms 510 occurs on two issue scans but does not rule out repeated source-copy/address error or prove a physical move/true premises number. Separate 1 June Council evidence places Case's saloon at Fifth/Main; later Palace 501 and later Pacific Telephone 510 remain unresolved. 24 June SHA-256 {by['case_1910_06_24']['sha256']} ({by['case_1910_06_24']['size']} bytes). Related evidence E-178."
replace_yaml_record("database/sources.yml", "S-199", mut_s199)

def mut_s172(rec):
    rec["notes"] = add_sentence(rec.get("notes"), f"Duplicate steward-upload alias `{by['smith_1909_09_17']['upload_name']}` reviewed 2 Sep 2026 is byte-identical to the existing repository PDF (SHA-256 {by['smith_1909_09_17']['sha256']}); no duplicate binary or ID created.")
replace_yaml_record("database/sources.yml", "S-172", mut_s172)

def mut_s150(rec):
    rec["notes"] = add_sentence(rec.get("notes"), f"Steward duplicate aliases reviewed 2 Sep 2026: `{by['dollar_1920_02_13']['upload_name']}` matches {by['dollar_1920_02_13']['repo_path']} SHA-256 {by['dollar_1920_02_13']['sha256']}; `{by['leland_1920_06_04']['upload_name']}` matches {by['leland_1920_06_04']['repo_path']} SHA-256 {by['leland_1920_06_04']['sha256']}. No duplicate binaries/IDs created.")
replace_yaml_record("database/sources.yml", "S-150", mut_s150)

def mut_e158(rec):
    rec["name"] = "Ralph O. Smith Palace Saloon license application at Fifth/Main, 25 June; repeated 2 July 1909"
    rec["claims"] = ["The 25 June and 2 July 1909 Courier pages both print Ralph O. Smith applying for a three-month liquor license at Palace Saloon, Fifth and Main streets.", "The 2 July notice is a repeat publication of the same application, not evidence of a second application or grant.", "Neither notice prints 501 Main or establishes property/building ownership."]
    rec["confidence"] = "Very High for repeated printed applicant, trade name, intersection and requested period; license grant, exact numbered address and title unresolved."
replace_yaml_record("database/evidence.yml", "E-158", mut_e158)

def mut_e178(rec):
    rec["name"] = "E. R. Case Palace Saloon application, printed 510 Main, 17 and 24 June 1910"
    rec["claims"] = ["Both 17 and 24 June 1910 Courier notices print E. R. Case applying for a three-month liquor license at the Palace Saloon, 510 Main street.", "The 24 June notice is a repeat publication of the same application.", "Repeated 510 on two separate issue scans rules out an OCR-only or single-scan transcription artifact but does not rule out repeated newspaper-copy/address error.", "Separate 1 June Council evidence places E. R. Case's saloon at Fifth/Main with an adjoining restaurant.", "Later Palace 501 and later 1910 Pacific Telephone 510 evidence remain unresolved; no move, renumbering, title, grant or physical-premises explanation is assumed."]
    rec["confidence"] = "Very High for both printed 510 notices and Case/Palace relationship; Unresolved conflict for 510 versus later Palace 501 and later 1910 Pacific Telephone 510."
replace_yaml_record("database/evidence.yml", "E-178", mut_e178)

def mut_p098(rec):
    rec["notes"] = add_sentence(rec.get("notes"), "A 2 July 1909 Courier page repeats Smith's three-month Palace Saloon, Fifth/Main application first preserved from 25 June; it is treated as repeat publication, not a second application or grant.")
    src = rec.setdefault("related_sources", [])
    if "S-178" not in src: src.append("S-178")
    ev = rec.setdefault("related_evidence", [])
    if "E-158" not in ev: ev.append("E-158")
replace_yaml_record("database/people.yml", "P-098", mut_p098)

def mut_p105(rec):
    rec["notes"] = add_sentence(rec.get("notes"), "The 24 June 1910 Courier repeats the 17 June Palace Saloon notice with the same printed 510 Main address; this proves repeated printed usage but not the true physical/legal premises number.")
    src = rec.setdefault("related_sources", [])
    if "S-199" not in src: src.append("S-199")
    ev = rec.setdefault("related_evidence", [])
    if "E-178" not in ev: ev.append("E-178")
replace_yaml_record("database/people.yml", "P-105", mut_p105)

def mut_bus024(rec):
    rec["notes"] = add_sentence(rec.get("notes"), "The Ralph O. Smith three-month Fifth/Main application appears on both 25 June and 2 July 1909. E. R. Case's Palace notice prints 510 Main in both 17 and 24 June 1910 issues; the repeat strengthens the printed-address evidence but does not resolve 510 versus later Palace 501 or later Pacific Telephone 510.")
replace_yaml_record("database/businesses.yml", "BUS-024", mut_bus024)

def mut_t053(rec):
    rec["summary"] = "Ralph O. Smith is reported purchasing former partner F. E. Hall's interest in Palace Saloon; a same-issue 25 June license notice places Smith at Palace Saloon, Fifth/Main, and the same three-month application is republished 2 July. No 501 number, license grant, transaction terms or real-estate title is proved."
replace_yaml_record("database/timeline.yml", "T-053", mut_t053)

def mut_t070(rec):
    rec["date"] = "17 and 24 June 1910"
    rec["summary"] = "E. R. Case's three-month Palace Saloon application prints 510 Main street in both the 17 and 24 June Courier; separate 1 June Council evidence places Case's saloon at Fifth/Main."
    rec["confidence"] = "Very High for repeated direct printed 510 wording on two issue scans; repetition does not rule out repeated source-copy/address error, and the relationship to later Palace 501 and later 1910 Pacific Telephone 510 remains unresolved."
replace_yaml_record("database/timeline.yml", "T-070", mut_t070)

append_once("people/profiles/ralph-o-smith.md", "## 2 July 1909 repeat-notice supplement", """## 2 July 1909 repeat-notice supplement
A newly supplied and visually verified **2 July 1909** *Courier* page repeats Smith's already documented three-month liquor-license application at **Palace Saloon, Fifth and Main streets** (`S-178` / `E-158`). It is treated as a repeat publication of the same application first preserved from 25 June, not as a second application or proof of grant. No 501 number or title is printed.""")
append_once("people/profiles/e-r-case.md", "## 24 June 1910 repeat-notice supplement", """## 24 June 1910 repeat-notice supplement
A second visually verified *Courier* page, **24 June 1910**, repeats Case's three-month Palace Saloon application and again prints **510 Main street** (`S-199` / `E-178`). This proves `510` appears on two separate weekly issue scans, not merely in OCR or a single scan transcription. Because the second item is a repeat notice, it could repeat the same source-copy/address error; the archive therefore continues to preserve 510 without treating it as proof of the physical/legal premises number.""")
append_once("businesses/palace-saloon.md", "## 2 September 2026 repeat-notice supplement", """## 2 September 2026 repeat-notice supplement
Two newly supplied pages extend already registered Palace notices without creating parallel source/evidence IDs.

- **2 July 1909:** Ralph O. Smith's three-month Palace Saloon, Fifth/Main license application is republished one week after the 25 June notice (`S-178` / `E-158`). This is repeat-publication evidence, not a second application or a grant.
- **24 June 1910:** E. R. Case's three-month Palace notice again prints **510 Main street**, one week after the 17 June notice (`S-199` / `E-178`). The repeat proves `510` is printed on two separate issue scans, but it can still represent repeated source copy. It does not resolve the conflict with Joe Wilson's later **501 Main** Palace or Pacific Telephone's later **510 Main** use.

No continuous Smith→Case transfer, license grant, deed/title, physical move or building continuity is inferred.""")
append_once("evidence/source-captures/1909-1911-palace-saloon-partnership-license-supplement-2026-09-01.md", "## 2 September 2026 repeat-page supplement", f"""## 2 September 2026 repeat-page supplement

### 2 July 1909 — repeat of S-178 / E-158
A newly supplied *Oregon City Courier* p. 7 scan again prints **Ralph O. Smith** applying for a three-month liquor license at **Palace Saloon, Fifth and Main streets**. This is a repeat publication of the 25 June notice already under `S-178` / `E-158`, so no new source/evidence ID was created.

Repository file: `{by['smith_1909_07_02']['actual_path']}`  
Original uploaded filename: `{by['smith_1909_07_02']['upload_name']}`  
SHA-256: `{by['smith_1909_07_02']['sha256']}` ({by['smith_1909_07_02']['size']} bytes).

### 17 September duplicate alias
The newly supplied `{by['smith_1909_09_17']['upload_name']}` is byte-identical to the already preserved `newspapers/oregon-city-courier/1909-09-17-page-5-palace-saloon-ralph-o-smith-license.pdf` (`S-172` / `E-152`), SHA-256 `{by['smith_1909_09_17']['sha256']}`. No duplicate file or ID was created.

### 24 June 1910 — repeat of S-199 / E-178
A newly supplied *Courier* p. 7 scan repeats **E. R. Case's** three-month Palace Saloon application and again prints **510 Main street**, one week after the 17 June page. The second issue confirms repeated printed usage of `510`; because it repeats the same notice, it does not eliminate the possibility of repeated source-copy/address error.

Repository file: `{by['case_1910_06_24']['actual_path']}`  
Original uploaded filename: `{by['case_1910_06_24']['upload_name']}`  
SHA-256: `{by['case_1910_06_24']['sha256']}` ({by['case_1910_06_24']['size']} bytes).

Annual statuses are unchanged.""")
append_once("evidence/source-captures/1910-main-street-research.md", "## 24 June 1910 repeat-notice supplement", """## 24 June 1910 repeat-notice supplement
A newly supplied and visually verified **24 June 1910 Courier p. 7** repeats E. R. Case's three-month Palace Saloon application and again prints **510 Main street** (`S-199` / `E-178`). This confirms the number occurs in two consecutive weekly issue scans (17 and 24 June), rather than being an OCR-only or one-scan reading. Because the 24 June item repeats the same notice, it may also repeat the same underlying source-copy/address error. The archive therefore preserves `510` literally but does not resolve it against the later Palace `501 Main` evidence or Pacific Telephone's later 1910 `510 Main` advertising. The year remains **IN PROGRESS**.""")
append_once("evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md", "## 2 September 2026 duplicate-upload reconciliation", f"""## 2 September 2026 duplicate-upload reconciliation
Two newly supplied steward PDFs were checked by exact SHA-256 and are byte-identical to pages already preserved under `S-150` / `E-135`; no duplicate binary or new ID was created.

- `{by['dollar_1920_02_13']['upload_name']}` → `{by['dollar_1920_02_13']['repo_path']}` — SHA-256 `{by['dollar_1920_02_13']['sha256']}`.
- `{by['leland_1920_06_04']['upload_name']}` → `{by['leland_1920_06_04']['repo_path']}` — SHA-256 `{by['leland_1920_06_04']['sha256']}`.

The historical interpretation above is unchanged: Dollar is block-located only; Leland is direct at 505½ Main; no same-hall succession or construction date is inferred.""")
append_once("buildings/501-main.md", "## June 1910 repeated 510 Palace wording", """## June 1910 repeated 510 Palace wording
The Palace/501 chronology now includes a second issue-page control for the unresolved 1910 number conflict: both **17 and 24 June 1910** *Courier* notices for E. R. Case print **Palace Saloon, 510 Main street** (`S-199` / `E-178`). This strengthens only the fact that `510` was repeatedly printed; it does not place the Palace conclusively in the physical 510 premises or prove a move from/to the later direct **501 Main** Palace anchor. A repeated notice may repeat the same source-copy error.""")
append_once("timelines/501-main.md", "## 2 September 2026 Palace repeat-notice supplement", """## 2 September 2026 Palace repeat-notice supplement
- **25 Jun. and 2 Jul. 1909:** Ralph O. Smith's three-month Palace Saloon application is printed at Fifth/Main (`S-178` / `E-158`); no 501 number or grant.
- **17 and 24 Jun. 1910:** E. R. Case's Palace application prints **510 Main** in two consecutive *Courier* issues (`S-199` / `E-178`); repeated wording does not resolve the conflict with the later direct 501 Palace anchor.""")
append_once("registers/business-timeline.md", "## 2 July 1909 and 24 June 1910 Palace repeat notices", """## 2 July 1909 and 24 June 1910 Palace repeat notices
`S-178` / `E-158` now includes the 2 July 1909 republication of Ralph O. Smith's three-month Palace Saloon, Fifth/Main application. `S-199` / `E-178` now includes the 24 June 1910 republication of E. R. Case's Palace application, again printing **510 Main**. Repeat publication is not treated as a second application, grant or premises transfer; the 1910 510-versus-later-501 conflict remains open.""")
append_once("timeline.md", "## 2 September 2026 — Palace repeat-notice controls", """## 2 September 2026 — Palace repeat-notice controls
A newly preserved **2 July 1909** *Courier* page republishes Ralph O. Smith's three-month liquor-license application at **Palace Saloon, Fifth and Main streets**, first preserved from 25 June (`S-178` / `E-158`). It is not treated as a second application or grant.

A newly preserved **24 June 1910** *Courier* page republishes E. R. Case's three-month Palace application and again prints **510 Main street**, one week after the 17 June notice (`S-199` / `E-178`). Two separate scans therefore carry `510`, but a repeated notice can repeat the same underlying source-copy/address error. The archive continues to preserve the unresolved relationship between this 1910 `510`, Joe Wilson's later direct **501 Main** Palace, and Pacific Telephone's later 1910 use of **510 Main**.""")
append_once("evidence/open-questions.md", "### OQ-032 update — repeated 1909/1910 Palace notices", """### OQ-032 update — repeated 1909/1910 Palace notices
The 2 July 1909 *Courier* repeats Ralph O. Smith's three-month Palace Saloon, Fifth/Main application from 25 June (`S-178` / `E-158`). More significantly, the 24 June 1910 *Courier* repeats E. R. Case's Palace application and again prints **510 Main** (`S-199` / `E-178`). This rules out `510` as an OCR-only or single-scan transcription artifact but does **not** prove 510 was the true physical/legal Palace premises because the repeated notice may reproduce the same source copy. Continue to resolve Smith→Case succession, license grants, and the 510→later-501 / Pacific-Telephone-510 conflict without normalizing the number.""")
append_once("evidence/research-leads.md", "### RL-045 repeat-notice update — 24 June 1910 confirms repeated printed 510", """### RL-045 repeat-notice update — 24 June 1910 confirms repeated printed 510
The 24 June 1910 *Courier* repeats E. R. Case's Palace Saloon application with **510 Main street**, matching the 17 June page (`S-199` / `E-178`). Shift the research question from “was 510 a one-page transcription/OCR anomaly?” to “why was 510 repeatedly printed?” Priority tests remain: Council license application/grant documents, 1909–1911 directories, property/tenancy records, address-numbering records, and advertisements capable of bracketing the transition to Pacific Telephone at 510 by August 1910 and Palace at 501 by March 1912. Do not assume move, typo or renumbering in advance.""")
append_once("indexes/id-crosswalk.md", "## 2 September 2026 Palace / pool-hall upload reconciliation", f"""## 2 September 2026 Palace / pool-hall upload reconciliation
- `S-178` / `E-158` / `P-098` / `BUS-024` — 25 Jun. 1909 Smith Palace Fifth/Main application plus newly preserved 2 Jul. repeat; no second application/grant inferred.
- `S-199` / `E-178` / `P-105` / `BUS-024` — 17 and 24 Jun. 1910 Case Palace notices both print 510 Main; repeated printed number strengthens source wording but does not resolve physical-address conflict.
- `S-172` / `E-152` — newly supplied 17 Sep. 1909 file is an exact duplicate alias of the existing repository PDF; no new ID.
- `S-150` / `E-135` — newly supplied 13 Feb. and 4 Jun. 1920 pool-hall PDFs are exact duplicate aliases of existing repository PDFs; no new IDs.
[Reconciliation record](../evidence/source-captures/1909-1920-palace-poolhall-steward-upload-reconciliation-2026-09-02.md).""")
append_once("ARCHIVE_INDEX.md", "## Steward uploads — 1909–1920 Palace / pool-hall reconciliation", """## Steward uploads — 1909–1920 Palace / pool-hall reconciliation
[Reconciliation audit](evidence/source-captures/1909-1920-palace-poolhall-steward-upload-reconciliation-2026-09-02.md) accounts for five supplied PDFs by exact SHA-256. New exact page files are the **2 Jul. 1909 Ralph O. Smith Palace Saloon Fifth/Main repeat notice** (`S-178` / `E-158`) and **24 Jun. 1910 E. R. Case Palace Saloon repeat notice at printed 510 Main** (`S-199` / `E-178`). The supplied 17 Sep. 1909 Smith page and 13 Feb./4 Jun. 1920 pool-hall pages are byte-identical to existing repository files and were not duplicated. No IDs were renumbered or duplicated; annual status is unchanged.""")

def replace_row_if_present(path, startswith, newrow):
    text = read(path)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(startswith):
            if line != newrow:
                lines[i] = newrow
                write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))
            return
    raise SystemExit(f"Index row not found in {path}: {startswith}")

replace_row_if_present("people/people-index.md", "| P-098 |", "| P-098 | [Ralph O. Smith](profiles/ralph-o-smith.md) | Palace Saloon business-interest purchaser / liquor-license applicant | 25 Jun. 1909 report says Smith bought former partner F. E. Hall's Palace interest; 25 Jun. and 2 Jul. notices print his three-month Palace Saloon, Fifth/Main application; 17 Sep. and 31 Dec. notices continue the dated Palace relationship. Repeat notices are not grants; no exact 501/title or uninterrupted succession is proved. |")
replace_row_if_present("people/people-index.md", "| P-105 |", "| P-105 | [E. R. Case](profiles/e-r-case.md) | Palace Saloon liquor-license applicant / Fifth-Main saloon context | 1 Jun. 1910 Council record places Case's saloon at Fifth/Main; 17 and 24 Jun. Courier notices print Palace Saloon, **510 Main street**, for the same three-month application. Repeated 510 is preserved but does not resolve true physical/legal number, later Palace 501, or later Pacific Telephone 510. |")
replace_row_if_present("businesses/business-index.md", "| BUS-024 |", "| BUS-024 | [Palace Saloon](palace-saloon.md) | Fifth/Main; exact 501 in Mar. 1912; conflicting repeated 510 wording in Jun. 1910 | Operator/license chronology includes Knapp, Surber, Ralph O. Smith, E. R. Case and Joe/Joseph Wilson with explicit gaps. Smith's 25 Jun. application repeats 2 Jul. 1909; Case's 510 Main application repeats 24 Jun. 1910. Repeat notices are not grants or proof of premises/title. |")

capture = f"""# 1909–1920 Palace / pool-hall steward-upload reconciliation

Review date: **2 September 2026**.

Status: **FIVE PROJECT-STEWARD NEWSPAPER PDF UPLOADS VISUALLY REVIEWED AND RECONCILED BY SHA-256.** This targeted integration does not change any annual research status.

## File reconciliation

| Supplied file | SHA-256 / bytes | Repository PDF | Handling | Source/evidence |
| --- | --- | --- | --- | --- |
| `{by['smith_1909_07_02']['upload_name']}` | `{by['smith_1909_07_02']['sha256']}` / {by['smith_1909_07_02']['size']} | `{by['smith_1909_07_02']['actual_path']}` | **{by['smith_1909_07_02']['handling']}** | existing `S-178` / `E-158` |
| `{by['case_1910_06_24']['upload_name']}` | `{by['case_1910_06_24']['sha256']}` / {by['case_1910_06_24']['size']} | `{by['case_1910_06_24']['actual_path']}` | **{by['case_1910_06_24']['handling']}** | existing `S-199` / `E-178` |
| `{by['smith_1909_09_17']['upload_name']}` | `{by['smith_1909_09_17']['sha256']}` / {by['smith_1909_09_17']['size']} | `{by['smith_1909_09_17']['actual_path']}` | **{by['smith_1909_09_17']['handling']}** | existing `S-172` / `E-152` |
| `{by['leland_1920_06_04']['upload_name']}` | `{by['leland_1920_06_04']['sha256']}` / {by['leland_1920_06_04']['size']} | `{by['leland_1920_06_04']['actual_path']}` | **{by['leland_1920_06_04']['handling']}** | existing `S-150` / `E-135` |
| `{by['dollar_1920_02_13']['upload_name']}` | `{by['dollar_1920_02_13']['sha256']}` / {by['dollar_1920_02_13']['size']} | `{by['dollar_1920_02_13']['actual_path']}` | **{by['dollar_1920_02_13']['handling']}** | existing `S-150` / `E-135` |

## Historical integration

### 2 July 1909 — Ralph O. Smith / Palace Saloon
The page prints the same three-month liquor-license application already documented from 25 June: **Ralph O. Smith**, **Palace Saloon, Fifth and Main streets**. This is treated as repeat publication of the same application, not a second application or a grant. No 501 number or title is printed.

### 24 June 1910 — E. R. Case / Palace Saloon / repeated printed 510 Main
The page repeats the application published 17 June and again prints **E. R. Case**, **the Palace Saloon, 510 Main street**, for three months. Two independently scanned weekly issue pages therefore contain `510`. This is stronger evidence for what the newspaper repeatedly printed, but a repeated legal notice can repeat the same source copy; it does **not** establish that 510 was the true physical/legal premises number. The later Palace 501 evidence and later 1910 Pacific Telephone 510 evidence remain an **UNRESOLVED CONFLICT / OPEN TRANSITION QUESTION**.

### 17 September 1909 duplicate
The supplied file is byte-identical to the already preserved `S-172` / `E-152` page. The existing record remains controlling; the new filename is retained here as an upload alias only.

### 13 February and 4 June 1920 duplicates
Both supplied files are byte-identical to the existing `S-150` / `E-135` pages. Historical interpretation is unchanged: **Clem Dollar** is proprietor of a pool hall somewhere on Main between Fifth and Sixth on 13 February; the 4 June report says **A. Leland** was granted permission to operate a pool hall at **505½ Main** and erect an electric street sign. No Dollar→Leland succession, same-hall identity, ownership or construction date is inferred.

## Method / limits

- Claims are based on direct visual inspection of the supplied page images; OCR/search is not substituted for scan review.
- Exact SHA-256 comparison controls duplicate handling.
- Repeat legal notices are not converted into multiple applications or license grants.
- Property ownership, business ownership, operation, license status, address and physical-building identity remain separate questions.
- Existing IDs were reused for repeated/duplicate evidence; **no IDs were renumbered or duplicated**.
- Annual research status remains unchanged.
"""
write("evidence/source-captures/1909-1920-palace-poolhall-steward-upload-reconciliation-2026-09-02.md", capture)

append_once("registers/research-log.md", "## 2 September 2026 — five-file Palace / pool-hall steward upload integration", f"""## 2 September 2026 — five-file Palace / pool-hall steward upload integration
- Refreshed current `main`, reread `AGENTS.md` and `RESEARCH-STANDARD.md`, and reviewed the controlling Palace and 1919–1920 pool-hall checkpoints before changes.
- Reconciled five supplied newspaper PDFs by exact SHA-256.
- Newly preserved `{by['smith_1909_07_02']['actual_path']}` and `{by['case_1910_06_24']['actual_path']}` byte-for-byte against the supplied uploads.
- Confirmed the supplied 17 Sep. 1909 Smith page and 13 Feb./4 Jun. 1920 pool-hall pages are exact duplicates of existing repository files; recorded aliases without duplicating binaries or IDs.
- Extended stable `S-178` / `E-158` with the 2 Jul. 1909 repeat Smith notice and stable `S-199` / `E-178` with the 24 Jun. 1910 repeat Case notice. The repeated 1910 `510 Main` wording is stronger evidence for newspaper wording but remains unresolved as a physical/legal address.
- No annual status changed; no existing ID was renumbered.""")

print("Integration records prepared successfully.")
for item in PAGES:
    print(f"{item['key']}: {item['handling']} -> {item['actual_path']}")
